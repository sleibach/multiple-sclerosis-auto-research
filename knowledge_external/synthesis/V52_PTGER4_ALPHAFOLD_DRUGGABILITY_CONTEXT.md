# V52 PTGER4 AlphaFold Druggability-Direction Context

Boundary: `external-unverifiable`; source:
https://alphafold.ebi.ac.uk/api/prediction/P35408; marker: `NOT_PROJECT_GROUNDED`.

This note records how the AlphaFold DB PTGER4 structure informs, but does not
change, the project’s PTGER4 therapeutic verdict. It is prediction-informed
context only, not a grounded project finding.

## Structural Record

- Structural record:
  `knowledge_external/structures/alphafold/PTGER4_P35408/record.json`
- UniProt: `P35408`
- AlphaFold model: `AF-P35408-F1`, version `6`
- Mean pLDDT: `70.8763`
- Median pLDDT: `80.47`
- Fraction residues pLDDT >= 70: `0.569672`
- Fraction residues pLDDT >= 90: `0.383197`
- Fraction residues pLDDT < 50: `0.305328`
- Mean PAE: `19.0695`
- Median PAE: `24.0`
- Main low-confidence region: C-terminal residues `356-488`

## Interpretation

PTGER4 is a known prostaglandin E receptor / EP4-class GPCR, so the structural
question is not whether the target class is intrinsically druggable. The
AlphaFold record is compatible with receptor-core interpretability, while the
long low-confidence C-terminal region should not be over-interpreted.

The project closure problem is not solved by structure:

1. The V14/V15/V16/V37 project artifacts treat PTGER4 as a mixed shared/distinct
   signal and a transfer-caution lead, not a clean MS therapeutic target.
2. V50 source-specific external rows support the same caution: rs4613763 rows
   preserve opposite MS/Crohn reported risk alleles, and Crohn-side expression
   modulation does not define an MS-safe direction.
3. A GPCR-like structure does not identify which disease signal, cell type, or
   direction should be pharmacologically modulated.

## V52 Verdict

PTGER4 remains closed as a naive MS/IBD transfer target. AlphaFold makes the
structural tractability context sharper, but it does not rehabilitate the lead
because the blocker is signal decomposition and direction-matched disease
biology, not lack of a receptor fold.

Evidence that would reopen PTGER4 remains unchanged:

- signal-specific fine-mapping/QTL data separating shared and distinct
  components;
- a cell-type-resolved MS direction for the disease-relevant PTGER4 component;
- perturbation or clinical-pharmacology evidence showing that a specific EP4
  modulation direction is protective in the MS-relevant context.

Until those exist, PTGER4 should not receive wet-lab or medicinal-chemistry
priority as an MS target from this project.
