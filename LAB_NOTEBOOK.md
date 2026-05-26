# Lab Notebook

All times are Europe/Berlin (`UTC+02:00`). Entries are append-only descriptions of actions and decisions; errors and abandoned paths remain recorded.

## 2026-05-26T17:04:39+02:00 - Resume and selection

- Re-read `MS_RESEARCH_LOG_2026-05-26.md` and persistent memory note.
- Environment observation: the working directory initially contained only the prior research log and `.DS_Store`; it was not a Git repository. Python `3.13.3` is installed; `R` is not installed.
- Initialized Git so requested intermediate outputs can be committed.
- Considered Hypothesis 1, but found no public paired EBV-imprinted CSF plus longitudinal PRL MRI dataset during feasibility search.
- Considered Hypothesis 2, but the closest mechanistic processed dataset (`GSE299939` plus Zenodo `10.5281/zenodo.15602185`) is an R/Seurat object from a mouse model and would mainly replicate its source publication.
- Selected a constrained test of Hypothesis 3 because `GSE180759` and `GSE279972` provide public human lesion expression data suitable for a necessary-intermediate test.
- Important downscope: lesion transcriptomes do not measure EBV infection/specificity. Any detected relationship is "EBV-compatible adaptive-to-microglial circuitry," not evidence for EBV causation.

## 2026-05-26T17:04:39+02:00 - Pre-analysis lock

- Created `SELECTION.md` and `PLAN.md` before downloading or examining expression values.
- Predeclared three gene programs and calling rules. The primary target is the association between `ADAPT_41BB` and `MIMS_LIPID_COMP`; the focus on the 4-1BB axis is motivated by EBV CNS-homing B-cell literature but is tested as a non-virus-specific tissue program.
- Planned to document any inability to conduct donor-aware tests or any insufficient rare-cell count as a limitation or negative outcome, not to substitute a data-driven successful pathway.

## 2026-05-26T17:06:00+02:00 - Git write restriction encountered

- Attempted to commit the locked selection and plan. The sandbox permitted repository initialization but rejected creation of `.git/index.lock` (`Operation not permitted`).
- This is an execution-environment restriction rather than an analytical failure. I will request permission for Git metadata writes so intermediate deliverables can be committed as required.

## 2026-05-26T17:09:00+02:00 - Retrieval scaffolding

- Git permission was granted and the locked plan was committed as `1865c32`.
- Added a deterministic data downloader for the two predeclared GEO accessions and a structural inspection script. Raw data will be excluded from Git; calculated SHA-256 manifests will be tracked.
- Added a pinned Python dependency list and end-to-end shell entry point. The statistical script is intentionally not yet written because deposited annotation formats must first be inspected rather than assumed.

## 2026-05-26T17:12:00+02:00 - Download and structural inspection

- Downloaded preregistered files from `GSE180759` and `GSE279972` and wrote SHA-256 checksums to `data/derived/data_manifest.tsv`. Installed pinned Python packages in `.venv`.
- `GSE180759` contains 66,432 nuclei with author-provided labels. It includes 21,522 nuclei at chronic active lesion edges, 19,770 periplaque, 15,510 chronic inactive edges, 4,339 lesion core, and 5,291 control white-matter nuclei.
- Constraint discovered before expression testing: only five donor-by-pathology blocks contain both at least 20 lymphocytes and at least 20 immune/myeloid nuclei; three are chronic active edges. Under `PLAN.md` Decision Point 1, this dataset will provide localization/descriptive cell-resolved evidence rather than a powered immune-to-microglia correlation.
- `GSE279972` provides 109 bulk count files with lesion codes, but the GEO SOFT record does not expose the foamy/nonfoamy and donor mapping needed for the planned donor-aware inference.
- Located the authors' open processed-data/code deposit through the published Nature Neuroscience data-availability statement: Zenodo concept DOI `10.5281/zenodo.17735822`, current record `10.5281/zenodo.19352263`, containing `Processed data all omics.xlsx` (28,838,573 bytes). Adding this deposited metadata workbook is consistent with the planned step to extract validation clinical/lesion metadata and does not select on expression outcomes.

## 2026-05-26T17:13:00+02:00 - Novelty boundary tightened before statistical testing

