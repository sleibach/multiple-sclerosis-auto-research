# V54 Progression Package Eligibility Validator

## Purpose

`scripts/v54_progression_package_eligibility_validator.py` converts the
64-field V54 acquisition contract into a fail-closed inventory gate for three
roles:

- `P1`: longitudinal disability/PIRA association;
- `P2`: P1 plus paired CNS/CSF-versus-blood localization;
- `P3`: functional intervention direction after a progression association has
  already qualified.

A pass means only that the package inventory is complete enough to write a
blinded cohort-specific pre-registration and proceed to data-level validation.
It is not evidence that data quality, an association, a model, or biology passes.

Inventory completeness is necessary but not sufficient. Before any P1/P2
expression score is accessed, the package must also pass
`scripts/v54_progression_outcome_semantic_checker.py` under
`PROGRESSION_P1_P2_BLINDED_PREREGISTRATION_V54.md`. This second gate rejects
complete-looking packages whose outcome is actually relapse-only, stage-only,
morphology-only, pharmacodynamic-only, unconfirmed, or undocumented.

## Inventory Format

Provide one row per schema field with:

| column | meaning |
|---|---|
| `field` | exact field from `V54_progression_cohort_required_fields.tsv` |
| `available` | `yes` or `no` |
| `verified` | `yes` only after source-level confirmation |
| `n_nonmissing` | count of nonmissing values |
| `source_file` | immutable received-file or manifest path |
| `notes` | audit context |

Unknown fields are warnings, not silently accepted substitutes. Missing,
unverified, empty, or source-less mandatory fields are blockers. P2 inherits P1
requirements. For a real inventory, every declared source path must exist; the
gate checks existence but does not inspect expression values. PIRA mode requires
relapse/steroid and PIRA definition fields.
P3 additionally fails unless `--progression-association-prequalified` is set;
that flag is an operator assertion to be backed by a separate committed result,
not something the inventory gate proves.

## Commands

Synthetic regression:

```bash
.venv/bin/python scripts/v54_progression_package_eligibility_validator.py
```

Future blinded package inventory:

```bash
.venv/bin/python scripts/v54_progression_package_eligibility_validator.py \
  --inventory data/quarantine/<package>/progression_field_inventory.tsv \
  --role P1 \
  --endpoint-mode pira \
  --output-dir analysis/<package>_progression_inventory_gate
```

Do not point the validator at quarantined data unless use terms permit local
inspection. It validates inventory metadata, not expression values.

## Synthetic Verification

The default run creates six deterministic, clearly labeled synthetic inventory
fixtures under `analysis/v54_progression_package_eligibility_validator/synthetic/`:

- complete P1 passes;
- P1 missing subject/outcome fields fails;
- complete P2 passes;
- P2 missing pairing/composition/batch fails;
- complete, prequalified P3 passes;
- P3 without prequalification and functional/collateral fields fails.

These fixtures test method behavior only and contain no biological data.
