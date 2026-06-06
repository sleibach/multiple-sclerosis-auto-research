# Wave56-J SP140 Genetics And Prior-Art Audit

Timestamp: 2026-05-27 11:31 UTC

Scope: targeted audit of whether `SP140` has target-resolved genetic evidence across multiple sclerosis, Crohn disease, ulcerative colitis, psoriasis, rheumatoid arthritis, ankylosing spondylitis, and Sjogren syndrome, and whether SP140 modulation is blocked by existing literature, patent, or clinical prior art.

## Executive Verdict

`SP140` should be demoted as a V3 therapeutic target nomination and retained only as a prior-art-positive mechanistic comparator or genotype-stratification axis.

Reason: the MS/Crohn genetic and mechanistic case is real, but direct SP140 modulation for autoimmune/inflammatory disease is already published and patented. Outside MS/Crohn/IBD, the evidence is mostly locus-level Open Targets/GWAS-prioritization support rather than target-resolved colocalization or Mendelian-randomization-grade causality. The direction is also conflicted: MS/CD risk alleles reduce full-length SP140/protein, while the published small-molecule strategy inhibits SP140 to suppress inflammatory macrophage/DC programs.

## Local V3 Starting Point

From `CONVERGENCE_CHECK_18.md` and Wave55 outputs:

- Wave55 call: `SP140` = `REOPEN_COLOC_OR_PERTURBATION_PRIORITY_ONLY`.
- Passed gates: cross-disease external genetics breadth, MS external genetics anchor, local cell-state replication, early Europe PMC crowding screen.
- Failed gates: coloc/MR-grade target resolution, strict local MS white-matter anchor, real perturbation support, tractable druggability.
- Local Wave55 values:
  - Open Targets genetic diseases >=0.25: `AS;Crohn;MS;Psoriasis;RA;UC`.
  - MS Open Targets genetic score: `0.7593921205206332`.
  - Local positive disease count: `4`, diseases `Crohn disease;Sjogren syndrome;psoriasis;ulcerative colitis`.
  - Local MS white-matter signal: delta `-0.0867628128456026`, p `0.7262224269643743`, FDR `0.9677805697088556`.
  - ChEMBL target: `CHEMBL3108643`; Wave55 found `0` bounded activity rows.

Trace files:

- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_candidate_audit.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/decision_matrix.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/chembl_top_candidate_summary.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/REPORT.md`

## Disease-By-Disease Genetics Audit

| Disease | Evidence found | Target-resolved assessment |
| --- | --- | --- |
| Multiple sclerosis | Strongest support. GWAS Catalog records `rs9989735-C` at `SP140`, p `4e-23`, PMID 24076602, and `rs35540610-C`, p `3e-33`, PMID 31604244. Matesanz et al. 2015 reported the functional `rs28445040` splice mechanism; risk-associated variants correlate with decreased full-length SP140 RNA, increased exon-7-skipped isoform, and allele-dependent lower SP140 protein in PBMCs. | Positive target-resolved functional genetics for MS susceptibility. Not positive for the local V3 MS white-matter lesion state. |
| Crohn disease | Strong support. GWAS Catalog records `rs7423615-T`, p `3e-13`, PMID 21102463; `rs6716753-C`, p `1e-16`, PMID 23128233; and later IBD/CD associations. Mehta et al. 2017 and Amatullah et al. 2022 link CD-associated SP140 variants/loss to altered splicing, lower protein, macrophage dysfunction, topoisomerase dysregulation, microbiota/pathobiont effects, and colitis. | Positive target-resolved functional genetics, strongest in CD among audited diseases. |
| Ulcerative colitis | Open Targets `gwas_credible_sets` query returned one SP140 evidence item for UC, score `0.8679834604263306`, PMID 26974007. Literature and Wave55 local cell-state signal support IBD/UC context. | Weaker than CD. I found no UC-specific SP140 coloc/eQTL paper that resolves SP140 as the causal target independent of the broader IBD locus. |
| Psoriasis | Open Targets `gwas_credible_sets` query returned two SP140 evidence items, scores `0.8512194752693176` and `0.8403971195220947`, PMIDs 26974007 and 40021644. Wave55 local cell-state signal was positive. | Locus/prioritization support only in this audit. No direct SP140 psoriasis eQTL/coloc or perturbation paper found. |
| Rheumatoid arthritis | Wave55 Open Targets associated-target sweep included RA with genetic score `0.5276738774106741`. A direct `gwas_credible_sets` query returned one evidence item, but the PMID was 26974007, a five-disease study not centered on RA, so I do not treat it as RA-specific target resolution. GSK761 paper profiled RA blood SP140 expression, and the patent describes SP140+ inflamed RA synovium. | Not target-resolved. Evidence is insufficient for RA causality. |
| Ankylosing spondylitis | Wave55 Open Targets associated-target sweep included AS with genetic score `0.5276738774106741`; direct `gwas_credible_sets` query returned one item with PMID 26974007. The Ellinghaus five-disease study includes AS, CD, psoriasis, PSC, and UC. | Locus/prioritization support only. No SP140-specific AS eQTL/coloc found. |
| Sjogren syndrome | Wave55 local cell-state signal was positive, but direct Open Targets `gwas_credible_sets` query for `EFO_0000699` returned count `0`. Patent prior art reports SP140+ cells in Sjogren inflamed tissue. | No target-resolved genetic evidence found. |

## Directionality And Cell Specificity

Evidence direction is not clean enough for therapeutic promotion.

- MS direction: Matesanz et al. 2015 supports decreased full-length SP140/protein as the risk mechanism for MS.
- CD direction: Mehta et al. 2017 and Amatullah et al. 2022 support SP140 loss/altered splicing as a macrophage-defect mechanism in Crohn disease.
- Inhibition direction: Ghiboub et al. 2022 shows pharmacologic SP140 inhibition with GSK761 suppresses inflammatory macrophage differentiation and LPS-induced activation, and 2023 DC work supports reduced DC maturation/inflammatory cytokines after GSK761 or siSP140.

Interpretation: SP140 has at least two separable biology modes:

1. `SP140-low/loss-of-function`: genetically supported in MS/CD; linked to defective macrophage identity, antimicrobial defense, topoisomerase de-repression, and microbiota/pathobiont-driven colitis.
2. `SP140-high inflammatory activation`: pharmacologically inhibitable in inflammatory macrophages/DCs; suppresses cytokine and antigen-presentation programs.

These modes may coexist across diseases, but they imply opposite intervention logic. Direct SP140 inhibition could be wrong for patients whose causal mechanism is SP140 loss of function.

## Verified Citations And Links

- Matesanz et al. 2015, "A functional variant that affects exon-skipping and protein expression of SP140 as genetic mechanism predisposing to multiple sclerosis", Human Molecular Genetics. PMID 26152201, DOI 10.1093/hmg/ddv256. Europe PMC: https://europepmc.org/article/MED/26152201
- Karaky et al. 2018, "SP140 regulates the expression of immune-related genes associated with multiple sclerosis and other autoimmune diseases by NF-kB inhibition", Human Molecular Genetics. PMID 30102396, DOI 10.1093/hmg/ddy284. Europe PMC: https://europepmc.org/article/MED/30102396
- Mehta et al. 2017, "Maintenance of macrophage transcriptional programs and intestinal homeostasis by epigenetic reader SP140", Science Immunology. PMID 28783698, DOI 10.1126/sciimmunol.aag3160. Europe PMC: https://europepmc.org/article/MED/28783698
- Amatullah et al. 2022, "Epigenetic reader SP140 loss of function drives Crohn's disease due to uncontrolled macrophage topoisomerases", Cell. PMID 35952671, DOI 10.1016/j.cell.2022.06.048. Europe PMC: https://europepmc.org/article/MED/35952671
- Fraschilla et al. 2022, "Immune chromatin reader SP140 regulates microbiota and risk for inflammatory bowel disease", Cell Host & Microbe. PMID 36130593, DOI 10.1016/j.chom.2022.08.018. Europe PMC: https://europepmc.org/article/MED/36130593
- Ghiboub et al. 2022, "Modulation of macrophage inflammatory function through selective inhibition of the epigenetic reader protein SP140", BMC Biology. PMID 35986286, DOI 10.1186/s12915-022-01380-6. Europe PMC: https://europepmc.org/article/MED/35986286
- Ghiboub et al. 2023, "The Epigenetic Reader Protein SP140 Regulates Dendritic Cell Activation, Maturation and Tolerogenic Potential", Current Issues in Molecular Biology. PMID 37232738, DOI 10.3390/cimb45050269. Europe PMC: https://europepmc.org/article/MED/37232738
- Tamburri et al. 2025, "SP140 represses specific loci by recruiting polycomb repressive complex 2 and NuRD complex", Nucleic Acids Research. PMID 39718989, DOI 10.1093/nar/gkae1215. Europe PMC: https://europepmc.org/article/MED/39718989
- Ellinghaus et al. 2016, "Analysis of five chronic inflammatory diseases identifies 27 new associations and highlights disease-specific patterns at shared loci", Nature Genetics. PMID 26974007, DOI 10.1038/ng.3528. Europe PMC: https://europepmc.org/article/MED/26974007
- Yazar et al. 2021, "The impact of cell type and context-dependent regulatory variants on human immune traits", Genome Biology. PMID 33926512, DOI 10.1186/s13059-021-02334-x. Europe PMC: https://europepmc.org/article/MED/33926512. Relevant point: reports Crohn GWAS colocalization with an SP140 splicing QTL in T cells.
- Chun et al. 2017, "Limited statistical evidence for shared genetic effects of eQTLs and autoimmune-disease-associated loci in three major immune-cell types", Nature Genetics. PMID 28218759, DOI 10.1038/ng.3795. Europe PMC: https://europepmc.org/article/MED/28218759
- International Multiple Sclerosis Genetics Consortium 2013, "Analysis of immune-related loci identifies 48 new susceptibility variants for multiple sclerosis", Nature Genetics. PMID 24076602, DOI 10.1038/ng.2770. Europe PMC: https://europepmc.org/article/MED/24076602
- International Multiple Sclerosis Genetics Consortium 2019, "Multiple sclerosis genomic map implicates peripheral immune cells and microglia in susceptibility", Science. PMID 31604244, DOI 10.1126/science.aav7188. Europe PMC: https://europepmc.org/article/MED/31604244
- Zhou et al. 2025, "GWAS meta-analysis of psoriasis identifies new susceptibility alleles impacting disease mechanisms and therapeutic targets", Nature Communications. PMID 40021644, DOI 10.1038/s41467-025-56719-8. Europe PMC: https://europepmc.org/article/MED/40021644
- Patent prior art: US9018184B2, "Inhibitors of SP140 and their use in therapy", Glaxo Group Ltd, status active, anticipated expiration 2031-11-23 on Google Patents. https://patents.google.com/patent/US9018184B2/en
- Patent family counterpart: EP2643462B1, "Inhibitors of sp140 and their use in therapy", Google Patents. https://patents.google.com/patent/EP2643462B1/en

## Prior-Art Assessment

Direct autoimmune/inflammatory SP140 modulation is not novel.

- The active US patent claims SP140 inhibitors for autoimmune and inflammatory diseases, and its specification explicitly lists or describes multiple conditions overlapping this audit: multiple sclerosis, inflammatory bowel disease including Crohn disease and ulcerative colitis, rheumatoid arthritis, psoriatic arthritis/psoriasis, ankylosing spondylitis, Sjogren syndrome, systemic lupus erythematosus, and type 1 diabetes.
- The 2022 BMC Biology paper describes GSK761 as the first selective small-molecule SP140 inhibitor and concludes that SP140 is a druggable epigenetic therapeutic target for Crohn disease.
- The 2023 dendritic-cell paper extends GSK761/siSP140 immune-modulatory evidence into monocyte-derived DC activation/maturation and tolerogenic potential.
- Commercial reagent pages for GSK761 exist, but I did not use them as primary evidence because the peer-reviewed BMC Biology paper is the verified source.
- ClinicalTrials.gov API searches for `SP140`, `GSK761`, `SP140 Crohn`, and `SP140 autoimmune` found no relevant SP140/GSK761 interventional autoimmune clinical trial. Returned hits were unrelated false positives.

## Explicit Not-Found Searches

Searches were run against Europe PMC, PubMed-indexed records through Europe PMC, ClinicalTrials.gov API, Google Patents, GWAS Catalog REST API, and Open Targets GraphQL.

Not found in this audit:

- `SP140 Crohn disease colocalization eQTL rs7423615`: Europe PMC hitCount `0`.
- `SP140 Sjogren syndrome colocalization eQTL`: Europe PMC hitCount `0`.
- `SP140 psoriasis colocalization eQTL`: Europe PMC hitCount `3`, but no direct SP140 psoriasis target-resolution paper in the returned set.
- `SP140 rheumatoid arthritis colocalization eQTL`: Europe PMC hitCount `7`, but no direct SP140 RA target-resolution paper in the returned set.
- `SP140 ankylosing spondylitis colocalization eQTL`: Europe PMC hitCount `1`, returned an ETS2 macrophage gene-desert paper rather than SP140 target resolution.
- ClinicalTrials.gov `GSK761`: no relevant studies returned.
- ClinicalTrials.gov `SP140 Crohn`: no relevant studies returned.
- GWAS Catalog `rs28445040` autoimmune disease associations: the current direct GWAS Catalog association returned in this audit was eosinophil count, not MS/CD; the autoimmune role of `rs28445040` comes from functional genetic papers rather than the single current GWAS Catalog SNP association endpoint.
- ChEMBL via Wave55: SP140 target found (`CHEMBL3108643`), but no bounded activity rows for SP140 in the local ChEMBL API result.

Found, and therefore novelty-blocking:

- Google Patents `SP140 inhibitor`: US9018184B2 active, broad autoimmune/inflammatory SP140 inhibitor claims.
- Google Patents `SP140 Crohn disease`: same patent family plus peer-reviewed GSK761/Crohn literature.
- Europe PMC/PubMed `SP140 inhibitor Crohn GSK761`: Ghiboub et al. 2022 direct SP140 inhibitor paper.

## Promotion/Demotion Rationale

Demotion criteria met:

1. Prior art blocks novelty for direct SP140 inhibition or generic SP140 modulation in autoimmune disease.
2. Cross-disease breadth is not target-resolved: MS/CD are strong; UC/psoriasis/AS are mostly shared-locus or Open Targets credible-set prioritization; RA and Sjogren are not causally resolved here.
3. The intervention direction is biologically unstable. Genetic risk often points to reduced SP140, while published inhibition suppresses inflammatory programs. Without genotype/cell-state stratification, the same intervention could help one state and harm another.
4. Local V3 MS lesion evidence is near-null and not FDR-supported.
5. No local real perturbation/foundation-model support was available in Wave55 for SP140.

What remains useful:

- `SP140` is a valuable positive-control axis for the broader V3 module because it links immune-restricted chromatin reading, macrophage identity, topoisomerase control, microbiota/pathobiont response, NF-kB/inflammatory regulation, and cross-disease genetics.
- It may still support a stratification hypothesis: SP140-loss genotype or exon-7-skipped isoform status could define a Crohn/MS/IBD subgroup with defective phagocyte antimicrobial programs rather than a generic inflammatory-myeloid excess state.

## Evidence Needed Next

Minimum evidence to revive SP140 as an actionable V3 axis:

1. Colocalization/MR-grade disease genetics across at least four audited diseases using disease GWAS summary statistics and immune-cell eQTL/sQTL data. Required: posterior probability `PP4 >= 0.8` or equivalent fine-mapping colocalization for SP140 expression/splicing, with allele direction reported.
2. Cell-type-specific directionality in monocyte/macrophage, DC, B-cell, and tissue-resident myeloid contexts. Required: risk allele effect on full-length SP140, exon-7 skipping, and protein abundance in each relevant cell state.
3. Genotype-by-perturbation experiment. Required: CRISPR allele editing or donor-genotype stratification for `rs28445040`/linked haplotype; compare SP140 inhibition, SP140 restoration, and TOP1/2 inhibition in macrophages/DCs.
4. Disease-tissue validation beyond IBD. Required: RA synovium, psoriasis skin, AS enthesis/synovium, Sjogren salivary gland, and MS lesion myeloid datasets must show SP140-linked state signal with FDR-supported disease effect and cell-state specificity.
5. Intervention-point resolution that avoids direct prior art. Most plausible route is not "SP140 inhibitor for autoimmunity" but a genotype-specific downstream rescue, e.g. TOP1/2 normalization in SP140-loss phagocytes, with explicit safety because topoisomerase inhibitors are cytotoxic and not trivially translatable.

## Final Call

`SP140` is not "the target" for FINDING_V3. It is too crowded and directionally conflicted for promotion. Keep it as a mechanistically rich comparator and possible stratification marker; move the main discovery track to either a downstream SP140-loss rescue mechanism with cleaner intervention logic or to another lipid-lysosomal myeloid node with less direct prior art.
