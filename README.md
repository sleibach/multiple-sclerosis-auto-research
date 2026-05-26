# MS Lesion Circuit Execution

This repository executes a constrained computational follow-up of the EBV-to-chronic-active-lesion research log. It tests whether a 4-1BB-linked adaptive costimulation transcript score (`TNFRSF9`/`TNFSF9`) tracks a lipid/complement microglial program in public human MS white-matter data.

## Run

From the repository root:

```bash
./run_analysis.sh
```

The entry point creates `.venv`, installs `environment/requirements.lock.txt`, downloads public inputs, records SHA-256 hashes, and executes `scripts/analyze.py`. Runtime on the development machine is approximately several minutes because `GSE180759` is streamed from a dense single-nucleus matrix.

Random seed: `20260526`.

## Data

| Accession | Purpose |
|---|---|
| `GSE180759` | Cell-resolved chronic active lesion localization/downscope assessment. |
| `GSE279972` | Quantitative bulk white-matter MS validation/test cohort. |
| Zenodo record `10.5281/zenodo.19352263` | Author-deposited donor and foamy/non-foamy morphology metadata for `GSE279972`. |

Raw public files are downloaded into `data/raw/` and ignored by Git. Their expected URLs, sizes, and hashes are in `data/derived/data_manifest.tsv`.

## Outputs

| File | Description |
|---|---|
| `results/validation_statistics.tsv` | Primary and secondary statistical tests. |
| `results/validation_sensitivity_models.tsv` | Confounder-adjusted focused sensitivity models. |
| `results/validation_leave_one_donor_out.tsv` | Influence analysis for the foamy-lesion side observation. |
| `results/validation_paired_donors.tsv` | Within-donor paired comparison where both morphologies exist. |
| `results/discovery_paired_eligible_blocks.tsv` | Sparse eligible cell-resolved blocks from `GSE180759`. |
| `results/falsification_power.tsv` | Reproducible power calculation for the proposed paired spatial follow-up. |
| `results/run_summary.json` | Machine-readable analysis summary. |
| `FINDING.md` | Scientific interpretation, novelty, falsification path, and scope. |

The analysis does not infer EBV infection or causal therapeutic effects; neither is measured in the selected human tissue datasets.
