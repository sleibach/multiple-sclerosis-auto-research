# Wave63-X SP140 Topoisomerase Transferability Audit

Timestamp: 2026-05-27

Scope: audit `SP140` loss-of-function, `TOP1`/`TOP2A`/`TOP2B`, topoisomerase rescue, macrophage state, Crohn specificity, MS/psoriasis/RA/other autoimmune transferability, therapeutic window, CNS/tissue feasibility, and prior-art blockage for the V3 autoimmune research session. This is a subagent report, not a final V3 finding.

## Verdict

`DEMOTE_FOR_V3_PROMOTION; PARK_AS_CROHN_SP140_LOF_STRATIFICATION_AND_MECHANISTIC_COMPARATOR`.

The SP140-to-topoisomerase axis is one of the strongest mechanistic stories encountered so far, but it is not a promotable cross-autoimmune therapeutic route. The pro case is real: MS and Crohn have target-resolved or functional SP140 risk evidence, Wave62 upgrades SP140 with MS L2G plus same-target QTL colocalisation, and Cell 2022 shows that SP140 loss in Crohn macrophages dysregulates topoisomerases and can be rescued experimentally by TOP1/TOP2 inhibition. The blockers are stronger: the rescue is Crohn/SP140-loss specific, direct SP140 inhibition is already published and patented for inflammatory disease, TOP1/TOP2 inhibitors have a chronic-autoimmune therapeutic-window problem, local MS lesion evidence is null, and cross-disease transfer beyond IBD is mostly association/cell-state signal without topoisomerase rescue validation.

## Evidence Table

