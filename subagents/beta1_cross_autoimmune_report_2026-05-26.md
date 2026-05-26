# Subagent β1 Cross-Autoimmune Report

**Returned:** 2026-05-26

No files edited by subagent.

## Bottom Line

`ACSL1` itself is not yet a clean pan-autoimmune recurrence. Strongest direct non-MS evidence is SLE myeloid biology and UC/bulk IBD lipid-gene analyses. The broader lipid-associated inflammatory myeloid module is more recurrent across lupus nephritis, rheumatoid arthritis, IBD, psoriasis, and probably Sjogren/T1D blood myeloid datasets.

At least five non-MS diseases are locally analyzable: SLE, IBD/UC/Crohn, psoriasis, T1D, Sjogren. RA and lupus nephritis are feasible but the best human single-cell objects may require ARK/Synapse/ImmPort access.

## Disease Notes

| Disease | Evidence tier | Accessions / URLs | Recommended local analysis | Red flags |
|---|---|---|---|---|
| RA | Pathway > direct `ACSL1`. Recent RA work supports `TREM2+` macrophage niches and metabolic macrophage exhaustion. | AMP RA synovium PMID `37938773`, Synapse DOI `10.7303/syn52297840`; earlier AMP PMID `31061532`, ImmPort `SDY998`. | Pseudobulk synovial myeloid subsets by donor; test `ACSL1` and LDAM module versus inflammatory RA subtype and TREM2 niche. | Best processed data are portal gated; TREM2/APOE macrophages may be regulatory/remodeling. |
| SLE / lupus nephritis | Direct `ACSL1` in SLE myeloid cells plus LN pathway evidence. IFN-I induces ACSL1; SLE myeloid cells show increased ACSL1. | Direct paper PMID `39675509`; sorted blood subsets `GSE10325`; LN atlas PMID `40900124`, ARK/Synapse DOI `10.7303/syn68564337.1`; mouse LN `GSE302065`; bulk LN `GSE32591`. | Reproduce `ACSL1` SLE-vs-control in sorted myeloid vs T/B cells in `GSE10325`; then LN myeloid pseudobulk if accessible. | IFN-I paper suggests ACSL1 may protect myeloid cells from saturated-fatty-acid death; inhibition could worsen injury. |
| IBD / Crohn / UC | Direct-ish `ACSL1` in UC bulk/bioinformatic lipid-gene studies; strong feasibility. | UC lipid-gene paper PMID `40949920`; bulk `GSE126124`, `GSE92415`, `GSE87466`; scRNA `GSE116222`, `GSE134809`, `GSE162335`. | Analyze inflamed versus non-inflamed myeloid pseudobulk; test ACSL1 versus LDAM/inflammatory/eicosanoid genes. | Published ACSL1 evidence is mostly bulk/ML; UC and Crohn may diverge. |
| Psoriasis | Pathway opportunity, no strong direct ACSL1 signal found. | Immune-cell scRNA `GSE151177`; sc/spatial psoriasis PMID `37308489`, `GSE173706`, `GSE225475`; skin zonation PMID `33958582`, `GSE162183`. | Compare lesional/nonlesional/healthy macrophage and DC subsets; spatial co-localization with inflammatory skin niches. | Keratinocyte lipid programs may swamp myeloid signal. |
| Type 1 diabetes | Direct tissue ACSL1 weak; blood monocyte datasets feasible. | CD14 monocytes `GSE154609`, PMID `32978233`; hyperglycemic memory `GSE164338`, PMID `33431659`; recent-onset monocytes `GSE33440`. | Regress monocyte ACSL1/LDAM against status and HbA1c; separate disease from glycemic burden. | Peripheral blood, not pancreatic lesion macrophages. |
| Sjogren's | Weak direct ACSL1; PBMC and salivary gland testing feasible. | PBMC scRNA `GSE157278`; salivary gland bulk `GSE23117`, `GSE40611`, `GSE80805`. | PBMC myeloid pseudobulk and salivary gland module scoring. | Disease often epithelial/B-cell/IFN-heavy. |
| Hashimoto / autoimmune thyroiditis | Weakest. | Bulk/cancer-adjacent thyroid `GSE138198`; PMID `38127960`. | Low-priority bulk contrast/deconvolution. | Poor myeloid resolution. |

## Recommendation

Do not frame V2 as “ACSL1 recurs across autoimmunity.” The defensible cross-disease claim is narrower: an ACSL1-compatible lipid-handling inflammatory myeloid module recurs across several autoimmune tissues, while direct ACSL1 support is strongest in SLE myeloid cells and UC/bulk IBD. The main target-level concern is that ACSL1 may sometimes be a stress-buffering or survival adaptation rather than a harmful driver.
