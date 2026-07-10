# Medical-Team Therapeutic Data Request V52

Date: 2026-07-10

Status: operational request packet. This document adds no new evidence, does
not change the V22 locked rule, and does not change the V42/V44 validation
pre-registration. It translates the V52 therapeutic-path synthesis into the
minimum data packages needed for action.

## Request Priority

The immediate therapeutic-impact priority is validation of the bounded
APC/HLA-II early treatment-response monitoring signal. The target-development
priority is separate and should not be substituted for validation.

| priority | package | purpose | decision it can support |
|---:|---|---|---|
| 1 | Paired DMF or DMF-like PBMC treatment-response package | Validate or bound the monitoring / stratification signal | Whether the frozen V22 rule is externally useful as an early pharmacodynamic monitor |
| 2 | chr1 genotype-linked immune/CSF molecular package | Resolve KIF21B vs GPR25 causal biology and therapeutic direction | Whether chr1 should move from hard-target handoff to dedicated target workup |
| 3 | Postpartum MS relapse-window immune package | Test the postpartum APC-arm imbalance under its frozen preregistration | Whether the postpartum APC-arm hypothesis is MS-specific and relapse-window linked |
| 4 | T/B compartment monitoring package | Test the secondary compartment-remodeling state | Whether a compartment-resolved monitoring readout replicates |

## Package 1: Treatment-Response Monitoring Validation

Ask for the following files and fields before any analysis:

| component | required fields | why needed |
|---|---|---|
| Expression matrix | sample IDs; feature IDs; expression values; raw counts if available or documented normalized values | score the frozen V22 modules |
| Sample metadata | sample ID; subject ID; baseline/on-treatment status; treatment name; collection day/week; QC flags | pair baseline with the earliest eligible treatment sample |
| Outcome metadata | subject ID; NEDA-4 or pre-specified equivalent response label; outcome window | define responder/nonresponder labels mechanically |
| Feature annotation | gene symbols or Ensembl/probe-to-gene map | verify module coverage |
| Batch/QC metadata | processing batch; lane; date; RIN or equivalent; sequencing depth; percent mapped; cell counts where available | run V44 additive batch guard and trust-envelope checks |
| Clinical confounders | steroid exposure; relapse timing; infection; DMT timing; cell-count metadata where available | interpret V32 immune-tone and confounder panels |

Minimum useful package:

1. One baseline PBMC expression sample per subject.
2. One early on-treatment PBMC expression sample per subject, ideally no later
   than 12 weeks.
3. Subject-level binary response label, preferably NEDA-4.
4. Enough feature coverage to score IFN/APC and HLA-II modules.
5. Batch/QC metadata sufficient to detect response-correlated technical
   structure.

Powered-study target from V43: aim for at least `30` responders and `30`
nonresponders when the true effect is around `1.0` and labels are clean. Smaller
cohorts are still useful for effect-size estimation but may not settle the rule.

## Package 1 Safe Interpretation

| received result | safe interpretation |
|---|---|
| Complete package, clean V42/V44 pass | Supports the scalar as an early pharmacodynamic monitoring readout in that treatment context |
| Raw pass but immune-tone or batch bounded | Supports a bounded monitoring readout only with required confounder and batch reporting |
| Underpowered directional signal | Use effect size and CI for the next powered cohort; do not call it a definitive pass |
| Adequately powered fail | Materially weakens the DMF/MS Class C branch of the monitoring lead |
| Missing labels, missing pairing, or failed module coverage | Unscoreable; not biological evidence for or against the rule |

No post-hoc endpoint substitution, timepoint tuning, feature tuning, or
threshold adjustment is allowed after the package is visible.

## Package 2: chr1 Target-Development Data

This package is for future target workup only. It does not validate the
monitoring scalar.

Required fields:

