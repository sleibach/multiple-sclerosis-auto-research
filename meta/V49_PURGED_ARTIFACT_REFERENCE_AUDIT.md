# V49 Purged Artifact Reference Audit

Status: operational audit after V49 history rewrite. This file documents
remaining references to paths removed from Git history, separating historical
provenance references from live rerun dependencies.

## Verdict

The purge did not leave any tracked copy of the removed large payloads. It did
leave many intentional references in old V3 reports, summaries, manifests, and
scripts. Those references are not push blockers. They mean that some historical
V3 scripts are no longer directly rerunnable from Git alone until their
disposable caches or generated tables are regenerated from source.

No old grounded result was rewritten for content. The audit boundary is:
preserve historical references, document runtime consequences, and prevent the
large payloads from returning to Git.

## Checks Run

Commands:

```bash
git ls-files | rg "^phases/v3/tmp/|^tmp_v3/|broad_h5ad_gene_contrasts\\.tsv$|power_simulation_subjects\\.tsv\\.gz$|gwascatalog_associations_20260317_convert\\.parquet$|ibd_natcomm\\.h5ad$|psoriasis_adult\\.h5ad$|model\\.safetensors$" || true
rg -l "phases/v3/tmp|tmp_v3|broad_h5ad_gene_contrasts\\.tsv|power_simulation_subjects\\.tsv\\.gz|results_v3/broad_h5ad_gene_discovery|Geneformer-V2-104M|ibd_natcomm\\.h5ad|psoriasis_adult\\.h5ad|gwascatalog_associations_20260317_convert\\.parquet" .
```

Results:

| check | result |
|---|---:|
| tracked files matching purged payload/path patterns | `0` |
| exact purged payload paths present on disk | `0` |
| tracked files above `50 MiB` | `0` |
| files with remaining textual references to purged/touched path patterns | `181` |
| referenced files under `scripts/` | `52` |
| referenced files under historical V3 result directories | `75` |
| referenced files under historical V3 subagent reports | `42` |
| referenced files under `docs/` | `6` |
| referenced files under `meta/` | `5` |
| referenced files under `data/` | `1` |

## Exact Payload Status

| path | current status | interpretation |
|---|---|---|
| `phases/v3/tmp/foundation_wave6/geneformer_assets/Geneformer-V2-104M/model.safetensors` | missing | Purged disposable downloaded model weight. Regenerate/download outside Git if a V3 Geneformer rerun is required. |
| `phases/v3/tmp/cellstate_subagent/ibd_natcomm.h5ad` | missing | Purged disposable cached AnnData. Regenerate/download outside Git if needed. |
| `phases/v3/tmp/cellstate_subagent/psoriasis_adult.h5ad` | missing | Purged disposable cached AnnData. Regenerate/download outside Git if needed. |
| `phases/v3/tmp/gwascatalog_associations_20260317_convert.parquet` | missing | Purged disposable GWAS Catalog conversion cache. Regenerate outside Git if needed. |
| `phases/v3/results/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv` | missing | Purged large generated broad H5AD contrast table. Regenerate from `scripts/v3_broad_h5ad_gene_discovery.py` and source data if a V3 rerun needs it. |
| `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv` | missing | Legacy pre-restructure path for the same generated contrast table. |
| `analysis/v43_method_validation/synthetic/power_simulation_subjects.tsv.gz` | missing | Purged seeded synthetic subject-level cache. Regenerate from `scripts/v43_method_validation_simulations.py`; summary/docs remain. |

## Ignore-Rule Verification

Checked representative purged payload paths with `git check-ignore -v` after
the V49 ignore rules were tightened. All representative paths are now ignored:

| path | ignore rule |
|---|---|
| `phases/v3/tmp/foundation_wave6/geneformer_assets/Geneformer-V2-104M/model.safetensors` | `.gitignore:24:**/tmp/` |
| `phases/v3/tmp/cellstate_subagent/ibd_natcomm.h5ad` | `.gitignore:24:**/tmp/` |
| `phases/v3/tmp/cellstate_subagent/psoriasis_adult.h5ad` | `.gitignore:24:**/tmp/` |
| `phases/v3/tmp/gwascatalog_associations_20260317_convert.parquet` | `.gitignore:24:**/tmp/` |
| `phases/v3/results/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv` | `.gitignore:32:phases/v3/results/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv` |
| `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv` | `.gitignore:33:results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv` |
| `analysis/v43_method_validation/synthetic/power_simulation_subjects.tsv.gz` | `.gitignore:34:analysis/v43_method_validation/synthetic/power_simulation_subjects.tsv.gz` |

