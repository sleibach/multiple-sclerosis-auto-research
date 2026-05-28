# Wave37 GSE212008 CRISPR Efferocytosis Screen

## Method

- Data: `GSE212008`, raw sgRNA counts from primary murine BMDM pooled CRISPR KO screen.
- Efficient-eater bins: `S1_Q2`, `S3_Q2`; non-eater bins: `S1_P5`, `S3_P5`; inputs: `S1_BS`, `S3_BS`.
- Scoring: library-size normalized log2(CPM+1) sgRNA enrichment vs input, summarized by gene median.
- Direction: efficient-eater enrichment means gene KO enhances efferocytosis; non-eater enrichment means KO impairs efferocytosis.

## Results

- sgRNAs: 74,674.
- genes: 19,672.
- KO-enhancer negative regulators by consistency gate: 214.
- KO-impaired positive regulators by consistency gate: 54.

## Guardrail

This screen is a direct functional efferocytosis assay, but it has no transcriptomic or autoimmune tissue readout. A candidate from this screen remains unpromoted unless expression perturbation, disease-state replication, druggability, and prior-art gates also pass.