| component | required fields | why needed |
|---|---|---|
| Genotypes | direct or high-quality imputed dosage for the V17/V19 chr1 credible-set variants, including `rs12132349`, `rs55838263`, `rs7554511`, and the V19 KIF21B exact shared SNPs | resolve protective haplotype direction |
| Subject metadata | MS/control/comparator status; ancestry or genotype PCs; disease activity/stage; treatment and steroid/relapse/infection metadata | avoid LD, ancestry, treatment, and immune-tone artifacts |
| Molecular readout | single-cell RNA, sorted-cell RNA, CITE-seq/protein, or CSF immune molecular data | locate the causal gene and cell state |
| Candidate genes | `GPR25`, `KIF21B`, `C1orf106/INAVA`, and nearby local genes | compare local alternatives rather than testing one favorite |
| Perturbation readout | direction-matched GPR25 or KIF21B perturbation if available | test whether moving the candidate in the protective direction changes phenotype |

Decision gate:

1. One candidate gene must beat local alternatives in an MS-relevant cell state.
2. The genotype-linked direction must match the genetically protective
   direction.
3. RNA and preferably protein must be detectable in the relevant cell state.
4. A plausible direction-matched modality must exist:
   - GPR25: agonism/restoration, not generic antagonism.
   - KIF21B: restoration/up-function or state correction, not generic kinesin
     inhibition/degradation/knockdown.
5. Perturbation must move an MS-relevant readout protectively.

Without all five, chr1 remains a controlled-data handoff, not a target program.

## Package 3: Postpartum APC-Arm Data

Ask for postpartum MS blood or CSF immune profiling with:

- pregnancy, delivery, and postpartum timing;
- relapse timing and relapse-free window;
- DMT stop/restart timing;
- steroid, infection, lactation, and cell-count metadata;
- enough APC/monocyte/HLA-II/CD64 coverage to score the preregistered axis;
- controls or comparator disease samples if available.

Use only the V44 postpartum preregistered harness. Do not construct a new
postpartum rule after seeing the data.

## Package 4: T/B Compartment Monitoring Data

Ask for single-cell or sorted-cell immune data with:

- T-cell and B-cell compartment resolution;
- paired timing or response labels if testing monitoring;
- cell-composition metadata sufficient to separate within-cell remodeling from
  composition shift;
- enough subjects per group for the V44 secondary harness to be informative.

This route is secondary to Package 1 and should not replace the frozen V22
validation.

## One-Sentence Request To Send

Please provide, if available, paired baseline and early on-treatment PBMC
expression with sample-level NEDA-4 or equivalent response labels, full
sample/QC/batch/confounder metadata, and feature annotation; separately, if
target development is a priority, provide genotype-linked immune or CSF
single-cell/protein data around the chr1 KIF21B/GPR25 credible set with ancestry
metadata and any direction-matched perturbation readouts.

## What The Project Will Not Do With The Package

- It will not tune the V22 rule, thresholds, timepoints, or endpoint after data
  receipt.
- It will not treat an unscoreable package as a biological null.
- It will not treat AlphaFold predicted structure as target evidence.
- It will not start target promotion from chr1 without causal-gene,
  cell-state, direction, and modality alignment.
- It will not use a target-development package as a substitute for
  treatment-response validation.

## Source Artifacts

- `docs/reports/THERAPEUTIC_PATH_V52.md`
- `docs/reports/THERAPEUTIC_PATH_SUMMARY_CARD_V52.md`
- `docs/reports/THERAPEUTIC_TARGET_EVIDENCE_MATRIX_V52.tsv`
- `docs/validation/PREREGISTRATION_V42.md`
- `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- `docs/validation/THERAPEUTIC_VALIDATION_HANDOFF_V52.md`
- `docs/validation/POWER_MAP_V43.md`
- `docs/workups/genetics/CHR1_GENOTYPE_LINKED_DATA_SPEC_V52.md`
- `docs/workups/genetics/GPR25_DIRECTION_MATCHED_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/KIF21B_RESTORATION_MODALITY_SPEC_V52.md`
