# MODEL_CARD_V25

Date: 2026-06-06

## Verdict

V25 did **not** produce a reliable reusable immune-state simulator.

The most honest validated product is a narrow empirical Mixscale module-response
model, and it fails to reach a useful held-out standard:

- held-out perturbations: `6`;
- held-out module predictions: `24`;
- direction accuracy: `0.542`;
- MAE: `0.261` log2FC;
- RMSE: `0.360` log2FC;
- Pearson predicted-vs-actual: `0.531`;
- Spearman predicted-vs-actual: `0.377`.

This is not strong enough to triage wet-lab hypotheses with confidence. The
model should not be used as a decision tool.

## Architecture

Architecture chosen in `MODEL_DESIGN_V25.md`:

- bounded empirical pathway/module mean model;
- trained on Mixscale pathway perturbation module summaries;
- predicts module-level mean log2FC for IFNB, IFNG, and TNFA pathway contexts.

Rejected:

- broad foundation-model fine-tuning: not feasible and not validateable from
  currently available mapped module outputs;
- mechanistic ODE/Boolean model: underdetermined;
- broad ML model: too few validated perturbation observations.

## Data

Inventory:

- `analysis/v25_immune_state_model/DATA_INVENTORY_V25.tsv`

Core train/validation substrate:

- `results_v3/mixscale/mixscale_module_summary.tsv`

External check substrate:

- `results_v3/state_parse_cd14_per_target_validation.tsv`
- `data/raw_v3/state_parse_split4/CD14_Mono_real_de.csv`
- `data/raw_v3/state_parse_split4/CD14_Mono_pred_de.csv`

State/Parse limitation:

- the State CD14 predictions have real-vs-predicted held-out validation, but
  feature IDs are not gene-symbol mapped for the project modules. Prior project
  status records `module_scoring_status = blocked_no_gene_symbols_for_feature_ids`.
  Therefore State cannot currently supply APC/HLA-II module predictions.

## Immutable Held-Out Split

Split file:

- `analysis/v25_immune_state_model/TRAIN_HELDOUT_SPLIT_V25.tsv`

Committed before validation in commit:

- `0bc726e`

Split:

- train perturbations: `18`;
- held-out perturbations: `6`;
- held-out perturbations: IFNB `IFNAR1`, IFNB `STAT1`, IFNG `HLA-DQB1`, IFNG
  `JAK2`, TNFA `CHUK`, TNFA `NFKB1`.

The split was not moved after seeing results.

## Held-Out Validation

Outputs:

- `analysis/v25_immune_state_model/heldout_predictions.tsv`
- `analysis/v25_immune_state_model/heldout_metrics_by_module.tsv`
- `analysis/v25_immune_state_model/calibration_by_confidence_bin.tsv`
- `analysis/v25_immune_state_model/model_validation_summary.json`

By-module direction accuracy:

| Module | n | Direction accuracy | MAE log2FC |
|---|---:|---:|---:|
| `gilt_lysosomal_apc` | 6 | 0.333 | 0.102 |
| `hla_ii_apc` | 6 | 0.500 | 0.344 |
| `ifn_apc` | 6 | 0.667 | 0.446 |
| `mif_cd74_receptor_state` | 6 | 0.667 | 0.154 |

Calibration:

| Confidence bin | n | Empirical direction accuracy | Mean abs error |
|---|---:|---:|---:|
| low | 12 | 0.500 | 0.168 |
| medium | 8 | 0.500 | 0.325 |
| high | 4 | 0.750 | 0.415 |

The higher-confidence bin has better direction accuracy but worse magnitude
error and only four observations. This is not enough to claim calibrated
confidence.

## Domain of Validity

Validated domain is too weak for deployment.

At most, this model can be used as a low-resolution descriptive prior for
Mixscale-like IFNB/IFNG/TNFA pathway perturbations on the four represented
modules. It cannot predict patient response, single-cell compartments, genetic
effect directions, or unseen pathways.

Required abstentions:

- `KIF21B/GPR25` chr1 expression-direction lead: outside domain.
- `ZMIZ1` opposite-direction genetics decoupling: outside domain.
- treatment-response clinical monitoring: outside domain as a patient-level
  rule; only broad IFNG/JAK module direction is weakly represented.

## Project-Finding Checks

Treatment-response monitoring biology:

- The model predicts IFNG/JAK-context decreases in `ifn_apc` and `hla_ii_apc`
  modules. This is directionally compatible with the idea that cytokine/JAK
  perturbation moves IFN/APC modules, but it does not validate the V22/V23
  patient-monitoring rule.

T/B compartment localization:

- Not assessable. Mixscale summaries here are cancer-line pathway perturbations,
  not immune T/B compartment data.

chr1 `KIF21B/GPR25`:

- Abstain. Genetics/eQTL expression direction is not represented in the
  validated perturbation domain.

`ZMIZ1`:

- Abstain. Opposite-direction cross-disease genetic decoupling is not
  represented in the validated perturbation domain.

## Live Hypothesis Triage

Output:

- `analysis/v25_immune_state_model/live_hypothesis_triage.tsv`

Triage verdict:

- IFN/JAK-STAT immune-remodeling monitoring signal: inside bounded pathway
  module domain only as a low-resolution directional prior, not a decision.
- IFNG/HLA-II/APC pathway remodeling: same limitation.
- KIF21B/GPR25: model abstains.
- ZMIZ1: model abstains.

No wet-lab candidate should be advanced or killed based on this model.

## Failure Modes

1. Training data are too small: 18 train perturbations and 6 held-out
   perturbations cannot support a robust simulator.
2. Mixscale pathways are not immune patient compartments.
3. State/Parse outputs are not module-scoreable until feature IDs are mapped to
   gene symbols.
4. Treatment-response data are too small and outcome-oriented, not perturbation
   training data.
5. Genetics/eQTL data provide causal direction but not perturbation-response
   module changes.

## What Would Upgrade This

The model build needs one of:

1. A gene-symbol-mapped State/Parse output or model interface that produces
   module-level predictions directly.
2. A larger immune-cell perturbation compendium with matched module outputs,
   ideally primary human PBMC/T/B/myeloid perturbations.
3. Controlled or collaborator datasets with genotype-linked perturbation or
   treatment-response time courses.

Until then, a validated in-silico immune-state simulator is not achievable from
current public/local data.

## Reproducibility

Script:

- `scripts/v25_build_bounded_immune_state_model.py`

Inputs:

- `results_v3/mixscale/mixscale_module_summary.tsv`
- `analysis/v25_immune_state_model/TRAIN_HELDOUT_SPLIT_V25.tsv`

Outputs:

- `analysis/v25_immune_state_model/bounded_model_parameters.tsv`
- `analysis/v25_immune_state_model/heldout_predictions.tsv`
- `analysis/v25_immune_state_model/heldout_metrics_by_module.tsv`
- `analysis/v25_immune_state_model/calibration_by_confidence_bin.tsv`
- `analysis/v25_immune_state_model/live_hypothesis_triage.tsv`
- `analysis/v25_immune_state_model/model_validation_summary.json`

No model output in this card is fabricated; all metrics come from the script
above.
