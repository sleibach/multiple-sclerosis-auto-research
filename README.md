# MS Auto-Research

An autonomous, reproducible computational search for a novel, falsifiable
therapeutic target in multiple sclerosis (MS) and the broader cross-autoimmune
mechanism landscape. The project runs in successive
phases (V1 through VN); each phase is preserved rather than overwritten so the
full reasoning trace stays auditable.

All analysis uses public human-tissue data only and random seed `20260526`
(V5 analyses use `20260528`).

## Current Status

The current phase is **V22**. The V4 directory structure remains canonical, and
V11 introduced the resume backbone for short-session continuity.

- Start here: `meta/CURRENT_STATUS.md` — the live mission state, active leads,
  and next actions.
- Current active treatment-response focus: the V20/V21 top actionable lead,
  dynamic APC/HLA-II treatment-response monitoring, underwent locked
  held-out validation in V22. `LOCKED_RULE_V22.md` was committed before
  validation. Primary locked results were mixed: MS dimethyl fumarate
  `GSE235357` passed the small-n rule (AUC `0.72`, Hedges g `0.65`, `n=10`),
  MS fingolimod `GSE250453` failed (AUC `0.60`, Hedges g `0.15`, `n=10`), and
  psoriasis adalimumab `GSE85034_ADA` failed (AUC `0.511`, Hedges g `0.044`,
  `n=14`). UC tofacitinib `GSE253006_TOF` passed numerically but is
  exploratory because the module was a precomputed approximation rather than
  the exact frozen V22 gene set. V22 does not reach breakthrough and does not
  meet the kill threshold; the rule remains a provisional early-treatment
  monitoring lead, not a validated clinical stratifier. V23 then pooled the
  small cohorts and resolved the UC tofacitinib caveat by exact raw-10x
  rescoring: exact `GSE253006_TOF` passes (AUC `0.95`, Hedges g `1.81`) and
  the bounded DMF-plus-exact-tofacitinib set reaches pooled AUC `0.811`
  (`0.567-1.000`). The unbounded primary rule remains weak (AUC `0.547`).
  Current interpretation: bounded early-monitoring hypothesis for
  immune-remodeling/JAK-STAT contexts, not a universal cross-therapy rule and
  not yet clinically validated.
- Current genetics/data focus: the chr1 MS-UC causal-gene question is
  computationally resolved for now and handed forward as real shared genetics,
  not an intervention-grade target. V20 widened back out to a ranked
  next-tier slate; V21 supplied the first LDSC genome-wide
  genetic-correlation backdrop and vetted the two queued next-tier genetics
  loci.
- Confirmed first-pass high-H4 regions from V13/V14 include MS-UC chr1,
  MS-UC chr5/PTGER4, MS-Crohn chr10, and MS-Crohn chr17/STAT3-STAT5. The
  chr1 and chr10 loci passed bounded SuSiE-coloc follow-up. V15 mapped the
  chr1 locus most strongly to `GPR25` and the chr10 locus most strongly to
  `ZMIZ1`, but did not upgrade matrix grades because raw eQTL/pQTL
  effect-allele alignment, stronger cell-state evidence, and perturbation
  support remain missing. V15 also downgraded chr17/STAT3-STAT5 under
  bounded SuSiE-coloc and reframed chr5/PTGER4 as a mixed shared/distinct
  signal-decomposition problem. V16 added allele-aligned GTEx/eQTLGen evidence:
  `GPR25` expression-increasing alleles are protective for both MS and UC,
  `ZMIZ1` expression-increasing alleles are MS-risk and Crohn-protective, and
  `PTGER4` remains signal-conflicted. V17 streamed the full eQTLGen file for
  chr1 candidate genes and found `GPR25` strongest in the disease-shared block,
  but bounded disease-vs-eQTL SuSiE-coloc also supports `KIF21B`; local MS CNS
  atlases did not contain measurable `GPR25`. V18 acquired and smoke-tested
  public OneK1K top eQTLs, DICE significant eQTL/mean expression, a targeted
  eQTL Catalogue chr1 extract, IUPHAR, and GPCRdb. These public genotype-linked
  immune sources favor `KIF21B` context but still do not resolve `GPR25`
  protein/genotype causality or the controlled MS PBMC/CSF immune-data gap.
  V19 ran dense QTD000021 KIF21B coloc against the chr1 disease signal:
  MS/eQTL PP.H4 `0.874879034973956`, UC/eQTL PP.H4 `0.868660082128031`;
  exact shared credible-set variants showed disease-risk alleles lowering
  KIF21B expression `11 / 11` for both MS and UC. The integrated verdict is
  real shared genetics/mechanism, not an intervention-grade target. V20 then
  generated `LEAD_SLATE_V20.md`, a 13-candidate ranked next-tier slate. The
  top actionable lead is dynamic APC/HLA-II treatment-response monitoring in
  MS. V21 then established the genome-wide LDSC backdrop: MS-UC is the
  strongest tested comparator (`rg = 0.3342`), MS-SLE is positive but caveated
  by high h2 intercept (`rg = 0.2439`), and MS-RA/MS-Crohn are modestly
  positive (`rg = 0.1692` and `0.1675`). The V20 queued chr14 `ZFP36L1`
  region was only suggestive under bounded SuSiE-coloc (`PP.H4 = 0.6877`),
  and chr2 `REL/PUS10/USP34` did not produce a SuSiE credible-set summary.
  Neither clears the chr1 bar.
