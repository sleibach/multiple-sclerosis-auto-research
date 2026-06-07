# Robustness Map V28

Date: 2026-06-07

## Scope

V28 re-attacked the bounded APC/HLA-II early treatment-response monitoring lead
with heterogeneous local tools and a paid/gated-tool preflight. The immutable
baseline remained `docs/locked_rules/LOCKED_RULE_V22.md`; no V22 module, class,
threshold, endpoint, or cohort rule was edited. No fresh Gafson/NEDA cohort was
present or read.

Executable analysis:

- `scripts/v28_heterogeneous_response_analysis.py`

Outputs:

- `analysis/v28_heterogeneous_response/heterogeneous_method_metrics.tsv`
- `analysis/v28_heterogeneous_response/cohort_adjusted_models.tsv`
- `analysis/v28_heterogeneous_response/bayesian_bootstrap_effects.tsv`
- `analysis/v28_heterogeneous_response/jackknife_influence.tsv`
- `analysis/v28_heterogeneous_response/v28_summary.json`

Seed: `28028`.

## Tooling Result

Reachability inventory:

- `meta/TOOLING_INVENTORY_V28.md`

Paid/gated key requests:

- `meta/TOOL_KEY_REQUESTS_V28.md`

No paid service was used in V28. `OPENAI_API_KEY` is requested as an optional
low-cost external critique/proposal lens. The OpenAI API host is reachable, but
no key is currently configured. Sub-model output was therefore not used as
evidence or as an ungrounded claim.

## Workstream A: Heterogeneous Re-Analysis

Primary set: bounded immune-remodeling/JAK-STAT domain:

- `GSE235357` MS dimethyl fumarate.
- `GSE253006_TOF_exact` UC tofacitinib exact rescoring.
- `n = 19`.

### Fixed-Score / Nonparametric Evidence

| Score | AUC | Bootstrap CI | Hedges g | Permutation p | Mann-Whitney greater p |
|---|---:|---|---:|---:|---:|
| V22 locked scalar | `0.811` | `0.578-1.000` | `1.191` | `0.0080` | `0.0124` |
| receptor control | `0.656` | `0.367-0.900` | `0.637` | `0.1419` | `0.1352` |
| V27 coupled projection | `0.689` | `0.414-0.917` | `0.661` | `0.0740` | `0.0890` |
| V27 coupled augmented | `0.633` | `0.352-0.869` | `0.542` | `0.1864` | `0.1739` |
| V27 coupling coordination | `0.733` | `0.477-0.932` | `0.777` | `0.0435` | `0.0471` |

Interpretation: the original locked scalar is the strongest fixed score. The
receptor control does not reproduce it. One coupled feature remains directional
but weaker than the scalar, consistent with V27.

### Cohort-Adjusted Model

Linear probability model with cohort fixed effects:

- bounded set: locked-score coefficient `0.322`, robust p
  `5.70e-07`, R2 `0.331`.
- all primary plus exact UC: locked-score coefficient `0.231`, robust p
  `0.00263`, R2 `0.130`.

Interpretation: the signal is not only a raw pooled rank artifact; it remains
positive after accounting for cohort labels. This is still small-n and should
not be mistaken for external validation.

### Bayesian Bootstrap

Posterior over responder-minus-nonresponder mean locked score:

- bounded set: mean difference `0.994`, 95% interval `0.388-1.715`,
  posterior P(diff > 0) `0.999`.
- all primary plus exact UC: mean difference `0.494`, 95% interval
  `0.067-0.979`, posterior P(diff > 0) `0.9885`.

Interpretation: under a distribution-light Bayesian-bootstrap lens, the locked
score direction is stable in the bounded set and remains positive, but smaller,
when the failed/out-of-domain cohorts are included.

### Regularized ML Lens

Ridge logistic LOOCV using `delta_IFN_APC`, `delta_HLAII`, `delta_RECEPTOR`,
and `locked_signed_score`:

- bounded set AUC `0.578`, CI `0.286-0.856`, Hedges g `0.582`.
- all primary plus exact UC AUC `0.575`, CI `0.402-0.747`, Hedges g `0.123`.

