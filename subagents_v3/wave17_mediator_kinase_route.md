# Wave17-A: Mediator kinase / MED16 translational route

Date: 2026-05-27  
Owner: Wave17-A  
Scope: MED16 to CDK8/CDK19/Cyclin C/Mediator kinase intervention only.

## Decision

**PARK.** CDK8/CDK19 inhibition is druggable and has real immune biology, but it should **not** be promoted as a clean translation of the GSE162464 `Med16_KO` phenotype yet.

The central problem is selectivity. `Med16_KO` locally behaves like a strong IFN-gamma-induced CIITA/MHC-II/CD74 suppressor with only modest generic IFN suppression. CDK8/CDK19 inhibition, by contrast, is supported externally as a broader IFN transcriptional dampener, STAT1/IRF1 regulator, IL-10 enhancer, and Treg-skewing intervention. Those are valid immunology routes, but they are not the same claim as MED16-like selective antigen-presentation suppression.

## Local Evidence

The local GSE162464 RNA-seq result is strong for `Med16_KO`:

- `Med16_IFNg_vs_NTC_IFNg` `ciita_mhc2_cd74` module: mean log2FC **-3.74**, median **-3.46**, negative fraction **1.0**.
- `mhc2_surface_core`: mean log2FC **-4.30**.
- Key genes: `Ciita` **-3.34**, `Cd74` **-2.46**, `H2-Aa` **-7.33**, `H2-Ab1` **-4.71**, `H2-Eb1` **-6.25**.
- Generic IFN core: mean log2FC only **-0.46**.

The local GSE162463 CRISPR/FACS screen does **not** support kinase-module genetic phenocopy:

- `Med16`: MHC-II low-vs-high mean log2 **3.31**, rank **42**, 4/4 sgRNAs positive.
- `Cdk19`: mean log2 **1.48**, rank **2231**, not significant.
- `Cdk8`: mean log2 **-0.54**, rank **6636**, not significant.
- `Ccnc`: mean log2 **-0.70**, rank **11553**, not significant.

This is the key internal objection: if CDK8/CDK19/Cyclin C inhibition were a simple MED16 route, at least one of `Cdk8`, `Cdk19`, or `Ccnc` should score more convincingly in the same MHC-II sorting system.

## External Mechanism

CDK8/CDK19 do regulate IFN responses. Bancerek et al. identified CDK8 as a STAT1 S727 kinase and reported that CDK8-mediated STAT1 phosphorylation regulates a large fraction of IFN-gamma-responsive genes in macrophage-relevant systems. Steinparzer et al. later showed CDK8 kinase activity promotes RNAPII pause release after IFN-gamma, with CDK8 and CDK19 having distinct IFN-gamma functions.

That means CDK8/CDK19 inhibition can reduce IFN-gamma-induced transcription. But the mechanism is upstream and broad: STAT1/IRF1 activity, RNAPII pause release, cytokine transcription, splicing, and metabolic effects. In Down syndrome hyperactive IFN models, cortistatin A suppresses IFN-response genes and cytokine programs, again supporting broad IFN antagonism rather than selective CIITA/MHC-II/CD74 gating.

Answer to Q1: **partial resemblance, not enough.** CDK8/CDK19 inhibition can move IFN-gamma-driven antigen-presentation genes downward, but current evidence does not show a MED16-like selective CIITA/MHC-II/CD74 phenotype.

## Autoimmune-Relevant Evidence

There is meaningful non-oncology evidence:

- Activated mouse and human dendritic cells: BRD6989 and other CDK8/CDK19 inhibitors increase IL-10 through AP-1/c-Jun biology.
- T cells: CCT251921 and Senexin A promote Foxp3+ Treg differentiation; CCT251921 ameliorated EAE in mice.
- IBD medicinal chemistry: a CDK8 inhibitor lead, compound 85, increased IL-10 and showed anti-inflammatory activity in an IBD model.
- Down syndrome hyperactive IFN: cortistatin A suppressed pro-inflammatory IFN signaling in lymphoblastoid cells.

Answer to Q2: **yes for autoimmune-relevant cells/models, but not for the exact desired APC antigen-presentation phenotype.**

## Drug And Compound Landscape

Potent tools exist:

