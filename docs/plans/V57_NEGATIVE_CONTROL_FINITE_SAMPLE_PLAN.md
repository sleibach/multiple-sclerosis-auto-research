# V57 Negative-Control Finite-Sample Remediation Plan

Status: frozen after the naive negative-control rule failed its clean-assay
family error gate. Synthetic method characterization only.

## Fixed Failure

With four controls in two donor panels, the predeclared normal critical value
`2.50` produced clean-assay family false-stop probabilities of `0.2438-0.2498`.
That rule is rejected. High detection under contaminated scenarios cannot
rescue an invalid false-positive rate.

## Remediation

Use a two-sided Bonferroni Student-t critical value for the complete family of
eight panel-by-control tests:

`t_(1 - 0.05 / (2 * 8), min(n_train, n_test) - 1)`.

No observed synthetic outcome selects the critical value. Vary only donor-pair
counts over the frozen grid:

`12/8`, `16/12`, `20/16`, `24/20`, `32/24`, `40/32`.

Retain four controls, clean variance `0.75`, common hidden drift `0.75`,
control-specific artifact `1.15`, three new seeds, and 5,000 screens per cell.

## Gate

The first eligible grid point must satisfy in every seed:

- clean family false-stop probability <= 0.05;
- common-drift detection >= 0.80;
- control-specific artifact detection >= 0.80.

No biological claim follows. Empirical control variance and control validity
must be established in a real assay before using the synthetic boundary.