- Full-text review identified relevant prior publications before results were generated.
- Van der Vliet et al., *Nature Neuroscience*, published 2026-05-21, directly report that foamy lesions contain an adaptive immune module with `CD79A`, `CCL5`, and `IGHG1`, together with microglial lipid/lysosomal modules. Consequently, general `B_APC`/`MIMS_LIPID_COMP` and `CCL5` associations are replication controls, not new findings.
- A 2020 study reports CD137-positive B cells in MS tissue including chronic active lesions, and murine/EAE work reports CD137L-linked microglial activation. Consequently, presence of 4-1BB biology in MS is not novel.
- The remaining possible delta is narrower: whether `TNFSF9`/`TNFRSF9` expression is specifically associated with the foamy/lipid-complement program in the newly published human bulk lesion cohort and localizable in the older cell-resolved chronic-active-edge dataset. This will be claimed only if supported under the locked thresholds and not stated directly in prior full text.

## 2026-05-26T17:15:00+02:00 - Validation metadata recovered and implementation adjusted

- Downloaded the authors' deposited `Processed data all omics.xlsx` from Zenodo record `19352263`; the generated SHA-256 hash is tracked in the data manifest.
- The workbook's metadata sheet exposes `NBB donor ID`, lesion categories, and `Morphology microglia`: 110 recorded RNA-seq metadata specimens from 38 donors, with 23 marked `foamy` and 32 marked `non_foamy`; other specimens have no applicable morphology classification.
- The workbook RNA sheet stores normalized expression keyed by Ensembl ID; the GEO count archive includes symbol-labelled count files. The analysis will use GEO counts for transparent normalization and the workbook only for deposited sample/donor/lesion metadata.
- Tightened reproducibility mechanics: the generated manifest will retain URLs, sizes, and hashes but omit run-time timestamps so repeat execution does not alter a tracked result; a full transitive dependency lock file is added for the entry point.

## 2026-05-26T17:19:00+02:00 - Statistical implementation written before outcome inspection

- Added a locked novelty addendum to `PLAN.md`: broad adaptive/B-cell-to-foamy-microglia module analysis is now a published-result replication control; `TNFRSF9`, `TNFSF9`, and their two-gene score are the focused target readouts.
- Implemented `scripts/analyze.py`. It reads symbol-labelled GEO counts, uses author-deposited donor/morphology metadata, computes `log2(CPM + 1)` target expression and predeclared module scores, applies donor-grouped GEE tests with Benjamini-Hochberg correction, and uses a fixed seed (`20260526`) for donor bootstrap confidence intervals and plots.
- For `GSE180759`, the implementation streams the dense matrix without loading it wholesale, aggregates nuclei into donor-by-pathology-by-cell-type pseudobulks, applies the predeclared 20-nucleus eligibility rule, and exports localization tables without upgrading the underpowered paired comparison to an inferential claim.

## 2026-05-26T17:23:00+02:00 - First locked analysis output and required suspicion check

- Executed `scripts/analyze.py` with random seed `20260526`.
- The broad module positive control reproduced the published direction in `GSE279972`: `ADAPT_41BB` versus `MIMS_LIPID_COMP` had Spearman `rho=0.383` across 99 MS samples from 28 donors; donor-grouped GEE `FDR=4.31e-05`. This is not novel because the source article already reports related adaptive and lipid/lysosomal modules.
- The focused result was initially interesting: among 54 specimens with deposited foamy/non-foamy morphology from 21 MS donors, the two-gene `COSTIM_41BB` score was elevated in foamy specimens (`d=1.117`; GEE coefficient `0.581`, lesion-class adjusted `p=0.00359`, focused-family `FDR=0.0216`).
- The result does **not** satisfy the originally desired bridge endpoint: `COSTIM_41BB` did not correlate with `MIMS_LIPID_COMP` across all 99 MS specimens (`rho=0.125`, 95% donor-bootstrap interval `-0.102` to `0.352`, `FDR=0.266`). `TNFRSF9` alone did associate weakly with the microglial program (`rho=0.238`, `FDR=0.0344`), below the predeclared biologically meaningful `rho >= 0.40` criterion.
- Discovery cross-validation is unavailable at adequate power: `GSE180759` yielded only five eligible paired lymphocyte/immune pseudobulk blocks and only three chronic-active edges. In those three edges, lymphocyte `COSTIM_41BB` scores were `-0.5`, `-0.5`, and `0.75`, so no consistent descriptive support exists.

## 2026-05-26T17:25:00+02:00 - Post-result sensitivity analysis rationale

