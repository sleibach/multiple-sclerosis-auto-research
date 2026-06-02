# ROADMAP_V9

Started: 2026-06-02 11:18:00 CEST

## Honest DoD Framing

The user-specified cure-class Definition of Done is intentionally higher than
what public computational analysis can usually satisfy in a single session. V9
therefore treats "breakthrough" as a tiered outcome:

1. **Robust map upgrade**: at least one V8 provisional high-value axis is
   upgraded using primary data and reproducible code.
2. **Mechanism convergence**: the upgraded axis converges with at least two
   other axes already in the map.
3. **Intervention hypothesis**: the convergent mechanism yields a named,
   druggable or modifiable intervention point with explicit falsification path.

Only if all three occur will V9 write a cure-class `FINDING_V9.md`. Otherwise
V9 writes a rigorous upgraded map artifact and the remaining blockers.

## Starting State

V8 produced:

- `MS_MECHANISM_MAP_V8.md`
- `analysis/v8_map/placement_matrix.tsv`: 120 disease-axis placements.
- `analysis/v8_map/evidence_registry.tsv`: 132 evidence rows.

Strongest V8 features:

- RA diverges from MS on blood IFN/APC treatment-response architecture, not
  globally.
- IBD is near MS on mucosal IFN/APC and repair/response-monitoring axes.
- UC has verified genetic proximity to MS via LDSC; Crohn is intermediate.
- SLE is supported on infectious-trigger/EBV and provisional on complement /
  pregnancy.

Largest V8 weakness:

- The microbiome axis is literature-anchored and all microbiome placements are
  provisional after V8 hostile critique. V9 makes this the primary track.

## Track Allocation

### Track A - Primary-Data Microbiome Axis

Goal: replace V8 literature-only microbiome placements with a harmonized,
primary-data-derived cross-disease matrix for at least MS, IBD, RA, and T1D if
public data access permits.

Priority data sources to acquire or mine:

- MS gut microbiome case-control or longitudinal cohorts with abundance tables.
- HMP2/iHMP IBDMDB for Crohn/UC.
- RA gut microbiome cohorts with Prevotella/oral/gut-joint signatures.
- TEDDY or other T1D longitudinal microbiome summaries if raw access is
  feasible; otherwise use verified published effect tables only and keep grade
  capped.

Primary question:

Does MS quantitatively resemble IBD/T1D more than RA on microbial functional
pathways relevant to immune modulation: SCFA, bile acid, tryptophan, LPS,
mucin/barrier, IgA/bacterial translocation?

### Track B - Genetics Upgrade

Goal: upgrade V8 genetics beyond UC/Crohn using verified published genetic
correlation values or reproducible local summary-stat analysis where feasible.

Priority:

- RA, SLE, psoriasis, T1D, celiac, AITD, Sjogren, ankylosing spondylitis.
- Preserve the rule: target overlap alone cannot exceed provisional.

### Track C - Mechanism / Intervention Synthesis

Goal: only after Track A or B produces an upgraded result, ask whether the
result converges with V8 axes into a mechanistic intervention hypothesis.

Candidate mechanism families from V8:

- Gut microbial metabolite / barrier-to-CNS immune modulation.
- IFN/APC tissue repair-response monitoring.
- EBV/complement/IFN comparator biology in SLE.

No intervention claim is permitted until primary-data or genetics evidence
survives its own locked test.

## Immediate Deliverables

1. `MAP_METHODOLOGY_V9.md`: locked criteria for primary microbiome/genetics
   axis upgrades before data analysis.
2. `DATA_SEARCH_V9.md`: searched datasets, access status, and reasons for
   inclusion/exclusion.
3. V9 scripts and outputs under:
   - `scripts/v9_*`
   - `analysis/v9_*`
4. `CONVERGENCE_CHECK_V9_01.md` after the first data acquisition / feasibility
   pass.

## Pivot Criteria

- If raw microbiome data cannot be accessed within resource limits, pivot to
  verified published feature/effect tables and keep all placements provisional
  unless the source provides quantitative cross-disease comparable statistics.
- If MS microbiome data are unavailable or incompatible with IBD/RA/T1D data,
  produce a rigorous blocker and shift to genetics upgrade.
- If genetics sources do not provide disease-pair values including MS, use them
  only as background and do not upgrade placements.
- If Track A and Track B point in different directions, do not synthesize an
  intervention; log the contradiction and keep axes separate.

## Integrity Rules

- No new placement upgrade before `MAP_METHODOLOGY_V9.md` exists.
- No simulated microbiome data presented as real.
- No literature-only microbiome placement above `provisional`.
- No disease-level "near/far" collapse across axes.
- Every upgraded placement must trace to a file, accession, URL, statistic, and
  script.
