# Wave111 GPR183 Spatial-Proxy Forcing Test

## Bottom Line

Branch call: `NO_REOPEN_GPR183_SPATIAL_PROXY`.

This test uses matched-donor compartment data as a spatial proxy. It requires
non-myeloid oxysterol-ligand-axis signal to predict myeloid/APC `GPR183`, and
then predict response modules after receptor adjustment, without parallel
control-module positives.

## Disease-Collapsed Summary

_No summary rows._

## Top Tests

_No tests._

## Decision Rule

Promotion to a deeper GPR183 branch would require coherent specific contexts in
at least two diseases. A coherent context needs FDR10 ligand-to-receptor support
and FDR10 response support, with zero FDR10 control-module support.

## Reproducibility

- Script: `scripts/v3_wave111_gpr183_spatial_proxy_forcing_test.py`
- Donor gene scores: `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_donor_scores.tsv`
- Donor module scores: `results_v3/direct_h5ad_cell_state/direct_h5ad_donor_module_scores.tsv`
- Pair output: `results_v3/wave111_gpr183_spatial_proxy_forcing_test/gpr183_spatial_proxy_pairs.tsv`
- Test output: `results_v3/wave111_gpr183_spatial_proxy_forcing_test/gpr183_spatial_proxy_tests.tsv`
- Summary output: `results_v3/wave111_gpr183_spatial_proxy_forcing_test/gpr183_spatial_proxy_summary.tsv`
- Seed: `20260527`
