# Novelty Assessment

**Search date:** 2026-05-26  
**Target claim assessed:** In postmortem MS white-matter specimens, a pre-specified `TNFRSF9`/`TNFSF9` costimulation score does not show a biologically meaningful positive association with a lipid/complement microglial program, although it may be enriched in samples morphologically labelled as containing foamy microglia.

## Databases And Queries

The search occurred after the locked primary run and before writing `FINDING.md`. The broad association of adaptive immune and foamy-microglial biology was already recognized as published before expression outcomes were inspected, as documented in `PLAN.md`.

| Database/source | Queries executed | Result relevant to target claim |
|---|---|---|
| PubMed, via NCBI E-utilities and web retrieval | `TNFSF9 foamy microglia multiple sclerosis`; `TNFRSF9 foamy microglia multiple sclerosis`; `CD137 chronic active multiple sclerosis`; `Identification of CD137-expressing B cells in multiple sclerosis` | No PubMed hits for the exact `TNFSF9`/`TNFRSF9` plus foamy-microglia queries. The CD137 searches retrieved existing lesion literature, including van Nierop et al. and Wong et al. |
| Google Scholar | `"TNFSF9" "foamy microglia" "multiple sclerosis"`; `"TNFRSF9" "foamy microglia" "multiple sclerosis"`; `"CD137" "chronic active" "multiple sclerosis"` | Zero visible results for both exact gene-plus-foamy queries at search time. The `CD137` query returned Wong et al. and related MS immune literature, confirming that general CD137 lesion biology is prior art. |
| bioRxiv | Direct site search for the three terms above was attempted; two requests returned HTTP `403` and one failed DNS resolution. A domain-restricted bioRxiv search and Europe PMC preprint-index (`PUBLISHER:"bioRxiv"`) search were then used. | No exact `TNFSF9`/`TNFRSF9` plus foamy-microglia report was located. A related preprint/published line of work addresses CD8/interferon chronic lesion inflammation, not this costimulation score. Direct bioRxiv query failure is retained as a limitation. |
| Europe PMC / full-text search | Same focused queries; full-text inspection/search of the available pages for Van der Vliet et al. 2026, Wong et al. 2020, Smolders et al. 2022, and the 2023 immune-checkpoint review | Located prior CD137-in-lesion and foamy-microglia/adaptive-module work. No directly stated `TNFRSF9`/`TNFSF9` score-to-lipid/complement association or reported negative test was found in the searched full text. |

## Closest Prior Work

| Prior work | What it already establishes | Delta from this execution |
|---|---|---|
| Wong HY, Prasad A, Gan SU, Chua JJE, Schwarz H. *Frontiers in Immunology*. 2020;11:571964. [DOI](https://doi.org/10.3389/fimmu.2020.571964), [PubMed](https://pubmed.ncbi.nlm.nih.gov/33240262/) | CD137 (`TNFRSF9`) positive cells occur in postmortem MS brain; the study included chronic active lesions and identified CD137-positive B cells in meningeal infiltrates; CD137 engagement increased inflammatory B-cell output in vitro. | This means "CD137 is present in MS/chronic active lesions" is **not novel**. It did not test a `TNFRSF9`/`TNFSF9` composite against foamy-microglia morphology or a lipid/complement transcript program in `GSE279972`. |
| Van der Vliet D, et al. *Nature Neuroscience*. 2026. *Foamy microglia link oxylipins to disease progression in multiple sclerosis*. [DOI](https://doi.org/10.1038/s41593-026-02302-3), [data record](https://doi.org/10.5281/zenodo.19352263) | In the same `GSE279972` tissue resource, reports foamy-microglia lesions, lipid/lysosomal biology, and an adaptive immune module including `CD79A`, `CCL5`, and `IGHG1`. | General adaptive-to-foamy association is **published** and is treated here only as a positive control. Searches of the article presentation did not locate a direct reported `TNFRSF9`/`TNFSF9` composite result or the negative co-variation test performed here. |
| Smolders J, van Luijn MM, Hsiao C-C, Hamann J. *Seminars in Immunopathology*. 2022;44:855-867. [DOI](https://doi.org/10.1007/s00281-022-00926-8) | Reviews T cells in MS brain, including activation marker CD137 and proximity of T cells to myelin-collecting foamy microglia in lesions. | Supports biological relevance, but does not quantify the transcript-level costimulation-to-lipid/complement relationship tested here. |
| Laderach F, et al. *Nature*. 2025. *EBV induces CNS homing of B cells attracting inflammatory T cells*. [DOI](https://doi.org/10.1038/s41586-025-09378-0) | Motivates examining inflammatory/costimulatory B/T recruitment in the EBV context in a humanized-mouse model. | It is not human MS lesion evidence and does not validate the present tissue association or negative result. |

## Novelty Conclusion

No directly published report of the **specific tested negative association** was located: failure of a pre-specified `TNFRSF9`/`TNFSF9` score to reach a meaningful positive association with a lipid/complement microglial program in `GSE279972`. However, this is a secondary reanalysis of a newly published cohort, and the biological ingredients are substantially pre-existing. The novelty claim is therefore limited to an **unreported targeted negative test and a secondary candidate enrichment**, pending independent confirmation and broader systematic searching.
