# V57 Multifidelity Adversarial Extension Plan

Status: frozen before simulation. Synthetic method behavior only.

## Proposal Sources and Boundary

Independent generic design critiques were requested from the configured Claude
and Gemini lineages without sending repository data. Claude proposed a
leave-one-donor stability check against leverage and an errors-in-variables
co-analysis. Gemini proposed prespecified negative-control perturbations for
unmeasured assay drift. Model output is proposal-only and is not evidence.

The parent design already uses a one-sided intersection rule and simultaneous
candidate-family critical value, so the separate Claude multiplicity concern is
already handled. Errors-in-variables needs empirical technical-replicate
variance and is queued rather than simulated from an invented estimate.

This extension tests the two immediately groundable proposals.

## A. Leave-One-Donor Stability

For the parent incremental-information gate, recalculate held-out RMSE gain and
candidate-residual correlation after dropping every training donor and every
held-out donor in turn. The stability gate requires:

- parent incremental gate passes;
- every leave-one-donor gain remains at least 0.10;
- every leave-one-donor residual correlation remains at least 0.50.

Test at 12/8 and 16/12 training/held-out donor pairs under:

1. the parent complementary-3D generator;
2. a no-true-increment scenario where one donor in each panel receives the same
   large candidate-pattern artifact.

Eligibility requires, in every seed, at least 0.80 sensitivity for true
complementarity and at most 0.05 false scale-up under the leverage artifact.

## B. Negative-Control Fail-Stop

Add four non-targeting/sham controls, randomized and processed exactly like
candidates. For each panel, test each control mean against zero with a fixed
two-sided simultaneous normal critical value `2.50`. Any crossing invalidates
clean escalation and requires assay investigation.

Across three seeds and 5,000 screens per seed, require:

- clean-assay family false stop <= 0.05;
- common hidden drift detection >= 0.80;
- control-specific process artifact detection >= 0.80.

Negative controls can detect shared assay failure, not prove absence of
candidate-specific confounding.

## Interpretation

A passing extension characterizes safeguards under the committed generators.
It is not evidence about MS, any perturbation, any donor population, or any 2D
or 3D biological model.
