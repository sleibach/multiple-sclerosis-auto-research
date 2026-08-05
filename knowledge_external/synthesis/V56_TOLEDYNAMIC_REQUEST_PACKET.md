# V56 ToleDYNAMIC Controlled-Data Request Packet

Status: submission-ready scientific content; sponsor/platform forms, a qualified
principal investigator, institutional approval, and data-use terms are still
required. No participant-level data have been obtained or viewed.

Boundary: `external-verifiable`; `NOT_PROJECT_GROUNDED`. Principal source:
https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf. Parent
trial sources: https://clinicaltrials.gov/study/NCT04411641 and
https://clinicaltrials.gov/study/NCT04458051. Extension source:
https://clinicaltrials.gov/study/NCT06372145. Date accessed: 2026-08-05.

## Plain-Language Summary

[`external-verifiable`; `NOT_PROJECT_GROUNDED`; source:
https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf]
HERCULES and PERSEUS tested tolebrutinib in two forms of progressive multiple
sclerosis. Their public protocol describes ToleDYNAMIC, an approximately
80-participant substudy with blood collected before treatment and at months 3
and 12. Planned measurements include detailed immune-cell phenotyping, tests of
monocyte function and metabolism, and RNA sequencing of selected B-cell and
monocyte samples.

The proposed project asks a limited question: do prespecified peripheral immune
programs change between baseline and month 3 among substudy participants, and
is the same trajectory observed in the two clinically divergent progressive-MS
trials? The analysis will use modules frozen before these data are accessed,
correct all module and functional tests as fixed families, and treat clinical
associations as estimation only. It will not search for a favorable patient
subgroup, infer that a blood change is a CNS mechanism, or make an individual
treatment recommendation.

[`external-verifiable`; `NOT_PROJECT_GROUNDED`; source:
https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf]
The public protocol specifies tolebrutinib-treated participants and sampling
after treatment initiation. The request therefore defaults to active-treatment-
only descriptive trajectories, with no treatment-effect or mechanism claim.
Randomized inference is permitted only if sponsor design metadata explicitly
document placebo sampling and outcome-blind selection. Controlled data will
remain in the approved secure workspace; only disclosure-approved aggregate
results will leave it.

[`external-verifiable`; `NOT_PROJECT_GROUNDED`; source:
https://clinicaltrials.gov/study/NCT06372145]
The current registry names ToleDYNAMIC within an active, nonrandomized,
open-label extension, lists biomarker change through 12 months, reports no
results, and estimates completion in 2029. The first request is therefore for
design continuity, protocol/SAP access, completed-assay counts, and an
availability timeline rather than an assumption that a mature package exists.

## Scientific Abstract

### Objective

Characterize prespecified month-3 pharmacodynamic trajectories in B-cell and
CD14-monocyte programs and functional monocyte readouts, and test whether the
same trajectory occurs in nrSPMS HERCULES and PPMS PERSEUS. Do not attribute
paired change to treatment without a documented randomized substudy comparison.

### Rationale

[`external-verifiable`; `NOT_PROJECT_GROUNDED`; source:
https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf]
ToleDYNAMIC was planned with baseline, month-3, and month-12 sampling; detailed
B/T/monocyte phenotyping; CD14-monocyte functional assays; and RNA sequencing
in selected sorted B-cell and monocyte samples. These intervention-linked
measurements can characterize peripheral pharmacodynamics. They can estimate a
randomized treatment effect only if both arms and outcome-blind substudy
selection are documented contrary to the active-treatment-only protocol reading.

### Prespecified Aims

1. Audit substudy selection, randomized-arm coverage, missingness, and assay
   batch structure without viewing outcome-associated expression or function.
2. In HERCULES, characterize paired month-3 change for nine previously frozen
   transcript modules in B cells and CD14 monocytes as one 18-slot max-T family,
   without attributing temporal change to treatment under the default branch.
3. Test a blinded-SAP-mapped family of monocyte functional endpoints and require
   independent transcript and function gates before using the label
   `functionally anchored`.
4. Compare any HERCULES transcript or functional trajectory with PERSEUS using
   the original fixed slots and thresholds, without family shrinkage or
   refitting; call this cross-trial concordance, not randomized replication.
5. Estimate, without promotion thresholds, whether replicated pharmacodynamic
   effects relate to the fixed 24-month EDSS progression endpoint.
6. If complete rollover metadata permit, estimate a secondary
   selection-conditional trajectory contrast between former-placebo initiators
   and former-tolebrutinib continuers; never label it a current randomized
   treatment effect.

### Primary Estimand

Under the public-protocol default, the primary summary is paired
month-3-minus-baseline change among tolebrutinib-treated participants, with a
full interval and fixed family correction. It is a temporal pharmacodynamic
trajectory, not a drug-effect estimand. If sponsor documentation establishes
the exceptional both-arm branch, the primary estimand becomes the randomized-
arm difference in that paired change. Month 12 assesses durability and cannot
rescue a month-3 failure.

### Mandatory Design Branch

- **Active arm only (public-protocol default), post-unblinding selection, or
  arm-confounded batch:**
  descriptive paired trajectories only; no treatment or mechanism claim.
- **Both randomized arms, outcome-blind selection documented by sponsor:**
  randomized treatment-by-time inference is permitted after validity gates.
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
- parent-trial eligibility, extension invitation/enrollment, non-enrollment
  reason, and substudy/RNA selection flow by prior randomized arm;
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
- Under the default active-treatment-only branch, HERCULES uses at least
  100,000 participant-level sign-flip max-T permutations for paired change;
  PERSEUS retains all 18 original slots with per-slot alpha `0.05/18`. Results
  are temporal trajectories and cross-trial concordance, not treatment effects
  or randomized replication.
- The secondary former-placebo-initiator versus former-active-continuer contrast
  requires complete rollover flow, exposure, selection, positivity, laboratory-
  blinding, weighting, selection-bound, and site/batch checks. It remains an
  onset-versus-continuation association.
- Only under sponsor-documented both-arm, outcome-blind sampling does the test
  change to randomization-stratified treatment-by-time max-T inference.
- Functional endpoints form a separate fixed family after blinded SAP/schema
  mapping; transcript-function correlation alone is not mediation.
- Clinical linkage is continuous, estimation-only, and cannot create a
  responder classifier, cutoff, treatment recommendation, or subgroup
  benefit-risk claim.
- No rare liver-injury classifier will be fit from this substudy.

The complete executable decision rules are in
`knowledge_external/synthesis/V56_TOLEDYNAMIC_ACCESS_AND_TEST_PLAN.md`.
The machine-readable design routing is frozen in
`docs/validation/TOLEDYNAMIC_DESIGN_BRANCH_LOCK_V56.json`, which binds the
unchanged 18-slot module lock and prevents its randomized contrast from being
used outside the sponsor-documented both-arm exception.

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
2. Ask Sanofi/Vivli how Appendix 11 relates to the NCT06372145 extension and
   whether ToleDYNAMIC is available with both parent trials and
   whether omics/FCS/function data require direct sponsor collaboration. State
   that the public protocol appears active-treatment-only and request explicit
   confirmation or documentary correction; do not infer placebo coverage from
   the randomized parent trials.
3. Submit HERCULES, PERSEUS, and NCT06372145 as one linked enquiry/request and
   attach this packet plus the full access/test plan.
4. Obtain written answers to the eight access questions in the full plan before
   accepting a package as scientifically usable.
5. Preserve the design branch and analysis commit hash in the controlled
   workspace before any outcome-associated values are opened.

This packet makes the request executable. It does not establish that the
substudy was completed, that both arms are present, or that any tested immune
program mediates progression benefit.
