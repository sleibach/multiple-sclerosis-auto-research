# V54 Combined Progression Intake Gate

## Purpose

`scripts/v54_progression_combined_intake_gate.py` binds the package inventory
gate and disability-endpoint semantic gate into one decision. It prevents a
complete inventory for one role, endpoint, or package from being paired with a
different declaration and mistakenly treated as ready.

The gate reads inventory and declaration metadata only. It does not open
expression values, calculate a molecular score, inspect subject-level outcomes,
or produce biological evidence.

## Bound Conditions

A pass requires all of the following:

- the role-specific inventory passes, including existing source paths;
- the endpoint declaration passes disability-progression semantics;
- package ID, role, endpoint mode, and synthetic/real status agree across the
  command and declaration;
- the declaration records no score or individual-outcome access before freeze.

An additive unknown inventory field may produce a warning but cannot substitute
for a mandatory field. Any gate error or cross-gate mismatch fails closed.

## Commands

Synthetic regression:

```bash
.venv/bin/python scripts/v54_progression_combined_intake_gate.py --fail-on-error
```

Future real package, while quarantined and blinded:

```bash
.venv/bin/python scripts/v54_progression_combined_intake_gate.py \
  --inventory path/to/progression_field_inventory.tsv \
  --declaration path/to/frozen_endpoint_declaration.tsv \
  --package-id EXACT_RECEIPT_PACKAGE_ID \
  --role P1 --endpoint-mode pira \
  --output-dir analysis/<package>_combined_progression_intake \
  --fail-on-error
```

Do not run the command against files whose use terms prohibit local inspection.
A pass permits only completion and commitment of the remaining blinded
cohort-specific pre-registration. It does not authorize interpreting data or
claiming progression.

## Synthetic Verification

Nine clearly labeled synthetic cases cover two valid P1/P2 declarations,
inventory-only failure, semantic-only failure, role mismatch, endpoint mismatch,
package-ID mismatch, prior score access, and additive unknown metadata. A
fixture passes only when both component gates and all binding checks pass.
These are method-behavior fixtures and contain no biological evidence.
