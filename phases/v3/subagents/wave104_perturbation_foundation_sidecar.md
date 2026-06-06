# Wave104 Perturbation / Foundation-Model Sidecar

Timestamp: 2026-05-27

Scope: target-specific perturbation and model evidence audit for `IFI30`, `SP140`, `GALC`, `CD58`, and `IL7R`.

This is not a finding claim. `GO` here would mean target promotion from perturbation/foundation evidence. None of the five reaches that bar.

## Artifacts Written

Query and provenance artifacts are under `results_v3/wave104_perturbation_foundation_sidecar/`:

- `local_exact_row_extracts.tsv`: exact extracted rows, with explicit `no_row` markers.
- `public_perturbation_resource_queries.tsv`: NCBI GDS/PubMed, Europe PMC, LINCS Data Portal, SigCom, and ChEMBL query summary.
- `targeted_canonical_public_queries.tsv`: stricter canonical-symbol public query summary.
- `chembl_activity_counts.tsv`: ChEMBL activity counts from direct symbol target-search hits.
- `chembl_alias_target_search.tsv` and `chembl_alias_activity_counts.tsv`: alias-based ChEMBL checks, retained to flag false-positive target mapping.
- `raw_api/`: 168 raw API response files.

LINCS note: initial LINCS Data Portal calls failed certificate verification; retry with an unverified SSL context returned HTTP `200` and `0` entities for all five genes. SigCom returned HTTP 500/server-error artifacts for all five genes, so SigCom is not counted as a biological negative.

## Executive Call

| gene | strongest perturbation/model evidence | strongest blocker | recommendation |
| --- | --- | --- | --- |
| `IFI30` | weak Wave79 model/readout concordance and public GILT/EAE antigen-processing biology | no clean direct disease-state rescue, no modality, host-defense/antigen-processing pleiotropy | `PARK_BENCHMARK_ONLY` |
| `SP140` | real public SP140 perturbation and ChEMBL target entries | local model/efferocytosis fails, prior-art Crohn/macrophage SP140 route, weak MS anchor | `PARK_TOOL_ONLY` |
| `GALC` | public GALC enzyme/lysosomal-storage perturbation literature and ChEMBL target | no autoimmune rescue direction, local model and CRISPR screen negative/unsupported | `NO_GO` |
| `CD58` | real CD2-CD58 druggability/prior art and local Wave79 targetability | no local foundation/direct rescue, direction conflicts with protective MS genetics and prior-art axis | `PARK_COMPARATOR_ONLY` |
| `IL7R` | strongest local Geneformer support among this set plus public IL7R biologic perturbation | saturated/prior-art CD127 axis, lymphoid safety and unclear APC-only direction | `PARK_COMPARATOR_ONLY` |

Weak surrogate rule applied: Geneformer in-silico deletion, broad PubMed/Europe PMC counts, oncology/CAR-T perturbation, lysosomal-storage models, and pathway-level antigen-presentation biology were not treated as direct autoimmune disease-state rescue.

## Local Evidence

Primary local inputs checked:

- `results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave79_targetability_shortlist_audit/targetability_integrated_decision.tsv`
- `results_v3/wave79_targetability_shortlist_audit/targetability_foundation_summary.tsv`
- `results_v3/wave79_targetability_shortlist_audit/targetability_foundation_rank_rows.tsv`
- `results_v3/wave79_targetability_shortlist_residual_audit/targetability_shortlist_candidate_matrix.tsv`
- `results_v3/wave103_intervention_first_successor_triage/intervention_first_successor_rank.tsv`
- `results_v3/wave103_sender_to_myeloid_bridge_scan/sender_bridge_gene_summary.tsv`
- `results_v3/wave103_fc_receptor_efferocytosis_route_audit/fc_efferocytosis_route_rank.tsv`

### Wave57 Geneformer Intervention-First