- `ACSL1`, `NAMPT`, and several early target candidates were demoted or parked
  under the V4/V5 prior-art and tiering framework. Current value has shifted to
  axis-disagreement mining, genetics-grounded transfer-validity analysis, and
  locked treatment-response biomarker validation.

## How To Read This Repository

For a future agent or human picking this up, the canonical read order is:

1. `meta/CURRENT_STATUS.md`
2. `meta/PRIOR_ART_RULEBOOK.md`
3. `meta/TIERING_RULEBOOK.md`
4. `knowledge/candidates/INDEX.md`
5. `knowledge/dimensions/INDEX.md`
6. `meta/NEXT_ACTIONS.md`
7. `archive/ARCHIVE_INDEX.md`

## Standing Session Rule

Every session must end by appending a `RUN SUMMARY` block to
`meta/SESSION_LOG.md` and echoing the same block in the final chat response.
The block must include active runtime, UTC start/end timestamps, frontier
advanced, stop reason, and next action. This rule is also recorded at the top
of `meta/SESSION_LOG.md`.

Every session must also update `README.md` before ending so the repository
entry point stays synchronized with the current project phase, frontier, and
standing rules. If no README content change is needed, the session must state
that explicitly in `meta/SESSION_LOG.md`.

## Repository Layout

| Path | Contents |
|---|---|
| `meta/` | Live status, roadmaps, rulebooks (prior-art and tiering), and convergence checks for the current phase. |
| `knowledge/` | Canonical distilled knowledge: per-candidate histories (`candidates/`), evidence dimensions (`dimensions/`), mechanism hypotheses (`mechanisms/`), dataset/tool registries, and an append-only decision log (`decisions/`). |
| `analysis/` | Tiered analyses (`tier_0_triage/`, `tier_1_mechanism/`) for the current phase, each with a `REPORT.md` and decision artifacts. |
| `results/`, `results_v2/`, `results_v3/` | Per-phase analysis outputs (TSV/JSON/reports). |
| `scripts/` | Analysis scripts; `v3_*.py` are the V3 wave scripts. |
| `subagents/`, `subagents_v3/` | Specialist subagent reports. |
| `data/` | `raw*/` (downloaded public inputs, Git-ignored) and `derived*/` (computed tables, manifests, and SHA-256 hashes). |
| `archive/` | Index and pointers freezing the V1–V3 phases as historical. |

## Phase History

