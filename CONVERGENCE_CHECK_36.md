# Convergence Check 36

Timestamp: 2026-05-27 17:20 CEST

## Forcing Question

After closing the biochemical route, does the `ETS2` inflammatory macrophage
axis provide a stronger cross-autoimmune intervention point?

## Result

No. `ETS2` has a real IBD myeloid signal, but it is not promotable in this V3
session.

## Evidence For Keeping It In Memory

- Direct `ETS2` broad h5ad expression is positive in Crohn disease and
  ulcerative colitis.
- The strongest context is UC colon myeloid:
  - effect `1.972`
  - p `0.0002169`
  - FDR `0.00079`
- The ETS2-labeled macrophage program is positive in Crohn disease, T1D, and
  UC.
- Prior literature supports an ETS2 macrophage inflammatory program in IBD/AS
  and related inflammatory diseases.

## Evidence Against Promotion

- Specificity fails:
  - only one specificity-pass context.
  - the ETS2-labeled program usually does not beat generic NF-kB/TNF, IFN/APC,
    or lysosome/APC comparators.
- MS fails:
  - direct `ETS2` in `GSE111972` white matter effect `-0.0608`, p `0.8649`,
    FDR `0.9802`.
  - ETS2 macrophage-program mean effect `-0.0145`, p `0.8943`.
- Treatment-response support fails:
  - GSE282122 mono/macrophage direct `ETS2` remission delta `-0.653` has
    nominal p `0.0649` and FDR `0.967`.
  - RA anti-TNF responder separation fails, and generic comparators are
    stronger or comparable.
- Genetics/target resolution fails:
  - Wave62 call `NO_GO_WAVE62_TARGET_RESOLUTION`.
  - no MS L2G support in the local Wave62 summary.
- Foundation-model support fails:
  - `ETS2` absent or below support threshold in Wave57/Wave69D.
- Translational route is weak:
  - direct ETS2 is not conventionally druggable.
  - MEK/ERK upstream route is broad, prior-arted, toxic, and already tested in
    RA.
- Novelty is narrow:
  - broad ETS2 inflammatory macrophage biology is already published.

## Decision

Do not write `FINDING_V3.md` from `ETS2`.

Retain `ETS2` as a comparator for a common false-positive pattern: strong
single-disease macrophage expression plus plausible genetics, but no MS,
specificity, treatment-response, foundation-model, modality, or novelty package.

## Next Forcing Question

The next branch should not be another generic macrophage inflammatory TF or
MEK/AP-1/NF-kB axis. It should either:

- introduce a genuinely new modality/evidence channel not already exhausted, or
- search for a cross-disease target that already has MS support and a realistic
  non-broad intervention point before spending more time on expression-derived
  macrophage programs.
