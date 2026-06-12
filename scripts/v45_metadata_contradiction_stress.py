#!/usr/bin/env python3
"""Audit validation-intake metadata for internal contradictions.

This guard is intake infrastructure only. It reads metadata tables and reports
contradictions; it does not read expression values, compute module scores, or
run a validation harness.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_metadata_contradiction_stress"
SEED = 450123


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    audit = sub.add_parser("audit")
    audit.add_argument("--metadata", type=Path, required=True)
    audit.add_argument("--outdir", type=Path, required=True)
    audit.add_argument("--expect-status", choices=["PASS", "FAIL"], default="PASS")

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


def norm_series(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.lower()


def add_issue(issues: list[dict[str, object]], severity: str, check: str, subject: str, detail: str) -> None:
    issues.append({"severity": severity, "check": check, "subject_or_group": subject, "detail": detail})


def audit_table(metadata: pd.DataFrame) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    required = {"sample_id", "patient", "timepoint", "response", "days_since_treatment", "batch"}
    missing = sorted(required - set(metadata.columns))
    for column in missing:
        add_issue(issues, "hard", "missing_required_metadata_column", column, f"required column absent: {column}")
    if missing:
        return issues

    md = metadata.copy()
    md["patient_norm"] = norm_series(md["patient"])
    md["sample_norm"] = norm_series(md["sample_id"])
    md["timepoint_norm"] = norm_series(md["timepoint"])
    md["response_norm"] = norm_series(md["response"])
    md["days_numeric"] = pd.to_numeric(md["days_since_treatment"], errors="coerce")

    duplicated_samples = md.loc[md["sample_norm"].duplicated(keep=False), "sample_norm"].unique()
    for sample in sorted(duplicated_samples):
        add_issue(issues, "hard", "duplicate_sample_id", sample, "sample_id appears more than once")

    for patient, group in md.groupby("patient_norm"):
        responses = sorted(set(group["response_norm"]) - {"", "nan"})
        if len(responses) > 1:
            add_issue(issues, "hard", "within_patient_response_conflict", patient, f"responses={responses}")

        timepoints = group["timepoint_norm"].tolist()
        if "baseline" not in timepoints:
            add_issue(issues, "hard", "missing_baseline_timepoint", patient, "baseline row absent")
        followup_count = sum(tp not in {"baseline", "", "nan"} for tp in timepoints)
        if followup_count < 1:
            add_issue(issues, "hard", "missing_followup_timepoint", patient, "no non-baseline row present")
        duplicated_timepoints = group.loc[group["timepoint_norm"].duplicated(keep=False), "timepoint_norm"].unique()
        for timepoint in sorted(tp for tp in duplicated_timepoints if tp not in {"", "nan"}):
            add_issue(issues, "hard", "duplicate_patient_timepoint", patient, f"duplicate timepoint={timepoint}")

        if group["days_numeric"].isna().any():
            add_issue(issues, "hard", "non_numeric_days_since_treatment", patient, "days_since_treatment has non-numeric values")
        baseline_days = group.loc[group["timepoint_norm"] == "baseline", "days_numeric"]
        followup_days = group.loc[group["timepoint_norm"] != "baseline", "days_numeric"]
        if not baseline_days.empty and not followup_days.empty:
            if baseline_days.min() != 0:
                add_issue(issues, "hard", "baseline_day_not_zero", patient, f"baseline minimum day={baseline_days.min()}")
            if followup_days.min() <= baseline_days.min():
                add_issue(issues, "hard", "followup_not_after_baseline", patient, "follow-up day is not greater than baseline day")

    response_values = sorted(set(md["response_norm"]) - {"", "nan"})
    for batch_column in [col for col in ["batch", "processing_batch", "sequencing_batch"] if col in md.columns]:
        batch = norm_series(md[batch_column])
        crosstab = pd.crosstab(batch, md["response_norm"])
        crosstab = crosstab[[col for col in crosstab.columns if col not in {"", "nan"}]]
        if len(response_values) > 1 and not crosstab.empty:
            batch_pure = (crosstab.gt(0).sum(axis=1) == 1).all()
            response_pure = (crosstab.gt(0).sum(axis=0) == 1).all()
            if batch_pure and response_pure:
                add_issue(
                    issues,
                    "hard",
                    "response_batch_perfect_confounding",
                    batch_column,
                    "each response class is isolated in a distinct batch; clean validation verdict would be invalid",
                )
    return issues


def audit(metadata_path: Path, outdir: Path, expect_status: str, synthetic: bool = False, case: str = "none") -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    metadata = pd.read_csv(metadata_path, sep="\t").fillna("")
    issues = audit_table(metadata)
    issue_path = outdir / "metadata_contradiction_issues.tsv"
    write_tsv(issue_path, issues, ["severity", "check", "subject_or_group", "detail"])
    hard = sum(1 for row in issues if row["severity"] == "hard")
    observed = "PASS" if hard == 0 else "FAIL"
    summary = {
        "synthetic": synthetic,
        "synthetic_case": case,
        "seed": SEED if synthetic else "",
        "purpose": "V45 metadata contradiction audit; no biological claim",
        "metadata": rel(metadata_path),
        "issues": rel(issue_path),
        "n_rows": int(len(metadata)),
        "n_hard_issues": hard,
        "observed_status": observed,
        "expected_status": expect_status,
        "expectation_met": observed == expect_status,
    }
    (outdir / "metadata_contradiction_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["expectation_met"] else 2


def clean_metadata() -> pd.DataFrame:
    rows = []
    for patient, response, batch in [("P1", "responder", "b1"), ("P2", "nonresponder", "b1"), ("P3", "responder", "b2"), ("P4", "nonresponder", "b2")]:
        rows.append({"sample_id": f"{patient}_BL", "patient": patient, "timepoint": "baseline", "response": response, "days_since_treatment": 0, "batch": batch, "processing_batch": f"p{batch[-1]}"})
        rows.append({"sample_id": f"{patient}_W6", "patient": patient, "timepoint": "week6", "response": response, "days_since_treatment": 42, "batch": batch, "processing_batch": f"p{batch[-1]}"})
    return pd.DataFrame(rows)


def synthetic_check(outdir: Path) -> int:
    outdir = resolve(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    synthetic_dir = outdir / "synthetic"
    synthetic_dir.mkdir(parents=True)

    cases: list[tuple[str, pd.DataFrame, str]] = []
    clean = clean_metadata()
    cases.append(("clean_pass", clean, "PASS"))

    response_conflict = clean.copy()
    response_conflict.loc[response_conflict["sample_id"] == "P1_W6", "response"] = "nonresponder"
    cases.append(("response_conflict_fail", response_conflict, "FAIL"))

    timepoint_conflict = clean.copy()
    timepoint_conflict.loc[timepoint_conflict["sample_id"] == "P2_W6", "timepoint"] = "baseline"
    timepoint_conflict.loc[timepoint_conflict["sample_id"] == "P2_W6", "days_since_treatment"] = 0
    cases.append(("timepoint_conflict_fail", timepoint_conflict, "FAIL"))

    batch_conflict = clean.copy()
    batch_conflict["batch"] = batch_conflict["response"].map({"responder": "batch_R", "nonresponder": "batch_NR"})
    batch_conflict["processing_batch"] = batch_conflict["batch"]
    cases.append(("batch_conflict_fail", batch_conflict, "FAIL"))

    rows = []
    exit_codes = []
    for case, table, expected in cases:
        metadata_path = synthetic_dir / f"{case}_metadata.tsv"
        table.to_csv(metadata_path, sep="\t", index=False)
        case_out = outdir / case
        rc = audit(metadata_path, case_out, expected, synthetic=True, case=case)
        exit_codes.append(rc)
        summary = json.loads((case_out / "metadata_contradiction_summary.json").read_text())
        rows.append(
            {
                "case": case,
                "expected_status": expected,
                "observed_status": summary["observed_status"],
                "expectation_met": str(summary["expectation_met"]).lower(),
                "n_hard_issues": summary["n_hard_issues"],
                "metadata": rel(metadata_path),
                "summary": rel(case_out / "metadata_contradiction_summary.json"),
            }
        )
    write_tsv(
        outdir / "metadata_contradiction_synthetic_cases.tsv",
        rows,
        ["case", "expected_status", "observed_status", "expectation_met", "n_hard_issues", "metadata", "summary"],
    )
    overall = {
        "synthetic": True,
        "seed": SEED,
        "purpose": "V45 metadata contradiction synthetic stress test; no biological claim",
        "n_cases": len(rows),
        "n_expectation_failures": sum(1 for row in rows if row["expectation_met"] != "true"),
        "case_table": rel(outdir / "metadata_contradiction_synthetic_cases.tsv"),
    }
    (outdir / "metadata_contradiction_stress_summary.json").write_text(json.dumps(overall, indent=2, sort_keys=True) + "\n")
    return 0 if all(code == 0 for code in exit_codes) and overall["n_expectation_failures"] == 0 else 2


def main() -> int:
    args = parse_args()
    if args.cmd == "audit":
        return audit(resolve(args.metadata), resolve(args.outdir), args.expect_status)
    return synthetic_check(resolve(args.outdir))


if __name__ == "__main__":
    raise SystemExit(main())
