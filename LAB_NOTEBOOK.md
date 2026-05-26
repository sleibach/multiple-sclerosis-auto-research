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
