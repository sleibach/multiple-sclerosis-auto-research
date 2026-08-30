# Multifidelity 2D-to-3D Escalation V57

Status: synthetic method characterization only. No MS biology, target, treatment,
or assay effect was established.

## Question

When should a costly crossed-donor 3D glial assay be scaled beyond a simpler 2D
microglial perturbation assay?

The predeclared gate tested two distinct reasons to escalate:

1. 3D adds reproducible held-out candidate information beyond the 2D state;
2. 3D exposes a replicated harmful reversal that the 2D assay misses.

Candidate/batch imbalance causes abstention. Donor pair, not well, guide, cell,
or organoid, is the biological replicate.

## Primary Synthetic Result

The primary run comprised 7,500 screens, 90,000 candidate evaluations, and
1,492,500 permuted candidate assignments across three seeds.

| scenario | mean relevant probability | verdict |
|---|---:|---|
| redundant 3D | scale `0.0013` | correct stop |
| complementary 3D | incremental scale `0.988` | passes |
| hidden 3D harm | any scale `0.830`; safety-specific scale `0.139` | safety gate fails |
| response-correlated 3D batch | batch abstention `1.000`; scale `0.000` | passes |
| small calibration panel | underpowered abstention `1.000`; scale `0.000` | passes |

The parent gate therefore **fails one of seven checks**. A 12-training/8-held-out
calibration can determine that 3D carries additional candidate information, but
cannot reliably state that the added information is specifically a replicated
safety reversal. Generic information gain must not be reported as safety.

## Fixed Safety-Power Extension

The extension varied only training and held-out donor-pair counts. It retained
the hidden-harm generator, safety margin, simultaneous critical value, batch
design, seeds, and 500 screens per seed.

It ran 12,000 additional screens and 144,000 candidate evaluations. The first
grid point with safety-specific scale probability at least `0.80` in **every**
seed was:

- 32 training donor pairs;
- 24 independent held-out donor pairs;
- mean safety-specific detection `0.840`;
- minimum seed-specific detection `0.826`.

This is a synthetic planning boundary, not a recommended biological sample size
without qualification. A real pilot must estimate blinded donor-level variance;
the existing V57 variance-adaptive machinery then selects or abstains without
seeing candidate effects.

## Operational Decision

1. Use a small, exactly batch-balanced 3D calibration only to test whether 3D
   adds reproducible information beyond 2D.
2. Stop at 2D when the incremental gate fails and there is no replicated harm.
3. Do not claim candidate-specific safety from a 12/8 donor split.
4. Size a safety-confirmation panel from blinded empirical variance; under the
   committed reference generator, 32/24 donor pairs is the first tested
   all-seed passing point.
5. Keep 2D and 3D endpoints distinct. A 3D model is not automatically superior
   because it is more complex.

## Reproducibility

- parent plan: `docs/plans/V57_MULTIFIDELITY_ESCALATION_PLAN.md`
- parent script: `scripts/v57_multifidelity_escalation.py`
- parent outputs: `analysis/v57_multifidelity_escalation/`
- safety extension plan: `docs/plans/V57_MULTIFIDELITY_SAFETY_EXTENSION_PLAN.md`
- safety extension script: `scripts/v57_multifidelity_safety_power.py`
- safety outputs: `analysis/v57_multifidelity_safety_power/`

The synthetic results characterize only the decision procedure. They do not
show that any 2D or 3D perturbation rescues an MS-relevant phenotype.
