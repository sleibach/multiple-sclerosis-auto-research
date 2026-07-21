#!/usr/bin/env python3
"""Adjudicate synthetic CDP/PIRA fixtures under an explicitly frozen protocol."""

from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "analysis/v54_progression_endpoint_adjudication"
REQUIRED_COLUMNS = [
    "subject_id",
    "day",
    "edss",
    "t25fw",
    "relapse",
    "steroid",
    "treatment_switch",
    "death",
    "dropout",
    "synthetic",
]
TERMINAL_COLUMNS = ["treatment_switch", "death", "dropout"]
VALID_ENDPOINTS = {"cdp", "pira"}


def yes(value: Any) -> bool:
    return str(value).strip().lower() == "yes"


def frozen_synthetic_protocol(endpoint_type: str = "pira") -> dict[str, Any]:
    return {
        "synthetic": True,
        "protocol_id": "SYNTHETIC_V54_CDP_PIRA_FIXTURE_PROTOCOL",
        "endpoint_type": endpoint_type,
        "baseline_day": 0,
        "components": {
            "edss": {"scale": "absolute", "threshold": 1.0},
            "t25fw": {"scale": "relative", "threshold": 0.20},
        },
        "component_rule": "all_components",
        "confirmation_min_days": 180,
        "confirmation_max_days": 240,
        "pira_relapse_window_before_days": 90,
        "pira_relapse_window_after_days": 30,
        "pira_steroid_window_before_days": 30,
        "pira_steroid_window_after_days": 30,
        "terminal_censoring_fields": TERMINAL_COLUMNS,
        "boundary": "Synthetic endpoint-processing protocol only; not a clinical recommendation or biological claim.",
    }


def component_crosses(row: pd.Series, baseline: pd.Series, protocol: dict[str, Any]) -> bool:
    results = []
    for component, rule in protocol["components"].items():
        value = float(row[component])
        base = float(baseline[component])
        if rule["scale"] == "absolute":
            results.append(value - base >= float(rule["threshold"]))
        elif rule["scale"] == "relative":
            if base <= 0:
                return False
            results.append((value - base) / base >= float(rule["threshold"]))
        else:
            raise ValueError(f"Unknown component scale: {rule['scale']}")
    if protocol["component_rule"] != "all_components":
        raise ValueError("Only the frozen all_components rule is implemented")
    return bool(all(results))


def any_flag_in_window(frame: pd.DataFrame, field: str, start: int, end: int) -> bool:
    selected = frame.loc[frame.day.between(start, end, inclusive="both")]
    return bool(selected[field].map(yes).any())


