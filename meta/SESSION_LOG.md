# SESSION_LOG

Append-only V11 resume log. Newest entries may be at the bottom.

## Standing Session-End Runtime Rule

At the end of every session, append a `RUN SUMMARY` block to this file and echo
the same block in the final chat message. This applies to all sessions,
including checkpoints, failed runs, provisioning-only sessions, and sessions
that stop because of environmental limits.

Before ending every session, update `README.md` so the repository entry point
reflects the current project phase, active frontier, and standing rules. If the
README is already current and no content edit is needed, state that explicitly
in the `RUN SUMMARY`.

Required fields:

- Active runtime: wall-clock time actually spent working this session,
  excluding usage-limit waiting time. If active runtime and total elapsed differ,
  state both. If runtime cannot be measured precisely, give the best estimate
  and label it as an estimate.
- Session start and end timestamps in UTC.
- Frontier advanced: one line naming what concretely moved, such as cells
  resolved, loci graded, tools provisioned, reports written, or blockers
  documented.
- Stop reason: `completed`, `environmental termination`, `blocker`, or
  `external`.
- Next action: the first thing the next session should do.

## 2026-06-06 10:38 CEST - README Rule Sync Session

Objective:

- Add the standing rule that `README.md` must be updated after every run.
- Bring `README.md` into sync with the current V18 project status.

Completed:

- Updated `README.md` Current Status from V17 to V18.
- Added V18 acquisition-triage status for the unresolved chr1 MS-UC
  `GPR25`-versus-`KIF21B` ambiguity.
- Added the standing README-update rule to `README.md`,
  `meta/CURRENT_STATUS.md`, and this session-log header.

RUN SUMMARY:

- Active runtime: approximately 1 minute active; total elapsed approximately
  1 minute. Runtime is an estimate because this was a short documentation
  synchronization run.
- Session start UTC: 2026-06-06 08:37:53 UTC.
- Session end UTC: 2026-06-06 08:38:47 UTC.
- Frontier advanced: standing README-update rule recorded and README
  synchronized to V18 current project status.
- Stop reason: completed.
- Next action: resume V18/V19 data-axis work by following
  `meta/NEXT_ACTIONS.md`, with README synchronization required before the next
  session ends.

## 2026-06-04 00:22 CEST - V11 Session 1

Objective:

- Initialize the V11 resume backbone and resolve at least one unresolved
  supported disagreement cell.

Completed:

- Created `scripts/v11_update_matrix_state.py`.
- Created canonical matrix state:
  - `analysis/v11_matrix/disagreement_matrix.tsv`
  - `meta/MATRIX_STATUS.md`
  - `meta/NEXT_ACTIONS.md`
- Imported the frozen V10 supported-only matrix: `10` qualifying cells.
- Pre-filled V10-resolved rows:
  - Sjogren IFN/APC versus lipid-lysosomal split.
  - RA IFN/APC versus pregnancy.
  - RA treatment response versus pregnancy.
  - UC treatment response versus tissue repair as an axis-nonindependence
    artifact.
- Resolved `001_ulcerative_colitis_axis_01_ifn_apc_vs_axis_07_treatment_response`
  as `intervention_derived`; see `docs/workups/genetics/UC_STATIC_DYNAMIC_APC_DECOUPLING_V11.md`.
- Resolved `005_rheumatoid_arthritis_axis_08_tissue_repair_resolution_vs_axis_09_sex_hormonal_pregnancy`
  as `artifact`; see `docs/findings/RA_TISSUE_REPAIR_PREGNANCY_SCOPE_AUDIT_V11.md`.
- Wrote `docs/convergence/CONVERGENCE_CHECK_V11_01.md`.

Current matrix:

- Total cells: `10`.
- Non-unresolved: `6`.
- Completion: `60.0%`.
- Unresolved: `4`.

Genetics access:

- `OPENGWAS_JWT` unavailable. Genetics execution remains blocked.

Next session first action:

- Read `meta/NEXT_ACTIONS.md`.
- Start with `006_ulcerative_colitis_axis_02_genetics_vs_axis_07_treatment_response`.
- If `OPENGWAS_JWT` remains absent, use existing supported published genetics
  evidence and document the coloc/local-rg limitation.

## 2026-06-05 14:41 CEST - V12 Session 1

Objective:

- Resolve the remaining supported disagreement matrix cells, prioritizing the
  genetics-involving cells under the V12 multi-tool triangulation standard.

Completed:

- Verified `OPENGWAS_JWT` status. It was not visible to this process, so new
  OpenGWAS/LDSC/HDL and cross-trait colocalization were not run.
- Queried the local knowledge index before starting the UC and Crohn genetics
  cells.
- Resolved `006_ulcerative_colitis_axis_02_genetics_vs_axis_07_treatment_response`
  as `intervention_derived`; see `docs/workups/genetics/UC_GENETICS_TREATMENT_DECOUPLING_V12.md`.
- Resolved `007_Crohn_disease_axis_01_ifn_apc_vs_axis_02_genetics` as
  `biological`; see `docs/workups/genetics/CROHN_IFN_APC_GENETICS_DECOUPLING_V12.md`.
- Resolved `008_Crohn_disease_axis_02_genetics_vs_axis_07_treatment_response`
  as `intervention_derived`; see
  `docs/workups/genetics/CROHN_GENETICS_RESPONSE_REPAIR_DECOUPLING_V12.md`.
- Resolved `009_Crohn_disease_axis_02_genetics_vs_axis_08_tissue_repair_resolution`
  as `intervention_derived`; see
  `docs/workups/genetics/CROHN_GENETICS_RESPONSE_REPAIR_DECOUPLING_V12.md`.
- Wrote `docs/findings/AXIS_DISAGREEMENT_FINDINGS_V12.md`.
- Wrote `docs/convergence/CONVERGENCE_CHECK_V12_01.md`.

Current matrix:

- Total cells: `10`.
- Non-unresolved: `10`.
- Completion: `100.0%`.
- Unresolved: `0`.

Genetics access:

- `OPENGWAS_JWT` unavailable to this process. Genetics cells are supported by
  multi-tool triangulation using existing project evidence and published
  genetics, not robust coloc-grade.

Next session first action:

- Read `meta/NEXT_ACTIONS.md`.
- If `OPENGWAS_JWT` is actually visible, upgrade the UC/MS and Crohn/MS
  genetics cells with executable OpenGWAS/HDL/LDSC and cross-trait coloc.
