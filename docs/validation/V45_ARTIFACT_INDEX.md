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

The current run indexes `665` paths across `8` fronts and `9` evidence classes.
This refresh supersedes the earlier item-38 snapshot, which covered roughly
`338-339` paths before the later V45 regression, readiness, acquisition, and
module-coverage artifacts were added.

Front counts:

| Front | Paths |
|---|---:|
| robustness | 196 |
| infrastructure | 262 |
| power/design | 113 |
| cohort dependence | 52 |
| data-free validation | 31 |
| infrastructure/RPT | 8 |
| external account | 2 |
| resume backbone | 1 |

Evidence-class counts:

| Evidence class | Paths | Allowed interpretation |
|---|---:|---|
| synthetic method behavior | 349 | method behavior/planning only; never biological evidence |
| documentation/governance | 105 | governance/readiness documentation |
| validation infrastructure | 82 | mechanical guardrail/readiness; no biological claim |
| software | 43 | executable infrastructure; no biological claim by itself |
| public/external acquisition operations | 49 | cohort availability/request readiness; no validation claim |
| internal convergence null | 27 | data-free internal support; not clinical validation |
| proposal-lens grounding | 7 | proposal prioritization only; no model output as evidence |
| synthesis documentation | 2 | external framing/checklist; no new analysis |
| resume state | 1 | resume state and running backlog |

## Drift Since Earlier Snapshot

The path count increased by about `326-327` paths because V45 continued after
the original index was committed. The dominant additions were:

- synthetic and regression outputs from primary, secondary, preflight,
  subject-map, response-column, checksum, and module-coverage checks;
- cohort-dependence and acquisition-operation records for Gafson, Karolinska,
  and GSE228330;
- validation-readiness guardrails such as the outcome-label dictionary, received
  data board, command-runner plan, and module-coverage precheck;
- infrastructure scripts and docs that make the validation handoff executable.

The refresh does not change interpretation. The index remains an artifact
governance ledger, not a result ledger.

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
