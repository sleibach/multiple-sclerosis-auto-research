# Wave86 Sidecar: Prior Art Audit For Anti-TNF Inflammatory Nonresponse

Timestamp: 2026-05-27 CEST

Role: sidecar prior-art scout. This document does not claim a V3 finding and
does not edit analysis code.

## Scope

Question: does Wave85's external anti-TNF nonresponse pattern, especially
baseline mucosal inflammatory/NF-kB and IFN-high signals, contain a gene or
route that is not already covered by prior art?

User-specified genes/routes:

- Inflammatory/NF-kB/myeloid: `OSM`, `TREM1`, `IL1B`, `CXCL8`,
  `CCL2`, `CCL3`, `CCL4`, `TNF`, `NFKBIA`.
- IFN/APC: `STAT1`, `IRF1`, `CXCL10`, `GBP1`, `CD74`, `IFI30`,
  `HLA-DRA`, `HLA-DRB1`, related HLA genes.
- Indications checked: UC, Crohn disease, RA, psoriasis, and MS where
  relevant.

Local artifacts read:

- `results_v3/wave85_external_geo_antitnf_validation/REPORT.md`
- `results_v3/wave85_external_geo_antitnf_validation/external_geo_response_tests.tsv`
- `results_v3/wave85_external_geo_antitnf_validation/external_geo_module_gene_coverage.tsv`
- `results_v3/wave86_external_geo_antitnf_gene_driver/REPORT.md`
- `subagents_v3/wave84_response_dataset_prior_art_scout.md`
- `subagents_v3/wave60q_osm_osmr_circuit_audit.md`
- `subagents_v3/intervention_ohm_report.md`

Internet searches were used for prior-art verification. Key citations and
links are listed inline below.

## Local Pattern Being Audited

Wave85 did not validate the original tissue stratification claim. The primary
endpoint `lysosomal_apc__resid_inflammatory_nfkb` had
`WEAK_EXTERNAL_DIRECTIONAL_SUPPORT_NOT_STRATIFICATION_GRADE`, with independent
overlap-group weighted mean Hedges g `-0.1285`, median AUC `0.4993`, and zero
nominal supportive cohorts.

The signal worth auditing is different: the raw inflammatory and IFN/APC
modules were consistently higher in future nonresponders in baseline mucosal
anti-TNF cohorts.

- `inflammatory_nfkb` was nonresponse-high in all tested Wave85 mucosal
  contexts, with strong rows in all IBD (`g=-1.232`, p `5.47e-06`), Crohn
  colitis (`g=-3.446`, p `8.87e-05`), ACT1 UC (`g=-1.892`,
  p `4.37e-04`), Crohn all (`g=-1.299`, p `6.98e-04`), and Leuven UC
  (`g=-1.177`, p `0.00259`).
- `ifn_apc` and `ifn_lysosomal_apc_composite` were also generally
  nonresponse-high, but the IFN residual over inflammatory/NF-kB was null.
- Wave86 gene decomposition ranked `IL1B`, `CXCL8`, `TREM1`, `CCL4`,
  `CCL3`, `CCL2`, `OSM`, `CXCL10`, `GBP1`, `STAT1`, and `IFI30` as
  nonresponse-high anchors in local mucosal data. `HLA-DPA1` and `HLA-DPB1`
  did not clear gene-level convergence in that report.

Interpretation guardrail: these are baseline response-association signals in
mostly old public mucosal cohorts. They are not target-causal evidence and
they reuse cohorts that are themselves part of the published prior-art
landscape.

## Closest Prior Art

### 1. Mucosal Anti-TNF Response Signatures In UC And Crohn Disease

This route is broadly prior-arted.

