# V54 P1 Intake-to-Lock Composition

Status: synthetic composition test only. It changes no locked rule,
pre-registration, endpoint, or decision threshold.

## Purpose

The individual V54 progression guards are necessary but not sufficient if a
future package can drift between them. This composition executes the actual
validators in sequence and binds every stage to one package identifier:

1. required-field inventory plus progression endpoint semantics;
2. event-time and censoring assumptions;
3. site and score-scale calibration;
4. treatment-switch estimands;
5. fixed nonlinear diagnostics;
6. blinded cohort-feasibility routing;
7. aggregate information accrual and lock handoff.

No molecular value, individual outcome, effect estimate, p-value, or efficacy
recommendation is available to the composition controller.

## State Machine

| final state | meaning |
|---|---|
| `LOCK_READY_FOR_FROZEN_ANALYSIS` | every blind process gate passes for one package and the aggregate information target is reached |
| `CONTINUE_BLINDED_ACCRUAL` | every blind process gate passes but the fixed information target is not reached |
| `HOLD_UNRESOLVED_METADATA` | process gates pass but the information monitor identifies unresolved reasons |
| `FAIL_CLOSED` | any stage fails, package identifiers drift, synthetic status conflicts, or an efficacy-bearing field appears |

Lock readiness authorizes only mechanical execution of the separately frozen
analysis. It is not a favorable result and contains no efficacy or biological
interpretation.

## Synthetic Regression

Run:

```bash
.venv/bin/python scripts/v54_progression_p1_intake_to_lock.py
```

The committed regression executes ten clearly labeled synthetic packages. One
reaches lock, one remains in blinded accrual, and eight fail at distinct
boundaries: intake, censoring, scale, switching, diagnostic rescue,
cross-summary identity, forbidden efficacy content, and cross-stage identity.

## Boundary

This is method and package-routing verification only. Synthetic records are not
MS data. A pass is not progression evidence, biomarker validation, treatment
effect, target evidence, or a route to halting MS.
