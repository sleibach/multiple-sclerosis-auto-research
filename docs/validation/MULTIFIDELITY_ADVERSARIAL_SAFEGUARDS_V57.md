# Multifidelity Adversarial Safeguards V57

Status: synthetic method characterization only. No MS biological or treatment
claim.

## Donor Stability

A leave-one-donor version of the incremental 3D information gate retained
complementary-signal sensitivity:

- `0.9425-0.9450` at 12 training / 8 held-out donor pairs;
- `0.98375-0.99375` at 16 / 12 donor pairs.

The constructed paired high-leverage artifact passed the parent gate only
`0-0.01375` and the leave-one-donor gate zero times. Thus the extension is a
reasonable sensitivity check, but this simulation did not show that it fixes a
material parent false-positive mode.

## Negative Controls

The first rule was rejected. A fixed normal cutoff of `2.50` across four
controls and two panels produced a clean family false-stop probability of
`0.2438-0.2498`.

A separately frozen finite-sample design used a two-sided Student-t critical
with Bonferroni control across all eight tests. Across 270,000 synthetic screens,
the first tested 12/8 donor point passed every seed:

- maximum clean family false-stop: `0.0388`;
- minimum common hidden-drift detection: `0.9646`;
- minimum control-specific artifact detection: `0.9610`.

This gate should be included in a real assay only with prespecified
non-targeting/sham controls processed identically to candidates. It detects
shared assay failure; it does not prove absence of candidate-specific
confounding.

## Remaining Gap

An errors-in-variables analysis for the 2D endpoint cannot be calibrated from
synthetic assumptions alone. It requires blinded empirical technical-replicate
variance and a predeclared direct-3D co-primary analysis. This remains a real
new-data requirement.
