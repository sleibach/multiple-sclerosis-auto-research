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

Current push target checkpoint, verified at `2026-06-14T21:48:34Z`:

- current branch: `main`
- current HEAD: `ecda219525448444c9b321a6bbcf1a239b9ef2e3`
- remote status: no remote configured (`git remote -v` printed nothing)

Recent local commit chain at this checkpoint:

```text
ecda2195 Recheck V49 grounded index boundary
3fd08db7 Add V49 binary extension audit
489b87e9 Add V49 tmp path guard
28275116 Record V49 OpenGWAS recheck
ac5fc741 Record V49 git integrity check
e6ad446f Refresh V49 artifact manifest for guard
18009d1b Refresh V49 resume checkpoint
8625c309 Audit V49 active time accounting
4f0e8149 Record V49 object store checkpoint
05285904 Add V49 final large file guard
401e43b6 Refresh V49 push handoff to latest head
3a52cc72 Document V43 power cache purge boundary
9e8705f9 Verify V49 purge ignore rules
983842ee Route V49 purge audit in reader handoff
2eedba8c Refresh V49 artifact manifest
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

Checked at `2026-06-14T21:35:52Z` after the latest V49 commits:

```text
git count-objects -vH
count: 602
size: 9.85 MiB
in-pack: 21745
packs: 1
size-pack: 426.79 MiB
prune-packable: 0
garbage: 0
size-garbage: 0 bytes
```

Additional local state:

- `.git` directory size: `440M`
- commit count on `main`: `560`
- current branch: `main`
- tracked files above `50 MiB`: `0`
- Git blobs above `50 MiB`: `0`

The pack is not tiny because the repository still has substantial legitimate
history, but the GitHub hard-blocking large blobs have been removed.

## Git Integrity Check

Checked at `2026-06-14T21:40:55Z` on HEAD
`e6ad446f17b1275175c96c9bc3b22efabcd2e14b`:

```bash
git fsck --full --strict
```

Result: PASS. The command exited `0` and printed no findings.

## Next Repository Rule

Do not commit files above `50 MiB`, files under `tmp/`, or regenerated caches.
If a future method needs large raw data, model weights, H5AD, parquet, or
compressed subject-level simulation tables, keep them ignored and commit only
the rerunnable scripts plus compact summaries.
