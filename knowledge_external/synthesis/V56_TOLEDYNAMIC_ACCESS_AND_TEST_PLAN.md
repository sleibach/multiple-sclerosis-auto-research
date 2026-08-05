# V56 ToleDYNAMIC Access And Test Plan

Status: pre-data controlled-access plan. The substudy is described in a public
protocol; completion, availability, participant coverage, randomization-arm
composition, and assay quality are not established.

Boundary: `external-verifiable`; `NOT_PROJECT_GROUNDED`; source:
https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf.

## Why This Is The Highest-Value Data Ask

- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf] Appendix 11 describes approximately 80 ToleDYNAMIC participants, about 40 each from HERCULES and PERSEUS, sampled before treatment and at months 3 and 12 with parent-trial clinical and MRI linkage.
- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf] Planned assays include detailed B/T/monocyte phenotyping, B-cell and CD14-monocyte RNA sequencing in a subset, monocyte cytokines, myelin phagocytosis, reactive oxygen species, and Seahorse metabolism.
- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf] The monocyte panel explicitly includes CD64 and other inflammatory, anti-inflammatory, chemokine-receptor, adhesion, and migration markers.

This is not proof that the data exist in an analyzable package. It is the first
identified progression-treatment dataset designed to connect randomized or
intervention-linked clinical outcomes with the exact immune compartments and
functional readouts the project has repeatedly encountered. It is therefore a
better use of access effort than another unrelated public expression cohort.

## Exact Access Questions

Before a scientific request is submitted, obtain written answers to:

1. Was ToleDYNAMIC completed, and how many HERCULES and PERSEUS participants
   have all three visits?
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

### Branch A: both randomized arms, outcome-blind substudy selection

Treatment-by-time effects are identifiable within the randomized substudy,
subject to selection and missingness audit. Run Gates 1-4 below.

### Branch B: active treatment only or arm revealed before selection

Paired changes cannot separate drug effect from time, regression, selection,
or study participation. Report descriptive trajectories only. No module,
functional effect, treatment-response marker, or mechanism advances.

### Branch C: only aggregate results or no parent-trial linkage

No project grounding is possible. Record the access limitation and stop.

The branch is determined from design metadata before expression or functional
values are viewed.

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
standardized log-expression scores. The primary contrast is arm difference in
paired month-3-minus-baseline change. Month 12 tests durability and cannot
rescue a month-3 failure.

Within each trial, use a participant model with arm, visit, arm-by-visit, site,
and assay batch, plus a random participant intercept. Calibrate the complete
valid module-by-cell-type family with at least `100,000` treatment-label
permutations constrained within parent-trial randomization strata and a max-T
statistic. If exact randomization strata cannot be reconstructed, label the
permutation approximate and require wild-cluster/bootstrap agreement.

HERCULES is the derivation trial only because its parent clinical endpoint was
positive at aggregate level. A module can enter PERSEUS replication only if it
passes HERCULES max-T, retains sign under leave-one-participant-out and
site/batch sensitivities, and has a bootstrap interval excluding zero. PERSEUS
uses the locked cell type, genes, score, direction, and month-3 contrast with
Bonferroni alpha `0.05/18`, regardless of how many HERCULES modules pass.

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
across all fixed functional endpoints for the randomized month-3 contrast.

A transcript module is called functionally anchored only if both its transcript
effect and a biologically corresponding functional endpoint pass their own
family-wise gates in the same trial and direction is specified before analysis.
Correlation alone does not establish mediation or causality.

## Gate 4: Clinical Link Is Estimation-Only

With at most about 40 participants per parent trial and fewer in the RNA subset,
no response classifier, subgroup cutoff, or clinical-utility claim is allowed.
For any HERCULES-to-PERSEUS replicated pharmacodynamic effect, estimate its
association with 24-month progression using a continuous interaction and report
the full interval. This is exploratory estimation with no promotion criterion.

A key informative outcome is mechanistic dissociation:

- the same pharmacodynamic change in positive HERCULES and negative PERSEUS
  means the measured peripheral effect is not sufficient to explain disability
  benefit;
- an effect only in HERCULES is phenotype-dependent but remains vulnerable to
  small substudy selection;
- no randomized pharmacodynamic effect rejects the tested peripheral module as
  a detectable month-3 mechanism in this package.

None establishes CNS target engagement without CNS measurement.

## Multiplicity Budget

| family | maximum tests | control |
|---|---:|---|
| HERCULES month-3 transcript modules | 18 (9 modules x 2 cell types) | max-T FWER 0.05 |
| PERSEUS transcript replication | fixed 18-slot universe | per-test alpha 0.05/18 |
| HERCULES functional endpoints | fixed after blinded SAP/schema mapping | one max-T FWER 0.05 |
| PERSEUS functional replication | same fixed universe | Bonferroni over original slots |
| Month-12 durability | same module families | cannot rescue month-3 failure |
| Clinical linkage | estimation only | no discovery claim |

## Decision Table

| result | verdict |
|---|---|
| Both arms and valid assay, no module pass | tested peripheral month-3 module mechanism not supported |
| HERCULES transcript pass, PERSEUS fail precisely | phenotype-specific or false-positive candidate; no shared mechanism |
| Both trials transcript pass, no function | reproducible pharmacodynamic transcript effect; function unestablished |
| Both transcript and matched function pass in both trials | replicated peripheral pharmacodynamic mechanism candidate; clinical mediation and CNS action unestablished |
| Same pharmacodynamics despite divergent parent efficacy | target engagement or peripheral change not sufficient for clinical benefit |
| Active arm only | descriptive paired change; no treatment-effect claim |
| Data unavailable | high-value external data blocker; no result |

## Access Action

Add ToleDYNAMIC explicitly to both Sanofi/Vivli requests rather than assume it
is included in standard clinical IPD. Ask for a sponsor scientific collaborator
if raw omics or functional data cannot be released through the ordinary Vivli
package. Submission and controlled-data obligations require a qualified human
principal investigator; no restricted participant data or small-cell output may
enter this public repository.

This route is the strongest identified path toward understanding a progression-
treatment mechanism with the mature project toolkit. It is still only a data
request and frozen test plan until the substudy data are obtained and rerun.
