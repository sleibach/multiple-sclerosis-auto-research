# Current Status

Last updated: 2026-06-07 12:20 CEST

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
V30 established SAP AI Core access for independent model review: auth,
deployment discovery, and Gemini inference work through a committed client, but
Claude and Mistral are not yet smoke-passing, so full multi-lineage review
remains blocked.
V31 resolved Claude through SAP AI Core Orchestration and completed the first
Claude-plus-Gemini independent review. It produced no lead upgrade, but it
prioritized a concrete raw-expression confounder panel for the V22/V23
treatment-response lead.
V32 completed that confounder audit on the bounded V22/V23 cohorts. The locked
scalar survived baseline APC/HLA-II, glucocorticoid/steroid-response,
proliferation, and marker-level cell-composition controls. A broad
metabolic/inflammatory/STAT1 joint adjustment attenuated but did not fully
explain away the signal, so the lead is now classified as partially
confounded / immune-tone bounded rather than a glucocorticoid or composition
artifact.

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
- V30 SAP AI Core / independent-lens review:
  - Access report: `meta/SAP_AI_CORE_ACCESS_V30.md`.
  - Reusable client: `scripts/sap_ai_core_client.py`.
  - Queue: `meta/V30_QUEUE.md`.
  - V30 inventory: `docs/history/LEAD_INVENTORY_V30.md`.
  - `SAP_AI_CORE_API_KEY` parses as service-key JSON from `.env`; OAuth2
    client-credentials exchange and deployment listing work.
  - Gemini deployments smoke-pass:
    - `gemini-3.1-flash-lite`: response `OK.`
    - `gemini-2.5-pro`: response `OK`
  - Claude deployments are discoverable and `RUNNING`, but tested subpaths
    (`/completion`, `/chat/completions`, `/messages`, `/v1/messages`, root,
    and model/invoke variants) are rejected or 404.
  - Mistral is discoverable and `RUNNING`, but corrected `/chat/completions`
    timed out.
  - Gemini-only review produced concrete queue items (steroid-pulse mimic,
    metabolic confounding, KIF21B trans/pathway checks), but none upgrades a
    lead; model output remains proposal-only.
  - Full multi-lineage triangulation remains queued until a second non-OpenAI
    lineage smoke-passes.
- V31 multi-lineage review:
  - Claude 4.7 Opus now works through SAP AI Core Orchestration:
    - orchestration deployment `d65236404bbfb6b2`
    - model deployment `def854013c7ac379`
    - smoke response `OK`
  - Gemini 2.5 Pro continues to smoke-pass through native Gemini endpoint.
  - Mistral remains optional/blocking only for a third lens: discoverable but
    timed out again on `/chat/completions`.
  - Reports/artifacts:
    - `docs/history/LEAD_INVENTORY_V31.md`
    - `meta/V31_QUEUE.md`
    - `analysis/v31_multi_lineage_review/`
  - Multi-lineage review converged on vulnerabilities around V22/V23:
    baseline-vs-dynamic confounding, small-n/pooling fragility, age/sex
    metadata adjustment, metabolic/inflammatory/STAT1 alternatives,
    proliferation/cell-composition artifacts, and V26 module-overlap risk.
  - Fast groundings:
    - cross-cohort threshold transfer is weak despite positive within-cohort
      AUCs (`GSE235357` AUC `0.72`; `GSE253006_TOF_exact` AUC `0.95`;
      threshold-transfer accuracies `0.667` and `0.600`);
    - DICE chr1 significant eQTL scan found `DDX59`-dominated credible-set
      hits, not a clean GPR25/KIF21B antagonistic model;
    - V26 modalities share module definitions, so module-overlap sensitivity
      is a real next audit.
  - No model-proposed item is evidence by itself and no lead is upgraded.
  - Next computational priority: raw-expression confounder scoring on V22/V23
    cohorts for baseline APC/HLA-II, metabolic, inflammatory,
    glucocorticoid, IFN-suppression, STAT1, proliferation, and cell-composition
    controls.
