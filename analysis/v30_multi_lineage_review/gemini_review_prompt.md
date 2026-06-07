You are an adversarial reviewer from outside the project's usual genetics/transcriptomics framing. Your output is not evidence; it is a proposal queue for grounding. Return JSON with two arrays: proposals and vulnerabilities. Each proposal has short_name, why_missed, data_artifacts, expected_direction, falsification_test, needs_new_data. Each vulnerability has claim, weakness, concrete_test. Prioritize items testable on existing local data.


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
- `KIF21B` now has independent dense QTD000021 colo


## meta/NEXT_ACTIONS.md
# NEXT_ACTIONS

Last updated: 2026-06-07 01:35 CEST

Start every resumed session here. Work the first unresolved item unless a higher-priority blocker has just cleared.

## Queue

No unresolved supported V12 cells remain. V14 has added a first-pass locus
landscape and prior-sensitivity layer over the V13 OpenGWAS coloc results.

Current genetics robustness state:

- `meta/PROVISIONING_REPORT.md` exists.
- R `coloc` 5.2.3 and `susieR` 0.14.2 are installed and smoke-tested.
- PyPI `ldsc` 2.0.1 is installed; munge and CLI smoke tests pass.
- Standard LDSC European LD-score reference panel is provisioned from Zenodo DOI
  `10.5281/zenodo.14993076` at `data/raw/ldsc_reference/eur_w_ld_chr/`.
- `w_hm3.snplist` is present inside the extracted reference panel.
- Reference-panel smoke test passed with `munge_sumstats.py` and `ldsc.py --h2`.
- Bounded SuSiE-coloc has been run for UC chr1 and Crohn chr10 using OpenGWAS
  EUR LD matrices and top-500 shared SNP subsets:
  - UC chr1 `1:200375242-201375897`: max PP.H4 `0.959324545654259`.
  - Crohn chr10 `10:80542475-81559335`: max PP.H4 `0.958107919239886`.
- V15 causal-gene/effect-direction workup exists at
  `docs/workups/genetics/GENETICS_LOCI_WORKUP_V15.md`.
- V15 verdict:
  - UC chr1 most likely maps to `GPR25` by stored blood eQTL colocalization
    in MS and UC; direction proxies are concordant but raw allele-aligned
    eQTL summary statistics were not rerun; not intervention-grade.
  - Crohn chr10 most likely maps to `ZMIZ1` by positional plus Crohn blood
    eQTL support; MS/Crohn disease-effect signs are opposite; not
    transfer-ready or intervention-grade.
- V15 next-tier SuSiE:
  - UC chr5/PTGER4 is mixed multi-signal: `max PP.H4 = 0.998601068519585`,
    `max PP.H3 = 0.998187670954932`, 21 pairwise rows.
  - Crohn chr17/STAT3-STAT5 is downgraded: `max PP.H4 =
    0.0267570011193013`.
- V16 eQTL direction:
  - GPR25 direction revised: expression-increasing alleles are protective for
    both MS and UC; risk associates with lower GPR25 expression.
  - ZMIZ1 direction confirmed: expression-increasing alleles are MS-risk and
    Crohn-protective.
  - PTGER4 remains mixed: shared and distinct signal components point in
    different MS/UC directions.

V17 checkpoint:

- `docs/workups/genetics/GENETICS_GPR25_WORKUP_V17.md` is the current lead-consolidation report.
- `docs/critiques/CRITIQUE_V17.md` records the local hostile critique; subagent spawning was
  attempted but failed because the agent thread limit was reached.
- `docs/workups/genetics/GPR25_KIF21B_EXPERIMENTAL_DESIGN_V17.md` records the current wet-lab
  handoff design for resolving the chr1 causal-gene ambiguity.
- Full eQTLGen file was streamed and filtered for chr1 candidate genes:
  `analysis/v17_gpr25_mechanism/eqtlgen_full_extract/chr1_candidate_gene_full_rows.tsv`.
- Full-file candidate-gene result:
  - `GPR25` is strongest in the disease-shared credible-set block;
  - `DDX59` has the strongest independent eQTL peak elsewhere but does not
    coloc with the disease signal;
  - `KIF21B` remains a serious competing causal gene because bounded eQTL
    SuSiE-coloc supports shared MS/eQTL and UC/eQTL components.
- Bounded eQTL SuSiE-coloc results:
  - `GPR25`: max PP.H4 `0.969296` for MS/eQTL, `0.981623` for UC/eQTL.
  - `KIF21B`: max PP.H4 `0.956099` for MS/eQTL, `0.963951` for UC/eQTL.
  - `DDX59` and `C1orf106`: mostly distinct eQTL signal, max PP.H4 near zero.
- Local MS CNS atlas result:
  - `GPR25` was not present in loc


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

Interpretation: flexible multifeature


## docs/workups/treatment_response/APC_HLA_MONITORING_WORKUP_V23.md
# V23 Workup: APC/HLA-II Dynamic Treatment-Response Monitoring

## Executive Verdict

V23 strengthens but bounds the V22 monitoring lead.

The unbounded cross-therapy rule remains weak:

