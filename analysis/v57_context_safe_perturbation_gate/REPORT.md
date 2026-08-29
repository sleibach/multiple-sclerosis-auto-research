# V57 Context-Safe Perturbation Gate

Status: **FAIL** as seeded synthetic method behavior;
no biological or MS claim.

## Scale

- Synthetic screens: `18,000`.
- Candidate evaluations: `432,000` per method.
- One-third prespecified minority context; pooled favorable effects can reverse
  across all efficacy outcomes in that context.

## Frozen Result

- `16` donors: **FAIL** across all frozen cells.
- `24` donors: **FAIL** across all frozen cells.

First tested passing context-safe design: `None` donors.
Failed checks: `29` of `60`.

Across the frozen 16/24-donor operating cells, the pooled gate's minimum
uniform-rescue detection was `0.992` and maximum subgroup-reversal promotion was
`0.011`. The context-safe gate's corresponding values were
`0.045` and
`0.000`.

## Meaning

The pooled gate can be inspected against `performance.tsv`; the context-safe
gate is acceptable only where it controls subgroup-reversal promotion and
retains uniform-rescue sensitivity under every seed and effect. Here it does
not: simultaneous within-context non-harm bounds add little specificity to the
already conservative pooled gate and destroy useful sensitivity. The method is
rejected rather than retuned. This is a design stress test under a known,
prespecified context. It neither discovers a human subgroup nor establishes a
biological rescue. Unknown contexts still require broader donor sampling and
independent replication.
