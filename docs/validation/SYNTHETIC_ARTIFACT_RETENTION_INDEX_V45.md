# Synthetic Artifact Retention / Interpretation Index V45

Status: artifact-governance document. No new biological claim is made here.

## Purpose

V43-V45 intentionally produced many synthetic and method-characterization
outputs. Those outputs are valuable, but they carry a high self-deception risk if
they are later read as biological evidence. This document and its machine-readable
index classify each V43-V45 analysis artifact family by allowed interpretation.

Machine-readable index:

- `analysis/v45_synthetic_artifact_index/v43_v45_artifact_index.tsv`
- `analysis/v45_synthetic_artifact_index/class_summary.tsv`
- `analysis/v45_synthetic_artifact_index/summary.json`

Generator:

- `scripts/v45_synthetic_artifact_index.py`

## Index Summary

The refreshed index covers `48` V43-V45 analysis directories, with `31`
directories containing synthetic inputs, synthetic outputs, or synthetic content
markers. Current V43-V45 analysis output footprint is approximately `154 MiB`.

| Class | Directories | Files | Allowed interpretation |
|---|---:|---:|---|
| `synthetic_method_characterization` | `10` | `195` | Method behavior only |
| `synthetic_regression` | `4` | `120` | Software regression only |
| `synthetic_intake_verification` | `6` | `88` | Method behavior only |
| `synthetic_harness_verification` | `3` | `42` | Method behavior only |
| `internal_convergence_null` | `6` | `32` | Data-free internal support, not clinical validation |
| `operations` | `4` | `5` | Acquisition operations only |
| `public_metadata_scout` | `3` | `20` | Cohort availability evidence only |
| `artifact_governance` | `4` | `10` | Index/storage/refresh accounting only |
| `power_design_planning` | `2` | `6` | Study-design planning only |
| `integrity_governance` | `2` | `11` | Repository/locked-artifact integrity only |
| `public_metadata_preparation` | `1` | `5` | Acquisition readiness only |
| `proposal_lens_grounding` | `1` | `6` | Proposal prioritization only |
| `validation_infrastructure` | `2` | `10` | Command/toolchain readiness only |

## Interpretation Rules

Synthetic classes:

- may support statements about false-positive behavior, power, robustness, and
  software correctness;
- may not support statements about MS biology, clinical validity, treatment
  response, or mechanism truth;
- must be described as seeded, synthetic, and method-only in reports.

Internal convergence classes:

- may support statements that the APC/HLA/IFN axis recurs across the project's
  corpus beyond the specified nulls;
- may not substitute for external paired treatment-response validation;
- must be paired with the V42/V44/V45 validation-readiness boundary.

Public metadata scout/preparation classes:

- may support data-availability and acquisition-route claims;
- may not count a cohort as usable unless paired structure, labels, and module
  coverage are verified;
- must distinguish open pharmacodynamic context from response validation.

Proposal-lens classes:

- may document that RPT/LLM proposal priorities matched or did not match
  artifact-derived expectations;
- may not be cited as evidence for biological claims.

## Retention Policy

Keep these artifacts in version control because they are reproducibility evidence
for method behavior and readiness, but keep their interpretation bounded:

1. Preserve synthetic inputs and outputs with their existing `synthetic` markers.
2. Do not merge synthetic method tables into biological evidence frames.
3. Do not cite synthetic pass/fail rates without saying they are method behavior
   only.
4. Do not use public metadata preparation artifacts as if the underlying real
   expression/outcome data were already acquired.
5. If a future script consumes a V43-V45 artifact, it should first check this
   index or explicitly state why the artifact class is appropriate.

See `docs/validation/SYNTHETIC_OUTPUT_RETENTION_POLICY_V45.md` for the more
explicit keep/archive/regenerate policy.

## Practical Use

Before external reporting, filter V43-V45 artifacts by class:

- include `synthetic_*` classes in methods/readiness sections only;
- include `internal_convergence_null` under internal convergence support only;
- include `public_metadata_*` under acquisition/data-availability only;
- include `operations` under project management only;
- exclude `proposal_lens_grounding` from evidence tables unless the table is
  explicitly about tooling behavior.
