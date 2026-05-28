# Wave 5 OSM/OSMR Tissue-Licensing Axis Scout

## Bottom Line

`OSM/OSMR` is a stronger pivot candidate than `LIPA`, residual `CD74/HLA`, or `NAMPT/PDE4` on genetics and translational tractability, but it does **not** currently pass V3 central-node status. The best-supported signal is an IBD-dominant myeloid-to-stromal/epithelial inflammatory tissue-licensing axis: disease myeloid cells express more `OSM`, and epithelial/stromal response surrogates (`STAT3`, `SOCS3`, `JAK1/JAK2`) are elevated in Crohn/UC. However, in the local donor-level h5ad pass, `OSMR` itself is not direction-stable across the analyzed autoimmune compartments, MS-specific evidence is absent or points to potentially protective OSM biology, and IBD prior art is already direct and substantial. Treat `OSM/OSMR` as a high-value IBD/skin tissue-licensing comparator, not as the V3 cross-autoimmune central node.

## Genetics

Local OpenTargets-style table:

- `OSMR` appears with genetic-association evidence in five inflammatory diseases: RA rank 282, Crohn rank 107, UC rank 65, psoriasis rank 172, and ankylosing spondylitis rank 96 in `results_v3/opentargets_candidate_disease_hits.tsv`.
- The genetic-association component is nontrivial: Crohn/UC `0.641`, psoriasis `0.519`, RA/AS `0.511`.
- `OSM` itself is weaker and appears only for Crohn in the local table, mainly through literature/RNA expression rather than genetic association.

Interpretation:

- This is better breadth than `LIPA`, `CD74`, or `NAMPT` in the V3 local target tables.
- It is still not a validated MR/colocalization result. The genetics reports (`subagents_v3/genetics_james_report.md`, `subagents_v3/wave3_genetics_kierkegaard_report.md`) did not promote `OSMR`; they still ranked HLA/MHC and `IRF1/CARINH` as the strongest cross-autoimmune anchors.
- Current genetics supports “OSMR-region disease association exists in several peripheral inflammatory diseases,” not “OSMR is causal across MS plus five autoimmune diseases.”

## Cell-State Evidence

Persisted local evidence:

- `results_v3/direct_h5ad_gene_replication/direct_h5ad_gene_donor_comparisons.tsv` tracks `OSM` but not `OSMR`.
- `OSM` is nominally increased in IBD myeloid compartments:
  - Crohn colon myeloid: delta `0.494`, Hedges g `1.380`, p `0.0382`, FDR `0.249`.
  - UC colon myeloid: delta `0.826`, Hedges g `1.468`, p `0.0357`, FDR `0.244`.
- `OSM` is not broadly positive elsewhere: Sjogren APC trends negative; psoriasis, T1D, and salivary epithelial results are null/weak.

Read-only inline extension across the same h5ad datasets for `OSMR`, `IL6ST`, `LIFR`, `STAT3`, `SOCS3`, `JAK1`, and `JAK2`:

- All queried genes were present in IBD, psoriasis, Sjogren, and T1D h5ad files.
- `OSMR` was only nominally increased in psoriasis keratinocytes: delta `0.461`, Hedges g `1.951`, p `0.0495`, panel FDR `0.328`.
- `OSMR` was weak/null in IBD epithelial, IBD myeloid, psoriasis APC, Sjogren epithelial/APC, and T1D beta/ductal/acinar compartments.
- Downstream response markers were IBD-heavy:
  - `STAT3` UC epithelial: delta `0.467`, Hedges g `4.498`, p `1.77e-05`, panel FDR `0.00311`.
  - `STAT3` Crohn epithelial: delta `0.475`, Hedges g `2.666`, p `0.00113`, panel FDR `0.0662`.
  - `STAT3` UC myeloid: delta `0.316`, p `0.0140`; Crohn myeloid: delta `0.267`, p `0.0269`.
  - `SOCS3` UC myeloid: delta `1.032`, p `0.0123`; Crohn myeloid: delta `0.662`, p `0.0133`.

Interpretation:

- The local h5ad result supports an IBD `OSM -> gp130/JAK/STAT3/SOCS3` inflammatory response lane.
- It does not support `OSMR` as a broad, direction-stable cross-autoimmune cell-state marker.
- The operationalization is imperfect because the current direct h5ad configs emphasize myeloid, epithelial, APC, keratinocyte, and pancreatic compartments. `OSMR` biology is often stromal/fibroblast-like; RA synovial fibroblasts and IBD fibroblast/stromal compartments were not yet quantified. That weakens a no-go conclusion, but it does not justify promotion.
- MS support is currently absent in the local quantitative tables: `OSM/OSMR` do not appear in `results_v3/existing_evidence_candidate_matrix.tsv`, `central_node_first_pass_rank.tsv`, or the MS GSE111972 outputs.

