# Relationship To Project Findings V47

This controlled vocabulary defines how an external-classed record may describe
its relationship to grounded project findings. The tag is navigation metadata,
not evidence. External records remain `NOT_PROJECT_GROUNDED` even when the
relationship tag is `supports` or `contradicts`.

## Allowed Values

| value | meaning | extra requirement |
|---|---|---|
| `orthogonal` | The external record describes a resource or claim that does not yet map to a specific grounded project finding. | No grounded finding reference required. |
| `untested` | The external record states a claim that could be tested or grounded later, but has not been tested by this project. | No grounded finding reference required; must not be described as a result. |
| `supports` | A specific external claim appears directionally consistent with a specific grounded project finding. | Requires `project_finding_reference.finding_id` and `project_finding_reference.artifact`; still not evidence. |
| `contradicts` | A specific external claim appears in tension with a specific grounded project finding. | Requires `project_finding_reference.finding_id` and `project_finding_reference.artifact`; flags scrutiny, never overrides grounded data. |

## Commands

```bash
.venv/bin/python scripts/v47_relationship_vocabulary_linter.py synthetic-check --outdir analysis/v47_relationship_vocabulary_linter --fail-on-error
.venv/bin/python scripts/v47_relationship_vocabulary_linter.py lint --outdir analysis/v47_relationship_vocabulary_linter --fail-on-error
```

The synthetic fixture verifies four cases:

- `orthogonal` can stand without a project-finding reference;
- `supports` with a grounded reference passes;
- `supports` without a grounded reference fails;
- an unsupported relationship value fails.
