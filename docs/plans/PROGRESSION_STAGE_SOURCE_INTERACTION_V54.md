# V54 Progressive-Stage Source-Interaction Audit

Status: frozen after the two-lineage critique and before execution. This is a
bounded sensitivity of the committed Macnair stage analysis, not discovery.

## Question

Are the cross-sectional SPMS-minus-PPMS module effects different between the
eligible Amsterdam white-matter and UK grey-matter source strata?

The audit addresses two model objections: apparent same-direction effects can
hide one near-null source, while opposite signs can arise from imprecision
rather than a supported source-by-stage interaction. Neither a supported nor a
null interaction identifies temporal progression.

## Frozen Inputs And Family

- Use only
  `analysis/v54_progressive_stage_modules/donor_standardized_residual_scores.tsv`.
- Preserve the existing 44 donor-level observations, diagnoses, source labels,
  nuisance residualization, and five-module family.
- Test all five modules; do not select only the three discordant modules or the
  two same-direction modules after observing their effects.

## Frozen Models And Null

For each module fit:

`score ~ SPMS + UK_source + SPMS:UK_source`

Report the interaction coefficient (UK minus Amsterdam SPMS-minus-PPMS
effect), HC3 95% confidence interval, and HC3 p-value. The permutation-style
null is a donor-level Rademacher wild residual bootstrap under the reduced
model `score ~ SPMS + UK_source`, which retains a common stage effect while
testing only the interaction. Use fixed seeds `54701`, `54702`, and `54703`,
100,000 replicates per seed, and max-T control across all five interaction
statistics.

Also report the already-defined per-source effects with HC3 intervals and a
leave-one-donor-out range within each source. LODO is an influence diagnostic,
not an additional significance test.

## Interpretation

A source interaction is `supported_context_heterogeneity` only if its HC3
interval excludes zero, aggregate wild p is at most 0.05, BH q is at most
0.10, and max-T p is at most 0.10. Otherwise it is not supported or
inconclusive. Same-sign source effects remain descriptive unless both have
adequate precision.

Any supported interaction would show cross-sectional tissue/source-context
heterogeneity only. It cannot be called progression, a transition, causal
biology, or an intervention direction because source and tissue are inseparable
in this held comparison.

