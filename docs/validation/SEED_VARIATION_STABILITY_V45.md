# Seed-Variation Stability Checks V45

Status: synthetic method-characterization only. These results are not biological
evidence about MS and do not change any locked rule or frozen pre-registration.

## Purpose

Several V45 robustness claims were initially based on one seeded synthetic grid
per harness. This run checks whether the method-behavior conclusions are stable
across independent seed families.

## Method

Script:

- `scripts/v45_seed_variation_stability.py`

Harness families rerun:

- primary V22 multi-confounder batch guard;
- postpartum APC-arm pathology guard;
- T/B compartment pathology guard.

Scale:

- seed bases: `46045`, `46145`, `46245`, `46345`, `46445`;
- `5` seed families;
- `30` replicates per truth / pathology / severity cell;
- total synthetic cohorts: `31,500`;
- output directory: `analysis/v45_seed_variation_stability/`.

The script stores metrics and summaries only, not another large subject-level
matrix.

## Results

| Harness | Worst raw synthetic-null pass | Worst guarded synthetic-null clean pass | Guarded null <= 0.05 in all seeds? |
|---|---:|---:|---|
| Primary multi-confounder batch guard | `0.9000` | `0.0333` | yes |
| Postpartum APC-arm | `0.8667` | `0.0333` | yes |
| T/B compartment | `0.5000` | `0.0333` | yes |

Across all five seed families:

- every harness kept worst guarded synthetic-null clean pass at or below
  `0.0333`;
- raw false-positive behavior remained high under severe synthetic pathologies;
- planted-signal clean-pass retention remained variable, confirming the known
  cost of conservative diagnostic guards.

## Interpretation

The V45 guard behavior is not a single-seed artifact at this resolution. The
main claim is stable:

> response-correlated technical or pathology structure can create raw synthetic
> false positives, and the guarded interpretation prevents those from becoming
> clean validation calls.

The complementary limitation also remains stable:

> conservative guards can downgrade planted synthetic signals when technical
> structure is severe or when many metadata fields are audited in small cohorts.

That limitation is a validation-readiness tradeoff, not a reason to relax the
guard before real data arrive.

## Outputs

- `analysis/v45_seed_variation_stability/summary.json`
- `analysis/v45_seed_variation_stability/seed_variation_metrics.tsv`
- `analysis/v45_seed_variation_stability/seed_variation_cell_summary.tsv`
- `analysis/v45_seed_variation_stability/seed_variation_per_seed_summary.tsv`
- `analysis/v45_seed_variation_stability/seed_variation_stability_summary.tsv`

