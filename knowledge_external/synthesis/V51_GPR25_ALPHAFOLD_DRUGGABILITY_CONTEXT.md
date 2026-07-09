# V51 GPR25 AlphaFold Druggability-Direction Context

Status: structural-prediction context only. This note does not alter the
grounded chr1 genetics verdict, locked rules, or validation plans.

Boundary: `external-unverifiable`; source: https://alphafold.ebi.ac.uk/api/prediction/O00155; marker: `NOT_PROJECT_GROUNDED`.

## Record

| field | value |
|---|---|
| structural record | [knowledge_external/structures/alphafold/GPR25_O00155/record.json](../structures/alphafold/GPR25_O00155/record.json) |
| model | AlphaFold DB `AF-O00155-F1`, version `6` |
| protein | GPR25, UniProt `O00155`, 361 aa |
| retrieval date | 2026-07-09 |
| mean pLDDT | `82.447` |
| median pLDDT | `92.06` |
| residues with pLDDT >= 70 | `79.5014%` |
| residues with pLDDT >= 90 | `59.8338%` |
| residues with pLDDT < 50 | `14.1274%` |
| low-confidence segments | residues `1-28` and `338-360` |
| mean PAE | `12.9196` |
| median PAE | `8.0` |
| PAE entries <= 10 | `56.8826%` |

## Prediction-Informed Context

The AlphaFold DB prediction is consistent with the prior V19 structural-context
view that GPR25 has a confidently modeled GPCR-like core while terminal regions
are less reliable. The high-confidence portion supports using the predicted
structure as tractability context for a seven-transmembrane receptor fold.

The low-confidence N-terminal and C-terminal regions are explicit caution zones.
Any claim depending on those flexible termini, tail-mediated signaling, or
precise loop geometry should be treated as structurally weak until an
experimental structure or focused assay exists.

The structure does not resolve the causal-gene uncertainty at the chr1 MS-UC
locus and does not make GPR25 intervention-grade. It also does not solve the
main direction-matching problem: the genetics-facing therapeutic direction
remains restoration or agonism, and the project record still shows immature
chemical matter for GPR25. The prediction therefore informs modality fit but
does not override the grounded verdict from V19: structurally plausible,
chemically immature, and causally unresolved.

## Next Use

If GPR25 remains a live mechanistic candidate after genotype/protein-level
follow-up, the useful structural next step is not another AlphaFold-only claim.
It is a confidence-aware pocket/ligandability workup on the high-confidence
transmembrane core, explicitly separated from the low-confidence terminal
regions and still gated by direction-matched agonism/restoration feasibility.