| gene | row present | token contexts >=3 | support / strong | best context | best z | projection minus random | priority | Wave57 call |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |
| `IL7R` | yes | `1` | `1 / 1` | `ra_myeloid_dendritic` | `0.5289555289406979` | `0.0317525753667318` | `7.25` | `REOPEN_MODEL_SUPPORTED_INTERVENTION_FIRST` |
| `GALC` | yes | `1` | `0 / 0` | `IBD_myeloid` | `1.2767979884541334` | `-0.039924054403349396` | `0.25` | `NO_GO_MODEL_SCREEN` |
| `SP140` | yes | `0` | `0 / 0` | `ra_nonclassical_monocyte` | `-0.4743264352507738` | `0.018558719669171102` | `0.0` | `NO_GO_MODEL_SCREEN` |
| `IFI30` | no | - | - | - | - | - | - | no row |
| `CD58` | no | - | - | - | - | - | - | no row |

Interpretation: only `IL7R` has a direct Wave57 model-support call. It is still a model surrogate with one token-adequate context.

### Wave81 Perturbation-First Integration

| gene | Wave81 call | score | direct perturbation | foundation support | foundation detail | MS anchor | target/genetics gate | broad positives | blocker / reason |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- | --- |
| `IL7R` | `NO_GO_PERTURBATION_FIRST_BLOCKED` | `9` | `0` | `1` | `wave57:support=1,strong=1,token_contexts=1;wave69d:support=1,strong=1,token_contexts=2;wave70c:support=3,strong=1,token_contexts=4` | `1` | `1` | `Crohn disease;type 1 diabetes mellitus;ulcerative colitis` | `IL7R genetics/druggability but prior audited and broad T-cell biology` |
| `SP140` | `NO_GO_PERTURBATION_FIRST_BLOCKED` | `8` | `0` | `0` | blank | `1` | `1` | `Crohn disease;Sjogren syndrome;psoriasis;ulcerative colitis` | closed SP140 prior-art/chemistry branch |
| `GALC` | `NO_GO_PERTURBATION_FIRST_BLOCKED` | `7` | `0` | `0` | blank | `1` | `1` | `psoriasis;type 1 diabetes mellitus;ulcerative colitis` | sphingolipid enzyme route prior audited; no translational specificity |
| `IFI30` | no row | - | - | - | - | - | - | - | not in integrated rank |
| `CD58` | no row | - | - | - | - | - | - | - | not in integrated rank |

Wave81 detail rows:

- `IL7R` Wave69d: `support_contexts=1`, `strong_support_contexts=1`, best context `GSE282122_DC_post_nonremission_to_remission_UC_only`, z `1.3475858023767018`, projection `0.0621426369969008`, priority `7.5`.
- `IL7R` Wave70c: `support_contexts=3`, `strong_support_contexts=1`, `opposing_contexts=1`, best context `GSE282122_DC_post_nonremission_to_remission`, z `1.0477840374075034`, projection `0.1107569133274308`, priority `13.5`.
- `SP140` Wave69d: `support_contexts=0`, `strong_support_contexts=0`, best z `-0.3570072808525479`, projection `-0.0240805782151356`, priority `0.0`.

### Wave37 GSE212008 CRISPR Efferocytosis Screen

| gene | row present | n sgRNA | efficient LFC | noneater LFC | efficient-minus-noneater LFC | contrast FDR | screen call |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `SP140` | yes | `4` | `0.47979961255173575` | `-0.5733526563236783` | `1.0553304433165922` | `0.920009505703422` | `UNRESOLVED` |
| `IL7R` | yes | `3` | `0.4388892132710165` | `0.6283890478029444` | `-0.15536182895519923` | `1.0` | `UNRESOLVED` |
| `IFI30` | yes | `4` | `-0.3216891245223269` | `0.1348614162787738` | `-0.24465894347146855` | `0.920009505703422` | `UNRESOLVED` |
| `GALC` | yes | `4` | `-0.42764911042457443` | `0.12424562933878536` | `-0.6411892122129084` | `0.9965506589785832` | `UNRESOLVED` |
| `CD58` | no | - | - | - | - | - | no row |

Interpretation: no target has a significant/direct efferocytosis screen call. `SP140` has a large positive median contrast, but the FDR is `0.9200`; it is explicitly `UNRESOLVED`.

### Wave79 Foundation / Targetability Outputs

Wave79 targetability rows are present only for `CD58` and `IFI30`.

