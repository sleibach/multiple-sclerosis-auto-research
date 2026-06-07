# NEXT_ACTIONS

Last updated: 2026-06-07 03:15 CEST

Start every resumed session here. Work the first unresolved item unless a higher-priority blocker has just cleared.

## Queue

V30 SAP AI Core independent-lens checkpoint:

- `SAP_AI_CORE_API_KEY` is configured in `.env` as SAP service-key JSON.
- `scripts/sap_ai_core_client.py` is the committed reusable client.
- OAuth and deployment listing work for resource group `default`.
- Gemini smoke tests pass for `gemini-3.1-flash-lite` and `gemini-2.5-pro`.
- Claude deployments are discoverable but inference is blocked by unresolved
  allowed subpath/schema.
- Mistral deployment is discoverable but corrected `/chat/completions` timed
  out.
- Gemini-only review produced proposal queue items, recorded in
  `docs/history/LEAD_INVENTORY_V30.md`, but no multi-lineage result is claimed.

First V30 continuation action:

1. Resolve Claude or Mistral SAP AI Core inference schema so at least two
   non-OpenAI lineages smoke-pass.
2. Re-run `meta/INDEPENDENT_REVIEW_QUEUE_V29.md` across working lineages.
3. Ground de-duplicated model proposals on local data before promoting any
   finding.

V31 update:

- Claude 4.7 Opus now smoke-passes through SAP AI Core Orchestration using
  `defaultOrchestrationConfig` deployment `d65236404bbfb6b2`.
- Gemini 2.5 Pro continues to smoke-pass through native Gemini endpoint.
- Claude + Gemini review completed and is documented in
  `docs/history/LEAD_INVENTORY_V31.md`.
- Mistral remains optional: discoverable but timed out.
- No lead was upgraded.

First V31 continuation action:

1. Run the raw-expression confounder panel prioritized by multi-lineage review:
   baseline APC/HLA-II, metabolic/glycolysis/OXPHOS, generic inflammatory,
   glucocorticoid, IFN-suppression, STAT1, proliferation, and cell-composition
   scores on the V22/V23 treatment-response cohorts.
2. Compare each score against the locked scalar by AUC, cohort-adjusted model,
   and residualization where possible.
3. Keep `LOCKED_RULE_V22.md` immutable; this is a confounder audit, not rule
   tuning.

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
  - `GPR25` was not present in local `GSE301908_sn_all.rds` or
    `GSE180759_expression_matrix.csv.gz`;
  - no MS lesion-cell or IFN/APC mechanism can be claimed from local data.
- Local h5ad cross-atlas result:
  - `GPR25` is absent or trace even in cell-type breakdowns; highest observed
    detection was Sjogren salivary pro-T cells at `0.9009%` (`n=111`) and
    most major T/myeloid groups were near zero;
  - `KIF21B` is materially more detectable in immune populations, including
    psoriasis helper T cells `10.17%`, psoriasis Tregs `8.79%`, psoriasis
    cytotoxic T cells `7.38%`, IBD T cells `4.09%`, and Sjogren effector CD8 T
    cells `3.55%`.
- Mechanism/prior-art result:
  - UniProt/IUPHAR support CXCL17-GPR25 as a real GPCR ligand axis;
  - ChEMBL has only two screening activity records and no mechanism records;
  - no ClinicalTrials.gov GPR25 studies were found;
  - Google Patents exact `GPR25` search returned broad target-list/platform
    hits, not a specific MS/UC GPR25 agonist program in top inspected records.
  - V17 GEO searches found no obvious public MS CITE-seq/protein dataset for
    `GPR25`, `CXCL17/GPR25`, or `KIF21B`.
  - V17 Europe PMC searches support CXCL17-GPR25 functional immune biology but
    did not identify direct public MS protein-level or perturbation data for
    resolving the chr1 causal gene.
- Current classification:
  - `GPR25`: alive Tier 1 lead, mechanism narrowed to protective
    CXCL17-GPR25 lymphocyte trafficking/residency, not intervention-grade;
    h5ad scans found it absent or nearly absent in available atlases.
  - `KIF21B`: reopened competing causal-gene candidate at the same locus and
    more consistently detectable than GPR25 in available h5ad atlases, but
    V17 scout found poor direct druggability.
  - `ZMIZ1`: locked opposite-direction MS/Crohn decoupling locus.
  - `PTGER4`: closed as not-a-clean-transfer-target unless signal-specific
    cell-type QTL data appears.
