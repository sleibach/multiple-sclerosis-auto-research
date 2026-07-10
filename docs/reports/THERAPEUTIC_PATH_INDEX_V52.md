# Therapeutic Path Artifact Index V52

Date: 2026-07-10

Status: navigation aid. This index adds no evidence and changes no verdict. It
maps the V52 therapeutic-path artifacts by reader use case.

## Fast Reading Order

1. `docs/reports/THERAPEUTIC_PATH_SUMMARY_CARD_V52.md`
2. `docs/reports/THERAPEUTIC_PATH_V52.md`
3. `docs/validation/MEDICAL_TEAM_THERAPEUTIC_DATA_REQUEST_V52.md`
4. `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md`
5. `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md`

This order gives the practical bottom line first, then the full synthesis, then
the two actionable data packages: monitoring validation and chr1 target
resolution.

## Executive And Downstream Synthesis

| artifact | reader | use |
|---|---|---|
| `docs/reports/THERAPEUTIC_PATH_SUMMARY_CARD_V52.md` | medical team / project lead | one-page bottom line: monitoring first, no intervention-grade target |
| `docs/reports/THERAPEUTIC_PATH_V52.md` | scientific reviewer | full synthesis of monitoring route, genetics closures, structure context, and restored OpenGWAS |
| `docs/reports/THERAPEUTIC_TARGET_EVIDENCE_MATRIX_V52.tsv` | downstream tooling / spreadsheet review | machine-readable route and lead status table |
| `docs/reports/THERAPEUTIC_REOPEN_CHECKLIST_V52.tsv` | downstream tooling / go-no-go review | machine-readable reopen gates and non-counting evidence for closed or conditional leads |
| `docs/reports/THERAPEUTIC_SKEPTIC_REBUTTAL_CHECKLIST_V52.md` | external reviewer / skeptical reader | pre-answers objections to monitoring-first and no-target conclusions |
| `docs/reports/THERAPEUTIC_ARTIFACT_CONSISTENCY_AUDIT_V52.md` | project maintainer / reviewer | verifies V52 artifacts preserve one route ranking and no-target conclusion |
| `docs/reports/THERAPEUTIC_CLAIM_HIERARCHY_V52.md` | author / reviewer | separates grounded findings, provisional claims, context, handoffs, and future asks |
| `docs/reports/THERAPEUTIC_PATH_INDEX_V52.md` | all readers | navigation across V52 artifacts |

## Validation Execution

| artifact | reader | use |
|---|---|---|
| `docs/validation/THERAPEUTIC_VALIDATION_HANDOFF_V52.md` | validation operator / medical team | what each Gafson/Karolinska result would mean clinically |
| `docs/validation/MEDICAL_TEAM_THERAPEUTIC_DATA_REQUEST_V52.md` | medical team / data owner | sendable request packet separating monitoring validation from chr1 target development |
| `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md` | validation operator | mechanical if/then interpretation tree for package receipt and V42/V44 outcomes |
| `docs/validation/MONITORING_VALIDATION_COMMAND_MANIFEST_V52.md` | validation operator | exact command order for preflight, self-test, frozen harness, and interpretation routing |
| `docs/validation/PREREGISTRATION_V42.md` | validation operator | frozen Gafson analysis plan |
| `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md` | validation operator / reviewer | pre-committed interpretation of pass/fail/inconclusive outcomes |
| `docs/validation/POWER_MAP_V43.md` | study designer | cohort-size and effect-size expectations |

## Genetics And Target Handoff

