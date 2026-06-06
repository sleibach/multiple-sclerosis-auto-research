# MODEL_DESIGN_V25

Date: 2026-06-06

## Objective

Build the most capable immune-state perturbation model the current data can
validate honestly. Required input is a perturbation specification; required
output is predicted direction and magnitude of changes in immune-state modules
relevant to the project: IFN/APC, HLA-II/APC, lysosomal/GILT/APC, and
MIF/CD74-receptor state.

## Data Reality

Available data are broad but uneven:

- Mixscale pathway perturbation summaries have gene-symbol-level module outputs
  and are directly usable for module-response modeling.
- State/Parse CD14 monocyte outputs have matched real and predicted
  differential expression and a real validation table, but the feature IDs are
  not mapped to gene symbols. Prior project work explicitly recorded
  `module_scoring_status = blocked_no_gene_symbols_for_feature_ids`.
- Treatment-response cohorts validate the clinical monitoring signal but are
  too small and outcome-focused to train a perturbation simulator.
- Genetics/eQTL data inform live hypotheses but are not perturbation-response
  training data.

## Architecture Choice

Chosen architecture: **bounded empirical module-response model**.

The model learns pathway-by-module and perturbation-class effects from
Mixscale module summaries and predicts held-out perturbation module effects by
training-set pathway/module means. This is intentionally simple. Its advantage
is that it can be validated cleanly on perturbations not used for fitting.

Rejected alternatives:

- **Fine-tuned foundation model**: infeasible for this session and not
  validateable on module genes from the available State output because feature
  IDs lack gene-symbol mapping.
- **Mechanistic ODE/Boolean circuit**: underdetermined. The project lacks
  enough perturbation observations for parameter identification across the
  IFN/APC/HLA-II circuit.
- **Broad ML perturbation predictor**: sample size is too small after enforcing
  held-out validation. A higher-capacity model would fit noise.
- **Hybrid model**: reasonable future direction, but current data support only
  a narrow empirical layer plus explicit abstention outside domain.

## Immutable Split

Split file:

- `analysis/v25_immune_state_model/TRAIN_HELDOUT_SPLIT_V25.tsv`

Rule:

- perturbations are sorted by pathway and perturbation name;
- every fifth perturbation within each pathway is held out;
- all other perturbations are training.

Counts:

- train: 18 perturbations;
- held out: 6 perturbations;
- represented pathways: IFNB, IFNG, TNFA.

This split is frozen. Do not alter it after validation.

## Predictions

Input:

- pathway context (`IFNB`, `IFNG`, `TNFA`);
- perturbation gene.

Output:

- module-level predicted mean log2 fold-change;
- predicted direction: suppresses, increases, or neutral;
- confidence from training-set pathway/module variability and calibration.

## Domain of Intended Validity

Potentially valid only for:

- Mixscale-like pathway perturbations;
- module outputs represented in `phases/v3/results/mixscale/mixscale_module_summary.tsv`;
- pathway contexts represented in training data.

The model must abstain for:

- genes/pathways not represented by the Mixscale pathway context;
- patient-level treatment response;
- genetics-only hypotheses such as KIF21B/GPR25 expression direction;
- State/Parse CD14 predictions until feature IDs are mapped to gene symbols.

## Success Criteria

Held-out validation must show useful direction prediction and calibrated
confidence. A model that is confidently wrong is a failed model even if average
direction accuracy is above chance.
