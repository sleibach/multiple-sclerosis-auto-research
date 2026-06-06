# UC_GENETICS_TREATMENT_DECOUPLING_V12

Status: V12 resolution of matrix cell
`006_ulcerative_colitis_axis_02_genetics_vs_axis_07_treatment_response`.

## Question

Why is ulcerative colitis near MS on genetic risk architecture while its
treatment-response architecture is contradictory?

Supported V11 placements:

- `axis_02_genetics`: UC `near/supported/medium`, germline genetic
  correlation.
- `axis_07_treatment_response`: UC `contradictory/supported/medium`,
  intestinal mucosa treatment perturbation.

## Credential Status

The V12 prompt stated that `OPENGWAS_JWT` was available, but the environment
visible to this process returned `OPENGWAS_JWT_MISSING`. Therefore:

- no new OpenGWAS/LDSC execution was run;
- no new cross-trait colocalization was run;
- this cell is resolved at **supported** grade using existing project evidence
  and verified published genetics, not at robust V12 genetics grade.

This is not a silent downgrade. It is the central limitation of the cell.

## Triangulation Ecosystems Used

### 1. Published Cross-Disease Genetic Correlation

Source:

- Yang et al., Nature Communications 2021,
  "Investigating the shared genetic architecture between multiple sclerosis and
  inflammatory bowel diseases", DOI `10.1038/s41467-021-25768-0`.

Verified source facts:

- The paper reports MS-UC genetic correlation `rg = 0.33`,
  p `1.66e-13`.
- MS-CD genetic correlation is weaker: `rg = 0.16`, p `2.40e-3`.
- MS-IBD is intermediate: `rg = 0.28`, p `2.01e-10`.
- The paper reports mild sample-overlap signal via genetic covariance
  intercept around `0.1`.

Interpretation:

- UC has stronger genome-wide genetic proximity to MS than Crohn.
- This supports the matrix `near` placement for UC genetics.
- Genetic correlation alone does not identify which genes, cell states, or
  treatment-response mechanisms are shared.

### 2. OpenTargets Shared Genetic Target Overlap

Local file:

- `analysis/v12_uc_genetics_treatment/shared_ms_uc_opentargets_genetic_targets.tsv`

Extraction:

- From `phases/v3/results/wave55_external_genetics_druggability_sweep/opentargets_associated_targets_raw.tsv`.
- Threshold: OpenTargets `genetic_association >= 0.5` in both MS and UC.

Result:

- Shared MS/UC OpenTargets genetic targets: `12`.
- Shared genes:
  - `TNFRSF1A`
  - `SP140`
  - `IL2RA`
  - `CD40`
  - `BACH2`
  - `IL12B`
  - `INAVA`
  - `STAT3`
  - `PUS10`
  - `IFNGR2`
  - `GALC`
  - `IRF5`

Interpretation:

- The shared genetic target set is immune-risk architecture, not a direct
  treatment-response biomarker set.
- Several nodes are known or blocked therapeutic axes in MS transfer contexts:
  `TNFRSF1A` has MS paradox/safety risk; `IL2RA` and `IL12B/IL23` are crowded
  or prior-art-heavy; transcription factors such as `STAT3`, `IRF5`, and
  `BACH2` are not straightforward selective intervention points.

### 3. QTL / Target-Resolution Evidence

Local file:

- `phases/v3/results/wave62_opentargets_target_resolution/target_resolution_summary.tsv`

Relevant examples:

- `SP140`: strong L2G diseases `Crohn;MS;Psoriasis`; strong QTL coloc diseases
  `Crohn;MS;Psoriasis`; MS relevant QTL biosamples include monocyte, T cell,
  blood, lymphoblastoid cell line, naive regulatory T cell, and transverse
  colon; V3 status `PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW`.
- `INAVA`: strong L2G diseases `AS;Crohn;MS;UC`; strong QTL coloc diseases
  `AS;Crohn;MS;PBC;UC`; V3 status `PARK_TARGET_RESOLVED_BUT_BLOCKED_OR_NARROW`.
- `IL2RA`: strong L2G diseases `Crohn;MS;Psoriasis;RA;T1D`; prior context
  blocker `CD25_IL2_axis_prior_art_directionality`.
- `TNFRSF1A`: high MS L2G/QTL support but V3 blocker
  `TNF_axis_prior_art_and_MS_paradox_risk`.

Interpretation:

- QTL/L2G evidence maps some shared genetics to immune genes and relevant
  immune or gut-associated biosamples.
- This is **not** cross-trait MS-UC colocalization. It cannot prove the same
  causal variant drives both MS and UC at a locus.
- It does show why genetic proximity need not transfer as treatment-response:
  shared risk nodes are upstream immune susceptibility nodes, not necessarily
  downstream mucosal repair-response controllers.

### 4. Cell-State Transcriptomics

Local V8 evidence:

- UC colon myeloid `mixscale_validated_ifng_readout`: Hedges g `3.271`,
  p `0.000116`, FDR `0.0250`, `6` UC cases and `6` controls.
- UC colon myeloid `ifn_apc`: Hedges g `2.359`, p `0.00130`, FDR `0.0525`,
  `6` UC cases and `6` controls.

Wave166 same-gene genetics/cell-state audit:

- `SP140`: genetics gate `True`, same-gene cell-state gate `True`,
  perturbation trend `True`, positive cell-state contexts include
  `ibd_crohn_myeloid;ibd_uc_myeloid`; selected score `7.5`.
- `STAT4`: genetics gate `True`, same-gene cell-state gate `True`, positive
  contexts include `ibd_crohn_myeloid;ibd_uc_myeloid`; score `7.3`.
