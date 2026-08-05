# V56 GSE281805 Raw Reconstruction Calibration

## Verdict

**Calibration failed. The matched lesion-minus-NAWM biological test was not
run.**

This is a pipeline-reproducibility result, not a biological null. It gives no
evidence for or against an MS progression mechanism or treatment.

## What Was Reconstructed

- Parsed all 296 public DCCs with the official `GeomxTools` reader and public
  WTA PKC.
- Applied the authors' available sequence/background QC, count-shift logic,
  official probe QC and outlier handling, target aggregation, 5% sample
  detection filter, 3% gene detection filter, TMM, 300 negative-control genes,
  and RUV4 with `k=5` preserving tissue class.
- Froze the calibration criteria before NAWM module outcomes were calculated.
- Compared the reconstruction against the 117 Figure 4 lesion AOIs that have a
  public DCC. Three other Figure 4 AOIs have no deposited DCC.

## Calibration Results

| criterion | frozen requirement | observed | result |
|---|---:|---:|---|
| source-AOI coverage | >=0.95 | 0.7179 (84/117) | fail |
| source-gene coverage | >=0.95 | 0.9898 (4,254/4,298) | pass |
| median sample Spearman | >=0.90 | 0.8555 | fail |
| 10th-percentile sample Spearman | >=0.80 | 0.8200 | pass |
| every valid module Spearman | >=0.80 | minimum 0.2516 | fail |
| all four key contrast signs | preserved | 3/4 | fail |

Module-score Spearman correlations were 0.9161 for MIF, 0.9038 for HLA
regulation, 0.7732 for OXPHOS, 0.5629 for resolution/efferocytosis, 0.5385 for
lysosomal state, 0.3893 for CD44/CXCR4, and 0.2516 for lipid/repair. The
CD44/CXCR4 BRL-minus-mixed sign reversed on the calibration subset (author
matrix -0.2543; reconstruction +1.3360).

All 296 AOIs passed reconstructible sequencing/background QC, but only 138
passed the published post-probe-QC LOQ sample filter. The authors' deposited
gene table implies a 211-segment modeling set (`DetectedSegments /
DetectionRate`). The mismatch cannot be repaired honestly by changing the
published 5% threshold or choosing samples based on module outcomes.

## Exact Boundary And Unblock

The public package omits the ROI worksheet fields used before expression
filtering (area and nuclei), the exact final `filtered_CD68.csv`, and the sourced
`nano_functions.r`; it also lacks three DCCs present in the author matrix.
Applying missing area/nuclei failure flags would only remove samples, so those
fields alone do not explain why the public reconstruction retains fewer rather
than more AOIs. Exact reproduction requires the authors' actual filtered sample
manifest and intermediate negative-control/LOQ metadata, or their post-QC
expression matrix including NAWM.

No approximate NAWM selection, outcome-guided threshold change, or substituted
normalization was used. The frozen matched-NAWM test remains blocked until the
calibration gate can be met.

## Reproducibility

- Plan: `docs/plans/V56_GSE281805_RAW_RECONSTRUCTION_CALIBRATION.md`
- Preparation: `scripts/v56_prepare_gse281805_geomx.py`
- Reconstruction: `scripts/v56_reconstruct_gse281805_geomx.R`
- Machine-readable calibration: `calibration_summary.json`
- Per-sample and per-module diagnostics are committed beside this report.
- Raw DCC/PKC files and generated count matrices remain ignored under
  `data/raw/`; no large raw data is committed.
