# V57 Combinatorial Perturbation Design Result

## Result

- Conditional D-optimal method gate: **PASS**.
- Scale: 9,000 seeded synthetic screens and
  18,000 design evaluations.
- No target identity or biological measurement was simulated as real evidence.

| seed | regime | D-opt/random RMSE | rank-correlation gain | top-10 recall gain |
|---:|---|---:|---:|---:|
| 5731 | descriptor_aligned | 0.637 | 0.074 | 0.100 |
| 5731 | mixed | 0.833 | 0.139 | 0.000 |
| 5731 | idiosyncratic | 0.816 | 0.006 | 0.000 |
| 5732 | descriptor_aligned | 0.635 | 0.077 | 0.100 |
| 5732 | mixed | 0.839 | 0.137 | 0.000 |
| 5732 | idiosyncratic | 0.827 | 0.006 | 0.000 |
| 5733 | descriptor_aligned | 0.508 | 0.099 | 0.200 |
| 5733 | mixed | 0.806 | 0.177 | 0.000 |
| 5733 | idiosyncratic | 0.804 | -0.006 | 0.000 |

## Decision boundary

A pass licenses only a small pilot whose pre-assay descriptors are audited and
whose random-design comparator is retained. The idiosyncratic regime is the
failure case: if descriptors do not encode real interaction structure, geometry
cannot create it. Any future human-cell screen still needs independent donors,
CRISPRi and CRISPRa direction arms, non-targeting controls, batch-balanced
processing, held-out perturbations, and orthogonal functional readouts. This
simulation does not nominate a target or establish anything about MS.