- If it remains absent, extend the matrix into lower-grade/thin-axis cells.

## 2026-06-05 16:11 CEST - V13 Session 1

Objective:

- Start the robust-grade genetics-axis upgrade now that `OPENGWAS_JWT` is
  known to work when loaded from `.env`.

Completed:

- Ran `.venv/bin/python scripts/check_opengwas_access.py`; OpenGWAS auth passed.
- Queried the local RAG index for prior genetics/coloc work before analysis.
- Created `scripts/v13_opengwas_coloc_uc_crohn.py`.
- Created `scripts/v13_annotate_coloc_regions.py`.
- Ran OpenGWAS API v4 POST `/tophits` and `/associations` calls for:
  - MS `ieu-b-18`;
  - UC `ieu-a-32`;
  - Crohn `ieu-a-30`.
- Analyzed `34` shared top-hit windows with first-pass single-causal-variant
  approximate coloc ABF.
- Annotated regions with Ensembl GRCh37 genes.
- Wrote `docs/workups/genetics/GENETICS_AXIS_V13_COLOCALIZATION_CHECKPOINT.md`.
- Wrote `docs/convergence/CONVERGENCE_CHECK_V13_01.md`.

Key outputs:

- `analysis/v13_genetics_coloc/REPORT.md`
- `analysis/v13_genetics_coloc/coloc_region_summary_annotated.tsv`
- `analysis/v13_genetics_coloc/coloc_snp_abf.tsv`

Key result:

- First-pass high-H4 regions:
  - MS-UC `1:200375242-201375897`, `PP.H4 = 0.9840`.
  - MS-UC `5:39896425-40944986`, `PP.H4 = 0.9337`.
  - MS-Crohn `10:80542475-81559335`, `PP.H4 = 0.9776`.
  - MS-Crohn `17:40014201-41029835`, `PP.H4 = 0.9413`.
- Multiple MHC windows favored distinct causal variants (`PP.H3 ~= 1`) rather
  than shared causal variants.

Decision:

- Do not upgrade matrix genetics cells yet.
- This checkpoint adds a real coloc layer, but robust grade still requires
  genome-wide LDSC/HDL, MHC-excluded sensitivity, multi-signal coloc, and
  eQTL/pQTL causal-gene mapping.

Next session first action:

- Run `.venv/bin/python scripts/check_opengwas_access.py`.
- Continue from `docs/workups/genetics/GENETICS_AXIS_V13_COLOCALIZATION_CHECKPOINT.md`.
- Prioritize LDSC/HDL scaffold or multi-signal coloc on the four high-H4
  regions and MHC H3 negative-control regions.

## 2026-06-05 16:11 CEST - V14 Session 1

Objective:

- Begin robust workup of the V13 high-H4 shared loci in landscape context, with
  PTGER4 treated as a hypothesis rather than assumed lead.

Completed:

- Verified OpenGWAS access with `scripts/check_opengwas_access.py`.
- Read `meta/MATRIX_STATUS.md` and `meta/NEXT_ACTIONS.md`.
- Queried the local knowledge index for PTGER4/STAT3/SuSiE/LDSC prior work.
- Checked local genetics tooling:
  - `ldsc.py`: missing.
  - `munge_sumstats.py`: missing.
  - R `susieR`: missing.
  - R `coloc`: missing.
- Created and ran `scripts/v14_locus_landscape.py`.
- Wrote `docs/workups/genetics/GENETICS_AXIS_V14_LANDSCAPE_CHECKPOINT.md`.
- Wrote `docs/convergence/CONVERGENCE_CHECK_V14_01.md`.

Outputs:

- `analysis/v14_locus_landscape/REPORT.md`
- `analysis/v14_locus_landscape/coloc_prior_sensitivity.tsv`
- `analysis/v14_locus_landscape/region_landscape_rollup.tsv`
- `analysis/v14_locus_landscape/shared_locus_gene_landscape.tsv`

Key result:

- Stable first-pass H4 regions:
  - UC `1:200375242-201375897`, minimum sensitivity `PP.H4 = 0.8591`.
  - Crohn `10:80542475-81559335`, minimum sensitivity `PP.H4 = 0.8088`.
- Nominal-H4-only regions:
  - Crohn `17:40014201-41029835`, minimum sensitivity `PP.H4 = 0.6141`.
  - UC/PTGER4 `5:39896425-40944986`, minimum sensitivity `PP.H4 = 0.5700`.

Decision:

- PTGER4 remains the highest-priority druggable locus, but it is not robust or
  intervention-grade.
- No matrix grade upgraded.

Next session first action:

- Provision LDSC/HDL and R `susieR`/`coloc`, then run multi-signal coloc and
  genome-wide rg/MHC sensitivity before re-grading.
## 2026-06-05 23:59 CEST - V14 genetics provisioning and bounded SuSiE-coloc

- User required tool provisioning before any genetics analysis.
- Wrote `meta/PROVISIONING_REPORT.md` before any downstream coloc or correlation.
- Installed and smoke-tested R `coloc` 5.2.3 and `susieR` 0.14.2 from CRAN mirror `https://cloud.r-project.org`.
- Evaluated pip-installable LD-score-regression alternatives:
  - `ldsc` 2.0.1 installed; CLI and toy munge smoke passed.
  - `ld-score-regression` and `ldsc-python` were unavailable on PyPI under those names.
  - Full genetic correlation remains blocked on reference LD-score panels and weights.
- Verified OpenGWAS token with `scripts/check_opengwas_access.py`; token valid until 2026-06-19 12:28 UTC.
- Added `scripts/v14_susie_coloc_confirmed_loci.py`.
- Ran bounded SuSiE-coloc using OpenGWAS EUR LD matrices for:
  - MS-UC chr1 `1:200375242-201375897`: 485 allele-aligned SNPs, max PP.H4 `0.959324545654259`.
  - MS-Crohn chr10 `10:80542475-81559335`: 492 allele-aligned SNPs, max PP.H4 `0.958107919239886`.
- Interpretation: positive multi-signal support for chr1 and chr10, but not full robust-grade upgrade because runs used top-500 SNP subsets, EUR reference LD, no LDSC/HDL, and no causal-gene/effect-direction mapping.
- Next first action: run SuSiE-coloc for UC chr5/PTGER4, Crohn chr17/STAT3-STAT5, and MHC H3 negative controls; provision LD-score reference panels before genetic correlation.

