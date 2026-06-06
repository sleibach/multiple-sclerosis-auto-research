# Wave15-A Surface/Trafficking Dependency Screen

## Scope

I tested candidate surface, endosomal trafficking, protease, chaperone, glycosylation, lysosomal, and uptake genes against the recurring `CD74`/`CIITA`/HLA-II state using only local V3 datasets. The statistical unit is donor/sample, not cells. Direct h5ad analyses are compartment-restricted; celiac uses marker-derived compartments; thyroid Visium and MS sorted microglia are sample-level tissue validations.

## Inputs

- `ibd_crohn_myeloid` (single_cell_h5ad): completed; n_cells=2610, n_units=12, n_candidate_genes_present=78
- `ibd_uc_myeloid` (single_cell_h5ad): completed; n_cells=1838, n_units=12, n_candidate_genes_present=78
- `ibd_crohn_epithelial` (single_cell_h5ad): completed; n_cells=11414, n_units=12, n_candidate_genes_present=78
- `ibd_uc_epithelial` (single_cell_h5ad): completed; n_cells=7646, n_units=12, n_candidate_genes_present=78
- `ibd_crohn_stromal` (single_cell_h5ad): completed; n_cells=1951, n_units=12, n_candidate_genes_present=78
- `ibd_uc_stromal` (single_cell_h5ad): completed; n_cells=2042, n_units=12, n_candidate_genes_present=78
- `psoriasis_skin_apc` (single_cell_h5ad): completed; n_cells=1086, n_units=6, n_candidate_genes_present=68
- `psoriasis_keratinocyte` (single_cell_h5ad): completed; n_cells=9583, n_units=6, n_candidate_genes_present=68
- `psoriasis_skin_stromal` (single_cell_h5ad): completed; n_cells=11297, n_units=6, n_candidate_genes_present=68
- `sjogren_gland_apc` (single_cell_h5ad): completed; n_cells=1695, n_units=25, n_candidate_genes_present=78
- `sjogren_gland_epithelial` (single_cell_h5ad): completed; n_cells=50097, n_units=25, n_candidate_genes_present=78
- `sjogren_gland_stromal` (single_cell_h5ad): completed; n_cells=17849, n_units=25, n_candidate_genes_present=78
- `ra_blood_myeloid` (single_cell_h5ad): completed; n_cells=23609, n_units=36, n_candidate_genes_present=78
- `t1d_beta_cell` (single_cell_h5ad): completed; n_cells=11298, n_units=23, n_candidate_genes_present=78
- `t1d_ductal_cell` (single_cell_h5ad): completed; n_cells=11924, n_units=24, n_candidate_genes_present=78
- `t1d_acinar_cell` (single_cell_h5ad): completed; n_cells=23216, n_units=24, n_candidate_genes_present=78
- `t1d_stellate_cell` (single_cell_h5ad): completed; n_cells=2163, n_units=24, n_candidate_genes_present=78
- `t1d_endothelial_cell` (single_cell_h5ad): completed; n_cells=2658, n_units=24, n_candidate_genes_present=78
- `gse111972_ms_microglia` (sorted_bulk_microglia): completed; n_samples=31, n_candidate_genes_present=77
- `gse315138_Healthy1` (single_cell_10x_marker_compartment): completed; n_cells=20401, n_genes_selected=134
- `gse315138_Healthy2` (single_cell_10x_marker_compartment): completed; n_cells=10918, n_genes_selected=134
- `gse315138_celiac1` (single_cell_10x_marker_compartment): completed; n_cells=16250, n_genes_selected=134
- `gse315138_celiac2` (single_cell_10x_marker_compartment): completed; n_cells=26208, n_genes_selected=134
- `gse315138_celiac_a2` (single_cell_10x_marker_compartment): completed; n_cells=22212, n_genes_selected=134
- `gse315138_celiac304` (single_cell_10x_marker_compartment): completed; n_cells=17438, n_genes_selected=134
- `gse248205_thyroid_spatial` (spatial_visium_sample_level): completed; n_samples=8, n_spots=16985, n_candidate_genes_present=78

## Methods

