# Coupled APC-Axis V27

Date: 2026-06-07

Status: feature definitions frozen before V27 scalar-vs-coupled response comparison.

## Purpose

V26 showed a replicated coupled APC remodeling structure linking `hla_ii_apc`, `ifn_apc`, `mif_cd74_receptor_state`, IFN readout, and lysosomal APC. V27 tests whether a fixed coupled-axis representation improves response monitoring over the immutable V22 scalar rule in already-held V22/V23 cohorts.

This document freezes the candidate coupled representations before any V27 response-prediction comparison.

## Immutable Baseline

The baseline comparator is `LOCKED_RULE_V22.md`.

Available paired-score columns in V22/V23 held data:

- `delta_IFN_APC`
- `delta_HLAII`
- `delta_RECEPTOR`
- `locked_signed_score`

The V22 scalar is:

- Class A: `-delta_IFN_APC`
- Class B: `delta_HLAII`
- Class C: `delta_HLAII - delta_IFN_APC`

V27 does not edit this rule.

## MIF/CD74 Proxy Limitation

The V22/V23 paired-score tables do not contain a separately scored `mif_cd74_receptor_state` module. They contain `delta_RECEPTOR`, defined from `CD74`, `CD44`, and `CXCR4`, originally used as a specificity control. V27 uses `delta_RECEPTOR` as the only available receptor-state proxy for MIF/CD74 coupling.

This is a limitation. A future validation cohort should compute the full V26 coupled module set directly, including the exact MIF/CD74 receptor-state module.

## Frozen V26 Weights

V26 supported a positive APC-remodeling axis in treatment pharmacodynamics and h5ad cell state. For modules present in V22/V23 paired scores, the positive loadings were:

| Module | Treatment pharmacodynamic PC1 | h5ad cell-state PC1 | Mean positive loading |
|---|---:|---:|---:|
| `ifn_apc` | 0.468457 | 0.431410 | 0.449934 |
| `hla_ii_apc` | 0.212755 | 0.326709 | 0.269732 |
| `mif_cd74_receptor_state` proxy by `delta_RECEPTOR` | 0.224456 | 0.327434 | 0.275945 |

Normalize these mean positive loadings to sum to one:

- `w_ifn = 0.4519`
- `w_hla = 0.2709`
- `w_receptor = 0.2772`

These weights are fixed and are not fitted to response labels.

## Candidate Coupled Representations

V27 evaluates three pre-specified fixed representations. Because multiple candidates are tested, the permutation null uses the maximum coupled-minus-scalar improvement across all three representations when judging whether any coupled feature truly improves.

### Candidate 1: `coupled_projection`

Feature:

- `projection = w_ifn * delta_IFN_APC + w_hla * delta_HLAII + w_receptor * delta_RECEPTOR`

Signed response score:

- Class A: `-projection`
- Class B: `projection`
- Class C: `projection`

Parameter count: zero fitted parameters.

Rationale: tests whether movement along the V26 positive APC-remodeling axis itself tracks response.

### Candidate 2: `coupled_v22_augmented`

Feature:

- Class A: `-(w_ifn * delta_IFN_APC + w_receptor * delta_RECEPTOR) / (w_ifn + w_receptor)`
- Class B: `(w_hla * delta_HLAII + w_receptor * delta_RECEPTOR) / (w_hla + w_receptor)`
- Class C: `w_hla * delta_HLAII - w_ifn * delta_IFN_APC + w_receptor * delta_RECEPTOR`

Parameter count: zero fitted parameters.

Rationale: preserves V22 therapy-class direction while adding the receptor-state proxy from the V26 coupling structure.

### Candidate 3: `coupling_coordination`

Feature:

Within each cohort, z-score `delta_IFN_APC`, `delta_HLAII`, and `delta_RECEPTOR`. Compute:

- `coordination_penalty = weighted mean absolute deviation from the weighted three-module center`
- `axis_component = coupled_projection` using the raw deltas above

