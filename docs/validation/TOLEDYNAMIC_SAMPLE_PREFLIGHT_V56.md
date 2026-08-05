# ToleDYNAMIC Sample-Manifest Preflight V56

Purpose: detect paired-coverage failures and perfect randomized-arm nesting in
site or assay batch before molecular, functional, or clinical values are read.
This is method behavior, not biological or treatment evidence.

## Input

The tab-separated sample manifest contains only:

`sample_id`, `participant_id`, `parent_trial`, `randomized_arm`, `site`,
`visit`, `assay`, `cell_type`, and `batch`.

Allowed trial values are `HERCULES` and `PERSEUS`; arms are `tolebrutinib` and
`placebo`; visits are `baseline`, `month3`, and `month12`. Assay values and
clinical outcomes are forbidden from this preflight input.

## Command

```bash
python3 scripts/v56_toledynamic_sample_preflight.py run \
  <controlled-workspace>/sample_manifest.tsv \
  --outdir <controlled-workspace>/sample_preflight \
  --fail-on-block
```

For every parent-trial, assay, and cell-type group, the preflight reports paired
baseline/month-3 counts by arm and whether arm is perfectly nested in site or
batch. A group is metadata-eligible for a randomized contrast only if both arms
have at least one pair and neither factor perfectly predicts arm.

If no assay group is eligible, the top-level result is `BLOCKED`; syntactic
completeness cannot be mistaken for scientific analyzability.

This deliberately weak minimum does not assert adequate power or assay quality.
The full analysis still requires participant counts and uncertainty, missingness
and RNA-subset audits, module coverage, value-level QC, influence checks, and
the frozen multiplicity gate. A preflight-eligible group may therefore still be
rejected.

## Synthetic Verification

```bash
python3 scripts/v56_toledynamic_sample_preflight.py synthetic-check \
  --outdir analysis/v56_toledynamic_sample_preflight \
  --fail-on-error
```

The deterministic synthetic fixtures test balanced, arm-batch-confounded,
missing-pair, and duplicate-sample manifests. They contain no biological values
and test only fail-closed preflight behavior.
