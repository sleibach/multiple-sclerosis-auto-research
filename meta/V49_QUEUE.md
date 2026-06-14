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
| 1 | `2026-06-14T19:57:24Z` | `2026-06-14T20:03:40Z` | 376 | initial V49 session through Phase 0 health checks |
| 2 | `2026-06-14T20:16:32Z` | OPEN | OPEN | resumed content-gap closure session |

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
- SAP AI Core: PASS after Phase 0 for Claude (`def854013c7ac379` via
  `--model claude`), Gemini (`gemini-2.5-pro`), and RPT (`sap-rpt-1-large`).
- V47 provenance gate: PASS after Phase 0 (`359` checks, `39` external JSON
  records, `0` failures).
- Oversized tracked-file check: PASS after Phase 0 (`0` tracked files above
  `50 MiB`; `0` Git blobs above `50 MiB`).

## Backlog

| id | priority | status | task | artifact |
|---:|---|---|---|---|
| 1 | high | done | Phase 0: purge tracked large tmp/cache/generated files from history and prevent recurrence | `.gitignore`, `meta/V49_QUEUE.md` |
| 2 | high | done | Verify no tracked file remains above 50 MiB and no filesystem file above 100 MiB remains under tracked paths | `meta/V49_QUEUE.md` |
| 3 | high | done | Run OpenGWAS, SAP AI Core, provenance gate, and external Markdown health checks after history rewrite | `meta/V49_QUEUE.md` |
| 4 | high | done | Close high-priority convergence/contradiction gap rows for bounded APC/HLA-II monitoring | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md` |
| 5 | high | done | Close high-priority convergence/contradiction gap rows for MS-UC backdrop | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md` |
| 6 | high | done | Close remaining high-priority V48 gap rows with asserted relationship or insufficient-overlap closure | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V48.md` |
| 7 | medium | done | Refresh decision-relevant convergence list after gap closure | `knowledge_external/synthesis/DECISION_RELEVANT_CONVERGENCES_V48.md` |
| 8 | medium | done | Refresh future-grounding queue from any contradiction or groundable external closures | `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V48.md` |
| 9 | medium | done | Refresh comparator matrix only where V49 content reveals concrete source-coverage changes | no resource-record changes; no comparator refresh required |
| 10 | medium | done | Rebuild public external index, governance preflight, provenance gate, and grounded TF-IDF after content updates | `knowledge_external/INDEX.md`, `knowledge/.index/` |
| 11 | high | done | Review the 16 insufficient-overlap rows and rank which future tests are genuinely groundable versus context-only | `knowledge_external/synthesis/V49_INSUFFICIENT_OVERLAP_TRIAGE.md` |
| 12 | high | done | Inspect the 9 remaining medium uncovered V37 findings and decide whether direct-source intake is warranted or would risk false corroboration | `knowledge_external/synthesis/V49_UNCOVERED_FINDING_TRIAGE.md` |
| 13 | medium | done | Add source-terms metadata or review notes for the 8 V49-added records where a quick conservative source-terms classification is possible | `knowledge_external/catalogs/indexes/SOURCE_TERMS_COVERAGE_V48.md` |
| 14 | medium | done | Build a concise V49 relationship-delta note for the medical-team reader: what was newly corroborated, what stayed insufficient-overlap, and what contradictions remain absent | `knowledge_external/synthesis/V49_RELATIONSHIP_DELTA_NOTE.md` |
| 15 | medium | done | Run a source-domain review of the newly added sources and decide whether any require access/terms parking before future reuse | `knowledge_external/catalogs/indexes/V49_NEW_SOURCE_DOMAIN_REVIEW.md` |
| 16 | medium | todo | Re-run full external governance and large-file safety checks after the next content task before committing | `analysis/v48_governance_preflight/`, `analysis/v47_provenance_gate/` |
| 17 | high | done | Expand the three source-specific high-actionability import routes into concrete future work packets: ZMIZ1, chr1 KIF21B/GPR25, and coupled APC architecture | `knowledge_external/synthesis/V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md` |
| 18 | high | todo | Cross-check that validation-ready high-actionability rows are already covered by frozen V42/V44 harnesses; queue only missing mechanical checks | `docs/validation/` |
| 19 | medium | todo | Summarize the seven low-actionability/context-only closures so future sessions do not reopen them without the named narrow data trigger | `knowledge_external/synthesis/V49_INSUFFICIENT_OVERLAP_TRIAGE.md` |

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
- Committed the audit and ignore rules before history rewrite, then ran:
  `git filter-repo --force --path phases/v3/tmp/ --path tmp_v3/ --path phases/v3/results/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv --path results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv --path analysis/v43_method_validation/synthetic/power_simulation_subjects.tsv.gz --invert-paths`.
- History rewrite completed successfully; new HEAD after rewrite:
  `3fce9f97`.
- `git-filter-repo` removed the `origin` remote as expected. Human follow-up:
  re-add `origin` pointing to
  `https://github.com/sleibach/multiple-sclerosis-auto-research.git`, force-push
  the rewritten `main`, and re-sync downstream clones before V50.
