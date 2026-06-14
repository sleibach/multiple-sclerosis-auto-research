# V49 Queue: Repository Hygiene + Convergence/Contradiction Content

Status: active. This queue tracks summed active session intervals, not calendar
span across resume gaps.

## Timing

- block_start_utc: `2026-06-14T19:57:24Z`
- active_target_seconds: `21600`
- active_target_hours: `6`
- active_time_rule: sum completed session intervals plus current open interval;
  exclude idle/resume gaps.

| session | start_utc | end_utc | active_seconds | note |
|---:|---|---|---:|---|
| 1 | `2026-06-14T19:57:24Z` | OPEN | OPEN | initial V49 session |

## Phase 0 Oversized-File Audit

Phase 0 is mandatory before research work. The first tracked-file audit found
six tracked files above `50 MiB`; three are GitHub hard blockers above
`100 MiB`.

| path | size_bytes | size_mib | status | disposition |
|---|---:|---:|---|---|
| `phases/v3/tmp/foundation_wave6/geneformer_assets/Geneformer-V2-104M/model.safetensors` | 417571156 | 398.2 | tracked; hard blocker | disposable downloaded Geneformer model weight under `tmp`; purge from history |
| `phases/v3/tmp/cellstate_subagent/ibd_natcomm.h5ad` | 183686537 | 175.2 | tracked; hard blocker | disposable cached cell-state dataset under `tmp`; purge from history |
| `phases/v3/tmp/cellstate_subagent/psoriasis_adult.h5ad` | 174736215 | 166.6 | tracked; hard blocker | disposable cached cell-state dataset under `tmp`; purge from history |
| `phases/v3/results/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv` | 101135644 | 96.5 | tracked; above V49 50 MiB ceiling | generated V3 broad H5AD contrast table; reproducible from scripts/results provenance, purge from history and keep references as provenance only |
| `phases/v3/tmp/gwascatalog_associations_20260317_convert.parquet` | 68633383 | 65.5 | tracked; above V49 50 MiB ceiling | disposable converted GWAS Catalog cache under `tmp`; purge from history |
| `analysis/v43_method_validation/synthetic/power_simulation_subjects.tsv.gz` | 55936861 | 53.3 | tracked; above V49 50 MiB ceiling | seeded synthetic subject-level simulation cache; method-characterization data, reproducible from committed simulation code, purge from history and retain summary artifacts |

Large files on disk under `.venv*`, `data/raw*`, and ignored raw-data trees are
not part of the tracked purge unless `git ls-files` shows them as tracked. The
tracked purge target is:

- `phases/v3/tmp/`
- `phases/v3/results/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `analysis/v43_method_validation/synthetic/power_simulation_subjects.tsv.gz`

## Required Checks

- OpenGWAS: PASS at session start. JWT valid until `2026-06-19 12:28 UTC`;
  renew soon. Access check used POST-only endpoints and returned HTTP 200.
- SAP AI Core: pending V49 health check after Phase 0.
- V47 provenance gate: pending after Phase 0.
- Oversized tracked-file check: pending history rewrite.

## Backlog

| id | priority | status | task | artifact |
|---:|---|---|---|---|
| 1 | high | in-progress | Phase 0: purge tracked large tmp/cache/generated files from history and prevent recurrence | `.gitignore`, `meta/V49_QUEUE.md` |
| 2 | high | todo | Verify no tracked file remains above 50 MiB and no filesystem file above 100 MiB remains under tracked paths | `meta/V49_QUEUE.md` |
| 3 | high | todo | Run OpenGWAS, SAP AI Core, provenance gate, and external Markdown health checks after history rewrite | `meta/V49_QUEUE.md` |
| 4 | high | todo | Close high-priority convergence/contradiction gap rows for bounded APC/HLA-II monitoring | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md` |
| 5 | high | todo | Close high-priority convergence/contradiction gap rows for MS-UC backdrop | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md` |
| 6 | high | todo | Close remaining high-priority V48 gap rows with asserted relationship or insufficient-overlap closure | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md` |
| 7 | medium | todo | Refresh decision-relevant convergence list after gap closure | `knowledge_external/synthesis/DECISION_RELEVANT_CONVERGENCES_V48.md` |
| 8 | medium | todo | Refresh future-grounding queue from any contradiction or external-verifiable closures | `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md` |
| 9 | medium | todo | Refresh comparator matrix only where V49 content reveals concrete source-coverage changes | `knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md` |
| 10 | medium | todo | Rebuild public external index, governance preflight, provenance gate, and grounded TF-IDF after content updates | `knowledge_external/INDEX.md`, `knowledge/.index/` |

## Iteration Notes

### Iteration 1

- Started V49 at `2026-06-14T19:57:24Z`; target active runtime is `21600`
  seconds.
- OpenGWAS check: PASS with JWT valid until `2026-06-19 12:28 UTC`; renew soon.
- Identified tracked oversized files above `50 MiB` and separated them from
  untracked ignored raw-data/virtualenv files on disk.
- Confirmed `git-filter-repo` is available at `/opt/homebrew/bin/git-filter-repo`.
- Added `.gitignore` rules for tmp/cache paths and the two reproducible generated
  non-tmp outputs that exceed the V49 size ceiling.
