# Data Manifest V3

Started: 2026-05-26 20:44 UTC

This manifest records datasets actually used or attempted in V3. Planned but
unused resources do not count as evidence.

## MS Evidence

- `GSE111972`: sorted human microglia RNA-seq, MS and control white/grey matter.
  Used by `scripts/v3_analyze_gse111972_microglia.py` for target-gene and
  module contrasts. Outputs:
  `results_v3/gse111972_module_contrasts.tsv`,
  `results_v3/gse111972_target_contrasts.tsv`,
  `results_v3/gse111972_full_ms_wm_signature.tsv`.
- `GSE279972`: MS lesion proteomics from prior execution/V2 artifact tree.
  Used through existing processed outputs under `results/`, especially
  `results/mims2_proteome_convergent_targets.tsv`.
- `GSE301908`: MS snRNA-derived MIMS2-like microglia evidence from prior
  processed outputs under `results/`.
- `GSE284005`: MS spatial MERFISH evidence from prior processed outputs under
  `results/`.

## Cross-Autoimmune Disease Screens

Existing V2 processed GEO outputs used by `scripts/v3_prioritize_module_nodes.py`
and `scripts/v3_rank_axes_from_disease_evidence.py`:

- `GSE97779`: rheumatoid arthritis macrophage expression.
- `GSE75214`: Crohn disease and ulcerative colitis intestinal mucosa.
- `GSE13355`: paired psoriasis lesional/non-lesional skin.
- `GSE32591`: lupus nephritis kidney.
- `GSE10325`: SLE sorted immune subsets.
- `GSE23117`: Sjogren minor salivary gland bulk expression.
- `GSE154609`: type 1 diabetes monocyte matrix was considered; platform
  annotation remained a blocker from V2 and is not currently counted as direct
  V3 evidence.

## Direct Single-Cell h5ad Validation

All files are public CZI h5ad downloads and are analyzed by
`scripts/v3_analyze_direct_h5ad_cell_states.py`.

- `data/raw_v3/cell_state/ibd_human_10x.h5ad`
  - local size: 175 MB
  - contents inspected: 46,700 cells, 32,354 genes; Crohn disease, ulcerative
    colitis, and normal colon; donor IDs present.
  - outputs: donor-level colon myeloid and epithelial module statistics in
    `results_v3/direct_h5ad_cell_state/`.
- `data/raw_v3/cell_state/psoriasis_skin.h5ad`
  - local size: 167 MB
  - contents inspected: 24,126 cells, 28,082 genes; psoriasis and normal skin;
    donor IDs present.
  - outputs: donor-level skin APC and keratinocyte module statistics.
- `data/raw_v3/cell_state/sjogren_salivary.h5ad`
  - source URL:
    `https://datasets.cellxgene.cziscience.com/31380664-ba9c-49d1-9961-b2bf4f7131a2.h5ad`
  - local size: 418 MB
  - contents inspected: 94,227 cells, 31,969 genes; Sjogren syndrome and normal
    labial gland; donor IDs present.
  - outputs: donor-level salivary gland APC and epithelial module statistics.
- `data/raw_v3/cell_state/t1d_hpap_islet.h5ad`
  - source URL:
    `https://datasets.cellxgene.cziscience.com/111d6e7d-d3d2-48fd-907a-4d3f8c77ee93.h5ad`
  - local size: 816 MB
  - contents inspected: 69,645 cells, 25,629 genes; type 1 diabetes mellitus
    and normal islet of Langerhans; donor IDs present; no major immune
    compartment in the exposed cell-type labels.
  - outputs: donor-level beta-cell, ductal-cell, and acinar-cell module
    statistics after adding the HPAP configs to
    `scripts/v3_analyze_direct_h5ad_cell_states.py`.
- `data/raw_v3/cell_state/ra_binvignat_blood.h5ad`
  - source URL:
    `https://datasets.cellxgene.cziscience.com/dbed890d-a14a-4502-a413-b57a4650d3af.h5ad`
  - CELLxGENE dataset ID:
    `d18736c3-6292-4379-919a-d6d973204c87`
  - publication DOI: `10.1172/jci.insight.178499`
  - local size: 256 MB; MD5 `e66d70ceffdaa99f824181d06cd76302`
  - contents inspected: 108,717 cells, 21,648 genes; 48,637 rheumatoid
    arthritis and 60,080 normal blood cells; donor IDs present.
  - used compartments: classical monocyte, non-classical monocyte, and myeloid
    dendritic cell as `ra_blood_myeloid`.
  - outputs: donor-level module and gene statistics in
    `results_v3/direct_h5ad_cell_state/`,
    `results_v3/direct_h5ad_gene_replication/`, and
    `results_v3/osmr_complement_axes/`.

## Targeted CELLxGENE Census Validation

- Perez et al. SLE PBMC dataset:
  - CELLxGENE dataset ID:
    `218acb0f-9f2f-4f76-b90b-15a4b7c7f629`
  - source h5ad version:
    `4118e166-34f5-4c1f-9eed-c64b90a3dace.h5ad`
  - source URL:
    `https://datasets.cellxgene.cziscience.com/4118e166-34f5-4c1f-9eed-c64b90a3dace.h5ad`
  - publication DOI: `10.1126/science.abf1970`
  - full source h5ad size by HTTP header: 11.3 GB; not downloaded in full.
  - Census metadata query found 1,263,676 primary blood PBMCs, including
    777,258 systemic lupus erythematosus and 486,418 normal cells.
  - Targeted selected-gene extraction is implemented in
    `scripts/v3_analyze_sle_census_targeted.py`; it samples monocyte/DC donor
    strata and materializes only V3 module genes. This route is remote and
    compute-heavy, so it is controlled in `run_v3_analysis.sh` by
    `RUN_SLE_CENSUS_TARGETED=1`.

## Spatial Tissue Validation

- `GSE248205`: autoimmune thyroid disease Visium spatial transcriptomics.
  - processed archive: `data/raw_v3/gse248205/GSE248205_Processed_data.tar.gz`
  - source URL:
    `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE248nnn/GSE248205/suppl/GSE248205_Processed_data.tar.gz`
  - local size: 159 MB; MD5 `4dcde7379df8596d24fcc119859ff154`
  - metadata: `data/raw_v3/gse248205/GSE248205_family.soft`
  - sample groups used: 2 controls, 3 Hashimoto thyroiditis, 3 Graves disease.
  - used by `scripts/v3_analyze_gse248205_thyroid_spatial.py`.
  - outputs under `results_v3/gse248205_thyroid_spatial/`.
  - caveat: Visium tissue spots, not single-cell; sample-level n is small, so
  standardized effect sizes are used only as recurrence evidence, not as
  population effect estimates.

## Marker-Derived Single-Cell Breadth Validation

- `GSE315138`: active celiac disease and healthy-control duodenal biopsy
  single-cell RNA-seq.
  - GEO raw archive:
    `data/raw_v3/gse315138/GSE315138_RAW.tar`
  - local size: 365 MB; MD5 `09b698d5e5bce143f2b38574420747cb`
  - GEO SOFT metadata:
    `data/raw_v3/gse315138/GSE315138_family.soft.gz`; PubMed ID recorded in
    SOFT: `41642982`.
  - additional supplement matrices downloaded:
    `GSE315138_Celiac-a2_matrix.mtx.gz`,
    `GSE315138_Celiac-a2_features.tsv.gz`,
    `GSE315138_Celiac-a2_barcodes.tsv.gz`,
    `GSE315138_Celiac304_matrix.mtx.gz`,
    `GSE315138_Celiac304_features.tsv.gz`,
    `GSE315138_Celiac304_barcodes.tsv.gz`.
  - used by `scripts/v3_analyze_gse315138_celiac_marker_compartments.py`.
  - outputs under `results_v3/gse315138_celiac_marker/`.
  - caveat: GEO supplement lacks curated cell annotations; V3 uses
    canonical-marker compartments. Count as recurrence/effect-size evidence,
    not atlas-grade cell-state proof.

## Perturbation Data

- Mixscale pathway Perturb-seq:
  - GEO: `GSE281048`
  - Zenodo DOI: `10.5281/zenodo.14035992`
  - local file: `data/raw_v3/mixscale/DE_results_all_pathway.zip`
  - local size: 309 MB
  - MD5 from local file: `f077cba680a1affc599f5153d99b0e45`
  - used by `scripts/v3_analyze_mixscale_perturbseq.py`
  - outputs under `results_v3/mixscale/`.

- LINCS/L1000FWD:
  - API queried by `scripts/v3_l1000fwd_reversal.py`.
  - CLUE LINCS2020 compound metadata:
    `data/raw_v3/lincs2020/compoundinfo_beta.txt`.
  - outputs:
    `results_v3/l1000fwd_reversal_hits.tsv`,
    `results_v3/l1000fwd_compound_summary.tsv`,
    `results_v3/l1000fwd_summary.json`.

- `GSE162463`: mouse macrophage IFN-gamma MHCII/CD40/PD-L1 CRISPR screen.
  - local processed file:
    `data/raw_v3/wave14_gsk3b_ciita/GSE162463_sgRNA_CountsNormalized.txt.gz`
  - SHA-256:
    `15440bdae7479121aceea530b8d617f16834dc5cd8a09b2f0ef868b825c64adb`
  - used by `scripts/v3_wave14_gsk3b_ciita_perturbation.py`.
- `GSE162464`: mouse macrophage NTC, `Gsk3b` KO, and `Med16` KO RNA-seq with
  and without IFN-gamma.
  - local processed file:
    `data/raw_v3/wave14_gsk3b_ciita/GSE162464_Normalized_Gene_Counts_Matrix.txt.gz`
  - SHA-256:
    `cae8a77b3612307e8ca68a3c2fc53cdbae9ce3c6dd9817094d0ea55c5a37f3d4`
  - used by `scripts/v3_wave14_gsk3b_ciita_perturbation.py`.
- `GSE294918`: human macrophage IFN-gamma memory/ruxolitinib RNA-seq CPM.
  - local processed file:
    `data/raw_v3/wave14_gsk3b_ciita/GSE294918_IFNyRNAseq_CPM.csv.gz`

## Wave101/Wave102 Accessible-Survivor Artifacts

- `results_v3/wave101_accessible_survivor_forcing_triage/`
  - integrates Wave94/W95/W37/W18/W62 and related prior V3 artifacts for
    `SEL1L3`, `FXYD5`, `APOC1`, `CD82`, `LAPTM5`, and other accessible
    survivors.
  - branch call: `NO_PROMOTABLE_ACCESSIBLE_SURVIVOR_YET`.
  - parked forcing candidates: `SEL1L3`, `FXYD5`, `APOC1`.
- `subagents_v3/wave101_accessible_survivor_mechanism_sidecar.md`
  - sidecar mechanism/directionality audit.
  - conclusion: no direct controller claim; keep `SEL1L3` for one residual
    test, kill `FXYD5` as an immediate target nomination, and kill `APOC1` as
    an intervention branch.
- `results_v3/wave102_accessible_survivor_residual_compartment_test/`
  - donor-level h5ad residual test across 18 direct compartments.
  - branch call: `NO_ACCESSIBLE_SURVIVOR_RESIDUAL_REOPEN`.
- `results_v3/wave102_sel1l3_fxyd5_target_specific_evidence_audit/`
  - target-specific audit for focal `SEL1L3`/`FXYD5`.
  - branch call: `NO_PROMOTABLE_SEL1L3_FXYD5_TARGET_SPECIFIC_EVIDENCE`.
- `results_v3/wave102_sel1l3_fxyd5_residual_controller_test/`
  - added controller-specific test of same-donor tissue-to-myeloid linkage.
  - branch call: `NO_REOPEN_ACCESSIBLE_SURVIVOR_AFTER_RESIDUAL_TEST`.
  - all five tested candidates (`SEL1L3`, `FXYD5`, `APOC1`, `CD82`, `LAPTM5`)
    were called `NO_GO_RESIDUAL_CONTROLLER_NOT_PROVEN`.
  - SHA-256:
    `adad09ae8edcb87f84f4275eef392a335064fa4cf6a2c5425284d195503c8b0b`
  - used as descriptive broad-JAK comparator by
    `scripts/v3_wave14_gsk3b_ciita_perturbation.py`.

## Treatment-Response Data

- `GSE253006`: ulcerative colitis biopsies before and after tofacitinib.
  - GEO title: "Differential effects of tofacitinib on macrophage activation
    contribute to lack of response in ulcerative colitis patients".
  - Raw archive: `data/raw_v3/gse253006/GSE253006_RAW.tar`.
  - Source URL:
    `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE253nnn/GSE253006/suppl/GSE253006_RAW.tar`.
  - Local size: 409 MB; MD5 `ea106b3ab755538a2c863f53b240e0f2`.
  - Metadata: `data/raw_v3/gse253006/GSE253006_family.soft`, 23 samples from
    11 UC patients, response group and timepoint available.
  - Used by `scripts/v3_analyze_gse253006_tofacitinib_uc.py`.
  - Caveat: GEO supplement exposes per-sample 10x matrices but no cell-type
    annotation file; V3 analysis is sample-level all-cell scoring and is not
    counted as cell-type-resolved proof.

## Foundation-Model Data

- Arc State released CD14 monocyte prediction/real DE files from
  `arcinstitute/ST-HVG-Parse`, split 4.
  - files used: `CD14_Mono_pred_de.csv`, `CD14_Mono_real_de.csv`, and
    `tmp_v3/var_dims_split4.pkl`.
  - used by `scripts/v3_analyze_state_parse_cd14.py`.
  - caveat: feature IDs are numeric without verified gene mapping unless
    `adata_real.h5ad` is fully downloaded and matches the 2,000-feature order.
  - output is therefore feature-agnostic cytokine-response validation, not
    gene-specific target prediction.

- Attempted but incomplete:
  - `data/raw_v3/state_parse_split4/adata_real.h5ad`, expected size 9.1 GB.
    Transfer stopped after about 1.1 GB; not used as evidence.

- Geneformer narrowed-candidate screen:
  - model: Geneformer V2-104M from `ctheodoris/Geneformer`
  - revision: `04c2b2e84da7c0f385c3f9ad8f3ec24bab6650e5`
  - local checkpoint:
    `tmp_v3/foundation_wave6/geneformer_assets/Geneformer-V2-104M`
  - script:
    `scripts/v3_wave14_geneformer_narrowed_candidate_screen.py`
  - output:
    `results_v3/wave14_geneformer_narrowed_candidate_delete/`
  - contexts: IBD myeloid/epithelial, psoriasis macrophage/dendritic, Sjogren
    APC, T1D ductal/acinar, RA classical monocyte, RA non-classical monocyte,
    RA myeloid dendritic cell.
  - caveat: custom token-deletion embedding screen, not official
    InSilicoPerturberStats; candidate-expressing disease cells are enriched and
    embedding shifts are model hypotheses only.

- Geneformer Wave15 loader/dependency deletion screen:
  - model: Geneformer V2-104M from `ctheodoris/Geneformer`
  - revision: `04c2b2e84da7c0f385c3f9ad8f3ec24bab6650e5`
  - local checkpoint:
    `tmp_v3/foundation_wave6/geneformer_assets/Geneformer-V2-104M`
  - script:
    `scripts/v3_wave15_geneformer_loader_dependency_screen.py`
  - output:
    `results_v3/wave15_geneformer_loader_dependency_delete/`
  - contexts: IBD myeloid/epithelial, psoriasis macrophage/dendritic, Sjogren
    APC, T1D ductal/acinar, RA classical monocyte, RA non-classical monocyte,
    and RA myeloid dendritic cell.
  - caveat: custom token-deletion embedding screen; quantitative outputs are
    foundation-model hypotheses and require real perturbation validation.

## Target And Prior-Art Resources

- OpenTargets candidate disease hits:
  `results_v3/opentargets_candidate_disease_hits.tsv`.
- OpenTargets Wave15 loader external gate:
  `results_v3/wave15_loader_external_gate/open_targets_gwas_credible_sets.tsv`
  and `literature_v3/wave15_loader_external_gate_detail.json`.
- Intervention/prior-art audit:
  `results_v3/intervention_prior_art_audit.tsv` and
  `literature_v3/intervention_prior_art_audit_detail.json`.
- Subagent novelty/prior-art reports preserved under `subagents_v3/`, especially
  `cd74_mif_novelty_galileo_report.md`.

## Wave15 Local Dependency And Perturbation Screens

- Surface/trafficking dependency family screen:
  - script: `scripts/v3_wave15_surface_trafficking_dependency.py`
  - output: `results_v3/wave15_surface_trafficking_dependency/`
  - candidate families: HLA loading chaperones, cathepsins, vesicle trafficking,
    glycosylation, galectins, Fc/complement uptake, lysosomal lipid handling,
    and myeloid marker controls.
  - statistical unit: donor/sample or sample-level spatial aggregate; cells are
    not treated as independent replicates.
  - caveat: celiac compartments are marker-derived and thyroid Visium uses few
    case/control samples.

- Orchestrator CTSH/local dependency fail-fast scan:
  - script: `scripts/v3_wave15_orchestrator_dependency_scan.py`
  - output: `results_v3/wave15_orchestrator_dependency_scan/`
  - purpose: re-rank loader/dependency candidates after residualizing state
    coupling against myeloid, generic NF-kappaB, lipid-loader/phagocytic, and
    IFN/APC upstream modules where available.

- Wave15 perturbation/drug-response comparator screen:
  - script: `scripts/v3_wave15_perturbation_drug_response.py`
  - output: `results_v3/wave15_perturbation_drug_response/`
  - inputs include local Mixscale IFN-gamma CRISPRi, GSE162464 knockout RNA-seq,
    GSE294918 IFN-gamma/ruxolitinib macrophage RNA-seq, and local L1000FWD
    reversal outputs.
  - caveat: this produced comparator evidence only; no compound was considered
    strong enough for nomination from this channel alone.

- Wave16 CTSH ChEMBL feasibility audit:
  - script: `scripts/v3_wave16_ctsh_chembl_feasibility.py`
  - output: `results_v3/wave16_ctsh_chembl_feasibility/`
  - ChEMBL targets: CTSH `CHEMBL2225`, CTSS `CHEMBL2954`, CTSB `CHEMBL4072`,
    CTSL `CHEMBL3837`, CTSK `CHEMBL268`, CTSZ `CHEMBL4160`.
  - purpose: quantify public bioactivity depth and observed cross-cathepsin
    overlap for CTSH feasibility.
  - caveat: public ChEMBL absence of comparator data is not proof of selectivity;
    output is a feasibility screen, not medicinal-chemistry validation.

- Wave16 CTSH chemistry/selectivity audit:
  - script: `scripts/v3_wave16_ctsh_chemistry_selectivity.py`
  - output: `results_v3/wave16_ctsh_chemistry_selectivity/`
  - sources: ChEMBL, IUPHAR/GtoPdb, UniProt, AlphaFold DB, RCSB PDB.
  - key result: 47 CTSH potency molecules were retained from ChEMBL; 41 had at
    least one requested cathepsin comparator assay; 0 had an observed 100x
    margin over all assayed comparators and only 1 had an observed 10x margin.
  - caveat: the audit is a public-chemistry tractability screen. It does not
    prove no selective CTSH chemistry can exist, but it blocks a public-data
    therapeutic nomination.

- Wave17 Mediator/CDK8-CDK19 translational gate:
  - script: `scripts/v3_wave17_mediator_route_gate.py`
  - output: `results_v3/wave17_mediator_route_gate/`
  - local perturbation input:
    `results_v3/wave15_perturbation_drug_response/ranked_direct_perturbations.tsv`.
  - local expression inputs:
    `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv` and
    `results_v3/wave14_gsk3b_local_gate/gsk3b_local_gate_gene_summary.tsv`.
  - ChEMBL targets: CDK8 `CHEMBL5719`, CDK19 `CHEMBL6002`,
    CDK8/Cyclin C `CHEMBL3038474`, CDK19/Cyclin C `CHEMBL3883323`,
    CDK8/CDK19 family `CHEMBL3885556`.
  - purpose: test whether the strong `Med16_KO` perturbation comparator can be
    translated into druggable Mediator kinase pharmacology.
  - caveat: output parks the route; it does not demonstrate CDK8/CDK19 inhibitor
    phenocopy in autoimmune APCs.

- GSE253006 marker-compartment tofacitinib response analysis:
  - script: `scripts/v3_analyze_gse253006_tofacitinib_marker_compartments.py`
  - output: `results_v3/gse253006_tofacitinib_marker/`
  - input: extracted GEO raw 10x-style matrices and `GSE253006_family.soft`.
  - cells/samples: 97,004 cells from 23 samples; 11 baseline samples, 5
    responders and 6 nonresponders.
  - purpose: reformulate the weaker sample-level UC tofacitinib analysis into
    marker-derived compartments before testing V3 modules.
  - caveat: compartments are marker-derived because GEO metadata did not
    include curated cell labels. Baseline response tests are underpowered and no
    module reached FDR significance.

- `GSE227835`: human PBMC single-cell RNA-seq from myasthenia gravis patients
  and controls.
  - GEO title: "Single-cell RNA-seq data of human PBMC from Myasthenia Gravis
    patients".
  - local raw/metadata directory: `data/raw_v3/gse227835/`.
  - script: `scripts/v3_wave14_gse227835_myasthenia_marker.py`.
  - output: `results_v3/wave14_gse227835_myasthenia/`.
  - sample groups: 10 AChR-positive MG, 10 healthy controls, 10 seronegative MG
    pre-treatment, 10 paired seronegative MG post-treatment.
  - caveat: GEO provides sample labels but not curated cell labels; all cell
    compartments are marker-derived PBMC compartments. This dataset supports
    lysosomal/APC breadth in MG but contradicts a simple universal HLA-II/CD74
    mechanism in seronegative pre-treatment B/APC-like and plasmablast-like
    compartments.

## Blocked Or Downscoped Data Routes

- Evo 2 local inference: blocked by macOS CPU/no CUDA and no hosted credentials.
- CELLxGENE Census expression extraction: metadata access worked, but selected
  expression materialization stalled or failed. Direct h5ad downloads were used
  instead.
- De novo State inference: blocked because compatible input AnnData in the
  trained feature space was not available.
- RA synovium/macrophage `E-MTAB-8322.project.h5ad`: selected as high-value
  disease-breadth validation, but HTTPS and directory-list requests to
  `ftp.ebi.ac.uk` timed out before data transfer. The route is preserved for
  later retry and was replaced locally by `GSE248205` thyroid spatial analysis.

- Wave18 treatment-response scout:
  - script: `scripts/v3_wave18_treatment_response_scout.py`
  - output: `results_v3/wave18_treatment_response/`
  - report: `subagents_v3/wave18_treatment_response_scout.md`
  - accessions scouted: `GSE253006`, `GSE138746`, `GSE183047`, `GSE261334`,
    `GSE296117`, `GSE250453`, `GSE235357`.
  - downloaded inputs:
    `data/raw_v3/wave18_gse138746/GSE138746_Counts_Normalization_PBMC.csv.gz`,
    `data/raw_v3/wave18_gse138746/GSE138746_Counts_Normalization_cd14.csv.gz`,
    `data/raw_v3/wave18_gse138746/GSE138746_Counts_Normalization_cd4.csv.gz`,
    `data/raw_v3/wave18_gse183047/GSE183047_RAW.tar`,
    `data/raw_v3/wave18_gse183047/GSE183047_family.soft.gz`.
  - key result: no corrected baseline response predictor in RA anti-TNF or UC
    tofacitinib; psoriasis secukinumab and UC tofacitinib provide only weak
    pharmacodynamic comparator evidence.

- Wave18 accessible/druggable state-component rescue:
  - script: `scripts/v3_wave18_accessible_target_rescue.py`
  - output: `results_v3/wave18_accessible_target_rescue/`
  - report: `subagents_v3/wave18_accessible_target_rescue.md`
  - sources: local V3 recurrence/state tables, local OpenTargets snapshots,
    Europe PMC query counts, ClinicalTrials.gov keyword counts, ChEMBL target
    and activity counts, Google Patents query URLs.
  - key result: 24 candidates screened; `0 GO`, `11 PARK`, `13 NO_GO`.

- Wave18 foundation-model rescue:
  - script: `scripts/v3_wave18_foundation_rescue.py`
  - output: `results_v3/wave18_foundation_rescue/`
  - report: `subagents_v3/wave18_foundation_rescue.md`
  - sources: existing Geneformer deletion screens, State parse-status outputs,
    and real perturbation readouts from Wave15.
  - key result: no candidate met strict stronger-than-CTSH Geneformer support
    plus direct real perturbation rescue.

- Wave19 orchestrator controller triage:
  - script: `scripts/v3_wave19_orchestrator_controller_triage.py`
  - output: `results_v3/wave19_orchestrator_controller_triage/`
  - sources: local V3 broad h5ad gene rank, Wave15 surface/dependency tables,
    Wave18 foundation and accessible-target tables, OpenTargets local genetic
    snapshot, and central-node first-pass rank.
  - key result: among 69 checkpoint, lysosomal/lipid-controller, SHP/SOCS/JAK,
    NRF2, and nuclear lipid-sensor genes, `LIPA`, `CD274`, and `NPC1` were
    parked for worker review; no candidate was promoted for immediate follow-up.

- Wave20 orchestrator unrestricted survivor triage:
  - script: `scripts/v3_wave20_orchestrator_unrestricted_triage.py`
  - output: `results_v3/wave20_orchestrator_unrestricted_triage/`
  - sources: `results_v3/unrestricted_survivor_scan/`, broad residual gate,
    Geneformer broad residual summaries, Wave18 foundation synthesis, local
    ChEMBL activity summary, and target-level genetics snapshot.
  - key result: `DAP`, `SNX10`, `FMNL2`, `C15ORF48`, and `CBX3` were parked for
    worker review; none had an immediate druggability/perturbation package.

