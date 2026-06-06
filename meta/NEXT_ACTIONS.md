# NEXT_ACTIONS

Last updated: 2026-06-06 02:51 CEST

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

Next session first action:

1. Run `.venv/bin/python scripts/check_opengwas_access.py`.
2. Read `meta/DATA_ACQUISITION_PLAN_V18.md` and
   `analysis/v18_source_triage/target_gene_eqtl_hits.tsv`.
3. Do not treat OneK1K/DICE top-hit KIF21B evidence as causal resolution. If
   continuing computationally, verify QTD000021/eQTL Catalogue metadata and run
   formal dense variant intersection/coloc with the V17 shared credible set.
4. Do not repeat generic GEO searches for `GPR25`/`KIF21B` MS CITE-seq without
   a new source; V17 found zero obvious public hits. Instead, look for
   controlled-access, consortium, CSF immune-cell, or unpublished protein/CITE
   datasets where `GPR25` surface protein is measurable.
5. If a suitable dataset is found or manually added, test genotype-linked or disease-linked
   expression of `GPR25` and `KIF21B` in T-cell/B-cell subsets; otherwise move
   to the existing wet-lab design in
   `GPR25_KIF21B_EXPERIMENTAL_DESIGN_V17.md` for genotype-linked expression and
   CXCL17 migration/RhoA/integrin assays.
6. Preserve `ZMIZ1` as a decoupling finding; do not re-litigate unless formal
   QTL coloc is needed for publication-grade writeup.
7. Do not spend more time on `PTGER4` unless signal-specific cell-type QTL or
   perturbation data appears.
8. Run real LDSC genetic correlation for MS vs UC/Crohn with MHC-excluded
   sensitivity and sample-overlap/intercept reporting when useful for the
   genetics-axis synthesis.
9. Do not claim intervention-grade therapeutic direction until causal gene,
   cell-state expression, perturbation, and modality feasibility all cohere.