- V32 treatment-response confounder audit:
  - Report: `docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md`.
  - Script: `scripts/v32_confounder_audit.py`.
  - Outputs: `analysis/v32_confounder_audit/`.
  - Audited bounded cohorts: `GSE235357` MS DMF and exact raw-10x
    `GSE253006_TOF`, total `n = 19`.
  - Raw locked scalar AUC remained `0.811`.
  - All `23 / 23` single confounder scores survived adjustment.
  - Baseline APC/HLA-II + glucocorticoid joint adjustment survived:
    residualized AUC `0.933`, permutation p `0.0020`.
  - Cell-composition joint adjustment survived: residualized AUC `0.811`,
    permutation p `0.0130`.
  - Broad metabolic/inflammatory/STAT1 joint adjustment attenuated:
    residualized AUC `0.656`, permutation p `0.1629`; leave-one-out CV still
    improved from confounders-only AUC `0.611` to locked-plus-confounders AUC
    `0.733`.
  - Overall verdict: partially confounded / immune-tone bounded, not explained
    away by steroid/glucocorticoid or cell-composition artifacts.
  - `docs/validation/VALIDATION_READINESS_V27.md` now requires future
    validation to report V32 confounder-adjusted results alongside the
    immutable V22 primary score.
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
- `docs/history/LEAD_SLATE_V20.md` now ranks 13 next-tier candidates:
  - `5` promising follow-ups;
  - `2` hard-target real-biology findings;
  - `6` negative/not-now findings.
- V20/V21 top actionable lead: dynamic APC/HLA-II treatment-response monitoring
  in MS, now V22-tested with mixed locked validation; it remains provisional.
- V21 genetic-correlation backdrop:
  - MS-UC `rg = 0.3342`, `SE = 0.0444`, `p = 4.8771e-14`;
  - MS-SLE `rg = 0.2439`, `SE = 0.0608`, `p = 6.0712e-05`, caveated by high
    SLE h2 intercept `1.1998`;
  - MS-RA `rg = 0.1692`, `SE = 0.0453`, `p = 0.0002`;
  - MS-Crohn `rg = 0.1675`, `SE = 0.0527`, `p = 0.0015`.
- V21 next genetics regions:
  - MS-Crohn chr14 `ZFP36L1`: suggestive bounded SuSiE `PP.H4 =
    0.687732800443124`, below robust threshold; parked, not promoted.
  - MS-UC chr2 `REL/PUS10/USP34`: bounded SuSiE returned no credible-set
    summary; closed/not-now.
- No V21 locus clears the chr1 bar for a next therapeutic lead.

Standing reporting rule:

- Every session must end by appending a `RUN SUMMARY` block to
  `meta/SESSION_LOG.md` and echoing the same block in the final chat message.
- The block must include active runtime, UTC start/end timestamps, frontier
  advanced, stop reason, and next action.
- Every session must update `README.md` before ending so it remains
  synchronized with the current project status. If no README content change is
  needed, say so explicitly in `meta/SESSION_LOG.md`.

Methodology backbone:

- V8 lock: `docs/roadmaps/ROADMAP_V8.md`, `docs/locked_rules/MAP_METHODOLOGY_V8.md`, commit `9c2e548`.
- V9 lock: `docs/roadmaps/ROADMAP_V9.md`, `docs/locked_rules/MAP_METHODOLOGY_V9.md`, commit `df7c7de`.
- V10 roadmap: `docs/roadmaps/ROADMAP_V10.md`.
- V11 resume backbone:
  - `meta/MATRIX_STATUS.md`
  - `meta/NEXT_ACTIONS.md`
  - `meta/SESSION_LOG.md`
  - `analysis/v11_matrix/disagreement_matrix.tsv`
- V12 synthesis:
  - `docs/findings/AXIS_DISAGREEMENT_FINDINGS_V12.md`
  - `docs/convergence/CONVERGENCE_CHECK_V12_01.md`
- V13 genetics checkpoint:
  - `docs/workups/genetics/GENETICS_AXIS_V13_COLOCALIZATION_CHECKPOINT.md`
  - `docs/convergence/CONVERGENCE_CHECK_V13_01.md`
  - `analysis/v13_genetics_coloc/`
- V14 locus-landscape checkpoint:
  - `docs/workups/genetics/GENETICS_AXIS_V14_LANDSCAPE_CHECKPOINT.md`
  - `docs/convergence/CONVERGENCE_CHECK_V14_01.md`
  - `analysis/v14_locus_landscape/`
