# CONVERGENCE_CHECK_V17_01

Date: 2026-06-06

## Question

Does the MS-UC chr1 locus now support an intervention-grade `GPR25` hypothesis?

## Answer

No. `GPR25` remains alive, but the locus is not resolved to a single causal
gene and the mechanism is not yet intervention-grade.

## Converging Evidence

- The MS-UC chr1 locus remains genetically serious: V14/V15 SuSiE-coloc and
  V17 eQTL-coloc support shared disease/eQTL components.
- Full eQTLGen extraction shows `GPR25` is the strongest candidate in the
  disease-shared credible-set block.
- V16/V17 direction evidence indicates higher `GPR25` expression is protective
  for both MS and UC, so the therapeutic direction would be restoration or
  agonism rather than inhibition.
- GPR25 now has a plausible ligand axis, CXCL17-GPR25, with lymphocyte
  trafficking/tissue-residency biology.
- Local h5ad ligand-context scan found CXCL17 strongly in Sjogren salivary
  epithelial compartments, confirming that the script can recover tissue
  ligand expression where present.

## Diverging Evidence

- `KIF21B` also has high bounded MS/eQTL and UC/eQTL PP.H4 at the same locus.
- `KIF21B` is much more detectable than `GPR25` in the local single-cell/h5ad
  atlases.
- `GPR25` is absent from the local MS CNS/lesion feature sets and nearly absent
  in available gut, RA blood, Sjogren salivary, psoriasis skin, and IBD myeloid
  h5ad atlases.
- CXCL17 was absent or trace in the gut, RA blood, psoriasis skin, and IBD
  myeloid datasets checked, so ligand-context scanning did not rescue a broad
  MS-UC tissue mechanism.
- No obvious public MS CITE-seq/protein dataset was found for GPR25, CXCL17-
  GPR25, or KIF21B.

## Current Classification

- `GPR25`: Tier 1 genetics-to-lymphocyte-trafficking lead.
- `KIF21B`: Tier 1 competing causal-gene candidate with stronger expression
  support but weak direct druggability.
- `ZMIZ1`: locked MS/Crohn opposite-direction decoupling locus.
- `PTGER4`: closed as not-a-clean-transfer-target.

## Next Forcing Question

Can genotype-linked immune-cell or CSF protein/CITE-seq data distinguish
between a protective CXCL17-GPR25 trafficking mechanism and a KIF21B
cytoskeletal/transport mechanism?

If no such dataset is accessible, the next useful output is not more weak
public transcript mining; it is a wet-lab handoff design for genotype-linked
GPR25/KIF21B expression and CXCL17 migration/RhoA/integrin assays.
