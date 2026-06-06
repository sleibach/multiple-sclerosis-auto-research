# NEXT_ACTIONS

Last updated: 2026-06-06 14:32 CEST

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
  `GENETICS_LOCI_WORKUP_V15.md`.
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

- `GENETICS_GPR25_WORKUP_V17.md` is the current lead-consolidation report.
- `CRITIQUE_V17.md` records the local hostile critique; subagent spawning was
  attempted but failed because the agent thread limit was reached.
- `GPR25_KIF21B_EXPERIMENTAL_DESIGN_V17.md` records the current wet-lab
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

- Report: `GENETICS_CHR1_REEVALUATION_V19.md`.
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

- Report: `LEAD_SLATE_V20.md`.
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
  - `GENETIC_CORRELATION_BACKDROP_V21.md`.
  - `LEAD_SLATE_V21.md`.
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

- `LOCKED_RULE_V22.md` was committed before validation in commit `013639b`.
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

- Report: `APC_HLA_MONITORING_WORKUP_V23.md`.
- Queue/log: `V23_ACTION_QUEUE.md`.
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

Next session first action:

1. Run `.venv/bin/python scripts/check_opengwas_access.py`.
2. Read `LOCKED_RULE_V22.md`, `VALIDATION_LEDGER_V22.md`,
   `FINDING_V22.md`, and `COHORT_SEARCH_V22.md`.
3. Do not tune `LOCKED_RULE_V22.md`. The next useful action is acquisition of
   a larger paired MS DMT response cohort (`n >= 30`) in an
   immune-remodeling/JAK-STAT-like therapy context. Only after that should a
   bounded successor rule be locked and tested.
4. Extend LDSC rg to remaining map diseases once the best OpenGWAS IDs are
   selected and verified: psoriasis, T1D, Sjogren's, celiac disease,
   autoimmune thyroid disease, and myasthenia gravis.
5. Keep chr1 (`KIF21B`/`GPR25`) in wet-lab/controlled-data handoff status; do
   not continue it computationally unless new genotype-linked protein/CSF data
   arrives.
6. Preserve `ZMIZ1` as a decoupling finding; do not re-litigate unless formal
   QTL coloc is needed for publication-grade writeup.
7. Do not spend more time on V21 chr14 `ZFP36L1`, V21 chr2
   `REL/PUS10/USP34`, `PTGER4`, chr17 `STAT3/STAT5`, generic `TYK2`, or MHC
   overlap as current leads without new fine-mapped or signal-specific data.
