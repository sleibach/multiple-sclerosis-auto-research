#!/usr/bin/env python3
"""Verify that the committed V56 closeout artifacts agree with one another."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v56_closeout_consistency/summary.json"


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())


def read_tsv(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def main() -> None:
    pbmc = read_tsv(
        "analysis/v56_gse247181_progression_modules/primary_rapid_vs_slow.tsv"
    )
    brl_primary = read_tsv(
        "analysis/v56_gse281805_brl_modules/primary_brl_vs_mixed.tsv"
    )
    brl_sensitivity = read_tsv(
        "analysis/v56_gse281805_brl_modules/post_result_common_slide_sensitivity.tsv"
    )
    calibration = read_json(
        "analysis/v56_gse281805_raw_reconstruction/calibration_summary.json"
    )
    lock_summary = read_json("analysis/v56_toledynamic_module_lock/summary.json")
    module_lock = read_json("docs/validation/TOLEDYNAMIC_MODULE_LOCK_V56.json")
    design_lock = read_json(
        "docs/validation/TOLEDYNAMIC_DESIGN_BRANCH_LOCK_V56.json"
    )
    power = read_json("analysis/v56_toledynamic_power_envelope/summary.json")
    ledger = read_tsv("docs/reports/PROGRESSION_THERAPY_OUTCOMES_V56.tsv")
    rag = read_json("knowledge/.index/manifest.json")
    report = (ROOT / "docs/reports/PROGRESSION_THERAPY_OPPORTUNITY_V56.md").read_text()
    index_text = (ROOT / "docs/reports/PROGRESSION_THERAPY_INDEX_V56.md").read_text()
    readme = (ROOT / "README.md").read_text()
    queue = (ROOT / "meta/V56_QUEUE.md").read_text()
    index_local_references = sorted({
        token
        for token in re.findall(r"`([^`]+)`", index_text)
        if "/" in token and " " not in token and not token.startswith("http")
    })
    missing_index_references = [
        token for token in index_local_references if not (ROOT / token).exists()
    ]

    checks = {
        "pbmc_has_nine_frozen_modules": len(pbmc) == 9,
        "pbmc_all_not_supported": all(row["verdict"] == "not_supported" for row in pbmc),
        "pbmc_exact_assignment_count": all(
            int(row["n_exact_assignments"]) == 184_756 for row in pbmc
        ),
        "brl_primary_has_four_gate_passes": sum(
            row["verdict"] == "brl_specific_gate_pass" for row in brl_primary
        ) == 4,
        "brl_common_slide_has_no_gate_pass": all(
            row["verdict"] != "sensitivity_gate_pass" for row in brl_sensitivity
        ),
        "raw_reconstruction_failed_calibration": calibration["calibration_pass"] is False,
        "raw_biological_output_absent": not (
            ROOT / "analysis/v56_gse281805_raw_reconstruction/aoi_module_scores.tsv"
        ).exists(),
        "module_lock_hash_matches_verifier": (
            module_lock["canonical_payload_sha256"]
            == lock_summary["observed_canonical_payload_sha256"]
        ),
        "design_lock_hash_matches_verifier": (
            design_lock["canonical_payload_sha256"]
            == lock_summary["observed_design_canonical_payload_sha256"]
        ),
        "active_only_is_public_default": (
            design_lock["public_design_default"] == "BRANCH_B_ACTIVE_ONLY_DEFAULT"
        ),
        "power_is_synthetic_method_only": power["synthetic"] is True,
        "both_null_fwer_calibrated": (
            power["null_fwer_range_over_designs"][0] <= 0.05
            <= power["null_fwer_range_over_designs"][1]
        ),
        "paired_null_fwer_calibrated": (
            power["paired_trajectory_null_fwer_range_over_designs"][0] <= 0.05
            <= power["paired_trajectory_null_fwer_range_over_designs"][1]
        ),
        "ledger_uses_only_grounded_or_synthetic_method": set(
            row["epistemic_layer"] for row in ledger
        ) <= {"grounded", "synthetic_method"},
        "rag_has_v56_closeout": rag["document_count"] >= 988,
        "rag_globs_exclude_external_tree": all(
            not pattern.startswith("knowledge_external") for pattern in rag["globs"]
        ),
        "report_states_no_progression_route": (
            "did **not** identify a project-grounded route to halt MS progression"
            in report
        ),
        "index_local_references_exist": not missing_index_references,
        "readme_points_to_v56": "meta/V56_QUEUE.md" in readme,
        "queue_records_current_design_hash": "1d7734...45c9" in queue,
    }
    failures = sorted(name for name, passed in checks.items() if not passed)
    summary = {
        "purpose": "cross-artifact V56 closeout consistency; no new biological evidence",
        "n_checks": len(checks),
        "n_fail": len(failures),
        "overall_status": "PASS" if not failures else "FAIL",
        "checks": checks,
        "failures": failures,
        "index_local_reference_count": len(index_local_references),
        "missing_index_references": missing_index_references,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