- Critique result:
  - do not upgrade GPR25 without protein-level or genotype-linked subset data;
  - do not ignore KIF21B because its expression support is stronger, even
    though direct druggability is weak;
  - preserve the distinction between shared eQTL component and distinct eQTL
    components at chr1.

V18 data-source acquisition checkpoint:

- Master plan: `meta/DATA_ACQUISITION_PLAN_V18.md`.
- Tier 2 key requests: `meta/DATA_TIER2_KEY_REQUESTS.md` (no new simple
  key-gated sources promoted).
- Tier 3 instructions: `meta/DATA_TIER3_DOWNLOAD_INSTRUCTIONS.md`.
- Acquired Tier 1 data under `data/raw/v18_source_triage/`:
  - OneK1K top eQTL Zenodo zip;
  - DICE mean expression plus significant immune-cell eQTL VCF panel;
  - eQTL Catalogue QTD000021 targeted chr1 extract;
  - IUPHAR and GPCRdb GPR25 JSON.
- Smoke-test summary:
  - OneK1K top-eQTL summaries found `14` target hits, all `KIF21B`;
  - DICE significant eQTL panel found `1` target hit, `KIF21B` in NK cells;
  - DICE mean expression shows `KIF21B` high across immune subsets, `GPR25`
    low but nonzero in selected T/NK subsets;
  - eQTL Catalogue QTD000021 chr1 target extract returned `8,416` target rows,
    all `KIF21B`;
  - fast overlap check found the OneK1K/DICE top/significant KIF21B hits do
    not exactly match the V17 shared credible-set variants; closest OneK1K hits
    were `17,230 bp` and `21,012 bp` away;
- no acquired public Tier 1 source resolves GPR25 at protein/CITE-seq level.

V19 chr1 first-principles re-evaluation checkpoint:

- Report: `docs/workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md`.
- Reproducible script: `scripts/v19_chr1_reanalysis.py`.
- V18 acquired-source checksums reverified: `19 / 19` matched.
- Dense eQTL Catalogue QTD000021 KIF21B coloc:
  - MS vs KIF21B eQTL PP.H4 `0.874879034973956` over `472` aligned SNPs;
  - UC vs KIF21B eQTL PP.H4 `0.868660082128031` over `472` aligned SNPs.
- Exact shared credible-set direction in QTD000021:
  - MS risk allele lowers KIF21B expression `11 / 11`;
  - UC risk allele lowers KIF21B expression `11 / 11`.
- First-principles druggability revision:
  - `GPR25`: structurally plausible GPCR, but agonism/restoration is required
    and chemical matter is immature.
  - `KIF21B`: structurally ligandable motor-domain protein, but simple
    inhibition/degradation is likely wrong-direction because risk lowers
    expression; restoration/up-function is the difficult modality.
- Integrated verdict: chr1 is a real genetics/mechanism lead, not an
  intervention-grade target.

V20 next-tier slate checkpoint:

- Report: `docs/history/LEAD_SLATE_V20.md`.
- Reproducible script: `scripts/v20_generate_lead_slate.py`.
- Output table: `analysis/v20_lead_slate/lead_slate_v20.tsv`.
- Slate size: `13` candidates.
- Verdict counts:
  - promising follow-up: `5`;
  - hard-target real biology: `2`;
  - negative/not-now: `6`.
- Top actionable lead:
  - dynamic APC/HLA-II treatment-response monitoring in MS; treat as
    biomarker/mechanism transfer, not direct target or drug repositioning.
- Next genetics regions:
  - MS-Crohn chr14 `14:68710199-69753364` (`ZFP36L1` neighborhood);
  - MS-UC chr2 `2:60689469-61742410` (`REL/PUS10/USP34` neighborhood).
- Guardrails:
  - `ZMIZ1` remains a locked opposite-direction decoupling finding, not a
    transfer target.
  - `PTGER4`, chr17 `STAT3/STAT5`, generic `TYK2`, and MHC overlap logic are
    not current leads without new signal-specific data.

