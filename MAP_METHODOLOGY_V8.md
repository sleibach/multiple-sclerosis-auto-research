# MAP_METHODOLOGY_V8 - Pre-Specified Placement Criteria

Date locked: 2026-05-29  
Status: must be committed before placement generation  
Purpose: define how the MS-centered multi-axis mechanism map is built.

## Unit Of Analysis

The map cell is:

`disease x mechanistic_axis x compartment/evidence_context`

The final display may summarize to one disease-axis placement, but the evidence
registry retains compartment-specific rows. A blood result and a tissue result
are never silently averaged.

## Placement Labels

Each disease-axis cell is placed relative to MS as one of:

- `near`: evidence supports shared mechanism, direction, or causal architecture
  with MS on that axis.
- `intermediate`: evidence supports partial overlap, compartment-restricted
  overlap, or shared upstream biology with divergent downstream manifestation.
- `far`: evidence supports absence of meaningful overlap after adequate testing,
  or evidence points to a distinct mechanism on that axis.
- `contradictory`: multiple adequate evidence sources conflict in a way that
  cannot be resolved by compartment, timing, assay, treatment, or disease-stage
  differences.
- `unresolved`: evidence is absent, too sparse, inaccessible, or too indirect.

`far` requires evidence. Lack of data is `unresolved`.

## Evidence Grades

Each placement receives a grade:

- `provisional`: Tier -1-grade evidence; exploratory, single dataset, nominal
  signal, literature-only, or uncorrected local result.
- `supported`: at least two independent evidence sources or datasets agree, and
  the primary quantitative test survives the axis-specific correction rule.
- `robust`: supported plus at least one of:
  - independent rediscovery across project versions or analysis families;
  - orthogonal evidence type agreement such as genetics plus transcriptomics,
    perturbation plus longitudinal, or tissue plus treatment-response;
  - a pre-registered/locked validation success.

Negative placements can be `supported` or `robust` if the negative evidence
meets the same replication and correction standards.

## Confidence Levels

Confidence is separate from grade:

- `high`: multiple datasets, adequate sample sizes, clear compartment, and
  low risk of endpoint/assay mismatch.
- `medium`: replicated but limited by compartment, endpoint, sample size, or
  indirect measurement.
- `low`: thin, exploratory, literature-only, or unresolved compartment.

Confidence may be lower than grade when the statistics are strong but biology is
a weak surrogate.

## Matrix-Wide Correction Plan

The full quantitative map contains `D` diseases and `A` axes. For every
axis-specific quantitative test, p values are corrected across all disease-axis
cells tested within that axis using Benjamini-Hochberg FDR.

Map-wide interpretation:

- Axis-level FDR `<0.10` is required for `supported` when the placement depends
  on newly computed local statistics.
- FDR `<0.05` or independent replication is required for `robust`.
- For pre-existing locked validation outputs, use their pre-specified threshold
  as the primary control, then report their results in the matrix; do not re-fit
  or reinterpret thresholds.
- Literature-derived placements do not receive artificial p values. They can be
  `provisional` or `supported` only if multiple verified sources agree and the
  evidence type is explicitly marked as non-local/literature.

Multiple-testing correction is not applied across heterogeneous literature
claims; instead, those cells are capped at `supported` unless backed by local
quantitative replication or genetics.

## Axis-Specific Criteria

### Axis 1 - IFN/APC Antigen-Presentation State

Primary evidence:

- local module scores using fixed genes where possible:
  - IFN/APC: `STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`, `CD74`, `HLA-DRA`;
  - HLA-II: `HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `HLA-DQA1`,
    `HLA-DQB1`.
- disease tissue or sorted immune compartments preferred over whole blood.

Placement:

- `near`: disease shows MS-like IFN/APC or HLA-II/APC enrichment in relevant
  pathogenic tissue/cells with same direction and at least two datasets or one
  dataset plus genetics/perturbation support.
- `intermediate`: same module appears but only in different compartment,
  opposite disease stage, treatment response rather than disease state, or only
  one component matches.
- `far`: adequate disease-relevant data show no IFN/APC/HLA-II signal after
  compartment adjustment.
- `contradictory`: blood and tissue, or independent datasets, disagree and
  compartment/timing cannot resolve the discrepancy.

### Axis 2 - Genetic Risk Architecture

Primary evidence:

- genome-wide genetic correlation;
- shared fine-mapped/colocalized causal genes;
- HLA architecture, non-HLA immune loci, and pathway-level genetic enrichment.

Placement:

- `near`: positive genetic correlation or multiple shared causal loci/pathways
  including MS-relevant immune/HLA architecture.
- `intermediate`: shared immune loci but divergent HLA direction, limited
  correlation, or overlap driven by broad autoimmunity rather than MS-specific
  architecture.
- `far`: no meaningful shared genetic correlation or shared loci after adequate
  data coverage.
- `contradictory`: genome-wide and locus-level evidence point in opposing
  directions.

Single-gene overlap alone cannot exceed `provisional`.

### Axis 3 - Gut Microbiome And Microbial-Immune Signaling

Primary evidence:

- longitudinal or treatment-linked microbiome/metabolite changes;
- MS microbiome features overlapping gut-disease microbial-immune mechanisms;
- microbial metabolite pathways such as SCFA, bile acid, tryptophan, LPS,
  mucin/IgA, and barrier integrity.

Placement:

- `near`: shared microbial taxa/function/metabolite direction with mechanistic
  immune readout, preferably longitudinal or perturbation evidence.
- `intermediate`: dysbiosis or pathway overlap without causality or with
  compartment mismatch.
- `far`: adequate microbiome evidence indicates distinct direction or mechanism.
- `contradictory`: datasets disagree on key microbial functions or direction.

Cross-sectional dysbiosis alone is capped at `provisional`.

### Axis 4 - Lipid-Lysosomal / Foamy Myeloid State

Primary evidence:

- lipid-loaded macrophage/microglia/monocyte states;
- lysosomal/APOE/LPL/TREM2/CTSS/foam-cell modules;
- local V2/V3 lipid-lysosomal module outputs.

Placement follows the same near/intermediate/far logic, with strong compartment
tracking: CNS microglia, intestinal macrophages, synovial macrophages, skin
macrophages, and blood monocytes are separate evidence contexts.

### Axis 5 - Complement And Innate Effector Biology

Primary evidence:

- complement gene/module activation;
- C1q/C3/CFB/C5 axis evidence;
- innate effector modules including Fc receptors, neutrophil/S100, and
  inflammasome only when specifically tied to complement/innate effector state.

Generic inflammation is insufficient for `near`.

### Axis 6 - T-Cell And Adaptive Repertoire

Primary evidence:

- Th1/Th17/Treg/B-cell repertoire evidence;
- TCR/BCR clonality or antigen-specific repertoire;
- shared T-cell genetic or perturbation evidence.

Bulk lymphocyte activation without cell-type or repertoire resolution is capped
at `provisional`.

### Axis 7 - Treatment-Response Architecture

Primary evidence:

- locked or pre-specified response prediction/monitoring tests;
- early pharmacodynamic response;
- failed-trial or responder/nonresponder transcriptomics.

Placement:

- `near`: therapy response architecture mirrors MS on predictor, compartment,
  and drug-mechanism class.
- `intermediate`: shares a response module but different component, timing, or
  compartment.
- `far`: adequate treatment-response cohorts fail in the same tested
  compartment/class.
- `contradictory`: baseline and dynamic tests or compartments disagree.

V7 locked results are inherited as fixed evidence, not retuned.

### Axis 8 - Tissue Repair And Resolution Biology

Primary evidence:

- remyelination/OPC/oligodendrocyte repair for MS;
- mucosal healing, synovial resolution, skin resolution, islet repair analogs;
- pro-resolving macrophage/efferocytosis/TAM/LXR/ABCA1-like programs.

Repair analogies require a traceable cell-state or pathway bridge; superficial
use of the word "healing" is insufficient.

### Axis 9 - Sex, Hormonal, And Pregnancy Modulation

Primary evidence:

- pregnancy natural experiments;
- sex-biased incidence and hormone-linked immune kinetics;
- postpartum flare/remission patterns.

Near/intermediate/far must track timing: late pregnancy, postpartum, and
pre-pregnancy baselines are separate contexts.

### Axis 10 - Infectious-Trigger Biology

Primary evidence:

- EBV, HHV6, CMV, HERV, SARS-CoV-2, gut pathogens, molecular mimicry;
- longitudinal serology or pre-disease evidence preferred.

EBV is treated as a strong MS anchor. Other diseases are near only if evidence
links infectious exposure to disease risk or mechanism, not merely association
with immune activation.

## Evidence Registry Schema

Every evidence row must include:

- `evidence_id`
- `axis`
- `disease`
- `compartment`
- `data_type`
- `dataset_or_source`
- `effect_direction`
- `statistic`
- `p_value`
- `fdr_or_correction`
- `sample_size`
- `causality_level`
- `supports_placement`
- `caveat`
- `file_or_url`

## Placement Matrix Schema

Every placement row must include:

- `axis`
- `disease`
- `placement`
- `grade`
- `confidence`
- `primary_evidence_ids`
- `contradiction_ids`
- `compartment_summary`
- `causality_summary`
- `selection_bias_risk`
- `notes`

## Contradiction Handling

Contradictions are first-class outputs. A contradiction is logged when:

- same disease-axis has opposite directions across independent datasets;
- blood and tissue disagree and no compartment explanation is supported;
- genetics and expression point to different mechanisms;
- treatment-response evidence disagrees with disease-state evidence.

Resolution attempts may change placement from `contradictory` to
`intermediate`, but only if the resolving variable is specified and evidence is
traced.

## Causality Levels

Each evidence row receives one:

- `cross_sectional`
- `longitudinal`
- `natural_experiment`
- `treatment_perturbation`
- `genetic`
- `mechanistic_perturbation`
- `clinical_trial`
- `literature_review`

Placements supported only by `cross_sectional` evidence cannot be `robust`.

## Source Verification

Rules:

- Local outputs are acceptable only if code and inputs are traceable.
- Literature claims require verified source links or PubMed/DOI/accession.
- If browsing is used, sources are saved or cited in axis notes.
- No citation is inferred from memory.

## Pre-Analysis Knowledge Query

The required V8 pre-analysis query was run before placement generation:

`MS RA IBD IFN APC antigen presentation genetic microbiome mechanism map`

Result: nearest local records were `HYP_V6_006`, V6 confounder mining, V7 sidecar
reports, pregnancy critiques, and genetics/celiac subagent reports. No existing
formal multi-axis MS mechanism map was found.