- V14 genetics robustness provisioning and bounded SuSiE-coloc:
  - `meta/PROVISIONING_REPORT.md`
  - `analysis/v14_susie_coloc/REPORT.md`
  - `scripts/v14_susie_coloc_confirmed_loci.py`
- V15 causal-gene/effect-direction workup:
  - `docs/workups/genetics/GENETICS_LOCI_WORKUP_V15.md`
  - `analysis/v15_loci_workup/locus_verdicts.tsv`
- V15 next-tier SuSiE addendum:
  - `docs/workups/genetics/GENETICS_AXIS_V15_NEXT_TIER_SUSIE_ADDENDUM.md`
  - `analysis/v14_susie_coloc/susie_coloc_rollup.tsv`
- V16 eQTL-grounded workup:
  - `docs/workups/genetics/GENETICS_EQTL_WORKUP_V16.md`
  - `docs/orchestration/ORCHESTRATION_LOG_V16.md`
  - `subagents/v16_gpr25_eqtl_report.md`
  - `subagents/v16_zmiz1_eqtl_report.md`
  - `subagents/v16_ptger4_signal_decomposition_report.md`
- V17 GPR25 mechanism workup:
  - `docs/workups/genetics/GENETICS_GPR25_WORKUP_V17.md`
  - `docs/workups/genetics/KIF21B_SCOUT_V17.md`
  - `docs/resources/SOURCES_V17.md`
  - `docs/orchestration/ORCHESTRATION_LOG_V17.md`
  - `docs/critiques/CRITIQUE_V17.md`
  - `docs/convergence/CONVERGENCE_CHECK_V17_01.md`
  - `docs/workups/genetics/GPR25_KIF21B_EXPERIMENTAL_DESIGN_V17.md`
  - `analysis/v17_gpr25_mechanism/`
- V18 data-source acquisition:
  - `meta/DATA_ACQUISITION_PLAN_V18.md`
  - `meta/DATA_TIER2_KEY_REQUESTS.md`
  - `meta/DATA_TIER3_DOWNLOAD_INSTRUCTIONS.md`
  - `docs/convergence/CONVERGENCE_CHECK_V18_01.md`
  - `analysis/v18_source_triage/`
  - `data/raw/v18_source_triage/`
- V19 chr1 re-evaluation:
  - `docs/workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md`
  - `scripts/v19_chr1_reanalysis.py`
  - `analysis/v19_chr1_druggability/`
- V20 next-tier slate:
  - `docs/history/LEAD_SLATE_V20.md`
  - `scripts/v20_generate_lead_slate.py`
  - `analysis/v20_lead_slate/lead_slate_v20.tsv`
  - `analysis/v20_lead_slate/lead_slate_v20_summary.json`
- V21 genetic-correlation and next-tier-locus checkpoint:
  - `docs/workups/genetics/GENETIC_CORRELATION_BACKDROP_V21.md`
  - `docs/history/LEAD_SLATE_V21.md`
  - `analysis/v21_ldsc_backdrop/`
- V22 locked treatment-response validation:
  - `docs/locked_rules/LOCKED_RULE_V22.md`
  - `docs/validation/VALIDATION_LEDGER_V22.md`
  - `docs/findings/FINDING_V22.md`
  - `docs/validation/COHORT_SEARCH_V22.md`
  - `docs/convergence/CONVERGENCE_CHECK_V22_01.md`
  - `analysis/v22_locked_apc_hla_validation/`
- V23 APC/HLA-II monitoring workup:
  - `docs/workups/treatment_response/APC_HLA_MONITORING_WORKUP_V23.md`
  - `meta/queues/V23_ACTION_QUEUE.md`
  - `docs/convergence/CONVERGENCE_CHECK_V23_01.md`
  - `analysis/v23_apc_hla_monitoring/`

## Current Matrix State

- Total qualifying supported disagreement cells: `10`.
- Resolved/classified cells: `10`.
- Completion: `100.0%`.
- Unresolved cells: `0`.

Status counts:

- `biological`: `4`.
- `artifact`: `2`.
- `intervention_derived`: `4`.

## OpenGWAS Access

OpenGWAS access works when `.env` is loaded explicitly. This shell does not
auto-load `.env`.

Verification command:

