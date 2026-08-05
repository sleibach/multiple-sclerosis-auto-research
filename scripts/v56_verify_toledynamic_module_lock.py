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


def main() -> int:
    lock = json.loads(LOCK.read_text())
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
    checks = {
        "required_fields_present": not missing,
        "source_modules_exact_match": extracted == lock.get("modules"),
        "nine_modules": len(lock.get("modules", {})) == 9,
        "two_cell_types": lock.get("cell_types") == ["b_cell", "cd14_monocyte"],
        "family_slots_18": lock.get("family_slots") == 18,
        "canonical_hash_match": observed_hash == lock.get("canonical_payload_sha256"),
    }
    failures = [name for name, passed in checks.items() if not passed]
    summary = {
        "purpose": "frozen module-lock drift verification; no biological evidence",
        "lock": str(LOCK.relative_to(ROOT)),
        "source": str(SOURCE.relative_to(ROOT)),
        "observed_canonical_payload_sha256": observed_hash,
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