## RUN SUMMARY - 2026-06-05 22:19 UTC

- Active runtime: approximately 5 minutes; total elapsed approximately 5 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-05 22:14 UTC (estimated).
- Session end UTC: 2026-06-05 22:19 UTC.
- Frontier advanced: standing mandatory session-end runtime reporting rule written into `meta/SESSION_LOG.md` and mirrored in project status.
- Stop reason: completed.
- Next action: continue V14 from `meta/NEXT_ACTIONS.md`, starting with bounded SuSiE-coloc on UC chr5/PTGER4, Crohn chr17/STAT3-STAT5, and MHC H3 negative controls.

## RUN SUMMARY - 2026-06-05 22:29 UTC

- Active runtime: approximately 2 minutes; total elapsed approximately 2 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-05 22:27 UTC.
- Session end UTC: 2026-06-05 22:29 UTC.
- Frontier advanced: LDSC and HDL GitHub documentation read; standard LDSC `eur_w_ld_chr.tar.bz2` and `w_hm3.snplist.bz2` documented URLs tested and recorded in `meta/PROVISIONING_REPORT.md`.
- Stop reason: blocker.
- Next action: locate a currently working official/mirrored source for the standard LDSC European LD-score panel and HapMap3 SNP list, or manually provide those files under `data/raw/ldsc_reference/`, then run a reference-panel presence/smoke test before LDSC.

## RUN SUMMARY - 2026-06-05 22:39 UTC

- Active runtime: approximately 4 minutes; total elapsed approximately 4 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-05 22:35 UTC.
- Session end UTC: 2026-06-05 22:39 UTC.
- Frontier advanced: DOI-stable Zenodo source for LDSC `eur_w_ld_chr` identified, downloaded, checksummed, extracted, and smoke-tested with `munge_sumstats.py` plus `ldsc.py --h2`.
- Stop reason: completed.
- Next action: run real LDSC genetic correlation for MS vs UC/Crohn using `data/raw/ldsc_reference/eur_w_ld_chr/`, with MHC-excluded sensitivity and sample-overlap/intercept reporting.

## RUN SUMMARY - 2026-06-05 22:42 UTC

- Active runtime: approximately 1 minute; total elapsed approximately 1 minute; no usage-limit waiting time observed.
- Session start UTC: 2026-06-05 22:41 UTC.
- Session end UTC: 2026-06-05 22:42 UTC.
- Frontier advanced: `README.md` updated to reflect V14 status, LDSC Zenodo reference-panel provisioning, and the mandatory session-end reporting rule.
- Stop reason: completed.
- Next action: run real LDSC genetic correlation for MS vs UC/Crohn using `data/raw/ldsc_reference/eur_w_ld_chr/`, with MHC-excluded sensitivity and sample-overlap/intercept reporting.

## RUN SUMMARY - 2026-06-05 23:34 UTC

- Active runtime: approximately 36 minutes; total elapsed approximately 36 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-05 22:58 UTC.
- Session end UTC: 2026-06-05 23:34 UTC.
- Frontier advanced: V15 completed causal-gene/effect-direction workup for both required loci, added reproducible V15 table generation, extended bounded SuSiE-coloc to chr5/PTGER4 and chr17/STAT3-STAT5, updated resume state, README, and knowledge index.
- Locus step status: chr1 MS-UC completed steps 1-6 with `GPR25` as moderate-high-confidence causal-gene candidate but no matrix upgrade; chr10 MS-Crohn completed steps 1-6 with `ZMIZ1` as moderate-confidence causal-gene candidate, opposite MS/Crohn effect direction, and no matrix upgrade.
- Stop reason: completed V15 bounded deliverable; no therapeutic-grade claim because raw eQTL/pQTL effect-allele alignment, stronger MS cell-state support, and perturbation evidence remain missing.
- Next action: retrieve raw eQTLGen/GTEx QTL summary statistics and run allele-aligned eQTL colocalization for chr1 (`GPR25`, `C1orf106/INAVA`, `KIF21B`, `CACNA1S`) and chr10 (`ZMIZ1`, with `PPIF` as nearby negative control), then decompose the mixed chr5/PTGER4 SuSiE signal before any intervention inference.

## RUN SUMMARY - 2026-06-06 00:28 UTC

- Active runtime: approximately 31 minutes; total elapsed approximately 31 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-05 23:56 UTC.
- Session end UTC: 2026-06-06 00:28 UTC.
- Frontier advanced: V16 replaced proxy directions with allele-aligned GTEx/eQTLGen evidence for GPR25, ZMIZ1, and PTGER4; wrote `docs/workups/genetics/GENETICS_EQTL_WORKUP_V16.md`, three labeled workstream reports, updated resume state, README, manifest, and knowledge index.
- Per-lead step-completion status: GPR25 completed GTEx/eQTLGen allele-aligned direction workup and revised direction to protective higher expression; ZMIZ1 completed eQTLGen allele-aligned direction workup and confirmed opposite MS/Crohn decoupling; PTGER4 completed signal-level eQTLGen direction workup and remains mixed/conflicted.
- Novel-result verdict: no intervention-grade or cure-class finding; strongest result is an eQTL-grounded refinement: GPR25 is a stronger MS-UC lead with restoration/agonism direction, ZMIZ1 is a confirmed opposite-direction decoupling locus, and PTGER4 is not a simple transfer target.
- Stop reason: completed V16 bounded deliverable; no remaining V16 lead is blocked at the significant-QTL direction layer, but formal full-summary-statistics QTL colocalization and cell-state/perturbation validation remain incomplete.
- Next action: run formal all-variant QTL colocalization if GTEx/eQTLGen full summary statistics can be indexed or downloaded; otherwise prioritize GPR25 cell-state expression and ligand/agonist feasibility while preserving ZMIZ1 as a decoupling finding.

## RUN SUMMARY - 2026-06-06 01:39 UTC

