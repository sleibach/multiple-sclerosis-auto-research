# Wave 5 Local Quant Report: OSM/OSMR and C1q/Complement

Timestamp: 2026-05-26 22:16:54 UTC.

## Scope

I added a narrow local quantification layer for two candidate axes:

- `OSM_OSMR`: `osm_ligand_inflammatory`, `osmr_receptor_response`, `osm_osmr_core`.
- `C1Q_COMPLEMENT`: `c1q_core`, `c1q_phagolysosomal`.

The script scores donor/sample-level data in the existing direct h5ad configurations and GSE111972, then applies one-at-a-time residual controls against `ifn_apc`, `inflammatory_nfkb`, `hif_nampt_metabolic`, `lipid_loader_repair`, and `lysosomal_apc`.

## Changed Files

- Added `scripts/v3_wave5_quant_osmr_complement.py`.
- Updated `run_v3_analysis.sh` to run `scripts/v3_wave5_quant_osmr_complement.py` after direct h5ad scoring.
- Added outputs under `results_v3/wave5_local_quant/`.
- Added this report: `subagents_v3/wave5_local_quant_report.md`.

## Commands Run

```bash
./.venv_v3_py312/bin/python scripts/v3_wave5_quant_osmr_complement.py
./.venv_v3_py312/bin/python -m py_compile scripts/v3_wave5_quant_osmr_complement.py
bash -n run_v3_analysis.sh
```

The final script run completed with:

```json
{
  "axis_support_counts_after_basic_residual_controls": {
    "C1Q_COMPLEMENT": 0,
    "OSM_OSMR": 3
  },
  "go_axes": ["OSM_OSMR"],
  "go_no_go": "GO",
  "n_raw_contrasts": 125,
  "n_residual_tests": 350
}
```

## Outputs

- `results_v3/wave5_local_quant/wave5_donor_sample_axis_scores.tsv`: donor/sample axis and covariate scores.
- `results_v3/wave5_local_quant/wave5_module_gene_presence.tsv`: per-analysis gene coverage.
- `results_v3/wave5_local_quant/wave5_raw_axis_contrasts.tsv`: raw case-control contrasts.
- `results_v3/wave5_local_quant/wave5_residual_axis_tests.tsv`: one-covariate residual tests.
- `results_v3/wave5_local_quant/wave5_axis_go_no_go.tsv`: disease-level go/no-go table.
- `results_v3/wave5_local_quant/wave5_local_quant_summary.json`: compact summary.

## Result

`OSM_OSMR` passes the local continuation rule in three diseases:

- Crohn disease, colon epithelial, `osm_osmr_core`: raw delta `0.165`, raw p `3.02e-05`; residual deltas stayed positive across all 5 covariates; 4/5 residual tests nominally positive; 1/5 residual FDR < 0.10; median residual Hedges g `1.41`.
- Ulcerative colitis, colon epithelial, `osm_osmr_core`: raw delta `0.155`, raw p `0.00144`; residual deltas stayed positive across all 5 covariates; 3/5 residual tests nominally positive; 2/5 residual FDR < 0.10; median residual Hedges g `1.12`.
- Type 1 diabetes, pancreatic ductal cell, `osmr_receptor_response`: raw delta `0.368`, raw p `0.0281`; residual deltas stayed positive across all 5 covariates; 3/5 residual tests nominally positive; 0/5 residual FDR < 0.10; median residual Hedges g `1.20`.

Important limitation: this is a continuation signal, not a therapeutic claim. MS GSE111972 microglia, psoriasis, and Sjögren did not pass. The OSM/OSMR signal is currently strongest in epithelial/barrier or ductal target-cell compartments, not in the MS microglia dataset used here.

`C1Q_COMPLEMENT` is no-go in this local test. It had zero diseases passing residual controls, and several plausible myeloid/microglia compartments were directionally negative, including UC myeloid `c1q_core` raw delta `-0.471`, p `0.0189`, and MS white-matter microglia `c1q_core` raw delta `-0.867`, p `0.0299`.

## Go / No-Go

Go for a narrow OSM/OSMR follow-up focused on tissue target-cell response in Crohn/UC/T1D-like epithelial or ductal compartments. No-go for C1q/complement as the Wave 5 central cross-autoimmune axis.

Pivot criterion result: because `OSM_OSMR` reaches three diseases with compartment-plausible, direction-stable residual support by the local rule, I do not recommend a new broad pivot before hour 6. I do recommend treating MS support as absent until tested in spatial lesion data containing OSMR-responsive astrocyte, oligodendrocyte-lineage, endothelial, or stromal compartments.
