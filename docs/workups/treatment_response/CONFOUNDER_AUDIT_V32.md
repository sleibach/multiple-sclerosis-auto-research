# Confounder Audit V32: V22 APC/HLA-II Treatment-Response Signal

Date: 2026-06-07

## Verdict

The immutable V22 bounded APC/HLA-II scalar is **not explained away** by the
highest-risk confounders tested here. It survives baseline APC/HLA-II,
glucocorticoid/steroid-response, and cell-composition adjustment on the
bounded V23 cohort set.

The honest classification is **PARTIALLY CONFOUNDED / IMMUNE-TONE BOUNDED**,
not artifact. The broad metabolic/inflammatory/STAT1 joint adjustment attenuates
the residualized locked-score AUC from `0.811` to `0.656` and loses permutation
support (`p = 0.163`), while adding the locked scalar to the same confounder set
still improves leave-one-out CV AUC from `0.611` to `0.733`. That means the
signal is partly entangled with broader immune-tone biology, but the audit does
not support calling it a glucocorticoid, baseline-state, proliferation, or
cell-composition artifact.

## Cohorts and Rule

No rule tuning was performed. `docs/locked_rules/LOCKED_RULE_V22.md` remained
immutable.

Audited bounded cohorts:

| Cohort | Context | Subjects |
|---|---:|---:|
| `GSE235357` | MS dimethyl fumarate, Class C | 10 |
| `GSE253006_TOF_exact` | UC tofacitinib exact raw-10x rescore, Class A | 9 |

Combined audited set: `n = 19`, locked scalar AUC `0.811` with stratified
bootstrap CI `0.571-1.000`.

Generated files:

- `analysis/v32_confounder_audit/v32_subject_confounder_scores.tsv`
- `analysis/v32_confounder_audit/v32_confounder_gene_coverage.tsv`
- `analysis/v32_confounder_audit/v32_confounder_adjustment_metrics.tsv`
- `analysis/v32_confounder_audit/v32_joint_adjustment_metrics.tsv`
- `analysis/v32_confounder_audit/v32_summary.json`

## Method

For each cohort, genes were z-scored within the cohort expression matrix. Frozen
gene-set scores were computed as the mean z-score of present genes. Paired
baseline and first eligible on-treatment samples were converted to baseline and
delta confounder scores.

For each confounder score the audit measured:

1. Confounder association with response by oriented AUC.
2. Spearman correlation with the locked V22 scalar.
3. Locked-score survival after residualizing the locked scalar against the
   confounder plus cohort.
4. Stratified bootstrap CI and stratified label-permutation p value for the
   residualized score.
5. Leave-one-out CV AUC for confounder-only versus locked-plus-confounder
   logistic models with cohort indicators and median imputation.

Verdict rule:

- `EXPLAINED_AWAY`: adjusted AUC `< 0.60` or AUC attenuation `>= 0.20`.
- `ATTENUATES`: AUC attenuation `>= 0.10`.
- `SURVIVES`: otherwise.

## Gene Coverage

Coverage was adequate for interpretation. Most panels were complete in both
cohorts. `GSE235357` missed `GILZ` as a literal symbol in the glucocorticoid
set, but included `TSC22D3`, the canonical symbol for the same glucocorticoid
response gene; its glucocorticoid coverage was therefore `9/10` by literal
gene symbol.

## Single-Panel Results

All `23` single baseline/delta confounder tests were classified as `SURVIVES`.

