# V54 Progression-Lesion State Test

Verdict: **NO_ORTHOGONALLY_SUPPORTED_PROGRESSION_LESION_MODULE**.

GSE180759 used donor/pathology immune pseudobulks with at least 20 nuclei
and exact paired sign flips. GSE279972 used 54 morphology-labelled MS
samples from 21 donors, lesion-class and B-APC adjustment, clustered
intervals, and 300,000 three-seed donor-wild nulls.

| module | active-inactive mean | exact p | foamy adjusted beta | wild p | BH q | max-T p | outcome |
|---|---:|---:|---:|---:|---:|---:|---|
| receptor_cd44_cxcr4 | 1.148 | 0.25 | 0.025 | 0.912 | 0.972 | 1 | inconclusive |
| hla_regulatory | 0.775 | 0.25 | -0.121 | 0.541 | 0.812 | 0.989 | not_supported |
| ifn_apc_unique | 0.284 | 0.75 | -0.161 | 0.466 | 0.812 | 0.957 | not_supported |
| lysosomal_unique | 0.263 | 0.75 | 0.493 | 0.00452 | 0.0271 | 0.05 | not_supported |
| complement_phagocytosis | 0.068 | 0.75 | -0.008 | 0.972 | 0.972 | 1 | not_supported |
| lipid_repair | 0.997 | 0.25 | 0.394 | 0.0249 | 0.0748 | 0.223 | inconclusive |

Even an orthogonally consistent row remains needs-data because only three
GSE180759 donor pairs are eligible (minimum exact two-sided p=0.25), and
foamy morphology is not the same estimand as a chronic-active lesion edge.
No result is a progression-rate, causal, intervention, or therapeutic claim.