- `.venv/bin/python scripts/check_opengwas_access.py`

Verified on 2026-06-05:

- `/user`: HTTP `200`.
- POST `/gwasinfo` for `ieu-b-18`: HTTP `200`.
- POST `/tophits` for `ieu-b-18`: HTTP `200`.

Use OpenGWAS API v4 POST calls for `gwasinfo`, `tophits`, and `associations`.
Do not reuse old GET-style scripts.

## V13 Genetics Checkpoint

First-pass OpenGWAS coloc has been run for MS/UC/Crohn overlapping top-hit
regions.

High-H4 first-pass regions:

- MS-UC `1:200375242-201375897`, `PP.H4 = 0.9840`.
- MS-UC `5:39896425-40944986`, `PP.H4 = 0.9337`.
- MS-Crohn `10:80542475-81559335`, `PP.H4 = 0.9776`.
- MS-Crohn `17:40014201-41029835`, `PP.H4 = 0.9413`.

MHC windows in both UC and Crohn mostly favored `PP.H3 ~= 1`, meaning distinct
causal variants rather than simple shared causality.

Matrix grade decision:

- No genetics matrix cell is upgraded to robust yet.
- The current coloc is single-causal-variant and top-hit-window selected.
- Required next layers: genome-wide LDSC/HDL, MHC-excluded sensitivity,
  multi-signal coloc, and eQTL/pQTL causal-gene mapping.

## V14 Locus-Landscape Checkpoint

V14 added prior/effect-size sensitivity and local evidence joins over the V13
OpenGWAS coloc outputs.

Stable first-pass H4:

- UC `1:200375242-201375897`: nominal `PP.H4 = 0.9840`; minimum sensitivity
  `PP.H4 = 0.8591`.
- Crohn `10:80542475-81559335`: nominal `PP.H4 = 0.9776`; minimum sensitivity
  `PP.H4 = 0.8088`.

Nominal-H4-only:

- Crohn `17:40014201-41029835`: nominal `PP.H4 = 0.9413`; minimum sensitivity
  `PP.H4 = 0.6141`.
- UC/PTGER4 `5:39896425-40944986`: nominal `PP.H4 = 0.9337`; minimum
  sensitivity `PP.H4 = 0.5700`.

PTGER4 status:

- Alive and high priority because it is druggable and has local L2G/QTL-coloc
  support across Crohn/MS/UC.
- Not robust or intervention-grade because multi-signal coloc and therapeutic
  direction are unresolved.

Tool status:

- R `coloc` 5.2.3 and `susieR` 0.14.2 are installed and smoke-tested.
- PyPI `ldsc` 2.0.1 is installed; CLI/help and toy munge smoke tests pass.
- LDSC reference-panel provisioning is now complete from Zenodo DOI
  `10.5281/zenodo.14993076`.
- `data/raw/ldsc_reference/eur_w_ld_chr/` contains 22 `.l2.ldscore.gz` files,
  22 `.l2.M_5_50` files, and `w_hm3.snplist`.
- Reference-panel smoke test passed with `munge_sumstats.py` and
  `ldsc.py --h2` on a reference-matched toy file.
- HDL remains separate and not provisioned; LDSC genetic correlation is now
  unblocked.

Bounded SuSiE-coloc status:

- UC chr1 `1:200375242-201375897`: top-500 shared SNP subset, 485
  allele-aligned SNPs used, max `PP.H4.abf = 0.959324545654259`.
- Crohn chr10 `10:80542475-81559335`: top-500 shared SNP subset, 492
  allele-aligned SNPs used, max `PP.H4.abf = 0.958107919239886`.
- Interpretation: supports the stable first-pass H4 loci under a multi-signal
  model, but does not yet justify robust genetics-axis upgrade because
  genome-wide LDSC/HDL, full-region sensitivity, MHC controls, and causal-gene
  direction mapping remain incomplete.

## V15 Causal-Gene / Direction Checkpoint

V15 worked up the two V14 SuSiE-surviving loci through credible sets,
positional annotation, stored QTL colocalization, direction proxies,
cell-state context, druggability, and novelty checks.

