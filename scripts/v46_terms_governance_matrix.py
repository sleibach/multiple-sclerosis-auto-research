#!/usr/bin/env python3
"""Classify data-use terms into safe validation-handling routes.

This is governance infrastructure only. It reads non-sensitive terms-capture
summaries and decides whether local preflight, aggregate-only handling,
author-run-only handling, or no processing is allowed. It does not read data,
run validation, or make a biological claim.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_terms_governance_matrix"
TEMPLATE = ROOT / "docs/validation/input_schemas/V45_data_use_terms_capture_template.tsv"

PASS_CLASSES = {"LOCAL_PREFLIGHT_ALLOWED", "AGGREGATE_ONLY_LOCAL_PREFLIGHT"}

LANGUAGE = {
    "LOCAL_PREFLIGHT_ALLOWED": {
        "operator_gate_status": "pass",
        "safe_route": "local preflight and frozen harness may proceed after all other gates pass",
        "hard_stop": "do not commit raw/private files unless terms explicitly allow it",
    },
    "AGGREGATE_ONLY_LOCAL_PREFLIGHT": {
        "operator_gate_status": "pass",
        "safe_route": "local processing may proceed, but only derived aggregate summaries may be committed/reported",
        "hard_stop": "do not commit individual-level expression, clinical labels, or restricted agreements",
    },
    "AUTHOR_RUN_ONLY": {
        "operator_gate_status": "blocked",
        "safe_route": "send or use author-run frozen harness packet; receive aggregate outputs only",
        "hard_stop": "do not process transferred individual-level data locally",
    },
    "NO_PROCESSING_ALLOWED": {
        "operator_gate_status": "blocked",
        "safe_route": "do not process; request revised terms or an allowed aggregate author-run return",
        "hard_stop": "do not run preflight, module coverage, validation harness, or score interpretation",
    },
    "AMBIGUOUS_TERMS_BLOCK": {
        "operator_gate_status": "blocked",
        "safe_route": "clarify terms before any preflight or package processing",
        "hard_stop": "do not treat unclear terms as approval",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    classify_cmd = sub.add_parser("classify")
    classify_cmd.add_argument("--terms", type=Path, required=True)
    classify_cmd.add_argument("--outdir", type=Path, required=True)
    classify_cmd.add_argument("--expect-class")

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


def norm(value: object) -> str:
    return str(value or "").strip().lower()


def read_terms(path: Path) -> dict[str, str]:
    table = pd.read_csv(path, sep="\t", dtype=str).fillna("")
    if table.empty:
        return {}
    return {key: str(value) for key, value in table.iloc[0].to_dict().items()}


def classify_terms(row: dict[str, str]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    status = norm(row.get("status"))
    redistribution = norm(row.get("redistribution_allowed"))
    derived = norm(row.get("derived_metrics_allowed"))
    aggregate = norm(row.get("aggregate_publication_allowed"))
    individual = norm(row.get("individual_level_publication_allowed"))
    approved = norm(row.get("approved_internal_use"))
    forbidden = norm(row.get("forbidden_use"))
    commit_allowed = norm(row.get("commit_allowed_files"))

    if "author-run" in approved or "author run" in approved or "owner runs" in approved:
        reasons.append("approved_internal_use indicates author-run-only handling")
        return "AUTHOR_RUN_ONLY", reasons
    if "no local processing" in forbidden or "do not process" in forbidden:
        reasons.append("forbidden_use blocks local processing")
        return "NO_PROCESSING_ALLOWED", reasons
    if status != "approved_for_preflight":
        reasons.append(f"status={status or 'missing'} is not approved_for_preflight")
        return "AMBIGUOUS_TERMS_BLOCK", reasons
    unclear = [name for name, value in [("redistribution_allowed", redistribution), ("derived_metrics_allowed", derived), ("aggregate_publication_allowed", aggregate)] if value in {"", "unclear"}]
    if unclear:
        reasons.append("unclear required permissions: " + ",".join(unclear))
        return "AMBIGUOUS_TERMS_BLOCK", reasons
    if derived == "no" and aggregate == "no":
        reasons.append("both derived metrics and aggregate publication are disallowed")
        return "NO_PROCESSING_ALLOWED", reasons
    if derived == "no" and aggregate == "yes":
        reasons.append("local derived metric generation disallowed but aggregate return may be allowed")
        return "AUTHOR_RUN_ONLY", reasons
    if derived == "yes" and aggregate == "yes":
        if redistribution == "yes" and individual == "yes":
            reasons.append("terms permit redistribution and individual-level publication")
            return "LOCAL_PREFLIGHT_ALLOWED", reasons
        if "aggregate" in commit_allowed or individual in {"no", "unclear", ""} or redistribution == "no":
            reasons.append("derived aggregate processing allowed; individual-level sharing remains restricted")
            return "AGGREGATE_ONLY_LOCAL_PREFLIGHT", reasons
        reasons.append("derived aggregate processing allowed")
        return "LOCAL_PREFLIGHT_ALLOWED", reasons
    reasons.append("permission combination not recognized as safe")
    return "AMBIGUOUS_TERMS_BLOCK", reasons


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def classify_path(terms: Path, outdir: Path, expect_class: str | None) -> int:
    terms = resolve(terms)
    outdir = resolve(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    row = read_terms(terms)
    result_class, reasons = classify_terms(row)
    language = LANGUAGE[result_class]
    decision_path = outdir / "terms_governance_decision.tsv"
    write_tsv(
        decision_path,
        [
            {
                "result_class": result_class,
                "operator_gate_status": language["operator_gate_status"],
                "safe_route": language["safe_route"],
                "hard_stop": language["hard_stop"],
                "reason": "; ".join(reasons),
            }
        ],
        ["result_class", "operator_gate_status", "safe_route", "hard_stop", "reason"],
    )
    summary = {
        "synthetic": "synthetic" in str(terms).lower() or "synthetic" in str(outdir).lower(),
        "purpose": "V46 terms-governance classifier; no biological claim",
        "terms": rel(terms),
        "result_class": result_class,
        "operator_gate_status": language["operator_gate_status"],
        "safe_route": language["safe_route"],
        "hard_stop": language["hard_stop"],
        "reasons": reasons,
        "decision": rel(decision_path),
        "expect_class": expect_class or "",
        "expectation_met": (not expect_class) or result_class == expect_class,
    }
    (outdir / "terms_governance_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["expectation_met"] else 2


def base_terms(case: str) -> dict[str, str]:
    table = pd.read_csv(TEMPLATE, sep="\t", dtype=str).fillna("")
    row = {column: "" for column in table.columns}
    row.update(
        {
            "cohort_id": f"synthetic_{case}",
            "source_name": f"synthetic {case}",
            "source_url_or_accession": "synthetic_fixture",
            "access_tier": "collaborator",
            "received_date_utc": "2026-06-13",
            "data_provider_contact_non_sensitive": "synthetic_role",
            "agreement_location_non_git": "NON_GIT_SYNTHETIC_RECORD",
            "redistribution_allowed": "no",
            "derived_metrics_allowed": "yes",
            "aggregate_publication_allowed": "yes",
            "individual_level_publication_allowed": "no",
            "commercial_use_allowed": "not_applicable",
            "data_retention_limit": "project duration",
            "requires_acknowledgement": "no",
            "requires_provider_review_before_publication": "no",
            "contains_personal_data_or_sensitive_clinical_data": "yes",
            "approved_internal_use": "local preflight and frozen harness",
            "forbidden_use": "commit raw data",
            "commit_allowed_files": "aggregate summaries only",
            "non_git_storage_path": "NON_GIT_SYNTHETIC_PATH",
            "notes_non_sensitive": "synthetic governance fixture; method behavior only",
            "reviewer": "synthetic_v46",
            "review_date_utc": "2026-06-13",
            "status": "approved_for_preflight",
        }
    )
    return row


def write_case(path: Path, row: dict[str, str]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([row]).to_csv(path, sep="\t", index=False)
    return path


def synthetic_check(outdir: Path) -> int:
    outdir = resolve(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    synthetic = outdir / "synthetic"
    cases: list[tuple[str, dict[str, str], str]] = []

    local = base_terms("local_preflight_allowed")
    local.update({"redistribution_allowed": "yes", "individual_level_publication_allowed": "yes", "commit_allowed_files": "raw and aggregate files if otherwise allowed"})
    cases.append(("local_preflight_allowed", local, "LOCAL_PREFLIGHT_ALLOWED"))

    aggregate_only = base_terms("aggregate_only_local_preflight")
    cases.append(("aggregate_only_local_preflight", aggregate_only, "AGGREGATE_ONLY_LOCAL_PREFLIGHT"))

    author_run = base_terms("author_run_only")
    author_run.update({"derived_metrics_allowed": "no", "approved_internal_use": "author-run-only: owner runs frozen harness locally and returns aggregate output"})
    cases.append(("author_run_only", author_run, "AUTHOR_RUN_ONLY"))

    no_processing = base_terms("no_processing")
    no_processing.update({"derived_metrics_allowed": "no", "aggregate_publication_allowed": "no", "forbidden_use": "do not process; no local processing"})
    cases.append(("no_processing", no_processing, "NO_PROCESSING_ALLOWED"))

    ambiguous = base_terms("ambiguous_terms")
    ambiguous.update({"redistribution_allowed": "unclear", "derived_metrics_allowed": "unclear", "status": "pending_review"})
    cases.append(("ambiguous_terms", ambiguous, "AMBIGUOUS_TERMS_BLOCK"))

    rows: list[dict[str, object]] = []
    exit_codes: list[int] = []
    for name, row, expected in cases:
        terms_path = write_case(synthetic / f"{name}_terms.tsv", row)
        case_out = outdir / name
        rc = classify_path(terms_path, case_out, expected)
        exit_codes.append(rc)
        summary = json.loads((case_out / "terms_governance_summary.json").read_text())
        rows.append(
            {
                "case": name,
                "expected_class": expected,
                "observed_class": summary["result_class"],
                "operator_gate_status": summary["operator_gate_status"],
                "expectation_met": str(summary["expectation_met"]).lower(),
                "summary": rel(case_out / "terms_governance_summary.json"),
            }
        )
    write_tsv(outdir / "terms_governance_synthetic_cases.tsv", rows, ["case", "expected_class", "observed_class", "operator_gate_status", "expectation_met", "summary"])
    n_fail = sum(1 for row in rows if row["expectation_met"] != "true")
    summary = {
        "synthetic": True,
        "purpose": "V46 synthetic terms-governance edge-case matrix; no biological claim",
        "n_cases": len(rows),
        "n_expectation_failures": n_fail,
        "overall_status": "PASS" if n_fail == 0 and all(rc == 0 for rc in exit_codes) else "FAIL",
        "case_table": rel(outdir / "terms_governance_synthetic_cases.tsv"),
    }
    (outdir / "terms_governance_synthetic_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir)
    return classify_path(args.terms, args.outdir, args.expect_class)


if __name__ == "__main__":
    raise SystemExit(main())
