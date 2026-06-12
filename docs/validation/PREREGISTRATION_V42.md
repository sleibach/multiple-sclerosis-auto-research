# PREREGISTRATION V42: Gafson DMF PBMC RNA-seq NEDA-4 Validation

Status: **pre-registered while blind to the Gafson validation data**
Date: 2026-06-10
Primary locked rule: `docs/locked_rules/LOCKED_RULE_V22.md`
Purpose: mechanical validation of the immutable V22 early-treatment monitoring
rule in the Gafson et al. 2018 dimethyl fumarate PBMC RNA-seq cohort with
subject-level NEDA-4 labels.

This document freezes the Gafson validation plan before the data are available
to the project. It does not edit or reinterpret the V22 locked rule. It fixes
the data-ingestion, missingness, confounder, success/failure, and
multiple-testing decisions around that rule so the eventual analysis is a
mechanical execution rather than a post-hoc analysis.

## Blindness And Quarantine

No Gafson/DMF/NEDA-4 expression or sample-level outcome data were read while
writing this plan. If such data are already on disk in a future session, they
must be recorded and quarantined before running this plan:

1. Record path, file sizes, and checksums.
2. Confirm the files were not opened during rule construction.
3. Run only the frozen harness described here.
4. Do not alter module genes, timepoint rules, therapy-class assignment,
   endpoint mapping, thresholds, covariate sets, or interpretation after
   inspecting the data.

## Operational Expiry Flag

OpenGWAS access is not expected to be required for this validation run, but the
project token expires on `2026-06-19 12:28 UTC`. If any validation-adjacent
OpenGWAS-dependent check is run after that timestamp, the token must be renewed
first. A failed or expired token must be reported as an auth blocker, not as a
biological null.

## Target Cohort

The primary target is the Gafson et al. 2018 dimethyl fumarate MS PBMC
transcriptomic cohort with paired baseline and early on-treatment RNA-seq plus
sample-level NEDA-4 outcome labels.

The cohort is assigned in advance to V22 **Class C - MS non-IFN DMT / broad
immune rebalancing**. This assignment is fixed and cannot be changed after
seeing expression or outcome results.

## Required Input Package

The validation input package must contain these files or equivalent fields:

| Component | Required fields | Primary use |
|---|---|---|
| Expression matrix | sample identifiers; gene, transcript, probe, or feature identifiers; expression values | compute frozen modules |
| Sample metadata | sample identifier, subject identifier, timepoint, baseline/treated label or treatment-relative time, treatment name, collection date or relative day/week where available | pair baseline and early treatment samples |
| Outcome metadata | subject identifier, NEDA-4 binary label, outcome assessment window, source definition of NEDA-4 | define responder/nonresponder labels |
| Feature annotation | gene symbols or Ensembl/probe/transcript to gene mapping where expression rows are not already official symbols | platform mapping |
| QC and batch metadata | batch, lane, capture/processing date, RIN, sequencing depth, percent mapped, cell counts, medication/steroid metadata where available | pre-specified audit only |

If raw counts and normalized expression are both provided, raw counts are used
for the primary expression preprocessing. If only normalized expression is
provided, it is accepted only if it is documented as log-like or otherwise
appropriate for across-sample z-scoring; this choice is made from file
metadata, not from rule performance.

## Subject And Sample Eligibility

Primary validation includes a subject only if all conditions are met:

1. Human MS subject treated with dimethyl fumarate.
2. One pre-treatment baseline PBMC RNA-seq sample is available.
3. At least one eligible early on-treatment PBMC RNA-seq sample is available.
4. Subject-level NEDA-4 outcome label is available and mappable to binary
   responder/nonresponder.
5. Baseline and selected early sample both pass the dataset-supplied QC flags,
   if such flags are provided.
6. IFN/APC and HLA-II frozen modules are scoreable under V22 coverage rules.

Subjects lacking a baseline, lacking an eligible early timepoint, lacking a
primary NEDA-4 label, or failing expression QC are excluded from the primary
metric and listed in the attrition table with the reason. Exclusion never uses
the V22 score or outcome direction.

