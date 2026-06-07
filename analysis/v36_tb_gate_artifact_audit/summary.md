# V36 T/B Gate Artifact Audit

Status: **survives_simple_count_fraction_residualization_but_not_definitive**.

- Patients: `9`.
- Original locked T/B-minus-non-T/B AUC gap: `0.158`.
- Residualized locked gap after baseline/delta compartment fraction adjustment: `0.133`.
- Best count/fraction-only oriented AUC: `0.900` (`myeloid_apc_like` / `delta_n_cells`).
- T-cell locked AUC -> residualized AUC: `1.000` -> `0.650`.
- B/plasma locked AUC -> residualized AUC: `0.950` -> `0.850`.

Interpretation:

Simple compartment abundance proxies do not explain away the T/B gate: residualizing locked scores against baseline and delta compartment fractions preserves a positive T/B-minus-non-T/B gap. However, this is not a full deconvolution or independent replication, and small n remains decisive.

Limit:

This does not prove within-cell remodeling. It only rejects the simplest
available count/fraction artifact using held data. The decisive test remains
an independent paired response cohort with T/B/myeloid compartments and
patient-level labels.