def adjudicate_subject(frame: pd.DataFrame, protocol: dict[str, Any]) -> dict[str, Any]:
    subject = str(frame.subject_id.iloc[0]) if len(frame) else ""
    endpoint = str(protocol.get("endpoint_type", "")).lower()
    if endpoint not in VALID_ENDPOINTS:
        return {"subject_id": subject, "status": "INVALID_INPUT", "reason": "unknown_endpoint"}
    if protocol.get("synthetic") is not True:
        return {"subject_id": subject, "status": "INVALID_INPUT", "reason": "protocol_not_marked_synthetic"}
    if not bool(frame.synthetic.map(yes).all()):
        return {"subject_id": subject, "status": "INVALID_INPUT", "reason": "fixture_not_marked_synthetic"}
    if frame.day.duplicated().any():
        return {"subject_id": subject, "status": "INVALID_INPUT", "reason": "duplicate_assessment_day"}
    baseline_rows = frame.loc[frame.day.eq(int(protocol["baseline_day"]))]
    if len(baseline_rows) != 1:
        return {"subject_id": subject, "status": "INVALID_INPUT", "reason": "baseline_missing_or_duplicate"}
    baseline = baseline_rows.iloc[0]
    for component in protocol["components"]:
        if pd.isna(baseline[component]):
            return {"subject_id": subject, "status": "INVALID_INPUT", "reason": f"baseline_{component}_missing"}

    frame = frame.sort_values("day").reset_index(drop=True)
    terminal_rows = frame.loc[frame[TERMINAL_COLUMNS].apply(lambda column: column.map(yes)).any(axis=1)]
    terminal_day = int(terminal_rows.day.min()) if len(terminal_rows) else np.inf
    candidate_rows = frame.loc[(frame.day > protocol["baseline_day"]) & (frame.day < terminal_day)]
    candidate_rows = candidate_rows.loc[
        candidate_rows.apply(lambda row: component_crosses(row, baseline, protocol), axis=1)
    ]
    if candidate_rows.empty:
        return {
            "subject_id": subject,
            "endpoint_type": endpoint,
            "status": "NO_EVENT_THRESHOLD_NOT_MET",
            "reason": "no_assessment_crosses_all_frozen_components",
        }

    seen_context_excluded = False
    seen_transient = False
    seen_missing = False
    seen_censored = False
    for candidate in candidate_rows.itertuples(index=False):
        onset = int(candidate.day)
        confirmation_start = onset + int(protocol["confirmation_min_days"])
        confirmation_end = onset + int(protocol["confirmation_max_days"])
        if endpoint == "pira":
            relapse = any_flag_in_window(
                frame,
                "relapse",
                onset - int(protocol["pira_relapse_window_before_days"]),
                onset + int(protocol["pira_relapse_window_after_days"]),
            )
            steroid = any_flag_in_window(
                frame,
                "steroid",
                onset - int(protocol["pira_steroid_window_before_days"]),
                onset + int(protocol["pira_steroid_window_after_days"]),
            )
            if relapse or steroid:
                seen_context_excluded = True
                continue

        if terminal_day < confirmation_start:
            seen_censored = True
            continue
        confirmations = frame.loc[
            frame.day.between(confirmation_start, confirmation_end, inclusive="both")
            & (frame.day < terminal_day)
        ]
        if confirmations.empty:
            seen_missing = True
            continue
        confirmed = confirmations.apply(
            lambda row: component_crosses(row, baseline, protocol), axis=1
        )
        if confirmed.any():
            confirmation = confirmations.loc[confirmed].iloc[0]
            return {
                "subject_id": subject,
                "endpoint_type": endpoint,
                "status": "CONFIRMED_EVENT",
                "reason": "all_frozen_components_confirmed_in_window",
                "onset_day": onset,
                "confirmation_day": int(confirmation.day),
            }
        seen_transient = True

    if seen_censored:
        status = "INCONCLUSIVE_CENSORED_BEFORE_CONFIRMATION"
        reason = "terminal_event_precedes_valid_confirmation"
    elif seen_missing:
        status = "INCONCLUSIVE_MISSING_CONFIRMATION"
        reason = "no_assessment_in_frozen_confirmation_window"
    elif seen_context_excluded:
        status = "NO_PIRA_EVENT_CONTEXT_EXCLUDED"
        reason = "confirmed-threshold candidate overlaps relapse_or_steroid_window"
    elif seen_transient:
        status = "NO_EVENT_TRANSIENT_OR_COMPONENT_DISCORDANT"
        reason = "in_window_assessment_does_not_confirm_all_components"
    else:
        status = "NO_EVENT_THRESHOLD_NOT_MET"
        reason = "no_eligible_candidate_remains"
    return {"subject_id": subject, "endpoint_type": endpoint, "status": status, "reason": reason}


