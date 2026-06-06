# Wave97 Sidecar: CCL20/CCR6 Mechanistic Directionality Audit

Timestamp: 2026-05-27 21:24 CEST

Scope: focused sidecar on the `CCL20`/`CCR6` axis after Wave97 reopened
`CCL20` as the only residual C15ORF48-proximal candidate. This file does not
claim a V3 finding. It asks whether `CCL20` is upstream, downstream, or
parallel to the `C15ORF48`/MOCCI lipid-lysosomal myeloid state, and whether
blocking the axis would plausibly resolve tissue pathology.

## Short Call

`CCL20` is best interpreted as a downstream or parallel inflammatory chemokine
output of the same NF-kB/TNF/IL-1/IL-17 tissue program that induces
`C15ORF48`, not as a demonstrated upstream controller of the C15ORF48/MOCCI
state. The receptor `CCR6` does not share the local C15 co-state in Wave96,
which supports a source-target split: CCL20 is produced by stressed tissue,
epithelial, stromal, or myeloid compartments, while CCR6 marks recruited
Th17/Treg/B/DC/ILC-like target cells.

Therapeutic implication: CCL20/CCR6 blockade is a plausible anti-trafficking
intervention in IL-17/Th17-rich tissue inflammation, but it is not currently a
defensible intervention point for resolving MS chronic active lesion rims or
the cross-autoimmune lipid-lysosomal myeloid module. It should be used as a
positive-control trafficking axis in C15-state experiments, not promoted as
the central V3 target.

## Local Evidence Read

Primary local files:

