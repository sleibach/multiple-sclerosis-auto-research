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

Current push target checkpoint, verified at `2026-06-14T23:03:19Z`:

- current branch: `main`
- current HEAD: `3a978397f6bbda5e990f22ab58ce97e056dfb14e`
- remote status: no remote configured (`git remote -v` printed nothing)

Recent local commit chain at this checkpoint:

```text
3a978397 Refill V49 backlog after active time audit
3e5688b3 Audit V49 active time after scheduled token check
2f460d61 Record V49 scheduled OpenGWAS and clean state
ff22782c Refresh V49 checkpoints after routing cleanup guards
f7e180ce Record V49 guard pass after routing cleanup
2542bbdd Refresh V49 git integrity after routing cleanup
17cb003e Refresh V49 handoff after routing cleanup
8d7be7f3 Refill V49 backlog and close token duplicates
2b5ff806 Record V49 gap audit routing consistency
62f09f13 Audit V49 active time after gap routing stretch
518ab6d5 Record V49 clean state after gap routing checkpoint
073c44c1 Refresh V49 checkpoints after gap routing guards
49d186e8 Record V49 gap routing guard pass
fed1e81f Refresh V49 handoff after gap checkpoint
5a68dfe9 Refill V49 backlog after gap checkpoint
b731b510 Record V49 clean state after gap audit checkpoint
d9473578 Refresh V49 checkpoints after gap audit guards
2f6ed2b0 Record V49 gap audit guard pass
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

## Local Object Store Checkpoint

Checked at `2026-06-14T22:55:29Z` after the latest V49 commits:

```text
git count-objects -vH
count: 940
size: 12.35 MiB
in-pack: 21745
packs: 1
size-pack: 426.79 MiB
prune-packable: 0
garbage: 0
size-garbage: 0 bytes
```

Additional local state:

- `.git` directory size: `442M`
- commit count on `main`: `630`
- current branch: `main`
- tracked files above `50 MiB`: `0`
- Git blobs above `50 MiB`: `0`

The pack is not tiny because the repository still has substantial legitimate
history, but the GitHub hard-blocking large blobs have been removed.

## Git Integrity Check

Checked at `2026-06-14T22:55:29Z` on HEAD
`17cb003ebc282e682fb0c65901bc72ca0c64cb42`:

```bash
git fsck --full --strict
```

Result: PASS. The command exited `0` and printed no findings.

## Next Repository Rule

Do not commit files above `50 MiB`, files under `tmp/`, or regenerated caches.
If a future method needs large raw data, model weights, H5AD, parquet, or
compressed subject-level simulation tables, keep them ignored and commit only
the rerunnable scripts plus compact summaries.