- Wave20 `C15ORF48/MOCCI` complex-IV switch test:
  - script: `scripts/v3_wave20_c15orf48_ndufa4_switch.py`
  - output: `results_v3/wave20_c15orf48_ndufa4_switch/`
  - sources: local broad h5ad gene contrasts plus MS white-matter microglia
    contrasts.
  - key result: 17 compartments tested; only Crohn colon myeloid showed the
    canonical `C15ORF48`-up/`NDUFA4`-down pattern, and `NDUFA4` repression was
    nominal but not FDR-significant. UC and T1D compartments showed
    `C15ORF48` induction without the reciprocal `NDUFA4` decrease. The branch
    is therefore not promoted as a broad autoimmune complex-IV subunit-switch
    mechanism.

- Wave19 lysosomal/lipid-controller audit:
  - script: `scripts/v3_wave19_lysosomal_controller.py`
  - output: `results_v3/wave19_lysosomal_controller/`
  - report: `subagents_v3/wave19_lysosomal_controller.md`
  - sources: local V3 recurrence/state tables, Geneformer/foundation summaries,
    ChEMBL/clinical/prior-art source log, and disease-mechanism sources listed
    in `source_log.tsv`.
  - key result: no upstream lysosomal/lipid controller promoted. `LIPA`,
    `NPC1/NPC2`, and `LRRK2` remain parked/readout or disease-specific branches;
    TFEB/TFE3, TRPML1, PIKFYVE, PPAR/LXR/ABCA1/ABCG1, GBA/GBA2, and generic
    mTOR/autophagy routes are no-go under the V3 gates.

- Wave19 tolerogenic/checkpoint-controller audit:
  - script: `scripts/v3_wave19_tolerogenic_checkpoint.py`
  - output: `results_v3/wave19_tolerogenic_checkpoint/`
  - report: `subagents_v3/wave19_tolerogenic_checkpoint.md`
  - sources: local recurrence/residual/foundation/perturbation tables plus
    Europe PMC, PubMed, preprint, ClinicalTrials.gov, ChEMBL, and Google
    Patents query URLs cached in `external_prior_art_query_log.tsv`.
  - key result: 29 checkpoint candidates screened; `0 PROMOTE`, `5 PARK`,
    `6 PARK_LOW`, `18 NO_GO`. `CD274`, `CD24`, `BTLA`, `CD200`, and `CD47`
    remain comparator axes only, not V3 therapeutic nominations.

- Wave20 unrestricted survivor stress test:
  - script: `scripts/v3_wave20_unrestricted_survivor.py`
  - output: `results_v3/wave20_unrestricted_survivor/`
  - report: `subagents_v3/wave20_unrestricted_survivor.md`
  - sources: local unrestricted survivor tables, broad residual gates,
    Geneformer screens, ChEMBL/UniProt lookups, and public source/query tables
    in `wave20_public_search_queries.tsv` and `wave20_source_links.tsv`.
  - key result: no survivor promoted. `SNX10` is retained only as the
    least-bad fail-fast comparator; the remaining candidates fail residual,
    perturbation/model, modality, safety/repair, or prior-art gates.

- Wave20 genetic/druggable alternate-axis scout:
  - script: `scripts/v3_wave20_genetic_druggable_altaxis.py`
  - output: `results_v3/wave20_genetic_druggable_altaxis/`
  - report: `subagents_v3/wave20_genetic_druggable_altaxis.md`
  - sources: local OpenTargets credible-set snapshot, target-level genetics
    truth table, broad h5ad gene ranks, disease-axis ranks, ChEMBL activity
    summary, Europe PMC, ClinicalTrials.gov, ChEMBL API, and curated public
    source interpretations.
  - key result: no genetically anchored, druggable alternate axis promoted.
    `PTPN2`, `SH2B3`, `CLEC16A`, `ATG16L1`, `OSMR`, `GPR65`, `IRF5`, `CARD9`,
    `IL10`, `TNFAIP3`, `IL6R`, and `TYK2` all fail at least one hard gate.

- Wave21 residual-druggability scan:
  - script: `scripts/v3_wave21_residual_druggability_scan.py`
  - output: `results_v3/wave21_residual_druggability_scan/`
  - sources: local residual/broad expression/genetics/prior-demotion tables,
    ChEMBL target/activity API, and UniProt REST API with cached raw responses
    under `raw_api/`.
  - key result: the final Wave21-A worker version scanned 26 strict-residual
    candidates; `SQLE` is `GO_REVIEW` only for hostile novelty/modality review,
    not target promotion. `LDLRAD3`, `C1QTNF1`, `TGM2`, `REG1A`, and `PTPRE`
    are parked for review; 20 candidates are no-go.

- Wave21 residual-candidate prior-art/modality review:
  - output: `results_v3/wave21_residual_candidate_prior_art/`
  - report: `subagents_v3/wave21_residual_candidate_prior_art.md`
  - sources: PubMed, Europe PMC, Europe PMC preprints, ClinicalTrials.gov,
    Google Patents, ChEMBL, and UniProt with 126 exact source-query rows and raw
    captures.
  - key result: no candidate promoted. `SQLE` is conditional stress-test
    comparator only; `CFB`, `IL15`, `IL7R`, `CXCL8`, and `HIF1A` are
    comparator-only prior-art/generic-modality failures.

- Wave22 SQLE fail-fast:
  - script: `scripts/v3_wave22_sqle_failfast.py`
  - output: `results_v3/wave22_sqle_failfast/`
  - sources: broad h5ad rank, broad residual-gate summary and residual tests,
    Wave18 foundation rescue, Wave18 direct perturbation/readout concordance,
    Geneformer broad residual deletion output, Wave21 prior-art review, LINCS
    `compoundinfo_beta.txt`, and existing L1000FWD reversal/selectivity tables.
  - key result: `SQLE` is `NO_GO_SQLE_FAILFAST`. It is broad-positive in 4
    diseases but strict residual survival is Crohn/UC stromal only, MS
    white-matter trend is negative, Geneformer triage is contradicted by the
    GSE162463 screen, SQLE-inhibitor names do not appear in existing L1000
    disease-reversal outputs, and prior art remains blocking.

- Wave23 orchestrator non-expression route triage:
  - script: `scripts/v3_wave23_orchestrator_nonexpression_axis_triage.py`
  - output: `results_v3/wave23_orchestrator_nonexpression_axis_triage/`
  - sources: local broad h5ad and residual-gate outputs, OpenTargets credible
    sets, Wave14 gate matrix, Wave18 foundation rescue, Wave15 perturbation
    synthesis, L1000FWD compound summaries, Wave20 genetic alternate-axis
    output, Wave18 treatment-response tables, and ChEMBL API target/activity
    snapshots cached under `raw_api/`.
  - key result: 16 route-level hypotheses and 56 genes were checked. Corrected
    calls: `2 PARK_REVIEW`, `14 NO_GO`, `0 GO_REVIEW`. Parked routes are
    `GPR65_pH_endolysosomal_gpcr` and `PTPN2_TCPTP_restoration`; neither is a
    target nomination. The baseline response biomarker route was demoted after
    the treatment-response gate was tightened to corrected baseline signals.

- Wave23 genetics-first restoration modality scout:
  - script: `scripts/v3_wave23_genetics_restoration_modality.py`
  - output: `results_v3/wave23_genetics_restoration_modality/`
  - report: `subagents_v3/wave23_genetics_restoration_modality.md`
  - sources: local OpenTargets credible sets, Wave20 genetic alternate-axis
    outputs, Wave14 target-level genetics table, broad h5ad rank, Wave15
    perturbation synthesis, druggability tables, and curated public source
    interpretation links.
  - key result: `0 GO`, `2 PARK`, `12 NO_GO`. `GPR65` and `IL10` are parked as
    feasible-modality but prior-art/local-evidence-blocked branches. `PTPN2`,
    `SH2B3`, `TNFAIP3`, `CLEC16A`, `ATG16L1`, and related genetics anchors fail
    restoration-modality gates.

- Wave24 L1000 recurrent reversal triage:
  - script: `scripts/v3_wave24_l1000_recurrent_reversal_triage.py`
  - output: `results_v3/wave24_l1000_recurrent_reversal/`
  - sources: V3 L1000FWD compound summary, Wave15 L1000 selectivity table, and
    PDE4/cAMP L1000 audit.
  - key result: no repurposing candidate promoted. Among 123 grouped compounds,
    20 recur across at least two opposite-mode queries, but known recurrent
    hits are cytotoxic/stress, oncology, steroid, or generic/prior
    inflammatory mechanisms. Unknown BRD compounds are parked only for
    deconvolution and cannot support a therapeutic claim.

- Wave23 hostile critique:
  - report: `subagents_v3/wave23_hostile_critique.md`
  - sources: local Wave22/Wave23/Wave20 outputs and report files.
  - key result: no target; accepted critique that `GPR65`, `PTPN2`, and the
    biomarker route remain weak. The non-redundant next route is
    target-resolved causal genetics to module state.

- Wave23 metabolite/barrier circuit scout:
  - script: `scripts/v3_wave23_metabolite_barrier_circuit.py`
  - output: `results_v3/wave23_metabolite_barrier_circuit/`
  - report: `subagents_v3/wave23_metabolite_barrier_circuit.md`
  - sources: local broad h5ad/residual outputs, OpenTargets credible sets,
    Wave19 PPAR/LXR demotion outputs, L1000FWD compound summaries, LINCS
    compound metadata, and public API snapshots from ChEMBL, EuropePMC, and
    ClinicalTrials.gov.
  - key result: 7 metabolite/barrier route classes audited; all `NO_GO`.
    AHR/tryptophan has the closest biology but no strict residual/genetic/L1000
    support. FXR/TGR5 is least crowded but locally unsupported.

- Wave25 target-resolved genetics-to-module proxy audit:
  - script: `scripts/v3_wave25_causal_genetics_module_proxy.py`
  - output: `results_v3/wave25_causal_genetics_module_proxy/`
  - sources: Wave14 target-level genetics table, GWAS Catalog mapped-gene top
    associations, OpenTargets credible-set snapshots, broad h5ad gene rank,
    broad residual-gate summary, Wave18 foundation/perturbation synthesis,
    Wave23 route/restoration/metabolite outputs, and Wave24 L1000 recurrence
    output.
  - key result: 206 candidates audited; `0` candidates have proper coloc/MR
    feasibility. `PTPN2` is `COLOC_NEEDED_NOT_CLAIMABLE`; 14 genes are module
    markers without genetic anchoring; 191 are `NO_GO_CAUSAL_PROXY`.
  - data audit: `tmp_v3/gwascatalog_associations_20260317_convert.parquet` is
    readable with 1,067,194 rows and 38 columns, but it is a top-association
    catalog schema, not SNP-level summary statistics sufficient for coloc/MR.

- Wave26 strict treatment-response biomarker audit:
  - script: `scripts/v3_wave26_treatment_response_strict_audit.py`
  - output: `results_v3/wave26_treatment_response_strict_audit/`
  - sources: Wave23 treatment-response baseline, pharmacodynamic, and ranked
    call tables.
  - key result: no treatment-response biomarker claim survives. The prior
    `GSE138746` RA anti-TNF `CD4_T_cell` `ifn_apc` `GO` row is demoted because
    global baseline FDR is 0.773794, global generic-adjusted FDR is 0.971730,
    and no independent same-module/direction replication exists.

- Wave27 L1000 unknown perturbagen deconvolution:
  - script: `scripts/v3_wave27_l1000_unknown_deconvolution.py`
  - output: `results_v3/wave27_l1000_unknown_deconvolution/`
  - sources: Wave24 recurrent L1000 compound triage and LINCS 2020
    `compoundinfo_beta.txt`.
  - key result: 62 unknown parked compounds audited; 61 are `NO_GO`, 1 remains
    alias-only external-lookup parked. Six recurrent unknowns deconvolve to
    purine/cAMP, Aurora kinase, prostanoid, natural-product, or unresolved BRD
    chemistry; none supplies a selective autoimmune intervention point.

- Wave28 target-first rescue audit:
  - script: `scripts/v3_wave28_target_first_rescue.py`
  - output: `results_v3/wave28_target_first_rescue/`
  - sources: Wave20 genetic/druggable alternate-axis output, Wave21 residual
    druggability output, Wave18 accessible-target rescue, Wave25 genetics proxy
    matrix, Wave18 foundation rescue, Wave15 direct perturbation synthesis,
    Wave24 L1000 recurrence output, central/intervention rank, local ChEMBL
    target-activity summary, Europe PMC API, ChEMBL API, and ClinicalTrials.gov
    API v2 with `countTotal=true`.
  - key result: 26 target-first candidates audited; 0 promoted, 1 parked
    (`SQLE`), 25 no-go. `SQLE` is parked only because residual/module evidence
    and druggability exist while target-level genetics and perturbation evidence
    are absent. `PTPN2` remains the strongest comparator but fails
    correct-direction modality and prior-art gates.

- Wave29 PTPN2 restoration model:
  - script: `scripts/v3_wave29_ptpn2_restoration_model.py`
  - output: `results_v3/wave29_ptpn2_restoration_model/`
  - sources: assumption-explicit ODE model seeded at `20260527`; no new
    external data. It uses V3-derived biological context from Wave25/Wave28 but
    the numerical model itself is simulated and labeled as such.
  - key result: no simulated intervention reaches the predefined selective
    therapeutic window. `ptpn2_restore_to_125pct` has median APC/lipid-module
    drop 0.130 and median host-defense drop 0.365; selective-window fraction
    0.0. This demotes PTPN2 restoration to a mechanism benchmark until real
    perturbation and coloc/MR data exist.

- Wave30 upstream niche-driver audit:
  - script: `scripts/v3_wave30_niche_driver_audit.py`
  - output: `results_v3/wave30_niche_driver_audit/`
  - public API cache: `results_v3/wave30_niche_driver_audit/raw_api/`
  - sources: V3 axis/gene convergence tables, Wave15 dependency and
    perturbation outputs, Wave18 accessible/foundation outputs, Wave19
    checkpoint and lysosomal-controller outputs, Wave23 nonexpression-axis
    triage, Wave25 genetics proxy matrix, Wave28 target-first rescue output,
    Europe PMC API, ChEMBL API, and ClinicalTrials.gov API v2.
  - key result after reformulation: 18 upstream/niche axes audited; 0 promoted,
    4 called `CENTRAL_STATE_DRIVER_NOT_SELECTIVE_THERAPEUTIC`, and 14 called
    `NO_GO_NICHE_DRIVER`. The script now separates candidate-specific breadth
    from global module breadth after an initial run inflated generic IFN/APC
    axes. Corrected central-state drivers are `IFNG_IFNGR_JAK_STAT1_CIITA`,
    `MIF_CD74_CXCR4_CD44`, `LILRB_HLA_INHIBITORY_MYLOID_CHECKPOINT`, and
    `SPP1_CD44_INTEGRIN_RETENTION`; none passes selectivity, prior-art,
    causality, and modality gates as a therapeutic target.

- Wave31 dynamic transition-controller audit:
  - script: `scripts/v3_wave31_dynamic_transition_controller_audit.py`
  - output: `results_v3/wave31_dynamic_transition_controller_audit/`
  - sources: Wave15 direct perturbation/drug-response outputs, Wave17 Mediator
    route verdict, Wave24 recurrent L1000 audit, Wave25 causal genetics/module
    proxy matrix, Wave28 target-first rescue output, and Wave14 cross-disease
    local gene summary.
  - key result: 17 candidates audited; 0 promoted. `MED16` is the strongest
    selective perturbation comparator in primary mouse macrophages
    (`target_suppression=3.14`, `generic_ifn_suppression=0.80`,
    `margin=2.34`) but is not directly druggable and lacks a validated
    therapeutic phenocopy. `CDK8_CDK19_MEDIATOR_KINASE` and `GSK3B` are parked
    but blocked by missing phenocopy/cross-disease support/prior art. L1000
    kinase and stress/proteostasis hits are not promotable as immune-cell
    transition controllers.

- Wave32-A cross-autoimmune efferocytosis/lipid-clearance target scan:
  - report: `WAVE32A_EFFEROCYTOSIS_RESOLUTION_SCAN.md`
  - sources: local V3 Wave32 resolution-rescue audit, Wave23
    metabolite/barrier candidate evidence, Wave19 lysosomal route summary,
    Wave18 accessible-target rescue, broad h5ad gene summaries, plus targeted
    PubMed/PMC/publisher/FDA/NICE web searches for `FPR2/ANXA1`, `MERTK/TAM`,
    `TREM2/APOE/LPL`, `LIPA/NPC1/NPC2`, `GPNMB`, `CD300`, and PPAR/LXR/retinoid
    axes.
  - key result: no target promoted. Best follow-up branch is biased
    `FPR2/ALX` pro-resolution agonism because it has local Crohn/UC myeloid
    `FPR2` signal and direct colitis efferocytosis pharmacology, but it lacks
    an MS anchor and is not a final V3 finding. `MERTK/TAM` is mechanistically
    broad but lacks mature correct-direction agonist modality; `TREM2/APOE` is
    the strongest MS repair comparator but remains parked by conflicting
    agonist-antibody evidence and marker/confounder-dominated cross-autoimmune
    support.

- Wave32 downstream-resolution rescue audit:
  - script: `scripts/v3_wave32_resolution_rescue_audit.py`
  - output: `results_v3/wave32_resolution_rescue_audit/`
  - public API cache: `results_v3/wave32_resolution_rescue_audit/raw_api/`
  - sources: local V3 gene/cell-state/residual/surface/foundation/checkpoint/
    lysosomal/genetics/target-first/perturbation outputs plus Europe PMC,
    ClinicalTrials.gov, and ChEMBL snapshots.
  - key result: 14 routes audited; 0 promoted. `TREM2_APOE_LIPID_REPAIR` is the
    only parked branch and fails causal/perturbation, prior-art, density, and
    independent-validation gates. `NPC1_NPC2_CHOLESTEROL_EGRESS` is the highest
    numeric route but no-go because it is a state/readout pattern, not a
    validated intervention. TAM/MERTK, LIPA, LXR/ABCA1, PPAR/RXR, GPNMB,
    CD200/CD300, SIRPA/CD47, IL10, NRF2, and MAF/KLF4 routes do not meet the V3
    therapeutic package.

- Wave32-C resolution-axis prior-art/translational feasibility audit:
  - script: `scripts/v3_wave32c_resolution_prior_art_audit.py`
  - output: `results_v3/wave32c_resolution_prior_art_audit/`
  - curated report: `WAVE32C_PRIOR_ART_AUDIT.md`
  - sources: PubMed E-utilities, Europe PMC REST search, ClinicalTrials.gov API
    v2, ChEMBL target/molecule APIs, PubChem PUG compound lookup, Google
    Patents search URLs and sampled patent pages, and Espacenet search URLs.
    Espacenet returned HTTP 403 in this runtime.
  - scale: 70 source queries, 146 target/drug database rows, 46 patent-search
    URLs.
  - correction: the initial `AL002 TREM2` ClinicalTrials.gov query was too
    restrictive; `AL002` and `INVOKE-2` were added and the script rerun.
  - key result: least blocked but not claim-ready route is biased
    `FPR2`/specialized-pro-resolving mediator agonism; `CD300` family
    modulation has whitespace but unacceptable direction ambiguity without
    receptor-specific perturbation data. `TREM2`, generic `LXR/ABCA1`,
    `PPAR/RXR/retinoid`, `TAM` inhibition, and `GPNMB` depletion/ADC routes are
    blocked or wrong-direction. `NPC1/NPC2`, `LIPA/LAL`, `TAM` agonism, and
    non-depleting `GPNMB` remain insufficient rather than promotable.

- Wave32-B perturbation/dataset availability scan:
  - report: `subagents_v3/wave32b_perturbation_dataset_availability_scan.md`
  - matrix: `results_v3/wave32b_dataset_availability_scan/candidate_dataset_matrix.tsv`
  - sources: GEO DataSets E-utilities, GEO FTP series directories and series
    matrices, ArrayExpress/BioStudies search API, local LINCS2020 compound
    metadata, previous V3 L1000 outputs, previous V3 Mixscale/perturbation
    outputs, and local State/Geneformer availability notes.
  - scale: 32 rows; 15 primary or primary-screen datasets/resources for
    immediate local testing.
  - strongest primary datasets: `GSE156234`, `GSE212008`, `GSE169160`,
    `GSE253577`, `GSE325329`, `GSE325042`, `GSE302857`, `GSE100260`,
    `GSE243117`, `GSE285961`, `GSE274954`, `GSE254406`, `GSE273340`,
    `GSE254572`, and `GSE287142`.
  - key result: enough public perturbation data exists to run a stricter
    resolution/efferocytosis analysis. `CD300*` and clean direct
    `AXL/TYRO3/PROS1` macrophage perturbation transcriptomes were not found;
    LINCS/CMap and foundation-model outputs are low-weight triage only.

- Wave34-A genetics-first target rescue:
  - script: `scripts/v3_wave34a_genetics_first_target_rescue.py`
  - report: `subagents_v3/wave34a_genetics_first_target_rescue.md`
  - outputs: `results_v3/wave34a_genetics_first_target_rescue/`
  - local sources: `tmp_v3/wave13_opentargets_gwas_credible_sets.tsv`,
    `tmp_v3/wave11_opentargets_target_disease_scores.tsv`,
    `tmp_v3/gwascatalog_associations_20260317_convert.parquet`,
    `results_v3/wave14_target_level_genetics/target_level_genetics_truth_table.tsv`,
    `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`,
    `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`,
    `results_v3/wave20_genetic_druggable_altaxis/`,
    `results_v3/wave23_genetics_restoration_modality/`,
    `results_v3/wave25_causal_genetics_module_proxy/`,
    `results_v3/wave28_target_first_rescue/`, and
    `results_v3/wave33_tolerance_costimulation_audit/`.
  - public sources: ChEMBL target/activity API, GTEx Portal gene and
    single-tissue eQTL APIs, Europe PMC search API, and ClinicalTrials.gov API
    v2; raw lookup cache in
    `results_v3/wave34a_genetics_first_target_rescue/raw_api/`.
  - scale: `23` candidates, `15,875` local GWAS Catalog autoimmune rows.
  - key result: no promoted target; parked candidates are `IRF5`, `IL10`,
    `PTPN22`, `FAP`, `GPR65`, `CCR6`, and `TNFRSF14`; `CD226` is demoted under
    the strict local credible-set/eQTL/cell-state gate despite broad weak GWAS
    Catalog mapped-gene signal.

- Wave35 corrected resolution perturbation analysis:
  - script: `scripts/v3_wave35_resolution_perturbation_analysis.py`
  - outputs: `results_v3/wave35_resolution_perturbation/`
  - correction: failed Ensembl REST calls had previously been cached as empty
    mappings, causing artificially low module coverage in Ensembl-indexed
    perturbation datasets.
  - added source: MyGene.info exact-symbol fallback for mouse Ensembl mapping,
    cached under `results_v3/wave35_resolution_perturbation/raw_api/`.
  - corrected coverage in Ensembl-indexed perturbation datasets: 28/28
    resolution genes, 21/27 lipid/APC genes, 13/15 IFN genes, 11/11 stress
    genes, and 6/7 fibrosis genes.
  - key result: 10 perturbation datasets, 29 contrasts, 145 module-contrast
    rows, and `0` strict controller-like perturbation contrasts.

- Wave37 direct efferocytosis CRISPR screen:
  - script: `scripts/v3_wave37_gse212008_crispr_efferocytosis_screen.py`
  - outputs: `results_v3/wave37_gse212008_crispr_efferocytosis_screen/`
  - accession: `GSE212008`
  - downloaded files:
    - `data/raw_v3/gse212008/GSE212008_RAW_sgRNA_counts.txt.gz`
    - `data/raw_v3/gse212008/GSE212008_family.soft.gz`
  - biological system: murine bone-marrow-derived macrophage pooled CRISPR
    knockout screen sorted into efficient eaters, non-eaters, and input
    fractions.
  - scale: 74,674 sgRNAs and 19,672 genes.
  - key result: 214 permissive KO-enhances-efferocytosis candidates and 54
    permissive KO-impairs-efferocytosis candidates. Canonical resolution
    candidates did not rescue the route.

- Wave38 CRISPR-state-druggability rescue:
  - script: `scripts/v3_wave38_crispr_state_druggability_rescue.py`
  - outputs: `results_v3/wave38_crispr_state_druggability_rescue/`
  - inputs: Wave37 gene-level screen scores,
    `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`,
    `results_v3/wave34_genetics_expression_druggability_scan/`, ChEMBL
    target/activity API, Europe PMC query counts, and ClinicalTrials.gov query
    counts.
  - scale: 184 screen-derived candidates.
  - key result: 184 `NO_GO_CRISPR_RESCUE`; 0 promoted. The superficially
    tractable `FCGRT` KO-enhancer failed disease-state direction, MS-anchor,
    and prior-art gates.

- Wave39 accessibility-first surfaceome rescue:
  - script: `scripts/v3_wave39_surfaceome_rescue_after_resolution_pivot.py`
  - outputs: `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/`
  - inputs: `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`,
    `results_v3/wave15_surface_trafficking_dependency/candidate_ranked.tsv`,
    `results_v3/wave18_accessible_target_rescue/`,
    `results_v3/wave21_residual_druggability_scan/`,
    `results_v3/wave21_residual_candidate_prior_art/`,
    `results_v3/wave25_causal_genetics_module_proxy/`,
    `results_v3/wave34_genetics_expression_druggability_scan/`, and
    `results_v3/wave38_crispr_state_druggability_rescue/`.
  - public sources: UniProt REST API, ChEMBL target/activity API, Europe PMC
    REST search API, and ClinicalTrials.gov API v2. Raw API cache:
    `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/raw_api/`.
  - scale: 224 broad recurrent candidates, 224 UniProt lookups, 90 ChEMBL
    target/activity lookups, and 60 Europe PMC/ClinicalTrials.gov prior-art
    lookups.
  - correction: the initial accessibility classifier falsely promoted `PSMA3`
    because incidental annotation text caused a proteasome core subunit to be
    treated as accessible. The script was patched to restrict accessibility to
    subcellular-location/feature evidence and to hard-exclude proteasome core
    machinery.
  - corrected key result: 0 `GO_REVIEW`, 6 `PARK_REVIEW`, and 218
    `NO_GO_SURFACEOME_RESCUE`.