- `results_v3/wave20_c15orf48_ndufa4_switch/c15orf48_ndufa4_switch_by_compartment.tsv`
- `results_v3/wave32_resolution_rescue_audit/summary.json`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/REPORT.md`
- `results_v3/wave67_gse282122_myeloid_pseudobulk/REPORT.md`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave71_global_survivor_meta_rank/global_survivor_meta_rank.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
- `results_v3/wave89_psoriasis_gse85034_response/REPORT.md`
- `results_v3/wave94_accessible_state_rerank/*`
- `results_v3/wave96_c15orf48_controller_search/*`
- `results_v3/wave97_c15_residual_costate_falsification/*`
- `subagents_v3/wave97_c15_directionality_sidecar.md`
- `subagents_v3/wave97_c15_prior_art_sidecar.md`

Key local numbers:

- Wave20: the strongest C15ORF48/NDUFA4 switch was in IBD colon myeloid
  compartments. Crohn myeloid had `C15ORF48` delta `3.882`, p `0.000614`,
  `NDUFA4` delta `-0.292`, p `0.0794`, switch delta `4.174`. UC myeloid had
  `C15ORF48` delta `4.446`, p `2.95e-05`, but `NDUFA4` was not reduced.
- Wave39: `CCL20` was accessible/secreted and broad-positive in Crohn disease,
  UC, psoriasis, and T1D, with MS white-matter trend delta `1.147`, p `0.0611`;
  call `PARK_REVIEW`, reason `generic_ifn_cytokine_or_chemokine_axis;
  prior_art_or_trial_saturation`.
- Wave94: `CCL20` ranked as an accessible state candidate but was demoted:
  `NO_GO_ACCESSIBLE_STATE_RERANK`, with blockers `prior_or_class_saturated`,
  `generic_immune_marker`, and `response_direction_conflict`.
- Wave94 context rows: `CCL20` was strong in UC myeloid delta `6.086`,
  Crohn myeloid delta `5.133`, Crohn epithelial delta `1.790`, UC epithelial
  delta `2.072`, T1D ductal delta `3.363`, T1D acinar delta `3.135`, T1D
  endothelial delta `3.795`, psoriasis stromal delta `1.637`, and psoriasis
  keratinocyte trend delta `3.195`.
- Wave94 response rows: RA baseline synovium showed nominal CCL20-high
  anti-TNF nonresponse signal, Hedges g responder-minus-nonresponder `-0.583`,
  p `0.0361`, FDR `0.100`. IBD anti-TNF and psoriasis adalimumab baseline
  response signals were inconsistent or weak.
- Wave96: `CCL20` had 5 C15-trend-positive contexts across 3 diseases, 3
  strict-positive contexts across 3 diseases, 2 myeloid-positive contexts,
  C15-state Pearson r `0.711`, p `0.00204`, and donor-case positive
  correlations in 3 contexts but only 1 disease. `CCR6` had 0 C15-positive
  contexts and no donor co-state.
- Wave96 independent support was incomplete: no direct perturbation support,
  no foundation-model support, no ChEMBL target activity for CCL20, mapped
  autoimmune genetics in 5 diseases but no target-resolved causal package.
- Wave97: after residualizing donor-level pseudo-bulk expression against
  disease status plus generic inflammatory/metabolic covariates, `CCL20` was
  the only reopened candidate. But the residual signal was narrow:
  residual-case positive in 1 context and 1 disease, median residual case
  r `0.188`, residual survival fraction `0.25`, best residual context
  `t1d_acinar_cell` with r `0.963`, p `0.00861`, n `5`.

## Directionality Model

I used four bins:

| Bin | Meaning | Evidence required |
| --- | --- | --- |
| C15-upstream | CCL20/CCR6 signaling induces C15ORF48/MOCCI in source or target cells. | Recombinant CCL20, CCR6+ cells, or CCR6 signaling increases C15ORF48/MOCCI, and blockade prevents it. |
| C15-downstream | C15ORF48/MOCCI controls CCL20 production. | C15ORF48 gain/loss changes CCL20 mRNA/protein after matched cytokine stimulus, independent of generic NF-kB burden. |
| Parallel inflammatory output | CCL20 and C15ORF48 are co-induced by common inflammatory inputs. | Shared induction by TNF/IL-1/IL-17/TLR/IFN; perturbing one does not move the other after input matching. |
| Tissue trafficking amplifier | CCL20 recruits CCR6+ target cells that then maintain inflammatory cytokine loops. | Neutralization reduces CCR6+ cell migration and downstream IL-17/GM-CSF/TNF loops, but not necessarily C15/MOCCI directly. |

Current best fit: `parallel inflammatory output` plus `tissue trafficking
amplifier`. There is not enough evidence for direct C15-upstream or
C15-downstream control.

## Disease-By-Disease Audit

| Disease / tissue | Local CCL20/C15 read | Literature direction | Cell source and target | Does blockade plausibly resolve pathology? | Sidecar call |
| --- | --- | --- | --- | --- | --- |
| MS / brain white matter and EAE gateway | Local MS white-matter trend for CCL20: delta `1.147`, p `0.0611`. CCR6 local C15 co-state absent. No lesion-spatial CCL20-to-C15 result. | EAE work supports CCR6+ Th17 entry through CCL20-expressing choroid plexus, but later EAE work reports CCL20/CCR6 not essential in another model. | Source likely choroid plexus/BBB/tissue stromal or inflamed lesion cells, not proven C15+ rim myeloid. Targets are CCR6+ Th17/Treg/B/DC-like cells. | Low for chronic active lesion resolution. More plausible as an early immune-entry modifier than as a lipid-lysosomal rim repair mechanism. | Parallel/upstream trafficking input; not a C15 controller. |
| RA / synovium | Wave94 nominal baseline anti-TNF nonresponse-high signal, g `-0.583`, p `0.0361`, FDR `0.100`. Wave65 bulk anti-TNF module effects failed specificity gates. | RA literature places CCL20 production in synoviocytes/FLS and synovial inflammation, recruiting CCR6+ Th17 cells. | Sources: FLS/synoviocytes, macrophages, endothelial/stromal cells under IL-1/TNF/IL-17. Targets: CCR6+ Th17 and other mononuclear cells. | Moderate-to-low. May reduce CCR6+ cell influx, but synovial cytokine redundancy is high and local data do not show C15/lipid-lysosomal resolution. | Downstream chemokine plus trafficking amplifier. |
| IBD / Crohn and UC gut | Strongest local C15 and CCL20 overlap. UC myeloid CCL20 delta `6.086`, Crohn myeloid `5.133`; epithelial CCL20 also positive. Wave97 residualization largely attenuated Crohn/UC residual coupling, except UC trend. | IBD literature supports epithelial CCL20 induction, CCR6+ T-cell/DC recruitment, and intrinsic CCR6 signaling in pathogenic Th17-like cells. C15ORF48/miR-147-NDUFA4 is independently reported as a gut epithelial anti-inflammatory metabolic brake. | Sources: colon epithelium and inflamed myeloid/APC compartments. Targets: CCR6+ Th17/Treg/DC/ILC/B cells in mucosa. | Medium biologic plausibility for reducing gut inflammatory trafficking, but not proven to restore the C15/NDUFA4/MOCCI brake or lipid-lysosomal myeloid clearance. Mucosal host-defense/Treg recruitment risk is material. | Best disease for a C15-vs-CCL20 ordering experiment; not yet a target claim. |
| Psoriasis / skin | Wave94 keratinocyte/stromal CCL20 positive/trending, but C15ORF48 was not positive in psoriasis keratinocyte or skin APC; response data did not support CCL20 as adalimumab nonresponse marker. | Strong prior literature: IL-17/TNF/IL-1 induce keratinocyte CCL20, recruiting CCR6+ IL-17-producing cells. | Sources: keratinocytes, fibroblasts, endothelial cells, dendritic cells. Targets: CCR6+ Th17/gamma-delta T/ILC-like cells and DCs. | Plausible anti-inflammatory skin trafficking effect, but prior-arted and not C15-linked. IL-17/TNF/IL-23 biologics already attack the loop more directly. | Established parallel Th17 chemokine loop, not C15/MOCCI mechanism. |
| T1D / pancreatic islet-associated tissue | Wave96/97 residual signal is strongest in T1D tissue-resident compartments, especially acinar/ductal/endothelial. Best residual context: T1D acinar r `0.963`, p `0.00861`, n `5`. | Literature supports inflammatory induction of CCL20 in pancreatic beta/islet contexts and CCR6+ IL-17-associated immune-cell trafficking in diabetes models, but this is less mature than psoriasis/IBD/RA. | Sources likely stressed beta/ductal/acinar/endothelial cells under NF-kB/IL-1. Targets: CCR6+ Th17/iNKT/neutrophil-like or DC/T-cell populations. | Possible early-infiltration prevention hypothesis, but not a current lesion/synovium/gut/skin resolution claim. The n=5 residual signal is fragile. | Interesting tissue-stress co-state; needs replication before intervention work. |
| Sjogren salivary gland | Local CCL20 weak in salivary APC delta `1.021`, p `0.335`; no residual support. | CCR6/CCL20 is broadly reviewed in mucosal/autoimmune trafficking, but no local C15 signal here. | Potential epithelial/APC source, CCR6+ lymphocyte target. | Not supported locally. | No current branch. |

## Mechanistic Interpretation

### Local source-target mismatch

The most important local fact is that ligand and receptor separate:

- `CCL20` is C15-proximal.
- `CCR6` is not C15-proximal: 0 C15-positive contexts, no donor co-state, weak
  MS expression anchor.

This does not refute CCL20/CCR6 biology. It argues that CCL20 mRNA in source
compartments is being captured, while CCR6+ target-cell abundance or activation
is either rare, in a different compartment, or not preserved by the pseudobulk
operationalization. Therefore, a CCL20-C15 correlation cannot be read as
autocrine CCR6 signaling in C15+ myeloid cells.

### Relation to C15ORF48/MOCCI

Published C15ORF48/MOCCI biology supports a compensatory inflammatory brake:
inflammatory signaling can induce C15ORF48; C15ORF48 reduces mitochondrial
activity/ATP, activates AMPK-ULK1 autophagy, increases glutathione-associated
oxidative-stress resistance, and in gut epithelium C15ORF48/miR-147 suppresses
NDUFA4, metabolism, NF-kB activation, and inflammation.

CCL20 biology points the other way: IL-1, TNF, IL-17, TLR, and related NF-kB
inputs induce CCL20, which then recruits CCR6+ immune cells. That makes CCL20
a readout and amplifier of inflammatory tissue state. If C15ORF48 is
functional in the same cell, the most plausible direct relationship is:

`IL-1/TNF/IL-17/NF-kB stimulus -> CCL20 secretion`

and simultaneously:

`IL-1/TNF/IL-17/NF-kB stimulus -> C15ORF48/MOCCI induction -> partial brake on
mitochondrial/NF-kB inflammatory amplification`

Under that model, C15ORF48 might suppress CCL20 indirectly by damping NF-kB,
but local data have not shown that.

## Would Blockade Resolve Tissue Pathology?

### MS lesion rim

Unconvincing. Anti-CCL20 or anti-CCR6 might reduce recruitment of CCR6+ cells
at CNS gateways or acute inflammatory entry points. The V3 lesion problem is
chronic active rim biology: lipid-loaded/lysosomal/APC myeloid dysfunction,
myelin debris handling, oxidative stress, and neurodegeneration. Local data do
not show that CCL20 controls these transitions. A reduction in CCR6+ traffic
would not by itself demonstrate remyelination, lipid clearance, or microglial
resolution.

### RA synovium

Plausible but redundant. CCL20 blockade could reduce CCR6+ Th17/mononuclear
recruitment into inflamed synovium. However, RA synovium has many parallel
chemokine and cytokine circuits. The local anti-TNF baseline association is
nominal and does not survive as a C15 mechanism. The withdrawn GSK3050002 PsA
trial also means clinical feasibility was explored but not proven.

### IBD gut

Most plausible mechanistically, but still not C15-proven. IBD has strong local
CCL20 and C15 overlap in colon myeloid/epithelial contexts, and published
C15ORF48/miR-147-NDUFA4 gut biology makes a real ordering experiment feasible.
But blocking CCL20 could also alter Treg/DC/mucosal defense traffic. The first
question is not "does blockade reduce inflammation"; it is "does CCL20 sit
downstream of a failed C15 brake or merely track epithelial/myeloid NF-kB
burden?"

### Psoriasis skin

Plausible anti-inflammatory effect, not novel and not C15-specific. The
keratinocyte IL-17/TNF -> CCL20 -> CCR6+ Th17 feedback loop is already a
canonical psoriasis mechanism. Local C15ORF48 does not anchor this skin signal.

## Weak Operationalizations Attacked

1. **Wave97 residual survival is too narrow.** `CCL20` survived the residual
   check, but only 1 case context and 1 disease remained positive at case-level
   residualization. The best residual hit is T1D acinar with n `5`, not MS
   lesion myeloid, RA synovium, IBD myeloid, or psoriasis keratinocyte.
2. **Ligand mRNA is not receptor signaling.** CCL20 expression in a source
   compartment does not prove CCR6+ target-cell recruitment, activation, or
   pathological function.
3. **CCR6 local absence cuts against autocrine C15 control.** The receptor did
   not share the C15 state. That can be a sampling problem, but it prevents a
   mechanistic claim.
4. **Mapped genetics are not target-resolved causality.** Wave55/Wave62 mapped
   CCL20/CCR6 autoimmune genetics are not MR/coloc-grade proof that modulating
   CCL20 itself is causal in each disease.
5. **Blocking cell traffic is not resolving lipid-lysosomal dysfunction.**
   A chemotaxis assay can look clean while leaving the C15/NDUFA4 switch,
   lysosomal APC program, lipid loading, ROS, and tissue injury unchanged.
6. **Prior-art is heavy.** Anti-CCL20 antibodies, CCR6 antagonism, autoimmune
   indications, MS/EAE, psoriasis/PsA, RA, and IBD are already in the literature
   and patents. The only remaining novelty delta is C15-state-specific
   directionality, not the therapeutic axis.

## Falsification Experiments

### Experiment 1: Cross-tissue spatial ordering

Question: Are CCL20-producing cells spatially and molecularly upstream of
C15ORF48+ lipid-lysosomal myeloid states, or are both just co-induced by local
inflammation?

Design:

- Tissues: MS chronic active white-matter lesions, RA synovium, inflamed IBD
  colon, psoriasis lesional skin, and T1D pancreas where available.
- Sample size: minimum n=10 donors per tissue/disease, with matched
  non-inflamed/control tissue where possible. For MS, include at least n=10
  chronic active lesions plus n=10 inactive/NAWM regions.
- Assay: multiplex RNAscope or spatial transcriptomics plus IF/IHC for
  `CCL20`, `CCR6`, `C15ORF48`, `NDUFA4`, `IL17A`, `RORC`, `CD3`, `CD68`/`IBA1`,
  `HLA-DRA`, `LAMP3`, epithelial/stromal markers (`EPCAM`, `KRT`, `COL1A1`,
  `PDPN`), and lipid/lysosomal markers where tissue-compatible.
- Primary test: within inflamed regions, fit spatial models asking whether
  CCL20 source-cell abundance/proximity predicts C15ORF48+ myeloid or
  tissue-resident state after adjusting for local IL1/TNF/IL17/NF-kB score.

Falsification rule:

- If CCL20 spatial abundance does not predict C15ORF48+ lipid-lysosomal myeloid
  state after inflammatory covariate adjustment in at least 3 tissues, or if
  CCL20 and C15ORF48 are consistently in separate source cells without
  CCR6+ target-cell proximity, then CCL20 is not a cross-autoimmune C15
  mechanism.

### Experiment 2: C15 perturbation -> CCL20 output

Question: Does C15ORF48/MOCCI directly suppress or induce CCL20?

Design:

- Cells: primary human monocyte-derived macrophages, iPSC microglia, RA FLS,
  colon epithelial organoids, keratinocyte organotypic cultures, and pancreatic
  islet/beta-cell or ductal models if feasible.
- Donors: n=8 healthy donors for macrophage/iPSC-microglia where feasible;
  n=6 disease-derived RA FLS and n=6 IBD organoid donors; technical triplicates.
- Perturbations: CRISPRi/siRNA knockdown and lentiviral or mRNA overexpression
  of `C15ORF48`; matched controls. Stimuli: IL-1beta, TNF, IL-17A/F, IFN-gamma,
  LPS, myelin debris for myeloid/CNS models, and disease-specific cocktails.
- Readouts: CCL20 mRNA, secreted CCL20 protein, C15ORF48 protein, NDUFA4,
  mitochondrial membrane potential, ATP, NF-kB p65 nuclear localization,
  ROS/GSH, lysosomal/APC module markers.

Expected if CCL20 is downstream of the C15 brake:

- C15ORF48 gain should reduce stimulus-induced CCL20 protein by at least 30%
  without global cytotoxicity.
- C15ORF48 loss should increase CCL20 by at least 50% or shift the EC50 of
  cytokine-induced CCL20 lower.
- Effects should remain significant after normalizing for NF-kB nuclear
  localization or upstream cytokine-response intensity.

Falsification rule:

- If C15ORF48 perturbation changes mitochondrial/autophagy readouts but does
  not change CCL20 output by at least 20% in at least two relevant cell systems,
  CCL20 is not a downstream effector of the C15 brake.

### Experiment 3: CCL20/CCR6 blockade -> C15/lipid-lysosomal state resolution

Question: Does blocking CCL20/CCR6 resolve the tissue-damaging state, or only
block chemotaxis?

Design:

- Use tissue-relevant co-cultures:
  - MS-like: human microglia/macrophages plus myelin debris plus autologous
    CCR6+ Th17-polarized cells.
  - RA: FLS/macrophage/CCR6+ Th17 synovial organoid.
  - IBD: colon organoid/myeloid/CCR6+ CD4 T-cell tri-culture.
  - Psoriasis: keratinocyte organotypic skin plus CCR6+ IL-17-producing cells.
- Intervention: anti-CCL20 antibody or CCR6 antagonist versus isotype/vehicle.
- Positive control: IL-17 or TNF pathway blockade appropriate to the tissue.
- Sample size: n=8 donor systems per tissue; predefine primary endpoint per
  tissue.

Primary endpoints:

- CCR6+ cell migration reduction of at least 50% confirms target engagement.
- Tissue/pathology endpoints must include at least 25% reduction in IL-17/TNF/
  IL-1 inflammatory output and at least 20% movement of C15/NDUFA4,
  lipid-lysosomal, ROS, or APC-state readouts toward control.

Falsification rule:

- If anti-CCL20/CCR6 reduces CCR6+ migration but fails to move C15/NDUFA4 or
  lipid-lysosomal/APC injury-state readouts by at least 20%, then the axis is
  a trafficking modifier, not a C15-state therapeutic mechanism.

## Verified Source Anchors

- Reboldi et al., Nat Immunol 2009, PMID `19305396`, DOI
  `10.1038/ni.1716`: CCR6-regulated Th17 entry through CCL20-expressing
  choroid plexus in EAE.
- Sachi et al., Biochem Biophys Res Commun 2023, PMID `36527746`: reports a
  negative/compensability result for CCL20/CCR6 in an EAE model.
- Hirota et al., J Exp Med 2007, PMID `18025126`/PMC `PMC2118525`:
  preferential recruitment of CCR6-expressing Th17 cells to inflamed joints via
  CCL20 in RA and model arthritis.
- Furue et al., Scand J Immunol 2020, PMID `31692008`: review of the
  CCL20/CCR6 axis in psoriasis.
- Homey et al., J Immunol 2000, PMID `10843722`: CCL20 and CCR6 are
  upregulated in psoriasis; keratinocytes, fibroblasts, endothelial cells, and
  DCs can be CCL20 sources under inflammatory mediators.
- Skovdahl et al., Int J Mol Sci 2018, PMC `PMC6214005`: CCL20/CCR6 in UC/CD
  PBMCs and CCL20 link to IL-1beta release.
- Meitei et al., Autoimmun Rev 2021, DOI `10.1016/j.autrev.2021.102846`:
  review of CCR6/CCL20 as an autoimmune therapeutic target in IBD, psoriasis,
  RA, and MS.
- Wasilko et al., Nat Commun 2020, PMC `PMC7295996`, PDB `6WWZ`, EMDB
  `EMD-21950`: 3.3 A cryo-EM structure of human CCR6 bound to CCL20 and Go.
- ClinicalTrials.gov `NCT02671188`: GSK3050002 anti-CCL20 proof-of-mechanism
  PsA trial; withdrawn before treating subjects.
- Google Patents `US8491901B2`: neutralizing anti-CCL20 antibodies with
  autoimmune indications including MS/RA/IBD/psoriasis.
- Xiong et al., PNAS 2024, PMID `38917002`, DOI `10.1073/pnas.2315944121`:
  epithelial C15ORF48/miR-147-NDUFA4 axis as a gut inflammatory/metabolic
  regulator.
- Mitochondrial C15ORF48 autophagy paper, Nat Commun 2024, PMID `38296961`,
  DOI `10.1038/s41467-024-45206-1`: C15ORF48 induces AMPK-ULK1 autophagy,
  glutathione/oxidative-stress resistance, and prevents autoimmunity in mice.

## Bottom Line

Do not promote CCL20/CCR6 as the V3 target. The axis is real, druggable in
principle, and heavily prior-arted, but the local C15-specific evidence supports
only a forcing experiment. The strongest next use is as a positive-control
traffic axis to test whether the C15ORF48/MOCCI brake suppresses inflammatory
chemokine output, especially in IBD gut and T1D tissue-resident contexts.
