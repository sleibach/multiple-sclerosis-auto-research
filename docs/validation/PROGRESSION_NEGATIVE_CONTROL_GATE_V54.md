# V54 Progression Negative-Control Gate

Status: additive blind process guard. It changes no locked rule,
pre-registration, primary endpoint, or primary model.

## Purpose

A future P1 package can generate a convincing association through leakage,
generic transcriptomic structure, endpoint nonspecificity, informative
follow-up, or site/batch structure. The negative-control family must therefore
be fixed before molecular scores or individual outcomes are opened.

Negative controls are diagnostic and non-rescuing. Passing them does not prove
causality, progression specificity, or treatment relevance. Failing them has a
predeclared consequence and cannot be hidden because the primary result is
favorable.

## Exact Seven-Control Family

1. `subject_blocked_score_permutation`: permute complete subject-level score
   trajectories within source cohort, collection site, and treatment stratum;
   preserve repeated-measure blocks.
2. `matched_random_module_bank`: 100 modules per seed, matched on module size,
   detected-gene count, mean expression, and variance, excluding primary genes;
   compare with max-T rather than selecting a favorable random set.
3. `unconfirmed_transient_worsening`: report association with candidate
   worsening that fails confirmation.
4. `relapse_associated_worsening`: report association with worsening inside the
   frozen relapse window; it is not PIRA.
5. `pre_index_progression_event`: report association with disability events
   preceding the molecular index; this diagnoses baseline burden/selection and
   is not a causal temporal negative proof.
6. `attendance_censoring_process`: test score association with attendance,
   missing confirmation, and censoring/death process under the frozen event-
   time family.
7. `site_batch_quality_process`: test residual score association with site,
   batch, platform, RIN/quality, and library depth after the frozen blind
   harmonization route.

Use fixed seeds `55451/55453/55459`, at least 10,000 blocked permutations per
seed, and the exact 100-module bank per seed. Diagnostic endpoint/process
p-values use Holm across the fixed family; the random bank uses max-T. Every
control and the primary are reported.

## Predeclared Actions

| control result | mandatory action |
|---|---|
| blocked permutation or random-bank calibration fails | `PRIMARY_INFERENCE_INVALID` |
| attendance/censoring process association survives correction | `EVENT_TIME_INFERENCE_FAIL_CLOSED` |
| site/batch/quality process association survives correction | `TRANSPORT_OR_TECHNICAL_INTERPRETATION_FAIL_CLOSED` |
| transient, relapse-associated, or pre-index endpoint association survives correction | `PROGRESSION_SPECIFICITY_DOWNGRADE` |
| all controls pass | retain the primary's own grade only; no upgrade |

Endpoint diagnostics can be biologically associated for legitimate reasons;
therefore their positive result downgrades specificity rather than proving
artifact. Process-control failures are more severe because they invalidate the
corresponding inference route.

## Machine Gate

Run synthetic regression:

```bash
.venv/bin/python scripts/v54_progression_negative_control_gate.py
```

Validate a blind declaration:

```bash
.venv/bin/python scripts/v54_progression_negative_control_gate.py \
  --declaration path/to/negative_control_declaration.json \
  --output-dir path/to/negative_control_gate --fail-on-error
```

The default fixtures contain no patient data. A pass establishes only that the
family, null construction, reporting, and failure actions were frozen before
access. It is not evidence that the controls are null in MS or that the primary
state predicts or can halt progression.