- Post-rewrite tracked-size verification:
  - `git ls-files` tracked files above `50 MiB`: `0`;
  - `git rev-list --objects --all` Git blobs above `50 MiB`: `0`;
  - purge paths now have no tracked files.
- `find . -type f -size +100M -not -path './.git/*'` still finds ignored local
  raw-data and virtualenv files under `.venv_v3_py312/`, `data/raw/`, and
  `data/raw_v3/`. These are not tracked and are not push blockers; they were not
  deleted because Phase 0 targeted tracked disposable caches/history, not local
  raw-data or the Python environment.
- Current open-session active time at `2026-06-14T20:01:40Z`: `256` seconds.
- Post-rewrite health checks:
  - OpenGWAS: PASS; JWT valid until `2026-06-19 12:28 UTC`; POST-only check
    returned HTTP 200.
  - SAP AI Core: Claude PASS, Gemini PASS, RPT PASS.
  - External Markdown linter: PASS (`312` checks, `60` Markdown files).
  - V47 provenance gate: PASS (`359` checks, `39` external JSON records).
  - Tracked files above `50 MiB`: `0`.
- Current open-session active time at `2026-06-14T20:03:40Z`: `376` seconds.

### Iteration 2

- Resumed at `2026-06-14T20:16:32Z`; session 1 was closed at the last
  recorded active checkpoint (`2026-06-14T20:03:40Z`) so idle/compaction time
  is not counted as active work.
- Added 8 segregated external records with source/provenance markers to close
  the high-priority V48 content gaps where a direct or adjacent source was
  available.
- Expanded the V48 convergence/contradiction matrix from `12` to `23` rows:
  `7` corroboration-context rows, `0` contradiction rows, `16`
  insufficient-overlap/context rows, and `0` missing-input rows.
- Closed the prior `11` high-priority V37 external coverage gap rows. The
  regenerated priority map now has `0` high-priority gaps and `9` medium
  uncovered findings.
- Refresh chain completed:
  - class-aware external index: PASS with `47` external JSON records;
  - convergence decision table: PASS with `23` rows;
  - decision-relevant convergence shortlist: PASS with `7` rows;
  - future-grounding queue: PASS with `23` tasks (`3` high priority);
  - source-terms coverage: PASS with `47` records (`8` with explicit terms
    metadata, `39` missing optional terms metadata);
  - high-priority external sourcing plan/search/checklist: refreshed to `0`
    current high-priority rows;
  - unresolved external coverage handoff: PASS with `23` future-grounding
    actions;
  - governance preflight: PASS (`65` checks, `0` failures);
  - V47 provenance gate: PASS (`436` checks, `47` external JSON records,
    `0` failures).
- Large-file safety:
  - tracked files above `50 MiB`: `0`;
  - non-ignored files above `100 MiB` outside raw-data/venv exclusions: `0`.
- Grounded TF-IDF index rebuilt with `728` grounded-tree documents;
  `knowledge_external/` remains outside grounded evidence indexing.
- Current cumulative active time at `2026-06-14T20:24:31Z`: `855` seconds
  (`376` seconds session 1 plus `479` seconds of current open session).
- Committed content gap closure as `1262d6ba` (`Close V49 convergence content
  gaps`).
- Task 11 triage generated `knowledge_external/synthesis/V49_INSUFFICIENT_OVERLAP_TRIAGE.md`
  and `knowledge_external/synthesis/v49_insufficient_overlap_triage.tsv`.
  Result: `16` insufficient-overlap rows triaged into `4` high-actionability,
  `5` medium-actionability, and `7` low-actionability/context-only rows.