Signed response score:

- Class A: `-axis_component - coordination_penalty`
- Class B: `axis_component - coordination_penalty`
- Class C: `coupled_v22_augmented - coordination_penalty`

Parameter count: zero fitted parameters.

Rationale: tests the V26-specific idea that coordinated module movement, not just level, carries predictive information. The penalty favors coherent movement of coupled modules.

## Evaluation Gate

A coupled successor rule is warranted only if all are true in the bounded immune-remodeling/JAK-STAT domain:

1. The best coupled representation improves AUC over V22 scalar by at least `0.05`.
2. The improvement survives the multi-candidate response-label permutation null at p `< 0.10`.
3. The coupled representation has Hedges g at least as large as the scalar.
4. No in-scope bounded cohort shows a severe contradictory drop relative to scalar (`AUC` decrease `> 0.10`).

If these gates are not met, no `LOCKED_RULE_V27.md` is written. The V26 coupling remains mechanistic context, not a predictive successor.

## V27 Comparison Results

Output directory: `analysis/v27_coupled_axis/`

Scripts:

- `scripts/v27_coupled_axis_comparison.py`
- `scripts/v27_apply_locked_rules.py`

The comparison used already-held V22/V23 cohorts only. No fresh Gafson/NEDA cohort was found on disk or read.

### Pooled Bounded Domain

Bounded domain cohorts:

- `GSE235357` MS dimethyl fumarate.
- `GSE253006_TOF_exact` UC tofacitinib exact all-cell rescoring.

| Feature | n | AUC | Bootstrap CI | Hedges g | Welch p |
|---|---:|---:|---|---:|---:|
| V22 scalar `locked_signed_score` | 19 | 0.811 | 0.589-1.000 | 1.191 | 0.0166 |
| `coupled_projection` | 19 | 0.689 | 0.444-0.900 | 0.661 | 0.1519 |
| `coupled_v22_augmented` | 19 | 0.633 | 0.356-0.867 | 0.542 | 0.2268 |
| `coupling_coordination` | 19 | 0.733 | 0.489-0.922 | 0.777 | 0.1110 |

Best coupled feature: `coupling_coordination`.

Best coupled-minus-scalar AUC delta: `-0.0778`.

Max-candidate label-permutation p for coupled advantage: `0.9128`.

Permutation null 95th percentile for best candidate delta AUC: `0.2889`.

### Bounded Cohort-Level Check

| Cohort | Scalar AUC | Best coupled AUC | Delta |
|---|---:|---:|---:|
| `GSE235357` | 0.72 | 0.64 | -0.08 |
| `GSE253006_TOF_exact` | 0.95 | 0.85 | -0.10 |

### All Primary Plus Exact UC

| Feature | n | AUC | Bootstrap CI | Hedges g |
|---|---:|---:|---|---:|
| V22 scalar `locked_signed_score` | 43 | 0.656 | 0.489-0.818 | 0.611 |
| `coupling_coordination` | 43 | 0.638 | 0.471-0.805 | 0.336 |

Best coupled-minus-scalar AUC delta: `-0.0175`.

Max-candidate label-permutation p for coupled advantage: `0.8568`.

## V27 Verdict

No V27 successor lock is warranted.

The coupled APC-axis structure is mechanistically useful but does not improve response prediction over the immutable V22 scalar in already-held bounded cohorts. The scalar remains the best available frozen rule for future external validation.

Interpretation:

- V26 coupling describes a real replicated module-dependency structure.
- That structure does not currently add predictive signal beyond the V22 scalar in tiny held cohorts.
- Adding receptor-state/coordination terms appears to dilute rather than improve the scalar response-monitoring signal.

Action:

- Do not write `LOCKED_RULE_V27.md`.
- Validate the V22 scalar on the next fresh paired cohort.
- Optionally report V27 coupled scores as pre-specified secondary exploratory outputs only, not as a successor rule.
