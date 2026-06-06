# UC_STATIC_DYNAMIC_APC_DECOUPLING_V11

Status: V11 resolution of matrix cell
`001_ulcerative_colitis_axis_01_ifn_apc_vs_axis_07_treatment_response`.

## Question

Why is ulcerative colitis near MS on IFN/APC antigen-presentation state but
contradictory on treatment-response architecture?

Supported V11 placements:

- `axis_01_ifn_apc`: UC `near/robust/high`, colon myeloid,
  cross-sectional.
- `axis_07_treatment_response`: UC `contradictory/supported/medium`,
  intestinal mucosa, treatment perturbation.

## Evidence

### UC Is Near MS On Cross-Sectional Colon Myeloid IFN/APC State

V8 evidence registry:

- Colon myeloid `mixscale_validated_ifng_readout`: delta `0.4433`, Hedges g
  `3.271`, p `0.000116`, axis-local FDR `0.0250`, `6` UC cases and `6`
  controls.
- Colon myeloid `ifn_apc`: delta `0.4847`, Hedges g `2.359`, p `0.00130`,
  axis-local FDR `0.0525`, `6` UC cases and `6` controls.

Interpretation:

- UC has a strong inflammatory IFN/APC state in colon myeloid cells.
- This is a disease-state marker and is cross-sectional, not a response
  prediction result.

### UC Treatment Response Is Contradictory Only If Static And Dynamic Features Are Collapsed

V7/V8 validation evidence:

- `GSE12251` UC baseline mucosal `baseline_IFN_APC`: AUC `0.250`, Hedges g
  `-1.043`, p `0.0195`, n `22`; failed as a baseline predictor.
- `GSE16879` IBD infliximab paired mucosa `-delta_IFN_APC`: AUC `0.754`,
  Hedges g `0.985`, p `0.000365`, n `60`; passed as early dynamic predictor.
- `GSE73661_IFX` UC infliximab paired mucosa `-delta_IFN_APC`: AUC `0.825`,
  Hedges g `1.390`, p `0.0127`, n `23`; passed as early dynamic predictor.
- `GSE73661_VDZ` exploratory vedolizumab week-6 mucosa `-delta_IFN_APC`: AUC
  `0.889`, Hedges g `1.286`, n `24`; same direction but exploratory and not
  part of the locked V7 validation.

Interpretation:

- Baseline IFN/APC height and early IFN/APC downshift are different biological
  quantities.
- The contradictory treatment-response placement is not evidence that IFN/APC
  is incoherent in UC. It is evidence that static inflammatory state and
  dynamic response plasticity should not be combined into one biomarker.

## Artifact Audit

Compartment:

- Axis 1 uses colon myeloid single-cell/single-nucleus evidence.
- Axis 7 uses intestinal mucosal biopsy expression.
- This is not perfectly matched. However, both axes are gut tissue rather than
  blood, and the treatment-response feature is a within-tissue early delta.
- Residual risk: treatment biopsy signal may reflect epithelial/stromal/immune
  composition rather than APC-intrinsic plasticity.

Cohort:

- Axis 1 cross-sectional evidence comes from local UC colon myeloid atlas rows.
- Axis 7 uses independent treatment-response cohorts.
- This reduces single-cohort artifact risk, but prevents direct within-person
  demonstration that high baseline colon myeloid IFN/APC and dynamic downshift
  are decoupled in the same patients.

Measurement grade:

- The mismatch is central: cross-sectional disease-state versus
  treatment-perturbation response.
- V11 classification treats this as the biological content only because the
  treatment-response evidence independently separates baseline failure from
  early-delta success across multiple cohorts.

## Hostile Critique

Criticism:

- The cell may be a semantic artifact: of course cross-sectional inflammation
  and treatment response are different axes.

Response:

- The objection is partly correct. This cell is not a direct causal mechanism.
  The resolved V11 claim is narrower: **baseline IFN/APC height must not be
  transferred to MS as a response stratifier merely because UC and MS are near
  on cross-sectional IFN/APC state**.

Criticism:

- Early IFN/APC downshift could be generic mucosal healing, not APC plasticity.

Response:

- Accepted. The V11 mechanism is phrased as dynamic inflammatory-state
  downshift / repair monitoring, not APC-intrinsic plasticity. APC-intrinsic
  plasticity requires single-cell paired treatment data.

Criticism:

- GSE16879 includes IBD rather than UC-only.

Response:

- Accepted. The UC-specific locked support is GSE12251 baseline failure and
  GSE73661_IFX early-delta success; GSE16879 supports the broader IBD mucosal
  pattern.

## Classification

V11 status: `intervention_derived`.

Resolved statement:

> UC is near MS on inflammatory IFN/APC state, but treatment-response transfer
> depends on dynamic IFN/APC downshift rather than baseline IFN/APC height.

This is a biological/measurement-class decoupling, not an artifact-only
dissolution and not a therapeutic claim.

## Mechanistic Explanation

Static IFN/APC height marks active inflammatory tissue state. Early IFN/APC
downshift marks transition away from inflammatory mucosal state during
successful therapy. These can decouple because baseline inflammatory load does
not by itself encode whether the tissue can remodel under a given therapeutic
perturbation.

Falsifiable prediction:

- In paired mucosal single-cell treatment-response data, baseline IFN/APC-high
  myeloid states will correlate with inflammation severity, while early
  downshift in IFN/APC-high myeloid or mixed inflammatory compartments will
  correlate more strongly with healing/response than baseline level.

Stop-loss:

- If two independent paired UC mucosal treatment cohorts show AUC `<0.60` or
  opposite direction for early `-delta_IFN_APC`, the dynamic-downshift
  interpretation is downgraded.

## MS Transfer Consequence

What transfers to MS:

- A trial-design warning: use early compartment-relevant IFN/APC delta as a
  pharmacodynamic readout candidate, not baseline IFN/APC height as a
  stratifier.

What does not transfer to MS:

- Baseline UC mucosal IFN/APC response prediction.
- Generic anti-TNF logic, because anti-TNF is clinically hazardous in MS.
- Generic broad microbiome transfer, because V9 did not support shared broad
  taxonomic dysbiosis after participant-aware inference.

MS-specific test:

- In paired early-treatment MS CSF, lesion-edge, or other compartment-relevant
  immune transcriptomics, responders or repair-stable patients should show
  larger early `-delta_IFN_APC` than nonresponders.

Stop-loss:

- AUC `<0.60` or opposite direction in two independent MS paired-compartment
  cohorts.