- Active runtime: approximately 61 minutes; total elapsed approximately 61 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-06 00:38 UTC.
- Session end UTC: 2026-06-06 01:39 UTC.
- Frontier advanced: V17 consolidated the chr1 MS-UC locus into a `GPR25` versus `KIF21B` causal-gene ambiguity, added h5ad/CXCL17 ligand-context scans, wrote critique/source/convergence/experimental-design artifacts, and made the V17 expression and checkpoint summaries reproducible.
- GPR25 step status: causal-gene hardening partially successful but not exclusive (`GPR25` MS/eQTL max PP.H4 `0.969296`, UC/eQTL `0.981623`; `KIF21B` also high at `0.956099` and `0.963951`); local MS CNS atlases lack `GPR25`; h5ad scans found `GPR25` absent/trace while `KIF21B` is more detectable; CXCL17 ligand context is strong in Sjogren salivary epithelium but absent/trace in gut, RA blood, psoriasis skin, and IBD myeloid atlases.
- ZMIZ1 lock status: preserved as a robust opposite-direction MS/Crohn eQTL decoupling finding; no Crohn-to-MS transfer claim.
- PTGER4 close-out status: closed as signal-conflicted and not a simple MS-UC transfer target unless signal-specific cell-type QTL data appears.
- GPR25 verdict: alive Tier 1 genetics-to-lymphocyte-trafficking lead, not intervention-grade; the chr1 locus requires protein-level or genotype-linked immune/CSF data to resolve `GPR25` versus `KIF21B`.
- Stop reason: completed V17 bounded deliverable and resume-state update; no long-running analysis processes remain.
- Next action: use `docs/workups/genetics/GPR25_KIF21B_EXPERIMENTAL_DESIGN_V17.md` as the default handoff unless controlled-access protein/CITE-seq data is found; test genotype-linked GPR25/KIF21B expression and CXCL17 migration/RhoA/integrin function before any intervention-grade claim.

## RUN SUMMARY - 2026-06-06 08:08 UTC

- Active runtime: approximately 35 minutes; total elapsed approximately 35 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-06 07:33 UTC (estimated from first V18 command and file timestamps).
- Session end UTC: 2026-06-06 08:08 UTC.
- Frontier advanced: V18 triaged acquisition sources, acquired and checksummed 19 Tier 1 files (~497 MB raw, gitignored), wrote Tier 2/Tier 3 acquisition instructions, updated manifest/resume state, and found public OneK1K/DICE/eQTL Catalogue data favors KIF21B context but does not resolve GPR25-versus-KIF21B causality.
- Sources triaged per tier: Tier 1 acquired/self-queryable `5` source families (OneK1K, DICE, eQTL Catalogue/FTP-tabix, IUPHAR, GPCRdb); Tier 1 service/resource-blocked or not acquired `5` source classes (eQTL Catalogue REST HTTP 500, full QTD000021, OneK1K GEO raw tar, DICE unfiltered VCFs, CELLxGENE/HCA expression-only); Tier 2 `0` new key-gated sources; Tier 3 `4` controlled/manual source classes.
- Tier 1 acquired vs blocked: acquired OneK1K top eQTL, DICE mean expression plus significant eQTL panel, eQTL Catalogue QTD000021 chr1 targeted extract, IUPHAR GPR25 JSON, GPCRdb GPR25 JSON; no proxy `x-deny-reason` observed; eQTL Catalogue REST returned HTTP 500 from `www.ebi.ac.uk`.
- Top human next-actions: prioritize MS PBMC/CSF genotype plus scRNA/CITE-seq controlled cohorts; then DICE controlled dbGaP `phs001703.v3.p1`; then OneK1K individual-level/raw data if needed; no host allowlisting is currently required.
- Stop reason: completed V18 acquisition-plan deliverable and resume-state update; no long-running processes remain.
- Next action: verify QTD000021/eQTL Catalogue metadata and run dense variant intersection/colocalization only if metadata is trustworthy; otherwise move to the Tier 3 controlled/protein-data path for genotype-linked GPR25/KIF21B expression.

## RUN SUMMARY - 2026-06-06 08:59 UTC

- Active runtime: approximately 12 minutes; total elapsed approximately 12 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-06 08:47:44 UTC.
- Session end UTC: 2026-06-06 08:59:22 UTC.
- Frontier advanced: V19 re-evaluated the chr1 MS-UC locus under first-principles druggability discipline, added dense QTD000021 KIF21B coloc, effect-direction counts, AlphaFold domain-confidence summaries, KIF11 comparator chemistry, and updated README/resume state.
- KIF21B status: serious competing causal-gene candidate; QTD000021 coloc PP.H4 `0.874879034973956` for MS/eQTL and `0.868660082128031` for UC/eQTL over `472` aligned SNPs; exact shared credible-set risk alleles lower KIF21B expression `11 / 11` for both MS and UC; structurally ligandable motor domain but likely wrong-direction for inhibition.
- GPR25 status: alive but downgraded from protected favorite; still strongest in eQTLGen shared-block evidence, but unsupported by V18 public immune-QTL sources and absent/trace in available scRNA; structurally plausible GPCR but agonism/restoration is chemically immature.
- Both druggability assessments: prior-art-only framing corrected; GPR25 is structurally plausible but causally/expression-limited, KIF21B is structurally tractable in the motor domain but therapeutically difficult because restoration/up-function is the direction.
- Integrated verdict: chr1 is real shared MS-UC genetics/mechanism, not an intervention-grade target; the decisive next layer is genotype-stratified immune-cell or CSF single-cell/CITE-seq/protein data for exact chr1 shared haplotype carriers.
- Stop reason: completed V19 bounded deliverable; remaining work is external/metadata-dependent rather than an unstarted V19 step.
- Next action: verify QTD000021/eQTL Catalogue metadata for publication-grade use or move to controlled/protein-data acquisition and wet-lab genotype-stratified expression/functional assays.

## RUN SUMMARY - 2026-06-06 09:59 UTC

- Active runtime: approximately 45 minutes; total elapsed cannot be measured precisely because the V20 session resumed from a context-compacted/interrupted state; no usage-limit waiting time was observed in the resumed segment.
- Session start UTC: approximately 2026-06-06 09:14 UTC.
- Session end UTC: 2026-06-06 09:59 UTC.
- Frontier advanced: V20 produced a reproducible 13-candidate next-tier lead slate across four workstreams, updated resume state and README, rebuilt the knowledge index, and documented the subagent thread-limit blocker.
- Leads generated per workstream: A next-tier colocalized loci `4`; B thin/unpopulated axes `3`; C repositioning/agreement structure `3`; D decoupling-as-signal `3`.
- Ranked slate summary: `5` promising follow-ups, `2` hard-target real-biology findings, and `6` negative/not-now entries; top lead is dynamic APC/HLA-II treatment-response monitoring, with chr14 `ZFP36L1` and chr2 `REL/PUS10/USP34` as next genetics-region follow-ups.
- Stop reason: completed bounded V20 slate deliverable; broad live subagent execution was environmentally blocked by agent thread limit, and new locus-level coloc was intentionally deferred to the next queued action so the slate remains resumable.
- Next action: run bounded SuSiE-coloc for MS-Crohn chr14 `14:68710199-69753364` and MS-UC chr2 `2:60689469-61742410`; if either survives, run allele-aligned immune-QTL colocalization plus first-principles direction-matched druggability.