- primary locked V22 cohorts only: pooled AUC `0.547`, stratified bootstrap CI
  `0.337-0.743`; fixed/random-effects Hedges g `0.254`, CI `-0.437-0.945`.

The bounded immune-remodeling / cytokine-signaling domain is materially
stronger:

- dimethyl fumarate MS plus exact tofacitinib UC: pooled AUC `0.811`, CI
  `0.567-1.000`; pooled-subject Hedges g `1.191`, Welch p `0.0166`.
- after exact all-cell GSE253006 rescoring, primary locked plus exact UC gives
  AUC `0.656`, CI `0.489-0.808`; pooled-subject Hedges g `0.611`,
  Welch p `0.0499`.

Interpretation: the signal is not a universal treatment-response rule. It is a
provisional early-treatment monitoring signal for immune-remodeling /
cytokine-signaling contexts, with current support from small MS dimethyl
fumarate and UC tofacitinib cohorts. It fails or weakens in fingolimod/S1P
trafficking and psoriasis lesional adalimumab contexts.

No Tier 4 breakthrough is claimed: there are only two small primary
in-scope passes after exact UC cleanup, not three independent passes, and only
one MS DMT pass. No kill is claimed either.

## Action 1: Pooled Estimate

Outputs:

- `analysis/v23_apc_hla_monitoring/v23_pooled_locked_rule_summary.tsv`
- `analysis/v23_apc_hla_monitoring/v23_meta_analysis.json`

Key estimates:

| Analysis set | n | Cohorts | AUC | CI | Hedges g |
|---|---:|---|---:|---|---:|
| Primary locked V22 only | 34 | GSE235357; GSE250453; GSE85034_ADA | 0.547 | 0.337-0.743 | 0.180 |
| Primary locked plus exact UC all-cell | 43 | GSE235357; GSE250453; GSE253006_TOF_exact; GSE85034_ADA | 0.656 | 0.489-0.808 | 0.611 |
| Immune-remodeling/JAK-STAT bounded set | 19 | GSE235357; GSE253006_TOF_exact | 0.811 | 0.567-1.000 | 1.191 |

Fixed/random-effects meta-analysis of cohort-level Hedges g:

- primary locked only: g `0.254`, CI `-0.437-0.945`, I2 `0`.
- primary locked plus exact UC: fixed g `0.493`, CI `-0.142-1.129`; random g
  `0.515`, CI `-0.180-1.209`, I2 `0.152`.

## Action 2: Mechanism Specificity

Outputs:

- `analysis/v23_apc_hla_monitoring/v23_mechanism_specificity.tsv`
- `analysis/v23_apc_hla_monitoring/v23_mechanism_specificity_summary.tsv`
- `analysis/v23_apc_hla_monitoring/v23_mechanism_specificity_verdict.json`

Mechanism pattern:

- `GSE235357` dimethyl fumarate: immune redox/Nrf2 rebalancing, pass.
- `GSE253006_TOF_exact` tofacitinib: JAK-STAT cytokine signaling, pass.
- `GSE250453` fingolimod: lymphocyte trafficking/S1P, fail.
- `GSE85034_ADA` adalimumab in psoriasis lesional skin: TNF blockade in a
  non-mucosal tissue/outcome context, fail.

Verdict: mechanism-specificity is supported but small-n. The bounded domain is
plausible; the unbounded cross-therapy rule is not supported.

## Action 3: Exact GSE253006 Resolution

V22 disqualified the UC tofacitinib pass because it used a broader precomputed
IFN/APC module. V23 recomputed exact frozen V22 genes directly from raw 10x
matrices.

Output:

- `analysis/v23_apc_hla_monitoring/gse253006_exact_locked/gse253006_exact_validation_ledger.tsv`

Exact all-cell result:

- cohort: `GSE253006_TOF_exact`;
- n `9` (`5` responders, `4` nonresponders);
- feature: exact `-delta_IFN_APC`;
- AUC `0.95`, CI `0.70-1.00`;
- Hedges g `1.811`;
- Welch p `0.0162`;
- receptor control AUC `0.90`, below locked score by `0.05`;
- pass.

Caveat: all-cell pseudobulk


## docs/findings/DEEP_STRUCTURE_V26.md
# Deep Structure V26

Date: 2026-06-07

## Scope

V26 tested whether the project's held data contain a deeper module-level structure that was missed by prior single-locus and single-modality analyses. The analysis used existing summarized artifacts only; no new datasets were fetched and no OpenGWAS analysis was run beyond token verification.

The executable analysis is `scripts/v26_deep_structure_analysis.py`. Outputs are under `analysis/v26_deep_structure/`.

Fixed seed: `26026`.

Permutation count: 2,000 per null test.

## Modality Inventory

All required V26 artifacts were present. The modality manifest with checksums is:

`analysis/v26_deep_structure/modality_manifest_v26.tsv`

Usable module-level matrices:

| Matrix | Rows | Modules |
|---|---:|---:|
| perturbation Mixscale | 24 | 4 |
| treatment pharmacodynamics | 24 | 8 |
| treatment response tests | 20 | 5 |
| cross-disease h5ad cell-state comparisons | 12 | 8 |
| cross-disease module summary | 6 | 8 |

