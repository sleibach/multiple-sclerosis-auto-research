# ToleDYNAMIC Metadata-Only Intake Classifier V56

Purpose: enforce the V56 pre-value causal-identification branch before assay or
clinical values are read. This is a method-control artifact, not biological
evidence and not proof that the controlled substudy package exists.

## Command

```bash
python3 scripts/v56_toledynamic_intake_classifier.py classify \
  <controlled-workspace>/toledynamic_manifest.json \
  --outdir <controlled-workspace>/toledynamic_intake
```

The manifest contains design metadata only. It must not contain expression,
flow, function, MRI, disability, safety, or treatment-response values.

## Required Manifest Fields

| field | type | meaning |
|---|---|---|
| `manifest_version` | string | intake schema version |
| `package_id` | string | non-identifying local package token |
| `terms_processing_allowed` | boolean | written terms permit processing |
| `participant_level` | boolean | records are participant-level rather than aggregate-only |
| `parent_trial_linkage` | boolean | substudy records link to HERCULES/PERSEUS participants |
| `randomized_arm_field` | boolean | randomized arm can be reconstructed |
| `hercules_both_arms` | boolean | both HERCULES arms are represented |
| `perseus_both_arms` | boolean | both PERSEUS arms are represented |
| `substudy_selection` | enum | `outcome_blind_pre_unblinding`, `post_unblinding`, or `unknown` |
| `baseline_available` | boolean | baseline samples are represented |
| `month3_available` | boolean | month-3 samples are represented |

Unknown is not treated as favorable. Documentary confirmation is required for
the outcome-blind selection state.

## Safe Classes

| class | maximum interpretation |
|---|---|
| `BRANCH_A_METADATA_ELIGIBLE` | proceed to assay-specific QC; randomized inference is not yet established |
| `BRANCH_B_DESCRIPTIVE_ONLY` | paired descriptive trajectories only after QC; no treatment/mechanism claim |
| `BRANCH_C_NO_GROUNDING` | aggregate/no-linkage package cannot ground the frozen tests |
| `STOP_TERMS_BLOCK` | do not inspect or process package content |

`BRANCH_A_METADATA_ELIGIBLE` is deliberately not named `PASS`: perfect nesting
of arm with site/batch, RNA-subset selection, missingness, module coverage, or
assay QC can still invalidate randomized analysis.

## Synthetic Verification

```bash
python3 scripts/v56_toledynamic_intake_classifier.py synthetic-check \
  --outdir analysis/v56_toledynamic_intake_classifier \
  --fail-on-error
```

The committed fixtures are synthetic and test six branches: metadata-eligible,
active-arm-only, unknown selection, missing month 3, aggregate-only, and
terms-blocked. They test classifier behavior only and are never MS evidence.
