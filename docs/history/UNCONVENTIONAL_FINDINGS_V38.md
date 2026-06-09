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

## Workstream E: RPT-Led Structural Mining

### E1. RPT Mining Over V37 Score Table And V38 Failure Annotations

Status: **completed for V37 score-table action-class probe**.

Question:

Does the tabular structure of the V37 scored findings table surface a pattern
or contradiction that the narrative synthesis missed?

Grounding artifacts:

- Script: `scripts/v38_rpt_structural_mining.py`
- Payload:
  `analysis/v38_rpt_structural_mining/v38_rpt_payload.json`
- Response:
  `analysis/v38_rpt_structural_mining/v38_rpt_response.json`
- Masked predictions:
  `analysis/v38_rpt_structural_mining/v38_rpt_masked_predictions.tsv`
- Grounded summary:
  `analysis/v38_rpt_structural_mining/v38_rpt_grounded_summary.json`

Method:

The table used V37 relevance, novelty, evidence grade, provisional/negative
flags, data-gap flags, transfer-warning flags, and V38 failure-table membership.
Six edge items were masked:

- bounded APC/HLA-II scalar;
- T/B-readable early IFN/APC/STAT1 state;
- postpartum HLA-II/CD64 APC-arm imbalance;
- ZMIZ1;
- PTGER4;
- V25 simulator negative.

Result:

- Masked rows: `6`.
- RPT predictions matching the artifact-derived V37 action class: `5/6`.
- Sole contradiction: the bounded APC/HLA-II scalar.
  - V37 true class: `external_validation_priority`.
  - RPT prediction: `data_gated_followup`, confidence `0.88`.

Interpretation:

RPT mostly rediscovered the V37 action taxonomy. The single contradiction is
useful: tabularly, the bounded scalar looks like other provisional,
data-gated follow-ups. Its "external validation priority" status is not earned
by generic table structure; it is earned by clinical relevance, pre-locking,
and the fact that a concrete Gafson/DMF validation path exists.

Verdict:

RPT does **not** demote the bounded scalar, because RPT output is not evidence.
It does sharpen the wording:

> The scalar is the top operational validation priority, not a structurally
> exceptional finding in the score table.

No V37 score changes are made.

## Workstream C: Unpublishable-But-True Exclusions

### C1. Conservative Exclusion / Non-Replication Ledger

Status: **completed first ledger**.

Question:

What has the project established is **not** supported as a target, biomarker,
transfer rule, or modeling capability under current data?

Grounding artifacts:

- Script: `scripts/v38_exclusion_ledger.py`
- Ledger:
  `analysis/v38_exclusion_ledger/exclusion_nonreplication_ledger.tsv`
- Counts:
  `analysis/v38_exclusion_ledger/exclusion_counts.tsv`
- Summary:
  `analysis/v38_exclusion_ledger/exclusion_summary.json`

Result:

- Exclusions/non-replications recorded: `16`.
- Strength counts:
  - `negative_established`: `13`;
  - `supported_exclusion`: `2`;
  - `data_gated_not_established`: `1`.

Decision-useful exclusions:

1. Baseline IFN/APC is not a valid general fallback stratifier.
2. The V22 scalar is not a broad cross-therapy response rule.
3. The V22 scalar is not a calibrated clinical threshold.
4. Glucocorticoid/steroid signature does not explain the bounded scalar.
5. Simple marker-level cell composition does not explain the bounded scalar.
6. Receptor-only CD74/CD44/CXCR4 does not dominate the scalar.
7. Coupled/dynamic/flexible ML variants do not improve over the scalar.
8. A broad immune-state simulator is not validated from current data.
9. No load-bearing invariant was established.
10. PTGER4 is not a clean MS-UC transfer target.
11. MHC/HLA overlap is not simple shared causal biology.
12. EBV/IFN APC imprint is not EBV-specific in current data.
13. Complement/lipid progressive axis is not supported as a combined axis.
14. NAMPT/eNAMPT is not reactivated as an MS target.
15. REL/PUS10/USP34 chr2 is not a current shared-locus lead.
16. ZFP36L1 chr14 is not robust enough for lead status.

Verdict:

This is the most "unpublishable but true" V38 product so far. The project has
created a reliable stop-spending ledger. Most entries do not mean the biology is
irrelevant to MS; they mean a specific translational interpretation is not
supported:

- not a target;
- not a general rule;
- not a clinical threshold;
- not a clean transfer locus;
- not EBV-specific;
- not validated as a simulator;
- not robustly colocalized.

This ledger should be used before any future wet-lab or data-acquisition spend.
If a proposed experiment reopens one of these exclusions, it must name the exact
new evidence that would override the current ledger.

## Workstream D: Cross-Scale / Control-Systems Reframing

