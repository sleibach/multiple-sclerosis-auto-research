# CROHN_GENETICS_RESPONSE_REPAIR_DECOUPLING_V12

Status: V12 resolution of matrix cells:

- `008_Crohn_disease_axis_02_genetics_vs_axis_07_treatment_response`
- `009_Crohn_disease_axis_02_genetics_vs_axis_08_tissue_repair_resolution`

## Question

Why is Crohn disease only intermediate relative to MS on genetic risk
architecture while near MS on treatment-response and tissue-repair /
resolution-monitoring axes?

## Credential Status

`OPENGWAS_JWT` was not visible to this process. No new OpenGWAS/LDSC, HDL, or
cross-trait colocalization was run. This V12 resolution is supported-grade and
must be upgraded with executable genetics later.

## Triangulation Ecosystems Used

### 1. Published Genetic Correlation

V8 evidence registry from Yang et al. 2021:

- MS-Crohn `rg = 0.16`.
- MS-UC `rg = 0.33`.
- MS-IBD `rg = 0.28`.

Interpretation:

- Crohn has intermediate MS genetic proximity, weaker than UC.

### 2. OpenTargets Shared Genetic Targets

Local output:

- `analysis/v12_uc_genetics_treatment/shared_ms_crohn_opentargets_genetic_targets.tsv`

Result:

- Shared MS/Crohn OpenTargets genetic targets at `genetic_association >= 0.5`:
  `19`.
- The shared set is immune-risk rich: `TNFRSF1A`, `IL7R`, `TAGAP`, `SP140`,
  `IL2RA`, `CD40`, `BACH2`, `ANKRD55`, `IL12B`, `INAVA`, `STAT3`, `IFNGR2`,
  `GALC`, `IRF5`, and others.

Interpretation:

- Shared immune genetic targets exist, but target overlap is not genome-wide
  genetic correlation or cross-trait coloc.

### 3. QTL / L2G / Same-Gene Cell-State Evidence

Local wave62/wave166 evidence:

- `SP140`: strong L2G/QTL support in Crohn and MS; same-gene cell-state gate
  positive in IBD myeloid contexts; perturbation trend positive; still parked
  because intervention route is blocked/narrow.
- `STAT4`: broad autoimmune genetic support and IBD myeloid cell-state
  recurrence; blocked as a transcription-factor/directionality problem.
- `IL7R`, `IL2RA`, `TNFRSF1A`, and `INAVA` provide genetic support but do not
  give an unblocked same-gene intervention route for MS transfer.

Interpretation:

- The bridge from Crohn/MS genetics to response/repair state is incomplete.
- Candidate bridge genes exist, but none currently satisfies genetics +
  cell-state + perturbation + druggability + MS safety.

### 4. Cell-State And Treatment-Response Evidence

Crohn/IBD response evidence:

- `GSE16879` paired IBD mucosa `-delta_IFN_APC`: AUC `0.754`, Hedges g
  `0.985`, p `0.000365`, n `60`.

Crohn cell-state evidence:

- Colon myeloid `mixscale_validated_ifng_readout`: Hedges g `2.115`,
  p `0.00389`, FDR `0.0525`.
- Colon myeloid `ifn_apc`: Hedges g `2.087`, p `0.00443`, FDR `0.0563`.

Interpretation:

- Crohn/IBD mucosal response-monitoring and repair-resolution behavior is
  downstream and dynamic.
- Its support is strongest as mucosal inflammatory-state downshift, not
  inherited-risk similarity.

### 5. V11/V12 Transfer-Validity Context

The UC V11/V12 cells already established that:

- baseline/static IFN/APC height fails as a response predictor;
- early dynamic IFN/APC downshift tracks response;
- genetics proximity does not license baseline treatment-response transfer.

Crohn extends this pattern:

- weaker genetic proximity can still coincide with downstream dynamic mucosal
  response convergence.

## Artifact Audit

Compartment:

- Genetics is germline.
- Treatment/repair evidence is intestinal mucosa.
- Cell-state evidence is colon myeloid.
- The mismatch is not an artifact to erase; it defines the layer separation.

Cohort:

- Genetic, target-overlap, cell-state, and treatment-response sources are
  independent.
- GSE16879 is IBD pooled, so Crohn-specific treatment/repair resolution is
  weaker than UC-specific GSE73661_IFX.

Measurement grade:

- Treatment/repair axes use therapy-induced dynamic change.
- Genetics uses inherited liability.
- This is downstream convergence without equally strong inherited-risk
  proximity.

Colocalization:

- New MS-Crohn cross-trait coloc was not run.
- Existing QTL/L2G evidence supports target resolution but does not prove
  shared causal variants between MS and Crohn.

## Hostile Critique

Criticism:

- These two cells may duplicate the Crohn IFN/APC-versus-genetics cell.

Response:

- Partly true. The mechanistic core is shared. The additional value here is the
  treatment/repair consequence: downstream convergence is dynamic and
  response-monitoring, not just cross-sectional cell state.

Criticism:

- GSE16879 is IBD pooled, not Crohn-only.

Response:

- Accepted. These Crohn cells remain supported, not robust. A Crohn-only paired
  mucosal cohort would be required for robust grade.

Criticism:

- SP140 could be the missing intervention node.

Response:

- Possible but not established. V3/V12 park SP140 because direct modality and
  prior-art/intervention-route blockers remain. It is a mechanistic comparator,
  not a V12 target nomination.

## Classification

Cell `008` status: `intervention_derived`.

Resolved statement:

> Crohn's intermediate MS genetic proximity does not prevent downstream
> mucosal treatment-response convergence; early IFN/APC downshift is a dynamic
> response-monitoring feature that can converge downstream of different
> inherited causes.

Cell `009` status: `intervention_derived`.

Resolved statement:

> Crohn's intermediate MS genetic proximity does not prevent downstream
> tissue-repair / resolution-monitoring convergence, but the transferable
> concept is inflammatory-state downshift, not remyelination biology or shared
> causal genetics.

## MS Transfer Consequence

What transfers:

- Dynamic mucosal inflammatory-state downshift as a model for designing MS
  pharmacodynamic readouts in the correct compartment.
- Candidate bridge genes such as `SP140` as mechanistic comparators to watch,
  not as direct targets.

What does not transfer:

- Crohn genetic targets directly to MS without cross-trait coloc and MS safety.
- Crohn mucosal healing biology as a literal model of CNS remyelination.
- Anti-TNF therapeutic logic.

## Upgrade / Falsification Path

Robust upgrade:

1. Run MS-Crohn LDSC/HDL with sample-overlap and ancestry checks.
2. Run cross-trait coloc for shared loci.
3. Analyze Crohn-only paired mucosal treatment-response cohorts.
4. Test whether coloc-positive genes predict early `-delta_IFN_APC` better
   than baseline IFN/APC.

Stop-loss:

- If Crohn-only paired cohorts do not reproduce early `-delta_IFN_APC`
  response monitoring, both cells are downgraded.
- If MS-Crohn colocalization reveals strong shared causal variants directly
  predicting response dynamics, the current downstream-convergence explanation
  is replaced by a shared-genetic-controller explanation.
