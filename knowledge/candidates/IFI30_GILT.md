# IFI30 / GILT

Status: demoted  
V4 tier: Tier 0  
Last updated: 2026-05-28

## V3 History

IFI30/GILT repeatedly appeared as an antigen-processing/lysosomal node with
MS genetic/QTL hints and IBD myeloid recurrence, but was demoted for
host-defense, poor reachability, and no clear selective modality.

## V4 Recalibration Question

Is IFI30/GILT an intervention target, a stratification biomarker, or a pathway
readout for safer upstream modulation?

## Current V4 Contribution

Verdict: **Evidence-driven demotion holds for direct IFI30/GILT intervention.**

Direct IFI30/GILT inhibition or activation remains demoted. A parked V4
contribution may exist only as a biomarker/pathway readout for safer upstream
modulation of antigen-processing-high APC states.

## Recalibration Evidence

Local V3 support for biology:

- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`:
  IFI30 has MS L2G support `0.650102` and MS monocyte QTL H4 `0.995901`, plus
  QTL colocalization in `Celiac;Crohn;MS`.
- `results_v3/wave91_lipid_lysosomal_module_intervention_rank/module_wide_evidence_matrix.tsv`:
  IFI30 has anti-TNF nonresponse and UC myeloid signals.
- `results_v3/wave166_same_gene_genetics_cellstate_overlap/same_gene_genetics_cellstate_rank.tsv`:
  genetics and cell-state gates pass.

Evidence against direct target promotion:

- MS white matter expression anchor is weak/null: delta `0.210162`, p
  `0.379947`, FDR `0.914127`.
- `results_v3/wave122_fresh_breadth_target_scan/fresh_breadth_target_rank.tsv`:
  IFI30 has support channels but no MS anchor, perturbation/model support, or
  modality.
- ChEMBL local summaries contain no IFI30 activity rows.
- Direct mechanism is antigen processing/host-defense biology, not a clearly
  safe selective intervention point.

Prior-art/biology context:

- IFI30/GILT is a lysosomal thiol reductase involved in MHC I/II antigen
  processing.
- Published GILT/MOG/EAE biology means MS relevance is not a sufficient
  novelty claim by itself.

This is evidence-driven, not merely prior-art-driven: modality, perturbation,
MS expression, and host-defense risk fail.

## Next Tier 0 Test

Do not pursue direct IFI30/GILT intervention.

Park only biomarker/readout test:

In treatment-response datasets, test whether baseline
`IFI30 + HLA-DRA + CD74 + CTSS` high APC/myeloid states predict nonresponse or
response to antigen-presentation-modulating therapies after adjusting for
generic IFN/JAK/STAT1 activity. Advance only if IFI30 adds predictive value
beyond the IFN/HLA-II module in at least two diseases or one MS/progressive-MS
cohort.
