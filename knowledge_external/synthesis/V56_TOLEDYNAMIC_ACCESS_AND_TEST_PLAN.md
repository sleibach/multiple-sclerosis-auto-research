# V56 ToleDYNAMIC Access And Test Plan

Status: pre-data controlled-access plan. The substudy is described in a public
protocol; completion, availability, participant coverage, and assay quality are
not established. The public protocol repeatedly specifies tolebrutinib-treated
participants, so active-treatment-only Branch B is the default design reading.

Boundary: `external-verifiable`; `NOT_PROJECT_GROUNDED`; source:
https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf.

## Why This Is The Highest-Value Data Ask

- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf] Appendix 11 describes approximately 80 ToleDYNAMIC participants, about 40 each from HERCULES and PERSEUS, sampled before treatment and at months 3 and 12 with parent-trial clinical and MRI linkage.
- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf] Planned assays include detailed B/T/monocyte phenotyping, B-cell and CD14-monocyte RNA sequencing in a subset, monocyte cytokines, myelin phagocytosis, reactive oxygen species, and Seahorse metabolism.
- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf] The monocyte panel explicitly includes CD64 and other inflammatory, anti-inflammatory, chemokine-receptor, adhesion, and migration markers.

This is not proof that the data exist in an analyzable package. It is the first
identified progression-treatment dataset designed to connect intervention-
linked clinical outcomes with the exact immune compartments and functional
readouts the project has repeatedly encountered. It is therefore a better
molecular access target than another unrelated public expression cohort, but
the public design does not support a randomized drug-effect claim.

## Public-Protocol Design Verdict

- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf] Appendix 11 objective 1 specifies flow cytometry of "tolebrutinib-treated participants" before and after treatment onset.
- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf] The design section specifies baseline sampling before treatment and months 3 and 12 after initiation of tolebrutinib.
- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf] The appendix does not describe placebo-arm sampling, while the parent trials themselves were randomized.

Therefore Branch B is fixed as the default before data access. Branch A is
available only if sponsor documentation explicitly establishes that placebo
participants were also sampled and that inclusion was fixed outcome-blind
before unblinding. Absence of arm metadata cannot be interpreted favorably.

## Extension-Registry Update

- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://clinicaltrials.gov/study/NCT06372145] ToleDYNAMIC is also named in the active, nonrandomized, open-label LTS17043 extension, with biomarker change from extension baseline through 12 months and estimated completion in April 2029.
- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://clinicaltrials.gov/study/NCT06372145] All participants from the progressive-MS parent trials start open-label tolebrutinib in the extension; no registry results are posted.

This confirms Branch B but adds a bounded secondary contrast if prior parent
assignment and exposure are linkable: former-placebo initiators versus
former-tolebrutinib continuers. That estimates an initiation-versus-continuation
trajectory among selected rollover participants, not a current randomized
drug-versus-placebo effect. The parent Appendix 11 and extension sampling
relationship must be documented before any baseline is chosen.

## Exact Access Questions

Before a scientific request is submitted, obtain written answers to:

1. Are Appendix 11 and LTS17043 ToleDYNAMIC one continuous substudy, and how
   many HERCULES and PERSEUS participants have all three visits?
2. Were both randomized arms sampled in each parent trial? If yes, was substudy
   enrollment fixed before unblinding and independent of post-randomization
   outcome?
3. Which participants received RNA sequencing, and was subset selection based
   on sample quality only or on clinical/assay results?
4. Are raw gene counts, normalized data, FASTQ/BAM access, FCS files, gating
   tables, absolute counts, cytokine values, phagocytosis readouts, ROS values,
   and Seahorse parameters requestable?
5. Can participant identifiers be linked to randomized arm, exposure,
   interruption, liver monitoring, MRI, EDSS, T25FW, 9HPT, relapse, prior DMT,
   NfL, CHI3L1, and final progression outcomes under the same workspace?
6. Is the separate ToleDYNAMIC SAP, laboratory manual, assay dictionary,
   batch/plate map, and missingness reason available?
7. What small-cell, export, collaboration, publication-review, and retention
   constraints apply?
8. For extension participants, are prior randomized assignment, exposure,
   rollover eligibility/non-enrollment, and every substudy-selection step
   linkable for a participant-flow and selection audit?

No absence or presence is inferred until these questions are answered.

## Requested Package

### Participant and design map

- parent trial, randomized arm, randomization strata, substudy consent/enrollment
  date, site, visit, draw time, exposure and interruption history;
- sample failures, reasons, freeze/thaw, processing delay, shipment time, plate,
  batch, operator, and subset-selection fields;
- parent-trial clinical, MRI, and safety linkage listed in the cross-trial plan.

### RNA sequencing