- MS-UC chr1 `1:200375242-201375897`:
  - credible-set intersection: 11 variants;
  - top causal-gene candidate: `GPR25`;
  - evidence: repeated stored blood eQTL colocalization in MS and UC;
  - direction: MS and UC association signs are concordant, and stored QTL
    direction proxies suggest risk-associated higher GPR25 expression;
  - limitation: raw eQTL effect-allele alignment was not rerun, MS lesion
    cell-state support is weak, and chemical matter is immature.
- MS-Crohn chr10 `10:80542475-81559335`:
  - credible-set intersection: 4 intronic variants;
  - top causal-gene candidate: `ZMIZ1`;
  - evidence: tight positional support plus Crohn blood eQTL colocalization;
  - direction: MS and Crohn association signs are opposite, making this a
    decoupling locus rather than a straightforward transfer locus;
  - limitation: no stored MS eQTL colocalization row, weak MS cell-state
    support, and no direct ChEMBL target.

Matrix decision:

- No matrix grade upgraded in V15.
- Next decisive layer is raw allele-aligned QTL colocalization for `GPR25` and
  `ZMIZ1`, plus pQTL lookup and perturbation/cell-state validation.

V15 also extended bounded SuSiE-coloc to the queued next-tier loci:

- MS-UC chr5/PTGER4: mixed multi-signal result, `max PP.H4 =
  0.998601068519585` and `max PP.H3 = 0.998187670954932` across 21 pairwise
  signal rows. This is a signal-decomposition problem, not a clean PTGER4
  therapeutic rescue.
- MS-Crohn chr17/STAT3-STAT5: downgraded by bounded SuSiE-coloc, `max PP.H4 =
  0.0267570011193013`, `max PP.H3 = 0.604986704498299`.

## V16 eQTL Direction Checkpoint

V16 replaced key proxy directions with allele-aligned GTEx/eQTLGen evidence.

- eQTL data access:
  - GTEx API reachable and used for targeted significant eQTL lookup.
  - eQTLGen significant cis-eQTL file downloaded from `download.gcc.rug.nl`
    using `curl -k` because the host TLS certificate is expired; SHA-256
    `8d963046d7b74cf3533c3510614cdc724e7ad0e325a3d2f7cca63ad13661b4c4`.
  - Full eQTLGen all-tested file is reachable but large (`4590510138` bytes)
    and was not downloaded.
- GPR25:
  - GTEx and eQTLGen support GPR25 as the leading chr1 blood eQTL gene.
  - Direction revised: expression-increasing alleles are protective for both MS
    and UC; risk associates with lower GPR25 expression.
  - This changes the therapeutic hypothesis from antagonism/lowering to
    restoration or agonism, pending cell-state and ligand feasibility.
- ZMIZ1:
  - eQTLGen confirms all four chr10 shared credible-set variants increase
    ZMIZ1 expression and are MS-risk but Crohn-protective.
  - This is a confirmed opposite-direction decoupling locus, not a transfer
    target.
- PTGER4:
  - eQTLGen confirms PTGER4 expression effects at both shared and distinct
    signal-marker SNPs.
  - The shared and distinct components have opposing disease implications; no
    global PTGER4 agonist/antagonist conclusion is justified.

Matrix decision:

- No cure-class or intervention-grade finding.
- GPR25 is upgraded from proxy-level lead to allele-aligned eQTL-grounded lead,
  but not to therapeutic finding.
- ZMIZ1 is upgraded to an eQTL-grounded decoupling finding.
- PTGER4 remains mixed-signal and must be decomposed with full QTL coloc before
  any intervention inference.

## V17 GPR25 Mechanism Checkpoint

V17 asked whether `GPR25` could move from genetics lead to mechanistically
grounded MS intervention hypothesis.

Data gates:

- OpenGWAS access verified; token valid until `2026-06-19 12:28 UTC`.
- GTEx API reachable, but historical full eQTL archive URLs still return HTTP
  `404`; no proxy `x-deny-reason`.
- eQTLGen full cis file reachable at `download.gcc.rug.nl` by `curl -k`;
  content length `4590510138`; Python TLS verification fails because the host
  certificate is expired.
- V17 streamed the full eQTLGen file and extracted chr1 candidate-gene rows
  without storing the full 4.6 GB file locally.
- Local MS CNS atlases checked:
  - `data/raw/GSE301908_sn_all.rds`;
  - `data/raw/GSE180759_expression_matrix.csv.gz`;
  - `GPR25` was absent from both feature sets.

