# Synthetic Artifact Retention / Interpretation Index V45

Status: artifact-governance document. No new biological claim is made here.

## Purpose

V43-V46 intentionally produced many synthetic and method-characterization
outputs. Those outputs are valuable, but they carry a high self-deception risk if
they are later read as biological evidence. This document and its machine-readable
index classify each V43-V46 analysis artifact family by allowed interpretation.

Machine-readable index:

- `analysis/v45_synthetic_artifact_index/v43_v46_artifact_index.tsv`
- `analysis/v45_synthetic_artifact_index/class_summary.tsv`
- `analysis/v45_synthetic_artifact_index/summary.json`

Generator:

- `scripts/v45_synthetic_artifact_index.py`

## Index Summary

The refreshed index covers `118` V43-V46 analysis directories, with `79`
directories containing synthetic inputs, synthetic outputs, or synthetic content
markers. Current V43-V46 analysis output footprint is approximately `157 MiB`.

| Class | Directories | Files | Allowed interpretation |
|---|---:|---:|---|
| `artifact_governance` | `1` | `1` | Refresh log only |
| `artifact_governance` | `1` | `3` | Storage/accounting only |
| `artifact_governance` | `2` | `7` | Index only |
| `integrity_governance` | `1` | `2` | OpenGWAS auth-expiry sentinel only |
| `integrity_governance` | `1` | `8` | Author-run packet checksum integrity only |
| `integrity_governance` | `1` | `6` | Author-run packet dry-run integrity only |
| `integrity_governance` | `1` | `6` | Collaborator package path integrity only |
| `integrity_governance` | `1` | `2` | Command-plan integrity only |
| `integrity_governance` | `1` | `6` | Cross-route readiness consistency only |
| `integrity_governance` | `1` | `5` | First-30 repair-template coverage only |
| `integrity_governance` | `1` | `2` | Generated-checker registry only |
| `integrity_governance` | `1` | `2` | Generated-document freshness check only |
| `integrity_governance` | `1` | `11` | Locked-artifact integrity only |
| `integrity_governance` | `1` | `5` | No-score-before-gates documentation check only |
| `integrity_governance` | `1` | `6` | Outbound request packet integrity only |
| `integrity_governance` | `1` | `2` | Pre-commit readiness only |
| `integrity_governance` | `1` | `3` | Readiness dashboard only |
| `integrity_governance` | `1` | `2` | Readiness freshness check only |
| `integrity_governance` | `1` | `6` | Received-package decision routing only |
| `integrity_governance` | `1` | `2` | Repository hygiene only |
| `integrity_governance` | `1` | `6` | Returned-package dependency graph only |
| `integrity_governance` | `1` | `4` | Returned-package documentation cross-link only |
| `integrity_governance` | `1` | `8` | Route packet checksum/freshness only |
| `integrity_governance` | `1` | `6` | State-machine transition consistency only |
| `internal_convergence_null` | `6` | `32` | Data-free internal support, not clinical validation |
| `operations` | `1` | `4` | Acquisition follow-up status only |
| `operations` | `1` | `1` | Author-run packet bundle only |
| `operations` | `1` | `3` | Cold-start operator sequence only |
| `operations` | `1` | `4` | Current action navigation only |
| `operations` | `1` | `2` | External blocker escalation status only |
| `operations` | `1` | `2` | External blocker status only |
| `operations` | `1` | `7` | External blocker timing status only |
| `operations` | `1` | `4` | First-30 returned-package status board only |
| `operations` | `1` | `4` | First-30-minute returned-package decision routing only |
| `operations` | `1` | `6` | Follow-up escalation drafts only |
| `operations` | `1` | `4` | Partial-label repair prioritization only |
| `operations` | `1` | `3` | Received-package status update only |
| `operations` | `1` | `6` | Request-sent intake template only |
| `operations` | `1` | `10` | Request-sent status update only |
| `operations` | `1` | `4` | Returned-package handoff navigation only |
| `operations` | `1` | `14` | Returned-package repair request drafts only |
| `operations` | `1` | `6` | Route-specific arrival commands only |
| `operations` | `1` | `12` | Unsent acquisition message drafts only |
| `operations` | `4` | `5` | Acquisition operations only |
| `power_design_planning` | `5` | `34` | Study-design planning only |
| `proposal_lens_grounding` | `1` | `6` | Proposal prioritization only |
| `public_metadata_preparation` | `1` | `5` | Acquisition readiness only |
| `public_metadata_scout` | `3` | `20` | Cohort availability evidence only |
| `synthetic_harness_verification` | `3` | `42` | Method behavior only |
| `synthetic_intake_verification` | `1` | `2` | Expected missing-output guard only |
| `synthetic_intake_verification` | `28` | `586` | Method behavior only |
| `synthetic_method_characterization` | `10` | `195` | Method behavior only |
| `synthetic_regression` | `1` | `9` | Status-board schema regression only |
| `synthetic_regression` | `2` | `941` | Software/readiness regression only |
| `synthetic_regression` | `4` | `120` | Software regression only |
| `validation_infrastructure` | `1` | `9` | Command handoff only |
| `validation_infrastructure` | `1` | `3` | Expected missing-output guard only |
| `validation_infrastructure` | `1` | `3` | Handoff completeness only |
| `validation_infrastructure` | `1` | `4` | Handoff manifest only |
| `validation_infrastructure` | `1` | `4` | Toolchain readiness only |

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
5. If a future script consumes a V43-V46 artifact, it should first check this
   index or explicitly state why the artifact class is appropriate.

See `docs/validation/SYNTHETIC_OUTPUT_RETENTION_POLICY_V45.md` for the more
explicit keep/archive/regenerate policy.

## Practical Use

Before external reporting, filter V43-V46 artifacts by class:

- include `synthetic_*` classes in methods/readiness sections only;
- include `internal_convergence_null` under internal convergence support only;
- include `public_metadata_*` under acquisition/data-availability only;
- include `operations` under project management only;
- exclude `proposal_lens_grounding` from evidence tables unless the table is
  explicitly about tooling behavior.
