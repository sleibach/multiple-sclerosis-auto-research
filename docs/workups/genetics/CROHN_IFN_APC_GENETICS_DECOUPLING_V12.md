# CROHN_IFN_APC_GENETICS_DECOUPLING_V12

Status: V12 resolution of matrix cell
`007_Crohn_disease_axis_01_ifn_apc_vs_axis_02_genetics`.

## Question

Why is Crohn disease near MS on IFN/APC antigen-presentation state but only
intermediate on genetic risk architecture?

Supported V11 placements:

- `axis_01_ifn_apc`: Crohn `near/supported/medium`, colon myeloid,
  cross-sectional.
- `axis_02_genetics`: Crohn `intermediate/supported/medium`, germline genetic
  correlation / target overlap.

## Credential Status

`OPENGWAS_JWT` was not visible to this process despite the V12 prompt. No new
OpenGWAS/LDSC, HDL, or cross-trait coloc was run. This cell is resolved at
supported grade using existing project evidence and published genetics.

## Triangulation Ecosystems Used

### 1. Published Cross-Disease Genetic Correlation

Source:

- Yang et al., Nature Communications 2021,
  DOI `10.1038/s41467-021-25768-0`.

Relevant values from the project V8 evidence registry:

- MS-Crohn genetic correlation: `rg = 0.16`.
- MS-UC genetic correlation: `rg = 0.33`.
- MS-IBD genetic correlation: `rg = 0.28`.

Interpretation:

- Crohn is genetically closer to MS than unrelated disease would be, but weaker
  than UC in the same source.
- This supports the matrix `intermediate` genetics placement.

### 2. OpenTargets Shared Genetic Target Overlap

Local output:

- `analysis/v12_uc_genetics_treatment/shared_ms_crohn_opentargets_genetic_targets.tsv`

Extraction:

- From `results_v3/wave55_external_genetics_druggability_sweep/opentargets_associated_targets_raw.tsv`.
- Threshold: OpenTargets `genetic_association >= 0.5` in both MS and Crohn.

Result:

- Shared MS/Crohn OpenTargets genetic targets: `19`.
- Top shared examples include `TNFRSF1A`, `IL7R`, `TAGAP`, `SP140`, `IL2RA`,
  `CD40`, `BACH2`, `ANKRD55`, `IL12B`, `INAVA`, `STAT3`, `IFNGR2`, `GALC`,
  and `IRF5`.

Interpretation:

- Shared target overlap exists, but it is broad autoimmune immune-risk
  architecture and does not lift Crohn to UC-level genome-wide genetic
  proximity.

### 3. QTL / Target Resolution And Same-Gene Cell-State Evidence

Local files:

- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave166_same_gene_genetics_cellstate_overlap/same_gene_genetics_cellstate_rank.tsv`

Relevant rows:

- `SP140`: strong L2G diseases `Crohn;MS;Psoriasis`, strong QTL coloc diseases
  `Crohn;MS;Psoriasis`, same-gene cell-state gate `True`, positive contexts
  include `ibd_crohn_myeloid;ibd_uc_myeloid`, perturbation trend `True`, but
  route remains parked/blocked.
- `STAT4`: broad autoimmune genetics, same-gene cell-state gate `True`,
  positive contexts include IBD myeloid, but transcription-factor and
  directionality blockers remain.
- `IL7R`, `IL2RA`, `TNFRSF1A`, `GALC`, and `INAVA` have genetic support but
  insufficient same-gene cell-state or intervention route support for a direct
  target claim.

Interpretation:

- Some specific genes bridge Crohn/MS genetics and IBD myeloid cell state,
  especially `SP140`.
- V3/V12 still do not identify an unblocked intervention route from these genes
  to MS treatment transfer.

### 4. Cell-State Transcriptomics

V8 local Crohn colon myeloid evidence:

- `mixscale_validated_ifng_readout`: delta `0.412`, Hedges g `2.115`,
  p `0.00389`, FDR `0.0525`, `6` Crohn cases and `6` controls.
- `ifn_apc`: delta `0.5851`, Hedges g `2.087`, p `0.00443`, FDR `0.0563`,
  `6` Crohn cases and `6` controls.

Interpretation:

- Crohn has strong downstream colon myeloid IFN/APC convergence with the
  MS-adjacent APC axis.

### 5. Treatment / Repair-Response Context

V7/V8 evidence:

- `GSE16879` paired IBD mucosa `-delta_IFN_APC`: AUC `0.754`, Hedges g
  `0.985`, p `0.000365`, n `60`.
- Crohn tissue-repair/response-monitoring placement is near, but the source is
  IBD pooled rather than Crohn-only.

Interpretation:

- Crohn's downstream mucosal inflammatory-resolution behavior is closer to the
  MS-adjacent APC plasticity hypothesis than its genetic architecture is.

## Artifact Audit

Compartment:

- Genetics is germline.
- IFN/APC evidence is colon myeloid.
- The compartment mismatch is expected and biologically meaningful: downstream
  mucosal inflammatory state can converge even when germline genetic
  architecture is only intermediate.

Cohort:

- Genetics, OpenTargets, QTL/L2G, cell-state atlas, and treatment-response
  evidence come from different sources.
- No single-cohort artifact explains the pattern.

Measurement grade:

- Genetic correlation measures inherited liability.
- IFN/APC cell state measures current inflammatory tissue state.
- The disagreement should be interpreted as layer decoupling, not as a direct
  contradiction.

Colocalization:

- New MS-Crohn cross-trait colocalization was not run.
- Existing QTL/L2G evidence is strongest for target resolution, not proof of
  shared MS-Crohn causal variants.

## Hostile Critique

Criticism:

- Crohn has 19 shared OpenTargets genetic targets with MS, more than UC's 12,
  so why call Crohn genetically intermediate?

Response:

- Target-count overlap is a proxy and is not comparable to genome-wide LDSC.
  The V8 placement used published LDSC values where MS-Crohn `rg=0.16` is
  weaker than MS-UC `rg=0.33`. Target overlap does not override LDSC.

Criticism:

- Crohn IFN/APC evidence is small-n donor local atlas evidence.

Response:

- Accepted. The effect sizes are large and supported, but this remains
  supported rather than robust. Replication in larger Crohn myeloid atlases
  would upgrade the cell.

Criticism:

- SP140 looks like a bridge; why not nominate it?

Response:

- V3/V12 explicitly park it: genetics/cell-state/perturbation support exists,
  but direct druggability, prior-art, and intervention-route blockers remain.
  The cell supports mechanism mapping, not a target claim.

## Classification

V12 status: `biological`.

Resolved statement:

> Crohn shares downstream colon myeloid IFN/APC inflammatory state with the
> MS-adjacent APC axis more strongly than it shares MS germline risk; this is
> downstream inflammatory convergence exceeding inherited-risk proximity.

## Mechanistic Explanation

Crohn and MS can converge on IFN/APC myeloid inflammatory state through tissue
inflammation and immune activation even when inherited disease liability is
less shared than MS-UC. In Crohn, barrier injury and mucosal inflammatory
context likely drive downstream APC activation; in MS, CNS/meningeal/immune
compartment processes can converge on related APC programs through different
upstream causes.

## MS Transfer Consequence

What transfers:

- Crohn-derived dynamic mucosal APC response-monitoring concepts may be useful
  as analogies for MS compartmental pharmacodynamic readouts.
- Specific genetics/cell-state bridge genes such as `SP140` remain useful
  mechanistic comparators.

What does not transfer:

- Crohn genetic targets as MS targets without cross-trait colocalization,
  causal direction, perturbation support, and MS safety/druggability review.
- Broad Crohn causal architecture as if it were UC-level MS genetic proximity.

## Upgrade / Falsification Path

Robust-grade upgrade:

1. Run MS-Crohn and MS-UC LDSC/HDL with sample-overlap checks once OpenGWAS is
   actually available in-process.
2. Run cross-trait colocalization for Crohn/MS shared loci, prioritizing
   `SP140`, `IL7R`, `TNFRSF1A`, `IL2RA`, `TAGAP`, `BACH2`, and `INAVA`.
3. Replicate Crohn colon myeloid IFN/APC state in an independent atlas.

Stop-loss:

- If MS-Crohn coloc-positive loci are as strong and numerous as MS-UC, and the
  Crohn IFN/APC state is not replicated in independent myeloid atlases, the
  downstream-convergence-exceeding-genetics claim is downgraded.
