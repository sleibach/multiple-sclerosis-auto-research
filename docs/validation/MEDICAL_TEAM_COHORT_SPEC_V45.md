# V45 Medical-Team Cohort Specification

## Purpose

Define the cohort the medical team should seek to make validation conclusive,
rather than merely adding another underpowered estimate. This specification is
derived from the V42 frozen plan, V43 power/robustness simulations, V44 batch
hardening and cohort scout, and V45 pathology stress tests.

Synthetic results cited here characterize method behavior only. They are not
biological evidence about MS.

## Direct Answer

The project should not rely on a single small Gafson-sized cohort to settle the
APC/HLA-II monitoring rule.

Minimum decision-grade target for the primary V22/V42 DMF/NEDA-style validation:

- at least `30` responders and `30` nonresponders if the true effect is large
  (`~1.0` synthetic effect size), labels are clean, and technical confounding is
  low;
- preferably `60-80` responders and `60-80` nonresponders if the true effect is
  moderate, labels are noisy, immune-tone confounding is present, or batch is
  imperfect;
- any cohort with `10-15` per group should be treated as effect-size/CI
  information, not as a decisive pass/fail unless the effect is large and the
  diagnostics are clean.

V43 found:

- Gafson-small cells (`10-15` per group) mean conclusive rate: `0.578`;
- effect size `1.00`, no label noise, no confounder reached 80% pass probability
  at `30` per group;
- effect size `0.75` with 10% label noise and immune-tone structure did not
  reach 80% pass probability up to `80` per group.

## Primary Validation Cohort: Required Fields

### Subjects And Timing

Required:

- MS subjects starting the therapy of interest, preferably dimethyl fumarate for
  direct Gafson/V22 continuity.
- Paired baseline and early on-treatment blood transcriptomics.
- Baseline sample before treatment or before biologically meaningful exposure.
- Early on-treatment sample ideally `4-8` weeks, acceptable `1-12` weeks only if
  exact days since treatment are recorded.
- Long-term clinical outcome window, ideally `12-15` months for NEDA-4 or a
  directly comparable event-free status.

Strongly preferred:

- a later transcriptomic timepoint for context, but it is not required for the
  primary locked early-change feature.

### Outcome Labels

Required:

- binary NEDA-4 or equivalent responder/nonresponder label;
- per-subject component labels: relapse, MRI activity, disability progression,
  brain-volume loss if NEDA-4 is used;
- date/window of outcome assessment;
- censoring/dropout flag;
- reason for missing or indeterminate outcome.

Label noise is a major power killer. If the outcome cannot be mapped
subject-by-subject to transcriptomic samples, the cohort is not validation-ready.

### Expression Data

Required:

- gene-by-sample expression matrix or raw counts plus a reproducible processing
  path;
- sample-to-subject map;
- sample-to-timepoint map;
- gene identifiers with mapping sufficient for the V22 frozen modules;
- normalization status clearly stated.

Required module coverage:

