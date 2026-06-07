# V36 Block Synthesis

## Verdict

V36 strengthened the treatment-response program by demoting post-hoc features
and sharpening the validation plan. It did **not** create a new locked rule or
an intervention-grade finding.

Primary conclusion:

The immutable V22/V23 bounded APC/HLA-II treatment-response monitoring rule
remains the primary validation target. V36-derived features are secondary audits
only.

## What Changed

1. **Multiplicity control reset the bar.**
   A 76-feature post-hoc search in the exact tofacitinib artifact produced
   perfect AUCs often under label permutation. The empirical max-AUC p-value
   was `0.5000`. Therefore V36 perfect-AUC features are exploratory, not
   findings.

2. **The biology was refactored.**
   The best held-data wording is now:

   > broad early on-treatment IFN/APC/STAT1-axis monitoring state,
   > T/B-readable, not T/B-specific, not glucocorticoid-explained,
   > STAT1/composition/QC-conditioned, and unreplicated.

3. **Therapy branches are now explicit.**
   - DMF/JAK/immune-remodeling context: IFN/APC/STAT1 downshift.
   - IFN-beta context: HLA-II competence/induction plus CD74/CD44/CXCR4
     receptor-state dynamics.
   - Fingolimod, adalimumab, and MTX psoriasis skin: no unbounded transfer.

4. **The primary MS DMT evidence is fragile.**
   `GSE235357` DMF locked score: AUC `0.720`, exact p `0.155`, leave-one-out
   minimum AUC `0.650`. Directionally supportive, not decisive.

5. **Validation planning is now stricter.**
   Gafson-style validation should aim for roughly `30` responders and `30`
   nonresponders or more. Future validation must use p-values plus an effect
   floor: current floor AUC `>= 0.70` and signed Hedges g `>= 0.50`.

## Best Current Action

Acquire Gafson et al. 2018 DMF PBMC RNA-seq processed counts plus sample-level
NEDA-4 labels using `docs/validation/GAFSON_DATA_REQUEST_V36.md`.

When data arrive:

1. Place files under `data/raw_v3/gafson_dmf_2018/`.
2. Checksum and update `data/manifest.tsv`.
3. Run the frozen validation harness.
4. Report V22 primary score first.
5. Report V32/V36/V36b audits: steroid, STAT1, glycolysis, composition,
   QC/batch, therapy branch, sample size, and effect-size floor.

## Do Not Do Next

- Do not tune `docs/locked_rules/LOCKED_RULE_V22.md`.
- Do not promote V36 post-hoc W8, compartment, substate, or receptor features
  to successor rules.
- Do not treat SAP model or RPT outputs as evidence.
- Do not interpret IFN-beta, fingolimod, adalimumab, or MTX stress tests as
  universal validation or universal failure of the bounded DMF/JAK-style claim.

## Key Artifacts

- Full slate: `docs/history/HYPOTHESIS_SLATE_V36.md`
- Queue/timing: `meta/V36_QUEUE.md`
- Validation readiness: `docs/validation/VALIDATION_READINESS_V27.md`
- Gafson request: `docs/validation/GAFSON_DATA_REQUEST_V36.md`
- Therapy branch map: `analysis/v36_therapy_branch_map/`
- DMF sensitivity: `analysis/v36_ms_dmt_locked_sensitivity/`
- Power simulations:
  - `analysis/v36_gafson_power_simulation/`
  - `analysis/v36_gafson_power_attenuation/`
