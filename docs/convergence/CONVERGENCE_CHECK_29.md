# Convergence Check 29 - Wave68 Corrected Unrestricted Gene Screen

Timestamp: 2026-05-27 15:54 CEST

## Forcing Question

After the pre-specified lipid-lysosomal/APC module failed in cell-resolved
anti-TNF data, does an unrestricted gene-level screen in the same myeloid
dataset identify a promotable target?

## Result

No. After correcting the Wave68 ranking and encoding the already-completed SP140
blocker, no gene is promoted as `REOPEN_GENE_LEVEL_TARGET_CANDIDATE`.

The screen tested 33,075 genes in paired `Mono_macro` and `DC` pseudobulk from
`GSE282122` / Zenodo `14007626`.

Corrected calls:

- `DESCRIPTIVE_GENE_SIGNAL`: 66,137 rows.
- `PARK_GENETIC_PERTURBATION_INTERSECTION`: 13 rows.

Top parked intersections:

- `RGS14` in DC: adjusted remission delta 1.872, adjusted FDR 0.0113, Wave62
  target-resolution score 5.30, cross-autoimmune genetics true, no direct
  druggability flag.
- `CD274` in DC: adjusted remission delta -1.910, adjusted FDR 0.0243, broad
  QTL colocalization, but checkpoint biology is obvious prior-art/safety
  territory and not currently a clean intervention route.
- `TNFSF15`, `CD80`, `IL7R`, `STAT4`, `FCGR2A/B`, `NCF1`, `ARHGAP31`, `LPP`,
  `TNFRSF9`, and `DCLRE1B` remain parked, not promoted.

`SP140` had a nominal/adjusted `Mono_macro` remission-response signal, but it is
demoted by prior V3 audits: direct inflammatory-disease SP140 inhibition and
Crohn SP140/topoisomerase rescue are prior art; SP140 inhibition conflicts with
SP140-low genetic risk direction; local MS white-matter signal was null.

## Interpretation

Wave68 is valuable because it prevents proxy-satisficing. The cell-resolved
anti-TNF dataset does not rescue the lipid-lysosomal module, and it does not
produce a clean direct target. It does, however, identify a set of genetically
anchored response-associated nodes that may point to upstream or downstream
controllers.

## Decision

Do not promote a Wave68 direct gene target. Continue with a successor
intervention branch:

1. Rank the 13 parked genes for pathway/controller convergence.
2. Require an intervention point that is druggable, less prior-art blocked, and
   directionally interpretable.
3. Validate any successor against independent MS/local autoimmune datasets
   before novelty search.