- Because the composite passed FDR while neither individual gene passed the same adjusted foamy/non-foamy contrast, I treated the result as potentially unstable or compositional rather than accepting it immediately.
- Manual sensitivity checks showed the composite foamy coefficient remained positive after adding `B_APC` or `MIMS_LIPID_COMP` to the donor-grouped lesion-class-adjusted GEE model, and was positive/significant in each leave-one-donor-out fit.
- However, only six donors contributed both foamy and non-foamy specimens; their paired composite difference had Wilcoxon `p=0.09375`. This materially limits within-person inference.
- Added these pre-specified-confounder/post-result robustness diagnostics to `scripts/analyze.py` so that the final evidence and its weakness are reproduced by the documented entry point rather than reported from an ad hoc console calculation.

## 2026-05-26T17:28:00+02:00 - Sensitivity rerun and intermediate results checkpoint

- Re-executed `scripts/analyze.py`; it completed without analytical errors and wrote sensitivity, leave-one-donor-out, paired-donor, and run-summary artifacts.
- Fixed one non-substantive Matplotlib deprecation warning (`labels` to `tick_labels`) while adding reproducible sensitivity output; it does not alter statistical results.
- Committed the result artifacts and post-result diagnostic implementation as Git checkpoint `e8befea`.

## 2026-05-26T17:33:00+02:00 - Novelty search outcome and final interpretation decision

- Queried PubMed, Google Scholar, bioRxiv (direct attempt plus indexed/domain-search fallback), Europe PMC, and accessible full text. Queries and limitations are written in `NOVELTY_SEARCH.md`.
- The novelty search confirms that general CD137 biology in MS lesions is existing work (Wong et al., 2020) and that adaptive/foamy-microglial module biology in `GSE279972` is published by its generators (Van der Vliet et al., 2026).
- No direct report of the specific targeted negative `TNFRSF9`/`TNFSF9` versus lipid/complement score analysis was located. The final output therefore reports a narrow negative finding and explicitly relegates the foamy enrichment to an exploratory side observation.

## 2026-05-26T17:36:00+02:00 - Traceability completion

- Added machine-readable output for the negative calling rule and for the planned spatial-validation sample-size calculation (`results/falsification_power.tsv`), so that numeric future-design statements in `FINDING.md` are produced by versioned code.
- Executed the documented end-to-end entry point `./run_analysis.sh`; it completed successfully, reused/download-verified public inputs, and regenerated the same result values plus the new power artifact.
- Automated consistency assertions confirmed that the negative-call values in `results/run_summary.json` equal the statistics table and that the `d=0.65`, 90%-power paired design rounds up to 27 donors. The proposed tissue collection target remains 30 to permit attrition.

# Therapeutic Discovery Phase

## 2026-05-26T17:53:00+02:00 - Reframe after reviewer correction

- Re-read the design log and executed negative report. Accepted the reviewer criticism that the prior bulk-score test was not a strong operationalization of a spatially restricted immune-to-microglia lesion mechanism.
- Discontinued 4-1BB score mining as a therapeutic discovery path. The prior negative remains valid for its narrow bulk surrogate only.
- Identified newly relevant public human spatial data from Feng et al.: MERFISH `GSE284005` (manageable `RAW.tar`, 31.4 MB) and paired snRNA-seq `GSE301908` (large processed/raw objects), as well as experimental microglia/EAE accessions `GSE301696` and `GSE301824`.
- Recorded critical prior-art boundaries: Feng et al. pharmacologically validate `DHCR24` inhibition (`SH42`) to stimulate sterol efflux in EAE and disclose related patent interests; Van der Vliet et al. identify `MAGL` and cite an ongoing progressive-MS trial of `RO7268489`. Neither can be relabelled as a novel therapeutic finding.
- Wrote `REFRAME.md`, `TOOLS.md`, and `THERAPEUTIC_PLAN.md`. The new requirement is convergence of spatial human disease evidence, independent human multi-omics, and CNS-capable drug evidence before a candidate can survive.

## 2026-05-26T18:12:00+02:00 - Spatial data retrieval and candidate nomination before expression testing

