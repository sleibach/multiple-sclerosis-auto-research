# V45 APC/HLA/IFN Leave-One-Source-Family-Out Check

## Status

Internal method-characterization only. This is not external validation, does not
change the V22 rule, and does not change any pre-registration.

## Question

Does the APC/HLA/IFN recurrence argument depend on a single artifact family,
such as the V32 confounder audit, V26 deep-structure workup, or V37 report
corpus?

## Script And Outputs

Script:

- `scripts/v45_leave_one_family_convergence.py`

Outputs:

- `analysis/v45_convergence_family_jackknife/summary.json`
- `analysis/v45_convergence_family_jackknife/leave_one_source_family_out.tsv`

The check uses the V45 source-file weighted and source-family collapsed null
envelopes from `analysis/v45_convergence_sensitivity/`.

## Result

All `12` source families were removed one at a time. In every removal:

- source-file weighted target remained rank `1`;
- modality + source-family collapsed target remained rank `1`;
- source-family collapsed target remained rank `1`;
- all three target scores remained above the corresponding V45 max-null p99.

Most severe removals:

| Removed family | Removed target source units | Weighted target | Modality-family target | Source-family target |
|---|---:|---:|---:|---:|
| `analysis/v32_confounder_audit` | `25` | `10.5267` | `15` | `9` |
| `analysis/v26_deep_structure` | `21` | `10.7667` | `10` | `9` |
| `docs/reports` | `9` | `12.0267` | `15` | `9` |

Reference V45 max-null p99 values:

- source-file weighted: `4.0756`;
- modality + source-family collapsed: `8`;
- source-family collapsed: `6`.

## Interpretation

The internal APC/HLA/IFN convergence signal is not carried by a single artifact
family. Even removing the densest supporting families leaves the target rank 1
and above the stricter V45 null envelopes.

This strengthens the data-free convergence argument, but does not remove the
need for external paired DMT response validation.