| Question | Evidence | Interpretation |
| --- | --- | --- |
| Is SP140 genetically anchored in MS? | Wave62 Open Targets target-resolution output: `SP140` MS L2G `0.8754889965057373`, MS same-target relevant QTL max `h4=0.9868116204726999`, QTL biosamples include CD14+ classical monocyte, T cell, blood, LCL, naive Treg, and transverse colon. Wave56-J cites Matesanz et al. 2015: MS-associated SP140 variant affects exon skipping/protein expression. | Strong susceptibility anchor, but not a lesion-progression or repair anchor. |
| Is SP140 genetically/mechanistically anchored in Crohn? | Wave62: Crohn L2G `0.8586564660072327`; Wave56-J cites Mehta et al. 2017 and Amatullah et al. 2022 linking Crohn-associated SP140 loss/altered splicing to macrophage dysfunction. | Strongest disease for this axis. Crohn is the lead biological context. |
| Does SP140 replicate locally across autoimmune cell states? | Wave56 local evidence: positive diseases `Crohn disease; Sjogren syndrome; psoriasis; ulcerative colitis`; no local negatives. Broad H5AD row: Crohn myeloid delta `2.4449`, UC myeloid delta `1.9`, Sjogren gland epithelial delta `0.872`, psoriasis keratinocyte delta `0.48`. | Cross-disease expression/cell-state recurrence exists, but compartments are heterogeneous and not all macrophage-specific. |
| Does SP140 replicate in local MS lesion tissue? | Wave56/Wave62 local MS white matter: delta `-0.0867628128456026`, p `0.7262224269643743`, FDR `0.9677805697088556`. | No. This blocks MS therapeutic promotion. |
| Is SP140 part of the lipid-lysosomal myeloid module? | Wave62 `in_lipid_lysosomal_myeloid_neighborhood=False`; residual strict core covariate-surviving disease count `0`. Wave56 residual signal retained only in Crohn myeloid nominal module tests. | SP140 is adjacent to inflammatory/APC macrophage identity, not the resolved central lipid-lysosomal node. |
| What is the topoisomerase rescue claim? | Amatullah et al. 2022 reports that SP140 loss of function drives Crohn disease through uncontrolled macrophage topoisomerases. The study identifies TOP1, TOP2A, and TOP2B as SP140-linked topoisomerase biology and uses topoisomerase inhibition as rescue in SP140-deficient macrophage/colitis systems. | Strong mechanistic proof-of-principle for SP140-loss Crohn macrophages. Not yet evidence for MS, psoriasis, RA, or pan-autoimmune treatment. |
| How do TOP1/TOP2A/TOP2B look locally? | Broad H5AD table: `TOP1` positive in Crohn only; `TOP2A` positive in Crohn, psoriasis, UC and negative in T1D; `TOP2B` no signal. None are in lipid-lysosomal neighborhood. | TOP2A breadth is likely contaminated by proliferation/cell-cycle biology; TOP1 is Crohn-skewed; TOP2B does not support transfer. |
| Does SP140 inhibition rescue the same biology? | Wave56-K parsed Ghiboub et al. 2022 supplement tables. GSK761 suppresses early M1/LPS IFN/NF-kB genes, but not a coherent lipid-lysosomal repair module. At 8 h LPS, lipid-loader genes move in opposing directions. | SP140 inhibition is a different therapeutic logic from SP140-loss/topoisomerase rescue and may be harmful in SP140-low genotypes. |
| Is direct SP140 druggability real? | Wave56-K: SP140 has reader domains and structures; ChEMBL target `CHEMBL3108643` has 61 activity rows, but local records are thermal-shift `Delta Tm`, not bounded nM functional potency. PubChem GSK761 `CID 168007146`: MW `646.8`, XLogP `7`, TPSA `94.5`, rotatable bonds `13`. | Real tool-compound/structure-guided route, weak CNS/lead-like route. |
| Is topoisomerase druggability real? | TOP1/TOP2 inhibitors are clinically druggable oncology mechanisms. Existing rescue tools include topotecan/TOP1 and etoposide/TOP2-class compounds in the literature context. | Druggable in oncology; not automatically feasible for chronic autoimmune use. |
| Therapeutic window | Topotecan and etoposide are cytotoxic topoisomerase agents with severe myelosuppression/secondary malignancy liabilities in prescribing-information class warnings. Broad TOP1/TOP2 poisoning is not macrophage-selective. | Major chronic-autoimmune blocker unless a gut-restricted, macrophage-targeted, non-genotoxic normalization modality is invented. |
| CNS feasibility | GSK761 descriptors are not CNS-lead-like in local PubChem summary. Topoisomerase inhibitors can reach some CNS compartments in oncology settings, but systemic DNA-damage toxicity and lack of microglia-selective target engagement block MS feasibility. | Do not transfer to MS therapy without new chemistry or delivery. |
| Prior art | Direct SP140 inflammatory-disease modulation is published and patented: Ghiboub et al. 2022; Ghiboub et al. 2023; EP2643462B1/US9018184B2. SP140-loss topoisomerase rescue in Crohn is published by Amatullah et al. 2022. | Direct novelty is blocked for SP140 inhibition and for the broad Crohn topoisomerase-rescue concept. |

## Strongest Pro Case

The strongest promotable-adjacent case is a genotype-stratified Crohn mechanism, not a pan-autoimmune target:

1. `SP140` has target-resolved genetic support in MS and Crohn, and supporting target-resolution in psoriasis in Wave62.
2. Crohn has the cleanest causal/mechanistic literature: SP140 loss/altered splicing disrupts macrophage transcriptional identity and host-microbe homeostasis.
3. Amatullah et al. 2022 turns the mechanism into an intervention test: uncontrolled macrophage topoisomerase activity is downstream of SP140 loss, and TOP1/TOP2 inhibition rescues disease-relevant phenotypes in SP140-deficient systems.
4. Local V3 data independently sees SP140 and TOP1/TOP2A signals strongest in IBD compartments, especially Crohn myeloid/epithelial and UC myeloid/epithelial contexts.
5. This provides a useful mechanistic comparator for the broader V3 module: "loss of an immune chromatin reader creates a macrophage dysregulation state that can look inflammatory but requires restoration/rescue, not simple suppression."

If pursued later, the cleanest hypothesis would be: SP140-low Crohn macrophages form a topoisomerase-dependent dysfunctional inflammatory/antimicrobial state that should be treated by genotype-specific downstream normalization, not by generic SP140 inhibition.

## Strongest Blockers

