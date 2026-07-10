# V52 Operator Artifact Hash Refresh Commands

Date: 2026-07-10

Status: operational command note. This document adds no evidence and does not
change any validation or target decision. It defines how to refresh the stable
operator artifact hash snapshot after an intentional operator-artifact edit.

## When To Use

Use this only after a deliberate change to a stable operator artifact. Do not
use it to hide unexplained drift. If the hash verification command fails and no
intentional edit was made, inspect the diff first.

## Current Stable Artifact List

The snapshot covers the V52 package intake, monitoring, chr1, OpenGWAS, and
hash-check artifacts listed in:

`docs/reports/V52_OPERATOR_ARTIFACT_HASH_SNAPSHOT.tsv`

## Refresh Command

Run from the repository root after intentional edits are reviewed:

```bash
python3 - <<'PY'
import csv
import hashlib
from pathlib import Path

snapshot = Path("docs/reports/V52_OPERATOR_ARTIFACT_HASH_SNAPSHOT.tsv")
rows = list(csv.DictReader(snapshot.open(), delimiter="\t"))
fieldnames = ["artifact", "sha256", "role", "frozen_status", "note"]

for row in rows:
    artifact = Path(row["artifact"])
    if not artifact.exists():
        raise SystemExit({"missing_artifact": row["artifact"]})
    row["sha256"] = hashlib.sha256(artifact.read_bytes()).hexdigest()

with snapshot.open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

print({"refreshed_hashes": len(rows), "snapshot": str(snapshot)})
PY
```

Then immediately run:

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

## Required Commit Shape

Commit the intentional artifact edit and the refreshed
`docs/reports/V52_OPERATOR_ARTIFACT_HASH_SNAPSHOT.tsv` together. The commit
message should name the operator artifact that changed. Do not commit a snapshot
refresh alone unless the only change is adding a newly frozen artifact to the
snapshot.

## Boundary

This command only refreshes hashes for already listed snapshot rows. It does not
decide whether an artifact should be frozen. Adding a new artifact to the
snapshot still requires a human-readable row with role and note.

## Related Artifact

- `docs/reports/V52_OPERATOR_ARTIFACT_HASH_VERIFY_COMMANDS.md`
