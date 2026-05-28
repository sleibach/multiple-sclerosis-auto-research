# MIF / CD74 Stratification

Status: demoted  
V5 tier: Tier 1 failed  
Last updated: 2026-05-28

## Rationale

V3 repeatedly surfaced MIF/CD74 receptor-state biology, including L1000 module
reversal contexts, but did not mature it as a stratification program.

## V4 Contribution Hypothesis

MS or cross-autoimmune patients with persistent MIF/CD74 APC-state activation
may define a treatment-resistance subgroup rather than a universal target.

## Next Tier 0 Test

Search treatment-resistance and failed-trial post-hoc dimensions for MIF/CD74
state enrichment.

## V4 Tier 0 Audit

Audit completed: `analysis/tier_0_triage/mif_cd74_stratification/decision.json`.

Call: `PARK_TIER0_COMPONENT_AND_TREATMENT_INTERACTION_REQUIRED`.

Result:
- MS white-matter microglia retain nominal IFN-residual support:
  residual delta `0.45572407980566854`, Hedges g `1.247930189567055`,
  p `0.007887505384977308`, residual FDR `0.4417003015587293`.
- Sjogren epithelial residual support is weak: p `0.07344896860686509`,
  residual FDR `0.97363654262921`, and target-vs-IFN R2 `0.9015149582126574`.
- No `mif_cd74_receptor_state` residual test survives FDR `<=0.10`.
- The available local IBD remission interaction table does not test
  `mif_cd74_receptor_state`.

Interpretation: under the V4 prior-art rule, MIF/CD74 is not killed merely
because ibudilast and CD74/MIF prior art exist. The surviving contribution is
narrow: a treatment-by-biomarker or lesion/CSF enrichment test for a
`CD74/CD44/CXCR4/HLA-II` receptor state. The local evidence does not yet
support Tier 1 promotion.

Next valid test: component-resolved residualization (`CD74` alone,
`CD74/CD44/CXCR4`, HLA-II-only, and full module) plus treatment-response or
failed-trial interaction. Do not rerun raw CD74/HLA expression screens.

## GSE282122 Anti-TNF Remission Interaction

Audit completed:
`analysis/tier_0_triage/mif_cd74_stratification/gse282122_remission_interaction/REPORT.md`.

Result:
- Major monocyte/macrophage remission is associated with increased
  post-treatment `mif_cd74_receptor_state`, not decreased: adjusted delta
  `0.4840720173619233`, adjusted p `0.03473492719224309`.
- Lower baseline monocyte/macrophage `mif_cd74_receptor_state` predicts
  remission in one adjusted logit model: coefficient `-4.088480806349443`,
  p `0.009857151903175113`, but raw baseline difference is not significant
  (Hedges g `-0.38734765558900636`, p `0.22965575235386465`).

Interpretation: the treatment-response evidence is conflicted and does not
promote the branch. It remains parked pending component-resolved testing or a
progressive-MS/SPRINT-MS-like treatment-by-biomarker dataset.

## V5 Promotion To Tier 1

V5 instruction ended the repeated parked-state loop. MIF/CD74 was promoted to
Tier 1 for a decisive mechanism test because it has recurred across V3, V4, and
V5 from independent routes.

Sidecar reports:
- `subagents/20260528_202839_mif_cd74_tier1_mechanism.md`
- `subagents/20260528_202906_mif_cd74_orthogonal_evidence.md`

Tier 1 working hypothesis:
MIF/CD74 is viable only as an MS-prioritized stratification mechanism, not as a
pan-autoimmune universal target. The candidate must show a component separable
from generic IFN/HLA-II/APC state and must eventually connect to a treatment or
clinical phenotype.

## V5 MS Component-Resolved Pseudobulk Test

Analysis completed:
`analysis/tier_1_mechanism/mif_cd74_component_ms_pseudobulk/REPORT.md`.

Scope guardrail:
- The local MS pseudobulk table contains `CD74` and HLA-II genes but lacks
  `MIF`, `CD44`, and `CXCR4`. This test can therefore evaluate CD74/HLA-II
  separability, not the full MIF/CD74/CD44/CXCR4 receptor complex.

