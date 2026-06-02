# DISAGREEMENT_RESOLUTION_V10

Status: first-pass artifact audit and mechanistic classification.

Source tables:

- `analysis/v10_disagreement/disagreement_pairs.tsv`
- `analysis/v10_disagreement/artifact_audit.tsv`

## Classification Summary

| Class | Count | Disagreements |
| --- | ---: | --- |
| Survives first audit as biological candidate | 1 | Sjogren IFN/APC versus lipid-lysosomal split |
| Biological candidate after reformulation | 1 | UC IFN/APC versus treatment-response |
| Unresolved biological candidate due compartment/measurement mismatch | 6 | UC genetics/treatment, RA pregnancy contrasts, Crohn genetics contrasts |
| Survives first audit as perturbation-class biological candidate | 1 | RA pregnancy/postpartum near versus blood APC/treatment far |
| Lower-priority biological candidate | 3 | Crohn genetics versus IFN/APC/treatment/repair |
| Downgraded due axis non-independence | 1 | UC treatment-response versus tissue-repair |

Counts overlap by interpretive grouping because several Crohn and RA entries
share the same mechanism family.

## Downgraded Candidate: UC Treatment-Response Versus Tissue-Repair

### UC Treatment-Response Contradiction Versus Tissue-Repair Proximity

Supported placements:

- `axis_07_treatment_response`: UC is `contradictory/supported`.
- `axis_08_tissue_repair_resolution`: UC is `near/supported`.

Initial reason this looked strong:

- Both placements use intestinal mucosa.
- Both placements use treatment perturbation evidence.
- The disagreement is not compartment-driven from matrix metadata.

Hostile critique result:

- This row has high axis non-independence risk.
- `axis_08_tissue_repair_resolution` substantially reuses the dynamic
  `-delta_IFN_APC` evidence that is also the successful subset of
  `axis_07_treatment_response`.
- Therefore the row is downgraded from independent biological disagreement to
  treatment-dynamics refinement / transfer-validity warning.

What the disagreement actually means:

> UC is not contradictory because mucosal response biology is incoherent; it is
> contradictory because **baseline/static IFN/APC state fails as a response
> predictor while early dynamic IFN/APC downshift succeeds as a repair/response
> monitor**.

Evidence:

- `GSE12251` baseline IFN/APC failed: AUC `0.250`, Hedges g `-1.043`, n `22`.
- `GSE16879` early `-delta_IFN_APC` passed: AUC `0.754`, Hedges g `0.985`, n
  `60`.
- `GSE73661_IFX` early `-delta_IFN_APC` passed: AUC `0.825`, Hedges g `1.390`,
  n `23`.
- `GSE73661_VDZ` exploratory same-direction result: AUC `0.889`, Hedges g
  `1.286`, n `24`; this weakens anti-TNF specificity and supports mucosal
  healing/plasticity.

Reformulated safe explanation:

> In UC treatment datasets, baseline mucosal IFN/APC height fails as a response
> predictor while early mucosal IFN/APC downshift repeatedly tracks response.

MS consequence:

- Do not transfer UC baseline mucosal IFN/APC stratification directly to MS
  PBMC or baseline CSF.
- Test the MS analogue as an early dynamic change in the relevant compartment:
  CSF myeloid, lesion-edge myeloid, or possibly gut-proxy immune tissue.
- A static baseline APC module may mark inflammatory burden without predicting
  whether the tissue can transition toward repair.

Falsifiable prediction:

- In MS cohorts with paired pre-treatment and early on-treatment CSF or
  lesion-edge immune data, responders or repair-stable patients will show a
  larger early decrease in the locked IFN/APC module than nonresponders.
- Stop-loss: AUC `<0.60` or opposite effect direction in two independent MS
  paired-compartment cohorts.

Promotion requirement:

- Rebuild `axis_08` with independent repair endpoints that are not the same
  IFN/APC delta used in `axis_07`, such as endoscopic/histologic healing,
  epithelial restitution, fibrosis/remodeling, or non-IFN repair modules.

