# Locked Artifact Hash Audit V45

Status: integrity infrastructure. No biological claim.

Purpose: mechanically detect accidental edits to locked rules and frozen
preregistration surfaces before validation or release checkpoints.

## Baseline

Committed baseline:

`docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv`

The baseline covers `9` artifacts:

| Category | Artifact |
|---|---|
| locked rule | `docs/locked_rules/LOCKED_RULE_V22.md` |
| primary preregistration | `docs/validation/PREREGISTRATION_V42.md` |
| primary interpretation grid | `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md` |
| primary batch guard | `docs/validation/BATCH_GUARD_V44.md` |
| secondary preregistration | `docs/validation/POSTPARTUM_APC_ARM_PREREGISTRATION_V44.md` |
| secondary preregistration | `docs/validation/TB_COMPARTMENT_PREREGISTRATION_V44.md` |
| context preregistration | `docs/validation/PHARMACODYNAMIC_ONLY_PREREGISTRATION_V45.md` |
| future addendum template | `docs/validation/KAROLINSKA_PREREGISTRATION_TEMPLATE_V45.md` |
| future addendum template | `docs/validation/GSE228330_OUTCOME_LABEL_ADDENDUM_TEMPLATE_V45.md` |

The future addendum templates are included because they define blind validation
surfaces for potential incoming labels. If either template must change, the
change should be intentional, reviewed, and accompanied by a baseline refresh
before any matching data are scored.

## Commands

Write or refresh the baseline intentionally:

```bash
.venv/bin/python scripts/v45_locked_artifact_hash_audit.py write-baseline \
  --out docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv
```

Audit current files against the committed baseline:

```bash
.venv/bin/python scripts/v45_locked_artifact_hash_audit.py audit \
  --baseline docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv \
  --outdir analysis/v45_locked_artifact_hash_audit \
  --fail-on-drift
```

Synthetic software check:

```bash
.venv/bin/python scripts/v45_locked_artifact_hash_audit.py synthetic-check \
  --outdir analysis/v45_locked_artifact_hash_audit
```

## Current Result

The current audit output is:

`analysis/v45_locked_artifact_hash_audit/locked_artifact_hash_audit_summary.json`

Summary:

```json
{
  "n_artifacts": 9,
  "overall_status": "PASS",
  "status_counts": {
    "DRIFT": 0,
    "MATCH": 9,
    "MISSING": 0
  }
}
```

The synthetic software check reports:

```json
{
  "changed_file_failed": true,
  "overall_status": "PASS",
  "pass_audit_passed": true,
  "synthetic": true
}
```

## Interpretation

`PASS` means the audited files match the committed byte-level SHA-256 baseline.
It does not mean the validation is biologically successful, and it does not
authorize changing any locked rule.

`DRIFT` or `MISSING` means stop before validation and identify whether the
change was intentional. Do not refresh the baseline merely to make an unexpected
drift pass.

Recommended placement:

- before running any received-cohort frozen harness;
- before release or external handoff;
- in the V45 pre-commit readiness checklist.