- Arijs et al. reported pretreatment mucosal gene signatures predicting
  infliximab response in UC. The Gut paper used baseline active UC colonic
  biopsies and identified a five-gene panel including `TNFRSF11B`, `STC1`,
  `PTGS2`, `IL13RA2`, and `IL11`, with high reported prediction accuracy
  ([Gut 2009 / PMID 19700435](https://gut.bmj.com/content/58/12/1612)).
- Toedter et al. analyzed ACT1 UC mucosal biopsies and found that nonresponders
  did not effectively modulate Th1, Th2, and Th17 pathways after infliximab;
  this is one of the same response contexts Wave85 reuses
  ([PubMed PMID 21448149](https://pubmed.ncbi.nlm.nih.gov/21448149/)).
- Crohn mucosal response work from the Leuven group identified a colonic CD
  infliximab response expression panel including `S100A8`, `S100A9`, `G0S2`,
  `TNFAIP6`, and `IL11`, later supported by genetic follow-up
  ([PMC4539178](https://pmc.ncbi.nlm.nih.gov/articles/PMC4539178/)).
- Verstockt et al. revisited Crohn mucosal anti-TNF nonresponse, validating
  `IL13RA2` and using WGCNA on `GSE16879`; the nonresponse module was enriched
  for TREM1 signaling and had predicted upstream regulators `TNF`, `TGF-beta`,
  and `IL-13`
  ([PMC6849553](https://pmc.ncbi.nlm.nih.gov/articles/PMC6849553/)).

Delta versus Wave85: Wave85 uses a compact inflammatory/NF-kB plus IFN/APC
module rather than the older published panels, and it reorients the signal as
nonresponse-high inflammatory state. That is a useful local decomposition, but
not a new prior-art-clean class.

### 2. OSM / OSMR

This is the strongest direct blocker.

- West et al. showed that inflamed IBD tissue expresses high `OSM` and
  `OSMR`, that stromal cells respond to OSM with inflammatory mediators, that
  OSM blockade attenuated anti-TNF-resistant intestinal inflammation in a
  model, and that high pretreatment mucosal `OSM` was strongly associated with
  anti-TNF failure in more than 200 IBD patients including infliximab and
  golimumab trial cohorts
  ([Nature Medicine 2017, PMID 28368383](https://eprints.gla.ac.uk/198290/)).
- The OSM/OSMR IBD patent estate explicitly claims measuring `OSM`/`OSMR` to
  predict anti-TNF-alpha response and administering OSM/OSMR antagonists for
  chronic intestinal inflammation/IBD
  ([US10822406B2](https://patents.google.com/patent/US10822406B2/en)).
- The anti-OSM Crohn trial `GSK2330811`/COSMIS was withdrawn because of a
  potential narrow therapeutic window, with no subjects enrolled
  ([NCT04151225](https://clinicaltrials.gov/study/NCT04151225)).
- Vixarelimab, an anti-OSMR-beta antibody, was tested in moderate-to-severe UC.
  The Roche participant summary states the phase 2 study stopped early because
  vixarelimab did not work as well as expected and did not show benefit over
  placebo for clinical remission
  ([NCT06137183 / Roche summary](https://forpatients.roche.com/content/dam/patient-platform/lps/global/ga44839/LPS_GA44839_final-results_November2025_English.pdf)).

Delta versus Wave85: none strong enough. Local `OSM` being nonresponse-high is
a replication/stress-test of a published IBD anti-TNF-resistant axis, not a
new route.

### 3. TREM1

This is also heavily blocked, with some tissue/blood direction nuances.

- Verstockt et al. prospectively measured whole-blood `OSM`, `TREM1`, `TNF`,
  and `TNFR2`, and mucosal expression in inflamed biopsies. Low baseline
  whole-blood `TREM1` identified future anti-TNF endoscopic remission; mucosal
  `TREM1` had similar AUC to blood and was anti-TNF-specific versus
  ustekinumab/vedolizumab
  ([PubMed PMID 30685385](https://pubmed.ncbi.nlm.nih.gov/30685385/)).
- Gaujoux et al. performed a cell-centered meta-analysis of colon biopsies.
  They found plasma-cell proportion as a nonresponse biomarker and associated
  inflammatory macrophage programs with `TREM1` and the `CCR2`-`CCL7` axis in
  anti-TNF nonresponders
  ([Gut 2019, DOI 10.1136/gutjnl-2017-315494](https://cris.iucc.ac.il/en/publications/cell-centred-meta-analysis-reveals-baseline-predictors-of-anti-tn/)).
- Prins et al. linked CD14+ monocyte TREM1 levels to impaired anti-TNF-induced
  regulatory macrophage differentiation, decreased autophagy, and Fc-gamma
  receptor activity
  ([Frontiers Immunology 2021](https://www.frontiersin.org/articles/10.3389/fimmu.2021.627535/full)).
- A 2025 translational paper directly reanalyzed `GSE16879`, reported mucosal
  `TREM1` upregulation in infliximab nonresponders, and tested a macrophage
  pyroptosis mechanism in colitis models
  ([Journal of Translational Medicine 2025](https://translational-medicine.biomedcentral.com/articles/10.1186/s12967-025-07304-6)).
- AbbVie acquired Celsius Therapeutics, whose lead asset is `CEL383`, an
  anti-TREM1 antibody for IBD that completed a phase 1 study
  ([AbbVie investor PDF](https://investors.abbvie.com/static-files/c9936258-3a4c-48f0-968b-6d533ead6dee)).

Delta versus Wave85: a local bulk-gene rank can say `TREM1` is one of the
strongest genes in the module, but the biomarker, tissue myeloid biology, Fc
mechanism, and therapeutic antibody route are already occupied.

### 4. IL1B / CXCL8 / CCL2-CCL3-CCL4 / TNF / NFKBIA

This whole class is prior-arted as inflammatory-myeloid/neutrophil burden,
rather than as a clean single-gene target claim.

- Leal et al. identified inflammatory mediators in Crohn patients unresponsive
  to anti-TNF-alpha. Nonresponders maintained increased `IL1B`, `IL17A`, and
  `S100A8`, and the paper pointed to `IL1B`/`IL17A` as potentially relevant
  refractory mucosal targets
  ([PubMed PMID 24700437](https://pubmed.ncbi.nlm.nih.gov/24700437/)).
- Martin et al. identified the GIMATS module in ileal Crohn disease:
  inflammatory mononuclear phagocytes, activated T cells, IgG plasma cells,
  stromal cells, and endothelial cells. The module correlated with failure to
  achieve durable corticosteroid-free remission on anti-TNF therapy, and its
  network includes macrophage `TNF`, `IL1B`, `OSM`, fibroblast `CCL2`/`CCL7`,
  and related chemokine circuits
  ([Cell 2019](https://www.sciencedirect.com/science/article/pii/S0092867419308967)).
- Recent neutrophil/ChemR23 work reported that mucosal neutrophil activation
  and degranulation signatures in pretreatment biopsies were associated with
  anti-TNF and anti-alpha4beta7 nonresponse in IBD
  ([PMC11057782](https://pmc.ncbi.nlm.nih.gov/articles/PMC11057782/)).
- `TNF` and NF-kB pathway variation has also been studied genetically in IBD
  anti-TNF response
  ([PubMed PMID 30811631](https://pubmed.ncbi.nlm.nih.gov/30811631/)).

Delta versus Wave85: Wave86's local rank makes `IL1B`, `CXCL8`, and CCL
chemokines the top gene-level anchors. That is biologically coherent, but it
looks like rediscovery of generic inflammatory burden in the same clinical
problem. `NFKBIA` is less often the named biomarker, but as an inducible NF-kB
feedback gene it does not create a clean new route.

### 5. IFN-High: STAT1 / IRF1 / CXCL10 / GBP1

This class is mixed but still mostly blocked as a broad IFN/JAK/CXCR3 axis.

- IBD IFN biology is well established. CXCL10 is repeatedly reported as
  upregulated in UC/CD mucosa, and biopsy `CXCL10` has been associated with
  secondary loss of response to anti-TNF after initial response
  ([PMC10460912](https://pmc.ncbi.nlm.nih.gov/articles/PMC10460912/)).
- Pediatric IBD anti-TNF transcriptome work reported `GBP1`, `FCGR1A`, and
  `FCGR1B` overexpression in nonresponders two weeks after anti-TNF initiation
  ([PubMed PMID 33429950](https://pubmed.ncbi.nlm.nih.gov/33429950/)).
- Anti-CXCL10/IP-10 has already been tested clinically in UC as eldelumab /
  BMS-936557 / MDX-1100
  ([PubMed PMID 23461895](https://pubmed.ncbi.nlm.nih.gov/23461895/),
  [phase 2b UC PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4946756/)).
- In RA, IFN/TNFi findings are not direction-stable. Wright et al. found
  higher neutrophil IFN-response gene expression correlated with better TNFi
  response ([Rheumatology 2015](https://academic.oup.com/rheumatology/article-pdf/54/1/188/17389103/keu299.pdf)),
  while Iwasaki et al. found higher type I IFN-related gene expression in
  PBMCs of TNFi nonresponders and linked `CXCL10` protein to the type I IFN
  signature
  ([Frontiers Immunology 2022](https://public-pages-files-2025.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2022.901437/pdf)).

Delta versus Wave85: local baseline mucosal `CXCL10`/`GBP1`/`STAT1`
nonresponse-high signal is plausible, but the route is crowded and not
selective. `STAT1`/`IRF1` are pathway regulators, not practical narrow
anti-TNF nonresponse intervention points.

### 6. CD74 / IFI30 / HLA Genes

This class is not as directly blocked in the exact Wave85 nonresponse direction,
but it is not open enough to justify a new branch.

- Wave86 locally found `IFI30` as a nonresponse-high anchor, but the HLA genes
  themselves did not clear gene-level convergence.
- The PANTS Crohn blood transcriptome preprint found baseline MHC, antigen
  presentation, myeloid receptor, and innate modules higher in primary
  anti-TNF responders, not nonresponders. This makes APC/MHC direction
  tissue- and compartment-dependent rather than a clean Wave85 route
  ([medRxiv 2023](https://www.medrxiv.org/content/10.1101/2023.04.19.23288234v1.full-text)).
- Local Wave85 `hla_ii_apc` was nonresponse-high in most mucosal contexts, but
  was not a strong independent result and did not rescue the residualized
  primary endpoint.
- `IFI30`/GILT is intracellular lysosomal biology with poor direct
  intervention tractability; `CD74`/HLA routes are broad APC/MIF/HLA biology
  with substantial safety and prior-art baggage.

Delta versus Wave85: possible residual biomarker work only. It would require a
new independent tissue/cell-resolved anti-TNF cohort and explicit residual
controls for inflammation, IFN, and cell composition. Current evidence does not
merit a new computational branch.

## Disease-Specific Notes

### UC And Crohn Disease

The Wave85/Wave86 pattern is closest to IBD prior art. UC and Crohn already
have:

- pretreatment mucosal infliximab response signatures;
- direct OSM/OSMR anti-TNF failure biology and patent coverage;
- TREM1 tissue/blood anti-TNF biomarker and mechanistic follow-up;
- GIMATS myeloid-stromal anti-TNF resistance biology;
- IL1B/IL17/S100A8 and neutrophil/myeloid nonresponse literature;
- IFN/CXCL10/CXCR3 intervention and biomarker literature.

Therefore IBD is validation context, not a novelty context.

### Rheumatoid Arthritis

RA does not rescue novelty. Dennis et al. showed that baseline synovial
myeloid phenotype was associated with better anti-TNF response, and serum
sICAM1/CXCL13 stratified adalimumab versus tocilizumab response
([PubMed PMID 25167216](https://pubmed.ncbi.nlm.nih.gov/25167216/)).
This is directionally different from Wave85 mucosal IBD inflammatory
nonresponse, and it reinforces that generic myeloid inflammation is
indication- and tissue-dependent.

RA blood anti-TNF classifier work is also substantial
([BMC Medical Genomics 2015](https://bmcmedgenomics.biomedcentral.com/articles/10.1186/s12920-015-0100-6)).
The IFN/TNFi direction is mixed across RA studies, so RA should remain a
specificity guardrail rather than a Wave86 branch.

### Psoriasis

Psoriasis has anti-TNF expression-response prior art, but it is not the closest
fit for Wave85. Etanercept response in psoriasis was linked to suppression of
IL-17 signaling rather than immediate TNF genes
([PMC2852188](https://pmc.ncbi.nlm.nih.gov/articles/PMC2852188/)). Baseline
TNF/CD4 and IFN-gamma signatures have been explored for etanercept response
([PMC3751090](https://pmc.ncbi.nlm.nih.gov/articles/PMC3751090/)). TNF
blockade can also induce paradoxical psoriasis through dysregulated type I IFN
biology
([Nature Communications 2018](https://www.nature.com/articles/s41467-017-02466-4)).

This makes psoriasis useful as an IFN/TNF cautionary comparator, not as a new
anti-TNF nonresponse branch for the mucosal module.

### Multiple Sclerosis

MS is a no-go relevance route for anti-TNF response. In the lenercept phase II
MS trial, TNF neutralization failed to benefit patients and increased
exacerbations versus placebo
([PubMed PMID 10449104](https://pubmed.ncbi.nlm.nih.gov/10449104/)).

Any Wave86 anti-TNF nonresponse biology should not be repurposed as an MS
therapeutic route. At most, MS is a directionality/safety blocker for broad TNF
or TNF-adjacent suppression.

## Bottom-Line Prior-Art Calls

| Route | Local Wave86 support | Closest blocker | Status | New branch? |
| --- | --- | --- | --- | --- |
| `OSM` / `OSMR` | `OSM` nonresponse-high in 4/4 primary mucosal contexts; local rank score high | West 2017 anti-TNF failure, OSM/OSMR patent, anti-OSM Crohn withdrawal, vixarelimab UC futility | `PRIOR_ART_BLOCKED_AS_IBD_STRATIFICATION_AND_TARGET` | No |
| `TREM1` | Top local nonresponse-high gene; 4/4 contexts | Verstockt, Gaujoux, Prins, 2025 IFX/TREM1 paper, CEL383/AbbVie | `PRIOR_ART_BLOCKED_AS_MYLOID_BIOMARKER_AND_TARGET` | No |
| `IL1B` | Top local nonresponse-high gene; 4/4 contexts | Leal refractory Crohn mediators, GIMATS IL1/TNF/OSM macrophage-stromal network | `PRIOR_ART_BLOCKED_AS_REFRACTORY_INFLAMMATORY_MEDIATOR` | No |
| `CXCL8` / neutrophil axis | Top local nonresponse-high gene | neutrophil/myeloid activation nonresponse literature; generic severity confounding | `PRIOR_ART_BLOCKED_AS_INFLAMMATORY_BURDEN` | No |
| `CCL2` / `CCL3` / `CCL4` | Strong local nonresponse-high chemokines | GIMATS `CCL2`/`CCL7` and Gaujoux `CCR2`/chemokine axes | `PRIOR_ART_BLOCKED_AS_MONOCYTE_RECRUITMENT_AXIS` | No |
| `TNF` / `NFKBIA` / NF-kB | Module-level strong nonresponse-high signal | canonical anti-TNF/NF-kB biology, IBD anti-TNF genetic and transcriptomic literature | `GENERIC_CANONICAL_BLOCKED` | No |
| `CXCL10` / CXCR3 | Local IFN/APC gene anchor | IBD CXCL10 response/loss literature and anti-CXCL10 clinical trials | `PRIOR_ART_BLOCKED_AS_IFN_CHEMOKINE_ROUTE` | No |
| `STAT1` / `IRF1` / IFN | Local IFN/APC module nonresponse-high, residual null over inflammation | IFN/JAK/STAT biology saturated; RA TNFi direction inconsistent | `BENCHMARK_ONLY_NOT_NOVEL` | No |
| `GBP1` | Local nonresponse-high and pediatric anti-TNF early nonresponse precedent | pediatric IBD anti-TNF transcriptome | `MOSTLY_BLOCKED_AS_IFN_RESPONSE_MARKER` | No |
| `IFI30` | Local nonresponse-high; better than HLA genes | broad APC/lysosomal prior art; poor direct tractability | `MAYBE_OPEN_AS_RESIDUAL_BIOMARKER_ONLY` | Not now |
| `CD74` / HLA genes | Module-level weak/moderate, HLA gene-level not convergent | MHC/APC response prior art and broad HLA safety/imprecision | `NOT_OPEN_FOR_TARGET_OR_CLASS_CLAIM` | No |

## Recommendation

Do not launch a new computational branch for the broad inflammatory/NF-kB or
IFN-high anti-TNF nonresponse pattern. It is real enough as a local stress-test
signal, but the best genes are the exact genes already present in IBD anti-TNF
nonresponse prior art.

Carry forward only this parked statement:

> Wave85/Wave86 recapitulates a prior-arted baseline mucosal inflammatory
> nonresponse state in anti-TNF-treated IBD, led by `IL1B`, `CXCL8`, `TREM1`,
> CCL chemokines, `OSM`, and IFN/APC genes. It should be used as a guardrail
> and comparator, not as a finding, target claim, or new intervention branch.

The only maybe-open sliver is a future, independent, cell-resolved test of
`IFI30`/CD74/HLA residual APC biology after controlling for inflammatory
NF-kB, IFN, and cell composition. Current Wave85 residual tests and HLA gene
rankings do not justify running that branch now.

