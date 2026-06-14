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

Current push target checkpoint, verified at `2026-06-14T22:04:02Z`:

- current branch: `main`
- current HEAD: `b2f9805163759cf530da9d0a53b6eab560ed438d`
- remote status: no remote configured (`git remote -v` printed nothing)

Recent local commit chain at this checkpoint:

```text
b2f98051 Record V49 clean tree and size guard
9590784c Record V49 OpenGWAS expiry recheck
eaf58d43 Audit V49 active time after checkpoint
bd04d815 Refresh V49 resume checkpoint after guards
e6235eed Record V49 post-checkpoint guard pass
4fdbbf0c Refresh V49 push handoff after checkpoint
f1b1ef2d Refresh V49 artifact manifest after checkpoint
4f12635a Add V49 final resumability checkpoint
91cb343d Record V49 final external lint pass
16bc14e8 Refresh V49 manifest for guard artifacts
f2238a70 Record V49 clean tree precheck
b67490a0 Refresh V49 push handoff after guards
ecda2195 Recheck V49 grounded index boundary
3fd08db7 Add V49 binary extension audit
489b87e9 Add V49 tmp path guard
28275116 Record V49 OpenGWAS recheck
ac5fc741 Record V49 git integrity check
e6ad446f Refresh V49 artifact manifest for guard
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

Checked at `2026-06-14T22:04:45Z` after the latest V49 commits:

```text
git count-objects -vH
count: 704
size: 10.54 MiB
in-pack: 21745
packs: 1
size-pack: 426.79 MiB
prune-packable: 0
garbage: 0
size-garbage: 0 bytes
```

Additional local state:

- `.git` directory size: `440M`
- commit count on `main`: `582`
- current branch: `main`
- tracked files above `50 MiB`: `0`
- Git blobs above `50 MiB`: `0`

The pack is not tiny because the repository still has substantial legitimate
history, but the GitHub hard-blocking large blobs have been removed.

## Git Integrity Check

Checked at `2026-06-14T22:04:45Z` on HEAD
`017c4e8ed701f97f82fab1969202caad4c85fe0b`:

```bash
git fsck --full --strict
```

Result: PASS. The command exited `0` and printed no findings.

## Next Repository Rule

Do not commit files above `50 MiB`, files under `tmp/`, or regenerated caches.
If a future method needs large raw data, model weights, H5AD, parquet, or
compressed subject-level simulation tables, keep them ignored and commit only
the rerunnable scripts plus compact summaries.
