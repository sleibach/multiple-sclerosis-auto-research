# V54 Progression P1 Analysis-Release Gate

Status: additive synthetic-verified composition guard. It does not modify the
frozen reference manifest, endpoint, primary model, or any pre-registration.

## Release Contract

A P1 package is released to the separately frozen analysis only when all of the
following hold for one package identity:

1. the seven-stage intake-to-lock composition returns
   `LOCK_READY_FOR_FROZEN_ANALYSIS`;
2. endpoint-confirmation provenance returns
   `PASS_CONFIRMATION_PROVENANCE_GATE`;
3. the exact seven-control family returns
   `PASS_FIXED_NEGATIVE_CONTROL_FAMILY`;
4. every stage binds the same package ID; and
5. the committed V54 reference manifest verifies and its contract SHA-256
   matches the supplied release declaration.

`CONTINUE_BLINDED_ACCRUAL` remains a valid non-release state. Any other stage
failure, package mismatch, manifest failure, or contract-hash mismatch fails
closed. Release authorizes mechanical execution only. It is not a favorable
result, validation, efficacy evidence, progression evidence, or target evidence.

## Machine Check

```bash
.venv/bin/python scripts/v54_progression_p1_analysis_release_gate.py
```

The default regression executes the actual upstream validators on ten synthetic
packages: one releases, one continues blinded accrual, and eight upstream,
confirmation, control, identity, or manifest faults fail closed.
