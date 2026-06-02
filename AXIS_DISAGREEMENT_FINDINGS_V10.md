# AXIS_DISAGREEMENT_FINDINGS_V10

Status: first V10 synthesis after hostile critique integration.

## Executive Finding

The strongest current V10 biological disagreement candidate after hostile
critique is:

> Sjogren salivary gland disease shares MS-like antigen-presentation activation
> but not MS-like lipid-lysosomal / foamy myeloid repair-state biology.

This is not a cure claim and not a resolved Tier 4 finding. It is a Tier 1
axis-disagreement candidate with a clear transfer-validity consequence:
Sjogren may be useful for epithelial/barrier antigen-presentation comparison,
but it should not be used to transfer lipid-lysosomal lesion-rim repair biology
to MS.

The strongest UC-derived hypothesis remains important but downgraded:

> In UC treatment datasets, baseline mucosal IFN/APC height fails as a response
> predictor while early mucosal IFN/APC downshift repeatedly tracks response.

The strongest RA-derived hypothesis is:

> RA shares with MS a pregnancy/postpartum immune-kinetic axis while remaining
> far from MS on blood APC treatment-response architecture.

## Evidence Chain: Sjogren Split

### Axis 1: Sjogren Is Near MS On IFN/APC Antigen-Presentation

V8 placement:

- Sjogren `axis_01_ifn_apc`: `near/supported/medium`.

V10 matched-compartment audit:

- salivary gland epithelial `hla_ii_apc`: Hedges g `1.034`, p `0.0206`, FDR
  `0.0914`.
- salivary gland epithelial `mif_cd74_receptor_state`: Hedges g `1.075`, p
  `0.0207`, FDR `0.0914`.
- salivary gland epithelial `ifn_apc`: Hedges g `0.844`, p `0.0568`, FDR
  `0.157`.
- salivary gland APC `mif_cd74_receptor_state`: Hedges g `0.747`, p `0.0831`,
  FDR `0.199`.

### Axis 2: Sjogren Is Far From MS On Lipid-Lysosomal / Foamy Myeloid State

V8 placement:

- Sjogren `axis_04_lipid_lysosomal`: `far/supported/medium`.

V10 matched-compartment audit:

- salivary gland APC `lipid_loader_repair`: Hedges g `-0.774`, p `0.0554`, FDR
  `0.156`.
- salivary gland epithelial `lipid_loader_repair`: Hedges g `-0.202`, p
  `0.604`, FDR `0.697`.
- salivary gland APC `lysosomal_apc`: Hedges g `-0.307`, p `0.434`, FDR
  `0.555`.
- salivary gland epithelial `lysosomal_apc`: Hedges g `-0.267`, p `0.484`, FDR
  `0.600`.

### Mechanistic Meaning

The split is not simply epithelial versus myeloid:

- Antigen-presentation modules are strongest in epithelium but trend positive
  in APC.
- Lipid-loader and lysosomal repair modules are negative/null in both
  epithelial and APC compartments.

Mechanistic hypothesis:

> Antigen-presentation activation can decouple from lipid-lysosomal
> repair-state biology across autoimmune tissues.

MS implication:

- IFN/APC or HLA-II/CD74 similarity alone is insufficient evidence that a
  comparator disease models MS chronic-active lesion rim biology.
- MS lesion-rim programs need lipid-lysosomal / foamy myeloid evidence
  specifically.

## Evidence Chain: UC Static-Versus-Dynamic IFN/APC

### Axis 1: UC Is Near MS On IFN/APC State

V8 placement:

- UC `axis_01_ifn_apc`: `near/robust/high`.

Evidence:

- Colon myeloid `mixscale_validated_ifng_readout`: delta `0.4433`, Hedges g
  `3.271`, p `0.000116`, axis-local FDR `0.0250`.
- Colon myeloid `ifn_apc`: delta `0.4847`, Hedges g `2.359`, p `0.00130`,
  axis-local FDR `0.0525`.

Interpretation:

- UC and MS share an inflammatory antigen-presentation state at the module
  level, but this is cross-sectional and not itself a response predictor.

### Axis 2: UC Tissue-Repair / Response Monitoring Is Not Independent Enough

V8 placement:

- UC `axis_08_tissue_repair_resolution`: `near/supported/medium`.

Evidence:

- `GSE73661_IFX`: early mucosal `-delta_IFN_APC` AUC `0.825`, Hedges g
  `1.390`.
- `GSE73661_VDZ` exploratory: early mucosal `-delta_IFN_APC` AUC `0.889`,
  Hedges g `1.286`.

Interpretation after hostile critique:

- Early dynamic IFN/APC downshift tracks mucosal response and may not be
  anti-TNF-specific.
- However, the tissue-repair axis substantially overlaps the treatment-response
  axis for UC. It cannot currently serve as an independent evidence channel.

