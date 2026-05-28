# Candidate Index

Candidate files are lifetime histories, not per-wave reports.

## V4 Phase 2 Recalibration Pool

| Candidate file | Display name | Current status | V4 tier | Reason |
|---|---|---:|---:|---|
| `NAMPT.md` | NAMPT | demoted | Tier 0 | constrained eNAMPT branch failed Tier 0; retain only as HIF/NAD/eNAMPT marker/readout |
| `CTSS.md` | CTSS | demoted | Tier 0 | V5 pH-conditional modality distinction noted, but no CTSS-specific causal/predictive evidence beyond APC/HLA-II/IFI30/IFN state |
| `TYK2.md` | TYK2 | demoted | Tier 0 | V5 allosteric-selectivity contribution not new enough; Sjogren occupied by active deucravacitinib Phase 3; no MS/subgroup anchor beyond broad JAK/IFN |
| `LTA4H.md` | LTA4H | demoted | Tier 0 | V5 lipid-lysosomal stratification concept lacks lipidomics, perturbation, non-IBD replication, or treatment-response predictive value |
| `CHI3L1.md` | CHI3L1 | parked | Tier 0 | biomarker/stratification branch only; direct therapeutic intervention remains marker-like |
| `TREM2.md` | TREM2 | demoted | Tier 0 | V5 AL002 prior art is adjacent not target-invalidating; demotion holds for lack of route-split repair-vs-activation evidence |
| `LXR_ABCA1_ABCG1.md` | LXR/ABCA1/ABCG1 | demoted | Tier 0 | cholesterol-efflux/readout axis only; direct target claim lacks direction, causal, and selectivity support |
| `LRRK2.md` | LRRK2 | parked | Tier 0 | generic claim killed; V4 subgroup/combo/natural-experiment contribution required |
| `MERTK_TAM.md` | MerTK/TAM family | demoted | Tier 0 | efferocytosis comparator only; correct-direction restoration lacks causal/modality support |
| `ACSL1.md` | ACSL1 | demoted | Tier 0 | original target claim failed incremental-value, simulation, direction, and modality gates |
| `CIITA_SELECTIVE.md` | CIITA selective approaches | parked | Tier 0 | selective decoupling mechanism survives, but only non-druggable/partial perturbation benchmarks exist |
| `CDK8_CDK19_MEDIATOR.md` | CDK8/CDK19 Mediator kinases | parked | Tier 0 | CDK8/19 chemical matter exists, but local evidence lacks MED16-like pharmacologic APC phenocopy |
| `FPR2_ALX.md` | FPR2/ALX biased agonism | parked | Tier 0 | constrained biased-agonism/efferocytosis branch exists, but MS anchor and direct dependency evidence are insufficient |
| `IFI30_GILT.md` | IFI30/GILT | demoted | Tier 0 | direct intervention evidence-driven failure; biomarker/readout only parked |

## Additional V3 Signals To Consider Later

- `MIF_CD74_STRATIFICATION.md`: V5 promoted this repeated parked branch to
  Tier 1 and demoted it after component-resolved MS pseudobulk and GSE282122
  treatment-response tests failed to show receptor-specific behavior beyond
  generic APC/HLA-II/IFN state.
- `PREGNANCY_REMISSION_AXIS.md`: active Tier 1 natural-experiment axis.
  `GSE17410` MS PBMC month-9 IFN/APC signal survives leave-one-out but is
  composition-confounded; `E-MTAB-12260`, `GSE235508`, and `GSE108497` refine
  the model toward compartmental/disease-specific kinetics.

## Status Semantics

- `alive`: active at a V4 tier.
- `parked`: plausible but blocked on data or modality.
- `demoted`: evidence-driven failure.
- `prior_art_recalibration_pending`: V3 demotion needs V4 rulebook review.
