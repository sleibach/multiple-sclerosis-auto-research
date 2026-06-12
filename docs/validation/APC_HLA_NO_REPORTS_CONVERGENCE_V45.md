# APC/HLA/IFN No-Reports Convergence Sensitivity V45

Status: data-free validation sensitivity. This does not change the V41/V44
recurrence definition or any locked rule.

## Purpose

V45 had already shown that `apc_hla_ifn_monitoring` remains exceptional under
source-file weighting, source-family collapse, and leave-one-family removal.
This additional sensitivity asks a sharper circularity question:

> Does the APC/HLA/IFN recurrence signal depend on corpus-synthesis or report
> table rows rather than primary analysis outputs?

## Method

Script:

- `scripts/v45_convergence_no_reports.py`

Input:

- `analysis/v41_joint_inference/integrated_evidence_frame.tsv`

Rows excluded before scoring:

- `modality == corpus_synthesis`
- `source_file` under `docs/reports/`
- `source_file` under `docs/history/`

In the current integrated frame, the exclusion removed `63` rows, all from:

- `docs/reports/FINDINGS_SCORES_V37.tsv`

The null kept the full entity universe from the original evidence frame and ran
`20,000` replicates with seed `45845`.

## Results

Filtered frame:

- original rows: `985`
- excluded rows: `63`
- filtered rows: `922`
- filtered positive source units: `86`

| Sensitivity | Target observed | Target rank | FWER p | Max-null p99 |
|---|---:|---:|---:|---:|
| Source-file weighted, no reports | `12.0267` | `1` | `0.00005` | `4.0635` |
| Modality/source-family collapsed, no reports | `15` | `1` | `0.00005` | `7` |
| Source-family collapsed, no reports | `9` | `1` | `0.00005` | `5` |

The p-values are at the floor for `20,000` null replicates.

Target source-family support after excluding reports:

- V32 confounder audit / treatment response: `25` source units;
- V26 deep structure / treatment pharmacodynamic: `7`;
- V35 T/B compartment gate / exploratory: `5`;
- V39 immune-tone anomaly / exploratory: `5`;
- V26 cross-disease summary: `4`;
- V36 therapy branch map / treatment response: `4`;
- additional support from V20, V26 perturbation/tests, V28, V35 lysosomal, and
  V35 metabolic artifacts.

## Verdict

The APC/HLA/IFN recurrence result is not dependent on report-derived or
corpus-synthesis rows. After removing those rows, the target remains rank `1` in
all three recurrence formulations and remains above the 99th percentile of the
family-wise null by a wide margin.

Interpretation: this strengthens the data-free convergence argument because the
signal is carried by analysis artifacts, not by the V37 scored-findings report
itself.

## Outputs

- `analysis/v45_convergence_no_reports/summary.json`
- `analysis/v45_convergence_no_reports/convergence_no_reports_null_summary.tsv`
- `analysis/v45_convergence_no_reports/source_file_weighted_recurrence_no_reports.tsv`
- `analysis/v45_convergence_no_reports/modality_source_family_collapsed_no_reports_recurrence.tsv`
- `analysis/v45_convergence_no_reports/source_family_collapsed_no_reports_recurrence.tsv`
- `analysis/v45_convergence_no_reports/excluded_report_rows.tsv`
- `analysis/v45_convergence_no_reports/target_source_family_breakdown_no_reports.tsv`

