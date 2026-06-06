# MILESTONE_2 - Actual Hour-4 Checkpoint

Timestamp: 2026-05-26 22:41 UTC

Elapsed wall time from V3 start: ~4.0 hours.

## Milestone Requirement

Hour 4 target from the user prompt:

- Cross-disease shared genes and shared cell states enumerated with statistics.
- First-pass central-node candidates ranked.
- Foundation-model perturbation predictions initiated.

Status: partially met. The statistical enumeration and ranking were completed.
Foundation-model routes were provisioned, but the strongest interpretable
foundation-model channel is weak and must not be overclaimed.

## Executed Evidence Channels

### Cross-Disease Single-Cell / Spatial Expression

Script:

- `scripts/v3_broad_h5ad_gene_discovery.py`

Output directory:

- `results_v3/broad_h5ad_gene_discovery/`

Statistics:

- 17 local h5ad disease/compartment analyses.
- 282,630 donor-level gene contrasts.
- 25,176 ranked genes.

Diseases and compartments directly included in this broad pass:

- Crohn disease: colon myeloid, epithelial, stromal.
- Ulcerative colitis: colon myeloid, epithelial, stromal.
- Psoriasis: skin APC, keratinocyte, stromal.
- Sjogren syndrome: salivary gland APC, epithelial, stromal.
- Type 1 diabetes: pancreatic beta, ductal, acinar, stellate, endothelial.
- MS anchor: GSE111972 white-matter microglia/macrophage gene-level statistics
  imported from the existing V3 matrix.

Important limitation: RA synovium/macrophage atlas `E-MTAB-8322` remains blocked
by repeated EBI FTP/HTTPS timeouts, so RA is represented only by earlier
literature/database lanes, not by local h5ad pseudobulk in this broad pass.

### First-Pass Ranked Candidates

Top broad-expression genes by the current ranking:

- `CBX3`: positive in 4 diseases / 10 compartments; MS white-matter delta
  0.351 log2-CPM, Hedges g 1.146, p=0.0166. Main weakness: chromatin/nuclear
  marker with unclear lipid-lysosomal or selective intervention mechanism.
- `IFITM3`: positive in 5 diseases / 11 compartments; best local broad marker
  and strongest Geneformer deletion signal, but MS white-matter direction is
  negative (delta -0.495, p=0.297), making it unsuitable as an MS-anchored
  central node.
- `IFITM2`: similar to `IFITM3`, with negative MS white-matter direction.
- `TIMP1`, `PSME2`, `CFB`, `MMP7`: broad tissue-stress / IFN / complement /
  remodeling markers, not yet druggable central nodes.

Top lipid-lysosomal-neighborhood candidates:

- `CHI3L1`: UC/Crohn/T1D tissue-injury compartments plus MS-positive
  white-matter signal (delta 2.007, Hedges g 1.347, p=0.00461), but heavy MS
  biomarker/prior-art burden and weak/mixed Geneformer support.
- `LTA4H`: MS-positive and Crohn/UC myeloid plus T1D acinar positive
  expression; demoted because Geneformer deletion support was zero by the
  posthoc rule and LTA4H/LTB4 inhibitor prior art is blocking.
- `FABP5`: MS-positive and psoriasis/UC local signals with broader existing
  matrix support, but directionally conflicted in local UC and likely
  prior-arted in autoimmunity/psoriasis/EAE. Requires focused scrutiny.
- `MSR1`: MS-positive in imported white-matter statistics and positive in the
  existing matrix across Crohn/Sjogren/UC/lupus nephritis/psoriasis, but the
  direct h5ad broad pass produced no local positive contrasts. Requires focused
  scrutiny before any target claim.
- `SCARB2`: MS-positive imported statistic, but local broad support is weak /
  negative. Retained only as a lysosomal receptor comparator.

### Foundation-Model Status

Arc State:

- Official `adata_real.h5ad` is now readable locally, but feature identifiers
  are numeric strings and `adata.var` has no gene-symbol columns.
