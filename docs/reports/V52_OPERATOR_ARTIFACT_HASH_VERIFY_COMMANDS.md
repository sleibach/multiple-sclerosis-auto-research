# V52 Operator Artifact Hash Verification Commands

Date: 2026-07-10

Status: operational verification note. This document adds no biological,
genetics, structural, or validation evidence. It only defines how to check
whether the operator artifact hash snapshot still matches the current files.

## Purpose

`docs/reports/V52_OPERATOR_ARTIFACT_HASH_SNAPSHOT.tsv` freezes SHA256 hashes for
stable V52 operator artifacts that are likely to be handed to a data owner,
operator, or reviewer. It intentionally excludes mutable navigation documents
such as queue, status, index, and summary files.

Use this note before sending an operator package outside the repo, after editing
any stable operator artifact, and after any resume where package drift is
suspected.

## Verification Command

Run from the repository root:

```bash
python3 - <<'PY'
import csv
import hashlib
from pathlib import Path

snapshot = Path("docs/reports/V52_OPERATOR_ARTIFACT_HASH_SNAPSHOT.tsv")
bad = []

with snapshot.open(newline="") as handle:
    reader = csv.DictReader(handle, delimiter="\t")
    for row in reader:
        artifact = Path(row["artifact"])
        expected = row["sha256"]
        if not artifact.exists():
            actual = "MISSING"
        else:
            actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
        if actual != expected:
            bad.append((row["artifact"], expected, actual))

if bad:
    print({"hash_mismatch": bad})
    raise SystemExit(1)

print("hash_snapshot=PASS")
PY
```

Expected output when no stable operator artifact drifted:

```text
hash_snapshot=PASS
```

## Interpreting A Mismatch

A mismatch means the current file contents differ from the recorded snapshot. It
does not mean a scientific result changed. Classify the mismatch before sending
or using the package:

| cause | action |
|---|---|
| intentional operator artifact edit | rerun the command after regenerating the snapshot in a dedicated commit |
| accidental formatting or copy edit | review the diff and either revert the accidental change or regenerate the snapshot after accepting it |
| missing artifact | restore the artifact or remove it from the snapshot only if the package scope changed |
| navigation/status edit only | should not affect this snapshot; if it does, the snapshot included a mutable file by mistake |

## Regeneration Rule

Regenerate `docs/reports/V52_OPERATOR_ARTIFACT_HASH_SNAPSHOT.tsv` only after a
deliberate change to a stable operator artifact. Do not regenerate it merely to
make a mismatch disappear.

## Snapshot Scope

The snapshot currently covers stable monitoring, chr1, and OpenGWAS operator
artifacts. It does not cover:

1. live queue files;
2. current-status and next-action files;
3. navigation indexes;
4. summary cards;
5. generated health-check timing outputs.

Those files are expected to change during normal operation.

## Source Artifact

- `docs/reports/V52_OPERATOR_ARTIFACT_HASH_SNAPSHOT.tsv`
