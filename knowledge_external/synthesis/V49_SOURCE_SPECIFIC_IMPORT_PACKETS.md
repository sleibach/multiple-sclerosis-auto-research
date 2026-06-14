# V49 Source-Specific Import Packets

Status: future-intake planning only. These packets define narrow source-import routes for the high-actionability insufficient-overlap rows from `V49_INSUFFICIENT_OVERLAP_TRIAGE.md`. They do not add external claims and do not change any grounded finding.

Boundary: source-specific import can create future external records. It cannot create project evidence. Any imported source still needs a later grounded comparison before it can affect a finding.

## Why These Three

The V49 insufficient-overlap triage identified three source-specific import routes where the current row is too broad but a concrete future import is feasible:

- `ZMIZ1 opposite-direction MS/Crohn decoupling` currently has only DisGeNET resource metadata.
- `chr1 KIF21B/GPR25 locus resolves to real biology but hard target` currently has only GWAS Catalog resource metadata.
- `Coupled APC remodeling architecture` currently has only MSGD resource metadata.

## Import Packets

| packet | grounded finding | required source fields | acceptance gate | first grounded check |
|---|---|---|---|---|
| `V49_IMPORT_ZMIZ1_DIRECTION` | ZMIZ1 opposite-direction MS/Crohn decoupling | gene; disease/trait; source database/version/date; assertion type; variant if present; direction/effect if present; source publication or dataset locator | Must address ZMIZ1 specifically and include direction/effect or a route to recover it; a generic gene-disease association is not enough. | Compare imported ZMIZ1 direction/effect fields to the project's MS/Crohn opposite-direction finding. |
| `V49_IMPORT_CHR1_KIF21B_GPR25_SIGNAL` | chr1 KIF21B/GPR25 locus resolves to real biology but hard target | trait; variant; effect allele; beta/OR/direction if available; p-value; mapped gene; study accession; publication; source version/date; QTL/coloc locator if available | Must be signal-specific and preserve direction or enough fields to derive direction; catalog-level locus existence is not enough. | Compare imported signal fields to V19's causal-gene, wrong-direction, and tractability conclusions. |
| `V49_IMPORT_COUPLED_APC_AXIS_RECORDS` | Coupled APC remodeling architecture | gene/module; disease context; cell type/compartment if present; pathway/interaction assertion; source publication/database version; direction/state if present; source date | Must contain source-specific information about the CD74/MIF/HLA/IFN-APC axis, cell state, or interaction; simple database presence is not enough. | Compare imported axis records to V26 coupled-axis loadings and V23 compartment localization. |

## Rejection Rules

- Reject or park records that are only broad gene listings.
- Reject or park records missing source version/date when the source is a mutable database.
- Reject or park records that cannot preserve or recover direction for direction-dependent findings.
- Do not add relationship-matrix rows until the imported record has a source, class marker, not-grounded marker, and source-specific overlap review.

## Next Safe Action

Use these packets as checklists during future source intake. They are intentionally narrow: if a candidate source does not satisfy the packet's acceptance gate, it should remain out of the convergence matrix rather than become false corroboration.