### Axis 3: UC Treatment-Response Architecture Is Contradictory

V8 placement:

- UC `axis_07_treatment_response`: `contradictory/supported/medium`.

Evidence:

- `GSE12251` baseline mucosal IFN/APC failed: AUC `0.250`, Hedges g `-1.043`,
  n `22`.
- `GSE16879` early mucosal `-delta_IFN_APC` passed: AUC `0.754`, Hedges g
  `0.985`, n `60`.
- `GSE73661_IFX` early mucosal `-delta_IFN_APC` passed: AUC `0.825`, Hedges g
  `1.390`, n `23`.

Interpretation:

- Baseline/static IFN/APC state and early dynamic IFN/APC plasticity are
  separable. Treating them as one biomarker is wrong.

### Axis 4: V9 Microbiome Does Not Explain The MS/IBD Proximity

V9 result:

- MS has supported one-dataset primary stool signals:
  - Bacteroides higher, age/sex-adjusted FDR `0.00639`.
  - Enterobacteriaceae/LPS proxy lower, adjusted FDR `0.00510`.
  - Faecalibacterium lower, adjusted FDR `0.0341`.
- IBDMDB/HMP2 independent-participant subset: no pre-specified family FDR
  `<0.10`.
- IBDMDB/HMP2 all-sample sensitivity: naive repeated-sample effects disappeared
  under participant-clustered inference.

Interpretation:

- The MS/IBD dynamic APC/repair proximity is not currently explained by shared
  broad taxonomic dysbiosis.
- A metabolite/pathway mechanism remains possible but is unproven.

### Axis 5: RA Provides A Negative Transfer Comparator

V8/V7 result:

- RA is `far/supported` on blood IFN/APC and treatment-response architecture.
- RA failed the locked V7 APC response rule in blood cohorts.
- RA is still `near/supported` on pregnancy modulation, showing that RA is not
  globally far from MS.

Interpretation:

- The APC plasticity rule is compartment and disease-axis specific. RA blood is
  a negative comparator for transferring IBD mucosal or MS compartmental APC
  response biomarkers.

## Evidence Chain: RA Pregnancy/Treatment Decoupling

### Axis 1: RA Is Far From MS On Blood APC State And Treatment Response

V8/V7 evidence:

- RA blood `mixscale_validated_ifng_readout`: delta `-0.0178`, Hedges g
  `-0.182`, p `0.580`, FDR `0.686`, n `18` RA and `18` controls.
- RA blood `ifn_apc`: delta `-0.0460`, Hedges g `-0.249`, p `0.450`, FDR
  `0.572`.
- `GSE12051` RA baseline blood IFN/APC response rule: AUC `0.382`, Hedges g
  `-0.339`, n `44`.
- `GSE138746_CD14` RA anti-TNF baseline CD14 monocytes: AUC `0.485`, Hedges g
  `-0.099`, n `78`.
- `GSE8350` RA infliximab 2-week blood `-delta_IFN_APC`: AUC `0.450`, Hedges g
  `-0.356`, n `18`.

Interpretation:

- RA blood does not reproduce the MS/IBD APC-state proximity or the IBD dynamic
  IFN/APC response-monitoring behavior.

### Axis 2: RA Is Near MS On Pregnancy/Postpartum Immune Kinetics

GSE235508 seropositive RA timecourse:

- `mif_cd74_receptor_state`: late pregnancy T3 - early T1 `-0.642`; 6wk
  postpartum T4 - T3 `0.526`; 6mo postpartum T5 - T3 `0.781`; later
  postpartum T6 - T3 `1.162`.
- `hla_ii_only`: T3 - T1 `-0.646`; T4 - T3 `0.493`; T5 - T3 `0.844`; T6 - T3
  `1.394`.
- `ifn_apc`: T3 - T1 `-0.551`; T4 - T3 `0.137`; T5 - T3 `0.651`; T6 - T3
  `1.267`.
- `lysosomal_apc`: T3 - T1 `-0.566`; T4 - T3 `0.309`; T5 - T3 `0.496`; T6 -
  T3 `0.835`.

Interpretation:

- Seropositive RA has a pregnancy trough and postpartum rebound in APC/HLA-II
  modules.
- This is a natural-experiment immune-kinetic axis, not the same biological
  object as anti-TNF treatment response.

### Mechanistic Meaning

The RA disagreement survives as a perturbation-class decoupling candidate:

> Pregnancy/postpartum endocrine-immune kinetics can align RA with MS even when
> RA blood APC treatment-response architecture does not.

MS implication:

- RA may be useful for postpartum flare timing and rebound hypotheses.
- RA is not a valid positive comparator for MS APC treatment-response
  biomarkers based on current blood evidence.