Genetics/eQTL artifacts were inventoried and retained for interpretation, but not forced into the module latent-factor test because the current held summaries do not provide a dense shared module representation for genetics/eQTL. This is a limitation, not a reason to fabricate a cross-modal axis.

## Workstream A: Cross-Modal Shared Latent Structure

Method: for each modality matrix, rows were contexts and columns were shared modules. Rows were z-scored and the first right singular vector was treated as the first module-loading axis. Pairwise cross-modality similarity used cosine similarity between module loadings. Null testing permuted module labels 2,000 times; BH correction was applied across tested modality pairs.

Supported pairings:

| Modality A | Modality B | Shared Modules | Cosine | Permutation p | BH q | Grade |
|---|---|---:|---:|---:|---:|---|
| treatment pharmacodynamic | cell-state h5ad | 8 | 0.934 | 0.0010 | 0.0100 | supported |
| cell-state h5ad | cross-disease summary | 8 | 0.879 | 0.0035 | 0.0175 | supported |

Top loadings on the supported pharmacodynamic/cell-state axis:

- Positive: `ifn_apc`, `hla_ii_apc`, `mif_cd74_receptor_state`, `mixscale_validated_ifng_readout`.
- Negative: `complement_phagocytosis`, `lipid_loader_repair`, `lysosomal_apc`.

Interpretation: the held data support a recurrent **immune-remodeling / antigen-presentation module axis** linking cross-disease cell-state differences and treatment pharmacodynamic movement. This is not a full all-modality factor: perturbation Mixscale and response-outcome tests did not pass the shared-latent-axis gate against the other modalities.

Unsupported pairings are retained in `workstream_a_latent_axes.tsv`; notably perturbation-vs-treatment and treatment-response-vs-pharmacodynamic axes did not survive the V26 null gate.

## Workstream B: Higher-Order Module Dependency Structure

Method: within each modality matrix, all module pairs were tested by Spearman correlation across contexts, with 2,000 row-permutation nulls and BH correction within modality. A dependency was called supported only if it was significant or near-significant after correction and replicated with the same sign in at least two modalities.

Supported replicated dependencies:

| Module A | Module B | Replicated Modalities | Median r | Minimum q |
|---|---|---:|---:|---:|
| `hla_ii_apc` | `mif_cd74_receptor_state` | 4 | 0.853 | 0.0015 |
| `ifn_apc` | `mixscale_validated_ifng_readout` | 3 | 0.962 | 0.0020 |
| `ifn_apc` | `lysosomal_apc` | 


## docs/history/LEAD_SLATE_V20.md
# V20 Next-Tier Lead Slate

Generated: 2026-06-06

## Scope

V20 widens beyond the resolved chr1 MS-UC locus. It does not continue the
`GPR25`/`KIF21B` workup. Its purpose is to produce a vetted slate of next-tier
MS leads across the remaining genetics, treatment-response, agreement, and
decoupling landscape.

First-action checks:

- OpenGWAS access verified after explicit `.env` load:
  `/user` HTTP `200`, token valid until `2026-06-19 12:28 UTC`; POST
  `gwasinfo` and `tophits` for `ieu-b-18` returned HTTP `200`.
- V18 immune-QTL sources checked:
  - OneK1K zip present.
  - eQTL Catalogue QTD000021 targeted chr1 extract present.
  - V18 target-gene eQTL summary present.
  - The exact prompt path `data/raw/v18_source_triage/dice/DICE_eqtl_supp_table1.xlsx`
    is absent, but DICE-derived acquisition outputs are documented in V18 and
    remain represented through the V18 smoke-test summaries.
- Subagent dispatch was attempted for the four workstreams but failed because
  the agent thread limit was reached. V20 was therefore executed as local
  independent workstreams, with the blocker preserved in `meta/SESSION_LOG.md`.

Reproducible outputs:

- `scripts/v20_generate_lead_slate.py`
- `analysis/v20_lead_slate/lead_slate_v20.tsv`
- `analysis/v20_lead_slate/lead_slate_v20_summary.json`

## Pre-Vetting Rule

Every candidate is judged on four front-loaded criteria learned from chr1:

1. Causal-gene confidence: colocalization and QTL evidence, not nearest gene.
2. Effect direction: allele-aligned when available; unresolved directions stay
   unresolved.
3. Druggability-direction match: whether the feasible modality pushes biology
   in the protective direction.
4. Recalibrated prior art: prior work is not a binary gate, but the V20
   contribution must be explicit.

No candidate in this slate is intervention-grade. The value is triage: which
leads deserve the next wet-lab or computational dollar, and which should not
consume more effort without new data.

## Ranked Slate

