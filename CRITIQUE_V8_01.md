# CRITIQUE_V8_01

Timestamp: 2026-05-29 00:20-00:40 CEST

Subagent status: a critique subagent could not be spawned because the agent
thread limit was reached. This critique was performed locally.

## Findings

1. **Literature-only cells were overgraded.**
   - Problem: the first V8 pass marked several literature-only placements as
     `supported`, especially microbiome, T-cell/adaptive, complement, and SLE
     infectious-trigger cells.
   - Why this matters: `supported` in `MAP_METHODOLOGY_V8.md` requires more
     than a plausible review-backed mechanism; it requires cross-dataset or
     correction-aware evidence.
   - Fix applied: downgraded literature-only microbiome rows and most
     literature-only axes to `provisional`, preserving placement direction but
     lowering grade. Clinical-perturbation/local quantified rows remain
     supported where justified.

2. **The synthesis text lagged behind the matrix downgrade.**
   - Problem: `MS_MECHANISM_MAP_V8.md` still described SLE and microbiome
     neighborhoods as if they were supported after the matrix had been
     downgraded.
   - Fix applied: patched `scripts/v8_write_map_synthesis.py` so the generated
     synthesis now states that MS-gut proximity is provisional and that SLE is
     a hypothesis space rather than a robust neighborhood.

3. **The genetics axis remains underpowered.**
   - Problem: UC/Crohn have verified LDSC evidence, but most other diseases
     remain OpenTargets target-overlap proxies.
   - Consequence: the map cannot yet claim a genome-wide MS mechanism
     neighborhood. It can only say that UC/Crohn genetics are partially
     upgraded and that other diseases remain unresolved/provisional.
   - Required next fix: LDSC/HDL or curated published genetic-correlation
     values for RA, SLE, psoriasis, T1D, celiac, AITD, Sjogren, AS, and MG.

4. **Compartment confounding remains the main RA risk.**
   - Problem: the strongest RA divergence evidence is blood and treatment
     response. RA synovium may be closer to MS on some axes.
   - Current mitigation: all RA divergence language is constrained to blood
     IFN/APC treatment-response architecture. The map explicitly does not claim
     RA is globally far from MS.
   - Required next fix: add RA synovium single-cell/spatial data for IFN/APC,
     lipid-lysosomal, complement, and repair axes.

5. **Microbiome is still not a quantitative answer to the MS-gut question.**
   - Problem: current microbiome rows are verified-source literature rows, not
     harmonized metagenomic/metabolomic effect sizes.
   - Current mitigation: microbiome placements are provisional and the
     synthesis says they justify testing, not that they establish, MS-IBD/T1D
     proximity.
   - Required next fix: build a harmonized microbiome matrix from MS, IBD, RA,
     and T1D cohorts.

## Decision

The V8 map is acceptable as a reproducible checkpoint and hypothesis map, but
not as the final robust-standard V8 deliverable promised in the full task. The
next work block must prioritize upgrading genetics and microbiome, because
those are the highest-value axes and the current evidence standard is still
below the map's intended publication grade.
