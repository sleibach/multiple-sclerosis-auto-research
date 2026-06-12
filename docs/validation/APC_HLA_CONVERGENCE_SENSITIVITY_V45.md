# V45 APC/HLA/IFN Convergence Sensitivity

## Status

Internal method-characterization only. This is not external validation and does
not change the immutable V22 rule or any validation threshold.

## Question

V44 showed that `apc_hla_ifn_monitoring` recurs across source units beyond
global, modality-aware, and source-local nulls. V45 asked whether that recurrence
is inflated by dense evidence rows from a few artifacts.

Two stricter sensitivity views were tested:

1. **Source-file weighting:** each source file contributes fixed total mass,
   so dense artifacts cannot dominate recurrence by having many rows.
2. **Source-family collapse:** source files are collapsed into broader families
   such as `analysis/v32_confounder_audit`, `analysis/v26_deep_structure`,
   `docs/reports`, and `analysis/v35_tb_compartment_gate`.

## Script And Outputs

Script:

- `scripts/v45_convergence_sensitivity.py`

Outputs:

- `analysis/v45_convergence_sensitivity/summary.json`
- `analysis/v45_convergence_sensitivity/convergence_sensitivity_null_summary.tsv`
- `analysis/v45_convergence_sensitivity/source_file_weighted_recurrence.tsv`
- `analysis/v45_convergence_sensitivity/modality_source_family_collapsed_recurrence.tsv`
- `analysis/v45_convergence_sensitivity/source_family_collapsed_recurrence.tsv`
- `analysis/v45_convergence_sensitivity/target_source_family_breakdown.tsv`

Null scale:

- `20,000` replicates per sensitivity null.

## Result

| Sensitivity | Observed target | Target rank | Max-null p99 | FWER p |
|---|---:|---:|---:|---:|
| source-file weighted | `12.5267` | `1` | `4.0756` | `0.00005` |
| modality + source-family collapsed | `16` | `1` | `8` | `0.00005` |
| source-family collapsed | `10` | `1` | `6` | `0.00005` |

`0.00005` is the empirical floor for 20,000 null replicates.

## Interpretation

The V44 recurrence result is not explained by a few dense files contributing many
duplicated evidence rows. `apc_hla_ifn_monitoring` remains the top entity after
source-file weighting and after collapsing sources into coarser families.

This strengthens the internal convergence argument:

> APC/HLA/IFN is not merely a repeated label in the project report corpus. It
> recurs across distinct artifact families and remains far beyond null
> expectations when dense sources are down-weighted.

## Limits

This still does not establish clinical validation. It supports the data-free
internal convergence argument while waiting for external paired DMT response
data. The lead remains:

- provisional;
- immune-tone bounded;
- batch-guarded;
- externally validation-gated.

## Practical Consequence

When explaining the internal evidence, use this V45 sensitivity alongside V44:

- V44 raw recurrence: `78` positive source units, strictest source-local max-null
  p99 `41`;
- V45 weighted/collapsed recurrence: rank `1` under all three sensitivity views,
  FWER at the 20,000-replicate empirical floor.

