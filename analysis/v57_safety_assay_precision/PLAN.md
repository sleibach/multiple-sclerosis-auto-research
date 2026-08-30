# V57 Orthogonal Safety-Assay Precision Plan

Status: predeclared seeded synthetic method characterization. No generated
observation is biological or MS evidence.

## Bottleneck

The committed two-stage design at `d362861f` rejected every context-harm
candidate but rarely confirmed a uniform rescue. Post-result component
diagnostics localized the main loss to the simultaneous viability bound. This
extension tests a prospective experimental remedy, not a weaker statistical
threshold.

## Frozen Design

- Discovery remains 12 donors, the pooled replicated gate, and at most four
  nominees. It is unchanged from `d362861f`.
- Confirmation remains independent and context-balanced.
- Confirmation efficacy observations, all efficacy margins, and all
  multiplicity rules remain unchanged.
- Confirmation donors per context: `8`, `12`.
- An independent orthogonal viability assay uses all three guides and `1`, `2`,
  or `4` technical wells per donor-guide.
- Viability variance components, fixed before simulation: donor-global SD
  `0.10`, candidate-by-donor SD `0.20`, guide SD `0.05`, and per-well assay SD
  `0.40`. Technical replication reduces only per-well assay noise; it does not
  reduce donor heterogeneity.
- Effect scales: `0.80`, `1.00`; seeds `57301`, `57302`, `57303`; `1,000`
  screens per cell (`36,000` total).
- Candidate truth classes and one-outcome minority-context harm follow
  `d362861f`.

## Frozen Confirmation Rule

Require every efficacy and orthogonal-viability lower bound in both contexts
to exceed the unchanged margins (`-0.25` efficacy, `-0.50` viability), with
alpha `0.05 / (4 candidates * 2 contexts * 5 outcomes)`. No endpoint can
compensate for another.

## Success Criteria

Every seed/effect cell for a donor/replicate design must meet:

- context-harm confirmation `<=0.05`;
- probability of at least one uniform rescue `>=0.80`;
- uniform-rescue precision `>=0.90`;
- context-harm confirmation below discovery nomination;
- uniform-rescue probability no more than `0.10` below discovery nomination.

The least resource-intensive passing combination, ordered by total donor-wells
(`2 * donors_per_context * 3 guides * technical_wells`), is the design result.
No variance component or threshold will change after simulation.
