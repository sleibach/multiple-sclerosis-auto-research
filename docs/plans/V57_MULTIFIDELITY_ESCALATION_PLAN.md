# V57 Multifidelity 2D-to-3D Escalation Plan

Status: predeclared synthetic method-characterization plan. No MS data,
biological effect, target, or treatment claim.

## Decision

Decide whether a small crossed-donor 3D glial calibration panel contains
reproducible candidate-specific functional information beyond a simpler 2D
microglial assay and therefore merits expensive 3D scale-up.

The inferential unit is the donor pair. Cells, wells, guides, and organoids are
technical observations, not independent biological replicates.

## Frozen Calibration Design

- 12 perturbation candidates;
- two independent technical measurements collapsed within each donor pair;
- training and held-out donor pairs fixed before model fitting;
- 12 training plus 8 held-out donor pairs for the primary design;
- all candidates represented in every donor pair;
- 3D batch allocation balanced within candidate and donor pair;
- proximal 2D state and distal 3D function oriented so larger is favorable.

## Escalation Paths

### Incremental-information path

1. Fit the training-only base relation between 3D function and 2D state,
   including the recorded 3D batch.
2. Estimate candidate-specific training residuals.
3. Apply those residuals without refitting to held-out donor pairs.
4. Calculate held-out RMSE gain over the base model and the correlation between
   training and held-out candidate residuals.
5. Permute the mapping of training residual effects to candidate identity and
   compare held-out gain to this fixed-candidate null.

Scale 3D only when all hold:

- held-out RMSE gain is at least 10%;
- training/held-out candidate-residual correlation is at least 0.50;
- permutation p is at most 0.05;
- candidate-by-batch imbalance is at most 0.25.

### Safety-discordance path

Scale 3D when a candidate is favorable in 2D but harmful in the distal 3D
endpoint in both training and held-out donor pairs, with the fixed margin and
standard-error bounds implemented in the script. Candidate family multiplicity
is controlled by simultaneous max-statistic calibration. This path exists
because a simpler model can be predictively adequate on average while missing
a context-specific harm.

## Fail-Closed Outcomes

- `STOP_AT_2D_REDUNDANT`: 3D adds no held-out information and no safety reversal.
- `ABSTAIN_BATCH_CONFOUNDED`: candidate/batch support is not separable.
- `ABSTAIN_UNDERPOWERED`: fewer than the frozen primary donor counts or unstable
  held-out estimates.
- `SCALE_3D_INCREMENTAL`: incremental-information path passes.
- `SCALE_3D_SAFETY`: safety-discordance path passes.

## Synthetic Scenarios and Gates

Three seeds are run for each scenario. The scenario-level checks are:

| scenario | required behavior |
|---|---|
| redundant 3D | scale-up probability <= 0.05 |
| complementary 3D | incremental scale-up probability >= 0.80 |
| hidden 3D harm | safety scale-up probability >= 0.80 |
| response-correlated 3D batch | false scale-up <= 0.05 and batch abstention >= 0.80 |
| small calibration panel | scale-up <= 0.20; report as underpowered |

The exact generator, margins, permutations, and seeds are committed in
`scripts/v57_multifidelity_escalation.py`. Thresholds are not changed after
observing results. A failed scenario rejects this candidate gate and is not
retuned in the same analysis.

## Interpretation Boundary

Synthetic success means only that the design makes the intended complexity
decision under its generator. It does not show that 3D models add information
in MS, that any perturbation is beneficial, or that the proposed organoid or
assembloid route is biologically valid.
