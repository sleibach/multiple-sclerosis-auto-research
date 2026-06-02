# DISAGREEMENT_MATRIX_V10

Status: first supported-only V10 disagreement matrix.

## Inputs

- V8 placement matrix: `analysis/v8_map/placement_matrix.tsv`
- V8 evidence registry: `analysis/v8_map/evidence_registry.tsv`
- V9 microbiome synthesis: `MICROBIOME_AXIS_V9.md`
- V10 builder: `scripts/v10_build_disagreement_matrix.py`

V10 methodology gate:

- A ranked disagreement is included only when both axis placements are
  `supported` or `robust`.
- Provisional microbiome placements are excluded from the real-disagreement
  core, even though V9 found a meaningful MS microbiome signal. V9 did not
  support MS/IBD broad taxonomic proximity.

## Matrix Coverage

- Input disease-axis placements: `120`.
- Supported or robust placements considered: `21`.
- Supported-axis disagreement pairs: `10`.

This is smaller than the full V8 map because V10 deliberately rejects
provisional-vs-provisional contrasts as real disagreements.

## Ranked Disagreements

| Rank | Disease | Axis A | Placement A | Axis B | Placement B | Distance | Initial artifact risk | V10 priority |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ulcerative colitis | IFN/APC antigen-presentation | near/robust | treatment-response architecture | contradictory/supported | `2.5` | compartment, causality, confidence mismatch | high |
| 2 | Sjogren syndrome | IFN/APC antigen-presentation | near/supported | lipid-lysosomal / foamy myeloid | far/supported | `3.0` | compartment mismatch | high |
| 3 | rheumatoid arthritis | IFN/APC antigen-presentation | far/supported | pregnancy modulation | near/supported | `3.0` | compartment and causality mismatch | high |
| 4 | rheumatoid arthritis | treatment-response architecture | far/supported | pregnancy modulation | near/supported | `3.0` | causality mismatch | high |
| 5 | rheumatoid arthritis | tissue-repair / resolution | far/supported | pregnancy modulation | near/supported | `3.0` | compartment and causality mismatch | high |
| 6 | ulcerative colitis | genetic risk architecture | near/supported | treatment-response architecture | contradictory/supported | `2.5` | compartment and causality mismatch | high |
| 10 | ulcerative colitis | treatment-response architecture | contradictory/supported | tissue-repair / resolution | near/supported | `2.5` | high axis non-independence risk; evidence overlap | downgraded internal-consistency note |
| 8 | Crohn disease | IFN/APC antigen-presentation | near/supported | genetic risk architecture | intermediate/supported | `1.0` | compartment and causality mismatch | medium |
| 9 | Crohn disease | genetic risk architecture | intermediate/supported | treatment-response architecture | near/supported | `1.0` | compartment and causality mismatch | medium |
| 10 | Crohn disease | genetic risk architecture | intermediate/supported | tissue-repair / resolution | near/supported | `1.0` | compartment and causality mismatch | medium |

Full table:

- `analysis/v10_disagreement/disagreement_pairs.tsv`

## Immediate Interpretation

### Supported Core Is Not The Same As The Intuitive V9 Story

The V9 MS/IBD microbiome-versus-mucosal disagreement is scientifically
important, but it is not in the supported-only V10 matrix because the
MS-relative IBD microbiome placement remains provisional. It belongs in the
Tier -1 / Tier 0 hypothesis-generating disagreement pool, not the supported
core.

### UC Treatment-Response Versus Tissue-Repair Is Downgraded After Critique

Initial matrix metadata treated this pair as low artifact risk because both
placements are intestinal mucosa treatment perturbation. Hostile critique
correctly identified a more important artifact: **axis non-independence**.
The treatment-response and tissue-repair placements reuse overlapping
datasets, features, and interpretive language.

After adding an independence penalty in `scripts/v10_build_disagreement_matrix.py`,
the UC treatment-response versus tissue-repair row falls to rank `10`.

The surviving content is still useful, but it is not an independent
axis-disagreement finding:

Mechanistic implication to test:

- The transferable object from IBD to MS is **early dynamic inflammatory
  downshift / repair monitoring**, not baseline treatment stratification.
- This matches V7's kill of the broad APC response-architecture rule and
  survival of the narrower `HYP_V7_001` IBD dynamic-downshift hypothesis.

Current classification: treatment-dynamics refinement / transfer-validity
warning, not a clean supported disagreement.

### RA Disagreements Are Real But Natural-Experiment-Specific

RA is far from MS on blood IFN/APC/treatment-response behavior but near on
pregnancy modulation. This is not a global RA/MS divergence. It likely means:

- pregnancy remission biology acts through systemic immune/hormonal mechanisms
  not captured by the blood APC treatment-response rule;
- RA can be MS-adjacent on hormonal natural-experiment dynamics while remaining
  a poor comparator for APC response biomarkers.

This requires artifact audit because pregnancy is a natural experiment and the
other axes are cross-sectional or treatment perturbation.

### Sjogren IFN/APC Versus Lipid-Lysosomal Is A Candidate Compartment Split

Sjogren is near MS on salivary gland epithelial IFN/APC state but far on
lipid-lysosomal / foamy myeloid state in salivary gland APC/epithelial
evidence. The likely first audit question is cell type: epithelial IFN/APC
activation may not imply myeloid lipid-lysosomal convergence.

### Crohn Genetics Disagreements Are Lower Magnitude

Crohn is near MS on mucosal IFN/APC and repair/treatment axes but only
intermediate on genetics. This suggests downstream convergent mucosal
inflammatory-resolution architecture with weaker shared inherited risk than UC.
Because the placement distance is only `1.0`, these are lower priority than UC,
RA, and Sjogren.

## Next Artifact Audit

Each high-ranked disagreement now needs explicit classification:

1. Biological candidate.
2. Compartment artifact likely.
3. Measurement-grade artifact likely.
4. Unresolved because more data is required.

The first mechanistic-resolution targets after independence correction are:

1. UC IFN/APC cross-sectional proximity versus treatment-response
   contradiction.
2. Sjogren IFN/APC versus lipid-lysosomal split.
3. RA pregnancy near versus APC/treatment far.