| gene | Wave79 call | gate count | positives | APC/myeloid positives | MS delta / p / FDR | QTL strong H4 diseases | RA p | IBD p | foundation rows | foundation support / do-not-promote | modality | reason |
| --- | --- | ---: | --- | --- | --- | --- | ---: | ---: | ---: | --- | --- | --- |
| `CD58` | `PARK_TARGETABILITY_SHORTLIST_NODE` | `8` | `Crohn disease;type 1 diabetes mellitus;ulcerative colitis` | `Crohn disease;ulcerative colitis` | `0.1797564428759965 / 0.3110884246237163 / 0.9095100064215184` | `Crohn;MS` | `0.002977517998379077` | `0.17319632161569962` | `0` | `0 / 0` | `surface_biologic_possible` | partial support, critical gates fail |
| `IFI30` | `NO_GO_TARGETABILITY_SHORTLIST_NODE` | `5` | `psoriasis;type 1 diabetes mellitus;ulcerative colitis` | `psoriasis;ulcerative colitis` | `0.21016237009791 / 0.379946954952182 / 0.9141270983319502` | `Celiac;Crohn;MS` | `0.3778191741777486` | `0.6648210415593697` | `12` | `1 / 1` | `benchmark_antigen_processing_no_clean_modality` | insufficient target-level convergence after strict gates |

Wave79 foundation rank details for `IFI30`:

- source: `wave15_loader_dependency_delete`
- total support / strong support: `1 / 1`
- best source context: `IBD_myeloid`
- best context cells with token: `3`
- best mean projection shift: `-0.0121384225785732`
- best context cosine z: `0.8853592302288179`
- best context projection-minus-random: `0.0496691847252401`
- GSE162463 MHCII median low-vs-high log2: `0.4599160523462348`
- GSE162463 MHCII FDR: `0.9813802911036013`
- readout sources: `GSE162464_mouse_macrophage_RNAseq;GSE294918_human_ruxolitinib;Mixscale_GSE281048`
- readout min log2FC: `-1.34385893389944`
- real perturbation alignment: `model_with_readout_concordance_only`
- foundation recommendation: `triage_only_no_direct_candidate_perturbation`

Wave79 residual audit:

- `CD58`: `PARK_CD58_MS_GENETIC_BUT_NO_STATE_RESPONSE_CONVERGENCE`; `pass_count=2`; direct residual disease count `0`; raw positive disease count `3`; MS expression anchor `False`; MS genetic anchor `True`; response support count `0`; modality ready local `True`.
- `IFI30`: `BENCHMARK_NOT_NOMINATION`; `pass_count=1`; direct residual disease count `0`; raw positive disease count `4`; MS expression anchor `False`; MS genetic anchor `True`; response support count `0`; modality ready local `False`.

### Wave103 Successor / Bridge Outputs

Wave103 intervention-first successor triage included all five and called all five `NO_GO_PRIOR_OR_SAFETY_BLOCKED`.

| gene | Wave103 score | gate count | missing gates | direct perturbation | foundation support | nonexpression anchor | MS anchor | cross-disease anchor | direction/response support | reachable modality | prior/safety blocked | call |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `IL7R` | `14.7` | `4` | `reachable_modality` | `False` | `True` | `True` | `True` | `True` | `True` | `False` | `True` | `NO_GO_PRIOR_OR_SAFETY_BLOCKED` |
| `SP140` | `7.35` | `3` | `direction_or_response_support;reachable_modality` | `False` | `False` | `True` | `True` | `True` | `False` | `False` | `True` | `NO_GO_PRIOR_OR_SAFETY_BLOCKED` |
| `GALC` | `5.699999999999999` | `3` | `direction_or_response_support;reachable_modality` | `False` | `False` | `True` | `True` | `True` | `False` | `False` | `True` | `NO_GO_PRIOR_OR_SAFETY_BLOCKED` |
| `CD58` | `4.699999999999999` | `3` | `direction_or_response_support;reachable_modality` | `False` | `False` | `True` | `True` | `True` | `False` | `False` | `True` | `NO_GO_PRIOR_OR_SAFETY_BLOCKED` |
| `IFI30` | `3.6999999999999993` | `4` | `reachable_modality` | `False` | `False` | `True` | `True` | `True` | `True` | `False` | `True` | `NO_GO_PRIOR_OR_SAFETY_BLOCKED` |

Additional Wave103 sender-to-myeloid bridge output:

- `IFI30` only: `bridge_link_count=0`, `bridge_link_disease_count=0`, `raw_up_tissue_disease_count=1`, `best_wave30_axis=IFNG_IFNGR_JAK_STAT1_CIITA`, best Wave30 call `CENTRAL_STATE_DRIVER_NOT_SELECTIVE_THERAPEUTIC`, `bridge_score=0.8239999999999998`, call `NO_GO_WEAK_OR_CONTEXT_SPECIFIC_BRIDGE`.

## External Query Summary

Public resources queried:

- NCBI GDS/GEO via E-utilities.
- PubMed via E-utilities.
- Europe PMC REST API.
- LINCS Data Portal entity API.
- SigCom LINCS metadata API.
- ChEMBL target and activity APIs.

Source URLs are in `public_perturbation_resource_queries.tsv`, `targeted_canonical_public_queries.tsv`, and ChEMBL TSVs. Key public source pages used for interpretation include PubMed/PMC SP140 GSK761 (`https://pubmed.ncbi.nlm.nih.gov/35986286/`), SP140 loss-of-function Crohn biology (`https://pmc.ncbi.nlm.nih.gov/articles/PMC9442451/`), IFI30/GILT EAE (`https://pubmed.ncbi.nlm.nih.gov/22586035/`), EAE translational review noting IFI30/GILT mechanism (`https://pmc.ncbi.nlm.nih.gov/articles/PMC4654535/`), CD2-CD58 autoimmune inhibition example (`https://pmc.ncbi.nlm.nih.gov/articles/PMC3707497/`), GSK2618960 anti-IL7R healthy-subject study (`https://pmc.ncbi.nlm.nih.gov/articles/PMC6339973/`), and IUPHAR lusvertikimab/OSE-127 page (`https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId=9604&tab=clinical`).

### Canonical Public Query Counts

| gene | NCBI GDS canonical perturbation | PubMed canonical title/abstract perturbation | PubMed Perturb-seq | Europe PMC title/abstract perturbation | Europe PMC Perturb-seq | LINCS Data Portal retry | SigCom | ChEMBL exact symbol search |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| `IFI30` | `2` | `32` | `0` | `68` | `6` | `0` | HTTP 500 | `0` |
| `SP140` | `49` | `30` | `0` | `54` | `5` | `0` | HTTP 500 | `2` |
| `GALC` | `21` | `169` | `0` | `234` | `38` | `0` | HTTP 500 | `2` |
| `CD58` | `50` | `301` | `1` | `325` | `58` | `0` | HTTP 500 | `2` |
| `IL7R` | `62` | `533` | `1` | `402` | `87` | `0` | HTTP 500 | `0` |

Interpretation caveat: Europe PMC Perturb-seq counts are broad co-mention counts and include reviews, oncology screens, and preprints. I did not treat these as direct target-specific Perturb-seq rescue evidence unless the top records were direct and disease-relevant. For this audit, none of the Perturb-seq query outputs supplies a clean autoimmune APC/myeloid rescue dataset.

### ChEMBL

Direct symbol target search:

- `SP140`: `CHEMBL3108643` nuclear body protein SP140, `61` activity rows; `CHEMBL4105997` SP140-like protein, `19` rows.
- `GALC`: `CHEMBL3713095` human galactocerebrosidase, `1988` rows; `CHEMBL2218` mouse galactocerebrosidase, `11` rows.
- `CD58`: `CHEMBL3790` LFA-3/CD58, `7` rows; `CHEMBL3885600` CD58/CD2 PPI, `9` rows.
- `IFI30`: no exact ChEMBL target by `IFI30`; alias query returned interferon/AIM2 false-positive targets, not IFI30/GILT.
- `IL7R`: no exact ChEMBL target by `IL7R` or `CD127`; alias query for `interleukin-7 receptor` returned other interleukin receptors, not a clean IL7R/CD127 target.

ChEMBL target links:

- SP140: `https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3108643/`
- GALC human: `https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3713095/`
- CD58/LFA-3: `https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3790/`
- CD58/CD2 PPI: `https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3885600/`

## Per-Gene Audit

### `IFI30`

Local evidence:

- No Wave57 intervention-first row.
- No Wave81 integrated-rank row.
- Wave37 CRISPR efferocytosis: `n_sgrna=4`, efficient-minus-noneater LFC `-0.24465894347146855`, contrast FDR `0.920009505703422`, `UNRESOLVED`.
- Wave79 targetability: `NO_GO_TARGETABILITY_SHORTLIST_NODE`, gate count `5`, MS delta `0.21016237009791`, MS p `0.379946954952182`, MS FDR `0.9141270983319502`, QTL strong H4 diseases `Celiac;Crohn;MS`, foundation rows `12`, supportive/do-not-promote `1/1`.
- Wave79 foundation rank: only `model_with_readout_concordance_only`, recommendation `triage_only_no_direct_candidate_perturbation`.
- Wave79 residual: `BENCHMARK_NOT_NOMINATION`; direct residual disease count `0`, response support count `0`, local modality ready `False`.
- Wave103 successor: `NO_GO_PRIOR_OR_SAFETY_BLOCKED`, score `3.7`, reachable modality missing.
- Wave103 sender bridge: `NO_GO_WEAK_OR_CONTEXT_SPECIFIC_BRIDGE`, bridge link count `0`.

External evidence:

- Canonical NCBI GDS perturbation count `2`, but top records are not clean IFI30 autoimmune/APC perturbation datasets.
- Canonical PubMed title/abstract perturbation count `32`; top records are antigen-processing, cancer, fibrosis, and vaccine/host-defense contexts.
- PubMed Perturb-seq count `0`.
- Europe PMC title/abstract perturbation count `68`; top direct hit includes cancer IFI30 knockdown, not autoimmune rescue.
- Europe PMC Perturb-seq count `6`; top records are co-mention or broad screens, not IFI30-specific autoimmune Perturb-seq.
- ChEMBL exact target search `0`.
- Public IFI30/GILT EAE literature is target-specific antigen-presentation biology, but it is a weak surrogate for therapeutic rescue: GILT deficiency changes MOG/EAE antigen processing and disease mechanism, not a selective lipid-lysosomal myeloid rescue route.

Weak surrogate flags:

- GILT/IFI30 is an antigen-processing and host-defense node. Target perturbation can alter antigen presentation in epitope-dependent ways.
- Wave79 model support is sparse and explicitly not a direct perturbation nomination.
- Public EAE biology is mechanistic and antigen-context dependent; it does not define a druggable target action.

Recommendation: `PARK_BENCHMARK_ONLY`. Use IFI30 as an antigen-processing benchmark/readout if needed. Do not promote as an intervention target.

### `SP140`

Local evidence:

- Wave57 row: token contexts >=3 `0`; support/strong `0/0`; best context `ra_nonclassical_monocyte`; best z `-0.4743264352507738`; projection `0.018558719669171102`; priority `0.0`; call `NO_GO_MODEL_SCREEN`.
- Wave81: `NO_GO_PERTURBATION_FIRST_BLOCKED`, score `8`, direct perturbation `0`, foundation support `0`, MS anchor `1`, target/genetics gate `1`, broad positives `Crohn disease;Sjogren syndrome;psoriasis;ulcerative colitis`.
- Wave81 Wave69d: support/strong `0/0`, best z `-0.3570072808525479`, projection `-0.0240805782151356`, priority `0.0`.
- Wave37 CRISPR efferocytosis: `n_sgrna=4`, efficient-minus-noneater LFC `1.0553304433165922`, contrast FDR `0.920009505703422`, `UNRESOLVED`.
- Wave103: score `7.35`, gate count `3`, missing `direction_or_response_support;reachable_modality`, direct perturbation `False`, foundation support `False`, call `NO_GO_PRIOR_OR_SAFETY_BLOCKED`.

External evidence:

- Canonical NCBI GDS perturbation count `49`; top records include direct SP140 inhibition datasets such as transient SP140 inhibition in human pluripotent-stem-cell fate assays and SP140 knockout in Ramos cells.
- Canonical PubMed title/abstract perturbation count `30`.
- Europe PMC title/abstract perturbation count `54`; top records include SP140 inflammatory/macrophage and antiviral/chromatin literature.
- PubMed Perturb-seq count `0`; Europe PMC Perturb-seq count `5`, top records are not direct SP140 autoimmune APC rescue datasets.
- ChEMBL exact target search found `CHEMBL3108643` with `61` activity rows and `CHEMBL4105997` with `19` rows.
- Public SP140 GSK761 macrophage paper is real target-specific perturbation evidence, but it is already a Crohn/inflammatory macrophage target route and does not establish V3 cross-autoimmune/MS lipid-lysosomal rescue.