1. **Direction conflict.** Genetic SP140 risk in MS/Crohn points toward reduced full-length SP140 or loss of function. GSK761 inhibits SP140. A patient whose disease is driven by SP140 loss could plausibly be harmed by additional SP140 inhibition.
2. **Crohn specificity.** The topoisomerase-rescue mechanism is demonstrated for SP140-deficient Crohn macrophage/colitis biology. Local TOP1 is Crohn-only; TOP2A is broader but likely confounded by proliferation; TOP2B has no local cross-disease signal.
3. **MS blocker.** Local MS white-matter SP140 signal is null: delta `-0.0868`, p `0.726`, FDR `0.968`. No local evidence shows SP140/TOP rescue in lesion-rim microglia or myelin-debris macrophages.
4. **Psoriasis/RA/Sjogren transfer blocker.** SP140 local/genetic signals exist in psoriasis/Sjogren/RA-adjacent sources, but I found no disease-specific SP140-loss to topoisomerase-rescue chain in those tissues. RA Open Targets support is weaker/shared-locus and not target-resolved enough for this mechanism.
5. **Therapeutic-window blocker.** Current topoisomerase inhibitors are DNA-damage oncology drugs. Chronic autoimmune dosing would need macrophage-selective or gut-restricted target engagement with negligible marrow/genotoxic exposure. No such modality was found locally.
6. **Prior-art blocker.** Direct SP140 inhibition for autoimmune/inflammatory diseases and Crohn-focused SP140 pharmacology are already published/patented. The topoisomerase rescue concept for SP140-loss Crohn is published prior art.

## Disease Transferability Assessment

| Disease | Transferability call | Rationale |
| --- | --- | --- |
| Crohn disease | `SUPPORTED_MECHANISM_PARKED` | Strongest genetics/mechanism; published SP140-loss/topoisomerase rescue; local SP140 and TOP1/TOP2A IBD signal. Blocked as novel target by prior art and therapeutic-window constraints. |
| Ulcerative colitis | `PARTIAL_IBD_TRANSFER` | Local SP140/UC myeloid and TOP2A/UC epithelial signals exist; Open Targets SP140 UC support exists, but UC-specific SP140-loss/topoisomerase rescue is not established. |
| Multiple sclerosis | `NO_GO_FOR_THERAPEUTIC_TRANSFER` | Susceptibility genetics are strong, but local lesion tissue signal is null and no CNS macrophage/microglia topoisomerase-rescue evidence was found. |
| Psoriasis | `ASSOCIATION_ONLY` | Wave62 supports SP140 L2G/QTL; local psoriasis keratinocyte and TOP2A skin/stromal signals exist. Mechanistic chain is not macrophage-rescue-like and TOP2A may be proliferation. |
| Rheumatoid arthritis | `WEAK_TRANSFER` | Prior reports/patent mention SP140+ inflamed RA tissue and Wave55 had RA Open Targets genetics, but target-resolved RA causality and topoisomerase rescue are not established here. |
| Sjogren syndrome | `CELL_STATE_ONLY` | Local SP140 signal exists in gland epithelial compartment; no target-resolved genetics or topoisomerase rescue chain. |
| AS/SLE/T1D/celiac/PBC/AITD | `NO_PROMOTION` | No sufficient SP140-loss/topoisomerase-rescue chain in current local artifacts. |

## Exact Citations And Queries

Verified citations used from local Wave56/Wave62 artifacts and web checks:

- Matesanz et al. 2015, "A functional variant that affects exon-skipping and protein expression of SP140 as genetic mechanism predisposing to multiple sclerosis", Human Molecular Genetics. PMID `26152201`, DOI `10.1093/hmg/ddv256`.
- Karaky et al. 2018, "SP140 regulates the expression of immune-related genes associated with multiple sclerosis and other autoimmune diseases by NF-kB inhibition", Human Molecular Genetics. PMID `30102396`, DOI `10.1093/hmg/ddy284`.
- Mehta et al. 2017, "Maintenance of macrophage transcriptional programs and intestinal homeostasis by epigenetic reader SP140", Science Immunology. PMID `28783698`, DOI `10.1126/sciimmunol.aag3160`.
- Amatullah et al. 2022, "Epigenetic reader SP140 loss of function drives Crohn's disease due to uncontrolled macrophage topoisomerases", Cell. PMID `35952671`, DOI `10.1016/j.cell.2022.06.048`.
- Fraschilla et al. 2022, "Immune chromatin reader SP140 regulates microbiota and risk for inflammatory bowel disease", Cell Host & Microbe. PMID `36130593`, DOI `10.1016/j.chom.2022.08.018`.
- Ghiboub et al. 2022, "Modulation of macrophage inflammatory function through selective inhibition of the epigenetic reader protein SP140", BMC Biology. PMID `35986286`, DOI `10.1186/s12915-022-01380-6`.
- Ghiboub et al. 2023, "The Epigenetic Reader Protein SP140 Regulates Dendritic Cell Activation, Maturation and Tolerogenic Potential", Current Issues in Molecular Biology. PMID `37232738`, DOI `10.3390/cimb45050269`.
- Yazar et al. 2021, "The impact of cell type and context-dependent regulatory variants on human immune traits", Genome Biology. PMID `33926512`, DOI `10.1186/s13059-021-02334-x`.
- Patent prior art: EP2643462B1 and US9018184B2, "Inhibitors of SP140 and their use in therapy", Glaxo Group Ltd.

Web queries run during this subagent audit:

- `Amatullah 2022 SP140 loss of function uncontrolled macrophage topoisomerases Crohn disease TOP1 TOP2A TOP2B rescue`
- `SP140 loss of function topoisomerase inhibitors rescue macrophage Crohn TOP1 TOP2A TOP2B`
- `GSK761 SP140 inhibitor macrophage inflammatory function Crohn Ghiboub 2022 BMC Biology`
- `Google Patents SP140 topoisomerase Crohn topotecan etoposide`
- `patent SP140 topoisomerase inhibitors Crohn disease`
- `SP140 TOP1 TOP2 inhibitors Crohn patent topotecan etoposide`
- `US9018184B2 Inhibitors of SP140 and their use in therapy Google Patents`
- `DailyMed etoposide injection secondary leukemia severe myelosuppression`
- `Pfizer topotecan hydrochloride prescribing information severe myelosuppression`
- `topotecan central nervous system penetration brain ECF less than plasma mice`

Local artifact queries/checks:

- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave62_opentargets_target_resolution/opentargets_l2g_rows.tsv`
- `results_v3/wave62_opentargets_target_resolution/opentargets_qtl_coloc_rows.tsv`
- `results_v3/wave56_sp140_targeted_reopener_audit/REPORT.md`
- `results_v3/wave56k_sp140_perturbation_druggability/gsk761_sp140_supplement_module_summary.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
- `subagents_v3/wave56j_sp140_genetics_prior_art.md`
- `subagents_v3/wave56k_sp140_perturbation_druggability.md`
- `subagents_v3/wave62v_opentargets_target_resolution.md`

## Promotion/Demotion Decision

Do not promote `SP140`, `TOP1`, `TOP2A`, `TOP2B`, or generic topoisomerase rescue as the V3 cross-autoimmune therapeutic finding.

Park the axis for two narrower uses:

1. **Comparator:** SP140 is a positive-control example of strong disease genetics plus macrophage epigenetic mechanism that still fails therapeutic promotion after directionality, local MS, novelty, and safety gates.
2. **Future Crohn stratification experiment:** In SP140-risk/low-expression Crohn donors, compare SP140 restoration, GSK761/SP140 inhibition, TOP1 inhibition, TOP2 inhibition, and inactive analogs in primary macrophages under microbial/LPS/IFNG/TNF stimulation. The route is falsified if TOP rescue does not improve antimicrobial/inflammatory transcriptomic defects by at least 30% without viability, DNA-damage, or efferocytosis penalties.

Operational recommendation to the orchestrator: use SP140/TOP biology to sharpen the "rescue versus suppression" decision rule for chromatin-risk macrophage states, but do not spend another V3 promotion cycle trying to convert it into a pan-autoimmune or MS treatment claim.
