# V49 Rewrite/Push Handoff

Status: operational handoff. V49 rewrote Git history to remove disposable
tracked large files that exceeded GitHub's size limits. This file records what
changed and what the human must do before treating the remote as synchronized.

## What V49 Did

V49 removed these tracked large/cache/generated paths from history with
`git-filter-repo`:

- `phases/v3/tmp/`
- `tmp_v3/`
- `phases/v3/results/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `analysis/v43_method_validation/synthetic/power_simulation_subjects.tsv.gz`

The tracked large-file checks after the rewrite found:

- tracked files above `50 MiB`: `0`
- Git blobs above `50 MiB`: `0`
- staged or unignored files above `50 MiB`: `0`

`.gitignore` now blocks recurrence for tmp/cache paths and the purged
reproducible large generated outputs.

## Important Side Effect

`git-filter-repo` removed the `origin` remote as a safety measure. Current local
remote status after V49: no remote configured.

## Required Human Steps

From this rewritten local clone:

```bash
git remote add origin https://github.com/sleibach/multiple-sclerosis-auto-research.git
git push --force-with-lease origin main
```

Current push target checkpoint, verified at `2026-06-14T21:32:53Z`:

- current branch: `main`
- current HEAD: `3a52cc72815fb03deabb68b3961df331db134cb9`
- remote status: no remote configured (`git remote -v` printed nothing)

Recent local commit chain at this checkpoint:

```text
3a52cc72 Document V43 power cache purge boundary
9e8705f9 Verify V49 purge ignore rules
983842ee Route V49 purge audit in reader handoff
2eedba8c Refresh V49 artifact manifest
a8f24542 Recheck V49 source URL duplicates
13af8589 Recheck V49 source terms coverage
495c62f3 Refresh V49 rewrite handoff checkpoint
fbef66cf Audit V49 purged artifact references
fb9d4a48 Add V49 artifact manifest
d169125d Add V49 resume checkpoint
9ec47cbb Record V49 OpenGWAS token status
d363ae84 Record V49 grounded index boundary check
1ed229ee Add V49 reader quickstart
6b9eaf08 Add V49 source independence delta
aced6317 Add V49 rewrite push handoff
```

If `--force-with-lease` rejects because the remote changed independently, stop
and inspect the remote commits before pushing. Do not use blind force unless the
remote state has been intentionally superseded.

## Required Re-Sync For Other Clones

Every other clone of this repository must be re-synced to the rewritten remote.
Recommended safe approach:

```bash
git fetch origin
git switch main
git reset --hard origin/main
```

Only run `reset --hard` in clones where local uncommitted work has already been
saved elsewhere. This is a human clone-maintenance step, not something V49 ran
automatically.

## Verification After Push

After force-pushing and re-syncing, verify:

```bash
git remote -v
git status --short
git ls-files | xargs -I{} sh -c 'test -f "$1" && [ "$(wc -c < "$1")" -gt 52428800 ] && echo "$1"' sh {}
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | awk '$1=="blob" && $3>52428800 {print}'
```

Both large-file commands should print nothing.

## Next Repository Rule

Do not commit files above `50 MiB`, files under `tmp/`, or regenerated caches.
If a future method needs large raw data, model weights, H5AD, parquet, or
compressed subject-level simulation tables, keep them ignored and commit only
the rerunnable scripts plus compact summaries.
