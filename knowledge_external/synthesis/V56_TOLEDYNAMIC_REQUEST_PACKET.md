# V56 ToleDYNAMIC Controlled-Data Request Packet

Status: submission-ready scientific content; sponsor/platform forms, a qualified
principal investigator, institutional approval, and data-use terms are still
required. No participant-level data have been obtained or viewed.

Boundary: `external-verifiable`; `NOT_PROJECT_GROUNDED`. Principal source:
https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf. Parent
trial sources: https://clinicaltrials.gov/study/NCT04411641 and
https://clinicaltrials.gov/study/NCT04458051. Date accessed: 2026-08-05.

## Plain-Language Summary

[`external-verifiable`; `NOT_PROJECT_GROUNDED`; source:
https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf]
HERCULES and PERSEUS tested tolebrutinib in two forms of progressive multiple
sclerosis. Their public protocol describes ToleDYNAMIC, an approximately
80-participant substudy with blood collected before treatment and at months 3
and 12. Planned measurements include detailed immune-cell phenotyping, tests of
monocyte function and metabolism, and RNA sequencing of selected B-cell and
monocyte samples.

The proposed project asks a limited question: did randomized treatment produce
an early, reproducible change in prespecified peripheral immune programs, and
was the same change observed across the two progressive-MS settings? The
analysis will use modules frozen before these data are accessed, correct all
module and functional tests as fixed families, and treat clinical associations
as estimation only. It will not search for a favorable patient subgroup, infer
that a blood change is a CNS mechanism, or make an individual treatment
recommendation.

The substudy's arm composition and assay availability are not public. If both
randomized arms were not sampled under outcome-blind selection, the project
will report paired trajectories descriptively and will make no treatment-effect
or mechanism claim. Controlled data will remain in the approved secure
workspace; only disclosure-approved aggregate results will leave it.

## Scientific Abstract

### Objective

Test whether tolebrutinib produces prespecified month-3 pharmacodynamic changes
in B-cell and CD14-monocyte programs and functional monocyte readouts, and
whether effects observed in nrSPMS HERCULES transport to PPMS PERSEUS.

### Rationale

[`external-verifiable`; `NOT_PROJECT_GROUNDED`; source:
https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf]
ToleDYNAMIC was planned with baseline, month-3, and month-12 sampling; detailed
B/T/monocyte phenotyping; CD14-monocyte functional assays; and RNA sequencing
in selected sorted B-cell and monocyte samples. These intervention-linked
measurements can test peripheral pharmacodynamics directly, provided both
randomized arms and outcome-blind substudy selection are available.

### Prespecified Aims

1. Audit substudy selection, randomized-arm coverage, missingness, and assay
   batch structure without viewing outcome-associated expression or function.
2. In HERCULES, test the randomized month-3 difference in change for nine
   previously frozen transcript modules in B cells and CD14 monocytes as one
   18-slot max-T family.
3. Test a blinded-SAP-mapped family of monocyte functional endpoints and require
   independent transcript and function gates before using the label
   `functionally anchored`.
4. Replicate any HERCULES transcript or functional effect in PERSEUS using the
   original fixed slots and thresholds, without family shrinkage or refitting.
5. Estimate, without promotion thresholds, whether replicated pharmacodynamic
   effects relate to the fixed 24-month EDSS progression endpoint.

### Primary Estimand

Within each parent trial, the primary estimand is the randomized-arm difference
in paired month-3-minus-baseline change. Participant, visit, arm, arm-by-visit,
site, and assay batch are represented as prespecified in the full analysis
plan. Month 12 assesses durability and cannot rescue a month-3 failure.

### Mandatory Design Branch

- **Both randomized arms, outcome-blind selection:** randomized
  treatment-by-time inference is permitted after validity gates.
- **Active arm only, post-unblinding selection, or arm-confounded batch:**
  descriptive paired trajectories only; no treatment or mechanism claim.
- **Aggregate-only data or no parent-trial linkage:** no project grounding;
  report the access limitation and stop.

## Requested Data And Documents

### Design and linkage