### D1. Baseline Load vs Dynamic Control Action vs Treated Set-Point

Status: **completed first control-systems probe**.

Question:

Is the bounded V22/V23 monitoring signal better read as a control-system
behavior: baseline immune load, early corrective action, or movement toward a
treated immune set-point?

Grounding artifacts:

- Script: `scripts/v38_control_system_reframing.py`
- Input table:
  `analysis/v32_confounder_audit/v32_subject_confounder_scores.tsv`
- Feature tests:
  `analysis/v38_control_system/control_feature_tests.tsv`
- Family tests:
  `analysis/v38_control_system/control_feature_family_tests.tsv`
- Set-point tests:
  `analysis/v38_control_system/setpoint_distance_tests.tsv`
- Summary:
  `analysis/v38_control_system/control_system_summary.json`

Frame:

- Subjects: `19` bounded V22/V23 cases.
- Responders / non-responders: `10 / 9`.
- Cohorts: GSE235357 DMF (`10`) and exact-module GSE253006 tofacitinib (`9`).
- Tested scalar features: `54`.
- Feature-level tests used exact label permutations preserving responder count.
- Supervised set-point distances used fixed-seed Monte Carlo label permutation
  with the responder centroid recomputed on each permutation.

Results:

| Framing | Best grounded result | Multiplicity-aware interpretation |
|---|---|---|
| Early dynamic/control action | Locked signed score AUC `0.811`, exact p `0.022` | Strongest simple scalar, but within-family max-AUC p `0.190` over 14 early-delta features and all-feature BH q `0.397`. |
| Treated-state features | Treated IFN/APC AUC `0.811`, exact p `0.022`; treated proliferation AUC `0.811`, exact p `0.022` | Similar apparent signal, but within-family max-AUC p `0.196`; not a rule-level improvement over the locked scalar. |
| Baseline-load features | Best baseline feature AUC `0.667`, exact p `0.243` | Baseline load remains weak; no support for converting the monitoring signal into a baseline stratifier. |
| Negative-feedback features | Best feedback feature AUC `0.778`, exact p `0.043` | Does not survive within-family max-AUC correction (`p=0.402`). |
| Responder set-point proximity | Treated IFN/HLA-II/STAT1/metabolic proximity AUC `0.867`, Monte Carlo p `0.0098`; treated composition proximity AUC `0.833`, p `0.0286` | Interesting control-systems hypothesis, but supervised/in-sample: the responder centroid is learned from the same small cohorts. It is a candidate validation readout, not established evidence. |

Verdict:

The data support a **dynamic/treated-state interpretation over baseline load**,
but they do not justify a new rule or a demotion of the locked scalar. The
control-systems view is useful mainly as framing:

- responders look more like they move toward a treated immune set-point;
- baseline state alone is not sufficient;
- the apparent set-point signal needs fresh external validation because its
  centroid is learned from the same `n=19` bounded cases.

V38 delta:

The V37 conclusion is **strengthened in one narrow way**: the signal is still
dynamic, not baseline. It is also narrowed: any set-point/feedback wording must
be explicitly exploratory until tested on Gafson/DMF or another fresh cohort.

## V37-to-V38 Delta So Far

Strengthened:

- V37's conservative framing of the V22/V23 scalar survived direct adversarial
  inversion.
- The need for Gafson DMF validation is stronger, because the only MS-internal
  anchor is DMF-only AUC `0.720` with exact p `0.155`.
- V37's broad discipline is strengthened by the failure-structure result: most
  dead ends were not random; they cluster around context/axis transfer, evidence
  resolution, and direction/modality constraints.
- RPT independently treats the bounded scalar as data-gated rather than
  intrinsically exceptional, reinforcing that its priority is operational and
  clinical, not a reason to inflate evidence grade.
- The exclusion ledger strengthens the negative side of V37: the project now
  has an explicit "do not pursue without new evidence" list rather than a set of
  scattered closed-lead notes.
- The control-systems probe strengthens the dynamic-over-baseline reading of
  the monitoring lead: baseline-load features are weak, while early-delta and
  treated-state features carry the apparent signal.

Weakened / narrowed:

- Any phrase implying "MS-validated" or "clinical threshold" is too strong.
- Any phrase implying APC/HLA-II specificity independent of broad
  STAT1/metabolic/inflammatory tone is too strong.
- Any phrase implying a validated immune set-point rule is too strong; the
  set-point result is supervised and in-sample.

Demoted:

- No V37 item is demoted yet. The inversion supports V37's existing
  `provisional` grade for the bounded scalar.

## Pending Workstreams

- B. Additional adversarial inversions: coupled APC architecture, MS-UC genetic
  backdrop, and layer-transfer map.
- D. Additional cross-domain reframings if they yield concrete grounded tests.
