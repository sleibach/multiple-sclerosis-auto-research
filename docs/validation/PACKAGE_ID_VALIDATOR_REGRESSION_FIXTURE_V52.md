# Package ID Validator Regression Fixture V52

Date: 2026-07-10

Status: operational regression note. This document adds no biological evidence
and does not inspect real package data.

## Purpose

This fixture records the minimum pass/fail cases for
`scripts/v52_validate_package_id.py`. Rerun it after any edit to the package-ID
validator or file-naming policy.

## Expected Cases

| case | package_id | expected |
|---|---|---|
| valid Karolinska-style ID | `20260710_karolinska_dmf_manifest` | PASS |
| valid chr1-style ID | `20260710_chr1_collaborator_genotype_expression` | PASS |
| uppercase rejected | `20260710_Karolinska_DMF` | FAIL |
| missing date rejected | `karolinska_dmf_manifest` | FAIL |
| hyphen rejected | `20260710_karolinska-dmf` | FAIL |
| slash rejected | `20260710_karolinska/dmf` | FAIL |
| path traversal rejected | `20260710_../secret` | FAIL |
| double underscore rejected | `20260710_karolinska__dmf` | FAIL |
| trailing underscore rejected | `20260710_karolinska_` | FAIL |

## Rerun Command

```bash
python3 - <<'PY'
import csv
import subprocess
from pathlib import Path

cases = [
    ("valid_karolinska", "20260710_karolinska_dmf_manifest", "PASS"),
    ("valid_chr1", "20260710_chr1_collaborator_genotype_expression", "PASS"),
    ("invalid_uppercase", "20260710_Karolinska_DMF", "FAIL"),
    ("invalid_no_date", "karolinska_dmf_manifest", "FAIL"),
    ("invalid_hyphen", "20260710_karolinska-dmf", "FAIL"),
    ("invalid_slash", "20260710_karolinska/dmf", "FAIL"),
    ("invalid_dotdot", "20260710_../secret", "FAIL"),
    ("invalid_double_underscore", "20260710_karolinska__dmf", "FAIL"),
    ("invalid_trailing_underscore", "20260710_karolinska_", "FAIL"),
]
rows = []
for case, package_id, expected in cases:
    proc = subprocess.run(
        ["python3", "scripts/v52_validate_package_id.py", package_id],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    observed = "PASS" if proc.returncode == 0 else "FAIL"
    rows.append(
        {
            "case": case,
            "package_id": package_id,
            "expected_status": expected,
            "observed_status": observed,
            "stdout": proc.stdout.strip(),
        }
    )
out = Path("analysis/v52_package_id_validation/package_id_validation_checks.tsv")
out.parent.mkdir(parents=True, exist_ok=True)
with out.open("w", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=["case", "package_id", "expected_status", "observed_status", "stdout"],
        delimiter="\t",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
failures = [row for row in rows if row["expected_status"] != row["observed_status"]]
print({"out": str(out), "cases": len(rows), "failures": len(failures)})
if failures:
    raise SystemExit({"failures": failures})
PY
```

## Recorded Output

The current recorded fixture is
`analysis/v52_package_id_validation/package_id_validation_checks.tsv`.

Current result: 9 cases, 0 expectation failures.
