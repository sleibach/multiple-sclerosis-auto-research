#!/usr/bin/env python3
"""Lightweight response-column audit for metadata drafts.

This is a pre-preflight guard for pharmacodynamic-only cohorts. It scans a
metadata table for response/outcome-like columns so an unlabeled context cohort
does not silently become a response-validation dataset.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GSE228330_DRAFT = (
    ROOT
    / "analysis/v45_gse228330_pharmacodynamic_runbook/"
    "gse228330_draft_pharmacodynamic_metadata_unverified.tsv"
)

RESPONSE_TOKENS = [
    "response",
    "responder",
    "nonresponder",
    "non_responder",
    "neda",
    "neda4",
    "relapse",
    "remission",
    "edss",
    "disability",
    "progression",
    "mri_activity",
    "disease_activity",
    "outcome",
    "event_free",
    "pasi",
    "mayo",
]

SAFE_CONTEXT_TOKENS = [
    "use_status",
    "clinical_status",
    "qc_status",
]


def normalize(value: object) -> str:
    return str(value).strip()


def matched_tokens(column: str) -> list[str]:
    lower = column.lower()
    if lower in SAFE_CONTEXT_TOKENS:
        return []
    return [token for token in RESPONSE_TOKENS if token in lower]


def audit_metadata(metadata: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    rows = []
    for col in metadata.columns:
        tokens = matched_tokens(col)
        if not tokens:
            continue
        nonmissing = metadata[col].dropna().astype(str)
        examples = sorted(set(nonmissing.map(normalize).tolist()))[:8]
        rows.append(
            {
                "column": col,
                "matched_tokens": ";".join(tokens),
                "nonmissing_count": int(nonmissing.shape[0]),
                "unique_nonmissing_values_sample": ";".join(examples),
                "severity_for_pharmacodynamic_only": "FAIL_RESPONSE_LIKE_COLUMN_PRESENT",
                "interpretation": "Do not run pharmacodynamic-only context harness until this column is removed, quarantined, or governed by a response-validation preregistration.",
            }
        )
    audit = pd.DataFrame(
        rows,
        columns=[
            "column",
            "matched_tokens",
            "nonmissing_count",
            "unique_nonmissing_values_sample",
            "severity_for_pharmacodynamic_only",
            "interpretation",
        ],
    )
    summary = {
        "overall_status": "PASS" if audit.empty else "FAIL_RESPONSE_LIKE_COLUMNS_PRESENT",
        "n_columns": int(len(metadata.columns)),
        "n_response_like_columns": int(len(audit)),
        "response_like_columns": audit["column"].tolist() if not audit.empty else [],
    }
    return audit, summary


def run_audit(metadata_path: Path, outdir: Path) -> dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    metadata = pd.read_csv(metadata_path, sep="\t")
    audit, summary = audit_metadata(metadata)
    summary["metadata_path"] = str(metadata_path)
    audit.to_csv(outdir / "response_column_audit.tsv", sep="\t", index=False)
    (outdir / "response_column_audit_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def write_synthetic_tables(outdir: Path) -> tuple[Path, Path]:
    synthetic_dir = outdir / "synthetic"
    synthetic_dir.mkdir(parents=True, exist_ok=True)
    safe = pd.DataFrame(
        {
            "sample_id": ["S1_B", "S1_W2"],
            "subject": ["S1", "S1"],
            "timepoint": ["baseline", "week2"],
            "clinical_status": ["stable", "stable"],
            "use_status": ["context_only", "context_only"],
        }
    )
    unsafe = safe.copy()
    unsafe["NEDA4_response"] = ["responder", "responder"]
    unsafe["relapse_12m"] = ["no", "no"]
    safe_path = synthetic_dir / "safe_pharmacodynamic_metadata.tsv"
    unsafe_path = synthetic_dir / "unsafe_response_metadata.tsv"
    safe.to_csv(safe_path, sep="\t", index=False)
    unsafe.to_csv(unsafe_path, sep="\t", index=False)
    return safe_path, unsafe_path


def run_synthetic_check(outdir: Path) -> dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    safe_path, unsafe_path = write_synthetic_tables(outdir)
    safe = run_audit(safe_path, outdir / "safe_pharmacodynamic_metadata")
    unsafe = run_audit(unsafe_path, outdir / "unsafe_response_metadata")
    gse = None
    if DEFAULT_GSE228330_DRAFT.exists():
        gse = run_audit(DEFAULT_GSE228330_DRAFT, outdir / "gse228330_public_draft")
    assertions = {
        "synthetic": True,
        "safe_metadata_pass": safe["overall_status"] == "PASS",
        "unsafe_metadata_fails": unsafe["overall_status"] == "FAIL_RESPONSE_LIKE_COLUMNS_PRESENT",
        "gse228330_public_draft_status": gse["overall_status"] if gse is not None else "not_run_missing_file",
        "safe_summary": safe,
        "unsafe_summary": unsafe,
        "gse228330_summary": gse,
    }
    assertions["overall_status"] = (
        "PASS"
        if assertions["safe_metadata_pass"] and assertions["unsafe_metadata_fails"]
        else "FAIL"
    )
    (outdir / "synthetic_check_assertions.json").write_text(json.dumps(assertions, indent=2, sort_keys=True) + "\n")
    return assertions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit", help="Audit one metadata TSV.")
    audit.add_argument("--metadata", required=True, type=Path)
    audit.add_argument("--outdir", required=True, type=Path)
    audit.add_argument("--fail-on-response-like", action="store_true")

    synth = sub.add_parser("synthetic-check", help="Run safe and unsafe fixture checks.")
    synth.add_argument("--outdir", required=True, type=Path)
    args = parser.parse_args()

    if args.command == "audit":
        summary = run_audit(args.metadata, args.outdir)
        print(json.dumps(summary, indent=2, sort_keys=True))
        if args.fail_on_response_like and summary["overall_status"] != "PASS":
            return 2
        return 0

    assertions = run_synthetic_check(args.outdir)
    print(json.dumps(assertions, indent=2, sort_keys=True))
    return 0 if assertions["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
