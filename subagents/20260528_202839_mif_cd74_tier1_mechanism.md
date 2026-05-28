# MIF/CD74 Tier 1 Mechanism Sidecar

Timestamp: 2026-05-28 20:28 CEST

Scope: Tier 1 mechanism assessment only. This report does not claim Tier 2
advancement.

## Read-In

Primary files reviewed:

- `meta/CURRENT_STATUS.md`
- `meta/ROADMAP_V5.md`
- `knowledge/candidates/MIF_CD74_STRATIFICATION.md`
- `knowledge/candidates/PREGNANCY_REMISSION_AXIS.md`
- `analysis/tier_0_triage/mif_cd74_stratification/REPORT.md`
- `analysis/tier_0_triage/mif_cd74_stratification/residual_evidence.tsv`
- `analysis/tier_0_triage/mif_cd74_stratification/gse282122_remission_interaction/REPORT.md`
- `results/pregnancy_dimension/gse17410_ms_modules/REPORT.md`
- `results/pregnancy_dimension/gse235508_modules/REPORT.md`
- `results/pregnancy_dimension/gse235508_timecourse/REPORT.md`
- `results/pregnancy_dimension/emt12260_ms_tcells/REPORT.md`
- `results/pregnancy_dimension/gse108497_sle/REPORT.md`

## Mechanistic Trace

Working hypothesis:

`MIF`/`CD74` is not a universal inflammatory target in autoimmunity. The viable
V5 version is a stratification hypothesis: a subset of MS lesions or patients
may have persistent `CD74` receptor-state biology coupled to antigen
presentation, lysosomal processing, and APC activation strongly enough to
identify response to a MIF/CD74-axis or APC-state intervention.

Trace:

1. Ligand/receptor level: extracellular `MIF` can signal through `CD74` in
   receptor complexes involving `CD44` and chemokine receptors such as `CXCR4`.
   The V4/V5 operational state is therefore not `CD74` alone, but
   `CD74/CD44/CXCR4` plus HLA-II context.
2. APC program level: `CD74` also functions as invariant chain for MHC-II
   trafficking. In tissue data, a raw `CD74` or MIF/CD74 score can therefore
   reflect generic antigen-presentation load rather than a therapeutically
   separable MIF receptor dependency.
3. Lipid-lysosomal/APC level: the relevant downstream cell state overlaps with
   HLA-II, lysosomal antigen processing, and IFN/APC modules. This is the same
   interpretability problem that caused V4 to require residualization against
   generic IFN/APC and HLA-II.
4. Tissue level in MS: local evidence is strongest in MS white-matter
   microglia. The V4 residual audit found nominal IFN-residual support in
   `GSE111972_white_matter`: residual delta `0.45572407980566854`, Hedges g
   `1.247930189567055`, p `0.007887505384977308`, but residual FDR
   `0.4417003015587293`. This is a real Tier 1 lead, not a validated anchor.
5. Clinical phenotype level: no local dataset yet connects the MS MIF/CD74
   residual state to disability progression, relapse, postpartum flare, or
   treatment response. The current clinical bridge is hypothesized, not shown.

Tier 1 interpretation: the molecule-to-cell part is plausible; the
cell-to-tissue part has nominal MS support; the tissue-to-clinical part is the
main missing link.

## MS-Specific Versus Cross-Disease Pattern

The signal is not cleanly pan-autoimmune.

MS:

- `GSE111972_white_matter` provides the strongest local support: MS
  white-matter microglia retain nominal MIF/CD74 residual signal after IFN
  adjustment, but the residual FDR fails.
- `GSE17410` MS PBMC pregnancy data shows `mif_cd74_receptor_state`
  directionally higher at month 9 versus pre-pregnancy, but not significant:
  delta `0.12194807085829851`, Hedges g `0.6524448023335351`, p
  `0.20974913196132225`. IFN/APC, not MIF/CD74, is the stronger MS pregnancy
  signal in that dataset.
