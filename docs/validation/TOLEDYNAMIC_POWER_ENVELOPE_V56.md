# ToleDYNAMIC Fixed-Family Power Envelope V56

Status: synthetic method-characterization only. No simulated effect is a claim
about MS, tolebrutinib, or the ToleDYNAMIC data. The controlled package has not
been obtained or read.

## Question

How large must a standardized randomized-arm difference in paired
month-3-minus-baseline change be for one slot to survive the frozen 18-slot
family-wise gate at plausible small substudy sizes?

## Simulation

`scripts/v56_toledynamic_power_envelope.py` uses a correlated noncentral-t
design approximation with:

- 18 two-sided endpoint slots and family-wise alpha `0.05`;
- `8`, `10`, `15`, `20`, `30`, or `40` participants per arm;
- one planted standardized change difference of `0.4` to `1.2`;
- endpoint correlation `0.0`, `0.5`, or `0.8`;
- 100,000 null families to calibrate each max-T critical value;
- 20,000 independent null families per seed and three seeds; and
- 5,000 alternative families per seed and design cell.

The run comprised 1,080,000 independent null-audit families and 1,350,000
alternative families. Mean audited null FWER was `0.04981`, ranging from
`0.04630` to `0.05385` across design/seed cells.

This is not the eventual mixed-model/randomization-permutation harness. It is a
planning approximation for one planted slot, with effect size defined on the
paired-change scale. It does not model site, batch, dropout, RNA-subset
selection, measurement error, or failed module coverage, all of which can
reduce usable power.

## Best-Case Forty-Participant Trial Scenario

For a total of 40 participants (`20` per arm), power across the three module-
correlation scenarios was:

| standardized change difference | minimum power | mean power | maximum power |
|---:|---:|---:|---:|
| 0.4 | 0.034 | 0.046 | 0.061 |
| 0.6 | 0.120 | 0.144 | 0.177 |
| 0.8 | 0.271 | 0.318 | 0.376 |
| 1.0 | 0.500 | 0.547 | 0.612 |
| 1.2 | 0.717 | 0.759 | 0.811 |

The conservative minimum across correlation scenarios did not reach 80% for
any tested effect at 20 participants per arm. It reached at least 80% only at:

- 30 per arm for a planted difference of `1.2`; and
- 40 per arm for a planted difference of `1.0`.

No tested sample size reached 80% worst-case power for effects `<=0.8`.

## Interpretation Boundary

1. A complete 40-participant parent-trial substudy is not reliably powered for
   moderate effects after the fixed 18-slot correction.
2. A smaller RNA subset should be expected to identify only very large effects;
   a null RNA family may be inconclusive rather than mechanistically decisive.
3. Functional assays measured in a larger paired set could be more informative,
   but they remain a separate corrected family and require the blinded mapping
   gate.
4. HERCULES discovery followed by a fixed PERSEUS replication can still reject
   large shared peripheral mechanisms. It cannot establish clinical mediation
   from a small positive subset.
5. The access request should prioritize complete both-arm sample accounting and
   all measured participants, not only the RNA subset.

The appropriate promise is therefore narrow: ToleDYNAMIC may detect or reject a
large randomized peripheral pharmacodynamic effect and test transport across
progressive-MS phenotypes. It is not sized to discover or validate a subtle
treatment-response classifier.

## Reproducible Outputs

- `analysis/v56_toledynamic_power_envelope/power_grid.tsv`
- `analysis/v56_toledynamic_power_envelope/null_calibration.tsv`
- `analysis/v56_toledynamic_power_envelope/summary.json`

All outputs are seeded synthetic method results and contain no participant or
biological data.