Result:
- In immune pseudobulk, `CD74` is almost entirely explained by broad APC/size
  covariates (`B_APC`, log nuclei, log library size): covariate R2
  `0.9702062941435217`.
- Immune `CD74` residual active-edge versus control-white-matter contrast is
  not significant: residual delta `0.08093819407908749`, Hedges g
  `1.1187687560796498`, p `0.1834066908183036`, FDR
  `0.7419955642189386`.
- Immune `CD74` residual periplaque versus control-white-matter contrast is
  not significant: residual delta `0.03280611033286629`, p
  `0.4803620508482015`.
- The only nominal positive residual `CD74` rows are in OPC contrasts
  (`inactive_edge_vs_control_wm` and `lesion_core_vs_control_wm`) and do not
  survive FDR. This is not the expected APC/microglia mechanism and should be
  treated as hypothesis-generating at most.

Interpretation:
- This weakens, rather than strengthens, the MS MIF/CD74 mechanism in the
  available lesion pseudobulk data.
- The candidate remains in Tier 1 only because the full receptor complex and
  clinical/treatment interaction have not yet been tested. It is now on a
  narrow survival path: pregnancy or treatment-response component testing must
  show receptor-specific behavior beyond HLA-II/APC, or the candidate should be
  demoted rather than re-parked.

## V5 GSE282122 Component Treatment-Response Test

Analysis completed:
`analysis/tier_1_mechanism/mif_cd74_gse282122_component_response/REPORT.md`.

Scope:
- Hostile-control treatment-response test in anti-TNF-treated IBD myeloid/DC
  data. This is not MS, but it tests whether the candidate behaves like a
  receptor-like `CD74/CD44/CXCR4` component or like generic HLA-II/IFN/APC
  biology.
- Computed component scores directly from local
  `data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad`, then paired
  pre/post anti-TNF samples using the existing GSE282122 paired module metadata.

Result:
- Major monocyte/macrophage `hla_ii_without_cd74` raw remission-associated
  post-treatment delta is positive and FDR-significant: raw delta
  `0.49146107002316664`, Hedges g `0.9957102949370042`, raw p
  `0.0011501724707556477`, raw FDR `0.011501724707556477`, but it loses support
  after IFN/APC adjustment: adjusted delta `0.07146939402819558`, adjusted p
  `0.643745816818418`, adjusted FDR `0.9877812110660807`.
- Major monocyte/macrophage receptor-only `CD74/CD44/CXCR4` raw effect is
  negative: raw delta `-0.23482858080007848`, Hedges g
  `-0.6528959302199949`, raw p `0.038295191538057154`, raw FDR
  `0.09573797884514287`, and disappears after IFN/APC adjustment: adjusted
  delta `0.007376665518260614`, adjusted p `0.9548551706972114`, adjusted FDR
  `0.9877812110660807`.
- Major DC `hla_ii_without_cd74` raw effect is also positive and FDR-significant
  (raw delta `0.2019702828200248`, p `0.007276149452464594`, FDR
  `0.03118349765341969`) but loses support after IFN/APC adjustment
  (adjusted p `0.4408760796062391`).
- No major-cell receptor-only or full MIF/CD74 component has adjusted FDR
  support.

V5 Tier 1 verdict:
- Demoted as a therapeutic mechanism / Tier 2 candidate.
- Reason: the decisive component tests did not show receptor-specific behavior.
  The MS pseudobulk signal collapses into generic APC/HLA-II/size behavior in
  immune cells, and the treatment-response hostile control is driven by
  HLA-II/IFN/APC rather than a retained `CD74/CD44/CXCR4` component.
- Preserved residual value: MIF/CD74 can remain a state readout or exploratory
  stratification biomarker label when explicitly residualized against HLA-II
  and IFN/APC, but it should not consume Tier 2/3 therapeutic resources without
  a new MS clinical-treatment interaction dataset.
