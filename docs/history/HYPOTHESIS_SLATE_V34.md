# Hypothesis Slate V34

Date: 2026-06-07

## Scope

V34 deepens V33 rather than generating another broad slate. The two concrete
tasks were:

1. Fix Gemini generation so two-lineage review can run without silently
   committing truncated outputs.
2. Deepen the top V33 hypothesis: postpartum HLA-II/CD64 APC split as a
   relapse-window state.

No locked rule was edited and no reserved fresh validation cohort was read.

## Phase 0: Gemini Generation Fix

V33 failure mode: Gemini smoke-passed, but longer generation outputs were
truncated and malformed. The root cause is now explicit: Gemini responses can
finish with `MAX_TOKENS`. The previous client returned the first text part
without checking the finish reason, so partial JSON could be written silently.

Client fix:

- `scripts/sap_ai_core_client.py` now concatenates all Gemini text parts.
- It checks `finishReason` / `finish_reason`.
- It raises a clear error if Gemini ends by `MAX_TOKENS` or `LENGTH`.
- It adds `debug-gemini`, which prints non-secret response-shape diagnostics
  and can optionally write the raw non-secret payload for schema inspection.

Verification:

- Low-token rerun of the V33 short generation now fails loudly with:
  `Gemini response ended by MAX_TOKENS; increase --max-output-tokens or shorten prompt`.
- Higher-token generation is rerun in V34 and recorded in
  `analysis/v34_gemini_generation_fixed.json`; it passed JSON validation.

## Phase 1: Two-Lineage Cross-Check

The V33 shortlist was sent independently to Claude and Gemini for ranking and
fatal-weakness/strongest-test review.

Artifacts:

- `analysis/v34_crosscheck_prompt.md`
- `analysis/v34_claude_crosscheck.json`
- `analysis/v34_gemini_crosscheck.json`

Gemini returned complete content but wrapped it in markdown fences, so raw
`json.tool` validation fails unless the fences are stripped. This is a format
compliance issue, not the V33 truncation failure.

Cross-lineage ranking:

| Hypothesis | Claude rank | Gemini rank | Agreement |
|---|---:|---:|---|
| MS-SLE EBV/IFN APC imprint | 1 | 1 | strong agreement: high plausibility, hard causal attribution |
| Postpartum HLA-II/CD64 APC relapse-window state | 3 | 4 | medium agreement: plausible, best test is serial pregnancy/postpartum immune profiling with lesion/relapse timing |
| Complement/lipid progressive axis | 4 | 2 | both plausible; Gemini prioritizes more strongly |
| T/B compartment remodeling gate | 2 | 6 | divergence: Claude sees high plausibility, Gemini sees broad/less specific remodeling |
| Lysosomal APC-processing bottleneck | 5 | 5 | agreement: medium plausibility, needs HLA-II ligandome / lysosomal activity data |
| Metabolic/sterol setpoint | 6 | 3 | divergence: Gemini prioritizes sterol biology, Claude downranks due weak/inconsistent causal lipid evidence |

Interpretation: two-lineage cross-check changed the priority queue. The
strongest cross-lineage agreement is now **MS-SLE EBV/IFN APC imprint**, but it
is also the least locally grounded because the project lacks an EBV-response
module and EBV-stratified APC/B-cell data. The best locally grounded and
clinically anchored hypothesis remains **postpartum HLA-II/CD64 APC-arm
imbalance**, so V34 deepens that first.

## Phase 2: Postpartum HLA-II/CD64 APC Split

### Sharpened Prediction

If the postpartum HLA-II/CD64 APC split is relevant to MS relapse risk, then the
HLA-II-minus-CD64 decoupling trajectory should peak in the known postpartum
relapse-risk window, especially around early-to-mid postpartum timepoints, and
should be stronger as a time-trajectory state than as a same-day disease-
activity correlate.

### Grounding Data

Existing project artifact:

- `analysis/tier_0_triage/hyp_v6_007_gse235508_decoupling/key_postpartum_decoupling.tsv`
- `analysis/tier_0_triage/hyp_v6_007_gse235508_decoupling/disease_activity_correlations.tsv`

Key HLA-II-minus-CD64 decoupling contrasts versus trimester 3:

| Group | 6wk delta | 6wk g | 6wk p | 6mo delta | 6mo g | 6mo p | 12mo delta | 12mo g | 12mo p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Healthy | `0.358` | `0.775` | `0.0214` | `0.559` | `1.286` | `0.000304` | NA | NA | NA |
| SLE | `0.203` | `0.320` | `0.349` | `0.521` | `0.890` | `0.0131` | `0.325` | `0.446` | `0.282` |
| SNRA | `0.367` | `1.083` | `0.0305` | `0.349` | `0.843` | `0.0995` | `0.164` | `0.454` | `0.587` |
| SPRA | `0.776` | `1.701` | `0.000068` | `0.928` | `2.038` | `0.000009` | `0.972` | `1.932` | `0.00463` |

Component interpretation:

- Healthy decoupling is driven mostly by CD64 fall, with modest/non-significant
  HLA-II rise.
- SLE decoupling at 6 months is driven by CD64 fall, not HLA-II rise.
- SPRA decoupling is driven mostly by HLA-II rebound; CD64 does not fall at
  6 months and rises by 12 months.
- SNRA decoupling weakens by 12 months.

### V34 Grounded Result

Status: **supported as postpartum immune-state trajectory, still unproven for
MS relapse**.

The deeper read strengthens the time-window concept: multiple disease/healthy
groups show positive HLA-II-minus-CD64 decoupling in early/mid postpartum
timepoints, and SPRA has a very large sustained effect. It also shows the
mechanism is not uniform: the same decoupling index can be produced by HLA-II
rebound, CD64 fall, or both. That heterogeneity matters for MS. The hypothesis
should therefore be framed as **APC-arm imbalance trajectory**, not a single
universal HLA-II-up/CD64-down rule.

Same-day disease-activity correlations from the prior V6 check were weak, so
the correct MS test is not cross-sectional EDSS/relapse status. The correct
test is time-to-relapse or relapse-within-window after delivery.

### Artifact Risks

- Pregnancy/lactation, treatment interruption, steroid exposure, infection, and
  cell-composition shifts can alter CD64 and HLA-II.
- Existing data are RA/SLE/healthy, not MS.
- The decoupling index is directionally interpretable only if both component
  arms are reported separately.

### Required Next Data

Minimum decisive dataset:

- MS pregnancy/postpartum blood or CSF expression, cytometry, or CITE-seq.
- Timepoints: trimester 3, 6 weeks postpartum, 3-6 months postpartum, ideally
  12 months postpartum.
- Outcome: relapse within 3-6 months postpartum or time-to-first postpartum
  relapse.
- Metadata: DMT stop/restart timing, steroid exposure, breastfeeding/lactation,
  infection, age, disease duration, baseline relapse activity, and cell counts.

Minimum test:

1. Compute HLA-II, CD64, and HLA-II-minus-CD64 trajectories.
2. Test whether trajectory slope or early postpartum delta predicts relapse
   within the postpartum risk window.
3. Adjust for cell-composition and glucocorticoid/steroid signatures using the
   V32-style audit panels.
4. Reject the hypothesis if relapse risk is not associated with the trajectory
   or is explained by steroid/composition artifacts.

## Re-Ranked Shortlist After V34

| Rank | Hypothesis | V34 status | Next action |
|---:|---|---|---|
| 1 | Postpartum HLA-II/CD64 APC-arm imbalance trajectory | strengthened as state trajectory, needs MS relapse labels | Search/acquire postpartum MS relapse-timing immune dataset |
| 2 | MS-SLE EBV/IFN APC imprint | two-lineage top plausibility, but currently data-limited | Build EBV/LMP1/EBNA-response module and test against MS/SLE B-cell/APC datasets |
| 3 | Complement/lipid progressive axis | cross-lineage plausible and supported structure, needs stage data | Mine progressive/chronic-active lesion datasets |
| 4 | T/B compartment remodeling gate | unchanged from V33; validation-design constraint | Test in sorted/single-cell MS DMT cohort |
| 5 | Lysosomal APC-processing bottleneck | supported by V26 dependencies; both models rate medium | Find APC perturbation data for cathepsin/V-ATPase/lysosomal flux |
| 6 | Metabolic/sterol setpoint | model-divergent; current metabolic proxies are insufficient | Score explicit sterol genes in APC-resolved data |

## V34 Verdict

The top exploratory hypothesis survives deeper grounding only as a **trajectory
and data-acquisition target**, not yet as an MS biomarker or therapeutic
hypothesis. The key refinement is mechanistic heterogeneity: postpartum
decoupling can arise from different arm movements in different diseases. Any MS
test must measure HLA-II and CD64 separately, not only the combined index.
