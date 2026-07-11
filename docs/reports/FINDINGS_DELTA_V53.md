# Findings Delta V53

Status: current evidence regrade. This document does not rewrite the historical
V26, V37, or V52 artifacts; it records what V53 changes after source-level
definition-overlap and evidence-lineage audits.

## Headline

The original claim of an independently coupled HLA-II versus MIF/CD74
receptor-state two-arm architecture is **demoted to not-supported under strict
disjoint-readout testing**. Three source-level layers fail their applicable
gates. The fourth, pharmacodynamics, retains pooled/rank concordance but fails a
portable-common-effect gate. The V26 cross-disease summary is a derived atlas,
not an independent fifth modality.

This does **not** change the immutable V22 scalar, its validation plan, or the
negative-established V27/V28 result that coupled complexity does not outperform
the scalar.

## Source-Level Regrade

| layer | original to disjoint result | corrected verdict |
|---|---|---|
| Perturbation | HLA/receptor rho `0.798` to `0.647`; global `q=0.0099`, but within-stimulus `q=0.7665` | Fails context-preserving coupling gate. |
| Cell state | rho `0.832` to `0.175`, `q=0.582`; attenuation CI `-1.380` to `-0.051` | Definition-overlap-sensitive; fails. |
| Treatment response | rho `0.878` to `-0.059`; global `q=0.807`, stratified `q=0.671`; attenuation CI `-1.361` to `-0.411` | Definition-overlap-sensitive; fails. |
| Pharmacodynamics | rho `0.758` to `0.535`; global `q=0.0150`, dataset-stratified `q=0.0231` | Disjoint rank association persists, but portability fails: centered rho `0.087`, `p=0.808`, cluster CI `-0.617` to `0.894`. |
| Cross-disease summary | Exact rebuild; `108/170` rows reuse direct h5ad and six matrix rows are derived summary metrics | Retired as independent corroboration; descriptive atlas only. |

## What Remains Supported

Source-level rescoring with globally disjoint genes across eight physical
cross-disease datasets supports positive direction recurrence for:

- IFN/APC: `7/8`, exact one-sided `p=0.0352`, BH `q=0.0703`.
- CD44/CXCR4 receptor state: `7/8`, exact one-sided `p=0.0352`, BH `q=0.0703`.

HLA-II does not pass that recurrence gate (`5/8`, `q=0.363`), nor does the
lysosomal module (`6/8`, `q=0.193`). The retained result is therefore a broad,
non-MS-specific IFN/receptor-state backdrop. It is not evidence for an
independent HLA-II two-arm mechanism, causal direction, treatment benefit, or a
therapeutic target.

Subsequent frozen-score testing adds a distinct MS-specific update: the
CD44/CXCR4 **state association** is same-direction in two independent public
Macnair matrices. The validation composite passes explicit microglia-depth and
joint-component adjustment; the larger discovery cohort passes the frozen
primary and all minimum-cell thresholds but is borderline after direct
cell-count adjustment (`p=0.05398`). This supports a replicated state marker
with a quality qualification, not a receptor-specific mechanism or target.

## Current Wording

Use:

> Held data support broad cross-disease IFN/APC and CD44/CXCR4 receptor-state
> recurrence. Independent MS brain cohorts also reproduce the CD44/CXCR4 state
> association, with microglial-yield sensitivity in the larger cohort. The
> previously reported independently coupled HLA-II/receptor two-arm architecture
> is not robust to source-level disjoint-readout and portability tests.

Do not use:

> A robust coupled HLA-II/MIF-CD74 architecture is established across
> modalities.

## Consequences

1. V22 remains the unchanged external-validation target; V53 changes only its
   surrounding mechanistic interpretation.
2. MIF/CD74 remains a tone-loaded state context, not a component-specific or
   direction-resolved target.
3. V26/V37/V52 remain historical records. Current summaries must link this
   delta whenever they cite their coupled-architecture conclusion.
4. No therapeutic lead is promoted by this regrade.
5. The CD44/CXCR4 state marker advances to replicated-with-quality-
   qualification; its component mechanism and intervention direction remain
   unresolved.

## Rerunnable Evidence

- `analysis/v53_deoverlapped_module_sensitivity/`
- `analysis/v53_cell_state_deoverlap_sensitivity/`
- `analysis/v53_treatment_response_deoverlap_sensitivity/`
- `analysis/v53_pharmacodynamic_deoverlap_sensitivity/`
- `analysis/v53_pharmacodynamic_edge_robustness/`
- `analysis/v53_cross_disease_summary_lineage_audit/`
- `analysis/v53_additional_atlas_disjoint_rescoring/`
- `analysis/v53_ms_microglia_independent_cohort_scout/`
