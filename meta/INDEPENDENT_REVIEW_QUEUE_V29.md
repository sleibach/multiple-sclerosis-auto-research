# Independent Review Queue V29

Date: 2026-06-07

## Key Status

Cross-lineage model keys checked after loading `.env`:

- `ANTHROPIC_API_KEY`: absent.
- `GOOGLE_API_KEY`: absent.
- `GEMINI_API_KEY`: absent.

Workstream A is therefore queued. No independent sub-model output was used in
V29, and no model-generated proposal is treated as evidence.

## Requested Model

Preferred: Anthropic Claude via `ANTHROPIC_API_KEY`.

Fallback: Google/Gemini via `GOOGLE_API_KEY` or `GEMINI_API_KEY`.

Reason for non-OpenAI request: this agent is OpenAI-lineage; V29 specifically
needs a different failure mode and different priors.

## Review Package To Feed The Independent Lens

Give the model the following project package, in this order:

1. `meta/CURRENT_STATUS.md`
2. `meta/NEXT_ACTIONS.md`
3. `docs/workups/treatment_response/ROBUSTNESS_MAP_V28.md`
4. `docs/workups/treatment_response/APC_HLA_MONITORING_WORKUP_V23.md`
5. `docs/findings/DEEP_STRUCTURE_V26.md`
6. `docs/history/LEAD_SLATE_V20.md`
7. `docs/history/LEAD_SLATE_V21.md`
8. `docs/workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md`
9. `docs/workups/genetics/GENETICS_EQTL_WORKUP_V16.md`
10. `knowledge/candidates/NAMPT.md`
11. `knowledge/candidates/MIF_CD74_STRATIFICATION.md`
12. `meta/MATRIX_STATUS.md`

## Prompt For Independent Lens

You are an adversarial reviewer from outside the project's usual
genetics/transcriptomics framing. Your output is not evidence; it is a proposal
queue for grounding.

Review the MS autoimmune research project and identify:

1. Overlooked cross-domain connections between treatment-response monitoring,
   genetics, pregnancy/postpartum biology, metabolism, structural biology, and
   tissue repair.
2. Dormant or parked leads that were dropped for a reason later corrected by
   the project, such as over-strict prior-art gating or class-precedent
   druggability assumptions.
3. Assumptions the project repeatedly makes but has not tested.
4. Analyses a researcher from metabolism, structural biology, systems
   immunology, or neurology would run that this project has avoided.
5. The top five proposals that are concrete enough to test on existing data.

For each proposal, return:

- short name;
- why the project may have missed it;
- exact data artifact(s) to test it on;
- expected direction if true;
- falsification test;
- whether it needs new data.

## Grounding Rule For Future Session

For every proposal returned by the independent lens:

1. Add it to `meta/queues/V29_QUEUE.md`.
2. Query the local RAG index for prior runs on the same analysis.
3. Implement the proposal on real local data or mark it blocked with the exact
   missing data/tool.
4. Record outcome as `held`, `failed`, or `inconclusive` in
   `docs/history/LEAD_INVENTORY_V29.md`.
5. Do not cite model confidence or language as evidence.
