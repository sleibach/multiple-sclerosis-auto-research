#!/usr/bin/env python3
"""Verify V53's mechanism regrade cannot leak into the frozen V22 rule."""

from __future__ import annotations

import ast
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v53_v22_interpretation_boundary"
LOCKED = ROOT / "docs/locked_rules/LOCKED_RULE_V22.md"
BASELINE = ROOT / "docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv"
HARNESS = ROOT / "scripts/v42_gafson_validation_harness.py"
PREREG = ROOT / "docs/validation/PREREGISTRATION_V42.md"
GRID = ROOT / "docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md"
EXPECTED_MODULES = {
    "IFN_APC": ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"],
    "HLAII": ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"],
    "RECEPTOR": ["CD74", "CD44", "CXCR4"],
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def module_constants(path: Path) -> dict[str, list[str]]:
    tree = ast.parse(path.read_text())
    found: dict[str, list[str]] = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if isinstance(target, ast.Name) and target.id in EXPECTED_MODULES:
            found[target.id] = list(ast.literal_eval(node.value))
    return found


def main() -> int:
    with BASELINE.open() as handle:
        baseline_rows = list(csv.DictReader(handle, delimiter="\t"))
    baseline = next(
        row
        for row in baseline_rows
        if row["path"] == "docs/locked_rules/LOCKED_RULE_V22.md"
    )
    current_hash = sha256(LOCKED)
    current_size = LOCKED.stat().st_size
    constants = module_constants(HARNESS)
    prereg_text = PREREG.read_text()
    grid_text = GRID.read_text()
    harness_text = HARNESS.read_text()

    checks = [
        {
            "check": "locked_rule_hash_matches_v45_baseline",
            "status": "PASS" if current_hash == baseline["sha256"] else "FAIL",
            "observed": current_hash,
            "expected": baseline["sha256"],
        },
        {
            "check": "locked_rule_size_matches_v45_baseline",
            "status": "PASS" if current_size == int(baseline["bytes"]) else "FAIL",
            "observed": current_size,
            "expected": baseline["bytes"],
        },
    ]
    for name, expected in EXPECTED_MODULES.items():
        checks.append(
            {
                "check": f"harness_{name}_genes_match_locked_definition",
                "status": "PASS" if constants.get(name) == expected else "FAIL",
                "observed": ";".join(constants.get(name, [])),
                "expected": ";".join(expected),
            }
        )
    checks.extend(
        [
            {
                "check": "harness_primary_score_excludes_receptor",
                "status": (
                    "PASS"
                    if 'out["v22_locked_signed_score"] = out["delta_HLAII"] - out["delta_IFN_APC"]'
                    in harness_text
                    else "FAIL"
                ),
                "observed": "delta_HLAII - delta_IFN_APC",
                "expected": "delta_HLAII - delta_IFN_APC",
            },
            {
                "check": "prereg_receptor_is_negative_control",
                "status": "PASS" if "Receptor-only negative control" in prereg_text else "FAIL",
                "observed": "present" if "Receptor-only negative control" in prereg_text else "missing",
                "expected": "present",
            },
            {
                "check": "outcome_grid_has_non_specific_downgrade",
                "status": "PASS" if "PASS_NON_SPECIFIC" in grid_text else "FAIL",
                "observed": "present" if "PASS_NON_SPECIFIC" in grid_text else "missing",
                "expected": "present",
            },
        ]
    )
    failures = sum(row["status"] == "FAIL" for row in checks)
    if failures:
        OUT.mkdir(parents=True, exist_ok=True)
        write_tsv(OUT / "interface_checks.tsv", checks)
        raise RuntimeError(f"V22/V53 interpretation-boundary audit failed {failures} checks")

    interpretations = [
        {
            "future_result": "V22_PASS_CLEAN",
            "allowed_current_interpretation": "Cohort supports the frozen early monitoring score under V42 criteria.",
            "not_established": "Independent HLA-II/receptor coupling; MIF causality; clinical threshold; therapeutic target.",
        },
        {
            "future_result": "V22_PASS_IMMUNE_TONE_BOUNDED",
            "allowed_current_interpretation": "Cohort supports an immune-tone-bounded early monitoring signal.",
            "not_established": "Pure APC/HLA mechanism; coupled two-arm architecture; MIF/CD74 target direction.",
        },
        {
            "future_result": "V22_PASS_NON_SPECIFIC",
            "allowed_current_interpretation": "A dynamic expression signal tracks response but fails specificity.",
            "not_established": "Intended V22 APC/HLA biology or any V53 receptor mechanism.",
        },
        {
            "future_result": "V22_FAIL_OR_INCONCLUSIVE",
            "allowed_current_interpretation": "Apply the frozen V42 failure/inconclusive wording only.",
            "not_established": "No post-hoc rescue by V53 modules, coupled scores, or structural context.",
        },
    ]
    summary = {
        "purpose": "V53 interface audit between the frozen V22 validation rule and revised mechanism context",
        "n_checks": len(checks),
        "n_fail": failures,
        "locked_rule_sha256": current_hash,
        "locked_rule_unchanged_from_v45_baseline": True,
        "primary_score_uses_receptor_module": False,
        "receptor_role": "negative_control_only",
        "v53_changes_score_or_threshold": False,
        "verdict": "V22_COMPUTATION_UNCHANGED_V53_ONLY_NARROWS_MECHANISTIC_INTERPRETATION",
        "boundary": "No locked rule, preregistration, harness formula, threshold, or result class was edited.",
    }

    OUT.mkdir(parents=True, exist_ok=True)
    write_tsv(OUT / "interface_checks.tsv", checks)
    write_tsv(OUT / "future_result_interpretation.tsv", interpretations)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# V53 V22 Interpretation Boundary",
        "",
        f"Verdict: **{summary['verdict']}**.",
        "",
        f"The locked-rule SHA-256 remains `{current_hash}` and matches the committed V45",
        "baseline. The V42 harness IFN/APC, HLA-II, and receptor gene lists match their",
        "frozen definitions. The primary Class-C score remains exactly `delta_HLAII -",
        "delta_IFN_APC`; receptor-only is a negative control and is not part of the score.",
        "",
        "V53 therefore changes no validation computation. It narrows what a future pass may",
        "mean: performance can support the frozen monitoring score, but cannot establish the",
        "demoted independent HLA-II/receptor architecture, MIF causality, clinical utility,",
        "or a therapeutic target. Existing V42 non-specific and immune-tone result classes",
        "already enforce this distinction.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