- Wave40 parked surface fail-fast:
  - script: `scripts/v3_wave40_parked_surface_failfast.py`
  - outputs: `results_v3/wave40_parked_surface_failfast/`
  - inputs: Wave39 parked rows plus broad h5ad, broad residual, Wave21 prior
    review, Wave25 causal proxy, and Wave34 genetics/druggability outputs.
  - scale: 6 parked candidates: `MMP7`, `CD82`, `FXYD5`, `SCD`, `CCL20`, and
    `IL23A`.
  - key result: 5 `NO_GO_PARKED_SURFACE_FAILFAST`; `FXYD5` is
    `PARK_ONLY_IF_NEW_PERTURBATION`, not promoted.

- Wave41 external deconvolution of the last unknown L1000 hit:
  - script: `scripts/v3_wave41_l1000_external_unknown_deconvolution.py`
  - outputs: `results_v3/wave41_l1000_external_unknown_deconvolution/`
  - input: `results_v3/wave27_l1000_unknown_deconvolution/unknown_l1000_deconvolution.tsv`
  - targeted item: `BRD-A72180425` / `K784-3188`, the only
    `PARK_EXTERNAL_TARGET_LOOKUP_ONLY` row from Wave27
  - public sources: PubChem PUG-REST, ChEMBL API, Europe PMC REST search,
    ClinicalTrials.gov API v2, L1000FWD DMOA page, and NCBI Bookshelf
  - raw API cache: `results_v3/wave41_l1000_external_unknown_deconvolution/raw_api/`
  - scale: 16 API/page calls, 1 candidate
  - key result: PubChem CID `3689416`, ChEMBL `CHEMBL1472126`, 57 ChEMBL
    activity rows, 0 ChEMBL mechanism rows, L1000FWD DMOA known MOA/targets
    `Unknown`/`Unknown`, and NCBI Bookshelf ML162/RAS-selective-lethal probe
    SAR context
  - decision: `NO_GO_CYTOTOXIC_PROBE_ANALOG`; no L1000 unknown candidate
    remains open

- Wave42 FADS genetics-first lipid-desaturation audit:
  - script: `scripts/v3_wave42_fads_lipid_desaturation_axis.py`
  - outputs: `results_v3/wave42_fads_lipid_desaturation_axis/`
  - inputs:
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
    - `tmp_v3/gwascatalog_associations_20260317_convert.parquet`
    - `data/raw_v3/lincs2020/compoundinfo_beta.txt`
  - public sources: ChEMBL target/activity API, Europe PMC REST search,
    ClinicalTrials.gov API v2, Google Patents search URLs
  - raw API cache: `results_v3/wave42_fads_lipid_desaturation_axis/raw_api/`
  - key local statistics:
    - 39 autoimmune/immune-related GWAS Catalog FADS-locus rows
    - 18 distinct autoimmune/immune-related traits
    - 27 rows naming FADS genes
    - 15 rows naming non-FADS locus genes
    - `FADS1` ChEMBL best nM value 0.52 across 61 nM-valued rows
    - 0 LINCS FADS1/FADS2 perturbagen rows
    - 0 FADS-autoimmune / D5D-inhibitor / FADS1-inhibitor ClinicalTrials.gov
      hits; 1 `AMG 786` hit
  - subagent critique:
    `subagents_v3/wave42b_fads_lipid_axis_critique.md`
  - decision:
    `PARK_ONLY_IF_COLOC_DIRECTION_AND_PERTURBATION_APPEAR`; no therapeutic
    claim

- Wave43 genetics-plus-druggability fail-fast:
  - script: `scripts/v3_wave43_genetic_druggable_failfast.py`
  - outputs: `results_v3/wave43_genetic_druggable_failfast/`
  - inputs:
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
    - `results_v3/wave42_fads_lipid_desaturation_axis/summary.json`
  - scale: 4 parked genetic-druggable rows (`FADS1`, `TYK2`, `NOD2`, `JAK2`)
  - key result: 0 promotions; `FADS1` already demoted by Wave42, `TYK2/JAK2`
    prior-art/generic immunosuppression, `NOD2` direction/context mismatch

- Wave44 CFB / alternative-complement stratification audit:
  - script: `scripts/v3_wave44_cfb_complement_stratification_audit.py`
  - outputs: `results_v3/wave44_cfb_complement_stratification_audit/`
  - inputs:
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
    - `results_v3/wave21_residual_candidate_prior_art/candidate_prior_art_gate.tsv`
    - `results_v3/wave25_causal_genetics_module_proxy/causal_proxy_candidate_matrix.tsv`
    - `results_v3/osmr_complement_axes/osmr_complement_summary.json`
  - public sources: Europe PMC REST search and ClinicalTrials.gov API v2;
    Google Patents search URLs generated
  - key result: `NO_GO_COMPLEMENT_STRATIFICATION_PRIOR_ART_BLOCKED`
  - local statistics:
    - 4 local positive diseases
    - 4 residual-retained diseases
    - strict-core residual survival only `ibd_crohn_stromal:Crohn disease`
    - MS white-matter microglia delta -0.982, p 0.287
    - ChEMBL factor B target `CHEMBL5731`, Wave34 best nM 1.0
    - Wave25 `NO_GO_CAUSAL_PROXY`
    - Europe PMC prior-art/crowding counts: 1148 complement-factor-B
      autoimmune-cluster hits, 190 factor-B-inhibitor autoimmune hits, 300
      iptacopan autoimmune hits

- Wave45 regulatory/restoration controller audit:
  - script: `scripts/v3_wave45_regulatory_controller_audit.py`
  - outputs: `results_v3/wave45_regulatory_controller_audit/`
  - inputs:
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
    - `results_v3/wave23_genetics_restoration_modality/ranked_go_park_no_go.tsv`
    - `results_v3/wave31_dynamic_transition_controller_audit/dynamic_transition_controller_audit.tsv`
    - `results_v3/wave25_causal_genetics_module_proxy/causal_proxy_candidate_matrix.tsv`
  - scale: 8 candidates (`TNFAIP3`, `SBNO2`, `SP140`, `GPR65`, `IL10`,
    `MED16`, `CDK8_CDK19_MEDIATOR_KINASE`, `GSK3B`)
  - key result: 0 promotions; regulatory/restoration-controller branch closed

- Wave46 central-axis closure audit:
  - script: `scripts/v3_wave46_central_axis_closure_audit.py`
  - outputs: `results_v3/wave46_central_axis_closure_audit/`
  - inputs:
    - `results_v3/central_and_intervention_candidate_rank.tsv`
    - `results_v3/mechanistic_model/ifng_apc_feedback_intervention_effects.tsv`
    - `results_v3/mechanistic_model/ifng_apc_feedback_summary.json`
    - `results_v3/wave14_target_level_genetics/target_level_genetics_truth_table.tsv`
    - `results_v3/wave15_loader_external_gate/loader_external_gate_summary.tsv`
    - `results_v3/wave19_lysosomal_controller/candidate_local_evidence.tsv`
    - `results_v3/wave19_lysosomal_controller/route_summary.tsv`
    - `results_v3/wave31_dynamic_transition_controller_audit/dynamic_transition_controller_audit.tsv`
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/wave43_genetic_druggable_failfast/genetic_druggable_failfast.tsv`
    - `results_v3/wave45_regulatory_controller_audit/regulatory_controller_audit.tsv`
  - key result: all five central axes closed for V3 promotion

- Wave47 late-stage survivor map:
  - script: `scripts/v3_wave47_late_stage_survivor_map.py`
  - outputs: `results_v3/wave47_late_stage_survivor_map/`
  - inputs:
    - Wave23 restoration and treatment-response tables
    - Wave28 target-first rescue
    - Wave32 resolution rescue
    - Wave33 tolerance/costimulation
    - Wave34A genetics-first target rescue
    - Wave38 CRISPR-state rescue
    - Wave39 surfaceome rescue
    - Wave40 parked surface fail-fast
    - Wave46 central-axis closure
  - scale: 75 late-stage routes scanned
  - key result: 0 promotable now; 15 reopen-only; 15 parked but likely blocked;
    43 closed/no-go/demoted; 2 closed prior-wave excluded axes

- Wave48 resolution-reopener audit:
  - script: `scripts/v3_wave48_resolution_reopener_audit.py`
  - outputs: `results_v3/wave48_resolution_reopener_audit/`
  - inputs:
    - `results_v3/wave32_resolution_rescue_audit/`
    - `results_v3/wave32c_resolution_prior_art_audit/`
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/wave36a_gene_level_controller_rescue/`
    - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
    - `results_v3/pivot_panel_triage/pivot_panel_summary.tsv`
    - `results_v3/geneformer_pivot_panel_delete/`
  - public sources: cached Wave32C PubMed/Europe PMC/ClinicalTrials.gov
    counts; live Europe PMC REST search; live ClinicalTrials.gov API v2;
    live ChEMBL target/activity search; Google Patents and Espacenet URLs
  - key result:
    - `FPR2_ANXA1_BIASED_RESOLUTION`:
      `REOPEN_WITH_WETLAB_TEST_ONLY_NOT_V3_PROMOTION`, 4/7 critical gates
      passed; ChEMBL FPR2 activity count 10101; Wave37 FPR2/ANXA1 calls
      unresolved
    - `CD300_RECEPTOR_SPECIFIC_TUNING`:
      `REOPEN_ONLY_IF_RECEPTOR_SPECIFIC_PERTURBATION_NOT_V3_PROMOTION`, 2/7
      critical gates passed; CD300E direct positives in Crohn/psoriasis/UC,
      but no strict MS anchor and no significant real perturbation anchor

- Wave49 PTPN22 directionality and modality audit:
  - script: `scripts/v3_wave49_ptpn22_directionality_audit.py`
  - outputs: `results_v3/wave49_ptpn22_directionality_audit/`
  - inputs:
    - `results_v3/wave47_late_stage_survivor_map/reopen_only_requirements.tsv`
    - `results_v3/wave34a_genetics_first_target_rescue/genetics_first_candidate_rank.tsv`
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
    - `results_v3/wave23_genetics_restoration_modality/ranked_go_park_no_go.tsv`
  - public sources: live Europe PMC REST search; ClinicalTrials.gov API v2;
    ChEMBL target/activity API; Google Patents and Espacenet URLs
  - scale:
    - 4 phosphatase targets queried in ChEMBL (`PTPN22`, `PTPN2`, `PTPN1`,
      `PTPN11`)
    - bounded off-target activity scan for top PTPN22 molecules
  - key result:
    - `PTPN22`:
      `NO_GO_BROAD_GENETICS_WITH_UNRESOLVED_DIRECTION_AND_SELECTIVITY`, 2/9
      gates passed
    - broad genetics: 28 GWAS Catalog traits, minimum p about 5e-174
    - local MS state: white-matter delta 0.820, p 0.031, FDR 0.851
    - ChEMBL bounded activity pull: 100 PTPN22 nM rows, best nM 270
    - selectivity blocker: minimum observed off-target/PTPN22 ratio 0.417 for
      a top PTPN22 molecule against PTPN1

- Wave50 GPR65 acid-sensing GPCR audit:
  - script: `scripts/v3_wave50_gpr65_acid_sensing_gpcr_audit.py`
  - outputs: `results_v3/wave50_gpr65_acid_sensing_gpcr_audit/`
  - inputs:
    - `results_v3/wave47_late_stage_survivor_map/reopen_only_requirements.tsv`
    - `results_v3/wave34a_genetics_first_target_rescue/genetics_first_candidate_rank.tsv`
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/wave20_genetic_druggable_altaxis/`
    - `results_v3/wave23_genetics_restoration_modality/ranked_go_park_no_go.tsv`
  - public sources: live Europe PMC REST search; ClinicalTrials.gov API v2;
    ChEMBL target/activity API; Google Patents and Espacenet URLs
  - key result:
    - `GPR65`: `NO_GO_GPR65_PRIOR_ART_AND_LOCAL_CELLSTATE_MISMATCH`, 3/8 gates
      passed
    - local genetics: 5 OpenTargets diseases (`AS`, `Crohn`, `MS`,
      `Psoriasis`, `UC`), 5 GWAS Catalog traits, minimum p 4e-18
    - local expression/state: 1 positive disease, 2 negative diseases; MS
      white-matter delta 0.090, p 0.624, FDR 0.949
    - druggability: ChEMBL target `CHEMBL3714081`, 99 bounded activity rows,
      best nM 364.84
    - trials: direct GPR65 autoimmune/agonist ClinicalTrials.gov queries 0

- Wave51 reachable stromal/surface audit:
  - script: `scripts/v3_wave51_reachable_stromal_surface_audit.py`
  - outputs: `results_v3/wave51_reachable_stromal_surface_audit/`
  - inputs:
    - `results_v3/wave47_late_stage_survivor_map/reopen_only_requirements.tsv`
    - `results_v3/wave34a_genetics_first_target_rescue/genetics_first_candidate_rank.tsv`
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank.tsv`
    - `results_v3/wave40_parked_surface_failfast/parked_surface_failfast.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
  - public sources: live Europe PMC REST search; ClinicalTrials.gov API v2;
    ChEMBL target/activity API; Google Patents and Espacenet URLs
  - key result:
    - `FAP`: `NO_GO_REACHABLE_SURFACE_STROMAL_ROUTE`, 2/8 gates passed;
      15 GWAS Catalog traits, minimum p 6e-25; Europe PMC max count 218;
      ClinicalTrials.gov `FAP autoimmune` count 5; ChEMBL `CHEMBL4683`, best
      bounded nM 4.6
    - `FXYD5`: `NO_GO_REACHABLE_SURFACE_STROMAL_ROUTE`, 1/8 gates passed;
      local positives 4, negatives 1; MS white-matter delta 0.352, p 0.0587,
      FDR 0.899; no ChEMBL target activity

- Wave52 remaining mechanistic reopener audit:
  - script: `scripts/v3_wave52_remaining_mechanistic_reopeners.py`
  - outputs: `results_v3/wave52_remaining_mechanistic_reopeners/`
  - inputs:
    - `results_v3/wave47_late_stage_survivor_map/reopen_only_requirements.tsv`
    - `results_v3/wave23_genetics_restoration_modality/ranked_go_park_no_go.tsv`
    - `results_v3/wave28_target_first_rescue/target_first_rescue_matrix.tsv`
    - `results_v3/wave32_resolution_rescue_audit/resolution_rescue_route_audit.tsv`
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/wave34a_genetics_first_target_rescue/genetics_first_candidate_rank.tsv`
    - `results_v3/wave22_sqle_failfast/sqle_decision.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
  - public sources: live Europe PMC REST search; ClinicalTrials.gov API v2;
    ChEMBL target/activity API; Google Patents and Espacenet URLs
  - candidate routes: `CCR6_TH17_TRAFFICKING`,
    `TREM2_APOE_LIPID_REPAIR`, `SQLE_STEROL_STROMAL`,
    `LOCALIZED_IL10_RESTORATION`
  - key result:
    - `CCR6_TH17_TRAFFICKING`:
      `NO_GO_CROWDED_TRAFFICKING_NO_COLOC_LOCAL_SUPPORT`, 2/8 gates passed
    - `TREM2_APOE_LIPID_REPAIR`:
      `NO_GO_TREM2_PRIOR_ART_MARKER_CONFOUNDER`, 3/8 gates passed
    - `SQLE_STEROL_STROMAL`: `NO_GO_SQLE_FAILFAST_RECONFIRMED`, 2/8 gates
      passed
    - `LOCALIZED_IL10_RESTORATION`:
      `NO_GO_IL10_PRIOR_ART_SYSTEMIC_CYTOKINE_DELIVERY`, 2/8 gates passed

- Wave53 perturbation-first pivot:
  - script: `scripts/v3_wave53_perturbation_first_pivot.py`
  - outputs: `results_v3/wave53_perturbation_first_pivot/`
  - inputs:
    - `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`
    - `results_v3/wave15_perturbation_drug_response/ranked_direct_perturbations.tsv`
    - `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
    - `results_v3/wave24_l1000_recurrent_reversal/recurrent_l1000_mechanism_summary.tsv`
    - `results_v3/wave26_treatment_response_strict_audit/strict_baseline_response_audit.tsv`
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
  - public sources: live Europe PMC REST search; ClinicalTrials.gov API v2;
    ChEMBL target/activity API; Google Patents and Espacenet URLs
  - key result:
    - `MED16_MEDIATOR_MODULE`:
      `WETLAB_ONLY_MED16_SELECTIVE_NONDRUGGABLE_ROUTE`, 2/8 gates passed
    - `GSK3B_INHIBITION`:
      `NO_GO_GSK3B_REAL_PERTURBATION_PRIOR_ART_PLEIOTROPY`, 2/8 gates passed
    - `TNFRSF1A_DAMPING`: `NO_GO_PERTURBATION_FIRST_PIVOT`, 3/8 gates passed
    - `RFX5_MHCII_PARTIAL_SUPPRESSION`: `NO_GO_PERTURBATION_FIRST_PIVOT`,
      2/8 gates passed
    - `CHUK_IKK_MODULATION`: `NO_GO_PERTURBATION_FIRST_PIVOT`, 2/8 gates
      passed

- Wave54 MFGE8 debris-opsonin audit:
  - script: `scripts/v3_wave54_mfge8_debris_opsonin_audit.py`
  - outputs: `results_v3/wave54_mfge8_debris_opsonin_audit/`
  - inputs:
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
    - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
  - public sources: live Europe PMC REST search; ClinicalTrials.gov API v2;
    ChEMBL target/activity API; Google Patents and Espacenet URLs
  - key result:
    - `MFGE8`: `PARK_EX_VIVO_ONLY_MFGE8_DEBRIS_OPSONIN`, 3/8 gates passed
    - local positive disease count 1; MS white-matter delta 0.559, p 0.0686,
      FDR 0.899
    - Wave37 efferocytosis contrast log fold-change 0.159, FDR 1.0,
      screen call `UNRESOLVED`

- Wave55 external genetics and druggability sweep:
  - script: `scripts/v3_wave55_external_genetics_druggability_sweep.py`
  - outputs: `results_v3/wave55_external_genetics_druggability_sweep/`
  - sources:
    - live Open Targets Platform GraphQL associated-target API
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
    - `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`
    - `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
    - live ChEMBL target/activity API
    - live Europe PMC REST API
  - key result:
    - live Open Targets rows: 6000
    - non-closed ranked targets: 2815
    - promoted targets: 0
    - reopen-priority targets: `SP140` and `IL12A`
    - `SP140`: 6 diseases with Open Targets genetic association >=0.25
      (`AS;Crohn;MS;Psoriasis;RA;UC`), local positive disease count 4,
      MS white-matter delta -0.087, p 0.726, FDR 0.968, no direct
      perturbation support, no ChEMBL activity rows
    - `IL12A`: 5 diseases with Open Targets genetic association >=0.25
      (`Celiac;MS;PBC;SLE;Sjogren`), local positive disease count 1,
      MS white-matter delta -0.914, p 0.443, FDR 0.921, high Open Targets
      clinical score 0.986

- Wave56 `SP140` targeted reopener audit:
  - script: `scripts/v3_wave56_sp140_targeted_reopener_audit.py`
  - outputs: `results_v3/wave56_sp140_targeted_reopener_audit/`
  - inputs:
    - `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
    - `results_v3/wave55_external_genetics_druggability_sweep/opentargets_associated_targets_raw.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
    - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
    - `results_v3/wave45_regulatory_controller_audit/regulatory_controller_audit.tsv`
    - `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
    - `results_v3/wave18_foundation_rescue/direct_perturbation_evidence_by_candidate.tsv`
    - `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`
    - live Europe PMC, ClinicalTrials.gov, ChEMBL, UniProt, and patent-search URLs
  - key result:
    - `SP140`: `NO_GO_SP140_TARGETED_AUDIT`, 2/10 gates passed
    - passed only external genetics breadth and local cell-state replication
    - failed target-resolved coloc/MR, strict module residual signal, strict
      MS white-matter anchor, real perturbation, foundation-model support,
      direct druggability, crowding, and correct-direction intervention
    - MS white-matter delta -0.087, p 0.726, FDR 0.968
    - ChEMBL activity rows 0; UniProt domains include HSR, SAND, bromodomain,
      and PHD-type regions

- Wave56-K `SP140` perturbation/druggability sidecar:
  - report: `subagents_v3/wave56k_sp140_perturbation_druggability.md`
  - script: `scripts/v3_wave56k_sp140_perturbation_druggability_audit.py`
  - outputs: `results_v3/wave56k_sp140_perturbation_druggability/`
  - key result:
    - published `SP140` siRNA/GSK761 perturbation evidence exists
    - GSK761 suppresses early IFN/NF-kB macrophage readouts, but not a
      coherent lipid-lysosomal repair module
    - demoted because MS local support is null, direct SP140 inhibition is
      prior art, and GSK761 is weak for CNS/lead-like feasibility

- Wave57 intervention-first Geneformer screen:
  - script: `scripts/v3_wave57_intervention_first_geneformer_screen.py`
  - outputs: `results_v3/wave57_intervention_first_geneformer_screen/`
  - model: Geneformer V2-104M, revision
    `04c2b2e84da7c0f385c3f9ad8f3ec24bab6650e5`
  - candidate genes: 26
  - contexts: 11 disease-relevant tissue/cell contexts
  - key result:
    - promotions: 0
    - reopeners: `CXCR2`, `IL7R`
    - `CXCR2`: model support in `IBD_myeloid`, local positives in
      Crohn/psoriasis/UC, external genetics in AS/Crohn/psoriasis/RA/UC, no
      MS genetic anchor
    - `IL7R`: model support in `ra_myeloid_dendritic`, external genetics in
      seven diseases including MS, local positives in Crohn/T1D/UC, strict MS
      local anchor failed

- Wave58 `CXCR2`/`IL7R` targeted audit:
  - script: `scripts/v3_wave58_cxcr2_il7r_targeted_audit.py`
  - outputs: `results_v3/wave58_cxcr2_il7r_targeted_audit/`
  - sources:
    - Wave57 intervention-first Geneformer outputs
    - Wave55 external genetics rank
    - broad h5ad discovery and residual-gate tables
    - Wave37 efferocytosis screen
    - live ChEMBL, UniProt, Europe PMC, ClinicalTrials.gov, and patent-search URLs
  - key result:
    - `CXCR2`: `NO_GO_WAVE58_TARGETED_AUDIT`, 4/9 gates passed; best ChEMBL
      nM 6.0, but no MS genetic anchor and generic-neutrophil/prior-art gates fail
    - `IL7R`: `NO_GO_WAVE58_TARGETED_AUDIT`, 5/9 gates passed; MS Open
      Targets genetic score 0.789 and clinical modality precedent, but
      strict MS local, perturbation, module-specificity, and prior-art gates fail

- Wave58 sidecar reports:
  - `subagents_v3/wave58m_cxcr2_therapeutic_audit.md`
    - closed `CXCR2` as a V3 target; useful comparator for druggable,
      model-positive, prior-arted neutrophil/remyelination biology
  - `subagents_v3/wave58n_il7r_therapeutic_audit.md`
    - closed `IL7R` as a V3 target; useful comparator for genetically real,
      prior-arted CD127/sIL7R adaptive-immune biology
  - `subagents_v3/wave58o_hostile_review_cxcr2_il7r.md`
    - hostile review confirmed closure of both branches

- Wave59 lysosomal/sphingolipid model reopener audit:
  - script: `scripts/v3_wave59_lysosomal_sphingolipid_model_reopener_audit.py`
  - outputs: `results_v3/wave59_lysosomal_sphingolipid_model_reopener_audit/`
  - random seed: 20260527
  - candidates:
    `CTSB`, `ASAH1`, `HEXB`, `HEXA`, `CTSS`, `CTSD`, `PSAP`, `LIPA`,
    `GALC`, `GBA1`, `SMPD1`
  - sources:
    - Wave57 intervention-first Geneformer outputs
    - Wave55 external genetics/druggability sweep
    - broad h5ad discovery and residual-gate tables
    - Wave37 efferocytosis CRISPR screen
    - live ChEMBL and Europe PMC API outputs cached under
      `results_v3/wave59_lysosomal_sphingolipid_model_reopener_audit/raw_api/`
  - key result:
    - promotions: 0
    - parked: 0
    - all candidates called `NO_GO_LYSOSOMAL_MODEL_REOPENER`
    - `GALC` had the best gate count at 4/10 but failed strict MS,
      perturbation/efferocytosis, model, module-residual, directionality, and
      prior-art gates
    - `CTSB` and `ASAH1` had the strongest model/druggability hints but failed
      genetics/MS/local/perturbation and safe-direction gates

