# Execution Plan

**Locked before expression-data analysis:** 2026-05-26  
**Question:** Is a 4-1BB-linked adaptive immune program associated with lipid-stressed/complement-rich microglial pathology in human chronic active MS lesions?

## Data Accessions

| Dataset | Input planned | Role |
|---|---|---|
| `GSE180759` | `GSE180759_expression_matrix.csv.gz`, `GSE180759_annotation.txt.gz` | Discovery/localization in single nuclei. |
| `GSE279972` | `GSE279972_RAW.tar` plus GEO metadata | Independent validation in bulk lesion tissue. |
| `GSE299939` and Zenodo `10.5281/zenodo.15602185` | Published metadata/source paper only unless a small interoperable table is exposed | Defines mechanistic rationale; not included in statistical evidence for human tissue. |

All downloaded files will be checksummed and listed in a generated manifest. Data will remain uncommitted due to size; code, metadata extracts, results, and checksums will be committed.

## Predeclared Programs

No tested gene will be added or removed because of observed results. If a gene is absent from a platform, it will be reported and omitted from the score denominator.

| Program | Genes | Interpretation |
|---|---|---|
| 4-1BB/adaptive activation (`ADAPT_41BB`) | `TNFRSF9`, `TNFSF9`, `IFNG`, `CCL5`, `NKG7`, `GZMB` | Activated/cytotoxic adaptive-cell and testable costimulation signal; not EBV-specific. |
| B-cell/APC support (`B_APC`) | `CD79A`, `MS4A1`, `CD74`, `HLA-DRA`, `HLA-DPA1`, `HLA-DPB1` | B-cell/antigen-presentation environment compatible with the upstream model. |
| Lipid/complement microglial pathology (`MIMS_LIPID_COMP`) | `GPNMB`, `APOE`, `LPL`, `TREM2`, `SPP1`, `C1QA`, `C1QB`, `C1QC`, `CD68`, `CTSB` | Lesion-associated microglial lipid handling and complement program. |

Individual `TNFSF9` and `TNFRSF9` results are targeted readouts. Module associations are the main tests because single-gene dropout is severe in single-nucleus data.

## Analysis 1: Cell-Resolved Discovery (`GSE180759`)

1. Download processed expression and annotation files from GEO; record SHA-256 hashes.
2. Inspect metadata structure and map authors' cell-type and tissue-stage labels without re-clustering.
3. Normalize raw counts, if counts are supplied, by pseudobulk aggregation within `sample x broad-cell-type`, then counts per million with `log2(CPM + 1)`. If data are already normalized, document the supplied scale and do not renormalize.
4. Determine whether B/plasma and T-cell populations have sufficient nuclei for pseudobulk inference: minimum `20` nuclei per sample-cell-type. If not, report failure for cell-specific costimulation localization rather than pooling in a misleading way.
5. Primary discovery test: within tissue blocks that contain eligible immune and microglial populations, test whether the `ADAPT_41BB` immune-cell score is positively associated with the microglial `MIMS_LIPID_COMP` score using Spearman correlation and donor-block bootstrap confidence intervals.
6. Localization tests: compare `TNFRSF9` and `ADAPT_41BB` in T/lymphocyte pseudobulks, and `MIMS_LIPID_COMP` in microglia, between chronic active edges and non-active/control regions using donor-aware permutation or paired testing where metadata permits.

## Analysis 2: Independent Validation (`GSE279972`)

1. Extract bulk expression and clinical/lesion metadata from the GEO archive/records.
2. Normalize bulk counts by `log2(CPM + 1)` unless supplied data are explicitly normalized.
3. Primary replication test: among MS tissue samples, compute Spearman correlation between `ADAPT_41BB` and `MIMS_LIPID_COMP`; assess significance by permutation at the donor level when multiple tissue blocks per donor are present.
4. Secondary test: correlation of `B_APC` with `MIMS_LIPID_COMP` and mediation-compatible co-occurrence of `B_APC`, `ADAPT_41BB`, and `MIMS_LIPID_COMP`. This remains association, not mediation or causal inference.
5. Where lesion labels permit, compare module scores in foamy-microglia/high-inflammatory lesion classes versus control or non-foamy tissue using donor-aware tests.

## Statistics and Calling Rules

