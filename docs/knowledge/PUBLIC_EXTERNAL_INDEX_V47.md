# V47 Public External Index

Status: navigation infrastructure only.

`scripts/v47_public_external_index.py` builds `knowledge_external/INDEX.md`, a
reader-facing index over the segregated external knowledge tree. The index links
only external-tree artifacts and repeats the boundary that external records are
`NOT_PROJECT_GROUNDED`.

Verification:

```bash
.venv/bin/python scripts/v47_public_external_index.py synthetic-check --fail-on-error
.venv/bin/python scripts/v47_public_external_index.py build
```

The generated index is not evidence and does not validate any external claim.

