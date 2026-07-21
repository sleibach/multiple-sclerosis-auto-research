# V54 Progression Frontier

Status: in progress. This report is cumulative and is updated as each
progression-focused probe reaches a grounded, resumable result.

## North-Star Boundary

The clinical objective is to halt disability accumulation in progressive MS.
The held public corpus does **not** contain a transcriptomic cohort with a
longitudinal disability outcome, so no V54 computation can establish that a
state predicts, causes, or can halt progression. V54 can still test bounded
necessary context: cross-sectional progressive subtype differences and
donor-aware chronic-active lesion states. Those are progression-adjacent
associations, not efficacy evidence.

Discovery remains closed under the V41 boundary. V54 performs targeted tests of
pre-existing modules and progression questions; it does not promote an
unexpected public-data pattern as a new finding.

## Progression Data Inventory

Status: **complete; coverage audit, not a biological result**.

Executable audit:

- `scripts/v54_progression_data_inventory.py`
- `analysis/v54_progression_data_inventory/REPORT.md`
- `analysis/v54_progression_data_inventory/progression_data_inventory.tsv`
- `analysis/v54_progression_data_inventory/progression_question_semantic_contract.tsv`

Seven held datasets or packages were audited. Only two bounded question types
are currently testable:

1. Cross-sectional PPMS-versus-SPMS module differences in the Macnair discovery
   package, restricted to Amsterdam and UK sources where both stages occur.
2. Small-donor chronic-active lesion-state contrasts in GSE180759.

Four clinically decisive questions are blocked or non-identifiable: repeated
disability prediction, RRMS-to-progressive transition, treatment-mediated
slowing, and a well-powered RRMS-versus-progressive brain comparison.

The highest-value first test is the source-overlap-restricted PPMS-versus-SPMS
comparison. It has 21 PPMS and 30 SPMS donors after excluding the one Edinburgh
SPMS donor whose source has no PPMS comparator. It remains cross-sectional and
cannot measure progression rate or transition.

## Outcome Ledger

| probe | result | evidence boundary |
|---|---|---|
| Progression-data semantic inventory | complete | Coverage and identifiability audit only; no biological claim. |
| Source-balanced PPMS versus SPMS module comparison | in progress | Cross-sectional disease-stage association only. |

