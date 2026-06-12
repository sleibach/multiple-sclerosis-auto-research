#!/usr/bin/env python3
"""Generate a manifest of expected V45 gate outputs for handoff."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


MODE_EXTRA_GATES = {
    "primary": [],
    "pharmacodynamic": [
        (
            "response_column_audit",
            "analysis/validation_command_runs/response_column_audit/{cohort_id}/response_column_audit_summary.json",
            "PASS for context-only packages with no response-like columns",
        )
    ],
    "postpartum": [],
    "tb": [],
}


COMMON_GATES = [
    (
        "data_use_terms",
        "data/quarantine/{cohort_id}/governance/data_use_terms_summary.tsv",
        "status=approved_for_preflight",
    ),
    (
        "checksum_manifest",
        "analysis/validation_command_runs/checksum_manifest/{cohort_id}/manifest_audit_summary.json",
        "overall_status=PASS",
    ),
    (
        "intake_preflight",
        "analysis/validation_command_runs/intake_preflight/{cohort_id}/preflight_summary.json",
        "overall_status=PASS",
    ),
    (
        "module_coverage_precheck",
        "analysis/validation_command_runs/module_coverage/{cohort_id}/module_coverage_precheck_summary.json",
        "overall_status=PASS when expression matrix is used",
    ),
    (
        "subject_map_sanity",
        "analysis/validation_command_runs/subject_map_sanity/{cohort_id}/subject_map_summary.json",
        "overall_status=PASS when paired deltas are required",
    ),
    (
        "outcome_dictionary",
        "data/quarantine/{cohort_id}/metadata/outcome_label_dictionary.tsv",
        "frozen before response scoring",
    ),
    (
        "locked_artifact_hash_audit",
        "analysis/v45_locked_artifact_hash_audit/locked_artifact_hash_audit_summary.json",
        "overall_status=PASS",
    ),
    (
        "precommit_readiness",
        "analysis/v45_precommit_readiness/precommit_readiness_summary.json",
        "overall_status=PASS",
    ),
]


HARNESS_OUTPUTS = [
    (
        "validation_summary",
        "analysis/validation_runs/{cohort_id}/validation_summary.json",
        "written by frozen harness after all gates pass",
    ),
    (
        "validation_result_report",
        "analysis/validation_runs/{cohort_id}/VALIDATION_RESULT_REPORT.md",
        "filled from V45 template after frozen harness run",
    ),
]


def build_rows(cohort_id: str, mode: str) -> list[dict[str, object]]:
    gate_specs = COMMON_GATES[:3] + MODE_EXTRA_GATES[mode] + COMMON_GATES[3:] + HARNESS_OUTPUTS
    rows = []
    for gate, template, expected in gate_specs:
        path_text = template.format(cohort_id=cohort_id)
        path = ROOT / path_text
        rows.append(
            {
                "cohort_id": cohort_id,
                "mode": mode,
                "gate_or_output": gate,
                "path": path_text,
                "expected_status_or_role": expected,
                "exists_now": path.exists(),
                "handoff_required": gate not in {"validation_summary", "validation_result_report"},
                "interpretation": "gate/handoff manifest only; no biological claim",
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cohort-id", required=True)
    parser.add_argument("--mode", choices=sorted(MODE_EXTRA_GATES), required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()

    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    table = pd.DataFrame(build_rows(args.cohort_id, args.mode))
    table.to_csv(outdir / "gate_output_bundle_manifest.tsv", sep="\t", index=False)
    summary = {
        "cohort_id": args.cohort_id,
        "mode": args.mode,
        "n_rows": int(len(table)),
        "n_present_now": int(table["exists_now"].sum()),
        "n_missing_now": int((~table["exists_now"]).sum()),
        "overall_status": "MANIFEST_ONLY",
        "note": "Missing rows are expected before data receipt; this manifest does not run validation.",
    }
    (outdir / "gate_output_bundle_manifest_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