Main results:

- eQTLGen full-file shared credible-set block:
  - `GPR25`: 11 overlap SNPs, max abs Z `15.8694`, all
    expression-up protective for MS and UC.
  - `KIF21B`: 11 overlap SNPs, max abs Z `7.5681`, also expression-up
    protective.
  - `DDX59`: strong independent cis eQTL peak, but bounded coloc is distinct.
  - `C1orf106`: weaker and mostly distinct.
- Bounded disease-vs-eQTL SuSiE-coloc:
  - `GPR25`: max PP.H4 `0.969296` for MS/eQTL and `0.981623` for UC/eQTL.
  - `KIF21B`: max PP.H4 `0.956099` for MS/eQTL and `0.963951` for UC/eQTL.
  - `DDX59` and `C1orf106` did not retain meaningful shared PP.H4.
- Mechanism and feasibility:
  - UniProt/IUPHAR support GPR25 as a CXCL17 receptor GPCR with
    lymphocyte-homing/RhoA/integrin biology.
  - ChEMBL has only two screening activity records and no mechanism records.
  - ClinicalTrials.gov has no GPR25 studies.
  - Local MS CNS data do not support a lesion-rim or IFN/APC mechanism.

V17 verdict:

- `GPR25` remains alive as a Tier 1 genetics-to-lymphocyte-trafficking lead.
- It is not intervention-grade: no local CNS cell-state support, immature
  agonist chemistry, and `KIF21B` remains a competing causal-gene candidate.
- Additional h5ad atlas scans found `GPR25` absent or nearly absent across
  local non-CNS atlases, while `KIF21B` was more consistently detectable.
  Cell-type breakdown reinforced this: GPR25 was trace even in T-cell groups,
  while KIF21B reached `10.17%` detection in psoriasis helper T cells, `8.79%`
  in psoriasis Tregs, `7.38%` in psoriasis cytotoxic T cells, and `4.09%` in
  IBD T cells.
- CXCL17 ligand-context scan found strong salivary epithelial expression in the
  Sjogren atlas but absent/trace signal in gut, RA blood, psoriasis skin, and
  IBD myeloid atlases, so ligand-context data did not rescue a broad MS-UC
  tissue mechanism.
- `ZMIZ1` remains locked as the opposite-direction MS/Crohn decoupling locus.
- `PTGER4` is closed as not-a-clean-transfer-target unless new signal-specific
  cell-type QTL data appears.
- `KIF21B` scout: better expression support than GPR25 but poor direct
  druggability; keep for causal-gene resolution, not as a direct target.

## V12 Findings

Completed synthesis:

- `docs/findings/AXIS_DISAGREEMENT_FINDINGS_V12.md`

Resolved V12 cell reports:

- `docs/workups/genetics/UC_GENETICS_TREATMENT_DECOUPLING_V12.md`
- `docs/workups/genetics/CROHN_IFN_APC_GENETICS_DECOUPLING_V12.md`
- `docs/workups/genetics/CROHN_GENETICS_RESPONSE_REPAIR_DECOUPLING_V12.md`

Core V12 interpretation:

UC is the stronger gut-disease comparator for MS inherited risk, while both UC
and Crohn support downstream mucosal IFN/APC response-monitoring analogies.
Therefore, genetic transfer and treatment-response biomarker transfer must be
treated as different axes.

## Transfer-Validity Rule

MS-adjacent autoimmune mechanisms transfer by biological layer, not by disease
label.

- UC: best gut-disease comparator for inherited immune genetic risk, but not a
  direct baseline IFN/APC response-stratifier template.
- Crohn: weaker genetic comparator than UC, but useful for downstream mucosal
  inflammatory-state response-monitoring analogies.
- RA: useful as a pregnancy/postpartum timing comparator, not as a blood APC
  treatment-response comparator.
- Sjogren: useful for antigen-presentation comparison, not for matched
  lysosomal/APC lesion-rim or foamy-myeloid biology without stronger matched
  tissue evidence.

## Highest-Value Next Actions