- For each analysis I library-size normalized selected genes, log-transformed them, z-scored genes against matched controls, and averaged to donor/sample-level gene scores.
- Disease-control evidence uses Welch tests and Hedges g on donor/sample gene z-scores and detection fractions, with BH FDR within each analysis/metric.
- State-coupling evidence uses donor/sample Spearman correlations between each candidate and two state modules: `hla_cd74_ciita_state` and `cd74_hla_surface_state`.
- Residual state coupling regresses both candidate and state module against `myeloid_abundance`, `generic_nfkb`, and `lipid_loader_phagocytic`; a stricter secondary model also includes `ifn_apc_upstream`.
- Pivot criterion applied: candidates with raw state coupling but no residual coupling, or stronger myeloid/confounder coupling than state coupling, are demoted as abundance/state markers.

## Ranked Candidates

| rank | gene | family | local call | rank score | delta trend+ diseases | residual state diseases | raw state diseases | confounder-dominant diseases | reason |
|---:|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | `HLA-DMA` | hla_chaperone_loading | NO_GO | 30.75 | 6 | 7 | 9 | 0 | strong local state biology but weak direct druggability/tractable modulation |
| 2 | `CTSH` | cathepsin_protease | GO_SCOUT | 30.00 | 5 | 8 | 8 | 3 | passes local dependency gate |
| 3 | `CTSS` | cathepsin_protease | GO_SCOUT | 28.25 | 4 | 6 | 10 | 4 | passes local dependency gate |
| 4 | `LGALS9` | galectin_glycan_checkpoint | GO_SCOUT | 27.25 | 4 | 7 | 9 | 3 | passes local dependency gate |
| 5 | `HLA-DMB` | hla_chaperone_loading | NO_GO | 26.50 | 5 | 7 | 8 | 1 | strong local state biology but weak direct druggability/tractable modulation |
| 6 | `HLA-DOA` | hla_chaperone_loading | NO_GO | 23.25 | 3 | 6 | 7 | 2 | strong local state biology but weak direct druggability/tractable modulation |
| 7 | `LAPTM5` | lysosome_membrane_or_lipid | GO_SCOUT | 22.75 | 3 | 6 | 7 | 3 | passes local dependency gate |
| 8 | `CLEC7A` | surface_phagocytic_lipid_receptor | NO_GO | 22.69 | 4 | 5 | 7 | 6 | confounder/myeloid coupling dominates state coupling |
| 9 | `LYZ` | myeloid_marker_control | NO_GO | 21.38 | 5 | 6 | 7 | 6 | confounder/myeloid coupling dominates state coupling; strong local state biology but weak direct druggability/tractable modulation |
| 10 | `LIPA` | lysosome_membrane_or_lipid | NO_GO | 20.50 | 4 | 5 | 6 | 6 | confounder/myeloid coupling dominates state coupling |
| 11 | `NPC1` | lysosome_membrane_or_lipid | NO_GO | 20.00 | 3 | 7 | 6 | 6 | near-confounder-dominant; not cleanly independent of myeloid/phagocytic state |
| 12 | `HLA-DOB` | hla_chaperone_loading | NO_GO | 19.75 | 4 | 5 | 6 | 2 | strong local state biology but weak direct druggability/tractable modulation |
| 13 | `CD68` | surface_phagocytic_lipid_receptor | NO_GO | 19.69 | 2 | 5 | 8 | 4 | near-confounder-dominant; not cleanly independent of myeloid/phagocytic state |
| 14 | `LST1` | myeloid_marker_control | NO_GO | 19.38 | 3 | 4 | 6 | 4 | confounder/myeloid coupling dominates state coupling; strong local state biology but weak direct druggability/tractable modulation |
| 15 | `ITGAM` | surface_phagocytic_lipid_receptor | WATCHLIST | 19.19 | 2 | 6 | 6 | 4 | watchlist: residual state support present but GO gate not met |

## Go/No-Go

Local `GO_SCOUT` candidates:
- `CTSH`: cathepsin_protease; delta support 5 diseases; residual state support 8 diseases; rank score 30.00.
- `CTSS`: cathepsin_protease; delta support 4 diseases; residual state support 6 diseases; rank score 28.25.
- `LGALS9`: galectin_glycan_checkpoint; delta support 4 diseases; residual state support 7 diseases; rank score 27.25.
- `LAPTM5`: lysosome_membrane_or_lipid; delta support 3 diseases; residual state support 6 diseases; rank score 22.75.

