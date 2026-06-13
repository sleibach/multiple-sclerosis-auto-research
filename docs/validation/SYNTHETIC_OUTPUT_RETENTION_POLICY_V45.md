# Synthetic Output Retention Policy V45

Status: storage and interpretation policy. No biological claim.

Purpose: define how V43-V46 synthetic, regression, and method-characterization
outputs are retained, archived, or regenerated without weakening
reproducibility or letting synthetic data masquerade as biological evidence.

## Current Footprint

The refreshed artifact index covers:

- `97` V43-V46 analysis directories;
- `65` directories with synthetic path/content markers;
- approximately `154 MiB` total across `analysis/v43_*`, `analysis/v44_*`,
  `analysis/v45_*`, and `analysis/v46_*` directories;
- no `unclassified_v43_v46` directories after the latest governance refresh.

Machine-readable source:

- `analysis/v45_synthetic_artifact_index/v43_v46_artifact_index.tsv`
- `analysis/v45_synthetic_artifact_index/class_summary.tsv`
- `analysis/v45_synthetic_artifact_index/summary.json`

## Retention Classes

| Class | Default action | Rationale |
|---|---|---|
| `synthetic_method_characterization` | retain summaries, configs, seeds, and compact result tables; archive bulky replicate-level tables only after summary regeneration is verified | supports power, robustness, and false-positive behavior claims |
| `synthetic_harness_verification` | retain | proves frozen harness mechanics before real data |
| `synthetic_intake_verification` | retain | proves quarantine/preflight/coverage guard behavior |
| `synthetic_regression` | retain latest committed outputs and keep scripts executable | supports software regression claims |
| `power_design_planning` | retain | directly supports medical-team cohort-size decisions |
| `internal_convergence_null` | retain | data-free internal support; not external validation |
| `public_metadata_scout` / `public_metadata_preparation` | retain | cohort availability and acquisition-route evidence |
| `operations` | retain while cohort requests are live | acquisition state and handoff audit trail |
| `artifact_governance` / `integrity_governance` | retain | index, storage accounting, no-raw and hash-audit guardrails |
| `proposal_lens_grounding` | retain as tooling/process evidence only | model/RPT output remains proposal-prioritization, not evidence |
| `validation_infrastructure` | retain | command/toolchain readiness |

## What May Be Archived Later

Archiving is allowed only for large replicate-level synthetic outputs when all
conditions hold:

1. the generator script is committed;
2. the random seeds/configuration are committed or printed in a committed
   summary;
3. compact summaries needed by docs are retained;
4. a regeneration command is documented;
5. archived files are not required by the regression aggregator or current
   command-runner plans.

Archiving means moving to an explicit archive location or external artifact
store with a manifest. It does not mean deleting without trace.

## What Must Not Be Archived Before Validation

Keep these in git while Gafson/Karolinska/GSE228330 acquisition remains live:

- V42/V43/V45 primary harness synthetic null/planted outputs;
- V45 regression aggregator outputs;
- intake preflight, checksum, subject-map, response-column, and module-coverage
  synthetic checks;
- locked-artifact hash-audit baseline and latest audit output;
- cohort acquisition and received-data triage tables;
- compact power/design tables used by collaborator requests.

## Interpretation Guard

Synthetic outputs can support only method statements:

- power and sample-size expectations;
- false-positive behavior under specified synthetic pathologies;
- harness/software correctness;
- intake/preflight guard behavior.

Synthetic outputs cannot support:

- MS biological mechanism claims;
- clinical validation claims;
- treatment-response effect estimates;
- cohort usability claims for real incoming data.

Any report citing synthetic output must use explicit method-only wording.

## Regeneration Check

Before pruning or archiving any synthetic directory, run the relevant executable
check if available:

```bash
.venv/bin/python scripts/v45_regression_aggregator.py \
  --outdir analysis/v45_regression_aggregator
```

For one-off directories, run the generator named in the linked documentation
and verify the summary status remains `PASS` or the documented expected null.

## Current Decision

Current footprint is small enough (`~154 MiB`) to keep all V43-V46 synthetic and
method-characterization outputs in version control. No pruning is recommended
before the first real validation package arrives, because these outputs are
active reproducibility evidence for the preregistered validation apparatus.