1. Start from `docs/workups/treatment_response/MODEL_CARD_V25.md`, `docs/workups/treatment_response/MODEL_DESIGN_V25.md`,
   `docs/workups/microbiome/DATA_SCOUT_V24.md`, and
   `analysis/v24_data_scout/v24_candidate_inventory.tsv`.
2. Do not use the V25 model for wet-lab triage; it failed held-out validation.
3. Primary APC/HLA monitoring unlock: obtain Gafson et al. 2018 DMF PBMC
   RNA-seq processed counts plus sample-level NEDA-4 responder labels (PMID
   `30283812`, DOI `10.1212/nxi.0000000000000470`). This is the best
   identified fresh validation cohort and was not public-ready in V24.
4. Secondary acquisition: request response-label mapping for
   `GSE130478/GSE130491/GSE130494` so the public DMF expression/methylation data
   become analyzable.
5. Optional computational stress test: run the unchanged V22 rule on unused
   `GSE85034_MTX` only if same-study/cross-disease secondary evidence is useful.
6. Keep chr1 (`KIF21B`/`GPR25`) in wet-lab/controlled-data handoff status; do
   not continue it computationally unless new genotype-linked protein/CSF data
   arrives.
7. Preserve `ZMIZ1` as the opposite-direction MS/Crohn decoupling finding and
   do not use it for Crohn-to-MS transfer.
8. Extend LDSC rg to remaining map diseases when genetics-axis synthesis is
   needed.

## V24 Treatment-Response Data Scout

- Report: `docs/workups/microbiome/DATA_SCOUT_V24.md`.
- Machine-readable logs:
  - `analysis/v24_data_scout/v24_search_log.tsv`.
  - `analysis/v24_data_scout/v24_candidate_inventory.tsv`.
- Verdict: public ready-to-run data are effectively dry for primary
  APC/HLA-II monitoring validation, but low-barrier data are not dry.
- Best next cohort: Gafson et al. 2018 DMF PBMC RNA-seq, PMID `30283812`,
  DOI `10.1212/nxi.0000000000000470`; it matches MS/DMF/early 6-week
  transcriptomics with NEDA-4 responder labels, but no clean public GEO/SRA/ENA
  accession was verified. Needs author/data request for counts and metadata.
- Best open-but-incomplete MS cohort: `GSE130478/GSE130491/GSE130494`; public
  DMF longitudinal expression/methylation data, but response-label mapping is
  absent from GEO metadata.
- Verified Tier 1 secondary stress test: unused `GSE85034_MTX`, psoriasis
  methotrexate lesional-skin arm, 13 PASI75-labeled paired baseline/week16
  subjects, 9 frozen module genes represented. This is not primary MS
  validation and must be caveated as same-study/late-tissue evidence.

## V25 Immune-State Model Build

- Design: `docs/workups/treatment_response/MODEL_DESIGN_V25.md`.
- Model card: `docs/workups/treatment_response/MODEL_CARD_V25.md`.
- Immutable split:
  `analysis/v25_immune_state_model/TRAIN_HELDOUT_SPLIT_V25.tsv`, committed
  before validation in commit `0bc726e`.
- Script: `scripts/v25_build_bounded_immune_state_model.py`.
- Architecture: bounded empirical Mixscale pathway/module mean model.
- Held-out validation:
  - train perturbations: `18`;
  - held-out perturbations: `6`;
  - held-out module predictions: `24`;
  - direction accuracy: `0.542`;
  - MAE: `0.261` log2FC;
  - Pearson predicted-vs-actual: `0.531`;
  - Spearman predicted-vs-actual: `0.377`.
- Verdict: no reliable reusable immune-state simulator was achieved. The model
  can only serve as a weak descriptive prior for Mixscale-like IFNB/IFNG/TNFA
  pathway module directions and must not be used for wet-lab candidate triage.
- Required abstentions: `KIF21B/GPR25`, `ZMIZ1`, patient-level response,
  single-cell compartment effects, genetics-only hypotheses, and unseen
  pathways.

## Compute / Access Notes

- Working directory: `/Users/soeren.leibach/Projects/ms-auto-research`.
- `.venv/bin/python` works for pandas/numpy/scipy/statsmodels scripts.
- `.venv_v3_py312/bin/python` works for the local TF-IDF knowledge index.
- R `4.6.0`, `phyloseq`, `vegan`, `coloc`, and `susieR` are installed.
