# Tooling Inventory V28

Date: 2026-06-07

Purpose: real reachability pre-flight for heterogeneous re-analysis of the
bounded APC/HLA-II treatment-response monitoring lead. This inventory was
written before V28 Workstream A modeling.

## Credential / Network

- OpenGWAS: reachable after explicit `.env` load.
  - Checker: `python3 scripts/check_opengwas_access.py`
  - Result: HTTP `200`; JWT valid until `2026-06-19 12:28 UTC`; `gwasinfo`
    and `tophits` POST calls for `ieu-b-18` succeed.
- PyPI: reachable.
  - Probe: `https://pypi.org/simple/scikit-learn/`
  - Result: HTTP `200`.
- OpenAI API host: reachable but no key present.
  - Probe: `https://api.openai.com/v1/models`
  - Result: HTTP `401` bearer-auth required, no proxy block observed.

## Languages / Runtimes

| Runtime | Status | Version / path | Notes |
|---|---|---|---|
| Python system | reachable | `/opt/homebrew/bin/python3`, Python `3.13.3` | Bare; core scientific packages not installed. |
| Python `.venv` | reachable | `.venv/bin/python` | NumPy/Pandas/SciPy/statsmodels/anndata available; no scikit-learn. |
| Python `.venv_v3_py312` | reachable | `.venv_v3_py312/bin/python` | Primary V28 analysis runtime; has scikit-learn, PyTorch, Scanpy, NetworkX, igraph. |
| R | reachable | R `4.6.0` | `coloc`, `susieR`, `nlme`, `mgcv`; no `limma`, `edgeR`, `glmnet`, `pROC`, or `tidymodels`. |
| Node.js | reachable | Node `v22.22.2` | Available, not needed for V28 statistics. |
| Java | reachable | OpenJDK via Homebrew | Available, not needed for V28. |
| Julia | absent | not found | Not available for V28. |
| Rust / Cargo | absent | not found | Not available for V28. |
| Go | absent | not found | Not available for V28. |

## Python Package Reachability

Primary usable runtime: `.venv_v3_py312`.

| Package | Status | Use in V28 |
|---|---|---|
| `numpy`, `pandas`, `scipy` | installed | Core statistics and permutation tests. |
| `sklearn` | installed | Ridge logistic regression, gradient boosting, random forest, Gaussian process classifiers, LOOCV. |
| `statsmodels` | installed | Fixed-effect and cohort-adjusted statistical models. |
| `torch` | installed | Small neural model is technically available, but V28 avoids it unless justified because n is tiny. |
| `anndata`, `scanpy` | installed | Available for single-cell follow-up; not needed for paired-score re-analysis. |
| `networkx`, `igraph` | installed | Available for graph/adjacent analyses. |
| `xgboost`, `lightgbm`, `catboost`, `pymc`, `gpytorch`, `tensorflow`, `dowhy`, `econml`, `causalml` | absent | Not used unless installed in a later run. |

## R Package Reachability

| Package | Status | Use in V28 |
|---|---|---|
| `coloc` `5.2.3`, `susieR` `0.14.2` | installed | Genetics only; not needed for V28 treatment-response re-analysis. |
| `nlme` `3.1.169`, `mgcv` `1.9.4` | installed | Potential mixed/additive modeling support. |
| `limma`, `edgeR`, `lme4`, `brms`, `rstanarm`, `randomForest`, `glmnet`, `pROC`, `caret`, `tidymodels` | absent | Not used. |

## Treatment-Response Inputs Present

| Artifact | Status |
|---|---|
| `docs/locked_rules/LOCKED_RULE_V22.md` | present; immutable baseline rule. |
| `docs/workups/treatment_response/APC_HLA_MONITORING_WORKUP_V23.md` | present; bounded-domain workup. |
| `docs/workups/treatment_response/COUPLED_AXIS_V27.md` | present; V27 coupled features failed to beat scalar. |
| `docs/validation/VALIDATION_READINESS_V27.md` | present; future-harness spec. |
| `analysis/v27_coupled_axis/v27_feature_table.tsv` | present; paired module deltas and V27 fixed features. |
| `analysis/v23_apc_hla_monitoring/gse253006_exact_compartments/` | present; exact UC compartment outputs. |

## Practical Tooling Decision

V28 can proceed locally with heterogeneous, grounded methods using
`.venv_v3_py312`: nonparametric statistics, cohort-adjusted models, LOOCV
regularized ML, Gaussian-process and tree-based classifiers, permutation nulls,
and graph/dynamical feature tests. External LLM/sub-model use is not available
without a key and is requested separately in `meta/TOOL_KEY_REQUESTS_V28.md`.