Weak surrogate flags:

- Public perturbation is strongest for Crohn/macrophage inflammatory biology and tool-compound SP140 inhibition.
- Local CRISPR efferocytosis has a large positive contrast but no statistical support.
- Local foundation screens fail.
- ChEMBL rows establish chemical/tool matter, not disease-specific target action.

Recommendation: `PARK_TOOL_ONLY`. Keep as a tool/comparator for SP140-high Crohn/macrophage biology. Do not promote as a new V3 target.

### `GALC`

Local evidence:

- Wave57 row: token contexts >=3 `1`; support/strong `0/0`; best context `IBD_myeloid`; best z `1.2767979884541334`; projection `-0.039924054403349396`; priority `0.25`; call `NO_GO_MODEL_SCREEN`.
- Wave81: `NO_GO_PERTURBATION_FIRST_BLOCKED`, score `7`, direct perturbation `0`, foundation support `0`, MS anchor `1`, target/genetics gate `1`, broad positives `psoriasis;type 1 diabetes mellitus;ulcerative colitis`.
- Wave37 CRISPR efferocytosis: `n_sgrna=4`, efficient-minus-noneater LFC `-0.6411892122129084`, contrast FDR `0.9965506589785832`, `UNRESOLVED`.
- Wave103: score `5.7`, gate count `3`, missing `direction_or_response_support;reachable_modality`, direct perturbation `False`, foundation support `False`, call `NO_GO_PRIOR_OR_SAFETY_BLOCKED`.

External evidence:

- Canonical NCBI GDS perturbation count `21`; top records are sphingolipid/oligodendrocyte/oncology or unrelated perturbations, not GALC autoimmune rescue.
- PubMed title/abstract perturbation count `169`.
- Europe PMC title/abstract perturbation count `234`; top records include GALC lysosomal-storage/Krabbe correction and disease models.
- PubMed Perturb-seq count `0`; Europe PMC Perturb-seq count `38`, but top records are broad CRISPR/review/co-mention records rather than GALC-targeted autoimmune Perturb-seq.
- ChEMBL exact target search found human GALC `CHEMBL3713095` with `1988` activity rows and mouse GALC `CHEMBL2218` with `11` rows.

Weak surrogate flags:

- GALC perturbation literature is dominated by enzyme deficiency, Krabbe disease, lipid/lysosomal-storage correction, and CNS/myelin biology.
- These are not evidence that GALC inhibition or restoration selectively rescues the autoimmune APC/myeloid state.
- ChEMBL enzyme activity rows do not define therapeutic direction.

Recommendation: `NO_GO`. The external signal is lysosomal-storage/enzyme biology, not target-specific autoimmune perturbation rescue.

### `CD58`

Local evidence:

- No Wave57 row.
- No Wave81 integrated-rank row.
- No Wave37 row.
- Wave79: `PARK_TARGETABILITY_SHORTLIST_NODE`, gate count `8`, positives `Crohn disease;type 1 diabetes mellitus;ulcerative colitis`, APC/myeloid positives `Crohn disease;ulcerative colitis`, MS delta `0.1797564428759965`, MS p `0.3110884246237163`, MS FDR `0.9095100064215184`, QTL strong H4 diseases `Crohn;MS`, RA response p `0.002977517998379077`, IBD response p `0.17319632161569962`, foundation rows `0`.
- Wave79 residual: `PARK_CD58_MS_GENETIC_BUT_NO_STATE_RESPONSE_CONVERGENCE`; direct residual disease count `0`, raw positive disease count `3`, response support count `0`, local modality ready `True`.
- Wave103: score `4.7`, gate count `3`, missing `direction_or_response_support;reachable_modality`, direct perturbation `False`, foundation support `False`, call `NO_GO_PRIOR_OR_SAFETY_BLOCKED`.

External evidence:

- Canonical NCBI GDS perturbation count `50`; top records are CAR-T, cancer immune escape, and CD58 regulator CRISPR screens.
- Canonical PubMed title/abstract perturbation count `301`; top records are immune-synapse/cancer/CAR-T/regulatory contexts.
- PubMed Perturb-seq count `1`: deletion of `TMEM30A` enabling leukemic NK evasion, not a CD58 autoimmune rescue dataset.
- Europe PMC Perturb-seq count `58`; top records are broad screening/review records.
- ChEMBL exact target search found LFA-3/CD58 `CHEMBL3790` with `7` rows and CD58/CD2 PPI `CHEMBL3885600` with `9` rows.
- Public CD2-CD58 inhibition literature and alefacept-like biology show the axis is targetable/prior-art, but this is not a novel or direction-clean autoimmune rescue.

