# V54 P2 Compartment-Interaction Power Design

All outputs are seeded synthetic method behavior. They are not biological
evidence and do not estimate compartment effects in MS.

The grid generated 288,000 unique synthetic cohorts and
576,000 route evaluations. Each used a direct
outcome-by-compartment interaction; no difference-of-significance rule was used.

## Null Calibration Families

| family | cells | median | maximum | max Wilson CI | family max-tail |
|---|---:|---:|---:|---:|---:|
| adjusted_perfect_composition | 48 | 0.048 | 0.065 | 0.050-0.085 | 0.834 |
| adjusted_noisy_composition_without_imbalance | 24 | 0.049 | 0.061 | 0.046-0.081 | 0.904 |
| adjusted_noisy_composition_with_imbalance | 24 | 0.072 | 0.223 | 0.194-0.254 | 0.000 |
| unadjusted_with_composition_imbalance | 48 | 0.135 | 0.583 | 0.547-0.617 | 0.000 |

## Planning Boundary

Within calibration-eligible regimes, the composition-adjusted route reached the 80% criterion in 27/36 assumption scenarios.
The 10/12 apparent passes under noisy measured composition plus true imbalance are not interpreted as power because that null
family is miscalibrated.
`minimum_group_n.tsv` reports the exact conditional thresholds. A real P2
package must rerun this design from blinded pairing, composition, outcome,
and compartment metadata and must first pass P1 endpoint semantics.
