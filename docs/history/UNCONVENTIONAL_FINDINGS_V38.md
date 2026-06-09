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

## Workstream A: Structure Of Failure

### A1. Failure-Mode Meta-Analysis Across V37 Negative/Closed Items

Status: **completed for V37 closed/negative item frame**.

Question:

Do the project's killed, closed, parked, and decoupling findings fail for a
common reason that itself reveals a constraint on MS biology or project
methodology?

Grounding artifacts:

- Script: `scripts/v38_failure_structure_meta.py`
- Input frame: `docs/reports/FINDINGS_SCORES_V37.tsv`
- Annotated failure table:
  `analysis/v38_failure_structure/failure_mode_table.tsv`
- Family counts:
  `analysis/v38_failure_structure/failure_family_counts.tsv`
- Mode counts:
  `analysis/v38_failure_structure/failure_mode_counts.tsv`
- Summary:
  `analysis/v38_failure_structure/failure_structure_summary.json`

Frame:

- V37 closed/negative/decoupling items analyzed: `20`.
- Categories included: `decoupling_negative` and `kills_closed`.
- Tags were explicit artifact-derived annotations, not model output.

Family-level results:

| Failure family | Items | Fraction | Interpretation |
|---|---:|---:|---|
| Evidence-resolution failure | `7` | `0.35` | The most common limit is not biological impossibility but insufficient causal resolution, full-QTL direction, held-out validation, or perturbation proof. |
| Context or axis dependence | `5` | `0.25` | Mechanisms often fail when moved across disease, tissue, therapy, baseline/dynamic state, or compartment. |
| Direction or modality constraint | `5` | `0.25` | Genetics and target leads often fail because the disease-protective direction is opposite, mixed, or requires hard restoration/up-function. |
| Specificity or control failure | `4` | `0.20` | Attractive broad module interpretations often fail under random controls, donor-aware tests, or distinct-causal-variant checks. |
| Complexity or modeling failure | `2` | `0.10` | More complex models or coupled successors fail to improve over simpler locked representations. |
| Marker-not-driver failure | `2` | `0.10` | Some attractive biology remains useful as covariate/readout, not as target. |

Most frequent individual tags:

- `module_specificity_failure`: `3` items.
- `transfer_invalid`, `hard_protective_direction`, `causal_gene_ambiguity`,
  `axis_mismatch`, `baseline_not_dynamic`, `compartment_mismatch`: `2` items
  each.

Verdict:

There is **no single universal failure mechanism**. The common structure is a
three-part constraint:

1. MS-adjacent mechanisms are highly context/axis dependent.
2. Therapeutic genetics often points toward hard directions: restoration,
   up-function, signal-specific modulation, or opposite disease directions.
3. Broad module stories collapse unless they survive specificity, donor-aware,
   full-QTL, or held-out validation gates.

This is decision-useful because it predicts where future leads should be
skeptically pre-filtered. A new lead should be penalized immediately if it
requires cross-axis transfer, restoration/up-function without modality, or broad
module interpretation without a matched specificity control.

## V37-to-V38 Delta So Far

Strengthened:

- V37's conservative framing of the V22/V23 scalar survived direct adversarial
  inversion.
- The need for Gafson DMF validation is stronger, because the only MS-internal
  anchor is DMF-only AUC `0.720` with exact p `0.155`.
- V37's broad discipline is strengthened by the failure-structure result: most
  dead ends were not random; they cluster around context/axis transfer, evidence
  resolution, and direction/modality constraints.

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
