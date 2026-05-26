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
