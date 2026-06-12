#!/usr/bin/env python3
"""Run the V45 pre-commit readiness guard sequence."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v45_precommit_readiness"


def run_step(name: str, args: list[str]) -> dict[str, object]:
    start = time.time()
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True)
    elapsed = round(time.time() - start, 3)
    return {
        "step": name,
        "command": " ".join(args),
        "returncode": result.returncode,
        "elapsed_seconds": elapsed,
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    steps = [
        ("no_raw_git_scanner", [py, "scripts/v45_no_raw_git_scanner.py"]),
        (
            "locked_artifact_hash_audit",
            [
                py,
                "scripts/v45_locked_artifact_hash_audit.py",
                "audit",
                "--baseline",
                "docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv",
                "--outdir",
                "analysis/v45_locked_artifact_hash_audit",
                "--fail-on-drift",
            ],
        ),
        ("regression_aggregator", [py, "scripts/v45_regression_aggregator.py"]),
        (
            "command_plan_consistency",
            [py, "scripts/v45_command_plan_consistency_check.py", "--outdir", "analysis/v45_command_plan_consistency"],
        ),
        ("governance_refresh", [py, "scripts/v45_refresh_governance_summaries.py"]),
    ]
    rows = [run_step(name, args) for name, args in steps]
    table = pd.DataFrame(rows)
    table.to_csv(OUT / "precommit_readiness_steps.tsv", sep="\t", index=False)
    summary = {
        "purpose": "V45 pre-commit readiness guard; no biological claim",
        "n_steps": int(len(table)),
        "n_pass": int((table["status"] == "PASS").sum()),
        "n_fail": int((table["status"] == "FAIL").sum()),
        "total_elapsed_seconds": float(round(table["elapsed_seconds"].sum(), 3)),
        "overall_status": "PASS" if (table["status"] == "PASS").all() else "FAIL",
        "steps": table[["step", "status", "elapsed_seconds", "returncode"]].to_dict(orient="records"),
    }
    (OUT / "precommit_readiness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
