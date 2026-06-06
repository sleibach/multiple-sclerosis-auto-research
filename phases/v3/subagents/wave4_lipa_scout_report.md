# Wave 4 LIPA / Lipid-Lysosomal Central Node Scout

Returned: 2026-05-27

## Bottom line

`LIPA` is not defensible as the V3 central cross-autoimmune node on the current evidence. It is mechanistically attractive for lipid-lysosomal repair biology and is the best of the tested single genes for reviving the original lipid-lysosomal lane after `ACSL1` and `NAMPT` demotion, but the local quantitative signal is compartment-restricted, not myeloid-consistent, not globally FDR-significant, and not genetically anchored across autoimmunity. Apply the pivot criterion: demote `LIPA` as a central node now. Retain it only as a secondary repair-competence / lysosomal lipid-handling marker, especially for T1D ductal/acinar stress, psoriasis keratinocytes, and MS white-matter repair follow-up.

Comparator call:

| Candidate | Current status vs LIPA |
|---|---|
| `CD74` | Broader expression recurrence than `LIPA` but IFN/APC-confounded and prior-art crowded; better state marker, worse lipid-lysosomal central node. |
| `IFI30` | Strong Hashimoto and MS-specific genetics-compatible antigen-processing effector, but IFN/MHC-II rather than lipid-lysosomal; prior-art and directionality risks. |
| `NAMPT` | Stronger IBD metabolic signal than `LIPA`, but IBD-dominant, prior-arted, weak MS/genetic support. |
| `ACSL1` | Mostly IBD/myeloid expression and contradicted by T1D/Sjogren; remains demoted. |
| `LIPA` | Best mechanistic fit to lysosomal lipid handling, but current disease breadth is too thin and contradictory for a central cross-autoimmune target. |

## Evidence for

- Local cross-disease gene summary ranks `LIPA` above `NAMPT` and `ACSL1` on breadth: tested in 6 diseases, trend-or-better in 3 (`Crohn disease`, `psoriasis`, `type 1 diabetes mellitus`), median positive Hedges g 1.559. Source: `results_v3/cross_disease_gene_summary.tsv`.
- Strongest local `LIPA` signals are:
  - T1D pancreatic ductal cells: delta 0.316 donor mean-z, Hedges g 2.606, p=0.00157, FDR=0.175; detection-fraction delta 0.118, p=0.0168. Source: `results_v3/direct_h5ad_gene_replication/direct_h5ad_gene_donor_comparisons.tsv`.
  - Psoriasis keratinocytes: delta 0.304 donor mean-z, Hedges g 3.639, p=0.00722, FDR=0.193; detection-fraction delta 0.109, p=0.0227.
  - Crohn epithelial cells: delta 0.102 donor mean-z, Hedges g 1.362, p=0.0463, FDR=0.272.
  - T1D acinar cells: trend only, delta 0.203, Hedges g 1.559, p=0.0713.
