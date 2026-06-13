#!/usr/bin/env python3
"""Classify the safe interpretation level for returned validation packages.

This is validation-readiness infrastructure only. It composes pre-score gates
and cohort-structure summaries into safe interpretation language. It does not
read validation score values, locked-rule metrics, expression matrices, raw
labels, or private data.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from copy import deepcopy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_returned_package_safe_interpretation"

GOOD_GATE = ROOT / "analysis/v45_author_run_return_gate_runner/complete_pass/author_run_return_gate_summary.json"
REDACTION_FAIL_GATE = ROOT / "analysis/v45_author_run_return_gate_runner/risky_redaction_fail/author_run_return_gate_summary.json"
COMPLETENESS_FAIL_GATE = ROOT / "analysis/v45_author_run_return_gate_runner/incomplete_completeness_fail/author_run_return_gate_summary.json"
GOOD_SCHEMA = ROOT / "analysis/v45_author_run_schema_validator/good/author_run_schema_validation_summary.json"
BAD_SCHEMA = ROOT / "analysis/v45_author_run_schema_validator/bad_metrics/author_run_schema_validation_summary.json"
SMALL_PAIR = ROOT / "analysis/v45_route_analyzable_pair_calculator/gafson_small_complete/analyzable_pair_summary.json"
CONTEXT_ONLY_PAIR = ROOT / "analysis/v45_route_analyzable_pair_calculator/gse228330_context_no_labels/analyzable_pair_summary.json"
METADATA_CLEAN = ROOT / "analysis/v45_metadata_contradiction_stress/clean_pass/metadata_contradiction_summary.json"
METADATA_FAIL = ROOT / "analysis/v45_metadata_contradiction_stress/batch_conflict_fail/metadata_contradiction_summary.json"


SAFE_LANGUAGE = {
    "BLOCKED_TERMS_OR_RECEIPT_GATES": {
        "allowed": "Report only that package terms or receipt gates block interpretation; request corrected terms/status evidence.",
        "forbidden": "Do not inspect or interpret returned validation scores.",
    },
    "BLOCKED_REDACTION": {
        "allowed": "Report only that redaction failed; request an aggregate-only redacted return package.",
        "forbidden": "Do not run completeness, schema, scoring, or outcome interpretation on the package.",
    },
    "BLOCKED_COMPLETENESS": {
        "allowed": "Report only the missing aggregate-output classes and request a complete return.",
        "forbidden": "Do not interpret partial returned metrics or fill missing fields by assumption.",
    },
    "BLOCKED_RETURN_GATE": {
        "allowed": "Report only that the combined return gate failed and use the gate step table for repair.",
        "forbidden": "Do not interpret any returned result.",
    },
    "BLOCKED_SCHEMA": {
        "allowed": "Report only schema/value-level failures and request repaired aggregate tables.",
        "forbidden": "Do not classify pass/fail/inconclusive from malformed aggregate outputs.",
    },
    "BLOCKED_METADATA_CONTRADICTION": {
        "allowed": "Report only the metadata contradiction and request corrected metadata before interpretation.",
        "forbidden": "Do not treat the returned package as validation-ready.",
    },
    "CONTEXT_ONLY_OR_LABELS_NEEDED": {
        "allowed": "Use only as pharmacodynamic/context evidence; request response labels before validation interpretation.",
        "forbidden": "Do not call this a response-validation result.",
    },
    "BELOW_V45_PLANNING_FLOOR": {
        "allowed": "Report that analyzable labeled pairs are below the V45 planning floor; use only for logistics and future design.",
        "forbidden": "Do not call pass, fail, or inconclusive based on the returned score.",
    },
    "INCONCLUSIVE_SMALL_COHORT": {
        "allowed": "Report only pre-registered effect-size-with-CI language; expect an inconclusive validation unless the frozen grid is cleanly met.",
        "forbidden": "Do not over-read a favorable or unfavorable score from a small cohort.",
    },
    "MINIMUM_DECISION_GRADE_CAUTION": {
        "allowed": "Apply the V42 grid, but state that decision-grade interpretation requires a large clean effect and clean diagnostics.",
        "forbidden": "Do not broaden conclusions beyond the pre-registered route and endpoint.",
    },
    "CAUTION_BATCH_OR_CONFOUNDER": {
        "allowed": "Apply the V42 grid only with explicit batch/confounder caution and report adjusted diagnostics beside raw results.",
        "forbidden": "Do not present a clean validation claim without the diagnostic caveat.",
    },
    "ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION": {
        "allowed": "Interpret mechanically under the frozen V42 grid and V45/V46 diagnostics, with no tuning or extra analyses.",
        "forbidden": "Do not add post-hoc thresholds, modules, timepoints, or unplanned analyses.",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    classify = sub.add_parser("classify")
    classify.add_argument("--gate-summary", type=Path, required=True)
    classify.add_argument("--schema-summary", type=Path, required=True)
    classify.add_argument("--analyzable-summary", type=Path, required=True)
    classify.add_argument("--metadata-summary", type=Path)
    classify.add_argument("--batch-confounder-summary", type=Path)
    classify.add_argument("--terms-status", choices=["PASS", "FAIL", "UNKNOWN"], default="PASS")
    classify.add_argument("--outdir", type=Path, required=True)
    classify.add_argument("--expect-class")

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


def read_json(path: Path | None) -> dict[str, object]:
    if path is None:
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def norm(value: object) -> str:
    return str(value or "").strip().upper()


def add_signal(rows: list[dict[str, object]], source: str, signal: str, status: str, detail: object) -> None:
    rows.append(
        {
            "source": source,
            "signal": signal,
            "status": status,
            "detail": detail,
            "score_values_read": "false",
        }
    )


def warning_from_summary(summary: dict[str, object]) -> tuple[bool, str]:
    if not summary:
        return False, "not provided"
    bad_tokens = {"FAIL", "WARN", "CAUTION", "ATTENUATES", "EXPLAINED_AWAY", "BLOCKED"}
    details: list[str] = []
    for key in ["overall_status", "observed_status", "batch_status", "confounder_status", "verdict", "diagnostic_status"]:
        value = norm(summary.get(key))
        if value:
            details.append(f"{key}={value}")
            if value in bad_tokens:
                return True, "; ".join(details)
    for key in ["n_warn", "n_warning", "n_warnings", "n_hard_issues", "n_fail"]:
        try:
            count = int(summary.get(key, 0))
        except Exception:
            count = 0
        if count > 0:
            details.append(f"{key}={count}")
            return True, "; ".join(details)
    warnings = summary.get("warnings")
    if isinstance(warnings, list) and warnings:
        details.append(f"warnings={len(warnings)}")
        return True, "; ".join(details)
    return False, "; ".join(details) if details else "no warning fields"


def pair_class(pair: dict[str, object]) -> str:
    band = str(pair.get("decision_band", "")).strip().lower()
    if band == "context_only_or_labels_needed":
        return "CONTEXT_ONLY_OR_LABELS_NEEDED"
    if band == "below_v45_planning_floor":
        return "BELOW_V45_PLANNING_FLOOR"
    if band == "effect_size_ci_information_likely_inconclusive":
        return "INCONCLUSIVE_SMALL_COHORT"
    if band == "minimum_decision_grade_only_if_large_clean_effect":
        return "MINIMUM_DECISION_GRADE_CAUTION"
    if band == "preferred_decision_planning_range":
        return "ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION"
    return "BELOW_V45_PLANNING_FLOOR"


def classify_package(
    gate_summary: Path,
    schema_summary: Path,
    analyzable_summary: Path,
    metadata_summary: Path | None,
    batch_confounder_summary: Path | None,
    terms_status: str,
    outdir: Path,
    expect_class: str | None,
) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    gate = read_json(gate_summary)
    schema = read_json(schema_summary)
    pair = read_json(analyzable_summary)
    metadata = read_json(metadata_summary)
    batch_confounder = read_json(batch_confounder_summary)
    signals: list[dict[str, object]] = []

    add_signal(signals, rel(gate_summary), "terms_status", terms_status, "operator/data-use status supplied before interpretation")
    if terms_status != "PASS":
        result_class = "BLOCKED_TERMS_OR_RECEIPT_GATES"
    else:
        add_signal(signals, rel(gate_summary), "redaction_status", norm(gate.get("redaction_status")), "must pass before any other interpretation")
        add_signal(signals, rel(gate_summary), "completeness_status", norm(gate.get("completeness_status")), "minimum aggregate outputs must be present")
        add_signal(signals, rel(gate_summary), "return_gate_overall", norm(gate.get("overall_status")), "combined return gate")
        if norm(gate.get("redaction_status")) != "PASS":
            result_class = "BLOCKED_REDACTION"
        elif norm(gate.get("completeness_status")) != "PASS":
            result_class = "BLOCKED_COMPLETENESS"
        elif norm(gate.get("overall_status")) != "PASS":
            result_class = "BLOCKED_RETURN_GATE"
        else:
            add_signal(signals, rel(schema_summary), "schema_status", norm(schema.get("overall_status")), "aggregate value schema must pass before interpretation")
            if norm(schema.get("overall_status")) != "PASS":
                result_class = "BLOCKED_SCHEMA"
            else:
                if metadata_summary:
                    add_signal(signals, rel(metadata_summary), "metadata_status", norm(metadata.get("observed_status") or metadata.get("overall_status")), "metadata contradictions must be absent")
                if metadata_summary and norm(metadata.get("observed_status") or metadata.get("overall_status")) == "FAIL":
                    result_class = "BLOCKED_METADATA_CONTRADICTION"
                else:
                    band = str(pair.get("decision_band", "missing"))
                    add_signal(signals, rel(analyzable_summary), "decision_band", band, "pre-score analyzable-pair planning band")
                    add_signal(signals, rel(analyzable_summary), "min_response_group_n", str(pair.get("min_response_group_n", "")), "cohort-size signal only; no score values read")
                    result_class = pair_class(pair)
                    warn, detail = warning_from_summary(batch_confounder)
                    if batch_confounder_summary:
                        add_signal(signals, rel(batch_confounder_summary), "batch_or_confounder_warning", "WARN" if warn else "PASS", detail)
                    if warn and result_class in {"ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION", "MINIMUM_DECISION_GRADE_CAUTION"}:
                        result_class = "CAUTION_BATCH_OR_CONFOUNDER"

    language = SAFE_LANGUAGE[result_class]
    synthetic_sources = [
        bool(data.get("synthetic"))
        for data in [gate, schema, pair, metadata, batch_confounder]
        if isinstance(data, dict)
    ]
    summary = {
        "synthetic": "synthetic" in str(outdir).lower() or any(synthetic_sources),
        "purpose": "V46 returned-package safe-interpretation classifier; no biological claim and no score values read",
        "score_values_read": False,
        "result_class": result_class,
        "safe_interpretation": language["allowed"],
        "forbidden_interpretation": language["forbidden"],
        "expect_class": expect_class or "",
        "expectation_met": (not expect_class) or result_class == expect_class,
        "signals": rel(outdir / "safe_interpretation_signals.tsv"),
        "sources": {
            "gate_summary": rel(gate_summary),
            "schema_summary": rel(schema_summary),
            "analyzable_summary": rel(analyzable_summary),
            "metadata_summary": rel(metadata_summary) if metadata_summary else "",
            "batch_confounder_summary": rel(batch_confounder_summary) if batch_confounder_summary else "",
        },
    }
    write_tsv(outdir / "safe_interpretation_signals.tsv", signals, ["source", "signal", "status", "detail", "score_values_read"])
    (outdir / "safe_interpretation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["expectation_met"] else 2


def write_json(path: Path, data: dict[str, object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    return path


def make_pair(summary_path: Path, outdir: Path, name: str, band: str, min_group_n: int) -> Path:
    data = deepcopy(read_json(summary_path))
    data["synthetic"] = True
    data["synthetic_case"] = name
    data["decision_band"] = band
    data["min_response_group_n"] = min_group_n
    data["n_analyzable_response_pairs"] = min_group_n * 2 if min_group_n else data.get("n_analyzable_response_pairs", 0)
    data["response_group_counts"] = {"responder": min_group_n, "nonresponder": min_group_n} if min_group_n else {}
    return write_json(outdir / "synthetic" / f"{name}_pair_summary.json", data)


def synthetic_check(outdir: Path) -> int:
    outdir = resolve(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    syn = outdir / "synthetic"
    preferred_pair = make_pair(SMALL_PAIR, outdir, "preferred", "preferred_decision_planning_range", 60)
    minimum_pair = make_pair(SMALL_PAIR, outdir, "minimum", "minimum_decision_grade_only_if_large_clean_effect", 30)
    below_pair = make_pair(SMALL_PAIR, outdir, "below_floor", "below_v45_planning_floor", 4)
    warning_summary = write_json(
        syn / "batch_confounder_warning.json",
        {
            "synthetic": True,
            "purpose": "synthetic warning fixture for V46 safe-interpretation classifier; no biological claim",
            "overall_status": "WARN",
            "warnings": ["response-correlated batch or confounder diagnostic requires caveated interpretation"],
        },
    )
    clean_warning = write_json(
        syn / "batch_confounder_clean.json",
        {
            "synthetic": True,
            "purpose": "synthetic clean diagnostic fixture for V46 safe-interpretation classifier; no biological claim",
            "overall_status": "PASS",
        },
    )
    cases = [
        ("eligible_preferred_clean", GOOD_GATE, GOOD_SCHEMA, preferred_pair, METADATA_CLEAN, clean_warning, "PASS", "ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION"),
        ("small_clean", GOOD_GATE, GOOD_SCHEMA, SMALL_PAIR, METADATA_CLEAN, clean_warning, "PASS", "INCONCLUSIVE_SMALL_COHORT"),
        ("minimum_clean", GOOD_GATE, GOOD_SCHEMA, minimum_pair, METADATA_CLEAN, clean_warning, "PASS", "MINIMUM_DECISION_GRADE_CAUTION"),
        ("below_floor", GOOD_GATE, GOOD_SCHEMA, below_pair, METADATA_CLEAN, clean_warning, "PASS", "BELOW_V45_PLANNING_FLOOR"),
        ("context_only", GOOD_GATE, GOOD_SCHEMA, CONTEXT_ONLY_PAIR, METADATA_CLEAN, clean_warning, "PASS", "CONTEXT_ONLY_OR_LABELS_NEEDED"),
        ("terms_block", GOOD_GATE, GOOD_SCHEMA, preferred_pair, METADATA_CLEAN, clean_warning, "FAIL", "BLOCKED_TERMS_OR_RECEIPT_GATES"),
        ("redaction_block", REDACTION_FAIL_GATE, GOOD_SCHEMA, preferred_pair, METADATA_CLEAN, clean_warning, "PASS", "BLOCKED_REDACTION"),
        ("completeness_block", COMPLETENESS_FAIL_GATE, GOOD_SCHEMA, preferred_pair, METADATA_CLEAN, clean_warning, "PASS", "BLOCKED_COMPLETENESS"),
        ("schema_block", GOOD_GATE, BAD_SCHEMA, preferred_pair, METADATA_CLEAN, clean_warning, "PASS", "BLOCKED_SCHEMA"),
        ("metadata_contradiction", GOOD_GATE, GOOD_SCHEMA, preferred_pair, METADATA_FAIL, clean_warning, "PASS", "BLOCKED_METADATA_CONTRADICTION"),
        ("batch_confounder_warning", GOOD_GATE, GOOD_SCHEMA, preferred_pair, METADATA_CLEAN, warning_summary, "PASS", "CAUTION_BATCH_OR_CONFOUNDER"),
    ]
    rows: list[dict[str, object]] = []
    exit_codes: list[int] = []
    for case, gate, schema, pair, metadata, warning, terms, expected in cases:
        case_out = outdir / case
        rc = classify_package(gate, schema, pair, metadata, warning, terms, case_out, expected)
        exit_codes.append(rc)
        summary = read_json(case_out / "safe_interpretation_summary.json")
        rows.append(
            {
                "case": case,
                "expected_class": expected,
                "observed_class": summary.get("result_class", "MISSING"),
                "expectation_met": str(summary.get("expectation_met", False)).lower(),
                "summary": rel(case_out / "safe_interpretation_summary.json"),
            }
        )
    write_tsv(
        outdir / "safe_interpretation_synthetic_cases.tsv",
        rows,
        ["case", "expected_class", "observed_class", "expectation_met", "summary"],
    )
    n_fail = sum(1 for row in rows if row["expectation_met"] != "true")
    summary = {
        "synthetic": True,
        "purpose": "V46 returned-package safe-interpretation synthetic verification; no biological claim",
        "n_cases": len(rows),
        "n_expectation_failures": n_fail,
        "overall_status": "PASS" if n_fail == 0 and all(rc == 0 for rc in exit_codes) else "FAIL",
        "case_table": rel(outdir / "safe_interpretation_synthetic_cases.tsv"),
    }
    (outdir / "safe_interpretation_synthetic_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir)
    return classify_package(
        resolve(args.gate_summary),
        resolve(args.schema_summary),
        resolve(args.analyzable_summary),
        resolve(args.metadata_summary) if args.metadata_summary else None,
        resolve(args.batch_confounder_summary) if args.batch_confounder_summary else None,
        args.terms_status,
        resolve(args.outdir),
        args.expect_class,
    )


if __name__ == "__main__":
    raise SystemExit(main())