- Random seed: `20260526`.
- Primary family: association of `ADAPT_41BB` with `MIMS_LIPID_COMP` in the discovery and validation datasets.
- Secondary family: `B_APC` associations, individual `TNFRSF9`/`TNFSF9` localization, and group contrasts.
- Multiple testing: Benjamini-Hochberg correction within the primary/secondary result table; a result is called statistically supported only at `FDR < 0.05`.
- Effect-size requirement for a positive finding:
  - primary association direction concordant in both datasets;
  - `Spearman rho >= 0.40` in validation or a clearly specified donor-aware standardized group difference `|d| >= 0.8`;
  - `FDR < 0.05` for the validation primary test.
- A result meeting direction/effect size but not FDR will be labelled exploratory signal, not a finding.
- A negative result is informative if the validation confidence interval excludes `rho >= 0.40`, or if neither dataset has sufficient eligible cells/samples to test the predicted relationship.

## Confounders and Sensitivity Analyses

- **Pseudoreplication:** do not treat cells as independent biological replicates; use sample/donor pseudobulks.
- **Tissue composition:** bulk association may reflect more immune cells rather than per-cell activation; interpret alongside cell-resolved discovery and report this limitation.
- **Batch/dataset differences:** do not directly merge datasets; require directional replication.
- **Cell rarity/dropout:** require minimum nuclei and report detected-gene coverage.
- **Lesion classification:** use deposited annotations only; no post hoc relabelling.
- **Published-signature circularity:** MIMS genes overlap known lesion biology; novelty can concern association with the pre-specified 4-1BB adaptive program, not rediscovery of MIMS.

## Decision Points

1. If `GSE180759` annotations cannot support eligible immune-to-microglia sample matching, use it only for qualitative localization and make `GSE279972` the quantitative analysis, stating the downscope.
2. If `GSE279972` lacks lesion or donor metadata needed for donor-aware inference, use a sample-level exploratory analysis only and do not claim a supported finding.
3. If the predeclared axis fails, do not search broadly for a substitute successful pathway; report the negative result.
4. If the data expose an interpretation error or normalization anomaly, stop the claim, investigate, and log it.

## Novelty Search Plan

After results are produced, search PubMed, Google Scholar, bioRxiv, and full-text sources (Europe PMC/PMC or journal full text) using queries combining:

- `"TNFSF9" OR "TNFRSF9" OR "4-1BB" OR "CD137"` with `"chronic active" "multiple sclerosis" lesion microglia`;
- `"Epstein-Barr" "4-1BBL" "chronic active" multiple sclerosis`;
- `"foamy microglia" "TNFRSF9" multiple sclerosis`;
- `"T-bet+ CXCR3+ B cells" "4-1BB" multiple sclerosis`.

If direct publication of the same tissue/program association is found, the output will be framed as replication or the claim narrowed to an unreported analysis if defensible.

## Locked Novelty Addendum Before Expression Testing

**Added 2026-05-26 after metadata inspection and full-text novelty screening, before any target-gene expression was queried.**

Van der Vliet et al. (*Nature Neuroscience*, published 2026-05-21; DOI `10.1038/s41593-026-02302-3`) directly report adaptive immune/B-cell (`CD79A`, `CCL5`, `IGHG1`) and lipid/lysosomal microglial modules in the `GSE279972` source cohort. Therefore:

- The predeclared `ADAPT_41BB` to `MIMS_LIPID_COMP` module test will still be run, but it is a reproducibility/positive-control test rather than a novel claim because `CCL5` overlaps the published adaptive module.
- The focused, potentially unreported target analysis is `TNFRSF9` and `TNFSF9`, individually and as a two-gene `COSTIM_41BB` score, in foamy versus non-foamy lesion specimens and in relation to `MIMS_LIPID_COMP`.
- This addendum narrows claims; it does not substitute new genes after observing expression values. `TNFRSF9` and `TNFSF9` were already specified as targeted readouts in the original locked plan.

## Reproducibility Outputs

- `scripts/download_data.py`: deterministic retrieval and hashing.
- `scripts/analyze.py`: preprocessing, scoring, statistics, plots/tables.
- `run_analysis.sh`: documented end-to-end entry point.
- `environment/requirements.txt`: pinned Python packages.
- `data/derived/data_manifest.tsv`: accessions, URLs, hashes.
- `results/`: machine-readable result tables and figures.
- `LAB_NOTEBOOK.md`: timestamped decision and failure log.
- `FINDING.md`: final claim, evidence, novelty, falsification, and scope.
