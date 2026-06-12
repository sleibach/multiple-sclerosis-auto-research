# Cold-Start Operator Sequence V45

Status: generated operational sequence. No biological claim and no scoring
authorization.

## Purpose

`scripts/v45_cold_start_operator_sequence.py` joins the current action card,
received-package decision tree, route-arrival packet index, and command-plan
outputs into one route-level sequence for an operator resuming from a clean
checkout or receiving a package.

The generator is plan-only. It does not inspect data, compute module scores,
score outcomes, or run a validation harness.

## Command

```bash
.venv/bin/python scripts/v45_cold_start_operator_sequence.py \
  --outdir analysis/v45_cold_start_operator_sequence
```

## Current Result

Current status: `PASS`.

| Metric | Value |
|---|---:|
| routes listed | `4` |
| routes with `may_score_now=yes` | `0` |

Machine-readable outputs:

- `analysis/v45_cold_start_operator_sequence/cold_start_operator_sequence.tsv`
- `analysis/v45_cold_start_operator_sequence/COLD_START_OPERATOR_SEQUENCE.md`
- `analysis/v45_cold_start_operator_sequence/cold_start_operator_sequence_summary.json`

## Interpretation

This sequence is an operator convenience layer. It tells the operator which
request packet, arrival packet, status template, updater/gate, and command plan
belong to each route. It does not supersede the linked route packet,
preregistration, or harness-ready decision template.

Current generated state: all four routes remain externally blocked or
pre-arrival, and no route may be scored now.
