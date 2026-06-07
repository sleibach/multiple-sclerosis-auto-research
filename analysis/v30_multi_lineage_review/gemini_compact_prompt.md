You are an adversarial reviewer. Return ONLY valid JSON, no markdown. Keep it under 1200 words. Output exactly: {"proposals":[...],"vulnerabilities":[...]}. At most 3 proposals and 3 vulnerabilities. Each item must be concrete and testable on existing local data. Include fields short_name, concrete_test, data_artifacts, expected_if_true, falsifies_if. Model output is not evidence; this is only a proposal queue.

## meta/CURRENT_STATUS.md
# Current Status

Last updated: 2026-06-06 14:32 CEST

## Mission State

V12 completed the supported-cell axis-disagreement matrix that V11 made
resumable. V13-V17 robustified the genetics axis from OpenGWAS coloc through
allele-aligned eQTL and mechanism workup. V18 completed data-source acquisition
triage for the unresolved chr1 MS-UC `GPR25`-versus-`KIF21B` causal-gene
ambiguity. V19 re-evaluated the chr1 locus under first-principles
druggability discipline. V20 widened back out from chr1 to a ranked
next-tier lead slate across the full landscape. V21 established the first
LDSC genome-wide genetic-correlation backdrop and vetted the two queued
next-tier genetics regions. V22 locked and tested the dynamic APC/HLA-II
treatment-response monitoring rule on reachable held-out cohorts. V23 pooled
the small cohorts, resolved the UC tofacitinib exact-module caveat, and bounded
the monitoring lead by therapy mechanism. V27 showed coupled-axis successors do
not beat the immutable V22 scalar. V28 then stress-tested the bounded signal
with heterogeneous local tools and found the scalar statistically tool-robust
but not improved by flexible ML, receptor-only, coupled-axis, or generic
dynamic-vector variants. V29 checked for a cross-lineage independent model key;
none was configured, so the adversarial review package was queued. The local
dormant-lead reactivation pass found no intervention-grade dormant rescue.

Current frontier:

- V22 treatment-response result:
  - `docs/locked_rules/LOCKED_RULE_V22.md` was committed before validation (`013639b`).
  - Primary locked validation is mixed:
    - `GSE235357` MS dimethyl fumarate passed the small-n rule: AUC `0.72`,
      Hedges g `0.651`, `n=10`.
    - `GSE250453` MS fingolimod failed: AUC `0.60`, Hedges g `0.150`, `n=10`.
    - `GSE85034_ADA` psoriasis adalimumab failed: AUC `0.511`, Hedges g
      `0.044`, `n=14`.
  - `GSE253006_TOF` UC tofacitinib passed numerically but is exploratory, not
    primary locked validation, because it uses precomputed all-cell module
    summaries broader than the exact frozen V22 module.
  - Verdict: no Tier 4 breakthrough and no kill. The dynamic APC/HLA-II rule
    remains a provisional early-treatment monitoring lead, not a validated
    baseline stratifier or clinical rule.
- V23 treatment-response workup:
  - Unbounded primary locked pooled AUC is weak: `0.547`, stratified bootstrap
    CI `0.337-0.743`.
  - Exact raw-10x rescoring resolves the `GSE253006_TOF` module caveat at
    all-cell level: AUC `0.95`, CI `0.70-1.00`, Hedges g `1.811`.
  - Exact marker-derived GSE253006 compartments pass most strongly in
    `t_cell_like` (AUC `1.00`, g `1.270`, receptor AUC `0.60`) and
    `b_plasma_like` (AUC `0.95`, g `1.487`, receptor AUC `0.75`), with
    myeloid/APC-like positive but weaker (AUC `0.80`).
  - Bounded DMF plus exact tofacitinib set: pooled AUC `0.811`, CI
    `0.567-1.000`, Hedges g `1.191`.
  - Verdict: bounded early-monitoring hypothesis for immune-remodeling /
    JAK-STAT contexts; no V23 successor rule locked because no fresh held-out
    dataset remains for honest testing.
