# V56 GSE281805 Raw GeoMx Reconstruction And Calibration

Status: **frozen before raw NAWM module scores or lesion-minus-NAWM contrasts
were computed**.

This plan governs a raw-data reconstruction needed because the deposited
processed Figure 4 matrix contains lesion AOIs but no NAWM. It is a calibration
and sensitivity analysis around the already frozen V54 modules. It is not an
unconstrained expression scan.

## Question

Can the public DCC/PKC deposit reproduce the authors' processed lesion matrix
well enough to support the previously specified donor-matched
lesion-minus-NAWM contrast? If so, does subtracting same-donor NAWM remove the
apparent BRL-versus-mixed difference in the frozen progression modules?

## Inputs And Immutable Boundaries

- Raw counts: the union of public DCCs from `GSE264094` and `GSE281805`.
- Probe annotation: public `Hs_R_NGS_WTA_v1.0` PKC.
- Sample identity, title, and tissue location: public GEO SOFT records.
- Author calibration target: Source Data Figure 4a processed lesion matrix.
- Author processing specification: committed source repository
  `walter-ca/MS-lesions_code`, specifically scripts 01-04.
- Frozen modules and donor-level statistics: inherited without alteration from
  `V56_GSE281805_BRL_MODULE_TEST.md`.

The public package does **not** contain the authors' ROI worksheet with segment
area, nuclei count, or their final `filtered_CD68.csv`. Three processed lesion
AOIs also lack a public DCC. These omissions are reported, never imputed. No
raw result can be called an exact reproduction or route-advancing result while
that metadata remains unavailable.

## Fixed Reconstruction

1. Parse reporter counts and GeoMx sequencing attributes from every DCC; map
   reporter IDs to PKC targets and aggregate probes to genes after the authors'
   fixed probe-QC logic where the required inputs exist.
2. Apply the authors' reconstructible segment thresholds: at least 1,000 raw
   reads; at least 80% trimmed, stitched, and aligned; at least 50% sequencing
   saturation; minimum negative count 1; maximum NTC count 1,000; and at least
   5% genes above the fixed LOQ. Apply the deposited assay's count-shift logic.
3. The unavailable area >=5,000 and nuclei >=100 filters are not approximated.
   Their absence is a mandatory residual limitation.
4. Retain genes detected above LOQ in at least 3% of retained segments, exactly
   as in the author code, plus negative controls for normalization.
5. Use `standR` 1.16.0: TMM log normalization; select 300 negative-control
   genes against `Slide.Name`; then RUV4 with `k=5`, preserving the fixed tissue
   state (`Type_main`). No parameter is tuned against module outcomes.
6. Tissue labels are derived mechanically from GEO titles/locations. `NAWM` is
   the primary reference; `PPWM` is excluded from the primary and may be shown
   only as a separately labeled sensitivity. The donor is the leading `MS<n>`
   identifier. The slide is the DCC ID without its terminal well.

## Calibration Gate

Calibration is assessed on the 117 Figure 4 lesion AOIs with both a deposited
DCC and an author-processed value. It is evaluated before NAWM biology is
interpreted. The reconstruction passes only if all of the following hold:

1. at least 95% of those 117 AOIs and at least 95% of the Figure 4 genes can be
   compared after deterministic mapping;
2. median sample-wise Spearman correlation across common variable genes is at
   least 0.90 and its 10th percentile is at least 0.80;
3. for every valid frozen module, reconstructed versus author sample scores
   have Spearman correlation at least 0.80;
4. all four processed-data gate-pass modules (`receptor_cd44_cxcr4`,
   `mif_ligand`, `lysosomal_unique`, and
   `resolution_efferocytosis_proxy`) preserve the sign of the donor-level
   BRL-minus-mixed estimate; and
5. no reconstruction choice is selected because it improves a biological
   module result.

Failure of any item blocks the biological matched-NAWM test. It is reported as
a reconstruction failure, not as a biological null.

## Frozen Matched-NAWM Test

If calibration passes, z-score each frozen gene across all eligible retained
AOIs and compute the unchanged module formulas. Within each donor and tissue
state, average AOIs. For each lesion-bearing donor with NAWM, calculate:

`lesion module mean - same-donor NAWM module mean`.

The primary comparison is BRL donor deltas versus mixed-rim donor deltas.
Donors represented in both lesion classes are removed from both groups before
inference. For every valid module report the difference in donor deltas,
Hedges' g, seeded 20,000-replicate bootstrap interval, exact two-sided
permutation p-value, exact max-T family-wise p-value across all frozen valid
modules, and leave-one-donor-out sign stability. Seed remains `56281805`.

The fixed association gate is max-T FWER p <= 0.05, bootstrap interval excluding
zero, and uniform leave-one-donor-out sign. A pass means only that the
progression-associated lesion-state signal survives a calibrated same-donor
NAWM subtraction under the available public reconstruction.

## Interpretation Boundary

Because area/nuclei metadata and the exact author-filtered NAWM set are absent,
even a calibrated gate pass is labeled **inconclusive pending exact ROI metadata
and independent longitudinal validation**. It cannot establish causality,
intervention direction, treatment response, disability slowing, a therapeutic
target, or a means to halt MS. A failed calibration produces no biological
verdict. A calibrated null argues against the proposed BRL-specific module
route under this public-data reconstruction and is reported without rescue.