Watchlist candidates that did not meet the strict local gate:
- `ITGAM`: surface_phagocytic_lipid_receptor; raw state support 6, residual support 6; reason: watchlist: residual state support present but GO gate not met.

## Per-Disease Evidence For Survivors And Biological Anchors

| gene | role in this screen | disease-control support | residual state-coupling support | raw state-coupling support | negative disease-control trends |
|---|---|---|---|---|---|
| `CTSH` | GO_SCOUT | Crohn disease; Graves disease; Hashimoto thyroiditis; type 1 diabetes mellitus; ulcerative colitis | Crohn disease; MS; Sjogren syndrome; celiac disease; psoriasis; rheumatoid arthritis; type 1 diabetes mellitus; ulcerative colitis | Crohn disease; Graves disease; Hashimoto thyroiditis; Sjogren syndrome; psoriasis; rheumatoid arthritis; type 1 diabetes mellitus; ulcerative colitis |  |
| `CTSS` | GO_SCOUT | Crohn disease; Hashimoto thyroiditis; type 1 diabetes mellitus; ulcerative colitis | Crohn disease; celiac disease; psoriasis; rheumatoid arthritis; type 1 diabetes mellitus; ulcerative colitis | Crohn disease; Graves disease; Hashimoto thyroiditis; MS; Sjogren syndrome; celiac disease; psoriasis; rheumatoid arthritis; type 1 diabetes mellitus; ulcerative colitis |  |
| `LGALS9` | GO_SCOUT | Hashimoto thyroiditis; psoriasis; type 1 diabetes mellitus; ulcerative colitis | MS; Sjogren syndrome; celiac disease; psoriasis; rheumatoid arthritis; type 1 diabetes mellitus; ulcerative colitis | Crohn disease; Graves disease; Hashimoto thyroiditis; MS; Sjogren syndrome; celiac disease; psoriasis; rheumatoid arthritis; type 1 diabetes mellitus |  |
| `LAPTM5` | GO_SCOUT | Hashimoto thyroiditis; Sjogren syndrome; ulcerative colitis | Crohn disease; Sjogren syndrome; celiac disease; psoriasis; type 1 diabetes mellitus; ulcerative colitis | Crohn disease; Graves disease; Hashimoto thyroiditis; MS; celiac disease; psoriasis; type 1 diabetes mellitus |  |
| `ITGAM` | WATCHLIST | Hashimoto thyroiditis; celiac disease | Crohn disease; MS; celiac disease; psoriasis; type 1 diabetes mellitus; ulcerative colitis | Crohn disease; Graves disease; Hashimoto thyroiditis; Sjogren syndrome; celiac disease; rheumatoid arthritis |  |
| `HLA-DMA` | strong local state biology but weak direct druggability/tractable modulation | Crohn disease; Hashimoto thyroiditis; Sjogren syndrome; celiac disease; type 1 diabetes mellitus; ulcerative colitis | Crohn disease; MS; Sjogren syndrome; celiac disease; rheumatoid arthritis; type 1 diabetes mellitus; ulcerative colitis | Crohn disease; Graves disease; Hashimoto thyroiditis; MS; Sjogren syndrome; celiac disease; rheumatoid arthritis; type 1 diabetes mellitus; ulcerative colitis |  |
| `HLA-DMB` | strong local state biology but weak direct druggability/tractable modulation | Crohn disease; Hashimoto thyroiditis; Sjogren syndrome; celiac disease; ulcerative colitis | Crohn disease; MS; Sjogren syndrome; celiac disease; rheumatoid arthritis; type 1 diabetes mellitus; ulcerative colitis | Crohn disease; Hashimoto thyroiditis; MS; Sjogren syndrome; celiac disease; rheumatoid arthritis; type 1 diabetes mellitus; ulcerative colitis |  |
| `HLA-DOA` | strong local state biology but weak direct druggability/tractable modulation | Crohn disease; Hashimoto thyroiditis; celiac disease | Crohn disease; MS; Sjogren syndrome; celiac disease; type 1 diabetes mellitus; ulcerative colitis | Crohn disease; Graves disease; Hashimoto thyroiditis; MS; Sjogren syndrome; celiac disease; ulcerative colitis |  |
| `HLA-DOB` | strong local state biology but weak direct druggability/tractable modulation | Graves disease; Hashimoto thyroiditis; Sjogren syndrome; type 1 diabetes mellitus | Crohn disease; MS; Sjogren syndrome; celiac disease; ulcerative colitis | Crohn disease; Graves disease; Hashimoto thyroiditis; MS; Sjogren syndrome; celiac disease | rheumatoid arthritis |

