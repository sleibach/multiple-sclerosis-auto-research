# Therapeutic Reviewer Quickstart V52

Date: 2026-07-10

Status: navigation and review guide. This document adds no evidence, changes no
verdict, and does not reopen discovery. It tells a reviewer how to read the V52
therapeutic-path artifacts without confusing validated findings, provisional
validation leads, structural context, and future data asks.

## Read These First

| order | artifact | why it matters |
|---:|---|---|
| 1 | `docs/reports/THERAPEUTIC_PATH_SUMMARY_CARD_V52.md` | fastest bottom line: monitoring first, no current intervention-grade target |
| 2 | `docs/reports/THERAPEUTIC_PATH_V52.md` | full synthesis and ranked routes toward impact |
| 3 | `docs/reports/THERAPEUTIC_CLAIM_HIERARCHY_V52.md` | claim boundary: what can be said now versus what remains context or future ask |
| 4 | `docs/reports/THERAPEUTIC_TARGET_EVIDENCE_MATRIX_V52.tsv` | machine-readable route and lead status table |
| 5 | `docs/validation/MEDICAL_TEAM_THERAPEUTIC_DATA_REQUEST_V52.md` | concrete data request that turns the synthesis into next action |

If time is short, read artifacts 1, 2, and 5. If reviewing rigor, include
artifacts 3 and 4.

## What The Reviewer Should Expect

| question | expected answer | check artifact |
|---|---|---|
| Is there a current MS target? | No. The project has no intervention-grade target under current evidence. | `docs/reports/THERAPEUTIC_PATH_V52.md` |
| What is the strongest near-term impact route? | External validation of the bounded APC/HLA-II treatment-response monitoring scalar. | `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md` |
| Does AlphaFold DB rescue closed genetics leads? | No. It sharpens feasibility context but does not solve causal-gene, direction, cell-state, or modality blockers. | `docs/reports/STRUCTURAL_EVIDENCE_BOUNDARY_QA_V52.md` |
| Did restored OpenGWAS reopen discovery? | No. It restored bounded rerun capacity only. | `docs/workups/genetics/OPENGWAS_PRE_EXPIRY_BOUNDED_POLISH_COMMANDS_V52.md` |
| What data would change the answer? | Complete paired response-validation data for monitoring; separate genotype-linked chr1 cell-state and perturbation data for target workup. | `docs/validation/VALIDATION_PACKAGE_FIELD_DICTIONARY_V52.tsv` |

## Evidence Classes To Keep Separate

| class in practical terms | examples | allowed use | not allowed |
|---|---|---|---|
| Locked rules and preregistration | V22 scalar, V42 plan, V42 interpretation grid | mechanical future validation | tuning after seeing data |
| Grounded project findings | V28 robustness, V32 confounder audit, V19 chr1 verdict, V41 exhaustion | project conclusions under stated limits | clinical validation without external cohort |
| Provisional validation route | bounded APC/HLA-II monitoring scalar | primary external validation target | treatment-switching rule or drug target |
| Mechanistic context | coupled APC architecture and immune-tone boundaries | interpretation and assay design | successor rule or target list |
| Structure context | GPR25, KIF21B, PTGER4 AlphaFold DB records | confidence-qualified feasibility context | disease evidence or target validation |
| Future data asks | Gafson/Karolinska, chr1 genotype-linked package, postpartum MS package | define what would be tested next | treated as evidence before arrival |

## How To Challenge The Main Conclusion

The V52 conclusion is deliberately narrow: monitoring / stratification is the
defensible near-term impact route; target-level impact awaits new data. A
reviewer should challenge it through these checks.

| challenge | where to look | what would change the conclusion |
|---|---|---|
| The monitoring scalar is overfit or confounded | `docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md`; `docs/validation/POWER_MAP_V43.md`; `docs/validation/BATCH_GUARD_V44.md` | External validation failure in an adequately powered clean cohort would demote the route. |
| chr1 should be target-ready already | `docs/workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md`; `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md` | Genotype-linked cell-state data plus direction-matched perturbation could move chr1 toward target workup. |
| Structure should count more heavily | `docs/reports/STRUCTURAL_EVIDENCE_BOUNDARY_QA_V52.md`; `docs/workups/genetics/STRUCTURE_AWARE_NO_GO_TABLE_V52.md` | Experimental or functional evidence could help future work, but AlphaFold DB context alone cannot resolve disease direction. |
| PTGER4 or ZMIZ1 was closed too strongly | `docs/workups/genetics/PTGER4_SIGNAL_SPECIFIC_REOPEN_SPEC_V52.md`; `docs/workups/genetics/ZMIZ1_RESTORED_OPENGWAS_HANDOFF_V52.md` | Signal-specific MS-protective direction and perturbation evidence would be required. |
| Public-data computation might still find a target | `docs/history/JOINT_INFERENCE_V41.md` | A new held-out-validated signal under the V41 gate, or genuinely new data, would be needed. |

## Common Misreadings To Avoid

1. A validated monitor would not by itself be a treatment-switching rule.
2. An underpowered external cohort should report effect size and confidence
   interval, not a pass or kill by narrative.
3. AlphaFold DB tractability context is not disease evidence.
4. External literature agreement can corroborate context, but it does not
   validate the locked scalar.
5. Restored OpenGWAS authentication is operational capacity, not a scientific
   result.
6. A closed target can be reopened only by the specific missing evidence named
   in the reopen artifacts, not by general prior-art plausibility.

## Artifact Map For Specific Reviewer Roles

| reviewer role | read |
|---|---|
| Medical lead | summary card; medical-team data request; monitoring decision tree |
| Genetics reviewer | therapeutic path; chr1 specification; GPR25/KIF21B/PTGER4 modality specs; OpenGWAS command list |
| Validation operator | command manifest; field dictionary; decision tree; result-report template; operator card |
| Drug-discovery reviewer | target evidence matrix; structure-aware no-go table; structural boundary QA; modality specs |
| Skeptical methods reviewer | V41 joint inference; V43 power map; V44 batch guard; therapeutic skeptic checklist |

## One-Sentence Review Verdict

The V52 artifact set supports a monitoring-first clinical validation path and a
separate chr1 controlled-data handoff, but it does not support starting an MS
target program from the current evidence.