Weak surrogate flags:

- Most public perturbation hits are oncology, CAR-T, immune escape, or PPI/prior-art immunosuppression.
- Local foundation support is absent.
- Local Wave79 response signal is insufficient and directionally conflicted by MS genetics/prior CD58 biology.

Recommendation: `PARK_COMPARATOR_ONLY`. Use CD58/CD2 as a benchmark or stratification/comparator axis, not as a promoted target.

### `IL7R`

Local evidence:

- Wave57: token contexts >=3 `1`; support/strong `1/1`; best context `ra_myeloid_dendritic`; best z `0.5289555289406979`; projection `0.0317525753667318`; priority `7.25`; call `REOPEN_MODEL_SUPPORTED_INTERVENTION_FIRST`.
- Wave81: `NO_GO_PERTURBATION_FIRST_BLOCKED`, score `9`, direct perturbation `0`, foundation support `1`, MS anchor `1`, target/genetics gate `1`, broad positives `Crohn disease;type 1 diabetes mellitus;ulcerative colitis`.
- Wave81 Wave69d: support/strong `1/1`, best z `1.3475858023767018`, projection `0.0621426369969008`, priority `7.5`.
- Wave81 Wave70c: support/strong `3/1`, opposing contexts `1`, best z `1.0477840374075034`, projection `0.1107569133274308`, priority `13.5`.
- Wave37 CRISPR efferocytosis: `n_sgrna=3`, efficient-minus-noneater LFC `-0.15536182895519923`, contrast FDR `1.0`, `UNRESOLVED`.
- Wave103: score `14.7`, gate count `4`, missing `reachable_modality`, direct perturbation `False`, foundation support `True`, direction/response support `True`, call `NO_GO_PRIOR_OR_SAFETY_BLOCKED`.

External evidence:

- Canonical NCBI GDS perturbation count `62`, mostly lymphoid/leukemia/immune context records rather than APC-only autoimmune rescue.
- PubMed title/abstract perturbation count `533`; public IL7R perturbation and antibody biology is extensive.
- PubMed Perturb-seq count `1`: orthogonal CRISPR screens in human CD8 T-cell function, not an APC/myeloid rescue dataset.
- Europe PMC title/abstract perturbation count `402`; top records include IL7R macrophage/cancer and inflammatory/immune biology.
- Europe PMC Perturb-seq count `87`; top records are mostly T-cell or broad screen references.
- LINCS Data Portal retry found `0` entities.
- ChEMBL exact symbol search found `0`; alias searches returned other interleukin receptor targets, not clean IL7R/CD127 entries.
- Public clinical/biologic perturbation exists outside ChEMBL, including anti-IL7R/CD127 antibodies such as GSK2618960 and lusvertikimab/OSE-127.

Weak surrogate flags:

- Local model support is the strongest of the five but still model-heavy and concentrated in limited myeloid/dendritic contexts.
- Public perturbation is dominated by lymphoid survival, memory T cells, TSLP/IL7 signaling, leukemias, and clinical biologics.
- Direct APC-only module rescue is not established.
- The route is prior-art and safety-conflicted for a new V3 target claim.

Recommendation: `PARK_COMPARATOR_ONLY`. Keep as a strong positive-control/comparator and possible APC-vs-T-cell falsification axis. Do not claim a novel finding.

## Final Recommendation

No `GO`.

- `PARK_BENCHMARK_ONLY`: `IFI30`
- `PARK_TOOL_ONLY`: `SP140`
- `PARK_COMPARATOR_ONLY`: `CD58`, `IL7R`
- `NO_GO`: `GALC`

Operationally, the only useful next uses are bounded controls: IFI30 as antigen-processing readout, SP140 as a Crohn/macrophage tool comparator, CD58 and IL7R as prior-art immune-axis comparators. `GALC` should be closed for this perturbation/foundation route unless a new target-specific autoimmune APC/myeloid rescue dataset appears.