| artifact | lead | use |
|---|---|---|
| `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md` | chr1 KIF21B/GPR25 | exact future data package needed to resolve causal gene, cell state, and direction |
| `docs/workups/genetics/CHR1_DIRECTION_MATCHED_EXPERIMENT_BLUEPRINT_V52.md` | chr1 KIF21B/GPR25 | staged experiment flow from genotype-linked data to perturbation and modality decision |
| `docs/workups/genetics/GPR25_DIRECTION_MATCHED_MODALITY_SPEC_V52.md` | GPR25 | required protective-haplotype to agonism/restoration chain |
| `docs/workups/genetics/KIF21B_RESTORATION_MODALITY_SPEC_V52.md` | KIF21B | required restoration/up-function chain |
| `docs/workups/genetics/PTGER4_SIGNAL_SPECIFIC_REOPEN_SPEC_V52.md` | PTGER4 | signal-specific reopen gate for a direction-conflicted locus |
| `docs/workups/genetics/ZMIZ1_RESTORED_OPENGWAS_HANDOFF_V52.md` | ZMIZ1 | bounded direction polish and transfer-warning status |
| `docs/workups/genetics/STRUCTURE_AWARE_NO_GO_TABLE_V52.md` | multiple | why structure does not override causal-gene/direction/modality blockers |
| `docs/workups/genetics/RESTORED_OPENGWAS_CATCHUP_V52.md` | genetics reruns | completed renewed-token checks and results |
| `docs/workups/genetics/RESTORED_OPENGWAS_BOUNDED_RERUN_MANIFEST_V52.md` | genetics reruns | allowed bounded reruns and explicitly excluded discovery work |

## Structural Context

| artifact | protein | use |
|---|---|---|
| `knowledge_external/structures/alphafold/GPR25_O00155/record.json` | GPR25 | confidence-scored AlphaFold DB record |
| `knowledge_external/synthesis/V51_GPR25_ALPHAFOLD_DRUGGABILITY_CONTEXT.md` | GPR25 | receptor-core tractability context and limitations |
| `knowledge_external/structures/alphafold/KIF21B_O75037/record.json` | KIF21B | confidence-scored AlphaFold DB record |
| `knowledge_external/synthesis/V52_KIF21B_ALPHAFOLD_DRUGGABILITY_CONTEXT.md` | KIF21B | motor/binding-region context and restoration-direction limits |
| `knowledge_external/structures/alphafold/PTGER4_P35408/record.json` | PTGER4 | confidence-scored AlphaFold DB record |
| `knowledge_external/synthesis/V52_PTGER4_ALPHAFOLD_DRUGGABILITY_CONTEXT.md` | PTGER4 | EP4 receptor-core context and signal/direction limits |
| `docs/reports/STRUCTURAL_EVIDENCE_BOUNDARY_QA_V52.md` | all structures | audit that V52 wording keeps AlphaFold DB outputs as context only |

## External Context And Future Tension Handling

| artifact | use |
|---|---|
| `knowledge_external/synthesis/V52_THERAPEUTIC_CONVERGENCE_CONTRADICTION.md` | checks whether sharper external context converges with or contradicts V52 therapeutic verdicts |
| `docs/reports/THERAPEUTIC_CONTRADICTION_SURVEILLANCE_V52.md` | pre-defines future same-evidence-level contradiction triggers |
| `docs/knowledge/EPISTEMIC_CLASSES.md` | epistemic-class boundary for grounded, external, and structural context |
| `scripts/v47_provenance_gate.py` | machine gate enforcing provenance segregation |

## Current Practical Bottom Line

| question | answer | primary artifact |
|---|---|---|
| What should be validated first? | Bounded APC/HLA-II early treatment-response monitoring scalar | `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md` |
| Is there an intervention-grade target now? | No | `docs/reports/THERAPEUTIC_PATH_V52.md` |
| Which target route is closest if new data arrive? | chr1 KIF21B/GPR25, but only with genotype-linked cell-state direction and perturbation | `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md` |
| Does AlphaFold rescue a closed lead? | No | `docs/reports/STRUCTURAL_EVIDENCE_BOUNDARY_QA_V52.md` |
| Does renewed OpenGWAS reopen discovery? | No | `docs/workups/genetics/RESTORED_OPENGWAS_BOUNDED_RERUN_MANIFEST_V52.md` |
