# Unconventional Findings V38

Block start UTC: 2026-06-08T20:30:23Z

Status: in progress.

V38 asks unconventional questions while keeping the evidence gate unchanged.
Model and RPT output are proposal sources only. Every claim below is grounded in
committed project data or explicitly marked blocked/inconclusive.

## Workstream B: Adversarial Self-Inversion

### B1. Inversion Of The Bounded V22/V23 Monitoring Signal

Status: **completed for first adversarial target**.

Question:

Could the project's strongest surviving lead, the bounded V22/V23 APC/HLA-II
early monitoring scalar, be better explained as an artifact than as a true
provisional validation lead?

Proposal sources:

- Claude and Gemini were prompted independently with a compact adversarial
  inversion prompt.
- Outputs:
  - `analysis/v38_adversarial_monitoring/claude_inversions.json`
  - `analysis/v38_adversarial_monitoring/gemini_inversions.json`
- Model output was used only to prioritize tests.

Grounding artifacts:

- Script: `scripts/v38_adversarial_monitoring_inversion.py`
- AUC set table:
  `analysis/v38_adversarial_monitoring/grounded_auc_sets.tsv`
- Inversion result table:
  `analysis/v38_adversarial_monitoring/grounded_inversion_results.tsv`
- Summary JSON:
  `analysis/v38_adversarial_monitoring/grounded_inversion_summary.json`

Grounded results:

| Inversion | Grounded result | Evidence | V38 delta |
|---|---|---|---|
| Bounded subset selection artifact | partially supported as scope limit | bounded DMF + exact tofacitinib AUC `0.811`, exact p `0.011`; primary locked all DMF + fingolimod + adalimumab AUC `0.547`; complement fingolimod + adalimumab AUC `0.557`, exact p `0.333` | Strengthens bounded-only wording; does not kill the bounded validation-lead status because V37 already scoped it as provisional and bounded. |
| Cross-disease exact tofacitinib drives the headline | supported as MS-specificity caveat | DMF-only AUC `0.720`, exact p `0.155`; exact tofacitinib-only AUC `0.950`, exact p `0.0159`; pooled bounded AUC `0.811` | Any MS-specific wording must be DMF-suggestive, not MS-validated. The Gafson DMF validation remains the decisive next step. |
| STAT1/metabolic/inflammatory tone explains independent APC specificity | partially supported | V32 broad immune-tone joint adjustment attenuates AUC to `0.656`, permutation p `0.163`; locked+confounders LOOCV AUC `0.733` still exceeds confounders-only `0.611` | Supports "immune-tone bounded" and "not APC/HLA-II-specific" wording; does not justify calling it a steroid or simple composition artifact. |
| Small-n winner's curse / family-wise fragility | partially supported for post-hoc extensions, not for the pre-locked scalar | V28 bounded scalar p `0.008`; Bonferroni across 9 V28 bounded methods would be `0.072`, but the scalar was locked before V28 method expansion | Reinforces no successor/post-hoc rule promotion. Does not invalidate the pre-locked scalar as a validation candidate. |
| Threshold calibration does not transfer across bounded cohorts | supported | DMF median threshold -> exact tofacitinib accuracy `0.667`; exact tofacitinib threshold -> DMF accuracy `0.600` | Blocks any clinical threshold claim. Keep as rank/direction monitoring candidate until fresh validation calibrates a threshold. |

Verdict:

The adversarial inversion **narrows but does not kill** the V37 claim. The
bounded monitoring scalar should be described as:

> bounded, small-n, partly immune-tone-conditioned, not MS-calibrated, not
> broad across therapies, and dependent on fresh DMF validation.

This is not a demotion relative to V37's honest framing. It is a useful stress
test that confirms the V37 wording should stay conservative and that the next
action remains frozen Gafson/DMF validation rather than building a successor
rule.

## V37-to-V38 Delta So Far

Strengthened:

- V37's conservative framing of the V22/V23 scalar survived direct adversarial
  inversion.
- The need for Gafson DMF validation is stronger, because the only MS-internal
  anchor is DMF-only AUC `0.720` with exact p `0.155`.

Weakened / narrowed:

- Any phrase implying "MS-validated" or "clinical threshold" is too strong.
- Any phrase implying APC/HLA-II specificity independent of broad
  STAT1/metabolic/inflammatory tone is too strong.

Demoted:

- No V37 item is demoted yet. The inversion supports V37's existing
  `provisional` grade for the bounded scalar.

## Pending Workstreams

- A. Failure-structure meta-analysis across killed/closed leads.
- B. Additional adversarial inversions: coupled APC architecture, MS-UC genetic
  backdrop, and layer-transfer map.
- C. Unpublishable-but-true exclusion/non-replication list.
- D. Cross-scale/control-systems reframing.
- E. RPT-led structural mining.
