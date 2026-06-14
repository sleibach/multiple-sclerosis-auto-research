# V49 Binary/Compressed Extension Audit

Status: operational repository hygiene check. This audits tracked files with
extensions that could become large-cache risks after the V49 purge.

Checked at `2026-06-14T21:45:12Z`.

## Summary

| extension | tracked count | policy result |
|---|---:|---|
| `.safetensors` | `0` | PASS; model weights are not tracked. |
| `.h5ad` | `0` | PASS; AnnData caches are not tracked. |
| `.parquet` | `0` | PASS; parquet caches are not tracked. |
| `.tsv.gz` | `5` | PASS with review; all are compact seeded synthetic method-characterization artifacts below `50 MiB`, not tmp/cache payloads. |

## Tracked `.tsv.gz` Files

| path | size_bytes | size_mib | status |
|---|---:|---:|---|
| `analysis/v45_tb_compartment_pathology/synthetic/tb_compartment_pathology_subjects.tsv.gz` | `23904581` | `22.8` | Retain; seeded synthetic method-characterization artifact below V49 size ceiling. |
| `analysis/v45_multiconfounder_batch_guard/synthetic/multiconfounder_subjects.tsv.gz` | `20984752` | `20.0` | Retain; seeded synthetic method-characterization artifact below V49 size ceiling. |
| `analysis/v45_postpartum_pathology/synthetic/postpartum_pathology_subjects.tsv.gz` | `20201403` | `19.3` | Retain; seeded synthetic method-characterization artifact below V49 size ceiling. |
| `analysis/v43_method_validation/synthetic/robustness_simulation_subjects.tsv.gz` | `8815119` | `8.4` | Retain; seeded synthetic method-characterization artifact below V49 size ceiling. |
| `analysis/v43_method_validation/synthetic/pipeline_null_replicates.tsv.gz` | `45216` | `0.0` | Retain; compact seeded synthetic-null replicate summary. |

## Policy Boundary

The V49 ignore rules intentionally block `*.tsv.gz` under tmp/cache paths and
the purged V43 subject-level power cache, not every compressed TSV globally.
These five retained files are already tracked, below `50 MiB`, and part of
method-behavior reproducibility. They remain synthetic-only and must not be
reported as biological evidence.

If any retained compressed TSV grows above `50 MiB`, move it to ignored
regenerable cache status and preserve only compact summaries.

