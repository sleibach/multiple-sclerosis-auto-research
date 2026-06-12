# No-Score-Before-Gates Linter V45

Status: validation-readiness guard. No biological claim.

## Purpose

`scripts/v45_no_score_before_gates_linter.py` checks that the main V45 operator
docs and route-arrival packets keep explicit no-scoring-before-gates language.
It is a documentation and operations guard only. It does not inspect data,
compute module scores, score outcomes, or run a validation harness.

## Command

Live check:

```bash
.venv/bin/python scripts/v45_no_score_before_gates_linter.py \
  --outdir analysis/v45_no_score_before_gates_linter/live \
  --expect-status PASS
```

Synthetic negative check:

```bash
.venv/bin/python scripts/v45_no_score_before_gates_linter.py \
  --outdir analysis/v45_no_score_before_gates_linter/synthetic_bad \
  --synthetic-case bad \
  --expect-status FAIL
```

## Current Result

| Check | Expected | Observed | Targets | Checks | Failures |
|---|---|---|---:|---:|---:|
| live operator docs and route packets | `PASS` | `PASS` | `9` | `63` | `0` |
| synthetic bad fixture | `FAIL` | `FAIL` | `1` | `7` | `6` |

Machine-readable outputs:

- `analysis/v45_no_score_before_gates_linter/live/no_score_before_gates_summary.json`
- `analysis/v45_no_score_before_gates_linter/live/no_score_before_gates_lint.tsv`
- `analysis/v45_no_score_before_gates_linter/synthetic_bad/no_score_before_gates_summary.json`
- `analysis/v45_no_score_before_gates_linter/synthetic_bad/no_score_before_gates_lint.tsv`

## Interpretation

A live pass means the checked docs retain required gate language and avoid
explicit shortcut phrases such as "score immediately" or "skip preflight." It
does not mean any cohort is received, preflighted, scoreable, or validated.

The synthetic bad fixture is intentionally invalid. Its failure verifies that
the linter can catch missing guard language and direct shortcut wording.
