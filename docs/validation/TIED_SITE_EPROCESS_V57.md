# V57 Tied-Score Site E-Process Calibration

Status: **synthetic method verification; no MS evidence accumulated**

## Question

Can the unchanged federated V57 evidence process safely receive small-site
permutation p-values when score rounding creates many ties?

## Frozen Test

The pre-outcome plan is
[`V57_TIED_SITE_EPROCESS_PLAN.md`](../plans/V57_TIED_SITE_EPROCESS_PLAN.md).
Latent normal scores were collapsed to fixed quintile levels, creating only
five possible score values. For each realized tie pattern, dynamic programming
enumerated the exact conditional distribution of the doubled midrank sum over
all label allocations. Selected distributions independently matched brute-
force label enumeration.

Three seeds, two p-value modes, three effects, and 50,000 sequences per cell
produced 900,000 synthetic sequences and 10.8 million synthetic site arrivals.

## Result

| Quantity | Frozen gate | Observed range | Outcome |
|---|---:|---:|---|
| Null ever-crossing by arrival 12 | `<=0.055` | `0.00146-0.00220` | pass |
| Maximum one-site null mean e-factor | `<=1.01` | `0.98888` | pass |
| Effect `0.9` crossing by arrival 12 | `>=0.75` | `0.92666-0.93014` | pass |

The descriptive effect `0.5` crossed by site 12 in `0.28652-0.28956` of
sequences. Coarse ties reduced power relative to the continuous-score test but
did not inflate optional-stopping error in the tested regimes.

Verdict: **`TIED_SITE_EPROCESS_VERIFIED`** for the tested five-level score
mechanism and valid exact conditional permutation p-values.

## Boundary

This result means a tied score need not be rejected solely because it is tied,
provided the site computes a valid conditional permutation p-value that
preserves the complete preprocessing and tie structure. It does not validate:

- an asymptotic p-value substituted without calibration;
- preprocessing or feature selection that used response labels outside the
  frozen rule;
- overlapping or dependent sites;
- a changed estimand, timepoint, therapy, endpoint, or evidence direction;
- any biological effect or external cohort result.

## Reproduce

```bash
.venv/bin/python scripts/v57_tied_site_eprocess_probe.py
```

Outputs are under `analysis/v57_tied_site_eprocess/`.
