#!/usr/bin/env python3
"""Regression tests for V45 validation/context harness guardrails.

These are infrastructure tests, not biological analyses. They execute existing
seeded synthetic checks and assert that null/planted/context-only invariants
still hold after future code edits.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v45_harness_regression_tests"


def run_cmd(args: list[str]) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def assert_true(name: str, value: bool, failures: list[str]) -> None:
    if not bool(value):
        failures.append(name)


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    py = sys.executable
    secondary_out = OUT / "secondary_real_ingest"
    pharma_out = OUT / "pharmacodynamic_only"

    run_cmd(
        [
            py,
            "scripts/v45_secondary_real_cohort_harness.py",
            "synthetic-check",
            "--outdir",
            str(secondary_out),
            "--n-boot",
            "120",
        ]
    )
    run_cmd(
        [
            py,
            "scripts/v45_pharmacodynamic_only_harness.py",
            "synthetic-check",
            "--outdir",
            str(pharma_out),
        ]
    )

    secondary = load_json(secondary_out / "synthetic_check_summary.json")
    pharma_summary = load_json(pharma_out / "synthetic_check" / "validation_summary.json")
    pharma_assertions = load_json(pharma_out / "synthetic_check" / "synthetic_check_assertions.json")

    failures: list[str] = []
    checks = secondary["checks"]
    assert_true("secondary_postpartum_null_expected_fail", checks["postpartum_null_expected_fail"], failures)
    assert_true("secondary_postpartum_planted_expected_pass", checks["postpartum_planted_expected_pass"], failures)
    assert_true("secondary_tb_null_expected_fail", checks["tb_null_expected_fail"], failures)
    assert_true("secondary_tb_planted_expected_pass", checks["tb_planted_expected_pass"], failures)

    assert_true("pharmacodynamic_context_only", pharma_summary["context_only"], failures)
    assert_true("pharmacodynamic_no_response_validation", not pharma_summary["response_validation_performed"], failures)
    assert_true("pharmacodynamic_paired_deltas_present", pharma_summary["n_paired_deltas"] == 24, failures)
    assert_true(
        "pharmacodynamic_assertions_all_true",
        all(bool(v) for v in pharma_assertions["checks"].values()),
        failures,
    )

    summary = {
        "synthetic": True,
        "secondary_real_ingest_outdir": str(secondary_out.relative_to(ROOT)),
        "pharmacodynamic_only_outdir": str(pharma_out.relative_to(ROOT)),
        "secondary_checks": checks,
        "pharmacodynamic_context_only": bool(pharma_summary["context_only"]),
        "pharmacodynamic_response_validation_performed": bool(pharma_summary["response_validation_performed"]),
        "pharmacodynamic_paired_deltas": int(pharma_summary["n_paired_deltas"]),
        "failures": failures,
        "overall_status": "PASS" if not failures else "FAIL",
    }
    (OUT / "regression_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
