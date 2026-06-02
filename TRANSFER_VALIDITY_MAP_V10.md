# TRANSFER_VALIDITY_MAP_V10

Status: first V10 transfer-validity map from supported axis disagreements.

## Principle

Transfer from another autoimmune disease to MS is valid only on the axis where
the disease is near MS. A disease can be useful for one MS mechanism and
misleading for another.

## Transfer Rules From Current Supported Disagreements

| Comparator disease | Transfers to MS | Does not transfer to MS | Why |
| --- | --- | --- | --- |
| UC | Dynamic mucosal inflammatory downshift / repair-monitoring architecture | Baseline IFN/APC response stratifier; broad taxonomic microbiome proximity | UC is near MS on IFN/APC, genetics, and tissue-repair axes, but treatment-response is contradictory because baseline fails while early delta succeeds. V9 did not support shared broad microbiome dysbiosis. |
| Crohn | Dynamic mucosal response-monitoring and repair concepts | Strong genetic-target transfer at UC-level confidence | Crohn is near on IFN/APC and repair/treatment axes, but only intermediate on genetic risk architecture. |
| RA | Pregnancy/hormonal natural-experiment hypotheses; negative comparator for APC response rules | Blood APC treatment-response biomarkers; anti-TNF-style APC response transfer | RA is near MS on pregnancy modulation but far on blood IFN/APC, treatment-response, and repair/response-monitoring axes. |
| Sjogren | Epithelial/barrier antigen-presentation hypotheses if matched to an MS analogue | Lipid-lysosomal / foamy myeloid lesion-rim biology | Sjogren is near on salivary epithelial IFN/APC but far on lipid-lysosomal / foamy myeloid state. |
| UC/Crohn as IBD group | Mucosal APC plasticity as a **dynamic pharmacodynamic readout** | Generic microbiome-mediated MS/IBD mechanism | V9 primary data supports MS microbiome shifts but not shared IBD broad taxonomic-family overlap after participant-aware inference. |

## Strongest Axis-Specific Transfer Consequence

### Antigen-Presentation Similarity Is Not Enough For Lesion-Rim Transfer

The cleanest V10 biological candidate is the Sjogren split:

> Sjogren is near MS on salivary antigen-presentation activation but far on
> lipid-lysosomal / foamy myeloid repair-state biology.

MS consequence:

- A comparator disease can share HLA-II/CD74/IFN antigen-presentation biology
  with MS without sharing the lipid-lysosomal myeloid biology relevant to
  chronic-active lesion rims.
- MS lesion-rim transfer programs should require explicit lipid-lysosomal /
  foamy myeloid evidence, not only IFN/APC similarity.

Transfer rule:

- Sjogren may inform epithelial/barrier antigen-presentation hypotheses.
- Sjogren should not currently be used as support for TREM2/APOE/LPL/GPNMB-like
  or lipid-loader lesion-rim repair interventions in MS.

## Strongest Biomarker-Design Consequence

### Dynamic APC Plasticity, Not Baseline APC Height

The strongest transfer-validity hypothesis from V10 is:

> For MS, adjacent-disease APC biology should be transferred as a dynamic,
> compartment-specific plasticity readout, not as a static baseline blood or
> tissue module.

Operational MS test:

- Measure locked IFN/APC module (`STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`,
  `CD74`, `HLA-DRA`) before treatment and at an early on-treatment timepoint.
- Use the relevant MS compartment:
  - CSF myeloid if available;
  - lesion-edge myeloid in tissue cohorts;
  - gut-proxy immune tissue only for gut-axis hypotheses;
  - PBMC only as a weak surrogate, never as definitive compartment evidence.
- Primary feature: early `-delta_IFN_APC`, not baseline IFN/APC level.

Expected result if this hypothesis is valid:

- Responders or tissue-repair-stable patients show larger early IFN/APC
  downshift than nonresponders.

Stop-loss:

- AUC `<0.60` or opposite direction in two independent paired MS
  compartment-relevant cohorts.

## Intervention Consequences

### What This Supports

1. **Biomarker-transfer program**
   - Use IBD to motivate dynamic APC plasticity as a pharmacodynamic biomarker
     in MS.
   - This is lower risk than claiming an IBD drug target transfers directly.

2. **Response-monitoring trial design**
   - In MS DMT or adjunctive trials, include early compartmental IFN/APC delta
     as a mechanistic readout.
   - This could be paired with NfL, MRI lesion activity, and, where feasible,
     CSF immune profiling.

3. **Pregnancy/hormonal comparator branch**
   - Use RA as a comparator for pregnancy remission/postpartum rebound biology,
     not for APC treatment-response transfer.
   - The supported RA pattern is a perturbation-class decoupling: seropositive
     RA shows late-pregnancy APC/HLA-II trough and postpartum rebound, while RA
     blood anti-TNF APC response rules fail.

