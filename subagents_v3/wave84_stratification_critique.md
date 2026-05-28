# Wave84 Sidecar A: Hostile Statistical Critique Of Stratification-First Branch

## Scope

Critique target: whether baseline `lysosomal_apc`, `lysosomal_apc__resid_inflammatory_nfkb`,
`ifn_lysosomal_apc_composite`, or related IFN/APC-lysosomal scores genuinely
predict anti-TNF response across RA `GSE198520` and IBD `GSE282122`, rather
than reflecting generic severity, cell composition, pathotype, label imbalance,
or overfitting.

Local sources used:

- `CONVERGENCE_CHECK_44.md`
- `results_v3/wave75_response_state_stratification/REPORT.md`
- `results_v3/wave75_response_state_stratification/cross_dataset_response_convergence.tsv`
- `results_v3/wave75_response_state_stratification/response_state_stratification_decision.tsv`
- `results_v3/wave76_adjusted_response_specificity/REPORT.md`
- `results_v3/wave76_adjusted_response_specificity/adjusted_cross_dataset_convergence.tsv`
- `results_v3/wave76_adjusted_response_specificity/adjusted_response_specificity_decision.tsv`
- `results_v3/wave76_adjusted_response_specificity/ra_wide_patient_table.tsv`
- `results_v3/wave76_adjusted_response_specificity/ibd_wide_patient_cellstate_table.tsv`
- `results_v3/wave84_stratification_first_audit/REPORT.md`
- `results_v3/wave84_stratification_first_audit/stratification_context_tests.tsv`

## Hostile Verdict

`NO_CLAIM_YET`. The branch has a real-looking tissue anti-TNF response signal,
but it is not yet a defensible biomarker claim. The best interpretation is:
baseline lysosomal/APC activity is a candidate tissue inflammatory-response
state, not yet a treatment-specific predictor. The current evidence is fragile
to adjustment, multiple testing, cell/tissue context, and endpoint definition.

## What Looks Real

- Wave75 found directionally stable nominal baseline associations for
  `lysosomal_apc`: RA effect `1.0179392799502753`, `p=0.0011271368016719564`,
  `FDR=0.03193554271403876`; IBD DC effect `0.8878463637078594`,
  `p=0.02039491399647716`, `FDR=0.09838770327180701`
  (`results_v3/wave75_response_state_stratification/cross_dataset_response_convergence.tsv`).
- The inflammatory-NFkB residualized version retained nominal direction:
  RA effect `0.9340213048095825`, `p=0.0030741099508615165`,
  `FDR=0.045128816259966884`; IBD DC effect `0.7897963481419672`,
  `p=0.03919596760603056`, `FDR=0.15143896575057259`
  (`results_v3/wave75_response_state_stratification/cross_dataset_response_convergence.tsv`).
- Wave76 adjustment did not invert the baseline signal. For
  `lysosomal_apc__resid_inflammatory_nfkb`, RA coefficient was
  `0.2887343634077032`, `p=0.07461177391074894`; IBD DC coefficient was
  `0.26043358269054373`, `p=0.03685687037603121`; sign stability was `True`
  (`results_v3/wave76_adjusted_response_specificity/adjusted_cross_dataset_convergence.tsv`).
- Wave84's direct residualized context test again found nominal tissue support:
  RA `lysosomal_apc__resid_inflammatory_nfkb` adjusted effect
  `0.2707064440560306`, `p=0.03441316781972741`, oriented AUC
  `0.6861598440545809`; IBD DC adjusted effect `0.19229134127296632`,
  `p=0.06807732763683204`, oriented AUC `0.6634615384615384`
  (`results_v3/wave84_stratification_first_audit/stratification_context_tests.tsv`).

## Why I Do Not Trust It Yet

1. **Multiple-testing correction is not supportive.**
   Wave76's best adjusted baseline row had RA `FDR=0.39544190713245103` and
   IBD `FDR=0.5048053278164863`; `passes_wave76_specificity=False`
   (`results_v3/wave76_adjusted_response_specificity/adjusted_response_specificity_decision.tsv`).
   Wave84's RA `lysosomal_apc__resid_inflammatory_nfkb` row had adjusted
   `FDR=0.21033265232747073`; the IBD DC residualized row had adjusted
   `FDR=0.2625839780277807`
   (`results_v3/wave84_stratification_first_audit/stratification_context_tests.tsv`).