- Added a therapeutic-specific downloader and inspection script; the original negative-result pipeline is left unchanged.
- The first download attempt failed before transfer with a transient DNS-resolution error for `ftp.ncbi.nlm.nih.gov`. A direct `curl` header check subsequently resolved successfully, and rerunning the deterministic downloader retrieved both files.
- Downloaded GEO `GSE284005_RAW.tar` (32,901,120 bytes; SHA-256 `3ce260f688412e14a9e0403e24ee0bc0a4d3c8344684e5cfb0836677b8f63816`) and its SOFT metadata file (4,252 bytes; SHA-256 `80f14d47c104cba9caa10c33eba0beaba275a5c48d0e5f396fe66281ce12850a`).
- Structural inspection establishes a strong operationalization improvement over the prior run: 17 spatial samples and 401,794 cells have deposited author labels (`majorCluster_final`, `Region_banksy`, `clean_sub`) plus coordinates and a 500-gene count panel. There are 39,765 myeloid cells and 3,473 lymphocytes; pathological labelled microglia include 5,845 `Micro Foamy`, 5,643 `Micro SPP1`, and 9,273 `Micro Stress`.
- Retrieved the authors' public code repository for method inspection only at Git commit `ff8652fa4f7372999467164babd62300550af5f6`. Their code defines T-cell neighborhoods using 100 nearest non-self neighbors, which supplies a reproducible spatial rule without guessing a radius.
- The raw labels include `DMWM`, `NAWM`, `healthyWM`, `GM`, and `Vas_Imm`, but do not contain the authors' derived lesion-rim label. New claims must therefore be restricted to DMWM/T-neighborhood context unless additional deposited rim metadata become available.
- Panel-only inspection nominated `SOAT1` as a high-risk, testable target: it is measured alongside `LIPA`, `PLIN2`, `ABCA1`, `ABCG1`, and `NR1H3`; `GBA1` and `NLRP3` are not measured. The nomination occurred before target-expression comparisons.
- Literature checks before analysis exposed a decisive risk: SOAT1 inhibition can increase `ABCA1` in myelin-debris-treated microglial cell lines (Huynh et al., 2024), but SOAT1-related lipid-droplet biogenesis is reported to be required for remyelination after focal demyelination (Gouna et al., 2021). `SOAT1` cannot become a therapeutic lead unless this repair-harm conflict is addressed experimentally.

## 2026-05-26T18:20:00+02:00 - Registered `SOAT1` spatial test fails and line is abandoned

- Implemented `scripts/analyze_spatial_targets.py` using deposited author labels and coordinates. T-near pathological microglia are defined by the authors' neighborhood convention: membership in the 100 nearest non-self neighbors of a labelled T cell within the same specimen. Inference uses donor-level means of eligible specimen pseudobulk differences, not cells as replicates.
- In `DMWM`, 12,848 myeloid cells were available, but only six donors supplied eligible paired contrasts after the locked `>=20` cells/group threshold.
- `SOAT1` failed the registered spatial gate. Pathological versus homeostatic microglia: mean delta `0.181` log2-normalized panel counts, paired `dz=0.224`, direction positive in `3/6` donors, Wilcoxon `p=0.6875`, target-family `FDR=0.9453`. T-near versus T-far pathological microglia: mean delta `0.169`, paired `dz=0.152`, positive in `3/6`, `p=0.84375`, `FDR=0.84375`.
- Registered pathway comparators did not reveal a replacement target after correction. `GPNMB` in pathological versus homeostatic microglia (`dz=1.743`, unadjusted `p=0.03125`, `FDR=0.2865`) and `APOE` in T-near versus T-far pathological microglia (`dz=1.541`, unadjusted `p=0.03125`, `FDR=0.3438`) are expected state signals and not druggable discoveries.
- Decision: abandon `SOAT1` as a therapeutic lead. It lacks supporting spatial enrichment and already carried a credible remyelination-harm concern. Proceed to an orthogonal, larger-cohort nomination screen in the existing human multi-omics lesion dataset, with `GSE284005` retained as a mandatory spatial localization validation rather than a low-power discovery bottleneck.

## 2026-05-26T18:31:00+02:00 - Orthogonal ABPP/lipidomics screen nominates `PLA2G7`

