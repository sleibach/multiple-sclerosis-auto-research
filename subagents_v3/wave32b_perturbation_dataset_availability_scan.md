# Wave32-B Perturbation And Dataset Availability Scan

Timestamp: 2026-05-27

Scope: identify real public datasets usable in this session to test whether perturbing resolution, efferocytosis, and lipid-clearance nodes moves macrophages, microglia, or APCs away from an inflammatory lipid-lysosomal/APC state toward resolution without generic IFN collapse. This is not a final finding and does not nominate a therapy.

## Search Trail

Searches executed:

- NCBI GEO DataSets via E-utilities using queries for `MERTK`, `AXL`, `TYRO3`, `GAS6`, `PROS1`, `TREM2`, `APOE`, `LPL`, `LXR`, `NR1H3`, `NR1H2`, `ABCA1`, `ABCG1`, `PPAR`, `retinoid`, `GPNMB`, `CD300`, `LIPA`, `NPC1`, `NPC2`, `efferocytosis`, `Perturb-seq`, and `CRISPR screen`.
- GEO FTP directory checks for series matrix and supplementary files.
- ArrayExpress/BioStudies API query checks. The useful ArrayExpress hits for this scope were mostly GEO mirrors, especially `E-GEOD-65067`, `E-GEOD-70475`, and `E-GEOD-66926` for TREM2 microglia.
- Local V3 resources checked: `data/raw_v3/lincs2020/compoundinfo_beta.txt`, Wave15 L1000 selectivity outputs, Wave23 metabolite/barrier L1000 route outputs, Mixscale/Perturb-seq tables, State parse outputs, and Geneformer outputs.

Primary output matrix:

- `results_v3/wave32b_dataset_availability_scan/candidate_dataset_matrix.tsv`

## High-Value Immediate Datasets

1. `GSE156234`: MerTK+/+ vs MerTK-/- peritoneal macrophages across no apoptotic-cell exposure and 2h/6h efferocytosis. This is the cleanest target-specific test for the TAM/efferocytosis branch because genotype and apoptotic-cell exposure are crossed. It is small but single-cell and has aggregated raw counts.

2. `GSE212008`: genome-wide pooled CRISPR knockout screen in primary BMDMs sorted into input, non-eaters, and efficient eaters. This is the best screen to ask whether candidate nodes are causal efferocytosis regulators. It does not have transcriptomic readouts, so it must be paired with expression datasets.

3. `GSE169160`: human CD14+ monocyte-derived macrophages with apoptotic-cell co-culture. This is the best human efferocytosis-resolution transcriptome and explicitly targets LXR/PPARD/efferocytosis biology.

4. `GSE325329`: BMDMs polarized with IFNg or IL10 and then separated by apoptotic Treg/Tconv phagocytosis. This is the strongest direct test of the “resolution without generic IFN collapse” criterion because IFNg non-phagocytic controls are present.

5. `GSE302857` plus `GSE66926`/`GSE70475`: TREM2/demyelination microglia anchor and replication datasets. `GSE302857` is the strongest MS-adjacent microglia dataset because it includes cuprizone, Trem2KO, sorted inflammatory subsets, and additional transcription-factor KOs.

6. `GSE100260`, `GSE243117`, and `GSE285961`: LIPA loss and gain datasets. Together they can test whether LIPA restoration is resolution-like or instead stress/APC/inflammation-shifting.

7. `GSE274954`: GPNMB mutant BMDMs with and without OxLDL. This is a direct perturbation under lipid loading and should be used to decide whether GPNMB is a controller or just a lipid-foam marker.

8. `GSE254406`, `GSE273340`, `GSE254572`, and `GSE287142`: nuclear receptor/retinoid/LXR/RXR datasets. These are useful but should be down-weighted because prior V3 work already found PPAR/LXR/RXR routes broad and crowded; their role here is mechanism testing, not target promotion.

## Weak Or Blocked Datasets

- `CD300*`: no credible macrophage perturbation transcriptomic dataset was found in this pass. GEO search returned irrelevant or non-perturbation material.
- Direct `AXL`, `TYRO3`, and `PROS1` macrophage perturbation: no strong target-specific transcriptomic dataset found. `GSE205267` is GAS6/AXL inflammatory tissue context but not a clean AXL perturbation expression contrast.
- `GSE246338`: useful GAS6/MerTK-context data, but all samples appear rGAS6-stimulated; it compares WT vs ATF3-CKO, not GAS6 vs control.
- `GSE306545`, `GSE106295`, and `GSE241928`: Mertk/cardiac tissue studies are relevant but too bulk-tissue/confounded for a primary macrophage claim.
- `GSE300844`: broad and large, but first inspected matrix was MPRA/variant-oriented THP-1 material, not a clean macrophage target perturbation for this mechanism. It may be useful later for regulatory variants, not this immediate perturbation test.
- LINCS/CMap/L1000: local metadata contains many relevant chemical names (`GW-3965`, `T-0901317`, PPAR ligands, retinoids, `BMS-777607`, `probucol`, `ezetimibe`), but prior V3 L1000 outputs showed cell-line, generic, or contradictory signatures. Use only as low-weight pharmacologic context.
- Foundation models: local State released files remain gene-mapping-limited; Evo was blocked by local runtime; Geneformer V2-104M is runnable but deletion-style and not a validated agonism/efferocytosis predictor. Use only as a veto/triage layer after real perturbation data.