| Rank | Lead | Class | Score | Verdict |
|---:|---|---|---:|---|
| 1 | APC/HLA-II treatment-response architecture | Promising follow-up | 7.2 | Most actionable non-genetic lead: dynamic APC remodeling should be tested as an MS response-monitoring or subgroup biomarker, not as a baseline static IFN/APC score. |
| 2 | Dynamic IFN/APC monitoring transfer | Promising follow-up | 7.0 | Transfer the IBD dynamic response-monitoring principle to MS DMT monitoring; do not treat it as drug repositioning. |
| 3 | Postpartum HLA-II/CD64 APC-axis split | Promising follow-up | 6.6 | Natural-experiment biology lead for postpartum MS flare prediction; no direct druggable node yet. |
| 4 | ZMIZ1 chr10 MS-Crohn opposite-direction locus | Hard-target real biology | 6.4 | Locked decoupling finding; useful for transfer-validity, not for Crohn-to-MS target transfer. |
| 5 | FPR2/ALX biased pro-resolution agonism | Hard-target real biology | 5.8 | Wet-lab resolution-route comparator; requires cargo- and ligand-bias-specific perturbation before any MS claim. |
| 6 | ZFP36L1 / chr14 MS-Crohn region | Promising follow-up | 5.656 | Best next genetics-region follow-up after chr1/chr10; suggestive H4 but no allele-aligned QTL direction yet. |
| 7 | REL/PUS10/USP34 chr2 MS-UC region | Promising follow-up | 4.618 | Rational next genetics-region test; not a target until SuSiE-coloc and QTL direction resolve. |
| 8 | STAT3/STAT5 chr17 MS-Crohn region | Negative / not now | 4.552 | First-pass signal failed


## docs/history/LEAD_SLATE_V21.md
# LEAD_SLATE_V21

V21 updates the V20 next-tier slate with a genome-wide LDSC backdrop and
bounded SuSiE-coloc/QTL context for the two queued genetics regions. No new
locus clears the chr1 bar.

## Backdrop Summary

Genome-wide LDSC genetic correlation now provides the context missing from
earlier locus work:

- MS-UC: `rg = 0.3342`, `SE = 0.0444`, `p = 4.8771e-14`.
- MS-SLE: `rg = 0.2439`, `SE = 0.0608`, `p = 6.0712e-05`, caveated by high
  SLE h2 intercept `1.1998`.
- MS-RA: `rg = 0.1692`, `SE = 0.0453`, `p = 0.0002`.
- MS-Crohn: `rg = 0.1675`, `SE = 0.0527`, `p = 0.0015`.

The central V20/V21 interpretation is unchanged but better grounded: UC is the
stronger gut comparator for MS inherited risk, while Crohn still contributes
downstream mucosal and decoupling biology. RA is genetically modestly near MS
but remains divergent on blood APC treatment-response architecture.

## Lead Card: MS-Crohn chr14 `14:68710199-69753364`

Candidate region: `ZFP36L1` neighborhood.

Bounded SuSiE-coloc:

- SNPs used: `483`.
- Pairwise credible-set comparisons: `1`.
- max `PP.H4 = 0.687732800443124`.
- max `PP.H3 = 0.28112512912872`.
- Verdict: suggestive, not robust. It does not meet the high-H4 standard used
  to advance chr1 and chr10.

Immune-QTL context:

- OneK1K top-eQTL target hits for `ZFP36L1` in this region: `0`.
- DICE significant eQTL target hits: `30` for `ZFP36L1`, mostly M2 macrophage
  context.
- DICE mean expression supports broad immune expression, including activated T
  cells, monocytes, and B cells.
- No all-variant immune-QTL colocalization was run because the disease
  SuSiE-coloc did not reach robust grade and the available DICE data are
  significant-hit summaries, not full locus QTL summary statistics.

Direction and druggability:

- No allele-aligned therapeutic direction is established.
- `ZFP36L1` is an RNA-binding/post-transcriptional regulator. First-principles
  targetability is biologically plausible through RNA/protein-regulatory
  modalities but not a clean direction-matched small-molecule target from the
  current evidence.

Backdrop interpretation:

- MS-Crohn global rg is modest (`0.1675`). A robust shared chr14 locus would
  be a useful standout within a weaker global architecture, but V21 only
  supports a suggestive signal.

V21 verdict: **parked/suggestive**, not a promising next lead.

## Lead Card: MS-UC chr2 `2:60689469-61742410`

Candidate region: `REL` / `PUS10` / `USP34`.

Bounded SuSiE-coloc:

- SNPs used: `499`.
- Status: `no_cs`.
- Error: `coloc.susie returned no summary`.
- Verdict: does not survive the bounded multi-signal disease-coloc screen.

Immune-QTL context:

- OneK1K top-eQTL target hits for `REL`, `PUS10`, or `USP34` in this region:
  `0`.
- DICE significant eQTL target hits: `45` `REL`, `7` `USP34`, `5` `PUS10`.
- DICE expression strongly supports `REL` in activated CD4/CD8 T cells and B
  cells, but expression/QTL context cannot rescue a disease-coloc failure.

Direction and druggability:

- No shared disease causal signal is established, so no allele-aligned
  therapeutic direction is inferred.
- `REL`/NF-kB biology is druggable in a broad pathway sense but crowded and
  safety-limited. `PUS10` and `USP34` do not become target claims without a
  surviving shared disease signal and all-variant QTL colocalization.

Backdrop interpretation:

- MS-UC has the strongest global rg in V21 (`0.3342`). In that context, a
  moderate chr2 overlap can be part of broad shared architecture without being


## docs/workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md
# GENETICS_CHR1_REEVALUATION_V19

Date: 2026-06-06

## Scope

