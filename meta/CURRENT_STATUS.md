# Current Status

Last updated: 2026-06-02 11:41 CEST

## Mission State

V9 is active. V8 produced the first MS-centered multi-axis autoimmune mechanism
map; V9 is deepening the highest-value gaps, especially the microbiome axis and
its relationship to the MS/IBD proximity signal.

Methodology integrity steps completed:

- V8 lock: `ROADMAP_V8.md`, `MAP_METHODOLOGY_V8.md`, git commit `9c2e548`.
- V9 lock: `ROADMAP_V9.md`, `MAP_METHODOLOGY_V9.md`, git commit `df7c7de`.

V9 explicitly states that a cure-class therapeutic claim is unlikely from one
public-data computational session. The current goal is robust axis upgrade and
mechanism/intervention hypothesis convergence without overclaiming.

## Current Deliverables

Core V8 map:

- `MS_MECHANISM_MAP_V8.md`
- `analysis/v8_map/evidence_registry.tsv`: 132 evidence rows.
- `analysis/v8_map/placement_matrix.tsv`: 120 disease-axis placements.

V9 active artifacts:

- `DATA_SEARCH_V9.md`
- `CONVERGENCE_CHECK_V9_01.md`
- `analysis/v9_microbiome/ms_primary_analysis/REPORT.md`
- `analysis/v9_microbiome/ibdmdb_subset_50_analysis/REPORT.md`
- `subagents/20260602_v9_microbiome_expansion_james.md`
- `subagents/20260602_v9_genetics_robustness_sartre.md`
- `subagents/20260602_v9_mechanism_intervention_nietzsche.md`

## Current Interpretation

The V8 map core still stands:

- RA diverges from MS on blood IFN/APC treatment-response architecture, not
  globally.
- IBD remains closest to MS on mucosal IFN/APC dynamics and tissue-repair /
  response-monitoring behavior.
- UC has the strongest verified genetic proximity to MS from the current
  encoded LDSC source; Crohn is intermediate.
- SLE remains a separate MS-adjacent hypothesis space around EBV/infectious
  trigger biology and possibly complement/pregnancy.

V9 microbiome update:

- MS now has primary-data microbiome evidence from processed stool `phyloseq`
  data: Bacteroides is higher in MS versus controls (Hedges g `0.716`, FDR
  `0.00108`; age/sex-adjusted FDR `0.00639`), Enterobacteriaceae/LPS proxy is
  lower (g `-0.569`, FDR `0.00836`; adjusted FDR `0.00510`), and
  Faecalibacterium is lower (unadjusted FDR `0.0557`; age/sex-adjusted FDR
  `0.0341`).
- IBDMDB/HMP2 106-profile independent-participant subset did not show any
  pre-specified taxonomic feature family at FDR `<0.10`.
- IBDMDB/HMP2 1,360-profile all-sample sensitivity showed naive repeated-sample
  taxonomic effects, but participant-clustered inference removed FDR support
  (CD Enterobacteriaceae p `0.00989`, FDR `0.119`).
- Therefore V9 does **not** support a simple microbiome-mediated explanation
  for MS/IBD proximity at the tested taxonomic-family level. MS/IBD proximity
  remains stronger on mucosal IFN/APC and repair/response-monitoring axes.

## Active Work

- No long-running local commands are active at this checkpoint.
- The genetics sidecar recommends a harmonized LDSC/HDL workflow with MHC
  exclusion before upgrading non-IBD genetics placements; automated OpenGWAS
  access is currently blocked by missing `OPENGWAS_JWT`.

## Highest-Value Next Actions

1. Use `MICROBIOME_AXIS_V9.md` as the current microbiome-axis synthesis.
2. Start `analysis/v9_genetics` download/munging only if OpenGWAS access or
   manual summary-stat paths become available.
3. Search for pathway/metabolite microbiome layers or independent MS
   microbiome replication; taxonomic family-level IBD overlap is not enough.
4. Keep the gut-barrier/metabolite/APC-plasticity intervention hypothesis
   conditional until pathway/metabolite or dynamic APC evidence supports it.

## Compute / Access Notes

- Working directory: `/Users/soeren.leibach/Projects/ms-auto-research`.
- `.venv/bin/python` works for V7-V9 pandas/numpy/scipy scripts.
- `.venv_v3_py312/bin/python` works for the local TF-IDF knowledge index.
- R `4.6.0` is installed. `phyloseq` and `vegan` are now installed in the
  Homebrew R site library after a long Bioconductor dependency build.
