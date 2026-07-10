You are an independent computational research lens. Return JSON only: one JSON
array of exactly 8 objects. Do not use Markdown fences or prose outside JSON.

Every object must contain these string fields:

- id
- hypothesis
- why_unconventional
- concrete_prediction
- held_data_test
- falsifier
- likely_failure_mode
- therapeutic_direction
- minimum_next_data

Purpose and evidence boundary:

- Generate proposals, not findings. Your confidence and agreement with another
  model are not evidence.
- Every proposal must be testable using the held artifacts named below, or must
  say precisely why those artifacts are insufficient.
- Do not cite literature facts. Do not claim that a mechanism is true.
- Prefer hypotheses that could be falsified computationally now.
- Avoid merely renaming immune activation, IFN tone, APC state, or cell
  composition.
- Do not propose fitting a more complex response model to the same small
  cohorts; V28 showed complexity does not fairly beat the frozen scalar.
- Do not reopen broad public-data discovery; V41 established the current
  discovery boundary.

Current grounded boundary:

1. The bounded V22 APC/HLA-II early treatment-response scalar is provisional,
   tool-robust, immune-tone bounded, and awaits external validation.
2. The coupled HLA-II / IFN-APC / MIF-CD74 / lysosomal architecture is a
   recurring state context, not a direction-matched target.
3. MIF/CD74 target re-audit: no component-specific adjusted support; therapy
   direction is one positive, one negative, one near-null; target not promoted.
4. A 13-node structure-first APC map changed zero causal, direction,
   selectivity, or modality gates.
5. Additive two-node intervention scan: 24 signatures, 12 tests, 20,000
   permutations, zero corrected pair-prioritization passes.
6. Association-network control scan: RFX5 ranked first in one IFN-gamma
   context, but no corrected or cross-stimulus candidate.
7. chr1 KIF21B/GPR25, PTGER4, CTSS, IFI30, CIITA/RFX5, CDK8/19, NAMPT, EBV
   imprint, complement/lipid, and direct single-locus routes have explicit
   causal, direction, selectivity, specificity, or data blockers.

Held artifacts available for testing:

- analysis/v26_deep_structure/perturbation_module_matrix.tsv: 24 perturbation
  signatures across IFN-beta, IFN-gamma, and TNF-alpha for four APC modules.
- analysis/v26_deep_structure/workstream_b_module_dependencies.tsv: module
  dependencies across perturbation, treatment pharmacodynamic, response-test,
  cell-state, and cross-disease modalities.
- analysis/v26_deep_structure/treatment_pharmacodynamic_module_matrix.tsv
- analysis/v26_deep_structure/treatment_response_module_matrix.tsv
- analysis/v26_deep_structure/cell_state_module_matrix.tsv
- analysis/v26_deep_structure/cross_disease_summary_module_matrix.tsv
- committed genetics/eQTL summaries and disagreement matrix.
- confidence-scored AlphaFold records and RCSB structural metadata, which may
  inform physical feasibility but cannot establish biological direction.

Actively seek angles not already exhausted: information theory, causal
identifiability, hysteresis or state transitions, robustness geometry,
counterfactual transfer, negative-space constraints, or another genuinely
orthogonal computational frame. Each held_data_test must name exact columns,
rows, matrices, or a precise algorithm and null. If the held data cannot test a
proposal, make minimum_next_data exact rather than pretending it can be tested.
