# Wave58-N IL7R Therapeutic Reopener Audit

Timestamp: 2026-05-27 12:25 UTC

## Verdict

`DEMOTE_NO_GO_V3_PRIOR_ART_AND_SURROGATE`.

`IL7R/CD127` is real autoimmune biology and a useful positive-control axis, but it should not be promoted as the V3 cross-autoimmune lipid-lysosomal myeloid-module intervention. The best reframe is not "generic T-cell survival"; it is a narrower `rs6897932 -> soluble/surface IL7R -> IL-7-amplified monocyte/APC and memory-T-cell circuit`. That reframe is biologically plausible and partly published, but it fails the V3 bar because local MS tissue support is null, the foundation-model signal is single-context and small, no V3 coloc/MR-grade causal direction is available, and the therapeutic/prior-art space is already crowded by anti-CD127 antibodies, IL7R-splicing ASOs, and IL7R-modulator biomarker patents.

## Local V3 Evidence Checked

- Wave57 reopened `IL7R` only as model-supported triage, not as a finding. In `results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv`, `IL7R` had one strong Geneformer support context out of 11 tested: `ra_myeloid_dendritic`, 12/24 disease cells with the token, cosine-shift z `0.529`, projection-minus-random `0.0318`, model priority score `7.25`.
- The same Wave57 row had Open Targets genetics breadth in seven diseases: `AITD;Crohn;MS;PBC;Psoriasis;SLE;T1D`, with MS genetic association score `0.7886`, but strict local MS white-matter support failed: delta `-0.6537`, p `0.5725`, FDR `0.9432`.
- Wave55 had already classified `IL7R` as `NO_GO_EXTERNAL_GENETICS_SWEEP`: Open Targets breadth and MS association passed, but coloc/MR-grade target resolution was not run, strict local MS anchor failed, real perturbation support failed, druggability as small-molecule ChEMBL activity failed, and literature saturation failed novelty. See `results_v3/wave55_external_genetics_druggability_sweep/REPORT.md`.
- Wave37 efferocytosis CRISPR screen did not support a phagocytosis/efferocytosis mechanism: `IL7R` median efficient-minus-noneater logFC `-0.1554`, contrast FDR `1.0`, screen call `UNRESOLVED` in `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`.
- Earlier Wave18 foundation rescue ranked `IL7R` `do_not_promote`; token coverage was absent in most disease-cell contexts and positive shifts were weak/mixed. Wave57 improves the RA dendritic context but does not overturn the pattern.

## Genetics And Direction

Positive:

- The MS genetic axis is not speculative. The IL7R exon 6/splicing mechanism around `rs6897932` is established enough to be therapeutic prior art. Galarza-Munoz et al. report that the MS risk allele enhances exon 6 exclusion, increases soluble IL7R, and that anti-sIL7R ASOs can correct the risk-allele splicing phenotype in human CD4+ T cells. Source: Europe PMC PMID `35613883`, DOI `10.1261/rna.079137.122`, https://europepmc.org/article/MED/35613883.
- A non-lymphoid bridge exists: Al-Mossawi et al. showed that LPS markedly induces monocyte surface and soluble IL7R, that both associate with `rs6897932`, and that synovial fluid monocytes from spondyloarthritis patients are enriched for IL7R+ cells with an IL-7-related transcriptional profile. Source: Europe PMC PMID `31594933`, DOI `10.1038/s41467-019-12393-1`, https://europepmc.org/article/MED/31594933.

Negative:

- V3 does not have coloc/MR-grade direction for `IL7R` across the five-plus-disease cluster. The Open Targets evidence is associated-target support, not a proof that IL7R expression/protein level causally drives each disease.
- The cross-disease direction is not uniformly target-actionable. For MS, the strongest causal story points to soluble IL7R splicing and T-cell expansion; for monocytes, the strongest data are LPS/spondyloarthritis context. That is not yet the same as the V3 lipid-lysosomal myeloid lesion/synovium/gut/skin module.

## Cell And Tissue Reframe

The only defensible V3-compatible reframe is:

`rs6897932/high sIL7R or inducible surface IL7R -> IL-7-amplified inflammatory monocyte/APC state -> increased HLA-II/APC and phagocytic inflammatory crosstalk with memory T cells`.

This is mechanistically sharper than generic T-cell survival, but current evidence is insufficient:

