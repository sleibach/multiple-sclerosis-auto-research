# V50 V22/V32 Contradiction Trigger Packet

Status: synthesis/navigation only. This packet defines what a future external
source must contain before it can be classified as converging with or
contradicting the locked V22 scalar or the V32 confounder-audit verdict. It
adds no external records, no validation result, and no change to any grounded
project artifact.

Primary project sources:

- `docs/locked_rules/LOCKED_RULE_V22.md`
- `docs/validation/PREREGISTRATION_V42.md`
- `docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md`
- `knowledge_external/synthesis/V50_ZERO_CONTRADICTION_SPECIFICITY_AUDIT.md`
- `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V50.md`

## Purpose

V50 found sharper treatment-response and confounder-context sources, but none
directly tested the frozen V22 scalar or V32 adjustment. This packet prevents
future source review from making either error:

- over-classifying broad DMF, APC, steroid, or composition context as
  validation;
- under-classifying a genuine same-definition source as merely context.

## Locked V22 Same-Definition Requirements

A future source can directly converge with or contradict the V22 scalar only if
all required fields below are present or recoverable without post-hoc choices.

| field | required same-definition value |
|---|---|
| Disease / cohort | Human MS treatment-response cohort; for Gafson-style primary route, DMF PBMC with NEDA-4 or author-primary response labels. |
| Samples | Paired baseline and early on-treatment transcriptomic samples by subject. |
| Early timepoint | At least 24 hours and no later than 12 weeks after treatment start; earliest eligible sample used. |
| Expression layer | PBMC/bulk or compartment/pseudobulk data with scoreable V22 genes. |
| Frozen modules | IFN/APC: `STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`, `CD74`, `HLA-DRA`; HLA-II: `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `HLA-DQA1`, `HLA-DQB1`. |
| Coverage | At least 50 percent of each frozen module after feature mapping. |
| Class C score | `delta_HLAII - delta_IFN_APC` for MS non-IFN DMT / broad immune rebalancing. |
| Direction | Responders predicted to have higher signed score than nonresponders. |
| Metrics | AUC and signed effect size, or enough subject-level data to compute them. |
| Negative control | Receptor-only control (`CD74`, `CD44`, `CXCR4`) if scoreable; source should not be treated as a clean pass if receptor-only outperforms by AUC at least 0.10. |
| No tuning | No source-defined feature selection, sign flip, endpoint switch, or threshold tuning after outcome inspection. |

## V22 Relationship Classification

| classification | minimum external-source content | action |
|---|---|---|
| same-definition convergence | Source or rerunnable source data applies the same dynamic V22 structure, responder-higher direction, and comparable response endpoint, and reports AUC/effect consistent with the locked pass criteria or allows computing them. | Record as external convergence only; route to future project grounding if data are available. |
| same-definition contradiction | Source or rerunnable source data applies the same dynamic V22 structure and comparable labels, but reports opposite direction, AUC below fail threshold, receptor-only dominance, or a direct failure under the locked criteria. | Record as contradiction flag; do not change V22 until the project reruns the frozen harness. |
| validation-context only | Source has DMF, PBMC, response labels, immune monitoring, or transcriptomics, but does not apply the frozen V22 modules/delta/direction or lacks enough data to compute them. | Keep as context or data route, not convergence/contradiction. |
| orthogonal marker result | Source studies DMF response but with different markers, pathways, cell types, or response definition. | Keep orthogonal unless it supplies data usable by the frozen harness. |
| insufficient overlap | Source is a drug label, broad mechanism paper, cohort metadata without expression/labels, or literature claim without module-level testability. | Do not classify as convergence or contradiction. |

## V32 Same-Definition Requirements

A future source can directly converge with or contradict the V32 confounder
audit only if it evaluates the locked V22 score alongside the relevant
confounder panels or provides enough subject-level data to do so.

| field | required same-definition value |
|---|---|
| Primary score | Frozen V22 signed score, not a newly selected APC/HLA-II marker. |
| Confounders | At minimum, glucocorticoid/steroid response, cell-composition markers, and broad immune-tone/STAT1/metabolic/inflammatory panels. |
| Adjustment design | Confounder-only and locked-plus-confounder comparisons, partial/residualized association, stratified or cohort-aware evaluation where applicable. |
| Evaluation | Small-n-aware cross-validation/null/permutation or bootstrap intervals sufficient to classify survival, attenuation, or explained-away behavior. |
| Verdict mapping | Same or comparable categories: survives, attenuates, explained away. |
| Data layer | Same subject-level treatment-response setting as the V22 validation route, or a clearly stated compartment where the V22 score is scoreable. |

## V32 Relationship Classification

| classification | minimum external-source content | action |
|---|---|---|
| confounder-audit convergence | Source applies or enables the locked V22 score and shows it survives steroid/glucocorticoid and cell-composition adjustment while broad immune-tone/STAT1/metabolic adjustment attenuates or bounds it. | Record as external convergence only; project artifact remains the evidence until rerun. |
| confounder-audit contradiction | Source applies or enables the locked V22 score and shows the signal is explained away by steroid/glucocorticoid or cell composition, or conversely shows no immune-tone attenuation where comparable data should detect it. | Record as contradiction flag and queue project rerun on the data if available. |
| confounder-class context | Source shows steroids, glucocorticoids, leukocyte composition, or DMF immune-cell shifts can affect MS blood expression, but does not test the locked V22 score. | Use as validation-guard context only. |
| insufficient overlap | Source lacks subject-level paired expression, response labels, confounder panels, or the locked score definition. | Do not classify as convergence or contradiction. |

## Current V50 Source Routing Under This Packet

| source group | current routing | reason |
|---|---|---|
| Gafson 2018 DMF PBMC/NEDA-4 context | validation-context / future data route | Matches validation setting but external record does not independently test frozen V22 modules and threshold. |
| GSE235357 DMF PBMC response context | potentially groundable data route | Needs schema verification and frozen-harness execution before any relationship claim. |
| DMF ROS or high-dimensional immune monitoring studies | orthogonal marker context | Treatment-response relevant, but different readout from locked V22 scalar. |
| Steroid/glucocorticoid transcriptome papers | confounder-class context | Support scoring steroid panels but do not test V22 adjustment. |
| DMF leukocyte/composition papers | confounder-class context | Support composition diagnostics but do not test V22 adjustment. |

## Future Intake Checklist

Before adding a future V22 or V32 convergence/contradiction row, record:

1. Source URL, DOI, accession, or dataset locator.
2. Whether paired baseline and early on-treatment samples exist.
3. Whether response labels exist and map to the frozen endpoint.
4. Whether V22 module genes pass coverage.
5. Whether the source uses or enables the frozen dynamic score.
6. Whether confounder panels can be scored, for V32 claims.
7. Whether the source's reported result is pre-specified or post-hoc.
8. Whether subject-level data are accessible for a project rerun.
9. Relationship class selected from the tables above.
10. Exact reason if the source remains validation-context, orthogonal, or
    insufficient-overlap.

## Decision

Do not classify future treatment-response sources as V22/V32 convergence or
contradiction unless they satisfy the same-definition requirements above. Most
DMF, steroid, APC, and composition papers should remain context unless they
provide the frozen score, comparable labels, and adjustment evidence, or
rerunnable data that the project can process through the pre-registered harness.