- Post-triage external Markdown linter: PASS (`359` checks, `61` Markdown
  files). V47 provenance gate: PASS (`436` checks, `47` external JSON records,
  `0` failures).
- Current cumulative active time at `2026-06-14T20:28:18Z`: `1082` seconds
  (`376` seconds session 1 plus `706` seconds of current open session).
- Committed insufficient-overlap triage as `0e12c50f` (`Triage V49
  insufficient-overlap rows`).
- Task 12 triage generated `knowledge_external/synthesis/V49_UNCOVERED_FINDING_TRIAGE.md`
  and `knowledge_external/synthesis/v49_uncovered_finding_triage.tsv`.
  Result: `9` uncovered V37 findings triaged into `4` medium direct-source
  or dataset/test-only routes and `5` low-priority/optional or do-not-expand
  routes.
- Post-task gates: external Markdown linter PASS (`360` checks, `62`
  Markdown files); V47 provenance gate PASS (`436` checks, `47` external JSON
  records, `0` failures).
- Current cumulative active time at `2026-06-14T20:30:45Z`: `1229` seconds
  (`376` seconds session 1 plus `853` seconds of current open session).
- Task 13 added conservative metadata-only source-terms blocks to the 8 V49
  external records. Source-terms coverage now reports `16` records with terms
  metadata and `31` missing optional terms metadata, down from `39`.
- Post-task gates: source terms metadata linter PASS (`111` checks, `0`
  failures), source terms freshness PASS, source terms coverage freshness PASS,
  high-priority source-terms packet freshness PASS, external Markdown linter
  PASS, V47 provenance gate PASS.
- Current cumulative active time at `2026-06-14T20:33:00Z`: `1364` seconds
  (`376` seconds session 1 plus `988` seconds of current open session).
- Task 14 added `knowledge_external/synthesis/V49_RELATIONSHIP_DELTA_NOTE.md`
  and `knowledge_external/synthesis/v49_relationship_delta_note.tsv`.
  It summarizes the V49 delta: matrix size `12 -> 23`, corroboration-context
  rows `2 -> 7`, contradiction rows `0 -> 0`, insufficient-overlap rows
  `10 -> 16`, and high-priority V37 external coverage gaps `11 -> 0`.
- Post-task gates: external Markdown linter PASS (`361` checks, `63`
  Markdown files); V47 provenance gate PASS (`436` checks, `47` external JSON
  records, `0` failures).
- Current cumulative active time at `2026-06-14T20:34:31Z`: `1455` seconds
  (`376` seconds session 1 plus `1079` seconds of current open session).
- Task 15 added `knowledge_external/catalogs/indexes/V49_NEW_SOURCE_DOMAIN_REVIEW.md`
  and `knowledge_external/catalogs/indexes/v49_new_source_domain_review.tsv`.
  Result: `8` V49-added sources reviewed; `0` need parking for current
  metadata-only use; `1` publisher-hosted source needs access/terms parking
  before fuller reuse; `4` PMC-hosted sources need source-specific terms review
  before table/figure/extended-text reuse.
- Post-task gates: external Markdown linter PASS (`362` checks, `64`
  Markdown files); V47 provenance gate PASS (`436` checks, `47` external JSON
  records, `0` failures).
- Current cumulative active time at `2026-06-14T20:36:09Z`: `1553` seconds
  (`376` seconds session 1 plus `1177` seconds of current open session).
- Task 17 added `knowledge_external/synthesis/V49_SOURCE_SPECIFIC_IMPORT_PACKETS.md`
  and `knowledge_external/synthesis/v49_source_specific_import_packets.tsv`
  for three high-actionability routes: ZMIZ1 direction import, chr1
  KIF21B/GPR25 signal import, and coupled APC-axis record import.
- Post-task gates: external Markdown linter PASS (`363` checks, `65`
  Markdown files); V47 provenance gate PASS (`436` checks, `47` external JSON
  records, `0` failures).
- Current cumulative active time at `2026-06-14T20:37:44Z`: `1648` seconds
  (`376` seconds session 1 plus `1272` seconds of current open session).