- V22 IFN/APC: `STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`, `CD74`, `HLA-DRA`;
- V22 HLA-II: `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `HLA-DQA1`,
  `HLA-DQB1`;
- receptor comparator: `CD74`, `CD44`, `CXCR4`;
- V32 confounder panels and V44 batch diagnostics where possible.

If module coverage falls near the threshold, the result should be treated as
mechanically fragile even if the raw score looks strong.

### Mandatory Clinical / Technical Metadata

Technical metadata required for a clean validation:

- batch / processing batch / sequencing batch;
- lane, flowcell, run, capture/library batch where applicable;
- collection date and processing date;
- RIN/RQN or equivalent RNA quality;
- sequencing depth / percent mapped or equivalent array QC;
- site if multi-center;
- sample storage/freeze-thaw if available.

Clinical confounder metadata required:

- steroid exposure, dose, date, and indication;
- relapse or infection near blood draw;
- prior DMT, washout, and concomitant medications;
- lymphocyte count and major immune-cell counts/fractions if available;
- age, sex, disease subtype, disease duration, baseline EDSS.

V44/V45 show why this is non-negotiable:

- primary V22 synthetic-null pass under severe response-correlated batch reached
  `0.40` in V43 and `0.8625` in a V45 multi-confounder stress scenario;
- the V44/V45 guards reduced clean synthetic-null passes to `0.00-0.0125`, but
  a raw positive with a batch flag becomes technically non-specific, not a clean
  validation.

## Data-Quality Conditions For Interpretability

A primary V22/V42 validation can be interpreted as clean only if:

1. both response groups have usable paired baseline/early samples;
2. response labels are sample-mapped and not post-hoc redefined;
3. module genes pass the frozen coverage thresholds;
4. batch metadata are supplied and do not strongly track response;
5. steroid exposure and immune-tone/confounder panels are scoreable;
6. no large outlier or normalization pathology is detected;
7. receptor-only score does not outperform the locked V22 score by `>=0.10` AUC.

If these conditions fail, the cohort can still inform effect size and future
power, but it should not be used to declare clean validation.

## Recommended Acquisition Priority

### Tier 1: Gafson DMF / NEDA-4

Use the existing request package, but set expectations correctly:

- best near-ideal biological fit;
- likely small, so it may be inconclusive;
- must include processed expression, raw counts if possible, sample-subject
  mapping, NEDA-4 labels, and complete technical covariates.

### Tier 2: Karolinska DMF ROS Cohort

Parallel request, not after Gafson:

- public omics exist;
- response labels and expression sample mapping are the blocker;
- useful as secondary MS DMF replication/stress test if labels are obtained.

### Tier 3: New Prospective / Collaborator Cohort

If the medical team can shape collection, the preferred design is:

- at least `60` responders and `60` nonresponders, with `80+80` preferred if the
  expected effect is moderate or labels are noisy;
- baseline plus `4-8` week on-treatment PBMC or whole-blood RNA-seq;
- NEDA-4 or relapse/MRI/disability composite at `12-15` months;
- batch-balanced processing blinded to future response status;
- steroid exposure and cell counts captured prospectively.

## Secondary Live Leads: Cohort Requirements

### Postpartum HLA-II/CD64 APC Arm

Required:

- MS pregnancy/postpartum cohort;
- late-pregnancy and early postpartum (`4-8` week) paired samples;
- relapse status through 3 months postpartum;
- HLA-II and CD64/FCGR1 feature coverage;
- steroid exposure, DMT restart, infection, lactation, and batch metadata.

V45 pathology stress test:

- synthetic-null raw postpartum pass under severe response-correlated batch:
  `0.7667`;
- guarded clean pass max: `0.0222`;
- severe module-coverage loss makes planted signals unscoreable.

### T/B Compartment Monitoring

Required:

- treatment-response cohort with baseline plus early on-treatment samples;
- response/NEDA/remission labels;
- B/plasma-like and T-like compartment expression or validated deconvolution;
- compartment fractions/counts and batch/QC metadata.

V45 pathology stress test:

- synthetic-null raw and composition-adjusted T/B pass under severe
  response-correlated batch: `0.3333`;
- guarded clean pass max: `0.0111`;
- pure composition artifacts were controlled by residualization, but batch
  required a separate guard.

## Exact Data Package Checklist

For every requested cohort, ask for:

1. expression matrix, raw counts preferred plus processed normalized values if
   available;
2. sample metadata table with sample ID, subject ID, timepoint, exact days since
   treatment or delivery, and assay batch fields;
3. clinical outcome table with subject ID, binary response/NEDA/relapse outcome,
   component outcomes, assessment dates, and missingness reasons;
4. clinical covariate table with steroid exposure, relapse/infection timing,
   prior/concomitant DMTs, EDSS, disease subtype, age, sex, and site;
5. technical QC table with batch, sequencing/array run, lane/flowcell if
   relevant, RIN/RQN, sequencing depth, mapping metrics, and processing dates;
6. data dictionary defining all labels and codes;
7. permission to publish aggregate validation metrics and non-identifying
   derived module scores.

## Interpretation Before Data Arrive

Pre-commit these expectations:

- A small clean positive is encouraging but likely provisional.
- A small negative is not a kill unless the cohort is adequately powered and
  technically clean.
- A raw positive with response-correlated batch is non-specific.
- A technically clean adequate-power failure demotes the lead.
- An underpowered or noisy cohort is still useful if it tightens the effect-size
  CI for the next cohort.

## Bottom Line

The next best data acquisition is not merely "get Gafson." It is:

1. get Gafson because it is the best biological fit;
2. pursue Karolinska labels in parallel because Gafson may be inconclusive;
3. if a prospective or collaborator cohort can be shaped, target at least
   `60+60`, preferably `80+80`, with exact early timepoints, clean NEDA-style
   labels, and response-balanced technical processing.

