#!/usr/bin/env python3
"""Verify the exact pre-existing V53 state referenced by V54 P1."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v54_progression_candidate_state_reference"
EXPECTED = {
    "docs/validation/MS_MICROGLIA_CD44_CXCR4_REPLICATION_SPEC_V53.md": "160c7b855ce52a6d01b96f0fdb97ae9bf0a2ffb09ff20665b9d457d76df126e3",
    "scripts/v53_analyze_macnair_microglia_replication.py": "df923fbbb0dff4f7863e59e7a8dc5aa4d62a3900008976c3dc7ac19dcb2252ea",
    "analysis/v53_ms_microglia_independent_cohort_scout/summary.json": "4b40ea71bd3deee1c14fb0c705ad881e85d3e068be8399aac9b04c7faef65bae",
}


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    hash_rows: list[dict[str, Any]] = []
    for relative, expected in EXPECTED.items():
        path = ROOT / relative
        observed = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "MISSING"
        hash_rows.append(
            {
                "artifact": relative,
                "expected_sha256": expected,
                "observed_sha256": observed,
                "exists": path.is_file(),
                "hash_match": observed == expected,
            }
        )

    spec = (ROOT / "docs/validation/MS_MICROGLIA_CD44_CXCR4_REPLICATION_SPEC_V53.md").read_text()
    implementation = (ROOT / "scripts/v53_analyze_macnair_microglia_replication.py").read_text()
    formula_checks = {
        "exact_genes_in_spec": "| CD44/CXCR4 receptor state | `CD44`, `CXCR4` | primary |" in spec,
        "zscore_then_mean_in_spec": "Z-score each gene across all eligible cohort samples\nbefore averaging genes." in spec,
        "no_substitution_in_spec": "Do not substitute genes." in spec,
        "microglia_compartment_in_spec": "Purified/sorted microglia" in spec,
        "exact_genes_in_implementation": '"receptor_cd44_cxcr4": ["CD44", "CXCR4"]' in implementation,
        "unweighted_mean_in_implementation": "z[usable].mean(axis=1)" in implementation,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "source_hashes.tsv", hash_rows)
    summary = {
        "purpose": "Verify V54 points to the exact pre-existing V53 CD44/CXCR4 state",
        "n_source_artifacts": len(hash_rows),
        "n_missing": sum(not row["exists"] for row in hash_rows),
        "n_hash_mismatch": sum(not row["hash_match"] for row in hash_rows),
        "n_formula_checks": len(formula_checks),
        "n_formula_checks_pass": sum(formula_checks.values()),
        "formula_checks": formula_checks,
        "compartment_boundary_explicit": formula_checks["microglia_compartment_in_spec"],
        "overall_status": "PASS" if all(row["hash_match"] for row in hash_rows) and all(formula_checks.values()) else "FAIL",
        "verdict": "EXACT_V53_STATE_REFERENCE_VERIFIED_MICROGLIA_ONLY",
        "boundary": "Identity verification only; no progression association, causal mechanism, intervention direction, target, or treatment evidence.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    if summary["overall_status"] != "PASS":
        raise RuntimeError("V54 candidate-state reference failed")


if __name__ == "__main__":
    main()
