# CONVERGENCE_CHECK_V18_01

Date: 2026-06-06

## Question

Did V18 acquisition find self-acquirable public data that resolves the
`GPR25` versus `KIF21B` chr1 MS-UC causal-gene ambiguity?

## Answer

No. V18 acquired useful public genotype-linked immune eQTL/expression data, but
it does not fully resolve causality. The acquired public layers strengthen
`KIF21B` context and do not upgrade `GPR25`.

## Acquired Evidence

- OneK1K top-eQTL summary zip acquired from Zenodo.
- DICE mean expression and significant immune-cell eQTL VCF panel acquired.
- eQTL Catalogue QTD000021 chr1 targeted remote-tabix extract acquired.
- IUPHAR and GPCRdb GPR25 resources acquired.

## Signal Direction

- OneK1K target-gene scan: `14` target hits, all `KIF21B`.
- DICE significant eQTL scan: `1` target hit, `KIF21B` in NK cells.
- eQTL Catalogue QTD000021 target extract: `8,416` target rows, all `KIF21B`.
- DICE mean expression: `KIF21B` is high across immune subsets; `GPR25` is low
  but nonzero in selected T/NK subsets.
- Fast overlap check: acquired OneK1K/DICE top/significant KIF21B variants do
  not exactly match the V17 shared credible-set variants. Two OneK1K hits are
  near the shared set (`17,230 bp` and `21,012 bp`); most are hundreds of kb
  away.

## Interpretation

The public Tier 1 acquisition pass shifts the practical next computational
question toward KIF21B variant overlap with the MS-UC shared credible set. It
does not prove KIF21B is causal, because:

- OneK1K top summaries are not all-variant colocalization.
- DICE significant VCFs miss non-significant or context-specific effects.
- The acquired top/significant KIF21B hits are not themselves the V17 shared
  credible-set variants.
- eQTL Catalogue QTD000021 metadata was not verified because REST metadata
  endpoints returned HTTP 500.
- No public MS protein/CITE-seq or genotype-linked CSF immune dataset was
  acquired.

## Next Forcing Question

Do dense QTD000021/eQTL Catalogue KIF21B variants colocalize with the V17
MS-UC shared credible set after metadata verification, or is controlled-access /
protein-level data still required?

The next session should not treat the OneK1K/DICE top-hit KIF21B evidence as
causal resolution. It should either run formal QTD000021 intersection/coloc
after metadata verification or move to the Tier 3 controlled/protein-data path.
