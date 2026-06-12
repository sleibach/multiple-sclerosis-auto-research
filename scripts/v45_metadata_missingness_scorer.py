#!/usr/bin/env python3
"""Score metadata missingness against the V45 batch/QC/steroid rubric.

This script reads metadata columns only. It does not read expression values,
module scores, or outcome labels.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_metadata_missingness_scorer"

CORE_FIELDS = ["sample_id", "subject_id", "timepoint"]
MAJOR_BATCH_FIELDS = ["processing_batch", "library_prep_batch", "sequencing_lane", "plate_or_array_id"]
QC_FIELDS = ["rin_or_rna_quality", "sequencing_depth_or_reads"]
STEROID_FIELDS = ["steroid_exposure_recent", "steroid_last_dose_days"]
COMPOSITION_FIELDS = ["cbc_lymphocyte_count", "cbc_monocyte_count", "cbc_neutrophil_count"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    check = sub.add_parser("score")
    check.add_argument("--metadata", type=Path, required=True)
    check.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    check.add_argument("--fail-on-red", action="store_true")
    syn = sub.add_parser("synthetic-check")
    syn.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def missing_fraction(table: pd.DataFrame, field: str) -> float | None:
    if field not in table.columns:
        return None
    values = table[field].astype(str).str.strip().str.lower()
    return float(values.isin({"", "nan", "none", "null", "not_available"}).mean())


def best_missing_fraction(table: pd.DataFrame, fields: list[str]) -> tuple[str, float | None]:
    present = [(field, missing_fraction(table, field)) for field in fields if field in table.columns]
    if not present:
        return "", None
    return min(present, key=lambda item: item[1] if item[1] is not None else 1.0)


def row(area: str, severity: str, report_status: str, trigger: str, action: str) -> dict[str, str]:
    return {
        "rubric_area": area,
        "severity": severity,
        "report_status": report_status,
        "trigger": trigger,
        "required_action": action,
    }


def score_metadata(metadata: Path, outdir: Path, fail_on_red: bool) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    table = pd.read_csv(metadata, sep="\t").fillna("")
    rows: list[dict[str, str]] = []

    core_missing = [field for field in CORE_FIELDS if field not in table.columns or missing_fraction(table, field) != 0.0]
    if core_missing:
        rows.append(row("core_pairing", "red_unscoreable", "METADATA_UNSCOREABLE", f"missing_or_incomplete={';'.join(core_missing)}", "stop_before_scoring"))
    else:
        rows.append(row("core_pairing", "green", "PASS_BASIC_PAIRING", "sample_id_subject_id_timepoint_complete", "continue"))

    trt_missing = missing_fraction(table, "treatment_relative_day")
    nonbaseline_timepoints = set(table.get("timepoint", pd.Series(dtype=str)).astype(str).str.lower()) - {"baseline", "bl", ""}
    if trt_missing is None:
        severity = "orange_weak" if len(nonbaseline_timepoints) > 1 else "yellow_limited"
        status = "TIMEPOINT_AMBIGUOUS" if severity == "orange_weak" else "TIMEPOINT_APPROXIMATE"
        rows.append(row("early_timepoint", severity, status, "treatment_relative_day_absent", "clarify_early_sample_if_ambiguous"))
    elif trt_missing == 0.0:
        rows.append(row("early_timepoint", "green", "TIMEPOINT_INTERPRETABLE", "treatment_relative_day_complete", "continue"))
    elif trt_missing <= 0.25:
        rows.append(row("early_timepoint", "yellow_limited", "TIMEPOINT_APPROXIMATE", f"missing_fraction={trt_missing:.3f}", "report_timing_limitation"))
    else:
        rows.append(row("early_timepoint", "orange_weak", "TIMEPOINT_AMBIGUOUS", f"missing_fraction={trt_missing:.3f}", "request_timing_repair"))

    batch_field, batch_missing = best_missing_fraction(table, MAJOR_BATCH_FIELDS)
    if batch_missing is None:
        qc_field, qc_missing = best_missing_fraction(table, QC_FIELDS)
        rows.append(row("batch_diagnostic", "orange_weak", "BATCH_UNAVAILABLE", f"no_major_batch_field;best_qc={qc_field or 'none'}", "report_batch_unavailable"))
    elif batch_missing == 0.0:
        rows.append(row("batch_diagnostic", "green", "BATCH_INTERPRETABLE", f"best_field={batch_field}", "report_batch_diagnostic"))
    elif batch_missing <= 0.25:
        rows.append(row("batch_diagnostic", "yellow_limited", "BATCH_LIMITED", f"best_field={batch_field};missing_fraction={batch_missing:.3f}", "report_batch_limitation"))
    else:
        rows.append(row("batch_diagnostic", "orange_weak", "BATCH_UNAVAILABLE", f"best_field={batch_field};missing_fraction={batch_missing:.3f}", "report_batch_unavailable"))

    steroid_present = [(field, missing_fraction(table, field)) for field in STEROID_FIELDS if field in table.columns]
    if len(steroid_present) == 2 and all(frac == 0.0 for _, frac in steroid_present):
        rows.append(row("steroid_metadata", "green", "STEROID_INTERPRETABLE", "primary_steroid_fields_complete", "report_steroid_metadata_audit"))
    elif steroid_present and min(frac for _, frac in steroid_present) <= 0.25:
        rows.append(row("steroid_metadata", "yellow_limited", "STEROID_LIMITED", "partial_steroid_metadata", "report_direct_steroid_limitation"))
    elif "relapse_or_acute_treatment_near_sampling" in table.columns:
        rows.append(row("steroid_metadata", "orange_weak", "STEROID_METADATA_UNAVAILABLE", "primary_steroid_fields_absent_with_acute_treatment_proxy", "use_expression_signature_only"))
    else:
        rows.append(row("steroid_metadata", "orange_weak", "STEROID_METADATA_UNAVAILABLE", "primary_steroid_fields_absent", "use_expression_signature_only"))

    qc_field, qc_missing = best_missing_fraction(table, QC_FIELDS)
    if qc_missing is None:
        rows.append(row("qc_metadata", "orange_weak", "QC_UNAVAILABLE", "core_qc_fields_absent", "report_qc_unavailable"))
    elif qc_missing == 0.0:
        rows.append(row("qc_metadata", "green", "QC_INTERPRETABLE", f"best_field={qc_field}", "report_qc_diagnostic"))
    elif qc_missing <= 0.25:
        rows.append(row("qc_metadata", "yellow_limited", "QC_LIMITED", f"best_field={qc_field};missing_fraction={qc_missing:.3f}", "report_qc_limitation"))
    else:
        rows.append(row("qc_metadata", "orange_weak", "QC_UNAVAILABLE", f"best_field={qc_field};missing_fraction={qc_missing:.3f}", "report_qc_unavailable"))

    comp_field, comp_missing = best_missing_fraction(table, COMPOSITION_FIELDS)
    if comp_missing is None:
        rows.append(row("composition_context", "yellow_limited", "COMPOSITION_PROXY_ONLY", "direct_counts_absent", "require_expression_marker_proxy_downstream"))
    elif comp_missing == 0.0:
        rows.append(row("composition_context", "green", "COMPOSITION_INTERPRETABLE", f"best_field={comp_field}", "report_composition_audit"))
    else:
        rows.append(row("composition_context", "yellow_limited", "COMPOSITION_PROXY_ONLY", f"best_field={comp_field};missing_fraction={comp_missing:.3f}", "report_direct_count_limitation"))

    severities = [r["severity"] for r in rows]
    if any(sev == "red_unscoreable" for sev in severities):
        overall = row("overall", "red_unscoreable", "METADATA_UNSCOREABLE", "at_least_one_red_panel", "stop_or_classify_unscoreable")
    elif any(sev == "orange_weak" for sev in severities):
        overall = row("overall", "orange_weak", "METADATA_WEAK_FOR_CLEAN_PASS", "at_least_one_orange_panel", "do_not_call_positive_result_clean")
    elif sum(sev == "yellow_limited" for sev in severities) >= 2:
        overall = row("overall", "yellow_limited", "METADATA_LIMITED", "two_or_more_yellow_panels", "report_limitations")
    else:
        overall = row("overall", "green", "METADATA_SUPPORTS_CLEAN_INTERPRETATION", "no_or_one_yellow_panel", "continue")
    rows.append(overall)

    result = pd.DataFrame(rows)
    result.to_csv(outdir / "metadata_missingness_scores.tsv", sep="\t", index=False)
    summary = {
        "synthetic": "synthetic" in str(metadata).lower(),
        "purpose": "metadata missingness rubric scoring; no biological claim",
        "metadata": str(metadata.relative_to(ROOT)) if metadata.is_relative_to(ROOT) else str(metadata),
        "n_samples": int(len(table)),
        "overall_severity": overall["severity"],
        "overall_report_status": overall["report_status"],
        "n_red": int((result["severity"] == "red_unscoreable").sum()),
        "n_orange": int((result["severity"] == "orange_weak").sum()),
        "n_yellow": int((result["severity"] == "yellow_limited").sum()),
        "n_green": int((result["severity"] == "green").sum()),
        "overall_status": "FAIL" if overall["severity"] == "red_unscoreable" else "PASS_WITH_LIMITATIONS" if overall["severity"] != "green" else "PASS",
    }
    (outdir / "metadata_missingness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if fail_on_red and overall["severity"] == "red_unscoreable" else 0


def synthetic_check(outdir: Path) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    complete = outdir / "synthetic_complete_metadata.tsv"
    weak = outdir / "synthetic_weak_metadata.tsv"
    complete_rows = []
    for i in range(8):
        complete_rows.append(
            {
                "sample_id": f"S{i:03d}",
                "subject_id": f"P{i//2:03d}",
                "timepoint": "baseline" if i % 2 == 0 else "week6",
                "treatment_relative_day": 0 if i % 2 == 0 else 42,
                "processing_batch": f"B{i%2}",
                "library_prep_batch": f"L{i%2}",
                "sequencing_lane": f"lane{i%2}",
                "plate_or_array_id": f"plate{i%2}",
                "rin_or_rna_quality": 8.0,
                "sequencing_depth_or_reads": 20_000_000,
                "steroid_exposure_recent": "false",
                "steroid_last_dose_days": "not_applicable",
                "relapse_or_acute_treatment_near_sampling": "false",
                "cbc_lymphocyte_count": 1.5,
                "cbc_monocyte_count": 0.4,
                "cbc_neutrophil_count": 3.0,
            }
        )
    pd.DataFrame(complete_rows).to_csv(complete, sep="\t", index=False)
    weak_rows = [{k: v for k, v in row.items() if k not in {"treatment_relative_day", "processing_batch", "library_prep_batch", "sequencing_lane", "plate_or_array_id", "steroid_exposure_recent", "steroid_last_dose_days", "rin_or_rna_quality", "sequencing_depth_or_reads", "cbc_lymphocyte_count", "cbc_monocyte_count", "cbc_neutrophil_count"}} for row in complete_rows]
    for row in weak_rows:
        row["relapse_or_acute_treatment_near_sampling"] = "unknown"
    pd.DataFrame(weak_rows).to_csv(weak, sep="\t", index=False)
    score_metadata(complete, outdir / "complete_fixture", False)
    score_metadata(weak, outdir / "weak_fixture", False)
    summary = {
        "synthetic": True,
        "purpose": "metadata missingness scorer synthetic check; no biological claim",
        "complete_fixture": json.loads((outdir / "complete_fixture/metadata_missingness_summary.json").read_text())["overall_report_status"],
        "weak_fixture": json.loads((outdir / "weak_fixture/metadata_missingness_summary.json").read_text())["overall_report_status"],
    }
    (outdir / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return 0


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir if args.outdir.is_absolute() else ROOT / args.outdir)
    return score_metadata(
        args.metadata if args.metadata.is_absolute() else ROOT / args.metadata,
        args.outdir if args.outdir.is_absolute() else ROOT / args.outdir,
        args.fail_on_red,
    )


if __name__ == "__main__":
    raise SystemExit(main())