V19 re-evaluated the MS-UC chr1 shared locus under the domain-reviewer's
objection that prior druggability calls were too class-precedent-driven:
`GPR25` was favored partly because GPCRs are familiar drug targets, while
`KIF21B` was down-weighted partly because kinesins are difficult. V19 therefore
tested the data-favored `KIF21B` candidate directly and separated
first-principles target features from existing chemical precedent.

Reproducible entry point:

```bash
.venv/bin/python scripts/v19_chr1_reanalysis.py
```

Primary outputs:

- `analysis/v19_chr1_druggability/v18_checksum_verification.tsv`
- `analysis/v19_chr1_druggability/kif21b_qtd000021_aligned_to_ms_uc.tsv`
- `analysis/v19_chr1_druggability/kif21b_qtd_coloc_abf_summary.tsv`
- `analysis/v19_chr1_druggability/v19_chr1_reanalysis_summary.json`
- `analysis/v19_chr1_druggability/alphafold_domain_confidence.tsv`

## First-Action Checks

- OpenGWAS token: verified with `scripts/check_opengwas_access.py`.
- `/user`: HTTP 200.
- JWT valid until `2026-06-19 12:28 UTC`.
- POST `gwasinfo` and `tophits` for `ieu-b-18`: HTTP 200.
- No OpenGWAS GET-style calls were used.
- RAG query for `V19 KIF21B GPR25 first-principles druggability chr1 credible
  set eQTL colocalization V18` returned `knowledge/candidates/KIF21B.md`,
  `knowledge/candidates/GPR25.md`, `meta/NEXT_ACTIONS.md`, and
  `meta/DATA_ACQUISITION_PLAN_V18.md` as the top project-memory hits.

## V18 Input Verification

`scripts/v19_chr1_reanalysis.py` rechecked all V18-acquired source checksums.

- Files checked: `19`.
- All expected SHA-256 values matched: `true`.

V18 smoke-test result reproduced:

- Public target eQTL hits: `15`.
- Hits by gene: `KIF21B = 15`; `GPR25 = 0`; `CXCL17 = 0`.
- Hits by source: `OneK1K_top_eqtl = 14`; `DICE_significant_eqtl = 1`.
- Exact overlap with V17 shared credible-set positions: `0`.
- Minimum distance from a OneK1K/DICE top/significant hit to a V17 shared
  credible-set variant: `17,230 bp`.

Interpretation: public top/significant immune eQTL hits support `KIF21B`
context but do not by themselves prove the V17 shared causal variant acts
through `KIF21B`.

## Investigation 1: KIF21B

### Dense Immune-QTL Colocalization

V18 acquired a dense eQTL Catalogue extract:

- Source file:
  `data/raw/v18_source_triage/eqtl_catalogue/QTD000021_chr1_200000000_202000000_targets.tsv`.
- `KIF21B` rows in the extract: `8,416`.
- Rows intersecting the saved V14 MS/UC chr1 disease SNP set after allele
  alignment: `472`.

V19 ran `coloc.abf` using allele-aligned KIF21B QTD000021 betas against the
V14 disease sumstats:

| Comparison | SNPs | PP.H3 | PP.H4 |
|---|---:|---:|---:|
| MS vs QTD000021 KIF21B eQTL | 472 | 0.0658560991820944 | 0.874879034973956 |
| UC vs QTD000021 KIF21B eQTL | 472 | 0.0691528812741881 | 0.868660082128031 |

Caveats:

- This is single-causal-variant `coloc.abf`, not SuSiE-coloc.
- The eQTL Catalogue REST metadata layer remains unusable for this run:
  - `GET https://www.ebi.ac.uk/eqtl/api/studies/QTD000021` returned HTTP 404
    with body `{"message":"Study QTD000021 does not exist!"}`.
  - `GET https://www.ebi.ac.uk/eqtl/api/studies?size=100&study_accession=QTS000002`
    returned HTTP 500.
  - FTP listings confirm the files exist at
    `https://ftp.ebi.ac.uk/pub/databases/spot/eQTL/sumstats/QTS000002/QTD000021/`,
    including `QTD000021.all.tsv.gz` (`2.8G`), `.tbi` (`1.8M`),
    `QTD000021.cc.tsv.gz` (`1.0G`), and `QTD0000


## docs/workups/genetics/GENETICS_EQTL_WORKUP_V16.md
# GENETICS_EQTL_WORKUP_V16

Date: 2026-06-06

## Question

Can V16 replace V15 proxy directions with allele-aligned QTL evidence for the
three live loci: chr1/GPR25, chr10/ZMIZ1, and chr5/PTGER4?

## Data Access

### OpenGWAS

- Verified with `scripts/check_opengwas_access.py`.
- `/user` returned HTTP 200.
- Token valid until `2026-06-19 12:28 UTC`.
- No OpenGWAS GET calls were used.

### GTEx

Reachable:

- `https://gtexportal.org/api/v2/dataset/tissueSiteDetail` returned HTTP 200.
- GTEx OpenAPI spec was downloaded from `https://gtexportal.org/api/v2/openapi.json`.
- Used endpoints:
  - `/reference/gene`
  - `/dataset/variant`
  - `/association/singleTissueEqtl`

