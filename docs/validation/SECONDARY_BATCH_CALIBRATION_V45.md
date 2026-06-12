# Secondary-Lead Batch Diagnostic Calibration V45

Status: synthetic method-characterization only. This does not change any locked
rule, frozen pre-registration, or biological claim.

## Purpose

V45 stress-tested the postpartum APC-arm and T/B compartment secondary harnesses
under synthetic data pathologies. Those tests showed that response-correlated
technical structure can create false positives and that batch guards are
therefore required. They also showed the expected downside of conservative
guarding: in small planted-signal cohorts, chance technical flags can downgrade
otherwise valid synthetic signals.

This run tests whether a permutation-calibrated batch flag improves that
tradeoff for the secondary leads.

## Inputs

Synthetic inputs only:

- `analysis/v45_postpartum_pathology/synthetic/postpartum_pathology_subjects.tsv.gz`
- `analysis/v45_postpartum_pathology/postpartum_pathology_metrics.tsv`
- `analysis/v45_tb_compartment_pathology/synthetic/tb_compartment_pathology_subjects.tsv.gz`
- `analysis/v45_tb_compartment_pathology/tb_compartment_pathology_metrics.tsv`

Script:

- `scripts/v45_secondary_batch_calibration.py`

Run:

```bash
.venv/bin/python scripts/v45_secondary_batch_calibration.py --n-perm 50
```

Scale:

- Seed: `45545`
- Cohorts: `12,600`
- Permutations per batch test: `50`
- Output directory: `analysis/v45_secondary_batch_calibration/`

## Method

For each synthetic cohort, the script recomputes a batch diagnostic against the
lead-specific locked score:

- postpartum APC-arm: `postpartum_apc_risk_score` versus
  `postpartum_relapse_3m`
- T/B compartment: `b_plasma_locked_delta` versus `responder`

The existing diagnostic flags a cohort if any of these hold:

- batch metadata AUC for response is at least `0.60`
- absolute Spearman correlation between batch and score is at least `0.35`
- score AUC attenuation after batch residualization is at least `0.05`

The calibrated sensitivity flag keeps the existing diagnostic but requires the
minimum of two permutation p-values to be `<= 0.10`:

- permutation p-value for response-batch association
- permutation p-value for batch-score correlation

The calibrated guard is evaluated against the prior synthetic pass/fail calls;
it is not used to change any real validation rule.

## Results

Overall:

| Metric | Existing Guard | Calibrated Guard |
|---|---:|---:|
| Worst synthetic-null guarded clean pass rate | `0.0222` | `0.0333` |
| Best planted guarded clean pass rate | `0.9111` | `0.9556` |

Postpartum APC-arm:

- Worst calibrated synthetic-null clean pass: `0.0333`, in
  `steroid_response_correlated` at severity `0.50`.
- Worst existing synthetic-null clean pass: `0.0222`, in
  `combined_steroid_dmt_batch` at severity `0.00`.
- Best calibrated planted clean pass: `0.9556`, in
  `missing_postpartum_timepoint` at severity `0.50`.
- Mean planted clean pass improves from `0.6394` to `0.6851`.

T/B compartment:

- Worst calibrated synthetic-null clean pass: `0.0111`, unchanged from the
  existing guard, in `compartment_label_noise` at severity `0.50`.
- Best calibrated planted clean pass: `0.9333`, in
  `b_fraction_response_correlated` at severity `0.00`.
- Mean planted clean pass improves from `0.5438` to `0.5848`.

## Verdict

The permutation-calibrated guard is useful as a secondary sensitivity readout,
but it is not strong enough to replace the stricter existing guard.

Reason: calibration improves planted-signal retention, but in the postpartum
APC-arm grid it also raises the worst synthetic-null clean-pass rate from
`0.0222` to `0.0333`. That increase is small, but V45's role is readiness
hardening, not relaxing guards. The correct additive tightening is therefore:

1. Keep the existing stricter secondary-lead batch guard as the primary
   validation gate.
2. Report the q-calibrated guard as an exploratory/sensitivity diagnostic if a
   future secondary-lead validation is otherwise downgraded only by a marginal
   batch flag.
3. Do not let the calibrated sensitivity result rescue a cohort with clear
   response-correlated batch, missing required timepoints, or inadequate module
   coverage.

## Outputs

- `analysis/v45_secondary_batch_calibration/secondary_batch_calibration_metrics.tsv`
- `analysis/v45_secondary_batch_calibration/secondary_batch_calibration_summary.tsv`
- `analysis/v45_secondary_batch_calibration/summary.json`

