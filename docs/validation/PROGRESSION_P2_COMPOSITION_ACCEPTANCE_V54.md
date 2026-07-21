# V54 P2 Composition Measurement Acceptance Contract

Status: additive blind-committed guard. It does not modify the frozen P2
interaction or any locked rule.

## Reason For The Guard

The V54 P2 synthetic design is calibrated when compartment composition is
measured without error, and under noisy measurement only when true
outcome-associated composition imbalance is absent. When imbalance exists, a
noisy proxy leaves severe residual false localization (maximum null pass rate
`0.2227` in the frozen generator); omitting composition is worse (`0.5827`).
Therefore “composition adjusted” is not a sufficient declaration.

## Accepted Measurement Classes

### Direct measured composition

Flow cytometry, CyTOF, CITE-seq, or sample-linked single-cell counts may enter
the direct route only when:

- every P2 compartment and outcome group is covered by the same frozen method;
- sample-to-composition linkage and collection-time correspondence are exact;
- cell definitions, QC, missingness, batch, and detection limits are declared;
- the method and analysis were selected before molecular score/outcome access;
- differential composition missingness has a frozen fail/inconclusive action.

The gate does not claim these technologies are error-free. It treats them as
direct measurements whose observed reliability and coverage must still be
reported.

### Direct-reference-validated proxy

A deconvolution or other proxy is conditionally eligible only if it has a
sample-linked direct reference in a blinded calibration subset, empirical
reliability is reported by compartment, and the V54 null simulation is rerun at
that reliability and observed imbalance before score access. Every relevant
null family must pass the frozen calibration rule. The proxy route remains a
sensitivity, not equivalent to direct measurement.

### Ineligible

Expression-derived identity/module scores alone, literature-only benchmark
claims, unlinked reference panels, outcome-selected cell definitions, or
unresolved differential missingness fail closed. Apparent absence of imbalance
cannot be established using the same unvalidated proxy whose residual error is
under question.

## Decisions

- `PASS_DIRECT_MEASUREMENT`: direct, linked, complete, blind-frozen method;
  cohort-specific P2 power/null calibration is still mandatory.
- `PASS_VALIDATED_PROXY_REQUIRES_SENSITIVITY`: direct-reference validation and
  empirical null calibration pass; proxy cannot be the sole localization
  evidence.
- `FAIL_CLOSED`: required measurement, linkage, coverage, blindness, or
  calibration condition is absent.

## Machine Check

```bash
.venv/bin/python scripts/v54_progression_p2_composition_gate.py
```

The default command runs nine clearly labeled synthetic declarations. A real
declaration is supplied with `--declaration` and remains a metadata/method gate,
not a biological result.

## Boundary

Passing means only that composition measurement is methodologically eligible
for the frozen direct interaction. It does not establish localization,
progression association, within-cell remodeling, causal biology, or a
therapeutic route.