Stale/not usable:

- `https://storage.googleapis.com/gtex_analysis_v8/single_tissue_qtl_data/GTEx_Analysis_v8_eQTL.tar` returned HTTP 404.
- `https://storage.googleapis.com/gtex_analysis_v8/single_tissue_qtl_data/GTEx_Analysis_v8_eQTL_EUR.tar` returned HTTP 404.
- No `x-deny-reason`; host reachable, paths stale.

### eQTLGen

Reachable with caveat:

- `https://www.eqtlgen.org/` returned HTTP 200.
- `https://www.eqtlgen.org/cis-eqtls.html` returned HTTP 200.
- Python TLS verification failed for `download.gcc.rug.nl` because the server
  certificate is expired.
- `curl -k -I` confirmed the significant file is reachable:
  - URL:
    `https://download.gcc.rug.nl/downloads/eqtlgen/cis-eqtl/2019-12-11-cis-eQTLsFDR0.05-ProbeLevel-CohortInfoRemoved-BonferroniAdded.txt.gz`
  - HTTP 200
  - content length `322775879`
  - SHA-256 after download:
    `8d963046d7b74cf3533c3510614cdc724e7ad0e325a3d2f7cca63ad13661b4c4`
- Full file is reachable but too large for this bounded pass:
  - `cis-eQTLs_full_20180905.txt.gz`
  - content length `4590510138`

Downgrade: V16 used the significant-only eQTLGen file, not the full all-tested
summary statistics. Therefore V16 can establish allele-aligned significant QTL
direction, but not formal all-variant QTL colocalization.

## Reproducible Commands

```bash
python3 scripts/v16_gtex_eqtl_lookup.py --targeted
```

Key outputs:

- `analysis/v16_eqtl_workup/gtex_targeted_significant_eqtl_lookup.tsv`
- `analysis/v16_eqtl_workup/gtex_positive_eqtl_disease_alignment.tsv`
- `analysis/v16_eqtl_workup/eqtlgen_significant_candidate_rows_exact.tsv`
- `analysis/v16_eqtl_workup/eqtlgen_exact_candidate_alignment.tsv`

## Lead 1: chr1 MS-UC / GPR25

### Result

`GPR25` is strengthened as the leading causal-gene candidate, but the V15
therapeutic direction is revised.

GTEx whole blood:

- `rs12132349`, GTEx variant `chr1_200906114_T_A_b38`, NES `0.236641`,
  p `2.89535e-10`; ALT `A` increases GPR25 expression and is protective for
  MS and UC.
- `rs55838263`, GTEx variant `chr1_200905600_A_G_b38`, NES `0.229834`,
  p `7.93893e-10`; ALT `G` increases GPR25 expression and is protective for
  MS and UC.
- `rs7554511`, GTEx variant `chr1_200908434_C_A_b38`, NES `0.236641`,
  p `2.89535e-10`; ALT `A` increases GPR25 expression and is protective for
  MS and UC.

eQTLGen blood:

- All 11 chr1 credible-set variants had significant GPR25 eQTL rows.
- Direction was consistent: assessed allele increases GPR25 expression and is
  protective for both MS and UC.
- Representative rows:
  - `rs59655222`, assessed `C`, Z `15.8694`, p `1.0322E-56`.
  - `rs12132349`, assessed `A`, Z `15.8625`, p `1.154E-56`.
  - `rs55838263`, assessed `G`, Z `15.7242`, p `1.0357E-55`.

### Verdict

The V15 proxy direction was wrong. The allele-aligned GTEx/eQTLGen direction is:

- higher GPR25 expressi


## knowledge/candidates/NAMPT.md
# NAMPT

Status: demoted  
V4 tier: Tier 0  
Last updated: 2026-05-28

## V3 History

V3 demoted NAMPT because NAMPT biology/inhibitors are well known, systemic
inhibition has safety concerns, and local evidence did not establish a
selective autoimmune therapeutic window.

## V4 Recalibration Question

Does V4 have a contribution beyond generic NAMPT inhibition, such as
biomarker-defined transient immunometabolic reset, tissue-targeted modality, or
combination therapy?

## Current V4 Contribution

Narrowly alive only as an eNAMPT or biomarker-defined transient NAMPT-axis
branch.

Closed:
- generic systemic intracellular NAMPT catalytic inhibition;
- FK866/APO866-style NAD-depletion logic for broad MS or pan-autoimmune use;
- NAMPT as a common-variant genetically anchored pan-autoimmune target.

V4 contribution:
- separate extracellular NAMPT / inflammatory eNAMPT biology from intracellular
  NAD-depletion biology;
- test whether NAMPT-high inflammatory myeloid/metabolic states define a
  treatment-resistance or remission-reversal subgroup;
- require a non-NAD-depleting or tightly time/tissue-bounded modality before
  promotion beyond Tier 0.

## V4 Recalibration Verdict

Verdict 2: demotion was partly prior-art-driven, but a constrained V4
contribution exists.

Prior-art grade: P1 high crowding for generic NAMPT/NAD intervention. It is not
P0 target-invalidating because no local evidence showed an equivalent autoimmune
clinical failure with adequate NAMPT target engagement. The live branch is not
generic NAMPT inhibition; it is eNAMPT/subgroup/transient-modulation biology.