## RUN SUMMARY - 2026-06-06 11:15 UTC

- Active runtime: approximately 2 minutes; total elapsed approximately 2 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-06 11:14 UTC.
- Session end UTC: 2026-06-06 11:15 UTC.
- Frontier advanced: LDSC reference-panel provisioning state verified on disk; `meta/LDSC_PANEL_STATUS.md` written, README updated, and knowledge index rebuilt.
- Stop reason: completed.
- Next action: LDSC genetic-correlation analyses may proceed from a provisioning standpoint; next research action remains bounded SuSiE-coloc for MS-Crohn chr14 `14:68710199-69753364` and MS-UC chr2 `2:60689469-61742410`.

## RUN SUMMARY - 2026-06-06 11:42 UTC

- Active runtime: approximately 23 minutes; total elapsed approximately 23 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-06 11:19 UTC.
- Session end UTC: 2026-06-06 11:42 UTC.
- Frontier advanced: V21 established the first LDSC genome-wide genetic-correlation backdrop for MS vs UC/Crohn/RA/SLE, ran bounded SuSiE-coloc for the two queued V20 loci, wrote `docs/workups/genetics/GENETIC_CORRELATION_BACKDROP_V21.md`, `docs/history/LEAD_SLATE_V21.md`, and `docs/convergence/CONVERGENCE_CHECK_V21_01.md`, updated resume state and README, and rebuilt the knowledge index.
- rg pairs computed: MS-UC `rg = 0.3342`, MS-Crohn `rg = 0.1675`, MS-RA `rg = 0.1692`, MS-SLE `rg = 0.2439`; UC/Crohn raw MHC-excluded runs were identical after LDSC merge because the verified reference panel has zero chr6:25-34 Mb SNPs in the active regression set.
- Loci verdicts: chr14 `ZFP36L1` is suggestive but not robust (`PP.H4 = 0.687732800443124`) and is parked; chr2 `REL/PUS10/USP34` returned no `coloc.susie` credible-set summary and is closed/not-now.
- chr1-bar verdict: neither V21 locus clears the chr1 bar; no new genetics target should be surfaced to the medical team from chr14 or chr2.
- Stop reason: completed the bounded V21 core deliverable for UC, Crohn, RA, SLE plus both queued loci; no long-running analysis processes remain.
- Next action: extend LDSC rg to remaining map diseases after verifying OpenGWAS IDs, or pivot to a locked dynamic APC/HLA-II MS DMT monitoring rule tested only on held-out cohorts.

## RUN SUMMARY - 2026-06-06 12:07 UTC

- Active runtime: approximately 24 minutes; total elapsed approximately 24 minutes; no usage-limit waiting time observed. Runtime is estimated because the V22 session resumed after context compaction.
- Session start UTC: approximately 2026-06-06 11:43 UTC.
- Session end UTC: 2026-06-06 12:07 UTC.
- Frontier advanced: V22 locked the APC/HLA-II dynamic treatment-response rule before held-out testing, validated it on reachable independent cohorts, wrote `docs/validation/VALIDATION_LEDGER_V22.md`, `docs/findings/FINDING_V22.md`, `docs/validation/COHORT_SEARCH_V22.md`, `docs/convergence/CONVERGENCE_CHECK_V22_01.md`, updated resume state and README, and rebuilt the knowledge index.
- Cohorts tested with pass/fail: `GSE235357` MS dimethyl fumarate primary locked pass (AUC `0.72`, Hedges g `0.651`, `n=10`); `GSE250453` MS fingolimod primary locked fail (AUC `0.60`, Hedges g `0.150`, `n=10`); `GSE85034_ADA` psoriasis adalimumab primary locked fail (AUC `0.511`, Hedges g `0.044`, `n=14`); `GSE253006_TOF` UC tofacitinib exploratory module-approximation pass (AUC `1.00`, Hedges g `1.522`, `n=9`) not counted as primary validation.
- Validation verdict: no Tier 4 breakthrough and no kill; the locked dynamic rule remains a provisional early-treatment monitoring lead.
- Stratifier vs monitor characterization: V22 supports only an early on-treatment monitoring interpretation; it does not validate a baseline patient-selection stratifier or a clinical decision threshold.
- Stop reason: completed the bounded V22 validation package; no long-running analysis processes remain.
- Next action: do not tune `docs/locked_rules/LOCKED_RULE_V22.md`; acquire or identify a larger paired MS DMT response cohort (`n >= 30`) or recompute exact frozen modules in `GSE253006_TOF` at compartment-resolved level before considering any successor locked rule.

## RUN SUMMARY - 2026-06-06 12:32 UTC