The legacy `results_v3/` broad-H5AD contrast path was not covered by the first
V49 ignore rule set; task 45 added the explicit rule shown above.

## Final Ignore-Rule Recheck

Rechecked at `2026-06-14T22:08:58Z` after the final handoff refresh. All
representative recurrence-risk paths still resolve to an ignore rule:

| path | ignore rule |
|---|---|
| `phases/v3/tmp/foundation_wave6/geneformer_assets/Geneformer-V2-104M/model.safetensors` | `.gitignore:24:**/tmp/` |
| `phases/v9/tmp/cache/example.h5ad` | `.gitignore:24:**/tmp/` |
| `phases/v9/tmp/cache/gwascatalog_associations.parquet` | `.gitignore:24:**/tmp/` |
| `analysis/v43_method_validation/synthetic/power_simulation_subjects.tsv.gz` | `.gitignore:34:analysis/v43_method_validation/synthetic/power_simulation_subjects.tsv.gz` |
| `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv` | `.gitignore:33:results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv` |
| `tmp_v3/any/cache.parquet` | `.gitignore:20:tmp_v3/` |

## Timeout-Resume Recurrence Recheck

Rechecked at `2026-06-20T08:27:59Z` after the timeout-resume V49 commits. The
repository still blocks representative temp/cache recurrence paths:

| representative path | ignore rule |
|---|---|
| `phases/v3/tmp/example.safetensors` | `.gitignore:24:**/tmp/` |
| `tmp/foo.h5ad` | `.gitignore:24:**/tmp/` |
| `phases/v9/tmp/cache.parquet` | `.gitignore:24:**/tmp/` |
| `phases/v3/tmp/cache.tsv.gz` | `.gitignore:24:**/tmp/` |
| `analysis/example/tmp/cache.parquet` | `.gitignore:24:**/tmp/` |

Tracked recurrence-pattern check:

| check | result |
|---|---:|
| tracked files under any `tmp/` path | `0` |
| tracked `.safetensors`, `.h5ad`, or `.parquet` files | `0` |
| tracked `.tsv.gz` files matching the broad recurrence pattern | `5` |
| tracked `.tsv.gz` files above `50 MiB` | `0` |

The five tracked `.tsv.gz` files are compact seeded synthetic method-validation
artifacts outside temp/cache paths. Sizes at this recheck ranged from `45,216`
bytes to `23,904,581` bytes, below the V49 `50 MiB` tracking ceiling. They are
not the purged `analysis/v43_method_validation/synthetic/power_simulation_subjects.tsv.gz`
cache and are not GitHub push blockers.

## Reference Classes

### Historical provenance references

Old V3 result summaries, lab notebooks, subagent reports, and repository
inventories still name the original paths because those files describe what was
used at the time. These references should remain unless a future migration
explicitly rewrites historical provenance, which V49 did not do.

Examples:

- `docs/resources/DATA_V3.md`
- `docs/lab_notebooks/LAB_NOTEBOOK_V3.md`
- `docs/orchestration/ORCHESTRATION_LOG_V3.md`
- `phases/v3/results/**/summary.json`
- `phases/v3/subagents/*.md`
- `meta/REPO_INVENTORY_PRE.md`
- `meta/REPO_INVENTORY_POST.md`

### Live rerun dependencies

The `52` matching files under `scripts/` are runtime dependencies for
historical V3 reruns, not current V49 content. They now require regenerated or
downloaded local caches before execution. This is expected after purging
disposable cache/history payloads.

Scripts in this class include V3 broad-H5AD consumers, V3 Geneformer wrappers,
Open Targets/GWAS Catalog cache consumers, and the V43 method-validation
simulator that can regenerate the removed synthetic subject cache.

### Data manifest references

`data/derived_v3/state_parse_split4_manifest.tsv` records source URLs and the
temporary local filenames originally used for State/Parse assets. It is a
manifest/provenance record, not a tracked payload.

## Operational Consequence

The repository is now push-safe with respect to GitHub's large-file limit, but a
subset of historical V3 scripts is no longer self-contained from Git alone.
Future reruns should:

1. Regenerate or download disposable cache inputs outside tracked Git paths.
2. Keep those regenerated payloads under ignored cache directories.
3. Re-run the relevant script from source.
4. Commit only compact summaries or tables that stay below the V49 size
   ceiling.

Do not re-add `phases/*/tmp/`, `tmp_v3/`, large model weights, large AnnData
caches, large parquet caches, or the subject-level V43 synthetic cache to Git.
