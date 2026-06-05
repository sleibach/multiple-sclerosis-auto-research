# CONVERGENCE_CHECK_V8_01

Timestamp: 2026-05-29 00:20:26 CEST

## Scope

This checkpoint covers the first V8 map build after the methodology lock. The locked files are `ROADMAP_V8.md` and `MAP_METHODOLOGY_V8.md`, committed in `9c2e548` before placement generation. Current generated map artifacts live under `analysis/v8_map/`.

## Current Axis Coverage

Populated axes:

| Axis | Status | Supported or robust placements | Main limitation |
| --- | --- | ---: | --- |
| axis_01_ifn_apc | populated from V3-V7 local evidence | 8/12 | Mostly cross-sectional tissue/blood evidence; SLE, MG, AS unresolved locally. |
| axis_02_genetics | populated as proxy plus UC/Crohn LDSC upgrade | 2/12 | UC/Crohn have verified Yang et al. 2021 LDSC evidence; other diseases remain OpenTargets target-overlap proxies. |
| axis_03_microbiome | populated from literature-anchored evidence rows | 0/12 | Literature-derived, not yet harmonized as quantitative cross-disease microbiome matrix; all current placements are provisional. |
| axis_04_lipid_lysosomal | populated from V3-V7 local evidence | 2/12 | Cross-sectional module evidence only; many compartments differ. |
| axis_07_treatment_response | populated from V7 validation ledger | 3/12 | Treatment-response evidence is deep for IBD/RA only; MS IFN-beta derivation evidence intentionally not counted as held-out map validation yet. |

Merged outputs:

- `analysis/v8_map/evidence_registry.tsv`: 70 evidence rows.
- `analysis/v8_map/placement_matrix.tsv`: 60 placements.
- `analysis/v8_map/axis_population_summary.tsv`: axis-level coverage summary.
- `analysis/v8_map/MAP_MERGE_REPORT.md`: generated merge report.

## Current Robust Core

1. **MS versus RA diverges on the IFN/APC antigen-presentation axis in blood/APC treatment-response evidence.**
   - Placement: RA `far`, `supported`, medium confidence on `axis_01_ifn_apc`; RA `far`, `supported`, medium confidence on `axis_07_treatment_response`.
   - Evidence basis: V3 blood myeloid/APC divergence plus V7 independent treatment-response failures in RA blood cohorts.
   - Caveat: this does **not** prove RA synovium is far from MS. The compartment label is essential.

2. **UC and Crohn are near MS on mucosal IFN/APC treatment-dynamic behavior, but not as a pretreatment stratifier.**
   - Placement: Crohn `near`, `supported` on treatment response; UC `contradictory`, `supported` because early delta validates while a baseline mucosal rule fails.
   - Evidence basis: V7 locked-rule ledger and HYP_V7_001 refinement.
   - Interpretation: this is more likely a mucosal-healing / response-monitoring axis than a universal autoimmune response predictor.

3. **MS is provisionally nearer to IBD and T1D than to RA on the microbiome axis under the current criterion of longitudinal gut microbial-immune/metabolite evidence.**
   - Placement: Crohn, UC, and T1D `near`, `provisional`, medium confidence; RA `intermediate`, `provisional`, low confidence.
   - Caveat: current microbiome evidence is literature anchored and needs a quantitative cross-disease matrix before this can become supported-grade.

## Contradictions Preserved

- **UC treatment response is not a clean near placement.** Dynamic early IFN/APC downshift passes in two mucosal anti-TNF/vedolizumab contexts, while baseline UC infliximab prediction fails in GSE12251. The map preserves this as `contradictory`, not averaged.
- **RA is not globally far from MS.** RA is far on blood IFN/APC treatment-response behavior, intermediate on genetics proxy, and intermediate on microbiome. This supports the V8 premise that disease similarity is axis-specific.
- **Genetics only partially reproduces gut-disease proximity.** UC is upgraded to `near/supported` and Crohn to `intermediate/supported` using verified Yang et al. 2021 LDSC evidence, but the remaining diseases still rely on target-overlap proxies.

## Methodological Risks

- The genetics axis is currently below V8 desired quality outside UC/Crohn. It is retained as provisional for most diseases because the methodology permits thin axes with explicit low confidence.
- The microbiome axis uses curated literature rows and verified sources, but not yet a single harmonized effect-size pipeline. It does not yet answer the MS-gut question at supported grade.
- Local transcriptomic axes inherit V3-V7 dataset selection. The matrix-wide correction plan is specified, but current local placement generation uses pre-existing pass/fail summaries, not raw re-analysis with a full multiple-testing correction across all cells.

## Next Forcing Question

Can the genetics axis be upgraded from OpenTargets overlap proxy to true genome-wide similarity or causal anchoring? If yes, test whether MS aligns genetically more with IBD/T1D/psoriasis/SLE or whether the IFN/APC partition is mostly transcriptomic/compartmental rather than genetic.

Immediate next actions:

1. Search for accessible cross-autoimmune GWAS genetic-correlation resources or summary-statistic-derived matrices.
2. Populate complement / innate-effector and infectious-trigger axes using literature plus any existing local artifacts.
3. Build `MS_MECHANISM_MAP_V8.md` incrementally only after priority axes are populated to supported/robust where feasible.