2. **The signal does not beat generic inflammation strongly enough in IBD.**
   Wave76 required target/generic absolute coefficient ratio `>=2` in both
   datasets. RA passed with ratio `3.715017599182136`, but IBD DC failed with
   ratio `1.696206200721428`; `both_ratio_ge2=False`
   (`results_v3/wave76_adjusted_response_specificity/adjusted_response_specificity_decision.tsv`).

3. **Adjustment materially attenuates the RA effect.**
   RA `lysosomal_apc` raw Wave84 effect was `0.5769893044285537`, but adjusted
   effect was `0.27070644405603056`, a roughly `53%` reduction
   (`results_v3/wave84_stratification_first_audit/stratification_context_tests.tsv`).
   This is compatible with a confounded tissue-severity or composition marker.

4. **The RA result is sensitive to complete-case versus imputed residualization.**
   Wave76 used complete-case adjusted models with `ra_n=42` and found
   `lysosomal_apc__resid_inflammatory_nfkb` `p=0.07461177391074894`
   (`results_v3/wave76_adjusted_response_specificity/adjusted_cross_dataset_convergence.tsv`).
   Wave84 residualization used `n=46` and found `p=0.03441316781972741`
   (`results_v3/wave84_stratification_first_audit/stratification_context_tests.tsv`).
   The four-patient handling difference is large relative to the evidence margin.

5. **IBD remission is partly entangled with disease label.**
   In `results_v3/wave76_adjusted_response_specificity/ibd_wide_patient_cellstate_table.tsv`,
   DC rows are `CD: 10 remission / 5 non-remission` and
   `UC: 3 remission / 11 non-remission`. Disease is adjusted in Wave76, but
   with only `29` DC patient-cell-state rows, this is a high-leverage covariate.

6. **RA is bulk synovium, not myeloid-resolved.**
   Wave75 explicitly states RA `GSE198520` is bulk synovium
   (`results_v3/wave75_response_state_stratification/REPORT.md`). Pathotype
   is available but coarse: `Fibroid 3 good / 5 not-good`,
   `Lymphoid 7 good / 10 not-good`, `Myeloid 9 good / 12 not-good`
   in `results_v3/wave76_adjusted_response_specificity/ra_wide_patient_table.tsv`.
   This does not exclude macrophage/DC abundance, lymphoid aggregate burden,
   or fibroblast-rich tissue state as the real predictor.

7. **The cross-dataset result is partly winner-selected.**
   Wave75 chooses the strongest RA comparison and strongest IBD cell state by
   nominal `p` inside `convergence()` in
   `scripts/v3_wave75_response_state_stratification.py`. For `lysosomal_apc`,
   the winner is RA `good_vs_moderate_none` and IBD `DC`
   (`results_v3/wave75_response_state_stratification/cross_dataset_response_convergence.tsv`).
   This is reasonable for screening but not for a claim without an empirical
   max-statistic null.

8. **Dynamic support is not stable after adjustment.**
   Wave75 delta rows looked coherent for `lysosomal_apc`: RA effect
   `-0.6148352456800532`, `p=0.031579767260470175`; IBD DC effect
   `-1.06129714657032`, `p=0.008288395908054424`
   (`results_v3/wave75_response_state_stratification/cross_dataset_response_convergence.tsv`).
   Wave76 adjusted delta for the same module had RA coefficient
   `0.32590420055361874` and IBD DC coefficient `-0.20348939517742498`,
   `sign_stable=False`
   (`results_v3/wave76_adjusted_response_specificity/adjusted_cross_dataset_convergence.tsv`).
   A baseline predictor without coherent on-treatment pharmacodynamic movement
   is easier to dismiss as a severity proxy.

9. **The IBD bootstrap threshold effect is unstable.**
   Wave84 IBD DC `lysosomal_apc` high-vs-low response-rate difference was
   `0.3142857142857143`, but the bootstrap CI was
   `-0.10476190476190472` to `0.6523809523809524`.
   For `lysosomal_apc__resid_inflammatory_nfkb`, the rate difference was
   `0.17619047619047618`, CI `-0.23333333333333334` to
   `0.5961538461538461`
   (`results_v3/wave84_stratification_first_audit/stratification_context_tests.tsv`).

10. **Peripheral blood contradicts broad generalization.**
    Wave84 marked unresidualized `lysosomal_apc` as
    `NO_GO_TISSUE_SIGNAL_BLOOD_CONTRADICTION`: tissue direction was
    `higher_in_responders`, while RA blood CD14 monocytes had adjusted effect
    `-0.28185386623744013`, `p=0.03895049117175384`
    (`results_v3/wave84_stratification_first_audit/module_stratification_summary.tsv`).
    This does not refute tissue biomarker use, but it blocks any blood biomarker
    or pan-compartment claim.