## Reformulated Biological Candidate

### UC IFN/APC Proximity Versus Treatment-Response Contradiction

Raw disagreement:

- UC is `near/robust` on cross-sectional colon myeloid IFN/APC state.
- UC is `contradictory/supported` on treatment-response architecture.

Artifact issue:

- Cross-sectional disease-state evidence and treatment perturbation evidence
  measure different biological quantities.

Reformulation:

> UC shares MS-like inflammatory antigen-presentation state, but state height
> and state plasticity are decoupled.

This is not a reason to discard the disagreement. It is the mechanistic content
of the disagreement.

Prediction:

- In IBD and MS, cross-sectional IFN/APC height will correlate with active
  inflammation but not necessarily with treatment response.
- Early IFN/APC delta will outperform baseline IFN/APC level as a
  response-monitoring signal in tissue-relevant compartments.

## RA Pregnancy Versus Blood APC/Treatment Divergence

Supported placements:

- RA is `far/supported` on IFN/APC blood myeloid/APC.
- RA is `far/supported` on treatment-response architecture.
- RA is `far/supported` on tissue-repair / response-monitoring architecture.
- RA is `near/supported` on pregnancy modulation.

Artifact audit:

- Pregnancy is a natural experiment; treatment response is a therapeutic
  perturbation.
- IFN/APC evidence is blood myeloid/APC and pregnancy evidence is blood, but
  timing and physiological perturbation differ.
- Tissue repair includes blood/synovium and is not cleanly matched.
- V10 RA audit file: `RA_PREGNANCY_TREATMENT_DECOUPLING_V10.md`.

Evidence details:

- RA blood `mixscale_validated_ifng_readout`: delta `-0.0178`, Hedges g
  `-0.182`, p `0.580`, FDR `0.686`, n `18/18`.
- RA blood `ifn_apc`: delta `-0.0460`, Hedges g `-0.249`, p `0.450`, FDR
  `0.572`.
- `GSE12051` RA baseline blood IFN/APC response rule: AUC `0.382`, Hedges g
  `-0.339`, n `44`.
- `GSE138746_CD14` RA anti-TNF CD14 monocytes: AUC `0.485`, Hedges g
  `-0.099`, n `78`.
- `GSE8350` RA infliximab 2-week blood `-delta_IFN_APC`: AUC `0.450`, Hedges g
  `-0.356`, n `18`.
- GSE235508 seropositive RA pregnancy timecourse shows late-pregnancy trough
  and postpartum rebound:
  - `mif_cd74_receptor_state`: T3-T1 `-0.642`; T6-T3 `1.162`.
  - `hla_ii_only`: T3-T1 `-0.646`; T6-T3 `1.394`.
  - `ifn_apc`: T3-T1 `-0.551`; T6-T3 `1.267`.
  - `lysosomal_apc`: T3-T1 `-0.566`; T6-T3 `0.835`.

First-pass interpretation:

> RA can be MS-adjacent on hormonal/natural-experiment immune modulation while
> remaining a poor comparator for APC treatment-response biomarkers.

MS consequence:

- RA pregnancy biology may be useful for postpartum flare or hormonal
  remission hypotheses in MS.
- RA anti-TNF or blood APC response architecture should remain a negative
  comparator for MS biomarker transfer.

Falsifiable prediction:

- Pregnancy-related immune-resolution signatures shared by RA and MS will not
  predict RA anti-TNF blood IFN/APC response, and will not rescue the failed
  V7 APC treatment-response rule.

Status:

- Tier 1 perturbation-class biological disagreement candidate.
- Not a therapeutic claim.
- Needs matched cell-composition-adjusted RA/MS pregnancy/postpartum datasets,
  ideally with monocyte/APC resolution and clinical activity timecourses.

## Sjogren IFN/APC Versus Lipid-Lysosomal Split

Supported placements:

- Sjogren is `near/supported` on salivary gland epithelial IFN/APC.
- Sjogren is `far/supported` on lipid-lysosomal / foamy myeloid state.

Artifact audit:

