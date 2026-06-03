# RA_TISSUE_REPAIR_PREGNANCY_SCOPE_AUDIT_V11

Status: V11 resolution of matrix cell
`005_rheumatoid_arthritis_axis_08_tissue_repair_resolution_vs_axis_09_sex_hormonal_pregnancy`.

## Question

Why is RA far from MS on tissue-repair / response-monitoring architecture but
near MS on pregnancy modulation?

Supported V11 placements:

- `axis_08_tissue_repair_resolution`: RA `far/supported/medium`,
  blood/synovium, treatment perturbation.
- `axis_09_sex_hormonal_pregnancy`: RA `near/supported/medium`, blood,
  natural experiment.

## Evidence

### RA Tissue-Repair / Response-Monitoring Placement Is Far Because Blood APC Response Monitoring Fails

V8 evidence registry:

- Axis 8 RA placement uses V7 RA anti-TNF blood cohorts:
  - `GSE8350`: early blood `-delta_IFN_APC` AUC `0.450`.
  - `GSE12051`: baseline blood IFN/APC AUC `0.382`.
  - `GSE138746_CD14`: baseline CD14 monocyte IFN/APC AUC `0.485`.
- V8 caveat: "Far for blood response-monitoring architecture; RA synovial
  tissue repair remains less tested."

Interpretation:

- The supported far placement is valid for **blood APC response-monitoring**.
- It is not a resolved statement about RA synovial tissue repair.

### RA Pregnancy Placement Is Near On Blood Natural-Experiment Kinetics

GSE235508 seropositive RA timecourse:

- `mif_cd74_receptor_state`: T3-T1 `-0.642`; T6-T3 `1.162`.
- `hla_ii_only`: T3-T1 `-0.646`; T6-T3 `1.394`.
- `ifn_apc`: T3-T1 `-0.551`; T6-T3 `1.267`.
- `lysosomal_apc`: T3-T1 `-0.566`; T6-T3 `0.835`.

Interpretation:

- RA shows late-pregnancy immune-module trough and postpartum rebound in blood.
- This is a systemic pregnancy/postpartum kinetic pattern, not a therapy
  response-monitoring endpoint.

## Artifact Audit

Compartment:

- Pregnancy evidence is blood.
- Tissue-repair placement is labeled blood/synovium, but the actual quantified
  support is blood anti-TNF response monitoring; synovial repair was caveated
  as under-tested.
- Therefore the disagreement is partly an axis-scope artifact: the `axis_08`
  label is broader than the evidence supporting the RA far placement.

Cohort:

- Pregnancy evidence and anti-TNF evidence come from different cohorts and
  perturbation contexts.
- This is unavoidable for this cell but prevents causal coupling claims.

Measurement grade:

- Pregnancy is a natural experiment with timecourse module kinetics.
- Tissue-repair/response monitoring is treatment perturbation with clinical
  response classification.
- The mismatch is real and should be preserved as perturbation-class
  decoupling, not collapsed into global RA/MS distance.

## Hostile Critique

Criticism:

- Calling this "tissue repair" is misleading because the RA evidence is mostly
  blood treatment-response failure.

Response:

- Accepted. V11 classifies this cell as an `artifact` for broad tissue-repair
  claims and a valid transfer warning only for blood response-monitoring.

Criticism:

- Synovial tissue repair could still be near MS on some inflammatory-resolution
  axis.

Response:

- Accepted. The current matrix does not resolve RA synovial repair. Future
  versions should rebuild RA `axis_08` with synovial tissue endpoints rather
  than blood APC response-rule failure.

## Classification

V11 status: `artifact`.

Resolved statement:

> The RA axis-08-versus-pregnancy disagreement is partly an axis-scope artifact:
> RA is far from MS for blood APC response-monitoring transfer, but RA synovial
> tissue repair is not sufficiently tested by the evidence currently assigned
> to the tissue-repair axis.

This does not erase the RA pregnancy/treatment decoupling resolved in V10/V11.
It prevents over-extending that result into a global RA tissue-repair claim.

## MS Transfer Consequence

What transfers to MS:

- RA pregnancy/postpartum timing and rebound hypotheses remain useful as a
  natural-experiment comparator.

What does not transfer:

- RA blood anti-TNF APC response-monitoring biomarkers.

What is unresolved:

- RA synovial repair biology as a comparator for MS lesion repair.

Falsifiable upgrade path:

- Build an RA synovial treatment-response axis using paired synovial tissue or
  validated synovial repair/histology endpoints.
- If RA synovial repair shows a dynamic IFN/APC downshift or other repair
  module resembling MS/IBD response-monitoring, then the current `far` axis-08
  placement should be split into blood-far and synovium-unresolved/near.