- Implemented a donor-aware, target-agnostic screen of the Van der Vliet et al. deposited workbook: 97 ABPP active proteins, 712 lipid measurements, and 3,237 quantified proteins. To avoid confusing lesion category with morphology, analysis was restricted to foamy/non-foamy specimens in active or mixed lesions (`36` metadata specimens) and fitted `value ~ foamy + active_vs_mixed` by Gaussian GEE grouped on donor.
- `MGLL`, the published source-paper target, was recovered in ABPP (`coef=1.179`, `FDR=0.0127`), providing an internal benchmark but not a discovery.
- `ABHD6` was more strongly enriched (`coef=1.677`, `FDR=0.00188`), but an immediate literature search found direct ABHD6 inhibitor efficacy claims in EAE/MS models (Wen et al., *Neuropharmacology* 2015, DOI `10.1016/j.neuropharm.2015.07.010`) and a subsequent report that the key `WWL70` anti-inflammatory effect is ABHD6-independent. It is not an honest novel therapeutic output.
- `PLA2G7`/Lp-PLA2 activity is elevated in foamy lesions (`coef=1.235`, `FDR=0.007741`, 28 specimens/18 donors). Independently measured `LPC(20:3)`, a lipid class consistent with Lp-PLA2 hydrolysis, is elevated (`coef=0.378`, `FDR=0.002666`, 29 specimens/20 donors). This nominates a mechanistic test, not yet a causal result.
- Prior-art triage found Lp-PLA2 measured previously as an MS inflammatory/vascular-risk biomarker (Sternberg et al., 2012) and discussed in EAE. The possible translational delta is a foamy-lesion/PRL-enriched subgroup for CNS-exposed Lp-PLA2 inhibition. `GSK2647544` is provisionally relevant because human PET evidence reports BBB crossing; `rilapladib` is specifically described as not believed brain-penetrant.
- Next gates: test activity-product coupling within overlapping lesions; independently validate lesion-edge immune expression in cell-resolved `GSE180759`; audit the source paper and patent/trial record before treating the subgroup proposal as novel.

## 2026-05-26T18:44:00+02:00 - Sparse-hit reporting correction and `PLA2G7` mechanistic rejection

- While interrogating screen outputs, identified a reporting artifact risk: sparse proteomic features with only eight quantified samples led the unfiltered rank order. Updated `scripts/screen_lesion_multiomics.py` to require at least 20 measured samples and 15 donors for top-lead reporting. This does not modify GEE tests or FDR across all measured features, and leaves the `PLA2G7` result unchanged.
- Implemented `scripts/link_pla2g7_lipids.py` to test 16 lysophosphatidylcholine species using only overlapping ABPP/lipidomic specimens and a donor-correlated model `lipid ~ PLA2G7 activity + foamy + lesion_group`.
- The mandatory product-link gate failed: for `LPC(20:3)`, 25 specimens from 18 donors produced residual enzyme coefficient `0.2294`, `p=0.3527`, LPC-family `FDR=0.7054`. The unadjusted Spearman correlation was only `rho=0.249` (`p=0.2296`). No LPC survived the family-wide `FDR < 0.05` criterion.
- Completed the independent targeted transcript check in `GSE180759`: only three donors had eligible paired chronic-active versus chronic-inactive lesion-edge immune pseudobulks. `PLA2G7` was higher in `2/3` donors (mean delta `0.4170` log2 CPM+1, `dz=0.626`, Wilcoxon `p=0.5`), which is underpowered and directionally incomplete rather than a replication.
- Decision: reject `PLA2G7` as a therapeutic output. Its active protein and a lipid product-class member co-enrich with foamy morphology, but the observed data do not support a target-specific product link after controlling that shared morphology.
- Pivot nominated before product coupling: `TBXAS1` has robust proteomic enrichment in foamy lesions (`coef=0.5572`, `FDR=6.90e-07`, 32 specimens/20 donors), while its stable product readout `thromboxane_B2` is elevated in lipidomics (`coef=1.5489`, `FDR=0.02529`). It now faces the same residual product-link and independent-localization gates.

## 2026-05-26T18:57:00+02:00 - `TBXAS1` product coupling passes; intended immune localization does not