## Perturbation/Drug-Response Evidence

Local perturbation and drug-response evidence:

- `subagents_v3/foundation_hubble_report.md` noted potential LINCS/CMap coverage for `OSMR` perturbation and `OSM` ligand signatures, but no valid OSM/OSMR perturbation branch has been executed.
- Current State outputs remain invalid for named-gene scoring because `adata_real.h5ad` is truncated and State features are anonymous; therefore State cannot support an OSM/OSMR claim.
- Existing L1000FWD top-hit outputs (`results_v3/l1000fwd_reversal_hits.tsv`, `results_v3/l1000fwd_compound_summary.tsv`) contain no useful OSM/OSMR-directed reversal result. The only relevant JAK-like hit is generic (`tozasertib`, listed as JAK inhibitor for the IFN/lysosomal APC query), not OSMR-selective.
- UC tofacitinib response analysis (`results_v3/gse253006_tofacitinib/*`) was weak for the prior IFN/HLA modules and did not test OSM/OSMR directly; it cannot rescue this lane.

Verified external perturbation/trial prior art:

- The primary IBD OSM paper directly reports that OSM drives intestinal inflammation and predicts response to anti-TNF therapy in IBD: West et al., *Nature Medicine* 2017, PMID `28368383`, DOI `10.1038/nm.4307`.
- A 2025 primary IBD paper reports an IL-22/OSM inflammatory axis in intestinal inflammation and tumorigenesis: PMID `40447860`, DOI `10.1038/s41590-025-02149-z`.
- A 2025 PubMed-indexed IBD paper explicitly addresses tissue receptor occupancy for OSMR blockade in IBD: PMID `41867146`.
- Prior anti-OSM clinical development exists in RA: Choy et al., *Annals of the Rheumatic Diseases* 2013, randomized placebo-controlled anti-OSM monoclonal antibody GSK315234 trial, PMID `24286335`, DOI `10.1136/annrheumdis-2013-203523`.

Interpretation:

- Perturbation evidence is presently external/prior-arted, not locally novel.
- Local data do not yet show that suppressing OSM/OSMR reverses the cross-autoimmune lipid-lysosomal/myeloid module.

## Druggability/Intervention

Druggability:

- `OSMR` is a cell-surface cytokine receptor, hence biologically druggable with antibodies.
- Clinical antibody precedent exists. Vixarelimab/KPL-716 is a monoclonal antibody against OSM receptor beta with phase 2a data in prurigo nodularis: PMID `36816342`, DOI `10.1016/j.eclinm.2023.101826`.
- Ligand blockade is also clinically precedented through anti-OSM antibodies, including GSK315234 in RA and GSK2330811 programs in inflammatory/fibrotic disease.

Selectivity and delivery:

- Systemic antibody delivery is feasible for gut, skin, joint, and salivary tissue; CNS delivery is weak.
- OSMR is shared by OSM and IL-31 receptor biology, so blockade can affect inflammatory tissue licensing and itch/epithelial programs. That is tractable but not cleanly selective for the V3 lipid-lysosomal myeloid module.
- CNS/MS feasibility is problematic because peripheral antibody exposure would not reliably engage CNS lesion-rim astrocyte/microglia compartments, and MS literature includes potentially protective OSM activity.

Intervention options:

- Anti-OSM ligand antibody: most direct for IBD OSM-high myeloid ligand state; already prior-arted.
- Anti-OSMR beta antibody: more potent receptor blockade but overlaps IL-31 signaling; prior-arted by vixarelimab/KPL-716 and IBD receptor-occupancy work.
- Downstream JAK/STAT3 modulation: druggable but too broad and already saturated by JAK inhibitor programs.
- Tissue-local delivery in gut/skin could improve safety, but novelty would need a sharply stratified niche, not “OSM/OSMR in autoimmunity.”

## Prior Art

Searches performed:

