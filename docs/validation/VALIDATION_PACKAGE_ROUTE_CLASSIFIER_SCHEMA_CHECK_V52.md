# Validation Package Route Classifier Schema Check V52

Date: 2026-07-10

Status: operational verification note. This document adds no evidence and runs
no package analysis. It provides a compact command to check that the V52 route
classifier and worked examples remain machine-readable and internally aligned.

## Command

Run from the repository root:

```bash
python3 - <<'PY'
import csv
from pathlib import Path

classifier_path = Path("docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv")
examples_path = Path("docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_EXAMPLES_V52.tsv")

classifier_required = [
    "route_class",
    "package_signal",
    "minimum_fields",
    "route_if_partial",
    "reject_or_context_only_if",
    "allowed_result_class",
    "primary_artifact",
    "forbidden_use",
    "next_action",
]
examples_required = [
    "example_id",
    "package_description",
    "key_fields_present",
    "key_fields_missing",
    "classifier_route",
    "allowed_interpretation",
    "forbidden_interpretation",
    "next_action",
]

def read_tsv(path, required):
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != required:
            raise SystemExit({"bad_header": str(path), "found": reader.fieldnames, "expected": required})
        rows = list(reader)
    if not rows:
        raise SystemExit({"empty_table": str(path)})
    for i, row in enumerate(rows, start=2):
        empty = [col for col in required if not row.get(col)]
        if empty:
            raise SystemExit({"empty_cells": str(path), "line": i, "columns": empty})
    return rows

classifier_rows = read_tsv(classifier_path, classifier_required)
example_rows = read_tsv(examples_path, examples_required)

routes = [row["route_class"] for row in classifier_rows]
if len(routes) != len(set(routes)):
    raise SystemExit({"duplicate_route_class": routes})

example_routes = {row["classifier_route"] for row in example_rows}
missing = sorted(example_routes - set(routes))
if missing:
    raise SystemExit({"example_route_without_classifier": missing})

for row in classifier_rows:
    artifact = Path(row["primary_artifact"])
    if not artifact.exists():
        raise SystemExit({"missing_primary_artifact": row["route_class"], "artifact": str(artifact)})

print({
    "classifier_rows": len(classifier_rows),
    "example_rows": len(example_rows),
    "status": "PASS",
})
PY
```

Expected output:

```text
{'classifier_rows': 9, 'example_rows': 10, 'status': 'PASS'}
```

## What This Checks

1. required headers are unchanged;
2. no row has an empty required cell;
3. route classes are unique;
4. every worked example points to an existing route class;
5. every classifier row points to an existing primary artifact.

## What This Does Not Check

This command does not inspect any incoming data, does not run a validation
harness, and does not decide whether a package is scoreable. It only keeps the
route-classifier tables internally consistent.

## Source Tables

- `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv`
- `docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_EXAMPLES_V52.tsv`