## Concrete Tests The Orchestrator Should Run Next

1. **Empirical max-statistic permutation.**
   Shuffle response labels within RA `pathotype x biologic` strata and within
   IBD `Disease` strata. Re-run the exact Wave75/Wave76 module/endpoint/cell
   selection and record the minimum cross-dataset nominal `p` or maximum
   priority statistic. Required pass: empirical familywise `p<=0.10` for the
   pre-specified `lysosomal_apc__resid_inflammatory_nfkb` baseline route.
   Expected failure mode: the observed Wave75/Wave76 winner is common under
   label permutations because modules/endpoints/cell states were searched.

2. **Complete-case versus imputation sensitivity.**
   Force Wave84's residualized RA test to use the same `42` complete cases as
   Wave76, then force Wave76 to use the same imputation rule as Wave84.
   Required pass: coefficient sign and `p<0.10` remain stable under both.
   Expected failure mode: the RA `p` moves back toward Wave76's `0.07461177391074894`
   or crosses above `0.10`, showing that the Wave84 `0.03441316781972741`
   result is handling-sensitive.

3. **Cell-composition stress test for RA bulk synovium.**
   Add deconvolution or marker-derived fractions for macrophage/DC, B cell,
   T cell, plasma cell, fibroblast, endothelial, and neutrophil-like states to
   the RA model. At minimum, score lineage marker modules and include them with
   `pathotype`, `biologic`, `inflammatory_score`, and `das28_score`. Required
   pass: `lysosomal_apc__resid_inflammatory_nfkb` retains at least `50%` of
   the Wave84 adjusted effect (`>=0.1353532220280153`) and remains `p<0.10`.
   Expected failure mode: the coefficient collapses, implying the signal is
   macrophage/DC abundance or tissue architecture rather than a molecular state.

4. **Disease-stratified IBD validation.**
   Run the IBD DC baseline model separately in CD and UC despite low power.
   Required pass: both diseases have the same positive direction and AUC `>0.60`.
   Expected failure mode: CD drives the signal because DC rows are
   `10 remission / 5 non-remission` in CD versus `3 remission / 11 non-remission`
   in UC.

5. **Ordinal RA endpoint rather than binary winner labels.**
   Fit ordered or multinomial models for `good`, `moderate`, and `none`, and a
   continuous model against `delta_das28`. Required pass: monotonic ordering
   `good > moderate > none` for baseline lysosomal/APC score and Spearman
   direction consistent with larger DAS28 improvement. Expected failure mode:
   only the `good_vs_moderate_none` split works, indicating label-threshold
   artifact.

6. **Matched-module null.**
   Build random modules matched to `lysosomal_apc` by gene count, mean
   expression, and inter-gene correlation in each dataset. Repeat the full
   RA/IBD convergence analysis. Required pass: observed cross-dataset statistic
   is in the top `5%` of matched modules. Expected failure mode: many
   high-expression APC/lysosomal/HLA-ish modules perform similarly.

7. **Treatment specificity test.**
   Compare anti-TNF tissue response with non-TNF contexts already in
   `results_v3/wave84_stratification_first_audit/secondary_pharmacodynamic_or_small_response_contexts.tsv`.
   Required pass: anti-TNF baseline effect is stronger than non-TNF
   pharmacodynamic/response contexts after harmonizing endpoint and module.
   Expected failure mode: lysosomal/APC is a generic inflammatory-treatment
   response marker, not anti-TNF-specific.

8. **Leave-one-context-out convergence.**
   Recompute convergence after removing RA, IBD DC, or IBD Mono_macro one at a
   time. Required pass: no single context is necessary for a positive branch
   call. Expected failure mode: the claim depends on RA plus IBD DC only;
   IBD Mono_macro `lysosomal_apc` adjusted effect is only
   `0.11329815373375358`, `p=0.3619208213388343`
   (`results_v3/wave84_stratification_first_audit/stratification_context_tests.tsv`).

## Stop/Promote Criteria I Would Enforce

- Promote only if the permutation max-statistic is `<=0.10`, complete-case and
  imputed models agree, disease-stratified IBD has same direction in CD and UC,
  and RA composition adjustment preserves at least half the effect.
- Otherwise keep the branch as `PARK_TISSUE_STRATIFICATION_SIGNAL`: useful for
  designing a prospective tissue biomarker study, not sufficient for
  `FINDING_V3.md`.