| Phase | Question | Outcome |
|---|---|---|
| V1 | Does a 4-1BB costimulation score (`TNFRSF9`/`TNFSF9`) track a lipid/complement microglial program in human MS lesions? | Constrained association test executed; see `MS_RESEARCH_LOG_2026-05-26.md`, `SELECTION.md`. |
| V2 | Can a single MS lipid-handling target (`ACSL1`) be promoted to a therapeutic claim? | No finding survived. `ACSL1` demoted to marker; `NAMPT` prior-art-blocked. See `FINDING_EXECUTION_PHASE.md`, `EXHAUSTION.md`. |
| V3 | What node or state transition in the cross-autoimmune lipid-lysosomal myeloid module is a druggable intervention point? | 170+ waves; no candidate met the Definition of Done. See `PLAN_V3.md`, `REFRAME_V3.md`, `LAB_NOTEBOOK_V3.md`. |
| V4 | Same question, under stricter prior-art and tiering rulebooks. | Reorganized knowledge into `knowledge/` + `meta/`; tiered triage. |
| V5 | Tiered continuation on concrete leads (pregnancy axis, MIF/CD74 resolution, longitudinal dimension). | Produced concrete leads but no Tier 4 claim. |
| V6-V7 | APC response architecture as cross-disease treatment-response stratifier. | Narrow IBD response-monitoring signal survived; broad APC rule killed. |
| V8-V12 | MS-centered multi-axis mechanism map and axis-disagreement matrix. | Matrix completed; UC/Crohn/MS genetics and treatment-response disagreements became priority. |
| V13 | OpenGWAS-backed first-pass cross-trait colocalization for MS/UC/Crohn shared loci. | Four high-H4 regions identified; MHC overlaps mostly ruled distinct causal variants. |
| V14 | Robust workup of confirmed shared loci. | Tooling and LDSC reference panel provisioned; bounded SuSiE-coloc supports chr1 UC and chr10 Crohn loci. Active. |
| V15 | Causal-gene and effect-direction workup for the SuSiE-surviving loci. | chr1 MS-UC points to concordant `GPR25` blood eQTL risk direction but weak cell-state/druggability support; chr10 MS-Crohn points to `ZMIZ1` with opposite disease-effect signs and no transfer-ready intervention claim; chr5/PTGER4 is mixed shared/distinct signal; chr17/STAT3-STAT5 is downgraded. See `GENETICS_LOCI_WORKUP_V15.md` and `GENETICS_AXIS_V15_NEXT_TIER_SUSIE_ADDENDUM.md`. |
| V16 | eQTL-grounded allele-direction workup of live loci. | `GPR25` direction corrected to protective higher expression; `ZMIZ1` confirmed as opposite-direction MS/Crohn decoupling locus; `PTGER4` confirmed signal-conflicted. See `GENETICS_EQTL_WORKUP_V16.md`. |
| V17 | GPR25 mechanism workup and lead consolidation. | `GPR25` survives as a Tier 1 genetics-to-lymphocyte-trafficking lead, not an intervention-grade finding. Full eQTLGen candidate extraction and bounded eQTL-coloc keep `GPR25` alive but reopen `KIF21B` as a competing causal gene; local MS CNS atlases do not support a lesion-cell GPR25 mechanism, and h5ad scans make KIF21B a stronger expression-supported competitor but weak direct target. See `GENETICS_GPR25_WORKUP_V17.md`, `KIF21B_SCOUT_V17.md`, `SOURCES_V17.md`, and `GPR25_KIF21B_EXPERIMENTAL_DESIGN_V17.md`. |
| V18 | Data-source acquisition and access triage. | Acquired public OneK1K top eQTL, DICE significant eQTL/mean expression, eQTL Catalogue targeted chr1 extract, IUPHAR, and GPCRdb sources. Public genotype-linked immune eQTL sources favor `KIF21B` context (`14` OneK1K target hits and `1` DICE NK hit, all KIF21B) but do not resolve GPR25 protein/genotype causality. See `meta/DATA_ACQUISITION_PLAN_V18.md`. |
| V19 | First-principles druggability and causal-gene re-evaluation of chr1. | Dense QTD000021 eQTL Catalogue coloc supports `KIF21B` as a serious causal-gene candidate (MS/eQTL PP.H4 `0.874879034973956`, UC/eQTL PP.H4 `0.868660082128031`), and exact shared credible-set variants show risk lowers KIF21B expression. Druggability was revised: `GPR25` is structurally plausible but agonism-immature; `KIF21B` is structurally ligandable but likely wrong-direction for inhibition. See `GENETICS_CHR1_REEVALUATION_V19.md`. |
| V20 | Next-tier lead generation across the full landscape. | Produced `LEAD_SLATE_V20.md` and `analysis/v20_lead_slate/lead_slate_v20.tsv`: 13 pre-vetted candidates across four workstreams, with 5 promising follow-ups, 2 hard-target real-biology findings, and 6 negative/not-now entries. Top lead is dynamic APC/HLA-II treatment-response monitoring; next genetics follow-ups are chr14 `ZFP36L1` and chr2 `REL/PUS10/USP34`. |
| V21 | Genome-wide genetic-correlation backdrop and queued next-tier locus vetting. | Used the verified LDSC panel to compute rg for MS vs UC, Crohn, RA, and SLE; UC is the strongest tested genetic comparator for MS. Bounded SuSiE-coloc parked chr14 `ZFP36L1` as suggestive and closed chr2 `REL/PUS10/USP34` as not-now. See `GENETIC_CORRELATION_BACKDROP_V21.md` and `LEAD_SLATE_V21.md`. |