- The broader `lipid_loader_repair` module containing `LIPA` is strong in MS sorted white-matter microglia: delta 0.478 log2 units, Hedges g 1.379, p=0.00528, FDR=0.0192. Source: `results_v3/gse111972_summary.json`.
- Mechanistic external evidence is real. `LIPA` encodes lysosomal acid lipase / cholesteryl ester hydrolase, which hydrolyzes lysosomal cholesteryl esters and triglycerides; see UniProt P38571 (<https://www.uniprot.org/uniprotkb/P38571/entry>) and GeneReviews (<https://www.ncbi.nlm.nih.gov/books/NBK305870/>).
- A 2026 Journal of Neuroinflammation paper directly supports CNS plausibility: LAL/Lipa was reported as a key regulator of GPNMB+ microglial reparative state, myelin-debris digestion, and remyelination in white-matter injury models, with LAL-dependent hydroxypropyl-beta-cyclodextrin effects. Source: <https://link.springer.com/article/10.1186/s12974-026-03782-7>.

## Evidence against/confounders

- No local `LIPA` disease contrast reaches global target-gene FDR. The best p-values are nominal only after broad tracked-gene correction.
- The strongest `LIPA` positives are epithelial/structural compartments, not the original inflammatory myeloid module:
  - T1D ductal/acinar cells and psoriasis keratinocytes support `LIPA`.
  - Psoriasis APC is null.
  - Crohn/UC myeloid compartments are negative.
  - Sjogren APC is negative-trending.
- Myeloid contradiction is the biggest problem. Crohn myeloid `LIPA` mean-z is lower in disease (delta -0.333, p=0.0383), UC myeloid is lower (delta -0.360, p=0.0278), and Sjogren APC trends lower (delta -0.180, p=0.0795). This is incompatible with a central inflammatory myeloid node.
- MS support is module-level, not gene-specific. In GSE111972 white-matter microglia, `LIPA` itself is positive-null only: delta 0.458 log2, Hedges g 0.493, p=0.273, FDR=0.480. Source: `results_v3/gse111972_target_contrasts.tsv`.
- The local cross-disease gene summary masks compartment contradictions because it collapses each disease to supportive calls. Direct compartment-level rows show that `LIPA` is mixed within IBD and negative in several APC/myeloid compartments.
- The genetics subagents explicitly ranked `LIPA` weak as a common-variant autoimmune anchor; no current local genetics output supports pan-autoimmune MR/colocalization for `LIPA`. Sources: `subagents_v3/genetics_james_report.md`, `subagents_v3/wave3_genetics_kierkegaard_report.md`.
- Directionality is unclear but likely opposite of an inflammatory-target inhibition story. LAL deficiency produces lipid accumulation and inflammatory pathology; inhibition would probably worsen lipid handling. Enhancement may be reparative, but the local autoimmune expression signal could simply mark stressed cells trying to clear lipid.
- Sparse single-cell expression is a confounder. The best signals include detection-fraction changes, and low-expression compartments can convert small detection shifts into large standardized effects.
- Psoriasis donor count is only 3 cases and 3 controls. Effect size is high, but population stability is unknown.

## Disease breadth table

Local quantitative evidence only; narrative subagent reports are not counted as direct support.

| Disease | Dataset / compartment | LIPA result | Interpretation |
|---|---|---|---|
| MS | `GSE111972`, sorted white-matter microglia | Gene: delta 0.458, g 0.493, p=0.273, FDR=0.480. Module `lipid_loader_repair`: delta 0.478, g 1.379, p=0.00528, FDR=0.0192. | Supports lipid-loader state, not `LIPA` as the gene-level driver. |
| Crohn disease | IBD h5ad, colon epithelial | Gene: delta 0.102, g 1.362, p=0.0463, FDR=0.272. | Weak epithelial positive. |
| Crohn disease | IBD h5ad, colon myeloid | Gene: delta -0.333, g -1.348, p=0.0383, FDR=0.249. | Against myeloid centrality. |
| Ulcerative colitis | IBD h5ad, colon myeloid | Gene: delta -0.360, g -1.500, p=0.0278, FDR=0.227. | Against myeloid centrality. |
| Ulcerative colitis | IBD h5ad, colon epithelial | Gene: delta 0.0416, p=0.474. | Null. |
| Psoriasis | Skin h5ad, keratinocyte | Gene: delta 0.304, g 3.639, p=0.00722, FDR=0.193. | Compartment-specific positive, small n. |
| Psoriasis | Skin h5ad, APC | Gene: delta -0.015, p=0.886. | Null in APC. |
| Sjogren syndrome | Salivary gland APC | Gene: delta -0.180, g -0.706, p=0.0795, FDR=0.335. | Negative trend. |
| Sjogren syndrome | Salivary epithelial | Gene: delta -0.004, p=0.954. | Null. |
| Type 1 diabetes | Pancreatic ductal cell | Gene: delta 0.316, g 2.606, p=0.00157, FDR=0.175. | Strongest local LIPA compartment. |
| Type 1 diabetes | Pancreatic acinar cell | Gene: delta 0.203, g 1.559, p=0.0713, FDR=0.326. | Positive trend. |
| Type 1 diabetes | Pancreatic beta cell | Gene: delta 0.183, p=0.609. | Null. |
| Hashimoto thyroiditis | `GSE248205` Visium | `LIPA` was not in the thyroid target-gene panel; lysosomal/APC modules were positive. | Missing direct LIPA test; do not count. |

## Mechanistic plausibility

`LIPA` is a plausible biology node, but not yet a central autoimmune node.

Established:

- LAL/LIPA is a lysosomal enzyme for neutral lipid hydrolysis; deficient activity causes lysosomal accumulation of cholesteryl esters/triglycerides and LAL deficiency. Sources: GeneReviews (<https://www.ncbi.nlm.nih.gov/books/NBK305870/>), UniProt (<https://www.uniprot.org/uniprotkb/P38571/entry>).
- LAL deficiency has strong macrophage and inflammatory phenotypes in model systems. Myeloid-specific LAL re-expression corrected multiple inflammatory phenotypes in LAL-deficient mice in published work (<https://pmc.ncbi.nlm.nih.gov/articles/PMC3178672/>).
- LIPA/LAL connects lysosomal cholesterol hydrolysis to efferocytosis and anti-inflammatory oxysterol/LXR biology in macrophages (<https://pmc.ncbi.nlm.nih.gov/articles/PMC6034181/>).
- A recent white-matter injury study argues that LAL-mediated lysosomal cholesteryl ester hydrolysis is required and sufficient for microglial repair/remyelination in mouse models and links this to GPNMB+ microglia and 25-OHC/LXR signaling (<https://link.springer.com/article/10.1186/s12974-026-03782-7>).

Supported by local analysis:

- MS white-matter microglia carry a strong lipid-loader/repair module, but `LIPA` is only a non-significant contributor.
- T1D ductal/acinar and psoriasis keratinocyte `LIPA` signals indicate a recurrent epithelial/structural-cell lipid-lysosomal stress response in some autoimmune tissues.

Assumed / not yet supported:

- That `LIPA` is causal rather than compensatory in human autoimmune tissue.
- That increasing `LIPA` would reduce autoimmune tissue damage outside CNS repair models.
- That the ductal/keratinocyte signal and MS microglial repair biology are the same mechanism.

## Druggability/intervention tractability

`LIPA` is biologically druggable, but not in the usual small-molecule target sense.

- ChEMBL recognizes human lysosomal acid lipase as target `CHEMBL4184` and sebelipase alfa as molecule `CHEMBL3039537`. Local ChEMBL API returned target accession P38571 and molecule metadata: enzyme therapeutic, first approval 2015, max phase 4, parenteral, orphan, not oral, black-box flag. URLs: <https://www.ebi.ac.uk/chembl/explore/target/CHEMBL4184>, <https://www.ebi.ac.uk/chembl/explore/compound/CHEMBL3039537>.
- Sebelipase alfa / Kanuma is an approved IV enzyme replacement therapy for LAL deficiency, not an autoimmune drug. FDA label: <https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/125561s020lbl.pdf>. GeneReviews describes IV sebelipase alfa use for LAL-D (<https://www.ncbi.nlm.nih.gov/books/NBK305870/>).
- Tissue delivery is a major blocker. Systemic enzyme replacement is optimized for LAL-D somatic disease and reticuloendothelial uptake, not CNS microglia, pancreatic ductal cells, or psoriatic keratinocytes. No local or verified source supports adequate CNS target engagement for IV sebelipase in MS lesions.
- Directionality favors enhancement/replacement, not inhibition. `LIPA` loss causes lipid accumulation/inflammation; Lalistat inhibitors are assay tools and inhibition would be a poor autoimmune therapeutic hypothesis. Lalistat-1/2 also have off-target hydrolase effects at common experimental concentrations (<https://pubmed.ncbi.nlm.nih.gov/35504532/>).
- The most plausible intervention class, if this lane survives, is local or cell-targeted LAL enhancement: engineered enzyme delivery, mRNA/LNP, AAV, or an indirect small molecule such as HβCD in CNS white-matter repair. But HβCD/LAL white-matter repair is already published prior art, and none of these modalities is currently supported by V3 autoimmune data.

## Prior-art blockers

Searches checked: PubMed/web queries for `"LIPA" "multiple sclerosis"`, `"lysosomal acid lipase" autoimmune`, `"sebelipase alfa" autoimmune`, `"LIPA" Crohn psoriasis rheumatoid lupus`, ClinicalTrials.gov API queries for `sebelipase alfa autoimmune`, `lysosomal acid lipase autoimmune`, `LIPA multiple sclerosis`, Google Patents queries for `LIPA lysosomal acid lipase autoimmune` and `lysosomal acid lipase multiple sclerosis`.

Blocking / limiting art:

- The direct CNS repair claim is no longer novel: Journal of Neuroinflammation 2026 already reports LAL/Lipa as a key determinant of GPNMB+ microglial white-matter repair and remyelination, including an intervention angle with HβCD (<https://link.springer.com/article/10.1186/s12974-026-03782-7>).
- LAL replacement itself is established for LAL-D: ARISE / NCT01757184 (<https://clinicaltrials.gov/study/NCT01757184>), early sebelipase studies such as NCT01307098 and NCT01371825, FDA label, GeneReviews.
- Patent space exists around LAL-D enzymes/variants/gene therapy, including WO2024254319A1 (<https://patents.google.com/patent/WO2024254319A1/en>) and WO2022122883A1 (<https://patents.google.com/patent/WO2022122883A1/en>). These do not directly block autoimmune use, but they crowd LAL replacement/gene-therapy modalities.
- I found no verified autoimmune clinical trial of sebelipase alfa or direct LIPA augmentation. ClinicalTrials.gov exact query `sebelipase alfa autoimmune` returned zero; `lysosomal acid lipase autoimmune` returned no direct autoimmune LAL intervention trial in the first API results. This is not enough to promote novelty because the local biology is weak.
- LIPA as immunometabolic biology is not novel. Published macrophage/efferocytosis and LAL-deficiency literature already links LAL to inflammatory tissue phenotypes and lipid homeostasis.

Net prior-art assessment: a broad "LIPA/LAL for MS remyelination" claim is blocked. A narrower "cross-autoimmune epithelial/repair-state LIPA biomarker" might be novel, but it is not therapeutically strong enough yet and lacks breadth.

## Exact next falsifying analysis

Run one targeted local analysis before spending more time on LIPA:

1. Build a donor/sample-level table from:
   - `results_v3/direct_h5ad_gene_replication/direct_h5ad_gene_donor_scores.tsv`
   - `results_v3/direct_h5ad_cell_state/direct_h5ad_donor_module_scores.tsv`
   - `results_v3/gse111972_target_contrasts.tsv` / source sample-level expression if available
2. For each compartment where `LIPA` is measured, fit a residual model:
   - `LIPA_mean_z ~ disease + lipid_loader_repair + lysosomal_apc + ifn_apc + log1p(n_cells) + LIPA_detection_fraction`
   - Use donor as the unit. Use HC3 robust SE for small-n compartments.
   - For GSE111972, retain the existing disease/region/age/sex covariate logic and add module residualization if sample-level modules are available.
3. Meta-analyze the adjusted disease coefficient across disease-compartments with a random-effects model, separately for epithelial/structural compartments and myeloid/APC compartments.

Falsification / demotion criteria:

- Immediate full demotion if adjusted `LIPA` disease beta is not positive nominally (p<0.05) in both T1D ductal cells and psoriasis keratinocytes.
- Immediate full demotion if myeloid/APC meta-effect remains negative or the epithelial/structural positive effect is driven by one dataset only.
- To keep LIPA alive as more than a marker, require positive adjusted `LIPA` residuals in at least three diseases, including at least one true myeloid/microglial compartment, and no same-disease opposite-direction myeloid contradiction.

Expected outcome from current data: likely demotion. The observed pattern already looks like two epithelial/structural stress positives plus myeloid negatives, not a central lipid-lysosomal autoimmune node.