## Evidence Ledger

- `docs/history/EXHAUSTION.md`: NAMPT was the top computational successor after ACSL1, with
  MS foamy proteome/snRNA convergence, recurrence in RA/psoriasis/IBD/SLE,
  ChEMBL tractability, and AlphaFold pLDDT 94.25; rejected for prior art,
  direction ambiguity, and systemic safety.
- `phases/v3/results/cross_disease_gene_summary.tsv`: NAMPT tested in 7 diseases;
  supportive/trend signal only in Crohn and UC; no strong disease count.
- `phases/v3/results/broad_residual_gate/broad_residual_gate_summary.tsv`: NAMPT
  residual support retained only in IBD; `non_ibd_retained_positive_disease_count
  = 0`, `strict_core_covariate_surviving_disease_count = 0`, MS white-matter
  delta -0.214, p 0.543.
- `phases/v3/results/wave20_genetic_druggable_altaxis/local_opentargets_genetics_summary.tsv`:
  NAMPT OpenTargets score 0.0, no disease genetics support.
- `phases/v3/results/wave96_c15orf48_controller_search/pre_donor_controller_rank.tsv`:
  NAMPT had positive contexts in Crohn myeloid, UC myeloid, and T1D acinar
  cell, but failed MS anchor, genetics, perturbation, foundation, and modality
  gates.
- `phases/v3/results/wave126_l1000_upstream_regulator_reopener/l1000_upstream_regulator_decisions.tsv`:
  withaferin-A/NAMPT did not reopen because the compound signal was high-risk
  cytotoxic/steroid/stress biology.
- `phases/v3/subagents/genetics_james_report.md`: NAMPT weak as a common-variant
  cross-autoimmune anchor; genetics favored HLA-II/IFI30/IRF1 instead.
- `phases/v3/subagents/wave19_hostile_critique.md`: local prior art cites FK866/NAMPT
  inhibition reducing EAE disability via NAD depletion (PMID 19936064) and
  protective NAD biology (PMID 25290058), supporting direction ambiguity.

## Next Tier 0 Test

Run an eNAMPT-vs-iNAMPT separation screen.

Question:
- Is the NAMPT signal in MS lesion, CSF extracellular vesicle/protein, or
  disease-rele


## knowledge/candidates/MIF_CD74_STRATIFICATION.md
# MIF / CD74 Stratification

Status: demoted  
V5 tier: Tier 1 failed  
Last updated: 2026-05-28

## Rationale

V3 repeatedly surfaced MIF/CD74 receptor-state biology, including L1000 module
reversal contexts, but did not mature it as a stratification program.

## V4 Contribution Hypothesis

MS or cross-autoimmune patients with persistent MIF/CD74 APC-state activation
may define a treatment-resistance subgroup rather than a universal target.

## Next Tier 0 Test

Search treatment-resistance and failed-trial post-hoc dimensions for MIF/CD74
state enrichment.

## V4 Tier 0 Audit

Audit completed: `analysis/tier_0_triage/mif_cd74_stratification/decision.json`.

Call: `PARK_TIER0_COMPONENT_AND_TREATMENT_INTERACTION_REQUIRED`.

Result:
- MS white-matter microglia retain nominal IFN-residual support:
  residual delta `0.45572407980566854`, Hedges g `1.247930189567055`,
  p `0.007887505384977308`, residual FDR `0.4417003015587293`.
- Sjogren epithelial residual support is weak: p `0.07344896860686509`,
  residual FDR `0.97363654262921`, and target-vs-IFN R2 `0.9015149582126574`.
- No `mif_cd74_receptor_state` residual test survives FDR `<=0.10`.
- The available local IBD remission interaction table does not test
  `mif_cd74_receptor_state`.

Interpretation: under the V4 prior-art rule, MIF/CD74 is not killed merely
because ibudilast and CD74/MIF prior art exist. The surviving contribution is
narrow: a treatment-by-biomarker or lesion/CSF enrichment test for a
`CD74/CD44/CXCR4/HLA-II` receptor state. The local evidence does not yet
support Tier 1 promotion.

Next valid test: component-resolved residualization (`CD74` alone,
`CD74/CD44/CXCR4`, HLA-II-only, and full module) plus treatment-response or
failed-trial interaction. Do not rerun raw CD74/HLA expression screens.

## GSE282122 Anti-TNF Remission Interaction

Audit completed:
`analysis/tier_0_triage/mif_cd74_stratification/gse282122_remission_interaction/REPORT.md`.

Result:
- Major monocyte/macrophage remission is associated with increased
  post-treatment `mif_cd74_receptor_state`, not decreased: adjusted delta
  `0.4840720173619233`, adjusted p `0.03473492719224309`.
- Lower baseline monocyte/macrophage `mif_cd74_receptor_state` predicts
  remission in one adjusted logit model: coefficient `-4.088480806349443`,
  p `0.009857151903175113`, but raw baseline difference is not significant
  (Hedges g `-0.38734765558900636`, p `0.22965575235386465`).

