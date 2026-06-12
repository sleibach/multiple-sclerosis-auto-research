# V45 T/B Compartment Harness Pathology Stress Test

## Status

Synthetic method-characterization only. These results are not biological
evidence about MS treatment response. No real validation cohort was read, and
the frozen V44 T/B compartment pre-registration was not changed.

## Question

The T/B compartment lead is vulnerable to a specific artifact: apparent
within-compartment remodeling may really be cell-composition or compartment
assignment noise. V45 stress-tested the frozen V44 mechanics against that risk.

## Simulation

Script:

- `scripts/v45_tb_compartment_pathology_simulation.py`

Outputs:

- `analysis/v45_tb_compartment_pathology/summary.json`
- `analysis/v45_tb_compartment_pathology/tb_compartment_pathology_summary.tsv`
- `analysis/v45_tb_compartment_pathology/tb_compartment_pathology_metrics.tsv`
- `analysis/v45_tb_compartment_pathology/synthetic/tb_compartment_pathology_subjects.tsv.gz`

Scale:

- `6,300` seeded synthetic cohorts.
- `378,000` synthetic subject rows.
- `90` replicates per truth / pathology / severity cell.
- Pathologies: composition shift only, B-fraction response correlation,
  T-fraction response correlation, compartment-label noise,
  response-correlated batch, timepoint jitter, and low compartment coverage.

## Headline Results

| Metric | Result |
|---|---:|
| Worst synthetic-null raw pass rate | `0.3333` |
| Worst synthetic-null composition-adjusted pass rate | `0.3333` |
| Worst synthetic-null guarded clean pass rate | `0.0111` |
| Worst planted guarded-clean pass drop | `1.0000` |

Interpretation:

- Composition adjustment is necessary but not sufficient for every pathology.
- Pure composition artifacts are controlled by the residualized B/plasma
  readout.
- Response-correlated batch can survive composition adjustment, so the separate
  batch guard is required.
- Low compartment coverage and severe compartment artifacts can make a true
  planted signal mechanically uninterpretable; this is a correct validation
  failure mode.

## Pathology-Specific Findings

### Response-Correlated Batch

Synthetic null:

- severity `1.00`: raw pass `0.3333`, composition-adjusted pass `0.3333`,
  guarded clean pass `0.0000`;
- severity `0.75`: raw pass `0.0556`, composition-adjusted pass `0.0556`,
  guarded clean pass `0.0000`.

Decision: batch metadata are mandatory. Composition adjustment alone cannot make
a T/B result interpretable if batch tracks response.

### Composition-Driven Artifacts

For synthetic-null B-fraction and composition-shift artifacts, composition
adjustment removed the pass signal:

- `b_fraction_response_correlated`, severity `1.00`: raw pass `0.0333`,
  composition-adjusted pass `0.0000`;
- `composition_shift_only`, severity `1.00`: raw pass `0.0111`,
  composition-adjusted pass `0.0000`.

Decision: the V44 requirement for B/plasma residual AUC after compartment
fraction/count adjustment is justified.

### Planted Signals With Severe Composition Distortion

In planted cohorts, raw B/plasma AUCs often remained high while residualized
performance collapsed under severe composition artifacts:

- `composition_shift_only`, severity `1.00`: raw pass `0.9444`,
  composition-adjusted pass `0.0000`;
- `b_fraction_response_correlated`, severity `1.00`: raw pass `0.9667`,
  composition-adjusted pass `0.0000`.

Decision: this lead requires compartment-resolved data of sufficient quality.
If response is inseparable from compartment fractions, the result is not a clean
validation even when raw AUC is high.

### Low Compartment Coverage

Severe coverage loss made planted results unclean despite strong raw signals:

- severity `0.75`: raw pass `0.9778`, guarded clean pass `0.0000`;
- severity `1.00`: raw pass `0.9333`, guarded clean pass `0.0000`.

Decision: B/plasma-like and T-like feature coverage is a hard acquisition
requirement.

## Trustworthy Envelope

A future T/B compartment validation is interpretable only if:

1. baseline and early on-treatment samples are paired;
2. response/remission/NEDA labels are sample-mapped;
3. B/plasma-like and T-like compartments are measured or deconvolved using a
   pre-specified method;
4. compartment fractions/counts are available for adjustment;
5. batch/QC metadata are available and not strongly response-correlated;
6. B/plasma-like coverage remains adequate.

If these conditions are not met, a raw T/B signal is context only and should not
be promoted beyond effect-size planning.

