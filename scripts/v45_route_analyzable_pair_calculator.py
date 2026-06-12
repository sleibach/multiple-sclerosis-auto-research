#!/usr/bin/env python3
"""Calculate analyzable paired subjects for V45 validation routes.

This is planning/intake infrastructure only. It reads sample metadata and counts
baseline/follow-up/label completeness. It does not read expression values,
compute module scores, or run validation.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_route_analyzable_pair_calculator"
SEED = 450124

ROUTES = {
    "gafson_dmf_2018": {
        "subject_fields": ["subject_id", "patient", "patient_id"],
        "timepoint_fields": ["timepoint"],
        "response_fields": ["response", "neda4_status", "neda_status"],
        "baseline_tokens": {"baseline", "bl", "pre", "pretreatment"},
        "followup_tokens": {"week6", "w6", "6w", "6_week", "early", "early_on_treatment"},
        "requires_response": True,
        "role": "primary_V22_V42_validation",
    },
    "karolinska_dmf_ros_2019": {
        "subject_fields": ["subject_id", "patient", "patient_id"],
        "timepoint_fields": ["timepoint"],
        "response_fields": ["response", "beneficial_response"],
        "baseline_tokens": {"baseline", "bl", "pre", "pretreatment"},
        "followup_tokens": {"month6", "m6", "6m", "6_month", "post", "followup"},
        "requires_response": True,
        "role": "secondary_MS_DMF_label_path",
    },
    "gse228330_ocrelizumab_pbmc": {
        "subject_fields": ["subject_id", "subject", "patient", "patient_id"],
        "timepoint_fields": ["timepoint"],
        "response_fields": ["response", "outcome", "neda_status"],
        "baseline_tokens": {"baseline", "bl", "pre", "pretreatment"},
        "followup_tokens": {"week2", "w2", "2w", "2_week", "month6", "m6", "6m", "6_month"},
        "requires_response": False,
        "role": "open_anti_cd20_pharmacodynamic_context_optional_label_request",
    },
}

MISSING_RESPONSE = {"", "nan", "na", "n/a", "missing", "unknown", "not_available"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    calc = sub.add_parser("calculate")
    calc.add_argument("--route", choices=sorted(ROUTES), required=True)
    calc.add_argument("--metadata", type=Path, required=True)
    calc.add_argument("--outdir", type=Path, required=True)
    calc.add_argument("--expect-status", choices=["PASS", "FAIL"], default="PASS")

    syn = sub.add_parser("synthetic-check")
    syn.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def pick_column(columns: list[str], candidates: list[str]) -> str:
    lower = {col.lower(): col for col in columns}
    for candidate in candidates:
        if candidate.lower() in lower:
            return lower[candidate.lower()]
    return ""


def normalize(value: object) -> str:
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


def decision_band(min_group_n: int, response_ready: bool, route: str) -> str:
    if not response_ready:
        return "context_only_or_labels_needed"
    if min_group_n >= 60:
        return "preferred_decision_planning_range"
    if min_group_n >= 30:
        return "minimum_decision_grade_only_if_large_clean_effect"
    if min_group_n >= 10:
        return "effect_size_ci_information_likely_inconclusive"
    return "below_v45_planning_floor"


def calculate(route: str, metadata_path: Path, outdir: Path, expect_status: str, synthetic: bool = False, case: str = "none") -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    cfg = ROUTES[route]
    md = pd.read_csv(metadata_path, sep="\t").fillna("")
    subject_col = pick_column(list(md.columns), cfg["subject_fields"])
    timepoint_col = pick_column(list(md.columns), cfg["timepoint_fields"])
    response_col = pick_column(list(md.columns), cfg["response_fields"])
    issues: list[dict[str, object]] = []

    for name, col in [("subject", subject_col), ("timepoint", timepoint_col)]:
        if not col:
            issues.append({"severity": "hard", "check": f"missing_{name}_column", "detail": f"no {name} column found"})
    if cfg["requires_response"] and not response_col:
        issues.append({"severity": "hard", "check": "missing_response_column", "detail": "route requires response labels"})

    rows: list[dict[str, object]] = []
    response_counts: dict[str, int] = {}
    if not issues:
        work = md.copy()
        work["_subject"] = work[subject_col].map(normalize)
        work["_timepoint"] = work[timepoint_col].map(normalize)
        work["_response"] = work[response_col].map(normalize) if response_col else ""
        for subject, group in work.groupby("_subject"):
            has_baseline = bool(set(group["_timepoint"]) & cfg["baseline_tokens"])
            has_followup = bool(set(group["_timepoint"]) & cfg["followup_tokens"])
            responses = sorted(set(group["_response"]) - MISSING_RESPONSE) if response_col else []
            response_value = responses[0] if len(responses) == 1 else ("conflict" if len(responses) > 1 else "")
            if response_value and response_value != "conflict":
                response_counts[response_value] = response_counts.get(response_value, 0) + (1 if has_baseline and has_followup else 0)
            rows.append(
                {
                    "subject": subject,
                    "has_baseline": str(has_baseline).lower(),
                    "has_followup": str(has_followup).lower(),
                    "has_response": str(bool(response_value and response_value != "conflict")).lower(),
                    "response": response_value,
                    "analyzable_pair": str(has_baseline and has_followup).lower(),
                    "analyzable_response_pair": str(has_baseline and has_followup and bool(response_value and response_value != "conflict")).lower(),
                }
            )
    subject_path = outdir / "subject_pair_completeness.tsv"
    write_tsv(
        subject_path,
        rows,
        ["subject", "has_baseline", "has_followup", "has_response", "response", "analyzable_pair", "analyzable_response_pair"],
    )
    issues_path = outdir / "analyzable_pair_issues.tsv"
    write_tsv(issues_path, issues, ["severity", "check", "detail"])

    analyzable_pairs = sum(1 for row in rows if row["analyzable_pair"] == "true")
    analyzable_response_pairs = sum(1 for row in rows if row["analyzable_response_pair"] == "true")
    response_ready = (not cfg["requires_response"] and response_col == "") or analyzable_response_pairs > 0
    if cfg["requires_response"]:
        response_ready = len(response_counts) >= 2
    min_group_n = min(response_counts.values()) if response_counts else 0
    hard = sum(1 for row in issues if row["severity"] == "hard")
    observed = "FAIL" if hard else "PASS"
    summary = {
        "synthetic": synthetic,
        "synthetic_case": case,
        "seed": SEED if synthetic else "",
        "purpose": "V45 route analyzable-pair calculator; no biological claim",
        "route": route,
        "role": cfg["role"],
        "metadata": rel(metadata_path),
        "subject_table": rel(subject_path),
        "issues": rel(issues_path),
        "n_subjects": len(rows),
        "n_analyzable_pairs": analyzable_pairs,
        "n_analyzable_response_pairs": analyzable_response_pairs,
        "response_group_counts": response_counts,
        "min_response_group_n": min_group_n,
        "decision_band": decision_band(min_group_n, response_ready, route),
        "observed_status": observed,
        "expected_status": expect_status,
        "expectation_met": observed == expect_status,
    }
    (outdir / "analyzable_pair_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["expectation_met"] else 2


def route_metadata(route: str, n_per_group: int, missing_followup: int = 0, missing_response: int = 0) -> pd.DataFrame:
    cfg = ROUTES[route]
    response_values = ["responder", "nonresponder"]
    rows = []
    subject_idx = 0
    for response in response_values:
        for i in range(n_per_group):
            subject_idx += 1
            subject = f"S{subject_idx:03d}"
            timepoints = ["baseline", next(iter(sorted(cfg["followup_tokens"])))]
            for tp in timepoints:
                if tp != "baseline" and missing_followup > 0:
                    missing_followup -= 1
                    continue
                label = response
                if missing_response > 0:
                    label = ""
                    missing_response -= 1
                rows.append(
                    {
                        "sample_id": f"{subject}_{tp}",
                        "subject_id": subject,
                        "timepoint": tp,
                        "response": label,
                        "beneficial_response": label,
                        "batch": "b1" if subject_idx % 2 else "b2",
                    }
                )
    return pd.DataFrame(rows)


def synthetic_check(outdir: Path) -> int:
    outdir = resolve(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    synthetic_dir = outdir / "synthetic"
    synthetic_dir.mkdir(parents=True)
    cases = [
        ("gafson_small_complete", "gafson_dmf_2018", route_metadata("gafson_dmf_2018", 12), "PASS"),
        ("gafson_partial_return", "gafson_dmf_2018", route_metadata("gafson_dmf_2018", 12, missing_followup=6, missing_response=4), "PASS"),
        ("karolinska_small_secondary", "karolinska_dmf_ros_2019", route_metadata("karolinska_dmf_ros_2019", 7), "PASS"),
        ("gse228330_context_no_labels", "gse228330_ocrelizumab_pbmc", route_metadata("gse228330_ocrelizumab_pbmc", 10, missing_response=40), "PASS"),
    ]
    case_rows = []
    exit_codes = []
    for case, route, table, expected in cases:
        metadata_path = synthetic_dir / f"{case}_metadata.tsv"
        table.to_csv(metadata_path, sep="\t", index=False)
        case_out = outdir / case
        rc = calculate(route, metadata_path, case_out, expected, synthetic=True, case=case)
        exit_codes.append(rc)
        summary = json.loads((case_out / "analyzable_pair_summary.json").read_text())
        case_rows.append(
            {
                "case": case,
                "route": route,
                "n_subjects": summary["n_subjects"],
                "n_analyzable_pairs": summary["n_analyzable_pairs"],
                "n_analyzable_response_pairs": summary["n_analyzable_response_pairs"],
                "min_response_group_n": summary["min_response_group_n"],
                "decision_band": summary["decision_band"],
                "summary": rel(case_out / "analyzable_pair_summary.json"),
            }
        )
    write_tsv(
        outdir / "route_analyzable_pair_synthetic_cases.tsv",
        case_rows,
        [
            "case",
            "route",
            "n_subjects",
            "n_analyzable_pairs",
            "n_analyzable_response_pairs",
            "min_response_group_n",
            "decision_band",
            "summary",
        ],
    )
    summary = {
        "synthetic": True,
        "seed": SEED,
        "purpose": "V45 route analyzable-pair synthetic planning cases; no biological claim",
        "n_cases": len(case_rows),
        "n_expectation_failures": sum(1 for code in exit_codes if code != 0),
        "case_table": rel(outdir / "route_analyzable_pair_synthetic_cases.tsv"),
    }
    (outdir / "route_analyzable_pair_synthetic_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return 0 if summary["n_expectation_failures"] == 0 else 2


def main() -> int:
    args = parse_args()
    if args.cmd == "calculate":
        return calculate(args.route, resolve(args.metadata), resolve(args.outdir), args.expect_status)
    return synthetic_check(resolve(args.outdir))


if __name__ == "__main__":
    raise SystemExit(main())
