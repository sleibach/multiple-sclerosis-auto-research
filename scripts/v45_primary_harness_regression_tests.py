#!/usr/bin/env python3
"""Regression test wrapper for the primary V42/Gafson validation harness.

This executes the existing seeded synthetic null/planted check and asserts the
main invariants. It is infrastructure only and does not analyze real data.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v45_primary_harness_regression_tests"

EXPECTED_RESULT_FILES = [
    "validation_summary.json",
    "paired_module_deltas.tsv",
    "gene_mapping_coverage.tsv",
    "sample_attrition.tsv",
    "locked_rule_metrics.tsv",
    "confounder_adjustment_metrics.tsv",
    "joint_confounder_metrics.tsv",
    "batch_diagnostic_metrics.tsv",
]


def run_cmd(args: list[str]) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def assert_true(name: str, value: bool, failures: list[str]) -> None:
    if not bool(value):
        failures.append(name)


def files_present(result_dir: Path) -> list[str]:
    return [name for name in EXPECTED_RESULT_FILES if (result_dir / name).exists()]


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    v42_out = OUT / "v42_primary_synthetic"
    run_cmd(
        [
            sys.executable,
            "scripts/v42_gafson_validation_harness.py",
            "synthetic-check",
            "--outdir",
            str(v42_out),
        ]
    )

    synthetic_summary = load_json(v42_out / "synthetic_check_summary.json")
    null_summary = load_json(v42_out / "null_result" / "validation_summary.json")
    planted_summary = load_json(v42_out / "planted_result" / "validation_summary.json")

    null_files = files_present(v42_out / "null_result")
    planted_files = files_present(v42_out / "planted_result")

    failures: list[str] = []
    assert_true("null_expected_fail", synthetic_summary.get("null_expected_fail") is True, failures)
    assert_true("planted_expected_pass", synthetic_summary.get("planted_expected_pass") is True, failures)
    assert_true("null_verdict_not_pass", null_summary.get("final_verdict") not in {"PASS_CLEAN", "PASS_PROVISIONAL_SMALL_N"}, failures)
    assert_true("planted_verdict_pass_clean", planted_summary.get("final_verdict") == "PASS_CLEAN", failures)
    assert_true("null_n_60", null_summary.get("n") == 60, failures)
    assert_true("planted_n_60", planted_summary.get("n") == 60, failures)
    assert_true("null_auc_near_random", 0.35 <= float(null_summary.get("primary_auc", -1)) <= 0.65, failures)
    assert_true("planted_auc_high", float(planted_summary.get("primary_auc", 0)) >= 0.95, failures)
    assert_true("null_result_files_present", set(null_files) == set(EXPECTED_RESULT_FILES), failures)
    assert_true("planted_result_files_present", set(planted_files) == set(EXPECTED_RESULT_FILES), failures)

    summary = {
        "synthetic": True,
        "v42_primary_outdir": str(v42_out.relative_to(ROOT)),
        "expected_result_files": EXPECTED_RESULT_FILES,
        "null_files_present": null_files,
        "planted_files_present": planted_files,
        "null_summary": {
            "final_verdict": null_summary.get("final_verdict"),
            "n": null_summary.get("n"),
            "primary_auc": null_summary.get("primary_auc"),
            "primary_hedges_g": null_summary.get("primary_hedges_g"),
            "receptor_auc": null_summary.get("receptor_auc"),
        },
        "planted_summary": {
            "final_verdict": planted_summary.get("final_verdict"),
            "n": planted_summary.get("n"),
            "primary_auc": planted_summary.get("primary_auc"),
            "primary_hedges_g": planted_summary.get("primary_hedges_g"),
            "receptor_auc": planted_summary.get("receptor_auc"),
        },
        "failures": failures,
        "overall_status": "PASS" if not failures else "FAIL",
    }
    (OUT / "regression_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
