# Myasthenia Gravis Report: Dalton

Returned: 2026-05-26 19:10 UTC

## Verdict

MG should be partial, not core, for V3 convergence. It supports IFN/APC plus
antigen-processing biology mainly in thymus/early-onset MG and some PBMC
inflammatory states, but the disease-defining neuromuscular junction lesion is
antibody/complement mediated rather than a local myeloid/APC lysosomal module.

## Evidence Summary

- Thymus: strongest support. Reported datasets/accessions include `GSE103974`,
  `GSE103812`, `HRA013414`, and EOMG thymus scRNA MIF-CD74 work. Candidate nodes:
  HLA-II, `CD74`, `CXCL10`, `CTSS`, pathway-level `STAT1/IRF1`; weaker direct
  evidence for `IFI30`, `CTSD`, `CTSB`, and `NAMPT`.
- NMJ: weak for this module. AChR+ MG has C1q/classical complement and MAC damage
  at the postsynaptic membrane. `GSE11465` is rat EAMG muscle/NMJ-adjacent
  transcriptomics and not decisive human convergence.
- PBMC: moderate/context-dependent. Candidate accessions include `GSE85452`,
  `HRA000997`, `GSE227835`, `GSE222427`, `HRA003797`, and `HRA013414`. Supports
  HLA-II/CD74/CXCL-axis inflammatory APC states, but not a coherent
  `IFI30/CTSD/CTSB/NAMPT/SPP1/C1Q` transcript module outside crisis contexts.

## Integration Decision

Classify MG as partial/supporting and thymus-anchored. Use it as corroboration
for IFN/APC and MHC-II/lysosomal processing, but not as a central convergence
disease.
