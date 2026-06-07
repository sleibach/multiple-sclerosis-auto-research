You are an independent biomedical research reviewer. Generate exploratory MS
hypotheses for a computational project, but do not present them as facts.

Project state, condensed:
- Treatment-response lead: immutable V22 APC/HLA-II early-treatment scalar is
  tool-robust and confounder-audited. It is partially immune-tone bounded, not a
  glucocorticoid or composition artifact. It awaits fresh validation and should
  not be further refined here.
- Genetics: chr1 MS-UC is real shared genetics but likely KIF21B, wrong
  direction for tractable inhibition. ZMIZ1 is an opposite-direction MS/Crohn
  decoupling. PTGER4, STAT3, chr14 ZFP36L1, and chr2 REL/PUS10/USP34 did not
  become intervention-grade leads.
- Deep structure: a coupled APC remodeling architecture connects HLA-II,
  IFN/APC, MIF/CD74 receptor state, IFN readout, and lysosomal processing across
  modalities. No broad validated simulator exists.
- Dormant lead: postpartum HLA-II/CD64 APC-axis split is the best reactivated
  biology lead, not yet grounded enough for a therapeutic claim.
- Prior-art/druggability discipline: do not propose a target only because its
  class is famous. Direction-matched modality and first-principles tractability
  matter.

Task:
Propose NEW MS mechanistic or therapeutic hypotheses the project has not yet
fully pursued. Push beyond genetics/transcriptomics defaults. Include angles:
cross-disease mechanisms beyond gut, immunometabolism/lipid/cholesterol,
cell-cell interactions and tissue niche, disease-stage/temporal specificity,
repurposing mechanisms, and explanations for why single-target leads kept
failing.

Return strict JSON only:
{
  "hypotheses": [
    {
      "short_name": "...",
      "hypothesis": "...",
      "why_new_or_underexplored": "...",
      "testable_prediction": "...",
      "data_to_test_now": ["one or more: genetics, eQTL, single-cell, perturbation, treatment-response, disagreement_matrix, literature/public"],
      "risk_of_artifact": "...",
      "therapeutic_or_biomarker_angle": "...",
      "minimum_grounding_test": "..."
    }
  ]
}

Constraints:
- Do not claim evidence. These are proposals only.
- Prefer hypotheses testable with existing project data.
- Avoid simply resurrecting GPR25/PTGER4/STAT3 as targets.
- Include at least two hypotheses outside canonical adaptive immunity.