- Local single-cell/foundation support is concentrated in one RA myeloid-dendritic context. `IL7R` had zero Geneformer token coverage in Wave57 IBD myeloid, psoriasis macrophage, psoriasis dendritic, Sjogren APC, T1D ductal/acinar, and RA nonclassical monocyte contexts.
- Local disease recurrence is stronger in IBD/T1D/UC than MS. That makes UC or SpA a plausible lead for existing IL7R programs, not a new MS-centered lipid-lysosomal target nomination.
- The APC mechanism remains a coupled lymphoid-myeloid circuit. The public monocyte evidence does not show that direct IL7R blockade in purified APCs reverses the V3 lipid-lysosomal module independently of T cells.

## Therapeutics, Trials, And Safety

Anti-CD127/IL7R blockade is clinically real and already tested across the relevant disease space:

- `PF-06342674/RN168` in T1D: Phase 1b, 37 subjects, near-complete receptor occupancy and pSTAT5 inhibition at >=1 mg/kg every other week; reduced effector/central memory T cells; most adverse events mild, but four subjects became anti-EBV IgG+ and two had active-infection symptoms. Source: Europe PMC PMID `31852846`, DOI `10.1172/jci.insight.126054`, https://europepmc.org/article/MED/31852846; trial `NCT02038764`, https://clinicaltrials.gov/study/NCT02038764.
- `PF-06342674/RN168` in MS: Phase 1b MS trial `NCT02045732`, terminated, actual enrollment 4, https://clinicaltrials.gov/study/NCT02045732. The registry explicitly frames PF-06342674 as an IL7R-blocking antibody being developed for MS.
- `GSK2618960` healthy-volunteer study: Phase 1, 18 subjects, >95% receptor occupancy, IL-7-mediated STAT5 inhibition, no serious/significant adverse events, but persistent anti-drug antibodies in 11/12 treated subjects and neutralizing antibodies in 7/12. Source: Europe PMC PMID `30161291`, DOI `10.1111/bcp.13748`, https://europepmc.org/article/MED/30161291; trial `NCT02293161`, https://clinicaltrials.gov/study/NCT02293161.
- `GSK2618960` in RRMS: trial `NCT01808482`, terminated, actual enrollment 16, https://clinicaltrials.gov/study/NCT01808482. `GSK2618960` in primary Sjogren's syndrome: `NCT03239600`, withdrawn, actual enrollment 0, https://clinicaltrials.gov/study/NCT03239600.
- `OSE-127/lusvertikimab/S95011`: Phase 1 healthy-subject study, 63 subjects, strict noncytotoxic IL7R antagonist, peripheral IL-7 pathway inhibition without significant lymphopenia or serious adverse events. Source: Europe PMC PMID `36734626`, DOI `10.4049/jimmunol.2200635`, https://europepmc.org/article/MED/36734626; trial `NCT03980080`, https://clinicaltrials.gov/study/NCT03980080.
- `OSE-127/lusvertikimab` in UC: Phase 2 `NCT04882007`, completed, actual enrollment 136, https://clinicaltrials.gov/study/NCT04882007. ECCO/JCC abstract reports clinical, endoscopic, and histologic efficacy signals; this strengthens the target class but weakens novelty. Source: DOI `10.1093/ecco-jcc/jjae190.0036`, https://academic.oup.com/ecco-jcc/article/19/Supplement_1/i71/7966890.
- `S95011/lusvertikimab` in primary Sjogren's: Phase 2 `NCT04605978`, completed, actual enrollment 48, https://clinicaltrials.gov/study/NCT04605978.
- Safety ceiling is biologically credible: inherited IL7R defects cause T-cell immunodeficiency/SCID, so chronic or high-grade blockade has a plausible infection and immune-reconstitution liability even if current antibodies avoid acute lymphopenia. Source example: PubMed `11023514`, https://pubmed.ncbi.nlm.nih.gov/11023514/.

## Patent And Prior-Art Audit

Blocking or crowding prior art is substantial:

- OSE Immunotherapeutics CD127 antibodies: `US20170129959A1` / granted `US10428152B2`, active patent family, "Antibodies Directed Against CD127", OSE assignee, broad inflammatory/immunological classifications. Source: https://patents.google.com/patent/US20170129959A1/en.
- sIL7R splice modulation: `WO2019183570A1`, "Soluble interleukin-7 receptor (sIL7R) modulating therapy to treat autoimmune diseases and cancer", covers IL7R exon 6 splice-modulating oligonucleotides that increase/decrease soluble IL7R; mentions autoimmune disease and MS. Source: https://patents.google.com/patent/WO2019183570A1/en.
- IL7R VHH biologics: `US11667719B2`, active, VHH domains binding IL-7R for autoimmune/inflammatory diseases, including IL-7/TSLP signaling inhibition. Source: https://patents.google.com/patent/US11667719B2/en.
- Biomarker/stratification prior art: `EP4499875B1`, "Biomarkers of IL7R modulator activity", active, covers predicting/evaluating response to IL7R modulators. Source: https://patents.google.com/patent/EP4499875B1/en.