- The next decisive test is composition-adjusted RA/MS pregnancy data with
  monocyte/APC resolution and clinical activity timecourses.

## Mechanistic Hypothesis

The V10 mechanistic hypothesis is:

> In MS-adjacent IBD biology, inflammatory APC-state height and APC-state
> plasticity are decoupled; static antigen-presentation activation marks
> inflammatory tissue state, while early downshift capacity marks transition
> toward repair.

MS implication:

- MS programs should test early dynamic IFN/APC downshift in the relevant
  compartment, not baseline PBMC or static tissue IFN/APC height.

## Intervention Consequence

This hypothesis supports a biomarker and trial-design proposal, not a new drug
target:

- Use dynamic IFN/APC downshift as a pharmacodynamic readout in MS DMT or
  adjunctive trials.
- Prioritize CSF/lesion-edge or biologically justified gut-proxy compartments.
- Pair the readout with NfL, MRI lesion activity, and clinical follow-up.

It does not support:

- anti-TNF use in MS;
- baseline PBMC IFN/APC stratification;
- generic microbiome therapy;
- broad IBD dysbiosis transfer to MS.

## Falsification Path

### Computational / Clinical Cohort

Dataset:

- Paired baseline and early on-treatment MS CSF, lesion-edge, or other
  compartment-relevant immune transcriptomics.

Test:

- Score locked IFN/APC module:
  `STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`, `CD74`, `HLA-DRA`.
- Primary feature: early `-delta_IFN_APC`.
- Outcome: responder, relapse-free/MRI-stable, NfL decline, or lesion-resolution
  proxy.

Success:

- AUC `>=0.70` or Hedges g `>=0.7` in discovery, with direction replicated in
  an independent cohort.

Stop-loss:

- AUC `<0.60` or opposite direction in two independent compartment-relevant MS
  datasets.

### Wet-Lab

Model:

- Human monocyte-derived macrophages/DCs and iPSC microglia.

Perturbation:

- Inflammatory IFN-gamma stimulation followed by MS-relevant
  immunomodulatory/recovery perturbation.

Readout:

- IFN/APC module dynamics, viability, stress/global IFN controls, phagocytosis
  or efferocytosis where relevant.

Stop-loss:

- Dynamic downshift only appears through nonspecific toxicity or global
  transcriptional collapse.

## Prior-Art Position

The novelty is not that IFN/APC, IBD mucosal healing, or MS biomarkers exist.
The V10 contribution is the **axis-disagreement-derived transfer-validity
hypothesis**:

- UC is useful for MS dynamic APC plasticity transfer.
- UC baseline response stratification is not transferable.
- IBD broad taxonomic dysbiosis is not currently supported as the mediator.
- RA blood response architecture is a negative transfer comparator.

Under the V4 prior-art rule, known biology does not invalidate this
contribution unless an equivalent dynamic compartmental APC-plasticity
stratifier has been prospectively tested in MS and failed for mechanistic
reasons. No such evidence exists in the local project artifacts.

## Confidence

- Axis-disagreement matrix construction: high, because the supported-only rule
  is explicit and reproducible.
- UC static-versus-dynamic IFN/APC interpretation: medium as a treatment
  dynamics refinement, low-to-medium as a mechanistic APC-plasticity claim.
- MS transfer-validity implication: low-to-medium until paired MS compartment
  data are analyzed.
- Therapeutic intervention claim: not made.

## Hostile Critique Integration

Hypatia's V10 hostile critique identified a real flaw: UC
`axis_07_treatment_response` and `axis_08_tissue_repair_resolution` are not
independent evidence channels. They reuse overlapping datasets, feature
definitions, and response/healing interpretation. V10 therefore downgraded the
UC treatment-response versus tissue-repair row from clean supported
disagreement to internal treatment-dynamics refinement.

Correction made:

- `scripts/v10_build_disagreement_matrix.py` now adds an
  `axis_nonindependence_risk` flag and `independence_penalty`.
- The UC treatment-response versus tissue-repair row now ranks last among the
  ten supported disagreement pairs.
- The current strongest unresolved disagreement candidates are:
  - UC cross-sectional IFN/APC proximity versus treatment-response
    contradiction;
  - Sjogren IFN/APC versus lipid-lysosomal split;
  - RA pregnancy near versus APC/treatment far.

## Reproducibility

Entry points:

```bash
.venv/bin/python scripts/v10_build_disagreement_matrix.py
```

Key outputs:

- `analysis/v10_disagreement/placement_matrix_v10_overlay.tsv`
- `analysis/v10_disagreement/disagreement_pairs.tsv`
- `analysis/v10_disagreement/artifact_audit.tsv`
- `DISAGREEMENT_MATRIX_V10.md`
- `DISAGREEMENT_RESOLUTION_V10.md`
- `TRANSFER_VALIDITY_MAP_V10.md`