Interpretation: the treatment-response evidence is conflicted and does not
promote the branch. It remains parked pending component-resolved testing or a
progressive-MS/SPRINT-MS-like treatment-by-biomarker dataset.

## V5 Promotion To Tier 1

V5 instruction ended the repeated parked-state loop. MIF/CD74 was promoted to
Tier 1 for a decisive mechanism test because it has recurred across V3, V4, and
V5 from independent routes.

Sidecar reports:
- `subagents/20260528_202839_mif_cd74_tier1_mechanism.md`
- `subagents/20260528_202906_mif_cd74_orthogonal_evidence.md`

Tier 1 working hypothesis:
MIF/CD74 is viable only as an MS-prioritized stratification mechanism, not as a
pan-autoimmune universal target. The candidate must show a component separable
from generic IFN/HLA-II/APC state and must eventually connect to a treatment or
clinical phenotype.

## V5 MS Component-Resolved Pseudobulk Test

Analysis completed:
`analysis/tier_1_mechanism/mif_cd74_component_ms_pseudobulk/REPORT.md`.

Scope guardrail:
- The local MS pseudobulk table contains `CD74` an


## meta/MATRIX_STATUS.md
# MATRIX_STATUS

Last updated: 2026-06-06 02:51 CEST

Canonical machine-readable state: `analysis/v11_matrix/disagreement_matrix.tsv`.

## Summary

- Total qualifying supported disagreement cells: `10`.
- Non-unresolved cells: `10`.
- Completion: `100.0%`.
- `unresolved`: `0`.
- `biological`: `4`.
- `artifact`: `2`.
- `explained`: `0`.
- `intervention_derived`: `4`.

## Cells

### 005_rheumatoid_arthritis_axis_08_tissue_repair_resolution_vs_axis_09_sex_hormonal_pregnancy

- Disease: `rheumatoid arthritis`.
- Axis A: `tissue repair and resolution biology` = `far/supported`.
- Axis B: `sex, hormonal, and pregnancy modulation` = `near/supported`.
- Rank score: `3.75`.
- Status: `artifact`.
- Resolution grade: `V11 axis-scope correction`.
- Last action: V11 audit found the RA axis-08 far placement is supported mainly by blood anti-TNF response-monitoring failures, while synovial tissue repair remains under-tested. The pregnancy contrast remains valid only against blood response-monitoring, not global RA tissue repair.
- Next action: Rebuild RA tissue-repair axis with paired synovial tissue or validated synovial repair endpoints. See docs/findings/RA_TISSUE_REPAIR_PREGNANCY_SCOPE_AUDIT_V11.md.

### 010_ulcerative_colitis_axis_07_treatment_response_vs_axis_08_tissue_repair_resolution

- Disease: `ulcerative colitis`.
- Axis A: `treatment-response architecture` = `contradictory/supported`.
- Axis B: `tissue repair and resolution biology` = `near/supported`.
- Rank score: `0.78125`.
- Status: `artifact`.
- Resolution grade: `downgraded axis-design issue`.
- Last action: V10 hostile critique found high evidence overlap between treatment-response and tissue-repair axes; row downgraded by independence penalty.
- Next action: Rebuild tissue-repair axis with independent repair endpoints.

### 002_Sjogren_syndrome_axis_01_ifn_apc_vs_axis_04_lipid_lysosomal

- Disease: `Sjogren syndrome`.
- Axis A: `IFN/APC antigen-presentation state` = `near/supported`.
- Axis B: `lipid-lysosomal / foamy myeloid state` = `far/supported`.
- Rank score: `3.75`.
- Status: `biological`.
- Resolution grade: `Tier 1 candidate`.
- Last action: V10 matched salivary epithelial/APC audit plus GSE23117 bulk replication; sharpened to IFN/APC-positive versus lysosomal/APC-null, lipid-loader-negative component remains weaker.
- Next action: Find independent salivary single-cell/spatial APC replication for lipid-loader/foamy-myeloid component.

### 003_rheumatoid_arthritis_axis_01_ifn_apc_vs_axis_09_sex_hormonal_pregnancy

- Disease: `rheumatoid arthritis`.
- Axis A: `IFN/APC antigen-presentation state` = `far/supported`.
- Axis B: `sex, hormonal, and pregnancy modulation` = `near/supported`.
- Rank score: `3.75`.
- Status: `biological`.
- Resolution grade: `Tier 1 perturbation-class candidate`.
- Last action: V10 RA audit: blood IFN/APC negative/null while seropositive RA pregnancy shows late-pregnancy trough and postpartum rebound.
- Next action: Seek composition-adjusted RA/MS pregnancy data with monocyte/APC resolution.

### 004_rheumatoid_arthritis_axis_07_treatment_response_vs_axis_09_sex_hormonal_pregnancy

- Disease: `rheumatoid arthritis`.
- Axis A: `treatment-response architecture` = `far/supported`.
- Axis B: `sex, hormonal, and pregnancy modulation` = `near/supported`.
- Rank score: `3.75`.
- Status: `biological`.
- Resolution grade: `Tier 1 perturbation-class candidate`.
- Last action: V10 RA audit: RA anti-TNF blood APC response rules fail, but pregnancy immune-kineti