- Active runtime: approximately 24 minutes; total elapsed approximately 24 minutes; no usage-limit waiting time observed.
- Session start UTC: approximately 2026-06-06 12:08 UTC.
- Session end UTC: 2026-06-06 12:32 UTC.
- Frontier advanced: V23 completed the self-driving workup of the APC/HLA-II monitoring lead: pooled V22 cohorts, characterized mechanism specificity, resolved the UC tofacitinib exact-module caveat from raw 10x data, regenerated exact marker-compartment scoring, wrote `docs/workups/treatment_response/APC_HLA_MONITORING_WORKUP_V23.md`, updated README/resume state, and rebuilt the knowledge index.
- Sequence of actions executed: Action 1 pooled small cohorts; Action 2 characterized drug-mechanism specificity; Action 3 recomputed exact frozen modules in `GSE253006_TOF`; Action 4 ran exact marker-derived compartment rescoring; Action 5 sharpened monitoring-only clinical utility; Action 6 decided not to lock a V23 successor rule without fresh held-out data.
- Pooled result: unbounded primary locked pooled AUC `0.547` (CI `0.337-0.743`), Hedges g `0.180`; primary plus exact UC AUC `0.656` (CI `0.489-0.808`), Hedges g `0.611`; bounded DMF plus exact tofacitinib AUC `0.811` (CI `0.567-1.000`), Hedges g `1.191`.
- Mechanism-bounding verdict: bounded immune-remodeling/JAK-STAT monitoring domain is plausible and stronger than the unbounded rule; fingolimod/S1P and psoriasis lesional adalimumab contexts fail or weaken the broad claim.
- Tofacitinib resolution: exact frozen all-cell `GSE253006_TOF` rescoring passes with AUC `0.95`, CI `0.70-1.00`, Hedges g `1.811`; exact marker-derived compartments show strongest specific signal in `t_cell_like` and `b_plasma_like`, with myeloid/APC-like positive but weaker.
- Stop reason: all V23 Actions 1-5 completed and Action 6 completed as "no successor lock without fresh held-out data"; no long-running analysis processes remain.
- Next action: acquire a larger paired MS DMT response cohort (`n >= 30`) in an immune-remodeling/JAK-STAT-like therapy context, then lock a bounded successor rule before testing it.

## RUN SUMMARY - 2026-06-06 14:45 UTC

- Active runtime: approximately 55 minutes; total elapsed approximately 55 minutes; no usage-limit waiting time observed. Runtime is estimated because this V24 session resumed after context compaction.
- Session start UTC: approximately 2026-06-06 13:50 UTC.
- Session end UTC: 2026-06-06 14:45 UTC.
- Frontier advanced: V24 completed the dedicated treatment-response validation cohort scout, wrote `docs/workups/microbiome/DATA_SCOUT_V24.md`, search log and candidate inventory TSVs, updated resume state and README, and identified the best low-barrier validation source.
- Source types searched: GEO; ArrayExpress/BioStudies; ENA/SRA; EGA; Zenodo/Figshare/Dryad/OSF; PubMed/Europe PMC paper mining; consortia/portal routes; preprint supplements; partially used datasets.
- Total candidates found/triaged: 8 ranked candidate sources in `analysis/v24_data_scout/v24_candidate_inventory.tsv`, plus rejected/false-positive hits logged in `analysis/v24_data_scout/v24_search_log.tsv`.
- Candidates usability-verified: `GSE130478/GSE130491/GSE130494`, `GSE85034_MTX`, `GSE253495`, and the Gafson et al. 2018 PubMed design/label description; Gafson public accession was not verified.
- Tier 1 downloaded/ready: no primary fresh MS validation cohort; `GSE85034_MTX` is already local and usable only as a secondary same-study/cross-disease stress test.
- Tier 2 low-barrier with steps: Gafson et al. 2018 DMF PBMC RNA-seq data request is the top action; `GSE130478/GSE130491/GSE130494` response-label mapping request is second.
- Dry-well verdict: public ready-to-run data are effectively dry for primary validation, but low-barrier data are not dry.
- Stop reason: completed V24 scout scope; no long-running analysis processes remain.
- Next action: request/acquire Gafson et al. 2018 processed PBMC RNA-seq counts plus NEDA-4 sample labels, then lock any successor rule only after fresh held-out data are present.

## RUN SUMMARY - 2026-06-06 20:56 UTC

- Active runtime: approximately 4 minutes; total elapsed approximately 4 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-06 20:52 UTC.
- Session end UTC: 2026-06-06 20:56 UTC.
- Frontier advanced: V25 inventoried model-building datasets, wrote and committed `docs/workups/treatment_response/MODEL_DESIGN_V25.md` plus immutable train/held-out split before validation, built a bounded empirical Mixscale module-response model, validated it on held-out perturbations, wrote `docs/workups/treatment_response/MODEL_CARD_V25.md`, and updated resume state and README.
- Phases completed: Phase 1 scope/data/split completed; Phase 2 bounded model built; Phase 3 held-out validation completed; Phase 4 project-finding checks completed; Phase 5 live hypothesis triage completed with abstentions; Phase 6 model card completed.
- Architecture chosen: bounded empirical pathway/module mean model over Mixscale IFNB/IFNG/TNFA perturbation summaries; broad foundation-model/ODE/ML approaches were rejected as not validateable with current data.
- Held-out validation result and validated domain: `6` held-out perturbations, `24` module predictions, direction accuracy `0.542`, MAE `0.261` log2FC, Pearson `0.531`, Spearman `0.377`; no reliable validated domain for wet-lab triage was established.
- Agreement with project findings: weak directional compatibility for IFNG/JAK suppression of IFN/APC/HLA-II modules; no valid test of T/B compartment localization, KIF21B/GPR25, or ZMIZ1.
- Hypothesis-triage output: IFN/JAK monitoring biology receives only a low-resolution descriptive prior; KIF21B/GPR25 and ZMIZ1 are outside domain and the model abstains.
- Honest simulator verdict: no usable validated simulator was achieved from current data; V25 is a bounded negative result.
- Stop reason: completed all V25 phases with a negative validation verdict; no long-running analysis processes remain.
- Next action: do not use V25 model for wet-lab triage; acquire Gafson et al. 2018 DMF PBMC RNA-seq counts plus NEDA-4 labels or map State/Parse feature IDs to gene symbols before any future model attempt.

## RUN SUMMARY - 2026-06-06 23:23 UTC

