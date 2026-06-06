# Wave105 CD82 Hostile Methods Review

Scope: reviewed `scripts/v3_wave105_cd82_niche_robustness_audit.py`, `results_v3/wave105_cd82_niche_robustness_audit/REPORT.md`, and upstream Wave104 niche-controller report/results. This is a methods attack, not a finding claim. Where I could not verify a point from the local artifacts, I say so.

## Bottom Line

Severity: **critical**.

The branch call should be downgraded from `REOPEN_CD82_ROBUST_NICHE_SIGNAL` to at most **provisional niche-biomarker signal requiring confirmatory validation**. A stricter reading is `NO_REOPEN_CD82_AFTER_ROBUSTNESS_UNTIL_MULTIPLICITY_AND_CONFOUNDING_PASS`.

The current reopen decision is not robust enough for the word "robust". It rests on four nominally positive M3 rows, three from the same Crohn epithelial-to-myeloid donor set and one borderline Sjogren row. After Benjamini-Hochberg correction across the nine M3-tested contexts, only Crohn `lysosomal_apc` remains significant (`m3_p` q=0.0314; `m3_perm_p` q=0.0180). The Crohn `lipid_loader_repair`, Crohn `complement_phagocytosis`, and Sjogren `lysosomal_apc` rows all fail FDR at 0.05.

## Critical Criticisms

1. **Multiplicity is ignored at the exact place where the branch call is made.**

   Severity: **critical**.

   Wave105 tests 24 CD82 contexts in the summary and 168 model-grid rows, then declares robustness using per-row nominal M3 thresholds (`p < 0.05`, `perm_p < 0.05`) in `summarize_tests()` (`scripts/v3_wave105_cd82_niche_robustness_audit.py:343-350`). The report's "robust" rows have marginal p-values: Crohn lipid `m3_perm_p=0.01599`, Sjogren lysosomal `m3_perm_p=0.04548`, Crohn complement `m3_perm_p=0.04298`. These are exactly the kind of p-values that disappear under family correction.

   Verified check: applying BH correction to the nine non-missing M3 tests gives only one surviving row: Crohn epithelial -> myeloid `lysosomal_apc`. The other three "robust" rows have q values around 0.072-0.102. If correcting across all 24 contexts, all but the top row would be even weaker.

   Exact fix/test: add BH q-values and maxT/permutation family-wise p-values to `cd82_robustness_summary.tsv`; require at least two disease-level positives with `m3_perm_q < 0.05` or family-wise p < 0.05. Recompute the branch call from corrected p-values, not nominal p-values.

2. **Disease-level replication is overstated because Crohn contributes three of four "robust" rows from the same 12 donors.**

   Severity: **critical**.

   The report counts two diseases, but the four robust contexts are not four independent tests. Three are the same source/target pair (`ibd_crohn_epithelial -> ibd_crohn_myeloid`) on the same 12 donors, merely different target modules. The second disease support is a single borderline Sjogren epithelial `lysosomal_apc` M3 row (`m3_p=0.03835`, `m3_perm_p=0.04548`) that fails FDR.

   Verified composition: CD82 Crohn epithelial has 6 case and 6 control donors; Sjogren epithelial has 9 case and 13 control donors. UC epithelial has the same 6/6 structure but does not pass M3 (`lipid_loader_repair p=0.255`, `lysosomal_apc p=0.960`, `complement p=0.592`).

   Exact fix/test: collapse target modules within each disease/source-target pair before branch calling. Use one prespecified primary module, or combine module p-values per disease with Brown/Fisher/Stouffer while accounting for module correlation. Require independent disease-level q-significant replication after collapsing. Under the current outputs, this likely downgrades to one convincing disease.

3. **The strict M4 model is treated as supportive when it is not run.**

   Severity: **critical**.

   For the Crohn robust rows, `M4_ifn_hla_extension` has `n=0` because 9 covariates on 12 donors are flagged as underpowered. The decision rule still allows underpowered M4 behavior to count as supportive (`scripts/v3_wave105_cd82_niche_robustness_audit.py:351-357`). That is backwards: an unestimable confounding model is missing evidence, not support.

   Exact fix/test: change `m4_supportive` so `fixed_underpowered` is neutral or failing, not supportive. Report an explicit `strict_model_estimable` flag. Recompute the branch call requiring either an estimable M4 with positive corrected evidence or an alternative prespecified low-dimensional confounder model that includes IFN/HLA with adequate degrees of freedom.