V21 genetic-correlation and next-tier-locus checkpoint:

- Reports:
  - `docs/workups/genetics/GENETIC_CORRELATION_BACKDROP_V21.md`.
  - `docs/history/LEAD_SLATE_V21.md`.
- Reproducible scripts:
  - `scripts/v21_ldsc_core_backdrop.py`.
  - `scripts/v21_next_tier_locus_susie.py`.
- LDSC rg results:
  - MS-UC `rg = 0.3342`, `SE = 0.0444`, `p = 4.8771e-14`.
  - MS-SLE `rg = 0.2439`, `SE = 0.0608`, `p = 6.0712e-05`, caveated by high
    SLE h2 intercept `1.1998`.
  - MS-RA `rg = 0.1692`, `SE = 0.0453`, `p = 0.0002`.
  - MS-Crohn `rg = 0.1675`, `SE = 0.0527`, `p = 0.0015`.
- MHC sensitivity note:
  - raw MHC-excluded sumstats were built for MS/UC/Crohn;
  - after LDSC reference merge, estimates were identical because the verified
    reference panel has zero chr6:25-34 Mb SNPs in the active regression set.
- Queued V20 genetics regions:
  - MS-Crohn chr14 `14:68710199-69753364` (`ZFP36L1`) produced bounded
    SuSiE max PP.H4 `0.687732800443124`; parked as suggestive, not robust.
  - MS-UC chr2 `2:60689469-61742410` (`REL/PUS10/USP34`) returned no
    `coloc.susie` credible-set summary; closed/not-now.
- Neither V21 locus clears the chr1 bar.

V22 locked treatment-response checkpoint:

- `docs/locked_rules/LOCKED_RULE_V22.md` was committed before validation in commit `013639b`.
- Primary locked validation:
  - `GSE235357` MS dimethyl fumarate: pass, AUC `0.72`, Hedges g `0.651`,
    `n=10`, wide CI.
  - `GSE250453` MS fingolimod: fail, AUC `0.60`, Hedges g `0.150`, `n=10`.
  - `GSE85034_ADA` psoriasis adalimumab: fail, AUC `0.511`, Hedges g
    `0.044`, `n=14`.
- Exploratory support:
  - `GSE253006_TOF` UC tofacitinib: numerical pass, AUC `1.00`, Hedges g
    `1.522`, `n=9`, but not counted as primary validation because the module
    is an approximation and compartment is unresolved.
- Verdict:
  - no breakthrough;
  - no kill;
  - the dynamic APC/HLA-II rule remains a provisional early-treatment
    monitoring lead.

V23 APC/HLA-II monitoring workup:

- Report: `docs/workups/treatment_response/APC_HLA_MONITORING_WORKUP_V23.md`.
- Queue/log: `meta/queues/V23_ACTION_QUEUE.md`.
- Unbounded primary locked pooled AUC: `0.547`, CI `0.337-0.743`.
- Exact raw-10x `GSE253006_TOF` rescoring: pass, AUC `0.95`, CI `0.70-1.00`,
  Hedges g `1.811`.
- Bounded DMF plus exact tofacitinib set: AUC `0.811`, CI `0.567-1.000`,
  Hedges g `1.191`.
- Exact GSE253006 compartment result: strongest specific compartments are
  `t_cell_like` and `b_plasma_like`, not exclusively myeloid/APC; interpret as
  broader cytokine/JAK-STAT immune remodeling.
- No `LOCKED_RULE_V23.md` exists. Do not create one until a fresh held-out
  cohort is acquired.

V26 deep-structure checkpoint:

- Report: `docs/findings/DEEP_STRUCTURE_V26.md`.
- Queue: `meta/queues/V26_QUEUE.md`.
- Reproducible script: `scripts/v26_deep_structure_analysis.py`.
- Output directory: `analysis/v26_deep_structure/`.
- Modality manifest: `analysis/v26_deep_structure/modality_manifest_v26.tsv`.
- Workstream A result:
  - supported treatment pharmacodynamic vs h5ad cell-state latent axis,
    cosine `0.933576`, permutation p `0.001000`, BH q `0.009995`;
  - supported h5ad cell-state vs cross-disease summary latent axis, cosine
    `0.879242`, permutation p `0.003498`, BH q `0.017491`;
  - perturbation and response-outcome matrices did not pass the shared latent
    axis gate against other modalities.
