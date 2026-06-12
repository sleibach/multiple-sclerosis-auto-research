#!/usr/bin/env python3
"""Refresh V45 artifact, synthetic-artifact, and storage governance summaries."""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v45_governance_refresh"


COMMANDS = [
    {
        "name": "artifact_index",
        "command": [sys.executable, "scripts/v45_artifact_index.py"],
        "primary_output": "analysis/v45_artifact_index/summary.json",
    },
    {
        "name": "synthetic_artifact_index",
        "command": [sys.executable, "scripts/v45_synthetic_artifact_index.py"],
        "primary_output": "analysis/v45_synthetic_artifact_index/summary.json",
    },
    {
        "name": "compute_storage_summary",
        "command": [sys.executable, "scripts/v45_compute_storage_summary.py"],
        "primary_output": "analysis/v45_compute_storage_summary/summary.json",
    },
]


def run_command(spec: dict[str, object]) -> dict[str, object]:
    started = time.time()
    result = subprocess.run(
        spec["command"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    elapsed = round(time.time() - started, 3)
    output_path = ROOT / str(spec["primary_output"])
    parsed_output = None
    if output_path.exists():
        try:
            parsed_output = json.loads(output_path.read_text())
        except json.JSONDecodeError:
            parsed_output = None
    return {
        "name": spec["name"],
        "command": " ".join(spec["command"]),
        "returncode": result.returncode,
        "elapsed_seconds": elapsed,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
        "primary_output": spec["primary_output"],
        "primary_output_exists": output_path.exists(),
        "primary_output_summary": parsed_output,
        "status": "PASS" if result.returncode == 0 and output_path.exists() else "FAIL",
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [run_command(spec) for spec in COMMANDS]
    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    summary = {
        "purpose": "refresh V45 governance summaries; no biological claim",
        "overall_status": overall,
        "n_commands": len(rows),
        "commands": rows,
    }
    (OUT / "governance_refresh_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if overall == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