4. **Residualization p-values are anti-conservative for small n and selected/saturated covariates.**

   Severity: **critical**.

   The pipeline residualizes predictor and outcome separately, then applies `stats.linregress()` to residuals as if no covariates were estimated (`scripts/v3_wave104_accessible_survivor_niche_controller_test.py:104-154`; reused in Wave105 at `scripts/v3_wave105_cd82_niche_robustness_audit.py:174-186`). This does not propagate degrees of freedom correctly for partial regression. It is especially problematic at n=12 with 5 M3 covariates and catastrophic for adaptive M5/M6 with 8 covariates.

   Evidence from outputs: Crohn M3 uses 12 donors and 5 covariates; adaptive Crohn M5 uses 8 covariates and reports predictor covariate R2=0.939. Sjogren M5 uses 12 covariates on 22 donors and loses the M3 signal (`p=0.141` for lysosomal), yet the branch call ignores that as non-primary.

   Exact fix/test: fit a single OLS model `target_module ~ source_gene_z + covariates` and report the coefficient, standard error, t-statistic, and p-value using correct residual degrees of freedom. Add HC3 robust SEs. For n=12, do exact or permutation tests using the full model residualization scheme with Freedman-Lane permutations and fixed covariates.

5. **Permutation p-values are not valid for the model-selection/search process.**

   Severity: **high**.

   Wave105 permutes residualized `x` against residualized `y` for each final model (`scripts/v3_wave105_cd82_niche_robustness_audit.py:156-171`). This only tests one chosen row and one chosen model. It does not preserve donor group strata, does not account for choosing CD82 from prior waves, choosing M3 as the robust model, screening multiple modules/diseases/source compartments, or adaptive covariate choice in Wave104.

   Exact fix/test: run a nested null that repeats the entire CD82 audit decision procedure under permutation: within each dataset/disease, permute donor labels or source-gene values within case/control strata; rebuild all M0-M6 tests; record the maximum evidence statistic across modules and source-target contexts; estimate the branch-level p-value. Also run a negative-control gene panel matched for expression/detection to estimate empirical false reopen rate.

## High-Severity Criticisms

6. **Donor pairing is matched by donor ID but not protected against shared upstream preprocessing, pseudo-replication, or module overlap.**

   Severity: **high**.

   The pair builder merges source and target rows by `dataset_path`, `disease_name`, `donor_id`, `disease`, and `group` (`scripts/v3_wave104_accessible_survivor_niche_controller_test.py:255-258`). That establishes same-donor pairing, but it does not prove independence of source predictor and target module outcome. Both source CD82 z-scores and target module scores originate from the same h5ad/donor processing and may share donor-level quality, inflammation, dissociation stress, cell-count, and library-size effects. I could not verify from these artifacts whether donor-level QC covariates, sample batch, site, sex, age, medication, or cell-count weights are available and controlled.

   Exact fix/test: add donor-level covariates where available: batch/sample, total cells per compartment, detection depth, percent mitochondrial/stress if available, source and target cell counts, medication/treatment, sex, age. If unavailable, state explicitly that unmeasured donor/batch confounding remains unresolved.

7. **Case/control composition is too thin for the key Crohn claim.**

   Severity: **high**.

   Crohn robust rows use only 12 donors: 6 cases and 6 controls. The case indicator is not enough to separate disease status from batch, sampling, tissue site, activity, or therapy. The UC paired analysis provides a same-dataset digestive-tissue counterexample with 6 cases and 6 controls, but CD82 does not survive M3 there. The report should treat this as a weakness, not merely a non-robust extra row.

   Exact fix/test: run case-only and control-only M3-compatible or reduced-covariate tests. Wave104 reports case-only CD82 effects as non-significant for key rows, including Sjogren stromal lysosomal (`case_only_p=0.4849`) and UC epithelial lipid (`case_only_p=0.6229`). Wave105 should explicitly require within-case support or state that disease/control mixing may drive the signal.

8. **Target-module circularity is insufficiently killed.**

   Severity: **high**.

   M5/M6 include target lipid/lysosomal modules as covariates except when equal to the target column, but the target modules are correlated biological readouts. A CD82 association with `lysosomal_apc` after adjusting for `target_lipid_loader_repair` can still be a target-module manifold artifact, and vice versa. Conversely, over-adjusting with highly collinear target modules can erase or invert real signal. The current audit alternates between M3 as the decision model and M5/M6 as "context excluding outcome", without a prespecified module-family strategy.

   Evidence: Crohn complement is M3-positive but M5/M6 flips negative in the report's `model_signs`. Sjogren epithelial lysosomal is M3-positive but M5/M6 is non-significant (`p=0.141`) after full context adjustment.

   Exact fix/test: define a primary target module before testing. Then run (a) module-family PC1 outcome, (b) leave-one-module-out residuals, and (c) negative-control modules unrelated to lipid/lysosomal/APC biology. Do not let a row pass if adding correlated target context flips direction or destroys the effect unless the biological estimand is explicitly "shared module manifold".

