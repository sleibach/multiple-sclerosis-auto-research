# Package Intake CLI Help Refresh Note V52

Date: 2026-07-10

Status: operational refresh note. This document adds no biological evidence,
does not inspect package data, and does not alter any validation rule or
therapeutic verdict.

## Purpose

The package-intake CLI help snapshot is a generated drift check. When an intake
script is added or its options intentionally change, regenerate the committed
help snapshot mechanically rather than hand-editing the TSV.

## Covered Output

`analysis/v52_package_intake_cli_help_snapshot/cli_help_snapshot.tsv`

## Refresh Command

```bash
python3 - <<'PY'
import csv
import subprocess
from pathlib import Path

commands = [
    ("package_id_validator", ["python3", "scripts/v52_validate_package_id.py", "--help"]),
    ("route_classifier", ["python3", "scripts/v52_package_route_classifier.py", "--help"]),
    ("intake_safety_audit", ["python3", "scripts/v52_received_intake_safety_audit.py", "--help"]),
    ("route_output_schema_audit", ["python3", "scripts/v52_route_output_schema_audit.py", "--help"]),
]

out = Path("analysis/v52_package_intake_cli_help_snapshot/cli_help_snapshot.tsv")
rows = []
for name, cmd in commands:
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    rows.append(
        {
            "script": name,
            "command": " ".join(cmd),
            "returncode": str(proc.returncode),
            "contains_usage": str("usage:" in proc.stdout.lower()),
            "stdout_summary": " | ".join(proc.stdout.strip().splitlines()),
        }
    )

with out.open("w", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=["script", "command", "returncode", "contains_usage", "stdout_summary"],
        delimiter="\t",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)

failures = [row for row in rows if row["returncode"] != "0" or row["contains_usage"] != "True"]
print({"wrote": str(out), "rows": len(rows), "failures": len(failures)})
raise SystemExit(1 if failures else 0)
PY
```

## Boundary

This only refreshes command-help text for package-intake scripts. It does not
validate package suitability, access terms, route eligibility, or biological
results.
