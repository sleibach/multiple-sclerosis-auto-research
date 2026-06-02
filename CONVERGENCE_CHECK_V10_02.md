# CONVERGENCE_CHECK_V10_02

Timestamp: 2026-06-02 12:52 CEST

## Matrix Coverage

- V10 supported disagreement matrix remains at `10` supported-axis
  disagreement pairs after evidence-overlap penalty.
- Genetics execution remains access-blocked because `OPENGWAS_JWT` is missing.
- The second V10 block focused on the RA pregnancy-near versus
  APC/treatment-far disagreement.

## New Audit Completed

Audit file:

- `RA_PREGNANCY_TREATMENT_DECOUPLING_V10.md`

RA evidence:

- Blood IFN/APC evidence is negative/null:
  - `mixscale_validated_ifng_readout`: delta `-0.0178`, Hedges g `-0.182`, p
    `0.580`, FDR `0.686`, n `18/18`.
  - `ifn_apc`: delta `-0.0460`, Hedges g `-0.249`, p `0.450`, FDR `0.572`.
- RA blood treatment-response rules fail:
  - `GSE12051`: baseline IFN/APC AUC `0.382`, Hedges g `-0.339`, n `44`.
  - `GSE138746_CD14`: baseline CD14 monocyte AUC `0.485`, Hedges g `-0.099`,
    n `78`.
  - `GSE8350`: 2-week blood `-delta_IFN_APC` AUC `0.450`, Hedges g `-0.356`,
    n `18`.
- GSE235508 seropositive RA pregnancy timecourse shows late-pregnancy trough
  and postpartum rebound in APC/HLA-II modules:
  - `mif_cd74_receptor_state`: T3-T1 `-0.642`; T6-T3 `1.162`.
  - `hla_ii_only`: T3-T1 `-0.646`; T6-T3 `1.394`.
  - `ifn_apc`: T3-T1 `-0.551`; T6-T3 `1.267`.
  - `lysosomal_apc`: T3-T1 `-0.566`; T6-T3 `0.835`.

## Updated Biological Versus Artifact Status

Resolved as first-pass biological disagreement candidate:

- Sjogren IFN/APC versus lipid-lysosomal split.

Survives first audit as perturbation-class biological candidate:

- RA pregnancy/postpartum near versus blood APC/treatment far.

Biological candidate after reformulation:

- UC cross-sectional IFN/APC proximity versus treatment-response contradiction,
  interpreted as static-state versus dynamic-downshift distinction.

Downgraded:

- UC treatment-response versus tissue-repair remains downgraded because the
  two axes reuse overlapping dynamic IFN/APC evidence.

## Transfer-Validity Consequence

RA is not globally far from MS and not globally near MS.

- Transfers: pregnancy/postpartum timing and rebound hypotheses.
- Does not transfer: RA blood APC anti-TNF response biomarkers.

## Next Forcing Questions

1. Attempt independent Sjogren replication or residualization for the
   IFN/APC-versus-lipid split.
2. Search for composition-adjusted RA/MS pregnancy datasets with monocyte/APC
   resolution and clinical activity timecourses.
3. Rebuild UC tissue-repair axis with endpoints that are independent of
   dynamic IFN/APC response evidence.
4. Replace blocked genetics execution with verified published pairwise
   estimates where primary execution remains unavailable.
