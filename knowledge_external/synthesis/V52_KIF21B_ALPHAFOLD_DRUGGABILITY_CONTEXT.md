# V52 KIF21B AlphaFold Druggability-Direction Context

Status: structural-prediction context only. This note does not alter the
grounded chr1 genetics verdict, locked rules, or validation plans.

Boundary: `external-unverifiable`; source: https://alphafold.ebi.ac.uk/api/prediction/O75037; marker: `NOT_PROJECT_GROUNDED`.

## Record

| field | value |
|---|---|
| structural record | [knowledge_external/structures/alphafold/KIF21B_O75037/record.json](../structures/alphafold/KIF21B_O75037/record.json) |
| model | AlphaFold DB `AF-O75037-F1`, version `6` |
| protein | KIF21B, UniProt `O75037`, 1637 aa |
| retrieval date | 2026-07-10 |
| mean pLDDT | `69.6468` |
| median pLDDT | `78.81` |
| residues with pLDDT >= 70 | `62.4313%` |
| residues with pLDDT >= 90 | `25.1680%` |
| residues with pLDDT < 50 | `26.0843%` |
| mean PAE | `25.3243` |
| median PAE | `28.0` |
| PAE entries <= 10 | `9.6645%` |

## Prediction-Informed Context

The full-length KIF21B AlphaFold DB prediction has modest global confidence and
high PAE across much of the protein, consistent with the V19 interpretation of
a structured motor domain plus large flexible/disordered regions. The full
protein should not be treated as a rigid, high-confidence assembly.

The decision-relevant tractability context is local, not global. V19's domain
summary found that the kinesin motor domain (`8-370`) has mean pLDDT `83.95`
and median pLDDT `90.06`, while the binding-site annotation (`87-94`) has mean
pLDDT `90.71`. That supports the narrow statement that KIF21B is not
structurally uninterpretable by first principles.

The prediction does not solve the therapeutic direction problem. V19 direction
analysis indicates disease risk lowers KIF21B expression at the exact shared
MS-UC credible-set SNPs. Therefore conventional inhibition, degradation, ASO, or
siRNA would likely be directionally wrong unless future data show a different
gain-of-toxic-function mechanism. The structure supports ligandability context;
it does not create a direction-matched modality.

## Next Use

If KIF21B remains a causal-gene candidate after genotype-linked immune/CSF
protein or expression follow-up, the useful structural next step is a focused,
confidence-aware motor-domain ligandability and selectivity analysis. That
would still need to be paired with a restoration/up-function modality concept
and perturbation data showing protective-direction movement.
