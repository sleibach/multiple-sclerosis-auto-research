# ToleDYNAMIC Extension Estimand Classifier V56

Purpose: route a possible NCT06372145 ToleDYNAMIC return using design metadata
only. This method guard reads no expression, function, safety, or clinical
outcome value and supplies no biological evidence.

## Use

```bash
.venv/bin/python scripts/v56_toledynamic_extension_estimand_classifier.py \
  classify <controlled-workspace>/extension_design_manifest.json \
  --outdir <controlled-workspace>/extension_estimand_route
```

The manifest records terms, participant/parent linkage, baseline/month-3
coverage, prior randomized arm and actual exposure linkage, complete rollover
and substudy selection flow, parent-exit covariates, positivity inputs,
laboratory blinding, site/batch maps, and paired counts for former-placebo
initiators and former-tolebrutinib continuers.

## Safe Classes

| class | maximum permitted action |
|---|---|
| `INITIATION_CONTINUATION_METADATA_ELIGIBLE` | run assay QC and the fixed non-causal initiation-versus-continuation sensitivity |
| `INITIATION_CONTINUATION_ESTIMATION_ONLY` | report estimates and intervals only; at least one group has fewer than eight pairs |
| `PAIRED_TRAJECTORY_ONLY` | run only within-participant active-exposure trajectories after QC |
| `NO_FROZEN_MONTH3_TRAJECTORY` | report coverage; do not substitute another visit |
| `NO_PARTICIPANT_LEVEL_GROUNDING` | report access/linkage limitation only |
| `STOP_TERMS_BLOCK` | inspect no package content |

The strongest class is metadata eligibility, not a pass. It cannot establish a
current randomized treatment effect because initiators and continuers differ in
prior exposure and enter through selected post-trial rollover and substudy
paths. Assay QC, covariate overlap, max-T, weighting, selection bounds, and
site/batch sensitivities still have to pass.

## Synthetic Verification

```bash
.venv/bin/python scripts/v56_toledynamic_extension_estimand_classifier.py \
  synthetic-check \
  --outdir analysis/v56_toledynamic_extension_estimand_classifier \
  --fail-on-error
```

Seven committed synthetic fixtures cover eligible, one-group-only, incomplete
rollover, small-group estimation, aggregate-only, missing-month-3, and
terms-blocked returns. They test software behavior only and are never MS or
treatment evidence.

