# Therapeutic Claim Hierarchy V52

Date: 2026-07-10

Status: synthesis hierarchy. This document adds no evidence, changes no verdict,
and does not reopen discovery. It states what level of claim each V52
therapeutic-path item is allowed to carry.

## Purpose

The V52 artifacts are now broad enough that claim boundaries matter. This
hierarchy prevents context or future asks from being read as findings.

## Claim Levels

| level | claim class | allowed wording | examples | not allowed |
|---:|---|---|---|---|
| 0 | locked / immutable rules | "frozen rule"; "pre-registered plan"; "must run mechanically" | V22 locked scalar; V42 preregistration; V42 interpretation grid | changing thresholds, signs, endpoints, modules, or timepoints after data receipt |
| 1 | grounded project findings | "supported"; "negative-established"; "closed under current standards" | V22/V28/V32 monitoring evidence; V19 chr1 hard-target verdict; PTGER4 closure; ZMIZ1 decoupling | treating a finding as externally clinically validated without the missing cohort |
| 2 | provisional validation lead | "primary validation lead"; "validation-ready"; "externally gated" | bounded APC/HLA-II monitoring scalar | "validated biomarker"; "clinical rule"; "treatment-switching threshold" |
| 3 | mechanistic context | "context"; "architecture"; "transfer boundary"; "assay-design guide" | coupled APC/HLA/IFN/MIF-CD74 axis; immune-tone context | target nomination or successor rule without validation |
| 4 | target-development handoff | "controlled-data handoff"; "conditional candidate"; "not target-ready" | chr1 KIF21B/GPR25; GPR25; KIF21B | intervention-grade target, wet-lab target program, or target rescue |
| 5 | structure context | "feasibility context"; "confidence-qualified"; "does not resolve causality or direction" | GPR25, KIF21B, PTGER4 AlphaFold DB context | disease evidence, experimental structure truth, target validation |
| 6 | future data ask | "needed to test"; "would reopen if"; "package requirement" | Gafson/Karolinska package; chr1 genotype-linked data; postpartum MS relapse-window data | implied evidence before the data arrive |
| 7 | model or external context | "context"; "corroboration"; "tension flag" | external convergence records; Claude/Gemini/RPT suggestions | project evidence without grounding |

## V52 Item Placement

| item | highest allowed claim level | allowed practical conclusion |
|---|---:|---|
| V22 bounded APC/HLA-II scalar | 2 | primary validation-ready monitoring lead |
| V42/V44 validation harness | 0 | mechanical run plan for external cohort |
| V32 confounder audit | 1 | signal is immune-tone bounded, not steroid/simple-composition artifact in held cohorts |
| V26/V41 APC architecture | 3 | mechanism and transfer-boundary context |
| chr1 KIF21B/GPR25 locus | 4 | closest target-development handoff, not target |
| GPR25 | 4 | conditional receptor candidate, closed for target promotion |
| KIF21B | 4 | serious conditional restoration candidate, closed for target promotion |
| PTGER4 | 1 | closed naive transfer target |
| ZMIZ1 | 1 | transfer-validity warning, not target |
| Postpartum HLA-II/CD64 | 6 | future data-gated biology lead |
| T/B compartment state | 6 | preregistered secondary validation route |
| AlphaFold DB records | 5 | feasibility context only |
| Restored OpenGWAS token | operational | enables bounded reruns; no discovery reopening |

## Claim Escalation Rules

| escalation | required evidence |
|---|---|
| Monitoring lead -> externally supported monitoring readout | Frozen V42/V44 pass in a complete external cohort, interpreted through V52 decision tree |
| Monitoring readout -> clinical utility | Independent replication plus prospective evidence that acting on the readout improves decisions or outcomes |
| chr1 handoff -> dedicated target workup | causal gene, cell state, protective direction, direction-matched perturbation, and feasible modality |
| GPR25 -> target workup | protective haplotype raises/restores GPR25 in a relevant cell state and agonism/restoration is protective |
| KIF21B -> target workup | protective direction is higher/restored KIF21B function and restoration/up-function perturbation is protective |
| PTGER4 -> reopened | signal-specific MS-protective direction and safe EP4 modulation route |
| ZMIZ1 -> reopened | MS-specific protective modulation direction plus perturbation and modality |

## What V52 Can Say

V52 can say:

1. the strongest near-term impact route is monitoring / stratification
   validation;
2. no intervention-grade target is currently supported;
3. chr1 is the closest controlled-data target-development handoff;
4. structure sharpens feasibility context but does not rescue targets;
5. restored OpenGWAS permits bounded reruns, not new discovery;
6. the medical team should prioritize complete paired response-validation data
   and, separately, genotype-linked chr1 cell-state data if target work remains
   a priority.

## What V52 Cannot Say

V52 cannot say:

1. the scalar is clinically validated;
2. Gafson/Karolinska will pass;
3. a single small cohort will settle the rule if underpowered;
4. GPR25, KIF21B, PTGER4, or ZMIZ1 is an MS therapeutic target;
5. AlphaFold DB context is disease evidence;
6. external context validates the locked scalar;
7. renewed OpenGWAS access reopens discovery.

## Source Artifacts

- `docs/reports/FINDINGS_REPORT_V37.md`
- `docs/reports/THERAPEUTIC_PATH_V52.md`
- `docs/reports/THERAPEUTIC_TARGET_EVIDENCE_MATRIX_V52.tsv`
- `docs/reports/THERAPEUTIC_REOPEN_CHECKLIST_V52.tsv`
- `docs/reports/STRUCTURAL_EVIDENCE_BOUNDARY_QA_V52.md`
- `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md`
- `docs/workups/genetics/CHR1_DIRECTION_MATCHED_EXPERIMENT_BLUEPRINT_V52.md`
