# V57 Federated Replicability Gate

Status: **verified method infrastructure; no external cohort evidence**

## Distinct Claims

The anytime-valid e-process asks whether evidence against the same-estimand
global null has accumulated. It can cross after one exceptional site. That is
not evidence that the effect recurs across sites.

This separate gate asks a narrower fixed-batch question: in a predeclared
complete family of four distinct V22 validation sites, are at least two effects
nonnull in the locked positive direction?

## Method

After all four records arrive, order their valid one-sided permutation
p-values and compute `p_partial_conjunction = min(1, 3 * p_(2))`.

The at-least-two claim passes only at `p <= 0.05`. The family size (`4`),
replication order (`2`), estimand, harness, and evidence units are frozen.
There is no interim claim, adaptive family size, site removal, or post-hoc
choice of the required replication count. A union bound makes the test valid
for true-null dependence, but hidden reuse of participants or source studies
still destroys the interpretation that evidence units are distinct.

## Verification

All `6/6` deterministic fixtures met their expected outcomes:

- two small site p-values produced partial-conjunction p `0.03` and passed;
- one exceptional site produced p `0.60` and did not establish replication;
- an all-null-compatible family did not establish replication;
- incomplete, duplicate-evidence-unit, and missing-uncertainty families were
  invalid.

A separately frozen calibration simulated `4,500,000` four-record families
across three seeds, correlations `0`, `0.5`, and `0.9`, and both all-null and
one-arbitrarily-nonnull configurations. Maximum false replication was
`0.049464` (two-Monte-Carlo-SE upper value `0.050331`), below the `0.055`
implementation gate.

```bash
.venv/bin/python scripts/v57_federated_replicability_gate.py synthetic-check \
  --outdir analysis/v57_federated_replicability
.venv/bin/python scripts/v57_federated_replicability_calibration.py
```

## Interpretation Boundary

No actual V22 validation sites were combined. This gate neither validates the
biomarker nor estimates a pooled effect. It prevents a future global-null
crossing driven by one site from being described as multi-site replication.
If fewer than four eligible independent sites can be acquired, this particular
replication claim remains unavailable rather than being redefined after seeing
results.
