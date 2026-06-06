# V25_BUILD_QUEUE

Last updated: 2026-06-06 20:55 UTC

## Queue

1. completed - Verify OpenGWAS token and read resume state.
2. completed - Inventory available model-building datasets.
3. completed - Commit immutable train/held-out split before model fitting.
4. in_progress - Build bounded empirical immune-state module-response model.
5. pending - Validate on held-out perturbations with calibration.
6. pending - Test against project findings.
7. pending - Triage live hypotheses only inside validated domain.
8. pending - Write `MODEL_CARD_V25.md`, update resume state, rebuild index,
   commit.

## Current Scope

The model is deliberately narrow. It predicts perturbation effects on
project-defined immune-state modules from Mixscale pathway perturbation data.
It does not attempt patient outcome prediction and does not claim single-cell
cell-state simulation.

## Integrity Lock

The immutable train/held-out split is:

- `analysis/v25_immune_state_model/TRAIN_HELDOUT_SPLIT_V25.tsv`

The split was written before model metrics were generated. Do not move held-out
perturbations after seeing validation results.
