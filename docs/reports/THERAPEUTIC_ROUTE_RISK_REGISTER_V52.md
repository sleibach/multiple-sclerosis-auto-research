# Therapeutic Route Risk Register V52

Date: 2026-07-10

Status: risk register. This document adds no evidence, changes no verdict, and
does not reopen discovery. It records residual risks around the V52
therapeutic-path synthesis and points to the artifact that currently mitigates
each risk.

## Executive Risk Posture

The main risk is not missing a ready target. The main risk is overinterpreting a
bounded monitoring signal or structurally plausible genetics lead beyond the
evidence it has. V52 mitigates that by separating monitoring validation,
prospective utility, and target workup into different packages with different
evidence thresholds.

## Route-Level Risks

| route | residual risk | severity | current mitigation | trigger for escalation |
|---|---|---:|---|---|
| Bounded APC/HLA-II monitoring scalar | external validation may be underpowered or batch-bounded, producing an inconclusive result that is over-read | high | V42 preregistration, V44 batch guard, V43 power map, V52 decision tree | complete external package produces fail, clean pass, or immune-tone-bounded pass under frozen harness |
| Monitoring clinical utility | a clean validation pass may be mistaken for evidence that score-guided treatment action improves outcomes | high | V52 prospective utility sketch and clinical-utility boundary checklist | validation passes and medical team asks how to use the score prospectively |
| APC/HLA/IFN coupled architecture | mechanistic recurrence may be mistaken for a superior rule or target list | medium | V27/V28 no-improvement result, V52 claim hierarchy, V52 artifact consistency audit | proposal to fit a successor rule on validation data |
| chr1 KIF21B/GPR25 locus | real locus biology may be prematurely converted into a target program before causal gene, cell state, and direction are resolved | high | chr1 genotype-linked data spec, experiment blueprint, collaborator appendix, no-go table | genotype-linked immune/CSF package arrives |
| GPR25 | GPCR-like structure may make receptor tractability look more advanced than the biology supports | high | GPR25 modality spec, structure boundary QA, chr1 experiment blueprint | collaborator provides GPR25 expression/protein or ligand data |
| KIF21B | ligandable motor-domain context may obscure the wrong-direction risk of inhibition/degradation | high | KIF21B restoration modality spec, structure-aware no-go table | perturbation or modality proposal targets inhibition, degradation, knockdown, ASO, or siRNA |
| PTGER4 | known druggability and external disease relevance may be used to bypass the MS-specific mixed-signal blocker | high | PTGER4 signal-specific reopen spec | signal-specific MS fine-mapping/QTL package arrives |
| ZMIZ1 | opposite-direction cross-disease biology may be misread as a therapeutic transfer opportunity | medium | ZMIZ1 restored-OpenGWAS handoff | MS-specific direction or perturbation evidence arrives |
| Postpartum APC-arm imbalance | cross-disease pregnancy trajectories may be over-read as MS relapse-window evidence | medium | V44 postpartum preregistration and V52 data request | postpartum MS relapse-timing immune package arrives |
| T/B compartment remodeling state | compartment signal may be cell composition rather than within-cell remodeling | medium | V44 secondary harness and acceptance criteria | compatible single-cell or sorted-cell package arrives |
| EBV/IFN APC imprint | broad external EBV/IFN biology may be mistaken for MS-specific grounded support | medium | V35/V36 downgrade and V52 contradiction surveillance | EBV-stratified APC/B-cell MS dataset becomes available |
| Complement/lipid progressive axis | progressive-MS relevance may be inferred without lesion-stage direction and perturbation | medium | V35 downgrade and route matrix | chronic-active lesion data with lipid/APC readouts arrives |
| NAMPT/eNAMPT | metabolic/inflammatory marker behavior may be promoted as a target despite confounding | medium | V32 confounder audit and V39 exclusion map | causal perturbation evidence is proposed |
| Closed coloc-screen leads | prior single-locus interest may be resurrected without frozen criteria | medium | V52 reopen checklist and restored-OpenGWAS bounded manifest | new coloc or QTL evidence is proposed |

## Cross-Cutting Risks

| risk | why it matters | mitigation |
|---|---|---|
| Discovery creep | V41 closed broad public-data discovery; using renewed OpenGWAS for open-ended search would break the boundary | Restored OpenGWAS bounded rerun manifest and renewal watch |
| External-context inflation | literature or database agreement may be treated as validation | V47/V48 provenance segregation and V52 convergence/contradiction wording |
| Structure inflation | AlphaFold DB context may be treated as target evidence | Structural evidence-boundary QA and structure-aware no-go table |
| Validation overfitting | tuning timepoints, thresholds, labels, or features on Gafson/Karolinska would invalidate the test | V42 preregistration and command manifest |
| Underpowered kill | a small inconclusive cohort may be incorrectly treated as killing the monitoring route | V43 power map and V42 interpretation grid |
| Package ambiguity | incoming data may be partial but interpreted as complete | Target package acceptance criteria and medical-team request packet |

## Operational Watch List

| watch item | current state | action |
|---|---|---|
| OpenGWAS token | verified active on 2026-07-10; expires 2026-07-24 08:00 UTC | renew before expiry or route around genetics-dependent polish |
| Push hygiene | `origin/main` push functioning after V49 rewrite | continue size/tmp guard before every push |
| Structural records | three AlphaFold DB records are segregated and gate-passing | do not move structure context into grounded findings |
| Validation harness | frozen and synthetic-verified in V42/V44 | run only when a quarantined, eligible package arrives |

## Decision Rule

If a risk materializes, the default action is not to reinterpret the result in
the favorable direction. The default action is to classify the package or claim
at the lower defensible level, queue the exact missing evidence, and leave the
V52 therapeutic verdict unchanged until that evidence is produced.

## Source Artifacts

- `docs/reports/THERAPEUTIC_PATH_V52.md`
- `docs/reports/THERAPEUTIC_TARGET_EVIDENCE_MATRIX_V52.tsv`
- `docs/reports/THERAPEUTIC_REOPEN_CHECKLIST_V52.tsv`
- `docs/reports/THERAPEUTIC_CLAIM_HIERARCHY_V52.md`
- `docs/reports/STRUCTURAL_EVIDENCE_BOUNDARY_QA_V52.md`
- `docs/validation/MONITORING_CLINICAL_UTILITY_BOUNDARY_CHECKLIST_V52.md`
- `docs/validation/PROSPECTIVE_MONITORING_UTILITY_STUDY_SKETCH_V52.md`
- `docs/workups/genetics/STRUCTURE_AWARE_NO_GO_TABLE_V52.md`
- `docs/workups/genetics/RESTORED_OPENGWAS_BOUNDED_RERUN_MANIFEST_V52.md`