- Strong cell-type/compartment risk: epithelial IFN/APC activation is not the
  same as foamy myeloid lipid-lysosomal state.

Mechanistic candidate:

> Sjogren may share MS-like antigen-presentation activation in glandular
> epithelium while lacking MS-like lipid-lysosomal myeloid pathology.

GSE23117 bulk replication adjustment:

- `ifn_apc`: Hedges g `2.164`, p `0.000271`, FDR `0.00162`.
- `lysosomal_apc`: Hedges g `0.165`, p `0.652`, FDR `0.652`.
- `lipid_loader_repair`: Hedges g `0.562`, p `0.144`, FDR `0.253`.

Interpretation:

- Bulk data independently supports strong IFN/APC activation and lack of a
  lysosomal/APC module signal.
- Bulk data does not support a strict lipid-loader-negative claim; lipid-loader
  is positive-null and must be resolved in matched APC/foamy-myeloid
  compartments.

MS consequence:

- Sjogren may transfer epithelial/barrier antigen-presentation ideas to MS
  only if an MS epithelial/barrier analogue is specified.
- It is a poor transfer source for chronic-active lesion rim foamy myeloid
  biology unless matched myeloid data overturns the current far placement.

Falsifiable prediction:

- In matched Sjogren salivary single-cell data, IFN/APC-high epithelial states
  will not be accompanied by MS-like lipid-lysosomal myeloid expansion.

Status:

- Unresolved because matched compartment scoring is needed.

## Crohn Downstream Convergence Versus Intermediate Genetics

Supported placements:

- Crohn is `near/supported` on colon myeloid IFN/APC.
- Crohn is `near/supported` on treatment-response and tissue-repair dynamics.
- Crohn is only `intermediate/supported` on genetic risk architecture.

Interpretation:

> Crohn may converge with MS downstream in mucosal inflammatory-resolution
> architecture more than it shares inherited risk, whereas UC is closer to MS
> genetically.

MS consequence:

- Crohn-derived response-monitoring concepts may transfer even when genetic
  target transfer is weaker.
- UC is the better genetics-transfer comparator; Crohn is the better or equal
  dynamic mucosal-response comparator.

Falsifiable prediction:

- MHC-excluded LDSC/local-rg will preserve weaker MS-Crohn than MS-UC genetic
  proximity, while Crohn and UC remain similar on dynamic IFN/APC downshift
  response monitoring.

Status:

- Lower priority because placement distance is only `1.0` and genetics access
  is currently blocked.

## V10 Strongest Disagreement-Derived Finding So Far After Critique

The strongest current biological disagreement candidate is the Sjogren split:

> Sjogren salivary gland disease shares MS-like antigen-presentation activation
> but not MS-like lipid-lysosomal / foamy myeloid repair-state biology.

This is supported by matched local salivary epithelial and APC module contrasts
summarized in `SJOGREN_SPLIT_AUDIT_V10.md`, with GSE23117 bulk replication for
IFN/APC-positive and lysosomal/APC-null directionality. The lipid-loader-negative
component remains weaker because GSE23117 bulk lipid-loader is positive-null.

The strongest RA-derived disagreement candidate is:

> RA shares a pregnancy/postpartum immune-kinetic axis with MS but not the
> blood APC treatment-response architecture tested in V7.

This is supported by `RA_PREGNANCY_TREATMENT_DECOUPLING_V10.md`.

The strongest **UC treatment-dynamics hypothesis** is downgraded:

> UC's MS-adjacent antigen-presentation biology separates static inflammatory
> state from dynamic treatment-induced downshift: baseline IFN/APC height fails
> as a response predictor while early IFN/APC downshift repeatedly tracks UC
> response.

This is an MS-relevant transfer-validity rule, not a direct MS therapeutic
claim. It instructs MS programs to test dynamic compartmental APC plasticity in
CSF/lesion-edge/gut-proxy compartments rather than transferring IBD baseline
biomarkers or RA blood treatment-response rules.

Current tier:

- Tier 0 / Tier 1 candidate, not Tier 4 finding.