## Early Timepoint Selection

The selected on-treatment sample is fixed by this rule:

1. Eligible treated samples are those collected at least `24 hours` after DMF
   start and no later than `12 weeks`.
2. If multiple eligible treated samples exist, use the earliest by recorded
   treatment-relative time.
3. If relative time is missing but visit labels are available, map labels in
   this order where unambiguous: Week 1, Week 2, Week 4, Week 6, Week 8,
   Week 12.
4. If multiple samples tie at the same eligible timepoint, choose the
   lexicographically first sample identifier and flag the tie.
5. If the first available treated sample is after the primary outcome
   assessment, the subject is excluded from primary validation and may only be
   listed as out-of-scope context.

This timepoint choice is made before computing any response association.

## Outcome Mapping

Primary outcome is subject-level NEDA-4 status.

| Source value | Primary response label |
|---|---|
| NEDA-4 true, yes, achieved, maintained, event-free | `Responder` |
| NEDA-4 false, no, not achieved, disease activity present | `Non-responder` |

If multiple outcomes are supplied, NEDA-4 is always primary for this cohort.
Relapse-free status, MRI activity, EDSS progression, or discontinuation can be
reported as descriptive secondary endpoints only if already supplied, but they
cannot replace NEDA-4 after seeing results.

If NEDA-4 is absent and only partial components are available, the primary
validation is blocked. A reconstructed endpoint is not allowed unless the
component-combination rule is specified by the source publication before seeing
scores.

## Expression Preprocessing

The preprocessing is frozen as follows:

1. Map features to official gene symbols.
2. Strip Ensembl version suffixes before mapping when Ensembl IDs are present.
3. Collapse multiple features mapping to the same gene by arithmetic mean
   within each sample.
4. For raw counts, compute CPM per sample and transform as `log2(CPM + 1)`.
5. For already normalized log expression, use the supplied values as-is after
   feature-to-gene collapse.
6. No batch correction, outcome-guided filtering, surrogate-variable analysis,
   or sample outlier removal is part of the primary score.
7. Z-score each gene across the eligible paired expression sample universe:
   all baseline and selected early treated samples that pass expression QC and
   sample-pairing criteria, regardless of whether the subject has a usable
   NEDA-4 label. The primary AUC/g calculation then uses only labeled paired
   subjects.
8. Compute each module as the arithmetic mean of available z-scored module
   genes.

The primary module coverage threshold follows V22 exactly: a module is
scoreable only if at least `50%` of frozen genes are present after mapping.
The Gafson primary validation is unscoreable if either IFN/APC or HLA-II fails
coverage. The receptor-only negative control is not required for primary
scoring, but if it fails coverage the specificity control is reported as
unavailable.

## Frozen V22 Modules

The module genes are reproduced here only for traceability. The authoritative
definition remains `docs/locked_rules/LOCKED_RULE_V22.md`.