## Mandatory Candidate Family Check

| gene | family | local call | delta trend+ | residual state | raw state | negative deltas | reason |
|---|---|---|---:|---:|---:|---:|---|
| `HLA-DMA` | hla_chaperone_loading | NO_GO | 6 | 7 | 9 | 0 | strong local state biology but weak direct druggability/tractable modulation |
| `CTSS` | cathepsin_protease | GO_SCOUT | 4 | 6 | 10 | 0 | passes local dependency gate |
| `LGALS9` | galectin_glycan_checkpoint | GO_SCOUT | 4 | 7 | 9 | 0 | passes local dependency gate |
| `HLA-DMB` | hla_chaperone_loading | NO_GO | 5 | 7 | 8 | 0 | strong local state biology but weak direct druggability/tractable modulation |
| `LIPA` | lysosome_membrane_or_lipid | NO_GO | 4 | 5 | 6 | 0 | confounder/myeloid coupling dominates state coupling |
| `NPC2` | lysosome_membrane_or_lipid | NO_GO | 2 | 4 | 8 | 0 | confounder/myeloid coupling dominates state coupling |
| `C1QA` | surface_uptake_fc_complement | NO_GO | 2 | 6 | 6 | 0 | confounder/myeloid coupling dominates state coupling |
| `SCARB1` | surface_phagocytic_lipid_receptor | NO_GO | 2 | 5 | 7 | 0 | near-confounder-dominant; not cleanly independent of myeloid/phagocytic state |
| `SNX10` | vesicle_sorting_trafficking | NO_GO | 5 | 2 | 5 | 0 | confounder/myeloid coupling dominates state coupling; strong local state biology but weak direct druggability/tractable modulation |
| `IFI30` | lysosomal_thiol_reductase | NO_GO | 3 | 5 | 5 | 0 | confounder/myeloid coupling dominates state coupling |
| `TYROBP` | surface_phagocytic_lipid_receptor | NO_GO | 3 | 3 | 6 | 0 | confounder/myeloid coupling dominates state coupling |
| `C1QB` | surface_uptake_fc_complement | NO_GO | 2 | 5 | 5 | 0 | confounder/myeloid coupling dominates state coupling |
| `FCGR2A` | surface_uptake_fc_complement | NO_GO | 3 | 5 | 5 | 0 | confounder/myeloid coupling dominates state coupling |
| `SNX5` | vesicle_sorting_trafficking | NO_GO | 3 | 4 | 6 | 0 | confounder/myeloid coupling dominates state coupling; strong local state biology but weak direct druggability/tractable modulation |
| `RAB11A` | vesicle_sorting_trafficking | NO_GO | 3 | 5 | 5 | 0 | confounder/myeloid coupling dominates state coupling; strong local state biology but weak direct druggability/tractable modulation |
| `AP2M1` | vesicle_sorting_trafficking | NO_GO | 3 | 4 | 6 | 0 | confounder/myeloid coupling dominates state coupling; strong local state biology but weak direct druggability/tractable modulation |
| `MRC1` | surface_phagocytic_lipid_receptor | NO_GO | 1 | 6 | 3 | 0 | confounder/myeloid coupling dominates state coupling |
| `RAB5A` | vesicle_sorting_trafficking | NO_GO | 2 | 5 | 4 | 0 | confounder/myeloid coupling dominates state coupling; strong local state biology but weak direct druggability/tractable modulation |
| `FCGR3A` | surface_uptake_fc_complement | NO_GO | 2 | 4 | 4 | 0 | confounder/myeloid coupling dominates state coupling |
| `SORT1` | vesicle_sorting_trafficking | NO_GO | 2 | 5 | 3 | 1 | confounder/myeloid coupling dominates state coupling; strong local state biology but weak direct druggability/tractable modulation |
| `TREM2` | surface_phagocytic_lipid_receptor | NO_GO | 1 | 4 | 5 | 0 | confounder/myeloid coupling dominates state coupling |
| `CTSL` | cathepsin_protease | NO_GO | 3 | 4 | 2 | 0 | confounder/myeloid coupling dominates state coupling |
| `MSR1` | surface_phagocytic_lipid_receptor | NO_GO | 2 | 4 | 4 | 0 | confounder/myeloid coupling dominates state coupling |
| `CTSB` | cathepsin_protease | NO_GO | 3 | 3 | 2 | 0 | confounder/myeloid coupling dominates state coupling |
| `M6PR` | glycosylation_mannose6p | NO_GO | 1 | 4 | 4 | 0 | confounder/myeloid coupling dominates state coupling; strong local state biology but weak direct druggability/tractable modulation |
| `VAMP3` | vesicle_sorting_trafficking | NO_GO | 1 | 4 | 3 | 0 | confounder/myeloid coupling dominates state coupling; strong local state biology but weak direct druggability/tractable modulation |
| `LAMP1` | lysosome_membrane_or_lipid | NO_GO | 0 | 5 | 3 | 0 | confounder/myeloid coupling dominates state coupling |
| `C1QC` | surface_uptake_fc_complement | NO_GO | 1 | 3 | 2 | 0 | confounder/myeloid coupling dominates state coupling |
| `LGALS3` | galectin_glycan_checkpoint | NO_GO | 2 | 3 | 2 | 1 | confounder/myeloid coupling dominates state coupling |
| `RAB7A` | vesicle_sorting_trafficking | NO_GO | 1 | 3 | 4 | 0 | confounder/myeloid coupling dominates state coupling; strong local state biology but weak direct druggability/tractable modulation |
| `CTSD` | cathepsin_protease | NO_GO | 2 | 1 | 2 | 0 | confounder/myeloid coupling dominates state coupling |
| `LAMP2` | lysosome_membrane_or_lipid | NO_GO | 0 | 5 | 1 | 0 | confounder/myeloid coupling dominates state coupling |
| `VAMP7` | vesicle_sorting_trafficking | NO_GO | 1 | 2 | 3 | 0 | confounder/myeloid coupling dominates state coupling; strong local state biology but weak direct druggability/tractable modulation |