- Wave60 circuit-coupling pivot:
  - script: `scripts/v3_wave60_circuit_coupling_pivot.py`
  - outputs: `results_v3/wave60_circuit_coupling_pivot/`
  - random seed: 20260527
  - sources:
    - `results_v3/direct_h5ad_cell_state/direct_h5ad_donor_module_scores.tsv`
    - `results_v3/osmr_complement_axes/osmr_complement_donor_module_scores.tsv`
    - `results_v3/broad_residual_gate/broad_residual_gene_donor_scores.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
    - `results_v3/gse111972_module_contrasts.tsv`
    - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
    - `results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv`
  - method:
    - donor-level context-standardized predictors
    - pathogenic core mean of lipid-loader, lysosomal, HLA-II/APC, and
      MIF/CD74 modules
    - residualized pathogenic core against IFN/APC and inflammatory NF-kB
    - case-donor-only Spearman coupling by analysis, combined with
      Fisher-z meta-analysis
  - key result:
    - donor-context rows: 309
    - predictors ranked: 276
    - full reopeners: 0
    - parked expression-coupling hypotheses: 63
    - `C15ORF48` failed circuit-coupling gate despite disease-up recurrence and
      nominal MS support
    - `OSM` failed circuit-coupling and MS gates
    - `OSMR` passed circuit-coupling/disease-up gates but failed MS and
      perturbation/model gates
    - `GPNMB` had strong coupling and nominal MS support but failed disease-up
      recurrence and perturbation gates

- Wave60-R hostile methods review:
  - report: `subagents_v3/wave60r_circuit_pivot_hostile_review.md`
  - verdict: no promotion from donor-level expression coupling
  - accepted requirement:
    circuit promotion needs donor-blocked, tissue-aware residualization plus
    real perturbation or response validation and prior-art delta

- Wave60-P/Q circuit sidecar reports:
  - `subagents_v3/wave60p_c15orf48_mocci_circuit_audit.md`
    - `C15ORF48`/MOCCI demoted to assay-only mitochondrial adaptation readout
  - `subagents_v3/wave60q_osm_osmr_circuit_audit.md`
    - `OSM`/`OSMR`/`IL6ST` demoted to comparator and IBD OSM-high
      stratification axis; not a cross-autoimmune V3 target

- Wave61 perturbation-first guardrail scorer:
  - script: `scripts/v3_wave61_intervention_guardrail_scorer.py`
  - outputs: `results_v3/wave61_perturbation_first_guardrail/`
  - random seed: 20260527
  - sources:
    - `results_v3/wave15_perturbation_drug_response/ranked_direct_perturbations.tsv`
    - `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`
    - `results_v3/wave24_l1000_recurrent_reversal/recurrent_l1000_compound_triage.tsv`
    - `results_v3/wave24_l1000_recurrent_reversal/recurrent_l1000_mechanism_summary.tsv`
    - `results_v3/wave27_l1000_unknown_deconvolution/unknown_l1000_deconvolution.tsv`
    - `results_v3/wave35_resolution_perturbation/contrast_level_calls.tsv`
    - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
    - `results_v3/wave53_perturbation_first_pivot/decision_matrix.tsv`
    - `results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
  - output files:
    - `intervention_evidence_tiers.tsv`
    - `efferocytosis_expression_reopener_rank.tsv`
    - `gate_matrix.tsv`
    - `summary.json`
    - `REPORT.md`
  - key result:
    - evidence rows: 395
    - direct perturbation rows: 186
    - L1000 rows: 180
    - resolution rows: 29
    - promotion candidates: 0
    - reopened perturbation candidates: 0
    - perturbation-first branch is hypothesis-generation only under current
      evidence

- Wave61-U hostile perturbation-first review:
  - report: `subagents_v3/wave61u_hostile_review_perturbation_first.md`
  - verdict: abandon perturbation-first as a V3 finding route under current
    evidence
  - accepted requirement:
    promotion needs human primary/ex vivo disease-cell perturbation, target
    engagement, held-out module/protein/function readouts, repair and
    host-defense guardrails, and claim-specific prior-art clearance

- Wave62 Open Targets target-resolution audit:
  - script: `scripts/v3_wave62_opentargets_target_resolution.py`
  - outputs: `results_v3/wave62_opentargets_target_resolution/`
  - source: Open Targets Platform GraphQL API
    `https://api.platform.opentargets.org/api/v4/graphql`
  - diseases queried:
    `MS`, `RA`, `Crohn`, `UC`, `Psoriasis`, `SLE`, `T1D`, `Sjogren`, `AS`,
    `AITD`, `Celiac`, `PBC`
  - raw/cache path:
    `results_v3/wave62_opentargets_target_resolution/raw_api/`
  - extracted files:
    - `opentargets_studies.tsv`
    - `opentargets_credible_sets.tsv`
    - `opentargets_l2g_rows.tsv`
    - `opentargets_qtl_coloc_rows.tsv`
    - `api_caps_and_errors.tsv`
    - `target_resolution_summary.tsv`
    - `target_resolution_gate_matrix.tsv`
    - `summary.json`
    - `REPORT.md`
  - key result:
    - study rows: 539
    - eligible GWAS studies: 95
    - credible sets: 2506
    - L2G rows: 4821
    - QTL colocalisation rows: 16823
    - target summaries: 2028
    - reopen calls: 0
    - park calls: 32
  - limitation:
    - `GCST90480502` was skipped after Open Targets rejected the query as too
      expensive
  - interpretation:
    - target-resolution triage only; no therapeutic target promoted

- Wave63 transition-controller integrator:
  - script: `scripts/v3_wave63_transition_controller_integrator.py`
  - outputs: `results_v3/wave63_transition_controller_integrator/`
  - input sources:
    - Wave62 target-resolution summary
    - broad h5ad gene discovery
    - broad residual gate
    - Wave31 dynamic transition-controller audit
    - Wave34/Wave34A genetics/druggability scans
    - Wave45 regulatory-controller audit
    - Wave55 external genetics sweep
    - Wave57 Geneformer intervention-first screen
    - Wave59 lysosomal/sphingolipid audit and decisions
    - Wave61 perturbation guardrail
  - output files:
    - `transition_controller_candidates.tsv`
    - `transition_controller_gate_matrix.tsv`
    - `summary.json`
    - `REPORT.md`
  - key result:
    - candidates evaluated: 55
    - promotion calls: 0
    - park calls: 2
    - parked rows: `IL7R`, `GALC`
  - accepted sidecar reports:
    - `subagents_v3/wave63x_sp140_topoisomerase_transfer.md`
    - `subagents_v3/wave63y_broad_genetics_benchmark.md`
    - `subagents_v3/wave63z_transition_controller_hostile.md`
  - interpretation:
    - no transition-controller candidate is ready for V3 therapeutic promotion

- Wave64 SLAMF7 perturbation audit:
  - script: `scripts/v3_wave64_slamf7_perturbation_audit.py`
  - outputs: `results_v3/wave64_slamf7_perturbation_audit/`
  - new accession: `GSE185509`
  - downloaded processed count file:
    `data/raw_v3/wave64_gse185509_slamf7/GSE185509_SLAMF7_stimulation_counts.csv.gz`
  - other inputs:
    - `results_v3/wave62_opentargets_target_resolution/opentargets_qtl_coloc_rows.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
  - result:
    - SLAMF7 route parked as directional inflammatory receptor biology, not a
      V3 target. Direct engagement amplifies TNF/NF-kB/host-defense modules,
      suppresses some lysosomal/lipid modules, lacks MS disease-cell anchor,
      and fails Wave64-C specificity/guardrail gates.

- Wave65 RA paired synovium anti-TNF audit:
  - script: `scripts/v3_wave65_gse198520_ra_synovium_antitnf_audit.py`
  - outputs: `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/`
  - accession: `GSE198520`
  - downloaded files:
    - `data/raw_v3/wave65_gse198520_ra_synovium/GSE198520_Raw_gene_count_matrix.txt.gz`
    - `data/raw_v3/wave65_gse198520_ra_synovium/GSE198520_series_matrix.txt.gz`
  - output files:
    - `gse198520_counts_used.tsv`
    - `gse198520_sample_metadata.tsv`
    - `gse198520_module_scores.tsv`
    - `module_gene_presence.tsv`
    - `gse198520_patient_module_deltas.tsv`
    - `paired_pharmacodynamic_tests.tsv`
    - `response_delta_tests.tsv`
    - `wave65_gate_summary.tsv`
    - `summary.json`
    - `REPORT.md`
  - result:
    - 92 samples, 46 patients, paired baseline/week-12 anti-TNF RA synovium.
    - all modules called `NO_GO_GSE198520_BULK_TISSUE`.
    - several modules decreased after treatment, but target/generic ratios were
      below 2.0 and response-specific effects did not survive generic/pathotype
      adjustment.

- Wave66 cross-autoimmune metabolomics/lipidomics class convergence:
  - script: `scripts/v3_wave66_metabolomics_class_convergence.py`
  - outputs: `results_v3/wave66_metabolomics_class_convergence/`
  - raw/cache directory: `data/raw_v3/wave66_metabolomics_workbench/`
  - Metabolomics Workbench studies:
    - `ST001949` RA plasma control/RA/RA+MTX
    - `ST000899` Crohn/UC/control serum
    - `ST002470` UC plasma severity/improvement
    - `ST002732` SLE plasma lipidome/coronary calcification strata
    - `ST002949` ankylosing spondylitis/control serum
    - `ST000422` T1D/control plasma
    - `ST003328` MS stem-cell-derived cellular lipidomics model
    - `ST000298` psoriasis biopsy steroid metabolites
    - `ST001636` TEDDY lipidomics availability only
    - `ST001386` TEDDY metabolomics summary only
  - output files:
    - `availability.tsv`
    - `class_contrast_effects.tsv`
    - `feature_contrast_effects.tsv`
    - `metabolite_class_inventory.tsv`
    - `class_convergence_rank.tsv`
    - `summary.json`
    - `REPORT.md`
  - accepted sidecar reports:
    - `subagents_v3/wave66a_metabolomics_access_scout.md`
    - `subagents_v3/wave66b_gse282122_feasibility.md`
  - result:
    - no biochemical class promoted as V3 therapeutic mechanism.
    - ceramide/glycosphingolipid classes provide weak orthogonal support for a
      sphingolipid/lysosomal stress axis, not a target claim.
    - `GSE282122` is feasible through Zenodo `myeloid_final.h5ad` and
      `paired_sample_list.csv` for cell-resolved anti-TNF pseudobulk analysis.

- Wave67 `GSE282122` myeloid anti-TNF pseudobulk audit:
  - script: `scripts/v3_wave67_gse282122_myeloid_pseudobulk.py`
  - outputs: `results_v3/wave67_gse282122_myeloid_pseudobulk/`
  - downloaded files:
    - `data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad`
    - `data/raw_v3/wave67_gse282122_myeloid/paired_sample_list.csv`
  - source:
    - Zenodo record `14007626`
    - `GSE282122` context
  - checksums:
    - `myeloid_final.h5ad`: MD5 `bdfe50345a11abdb1a72b2439bf9950e`
    - `paired_sample_list.csv`: MD5 `3300a53889bb4b70c48ec66dbb66beea`
  - output files:
    - `paired_sample_list_used.tsv`
    - `cell_obs_used.tsv`
    - `module_gene_presence.tsv`
    - `pseudobulk_metadata.tsv`
    - `pseudobulk_module_gene_counts.tsv`
    - `pseudobulk_module_gene_logcpm.tsv`
    - `pseudobulk_module_scores.tsv`
    - `paired_module_deltas.tsv`
    - `paired_delta_tests.tsv`
    - `remission_interaction_tests.tsv`
    - `wave67_gate_summary.tsv`
    - `summary.json`
    - `REPORT.md`
  - result:
    - no lipid-loader, lysosomal-APC, or complement-phagocytosis module
      promoted in `Mono_macro` or `DC`.
    - lipid-loader modules were null; lysosomal-APC showed weak positive but
      non-significant paired deltas without remission interaction.
    - HLA-II/MIF-CD74-like non-target modules had the strongest raw paired
      signals and motivate unrestricted gene-level follow-up.

- Wave68 unrestricted `GSE282122` myeloid/DC gene screen:
  - script: `scripts/v3_wave68_gse282122_unrestricted_gene_screen.py`
  - outputs: `results_v3/wave68_gse282122_unrestricted_gene_screen/`
  - reused raw data:
    - `data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad`
    - `data/raw_v3/wave67_gse282122_myeloid/paired_sample_list.csv`
  - external target-resolution input:
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
  - output files:
    - `primary_cell_obs_used.tsv`
    - `all_gene_pseudobulk_metadata.tsv`
    - `all_gene_pair_metadata.tsv`
    - `paired_gene_delta_tests.tsv`
    - `raw_remission_response_gene_tests.tsv`
    - `adjusted_top_gene_ols.tsv`
    - `integrated_gene_target_rank.tsv`
    - `summary.json`
    - `REPORT.md`
  - result:
    - 33,075 genes tested in paired `Mono_macro` and `DC` pseudobulk.
    - 13 genes parked as genetic/perturbation intersections.
    - zero genes promoted after the SP140 post-hoc blocker was encoded from
      prior V3 audits.

- Wave69 parked-gene controller branch:
  - controller rank script:
    - `scripts/v3_wave69_parked_controller_rank.py`
    - outputs: `results_v3/wave69_parked_controller_rank/`
    - external APIs used:
      - OmniPath interactions API
      - Enrichr API
      - ChEMBL target/activity/mechanism API
      - EuropePMC search API
      - ClinicalTrials.gov v2 API
    - output files:
      - `wave68_parked_anchor_genes.tsv`
      - `parked_gene_enrichr.tsv`
      - `parked_gene_omnipath_interactions.tsv`
      - `controller_node_network_summary.tsv`
      - `controller_chembl_summary.tsv`
      - `controller_public_crowding.tsv`
      - `controller_intervention_rank.tsv`
      - `summary.json`
      - `REPORT.md`
    - result:
      - 13 Wave68 anchors, 156 OmniPath/manual interactions, 130 controller
        nodes.
      - Enrichment confirms immune/checkpoint/costimulation/Fc-phagosome
        structure.
      - only `PRKDC` and `BLK` remained as parked druggable controller scouts
        after broad kinase/checkpoint/JAK/TNF blockers.
  - independent validation scout:
    - `scripts/v3_wave69b_independent_validation_scout.py`
    - outputs: `results_v3/wave69b_independent_validation_scout/`
    - report: `subagents_v3/wave69b_independent_validation_scout.md`
    - result:
      - no Wave68 parked candidate reopened.
      - `RGS14` failed independent validation.
      - `FCGR2B` and `NCF1` show RA anti-TNF bulk pharmacodynamic movement but
        not cell-resolved controller validation.
  - foundation feasibility report:
    - `subagents_v3/wave69c_foundation_model_feasibility.md`
    - result:
      - Arc State remains blocked for named-gene claims.
      - local Geneformer V2-104M remission-centroid deletion screen is runnable.
  - Geneformer remission-centroid script:
    - `scripts/v3_wave69d_gse282122_geneformer_remission_centroid.py`
    - outputs:
      `results_v3/wave69d_gse282122_geneformer_remission_centroid/`
    - model:
      - local Geneformer V2-104M checkpoint
      - 104,365,056 loaded encoder parameters
      - seed `20260527`
    - result:
      - `PRKDC` and `BLK` not rescued.
      - model support observed only for blocked comparators (`FCGR2A`, `JAK1`,
        `IL7R`, `CD80`, `NCF1`, `SRC`, `SYK`, `CD274`, `JAK2`).

- Wave70 Fc/ROS-resolution matrix:
  - script: `scripts/v3_wave70_fc_ros_resolution_matrix.py`
  - outputs: `results_v3/wave70_fc_ros_resolution_matrix/`
  - input files:
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
    - `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
    - `results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv`
    - `results_v3/wave69d_gse282122_geneformer_remission_centroid/geneformer_remission_candidate_calls.tsv`
    - `results_v3/wave61_perturbation_first_guardrail/intervention_evidence_tiers.tsv`
  - output files:
    - `fc_ros_resolution_candidate_matrix.tsv`
    - `ra_deltas.tsv`
    - `ra_paired.tsv`
    - `ra_response.tsv`
    - `summary.json`
    - `REPORT.md`
  - result:
    - no promoted candidate.
    - blocked/highest-evidence comparators: `FCGR2A`, `NCF1`, `NCF2`, `LYN`,
      `CYBB`, `SYK`, `BTK`, `PIK3CD`.
    - less-blocked but insufficient: `LILRB2`, `LILRB1`, `LILRB3`, `LILRB4`,
      `INPP5D`, `PTPN6`, `LAIR1`, `SIGLEC10`, `CD300A`, TAM-axis nodes.
    - `LILRB2` is the only unblocked candidate with both `GSE282122` and broad
      Crohn/UC myeloid recurrence; it remains a falsification target, not a
      therapeutic claim.

- Wave70-B Fc/ROS-resolution computational scout:
  - script: `scripts/v3_wave70b_fc_ros_computational_scout.py`
  - outputs: `results_v3/wave70b_fc_ros_computational_scout/`
  - report: `subagents_v3/wave70b_fc_ros_computational_scout.md`
  - result:
    - no candidate promoted.
    - `LILRB2` strongest falsification target: `GSE282122` DC adjusted beta
      `-0.949`, FDR `0.0191`; Wave68 adjusted delta `-0.884`, FDR `0.0224`;
      broad Crohn/UC myeloid recurrence; no RA replication; no local
      cross-autoimmune genetic anchor.
    - `INPP5D`, `PTPN6`, and `CD300A` remained comparator/readout nodes.

- Wave70-C inhibitory-receptor Geneformer directionality screen:
  - script: `scripts/v3_wave70c_inhibitory_receptor_geneformer_direction.py`
  - outputs: `results_v3/wave70c_inhibitory_receptor_geneformer_direction/`
  - model:
    - local Geneformer V2-104M checkpoint
    - 104,365,056 loaded encoder parameters
    - seed `20260527`
  - output files:
    - `geneformer_direction_metrics.tsv`
    - `geneformer_direction_gene_summary.tsv`
    - `geneformer_direction_candidate_calls.tsv`
    - `summary.json`
    - `REPORT.md`
  - result:
    - model support concentrated on blocked Fc/NOX comparators (`NCF1`,
      `FCGR2A`, `CYBB`, `NCF2`).
    - `LILRB2`, `LILRB1`, `LILRB4`, and `INPP5D` failed the reopener
      threshold.
    - Fc/ROS branch retained as biology but closed as a target branch.

- Wave70-B Fc/ROS-resolution local computational scout:
  - script: `scripts/v3_wave70b_fc_ros_computational_scout.py`
  - report: `subagents_v3/wave70b_fc_ros_computational_scout.md`
  - outputs: `results_v3/wave70b_fc_ros_computational_scout/`
  - input files:
    - `data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad`
    - `data/raw_v3/wave67_gse282122_myeloid/paired_sample_list.csv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
    - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
    - `results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv`
    - `results_v3/wave69d_gse282122_geneformer_remission_centroid/geneformer_remission_candidate_calls.tsv`
    - `results_v3/wave18_foundation_rescue/geneformer_source_gene_summary.tsv`
    - `results_v3/geneformer_pivot_panel_delete/geneformer_pivot_panel_gene_summary.tsv`
  - output files:
    - `integrated_fc_ros_candidate_scout.tsv`
    - `gse282122_candidate_pseudobulk_metadata.tsv`
    - `gse282122_candidate_pair_deltas.tsv`
    - `gse282122_candidate_paired_tests.tsv`
    - `gse282122_candidate_remission_response_tests.tsv`
    - `wave68_candidate_rows.tsv`
    - `ms_gse111972_candidate_rows.tsv`
    - `broad_h5ad_candidate_summary.tsv`
    - `broad_h5ad_candidate_contrasts.tsv`
    - `ra_gse198520_candidate_patient_deltas.tsv`
    - `ra_gse198520_candidate_paired_tests.tsv`
    - `ra_gse198520_candidate_response_tests.tsv`
    - `wave37_efferocytosis_candidate_rows.tsv`
    - `geneformer_candidate_rows.tsv`
    - `summary.json`
    - `REPORT.md`
  - result:
    - no candidate promoted.
    - integrated call counts: 16 `PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED`,
      2 `DESCRIPTIVE_SIGNAL_ONLY`, 1 `NO_GO_LOCAL_SUPPORT_WEAK`.
    - strongest local signal: `LILRB2` (`GSE282122` DC adjusted beta `-0.949`,
      FDR `0.0191`; broad Crohn/UC recurrence with 1 FDR10 compartment) but
      no local Wave68/Wave62 cross-autoimmune genetics and no RA replication.
    - `INPP5D`, `PTPN6`, and `CD300A` are readout/comparator signals only.

- Wave71 global survivor and branch-memory integration:
  - artifacts:
    - `subagents_v3/wave71b_prior_branch_status_synthesis.md`
    - `subagents_v3/wave71c_cross_autoimmune_intervention_scout.md`
    - `scripts/v3_wave71_global_survivor_meta_rank.py`
    - `results_v3/wave71_global_survivor_meta_rank/`
    - `subagents_v3/wave71a_global_survivor_meta_rank.md`
  - sources:
    - existing V3 reports/checkpoints and high-number wave outputs.
    - 19 local candidate/evidence tables in the Wave71-A meta-rank.
  - scale:
    - Wave71-A candidate count: 679.
    - evidence row count: 909.
  - key result:
    - no candidate reopened.
    - top non-reopening rows: `CD58`, `CARMIL1`, `RAD51B`, `PARK7`, `ADCY3`,
      `FADS1`, `CCDC88B`, `PRR5L`, `YDJC`, `ARID5B`.
    - all miss multi-channel reopener thresholds or have blockers.
  - interpretation:
    - do not reopen existing expression/genetics survivors without a new
      evidence channel that answers a decisive blocker.

- Wave72 lipid-mediator intervention scout:
  - script: `scripts/v3_wave72_lipid_mediator_intervention_scout.py`
  - outputs: `results_v3/wave72_lipid_mediator_intervention_scout/`
  - inputs:
    - `results_v3/wave66_metabolomics_class_convergence/feature_contrast_effects.tsv`
    - `results_v3/wave66_metabolomics_class_convergence/class_contrast_effects.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
    - `results/mims2_proteome_convergent_targets.tsv`
  - scale:
    - feature matches: 207.
    - branch calls: 2 `NO_GO_WAVE72`, 2 `PARK_ORTHOGONAL_BIOCHEMICAL_SCOUT`.
  - key result:
    - `NAAA`: no-go; only one weak anandamide-related feature and no
      supportive disease.
    - `EPHX2`: parked; 2 supportive diseases (`MS_model`, `UC`) and one
      normalization hit, but no target-level gene convergence.
    - `GPR183`: no-go; sparse oxysterol-like support restricted to `T1D`.
    - `P2RX7`: parked; purine feature disturbance across `AS`, `Crohn`, `RA`,
      `T1D`, and `UC`, plus 4 UC improvement-normalizing feature hits, but
      no target-level gene convergence.
  - interpretation:
    - biochemical signals may stratify inflammatory states, but do not yet
      identify a therapeutic target.

- Wave73 P2RX7/purine-inflammasome stratification test:
  - script: `scripts/v3_wave73_p2rx7_stratification_test.py`
  - outputs: `results_v3/wave73_p2rx7_stratification_test/`
  - inputs:
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/raw_remission_response_gene_tests.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/paired_gene_delta_tests.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
    - `results_v3/wave72_lipid_mediator_intervention_scout/lipid_mediator_decisions.tsv`
  - key outputs:
    - `broad_module_summary.tsv`
    - `ms_module_summary.tsv`
    - `gse282122_module_response_summary.tsv`
    - `ra_module_response_summary.tsv`
    - `integrated_decision.tsv`
    - `summary.json`
    - `REPORT.md`
  - result:
    - verdict: `PARK_P2RX7_STRATIFICATION_NEEDS_TARGET_LEVEL_DATA`.
    - gate count: 2 of 7.
    - broad `p2rx7_inflammasome` signal: 5 positive contexts, 3 positive
      diseases, 0 specificity-pass contexts.
    - MS GSE111972: mean effect `-0.214`, combined `p=0.0608`,
      FDR `0.0912`; no MS module support.
    - IBD GSE282122: best remission-response row DC mean effect `0.0884`,
      combined `p=0.223`, FDR `0.499`.
    - RA GSE198520: anti-TNF paired decrease exists, but no responder-specific
      support (`good_vs_other_p=0.533`, `modgood_vs_none_p=0.491`).
  - interpretation:
    - broad purine biochemistry does not currently resolve to a P2RX7
      therapeutic or stratification target.

- Wave74 EPHX2 direct-ratio audit:
  - script: `scripts/v3_wave74_ephx2_direct_ratio_audit.py`
  - outputs: `results_v3/wave74_ephx2_direct_ratio_audit/`
  - inputs:
    - `data/raw_v3/wave66_metabolomics_workbench/`
    - `results_v3/wave66_metabolomics_class_convergence/feature_contrast_effects.tsv`
  - key outputs:
    - `ephx2_feature_inventory.tsv`
    - `direct_pair_inventory.tsv`
    - `direct_ratio_contrasts.tsv`
    - `proxy_feature_contrasts.tsv`
    - `ephx2_direct_ratio_decision.tsv`
    - `summary.json`
    - `REPORT.md`
  - result:
    - verdict: `NO_GO_EPHX2_DIRECT_RATIO_UNAVAILABLE`.
    - corrected EPHX2-relevant feature count: 37.
    - direct same-study same-site epoxide/diol pairs: 0.
    - direct ratio tests: 0.
    - proxy diol-supportive diseases: 2 (`T1D`, `UC`).
  - interpretation:
    - product-only DiHOME or unmatched EET/DHET family features cannot support
      target-level EPHX2 activity or intervention claims.