This prior art directly overlaps both candidate reframes: anti-CD127 blockade and sIL7R/splicing stratification.

## Search Log

- Europe PMC: `IL7R multiple sclerosis rs6897932 soluble receptor`; key hits PMID `35613883`, `31594933`.
- Europe PMC: `IL7R autoimmune monocytes soluble surface receptor rs6897932`; key hit PMID `31594933`.
- Europe PMC: `PF-06342674 IL-7 receptor alpha type 1 diabetes`; key hits PMID `31852846`, `31900603`.
- Europe PMC: `GSK2618960 IL-7 receptor alpha Sjogren multiple sclerosis`; key hit PMID `30161291`.
- Europe PMC: `OSE-127 Phase 1 IL-7R`; key hit PMID `36734626`.
- ClinicalTrials.gov API terms: `IL7R`, `CD127`, `IL-7 receptor`, `OSE-127`, `lusvertikimab`, `PF-06342674`, `GSK2618960`, `S95011`; key trials `NCT01740609`, `NCT02038764`, `NCT02045732`, `NCT01808482`, `NCT02293161`, `NCT03239600`, `NCT03980080`, `NCT04605978`, `NCT04882007`.
- Google Patents: `OSE-127 IL-7R alpha antibody patent CD127`; `lusvertikimab IL-7R alpha antibody patent CD127`; `IL7R rs6897932 multiple sclerosis autoimmune patent`; key records `US20170129959A1`, `WO2019183570A1`, `US11667719B2`, `EP4499875B1`.

## Decisive Next Experiment

The experiment that would rescue `IL7R` from demotion is not another bulk signature correlation. It must separate direct APC biology from T-cell survival biology.

Design:

- Samples: genotype-balanced human donors for `rs6897932`, minimum 24 PBMC donors split 12 risk-allele carriers and 12 noncarriers; add disease tissue if available, preferably 8-12 RA/SpA synovial fluid or UC lamina propria samples because that is where the monocyte/APC claim is strongest.
- Cells: sort CD14+ monocytes, CD1c+ dendritic cells, and autologous memory CD4+ T cells. Run purified APC-only, purified T-cell-only, and APC:T-cell co-culture arms.
- Perturbations: vehicle, IL-7, IL-7 plus recombinant sIL7R, anti-CD127/lusvertikimab-like antagonist, IL7R exon-6 anti-sIL7R ASO, and isotype/scrambled controls. Stimulate APCs with LPS plus IFN-gamma or disease-relevant debris/myelin-lipid stimulus.
- Readouts: surface CD127, secreted sIL7R, pSTAT5, single-cell RNA/CITE-seq, HLA-II/APC score, C1Q phagocytic score, lipid-loader/lysosomal score, cytokines, T-cell memory survival, and myelin/debris uptake or efferocytosis assay.
- Promotion criterion: in purified APCs, anti-CD127 or anti-sIL7R ASO must reduce the V3 APC/lipid-lysosomal inflammatory module by at least `0.5 SD` and reduce inflammatory phagocytic output or myelin/debris uptake by at least `25%`, FDR < `0.05`, with a consistent genotype interaction in the risk-allele group. Effects confined to APC:T-cell co-culture are acceptable only for a stratified lymphoid-myeloid claim, not for a direct myeloid target claim.
- Falsification/stop-loss: if an interim 12-donor set shows APC-only module effect < `0.2 SD`, or if IL7R induction is absent in >75% of purified APC samples after stimulation, stop the V3 reopener. If effects occur only through T-cell depletion/survival, keep `IL7R` as an existing clinical program/biomarker comparator, not a novel V3 target.

## Final Call

Do not promote `IL7R` as the V3 therapeutic finding. It is a strong comparator because it has genetics, clinical tools, and a real monocyte extension. But the exact reframe needed for V3 is already partly published and patent-covered, and the current local/foundation evidence does not establish that IL7R modulation controls the lipid-lysosomal myeloid module in MS or across the autoimmune cluster.