- V28 heterogeneous robustness workup:
  - Report: `docs/workups/treatment_response/ROBUSTNESS_MAP_V28.md`.
  - Tooling: `meta/TOOLING_INVENTORY_V28.md`; optional external LLM key
    request: `meta/TOOL_KEY_REQUESTS_V28.md`.
  - Bounded V22 scalar: AUC `0.811`, Hedges g `1.191`, permutation p `0.0080`.
  - Cohort-adjusted locked-score coefficient remains positive: `0.322`,
    robust p `5.70e-07`.
  - Bayesian-bootstrap posterior P(responder mean score > nonresponder mean
    score): `0.999`.
  - Jackknife bounded AUC range: `0.788-0.888`; no single subject removes the
    signal.
  - Ridge multifeature ML, receptor-only control, V27 coupled features, and
    dynamic-vector features do not beat the scalar.
  - Verdict: the bounded signal is statistically tool-robust but
    model-flexibility fragile; validate the scalar, do not add complexity.
- V29 dormant-lead reactivation:
  - Reports: `docs/history/LEAD_INVENTORY_V29.md` and
    `meta/INDEPENDENT_REVIEW_QUEUE_V29.md`.
  - Cross-lineage keys checked: `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, and
    `GEMINI_API_KEY` absent.
  - No independent sub-model output was used.
  - No dormant lead became intervention-grade.
  - Best reactivated biology lead: postpartum HLA-II/CD64 APC-axis split for
    flare-timing/natural-experiment work.
  - MIF/CD74 is partially reactivated as coupled APC mechanism context, not as
    a standalone target or predictor.
  - ZMIZ1 remains a robust transfer-validity decoupling finding.
  - NAMPT, PTGER4, ZFP36L1, REL/PUS10/USP34, and generic TYK2 remain parked or
    closed under current standards.
- `GPR25` remains a live eQTLGen-supported lead, but not a protected favorite:
  public V18 immune-QTL sources did not support it, and its required therapeutic
  direction is agonism/restoration of a sparsely tooled receptor.
- `KIF21B` now has independent dense QTD000021 coloc support against the chr1
  disease signal: MS/eQTL PP.H4 `0.874879034973956`, UC/eQTL PP.H4
  `0.868660082128031`; exact shared credible-set variants show risk alleles
  lowering KIF21B expression `11 / 11` for both MS and UC.
- The chr1 locus is a tractable genetics/mechanism lead, not an
  intervention-grade target. Controlled or richer immune-genotype/protein data
  remain the decisive next layer, but V20 does not continue chr1.
- `docs/history/LEAD_SLATE_V20.md` now ranks 13 next-tier cand

## docs/workups/treatment_response/ROBUSTNESS_MAP_V28.md
# Robustness Map V28

Date: 2026-06-07

## Scope

V28 re-attacked the bounded APC/HLA-II early treatment-response monitoring lead
with heterogeneous local tools and a paid/gated-tool preflight. The immutable
baseline remained `docs/locked_rules/LOCKED_RULE_V22.md`; no V22 module, class,
threshold, endpoint, or cohort rule was edited. No fresh Gafson/NEDA cohort was
present or read.

Executable analysis:

- `scripts/v28_heterogeneous_response_analysis.py`

Outputs:

- `analysis/v28_heterogeneous_response/heterogeneous_method_metrics.tsv`
- `analysis/v28_heterogeneous_response/cohort_adjusted_models.tsv`
- `analysis/v28_heterogeneous_response/bayesian_bootstrap_effects.tsv`
- `analysis/v28_heterogeneous_response/jackknife_influence.tsv`
- `analysis/v28_heterogeneous_response/v28_summary.json`

Seed: `28028`.

## Tooling Result

Reachability inventory:

- `meta/TOOLING_INVENTORY_V28.md`

Paid/gated key requests:

- `meta/TOOL_KEY_REQUESTS_V28.md`

No paid service was used in V28. `OPENAI_API_KEY` is requested as an optional
low-cost external critique/proposal lens. The OpenAI API host is reachable, but
no key is currently configured. Sub-model output was therefore not used as
evidence or as an ungrounded claim.

## Workstream A: Heterogeneous Re-Analysis

Primary set: bounded immune-remodeling/JAK-STAT domain:

- `GSE235357` MS dimethyl fumarate.
- `GSE253006_TOF_exact` UC tofacitinib exact rescoring.
- `n = 19`.

### Fixed-Score / Nonparametric Evidence

| Score | AUC | Bootstrap CI | Hedges g | Permutation p | Mann-Whitney greater p |
|---|---:|---|---:|---:|---:|
| V22 locked scalar | `0.811` | `0.578-1.000` | `1.191` | `0.0080` | `0.0124` |
| receptor control | `0.656` | `0.367-0.900` | `0.637` | `0.1419` | `0.1352` |
| V27 coupled projection | `0.689` | `0.414-0.917` | `0.661` | `0.0740` | `0.0890` |
| V27 coupled augmented | `0.633` | `0.352-0.869` | `0.542` | `0.1864` | `0.1739` |
| V27 coupling coordination | `0.733` | `0.477-0.932` | `0.777` | `0.0435` | `0.0471` |

Interpretation: the original locked scalar is the strongest fixed score. The
receptor control does not reproduce it. One coupled feature remains directional
but weaker than the scalar, consistent with V27.

### Cohort-Adjusted Model

Linear probability model with cohort fixed effects:

- bounded set: locked-score coefficient `0.322`, robust p
  `5.70e-07`, R2 `0.331`.
- all primary plus exact UC: locked-score coefficient `0.231`, robust p
  `0.00263`, R2 `0.130`.

Interpretation: the signal is not only a raw pooled rank artifact; it remains
positive after accounting for cohort labels. This is still small-n and should
not be mistaken for external validation.

### Bayesian Bootstrap

Posterior over responder-minus-nonresponder mean locked score:

- bounded set: mean difference `0.994`, 95% interval `0.388-1.715`,
  posterior P(diff > 0) `0.999`.
- all primary plus exact UC: mean difference `0.494`, 95% interval
  `0.067-0.979`, posterior P(diff > 0) `0.9885`.

Interpretation: under a distribution-light Bayesian-bootstrap lens, the locked
score direction is stable in the bounded set and remains positive, but smaller,
when the failed/out-of-domain cohorts are included.

### Regularized ML Lens

Ridge logistic LOOCV using `delta_IFN_APC`, `delta_HLAII`, `delta_RECEPTOR`,
and `locked_signed_score`:

- bounded set AUC `0.578`, CI `0.286-0.856`, Hedges g `0.582`.
- all primary plus exact UC AUC `0.575`, CI `0.402-0.747`, Hedges g `0.123`.

Interpretation: flexible multifeature modeling does not improve the lead; it
dilutes it. This is important. The signal is not strengthened by throwing more
features or model flexibility at the tiny cohorts. The most defensible form
remains the pre-locked scalar.

Heavier tree/SVM/Gaussian-process branches were reachable in principle through
scikit-learn but were not retained for the final V28 run because LOOCV/null
runtime was disproportionate to the tiny sample size. This limitation does not
affect the primary fixed-score conclusion.

## Workstream B: Sub-Model Lens

No external LLM or hosted foundation-model key was present. V28 therefore did
not use sub-model output. This is a documented block, not a silent omission.

Grounded local hostile proposals tested instead:

| Proposal | Grounded test | Result |
|---|---|---|
| Receptor-state confounding could explain the pass. | Receptor-only module AUC and permutation p. | Failed: receptor AUC `0.656`, p `0.142`, weaker than scalar by `0.156`. |
| Cohort pooling could explain the pass. | Cohort fixed-effect model. | Failed as sole explanation: locked-score coefficient remains positive, robust p `5.70e-07` in bounded set. |
| One or two subjects could drive the bounded pass. | Leave-one-subject jackknife. | Failed as sole explanation: bounded jackknife AUC range `0.788-0.888`; no single subject removes the signal. |
| V26 dynamic/coupled geometry could improve the rule. | Coupled and dynamic adjacent feature tests. | Mostly failed: coupled features and vector/angle features do not beat V22 scalar. |

If `OPENAI_API_KEY` is provided, the next run can use the requested checker and
ask for additional critique proposals, but those proposals must still be
implemented against these same local data before they matter.

## Workstream C: Cross-Tool Robustness Verdict

Agreement:

- The bounded V22 scalar is positive under raw AUC, nonparametric rank test,
  permutation null, cohort-adjusted regression, Bayesian bootstrap, and
  jackknife influence analysis.
- The r

## docs/history/LEAD_INVENTORY_V29.md
# Lead Inventory V29

Date: 2026-06-07

## Scope

V29 performs a grounded dormant-lead reactivation and cross-domain reframing
pass after V28 settled the bounded APC/HLA-II monitoring lead computationally.
No locked rule was edited. No fresh validation cohort was present or read.

Cross-lineage sub-model status:

- `ANTHROPIC_API_KEY`: absent.
- `GOOGLE_API_KEY`: absent.
- `GEMINI_API_KEY`: absent.

Therefore Workstream A is queued in
`meta/INDEPENDENT_REVIEW_QUEUE_V29.md`; no independent sub-model proposals were
used in this run.

RAG query before analysis:

```bash
.venv_v3_py312/bin/python scripts/query_knowledge_index.py \
  "V29 dormant leads NAMPT MIF CD74 PTGER4 ZMIZ1 KIF21B GPR25 ZFP36L1 TYK2 reactivation" 12