## Confounder Critique

- C1q/TYROBP/TREM2/APOE/GPNMB-like genes are biologically close to the original lipid-lysosomal myeloid module, but this screen treats them skeptically: if their strongest association is with `myeloid_abundance` or `lipid_loader_phagocytic` instead of residual HLA/CD74 state, they are demoted.
- Thyroid Visium has only two controls and three cases per autoimmune thyroid subgroup; it is useful spatial recurrence evidence but not robust enough alone.
- Celiac compartments are marker-derived because no curated cell labels were present in the GEO supplement; celiac results are recurrence evidence, not definitive cell-type-specific inference.
- MS GSE111972 is sorted microglia from white/grey matter, not lesion-rim spatial data; it is an independent MS myeloid validation/contradiction only.
- Residualizing against `ifn_apc_upstream` is intentionally harsh and can remove the biology of an IFN-induced antigen-presentation dependency. The primary demotion gate therefore uses the non-IFN residual model, with the IFN residual model reported separately.

## Output Files

- `results_v3/wave15_surface_trafficking_dependency/candidate_donor_scores.tsv`
- `results_v3/wave15_surface_trafficking_dependency/state_module_scores.tsv`
- `results_v3/wave15_surface_trafficking_dependency/candidate_disease_delta_tests.tsv`
- `results_v3/wave15_surface_trafficking_dependency/candidate_state_couplings.tsv`
- `results_v3/wave15_surface_trafficking_dependency/candidate_ranked.tsv`
- `results_v3/wave15_surface_trafficking_dependency/summary.json`

## Bottom Line

CTSH is the top local GO_SCOUT dependency candidate in this family screen, with residual CD74/HLA state coupling across 8 diseases and disease-control trend support across 5 diseases. This is a local expression/state-coupling nomination, not causal validation.

