#!/usr/bin/env python3
"""Regression tests for the V45 validation intake preflight guard."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v45_preflight_regression_tests"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    subprocess.run(
        [
            sys.executable,
            "scripts/v45_validation_intake_preflight.py",
            "synthetic-check",
            "--outdir",
            str(OUT / "synthetic_check"),
        ],
        cwd=ROOT,
        check=True,
    )
    assertions = load_json(OUT / "synthetic_check" / "synthetic_check_assertions.json")
    primary = load_json(OUT / "synthetic_check" / "primary_preflight" / "preflight_summary.json")
    pharma = load_json(OUT / "synthetic_check" / "pharmacodynamic_preflight" / "preflight_summary.json")
    bad_pharma = load_json(
        OUT / "synthetic_check" / "pharmacodynamic_response_guard_preflight" / "preflight_summary.json"
    )

    checks = {
        "primary_preflight_pass": primary["overall_status"] == "PASS",
        "pharmacodynamic_preflight_pass": pharma["overall_status"] == "PASS",
        "pharmacodynamic_response_label_guard_fails": bad_pharma["overall_status"] == "FAIL",
        "primary_missing_checksum_count_zero": primary["missing_checksum_count"] == 0,
        "pharmacodynamic_missing_checksum_count_zero": pharma["missing_checksum_count"] == 0,
        "bad_pharmacodynamic_has_fail_count": bad_pharma["fail_count"] >= 1,
        "assertions_match": all(bool(v) for k, v in assertions.items() if k != "synthetic"),
        "no_module_scores_computed": assertions["no_module_scores_computed"] is True,
    }
    summary = {
        "synthetic": True,
        "preflight_synthetic_outdir": str((OUT / "synthetic_check").relative_to(ROOT)),
        "checks": checks,
        "primary_summary": primary,
        "pharmacodynamic_summary": pharma,
        "bad_pharmacodynamic_summary": bad_pharma,
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (OUT / "regression_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