- PubMed/eutils: `"Oncostatin M" "West" "Nature Medicine" "inflammatory bowel"`, `"OSM" "OSMR" "anti-TNF" "Nature Medicine"`, `"anti-oncostatin M" "rheumatoid arthritis" GSK315234`, `"tissue receptor occupancy" "oncostatin M receptor" inflammatory bowel disease`, `vixarelimab oncostatin M receptor beta phase 2a prurigo nodularis`, `"Dectin-1 limits autoimmune neuroinflammation" Oncostatin M`, `"Oncostatin M-induced astrocytic tissue inhibitor" remyelination`.
- Web/registry/patent searches: `clinical trial anti oncostatin M ulcerative colitis GSK2330811 NCT`, `GSK2330811 Crohn disease oncostatin M phase 2 results`, `Google Patents OSMR autoimmune Crohn psoriasis oncostatin M receptor antibody`, `patent oncostatin M receptor OSMR inflammatory bowel disease antibody`.

Blocking or near-blocking prior art:

- IBD disease mechanism and anti-TNF response stratification are directly published: West et al. 2017, PMID `28368383`.
- IBD OSM/OSMR therapeutic development is already active enough to include receptor-occupancy methodology: PMID `41867146`.
- Anti-OSM antibody has already been tested clinically in RA: Choy et al. 2013, PMID `24286335`.
- Anti-OSMR beta antibody clinical data exist in inflammatory skin/neuroimmune itch context: vixarelimab, PMID `36816342`.
- Patent prior art covers OSMR/OSM-axis antibodies and inflammatory/autoimmune indications; one example is Justia/Google Patents publication `US20220056144A1` on antigen-binding proteins against OSMR with inflammatory disease claims.

MS-specific cautionary prior art:

- OSM is reported in inflammatory brain lesions and affects human cerebral endothelial cells: PMID `11706938`.
- In EAE, Dectin-1-induced OSM promoted myeloid-astrocyte crosstalk and limited autoimmune neuroinflammation: PMID `33581044`, DOI `10.1016/j.immuni.2021.01.004`.
- OSM-induced astrocytic TIMP-1 drove remyelination in a demyelination model: PMID `32071226`, DOI `10.1073/pnas.1912910117`.

Interpretation:

- For IBD, OSM/OSMR is not novel.
- For MS, the therapeutic direction is not obviously blockade; OSMR activation or context-dependent modulation may be protective. That directly conflicts with a broad anti-OSMR cross-autoimmune intervention claim.

## Falsifying Next Analysis

The next decisive analysis should test the actual receptor-bearing stromal/tissue-license compartment, not myeloid ligand alone.

Required analysis:

1. Download and run RA synovium `E-MTAB-8322.project.h5ad` and an IBD stromal/fibroblast-capable dataset.
2. Define an OSMR response module from primary OSM-treated fibroblast/stromal signatures, not ad hoc `STAT3/SOCS3` alone. Minimum genes: `OSMR`, `IL6ST`, `STAT3`, `SOCS3`, `JUNB`, `FOS`, `CXCL1/2/3`, `IL6`, `ICAM1`, `VEGFA`, matrix/remodeling genes, with dataset-specific gene availability recorded.
3. Donor-level test in disease versus control stromal/fibroblast compartments for RA, Crohn, UC, psoriasis skin, Sjogren gland, and MS lesion-associated astrocyte/fibroblast-like/glial compartments if available.
4. Residualize against generic inflammation controls in the same donors: `TNF/NFKB`, `IFN/APC`, myeloid fraction, and tissue damage score.
5. Falsification rule: demote OSM/OSMR permanently if fewer than three diseases show positive OSMR-response residual signal with p <= 0.05 and direction-stable Hedges g >= 0.8, or if MS glial/tissue datasets show opposite/protective OSMR biology relative to the proposed intervention direction.

Useful perturbation follow-up:

- Query LINCS/CLUE or full CMap for `OSMR` knockdown and `OSM` ligand signatures, then test whether the inferred OSMR response is reversed by anti-inflammatory drugs without collapsing into generic JAK inhibition.
- If feasible, use Mixscale/scPerturb only as downstream JAK/STAT comparator, because current Mixscale pathway data do not directly validate OSMR.

## Go/No-Go For V3 Central-Node Status

No-go as a V3 central node now.

Reasons:

- Breadth is insufficient in local expression data: `OSM` is mainly IBD myeloid; `OSMR` is only nominal in psoriasis keratinocytes and not reproduced broadly.
- MS evidence is missing locally and externally ambiguous because OSM can limit EAE neuroinflammation and promote remyelination.
- Perturbation evidence is not locally executed for OSM/OSMR.
- Prior art is heavy in IBD, RA, skin, and OSMR antibody development.
- The best remaining use is as a comparator/pivot: quantify stromal OSMR tissue-licensing in RA/IBD/psoriasis with proper residual controls. Promotion should require stromal-compartment replication plus intervention-direction clarity, not just OpenTargets genetics.
