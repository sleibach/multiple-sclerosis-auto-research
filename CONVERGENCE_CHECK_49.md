# Convergence Check 49: FABP5 Parked Then Blocked

Timestamp: 2026-05-27 19:38 CEST

## Forcing Question

After direct `LPL` was parked as a marker, does any nearby lipid-loader node
provide a better therapeutic intervention point?

## Wave91 Result

Script:

- `scripts/v3_wave91_lipid_neighborhood_controller_scan.py`

Outcome:

- `17` candidates scanned.
- `FABP5` was the only candidate parked for deep validation.

`FABP5` evidence:

- MS white matter: delta `1.2651`, Hedges g `1.3549`, p `0.00414`.
- Direct h5ad nominal positive/trend contexts in psoriasis and UC, but also a
  negative UC epithelial context.
- RA anti-TNF baseline response: Hedges g `-0.4081`, p `0.2010`.
- Psoriasis adalimumab response: Hedges g `-0.1782`, p `0.7059`.
- Geneformer pivot-panel deletion:
  - `5` usable rows.
  - IBD epithelial deletion row moved the embedding toward the control
    centroid.

Wave91 call:

- `PARK_CONTROLLER_FOR_DEEP_VALIDATION`

Failures:

- `case_control_negative_context_present`
- `weak_or_inconsistent_response_direction`

## Wave92 Prior-Art Result

Script:

- `scripts/v3_wave92_fabp5_prior_art_audit.py`

Wave92 call:

- `FABP5_PRIOR_ART_BLOCKED_FOR_MS_THERAPEUTIC_NOVELTY`

Blocking records:

- PMID `34624687`: a FABP5/FABP7 inhibitor ameliorates oligodendrocyte injury
  in MS mouse models. DOI `10.1016/j.ebiom.2021.103582`.
- PMID `33124722`: the Fabp5/calnexin complex is required for EAE
  sensitization. DOI `10.1096/fj.202001539RR`.

## Decision

Do not promote `FABP5` as the V3 therapeutic target.

Interpret `FABP5` as independent confirmation that the lipid-state axis is
biologically meaningful and drug-proximal. It does not solve the novelty
requirement because the direct MS/EAE target route already exists.

## Next Forcing Question

Find a target or modality that preserves the lipid-state intervention concept
while avoiding direct prior-art collision with:

- FABP5/FABP7 inhibition,
- NAMPT,
- OSM/OSMR,
- TREM1,
- IL1B,
- broad PPAR/LXR class claims,
- direct LPL modulation.

The next search should bias toward a more specific state-transition regulator
or delivery/stratification mechanism rather than another obvious lipid enzyme.