- Wave166 branch call: `NO_UNBLOCKED_SAME_GENE_GENETICS_CELLSTATE_ROUTE`.

Interpretation:

- UC has strong inflammatory myeloid/APC state evidence.
- Some genetic nodes overlap cell-state recurrence, but V3 did not find an
  unblocked same-gene intervention route.

### 5. Treatment-Response Evidence

Local V7/V8 evidence:

- `GSE12251` UC baseline mucosal `baseline_IFN_APC`: AUC `0.250`, Hedges g
  `-1.043`, p `0.0195`, n `22`; baseline fails.
- `GSE16879` paired IBD mucosa `-delta_IFN_APC`: AUC `0.754`, Hedges g
  `0.985`, p `0.000365`, n `60`; early delta passes.
- `GSE73661_IFX` paired UC mucosa `-delta_IFN_APC`: AUC `0.825`, Hedges g
  `1.390`, p `0.0127`, n `23`; early delta passes.
- `GSE73661_VDZ` exploratory vedolizumab `-delta_IFN_APC`: AUC `0.889`,
  Hedges g `1.286`, n `24`; exploratory, same direction.

Interpretation:

- UC treatment response depends on dynamic mucosal inflammatory-state
  downshift, not static baseline IFN/APC height.

## Artifact Audit

Compartment:

- Genetics is germline and not compartment-specific.
- Treatment response is intestinal mucosa.
- Cell-state support is colon myeloid.
- The compartment mismatch is real but informative: germline immune risk can be
  shared between MS and UC while the response-monitoring axis is constrained by
  mucosal tissue dynamics.

Cohort:

- Genetics source, OpenTargets target overlap, cell-state atlas evidence, and
  V7 treatment-response cohorts are independent evidence sources.
- No single-cohort artifact explains the disagreement.

Measurement grade:

- Genetic correlation measures inherited liability.
- Treatment response measures dynamic therapy-induced change.
- These are different biological layers. The disagreement is biological only
  if interpreted as layer decoupling, not as direct contradiction.

Sample overlap / stratification:

- Yang 2021 reports genetic covariance intercept around `0.1`, interpreted
  there as mild sample overlap.
- V12 did not rerun LDSC or sample-overlap checks because `OPENGWAS_JWT` was
  not visible.
- Population stratification sensitivity is inherited from the published
  analysis, not independently audited here.

Colocalization:

- New cross-trait MS-UC coloc was not run.
- Existing QTL coloc/L2G evidence maps disease loci to genes, but does not
  establish that MS and UC share identical causal variants at those loci.

## Hostile Critique

Criticism:

- This is not the V12 full genetics standard because OpenGWAS/coloc did not
  run.

Response:

- Correct. The cell is resolved at supported grade, not robust V12 genetics
  grade. The resume state must preserve this upgrade requirement.

Criticism:

- The shared OpenTargets genes are broad autoimmune genes and may not explain
  UC treatment response.

Response:

- Correct. That is the mechanism of the disagreement: shared genetic liability
  acts upstream at immune-risk architecture, while UC treatment response is a
  downstream mucosal dynamic state.

Criticism:

- Dynamic IFN/APC downshift could be generic healing rather than genetically
  mediated APC plasticity.

Response:

- Accepted. V12 does not claim genetically mediated APC plasticity. It claims
  shared genetic susceptibility does not license transfer of baseline or static
  treatment-response biomarkers.

## Classification

V12 status: `intervention_derived`.

Resolved statement:

> MS and UC share upstream immune genetic liability, but UC treatment-response
> transfer depends on downstream mucosal inflammatory-state dynamics; shared
> genetic risk does not imply baseline IFN/APC response-stratifier transfer.

This is a genetics-to-treatment-response layer decoupling, not a therapeutic
target nomination.

## Mechanistic Explanation

The shared MS/UC genetic architecture implicates immune susceptibility nodes
and immune regulatory pathways. Those nodes can increase disease liability
without determining whether inflamed mucosal tissue can dynamically downshift
IFN/APC activity after therapy. Treatment-response architecture therefore
operates downstream of genetic liability and is shaped by tissue compartment,
therapy mechanism, and repair kinetics.

## MS Transfer Consequence

What transfers to MS:

- Genetic proximity supports watching UC/IBD immune-risk biology for MS
  mechanism hypotheses, especially immune regulatory nodes that also have MS
  evidence.
- Dynamic response-monitoring logic may transfer only as an early
  compartment-relevant pharmacodynamic readout.

What does not transfer to MS:

- UC baseline mucosal IFN/APC response stratification.
- UC anti-TNF therapeutic logic, because TNF blockade has MS-specific paradox
  and safety risk.
- Any shared genetic node as an MS target without locus-level colocalization,
  causal direction, cell-state expression, perturbation support, and MS safety
  review.

## Falsification / Upgrade Path

Robust-grade upgrade:

1. Run OpenGWAS/LDSC or HDL for MS-UC with explicit sample-overlap and
   population-stratification checks.
2. Run cross-trait colocalization at the 12 shared OpenTargets genetic nodes
   and at genome-wide significant MS/UC shared loci.
3. Map coloc-positive variants to genes using eQTL/pQTL in blood, monocyte,
   T-cell, colon, and relevant CNS/CSF-adjacent tissues.
4. Test whether coloc-positive genes predict baseline IFN/APC or early
   `-delta_IFN_APC` in UC treatment cohorts.

Stop-loss:

- If coloc-positive shared MS/UC genes directly predict UC baseline response
  with AUC `>=0.70` in independent cohorts, the decoupling claim is weakened.
- If no coloc-positive shared genes survive after proper coloc, the genetic
  axis remains genome-wide correlation only and this cell should be downgraded
  from intervention-derived to supported biological hypothesis.
