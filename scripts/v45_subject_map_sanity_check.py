#!/usr/bin/env python3
"""Audit longitudinal subject maps before paired-delta validation.

The checker is intentionally conservative. Public-order or inferred subject
maps are allowed to be documented, but they must fail this audit before any
paired baseline/on-treatment delta harness can use them.
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

REQUIRED_COLUMNS = ["sample_id", "subject", "timepoint"]
UNVERIFIED_TOKENS = [
    "UNVERIFIED",
    "INFERRED",
    "PUBLIC_ORDER",
    "PSEUDO",
    "PLACEHOLDER",
]
UNVERIFIED_PAIRING_TOKENS = ["unverified", "inferred", "public_order", "placeholder"]
BASELINE_TIMEPOINTS = {
    "baseline",
    "base",
    "pre",
    "pre_treatment",
    "pretreatment",
    "before",
    "week0",
    "w0",
    "month0",
    "m0",
    "day0",
    "d0",
    "0",
}


def normalize_text(value: object) -> str:
    return str(value).strip()


def normalize_timepoint(value: object) -> str:
    return normalize_text(value).lower().replace(" ", "_").replace("-", "_")


def numeric_days(series: pd.Series | None, n_rows: int) -> pd.Series:
    if series is None:
        return pd.Series([pd.NA] * n_rows)
    return pd.to_numeric(series, errors="coerce")


def is_baseline(row: pd.Series) -> bool:
    timepoint = normalize_timepoint(row.get("timepoint", ""))
    if timepoint in BASELINE_TIMEPOINTS:
        return True
    days = pd.to_numeric(pd.Series([row.get("days_since_treatment", pd.NA)]), errors="coerce").iloc[0]
    return pd.notna(days) and float(days) == 0.0


def issue(rows: list[dict[str, object]], level: str, check: str, subject: str, sample_id: str, detail: str) -> None:
    rows.append(
        {
            "level": level,
            "check": check,
            "subject": subject,
            "sample_id": sample_id,
            "detail": detail,
        }
    )


def audit_subject_map(metadata: pd.DataFrame, min_paired_subjects: int = 1) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, object]]:
    rows: list[dict[str, object]] = []
    n_rows = len(metadata)

    for col in REQUIRED_COLUMNS:
        if col not in metadata.columns:
            issue(rows, "FAIL", "missing_required_column", "", "", f"Required column absent: {col}")
    if rows:
        audit = pd.DataFrame(rows)
        summary = {
            "overall_status": "FAIL",
            "n_samples": n_rows,
            "n_subjects": 0,
            "n_paired_subjects": 0,
            "n_fail": int((audit["level"] == "FAIL").sum()),
            "n_warn": int((audit["level"] == "WARN").sum()),
            "min_paired_subjects": min_paired_subjects,
        }
        return audit, pd.DataFrame(), summary

    metadata = metadata.copy()
    metadata["sample_id"] = metadata["sample_id"].map(normalize_text)
    metadata["subject"] = metadata["subject"].map(normalize_text)
    metadata["timepoint"] = metadata["timepoint"].map(normalize_text)
    metadata["_days"] = numeric_days(metadata.get("days_since_treatment"), len(metadata))
    metadata["_is_baseline"] = metadata.apply(is_baseline, axis=1)
    metadata["_timepoint_norm"] = metadata["timepoint"].map(normalize_timepoint)

    duplicated_samples = metadata[metadata["sample_id"].duplicated(keep=False)]
    for _, row in duplicated_samples.iterrows():
        issue(
            rows,
            "FAIL",
            "duplicate_sample_id",
            row["subject"],
            row["sample_id"],
            "sample_id appears more than once",
        )

    for _, row in metadata.iterrows():
        subject_upper = row["subject"].upper()
        matching_tokens = [token for token in UNVERIFIED_TOKENS if token in subject_upper]
        if matching_tokens:
            issue(
                rows,
                "FAIL",
                "unverified_subject_identifier",
                row["subject"],
                row["sample_id"],
                f"subject contains placeholder/unverified token(s): {','.join(matching_tokens)}",
            )
    if "pairing_status" in metadata.columns:
        for _, row in metadata.iterrows():
            status = normalize_text(row.get("pairing_status", "")).lower()
            matching = [token for token in UNVERIFIED_PAIRING_TOKENS if token in status]
            if matching:
                issue(
                    rows,
                    "FAIL",
                    "unverified_pairing_status",
                    row["subject"],
                    row["sample_id"],
                    f"pairing_status indicates unverified/inferred map: {row.get('pairing_status')}",
                )

    duplicated_subject_timepoints = metadata[metadata.duplicated(["subject", "_timepoint_norm"], keep=False)]
    for _, row in duplicated_subject_timepoints.iterrows():
        issue(
            rows,
            "FAIL",
            "duplicate_subject_timepoint",
            row["subject"],
            row["sample_id"],
            f"subject has more than one sample at timepoint {row['timepoint']}",
        )

    subject_rows = []
    for subject, sub in metadata.groupby("subject", sort=True):
        n_baseline = int(sub["_is_baseline"].sum())
        n_nonbaseline = int((~sub["_is_baseline"]).sum())
        has_day_info = bool(sub["_days"].notna().any())
        min_day = float(sub["_days"].min()) if has_day_info else None
        max_day = float(sub["_days"].max()) if has_day_info else None
        paired = n_baseline == 1 and n_nonbaseline >= 1
        subject_rows.append(
            {
                "subject": subject,
                "n_samples": int(len(sub)),
                "n_baseline": n_baseline,
                "n_nonbaseline": n_nonbaseline,
                "min_days_since_treatment": min_day,
                "max_days_since_treatment": max_day,
                "paired_map_usable": paired,
                "sample_ids": ";".join(sub["sample_id"].tolist()),
                "timepoints": ";".join(sub["timepoint"].tolist()),
            }
        )
        sample_ids = ";".join(sub["sample_id"].tolist())
        if n_baseline == 0:
            issue(rows, "FAIL", "subject_missing_baseline", subject, sample_ids, "subject has no baseline sample")
        elif n_baseline > 1:
            issue(rows, "FAIL", "subject_multiple_baselines", subject, sample_ids, "subject has multiple baseline samples")
        if n_nonbaseline == 0:
            issue(rows, "FAIL", "subject_no_nonbaseline", subject, sample_ids, "subject has no on-treatment/nonbaseline sample")
        if has_day_info:
            baseline_days = sub.loc[sub["_is_baseline"], "_days"].dropna()
            nonbaseline_days = sub.loc[~sub["_is_baseline"], "_days"].dropna()
            if not baseline_days.empty and (baseline_days != 0).any():
                issue(
                    rows,
                    "FAIL",
                    "baseline_day_not_zero",
                    subject,
                    sample_ids,
                    f"baseline day values are not all zero: {baseline_days.tolist()}",
                )
            if not nonbaseline_days.empty and (nonbaseline_days <= 0).any():
                issue(
                    rows,
                    "FAIL",
                    "nonbaseline_day_not_positive",
                    subject,
                    sample_ids,
                    f"nonbaseline day values are not strictly positive: {nonbaseline_days.tolist()}",
                )
            ordered = sub.sort_values(["_days", "sample_id"], na_position="last")
            finite_days = ordered["_days"].dropna().tolist()
            if finite_days != sorted(finite_days):
                issue(
                    rows,
                    "WARN",
                    "nonmonotonic_days",
                    subject,
                    sample_ids,
                    f"days_since_treatment not monotonic after sorting: {finite_days}",
                )

    subject_summary = pd.DataFrame(subject_rows)
    n_paired = int(subject_summary["paired_map_usable"].sum()) if not subject_summary.empty else 0
    if n_paired < min_paired_subjects:
        issue(
            rows,
            "FAIL",
            "insufficient_paired_subjects",
            "",
            "",
            f"usable paired subjects {n_paired} < required {min_paired_subjects}",
        )

    if not rows:
        issue(rows, "PASS", "subject_map_sanity", "", "", "subject map passes required pairing checks")
    audit = pd.DataFrame(rows)
    n_fail = int((audit["level"] == "FAIL").sum())
    n_warn = int((audit["level"] == "WARN").sum())
    summary = {
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "n_samples": int(n_rows),
        "n_subjects": int(metadata["subject"].nunique()),
        "n_paired_subjects": n_paired,
        "n_fail": n_fail,
        "n_warn": n_warn,
        "min_paired_subjects": min_paired_subjects,
    }
    return audit, subject_summary, summary


def run_check(metadata_path: Path, outdir: Path, min_paired_subjects: int = 1) -> dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    metadata = pd.read_csv(metadata_path, sep="\t")
    audit, subject_summary, summary = audit_subject_map(metadata, min_paired_subjects=min_paired_subjects)
    audit.to_csv(outdir / "subject_map_audit.tsv", sep="\t", index=False)
    subject_summary.to_csv(outdir / "subject_summary.tsv", sep="\t", index=False)
    summary["metadata_path"] = str(metadata_path)
    (outdir / "subject_map_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def write_valid_synthetic(path: Path) -> None:
    rows = []
    for subject in ["SYN001", "SYN002", "SYN003"]:
        for sample_suffix, timepoint, day in [
            ("B", "baseline", 0),
            ("W2", "week2", 14),
            ("M6", "month6", 180),
        ]:
            rows.append(
                {
                    "sample_id": f"{subject}_{sample_suffix}",
                    "subject": subject,
                    "timepoint": timepoint,
                    "days_since_treatment": day,
                    "therapy": "synthetic_dmf",
                    "pairing_status": "verified_author_map",
                }
            )
    pd.DataFrame(rows).to_csv(path, sep="\t", index=False)


def run_synthetic_check(outdir: Path) -> dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    synthetic_dir = outdir / "synthetic"
    synthetic_dir.mkdir(parents=True, exist_ok=True)
    valid_metadata = synthetic_dir / "valid_verified_subject_map.tsv"
    write_valid_synthetic(valid_metadata)
    valid_summary = run_check(valid_metadata, outdir / "valid_verified_subject_map", min_paired_subjects=2)

    negative_path = DEFAULT_GSE228330_DRAFT if DEFAULT_GSE228330_DRAFT.exists() else synthetic_dir / "negative_unverified_subject_map.tsv"
    if not negative_path.exists():
        negative = pd.read_csv(valid_metadata, sep="\t")
        negative["subject"] = [f"UNVERIFIED_PUBLIC_ORDER_{idx:02d}" for idx in range(1, len(negative) + 1)]
        negative["pairing_status"] = "inferred_unverified"
        negative.to_csv(negative_path, sep="\t", index=False)
    negative_summary = run_check(negative_path, outdir / "negative_unverified_subject_map", min_paired_subjects=2)

    assertions = {
        "synthetic": True,
        "valid_paired_map_pass": valid_summary["overall_status"] == "PASS",
        "unverified_map_fails": negative_summary["overall_status"] == "FAIL",
        "negative_metadata_path": str(negative_path),
        "valid_summary": valid_summary,
        "negative_summary": negative_summary,
    }
    assertions["overall_status"] = (
        "PASS"
        if assertions["valid_paired_map_pass"] and assertions["unverified_map_fails"]
        else "FAIL"
    )
    (outdir / "synthetic_check_assertions.json").write_text(json.dumps(assertions, indent=2, sort_keys=True) + "\n")
    return assertions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="Audit one metadata table.")
    check.add_argument("--metadata", required=True, type=Path)
    check.add_argument("--outdir", required=True, type=Path)
    check.add_argument("--min-paired-subjects", type=int, default=1)
    check.add_argument("--fail-on-error", action="store_true")

    synth = sub.add_parser("synthetic-check", help="Run passing and failing fixture checks.")
    synth.add_argument("--outdir", required=True, type=Path)

    args = parser.parse_args()
    if args.command == "check":
        summary = run_check(args.metadata, args.outdir, min_paired_subjects=args.min_paired_subjects)
        print(json.dumps(summary, indent=2, sort_keys=True))
        if args.fail_on_error and summary["overall_status"] != "PASS":
            return 2
        return 0
    assertions = run_synthetic_check(args.outdir)
    print(json.dumps(assertions, indent=2, sort_keys=True))
    return 0 if assertions["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
