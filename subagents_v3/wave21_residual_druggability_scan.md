# Wave21-A Residual Druggability Scan

Date: 2026-05-27

Scope:

- Script: `scripts/v3_wave21_residual_druggability_scan.py`
- Results: `results_v3/wave21_residual_druggability_scan/`

This is gate evidence only. `GO_REVIEW` means "route to hostile novelty and
modality review"; it is not a final therapeutic finding.

## Run

```bash
.venv_v3_py312/bin/python scripts/v3_wave21_residual_druggability_scan.py
```

Inputs combined:

- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
- `tmp_v3/wave13_opentargets_gwas_credible_sets.tsv`
- `results_v3/opentargets_candidate_disease_hits.tsv`
- local ChEMBL/UniProt outputs under `results_v3/druggability/`
- Wave14/Wave19/Wave20 prior exclusion outputs
- ChEMBL target/activity API
- UniProt reviewed-human target API

Outputs written:

- `strict_residual_candidate_pool.tsv`
- `local_integrated_strict_residual_evidence.tsv`
- `api_druggability_evidence.tsv`
- `prior_exclusion_evidence.tsv`
- `wave21_residual_druggability_rank.tsv`
- `summary.json`
- `raw_api/` cache

## Counts

Strict residual candidate pool: 26 genes.

Gate calls:

- `GO_REVIEW`: 1
- `PARK_REVIEW`: 5
- `NO_GO`: 20

Guardrail classes:

- core machinery/stress/structural: 11
- prior exhausted route: 7
- no prior guardrail class: 8

## Top Gate Evidence

| Gene | Call | Evidence | Gate reason |
|---|---|---|---|
| `SQLE` | `GO_REVIEW` | strict residual in Crohn and UC stromal; retained positives in 3 diseases; broad positives in 4 diseases; ChEMBL `CHEMBL3592` with 99 activity records; UniProt `Q14534` enzyme | Route to hostile review only. No local genetics, no perturbation support, no MS anchor, and strict survival is IBD-stromal only. |
| `LDLRAD3` | `PARK_REVIEW` | strict residual in Crohn and UC stromal; retained positives in 3 diseases; UniProt cell-membrane protein | No ChEMBL activity, no genetics, and intervention direction is speculative. |
| `C1QTNF1` | `PARK_REVIEW` | strict residual in Crohn and UC stromal; broad positives in 4 diseases; UniProt secreted protein | Secreted biology is reachable in principle, but agonism versus blockade is unclear and no genetics/MS/non-IBD residual support offsets IBD-only strict survival. |
| `TGM2` | `PARK_REVIEW` | strict residual in UC stromal; broad positives in 3 diseases; ChEMBL `CHEMBL2730` with 807 activity records; UniProt enzyme/extracellular evidence | Enzyme modality exists, but local support is IBD-only strict, with no genetics/MS/non-IBD residual support; close celiac/fibrosis/repair prior art must be hostile-reviewed before any promotion. |
| `REG1A` | `PARK_REVIEW` | strict residual in T1D ductal/endothelial analyses; broad positives in 3 diseases; UniProt secreted protein | Looks like epithelial injury/regeneration readout; no actionable modality or clear direction. |
| `PTPRE` | `PARK_REVIEW` | strict residual in UC stromal; broad positives in 4 diseases; ChEMBL `CHEMBL4850` with 61 activity records; UniProt membrane/cytoplasmic phosphatase | Direction unclear and ChEMBL potency snapshot is weak; no genetics/MS/non-IBD residual support. |

## Demotions

`ATOX1` had strong local residual evidence but failed the modality/direction
gate: intracellular copper chaperone, no ChEMBL target/activity, no genetics,
and no explicit safe autoimmune direction.

Druggable-looking generic or prior-exhausted hits were demoted:

- `CFB`: complement route, already excluded without a new selective delta.
- `CXCL8` and `IL7R`: generic inflammatory/cytokine target classes.
- `TIMP1`, `PDPN`, `COL4A1`, `REG1A`-like signals: stromal, matrix, or repair
  liability/readout concerns.
- `ACSL1` and `ACSL3`: lipid-metabolism route reopened no new direction delta.
- `HIF1A`, `CBX3`, `TPM4`, `SEC61A1`, `SEC61B`, `PPIB`, `RPL17`, `NME1`,
  `MPHOSPH6`, and `PDLIM7`: core machinery/stress/structural markers despite
  occasional ChEMBL target hits.

## Bottom Line

Wave21-A did not produce a final finding. It produced one local/API
gate-positive routing candidate, `SQLE`, and five parked weak candidates.
`SQLE` should be treated as a hostile-review input, not as a therapeutic claim.
The main unresolved blockers are novelty/prior art, perturbation direction,
target-level genetics, MS anchoring, and whether the strict residual signal is
only an IBD-stromal state marker.
