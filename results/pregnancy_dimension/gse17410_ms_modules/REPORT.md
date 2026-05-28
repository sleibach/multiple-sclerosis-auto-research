# GSE17410 MS Pregnancy Module Screen

Random seed: `20260528`

## Dataset

`GSE17410`: processed Affymetrix PBMC expression data from 8 MS pre-pregnancy
samples and 9 MS ninth-month pregnancy samples. The SOFT family file contains
sample VALUE tables and platform gene symbols, so this Tier 0 screen did not
reprocess CEL files.

## Result

MS month-9 pregnancy does not replicate the seropositive-RA direction observed
in `GSE235508`.

| Module | n pre | n month 9 | delta month9 - pre | Hedges g | Welch p |
|---|---:|---:|---:|---:|---:|
| `mif_cd74_receptor_state` | 8 | 9 | 0.12194807085829851 | 0.6524448023335351 | 0.20974913196132225 |
| `hla_ii_only` | 8 | 9 | 0.10172657772569593 | 0.34479641188020244 | 0.4898578270285561 |
| `ifn_apc` | 8 | 9 | 0.6358630063022481 | 1.0723962239804705 | 0.03686721892111262 |
| `lysosomal_apc` | 8 | 9 | 0.2256790925825065 | 0.8003164431988316 | 0.10817209971275203 |
| `hif_nampt_metabolic` | 8 | 9 | 0.27985942791597296 | 0.9556739592685641 | 0.05686234197712875 |

## Interpretation

This is a constraint on the V4 pregnancy-remission axis. The public MS PBMC
dataset does not show broad suppression of the tested APC/HLA-II modules at
month 9. Instead, the IFN/APC module is higher. This may reflect PBMC
composition, treatment withdrawal/pre-pregnancy sampling, small n, array
platform effects, or pregnancy biology not aligned with peripheral IFN/APC
suppression. It prevents a simple cross-disease claim that pregnancy remission
works by uniformly suppressing the APC/HLA-II module.

## Caveats

- Small n (`8` pre, `9` month 9).
- This is PBMC bulk array, not lesion or single-cell data.
- No relapse-free versus relapsing labels were available in the parsed sample
  metadata for this subset.
- No multiple-testing correction has been applied in this Tier 0 pass.

## Trace

- Script: `scripts/analyze_gse17410_ms_pregnancy_modules.py`
- Metadata: `data/derived/GSE17410/sample_metadata.tsv`
- Raw input: `data/raw/GSE17410/GSE17410_family.soft.gz`
- Outputs:
  - `sample_module_scores.tsv`
  - `module_probe_map.tsv`
  - `month9_vs_pre_contrasts.tsv`
  - `summary.json`
