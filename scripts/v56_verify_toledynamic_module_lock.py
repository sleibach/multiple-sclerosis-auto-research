#!/usr/bin/env python3
"""Verify that the frozen ToleDYNAMIC module lock has not drifted."""

from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "docs/validation/TOLEDYNAMIC_MODULE_LOCK_V56.json"
DESIGN_LOCK = ROOT / "docs/validation/TOLEDYNAMIC_DESIGN_BRANCH_LOCK_V56.json"
SOURCE = ROOT / "scripts/v56_analyze_gse247181.py"
OUT = ROOT / "analysis/v56_toledynamic_module_lock"
PAYLOAD_FIELDS = (
    "cell_types",
    "coverage_rules",
    "family_slots",
    "modules",
    "primary_contrast",
    "score_rules",
)
DESIGN_PAYLOAD_FIELDS = (
    "branches",
    "durability_visit",
    "family_slots",
    "module_lock_binding",
    "primary_visit",
    "public_design_default",
    "source",
)


def extract_modules(path: Path) -> dict[str, list[str]]:
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "MODULES" for target in node.targets
        ):
            value = ast.literal_eval(node.value)
            if not isinstance(value, dict) or not all(
                isinstance(name, str)
                and isinstance(genes, list)
                and all(isinstance(gene, str) for gene in genes)
                for name, genes in value.items()
            ):
                raise ValueError("MODULES must be a literal string-to-string-list mapping")
            return value
    raise ValueError("literal MODULES assignment not found")


def canonical_payload(lock: dict[str, Any]) -> dict[str, Any]:
    return {field: lock[field] for field in PAYLOAD_FIELDS}


def payload_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def canonical_design_payload(lock: dict[str, Any]) -> dict[str, Any]:
    return {field: lock[field] for field in DESIGN_PAYLOAD_FIELDS}


def main() -> int:
    lock = json.loads(LOCK.read_text())
    design_lock = json.loads(DESIGN_LOCK.read_text())
    required = set(PAYLOAD_FIELDS) | {
        "boundary",
        "canonical_payload_sha256",
        "lock_version",
        "source_module_definition",
    }
    missing = sorted(required - set(lock))
    extracted = extract_modules(SOURCE)
    payload = canonical_payload(lock) if not missing else {}
    observed_hash = payload_hash(payload) if payload else ""
    design_required = set(DESIGN_PAYLOAD_FIELDS) | {
        "boundary",
        "canonical_payload_sha256",
        "lock_version",
    }
    design_missing = sorted(design_required - set(design_lock))
    design_payload = canonical_design_payload(design_lock) if not design_missing else {}
    observed_design_hash = payload_hash(design_payload) if design_payload else ""
    binding = design_lock.get("module_lock_binding", {})
    branches = design_lock.get("branches", {})
    branch_a = branches.get("BRANCH_A_RANDOMIZED_EXCEPTION", {})
    branch_b = branches.get("BRANCH_B_ACTIVE_ONLY_DEFAULT", {})
    checks = {
        "required_fields_present": not missing,
        "source_modules_exact_match": extracted == lock.get("modules"),
        "nine_modules": len(lock.get("modules", {})) == 9,
        "two_cell_types": lock.get("cell_types") == ["b_cell", "cd14_monocyte"],
        "family_slots_18": lock.get("family_slots") == 18,
        "canonical_hash_match": observed_hash == lock.get("canonical_payload_sha256"),
        "design_required_fields_present": not design_missing,
        "design_canonical_hash_match": observed_design_hash
        == design_lock.get("canonical_payload_sha256"),
        "design_binds_exact_module_lock": binding.get(
            "expected_canonical_payload_sha256"
        )
        == lock.get("canonical_payload_sha256"),
        "design_binds_module_lock_path": binding.get("path")
        == str(LOCK.relative_to(ROOT)),
        "public_default_is_active_only": design_lock.get("public_design_default")
        == "BRANCH_B_ACTIVE_ONLY_DEFAULT",
        "randomized_contrast_limited_to_branch_a": binding.get(
            "randomized_primary_contrast_authorized_only_in"
        )
        == "BRANCH_A_RANDOMIZED_EXCEPTION"
        and branch_a.get("primary_contrast") == lock.get("primary_contrast"),
        "active_only_contrast_is_paired_change": branch_b.get("primary_contrast")
        == "paired_month3_minus_baseline_change_among_tolebrutinib_treated_participants",
        "active_only_forbids_causal_claims": {
            "randomized_treatment_effect",
            "causal_treatment_mechanism",
            "clinical_mediation",
            "CNS_target_engagement",
            "individual_treatment_response_classifier",
        }.issubset(set(branch_b.get("forbidden_interpretations", []))),
        "design_family_matches_module_family": design_lock.get("family_slots")
        == lock.get("family_slots"),
    }
    failures = [name for name, passed in checks.items() if not passed]
    summary = {
        "purpose": "frozen module-lock drift verification; no biological evidence",
        "lock": str(LOCK.relative_to(ROOT)),
        "design_lock": str(DESIGN_LOCK.relative_to(ROOT)),
        "source": str(SOURCE.relative_to(ROOT)),
        "observed_canonical_payload_sha256": observed_hash,
        "observed_design_canonical_payload_sha256": observed_design_hash,
        "checks": checks,
        "n_fail": len(failures),
        "failures": failures,
        "overall_status": "PASS" if not failures else "FAIL",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