9. **Overfitting is still present despite the "fixed grid" framing.**

   Severity: **high**.

   The audit claims to replace adaptive single-model testing with a fixed grid, but the branch rule chooses M3 as the robust model because it is estimable and favorable. M4 is allowed to be absent, and M5/M6 are shown but not required. This is model-shopping by decision rule.

   Exact fix/test: preregister one primary model per sample-size regime before seeing results. For n=12, use at most case indicator plus one source/target inflammatory PC. For n=22, allow a second PC. Run all alternatives as sensitivity only. Recompute branch call from the primary model alone.

## Medium-Severity Criticisms

10. **Leave-one-donor-out sign stability is too weak as an influence diagnostic.**

    Severity: **medium**.

    `loo_positive_fraction=1` sounds strong, but for Crohn M3 it only means all 11-donor refits preserve positive slope. It does not test p-value stability, leverage, Cook's distance, or whether one subgroup creates the association. For adaptive M5 Crohn, LOO slopes can cross negative (`loo_min_slope=-1.38` for lysosomal; `-0.686` for lipid; `-3.03` for complement), showing fragility under richer adjustment.

    Exact fix/test: add Cook's distance, DFBETAs, leave-one-case-control-pair-out, leave-two-out, and bootstrap confidence intervals. Plot residualized x/y with donor labels for the four claimed robust rows.

11. **The branch rule ignores robust negative or direction-conflict evidence outside M3.**

    Severity: **medium**.

    `robust_negative` only checks M3 negativity (`scripts/v3_wave105_cd82_niche_robustness_audit.py:360-366`). But direction conflicts exist in M5/M6 signs for Crohn complement and Sjogren lipid. If the audit is hostile, richer-model sign flips should count as fragility, not be excluded from "robust negative disease" accounting.

    Exact fix/test: add a `direction_conflict` flag for any estimable model M0-M6 with opposite sign and p/permutation p below a relaxed threshold. Require no direction conflict in any prespecified sensitivity model.

12. **The report does not quantify uncertainty around slopes.**

    Severity: **medium**.

    Slopes are reported without confidence intervals. In small n partial regressions, a p-value without effect uncertainty is inadequate.

    Exact fix/test: report 95% CIs from OLS and bootstrap CIs from donor resampling stratified by group. Require CIs to exclude zero for disease-level primary tests after correction.

## Exact Downgrade Rationale

The current `REOPEN_CD82_ROBUST_NICHE_SIGNAL` call requires robust positive coupling in at least two diseases with no robust negative disease. That rule is too permissive because:

- the second disease support is one borderline Sjogren M3 row that fails M3 FDR;
- Crohn contributes multiple module rows from the same 12 donors, not independent replication;
- unestimable M4 is treated as supportive for the Crohn rows;
- residualization p-values are likely anti-conservative;
- the permutation test is row-level, not branch-level;
- UC and psoriasis do not provide supportive disease-level replication.

Recommended revised call: **`CD82_PROVISIONAL_NICHE_BIOMARKER_SIGNAL_NOT_REOPENED`**.

## Tests To Run Next

1. Recompute Wave105 with correct OLS partial regression p-values and HC3 robust SEs.
2. Add BH q-values over all CD82 M3 contexts and over all model-grid tests; separately add disease-collapsed q-values.
3. Run nested branch-level permutations that repeat the whole decision rule and use max statistics across modules/source-target contexts.
4. Require estimable strict confounding models; do not count underpowered M4 as supportive.
5. Collapse correlated target modules into a prespecified module-family PC or one primary module before branch calling.
6. Run case-only and control-only reduced models; require within-case directional support for a disease mechanism claim.
7. Add batch/QC/cell-count covariates or explicitly mark them unavailable and unresolved.
8. Add matched negative-control genes and unrelated target modules to estimate empirical false-positive rate.
9. Add influence diagnostics: residual plots, Cook's distance, DFBETAs, leave-one-case-control-pair-out, leave-two-out, and stratified bootstrap CIs.
10. Re-run the branch call using disease-level independent units, not module rows.

## Verification Notes

- Verified local files read: Wave105 script/report/summary/model grid/robust tests and Wave104 script/report/matched pairs.
- Verified CD82 pair composition from local `matched_niche_pairs.tsv`: Crohn epithelial/myeloid 6 case + 6 control; UC epithelial/myeloid 6 case + 6 control; psoriasis source-target contexts 3 case + 3 control; Sjogren epithelial/APC and stromal/APC 9 case + 13 control.
- Verified multiplicity check locally with the project venv. System `python3` lacked pandas, so checks used `.venv_v3_py312/bin/python`.
- I did not verify raw h5ad-level batch/QC metadata availability; the review therefore treats batch/QC confounding as unresolved, not proven.
