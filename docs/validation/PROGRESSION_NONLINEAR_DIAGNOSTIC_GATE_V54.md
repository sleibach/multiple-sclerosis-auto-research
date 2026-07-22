# V54 Progression Nonlinear Diagnostic Gate

Status: additive blind-committed receipt guard. It does not modify the frozen
V54 progression design, a locked rule, or any pre-registration.

## Purpose

The seeded V54 misspecification audit found one narrow method warning: a linear
Cox coefficient can miss a U-shaped crossing association even when a fixed
linear-plus-quadratic diagnostic detects it. No MS risk shape was inferred.
This gate prevents that warning from creating post-result flexibility.

The primary analysis remains one standardized linear score coefficient. The
three diagnostics are fixed before molecular scores or individual outcomes are
seen and cannot rescue, replace, or reinterpret a failed primary result.

## Frozen Diagnostic Family

Every declaration must contain exactly:

1. a high-threshold indicator at observed standardized score `z > 0.674`;
2. the saturated transform `tanh(1.5 * observed_z)`;
3. a two-degree-of-freedom linear-plus-quadratic omnibus model.

The primary alpha is `0.05`. Individual diagnostic tests use `0.05/3`, with a
family alpha of `0.05`, unless thresholds come from a named independent null
calibration bank. An empirical route must declare a source, disjoint seeds, and
data that are disjoint from evaluation. Diagnostics not in this family require
a separate future pre-registration; they cannot be selected after inspection.

## Required Blind Declaration

- package, protocol, and analysis-plan sources;
- the exact primary model and interpretation rule;
- the exact diagnostic family, threshold, transform, and omnibus formula;
- the multiplicity route and alpha budget;
- an independent calibration source and disjointness declarations when an
  empirical null bank is used;
- confirmation that the declaration was frozen before score/outcome access;
- confirmation that every diagnostic and the primary will be reported;
- explicit bans on post-result substitution, transform selection, primary
  replacement, and diagnostic rescue.

## Decisions

| decision | conditions | permitted interpretation |
|---|---|---|
| `PASS_FIXED_NONLINEAR_DIAGNOSTIC_FAMILY` | exact family and transforms, valid correction/calibration, blind freeze, primary preserved | run the primary and fixed non-rescuing diagnostic panel |
| `FAIL_CLOSED` | missing/changed diagnostic, uncorrected alpha, overlapping calibration, prior access, or any rescue/replacement authority | no confirmatory nonlinear interpretation |

A diagnostic signal can only motivate a separately pre-registered future
model. It cannot convert a failed primary coefficient into evidence.

## Machine Check

Run the synthetic regression:

```bash
.venv/bin/python scripts/v54_progression_nonlinear_diagnostic_gate.py
```

For a quarantined package declaration:

```bash
.venv/bin/python scripts/v54_progression_nonlinear_diagnostic_gate.py \
  --declaration path/to/blind_nonlinear_diagnostic_declaration.json \
  --output-dir path/to/nonlinear_gate --fail-on-error
```

The default regression contains ten clearly labeled synthetic declarations:
two valid process routes and eight fail-closed variants. It contains no patient
data and makes no biological claim.

## Boundary

Passing establishes only that model diagnostics were fixed blind and cannot
rescue the primary analysis. It is not evidence of a nonlinear MS association,
progression prediction, mechanism, target, or route to halting MS.
