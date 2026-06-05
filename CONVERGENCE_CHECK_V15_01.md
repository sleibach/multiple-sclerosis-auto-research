# CONVERGENCE_CHECK_V15_01

Date: 2026-06-06

## Cells / Loci Advanced

- MS-UC chr1 `1:200375242-201375897`: worked from SuSiE credible set to candidate causal gene and direction proxy.
- MS-Crohn chr10 `10:80542475-81559335`: worked from SuSiE credible set to candidate causal gene and direction proxy.

## Convergence

- Both loci remain credible shared inherited-risk loci after V14 SuSiE-coloc.
- Both loci look predominantly regulatory rather than directly protein-altering.
- Neither locus currently converges with the project's strongest MS lesion/cell-state modules.

## Divergence

- chr1/MS-UC: disease association signs are concordant and stored QTL evidence points to `GPR25`.
- chr10/MS-Crohn: disease association signs are opposite and stored QTL evidence points to `ZMIZ1` mainly from the Crohn side.

## Hostile Critique

1. The `GPR25` direction claim is still only a stored direction-proxy claim. Without raw eQTL effect-allele alignment, it must not be converted into a therapeutic agonist/antagonist recommendation.
2. The `ZMIZ1` causal-gene claim is plausible but not fully proven for MS. The tight credible-set location and Crohn eQTL support are not equivalent to MS eQTL colocalization.
3. ChEMBL target presence for `GPR25` is not meaningful druggability by itself. The retrieved activity records are GPCRome screen outputs, not selective chemical matter.
4. The lack of MS lesion cell-state support for both genes is a major translational gap. Genetics alone does not establish the tissue compartment where intervention would matter.
5. Prior literature already supports shared MS/IBD genetic architecture. V15's contribution is the stricter locus-level triage, not the broad sharing claim.

## Decision

Do not upgrade the genetics cells or propose a drug. Preserve both loci as regulatory genetics leads requiring raw QTL alignment:

- `GPR25`: prioritized for allele-aligned eQTL coloc and deorphanization feasibility if direction survives.
- `ZMIZ1`: prioritized as a decoupling locus; test whether MS risk lowers ZMIZ1 expression while Crohn risk raises it.

