# CONVERGENCE_CHECK_V21_01

Timestamp: 2026-06-06 13:58 CEST

## What V21 Tested

V21 asked whether the newly verified LDSC reference panel changes the genetic
backdrop for the MS-centered map, and whether the two V20 queued genetics
regions produce a cleaner next therapeutic lead than chr1.

## Convergence

The genome-wide backdrop supports the existing map rather than overturning it:

- UC is the strongest tested genetic comparator for MS (`rg = 0.3342`).
- Crohn is positive but weaker (`rg = 0.1675`).
- RA is not genetically far from MS (`rg = 0.1692`), reinforcing that the RA
  divergence is specific to blood APC treatment-response architecture rather
  than global autoimmunity distance.
- SLE remains plausible but caveated because its h2 intercept is high.

The queued loci did not converge into a next therapeutic target:

- chr14 `ZFP36L1` is suggestive (`PP.H4 = 0.6877`) but below robust threshold
  and lacks allele-aligned direction.
- chr2 `REL/PUS10/USP34` failed bounded multi-signal disease-coloc.

## Decision

No V21 locus clears the chr1 bar. The frontier shifts back to:

1. Dynamic APC/HLA-II treatment-response monitoring as the top actionable
   biomarker/mechanism lead.
2. Extending the LDSC backdrop to remaining map diseases for context.
3. Keeping chr1 in wet-lab/controlled-data handoff status.

## Methodological Caveat

MHC-excluded raw sumstats were generated for MS/UC/Crohn, but the active LDSC
reference panel has no chr6:25-34 Mb SNPs after merge. The identical full and
MHC-excluded estimates should be interpreted as reference-panel behavior, not
as a separate sensitivity from an MHC-containing regression panel.
