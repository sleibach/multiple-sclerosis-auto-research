# V36 Branch Cross-Exam Availability Audit

Iteration start UTC: `2026-06-07T20:12:38Z`.

Question: after Claude proposed cross-drug pathway classifiers and GSEA, which
named datasets are already held locally?

## Local Search

Command families:

- `rg` across repository text for `GSE19285`, `GSE126480`, `GSE97779`,
  `GSE73721`, `GSE33377`, `GSE15573`, and already-used treatment cohorts.
- `find data analysis phases` for matching local data/artifact paths.

## Held Locally

| Accession / artifact | Local status | Relevant path(s) | Usefulness |
|---|---|---|---|
| `GSE235357` | held | `data/raw_v3/wave96_ms_treatment/GSE235357_normalized_annotated.csv.gz` | MS DMF locked-rule support; already audited in V36. |
| `GSE250453` | held | `data/raw_v3/wave96_ms_treatment/GSE250453_fingo_RNAseq_all.tsv.gz` | MS fingolimod negative/weak comparator; already audited in V36. |
| `GSE85034` | held | `data/raw_v3/wave89_psoriasis_response/GSE85034_series_matrix.txt.gz` | Psoriasis ADA/MTX stress tests; already audited in V36. |
| `GSE253006` | held | `data/raw_v3/gse253006/GSE253006_RAW.tar` | UC tofacitinib exact single-cell artifact; already audited in V36. |
| `GSE24427` | held | `data/raw/GSE24427/GSE24427_family.soft.gz` | MS IFN-beta longitudinal branch audit; already audited in V36. |
| `GSE138064` | held | `data/raw/GSE138064/GSE138064_family.soft.gz` | MS IFN-beta dose/hour branch audit; already audited in V36. |
| `GSE97779` | held as RA artifact | `data/raw_v2/GSE97779_series_matrix.txt.gz` | RA macrophage artifact; not a clean treatment-response branch validation cohort. |

## Not Held as Usable Local Treatment-Response Cohorts

| Model-named dataset | Local result | Implication |
|---|---|---|
| `GSE19285` | mentioned in old scout text only; no local data path found | acquisition needed before classifier/GSEA proposal can run. |
| `GSE126480` | no local data path found | acquisition needed. |
| `GSE73721` | no local data path found | acquisition needed. |
| `GSE33377` | mentioned in old RA validation scout only; no local data path found | acquisition needed, plus response-label mapping. |
| `GSE15573` | no local data path found | acquisition needed. |

## Verdict

The model-proposed cross-drug classifier/GSEA tests are not immediately
executable as written. The held local substitutes are exactly the cohorts V36
already audited: MS DMF/fingolimod, UC tofacitinib, psoriasis ADA/MTX, and MS
IFN-beta `GSE24427`/`GSE138064`. A true cross-drug classifier/GSEA pass should
be treated as a future data-acquisition workstream, not as an unrun in-hand
analysis.