- parent trial, pseudonymous participant, randomized arm and strata, site;
- substudy invitation, consent, enrollment, and RNA-subset selection dates and
  reasons, including whether selection preceded unblinding;
- visit, nominal/actual collection time, processing delay, shipment,
  freeze-thaw, plate, batch, operator, assay failure, and missingness reason;
- treatment start, dose/exposure, interruption/discontinuation and reason;
- EDSS, T25FW, 9HPT, relapse, MRI, prior-DMT, baseline gadolinium lesion,
  NfL, CHI3L1, safety, and liver-monitoring linkage where releasable.

### Transcriptomics

- raw integer gene counts for sorted B cells and CD14 monocytes;
- participant/visit/cell-type/sample map and all included/excluded libraries;
- stable gene identifiers and versions, library protocol and strandedness;
- sequencing, alignment, counting, normalization, and QC specifications;
- library size, mapping, duplication, contamination, plate/batch, and failed-QC
  fields;
- FASTQ/BAM only where specifically approved and usable in the secure workspace.

### Flow and monocyte function

- FCS files if releasable, compensation, panel/lot, frozen gating hierarchy,
  absolute counts, positive fraction, and intensity summaries;
- full prespecified marker table, including monocyte CD64;
- cytokine/chemokine condition, controls, units, values, censoring, and QC;
- myelin-phagocytosis endpoint, controls, units, values, and QC;
- reactive-oxygen-species endpoint, controls, units, values, and QC;
- Seahorse plate map, basal and maximal respiration, ATP-linked respiration,
  spare capacity, glycolytic measures, derived-variable definitions, and QC.

### Documents

- ToleDYNAMIC protocol/amendments, separate SAP, laboratory and assay manuals;
- data dictionaries, case-report forms, derivation specifications, batch maps;
- substudy enrollment and analysis flow diagrams; and
- disclosure, export, retention, small-cell, review, and publication rules.

## Frozen Analysis Commitments

- Eligibility and analysis branch are determined from design metadata before
  expression, functional, or clinical outcome values are viewed.
- No outcome-driven participant, assay, gene, module, endpoint, timepoint, or
  threshold selection is permitted.
- The transcript universe is the nine modules already committed in
  `scripts/v56_analyze_gse247181.py`, evaluated in two cell types as one
  18-slot family.
- HERCULES uses at least 100,000 randomization-stratified max-T permutations;
  PERSEUS retains all 18 original slots with per-slot alpha `0.05/18`.
- Functional endpoints form a separate fixed family after blinded SAP/schema
  mapping; transcript-function correlation alone is not mediation.
- Clinical linkage is continuous, estimation-only, and cannot create a
  responder classifier, cutoff, treatment recommendation, or subgroup
  benefit-risk claim.
- No rare liver-injury classifier will be fit from this substudy.

The complete executable decision rules are in
`knowledge_external/synthesis/V56_TOLEDYNAMIC_ACCESS_AND_TEST_PLAN.md`.

## Privacy, Security, And Dissemination

- All participant-level and sequence-level material remains in the approved
  controlled workspace under sponsor/platform terms.
- The public repository receives code, frozen metadata schemas, synthetic
  fixtures, and disclosure-approved aggregate outputs only.
- No attempt will be made to reidentify participants or combine controlled
  records with unapproved external individual-level data.
- Small cells, influence diagnostics, and subgroup outputs are exported only
  after required disclosure review.
- Negative, inconclusive, and branch-limited outcomes will be reported with the
  same prominence as positive outcomes.

## Human Submission Checklist

1. Nominate a qualified principal investigator and institutional signatory.
2. Ask Sanofi/Vivli whether ToleDYNAMIC is available with both parent trials and
   whether omics/FCS/function data require direct sponsor collaboration.
3. Submit HERCULES and PERSEUS as one linked scientific request and attach this
   packet plus the full access/test plan.
4. Obtain written answers to the seven access questions in the full plan before
   accepting a package as scientifically usable.
5. Preserve the design branch and analysis commit hash in the controlled
   workspace before any outcome-associated values are opened.

This packet makes the request executable. It does not establish that the
substudy was completed, that both arms are present, or that any tested immune
program mediates progression benefit.
