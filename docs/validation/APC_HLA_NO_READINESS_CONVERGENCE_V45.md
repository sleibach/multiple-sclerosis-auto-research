# APC/HLA/IFN No-Readiness Convergence Sensitivity V45

Status: data-free validation sensitivity. This does not change the V41/V44
recurrence definition, the locked V22 rule, or any validation pre-registration.

## Purpose

V45 has added many validation-readiness artifacts. This sensitivity asks a
narrow circularity question:

> Does the APC/HLA/IFN recurrence result depend on validation/readiness
> artifacts generated after the V42 pre-registration?

This is distinct from the earlier no-report sensitivity
`docs/validation/APC_HLA_NO_REPORTS_CONVERGENCE_V45.md`, which removed V37
report/corpus-synthesis rows. Here the target is specifically post-V42 readiness
material: power maps, harnesses, batch guards, cohort specs, intake preflight,
Karolinska/GSE228330 readiness, and other validation-preparation outputs.

## Method

Script:

- `scripts/v45_convergence_no_readiness.py`

Input:

- `analysis/v41_joint_inference/integrated_evidence_frame.tsv`

Exclusion rule:

- any `source_file` under `docs/validation/`;
- any `source_file` under `analysis/v43_`, `analysis/v44_`, or `analysis/v45_`;
- any source path containing readiness tokens such as `PREREGISTRATION`,
  `VALIDATION_READINESS`, `POWER_MAP`, `HARNESS`, `ROBUSTNESS`,
  `BATCH_GUARD`, `COHORT_SPEC`, `KAROLINSKA`, `GSE228330`, or `PREFLIGHT`.

The null kept the original entity universe and used `20,000` replicates with
seed `45945`.

## Result

The V41 integrated evidence frame contained **zero** post-V42 readiness rows.
Therefore the main result is not just that the signal survives exclusion; this
specific circularity channel is absent from the convergence object.

Frame audit:

- original rows: `985`
- post-V42 readiness rows excluded: `0`
- filtered rows: `985`
- filtered positive source units: `104`

| Sensitivity | Target observed | Target rank | FWER p | Max-null p99 |
|---|---:|---:|---:|---:|
| Source-file weighted, no readiness | `12.5267` | `1` | `0.00005` | `4.0734` |
| Modality/source-family collapsed, no readiness | `16` | `1` | `0.00005` | `8` |
| Source-family collapsed, no readiness | `10` | `1` | `0.00005` | `6` |

P-values are at the floor for `20,000` null replicates.

## Interpretation

The APC/HLA/IFN recurrence result is not inflated by V42+ validation-readiness
work because those artifacts are not present in the V41 integrated evidence
frame. This strengthens the audit trail for V45's later infrastructure work: the
infrastructure is downstream of the convergence result, not a contributor to it.

The remaining `docs/reports` support visible in the full frame is addressed by
the separate no-report check, where the target also remained rank `1` and at the
FWER floor after removing report-derived rows.

## Outputs

- `analysis/v45_convergence_no_readiness/summary.json`
- `analysis/v45_convergence_no_readiness/convergence_no_readiness_null_summary.tsv`
- `analysis/v45_convergence_no_readiness/excluded_readiness_rows.tsv`
- `analysis/v45_convergence_no_readiness/all_source_files_audited.tsv`
- `analysis/v45_convergence_no_readiness/target_source_family_breakdown_no_readiness.tsv`
- `analysis/v45_convergence_no_readiness/source_file_weighted_recurrence_no_readiness.tsv`
- `analysis/v45_convergence_no_readiness/modality_source_family_collapsed_no_readiness_recurrence.tsv`
- `analysis/v45_convergence_no_readiness/source_family_collapsed_no_readiness_recurrence.tsv`