def adjudicate_file(data_path: Path, protocol_path: Path, output_dir: Path) -> dict[str, Any]:
    frame = pd.read_csv(data_path, sep="\t", dtype=str, keep_default_na=False)
    missing = sorted(set(REQUIRED_COLUMNS) - set(frame.columns))
    if missing:
        raise RuntimeError(f"Input missing required columns: {missing}")
    frame["day"] = pd.to_numeric(frame.day, errors="raise").astype(int)
    for component in ("edss", "t25fw"):
        frame[component] = pd.to_numeric(frame[component], errors="coerce")
    protocol = json.loads(protocol_path.read_text())
    rows = [
        adjudicate_subject(group.copy(), protocol)
        for _, group in frame.groupby("subject_id", sort=True)
    ]
    output_dir.mkdir(parents=True, exist_ok=True)
    decisions = pd.DataFrame(rows)
    decisions.to_csv(output_dir / "adjudication.tsv", sep="\t", index=False)
    summary = {
        "purpose": "V54 synthetic CDP/PIRA endpoint adjudication behavior; no biological claim",
        "synthetic": bool(frame.synthetic.map(yes).all() and protocol.get("synthetic") is True),
        "endpoint_type": protocol.get("endpoint_type"),
        "n_subjects": len(decisions),
        "status_counts": decisions.status.value_counts().sort_index().to_dict(),
        "boundary": "Endpoint-processing behavior only; no patient data, clinical recommendation, or biological evidence.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return {"summary": summary, "decisions": decisions}


def row(day: int, edss: str, t25fw: str, **flags: str) -> dict[str, str]:
    result = {
        "subject_id": "SYNTHETIC_SUBJECT",
        "day": str(day),
        "edss": edss,
        "t25fw": t25fw,
        "relapse": "no",
        "steroid": "no",
        "treatment_switch": "no",
        "death": "no",
        "dropout": "no",
        "synthetic": "yes",
    }
    result.update(flags)
    return result


def base_rows() -> list[dict[str, str]]:
    return [row(0, "2.0", "10.0"), row(30, "3.0", "12.0"), row(210, "3.0", "12.0")]


def synthetic_regression(output_dir: Path) -> dict[str, Any]:
    cases: list[tuple[str, str, list[dict[str, str]], str]] = []
    cases.append(("confirmed_clean_pira", "pira", base_rows(), "CONFIRMED_EVENT"))

    transient = base_rows()
    transient[-1] = row(210, "2.0", "10.0")
    cases.append(("transient_worsening", "pira", transient, "NO_EVENT_TRANSIENT_OR_COMPONENT_DISCORDANT"))

    missing = [row(0, "2.0", "10.0"), row(30, "3.0", "12.0"), row(300, "3.0", "12.0")]
    cases.append(("missing_confirmation", "pira", missing, "INCONCLUSIVE_MISSING_CONFIRMATION"))

    too_early = [row(0, "2.0", "10.0"), row(30, "3.0", "12.0"), row(180, "3.0", "12.0")]
    cases.append(("confirmation_too_early", "pira", too_early, "INCONCLUSIVE_MISSING_CONFIRMATION"))

    relapse = base_rows() + [
        row(20, "2.0", "10.0", relapse="yes"),
        row(200, "2.0", "10.0", relapse="yes"),
    ]
    cases.append(("relapse_overlap_pira", "pira", relapse, "NO_PIRA_EVENT_CONTEXT_EXCLUDED"))
    cases.append(("relapse_overlap_cdp", "cdp", relapse, "CONFIRMED_EVENT"))

    steroid = base_rows() + [
        row(25, "2.0", "10.0", steroid="yes"),
        row(200, "2.0", "10.0", steroid="yes"),
    ]
    cases.append(("steroid_overlap_pira", "pira", steroid, "NO_PIRA_EVENT_CONTEXT_EXCLUDED"))

    onset_discordant = [row(0, "2.0", "10.0"), row(30, "3.0", "11.0"), row(210, "3.0", "11.0")]
    cases.append(("component_disagreement_onset", "pira", onset_discordant, "NO_EVENT_THRESHOLD_NOT_MET"))

    confirm_discordant = base_rows()
    confirm_discordant[-1] = row(210, "3.0", "11.0")
    cases.append(("component_disagreement_confirmation", "pira", confirm_discordant, "NO_EVENT_TRANSIENT_OR_COMPONENT_DISCORDANT"))

    switched = base_rows() + [row(100, "3.0", "12.0", treatment_switch="yes")]
    cases.append(("switch_before_confirmation", "pira", switched, "INCONCLUSIVE_CENSORED_BEFORE_CONFIRMATION"))

    no_baseline = [row(30, "3.0", "12.0"), row(210, "3.0", "12.0")]
    cases.append(("missing_baseline", "pira", no_baseline, "INVALID_INPUT"))

    fixture_dir = output_dir / "synthetic"
    protocol_dir = output_dir / "protocols"
    rows_out = []
    for name, endpoint, fixture_rows, expected in cases:
        data_path = fixture_dir / f"{name}.tsv"
        protocol_path = protocol_dir / f"{endpoint}.json"
        data_path.parent.mkdir(parents=True, exist_ok=True)
        protocol_path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(fixture_rows, columns=REQUIRED_COLUMNS).to_csv(data_path, sep="\t", index=False)
        protocol_path.write_text(json.dumps(frozen_synthetic_protocol(endpoint), indent=2) + "\n")
        result = adjudicate_file(data_path, protocol_path, output_dir / "runs" / name)
        observed = str(result["decisions"].iloc[0].status)
        rows_out.append(
            {
                "fixture": name,
                "synthetic": True,
                "endpoint_type": endpoint,
                "expected_status": expected,
                "observed_status": observed,
                "regression_pass": observed == expected,
            }
        )
    results = pd.DataFrame(rows_out)
    results.to_csv(output_dir / "synthetic_regression.tsv", sep="\t", index=False)
    passed = bool(results.regression_pass.all())
    summary = {
        "purpose": "Synthetic regression of V54 CDP/PIRA adjudication edge cases",
        "synthetic": True,
        "n_fixtures": len(results),
        "n_pass": int(results.regression_pass.sum()),
        "overall_status": "PASS" if passed else "FAIL",
        "boundary": "Synthetic endpoint-processing behavior only; not patient data or biological evidence.",
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if not passed:
        raise RuntimeError("V54 progression endpoint adjudication regression failed")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path)
    parser.add_argument("--protocol", type=Path)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    if bool(args.data) != bool(args.protocol):
        raise SystemExit("--data and --protocol must be supplied together")
    if args.data:
        result = adjudicate_file(args.data, args.protocol, args.output_dir)
        print(json.dumps(result["summary"], indent=2))
    else:
        print(json.dumps(synthetic_regression(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
