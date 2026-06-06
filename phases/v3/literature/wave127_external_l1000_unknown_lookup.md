# Wave127 External Lookup - Recurrent Unknown L1000 Hits

Timestamp: 2026-05-28 10:00 CEST

## Purpose

Wave126 left recurrent L1000 reversal hits with unresolved or weakly resolved
targets. Before spending more effort on this branch, I checked whether the
highest-scoring unknowns had obvious external target annotations.

## Queries

- `"BFOWTYGBWYCXKR"`
- `"GNLIZSFOCYRQDY" "BRD-K35024477"`
- `"BRD-K05197617"`
- `"BRD-K35024477"`

Database/tool:

- Web search via the session browser.

## Results

### BRD-K05197617

Local Wave27:

- LINCS alias: unresolved BRD structure.
- SMILES/InChIKey present:
  `BFOWTYGBWYCXKR-UHFFFAOYSA-N`.
- Wave27 call: `NO_GO_UNRESOLVED`.

External spot-check:

- A BMC Genomic Data table using L1000FWD lists `BRD-K05197617` with MOA
  `EGFR inhibitor`.
- A PMC copy of the same article reports the same table.
- A Frontiers review-like article also repeats that `BRD-K05197617` is an EGFR
  inhibitor.

Interpretation:

- Even if the EGFR inhibitor annotation is accepted, the route does not reopen:
  EGFR inhibition is an oncology/growth-factor route, not a specific
  lipid-lysosomal myeloid intervention, and the L1000 hit remains a generic
  transcriptomic reversal without autoimmune target-resolution.

Sources:

- https://bmcgenomdata.biomedcentral.com/articles/10.1186/s12863-022-01097-z/tables/2
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9667687/
- https://www.frontiersin.org/journals/oncology/articles/10.3389/fonc.2023.1183766/full

### BRD-K35024477

Local Wave27:

- LINCS alias: unresolved BRD structure.
- SMILES/InChIKey present:
  `GNLIZSFOCYRQDY-CUMRGQLISA-N`.
- Wave27 call: `NO_GO_UNRESOLVED`.

External spot-check:

- Search results found an OCTAD compound-cluster PDF containing
  `BRD-K35024477`, but not a clear target or autoimmune-relevant mechanism.

Interpretation:

- No external target/MOA sufficient for reopening was identified.

Source:

- https://octad.org/static/octad_compounds_clusters.pdf

## Decision

Do not reopen the recurrent unknown L1000 branch.

Reason:

- Locally resolved recurrent unknowns map to purine/cAMP, prostanoid,
  polyphenol/electrophile, Aurora/cell-cycle, or unresolved structures.
- External spot-check does not provide a selective autoimmune target. The only
  new plausible annotation (`BRD-K05197617` as EGFR inhibitor) shifts the route
  into a broad oncology/growth-factor bucket, not into a V3 therapeutic finding.
