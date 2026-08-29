# V57 Multi-Criterion Donor-Count Resolution Plan

Status: predeclared synthetic method-characterization extension. No generated
observation is biological evidence.

## Fixed Parent Method

The data-generating model, candidate truth classes, four efficacy outcomes,
viability outcome, three-guide structure, noise covariance, and all selection
criteria are frozen at commit `5c407480` in
`scripts/v57_multicriterion_perturbation_gate.py`. No threshold, effect, margin,
or multiplicity rule may change in this extension.

## Resolution Sweep

- Donor counts: `9`, `10`, and `11`.
- Broad-rescue effect scales: `0.80` and `1.00` standardized units.
- Seeds: `57061`, `57062`, and `57063`.
- Synthetic screens per cell: `2,000`.
- Total synthetic screens: `36,000`.
- Both the averaged-endpoint comparator and the replicated broad-rescue gate
  are retained.

## Decision

For each donor count, require every seed and both effect scales to satisfy the
same five parent checks:

1. false-promotion probability `<=0.05`;
2. probability of at least one true rescue `>=0.80`;
3. selection precision `>=0.90`;
4. false promotion below the averaged endpoint;
5. probability of a true rescue no more than `0.10` below the averaged
   endpoint.

The smallest tested donor count passing all 30 checks is the resolved
synthetic design point. If none passes, the existing 12-donor result remains
the first tested passing design. This is not a biological power calculation;
it characterizes only the committed synthetic assumptions.
