# V45 Artifact Index

Status: artifact governance index. No biological claim.

## Purpose

V45 is a long, self-directed readiness block with many small checkpoints. This
index maps committed V45 outputs to:

- project front;
- artifact status;
- evidence/usage class;
- allowed interpretation;
- latest commit where available.

The goal is handoff and auditability: a reviewer should be able to tell which
files are synthetic method checks, which are public metadata scouts, which are
software, and which are documentation.

## Generator

`scripts/v45_artifact_index.py`

Command:

```bash
.venv/bin/python scripts/v45_artifact_index.py
```

Outputs:

- `analysis/v45_artifact_index/v45_artifact_index.tsv`
- `analysis/v45_artifact_index/front_class_summary.tsv`
- `analysis/v45_artifact_index/summary.json`

## Current Summary

The current run indexes `338` paths across `8` fronts and `9` evidence classes.

Front counts:

| Front | Paths |
|---|---:|
| robustness | 138 |
| infrastructure | 108 |
| cohort dependence | 37 |
| data-free validation | 31 |
| power/design | 13 |
| infrastructure/RPT | 8 |
| external account | 2 |
| resume backbone | 1 |

Evidence-class counts:

| Evidence class | Paths | Allowed interpretation |
|---|---:|---|
| synthetic method behavior | 161 | method behavior/planning only; never biological evidence |
| validation infrastructure | 49 | mechanical guardrail/readiness; no biological claim |
| public/external acquisition operations | 34 | cohort availability/request readiness; no validation claim |
| documentation/governance | 31 | governance/readiness documentation |
| internal convergence null | 27 | data-free internal support; not clinical validation |
| software | 26 | executable infrastructure; no biological claim by itself |
| proposal-lens grounding | 7 | proposal prioritization only; no model output as evidence |
| synthesis documentation | 2 | external framing/checklist; no new analysis |
| resume state | 1 | resume state and running backlog |

Rows with `latest_commit=pending_this_checkpoint` are files created by the same
checkpoint that generated this index; the commit hash becomes available after
the checkpoint is committed.

## Interpretation Guard

This index is not a result ledger. It is an artifact ledger. In particular:

- synthetic outputs remain method-characterization only;
- public metadata scouts establish availability/blockers, not validation;
- internal convergence/null rows are data-free support, not external clinical
  validation;
- scripts are executable infrastructure and require their linked outputs for
  interpretation.