- Workstream B result:
  - `25` supported replicated module-dependency rows;
  - strongest recurring dependency is `hla_ii_apc` with
    `mif_cd74_receptor_state` across four modalities;
  - APC/HLA-II monitoring is strengthened mechanistically as coupled early
    immune remodeling, not as a baseline stratifier.
- Workstream C result:
  - zero load-bearing invariants passed BH correction;
  - do not claim invariant immune constraints from V26.
- Stalled lead reread:
  - chr1/KIF21B remains causal-favored, hard target, wrong-direction for
    tractable inhibition;
  - GPR25 remains unsupported by held module/QTL data;
  - ZMIZ1 remains a locked opposite-direction decoupling;
  - PTGER4 remains closed.

V27 coupled-axis rule checkpoint:

- Reports:
  - `docs/workups/treatment_response/COUPLED_AXIS_V27.md`.
  - `docs/validation/VALIDATION_READINESS_V27.md`.
  - `meta/queues/V27_QUEUE.md`.
- Reproducible scripts:
  - `scripts/v27_coupled_axis_comparison.py`.
  - `scripts/v27_apply_locked_rules.py`.
- Output directory: `analysis/v27_coupled_axis/`.
- No fresh Gafson/NEDA cohort was found on disk or read during rule work.
- V27 used `delta_RECEPTOR` (`CD74`, `CD44`, `CXCR4`) as the only available
  MIF/CD74 receptor-state proxy in V22/V23 paired-score tables.
- Frozen coupled candidates tested:
  - `coupled_projection`;
  - `coupled_v22_augmented`;
  - `coupling_coordination`.
- Bounded domain result:
  - V22 scalar AUC `0.811111`, Hedges g `1.190835`;
  - best coupled feature `coupling_coordination` AUC `0.733333`, Hedges g
    `0.776968`;
  - coupled-minus-scalar AUC delta `-0.077778`;
  - max-candidate label-permutation p for coupled advantage `0.912817`.
- All-primary-plus-exact result:
  - V22 scalar AUC `0.655702`;
  - best coupled feature `coupling_coordination` AUC `0.638158`;
  - max-candidate label-permutation p for coupled advantage `0.856829`.
- Verdict:
  - no `LOCKED_RULE_V27.md` was written;
  - V26 coupling remains mechanistic context;
  - the immutable V22 scalar remains the primary frozen rule for future
    validation.

V28 heterogeneous-toolchain robustness checkpoint:

- Reports:
  - `docs/workups/treatment_response/ROBUSTNESS_MAP_V28.md`.
  - `meta/TOOLING_INVENTORY_V28.md`.
  - `meta/TOOL_KEY_REQUESTS_V28.md`.
  - `meta/queues/V28_QUEUE.md`.
- Reproducible script:
  - `scripts/v28_heterogeneous_response_analysis.py`.
- Output directory: `analysis/v28_heterogeneous_response/`.
- Tooling result:
  - `.venv_v3_py312` provides the usable heterogeneous local analysis stack
    (`scipy`, `sklearn`, `statsmodels`, `torch`, `scanpy`, `networkx`,
    `igraph`);
  - no external LLM key is configured; `OPENAI_API_KEY` is requested only as an
    optional proposal/critique lens.
- Bounded V22 scalar robustness:
  - AUC `0.811111`, Hedges g `1.190835`, permutation p `0.007996`;
  - cohort-adjusted locked-score coefficient `0.321803`, robust p
    `5.7045e-07`;
  - Bayesian-bootstrap P(responder mean > nonresponder mean) `0.999`;
  - jackknife bounded AUC range `0.7875-0.8875`.
- V28 verdict:
  - bounded scalar is statistically tool-robust across independent statistical
    lenses;
  - flexible multifeature ML, receptor-only, V27 coupled features, and generic
    dynamic-vector features do not improve it;
  - validate the immutable scalar rather than adding complexity.

V29 independent-lens and dormant-lead checkpoint:

- Reports:
  - `docs/history/LEAD_INVENTORY_V29.md`.
  - `meta/INDEPENDENT_REVIEW_QUEUE_V29.md`.
  - `meta/queues/V29_QUEUE.md`.
