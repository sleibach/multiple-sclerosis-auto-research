# Convergence / Contradiction Skeleton V47

This document describes the V47 skeleton that keeps external resource records
separate from grounded project findings until a future, explicit review links a
specific external claim to a specific grounded artifact.

The generated skeleton is intentionally placeholder-only:

- `project_finding_id` remains `UNLINKED_RESOURCE_METADATA_ONLY`;
- `synthesis_status` remains `placeholder_no_claim_conclusion`;
- no convergence, contradiction, support, or validation is inferred;
- every row preserves source and `NOT_PROJECT_GROUNDED`.

## Commands

```bash
.venv/bin/python scripts/v47_convergence_contradiction_skeleton.py synthetic-check --outdir analysis/v47_convergence_contradiction_skeleton --fail-on-error
.venv/bin/python scripts/v47_convergence_contradiction_skeleton.py build --index knowledge_external/catalogs/indexes/external_knowledge_index.tsv --outdir knowledge_external/synthesis --analysis-outdir analysis/v47_convergence_contradiction_skeleton
```

## Outputs

- `knowledge_external/synthesis/convergence_contradiction_skeleton.tsv`
- `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_SKELETON.md`
- `analysis/v47_convergence_contradiction_skeleton/convergence_contradiction_skeleton_summary.json`

The synthetic check verifies that placeholder rows remain unlinked and preserve
source and epistemic-marker fields.