- Cortistatin A / dCA: very potent and selective CDK8/CDK19 probe, commonly used around 100 nM in cells.
- CCT251921: CDK8 IC50 about 2.3 nM and CDK19 IC50 about 2.6 nM; oral preclinical probe.
- MSC2530818: CDK8 IC50 about 2.6 nM; CDK8/CDK19 binding around 4 nM; oral preclinical probe.
- BRD6989: weaker CDK8-biased immune tool, useful for IL-10 mechanism, not a development candidate.
- Senexin B / BCD-115: clinical Phase 1 oncology precedent.
- SEL120 / RVU120: oral CDK8/CDK19 inhibitor in oncology/hematology trials, including AML/MDS, solid tumors, lower-risk MDS, and myelofibrosis.

No approved CDK8/CDK19 drug was found. No autoimmune clinical trial was found. No credible tissue-targeted gut, skin, or CNS delivery strategy was found for this route. Current clinical development is systemic oncology/hematology.

Safety is unresolved for chronic autoimmune use. Later work argues the severe toxicity reported for CCT251921 and MSC2530818 did not correlate with CDK8/CDK19 target inhibition and may be off-target. That is useful, but chronic suppression of IFN transcription, cytokine programs, and splicing in non-cancer patients remains a real liability.

## Prior Art

Prior art is a major blocker. US11285144B2 / WO2018027082A1 broadly covers CDK8 inhibitors for inflammation and autoimmune disease, including increasing IL-10 and enhancing Treg differentiation, with a long disease list that includes Crohn disease, ulcerative colitis, multiple sclerosis, type 1 diabetes, psoriasis, Sjogren syndrome, rheumatoid arthritis, and lupus.

This does not necessarily block every possible MED16-like biomarker or tissue-targeted development concept, but it blocks the obvious autoimmune CDK8-inhibitor story. Published IL-10, Treg, IBD, EAE, Down syndrome IFN, and oncology CDK8/CDK19 work further reduces novelty.

Answer to Q4: **yes, broad autoimmune-use prior art is blocking or at least highly constraining.**

## Final Go/No-Go

**PARK, not promote; do not kill.**

Reason to park: the target class is druggable, has human clinical molecules, and has immune-cell evidence. Reason not to promote: the strongest local MED16 result is not phenocopied by local `Cdk8`/`Cdk19`/`Ccnc` perturbation, and external pharmacology is broad IFN/IL-10/Treg rather than selective antigen-presentation suppression.

Promote only if a focused experiment shows low-dose CDK8/CDK19 inhibition in human monocyte-derived macrophages or dendritic cells suppresses `CIITA`, `HLA-DRA/DP/DQ`, `CD74`, and surface HLA-DR with a selectivity ratio comparable to `Med16_KO`, while sparing `STAT1`, `IRF1`, `CXCL10`, `GBP1`, and viability.

## Outputs

- `results_v3/wave17_mediator_kinase_route/local_perturbation_evidence.tsv`
- `results_v3/wave17_mediator_kinase_route/compound_landscape.tsv`
- `results_v3/wave17_mediator_kinase_route/clinical_trials_snapshot.tsv`
- `results_v3/wave17_mediator_kinase_route/prior_art_risk.tsv`
- `results_v3/wave17_mediator_kinase_route/source_bibliography.tsv`
- `results_v3/wave17_mediator_kinase_route/route_verdict.json`

## Key Sources

- Bancerek et al., CDK8/STAT1 IFN mechanism: https://pmc.ncbi.nlm.nih.gov/articles/PMC3580287/
- Steinparzer et al., IFN-gamma Mediator kinase pause release: https://www.sciencedirect.com/science/article/pii/S1097276519305891
- Johannessen et al., CDK8/IL-10 myeloid cells: https://pmc.ncbi.nlm.nih.gov/articles/PMC5693369/
- Cdk8/Cdk19 Treg and EAE evidence: https://pmc.ncbi.nlm.nih.gov/articles/PMC6736578/
- CDK8 inhibitor IBD medicinal chemistry: https://pubs.acs.org/doi/10.1021/acs.jmedchem.2c00356
- Down syndrome hyperactive IFN mediator kinase inhibition: https://pmc.ncbi.nlm.nih.gov/articles/PMC10349994/
- CCT251921 probe profile: https://www.chemicalprobes.org/cct251921
- Cortistatin A probe profile: https://www.chemicalprobes.org/cortistatin
- MSC2530818 probe profile: https://www.chemicalprobes.org/msc2530818
- CDK8/19 toxicity analysis: https://www.mdpi.com/2073-4409/8/11/1413
- Autoimmune CDK8 inhibitor patent: https://patents.google.com/patent/US11285144B2/en
- ClinicalTrials.gov CDK8/CDK19 query: https://clinicaltrials.gov/search?term=CDK8%20CDK19