- `E-MTAB-12260` sorted MS T-cell pregnancy RNA-seq does not support a
  pan-lymphocyte MIF/CD74 pregnancy mechanism. Adjusted third-trimester
  MIF/CD74 term versus before pregnancy is negative and non-significant
  (coef `-0.13814738321710288`, p `0.6569105661962384`); postpartum is also
  negative and non-significant (coef `-0.22313938452244758`, p
  `0.28589633708574114`). This argues that any MS pregnancy/PBMC signal is
  more likely monocyte/APC composition or activation than T-cell intrinsic
  MIF/CD74.

RA:

- `GSE235508` seropositive RA shows pregnancy-associated suppression of the
  receptor-state/APC axis: `mif_cd74_receptor_state` pregnancy versus
  nonpregnant/postpartum delta `-0.4850522024358721`, Hedges g
  `-0.5860997928281567`, p `0.006276097402756851`.
- Timecourse analysis shows a late-pregnancy trough and postpartum rebound in
  seropositive RA: T3 - T0 `-0.6424432741594277`; T4 - T3
  `0.5257536055434748`; T5 - T3 `0.7805233800580105`; T6 - T3
  `1.1619638346454728`.
- Disease activity correlation was not significant, so this is a pregnancy
  immune-state observation, not yet a clinical response biomarker.

SLE:

- `GSE108497` uncomplicated SLE shows late-pregnancy MIF/CD74 decrease and
  postpartum rebound directionally similar to RA but weaker: 32-40 weeks versus
  <16 weeks delta `-0.20332580116827784`, p `0.22910979600797657`; postpartum
  versus 32-40 weeks delta `0.3058115266507866`, p `0.07221679931479383`.
- Complicated SLE trends in the opposite direction during late pregnancy:
  32-40 weeks versus <16 weeks delta `0.27474571161497024`, p
  `0.19887004956188656`. This suggests disease-context or complication-context
  modulation, not a universal pregnancy program.

Sjogren, IBD, T1D, psoriasis, thyroid disease:

- The V4 residual audit found only weak Sjogren epithelial residual support
  (p `0.07344896860686509`, residual FDR `0.97363654262921`) and high
  target-vs-IFN coupling (R2 `0.9015149582126574`), making it likely generic
  IFN/HLA-II rather than a separable MIF/CD74 dependency.
- IBD anti-TNF data is conflicted. In `GSE282122`, major monocyte/macrophage
  remission is associated with increased post-treatment MIF/CD74 state:
  adjusted delta `0.4840720173619233`, adjusted p `0.03473492719224309`.
  Lower baseline monocyte/macrophage MIF/CD74 predicts remission in one
  adjusted model (coefficient `-4.088480806349443`, p
  `0.009857151903175113`), but the raw baseline difference is not significant.
- T1D, psoriasis, Crohn/UC, Graves, Hashimoto raw signals mostly collapse after
  IFN residualization in the V4 audit.

Conclusion: the current evidence supports an MS-prioritized stratification
mechanism with RA/SLE pregnancy as useful comparator biology, not a broad
pan-autoimmune target claim.

## Public Datasets Already Present Locally

Datasets that can support or refute the Tier 1 mechanism:

| Dataset / artifact | Disease | Modality | Relevance |
|---|---|---|---|
| `GSE111972_white_matter` via `analysis/tier_0_triage/mif_cd74_stratification/residual_evidence.tsv` | MS | white-matter microglia/spatial or cell-resolved residual audit from V3/V4 | strongest MS tissue anchor; nominal residual support, FDR failure |
| `GSE111972_grey_matter` via same audit | MS | grey-matter microglia residual audit | negative/weak comparator; helps test lesion-compartment specificity |
| `GSE17410` | MS | PBMC expression, pre-pregnancy vs ninth month | natural-experiment MS pregnancy channel; IFN/APC positive, MIF/CD74 weak |
| `E-MTAB-12260` | MS | sorted CD4/CD8 T-cell RNA-seq across pregnancy/postpartum | refutes pan-T-cell intrinsic MIF/CD74 pregnancy mechanism |
| `GSE235508` | RA/SLE/healthy | longitudinal whole-blood pregnancy RNA-seq | seropositive RA pregnancy suppression and postpartum rebound of MIF/CD74/HLA-II axis |
| `GSE108497` | SLE/healthy | longitudinal pregnancy/postpartum whole-blood Illumina array | independent pregnancy/postpartum comparator; complication-stratified SLE behavior |
| `GSE282122` derived pseudobulk | IBD | paired anti-TNF myeloid pseudobulk with remission labels | treatment-response channel; currently directionally conflicted |
| `sjogren_gland_epithelial`, `sjogren_gland_apc` residual audit rows | Sjogren | salivary gland cell-state residual audit | weak cross-disease comparator; likely IFN/HLA-II confounding |
| IBD/T1D/psoriasis/thyroid residual audit rows | multiple autoimmune diseases | cross-disease residual audit | mostly refutes a broad residual MIF/CD74 dependency |

## Tier 1 Assessment

Evidence dimensions currently available:

- Tissue/cell-state residualization: positive nominally in MS white-matter
  microglia, not FDR-stable.
- Natural experiment: pregnancy data supports a related APC/HLA-II/MIF-CD74
  kinetic axis in seropositive RA and SLE; MS PBMC has a divergent IFN/APC
  signal and weak MIF/CD74 signal.
- Treatment-response/perturbation proxy: IBD anti-TNF response is conflicted
  and cannot currently support therapeutic direction.
- Cell-type dissection: MS sorted T-cell pregnancy data argues against a
  T-cell-intrinsic explanation; monocyte/APC-specific testing is still needed.

Tier 1 status from this sidecar: still plausible, but not pass-ready. The
candidate should remain in active Tier 1 until the component-resolved tests
specified below are run. If those fail, demote rather than park.

## Concrete Next Tests

Required before any Tier 2 claim:

1. Component-resolved MS residualization in `GSE111972_white_matter` and
   `GSE111972_grey_matter`: test `CD74` alone, `CD74/CD44/CXCR4`,
   HLA-II-only, and full `mif_cd74_receptor_state`, each residualized against
   IFN/APC and HLA-II where appropriate.
2. Component-resolved pregnancy tests in `GSE17410`, `GSE235508`,
   `GSE108497`, and `E-MTAB-12260`: determine whether the signal follows
   `CD74/CD44/CXCR4`, HLA-II-only, IFN/APC, or monocyte/APC markers.
3. Search local and public progressive-MS/SPRINT-MS-like biospecimen or
   post-hoc biomarker data for a treatment-by-biomarker test. Without clinical
   or treatment interaction, MIF/CD74 remains a biology marker.
4. Perturbation support: find real MIF, CD74, CD44, or CXCR4 perturbation data
   in human monocytes/macrophages/microglia/APCs and ask whether perturbation
   selectively changes lysosomal APC state without simply suppressing broad
   IFN/JAK signaling.

## Kill Criteria

Demote MIF/CD74 if any of the following occur:

1. Component-resolved MS lesion analysis shows the apparent signal is explained
   by HLA-II-only or generic IFN/APC, with no retained `CD74/CD44/CXCR4`
   residual effect in white matter.
2. The MS white-matter residual effect fails in an independent MS lesion,
   CSF, or microglia dataset, or reverses direction after cell-state
   adjustment.
3. Pregnancy datasets show only generic APC/HLA-II kinetics and no reproducible
   MIF/CD74 receptor-state component beyond HLA-II in any disease context.
4. Treatment-response or perturbation data show that lowering the MIF/CD74
   receptor-state worsens resolution programs, or that remission consistently
   requires increased MIF/CD74 state.
5. No public or obtainable dataset can connect the MIF/CD74 residual state to
   MS clinical phenotype, progression, postpartum flare, or treatment response.

If kill criterion 5 is the only failure, the candidate can survive only as a
biomarker-discovery lead, not as a therapeutic mechanism.

