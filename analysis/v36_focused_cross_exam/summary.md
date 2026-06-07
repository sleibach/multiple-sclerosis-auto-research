# V36 Focused Cross-Exam

Status: **completed_two_lineage_cross_exam**.

Role: adversarial proposal generation only. No model output is evidence.

Model status:

- Claude returned `5` JSON weaknesses/tests.
- Gemini hit `MAX_TOKENS` on the full prompt, then returned `3` compact JSON
  weaknesses/tests.

Convergent or useful issues:

| Issue | Source | Held-data status |
|---|---|---|
| Small-n/unreplicated risk | Claude, Gemini | already acknowledged; external validation needed |
| Batch/technical confounding | Claude | metadata likely limited; feasibility check remains possible |
| Fine composition/substate artifact | Claude | partially grounded in Iteration 22 |
| Viral/generic ISG confounding | Claude | partly overlaps V32 IFN-suppression residualization |
| Glycolysis decoupling from IFN/STAT | Claude, Gemini mechanistic concern | executable next on V32 subject-level modules |
| Steroid dose interaction | Gemini | not testable with held metadata; validation-cohort requirement |

Next executable grounding:

Run glycolysis decoupling: residualize `delta_glycolysis` against
`delta_IFN_APC`/`delta_stat1_axis` and conversely in `GSE253006_TOF_exact`,
then test whether either retains response AUC. This determines whether
glycolysis is an independent remodeling component or just rides with IFN/STAT.
