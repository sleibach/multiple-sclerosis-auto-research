#!/usr/bin/env python3
"""Run V50 public-facing guard checks together.

This wrapper runs:

1. V50 status freshness lint.
2. V50 non-OpenGWAS public route checks.

The output is operational guard metadata only. It does not create biological
evidence and does not call OpenGWAS.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis" / "v50_public_guards"


def run_command(label: str, command: list[str]) -> dict[str, Any]:
    started = time.time()
    proc = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    elapsed_ms = int((time.time() - started) * 1000)
    return {
        "label": label,
        "command": command,
        "returncode": proc.returncode,
        "elapsed_ms": elapsed_ms,
        "status": "PASS" if proc.returncode == 0 else "FAIL",
        "stdout_tail": proc.stdout[-2000:],
        "stderr_tail": proc.stderr[-2000:],
    }


def write_tsv(rows: list[dict[str, Any]], path: Path) -> None:
    fields = ["label", "status", "returncode", "elapsed_ms", "command", "stderr_tail"]
    with path.open("w", encoding="utf-8") as handle:
        handle.write("\t".join(fields) + "\n")
        for row in rows:
            handle.write(
                "\t".join(
                    str(row.get(field, "")).replace("\t", " ").replace("\n", " ")
                    for field in fields
                )
                + "\n"
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["run"])
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    status_outdir = outdir / "status_freshness"
    route_outdir = outdir / "non_opengwas_routes"

    commands = [
        (
            "status_freshness",
            [
                sys.executable,
                "scripts/v50_status_freshness_linter.py",
                "lint",
                "--outdir",
                str(status_outdir),
                "--fail-on-error",
            ],
        ),
        (
            "non_opengwas_routes",
            [
                sys.executable,
                "scripts/v50_check_non_opengwas_routes.py",
                "check",
                "--outdir",
                str(route_outdir),
                "--fail-on-error",
            ],
        ),
    ]

    rows = [run_command(label, command) for label, command in commands]
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    tsv_path = outdir / "public_guard_results.tsv"
    write_tsv(rows, tsv_path)
    summary = {
        "purpose": "V50 public guard wrapper; status and public-route checks only; no biological claim",
        "synthetic": False,
        "checked_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "open_gwas_used": False,
        "results": str(tsv_path.relative_to(ROOT)),
        "status_freshness_outdir": str(status_outdir.relative_to(ROOT)),
        "non_opengwas_routes_outdir": str(route_outdir.relative_to(ROOT)),
    }
    summary_path = outdir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and n_fail:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