- Consequence: State can be used for feature-agnostic perturbation calibration
  but cannot currently support named-gene module scoring or named-gene
  perturbation claims in this workspace.

Geneformer:

- Real local named-gene route completed with official `ctheodoris/Geneformer`
  V2-104M assets, revision `04c2b2e84da7c0f385c3f9ad8f3ec24bab6650e5`.
- Candidate deletion screen output:
  `results_v3/geneformer_candidate_delete/`.
- `IFITM3` had the strongest model-normalization signal
  (8 contexts, 45 disease cells with token, mean cosine shift 0.000189,
  mean projection shift 0.0239, support contexts 3), but fails MS-direction
  anchoring.
- `LTA4H` was weak/negative (4 contexts, 6 disease cells with token, mean
  cosine shift -0.000289, mean projection shift -0.00278, support contexts 0).
- `CHI3L1` was mixed/weak (support contexts 1).

Interpretation: foundation-model predictions have been initiated and are
traceable, but they currently function as a veto/triage channel rather than as
positive DoD-grade perturbation support.

## Current Demotions

The following are not acceptable V3 central nodes as of hour 4:

- ACSL1: demoted in V2 after module-adjusted test.
- CD74/HLA/IFI30/IFN antigen-presentation axis: real broad autoimmune state,
  but too generic/prior-arted and currently better as stratification biology.
- LIPA: marker of lipid-lysosomal epithelial/ductal/keratinocyte stress; not a
  stable myeloid central node.
- OSM/OSMR: strong IBD/skin comparator and tissue-continuation axis, but weak
  MS anchoring and direct prior art.
- Complement/C1q: strong in specific compartments/diseases but inconsistent
  locally, disease-specific, and prior-arted.
- LTA4H: attractive enzyme from expression screen, but fails the current
  Geneformer deletion gate and is prior-arted.

## Convergence State

The broad track says the shared signal is real but mostly separates into:

1. Generic antiviral/IFN/stress programs (`IFITM2/3`, `PSME1/2`, HLA/IFN
   remnants).
2. Tissue-remodeling injury programs (`CHI3L1`, `TIMP1`, `MMP7`).
3. Lipid-lysosomal receptor/enzyme candidates with weaker and more conflicted
   evidence (`FABP5`, `MSR1`, `SCARB2`, `GPNMB`, `LIPA`, `LTA4H`).

The foundation-model track agrees only weakly: it supports IFITM3 more than the
lipid candidates, but IFITM3 is not MS-positive in the current MS anchor.

The genetics/druggability/prior-art tracks so far veto many attractive
expression hits because they are either generic immune-state markers or already
claimed in MS/IBD/psoriasis/RA patent and literature space.

## Next Forcing Question

The next two-hour block should not rescue a demoted candidate by relaxing
criteria. It should answer:

Which lipid-lysosomal receptor/effector has the best combination of

- MS-positive evidence,
- cross-disease replication in at least three directly analyzed tissues,
- named-gene foundation-model support or real perturbation-data reversal,
- druggability/selectivity,
- and no blocking prior art for the specific autoimmune use?

Priority candidates for the hour-4 to hour-6 block:

- `FABP5`: strongest local MS-positive lipid-neighborhood signal but likely
  prior-arted and directionally conflicted.
- `MSR1`: broad scavenger-receptor biology and existing matrix breadth, but
  direct h5ad local support is missing.
- `SCARB2`: lysosomal receptor with MS signal; needs breadth and druggability
  scrutiny.
- `LGALS1/LGALS3` and related glycan checkpoint biology: possible cross-disease
  immune/tissue interface; requires prior-art and local-data test before
  elevation.

Open operational route:

- Await wave-7 target-scout subagent result.
- Patch the State feature-identity blocker documentation.
- Run a focused local/perturbation/prior-art triage for `FABP5`, `MSR1`,
  `SCARB2`, and glycan-checkpoint candidates.

