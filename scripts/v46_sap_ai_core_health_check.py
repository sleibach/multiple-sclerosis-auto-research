#!/usr/bin/env python3
"""Run the V46 SAP AI Core health check with model-family-specific commands.

This is infrastructure/readiness only. It verifies access paths for Claude,
Gemini, and SAP RPT without treating any model output as evidence.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis" / "v46_sap_ai_core_health_check"


CHECKS = [
    {
        "model_family": "claude_orchestration",
        "model": "anthropic--claude-4.7-opus",
        "command_kind": "smoke",
        "timeout_seconds": 60,
        "max_output_tokens": 64,
        "expected_text": "OK",
    },
    {
        "model_family": "gemini_native",
        "model": "gemini-2.5-pro",
        "command_kind": "smoke",
        "timeout_seconds": 60,
        "max_output_tokens": 256,
        "expected_text": "OK",
    },
    {
        "model_family": "sap_rpt_predict",
        "model": "sap-rpt-1-large",
        "command_kind": "rpt-smoke",
        "timeout_seconds": 120,
        "max_output_tokens": None,
        "expected_text": "\"status\"",
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def command_for(check: dict[str, object]) -> list[str]:
    py = sys.executable
    if check["command_kind"] == "rpt-smoke":
        return [
            py,
            "scripts/sap_ai_core_client.py",
            "rpt-smoke",
            "--model",
            str(check["model"]),
            "--timeout",
            str(check["timeout_seconds"]),
        ]
    if check["command_kind"] == "smoke":
        return [
            py,
            "scripts/sap_ai_core_client.py",
            "smoke",
            "--model",
            str(check["model"]),
            "--timeout",
            str(check["timeout_seconds"]),
            "--max-output-tokens",
            str(check["max_output_tokens"]),
        ]
    raise ValueError(f"Unsupported command_kind: {check['command_kind']}")


def run_check(check: dict[str, object]) -> dict[str, object]:
    command = command_for(check)
    started = time.time()
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    elapsed = round(time.time() - started, 3)
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    expected_text = str(check["expected_text"])
    family_specific_guard = "PASS"
    if check["model_family"] == "sap_rpt_predict" and "No implemented request schema" in (stdout + stderr):
        family_specific_guard = "FAIL"
    expected_guard = "PASS" if expected_text in stdout else "FAIL"
    status = "PASS" if proc.returncode == 0 and expected_guard == "PASS" and family_specific_guard == "PASS" else "FAIL"
    return {
        "model_family": check["model_family"],
        "model": check["model"],
        "command_kind": check["command_kind"],
        "command": " ".join(command),
        "returncode": proc.returncode,
        "elapsed_seconds": elapsed,
        "expected_text_present": expected_guard == "PASS",
        "family_specific_guard": family_specific_guard,
        "status": status,
        "stdout_tail": stdout[-2000:] or "(empty)",
        "stderr_tail": stderr[-2000:] or "(empty)",
    }


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    rows = [run_check(check) for check in CHECKS]
    fieldnames = [
        "model_family",
        "model",
        "command_kind",
        "command",
        "returncode",
        "elapsed_seconds",
        "expected_text_present",
        "family_specific_guard",
        "status",
        "stdout_tail",
        "stderr_tail",
    ]
    write_tsv(outdir / "sap_ai_core_health_checks.tsv", rows, fieldnames)
    summary = {
        "purpose": "V46 SAP AI Core model-family-specific health check; no biological claim",
        "checks": len(rows),
        "pass_count": sum(1 for row in rows if row["status"] == "PASS"),
        "fail_count": sum(1 for row in rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
        "important_operational_rule": (
            "Use sap_ai_core_client.py rpt-smoke for sap-rpt-1-large; the generic "
            "smoke command is for LLM-style text generation and will correctly "
            "reject RPT as an unsupported generation schema."
        ),
        "outputs": [rel(outdir / "sap_ai_core_health_checks.tsv")],
    }
    (outdir / "sap_ai_core_health_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if args.fail_on_error and summary["overall_status"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
