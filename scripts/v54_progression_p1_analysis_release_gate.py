#!/usr/bin/env python3
"""Compose V54 P1 lock, provenance, controls, and manifest into release."""

from __future__ import annotations

import csv
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import v54_progression_confirmation_provenance_gate as confirmation
import v54_progression_negative_control_gate as negative_control
import v54_progression_p1_intake_to_lock as intake_lock
import v54_progression_reference_manifest as reference_manifest


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_p1_analysis_release_gate"
MANIFEST = ROOT / "analysis/v54_progression_reference_manifest/manifest.json"


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def run_case(
    name: str,
    edits: dict[str, Any],
    output_dir: Path,
    manifest_summary: dict[str, Any],
    expected_contract_sha: str,
) -> dict[str, Any]:
    case_root = output_dir / "runs" / name
    upstream_edits: dict[str, Any] = {}
    if edits.get("continue_accrual"):
        upstream_edits["continue_accrual"] = True
    if edits.get("upstream_fail"):
        upstream_edits["site_fail"] = True
    if edits.get("upstream_cross_stage_mismatch"):
        upstream_edits["cross_stage_package_mismatch"] = True
    upstream = intake_lock.run_case(name, upstream_edits, case_root / "upstream")
    package_id = upstream["package_id"]

    confirmation_declaration = confirmation.base_declaration()
    confirmation_declaration["package_id"] = (
        "SYNTHETIC_DIFFERENT_PACKAGE"
        if edits.get("confirmation_package_mismatch")
        else package_id
    )
    if edits.get("confirmation_fail"):
        confirmation_declaration["confirmation_assessor_molecular_blinding"] = "unknown"
    confirmation_result = confirmation.validate(
        confirmation_declaration, case_root / "confirmation"
    )

    negative_declaration = negative_control.base_declaration()
    negative_declaration["package_id"] = (
        "SYNTHETIC_DIFFERENT_PACKAGE"
        if edits.get("negative_package_mismatch")
        else package_id
    )
    if edits.get("negative_fail"):
        negative_declaration["control_can_rescue_primary"] = True
    negative_result = negative_control.validate(
        negative_declaration, case_root / "negative_control"
    )

    current_manifest = deepcopy(manifest_summary)
    supplied_contract_sha = expected_contract_sha
    if edits.get("manifest_status_fail"):
        current_manifest["overall_status"] = "FAIL"
    if edits.get("manifest_hash_mismatch"):
        supplied_contract_sha = "0" * 64

    blockers: list[str] = []
    rows = []
    stage_values = [
        ("intake_to_lock", upstream.get("package_id"), upstream.get("decision")),
        ("confirmation_provenance", confirmation_result.get("package_id"), confirmation_result.get("decision")),
        ("negative_control", negative_result.get("package_id"), negative_result.get("decision")),
    ]
    for stage, observed_package, decision in stage_values:
        package_bound = observed_package == package_id
        if not package_bound:
            blockers.append(f"{stage}:package_id_mismatch")
        rows.append(
            {
                "stage": stage,
                "package_id": observed_package,
                "package_bound": package_bound,
                "decision": decision,
            }
        )
    if upstream["decision"] not in {
        "LOCK_READY_FOR_FROZEN_ANALYSIS",
        "CONTINUE_BLINDED_ACCRUAL",
    }:
        blockers.append(f"intake_to_lock:decision:{upstream['decision']}")
    if confirmation_result["decision"] != "PASS_CONFIRMATION_PROVENANCE_GATE":
        blockers.append(f"confirmation_provenance:decision:{confirmation_result['decision']}")
    if negative_result["decision"] != "PASS_FIXED_NEGATIVE_CONTROL_FAMILY":
        blockers.append(f"negative_control:decision:{negative_result['decision']}")
    if current_manifest.get("overall_status") != "PASS":
        blockers.append("reference_manifest:verification_failed")
    if supplied_contract_sha != expected_contract_sha:
        blockers.append("reference_manifest:contract_sha256_mismatch")

    blockers = sorted(set(blockers))
    if blockers:
        decision = "FAIL_CLOSED"
    elif upstream["decision"] == "CONTINUE_BLINDED_ACCRUAL":
        decision = "CONTINUE_BLINDED_ACCRUAL"
    else:
        decision = "RELEASE_READY_FOR_FROZEN_ANALYSIS"
    write_tsv(case_root / "stage_bindings.tsv", rows)
    summary = {
        "purpose": "V54 synthetic P1 analysis-release composition; no biological claim",
        "synthetic": True,
        "package_id": package_id,
        "reference_contract_sha256": supplied_contract_sha,
        "n_stages": len(stage_values) + 1,
        "n_blockers": len(blockers),
        "blockers": blockers,
        "upstream_decision": upstream["decision"],
        "decision": decision,
        "boundary": "Synthetic release routing only; release authorizes mechanical frozen analysis, not a favorable result, validation, progression evidence, or treatment effect.",
    }
    (case_root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def synthetic_regression(output_dir: Path = OUT) -> dict[str, Any]:
    manifest_summary = reference_manifest.evaluate(write=False)
    expected_contract_sha = json.loads(MANIFEST.read_text())["contract_sha256"]
    cases = [
        ("reference_release", {}, "RELEASE_READY_FOR_FROZEN_ANALYSIS"),
        ("continue_accrual", {"continue_accrual": True}, "CONTINUE_BLINDED_ACCRUAL"),
        ("upstream_failure", {"upstream_fail": True}, "FAIL_CLOSED"),
        ("confirmation_failure", {"confirmation_fail": True}, "FAIL_CLOSED"),
        ("negative_control_failure", {"negative_fail": True}, "FAIL_CLOSED"),
        ("confirmation_package_mismatch", {"confirmation_package_mismatch": True}, "FAIL_CLOSED"),
        ("negative_package_mismatch", {"negative_package_mismatch": True}, "FAIL_CLOSED"),
        ("manifest_status_failure", {"manifest_status_fail": True}, "FAIL_CLOSED"),
        ("manifest_hash_mismatch", {"manifest_hash_mismatch": True}, "FAIL_CLOSED"),
        ("upstream_cross_stage_mismatch", {"upstream_cross_stage_mismatch": True}, "FAIL_CLOSED"),
    ]
    rows: list[dict[str, Any]] = []
    for name, edits, expected in cases:
        result = run_case(
            name,
            deepcopy(edits),
            output_dir,
            manifest_summary,
            expected_contract_sha,
        )
        rows.append(
            {
                "fixture": name,
                "synthetic": True,
                "expected_decision": expected,
                "observed_decision": result["decision"],
                "n_blockers": result["n_blockers"],
                "regression_pass": result["decision"] == expected,
            }
        )
    write_tsv(output_dir / "synthetic_regression.tsv", rows)
    n_pass = sum(row["regression_pass"] for row in rows)
    summary = {
        "purpose": "Synthetic regression of V54 P1 analysis-release composition",
        "synthetic": True,
        "n_fixtures": len(rows),
        "n_pass": n_pass,
        "n_release_ready": sum(row["observed_decision"] == "RELEASE_READY_FOR_FROZEN_ANALYSIS" for row in rows),
        "n_continue_accrual": sum(row["observed_decision"] == "CONTINUE_BLINDED_ACCRUAL" for row in rows),
        "n_fail_closed": sum(row["observed_decision"] == "FAIL_CLOSED" for row in rows),
        "reference_contract_sha256": expected_contract_sha,
        "overall_status": "PASS" if n_pass == len(rows) else "FAIL",
        "boundary": "Synthetic composition behavior only; no patient data, validation result, progression evidence, target, or treatment effect.",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if summary["overall_status"] != "PASS":
        raise RuntimeError("V54 P1 analysis-release composition regression failed")
    return summary


if __name__ == "__main__":
    print(json.dumps(synthetic_regression(), indent=2))