- Active runtime: approximately 7 minutes; total elapsed approximately 7 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-06 23:16 UTC.
- Session end UTC: 2026-06-06 23:23 UTC.
- Frontier advanced: V26 inventoried held modality artifacts, ran null-tested cross-modal latent-axis, module-dependency, and invariant scans over existing module-level data, wrote `docs/findings/DEEP_STRUCTURE_V26.md`, updated `meta/queues/V26_QUEUE.md`, `meta/NEXT_ACTIONS.md`, and README.
- Workstreams completed: A cross-modal latent structure completed; B higher-order module dependency completed; C invariant/negative-space completed; D stalled-lead reread/integration completed.
- Robust latent axes found: `2` supported pairings: treatment pharmacodynamic vs h5ad cell state (cosine `0.933576`, BH q `0.009995`) and h5ad cell state vs cross-disease summary (cosine `0.879242`, BH q `0.017491`).
- Surviving interactions: `25` supported replicated module-dependency rows; strongest recurring dependency is `hla_ii_apc` with `mif_cd74_receptor_state` across four modalities.
- Load-bearing invariants: `0` passed the stricter invariant gate after BH correction; do not claim V26 invariants.
- Cross-workstream convergences: coupled APC remodeling structure links HLA-II, IFN/APC, MIF/CD74 receptor state, IFN readout, and lysosomal processing; it strengthens the monitoring-mechanism interpretation but not baseline stratification or target nomination.
- Re-reading of stalled leads: bounded APC/HLA-II monitoring strengthened as coupled early immune remodeling; chr1/KIF21B remains hard-target wrong-direction; GPR25 remains unsupported by held module/QTL data; ZMIZ1 remains opposite-direction decoupling; PTGER4 remains closed.
- Single best structurally-grounded hypothesis: a coordinated APC remodeling architecture should be measured as a coupled early on-treatment axis, and falsified by testing whether the coupled score outperforms single modules in a fresh paired cohort and in APC/T/B perturbation data.
- Stop reason: completed all four bounded V26 workstreams and synthesis; no long-running analysis processes remain.
- Next action: acquire/request Gafson et al. 2018 DMF PBMC RNA-seq counts plus NEDA-4 labels or another fresh paired treatment-response cohort, then test whether the coupled APC remodeling axis improves over the immutable V22 scalar without tuning on validation data.

## RUN SUMMARY - 2026-06-06 23:35 UTC

- Active runtime: approximately 12 minutes; total elapsed approximately 12 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-06 23:23 UTC.
- Session end UTC: 2026-06-06 23:35 UTC.
- Frontier advanced: V27 froze coupled APC-axis candidate features before comparison, ran fixed-feature scalar-vs-coupled evaluation with bootstrap and 5,000-permutation max-candidate null, wrote `docs/workups/treatment_response/COUPLED_AXIS_V27.md`, `docs/validation/VALIDATION_READINESS_V27.md`, `meta/queues/V27_QUEUE.md`, and future scoring harness scripts.
- Phases completed: Phase 1 coupled representation completed; Phase 2 scalar-vs-coupled comparison completed; Phase 3 successor-lock decision completed with no lock; Phase 4 validation harness completed; Phase 5 mechanistic interpretation completed.
- Scalar-vs-coupled verdict: no coupled feature improved over the immutable V22 scalar. In the bounded domain, V22 scalar AUC `0.811111`, Hedges g `1.190835`; best coupled feature `coupling_coordination` AUC `0.733333`, Hedges g `0.776968`; coupled-minus-scalar AUC delta `-0.077778`; max-candidate permutation p `0.912817`.
- Held-out/null evidence: fixed zero-parameter features were evaluated on already-held V22/V23 cohorts only; label-permutation null with `5,000` permutations showed no coupled advantage. No fresh Gafson/NEDA cohort was present or read.
- Successor locked: no; `LOCKED_RULE_V27.md` was intentionally not created.
- Validation-harness readiness: `scripts/v27_apply_locked_rules.py` and `docs/validation/VALIDATION_READINESS_V27.md` are ready for future paired module-delta cohorts; primary validation remains `docs/locked_rules/LOCKED_RULE_V22.md`.
- Stop reason: completed all V27 phases and documented a negative successor-rule result; no long-running analysis processes remain.
- Next action: acquire/request Gafson et al. 2018 DMF PBMC RNA-seq counts plus NEDA-4 labels, prepare the paired module-delta TSV, and run the frozen V22 scoring harness mechanically without tuning.

## RUN SUMMARY - 2026-06-06 23:46 UTC

- Active runtime: approximately 18 minutes; total elapsed approximately 18 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-06 23:28 UTC.
- Session end UTC: 2026-06-06 23:46 UTC.
- Frontier advanced: maintenance-only repository restructuring completed; `meta/REPO_INVENTORY_PRE.md`, `meta/REPO_RESTRUCTURE_PLAN.md`, `meta/REPO_MOVE_MAP.tsv`, `docs/ARTIFACT_INDEX.md`, and `meta/REPO_INVENTORY_POST.md` written; root Markdown artifacts moved into `docs/`/`meta/queues/` with `git mv`; canonical README/meta/knowledge references updated; RAG index rebuilt.
- Stop reason: completed.
- Next action: resume research from `meta/NEXT_ACTIONS.md`; primary scientific next action remains acquiring/requesting Gafson et al. 2018 DMF PBMC RNA-seq counts plus NEDA-4 labels and validating the immutable V22 rule mechanically when fresh paired data arrives.

## RUN SUMMARY - 2026-06-06 23:55 UTC

- Active runtime: approximately 9 minutes; total elapsed approximately 9 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-06 23:46 UTC.
- Session end UTC: 2026-06-06 23:55 UTC.
- Frontier advanced: maintenance-only root cleanup completed for project-owned V2/V3 artifacts; `results_v2`, `results_v3`, `literature_v3`, `subagents_v3`, and V2/V3 entrypoint scripts moved with `git mv`; empty V2/V3 placeholder directories moved under `phases/` with `.gitkeep`; path references, README, artifact index, and RAG index updated.
- Stop reason: completed.
- Next action: resume research from `meta/NEXT_ACTIONS.md`; primary scientific next action remains acquiring/requesting Gafson et al. 2018 DMF PBMC RNA-seq counts plus NEDA-4 labels and validating the immutable V22 rule mechanically when fresh paired data arrives.

## RUN SUMMARY - 2026-06-07 00:13 UTC

