#!/usr/bin/env python3
"""Run the V45 synthetic/software guardrail regression suite."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v45_regression_aggregator"


def run_step(name: str, args: list[str]) -> dict[str, object]:
    start = time.time()
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    elapsed = time.time() - start
    return {
        "step": name,
        "command": " ".join(args),
        "returncode": result.returncode,
        "elapsed_seconds": round(elapsed, 3),
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    steps = [
        ("primary_harness_regression", [py, "scripts/v45_primary_harness_regression_tests.py"]),
        ("secondary_and_context_harness_regression", [py, "scripts/v45_harness_regression_tests.py"]),
        ("intake_preflight_regression", [py, "scripts/v45_preflight_regression_tests.py"]),
        (
            "checksum_manifest_synthetic",
            [py, "scripts/v45_checksum_manifest_validator.py", "synthetic-check", "--outdir", "analysis/v45_regression_aggregator/checksum_manifest"],
        ),
        (
            "response_column_synthetic",
            [py, "scripts/v45_response_column_audit.py", "synthetic-check", "--outdir", "analysis/v45_regression_aggregator/response_column"],
        ),
        (
            "subject_map_synthetic",
            [py, "scripts/v45_subject_map_sanity_check.py", "synthetic-check", "--outdir", "analysis/v45_regression_aggregator/subject_map"],
        ),
    ]
    rows = [run_step(name, args) for name, args in steps]
    table = pd.DataFrame(rows)
    table.to_csv(OUT / "regression_steps.tsv", sep="\t", index=False)
    summary = {
        "synthetic_or_software_regression_only": True,
        "n_steps": int(len(table)),
        "n_pass": int((table["status"] == "PASS").sum()),
        "n_fail": int((table["status"] == "FAIL").sum()),
        "total_elapsed_seconds": float(round(table["elapsed_seconds"].sum(), 3)),
        "overall_status": "PASS" if (table["status"] == "PASS").all() else "FAIL",
        "steps": table[["step", "status", "elapsed_seconds", "returncode"]].to_dict(orient="records"),
    }
    (OUT / "regression_aggregator_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