- Wave73 `P2RX7`/purine-inflammasome stratification test:
  - script: `scripts/v3_wave73_p2rx7_stratification_test.py`
  - outputs: `results_v3/wave73_p2rx7_stratification_test/`
  - inputs:
    - `results_v3/wave72_lipid_mediator_intervention_scout/lipid_mediator_decisions.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/paired_gene_delta_tests.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/raw_remission_response_gene_tests.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
  - modules:
    - `p2rx7_inflammasome`
    - `inflammasome_no_p2rx7`
    - `purinergic_adenosine`
    - `generic_nfkb_tnf`
    - `interferon_apc`
    - `lysosome_apc`
  - key result:
    - integrated call `PARK_P2RX7_STRATIFICATION_NEEDS_TARGET_LEVEL_DATA`.
    - broad h5ad `p2rx7_inflammasome` positive in 3 diseases and 5 FDR10
      contexts, but 0 specificity-pass contexts.
    - MS `GSE111972` white-matter `p2rx7_inflammasome` mean effect `-0.214`,
      p `0.0608`, FDR `0.0912`, no support.
    - IBD `GSE282122` anti-TNF best response row FDR `0.499`, no support.
    - RA `GSE198520` anti-TNF paired drop FDR `0.0100` but responder
      separation FDR `0.593`, no support.
  - interpretation:
    - purine biology remains a context marker; `P2RX7` is not supported as the
      central cross-autoimmune intervention node in available local data.

- Wave74-C prior-art/druggability scout:
  - artifact: `subagents_v3/wave74c_prior_art_druggability_scout.md`
  - verification sources checked:
    - Google Patents `WO2000023060A2` for soluble epoxide hydrolase inhibitor
      immunological/autoimmune claims.
    - PubMed/PMC search results for sEH inhibitor TPPU in EAE/MS model
      (`PMID 33925035` / PMC `PMC8125305`).
    - ClinicalTrials search results for `IPG11406`/`GPR183` UC
      (`NCT07535489`) and lupus nephritis (`NCT06717815`).
    - PubMed/search result for GPR183 RA antagonist medicinal chemistry
      (`PMID 38047891`).
    - PubMed/ClinicalTrials/patent search results for `P2RX7` RA and Crohn
      clinical trials plus MS-specific antagonist patent `EP1655032B1`.
  - key result:
    - `EPHX2`: `BLOCKED_BY_PRIOR_ART`.
    - `GPR183`: `BLOCKED_BY_PRIOR_ART`.
    - `P2RX7`: `TRANSLATION_BLOCKED`.
  - interpretation:
    - local-data positives for these branches would require narrow novelty
      deltas, not broad autoimmune target claims.

- Wave74-B `GPR183`/oxysterol-niche audit:
  - script: `scripts/v3_wave74_gpr183_oxysterol_niche.py`
  - outputs: `results_v3/wave74_gpr183_oxysterol_niche/`
  - inputs:
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/raw_remission_response_gene_tests.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/paired_gene_delta_tests.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
    - `results_v3/wave66_metabolomics_class_convergence/feature_contrast_effects.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/wave57_intervention_first_geneformer_screen/wave57_geneformer_gene_summary.tsv`
    - `results_v3/wave69d_gse282122_geneformer_remission_centroid/geneformer_remission_gene_summary.tsv`
    - Wave72 lipid-mediator feature/gene-evidence tables.
  - key result:
    - call `PARK_GPR183_OXYSTEROL_NICHE`.
    - coherent ligand-plus-receptor-plus-response disease count 0.
    - ligand-production support restricted to T1D.
    - direct `GPR183` receptor anchor positive in Crohn/Sjogren/UC but
      negative in psoriasis and unsupported in MS `GSE111972`.
    - IBD/RA response modules show signal, but direct receptor support is
      weaker than trafficking modules and prior art blocks broad promotion.
  - interpretation:
    - not a V3 target; useful only as trafficking/niche comparator.

- Wave74-A `EPHX2`/oxylipin specificity audit:
  - script: `scripts/v3_wave74_ephx2_oxylipin_specificity.py`
  - outputs: `results_v3/wave74_ephx2_oxylipin_specificity/`
  - key result:
    - call `NO_GO`.
    - EPHX2-specific biochemical support: 1 supportive disease, 1 normalizing
      treatment hit.
    - ratio proxy support count 0.
    - target-level support count 0.
    - specificity-pass context count 0.
    - no support from Wave62, broad h5ad, MS white matter, IBD anti-TNF, RA
      anti-TNF, or Geneformer outputs.
  - interpretation:
    - available local data do not resolve an EPHX2-specific mechanism over
      generic lipid/inflammatory disturbance.

- Wave74 direct `EPHX2` ratio audit:
  - script: `scripts/v3_wave74_ephx2_direct_ratio_audit.py`
  - outputs: `results_v3/wave74_ephx2_direct_ratio_audit/`
  - inputs:
    - `results_v3/wave66_metabolomics_class_convergence/feature_contrast_effects.tsv`
    - `data/raw_v3/wave66_metabolomics_workbench`
  - key result:
    - call `NO_GO_EPHX2_DIRECT_RATIO_UNAVAILABLE`.
    - 37 EPHX2-relevant features.
    - 0 same-study same-site direct epoxide/diol pairs.
    - 0 direct ratio tests.
  - interpretation:
    - product-only or substrate-only oxylipin features are weak proxies and do
      not support a target-level soluble epoxide hydrolase activity claim.

- Wave75 `ETS2` inflammatory macrophage program audit:
  - script: `scripts/v3_wave75_ets2_macrophage_program_audit.py`
  - outputs: `results_v3/wave75_ets2_macrophage_program_audit/`
  - prior-art artifact:
    - `subagents_v3/wave75c_ets2_prior_art_directionality.md`
  - key result:
    - call `PARK_IBD_MYELOID_PROGRAM_NOT_PROMOTABLE`.
    - broad direct `ETS2` support in Crohn and UC; best UC myeloid effect
      `1.972`, p `0.0002169`, FDR `0.00079`.
    - ETS2 macrophage program positive in Crohn, T1D, and UC, but negative in
      psoriasis and nonspecific against generic inflammatory/APC comparators.
    - MS `GSE111972` direct `ETS2` effect `-0.0608`, p `0.8649`, FDR `0.9802`.
    - IBD anti-TNF and RA anti-TNF response gates failed after correction.
    - Wave62 `ETS2` call `NO_GO_WAVE62_TARGET_RESOLUTION`.
    - no Wave57/Wave69D Geneformer support.
  - prior-art/direction:
    - broad ETS2 macrophage inflammatory axis already published for IBD/AS
      and adjacent inflammatory diseases.
    - direct ETS2 is not conventionally druggable.
    - MEK/ERK upstream route is broad, prior-arted, and toxic.
  - interpretation:
    - not a V3 therapeutic finding; retain as IBD-myeloid/generic-program
      comparator.

- Wave75 response-state stratification audit:
  - script: `scripts/v3_wave75_response_state_stratification.py`
  - outputs: `results_v3/wave75_response_state_stratification/`
  - inputs:
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
    - `data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/all_gene_pair_metadata.tsv`
  - key result:
    - call `REOPEN_RESPONSE_STRATIFICATION`.
    - best module `lysosomal_apc`, endpoint `baseline_pre`.
    - RA effect `1.018`, p `0.00113`, FDR `0.0319`.
    - IBD DC effect `0.888`, p `0.0204`, FDR `0.0984`.
  - interpretation:
    - response-state biomarker signal reopened, not target-level evidence.

- Wave76 adjusted response-specificity stress test:
  - script: `scripts/v3_wave76_adjusted_response_specificity.py`
  - outputs: `results_v3/wave76_adjusted_response_specificity/`
  - inputs:
    - `results_v3/wave75_response_state_stratification/ra_patient_module_pairs.tsv`
    - `results_v3/wave75_response_state_stratification/ibd_patient_module_pairs.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
  - key result:
    - call `PARK_RESPONSE_SIGNAL_GENERIC_LIMITED`.
    - best module `lysosomal_apc__resid_inflammatory_nfkb`, endpoint
      `baseline_pre`.
    - RA adjusted coefficient `0.289`, p `0.0746`,
      target/generic ratio `3.72`.
    - IBD DC adjusted coefficient `0.260`, p `0.0369`,
      target/generic ratio `1.70`.
  - interpretation:
    - signal survives covariate adjustment but fails the target/generic
      specificity ratio gate in IBD.

- Wave77 `ETS2` local axis audit:
  - script: `scripts/v3_wave77_ets2_macrophage_axis_audit.py`
  - outputs: `results_v3/wave77_ets2_macrophage_axis_audit/`
  - inputs:
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/raw_remission_response_gene_tests.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/paired_gene_delta_tests.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
    - `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`
    - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
  - key result:
    - call `NO_GO_ETS2_LOCAL_AUDIT`.
    - broad positive diseases: Crohn disease and ulcerative colitis.
    - MS `GSE111972` direct effect `-0.0608`, p `0.8649`, FDR `0.9802`.
    - RA direct `ETS2` baseline responder effect `0.958`, p `0.00105`,
      FDR `0.00524`, but no MS, perturbation, target-resolution, or
      druggable-route support.
  - interpretation:
    - independent no-go confirmation for `ETS2`.

- Wave78 LILRB inhibitory-receptor target-level audit:
  - script: `scripts/v3_wave78_lilrb_family_target_audit.py`
  - outputs: `results_v3/wave78_lilrb_family_target_audit/`
  - prior-art artifact:
    - `subagents_v3/wave78a_lilrb_prior_art_feasibility.md`
  - inputs:
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
    - `results_v3/wave70c_inhibitory_receptor_geneformer_direction/geneformer_direction_candidate_calls.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_module_scores.tsv`
  - key result:
    - local call `NO_GO_LILRB_TARGET_LEVEL_CONVERGENCE`.
    - prior-art/translational call `PARK_DIRECTIONALITY`.
    - strongest IBD anti-TNF adjusted response effects:
      - `LILRB1` mono/macrophage delta `-1.035`, p `0.000937`,
        FDR `0.0120`.
      - `LILRB4` mono/macrophage delta `-1.476`, p `0.000730`,
        FDR `0.0113`.
      - `LILRB2` DC delta `-0.884`, p `0.00505`, FDR `0.0224`.
      - `LILRB3` mono/macrophage delta `-0.884`, p `0.0208`,
        FDR `0.0384`.
    - specificity blocker:
      - all LILRB genes have `broad_specific_positive_disease_count = 0`
        because same-context LILRA activating paralogs are stronger.
    - MS blocker:
      - `LILRB2` is nominally lower in MS white matter: delta `-0.730`,
        p `0.00778`.
    - RA blocker:
      - no LILRB-family member has a replicated RA suppression-response signal;
        `LILRB4` shows only weak restoration-like RA evidence.
    - genetics blocker:
      - target-level genetic breadth is absent or limited to one-disease proxy
        rows for `LILRB3`/`LILRB4`.
  - interpretation:
    - LILRB family remains a real myeloid/tolerance biology class but not a
      V3-valid cross-autoimmune/MS intervention point.
    - broad agonism is prior-art crowded; antagonism/depletion is oncology
      crowded and directionally risky for autoimmunity.

- Wave78 LILRB inhibitory-receptor target audit:
  - script: `scripts/v3_wave78_lilrb_inhibitory_receptor_audit.py`
  - outputs: `results_v3/wave78_lilrb_inhibitory_receptor_audit/`
  - sidecar:
    - `subagents_v3/wave78_lilrb_prior_art_directionality.md`
  - inputs:
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/wave62_opentargets_target_resolution/opentargets_qtl_coloc_rows.tsv`
    - `results_v3/wave70b_fc_ros_computational_scout/integrated_fc_ros_candidate_scout.tsv`
    - `results_v3/wave70c_inhibitory_receptor_geneformer_direction/geneformer_direction_candidate_calls.tsv`
    - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/all_gene_pair_metadata.tsv`
  - key result:
    - no LILRB member promoted.
    - `LILRB4` call `PARK_LILRB_DIRECTIONALLY_UNRESOLVED`; IBD response p
      `0.00819`, target/generic ratio `5.19`, but RA p `0.859`, MS null,
      and Wave70C no-go direction.
    - `LILRB2` call `PARK_LILRB_DIRECTIONALLY_UNRESOLVED`; Crohn/UC broad
      positives and Crohn/T1D pQTL colocalization, but RA p `0.561`, MS
      nominal down delta `-0.730`, p `0.00778`, FDR `0.834`, and Wave70C
      no-go direction.
    - `LILRB1` and `LILRB3` have partial IBD/broad signal only.
    - comparator `FCGR2B` passes adjusted RA/IBD response specificity but is
      blocked as broad Fc/inhibitory-receptor biology.
  - interpretation:
    - LILRB family remains a response-state comparator, not a V3 intervention
      claim.

