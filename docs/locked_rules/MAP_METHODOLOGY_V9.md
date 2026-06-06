# MAP_METHODOLOGY_V9

Locked: 2026-06-02 11:18:00 CEST

Purpose: upgrade the highest-value V8 provisional axes, especially the
microbiome axis, without weakening the V8 evidence standards.

## Relationship To V8

V8 methodology remains active. V9 adds stricter upgrade rules for two axes:

- Axis 3: gut microbiome and microbial-immune signaling.
- Axis 2: genetic risk architecture.

All V8 placement labels, grade definitions, confidence levels, compartment
rules, contradiction handling, and evidence schemas remain unchanged.

## Cure-Class Claim Standard

V9 distinguishes three outputs:

1. **Axis upgrade**: a V8 provisional placement becomes supported or robust.
2. **Mechanistic hypothesis**: upgraded axis evidence converges with other axes
   into a specific mechanism.
3. **Intervention hypothesis**: the mechanism nominates an actionable target,
   pathway, modality, or trialable biomarker strategy.

A cure-class `FINDING_V9.md` requires all three. An axis upgrade alone is not
allowed to masquerade as a therapeutic finding.

## Axis 3 Microbiome Upgrade Criteria

### Required Inputs

Primary-data microbiome evidence must include at least one of:

- taxonomic relative-abundance table;
- metagenomic functional pathway table;
- metabolomics table linked to microbiome samples;
- published machine-readable feature/effect table with statistics.

Literature narrative or review-only evidence remains `provisional`.

### Harmonization

Preferred features:

- functional pathways: SCFA, bile acid, tryptophan, LPS/endotoxin,
  mucin/barrier degradation, IgA/bacterial translocation;
- taxa only when mapped to a clear functional mechanism or repeatedly observed:
  `Akkermansia`, `Faecalibacterium`, `Prevotella`, `Bacteroides`,
  butyrate-producing Clostridia, Enterobacteriaceae.

If raw taxa cannot be consistently mapped across studies, V9 uses
directional feature families rather than overfitting exact taxa.

### Quantitative Placement Rules

For a disease relative to MS:

- `near/supported`: at least two independent datasets or one dataset plus
  longitudinal/treatment perturbation evidence show same-direction overlap in
  at least two microbial functional families, with FDR `<0.10` within the
  tested feature matrix or explicit published corrected statistics.
- `intermediate/supported`: overlap exists in one family or direction agrees
  but disease mechanism differs by compartment/pathway, with at least one
  corrected quantitative source.
- `far/supported`: adequate disease-specific primary data show opposite
  direction or no overlap across the pre-specified feature families.
- `robust`: supported plus either longitudinal evidence, treatment
  perturbation, or independent cross-platform replication.

Cross-sectional case-control data alone cannot be `robust`.

### Similarity Metrics

When comparable feature vectors are available, compute:

- signed overlap count across pre-specified feature families;
- cosine similarity of signed standardized effects;
- Spearman correlation of signed feature effects;
- bootstrap confidence interval over feature families where feature count
  permits.

When only partially comparable feature sets exist, report feature-family
agreement and keep confidence at low or medium.

## Axis 2 Genetics Upgrade Criteria

Target-overlap remains `provisional`.

Upgrade requires at least one:

- LDSC/HDL genome-wide genetic correlation with MS;
- coloc/fine-mapping at shared loci;
- MR with validated instruments and pleiotropy assessment;
- verified published cross-disease genetic-correlation matrix with MS included.

Rules:

- `near/supported`: positive MS genetic correlation or multiple shared
  fine-mapped loci/pathways, with corrected significance.
- `intermediate/supported`: limited positive correlation or broad autoimmunity
  overlap without MS-specific direction.
- `far/supported`: no meaningful genetic correlation after adequate data
  coverage.
- HLA-only overlap cannot exceed `intermediate/supported` without non-HLA
  support.

## Intervention Synthesis Rules

An intervention hypothesis may be opened only if:

- at least one microbiome or genetics placement is upgraded to `supported`;
- the upgraded placement converges with at least two non-identical axes;
- the intervention point is specific enough to falsify.

Allowed intervention-point classes:

- microbial metabolite augmentation or depletion;
- barrier/mucosal immune modulation;
- APC-state modulation;
- complement or EBV-linked immune control;
- biomarker-guided transfer of an adjacent-disease therapy.

No patient recommendation is permitted.

## Multiple Testing

For newly computed microbiome features, use Benjamini-Hochberg FDR within each
analysis family:

- disease-vs-control feature tests;
- disease-pair signed-similarity tests;
- intervention-candidate enrichment tests.

Report both nominal p values and FDR. Do not upgrade a placement based only on
nominal results.

## Data Access And Blockers

If a dataset is inaccessible, too large, requires controlled access, or lacks
machine-readable feature tables, log it in `DATA_SEARCH_V9.md` and route around
it. Inaccessible data do not justify fabricated or inferred results.

## Locked Status

This methodology must exist before any V9 placement upgrade. Any analysis
started before this file is exploratory and cannot be used for upgrade unless
rerun under this methodology.