| Module | Genes |
|---|---|
| IFN/APC | `STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`, `CD74`, `HLA-DRA` |
| HLA-II | `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `HLA-DQA1`, `HLA-DQB1` |
| Receptor-only negative control | `CD74`, `CD44`, `CXCR4` |

For each subject:

`delta_module = early_on_treatment_module_score - baseline_module_score`

For Gafson DMF Class C:

`v22_locked_signed_score = delta_HLAII - delta_IFN_APC`

Responders are predicted to have higher `v22_locked_signed_score` than
nonresponders.

The receptor-only negative-control score is:

`delta_RECEPTOR = early_on_treatment_RECEPTOR - baseline_RECEPTOR`

If receptor-only AUC exceeds V22 locked-score AUC by at least `0.10`, a raw
Gafson pass is downgraded to a non-specific pass for interpretation.

## Primary Metrics

Primary validation metrics:

1. ROC AUC of `v22_locked_signed_score` for `Responder` versus
   `Non-responder`.
2. Signed Hedges g, responder minus nonresponder.
3. Bootstrap 95% CI for AUC using `2000` resamples and seed `20260606`.
4. Exact label-permutation p value for AUC when computationally feasible; else
   `10000` permutations with seed `20260606`.

Responder-higher orientation is fixed. The score is not sign-flipped if AUC is
below `0.50`.

## Pass, Fail, Inconclusive, And Kill Criteria

For `n >= 30` labeled paired subjects total, Gafson is a clean cohort-level
pass only if all are true:

1. AUC `>= 0.70`.
2. Signed Hedges g `>= 0.50`.
3. Lower bootstrap 95% CI for AUC `> 0.55`.
4. Direction is responder-higher as locked.
5. Receptor-only control does not outperform by AUC `>= 0.10`, if scoreable.

For `n < 30`, Gafson can be a small-n directional pass only if AUC `>= 0.70`,
signed Hedges g `>= 0.50`, and direction is locked. If either response group
has fewer than `15` labeled subjects, the result remains provisional even when
the small-n pass criteria are met.

Gafson is a clear fail if:

1. It has at least `30` labeled paired subjects total, both response groups have
   at least `10` subjects, and AUC `< 0.60` or signed Hedges g `< 0.20`; or
2. The locked score points opposite to prediction with AUC `< 0.45`; or
3. Receptor-only outperforms the locked score by AUC `>= 0.10` and the locked
   score does not meet the pass threshold.

Gafson is inconclusive if sample size, coverage, outcome labels, or CI width
prevent a clean pass or fail. Inconclusive results still report the observed
effect size and CI for future power planning.

This single cohort cannot alone create a V22 breakthrough, because V22 requires
multiple independent held-out cohorts. It can, however, materially strengthen,
weaken, or bound the DMF/MS Class C branch. It also cannot alone trigger the
full V22 kill unless combined with the existing failed MS DMT cohorts under the
locked V22 kill language.

## Frozen Confounder Panels

The V32 confounder audit panels are frozen for Gafson. A panel is scoreable if
at least `40%` of panel genes are present, matching V32 implementation.

| Panel | Genes |
|---|---|
| Glycolysis | `HK1`, `HK2`, `GPI`, `PFKP`, `PFKM`, `ALDOA`, `GAPDH`, `PGK1`, `PGAM1`, `ENO1`, `PKM`, `LDHA`, `SLC2A1`, `PFKFB3` |
| OXPHOS | `NDUFA1`, `NDUFA2`, `NDUFA9`, `NDUFB8`, `SDHA`, `SDHB`, `UQCRC1`, `UQCRC2`, `COX4I1`, `COX5A`, `ATP5F1A`, `ATP5F1B`, `ATP5MC1` |
| HIF/NAMPT immunometabolism | `NAMPT`, `HIF1A`, `SLC2A1`, `LDHA`, `PFKFB3`, `ENO1`, `HK2`, `VEGFA`, `BNIP3`, `NDRG1` |
| Glucocorticoid response | `FKBP5`, `TSC22D3`, `DUSP1`, `KLF9`, `ZBTB16`, `PER1`, `SGK1`, `NFKBIA`, `GILZ`, `SOCS1` |
| General inflammatory tone | `IL1B`, `TNF`, `IL6`, `CXCL8`, `CCL2`, `NFKB1`, `NFKBIA`, `PTGS2`, `ICAM1`, `JUN`, `FOS` |
| IFN-suppression / inverse ISG | `ISG15`, `IFI6`, `IFI44L`, `MX1`, `OAS1`, `OAS2`, `IFIT1`, `IFIT3`, `RSAD2`, `CXCL10` |
| STAT1 axis | `STAT1`, `IRF1`, `GBP1`, `GBP2`, `CXCL10`, `IDO1`, `TAP1`, `PSMB9`, `WARS1` |
| Proliferation | `MKI67`, `TOP2A`, `PCNA`, `MCM2`, `MCM5`, `TYMS`, `UBE2C`, `BIRC5`, `CDK1`, `CCNB1` |
| Monocyte/myeloid composition | `LYZ`, `LST1`, `S100A8`, `S100A9`, `FCGR3A`, `MS4A7`, `CD14`, `CTSS`, `CST3` |
| T-cell composition | `CD3D`, `CD3E`, `TRAC`, `CD4`, `CD8A`, `IL7R`, `CCR7`, `NKG7` |
| B-cell composition | `MS4A1`, `CD79A`, `CD79B`, `CD74`, `BANK1`, `CD19` |

For every scoreable panel, compute both baseline level and early delta using
the same z-scored expression matrix as the primary V22 modules.

The baseline APC/HLA-II level covariate is:

`baseline_apc_hla_level = baseline_HLAII - baseline_IFN_APC`

## Confounder Adjustment Plan

The primary unadjusted V22 result is always reported first and remains the
formal validation result. Confounder adjustment is an interpretation audit; it
cannot convert a failed primary result into a pass.

## V44 Additive Batch-Diagnostic Guard

This section was added blind to Gafson data on 2026-06-12 after the V43
synthetic robustness audit showed response-correlated batch effects can create
false-positive primary passes. It is an additive technical diagnostic only. It
does not change the V22 locked score, score orientation, primary thresholds,
timepoint selection, endpoint, or pass/fail criteria.

If any technical metadata are supplied, including `batch`, `lane`, `flowcell`,
`run`, `sequencing_batch`, `processing_batch`, `capture_batch`,
`library_batch`, `collection_date`, `processing_date`, `rin`, `rqn`,
`sequencing_depth`, `percent_mapped`, or `steroid_exposure`, the harness must:

1. carry baseline and treated technical metadata into the paired-subject table;
2. construct baseline, treated, paired-pattern, and changed-status metadata
   diagnostics where both baseline and treated values exist;
3. report each metadata feature's response association, association with the
   locked score, and residualized locked-score AUC where sample size permits;
4. write `batch_diagnostic_metrics.tsv`;
5. set `batch_guard_flag=true` in `validation_summary.json` if any metadata
   feature triggers `BATCH_RISK_FLAG`.

`BATCH_RISK_FLAG` is triggered when any of these pre-specified conditions hold:

- metadata AUC for response is at least `0.60` in either orientation;
- absolute Spearman correlation between metadata coding and locked score is at
  least `0.35`;
- residualizing the locked score against the metadata feature attenuates AUC by
  at least `0.05`.

If a raw Gafson result passes the primary V22 threshold but `batch_guard_flag`
is true, the result is reported as **technically non-specific pending batch
resolution**, not as a clean validation. The primary result remains visible and
unchanged, but interpretation is downgraded under
`docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`. A failed primary result
cannot be rescued by batch adjustment.

For each individual confounder feature:

1. Report confounder AUC for response using its observed orientation.
2. Report Spearman correlation with `v22_locked_signed_score`.
3. Residualize `v22_locked_signed_score` against the confounder.
4. Compute residual-score AUC, Hedges g, bootstrap CI, and permutation p.

For the pre-specified joint confounder families:

| Family | Features |
|---|---|
| Baseline and steroid | `baseline_apc_hla_level`, baseline/delta glucocorticoid response |
| Cell composition | baseline/delta monocyte-myeloid, T-cell, and B-cell composition |
| Metabolic/inflammatory/STAT1 | baseline/delta glycolysis, HIF/NAMPT immunometabolism, general inflammatory tone, STAT1 axis, IFN-suppression/inverse-ISG |

Residualize the locked score against all scoreable features in the family and
report the same residual metrics. If sample size is too small for a stable
multivariable residualization, defined as fewer than `5` labeled subjects per
included covariate after missingness filtering, report the family as
statistically underpowered and run the individual-feature residualizations
only. Do not choose a smaller subset after seeing results.

Where batch or direct steroid-exposure metadata are supplied:

1. Report metadata association with response and locked score.
2. Add batch/steroid metadata as a separate audit covariate if each level has
   at least `3` subjects and both response classes are represented after
   grouping.
3. Do not include metadata covariates in the primary score.

## Adjustment Verdicts

For each adjustment, use these fixed labels:

| Label | Criterion |
|---|---|
| `SURVIVES` | adjusted AUC `>= 0.70` and attenuation from raw AUC `< 0.05` |
| `ATTENUATES` | adjusted AUC `< 0.70` or attenuation `>= 0.05`, but adjusted AUC `>= 0.65` or attenuation `< 0.10` |
| `EXPLAINED_AWAY` | adjusted AUC `< 0.65` and attenuation `>= 0.10` |
| `UNDERPOWERED` | sample size or covariate count violates the fixed stability rule |
| `UNSCOREABLE` | gene coverage or metadata are insufficient |

The V32 prior expectation is that the broad metabolic/inflammatory/STAT1 family
may attenuate the signal. If that happens in Gafson, it is reported as
consistent with the immune-tone-bounded interpretation, not as a post-hoc
rescue.

## Multiple-Comparison Budget

The analysis count is fixed in advance.

| Family | Tests | Correction / interpretation |
|---|---:|---|
| Primary V22 validation | 1 | no multiplicity correction |
| Receptor-only negative control | 1 | specificity downgrade only |
| Individual confounder audits | up to 23 | Benjamini-Hochberg q within audit family; cannot create pass |
| Joint confounder families | 3 | reported separately; cannot create pass |
| V36 secondary audits | up to 7 domains | descriptive, corrected within available secondary family |
| Optional clinical component outcomes | number fixed by supplied NEDA components | descriptive only; cannot replace NEDA-4 |

No additional exploratory feature, cell subset, alternative endpoint,
alternative timepoint, fitted coefficient, or model-derived score is part of
this validation unless a separate locked successor rule exists before data
arrival. None exists at V42.

## V36 Secondary Audits

Run these only where data support them:

1. Timing table for baseline and selected early timepoint.
2. Baseline, treated, and delta IFN/APC and HLA-II reported separately.
3. STAT1-axis and IFN-suppression residualization.
4. Glycolysis and HIF/NAMPT residualization.
5. Compartment readouts if sorted-cell or single-cell data are provided.
6. B/plasma substate composition only if raw single-cell data are provided.
7. Technical QC/batch audit where metadata are provided.

These audits cannot replace the primary V22 locked result.

## Output Artifacts

The future Gafson run writes to `analysis/gafson_validation_v42/` unless a
specific cohort version suffix is required.

Required outputs:

- `input_inventory.tsv`: file names, sizes, checksums, and received fields.
- `sample_attrition.tsv`: every subject and inclusion/exclusion reason.
- `gene_mapping_coverage.tsv`: module and confounder panel coverage.
- `paired_module_deltas.tsv`: one row per primary eligible subject.
- `locked_rule_scores.tsv`: V22 score and receptor control.
- `locked_rule_metrics.tsv`: primary AUC, Hedges g, CI, p value, pass/fail.
- `confounder_scores.tsv`: baseline and delta panel scores.
- `confounder_adjustment_metrics.tsv`: individual adjustment results.
- `joint_confounder_metrics.tsv`: three fixed family adjustments.
- `validation_summary.json`: machine-readable final verdict.
- `VALIDATION_REPORT.md`: human-readable result interpreted under
  `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`.

## Prohibited After Data Arrival

The following are explicitly forbidden after seeing Gafson expression or
outcome data:

- changing any V22 module gene;
- changing DMF therapy class;
- selecting a different early timepoint because performance is better;
- switching from NEDA-4 to another outcome because performance is better;
- adding fitted weights or a learned model;
- flipping the score orientation;
- batch-correcting the primary score based on performance;
- dropping a scoreable subject because it weakens the result;
- promoting an exploratory or confounder-adjusted analysis as the primary
  validation.

## Pre-Registered Conclusion Template

The final report must state, in this order:

1. Whether the data package was eligible and scoreable.
2. Primary raw V22 locked result.
3. Receptor-only specificity control.
4. Confounder-adjusted interpretation.
5. Final classification under the V42 outcome grid.
6. What the result changes, if anything, about the project state.
7. What remains needed for clinical use.

This order is fixed so the primary result is not buried under post-hoc
interpretation.