- Wave79 non-LILRB targetability shortlist audit:
  - script: `scripts/v3_wave79_targetability_shortlist_audit.py`
  - outputs: `results_v3/wave79_targetability_shortlist_audit/`
  - inputs:
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/wave62_opentargets_target_resolution/opentargets_qtl_coloc_rows.tsv`
    - `results_v3/wave21_residual_druggability_scan/wave21_residual_druggability_ranked_full.tsv`
    - `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
    - `results_v3/wave71_global_survivor_meta_rank/global_survivor_meta_rank.tsv`
    - `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
    - `results_v3/wave18_foundation_rescue/geneformer_consolidated_context_metrics.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/all_gene_pair_metadata.tsv`
  - key result:
    - `CD58` parked, not promoted:
      - gate count 8.
      - MS L2G `0.951`.
      - strong-H4 QTL diseases Crohn and MS.
      - broad positives Crohn disease, T1D, UC.
      - APC/myeloid positive diseases Crohn disease and UC.
      - RA adjusted response p `0.00298`, target/generic ratio `11.71`.
      - IBD adjusted response p `0.173`, target/generic ratio `1.62`.
      - strict residual surviving disease count `0`.
    - `P4HB`, `SPNS1`, `SEL1L3` no-go:
      - P4HB mostly epithelial/stromal broad ER/redox signal with no MS anchor.
      - SPNS1 lacks MS/genetics/modality/response specificity.
      - SEL1L3 has nominal MS expression but stromal/endothelial localization
        and do-not-promote model evidence.
  - interpretation:
    - only `CD58` justified a narrow follow-up before sidecar review; no
      Wave79 finding.
  - sidecar:
    - artifact: `subagents_v3/wave79_targetability_prior_art_directionality.md`
    - call: `NO_PROMOTION_FOR_TARGETABILITY_SHORTLIST`
    - `CD58`: `PARK_PRIOR_ART_DIRECTIONALITY`; comparator/stratification axis
      only, not a novel target.
    - `SPNS1`: `PARK_PRECLINICAL_LYSOSOMAL_LIPID_FLUX_LEAD`; no translational
      target claim.
    - `P4HB`: `NO_GO_GENERIC_ER_REDox_PDI_TOXICITY_PRIOR_ART`.
    - `SEL1L3`: `NO_GO_UNCHARACTERIZED_MARKER_NO_MODALITY`.
    - updated interpretation:
      - do not run a CD58 target-promotion branch; any further CD58 work must
        be a closure/falsification or biomarker/stratification analysis.

- Wave80 `CD58`/CD2-axis deepening:
  - script: `scripts/v3_wave80_cd58_cd2_axis_deepening.py`
  - outputs: `results_v3/wave80_cd58_cd2_axis_deepening/`
  - inputs:
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
    - `results_v3/wave79_targetability_shortlist_audit/targetability_integrated_decision.tsv`
    - `results_v3/wave79_targetability_shortlist_audit/targetability_adjusted_response_convergence.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/wave62_opentargets_target_resolution/opentargets_qtl_coloc_rows.tsv`
  - key result:
    - call `PARK_CD58_CD2_AXIS_PRIOR_ART_OR_IBD_LIMITED`.
    - RA baseline `CD58` good-responder coefficient after generic, T-cell, and
      effector-memory T-cell adjustment: `0.870`, p `0.00871`.
    - Wave79 IBD response remains weak: p `0.173`, target/generic ratio
      `1.62`.
    - prior-art table documents MS CD58 genetics and alefacept/CD2-CD58
      autoimmune precedent in psoriasis and T1D.
  - interpretation:
    - `CD58` is strengthened as a response-context signal but blocked as a V3
      therapeutic finding by IBD weakness, direction conflict, and prior art.

- Wave81 perturbation-first rescue:
  - script: `scripts/v3_wave81_perturbation_first_rescue.py`
  - outputs: `results_v3/wave81_perturbation_first_rescue/`
  - sidecar:
    - `subagents_v3/wave81_perturbation_first_rescue_scout.md`
  - inputs:
    - `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`
    - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
    - `results_v3/wave57_intervention_first_geneformer_screen/wave57_geneformer_gene_summary.tsv`
    - `results_v3/wave69d_gse282122_geneformer_remission_centroid/geneformer_remission_gene_summary.tsv`
    - `results_v3/wave70c_inhibitory_receptor_geneformer_direction/geneformer_direction_gene_summary.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/raw_remission_response_gene_tests.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/paired_gene_delta_tests.tsv`
    - `results_v3/wave71_global_survivor_meta_rank/global_survivor_meta_rank.tsv`
  - corrections:
    - table-presence support was replaced with strict positive support:
      direct perturbation requires a non-unresolved screen call or
      non-not-nominated selective transcript perturbation;
      foundation-model support requires positive support contexts with token
      coverage.
    - missing blocker fields are treated as empty rather than literal `nan`.
  - key result:
    - no `REOPEN_PERTURBATION_FIRST_TARGET`.
    - top parked rows after strict support:
      - `DAB2`: direct efferocytosis support, MS expression p `0.0111`, IBD
        nominal response, but no genetics/modality/model/breadth.
      - `CD9`: direct efferocytosis support, MS expression p `0.00197`, but no
        genetics/breadth/modality/model.
      - `PARK7`: Geneformer support (`wave57:support=2`) plus modality channel,
        but no MS anchor, no response-FDR support, and insufficient breadth.
      - `PSAP`: Geneformer support (`wave57:support=1`) plus MS expression p
        `0.0223`, but no genetics/modality/breadth.
  - interpretation:
    - perturbation/model evidence alone is insufficient; no Wave81 candidate is
      intervention-grade.

- Wave82 parked intervention-route audit:
  - script: `scripts/v3_wave82_parked_intervention_route_audit.py`
  - outputs: `results_v3/wave82_parked_intervention_route_audit/`
  - inputs:
    - `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
    - `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
    - `results_v3/wave21_residual_druggability_scan/wave21_residual_druggability_ranked_full.tsv`
  - candidates:
    - residual candidates: `DAB2`, `CD9`, `PSAP`, `PARK7`, `LYN`, `FAM49B`,
      `LRRC61`, `HEXA`, `HEXB`, `DAP`, `FMNL2`.
    - false-positive controls: `SP140`, `RGS14`, `STAT4`.
  - key result:
    - `REOPEN_INTERVENTION_ROUTE`: 0.
    - `PARK_ROUTE_POSSIBLE_BUT_EVIDENCE_INCOMPLETE`: 1 (`PARK7`).
    - `NO_GO_NO_CREDIBLE_INTERVENTION_ROUTE`: 10.
    - `NO_GO_FALSE_POSITIVE_CONTROL`: 3.
  - interpretation:
    - `PARK7` has only incomplete route plausibility and fails MS anchor,
      cross-disease breadth, and response-FDR gates.
    - all other residuals fail reachability, genetics/target-resolution, MS
      anchoring, response-FDR support, or safe direction.

- Wave79-B targetability residual stress test:
  - script: `scripts/v3_wave79_targetability_shortlist_residual_audit.py`
  - outputs: `results_v3/wave79_targetability_shortlist_residual_audit/`
  - inputs:
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
    - `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/*`
  - key result:
    - call `PARK_CD58_MS_GENETIC_BUT_NO_STATE_RESPONSE_CONVERGENCE`.
    - `CD58`: MS genetic anchor true (`ms_max_l2g_score=0.9514`) but MS
      white-matter expression anchor false (`delta=0.1798`, p `0.3111`) and
      no RA/IBD suppression-response support.
    - `SEL1L3`: MS expression anchor true (`delta=0.9225`, p `0.0181`) but no
      genetic, response, modality, or residual disease breadth.
    - `P4HB`: one residual Sjogren stromal context (`residual_delta=0.7515`,
      p `0.0159`) but no MS anchor and prior-art/safety blockers.
    - `SPNS1`: one residual Sjogren APC context (`residual_delta=0.8269`,
      p `0.0270`) but no MS anchor, modality, or genetics.
  - sidecar:
    - artifact: `subagents_v3/wave79a_targetability_shortlist_prior_art.md`
    - `CD58`: `BLOCKED_BY_PRIOR_ART`.
    - `P4HB`: `BLOCKED_BY_PRIOR_ART`.
    - `SPNS1`: `NO_GO`.
    - `SEL1L3`: `NO_GO`.
  - interpretation:
    - targetability shortlist closed; do not reopen expression-derived
      targetability without a new perturbation, genetics, or clinical-response
      anchor.

- Wave81 perturbation-first rescue audit:
  - script: `scripts/v3_wave81_perturbation_first_rescue.py`
  - outputs: `results_v3/wave81_perturbation_first_rescue/`
  - inputs:
    - `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`
    - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
    - `results_v3/wave57_intervention_first_geneformer_screen/wave57_geneformer_gene_summary.tsv`
    - `results_v3/wave69d_gse282122_geneformer_remission_centroid/geneformer_remission_gene_summary.tsv`
    - `results_v3/wave70c_inhibitory_receptor_geneformer_direction/geneformer_direction_gene_summary.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/*`
    - `results_v3/wave71_global_survivor_meta_rank/global_survivor_meta_rank.tsv`
  - implementation correction:
    - initial table-presence model/direct support was rejected as too weak;
      final script requires positive model support contexts and non-unresolved
      direct perturbation calls.
  - key result after stricter gates:
    - `REOPEN_PERTURBATION_FIRST_TARGET`: `0`.
    - `PARK_PERTURBATION_FIRST_CANDIDATE`: `89`.
    - `NO_GO_PERTURBATION_FIRST_BLOCKED`: `42`.
    - `NO_GO_NO_PERTURBATION_SUPPORT`: `150`.
    - false-positive controls demoted:
      - `SP140`: Geneformer `support_contexts=0`, efferocytosis `UNRESOLVED`,
        contrast FDR `0.920`.
      - `RGS14`: Geneformer `support_contexts=0`, no direct perturbation.
      - `STAT4`: direct perturbation `null_or_wrong_direction`, no positive
        model support.
  - interpretation:
    - perturbation-first scan does not yet identify a promotable V3 target;
      proceed to Wave82 intervention-route stress testing of parked candidates.

- Wave82 parked perturbation intervention audit:
  - script: `scripts/v3_wave82_parked_perturbation_intervention_audit.py`
  - outputs: `results_v3/wave82_parked_perturbation_intervention_audit/`
  - sidecars:
    - `subagents_v3/wave82a_parked_perturbation_feasibility.md`
    - `subagents_v3/wave82b_cross_disease_evidence_stress_test.md`
  - inputs:
    - `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
    - `results_v3/wave57_intervention_first_geneformer_screen/wave57_geneformer_gene_summary.tsv`
    - `results_v3/wave69d_gse282122_geneformer_remission_centroid/geneformer_remission_gene_summary.tsv`
    - `results_v3/wave70c_inhibitory_receptor_geneformer_direction/geneformer_direction_gene_summary.tsv`
    - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
    - `results_v3/gse111972_full_ms_wm_signature.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/*`
    - live/cached ChEMBL, UniProt, Europe PMC, ClinicalTrials.gov API calls in
      `data/raw_v3/wave82_api_cache/`
  - key result:
    - verdict `NO_PROMOTABLE_INTERVENTION_ROUTE`.
    - call counts:
      - `PARK_READOUT_OR_PRECLINICAL_PROBE`: `7`.
      - `NO_GO_WAVE82_BLOCKED`: `3`.
    - `SP140`: strongest evidence count (`4`) but blocked by no positive
      strict perturbation/model support and prior directionality/chemistry
      concerns.
    - `LYN`: ChEMBL-rich and model/state positive, but no MS anchor/genetics
      and broad SRC-family kinase safety/direction blocker.
    - `STAT4`: broad genetics, but no positive strict perturbation/model
      support and not selectively druggable in the correct direction.
    - `CD9`, `DAB2`, `PSAP`, `RGS14`, `PARK7`, `HEXA`, `HEXB`: readout or
      preclinical probes only.
  - public-source pinning:
    - UniProt accessions pinned to avoid ambiguous gene-name resolution:
      `DAB2=P98082`, `CD9=P21926`, `PARK7=Q99497`, `PSAP=P07602`,
      `LYN=P07948`, `HEXA=P06865`, `HEXB=P07686`, `SP140=Q13342`,
      `RGS14=O43566`, `STAT4=Q14765`.
    - ChEMBL target IDs pinned where verified:
      `PARK7=CHEMBL5169188;CHEMBL6066048`,
      `PSAP=CHEMBL3580523`,
      `LYN=CHEMBL3905;CHEMBL6066565`,
      `HEXA=CHEMBL1250415;CHEMBL3038485`,
      `HEXB=CHEMBL5877;CHEMBL3038485`,
      `SP140=CHEMBL3108643;CHEMBL4105997`,
      `STAT4=CHEMBL4523296;CHEMBL4523706`.
  - interpretation:
    - parked perturbation candidates do not rescue a V3 intervention claim.
      The next branch should be genetics-first/druggable-survivor scanning.

- Wave82 parked intervention-route audit:
  - script: `scripts/v3_wave82_parked_intervention_route_audit.py`
  - outputs: `results_v3/wave82_parked_intervention_route_audit/`
  - inputs:
    - `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
    - `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
    - `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
    - `results_v3/wave21_residual_druggability_scan/wave21_residual_druggability_ranked_full.tsv`
  - candidate set:
    - residual candidates: `DAB2`, `CD9`, `PSAP`, `PARK7`, `LYN`, `FAM49B`,
      `LRRC61`, `HEXA`, `HEXB`, `DAP`, `FMNL2`;
    - false-positive controls: `SP140`, `RGS14`, `STAT4`.
  - key result:
    - `REOPEN_INTERVENTION_ROUTE`: `0`.
    - `PARK_ROUTE_POSSIBLE_BUT_EVIDENCE_INCOMPLETE`: `1` (`PARK7`).
    - `NO_GO_NO_CREDIBLE_INTERVENTION_ROUTE`: `10`.
    - `NO_GO_FALSE_POSITIVE_CONTROL`: `3`.
  - sidecar:
    - artifact: `subagents_v3/wave82_cross_disease_residuals.md`.
    - promotion count `0`.
    - no residual candidate has a real pan-autoimmune lipid-lysosomal/myeloid
      mechanism; failures include FDR failure, generic macrophage/tissue
      abundance, tissue-cell mismatch, mouse-only perturbation, and missing MS
      genetics.
  - interpretation:
    - residual perturbation/model candidates are not promotable as targets.
    - next branch should invert the search: reachable intervention class first,
      then test whether the intervention controls the shared module.

- Wave83 intervention-class-first scan:
  - script: `scripts/v3_wave83_intervention_class_first_scan.py`
  - outputs: `results_v3/wave83_intervention_class_first_scan/`
  - inputs:
    - `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
    - `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
    - `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
    - `results_v3/wave57_intervention_first_geneformer_screen/wave57_geneformer_gene_summary.tsv`
    - `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
    - `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`
    - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
    - `results_v3/wave24_l1000_recurrent_reversal/recurrent_l1000_mechanism_summary.tsv`
    - `results_v3/wave61_perturbation_first_guardrail/intervention_evidence_tiers.tsv`
  - method:
    - built a local candidate universe from reachable/intervention-class
      evidence first, then overlaid module recurrence, MS evidence, genetics,
      foundation/direct perturbation, response, and blocker fields.
  - key result:
    - `REOPEN_REACHABLE_INTERVENTION_CANDIDATE`: `0`.
    - `PARK_REACHABLE_BUT_EVIDENCE_INCOMPLETE`: `10`.
    - `NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED`: `39`.
    - `NO_GO_NOT_REACHABLE_FIRST_CLASS`: `152`.
  - parked candidates:
    - `MMP7`, `CD274`, `IL15`, `CASP4`, `KCNJ2`, `CD74`, `HLA-DRB1`,
      `APOL1`, `TIMP1`, `IL23A`.
  - interpretation:
    - route-first scanning does not provide a promotable target.
    - parked candidates are mostly broad inflammatory, prior-art saturated,
      or MS-unanchored; they are better suited to stratification testing than
      direct target nomination.

- Wave83 intervention-class meta-rank:
  - script: `scripts/v3_wave83_intervention_class_meta_rank.py`
  - outputs: `results_v3/wave83_intervention_class_meta_rank/`
  - inputs:
    - `results_v3/wave23_metabolite_barrier_circuit/wave23_ranked_routes.tsv`
    - `results_v3/wave44_cfb_complement_stratification_audit/wave21_prior_CFB_row.tsv`
    - `results_v3/wave48_resolution_reopener_audit/route_reopener_audit.tsv`
    - `results_v3/wave48_resolution_reopener_audit/decision_matrix.tsv`
    - `results_v3/wave50_gpr65_acid_sensing_gpcr_audit/gpr65_audit.tsv`
    - `results_v3/wave53_perturbation_first_pivot/perturbation_first_audit.tsv`
    - `results_v3/wave54_mfge8_debris_opsonin_audit/decision_matrix.tsv`
    - `results_v3/wave58_cxcr2_il7r_targeted_audit/cxcr2_il7r_decision.tsv`
    - `results_v3/wave59_lysosomal_sphingolipid_model_reopener_audit/lysosomal_sphingolipid_decision.tsv`
    - `results_v3/wave64_slamf7_perturbation_audit/wave64c_gate_row.tsv`
    - `results_v3/wave72_lipid_mediator_intervention_scout/lipid_mediator_decisions.tsv`
    - `results_v3/wave73_p2rx7_stratification_test/p2rx7_stratification_decision.tsv`
    - `results_v3/wave74_gpr183_oxysterol_niche/integrated_decision.tsv`
    - `results_v3/wave74_ephx2_oxylipin_specificity/final_decision.tsv`
    - `results_v3/wave78_lilrb_inhibitory_receptor_audit/lilrb_integrated_decision.tsv`
    - `results_v3/wave79_targetability_shortlist_audit/targetability_integrated_decision.tsv`
    - `results_v3/wave80_cd58_cd2_axis_deepening/cd58_cd2_axis_decision.tsv`
    - `results_v3/wave82_parked_intervention_route_audit/parked_intervention_route_audit.tsv`
  - key result:
    - corrected `REOPEN_INTERVENTION_CLASS`: `0`.
    - `PARK_INTERVENTION_CLASS_NEEDS_FORCING_TEST`: `1`
      (`GPR183_EBI2_OXYSTEROL_NICHE`).
    - `NO_GO_INTERVENTION_CLASS_META_RANK`: `58`.
  - correction:
    - initial `CD58_TARGETABILITY` reopen was rejected as a scoring artifact
      because the source audit call was `PARK` and only one support channel was
      present.
  - interpretation:
    - no direct intervention class satisfies the V3 gate stack.
    - the next useful test is stratification: whether this module identifies
      responders/nonresponders to existing therapies across diseases.
## Wave83 Intervention-Class-First Survivor Sweep

Timestamp: 2026-05-27 18:17 CEST

Script:

- `scripts/v3_wave83_intervention_class_first_scan.py`

Inputs:

- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave34a_genetics_first_target_rescue/genetics_first_candidate_rank.tsv`
- `results_v3/wave57_intervention_first_geneformer_screen/wave57_geneformer_gene_summary.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave24_l1000_recurrent_reversal/recurrent_l1000_mechanism_summary.tsv`
- `results_v3/wave61_perturbation_first_guardrail/intervention_evidence_tiers.tsv`
- `results_v3/wave71_global_survivor_meta_rank/global_survivor_meta_rank.tsv`

Outputs:

- `results_v3/wave83_intervention_class_first_scan/reachable_intervention_rank.tsv`
- `results_v3/wave83_intervention_class_first_scan/reachable_intervention_class_summary.tsv`
- `results_v3/wave83_intervention_class_first_scan/summary.json`
- `results_v3/wave83_intervention_class_first_scan/REPORT.md`

Result:

- `735` reachable/genetics/intervention-class candidates scanned.
- No `REOPEN_REACHABLE_INTERVENTION_CANDIDATE` rows.
- The strongest high-scoring rows were prior-closed comparator axes, not live
  V3 candidates.

## Wave85 External GEO Anti-TNF Validation

Timestamp: 2026-05-27 18:36 CEST

Raw inputs:

- `data/raw_v3/wave84_external_geo/GSE12251_series_matrix.txt.gz`
  - NCBI GEO series matrix.
  - Platform: `GPL570`.
  - GEO matrix title: "A Predictive Response Signature to Infliximab Treatment
    in Ulcerative Colitis".
  - PubMed ID listed in matrix: `19700435`.
  - Used samples: baseline UC colonic biopsies before infliximab, response
    labelled by week-8 endoscopic/histologic healing.
- `data/raw_v3/wave84_external_geo/GSE14580_series_matrix.txt.gz`
  - NCBI GEO series matrix.
  - Platform: `GPL570`.
  - GEO matrix title: "Mucosal gene signatures to predict response to
    infliximab in patients with ulcerative colitis".
  - PubMed ID listed in matrix: `19700435`.
  - Used samples: baseline active UC colonic biopsies before first infliximab;
    controls excluded.
  - Independence warning: the UC patient GSMs overlap the UC subset of
    GSE16879 and are not counted as independent validation.
- `data/raw_v3/wave84_external_geo/GSE16879_series_matrix.txt.gz`
  - NCBI GEO series matrix.
  - Platform: `GPL570`.
  - GEO matrix title: "Mucosal expression profiling in patients with
    inflammatory bowel disease before and after first infliximab treatment".
  - PubMed ID listed in matrix: `19956723`.
  - Used samples: baseline UC, Crohn colitis, and Crohn ileitis mucosal
    biopsies before first infliximab; controls and post-treatment samples
    excluded from baseline response tests.
- `data/raw_v3/wave84_external_geo/GPL570.annot.gz`
  - NCBI GEO GPL570 annotation downloaded from
    `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPLnnn/GPL570/annot/GPL570.annot.gz`.
  - Used for probe-to-gene mapping of V3 module genes.

Script:

- `scripts/v3_wave85_external_geo_antitnf_validation.py`

Outputs:

- `results_v3/wave85_external_geo_antitnf_validation/series_matrix_summaries.tsv`
- `results_v3/wave85_external_geo_antitnf_validation/gpl570_module_probe_gene_map.tsv`
- `results_v3/wave85_external_geo_antitnf_validation/external_geo_module_gene_coverage.tsv`
- `results_v3/wave85_external_geo_antitnf_validation/external_geo_patient_module_scores.tsv`
- `results_v3/wave85_external_geo_antitnf_validation/external_geo_response_tests.tsv`
- `results_v3/wave85_external_geo_antitnf_validation/external_geo_primary_meta_summary.tsv`
- `results_v3/wave85_external_geo_antitnf_validation/summary.json`
- `results_v3/wave85_external_geo_antitnf_validation/REPORT.md`

Processing:

- Series matrices were parsed directly.
- Values were log2-transformed where raw/global-scaled intensity values
  exceeded 50.
- Probes were collapsed to module genes by median across matching GPL570 probes.
- Genes were z-scored within each tested cohort before module scoring.
- Duplicate samples for the same patient were averaged before statistical
  testing.
- `GSE14580_UC_Leuven_baseline` and `GSE16879_UC_Leuven_baseline` are marked
  with the same overlap group.

## Wave86 External GEO Anti-TNF Gene Driver Decomposition

Timestamp: 2026-05-27 18:49 CEST

Script:

- `scripts/v3_wave86_external_geo_antitnf_gene_driver.py`

Inputs:

- Reused Wave85 matrices:
  - `data/raw_v3/wave84_external_geo/GSE12251_series_matrix.txt.gz`
  - `data/raw_v3/wave84_external_geo/GSE14580_series_matrix.txt.gz`
  - `data/raw_v3/wave84_external_geo/GSE16879_series_matrix.txt.gz`
  - `data/raw_v3/wave84_external_geo/GPL570.annot.gz`

Outputs:

- `results_v3/wave86_external_geo_antitnf_gene_driver/external_geo_gene_coverage.tsv`
- `results_v3/wave86_external_geo_antitnf_gene_driver/external_geo_gene_patient_scores.tsv`
- `results_v3/wave86_external_geo_antitnf_gene_driver/external_geo_gene_response_tests.tsv`
- `results_v3/wave86_external_geo_antitnf_gene_driver/external_geo_gene_meta_rank.tsv`
- `results_v3/wave86_external_geo_antitnf_gene_driver/module_gene_membership.tsv`
- `results_v3/wave86_external_geo_antitnf_gene_driver/summary.json`
- `results_v3/wave86_external_geo_antitnf_gene_driver/REPORT.md`

Primary independent contexts counted:

- `GSE12251_UC_ACT1_baseline`
- `GSE14580_UC_Leuven_baseline`
- `GSE16879_Crohn_colitis_Leuven_baseline`
- `GSE16879_Crohn_ileitis_Leuven_baseline`

Non-independent/sensitivity contexts retained but not counted as primary:

- `GSE16879_UC_Leuven_baseline`
- `GSE16879_Crohn_all_Leuven_baseline`
- `GSE16879_all_IBD_Leuven_baseline`

Result summary:

- `45` module genes tested.
- `16` genes called `GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR`.
- `9` genes called `PARK_DIRECTIONAL_NONRESPONSE_GENE`.
- Top gene: `IL1B`.

## Wave87 Cross-System Anti-TNF Resistance Gene Check

Timestamp: 2026-05-27 18:49 CEST

Script:

- `scripts/v3_wave87_cross_system_antitnf_resistance_gene_check.py`

Inputs:

- `results_v3/wave86_external_geo_antitnf_gene_driver/external_geo_gene_meta_rank.tsv`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/raw_remission_response_gene_tests.tsv`

Outputs:

- `results_v3/wave87_cross_system_antitnf_resistance_gene_check/ra_synovium_baseline_gene_response_tests.tsv`
- `results_v3/wave87_cross_system_antitnf_resistance_gene_check/gse282122_top_gene_response_delta_summary.tsv`
- `results_v3/wave87_cross_system_antitnf_resistance_gene_check/cross_system_antitnf_gene_integration.tsv`
- `results_v3/wave87_cross_system_antitnf_resistance_gene_check/summary.json`
- `results_v3/wave87_cross_system_antitnf_resistance_gene_check/REPORT.md`

Processing:

- RA baseline pre-treatment synovium counts were converted to logCPM and
  z-scored per gene.
- Baseline gene scores were residualized against `pathotype`, `biologic`,
  `inflammatory_score`, and `das28_score`.
- Response endpoint: `responder_moderate_or_good` from the existing GSE198520
  metadata table.

Result summary:

- `25` Wave86 anchor/park genes considered.
- `22` genes had usable RA synovium expression after finite-value filtering.
- `2` genes parked as cross-system anti-TNF resistance genes:
  - `LAMP3`
  - `IL1B`

## Wave89 Psoriasis GSE85034 Response Validation

Timestamp: 2026-05-27 19:10 CEST

Script:

- `scripts/v3_wave89_psoriasis_gse85034_response_validation.py`

Inputs:

- `data/raw_v3/wave89_psoriasis_response/GSE85034_series_matrix.txt.gz`
  - NCBI GEO series matrix downloaded from
    `https://ftp.ncbi.nlm.nih.gov/geo/series/GSE85nnn/GSE85034/matrix/GSE85034_series_matrix.txt.gz`.
- `data/raw_v3/wave89_psoriasis_response/GPL10558.annot.gz`
  - GPL10558 platform annotation downloaded from
    `https://ftp.ncbi.nlm.nih.gov/geo/platforms/GPL10nnn/GPL10558/annot/GPL10558.annot.gz`.
- `results_v3/wave86_external_geo_antitnf_gene_driver/external_geo_gene_meta_rank.tsv`
- `results_v3/wave87_cross_system_antitnf_resistance_gene_check/cross_system_antitnf_gene_integration.tsv`

Outputs:

- `results_v3/wave89_psoriasis_gse85034_response/sample_metadata.tsv`
- `results_v3/wave89_psoriasis_gse85034_response/patient_response_table.tsv`
- `results_v3/wave89_psoriasis_gse85034_response/candidate_gene_sources.tsv`
- `results_v3/wave89_psoriasis_gse85034_response/platform_gene_coverage.tsv`
- `results_v3/wave89_psoriasis_gse85034_response/treatment_response_counts.tsv`
- `results_v3/wave89_psoriasis_gse85034_response/psoriasis_baseline_gene_response_tests.tsv`
- `results_v3/wave89_psoriasis_gse85034_response/psoriasis_baseline_module_response_tests.tsv`
- `results_v3/wave89_psoriasis_gse85034_response/primary_gene_cross_system_integration.tsv`
- `results_v3/wave89_psoriasis_gse85034_response/summary.json`
- `results_v3/wave89_psoriasis_gse85034_response/REPORT.md`

Processing:

- Reconstructed week-16 PASI75 response from GEO PASI fields.
- Used baseline lesional skin (`timepoint: LS`) only for expression
  predictors.
- Treated adalimumab as the primary anti-TNF arm and methotrexate as a
  therapy-specificity control.
- Subject 28 was excluded from baseline-lesional response tests because the
  available lesional sample is annotated as `WK1_LS`, not baseline `LS`.

Result summary:

- Analysis call: `WEAK_DIRECTIONAL_THIRD_DISEASE_SUPPORT_ONLY`.
- Adalimumab evaluable subjects: `14` (`9` PASI75 responders, `5`
  nonresponders).
- `IL1B` was same-direction but weak in adalimumab psoriasis:
  Hedges g `-0.6325`, high-expression nonresponse AUC `0.5556`, p `0.3940`.
- `LAMP3` reversed in adalimumab psoriasis:
  Hedges g `0.4960`, high-expression nonresponse AUC `0.3556`, p `0.2968`.
- `LPL` was the strongest adalimumab gene-level signal among tested module
  genes: Hedges g `-2.2089`, high-expression nonresponse AUC `0.9556`,
  p `0.0111`, FDR `0.4998`.

## Wave90 LPL Cross-Disease Audit

Timestamp: 2026-05-27 19:19 CEST

Script:

- `scripts/v3_wave90_lpl_cross_disease_audit.py`

Inputs:

- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/gse111972_module_contrasts.tsv`
- `results_v3/direct_h5ad_gene_replication/direct_h5ad_gene_donor_comparisons.tsv`
- `results_v3/wave86_external_geo_antitnf_gene_driver/external_geo_gene_meta_rank.tsv`
- `results_v3/wave86_external_geo_antitnf_gene_driver/external_geo_gene_response_tests.tsv`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
- `results_v3/wave89_psoriasis_gse85034_response/psoriasis_baseline_gene_response_tests.tsv`

Outputs:

- `results_v3/wave90_lpl_cross_disease_audit/lpl_ms_bulk_evidence.tsv`
- `results_v3/wave90_lpl_cross_disease_audit/lpl_direct_h5ad_case_control_evidence.tsv`
- `results_v3/wave90_lpl_cross_disease_audit/lpl_ibd_antitnf_meta_evidence.tsv`
- `results_v3/wave90_lpl_cross_disease_audit/lpl_ibd_antitnf_context_tests.tsv`
- `results_v3/wave90_lpl_cross_disease_audit/lpl_ra_synovium_baseline_response.tsv`
- `results_v3/wave90_lpl_cross_disease_audit/lpl_psoriasis_baseline_response.tsv`
- `results_v3/wave90_lpl_cross_disease_audit/lpl_response_direction_summary.tsv`
- `results_v3/wave90_lpl_cross_disease_audit/summary.json`
- `results_v3/wave90_lpl_cross_disease_audit/REPORT.md`

Result summary:

- Analysis call:
  `PARK_LPL_RESPONSE_MARKER_WITH_CASE_CONTROL_CONFLICT`.
- `LPL` is MS white-matter lesion-up in `GSE111972`:
  delta `1.7596`, Hedges g `1.8731`, p `0.000622`, FDR `0.7144`.
- The lipid-loader module is MS white-matter-up:
  delta `0.4784`, Hedges g `1.3791`, p `0.00528`, FDR `0.01916`.
- Anti-TNF response direction is nonresponse-high in IBD, RA, and psoriasis,
  but only the small psoriasis adalimumab arm is nominally strong.
- Direct h5ad donor case-control data conflict with direct target promotion:
  Crohn colon epithelial LPL is case-high, while psoriasis skin APC LPL is
  control-high.

## Wave91 Lipid/Lysosomal Module Intervention-Rank Audit

Timestamp: 2026-05-27 19:41 CEST

Script:

- `scripts/v3_wave91_lipid_lysosomal_module_intervention_rank.py`

Inputs:

- `results_v3/wave89_psoriasis_gse85034_response/psoriasis_baseline_gene_response_tests.tsv`
- `results_v3/wave89_psoriasis_gse85034_response/candidate_gene_sources.tsv`
- `results_v3/wave86_external_geo_antitnf_gene_driver/external_geo_gene_meta_rank.tsv`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/direct_h5ad_gene_replication/direct_h5ad_gene_donor_comparisons.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`

Outputs:

- `results_v3/wave91_lipid_lysosomal_module_intervention_rank/ra_all_candidate_response_tests.tsv`
- `results_v3/wave91_lipid_lysosomal_module_intervention_rank/module_wide_evidence_matrix.tsv`
- `results_v3/wave91_lipid_lysosomal_module_intervention_rank/lipid_lysosomal_intervention_rank.tsv`
- `results_v3/wave91_lipid_lysosomal_module_intervention_rank/summary.json`
- `results_v3/wave91_lipid_lysosomal_module_intervention_rank/REPORT.md`

Result summary:

- Analysis call:
  `NO_REOPEN_MODULE_WIDE_LIPID_LYSOSOMAL_INTERVENTION_NODE`.
- Candidate genes tested: `45`; reopened: `0`; parked: `10`.
- Strict call counts:
  - `NO_GO_NO_MS_WHITE_MATTER_SINGLE_GENE_ANCHOR`: `20`.
  - `NO_GO_RESPONSE_SIGNAL_NOT_SHARED_ACROSS_DISEASES`: `13`.
  - `PARK_RESPONSE_DIRECTIONS_WEAK_OR_UNDERPOWERED`: `10`.
  - `NO_GO_DIRECT_ATLAS_CONTRADICTION`: `1`.
  - `NO_GO_ROUTE_BLOCKED`: `1`.
- Interpretation:
  - The measured lipid/lysosomal genes behave more like state markers than
    unblocked intervention-grade controllers.
  - Direct module-internal targeting is now deprioritized.

## Wave91 Lipid-Neighborhood Controller Scan

Timestamp: 2026-05-27 19:38 CEST

Script:

- `scripts/v3_wave91_lipid_neighborhood_controller_scan.py`

Inputs:

- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/direct_h5ad_gene_replication/direct_h5ad_gene_donor_comparisons.tsv`
- `results_v3/wave86_external_geo_antitnf_gene_driver/external_geo_gene_meta_rank.tsv`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
- `results_v3/wave89_psoriasis_gse85034_response/psoriasis_baseline_gene_response_tests.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- existing Geneformer delete outputs under `results_v3/geneformer_*` and
  `results_v3/wave57_intervention_first_geneformer_screen/`.

Outputs:

- `results_v3/wave91_lipid_neighborhood_controller_scan/lipid_neighborhood_controller_rank.tsv`
- `results_v3/wave91_lipid_neighborhood_controller_scan/summary.json`
- `results_v3/wave91_lipid_neighborhood_controller_scan/REPORT.md`

Result summary:

- `17` lipid-neighborhood candidates scanned.
- `FABP5` was the only candidate parked for deep validation, with score
  `7.05`.
- `FABP5` was not promoted because it retained case-control directional
  conflict and weak/inconsistent response evidence.

## Wave92 FABP5 Prior-Art Audit

Timestamp: 2026-05-27 19:38 CEST

Script:

- `scripts/v3_wave92_fabp5_prior_art_audit.py`

Inputs/queries:

- PubMed E-utilities queries:
  - `FABP5 multiple sclerosis`
  - `"fatty acid-binding protein 5" "multiple sclerosis"`
  - `FABP5 experimental autoimmune encephalomyelitis`
  - `FABP5 inhibitor autoimmune`
  - `FABP5 psoriasis`
  - `FABP5 inflammatory bowel disease`
  - `FABP5 rheumatoid arthritis`
- ClinicalTrials API queries:
  - `FABP5`
  - `"fatty acid binding protein 5"`
  - `MF6 FABP`
  - `FABP inhibitor autoimmune`
- Patent search URLs recorded for Google Patents and Espacenet.

Outputs:

- `results_v3/wave92_fabp5_prior_art_audit/pubmed_query_log.tsv`
- `results_v3/wave92_fabp5_prior_art_audit/pubmed_records.tsv`
- `results_v3/wave92_fabp5_prior_art_audit/clinicaltrials_records.tsv`
- `results_v3/wave92_fabp5_prior_art_audit/patent_search_urls.tsv`
- `results_v3/wave92_fabp5_prior_art_audit/summary.json`
- `results_v3/wave92_fabp5_prior_art_audit/REPORT.md`

Result summary:

- Analysis call:
  `FABP5_PRIOR_ART_BLOCKED_FOR_MS_THERAPEUTIC_NOVELTY`.
- Blocking PubMed records:
  - PMID `34624687`, DOI `10.1016/j.ebiom.2021.103582`
  - PMID `33124722`, DOI `10.1096/fj.202001539RR`

## Wave92 Lipid-State Controller Route Audit

Timestamp: 2026-05-27 19:56 CEST

Script:

- `scripts/v3_wave92_lipid_state_controller_route_audit.py`

Inputs:

- External IBD anti-TNF GEO series under `data/raw_v3/wave84_external_geo/`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
- `data/raw_v3/wave89_psoriasis_response/GSE85034_series_matrix.txt.gz`
- `data/raw_v3/wave89_psoriasis_response/GPL10558.annot.gz`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/wave30_niche_driver_audit/niche_driver_axis_audit.tsv`
- `results_v3/wave32c_resolution_prior_art_audit/route_feasibility_ranked.tsv`
- `results_v3/wave48_resolution_reopener_audit/route_reopener_audit.tsv`
- `results_v3/wave74_gpr183_oxysterol_niche/integrated_decision.tsv`

Outputs:

- `results_v3/wave92_lipid_state_controller_route_audit/external_ibd_controller_route_response_tests.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/ra_controller_route_response_tests.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/psoriasis_controller_route_response_tests.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/route_gene_coverage.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/controller_route_response_summary.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/ms_white_matter_controller_route_support.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/broad_h5ad_controller_route_summary.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/controller_route_prior_status.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/controller_route_rank.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/summary.json`
- `results_v3/wave92_lipid_state_controller_route_audit/REPORT.md`

Result summary:

- Analysis call: `NO_REOPEN_CONTROLLER_ROUTE`.
- Routes tested: `15`; reopened: `0`.
- Top route: `CD300_RECEPTOR_SPECIFIC_TUNING`, but it fails the MS
  white-matter route anchor.
- `LXR_ABCA1_ABCG1_EFFLUX` is the only tested controller route with a strong
  MS white-matter route anchor, but it is prior-art/safety blocked and lacks
  broad supportive atlas recurrence.

## Wave93 GPR183/EBI2 Oxysterol-Niche Forcing Test

Timestamp: 2026-05-27 19:48 CEST

Script:

- `scripts/v3_wave93_gpr183_oxysterol_forcing_test.py`

Inputs:

- `results_v3/wave74_gpr183_oxysterol_niche/`
- `results_v3/wave83_intervention_class_meta_rank/intervention_class_meta_rank.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- IBD external anti-TNF GEO data under `data/raw_v3/wave84_external_geo/`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
- `data/raw_v3/wave89_psoriasis_response/GSE85034_series_matrix.txt.gz`
- `data/raw_v3/wave89_psoriasis_response/GPL10558.annot.gz`
- ChEMBL API target/activity queries
- PubMed E-utilities queries
- ClinicalTrials.gov API queries
- Google Patents and Espacenet search URLs

Outputs:

- `results_v3/wave93_gpr183_oxysterol_forcing_test/ms_gse111972_target_gene_rows.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/broad_h5ad_target_gene_rows.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/broad_h5ad_target_gene_summary.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/ibd_external_antitnf_gene_response_tests.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/ibd_external_antitnf_gene_response_meta.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/ra_gse198520_baseline_gene_response_tests.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/ra_gse198520_baseline_gene_response_meta.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/psoriasis_gse85034_baseline_gene_response_tests.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/psoriasis_gse85034_ada_gene_response_meta.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/target_resolution_rows.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/chembl_target_query.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/pubmed_query_log.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/pubmed_records.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/clinicaltrials_records.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/patent_search_urls.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/gate_audit.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/integrated_decision.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/summary.json`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/REPORT.md`

Result summary:

- Analysis call:
  `NO_GO_GPR183_NO_MS_RECEPTOR_OR_LIGAND_ANCHOR`.
- Current rerun has local expression/response outputs but PubMed and ChEMBL
  API calls failed with DNS errors in the sandbox. The PubMed/ChEMBL fields in
  the current Wave93 artifacts must therefore not be used for novelty or
  druggability claims.
- The no-go result does not depend on those APIs:
  - `GPR183` MS white-matter delta `-0.1364`, p `0.6637`.
  - ligand-production module mean effect `0.0711`.
  - coherent ligand/receptor/response disease count `0`.
  - target-resolved genetics breadth `2`.
  - response support systems `1`.

## Wave94 Accessible State Candidate Rerank

Timestamp: 2026-05-27 20:03 CEST

Script:

- `scripts/v3_wave94_accessible_state_rerank.py`

Inputs:

- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
- `results_v3/wave91_lipid_neighborhood_controller_scan/lipid_neighborhood_controller_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- IBD external anti-TNF GEO data via the Wave85/Wave86 parsers
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_counts_used.tsv`
- `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/gse198520_sample_metadata.tsv`
- `data/raw_v3/wave89_psoriasis_response/GSE85034_series_matrix.txt.gz`
- `data/raw_v3/wave89_psoriasis_response/GPL10558.annot.gz`
- Existing Geneformer output summaries under `results_v3/`

Outputs:

- `results_v3/wave94_accessible_state_rerank/candidate_pool.tsv`
- `results_v3/wave94_accessible_state_rerank/broad_candidate_context_rows.tsv`
- `results_v3/wave94_accessible_state_rerank/broad_candidate_summary.tsv`
- `results_v3/wave94_accessible_state_rerank/ms_candidate_rows.tsv`
- `results_v3/wave94_accessible_state_rerank/ibd_candidate_response_tests.tsv`
- `results_v3/wave94_accessible_state_rerank/ibd_platform_coverage.tsv`
- `results_v3/wave94_accessible_state_rerank/ra_candidate_response_tests.tsv`
- `results_v3/wave94_accessible_state_rerank/psoriasis_candidate_response_tests.tsv`
- `results_v3/wave94_accessible_state_rerank/psoriasis_platform_coverage.tsv`
- `results_v3/wave94_accessible_state_rerank/candidate_response_meta.tsv`
- `results_v3/wave94_accessible_state_rerank/candidate_genetics_rows.tsv`
- `results_v3/wave94_accessible_state_rerank/candidate_genetics_summary.tsv`
- `results_v3/wave94_accessible_state_rerank/candidate_foundation_summary.tsv`
- `results_v3/wave94_accessible_state_rerank/accessible_state_candidate_rank.tsv`
- `results_v3/wave94_accessible_state_rerank/summary.json`
- `results_v3/wave94_accessible_state_rerank/REPORT.md`

Result summary:

- Analysis call:
  `ACCESSIBLE_STATE_RERANK_COMPLETED`.
- This is branch-selection output, not a therapeutic claim.
- `46` candidates ranked after hard penalties for known closed routes and
  generic immune markers.
- Top parked routes:
  `SEL1L3`, `NRCAM`, `PLEK2`, `C15ORF48`, `CD200`, `CHI3L1`, `ROMO1`.
- Immediate interpretation:
  - `SEL1L3` has the best score but weak mechanistic interpretability.
  - `NRCAM` has strong response consistency but likely neural-safety problems.
  - `C15ORF48` has the best mechanistic immunometabolic story but weak direct
    druggability and no Geneformer token support in the existing tiny model.

## Wave95 Mechanistic Forcing Triage

Timestamp: 2026-05-27 20:22 CEST

Script:

- `scripts/v3_wave95_mechanistic_forcing_triage.py`

Inputs:

- `results_v3/wave94_accessible_state_rerank/accessible_state_candidate_rank.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/controller_route_rank.tsv`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
- `results_v3/wave79_targetability_shortlist_audit/targetability_integrated_decision.tsv`
- `results_v3/wave83_intervention_class_meta_rank/intervention_class_meta_rank.tsv`

Outputs:

- `results_v3/wave95_mechanistic_forcing_triage/mechanistic_forcing_candidate_rank.tsv`
- `results_v3/wave95_mechanistic_forcing_triage/mechanistic_forcing_gate_audit.tsv`
- `results_v3/wave95_mechanistic_forcing_triage/mechanistic_forcing_metric_long.tsv`
- `results_v3/wave95_mechanistic_forcing_triage/summary.json`
- `results_v3/wave95_mechanistic_forcing_triage/REPORT.md`

Result summary:

- Analysis call:
  `NO_MECHANISTIC_THERAPEUTIC_PROMOTION`.
- Candidates tested: `15`.
- Promoted candidates: `0`.
- Direct accessible/state candidates failed because expression/response support
  lacked residualized controller evidence and validated perturbation direction.
- `MFGE8`, `FXYD5`, `FPR2_ANXA1_BIASED_RESOLUTION`, and
  `CD300_RECEPTOR_SPECIFIC_TUNING` remain wet-lab-only kill-test routes.
- `C15ORF48` remains the strongest mechanistic clue, but not a direct
  intervention node.

## Wave96 C15ORF48 Controller Search

Timestamp: 2026-05-27 20:36 CEST

Script:

- `scripts/v3_wave96_c15orf48_controller_search.py`

Inputs:

- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
- `results_v3/wave79_targetability_shortlist_audit/targetability_integrated_decision.tsv`
- `results_v3/wave94_accessible_state_rerank/accessible_state_candidate_rank.tsv`
- `results_v3/wave95_mechanistic_forcing_triage/mechanistic_forcing_candidate_rank.tsv`
- Raw h5ad atlases under `data/raw_v3/cell_state/`

Outputs:

- `results_v3/wave96_c15orf48_controller_search/c15orf48_anchor_contexts.tsv`
- `results_v3/wave96_c15orf48_controller_search/contrast_state_rank_all.tsv`
- `results_v3/wave96_c15orf48_controller_search/pre_donor_controller_rank.tsv`
- `results_v3/wave96_c15orf48_controller_search/donor_level_c15_costate_correlations.tsv`
- `results_v3/wave96_c15orf48_controller_search/donor_level_c15_costate_summary.tsv`
- `results_v3/wave96_c15orf48_controller_search/c15orf48_controller_candidate_rank.tsv`
- `results_v3/wave96_c15orf48_controller_search/summary.json`
- `results_v3/wave96_c15orf48_controller_search/REPORT.md`

Result summary:

- Analysis call:
  `C15_CONTROLLER_SEARCH_COMPLETED`.
- Genes ranked: `25175`.
- Reopened controller candidates: `0`.
- Parked proximal intervention candidates: `13`.
- Wave96 is a branch map, not a therapeutic claim.

## Wave97 C15 Residual Co-State Falsification

Timestamp: 2026-05-27 20:41 CEST

Script:

- `scripts/v3_wave97_c15_residual_costate_falsification.py`

Inputs:

- `results_v3/wave96_c15orf48_controller_search/c15orf48_controller_candidate_rank.tsv`
- `results_v3/wave96_c15orf48_controller_search/c15orf48_anchor_contexts.tsv`
- Raw h5ad atlases under `data/raw_v3/cell_state/`

Outputs:

- `results_v3/wave97_c15_residual_costate_falsification/residual_costate_context_tests.tsv`
- `results_v3/wave97_c15_residual_costate_falsification/donor_covariate_scores.tsv`
- `results_v3/wave97_c15_residual_costate_falsification/residual_costate_candidate_summary.tsv`
- `results_v3/wave97_c15_residual_costate_falsification/summary.json`
- `results_v3/wave97_c15_residual_costate_falsification/REPORT.md`

Result summary:

- Analysis call:
  `C15_RESIDUAL_COSTATE_FALSIFICATION_COMPLETED`.
- Reopened after residualization: `CCL20`.
- `CCL20` was not promoted after sidecar integration because the CCL20/CCR6
  autoimmune/MS axis is prior-art saturated and likely a downstream inflammatory
  passenger.
- Novelty-open but insufficient routes after Wave97:
  `LITAF`, `PLEK2`, `CASP4`, and `PIK3R2`.

## Wave98 C15 Successor Perturbation-First Audit

Timestamp: 2026-05-27 20:50 CEST

Script:

- `scripts/v3_wave98_c15_successor_perturbation_first_audit.py`

Inputs:

- `results_v3/wave96_c15orf48_controller_search/c15orf48_controller_candidate_rank.tsv`
- `results_v3/wave97_c15_residual_costate_falsification/residual_costate_candidate_summary.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`

Outputs:

- `results_v3/wave98_c15_successor_perturbation_first_audit/c15_successor_perturbation_first_rank.tsv`
- `results_v3/wave98_c15_successor_perturbation_first_audit/c15_successor_residual_context_tests.tsv`
- `results_v3/wave98_c15_successor_perturbation_first_audit/summary.json`
- `results_v3/wave98_c15_successor_perturbation_first_audit/REPORT.md`

Result summary:

- Analysis call:
  `NO_REOPEN_C15_SUCCESSOR_TARGET`.
- `LITAF` remained only `PARK_PERTURBATION_ORDERING_REQUIRED`.
- `CASP4` was `NO_GO_CLOSE_PRIOR_OR_SAFETY_BLOCKED`.
- `PLEK2` and `PIK3R2` failed perturbation-first promotion.

## Wave99B Endogenous Inflammasome-Brake Audit

Timestamp: 2026-05-27 21:08 CEST

Script:

- `scripts/v3_wave99_endogenous_inflammasome_brake_audit.py`

Inputs:

- `results_v3/wave96_c15orf48_controller_search/c15orf48_anchor_contexts.tsv`
- `results_v3/wave96_c15orf48_controller_search/contrast_state_rank_all.tsv`
- `results_v3/wave96_c15orf48_controller_search/donor_level_c15_costate_summary.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
- `results_v3/wave98_c15_successor_perturbation_first_audit/c15_successor_perturbation_first_rank.tsv`
- Raw h5ad atlases under `data/raw_v3/cell_state/`

Outputs:

- `results_v3/wave99_endogenous_inflammasome_brake_audit/inflammasome_brake_candidate_rank.tsv`
- `results_v3/wave99_endogenous_inflammasome_brake_audit/inflammasome_brake_c15_residual_context_tests.tsv`
- `results_v3/wave99_endogenous_inflammasome_brake_audit/inflammasome_brake_c15_residual_summary.tsv`
- `results_v3/wave99_endogenous_inflammasome_brake_audit/inflammasome_brake_donor_covariate_scores.tsv`
- `results_v3/wave99_endogenous_inflammasome_brake_audit/summary.json`
- `results_v3/wave99_endogenous_inflammasome_brake_audit/REPORT.md`

Result summary:

- Analysis call:
  `NO_REOPEN_ENDOGENOUS_INFLAMMASOME_BRAKE_TARGET`.
- Candidates tested: `17`.
- Top candidate:
  `CARD16`, `NO_GO_COMPENSATORY_BRAKE_MARKER`.
- No endogenous brake cleared MS anchoring, residual C15 coupling,
  perturbation direction, genetics, modality, and prior-art/safety gates.

## Wave100 cAMP-Restoration Intervention-Class Audit

Timestamp: 2026-05-27 21:19 CEST

Script:

- `scripts/v3_wave100_camp_restoration_class_audit.py`

Inputs:

- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
- `results_v3/wave96_c15orf48_controller_search/contrast_state_rank_all.tsv`
- `results_v3/wave96_c15orf48_controller_search/donor_level_c15_costate_summary.tsv`
- `results_v3/wave28_target_first_rescue/target_first_rescue_matrix.tsv`
- `results_v3/wave50_gpr65_acid_sensing_gpcr_audit/summary.json`
- `results_v3/pde4_camp_l1000_audit_summary.json`

Outputs:

- `results_v3/wave100_camp_restoration_class_audit/camp_restoration_candidate_rank.tsv`
- `results_v3/wave100_camp_restoration_class_audit/camp_candidate_context_rows.tsv`
- `results_v3/wave100_camp_restoration_class_audit/summary.json`
- `results_v3/wave100_camp_restoration_class_audit/REPORT.md`

Candidate routes:

- `ADCY3` positive modulation.
- `GPR65` acidic-tissue cAMP agonism/PAM.
- `PDE4B` and `PDE4D` inhibition.
- `PTGER4`/EP4 contextual modulation.
- `ADORA2A` and `ADORA2B` adenosine receptor modulation.
- `HCAR2`, `HCAR3`, and `FFAR2` metabolite/GPCR routes.

Result summary:

- Branch call:
  `NO_REOPEN_CAMP_RESTORATION_CLASS`.
- Candidates tested: `10`.
- Promoted candidates: `0`.
- Call counts:
  `NO_GO_PRIOR_ART_OR_BRANCH_BLOCKED=8`,
  `NO_GO_NO_SELECTIVE_ACTIONABLE_MODALITY=2`.
- `ADCY3` ranked highest but lacked actionable modality, clear direction,
  cross-disease cell-state support, MS genetic anchor, and perturbation/model
  support.
- `PDE4B` remained the best wet-lab comparator route but not a V3 target:
  raw positive disease count `4`, retained positive disease count `3`,
  MS white-matter delta `-0.4295`, p `0.2821`, no target-resolved genetics,
  no core PDE4/cAMP L1000 reversal hits, and prior-art/safety blockers.
- Class-level PDE4/cAMP perturbation audit carried forward:
  `85` LINCS metadata rows, `34` unique perturbagen IDs, `2` broad term
  opposite-hit rows, and `0` core compound opposite-hit rows.

## Wave101 Accessible-Survivor Forcing Triage

Timestamp: 2026-05-27 21:29 CEST

Script:

- `scripts/v3_wave101_accessible_survivor_forcing_triage.py`

Inputs:

- `results_v3/wave95_mechanistic_forcing_triage/mechanistic_forcing_candidate_rank.tsv`
- `results_v3/wave94_accessible_state_rerank/accessible_state_candidate_rank.tsv`
- `results_v3/wave79_targetability_shortlist_audit/targetability_integrated_decision.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
- `results_v3/wave91_lipid_lysosomal_module_intervention_rank/lipid_lysosomal_intervention_rank.tsv`
- `results_v3/wave47_late_stage_survivor_map/late_stage_survivor_map.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`

Outputs:

- `results_v3/wave101_accessible_survivor_forcing_triage/accessible_survivor_forcing_rank.tsv`
- `results_v3/wave101_accessible_survivor_forcing_triage/summary.json`
- `results_v3/wave101_accessible_survivor_forcing_triage/REPORT.md`

Candidate panel:

- `SEL1L3`, `FXYD5`, `CD82`, `LAPTM5`, `NRCAM`, `CD200`, `MFGE8`,
  `CHI3L1`, `GPNMB`, `BTN2A2`, `ADM`, `APOC1`.

Result summary:

- Branch call:
  `NO_PROMOTABLE_ACCESSIBLE_SURVIVOR_YET`.
- Candidates tested:
  `12`.
- Top parked candidates for a target-specific forcing branch:
  `SEL1L3`, `FXYD5`, `APOC1`.
- No candidate had target-specific perturbation support or target-resolved
  genetic anchoring.
- `CD82`, `CD200`, `CHI3L1`, and `MFGE8` were blocked by prior-art/crowding
  or route-specific safety concerns.
- `NRCAM` retained high expression/response signal but failed on neural
  adhesion safety.

## Wave102 Accessible-Survivor Residual Compartment Test

Timestamp: 2026-05-27 21:34 CEST

Script:

- `scripts/v3_wave102_accessible_survivor_residual_compartment_test.py`

Inputs:

- `results_v3/wave101_accessible_survivor_forcing_triage/accessible_survivor_forcing_rank.tsv`
- Direct h5ad autoimmune atlases under `data/raw_v3/cell_state/`
- Donor module scores from:
  `results_v3/osmr_complement_axes/osmr_complement_donor_module_scores.tsv`
  and `results_v3/direct_h5ad_cell_state/direct_h5ad_donor_module_scores.tsv`

Outputs:

- `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_donor_scores.tsv`
- `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_gene_presence.tsv`
- `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_raw_tests.tsv`
- `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_residual_tests.tsv`
- `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_residual_summary.tsv`
- `results_v3/wave102_accessible_survivor_residual_compartment_test/summary.json`
- `results_v3/wave102_accessible_survivor_residual_compartment_test/REPORT.md`

Result summary:

- Branch call:
  `NO_ACCESSIBLE_SURVIVOR_RESIDUAL_REOPEN`.
- Completed analyses:
  `18`.
- Candidates tested:
  `12`.
- `strict_core_covariate_surviving_disease_count=0` for every candidate.
- `core_all_multivariable_surviving_disease_count=0` for every candidate.
- `FXYD5` had the best raw focus-candidate replication:
  raw-positive disease count `3`, retained-positive disease count `2`, but no
  strict or core-all residual survival and one raw-negative analysis.
- `SEL1L3` had only one raw-positive disease and no non-IBD retained disease.
- `APOC1` had no direct h5ad replication in this test.

## Wave103 Fc/FcRn/Efferocytosis Route Audit

Timestamp: 2026-05-27 21:49 CEST

Script:

- `scripts/v3_wave103_fc_receptor_efferocytosis_route_audit.py`

Inputs:

- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`

Outputs:

- `results_v3/wave103_fc_receptor_efferocytosis_route_audit/fc_efferocytosis_route_rank.tsv`
- `results_v3/wave103_fc_receptor_efferocytosis_route_audit/summary.json`
- `results_v3/wave103_fc_receptor_efferocytosis_route_audit/REPORT.md`

Result summary:

- Branch call:
  `NO_REOPEN_FC_EFFEROCYTOSIS_ROUTE`.
- Candidates tested:
  `15`.
- `FCGRT` had CRISPR efferocytosis support and an existing drug class, but no
  MS/module/genetic anchor in local evidence.
- `DAB2` and `CD9` had MS expression and efferocytosis-screen support, but no
  cross-disease expression/genetics and no clean modality or direction.
- Activating Fc receptors, Fc adaptors, and TAM receptors remained blocked by
  direction, safety, prior art, or weak local anchoring.

## Wave104 Accessible-Survivor Niche-Controller Test

Timestamp: 2026-05-27 21:55 CEST

Script:

- `scripts/v3_wave104_accessible_survivor_niche_controller_test.py`

Inputs:

- `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_donor_scores.tsv`
- `results_v3/direct_h5ad_cell_state/direct_h5ad_donor_module_scores.tsv`
- `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_residual_summary.tsv`

Outputs:

- `results_v3/wave104_accessible_survivor_niche_controller_test/matched_niche_pairs.tsv`
- `results_v3/wave104_accessible_survivor_niche_controller_test/niche_controller_tests.tsv`
- `results_v3/wave104_accessible_survivor_niche_controller_test/niche_controller_summary.tsv`
- `results_v3/wave104_accessible_survivor_niche_controller_test/summary.json`
- `results_v3/wave104_accessible_survivor_niche_controller_test/REPORT.md`

Result summary:

- Branch call:
  `REOPEN_ACCESSIBLE_SURVIVOR_NICHE_CONTROLLER`.
- Matched donor pairs:
  `520`.
- Tests:
  `120`.
- `CD82` was the only reopened candidate:
  adjusted positive disease count `3`, adjusted negative disease count `0`.
- `SEL1L3`, `FXYD5`, `LAPTM5`, and `APOC1` were direction-conflicted.
- The `CD82` reopener is explicitly provisional because small IBD paired tests
  required adaptive covariate trimming.

## Wave105 CD82 Niche Robustness Audit

Timestamp: 2026-05-27 23:45 CEST

Script:

- `scripts/v3_wave105_cd82_niche_robustness_audit.py`

Inputs:

- `results_v3/wave104_accessible_survivor_niche_controller_test/matched_niche_pairs.tsv`
- `results_v3/wave104_accessible_survivor_niche_controller_test/niche_controller_tests.tsv`
- Sidecar context:
  `subagents_v3/wave105_cd82_prior_art_sidecar.md`

Outputs:

- `results_v3/wave105_cd82_niche_robustness_audit/cd82_model_grid_tests.tsv`
- `results_v3/wave105_cd82_niche_robustness_audit/cd82_robustness_summary.tsv`
- `results_v3/wave105_cd82_niche_robustness_audit/cd82_robust_tests.tsv`
- `results_v3/wave105_cd82_niche_robustness_audit/summary.json`
- `results_v3/wave105_cd82_niche_robustness_audit/REPORT.md`

Result summary:

- Branch call:
  `REOPEN_CD82_ROBUST_NICHE_SIGNAL`.
- Model-grid rows:
  `168`.
- Test contexts:
  `24`.
- Robust positive contexts:
  `4`.
- Robust positive diseases:
  `2` (`Crohn disease`, `Sjogren syndrome`).
- Robust negative contexts:
  `0`.
- Guardrail:
  the branch is mechanism/biomarker only; direct CD82 therapeutic promotion is
  blocked by prior art and tetraspanin pleiotropy.

## Wave106 CD82 Specificity / Confounder Audit

Timestamp: 2026-05-27 23:55 CEST

Script:

- `scripts/v3_wave106_cd82_specificity_confounder_audit.py`

Inputs:

- `results_v3/wave104_accessible_survivor_niche_controller_test/matched_niche_pairs.tsv`
- `results_v3/wave105_cd82_niche_robustness_audit/cd82_robust_tests.tsv`
- Sidecar critique:
  `subagents_v3/wave105_cd82_hostile_methods_review.md`

Outputs:

- `results_v3/wave106_cd82_specificity_confounder_audit/cd82_specificity_tests.tsv`
- `results_v3/wave106_cd82_specificity_confounder_audit/cd82_specificity_summary.tsv`
- `results_v3/wave106_cd82_specificity_confounder_audit/summary.json`
- `results_v3/wave106_cd82_specificity_confounder_audit/REPORT.md`

Result summary:

- Branch call:
  `CD82_SIGNAL_PARTLY_GENERIC_OR_CONTEXT_LIMITED`.
- Contexts:
  `8`.
- Tests:
  `168`.
- Robust-specific contexts:
  `1`.
- Robust-specific diseases:
  `1`.
- Robust-generic contexts:
  `1`.
- Interpretation:
  CD82 does not currently survive as a specific cross-disease lipid-lysosomal
  intervention route; it remains a provisional niche biomarker/readout.

## Wave107 CD82 Multiplicity / Disease-Collapse Audit

Timestamp: 2026-05-28 00:02 CEST

Script:

- `scripts/v3_wave107_cd82_multiplicity_disease_collapse_audit.py`

Inputs:

- `results_v3/wave105_cd82_niche_robustness_audit/cd82_model_grid_tests.tsv`
- `results_v3/wave105_cd82_niche_robustness_audit/cd82_robustness_summary.tsv`
- `results_v3/wave106_cd82_specificity_confounder_audit/cd82_specificity_summary.tsv`

Outputs:

- `results_v3/wave107_cd82_multiplicity_disease_collapse_audit/cd82_context_multiplicity.tsv`
- `results_v3/wave107_cd82_multiplicity_disease_collapse_audit/cd82_disease_collapsed_evidence.tsv`
- `results_v3/wave107_cd82_multiplicity_disease_collapse_audit/summary.json`
- `results_v3/wave107_cd82_multiplicity_disease_collapse_audit/REPORT.md`

Result summary:

- Branch call:
  `CD82_PROVISIONAL_NICHE_BIOMARKER_SIGNAL_NOT_REOPENED`.
- Contexts:
  `24`.
- Disease/source-target units:
  `8`.
- Strict disease pass count:
  `0`.
- Provisional disease pass count:
  `1`.
- Interpretation:
  CD82 is closed as a therapeutic-discovery branch and retained only as a
  provisional niche biomarker/readout.

## Wave108 MFGE8-Like Debris-Opsonin Safety-Window Model

Timestamp: 2026-05-28 00:18 CEST

Script:

- `scripts/v3_wave108_mfge8_debris_opsonin_safety_window_model.py`

Inputs:

- `results_v3/wave54_mfge8_debris_opsonin_audit/decision_matrix.tsv`

Outputs:

- `results_v3/wave108_mfge8_debris_opsonin_safety_window_model/mfge8_safety_window_grid.tsv`
- `results_v3/wave108_mfge8_debris_opsonin_safety_window_model/mfge8_selectivity_summary.tsv`
- `results_v3/wave108_mfge8_debris_opsonin_safety_window_model/summary.json`
- `results_v3/wave108_mfge8_debris_opsonin_safety_window_model/REPORT.md`

Result summary:

- Branch call:
  `MFGE8_LOCAL_OPSONIN_NO_THEORETICAL_SAFETY_WINDOW`.
- Grid points:
  `13200`.
- Strict safe grid points:
  `0`.
- Scope:
  simulation-only, not real efficacy.

## Wave109 MFGE8 Threshold Sensitivity Audit

Timestamp: 2026-05-28 00:18 CEST

Script:

- `scripts/v3_wave109_mfge8_threshold_sensitivity_audit.py`

Inputs:

- `results_v3/wave108_mfge8_debris_opsonin_safety_window_model/mfge8_safety_window_grid.tsv`

Outputs:

- `results_v3/wave109_mfge8_threshold_sensitivity_audit/mfge8_threshold_sensitivity.tsv`
- `results_v3/wave109_mfge8_threshold_sensitivity_audit/summary.json`
- `results_v3/wave109_mfge8_threshold_sensitivity_audit/REPORT.md`

Result summary:

- Branch call:
  `MFGE8_MODEST_1_5X_WINDOW_ONLY`.
- Strict 2x / p90 viable loss <= 5% / p90 cytokine <= 1.20 points:
  `0`.
- Modest 1.5x / p90 viable loss <= 5% / p90 cytokine <= 1.20 points:
  `19`.
- Minimum debris-over-viable selectivity for the modest window:
  approximately `316x`.
- Interpretation:
  quantitative ex vivo engineering constraint, not target promotion.

## Wave110 Post-Closure Intervention Route Map

Timestamp: 2026-05-28 00:35 CEST

Script:

- `scripts/v3_wave110_post_closure_intervention_route_map.py`

Inputs:

- `results_v3/wave83_intervention_class_meta_rank/intervention_class_meta_rank.tsv`
- `results_v3/wave91_lipid_lysosomal_module_intervention_rank/lipid_lysosomal_intervention_rank.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`

Outputs:

- `results_v3/wave110_post_closure_intervention_route_map/post_closure_route_map.tsv`
- `results_v3/wave110_post_closure_intervention_route_map/summary.json`
- `results_v3/wave110_post_closure_intervention_route_map/REPORT.md`

Result summary:

- Branch call:
  `NO_PROMOTABLE_ROUTE_SELECT_NEXT_FORCING_TEST`.
- Routes ranked:
  `138`.
- Top local forcing route:
  `PSAP` by local score, but the independent sidecar selected `GPR183/EBI2`
  as the least-bad intervention-first route because it has a concrete GPCR
  spatial-niche forcing test.

## Wave111 GPR183 Spatial-Proxy Forcing Test

Timestamp: 2026-05-28 00:35 CEST

Script:

- `scripts/v3_wave111_gpr183_spatial_proxy_forcing_test.py`

Inputs:

- `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_donor_scores.tsv`
- `results_v3/direct_h5ad_cell_state/direct_h5ad_donor_module_scores.tsv`

Outputs:

- `results_v3/wave111_gpr183_spatial_proxy_forcing_test/gpr183_gene_module_donor_scores.tsv`
- `results_v3/wave111_gpr183_spatial_proxy_forcing_test/gpr183_spatial_proxy_pairs.tsv`
- `results_v3/wave111_gpr183_spatial_proxy_forcing_test/gpr183_spatial_proxy_tests.tsv`
- `results_v3/wave111_gpr183_spatial_proxy_forcing_test/gpr183_spatial_proxy_summary.tsv`
- `results_v3/wave111_gpr183_spatial_proxy_forcing_test/summary.json`
- `results_v3/wave111_gpr183_spatial_proxy_forcing_test/REPORT.md`

Result summary:

- Branch call:
  `NO_REOPEN_GPR183_SPATIAL_PROXY`.
- Pairs:
  `0`.
- Tests:
  `0`.
- Reason:
  donor-level gene scores for `GPR183` and ligand-axis genes were not present
  in the precomputed accessible-survivor donor-score table.

## Wave112 GPR183 Compartment-Contrast Fallback

Timestamp: 2026-05-28 00:45 CEST

Script:

- `scripts/v3_wave112_gpr183_compartment_contrast_fallback.py`

Inputs:

- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/ibd_external_antitnf_gene_response_meta.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/ra_gse198520_baseline_gene_response_meta.tsv`
- `results_v3/wave93_gpr183_oxysterol_forcing_test/psoriasis_gse85034_ada_gene_response_meta.tsv`

Outputs:

- `results_v3/wave112_gpr183_compartment_contrast_fallback/gpr183_broad_target_gene_rows.tsv`
- `results_v3/wave112_gpr183_compartment_contrast_fallback/gpr183_compartment_contrast_summary.tsv`
- `results_v3/wave112_gpr183_compartment_contrast_fallback/gpr183_response_support_rows.tsv`
- `results_v3/wave112_gpr183_compartment_contrast_fallback/summary.json`
- `results_v3/wave112_gpr183_compartment_contrast_fallback/REPORT.md`

Result summary:

- Branch call:
  `NO_REOPEN_GPR183_COMPARTMENT_FALLBACK`.
- Coherent compartment disease count:
  `0`.
- Response-support systems for `GPR183` at p < 0.10:
  `2`.
- Interpretation:
  receptor/ligand compartment coherence fails despite treatment-response
  movement, so GPR183 is closed locally.

## Wave113 PSAP Recurrence / Specificity Audit

Timestamp: 2026-05-28 00:55 CEST

Script:

- `scripts/v3_wave113_psap_recurrence_specificity_audit.py`

Inputs:

- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_ms_rows.tsv`
- `results_v3/wave57_intervention_first_geneformer_screen/wave57_geneformer_gene_summary.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`

Outputs:

- `results_v3/wave113_psap_recurrence_specificity_audit/psap_broad_contexts.tsv`
- `results_v3/wave113_psap_recurrence_specificity_audit/psap_disease_summary.tsv`
- `results_v3/wave113_psap_recurrence_specificity_audit/psap_evidence_rows.tsv`
- `results_v3/wave113_psap_recurrence_specificity_audit/summary.json`
- `results_v3/wave113_psap_recurrence_specificity_audit/REPORT.md`

Result summary:

- Branch call:
  `NO_REOPEN_PSAP_WEAK_SINGLE_CONTEXT_MARKER`.
- Positive disease count at p < 0.10:
  `1`.
- Myeloid positive disease count at p < 0.10:
  `0`.
- Negative disease count at p < 0.10:
  `2`.
- MS nominal positive:
  `true`.
- Geneformer strong support:
  `false`.
- CRISPR support:
  `false`.

## Wave114 P2RX7 Target-Level Closure Audit

Timestamp: 2026-05-28 06:41 CEST

Script:

- `scripts/v3_wave114_p2rx7_target_level_closure_audit.py`

Inputs:

- `results_v3/wave73_p2rx7_stratification_test/p2rx7_stratification_decision.tsv`
- `results_v3/wave73_p2rx7_stratification_test/broad_h5ad_module_summary.tsv`
- `results_v3/wave73_p2rx7_stratification_test/ms_gse111972_module_tests.tsv`
- `results_v3/wave73_p2rx7_stratification_test/ra_gse198520_module_tests.tsv`
- `results_v3/wave73_p2rx7_stratification_test/gse282122_module_response_tests.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave95_mechanistic_forcing_triage/mechanistic_forcing_metric_long.tsv`

Outputs:

- `results_v3/wave114_p2rx7_target_level_closure_audit/p2rx7_closure_evidence.tsv`
- `results_v3/wave114_p2rx7_target_level_closure_audit/summary.json`
- `results_v3/wave114_p2rx7_target_level_closure_audit/REPORT.md`

Result summary:

- Branch call:
  `NO_REOPEN_P2RX7_TARGET_LEVEL_STRATIFICATION`.
- Specificity-pass context count:
  `0`.
- MS module support:
  `false`.
- RA response discrimination:
  `false`.
- IBD response discrimination:
  `false`.
- CRISPR/efferocytosis support:
  `false`.

## Wave115 SPNS1 Controller Falsification Audit

Timestamp: 2026-05-28 06:50 CEST

Script:

- `scripts/v3_wave115_spns1_controller_falsification_audit.py`

Inputs:

- `results_v3/wave79_targetability_shortlist_residual_audit/direct_shortlist_donor_scores.tsv`
- `results_v3/wave79_targetability_shortlist_residual_audit/targetability_shortlist_candidate_matrix.tsv`
- `results_v3/wave79_targetability_shortlist_residual_audit/ms_white_matter_shortlist_rows.tsv`
- `results_v3/wave79_targetability_shortlist_residual_audit/ra_antitnf_shortlist_response_rows.tsv`
- `results_v3/wave79_targetability_shortlist_residual_audit/ibd_antitnf_shortlist_response_rows.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave94_accessible_state_rerank/accessible_state_candidate_rank.tsv`

Outputs:

- `results_v3/wave115_spns1_controller_falsification_audit/spns1_case_only_partial_controller_tests.tsv`
- `results_v3/wave115_spns1_controller_falsification_audit/spns1_controller_disease_summary.tsv`
- `results_v3/wave115_spns1_controller_falsification_audit/spns1_external_gate_evidence.tsv`
- `results_v3/wave115_spns1_controller_falsification_audit/summary.json`
- `results_v3/wave115_spns1_controller_falsification_audit/REPORT.md`

Result summary:

- Branch call:
  `NO_REOPEN_SPNS1_CONTROLLER_ROUTE`.
- Controller-pass diseases:
  `0`.
- Myeloid-pass contexts:
  `0`.
- MS anchor:
  `false`.
- Response support:
  `false`.
- CRISPR/efferocytosis support:
  `false`.
- Target-resolution support:
  `false`.
- Modality ready:
  `false`.

## Wave116 Closure-Aware Route Rerank

Timestamp: 2026-05-28 07:02 CEST

Script:

- `scripts/v3_wave116_closure_aware_route_rerank.py`

Inputs:

- `results_v3/wave110_post_closure_intervention_route_map/post_closure_route_map.tsv`
- `results_v3/wave95_mechanistic_forcing_triage/mechanistic_forcing_candidate_rank.tsv`
- `results_v3/wave83_intervention_class_meta_rank/intervention_class_meta_rank.tsv`
- `results_v3/wave91_lipid_lysosomal_module_intervention_rank/lipid_lysosomal_intervention_rank.tsv`

Outputs:

- `results_v3/wave116_closure_aware_route_rerank/closure_aware_route_universe.tsv`
- `results_v3/wave116_closure_aware_route_rerank/summary.json`
- `results_v3/wave116_closure_aware_route_rerank/REPORT.md`

Result summary:

- Branch call:
  `ROUTE_AVAILABLE_FOR_FORCING_TEST`.
- Routes:
  `257`.
- Open routes:
  `223`.
- Actionable non-`NO_GO` routes:
  `132`.
- Selected candidate:
  `PARK7`.

## Wave117 PARK7/DJ-1 Stress-Route Forcing Test

Timestamp: 2026-05-28 07:06 CEST

Script:

- `scripts/v3_wave117_park7_stress_route_forcing_test.py`

Inputs:

- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_ms_rows.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_broad_summary.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave57_rows.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_ibd_response_summary.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave62_rows.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave37_rows.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/broad_residual_gate/broad_residual_residual_tests.tsv`

Outputs:

- `results_v3/wave117_park7_stress_route_forcing_test/park7_broad_contexts.tsv`
- `results_v3/wave117_park7_stress_route_forcing_test/park7_broad_disease_summary.tsv`
- `results_v3/wave117_park7_stress_route_forcing_test/park7_generic_covariate_residual_rows.tsv`
- `results_v3/wave117_park7_stress_route_forcing_test/park7_generic_covariate_residual_summary.tsv`
- `results_v3/wave117_park7_stress_route_forcing_test/park7_gate_evidence.tsv`
- `results_v3/wave117_park7_stress_route_forcing_test/summary.json`
- `results_v3/wave117_park7_stress_route_forcing_test/REPORT.md`

Result summary:

- Branch call:
  `NO_REOPEN_PARK7_GENERIC_STRESS_ROUTE`.
- Broad myeloid-positive diseases:
  `2`.
- Generic-covariate residual diseases:
  `0`.
- MS anchor:
  `false`.
- Foundation strong support:
  `false`.
- Response support:
  `false`.
- Target-resolution support:
  `false`.
- CRISPR/efferocytosis support:
  `false`.

## Wave118 DAB2/CD9 Efferocytosis Directionality Audit

Timestamp: 2026-05-28 07:16 CEST

Script:

- `scripts/v3_wave118_dab2_cd9_efferocytosis_directionality_audit.py`

Inputs:

- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_ms_rows.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_broad_summary.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_ibd_response_summary.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave71_rows.tsv`
- `results_v3/wave110_post_closure_intervention_route_map/post_closure_route_map.tsv`

Outputs:

- `results_v3/wave118_dab2_cd9_efferocytosis_directionality_audit/dab2_cd9_directionality_decisions.tsv`
- `results_v3/wave118_dab2_cd9_efferocytosis_directionality_audit/dab2_cd9_evidence_rows.tsv`
- `results_v3/wave118_dab2_cd9_efferocytosis_directionality_audit/summary.json`
- `results_v3/wave118_dab2_cd9_efferocytosis_directionality_audit/REPORT.md`

Result summary:

- Branch call:
  `NO_REOPEN_DAB2_CD9_EFFEROCYTOSIS_ROUTE`.
- `DAB2` and `CD9` both fail FDR-supported MS, positive cross-disease
  direction, FDR-supported CRISPR, response, target-genetics, and modality
  gates.

## Wave119 Remaining Wave110 Survivor Prefilter

Timestamp: 2026-05-28 07:36 CEST

Script:

- `scripts/v3_wave119_wave110_remaining_survivor_prefilter.py`

Inputs:

- `results_v3/wave110_post_closure_intervention_route_map/post_closure_route_map.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_ms_rows.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_broad_summary.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_ibd_response_summary.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave62_rows.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave71_rows.tsv`

Outputs:

- `results_v3/wave119_wave110_remaining_survivor_prefilter/remaining_wave110_prefilter_decisions.tsv`
- `results_v3/wave119_wave110_remaining_survivor_prefilter/remaining_wave110_prefilter_evidence.tsv`
- `results_v3/wave119_wave110_remaining_survivor_prefilter/summary.json`
- `results_v3/wave119_wave110_remaining_survivor_prefilter/REPORT.md`

Result summary:

- Branch call:
  `NO_REMAINING_WAVE110_SURVIVOR_AFTER_PREFILTER`.
- Candidates tested:
  `14`.
- Candidates parked:
  `0`.
## Wave120 - EPHX2/sEH Target-PD Coherence Closure

- Script: `scripts/v3_wave120_ephx2_target_pd_coherence_closure.py`
- Output directory: `results_v3/wave120_ephx2_target_pd_coherence_closure/`
- Inputs:
  - `results_v3/wave74_ephx2_direct_ratio_audit/ephx2_direct_ratio_decision.tsv`
  - `results_v3/wave74_ephx2_oxylipin_specificity/final_decision.tsv`
  - `results_v3/wave74_ephx2_oxylipin_specificity/ephx2_gene_evidence.tsv`
  - `results_v3/wave74_ephx2_oxylipin_specificity/module_specificity_margins.tsv`
  - `results_v3/wave74_ephx2_oxylipin_specificity/metabolite_cross_disease_stats.tsv`
  - `subagents_v3/wave74c_prior_art_druggability_scout.md`
- Branch call: `NO_REOPEN_EPHX2_TARGET_PD_COHERENCE`
- Gate result: 0/6 strict gates passed.

## Wave121 - Final Wet-Lab-Only Route Closure

- Script: `scripts/v3_wave121_final_wetlab_only_route_closure.py`
- Output directory: `results_v3/wave121_final_wetlab_only_route_closure/`
- Inputs:
  - `results_v3/wave95_mechanistic_forcing_triage/mechanistic_forcing_candidate_rank.tsv`
  - `subagents_v3/wave95_sidecar_returns_integrated.md`
  - `subagents_v3/wave94_remaining_route_hostile_rank.md`
  - `results_v3/wave32c_resolution_prior_art_audit/resolution_prior_art_audit.tsv`
  - `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
  - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- Branch call: `NO_OPEN_ROUTE_AFTER_WETLAB_ONLY_AUDIT`
- Route decisions:
  - `FPR2_ANXA1_BIASED_RESOLUTION`: `NO_REOPEN_WETLAB_ONLY_ROUTE`, 2/10 gates.
  - `CD300_RECEPTOR_SPECIFIC_TUNING`: `NO_REOPEN_WETLAB_ONLY_ROUTE`, 2/10 gates.

## Wave122 - Fresh Breadth-First Target Scan

- Script: `scripts/v3_wave122_fresh_breadth_target_scan.py`
- Output directory: `results_v3/wave122_fresh_breadth_target_scan/`
- Inputs:
  - `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
  - `results_v3/gse111972_full_ms_wm_signature.tsv`
  - `results_v3/wave87_cross_system_antitnf_resistance_gene_check/cross_system_antitnf_gene_integration.tsv`
  - `results_v3/wave91_lipid_lysosomal_module_intervention_rank/lipid_lysosomal_intervention_rank.tsv`
  - `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
  - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
  - `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave62_rows.tsv`
  - `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_druggability_sweep.tsv`
- Branch call: `NO_FRESH_ROUTE_FROM_LOCAL_SCAN`
- Genes scanned: 32,096
- Top gene: `NCF2`, blocked by NOX2 host-defense/CGD directionality risk and
  target-resolution no-go.

## Wave123 - Boyle Sidecar Candidate Kill Audit

- Script: `scripts/v3_wave123_sidecar_candidate_kill_audit.py`
- Output directory: `results_v3/wave123_sidecar_candidate_kill_audit/`
- Inputs:
  - `results_v3/wave122_fresh_breadth_target_scan/fresh_breadth_target_rank.tsv`
  - `results_v3/wave95_mechanistic_forcing_triage/mechanistic_forcing_candidate_rank.tsv`
  - `results_v3/wave91_lipid_lysosomal_module_intervention_rank/lipid_lysosomal_intervention_rank.tsv`
  - `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
  - `results_v3/wave87_cross_system_antitnf_resistance_gene_check/cross_system_antitnf_gene_integration.tsv`
  - `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave62_rows.tsv`
- Branch call: `NO_REOPEN_ANY_SIDECAR_CANDIDATE`
- Candidates tested: `NRCAM`, `CD200`, `MERTK`, `CHI3L1`, `LIPA`

## Wave124 - NCF2/NOX2 Strict Closure Audit

- Script: `scripts/v3_wave124_ncf2_nox2_strict_closure_audit.py`
- Output directory: `results_v3/wave124_ncf2_nox2_strict_closure_audit/`
- Inputs:
  - `results_v3/wave122_fresh_breadth_target_scan/fresh_breadth_target_rank.tsv`
  - `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
  - `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave71_rows.tsv`
  - `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave62_rows.tsv`
  - `results_v3/wave70_fc_ros_resolution_matrix/fc_ros_resolution_candidate_matrix.tsv`
  - `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
  - `results_v3/wave96_c15orf48_controller_search/c15orf48_controller_candidate_rank.tsv`
- Branch call: `NO_REOPEN_NCF2_NOX2_ROUTE`
- Gate result: 1/11 passed.

## Wave125 - Mechanism-Class Failure Map

- Script: `scripts/v3_wave125_mechanism_class_failure_map.py`
- Output directory: `results_v3/wave125_mechanism_class_failure_map/`
- Input:
  - `results_v3/wave122_fresh_breadth_target_scan/fresh_breadth_target_rank.tsv`
- Branch call: `MECHANISM_FAILURE_MAP_COMPLETE`
- Top 300 Wave122 candidates mapped.
- Dominant failure modes:
  - response absent: 297/300
  - no modality: 280/300
  - no causal channel: 274/300

## Wave126 - L1000 Upstream-Regulator Reopener

- Script: `scripts/v3_wave126_l1000_upstream_regulator_reopener.py`
- Output directory: `results_v3/wave126_l1000_upstream_regulator_reopener/`
- Inputs:
  - `results_v3/wave24_l1000_recurrent_reversal/recurrent_l1000_compound_triage.tsv`
  - `results_v3/wave15_perturbation_drug_response/l1000fwd_selectivity_compound_rank.tsv`
  - `results_v3/l1000fwd_reversal_hits.tsv`
  - `results_v3/wave125_mechanism_class_failure_map/pivot_recommendations.tsv`
- Branch call: `NO_L1000_UPSTREAM_REOPENER`
- Compounds tested: 123
- Reopened compounds: 0

## Wave127 - External L1000 Unknown Lookup

- Artifact: `literature_v3/wave127_external_l1000_unknown_lookup.md`
- Search queries:
  - `"BFOWTYGBWYCXKR"`
  - `"GNLIZSFOCYRQDY" "BRD-K35024477"`
  - `"BRD-K05197617"`
  - `"BRD-K35024477"`
- Branch decision: no recurrent unknown L1000 hit reopened.

## Wave128 - Genetics-First Reopener

- Script: `scripts/v3_wave128_genetics_first_reopener.py`
- Output directory: `results_v3/wave128_genetics_first_reopener/`
- Inputs:
  - `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
  - `results_v3/wave55_external_genetics_druggability_sweep/decision_matrix.tsv`
  - `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
  - `results_v3/wave122_fresh_breadth_target_scan/fresh_breadth_target_rank.tsv`
- Branch call: `NO_GENETICS_FIRST_REOPENER`
- Candidates tested: 195
- Reopened candidates: 0

## Wave129 - Response/Stratification Salvage

- Script: `scripts/v3_wave129_response_stratification_salvage.py`
- Output directory: `results_v3/wave129_response_stratification_salvage/`
- Inputs:
  - `results_v3/wave87_cross_system_antitnf_resistance_gene_check/cross_system_antitnf_gene_integration.tsv`
  - `results_v3/wave75_response_state_stratification/cross_dataset_response_convergence.tsv`
  - `results_v3/wave76_adjusted_response_specificity/adjusted_cross_dataset_convergence.tsv`
  - `results_v3/wave84_response_prediction_audit/response_prediction_decision.tsv`
  - `results_v3/wave122_fresh_breadth_target_scan/fresh_breadth_target_rank.tsv`
- Branch call: `BIOMARKER_ONLY_SIGNAL_EXISTS`
- Biomarker-only candidates: `IL1B`, `LAMP3`
- Target nominations allowed: 0

## Wave130 - MS Treatment-Response Audit

- Script: `scripts/v3_wave130_ms_treatment_response_audit.py`
- Output directory: `results_v3/wave130_ms_treatment_response_audit/`
- Inputs:
  - `data/raw_v3/wave96_ms_treatment/GSE235357_normalized_annotated.csv.gz`
  - `data/raw_v3/wave96_ms_treatment/GSE235357_series_matrix.txt.gz`
  - `data/raw_v3/wave96_ms_treatment/GSE250453_fingo_RNAseq_all.tsv.gz`
  - `data/raw_v3/wave96_ms_treatment/GSE250453_series_matrix.txt.gz`
  - `results_v3/wave129_response_stratification_salvage/response_stratification_salvage_decisions.tsv`
- Outputs:
  - `results_v3/wave130_ms_treatment_response_audit/ms_treatment_response_feature_tests.tsv`
  - `results_v3/wave130_ms_treatment_response_audit/ms_treatment_response_cross_dataset_stability.tsv`
  - `results_v3/wave130_ms_treatment_response_audit/missing_features.tsv`
  - `results_v3/wave130_ms_treatment_response_audit/summary.json`
  - `results_v3/wave130_ms_treatment_response_audit/REPORT.md`
- Accessions: GSE235357, GSE250453
- Branch call: `GENERIC_IFN_APC_SIGNAL_ONLY_NO_LIPID_LYSOSOMAL_RESCUE`

## Wave131 - Class-Route Forcing Audit

- Script: `scripts/v3_wave131_class_route_forcing_audit.py`
- Output directory: `results_v3/wave131_class_route_forcing_audit/`
- Inputs:
  - `results_v3/wave83_intervention_class_meta_rank/intervention_class_meta_rank.tsv`
  - `results_v3/wave83_intervention_class_meta_rank/intervention_class_candidate_universe.tsv`
  - `results_v3/wave130_ms_treatment_response_audit/ms_treatment_response_cross_dataset_stability.tsv`
  - `results_v3/wave126_l1000_upstream_regulator_reopener/l1000_upstream_reopener_decisions.tsv`
  - `results_v3/wave128_genetics_first_reopener/genetics_first_reopener_decisions.tsv`
- Outputs:
  - `results_v3/wave131_class_route_forcing_audit/class_route_forcing_decisions.tsv`
  - `results_v3/wave131_class_route_forcing_audit/class_route_forcing_evidence.tsv`
  - `results_v3/wave131_class_route_forcing_audit/summary.json`
  - `results_v3/wave131_class_route_forcing_audit/REPORT.md`
- Branch call: `NO_CLASS_ROUTE_REOPENED_AFTER_WAVE130`

## Wave132 - GPR183 Post-Wave130 Closure

- Script: `scripts/v3_wave132_gpr183_post_wave130_closure.py`
- Output directory: `results_v3/wave132_gpr183_post_wave130_closure/`
- Inputs:
  - `results_v3/wave83_intervention_class_meta_rank/intervention_class_meta_rank.tsv`
  - `results_v3/wave93_gpr183_oxysterol_forcing_test/integrated_decision.tsv`
  - `results_v3/wave111_gpr183_spatial_proxy_forcing_test/summary.json`
  - `results_v3/wave112_gpr183_compartment_contrast_fallback/summary.json`
  - `results_v3/wave130_ms_treatment_response_audit/ms_treatment_response_cross_dataset_stability.tsv`
- Outputs:
  - `results_v3/wave132_gpr183_post_wave130_closure/gpr183_post_wave130_closure.tsv`
  - `results_v3/wave132_gpr183_post_wave130_closure/summary.json`
  - `results_v3/wave132_gpr183_post_wave130_closure/REPORT.md`
- Branch call: `NO_REOPEN_GPR183_AFTER_POST_WAVE130_AUDIT`