4. **MS-specific lesion-rim branch**
   - Sjogren's IFN/APC similarity without lipid-lysosomal similarity reinforces
     that antigen-presentation activation is separable from foamy myeloid
     lesion-rim biology. Chronic-active MS lesion programs need myeloid
     lipid-lysosomal evidence, not only IFN/APC activation evidence.

### What This Does Not Support

- It does not support anti-TNF use in MS.
- It does not support baseline PBMC IFN/APC stratification for MS therapy.
- It does not support generic microbiome therapy for MS.
- It does not support direct transfer of IBD taxonomic dysbiosis signatures to
  MS.
- It does not support RA blood treatment-response biomarkers as MS biomarkers.
- It does not support treating RA as globally far from MS; RA is axis-near on
  pregnancy/postpartum immune kinetics and axis-far on blood APC treatment
  response.

## Prior-Art Recalibration

The V4 prior-art rule applies:

- Existing prior art on IFN/APC biology, IBD mucosal healing, or MS biomarkers
  does not invalidate the V10 contribution.
- The V10 contribution is the **axis-specific transfer-validity rule**:
  adjacent-disease mechanisms transfer by axis and compartment, and UC's useful
  transfer to MS is dynamic APC plasticity rather than baseline state or broad
  microbiome profile.
- Target-invalidating prior art would require an equivalent dynamic
  compartmental APC-plasticity stratifier to have been prospectively tested in
  MS and failed for target-mechanistic reasons. No such local evidence exists
  in the project artifacts.

## Falsification Path

### Wet-Lab / Ex Vivo

Experiment:

- Human monocyte-derived macrophages/DCs, iPSC microglia, and, if feasible,
  gut immune co-culture.
- Stimulate with IFN-gamma or inflammatory cocktail.
- Apply standard MS-relevant immunomodulatory perturbations or candidate
  repair-promoting conditions.
- Measure IFN/APC module at baseline, early perturbation, and recovery.

Decision rule:

- Dynamic downshift capacity must separate responder-like and nonresponder-like
  conditions by Hedges g `>=0.7` without global cytotoxicity or total IFN
  collapse.
- Stop-loss: effect below Hedges g `0.3` in two systems, or reduction explained
  by nonspecific transcriptional suppression.

### Clinical / Translational

Pilot design:

- Paired-compartment observational study nested in MS treatment initiation.
- Population: active inflammatory MS starting or switching DMT.
- Sampling: baseline and early on-treatment CSF/PBMC; lesion-edge tissue only
  if clinically/ethically available in existing tissue cohorts.
- Primary mechanistic endpoint: early `-delta_IFN_APC`.
- Secondary endpoints: NfL, MRI inflammatory activity, relapse/MRI activity
  over follow-up.

Sample size:

- Discovery: `40-60` participants if CSF is available.
- Replication: independent `60-100` participants or multicohort meta-analysis.

Stop-loss:

- No directionally consistent early IFN/APC downshift in responders, or no
  association with NfL/MRI trends after adjustment.

## Hostile-Critique Adjustment

The UC treatment-response and tissue-repair axes are not currently independent
evidence channels. Therefore, dynamic IFN/APC downshift should be treated as a
V10 transfer-validity **hypothesis and warning**, not as a validated rule.

The valid warning is:

- do not transfer baseline/static APC biomarkers to MS as if they were dynamic
  response readouts;
- do not claim tissue-repair mechanism until independent repair endpoints
  validate the dynamic IFN/APC interpretation.

## RA Pregnancy/Treatment Decoupling Adjustment

The V10 RA audit preserves a second transfer-validity rule:

> RA can transfer to MS as a pregnancy/postpartum timing comparator while
> failing as a blood APC treatment-response comparator.

Evidence:

- RA blood IFN/APC and anti-TNF response features are negative or failed:
  `GSE12051` AUC `0.382`, `GSE138746_CD14` AUC `0.485`, `GSE8350` early
  `-delta_IFN_APC` AUC `0.450`.
- Seropositive RA pregnancy data show a late-pregnancy trough and postpartum
  rebound in MIF/CD74, HLA-II, IFN/APC, and lysosomal/APC modules.

MS consequence:

- RA is a useful comparator for postpartum flare biology only if the analysis
  is time-resolved and composition-adjusted.
- RA should remain a negative comparator for blood APC treatment-response
  biomarker transfer.

## Current Confidence

- Dynamic UC mucosal IFN/APC downshift transfer hypothesis: medium as a UC
  response-monitoring observation; low-to-medium as an MS transfer rule.
- RA pregnancy/postpartum transfer hypothesis: medium as an RA natural
  experiment observation; low-to-medium as an MS transfer rule until matched
  RA/MS pregnancy data are composition-adjusted.
- MS clinical actionability today: low; needs compartment-relevant MS paired
  data.
- Direct therapeutic intervention claim: not made.