## Recommended Local Analysis

Recommended first-pass script: `scripts/v3_wave32b_resolution_perturbation_analysis.py`.

Core design:

1. Download only processed count or expression files first:
   - `GSE156234_aggregated_raw_counts.tsv.gz`
   - `GSE169160_Normalized_counts_MF.txt.gz` and `GSE169160_Normalized_reads_MF_AC.txt.gz`
   - `GSE253577_RNAseq_table_mouse_raw_counts.txt.gz`
   - `GSE325042_raw_gene_counts.tsv.gz`
   - `GSE100260_control_LIPA_KO_FPKM.tsv.gz`
   - `GSE243117_PM_RldNormalizedCounts.csv.gz`
   - `GSE285961_PlaqueMacs_RldNormalizedCounts.csv.gz`
   - `GSE274954_gene_count.csv.gz`
   - `GSE254406_Genes_count_table.tsv.gz`
   - `GSE273340_Genes_count_table.tsv.gz`
   - `GSE287142_rawcount.csv.gz`

2. Define fixed modules before inspecting effect directions:
   - inflammatory lipid-lysosomal/APC state: existing V3 `ifn_lysosomal_apc_state`, HLA-II/CD74/GILT module, APOE/LPL/GPNMB/SPP1/TYROBP/CTSD/LIPA/PLIN2 lipid-lysosomal module.
   - resolution/efferocytosis module: `MERTK`, `AXL`, `TYRO3`, `GAS6`, `PROS1`, `TREM2`, `APOE`, `LPL`, `ABCA1`, `ABCG1`, `NR1H3`, `NR1H2`, `PPARD`, `PPARG`, `MRC1`, `CD163`, `IL10`, `TGFB1`, `VSIG4`, `C1QA`, `C1QB`, `C1QC`, `F13A1`, `LYVE1`.
   - generic IFN safety module: `STAT1`, `IRF1`, `IRF7`, `ISG15`, `MX1`, `IFIT1`, `IFIT2`, `IFIT3`, `OAS1`, `GBP1`, `CXCL10`.
   - stress/cytotoxicity module: `DDIT3`, `HSPA1A`, `HSPA1B`, `ATF4`, `XBP1`, `BAX`, `CASP3`, `FOS`, `JUN`.

3. For each contrast compute:
   - mean module delta and standardized Hedges-like effect where replicate count permits;
   - resolution gain = delta(resolution/efferocytosis);
   - target-state rescue = negative delta(inflammatory lipid/APC) where disease/activation baseline is high;
   - IFN preservation score = `abs(delta_generic_ifn) < 0.5 * abs(delta_resolution)` and no collapse of HLA-II when the biological question requires antigen-presentation preservation;
   - stress penalty = positive stress module delta.

4. Prioritize contrasts:
   - `GSE156234`: interaction `(MerTK+/+ AC - MerTK+/+ media) - (MerTK-/- AC - MerTK-/- media)`.
   - `GSE325329`: IFNg phagocytic Treg/Tconv vs IFNg non-phagocytic, then compare IL10 analogs.
   - `GSE302857`: Trem2KO vs WT within cuprizone inflammatory microglia subsets and compare to `GSE66926`.
   - `GSE100260`/`GSE243117`/`GSE285961`: LIPA loss/gain direction consistency.
   - `GSE274954`: OxLDL interaction `(Gpnmb mutant OxLDL - WT OxLDL) - (Gpnmb mutant untreated - WT untreated)`.
   - `GSE254406`/`GSE273340`/`GSE287142`: nuclear receptor loss or RXR agonism as mechanism comparators, not primary target evidence.

5. Use `GSE212008` and `GSE299696` as screen-only filters:
   - If a candidate is not enriched in the primary efferocytosis CRISPR screen and has no transcriptomic rescue effect, demote it.
   - If a candidate appears only in THP-1 cholesterol-efflux screen data but not primary macrophage/efferocytosis datasets, keep it as readout-only.

Decision rule for Wave32 integration:

- Promote only candidates where target perturbation or direct efferocytosis shifts increase the resolution/efferocytosis module and reduce lipid/APC inflammatory excess without suppressing the generic IFN module more strongly than the target-state module.
- Demote candidates if the apparent improvement is generic IFN/JAK/TNF collapse, cytotoxic stress, bulk tissue deconvolution, or only screen/readout support.

## Sources

Official GEO pages follow the pattern `https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=<ACCESSION>`.

Supplementary files were verified through NCBI GEO FTP directories, for example:

- `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE156nnn/GSE156234/`
- `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE212nnn/GSE212008/`
- `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE169nnn/GSE169160/`
- `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE302nnn/GSE302857/`
- `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE274nnn/GSE274954/`
- `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE254nnn/GSE254406/`
