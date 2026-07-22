# V54 P1 Post-Result Interpretation Gate

Status: additive implementation of the frozen P1 interpretation contract. It
changes no endpoint, threshold, analysis family, locked rule, pre-registration,
or reference manifest.

## Purpose

After a package is released and the frozen analysis runs once, this gate maps
the result to the four precommitted classes in
`PROGRESSION_P1_P2_BLINDED_PREREGISTRATION_V54.md`. It computes interval
relationships from the cohort plan's already-frozen null and minimum-material
boundaries; it does not choose those boundaries.

## Decision Order

1. Identity, plan hash, freeze/access order, numeric coherence, and one-run
   execution must be valid. Otherwise: `INVALID_INPUT_OR_PROVENANCE`.
2. Random-module/permutation calibration, attendance/censoring, and
   site/batch/quality process controls must be clean. A failure invalidates the
   corresponding inference route; controls never rescue the primary.
3. Fewer than 10 independent events is
   `INCONCLUSIVE_DESCRIPTIVE_ONLY`. A higher cohort-specific information floor
   remains controlling when precommitted.
4. Wrong-direction estimates fail. An interval excluding the precommitted
   minimum material effect in the favorable direction also fails.
5. Intervals spanning both the null and minimum-material boundaries,
   unresolved quality, failed corrected-family criteria, or mandatory
   direction instability are inconclusive.
6. A favorable, corrected, null-excluding, material-compatible, sensitivity-
   stable result is `PASS_BOUNDED_ASSOCIATION`. A positive transient/relapse/
   pre-index specificity diagnostic changes this only to
   `PASS_WITH_PROGRESSION_SPECIFICITY_DOWNGRADE`.

A pass is a bounded predictive-association transport result under the declared
design. It is not a mechanism, target, treatment effect, or evidence that an
intervention can halt MS progression. A fail rejects transport under the
declared design and does not prove absence of progression biology.

## Machine Check

```bash
.venv/bin/python scripts/v54_progression_result_interpretation_gate.py
```

The default regression runs 17 clearly labeled synthetic result packets across
both favorable directions and every decision family. No patient data or
biological claim is involved.