| Panel | Strongest tested feature | Confounder AUC | Corr. with locked score | Adjusted locked AUC | LOOCV confounder-only -> locked+confounder | Verdict |
|---|---:|---:|---:|---:|---:|---|
| Baseline APC/HLA-II | baseline APC/HLA level | `0.511` | `-0.581` | `0.856` | `0.000 -> 0.733` | survives |
| Glucocorticoid/steroid | delta glucocorticoid response | `0.578` | `-0.137` | `0.900` | `0.000 -> 0.822` | survives |
| Glucocorticoid/steroid | baseline glucocorticoid response | `0.544` | `0.433` | `0.856` | `0.156 -> 0.700` | survives |
| IFN suppression | delta inverse ISG | `0.722` | `-0.672` | `0.789` | `0.578 -> 0.733` | survives |
| STAT1 axis | delta STAT1 axis | `0.611` | `-0.572` | `0.856` | `0.522 -> 0.733` | survives |
| Metabolism | delta glycolysis | `0.689` | `-0.658` | `0.900` | `0.156 -> 0.767` | survives |
| Metabolism | delta immunometabolism/HIF/NAMPT | `0.567` | `-0.551` | `0.933` | `0.000 -> 0.767` | survives |
| General inflammation | delta inflammatory tone | `0.500` | `-0.200` | `0.889` | `0.000 -> 0.778` | survives |
| Proliferation | delta proliferation | `0.711` | `-0.281` | `0.956` | `0.156 -> 0.767` | survives |
| Cell composition | delta T-cell markers | `0.689` | `-0.667` | `0.800` | `0.589 -> 0.722` | survives |
| Cell composition | delta B-cell markers | `0.622` | `-0.461` | `0.833` | `0.433 -> 0.689` | survives |
| Cell composition | delta myeloid markers | `0.600` | `-0.365` | `0.922` | `0.000 -> 0.778` | survives |

The two highest-risk confounders from V31, glucocorticoid response and
cell-composition shifts, did not explain the signal.

## Joint Adjustment

| Joint set | Adjusted AUC | Permutation p | LOOCV confounders-only -> locked+confounders | Verdict |
|---|---:|---:|---:|---|
| Baseline APC/HLA-II + baseline/delta glucocorticoid | `0.933` | `0.0020` | `0.156 -> 0.789` | survives |
| Cell-composition markers | `0.811` | `0.0130` | `0.467 -> 0.622` | survives |
| Metabolic + inflammatory + STAT1/IFN family | `0.656` | `0.1629` | `0.611 -> 0.733` | attenuates |

The broad metabolic/inflammatory/STAT1 family is the main interpretive caveat.
It overlaps the biology the locked scalar is intended to monitor, so this is
not a clean nuisance covariate. Still, it means future validation must report
both unadjusted locked-rule performance and adjusted performance against these
immune-tone panels.

## Interpretation

The V22/V23 bounded signal remains a provisional early-treatment monitoring
lead. This audit strengthens it against the specific artifact concerns raised
by V31:

- not explained by baseline APC/HLA-II state;
- not explained by scored glucocorticoid/steroid response;
- not explained by marker-level bulk cell-composition shifts;
- not explained by proliferation.

It also narrows the claim:

- the scalar is not separable from all broader immune-remodeling context;
- metabolic/inflammatory/STAT1 adjustment attenuates the signal enough that
  validation should treat this as a bounded immune-tone monitoring rule, not a
  purely APC/HLA-II-specific biomarker.

## Limitations

- `n = 19` remains small. The audit is a confounder stress test, not clinical
  validation.
- Bulk cell-composition scores are marker proxies, not full deconvolution.
- No direct steroid-exposure metadata was available; glucocorticoid response
  was tested by expression signature.
- Age/sex and other clinical covariates were not harmonized in this run.
- `GSE253006_TOF_exact` remains cross-disease and exact-module exploratory
  support, not an MS DMT validation cohort.

## Validation Consequence

The future Gafson/NEDA or equivalent validation run should score the V32
confounder panels prospectively and report:

1. Primary immutable V22 locked-scalar performance.
2. Steroid/glucocorticoid-adjusted performance.
3. Cell-composition-adjusted performance.
4. Broad metabolic/inflammatory/STAT1-adjusted performance.

The V22 rule itself must not be retuned. If the future cohort validates
unadjusted but fails broad immune-tone adjustment, the claim should be framed
as an immune-remodeling monitoring signal rather than an APC/HLA-II-specific
mechanism.