`FINDING.md` documents the (since-demoted) `ACSL1` target hypothesis from an
earlier phase and is retained for the historical trace.

## Reproducibility

Each phase has its own entry point at the repository root:

```bash
./run_analysis.sh            # V1
./run_therapeutic_analysis.sh # ACSL1-phase analysis
./run_v2_analysis.sh         # V2
./run_v3_analysis.sh         # V3
```

Each script provisions a virtual environment, installs pinned dependencies,
downloads public inputs, records SHA-256 hashes, and runs the phase analysis.
Expected input URLs, sizes, and hashes are recorded in the per-phase data
manifests under `data/derived*/` and `data/manifest.tsv`.

Python environments currently used:

- `.venv`: Python 3.13 genetics tooling, including PyPI `ldsc` 2.0.1.
- `.venv_v3_py312`: local TF-IDF knowledge index tooling.

R genetics tooling:

- R 4.6.0
- `coloc` 5.2.3
- `susieR` 0.14.2

V17 reproducibility entry points:

- `scripts/v17_extract_eqtlgen_chr1_candidates.sh` regenerates the streamed
  full-eQTLGen chr1 candidate-gene extract used in V17.
- `scripts/v17_scan_h5ad_gpr25_kif21b.py` regenerates the local h5ad
  GPR25/KIF21B/CXCL17 expression tables under
  `analysis/v17_gpr25_mechanism/`.
- `scripts/v17_summarize_gpr25_checkpoint.py` prints the key V17 numeric
  checkpoint values from saved TSV outputs.

V18 reproducibility entry point:

- `scripts/v18_smoke_test_acquired_sources.py` regenerates target-gene smoke
  summaries from acquired OneK1K and DICE files.

V19 reproducibility entry point:

- `scripts/v19_chr1_reanalysis.py` verifies V18 source checksums, aligns the
  QTD000021 KIF21B extract to the saved V14 MS/UC chr1 disease sumstats, runs
  coloc.abf, and writes the V19 chr1 re-analysis summary under
  `analysis/v19_chr1_druggability/`.

V20 reproducibility entry point:

- `scripts/v20_generate_lead_slate.py` consolidates V13-V19 evidence into the
  ranked next-tier slate under `analysis/v20_lead_slate/` and supports
  `LEAD_SLATE_V20.md`.

V21 reproducibility entry points:

- `scripts/v21_ldsc_core_backdrop.py` consumes local OpenGWAS VCFs under
  `data/raw/opengwas_v21/`, converts them to HapMap3 plain TSV summary
  statistics, runs `munge_sumstats.py`, and runs LDSC rg against the verified
  European reference panel.
- `scripts/v21_next_tier_locus_susie.py` regenerates bounded SuSiE-coloc for
  the chr14 `ZFP36L1` and chr2 `REL/PUS10/USP34` follow-up loci under
  `analysis/v21_next_tier_loci/`.

LDSC reference panel:

- Working DOI-stable source: Zenodo `10.5281/zenodo.14993076`
- Download URL: `https://zenodo.org/records/14993076/files/eur_w_ld_chr.tgz`
- Local archive: `data/raw/ldsc_reference/eur_w_ld_chr.tgz`
- Extracted panel: `data/raw/ldsc_reference/eur_w_ld_chr/`
- Archive MD5: `76c1890c8cf22d99d05c6707cc8441b4`
- Archive SHA-256:
  `0ac97e1c128ca5ba5dfd5858c736741b1544434924248027ae73725a9773311a`
- `w_hm3.snplist` is included in the extracted archive and has `1217312`
  lines including header.
- Reference-panel smoke test passed with `munge_sumstats.py` and `ldsc.py --h2`;
  details are in `meta/PROVISIONING_REPORT.md`.
- Provisioning-only verification on 2026-06-06 confirmed the archive and
  `w_hm3.snplist` checksums match and a parse smoke test passes; see
  `meta/LDSC_PANEL_STATUS.md`.

V24 data-scout entry points:

- `DATA_SCOUT_V24.md` is the current treatment-response cohort acquisition
  verdict for the APC/HLA-II monitoring lead.
- `analysis/v24_data_scout/v24_search_log.tsv` records searched source types,
  queries, hit counts/results, and inspection outcomes.
- `analysis/v24_data_scout/v24_candidate_inventory.tsv` records the ranked
  candidate sources and access-tier triage.
- V24 conclusion: no clean public ready-to-run n>=30 fresh MS DMT
  transcriptomic validation cohort was found. The public ready-to-run well is
  effectively dry for primary validation, but low-barrier data are not dry:
  the best next cohort is Gafson et al. 2018 DMF PBMC RNA-seq (PMID
  `30283812`, DOI `10.1212/nxi.0000000000000470`), requiring author/data
  request for processed counts and NEDA-4 sample labels. `GSE130478/GSE130491`
  are open but need response-label mapping; `GSE85034_MTX` is a local,
  secondary psoriasis stress test only.

V25 model-build entry points:

- `MODEL_DESIGN_V25.md` records the architecture choice and why V25 downscoped
  to a bounded empirical Mixscale module-response model.
- `analysis/v25_immune_state_model/DATA_INVENTORY_V25.tsv` inventories the
  data substrates considered for model building.
- `analysis/v25_immune_state_model/TRAIN_HELDOUT_SPLIT_V25.tsv` is the
  immutable held-out split, committed before validation in commit `0bc726e`.
- `scripts/v25_build_bounded_immune_state_model.py` rebuilds the bounded model
  and held-out validation outputs.
- `MODEL_CARD_V25.md` is the final V25 deliverable. Verdict: V25 did not
  achieve a reliable immune-state simulator. Held-out direction accuracy was
  `0.542` across `24` module predictions, calibration was weak, and the model
  must abstain on `KIF21B/GPR25`, `ZMIZ1`, patient response, single-cell
  compartments, and unseen pathways.

V26 deep-structure entry points:

- `V26_QUEUE.md` records the V26 self-driving queue and completed workstream
  statuses.
- `scripts/v26_deep_structure_analysis.py` rebuilds the held-data modality
  manifest, module matrices, latent-axis tests, dependency tests, invariant
  tests, and stalled-lead reread tables under `analysis/v26_deep_structure/`.
- `DEEP_STRUCTURE_V26.md` is the final V26 deliverable. Verdict: V26 found a
  supported shared APC remodeling structure, not a cure-class target and not a
  load-bearing invariant. Supported latent pairings were treatment
  pharmacodynamics vs cross-disease h5ad cell state (cosine `0.934`, BH q
  `0.010`) and h5ad cell state vs cross-disease summary (cosine `0.879`, BH q
  `0.017`). The strongest replicated dependency was `hla_ii_apc` with
  `mif_cd74_receptor_state` across four modalities. Zero invariants passed the
  stricter V26 invariant gate.

## Honest Scope

This is a reproducible computational prioritization, not a validated mechanism,
a patient recommendation, or evidence of clinical efficacy. The analyses
establish associations and triage hypotheses in public human-tissue data; they
do not infer viral causation, cell-cell interaction without spatial/protein
follow-up, or therapeutic benefit.