- Implemented `scripts/link_tbxas1_thromboxane.py`. In 28 overlapping active/mixed-lesion specimens from 20 donors, `TBXAS1` protein strongly tracked the stable thromboxane A2 readout `thromboxane_B2`: Spearman `rho=0.7586` (`p=2.90e-06`); donor-correlated model adjusted for foamy morphology and lesion group gave coefficient `2.5205` (`p=3.65e-09`).
- The result is materially stronger than the failed `PLA2G7` product link but remains same-cohort evidence selected after screening; it requires independent cellular validation and prior-art/pharmacology audit.
- `GSE284005` MERFISH panel does not include `TBXAS1`, `ASAH1`, `PLA2G7`, `PTGS1`, or `PTGS2`; that spatial dataset cannot localize this candidate.
- A targeted immune-pseudobulk run in independent `GSE180759` found `TBXAS1` transcript, but only three donors had eligible paired chronic-active versus chronic-inactive lesion-edge immune blocks. Expression was higher in only `1/3` paired donors despite a positive outlier-driven mean delta (`0.3591` log2 CPM+1; Wilcoxon `p=1.0`). This fails the intended immune-cell replication.
- Because thromboxane synthase could instead arise from vascular or other tissue compartments, expanded the check to all author-defined cell compartments rather than silently accepting the immune result. The first expanded run failed computationally because cell types lacking any eligible paired blocks produced an empty table not handled by the summarizer (`KeyError: gene`); fixed that explicit empty-group case and will rerun.

## 2026-05-26T19:09:00+02:00 - Prior-art boundary and matched-state validation decision for `TBXAS1`

- Retrieved the official open full text of Van der Vliet et al., *Nature Neuroscience* (published 21 May 2026, DOI `10.1038/s41593-026-02302-3`). The paper already reports `TBXAS1` in a foamy-microglia lipid-metabolism module and presents `TBXAS1` immunohistochemical staining/quantification in rims of mixed lesions with foamy versus nonfoamy microglia. Therefore `TBXAS1` cannot be claimed as a novel lesion target; only an unreported intervention/stratification proposition could remain novel.
- The expanded `GSE180759` rerun found no coherent immune or vascular replication (`TBXAS1` higher in only `1/3` paired donors for each). Oligodendrocytes showed positive chronic-active versus inactive-edge deltas in `3/3` donors (mean `0.6045` log2 CPM+1, Wilcoxon `p=0.25`), but this is too small and mismatched to the foamy-microglial mechanism for promotion.
- `GSE180759` compares chronic-active to chronic-inactive lesion edges and does not label foamy versus nonfoamy pathological microglial states. It is an important conflict check, but not a matched replication of the source paper's cell-state observation.
- Decision: acquire GEO `GSE301908`, Feng et al.'s independent human snRNA-seq atlas paired to their spatial study, because it provides the relevant foamy microglial states across a larger chronic-active cohort. This is a deliberate reformulation toward the cell-state mechanism rather than substituting an easy but mismatched tissue contrast.
- Initial acquisition of the 1.3 GB `GSE301908_sn_all.rds` object was interrupted after transfer stalled; a 20,971,520-byte partial file remained. Updated the therapeutic downloader to resume a partial download only when the server honors an HTTP byte range and to use a bounded socket timeout. This is a retrieval-mechanics change, not a change in candidate or endpoint.
- The first attempt to install an R runtime also stalled during Homebrew metadata auto-update and was interrupted before installation. It will be retried with auto-update disabled; no analysis is claimed from the uninstalled runtime.

## 2026-05-26T18:38:56+02:00 - Resumption, acquisition route-around, and locked matched-state gate

- This timestamp is taken directly from the resumed host clock; it precedes the last interrupted-session notebook timestamp, so the ordering of these entries rather than their wall-clock difference should be used for provenance.
- Verified Git remained clean at resumed start (`HEAD ba76c80`), so no undocumented analytical edits occurred during interruption.
- The Python range-resume attempt for `GSE301908_sn_all.rds` encountered intermittent DNS-resolution failures. Routed around this by launching a `curl --continue-at -` transfer with retries and low-speed timeout; the partial transfer is retained until it is complete and checksum-manifested. No expression object has been opened.
- Installed Homebrew R `4.6.0` after suppressing the stalled auto-update phase. The installation is an analysis-runtime dependency only; it does not alter candidate selection.
- A direct PubMed E-utilities query for `(TBXAS1 OR thromboxane synthase OR ozagrel) AND multiple sclerosis` initially suffered DNS timeouts, then returned three PubMed identifiers. These are leads for verification, not interpreted citations.
- Locked the `GSE301908` target survival rule before inspecting expression: deposited `Micro2` versus `Micro0` donor-level pseudobulk requires at least eight paired donors with at least 20 nuclei/state, `TBXAS1` mean delta `>0`, positive direction in at least two thirds, paired `dz >= 0.5`, and single-target two-sided paired Wilcoxon `p < 0.05`; deposited state identity must also be supported by at least three of four positive-control markers (`GPNMB`, `APOE`, `LPL`, `SPP1`) directionally higher in `Micro2`.
