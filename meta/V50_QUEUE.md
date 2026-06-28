# V50 Queue: Sharper External Knowledge + Per-Iteration Push

Status: active. This queue tracks summed active session intervals, not calendar
span across resume gaps.

## Timing

- block_start_utc: `2026-06-28T13:01:18Z`
- active_target_seconds: `21600`
- active_target_hours: `6`
- active_time_rule: sum completed session intervals plus current open interval;
  exclude idle/resume gaps.

| session | start_utc | end_utc | active_seconds | note |
|---:|---|---|---:|---|
| 1 | `2026-06-28T13:01:18Z` | OPEN | OPEN | initial V50 session |

## Remote / Push Status

Remote status at V50 start:

- `origin` configured: `https://github.com/sleibach/multiple-sclerosis-auto-research.git`
- local rewritten `main` at V50 start: `9794adf0af7429f1a3d47e53fc5a2f10817d9842`
- remote `main` before one-time reconciliation: `dabc45526f3e665dc7a2110c0e0d360d1fe661d8`
- divergence after fetching `origin/main`: local has `700` left-only commits;
  remote has `41` right-only commits from the pre-rewrite history.
- push state: `BLOCKED_ON_HUMAN_RECONCILIATION`

The human attempted `git push --force-with-lease origin main`, which failed with
`stale info` because the remote lease had not yet been fetched after re-adding
`origin`. V50 fetched the remote ref into `origin/main`; the safe human command
is now:

```bash
git push --force-with-lease=refs/heads/main:dabc45526f3e665dc7a2110c0e0d360d1fe661d8 origin main:main
```

Do not run a blind force push. If the explicit lease rejects, fetch and inspect
the new remote `main` before retrying.

Until the one-time reconciliation succeeds, V50 commits locally, runs all
guards, attempts plain push after each iteration, records rejection, and does
not force-push over the divergent remote.

## OpenGWAS Status

OpenGWAS work is disabled for V50 until token renewal:

- `OPENGWAS_JWT` present in `.env`: yes
- decoded expiry: `2026-06-19T12:28:39Z`
- status: expired
- policy: do not call OpenGWAS endpoints; route around OpenGWAS-dependent work;
  renewal is a pending human step.

## Tooling Health

Checked at V50 start:

- SAP AI Core Claude smoke: PASS (`anthropic--claude-4.7-opus`, deployment
  `def854013c7ac379`)
- SAP AI Core Gemini smoke: PASS (`gemini-2.5-pro`, deployment
  `d6dc532885507ac7`)
- SAP RPT smoke: PASS (`sap-rpt-1-large`, deployment `d61aae51af327bbc`)

## Backlog

| id | priority | status | task | artifact |
|---:|---|---|---|---|
| 1 | high | done | Start V50 queue, record active-time rules, remote blocker, OpenGWAS expiry, and tool health | `meta/V50_QUEUE.md` |
| 2 | high | todo | Diagnose all 16 V49 insufficient-overlap rows by specificity gap, novelty gap, and exact sharper-source requirement | `knowledge_external/synthesis/V50_INSUFFICIENT_OVERLAP_DIAGNOSIS.md` |
| 3 | high | todo | Acquire sharper external records for bounded APC/HLA-II monitoring and V22 immune-tone confounding without using OpenGWAS | `knowledge_external/records/`, `knowledge_external/synthesis/` |
| 4 | high | todo | Acquire sharper external records for ZMIZ1 and chr1 KIF21B/GPR25 direction/tractability claims without using OpenGWAS | `knowledge_external/records/`, `knowledge_external/synthesis/` |
| 5 | high | todo | Reassess convergence/contradiction rows against newly sharpened records and update counts honestly | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V50.md` |
| 6 | medium | todo | Update public external index and reader quickstart for V50 sharper-source artifacts | `knowledge_external/INDEX.md`, `knowledge_external/synthesis/V49_READER_QUICKSTART.md` |
| 7 | high | todo | Run provenance, public-index, external Markdown, matrix-count, large-file, tmp-path, and Git-blob guards after first V50 content iteration | `analysis/v47_provenance_gate/`, `analysis/v47_external_markdown_index_linter/` |
| 8 | medium | todo | Commit first V50 content iteration and attempt plain push; record success or blocker | `meta/V50_QUEUE.md` |
| 9 | medium | todo | Refresh final/resume checkpoints or add V50 checkpoint card after first guard/push cycle | `meta/V50_QUEUE.md` |
| 10 | medium | todo | Refill V50 backlog above threshold after task 9 | `meta/V50_QUEUE.md` |

## Iteration Notes

- Task 1 initialized V50. Remote reconciliation is not complete: `origin` exists
  and `origin/main` was fetched, but remote `main` still points to the old
  history. Human must run the explicit `--force-with-lease=<remote-sha>` command
  above. V50 will not force-push over the divergent remote.
- Task 1 pre-commit guards: provenance PASS (`436` checks, `47` external JSON
  records, `0` failures); local `HEAD` large-blob guard PASS (`0` blobs above
  `50 MiB`); tracked-file size guard PASS (`0` tracked files above `50 MiB`);
  tracked tmp-path guard PASS (`0` tracked tmp paths). All-refs Git blob guard
  detects the old purged blob through fetched `origin/main`
  (`results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`,
  `101135644` bytes), confirming the remote still needs the one-time rewritten
  history reconciliation before all-ref guards can be green.
- Current cumulative active time at `2026-06-28T13:04:35Z`: `197` seconds.
  Target met: `false`.
