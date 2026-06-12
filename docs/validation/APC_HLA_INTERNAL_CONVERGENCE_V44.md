# V44 Internal Convergence Argument For The APC/HLA-II Monitoring Lead

Date: 2026-06-12

Status: method/internal-validation artifact. This is not a new biological discovery and does not validate the V22 rule clinically.

## Question

Can the project state a stronger data-free internal-validation argument for the APC/HLA-II monitoring lead while Gafson and other external cohorts are delayed?

This workstream reuses the V41 corpus-level evidence frame and the V43/V44 synthetic-null self-audit. It does not change the locked V22 rule, the V42 preregistration, or any validation threshold.

## Evidence Package

The internal convergence argument rests on five independent checks:

1. V22/V23 locked-rule validation on already-held small treatment-response cohorts: provisional and mechanism-bounded, not externally validated.
2. V28 heterogeneous-toolchain robustness: more flexible methods did not improve over the scalar, so complexity is not driving the signal.
3. V32 confounder audit: the signal is immune-tone bounded and partially attenuated, but not explained away by glucocorticoid or simple cell-composition controls.
4. V41 joint inference: the APC/HLA/IFN entity is the only entity selected by the conservative train-side family-wise joint gate and is held-out treatment-response supported, but the joint z is borderline against the max-z null.
5. V43/V44 recurrence self-audit: source-unit recurrence is far beyond multiple null envelopes and is the strongest internal formulation.

## V44 Added Stress Test

Script and outputs:

- `scripts/v44_internal_convergence_validation.py`
- `analysis/v44_internal_validation/convergence_stress_summary.json`
- `analysis/v44_internal_validation/recurrence_stricter_nulls.tsv`
- `analysis/v44_internal_validation/recurrence_modality_jackknife.tsv`
- `analysis/v44_internal_validation/recurrence_source_file_jackknife.tsv`

The script preserves the V41 recurrence definition: positive-direction source units, regardless of p-value threshold. It runs 20,000 replicates under each of three nulls:

- `global`: source-unit entity assignments are randomized across the full entity vocabulary.
- `modality`: source-unit assignments are randomized only within each modality's entity vocabulary.
- `source_local`: assignments are randomized within the same modality and source-file entity vocabulary where possible, falling back to modality when the local universe is tautologically small.

## Null Results

Observed APC/HLA/IFN recurrence: `78` positive source units across `11` modalities.

| Null mode | Replicates | Max-null p95 | Max-null p99 | Target-null p95 | Target-null p99 | Target FWER p |
|---|---:|---:|---:|---:|---:|---:|
| global | `20000` | `12` | `14` | `8` | `10` | `0.00005` |
| modality | `20000` | `35` | `38` | `32` | `35` | `0.00005` |
| source_local | `20000` | `38` | `41` | `38` | `41` | `0.00005` |

Interpretation: the recurrence is not only beyond the original V41/V43 global null. It remains beyond a modality-aware null and a stricter source-local null that preserves much of the source/report structure.

## Jackknife Robustness

### Modality Removal

The largest recurrence drop comes from removing `treatment_response`, as expected for a monitoring lead. Even then, target recurrence remains `46`, which is above the strictest source-local null p99 (`41`).

| Removed modality | Remaining recurrence | Drop |
|---|---:|---:|
| treatment_response | `46` | `32` |
| exploratory | `66` | `12` |
| corpus_synthesis | `69` | `9` |
| treatment_pharmacodynamic | `71` | `7` |
| cross_disease_summary | `74` | `4` |

No single modality eliminates the recurrence signal.

### Source-File Removal

The largest source-file dependence is the V32 confounder audit, followed by the V26 module-dependency table. That is expected because these are dense summary outputs. Removing either still leaves recurrence beyond the strictest source-local null p99.

| Removed source file | Remaining recurrence | Drop |
|---|---:|---:|
| `analysis/v32_confounder_audit/v32_confounder_adjustment_metrics.tsv` | `55` | `23` |
| `analysis/v26_deep_structure/workstream_b_module_dependencies.tsv` | `59` | `19` |
| `docs/reports/FINDINGS_SCORES_V37.tsv` | `69` | `9` |
| `analysis/v35_tb_compartment_gate/tb_compartment_gate.tsv` | `73` | `5` |
| `analysis/v39_immune_tone_anomaly/immune_tone_anomaly_spaces.tsv` | `73` | `5` |

No single source file eliminates the recurrence signal.

## What This Strengthens

The strongest internal statement is now:

> Across the held public corpus and project-derived evidence frame, the APC/HLA-II/IFN monitoring entity recurs across independent source units far beyond global, modality-aware, and source-local synthetic-null expectations; it is not eliminated by removing any one modality or source file.

This is stronger than the V41 joint-z statement because it directly addresses the corpus-level convergence pattern rather than relying on a family-wise max-z search statistic.

## What This Does Not Establish

This does not prove clinical utility, does not validate the V22 scalar on an external cohort, and does not remove the V32 immune-tone caveat. The lead remains:

- provisional,
- immune-tone bounded,
- batch-guarded after V44,
- and dependent on external paired DMT response validation.

## Practical Consequence

For external communication, lead with the recurrence/convergence argument and use the joint-z result as a conservative secondary check:

- Primary internal evidence: recurrence under strict nulls (`78` observed; strictest max-null p99 `41`; FWER `0.00005` in 20,000 replicates).
- Secondary internal evidence: V41 joint inference selected APC/HLA/IFN but was borderline under the family-wise max-z null (`z=8.0548`, FWER `0.0684`).
- Decisive evidence still required: Gafson or another external paired DMT response cohort run through the frozen V42/V44 harness.