```

Top hits included `meta/NEXT_ACTIONS.md`, `knowledge/candidates/KIF21B.md`,
`knowledge/candidates/GPR25.md`, MIF/CD74 sidecars, V18 data acquisition, and
V16 ZMIZ1/PTGER4 reports. V29 therefore does not re-derive completed cells.

## Workstream B: Dormant-Lead Reactivation

### Summary Table

| Lead | Prior status | V29 re-grade | Reactivated? | Reason |
|---|---|---|---|---|
| APC/HLA-II treatment-response scalar | provisional bounded monitoring lead | top active computational lead, awaiting fresh validation | yes, already active | V28 confirmed statistical tool-robustness; complexity does not improve it. |
| MIF/CD74 axis | demoted as therapeutic mechanism | reactivated only as coupled-axis context / mechanism covariate | partial | V26 shows HLA-II/MIF-CD74 coupling is real, but V27/V28 show receptor/coupled features do not improve prediction. |
| NAMPT/eNAMPT | demoted to marker/readout | remains demoted marker/readout | no | V4/V5 issue was not only prior art; local evidence lacks MS/non-IBD retained residual and no eNAMPT-specific modality evidence. |
| KIF21B chr1 MS-UC | real shared genetics, hard target | remains real biology / difficult target | partial | Current standards strengthened, not weakened, the conclusion: causal evidence favors KIF21B, but risk lowers expression and restoration/up-function is hard. |
| GPR25 chr1 MS-UC | live but weakened causal candidate | remains conditional lead pending controlled data | partial | eQTLGen supports it, but V18 public immune-QTL and atlas evidence do not; agonism/restoration remains immature. |
| ZMIZ1 chr10 MS-Crohn | opposite-direction decoupling | robust decoupling/transfer-validity finding | yes as finding, not target | Same alleles increase ZMIZ1 expression, raise MS risk, and protect Crohn; blocks Crohn-to-MS target transfer. |
| PTGER4 chr5 MS-UC | closed mixed signal | remains closed / transfer warning | no | Mixed shared/distinct components and opposite disease-direction implications still block direction discipline. |
| ZFP36L1 chr14 MS-Crohn | V20 promising, V21 parked suggestive | remains parked suggestive | no | Bounded SuSiE PP.H4 `0.6877` is below robust threshold and direction/QTL coloc absent. |
| REL/PUS10/USP34 chr2 MS-UC | V20 promising, V21 closed | remains closed/not-now | no | Disease SuSiE produced no credible-set summary; expression/QTL context cannot rescue failed disease coloc. |
| TYK2 allosteric subgroup | negative/not-now | remains negative/not-now | no | Druggable class exists, but no MS-specific direction/subgroup anchor independent of generic IFN/JAK biology. |
| FPR2/ALX biased agonism | hard-target real biology | reactivated as wet-lab comparator only | partial | First-principles GPCR tractability exists, but ligand/cargo/context direction must be tested experimentally. |
| Postpartum HLA-II/CD64 APC split | promising natural experiment | reactivated as biomarker/natural-experiment lead | yes as Tier -1/Tier 0 biology | It may connect pregnancy/postpartum flare timing to APC-axis bifurcation; needs postpartum MS cohort. |

### Dormant-Lead Details

#### MIF/CD74

V5 demoted MIF/CD74 as a therapeutic mechanism because receptor-only or full
MIF/CD74 components did not retain adjusted FDR and CD74 collapsed into broad
APC/cell-size context. V26 changes the interpretation, not the therapeutic
verdict: HLA-II and MIF/CD74 receptor-state are strongly coupled across
modalities, so MIF/CD74 is a useful context variable for APC remodeling. V27
and V28 prevent over-promotion: adding receptor/coupling terms diluted or failed
to improve the locked scalar.

V29 verdict: **partial reactivation as mechanism context only**. Do not revive
MIF/CD74 as a direct target or standalone predictor without new perturbation or
compartment evidence.

#### NAMPT

NAMPT was vulnerable to prior-art over-gating earlier, but V4/V5 already
separated generic intracellular NAMPT inhibition from constrained eNAMPT or
marker biology. The retained local facts still kill active nomination:

- MS white-matter delta log2 `-0.214`, p `0.543`.
- Non-IBD retained positive disease count `0`.
- Strict core-covariate surviving disease count `0`.
- OpenTargets genetics score `0.0`.

V29 verdict: **no reactivation**. The corrected modern status is marker/readout
for HIF/NAD/eNAMPT inflammatory metabolism, not a therapeutic lead.

#### KIF21B / GPR25 chr1

V19 corrected the druggability-prior-art trap. The data-favored gene is no
longer dismissed for class reasons:

- KIF21B dense QTD000021 coloc: MS/eQTL PP.H4 `0.8749`, UC/eQTL PP.H4
  `0.8687`.
- Exact shared credible-set variants: risk lowers KIF21B expression `11/11` in
  both MS and UC.
- Direction-matched intervention would require restoration/up-function, not
  simple inhibition.

GPR

## meta/INDEPENDENT_REVIEW_QUEUE_V29.md
# Independent Review Queue V29

Date: 2026-06-07

## Key Status

Cross-lineage model keys checked after loading `.env`:

- `ANTHROPIC_API_KEY`: absent.
- `GOOGLE_API_KEY`: absent.
- `GEMINI_API_KEY`: absent.

Workstream A is therefore queued. No independent sub-model output was used in
V29, and no model-generated proposal is treated as evidence.

## Requested Model

Preferred: Anthropic Claude via `ANTHROPIC_API_KEY`.

Fallback: Google/Gemini via `GOOGLE_API_KEY` or `GEMINI_API_KEY`.

Reason for non-OpenAI request: this agent is OpenAI-lineage; V29 specifically
needs a different failure mode and different priors.

## Review Package To Feed The Independent Lens

Give the model the following project package, in this order:

1. `meta/CURRENT_STATUS.md`
2. `meta/NEXT_ACTIONS.md`
3. `docs/workups/treatment_response/ROBUSTNESS_MAP_V28.md`
4. `docs/workups/treatment_response/APC_HLA_MONITORING_WORKUP_V23.md`
5. `docs/findings/DEEP_STRUCTURE_V26.md`
6. `docs/history/LEAD_SLATE_V20.md`
7. `docs/history/LEAD_SLATE_V21.md`
8. `docs/workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md`
9. `docs/workups/genetics/GENETICS_EQTL_WORKUP_V16.md`
10. `knowledge/candidates/NAMPT.md`
11. `knowledge/candidates/MIF_CD74_STRATIFICATION.md`
12. `meta/MATRIX_STATUS.md`

## Prompt For Independent Lens

You are an adversarial reviewer from outside the project's usual
genetics/transcriptomics framing. Your output is not evidence; it is a proposal
queue for grounding.

Review the MS autoimmune research project and identify:

1. Overlooked cross-domain connections between treatment-response monitoring,
   genetics, pregnancy/postpartum biology, metabolism, structural biology, and
   tissue repair.
2. Dormant or parked leads that were dropped for a reason later corrected by
   the project, such as over-strict prior-art gating or class-precedent
   druggability assumptions.
3. Assumptions the project repeatedly makes but has not tested.
4. Analyses a researcher from metabolism, structural biology, systems
   immunology, or neurology would run that this project has avoided.
5. The top five proposals that are concrete enough to test on existing data.

For each proposal, return:

- short name;
- why the project may have missed it;
- exact data artifact(s) to test it on;
- expected direction if true;
- falsification test;
- whether it needs new data.

## Grounding Rule For Future Session

For every proposal returned by the independent lens:

1. Add it to `meta/queues/V29_QUEUE.md`.
2. Query the local RAG index for prior runs on the same analysis.
3. Implement the proposal on real local data or mark it blocked with the exact
   missing data/tool.
4. Record outcome as `held`, `failed`, or `inconclusive` in
   `docs/history/LEAD_INVENTORY_V29.md`.
5. Do not cite model confidence or language as evidence.