- Cross-lineage key status:
  - `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, and `GEMINI_API_KEY` absent after
    explicit `.env` load.
  - independent model review not run; queued for immediate use when a key is
    provided.
- Dormant-lead result:
  - no dormant lead became intervention-grade;
  - postpartum HLA-II/CD64 APC-axis split is the best reactivated biology lead;
  - MIF/CD74 is partially reactivated as coupled APC context, not as a
    standalone target/predictor;
  - ZMIZ1 remains a transfer-validity decoupling finding;
  - NAMPT, PTGER4, ZFP36L1, REL/PUS10/USP34, and generic TYK2 remain parked or
    closed.
- Cross-domain reframing:
  - NAMPT/HIF/glycolysis should be used as a metabolic-stress covariate in
    future APC/HLA-II monitoring validation, not as a revived target;
  - systems/dynamics reframing supports the simple V22 scalar over generic
    trajectory geometry;
  - structural reframing keeps FPR2/ALX as a wet-lab comparator, not a current
    computational MS target.

Next session first action:

1. Run `.venv/bin/python scripts/check_opengwas_access.py`.
2. Read `docs/history/LEAD_INVENTORY_V29.md`, `meta/INDEPENDENT_REVIEW_QUEUE_V29.md`,
   `docs/workups/treatment_response/ROBUSTNESS_MAP_V28.md`, `docs/workups/treatment_response/COUPLED_AXIS_V27.md`, `docs/validation/VALIDATION_READINESS_V27.md`,
   `docs/findings/DEEP_STRUCTURE_V26.md`, `docs/workups/treatment_response/MODEL_CARD_V25.md`, `docs/workups/microbiome/DATA_SCOUT_V24.md`,
   `analysis/v24_data_scout/v24_candidate_inventory.tsv`,
   `docs/workups/treatment_response/APC_HLA_MONITORING_WORKUP_V23.md`, and `docs/locked_rules/LOCKED_RULE_V22.md`.
3. Do not use the V25 model for wet-lab triage; held-out validation failed to
   support a deployable simulator. Do not tune `docs/locked_rules/LOCKED_RULE_V22.md`. Treat V26
   as structural support for coupled APC/HLA-II/MIF-CD74 monitoring only, not a
   validated clinical rule or target. V27 showed the coupled representation did
   not outperform the V22 scalar, and V28 showed heterogeneous local methods
   support the scalar but not added model complexity.
4. If `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, or `GEMINI_API_KEY` is provided,
   verify it and run the queued independent review package in
   `meta/INDEPENDENT_REVIEW_QUEUE_V29.md`; ground every proposal before using
   it.
5. Primary next action is human/low-barrier
   acquisition of Gafson et al. 2018 DMF PBMC RNA-seq processed counts plus
   sample-level NEDA-4 responder labels (PMID `30283812`, DOI
   `10.1212/nxi.0000000000000470`).
6. Secondary acquisition: request response-label mapping for
   `GSE130478/GSE130491/GSE130494` from the GEO contact so the open DMF
   expression/methylation data become analyzable.
7. Optional computational stress test, only if the medical team accepts the
   caveat: apply the unchanged V22 rule to the unused `GSE85034_MTX` arm
   (psoriasis methotrexate, same-study context, paired baseline/week16,
   PASI75 labels).
8. Extend LDSC rg to remaining map diseases once the best OpenGWAS IDs are
   selected and verified: psoriasis, T1D, Sjogren's, celiac disease,
   autoimmune thyroid disease, and myasthenia gravis.
9. Keep chr1 (`KIF21B`/`GPR25`) in wet-lab/controlled-data handoff status; do
   not continue it computationally unless new genotype-linked protein/CSF data
   arrives.
10. Preserve `ZMIZ1` as a decoupling finding; do not re-litigate unless formal
   QTL coloc is needed for publication-grade writeup.
11. Do not spend more time on V21 chr14 `ZFP36L1`, V21 chr2
   `REL/PUS10/USP34`, `PTGER4`, chr17 `STAT3/STAT5`, generic `TYK2`, or MHC
   overlap as current leads without new fine-mapped or signal-specific data.
