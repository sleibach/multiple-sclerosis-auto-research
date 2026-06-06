# Current Status

Last updated: 2026-06-06 02:51 CEST

## Mission State

V12 completed the supported-cell axis-disagreement matrix that V11 made
resumable. V13-V15 are robustifying the genetics axis using the working
OpenGWAS token from `.env`.

Standing reporting rule:

- Every session must end by appending a `RUN SUMMARY` block to
  `meta/SESSION_LOG.md` and echoing the same block in the final chat message.
- The block must include active runtime, UTC start/end timestamps, frontier
  advanced, stop reason, and next action.

Methodology backbone:

- V8 lock: `ROADMAP_V8.md`, `MAP_METHODOLOGY_V8.md`, commit `9c2e548`.
- V9 lock: `ROADMAP_V9.md`, `MAP_METHODOLOGY_V9.md`, commit `df7c7de`.
- V10 roadmap: `ROADMAP_V10.md`.
- V11 resume backbone:
  - `meta/MATRIX_STATUS.md`
  - `meta/NEXT_ACTIONS.md`
  - `meta/SESSION_LOG.md`
  - `analysis/v11_matrix/disagreement_matrix.tsv`
- V12 synthesis:
  - `AXIS_DISAGREEMENT_FINDINGS_V12.md`
  - `CONVERGENCE_CHECK_V12_01.md`
- V13 genetics checkpoint:
  - `GENETICS_AXIS_V13_COLOCALIZATION_CHECKPOINT.md`
  - `CONVERGENCE_CHECK_V13_01.md`
  - `analysis/v13_genetics_coloc/`
- V14 locus-landscape checkpoint:
  - `GENETICS_AXIS_V14_LANDSCAPE_CHECKPOINT.md`
  - `CONVERGENCE_CHECK_V14_01.md`
  - `analysis/v14_locus_landscape/`
- V14 genetics robustness provisioning and bounded SuSiE-coloc:
  - `meta/PROVISIONING_REPORT.md`
  - `analysis/v14_susie_coloc/REPORT.md`
  - `scripts/v14_susie_coloc_confirmed_loci.py`
- V15 causal-gene/effect-direction workup:
  - `GENETICS_LOCI_WORKUP_V15.md`
  - `analysis/v15_loci_workup/locus_verdicts.tsv`
- V15 next-tier SuSiE addendum:
  - `GENETICS_AXIS_V15_NEXT_TIER_SUSIE_ADDENDUM.md`
  - `analysis/v14_susie_coloc/susie_coloc_rollup.tsv`
- V16 eQTL-grounded workup:
  - `GENETICS_EQTL_WORKUP_V16.md`
  - `ORCHESTRATION_LOG_V16.md`
  - `subagents/v16_gpr25_eqtl_report.md`
  - `subagents/v16_zmiz1_eqtl_report.md`
  - `subagents/v16_ptger4_signal_decomposition_report.md`
- V17 GPR25 mechanism workup:
  - `GENETICS_GPR25_WORKUP_V17.md`
  - `KIF21B_SCOUT_V17.md`
  - `SOURCES_V17.md`
  - `ORCHESTRATION_LOG_V17.md`
  - `CRITIQUE_V17.md`
  - `CONVERGENCE_CHECK_V17_01.md`
  - `GPR25_KIF21B_EXPERIMENTAL_DESIGN_V17.md`
  - `analysis/v17_gpr25_mechanism/`

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

- `AXIS_DISAGREEMENT_FINDINGS_V12.md`

Resolved V12 cell reports:

- `UC_GENETICS_TREATMENT_DECOUPLING_V12.md`
- `CROHN_IFN_APC_GENETICS_DECOUPLING_V12.md`
- `CROHN_GENETICS_RESPONSE_REPAIR_DECOUPLING_V12.md`

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

1. Resolve the chr1 MS-UC causal-gene ambiguity: `GPR25` versus `KIF21B`.
   Current evidence supports both as shared disease/eQTL components, while
   single-cell expression support favors KIF21B and druggability/ligand biology
   favors GPR25.
2. Do not repeat generic GEO searches for public MS `GPR25`/`KIF21B` CITE-seq
   datasets; V17 found zero obvious hits. Look instead for controlled-access,
   consortium, CSF immune-cell, or protein-level datasets where GPR25 surface
   protein can be measured.
3. If no suitable dataset is accessible, formalize the decisive wet-lab test:
   genotype-linked GPR25/KIF21B expression in immune/CSF subsets plus
   CXCL17-directed migration/RhoA/integrin readouts. Draft exists at
   `GPR25_KIF21B_EXPERIMENTAL_DESIGN_V17.md`.
4. Preserve `ZMIZ1` as the opposite-direction MS/Crohn decoupling finding and
   do not use it for Crohn-to-MS transfer.
5. Keep `PTGER4` closed as not-a-clean-transfer-target unless signal-specific
   cell-type QTL data appears.
6. Run real LDSC genetic correlation for MS vs UC/Crohn with MHC-excluded
   sensitivity and sample-overlap/intercept reporting when needed for
   genetics-axis synthesis.

## Compute / Access Notes

- Working directory: `/Users/soeren.leibach/Projects/ms-auto-research`.
- `.venv/bin/python` works for pandas/numpy/scipy/statsmodels scripts.
- `.venv_v3_py312/bin/python` works for the local TF-IDF knowledge index.
- R `4.6.0`, `phyloseq`, `vegan`, `coloc`, and `susieR` are installed.
