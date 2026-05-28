# Evidence Dimensions Index

V4 requires at least five orthogonal dimensions for a Tier 4 finding, including
at least one longitudinal or natural-experiment dimension.

| ID | Dimension | Data/source examples | Access status | V3 usage | V4 priority |
|---|---|---|---|---|---|
| D01 | Cross-sectional single-cell/spatial atlases | MS lesions, RA synovium, IBD lamina propria, psoriasis skin, T1D islets, Sjogren gland | local derived/V3 partial | heavy | medium |
| D02 | Genetics and target resolution | Open Targets, GWAS Catalog, FinnGen/OpenGWAS where available, coloc/eQTL/pQTL | local V3 tables plus external as needed | heavy but imperfect | high |
| D03 | Perturbation and foundation-model prediction | CRISPR screens, Mixscape/Mixscale, L1000/CMap, Geneformer-like outputs, State/Stack alternatives | local V3 partial | medium | high |
| D04 | Longitudinal pre-disease cohorts | DoD serum/EBV MS studies, TEDDY T1D, nested IBD/celiac cohorts | V5 scoping started; see `D04_LONGITUDINAL_PRE_DISEASE.md` | minimal | very high |
| D05 | Pregnancy and hormonal natural experiments | `GSE235508` RA/SLE/healthy longitudinal pregnancy blood; `GSE17410` MS pregnancy PBMC; `GSE17449` MS pregnancy-related superseries; `GSE153459` healthy pregnancy CD4 methylation; `GSE122894` pregnant vs non-pregnant EAE TCR-beta repertoire | locally scouted, not downloaded | absent in V3; now first V4 dimensional expansion target | very high |
| D06 | Treatment-resistance phenotyping | progressive MS, anti-TNF-refractory IBD/RA, JAK-refractory psoriasis, remission/nonresponse cohorts | V3 partial for anti-TNF/UC | partial | high |
| D07 | Failed-trial post-hoc evidence | failed MS/IBD/RA/SLE/psoriasis trials as perturbation experiments | not yet structured | minimal | high |
| D08 | Microbiome and metabolite convergence | HMP2, MetaCardis, IBD multi-omics, bile acids, SCFAs, oxylipins | V3 small metabolite/lipid checks | low | high |
| D09 | Infectious triggers beyond EBV | CMV, HHV6, HERVs, SARS-CoV-2, molecular mimicry datasets | not yet structured | low | medium |
| D10 | Immune repertoire and structural antigen biology | iReceptor, VDJdb, McPAS-TCR, pMHC binding, BCR clonotypes | not yet structured | absent | medium |
| D11 | Cross-species comparative perturbation | EAE, DSS colitis, collagen arthritis, NOD mouse, organoids, humanized systems | V3 partial | low | high |
| D12 | Real-world clinical trajectory and comorbidity | UK Biobank, FinnGen endpoints, EHR comorbidity, treatment sequencing | not locally populated | absent | medium |
| D13 | Adjacent-disease bridges | GVHD, checkpoint-induced autoimmunity, autoinflammatory syndromes, pediatric autoimmunity, transplant tolerance | literature only | low | medium |
| D14 | Structural/selectivity/pharmacology | AlphaFold/PDB/ChEMBL/DrugBank/selectivity, CNS exposure | V3 partial | medium | high for Tier 3 |

## Immediate Dimensional Gaps

- D04 and D05 are mandatory priorities because V4 requires longitudinal or
  natural-experiment evidence for Tier 2+.
- D07 can convert failed clinical programs from "negative prior art" into
  mechanistic perturbation evidence.
- D08 may rescue or kill lipid-lysosomal hypotheses more causally than
  cross-sectional transcriptomics.