- Active runtime: approximately 13 minutes; total elapsed approximately 13 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-07 00:00 UTC.
- Session end UTC: 2026-06-07 00:13 UTC.
- Frontier advanced: V28 heterogeneous-toolchain assault completed; wrote `meta/TOOLING_INVENTORY_V28.md`, `meta/TOOL_KEY_REQUESTS_V28.md`, `meta/queues/V28_QUEUE.md`, `scripts/check_openai_access.py`, `scripts/v28_heterogeneous_response_analysis.py`, `analysis/v28_heterogeneous_response/`, and `docs/workups/treatment_response/ROBUSTNESS_MAP_V28.md`; README, current status, next actions, and RAG index updated.
- Tools/languages/sub-models used: OpenGWAS checker via `python3`; `.venv_v3_py312` Python stack with `numpy`, `pandas`, `scipy`, `sklearn`, and `statsmodels`; R/Node/Java inventoried but not used for analysis; external LLM/sub-model not used because no key is configured.
- Paid services used / spend: none; estimated spend `$0`.
- Keys requested: `OPENAI_API_KEY` as optional low-cost external critique/proposal lens, with checker `scripts/check_openai_access.py`.
- Tool-robust-vs-tool-dependent verdict: bounded V22 scalar is statistically tool-robust across fixed-score permutation, nonparametric, cohort-adjusted, Bayesian-bootstrap, and jackknife lenses, but model-flexibility fragile because ridge multifeature ML, receptor-only, coupled-axis, and dynamic-vector variants do not improve it.
- Grounded sub-model proposals: no external sub-model proposals were run; local hostile proposals tested receptor confounding, cohort pooling, single-subject influence, and dynamic/coupled extensions. Receptor/cohort/single-subject artifact explanations failed; dynamic/coupled extensions did not improve the scalar.
- Novel analyses and outcomes: dynamic/vector features (`apc_vector_norm`, `hla_vs_ifn_angle`, `hla_ifn_product`) did not outperform the scalar; bounded scalar AUC `0.811`, Hedges g `1.191`, permutation p `0.007996`, cohort-adjusted p `5.70e-07`, Bayesian-bootstrap P(diff > 0) `0.999`, jackknife AUC range `0.7875-0.8875`.
- Breadth value: broadened tooling strengthened confidence in the simple immutable scalar and argued against adding complexity before fresh validation.
- Stop reason: completed all V28 workstreams with local tools; no long-running analysis processes remain.
- Next action: acquire/request Gafson et al. 2018 DMF PBMC RNA-seq processed counts plus NEDA-4 labels and run the frozen V22 scoring harness mechanically; if `OPENAI_API_KEY` is provided, run `python3 scripts/check_openai_access.py` and use it only to generate additional grounded critique proposals.

## RUN SUMMARY - 2026-06-07 00:30 UTC

- Active runtime: approximately 16 minutes; total elapsed approximately 16 minutes; no usage-limit waiting time observed.
- Session start UTC: 2026-06-07 00:14 UTC.
- Session end UTC: 2026-06-07 00:30 UTC.
- Frontier advanced: V29 independent-lens queue and dormant-lead reactivation completed; OpenGWAS verified; Anthropic/Google/Gemini key absence documented; wrote `meta/INDEPENDENT_REVIEW_QUEUE_V29.md`, `meta/queues/V29_QUEUE.md`, and `docs/history/LEAD_INVENTORY_V29.md`; README, current status, next actions, and RAG index updated.
- Cross-lineage lens availability and spend: no `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, or `GEMINI_API_KEY` configured; independent sub-model not used; paid spend `$0`.
- Independent-lens proposals grounded: none this session because no cross-lineage key was available; full review package queued for immediate use when a key lands.
- Dormant leads reactivated: no intervention-grade dormant lead; postpartum HLA-II/CD64 APC-axis split reactivated as the best natural-experiment biology lead; MIF/CD74 partially reactivated as coupled APC context; ZMIZ1 preserved as a transfer-validity decoupling finding.
- Cross-domain reframings and outcomes: NAMPT/HIF/glycolysis reframed as metabolic-stress covariate, not target; systems/dynamics reframing supports the simple V22 scalar over generic trajectory geometry; structural reframing keeps FPR2/ALX as a wet-lab comparator only.
- Refreshed lead inventory: top queue is V22 APC/HLA-II scalar validation, postpartum HLA-II/CD64 split, ZMIZ1 decoupling, chr1 KIF21B/GPR25 controlled-data handoff, MIF/CD74 context, FPR2/ALX comparator, NAMPT covariate; NAMPT/PTGER4/ZFP36L1/REL/TYK2 remain parked or closed.
- Stop reason: completed all available V29 workstreams; model-gated Workstream A is blocked only by absent cross-lineage key; no long-running analysis processes remain.
- Next action: if `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, or `GEMINI_API_KEY` is provided, verify and run `meta/INDEPENDENT_REVIEW_QUEUE_V29.md`; otherwise continue acquiring/requesting Gafson et al. 2018 DMF PBMC RNA-seq counts plus NEDA-4 labels and run the frozen V22 scoring harness mechanically.
## RUN SUMMARY - V30 SAP AI Core Independent Review Checkpoint

- Active runtime: approximately 24 minutes active; total elapsed approximately
  24 minutes (no usage-limit waiting).
- Session start timestamp (UTC): 2026-06-07 00:29:00 UTC (estimated).
- Session end timestamp (UTC): 2026-06-07 00:53:00 UTC.
- Frontier advanced: SAP AI Core service-key auth, deployment discovery, Gemini
  smoke tests, reusable client, access report, and Gemini-only grounded
  proposal queue were completed; full multi-lineage review remains blocked.
- Stop reason: completed available V30 work with documented blocker for
  multi-lineage completion.
- Next action: resolve Claude or Mistral SAP AI Core inference schema so at
  least two non-OpenAI lineages smoke-pass, then rerun the V29 review package
  across lineages and ground the de-duplicated proposals.
- SAP AI Core access status: OAuth and deployment listing work; Gemini
  `gemini-3.1-flash-lite` and `gemini-2.5-pro` smoke-pass; Claude deployments
  are running but reject tested subpaths; Mistral corrected chat-completions
  request timed out.
- Model spend: SAP AI Core usage only; no separate paid service spend observed
  or estimated in-repo.
- Multi-model proposals grounded: Gemini-only proposals recorded; no
  multi-lineage proposal was grounded. Steroid-pulse mimic is blocked on fresh
  data scout; metabolic confounding is queued for pathway scoring; KIF21B
  trans/pathway analysis is queued/data-limited.
- Model-raised vulnerabilities tested: arbitrary mechanism boundary is
  partially addressed by V23/V28 cohort-adjusted/jackknife evidence; small-n
  model fallacy is held as a real limitation; premature KIF21B modality filter
  remains queued for trans-eQTL/pathway analysis.
- Biology leads advanced: no lead upgraded; postpartum HLA-II/CD64 APC split
  remains the best dormant biology lead; V22 bounded scalar remains the active
  validation lead.
- Multi-lineage review added value beyond agent analysis: not yet established,
  because only Gemini smoke-passed; Gemini did add concrete queue items but no
  grounded lead upgrade.
