# Wave51 Reachable Stromal/Surface Audit

Random seed: `20260527`.

## Verdict

- `FAP`: `NO_GO_REACHABLE_SURFACE_STROMAL_ROUTE`; FAP remains reachable/druggable-looking but not promotable: local positives=2.0, negatives=0.0, MS delta=-999.0, p=1.0, FDR=None, strict residual=0.0, GWAS traits=15, EuropePMC=218, ClinicalTrials=5.
  - Blocker: FAP is a stromal/remodeling and imaging/prior-art saturated route without MS or perturbation proof; FXYD5 has surface accessibility and multi-tissue expression but no clear modality, no FDR-supported MS anchor, a conflicting Crohn negative signal, and unresolved Na/K-ATPase/barrier direction.
- `FXYD5`: `NO_GO_REACHABLE_SURFACE_STROMAL_ROUTE`; FXYD5 remains reachable/druggable-looking but not promotable: local positives=4.0, negatives=1.0, MS delta=0.3524746864413863, p=0.0587113391653537, FDR=0.8989378106274888, strict residual=0.0, GWAS traits=0, EuropePMC=101, ClinicalTrials=0.
  - Blocker: FAP is a stromal/remodeling and imaging/prior-art saturated route without MS or perturbation proof; FXYD5 has surface accessibility and multi-tissue expression but no clear modality, no FDR-supported MS anchor, a conflicting Crohn negative signal, and unresolved Na/K-ATPase/barrier direction.

## Gate Matrix

- `FAP` / `cross_disease_local_signal`: FAIL (`positive=2.0; negative=0.0`) - requires broad non-contradictory local signal.
- `FAP` / `strict_ms_anchor`: FAIL (`delta=-999.0; p=1.0; fdr=None`) - requires FDR-supported MS signal.
- `FAP` / `target_level_genetics`: PASS (`traits=15; min_p=6e-25`) - requires target/locus support.
- `FAP` / `strict_residual_state_survival`: FAIL (`0.0`) - requires survival after covariate/core-module residualization.
- `FAP` / `direction_and_safety_resolved`: FAIL (`unresolved`) - requires intervention direction that does not impair repair/barrier biology.
- `FAP` / `real_perturbation_anchor`: FAIL (`absent`) - requires disease-relevant perturbation rescue.
- `FAP` / `tractable_modality`: PASS (`activity_rows=37; best_nM=4.6; trials=5`) - requires usable inhibitor/antibody/modality.
- `FAP` / `novelty_prior_art_not_blocking`: FAIL (`EuropePMC=218; ClinicalTrials=5; prior_block=True`) - requires no direct crowded/prior-art blockage.
- `FXYD5` / `cross_disease_local_signal`: FAIL (`positive=4.0; negative=1.0`) - requires broad non-contradictory local signal.
- `FXYD5` / `strict_ms_anchor`: FAIL (`delta=0.3524746864413863; p=0.0587113391653537; fdr=0.8989378106274888`) - requires FDR-supported MS signal.
- `FXYD5` / `target_level_genetics`: FAIL (`traits=0; min_p=1.0`) - requires target/locus support.
- `FXYD5` / `strict_residual_state_survival`: FAIL (`0.0`) - requires survival after covariate/core-module residualization.
- `FXYD5` / `direction_and_safety_resolved`: FAIL (`unresolved`) - requires intervention direction that does not impair repair/barrier biology.
- `FXYD5` / `real_perturbation_anchor`: FAIL (`absent`) - requires disease-relevant perturbation rescue.
- `FXYD5` / `tractable_modality`: FAIL (`activity_rows=0; best_nM=nan; trials=0`) - requires usable inhibitor/antibody/modality.
- `FXYD5` / `novelty_prior_art_not_blocking`: PASS (`EuropePMC=101; ClinicalTrials=0; prior_block=False`) - requires no direct crowded/prior-art blockage.