- raw integer gene-count matrices for sorted B cells and CD14 monocytes;
- gene identifier/version map, library size, strandedness, protocol, sequencing
  batch, alignment/counting pipeline, QC metrics, and excluded-library log;
- FASTQ/BAM only if sponsor terms and secure compute permit; no sequence-level
  data are committed publicly.

### Flow and function

- FCS files if permitted, frozen gating hierarchy, compensation, panel/lot,
  positive-fraction and intensity summaries, and absolute cell counts;
- monocyte CD64 and the complete prespecified marker panel;
- ex-vivo and stimulated cytokine/chemokine outputs with condition and controls;
- myelin-phagocytosis assay definition, controls, and quantitative endpoint;
- ROS endpoint and controls;
- Seahorse plate map plus basal respiration, ATP-linked respiration, maximal
  respiration, spare capacity, glycolytic measures, and QC flags where derived
  by the substudy SAP.

## Immutable Branch Before Values

### Branch A: sponsor-documented exception, both randomized arms and outcome-blind selection

Treatment-by-time effects are identifiable within the randomized substudy,
subject to selection and missingness audit. Run Gates 1-4 below.

### Branch B: public-protocol default, active treatment only or arm revealed before selection

Paired changes cannot separate drug effect from time, regression, selection,
or study participation. Report corrected descriptive trajectories only. A
shared change across clinically divergent parent trials can show that the
peripheral change is not sufficient to explain benefit; it cannot establish a
drug effect. No module, functional effect, treatment-response marker, or
mechanism advances.

### Branch C: only aggregate results or no parent-trial linkage

No project grounding is possible. Record the access limitation and stop.

The branch is determined from design metadata before expression or functional
values are viewed. The machine-readable branch contract is
`docs/validation/TOLEDYNAMIC_DESIGN_BRANCH_LOCK_V56.json`. It binds the
unchanged module lock by canonical hash and limits that older lock's
`randomized_arm_difference` contrast to Branch A. The module genes, score
rules, coverage rules, and 18 family slots remain unchanged.

## Gate 1: Sample And Assay Validity

- Freeze eligible participants from design metadata; no outcome-driven sample
  exclusion.
- Require baseline plus month 3 for the primary pharmacodynamic test. Month 12
  is durability only.
- Report arm-by-trial paired coverage, RNA subset mechanism, site/batch balance,
  processing delay, library depth, mapping, outliers, and missingness.
- If arm is perfectly nested within site, plate, sequencing batch, or processing
  delay category, that assay cannot support a treatment effect.
- A module is valid within a cell type only under the existing V56 coverage
  rule: at least half of frozen genes are variable, with both MOCCI genes and
  MIF mandatory for their one/two-gene modules.

## Gate 2: Frozen Transcript Module Family

No genes are selected from ToleDYNAMIC outcomes. Use the exact nine modules
committed before this substudy was identified in
`scripts/v56_analyze_gse247181.py`:

1. `receptor_cd44_cxcr4`
2. `hla_regulatory`
3. `ifn_apc_unique`
4. `mif_ligand`
5. `lysosomal_unique`
6. `oxphos`
7. `lipid_repair`
8. `resolution_efferocytosis_proxy`
9. `mocci_inflammatory_switch`

Within B cells and CD14 monocytes separately, compute frozen-gene mean
standardized log-expression scores. Month 12 tests durability and cannot rescue
a month-3 failure. The inferential contrast depends on the metadata-only branch:

- **Branch B (default):** within each trial, test paired
  month-3-minus-baseline change with participant-level sign flips, retaining
  site and assay batch as prespecified nuisance terms where identifiable. Use
  at least `100,000` sign-flip permutations and max-T across the complete valid
  18-slot module-by-cell-type family. This is a corrected temporal-trajectory
  test, not a treatment-effect test.
- **Branch A (documented exception):** use a participant model with arm, visit,
  arm-by-visit, site, and assay batch, plus a random participant intercept. The
  primary contrast is the randomized-arm difference in paired change. Use at
  least `100,000` treatment-label permutations constrained within reconstructed
  parent-trial randomization strata and max-T across all valid slots. If exact
  strata cannot be reconstructed, label the permutation approximate and require
  wild-cluster/bootstrap agreement.

HERCULES is the prespecified first trial because its parent clinical endpoint
was positive at aggregate level. A slot can enter the fixed PERSEUS comparison
only if it passes HERCULES max-T, retains sign under
leave-one-participant-out and site/batch sensitivities, and has a bootstrap
interval excluding zero. PERSEUS uses the locked cell type, genes, score,
direction, and month-3 contrast with Bonferroni alpha `0.05/18`, regardless of
how many HERCULES slots pass. Under Branch B this is cross-trial trajectory
concordance, not randomized replication. Under Branch A it is fixed randomized
replication.

## Gate 3: Functional Anchors

