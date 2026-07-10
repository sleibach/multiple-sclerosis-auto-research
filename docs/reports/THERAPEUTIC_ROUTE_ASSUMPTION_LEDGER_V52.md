# Therapeutic Route Assumption Ledger V52

Date: 2026-07-10

Status: assumption ledger. This document adds no evidence, changes no verdict,
and does not reopen discovery. It makes explicit the assumptions behind the V52
therapeutic-path synthesis so future data can test them cleanly.

## Purpose

The V52 conclusion is deliberately conservative: monitoring / stratification is
the most defensible near-term impact route, while direct target work remains
data-gated. This ledger states the assumptions under that conclusion, how well
each is currently supported, and what would falsify or revise it.

## Core Assumptions

| assumption | current support | confidence | would revise or falsify | controlling artifact |
|---|---|---|---|---|
| The bounded APC/HLA-II scalar is the only near-term clinically actionable route | V22/V28/V32 robustness and confounder audit; V41 discovery exhaustion | medium | external frozen validation fails cleanly in an adequately powered cohort | V42 preregistration; V52 decision tree |
| The scalar is a monitoring / stratification readout, not a direct treatment mechanism | V32 immune-tone-bounded interpretation; no intervention point identified | high | prospective action evidence showing score-guided decisions improve outcomes | prospective utility sketch |
| More complex APC-axis features should not replace the locked scalar for validation | V27/V28 found no fair improvement over the scalar | high | pre-registered external validation of a successor rule, not fit on Gafson/Karolinska | claim hierarchy; command manifest |
| Broad public-data discovery should stay closed | V41 joint inference produced no unexpected held-out-validated signal and bounded remaining success probability | high | a new independent dataset or a pre-specified bounded re-analysis target | restored OpenGWAS bounded manifest |
| chr1 is real biology but not target-ready | V17/V19 locus support plus unresolved causal gene and direction/modality blockers | high | genotype-linked immune/CSF package resolves gene, cell state, direction, perturbation, and modality | chr1 data spec and experiment blueprint |
| GPR25 tractability does not overcome causal/cell-state/direction gaps | AlphaFold DB and GPCR context are compatible with tractability, but immune-QTL/scRNA support is weak | high | protective haplotype raises/restores GPR25 in relevant cells and agonism/restoration is protective | GPR25 modality spec |
| KIF21B structural interpretability does not solve wrong-direction modality risk | KIF21B QTD000021 direction suggests risk alleles lower expression; common modalities lower function | high | protective direction is lower KIF21B, or a restoration/up-function modality proves protective | KIF21B restoration spec |
| PTGER4 remains closed despite receptor tractability | V37/V52 closure is signal/direction-conflict driven, not structure driven | high | signal-specific MS-protective direction and safe EP4 modality | PTGER4 reopen spec |
| ZMIZ1 should be treated as transfer-warning biology, not a target | opposite-direction MS/Crohn result and no MS-specific modality | high | MS-specific genotype-linked direction plus perturbation and feasible modality | ZMIZ1 handoff |
| External context can corroborate or flag tension but cannot validate the grounded findings | V47-V49 provenance segregation; V52 convergence/contradiction review | high | later external claim is grounded by project rerun on reachable data | provenance gate and convergence file |
| AlphaFold DB outputs inform tractability but cannot rescue a target verdict | V51/V52 structural segregation and V52 no-go table | high | experimental structural plus functional evidence arrives, and direction-matched biology also holds | structural boundary QA |

## Practical Assumptions For Incoming Data

| assumption | operational consequence | failure mode |
|---|---|---|
| A complete monitoring package can be scored mechanically | run V42/V44 command manifest without tuning | missing pairing, labels, module genes, or batch/QC metadata makes package unscoreable |
| A small external cohort may be informative but not decisive | report effect size and CI even when inconclusive | treating an underpowered directional estimate as pass or kill |
| Batch or immune-tone-bounded results are still useful but narrower | classify as bounded monitoring support, not clean validation | calling bounded result a pure APC/HLA-II-specific marker |
| chr1 target data and monitoring validation are separate asks | do not substitute target-development data for scalar validation | target package is used to claim clinical monitoring validation |
| Perturbation without genotype-linked direction is non-counting for chr1 reopening | classify as context only | tool perturbation is used to rescue a favorite gene |

## Assumptions Worth Testing First

| priority | assumption to test | needed data | why it matters |
|---:|---|---|---|
| 1 | the monitoring scalar externally validates as a bounded pharmacodynamic readout | paired PBMC/NEDA Gafson/Karolinska-style package | determines whether near-term clinical impact exists |
| 2 | chr1 protective haplotype maps to one causal gene and direction in relevant cells | genotype-linked immune/CSF molecular package | only plausible bridge from genetics to target workup |
| 3 | KIF21B or GPR25 has a direction-matched perturbation phenotype | perturbation after causal-gene/direction resolution | separates biology from therapeutic tractability |
| 4 | postpartum APC-arm imbalance is MS relapse-window specific | postpartum MS relapse-timing immune data | tests a clinically anchored biology lead |
| 5 | T/B compartment state survives composition controls externally | compatible compartment-resolved dataset | tests a secondary monitoring route |

## Decision Rule

If future data contradict an assumption, update the route status at the lowest
level supported by the new evidence. Do not reinterpret the new result to
protect the V52 conclusion, and do not promote a route unless the route-specific
reopen or validation criteria are met.

## Source Artifacts

- `docs/reports/THERAPEUTIC_PATH_V52.md`
- `docs/reports/THERAPEUTIC_CLAIM_HIERARCHY_V52.md`
- `docs/reports/THERAPEUTIC_ROUTE_RISK_REGISTER_V52.md`
- `docs/reports/THERAPEUTIC_REOPEN_CHECKLIST_V52.tsv`
- `docs/reports/STRUCTURAL_EVIDENCE_BOUNDARY_QA_V52.md`
- `docs/validation/PROSPECTIVE_MONITORING_UTILITY_STUDY_SKETCH_V52.md`
- `docs/workups/genetics/CHR1_DIRECTION_MATCHED_EXPERIMENT_BLUEPRINT_V52.md`
- `docs/workups/genetics/RESTORED_OPENGWAS_BOUNDED_RERUN_MANIFEST_V52.md`
