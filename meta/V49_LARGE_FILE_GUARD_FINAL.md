# V49 Large-File Guard Final

Status: operational repository hygiene check. This records the large-file guard
after the V49 history rewrite and later V49 commits.

Checked at `2026-06-14T21:34:10Z`.

## Results

| check | threshold/scope | result |
|---|---|---:|
| tracked working-tree files | `>50 MiB` | `0` |
| Git blobs in current rewritten history | `>50 MiB` | `0` |
| unignored filesystem files outside raw-data/venv exclusions | `>100 MiB` | `0` |

## Commands

```bash
python3 - <<'PY'
import os, subprocess
large=[]
for path in subprocess.check_output(['git','ls-files'], text=True).splitlines():
    try: size=os.path.getsize(path)
    except FileNotFoundError: continue
    if size > 50*1024*1024: large.append((size,path))
print('tracked_over_50MiB', len(large))
PY

git rev-list --objects --all \
  | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' \
  | awk '$1=="blob" && $3>52428800 {print}'

find . -type f -size +100M -not -path './.git/*' \
  -not -path './.venv*/*' \
  -not -path './data/raw/*' \
  -not -path './data/raw_v3/*' \
  -not -path './data/processed/*' \
  -not -path './data/processed_v3/*' \
  -not -path './data/external/*' \
  -not -path './data/external_v3/*' \
  -not -path './data/onek1k/*'
```

The second and third commands printed no file/blob rows. The first reported
`tracked_over_50MiB 0`.

## Boundary

This is a push-safety and repository-hygiene check only. It does not change any
scientific result, external source relationship, locked rule, or validation
pre-registration.