Interpretation: flexible multifeature modeling does not improve the lead; it
dilutes it. This is important. The signal is not strengthened by throwing more
features or model flexibility at the tiny cohorts. The most defensible form
remains the pre-locked scalar.

Heavier tree/SVM/Gaussian-process branches were reachable in principle through
scikit-learn but were not retained for the final V28 run because LOOCV/null
runtime was disproportionate to the tiny sample size. This limitation does not
affect the primary fixed-score conclusion.

## Workstream B: Sub-Model Lens

No external LLM or hosted foundation-model key was present. V28 therefore did
not use sub-model output. This is a documented block, not a silent omission.

Grounded local hostile proposals tested instead:

| Proposal | Grounded test | Result |
|---|---|---|
| Receptor-state confounding could explain the pass. | Receptor-only module AUC and permutation p. | Failed: receptor AUC `0.656`, p `0.142`, weaker than scalar by `0.156`. |
| Cohort pooling could explain the pass. | Cohort fixed-effect model. | Failed as sole explanation: locked-score coefficient remains positive, robust p `5.70e-07` in bounded set. |
| One or two subjects could drive the bounded pass. | Leave-one-subject jackknife. | Failed as sole explanation: bounded jackknife AUC range `0.788-0.888`; no single subject removes the signal. |
| V26 dynamic/coupled geometry could improve the rule. | Coupled and dynamic adjacent feature tests. | Mostly failed: coupled features and vector/angle features do not beat V22 scalar. |

If `OPENAI_API_KEY` is provided, the next run can use the requested checker and
ask for additional critique proposals, but those proposals must still be
implemented against these same local data before they matter.

## Workstream C: Cross-Tool Robustness Verdict

Agreement:

- The bounded V22 scalar is positive under raw AUC, nonparametric rank test,
  permutation null, cohort-adjusted regression, Bayesian bootstrap, and
  jackknife influence analysis.
- The receptor-only negative control does not reproduce the scalar's strength.
- All-primary/unbounded analysis is weaker, matching V23's bounded-domain
  interpretation.

Divergence:

- Regularized multifeature ML does not recover an improved predictive rule.
- V27 coupled-axis and V28 dynamic vector features remain weaker than the
  scalar.
- The lead is not a general multifeature response classifier; it is a narrow
  fixed pharmacodynamic scalar that remains data-limited.

Verdict:

> The bounded APC/HLA-II monitoring signal is **statistically tool-robust but
> model-flexibility fragile**. Multiple independent statistical lenses confirm
> the locked scalar's direction in the bounded domain, but flexible ML and
> coupled/dynamic extensions do not improve it. The lead is strengthened as a
> simple, pre-locked monitoring scalar, not as a broader learned classifier.

## Workstream D: Adjacent Analyses

Dynamic/vector features tested:

| Feature | Bounded AUC | Hedges g | Permutation p | Verdict |
|---|---:|---:|---:|---|
| APC vector norm | `0.389` | `-0.109` | `0.775` | not supported |
| HLA-vs-IFN angle | `0.489` | `-0.104` | `0.521` | not supported |
| HLA/IFN product | `0.644` | `0.094` | `0.131` | not supported |

Interpretation: treating response as vector magnitude/angle in module-change
space does not improve the lead. Directional class-aware scalar movement is
more informative than generic trajectory geometry in the held cohorts.

## Breadth Value

V28 added value by narrowing what should be trusted:

- It strengthened confidence that the V22 scalar is not only an artifact of one
  original analysis implementation.
- It weakened the case for adding complexity: receptor, coupled, dynamic, and
  regularized multifeature variants do not beat the scalar.
- It identified a tooling gap: an external sub-model lens is reachable only
  after an API key is provided, and should be used for proposal generation, not
  evidence.

No cure-class finding is claimed. The next real validation step remains a fresh
paired cohort, preferably Gafson et al. 2018 DMF PBMC RNA-seq with NEDA-4
labels, scored mechanically under `LOCKED_RULE_V22.md`.