Functional endpoints are not inferred from transcript scores. Before values are
viewed, map the substudy SAP to exactly one frozen endpoint in each available
family:

1. myelin-phagocytosis capacity;
2. CD64 monocyte abundance/intensity;
3. ROS production;
4. basal and spare respiratory capacity, treated as one two-endpoint metabolic
   family;
5. the SAP-designated primary stimulated-monocyte inflammatory cytokine summary
   if one exists.

If the SAP does not designate an endpoint unambiguously, that family is
descriptive and cannot be selected from observed p-values. Use one max-T family
across all fixed functional endpoints. Branch B applies participant-level sign
flips to paired month-3 change; Branch A applies the randomized month-3
treatment-by-time contrast.

A transcript module is called functionally anchored only if both its transcript
change and a biologically corresponding functional endpoint pass their own
family-wise gates in the same trial and direction is specified before analysis.
In Branch B this means a functionally concordant temporal trajectory, not a
treatment mechanism. Correlation alone does not establish mediation or
causality in either branch.

## Gate 4: Clinical Link Is Estimation-Only

With at most about 40 participants per parent trial and fewer in the RNA subset,
no response classifier, subgroup cutoff, or clinical-utility claim is allowed.
For any HERCULES-to-PERSEUS concordant pharmacodynamic trajectory, estimate its
association with 24-month progression using a continuous interaction and report
the full interval. Branch A may additionally estimate the randomized
treatment-by-trajectory interaction. These are exploratory estimates with no
promotion criterion; they do not establish mediation.

A key informative outcome is mechanistic dissociation:

- the same active-treatment trajectory in positive HERCULES and negative
  PERSEUS means the measured peripheral change is not sufficient across the two
  progressive-MS contexts to explain disability benefit;
- an effect only in HERCULES is phenotype-dependent but remains vulnerable to
  small substudy selection;
- under Branch A, no randomized pharmacodynamic effect rejects the tested
  peripheral module as a detectable month-3 mechanism in this package; and
- under Branch B, no corrected paired trajectory means no detectable temporal
  shift, but cannot reject an unobserved treatment effect without a comparator.

None establishes CNS target engagement without CNS measurement.

## Multiplicity Budget

| family | maximum tests | control |
|---|---:|---|
| HERCULES month-3 transcript modules | 18 (9 modules x 2 cell types) | Branch B paired-sign-flip max-T or Branch A randomization max-T; FWER 0.05 |
| PERSEUS transcript comparison | fixed 18-slot universe | per-test alpha 0.05/18; concordance in Branch B, randomized replication in Branch A |
| HERCULES functional endpoints | fixed after blinded SAP/schema mapping | branch-matched max-T FWER 0.05 |
| PERSEUS functional comparison | same fixed universe | Bonferroni over original slots |
| Month-12 durability | same module families | cannot rescue month-3 failure |
| Clinical linkage | estimation only | no discovery claim |

## Decision Table

| result | verdict |
|---|---|
| Both arms and valid assay, no module pass | tested peripheral month-3 module mechanism not supported |
| Branch A: HERCULES transcript pass, PERSEUS fail precisely | phenotype-specific or false-positive candidate; no shared mechanism |
| Branch B: HERCULES trajectory pass, PERSEUS fail precisely | context-specific temporal trajectory or selection; no treatment-effect inference |
| Both trials transcript pass, no function | cross-trial transcript trajectory; function unestablished; randomized effect only in Branch A |
| Branch B: transcript and matched function pass in both trials | functionally concordant temporal trajectory; no treatment-effect, mediation, or CNS-action claim |
| Branch A: transcript and matched function pass in both trials | replicated peripheral pharmacodynamic mechanism candidate; clinical mediation and CNS action unestablished |
| Same active-treatment trajectory despite divergent parent efficacy | peripheral change is not sufficient across both disease contexts; context dependence and clinical mediation remain unresolved |
| Active arm only | corrected paired trajectory; no treatment-effect claim |
| Data unavailable | high-value external data blocker; no result |

## Access Action

Add ToleDYNAMIC explicitly to both Sanofi/Vivli requests rather than assume it
is included in standard clinical IPD. Ask for a sponsor scientific collaborator
if raw omics or functional data cannot be released through the ordinary Vivli
package. Submission and controlled-data obligations require a qualified human
principal investigator; no restricted participant data or small-cell output may
enter this public repository.

This route is the strongest identified molecular pharmacodynamic data ask with
the mature project toolkit. Under the public active-treatment-only design it is
not a randomized mechanism test. It is still only a data request and frozen
descriptive/sufficiency plan until the substudy data are obtained and rerun.

The submission-ready plain-language summary, scientific abstract, exact field
request, privacy boundary, and human checklist are in
`knowledge_external/synthesis/V56_TOLEDYNAMIC_REQUEST_PACKET.md`.
