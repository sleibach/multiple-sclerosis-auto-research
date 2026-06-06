# KIF21B

Status: alive Tier 1 competing causal-gene candidate  
Last updated: 2026-06-06  
Primary evidence files: `../../GENETICS_GPR25_WORKUP_V17.md`,
`../../KIF21B_SCOUT_V17.md`

## Current Verdict

`KIF21B` is reopened as a competing causal-gene candidate at the MS-UC chr1
shared locus. It prevents an exclusive `GPR25` causal-gene claim.

## Evidence

- V17 eQTLGen full-file extraction: all 11 MS-UC shared credible-set variants
  have `KIF21B` eQTL evidence with expression-up protective direction for both
  MS and UC.
- V17 bounded disease-vs-eQTL SuSiE-coloc:
  - MS/eQTL max PP.H4 `0.956099`;
  - UC/eQTL max PP.H4 `0.963951`.
- Local MS CNS atlas `GSE301908_sn_all.rds` contains measurable `KIF21B`
  expression across several major clusters, including lymphocytes, microglia,
  astrocytes, and neurons.
- V17 h5ad atlas scans found `KIF21B` more consistently detectable than GPR25
  across gut, IBD myeloid, RA blood, Sjogren salivary, and psoriasis skin
  atlases.
- Cell-type breakdown found KIF21B detection in psoriasis helper T cells
  `10.17%`, psoriasis Tregs `8.79%`, psoriasis cytotoxic T cells `7.38%`, IBD
  T cells `4.09%`, and Sjogren effector CD8 T cells `3.55%`.
- V18 acquired-source triage:
  - OneK1K public top-eQTL summaries produced `14` target hits, all `KIF21B`;
  - DICE public significant eQTLs produced `1` target hit, `KIF21B` in NK
    cells;
  - eQTL Catalogue QTD000021 targeted chr1 extract produced `8,416` target
    rows, all `KIF21B`;
  - DICE mean expression showed KIF21B high across immune subsets.
- Fast overlap check found no exact match between the OneK1K/DICE
  top/significant KIF21B hits and the V17 shared MS-UC credible-set variants;
  the closest OneK1K hits were `17,230 bp` and `21,012 bp` away.

## Limits

- `GPR25` remains stronger in the disease-shared eQTL block by eQTLGen Z-score.
- `KIF21B` mechanism and druggability were not worked up in V17.
- No intervention claim is made.
- V17 scout found poor direct druggability: no ChEMBL target, no ChEMBL
  mechanisms, no ClinicalTrials.gov studies, and no specific autoimmune
  intervention patent in inspected top Google Patents hits.
- Literature search confirms KIF21B is prior art as an MS and IBD
  susceptibility locus; any V17/V18 contribution would be causal-gene
  resolution and cell-state mechanism, not locus novelty.
- Public top/significant QTL summaries are not sufficient for exclusive
  causal-gene assignment; controlled full-summary or individual-level data is
  still needed.
- The V18 public KIF21B hits are context-strengthening, not causal resolution.

## Next Required Test

Run cell-type-resolved expression and perturbation checks for `KIF21B` in the
same immune-cell datasets used to test `GPR25`; decide whether the chr1 locus is
better explained by lymphocyte trafficking (`GPR25`) or intracellular
cytoskeletal/transport biology (`KIF21B`). If `KIF21B` wins, expect a mechanism
or biomarker contribution rather than direct drug repositioning.
