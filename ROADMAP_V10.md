# ROADMAP_V10

Started: 2026-06-02 12:05 CEST

## Objective

V10 mines the MS-centered multi-axis map for **axis disagreements**: cases
where a disease is near MS on one supported axis but far, contradictory, or
otherwise materially different on another supported axis.

The cure-class DoD remains the forcing function: a mechanism-grounded MS
intervention hypothesis with five-axis convergent support including a
causal-grade axis, mechanistic chain, translational feasibility audit, V4
prior-art contribution, falsification path, and reproducibility.

Honest calibration: this cure-class DoD is very unlikely to be reachable from
public computational data in one session. V10's realistic product is the
resolved axis-disagreement structure of the MS map, plus the strongest
mechanistic and transfer-validity consequences it supports.

## Required Discipline

- No disagreement is claimed unless both placements are at least `supported`.
- Provisional-vs-supported or provisional-vs-provisional contrasts can be
  hypothesis-generating only; they do not enter the real disagreement core.
- Biological attribution is forbidden until compartment, cohort, and
  measurement-grade artifacts have been assessed.
- No binary disease clustering. Every conclusion is axis-specific.
- V9 primary microbiome evidence is incorporated as an axis update, but V9 did
  **not** support MS/IBD microbiome-mediated proximity.

## Genetics Credential Check

`OPENGWAS_JWT`: missing at start of V10.

Consequence:

- Automated OpenGWAS summary-stat download and harmonized LDSC cannot be run
  honestly at this checkpoint.
- V10 will use the existing supported UC/Crohn genetic-correlation source from
  V8 and the V9 genetics source manifest as access documentation.
- Genetics-involving disagreements outside UC/Crohn remain unresolved or
  provisional until JWT/manual summary-stat paths are available.

## Phase Plan

### Phase 1: Matrix Construction

Inputs:

- `analysis/v8_map/placement_matrix.tsv`
- `analysis/v8_map/evidence_registry.tsv`
- `MICROBIOME_AXIS_V9.md`
- `analysis/v9_microbiome/*`
- `analysis/v9_genetics/source_manifest.tsv`

Outputs:

- `analysis/v10_disagreement/placement_matrix_v10_overlay.tsv`
- `analysis/v10_disagreement/disagreement_pairs.tsv`
- `DISAGREEMENT_MATRIX_V10.md`

Method:

- Start from V8 placements.
- Apply V9 overlay annotations:
  - MS microbiome primary-data evidence exists but is one-dataset MS-only.
  - IBD microbiome proximity remains not supported.
  - Therefore Crohn/UC microbiome placement remains `provisional` for
    MS-relative proximity and cannot generate a supported disagreement.
- Encode placements ordinally for ranking:
  - `near = 3`
  - `intermediate = 2`
  - `far = 0`
  - `contradictory = special`: material disagreement with any non-contradictory
    supported axis; score distance `2.5` unless manually refined.
- Skip `unresolved`.
- Rank only pairs where both axes are `supported` or `robust`.

### Phase 2: Artifact Classification

For each high-ranked disagreement:

1. Compare compartments.
2. Compare data type and cohort family.
3. Compare causality level.
4. Compare evidence grade and confidence.
5. Classify as:
   - biological candidate;
   - compartment artifact likely;
   - measurement-grade artifact likely;
   - unresolved because one axis needs stronger data.

Outputs:

- `analysis/v10_disagreement/artifact_audit.tsv`
- `DISAGREEMENT_RESOLUTION_V10.md`

### Phase 3: Mechanistic Explanation

For each biological candidate:

- State the mechanistic decoupling in one sentence.
- Identify the MS-relevant implication.
- State a falsifiable prediction.
- Identify the data needed to falsify or confirm.

Priority expected candidates:

1. MS/IBD mucosal IFN/APC and repair proximity versus microbiome non-proximity.
2. RA far from MS on blood IFN/APC/treatment response but near on pregnancy.
3. UC near on IFN/APC/genetics/repair but contradictory on treatment-response
   architecture.
4. Sjogren near on IFN/APC but far on lipid-lysosomal state.

The list is provisional; the matrix controls priority.

### Phase 4: Intervention And Transfer-Validity Consequences

For each explained disagreement:

- What transfers from the comparator disease to MS?
- What does not transfer?
- What biomarker transfer is valid only in a specific compartment?
- What MS-specific intervention gap does the disagreement expose?
- Apply V4 prior-art recalibration: known targets are not invalidated merely
  because they are known; only equivalent failed mechanism tests invalidate.

Outputs:

- `TRANSFER_VALIDITY_MAP_V10.md`
- `AXIS_DISAGREEMENT_FINDINGS_V10.md`

## Stop Policy

Do not stop for failure of a single disagreement. Continue through ranked
supported disagreements, then into provisional hypothesis-generating
disagreements if the supported core is exhausted.

The session can stop only if externally interrupted, if a cure-class
breakthrough is achieved, or if the high-ranked disagreement matrix is resolved
and synthesized.
