# Therapeutic Package Handoff Link Audit V52

Date: 2026-07-10

Status: operational smoke audit. This document adds no evidence and runs no
package analysis. It records whether the package handoff bundle points only to
artifacts that exist in the repository.

## Command

Run from the repository root:

```bash
python3 - <<'PY'
import re
from pathlib import Path

bundle = Path("docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md")
text = bundle.read_text()
refs = sorted(set(re.findall(r"`([^`]+\\.(?:md|tsv))`", text)))
missing = [ref for ref in refs if not Path(ref).exists()]
print({"bundle": str(bundle), "refs": len(refs), "missing": missing})
if missing:
    raise SystemExit(1)
PY
```

## Result

Executed on 2026-07-10:

```text
{'bundle': 'docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md', 'refs': 26, 'missing': []}
```

Interpretation: all 26 linked handoff-bundle artifacts resolved locally at the
time of the audit.

## Boundary

This audit checks path existence only. It does not validate package contents,
does not run a validation harness, and does not decide whether any incoming data
package is scoreable.

## Source Artifact

- `docs/validation/THERAPEUTIC_PACKAGE_HANDOFF_BUNDLE_INDEX_V52.md`
