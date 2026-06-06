# V25_BUILD_QUEUE

Last updated: 2026-06-06 20:55 UTC

## Queue

1. completed - Verify OpenGWAS token and read resume state.
2. completed - Inventory available model-building datasets.
3. completed - Commit immutable train/held-out split before model fitting.
4. completed - Build bounded empirical immune-state module-response model.
5. completed - Validate on held-out perturbations with calibration.
6. completed - Test against project findings.
7. completed - Triage live hypotheses only inside validated domain.
8. in_progress - Write `MODEL_CARD_V25.md`, update resume state, rebuild index,
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

## Current Verdict

V25 did not achieve a reliable simulator. Held-out direction accuracy is `0.542`
across `24` module predictions, and calibration is too weak for wet-lab triage.
The model card documents this as a bounded negative result.
