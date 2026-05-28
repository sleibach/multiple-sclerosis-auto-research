# FPR2 / ALX Biased Agonism

Status: parked  
V4 tier: Tier 0  
Last updated: 2026-05-28

## V3 History

V3 Wave162 kept FPR2/ANXA1 closed for V3 promotion because of weak MS anchor and
crowded pro-resolution prior art.

## V4 Recalibration Question

Does biased agonism, subgroup selection, or combination with debris/efferocytosis
biology create a non-equivalent contribution?

## Current V4 Contribution

Narrow V4 contribution exists, but it is not ready as an active MS therapeutic
nomination.

Closed:
- generic FPR2 agonism;
- generic specialized pro-resolving mediator claims;
- MS target nomination based on ANXA1/SPM/EAE context alone.

Parked branch:
- biased FPR2/ALX pro-resolution agonism or ANXA1-mimetic biology for an
  IBD/lupus-nephritis-first resolution/efferocytosis indication;
- possible later MS bridge only if human myelin-loaded microglia or MS
  lesion-derived myeloid systems show FPR2-dependent cargo clearance and
  lipid-inflammatory state reduction.

The V4 contribution is ligand-bias and disease-stage/cell-state specificity,
not the existence of FPR2/ALX biology itself.

## V4 Recalibration Verdict

Verdict 2: demotion was partly prior-art-driven, but a constrained V4
contribution exists.

Prior-art grade: P1 high crowding. FPR2/SPM/ANXA1 resolution biology is heavily
published and patents cover broad FPR2 agonist inflammatory/neuroinflammatory
uses, including MS examples. It is not P0 target-invalidating because the local
V3 record did not identify an equivalent biased FPR2/ALX intervention tested
clinically in MS, IBD, or lupus nephritis and failed for target-mechanistic
reasons with adequate target engagement.

The branch is parked rather than alive because V3's blockers were not merely
prior-art blockers: MS white-matter support was weak/negative, target-resolved
genetics were absent, direct efferocytosis CRISPR evidence was unresolved, and
FPR2 ligand bias creates real sign risk.

## Evidence Ledger

- `subagents_v3/wave34b_fpr2_anxa1_resolution.md`: parked FPR2/ALX + ANXA1 as
  plausible IBD/lupus-nephritis follow-up but not MS promotion. Local Crohn
  colon myeloid `FPR2` delta 4.638, Hedges g 2.933, p 0.000260, FDR 0.068672;
  UC colon myeloid delta 4.123, Hedges g 2.633, p 0.000587, FDR 0.082977. MS
  white matter was negative/null: `FPR2` delta -0.933, p 0.372, FDR 0.914;
  `ANXA1` delta -0.069, p 0.880, FDR 0.983.
- `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`:
  `FPR2` was `NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY`; failed genetic
  breadth, local cell-state, druggable-surface, and perturbation/model gates
  despite not being marked prior-art-blocked.
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/candidate_gene_screen_scores.tsv`
  as summarized in `subagents_v3/wave61s_intervention_mining.md`: `FPR2` and
  `ANXA1` were tracked resolution/efferocytosis candidates but both were
  unresolved; `FPR2` median efficient-minus-noneater LFC -0.246, FDR 0.920;
  `ANXA1` median LFC -0.348, FDR 0.920.
- `results_v3/wave161_post_interface_route_reprioritization/post_interface_route_rank.tsv`:
  `FPR2_ANXA1_BIASED_RESOLUTION` was
  `REOPEN_WITH_WETLAB_TEST_ONLY_NOT_V3_PROMOTION`; blockers were strict MS
  anchor, target resolution/genetics, lack of perturbation/model response, and
  fewer than two support channels.
- `subagents_v3/wave48g_resolution_reopener_critique.md`: branch was
  `REOPEN_WITH_NEW_TEST_ONLY`; strongest evidence was biased FPR2 colitis
  pharmacology and CNS-adjacent FPR2/ALX astrocytopathy support, but blockers
  remained ligand-bias sign risk, ANXA1/EAE context conflict, weak/negative MS
  signal, no target-level genetics, no human disease-tissue FPR2 dependency,
  and unsettled CNS delivery.
- `subagents_v3/wave47g_overlooked_route_critique.md`: called FPR2/ANXA1 the
  only real overlooked resolution-route reopener, but explicitly required
  human macrophage/microglia cargo-clearance dependency testing rather than
  another expression correlation.
- `results_v3/wave23_metabolite_barrier_circuit/chembl_target_snapshot.tsv`:
  FPR2 is a tractable GPCR target (`CHEMBL4227`, UniProt `P25090`) with 3374
  ChEMBL nM activity records in the V3 snapshot.
- `results_v3/wave32c_resolution_prior_art_audit/route_feasibility_ranked.tsv`:
  specialized pro-resolving mediator/FPR2 route was the least-blocked
  resolution route but still `NOT_BLOCKED_BUT_IMMATURE`, with IBD favored
  before MS.
- `subagents_v3/wave34b_fpr2_anxa1_resolution.md`: local prior-art/trial
  surface found no direct ClinicalTrials.gov FPR2 agonist, FPR2 MS, or annexin
  A1 autoimmune interventional trial, but did identify broad Google Patents
  coverage including `US11708327B2` and `EP3981878A1`.

## Next Tier 0 Test

Do not reopen generic FPR2 agonism.

Allowed Tier 0 re-entry test:
- Run a ligand-bias and cargo-resolved perturbation screen in primary Crohn/UC
  lamina propria macrophages, lupus-nephritis kidney macrophage/slice models,
  and human iPSC microglia or MS lesion-derived myeloid cultures loaded with
  myelin debris and apoptotic oligodendrocyte-lineage cells.
- Compare columbamine, Quin-C1, AT-01-KG or other biased FPR2 agonists, Ac2-26
  or ANXA1-mimetic controls, inactive analogs, and FPR2 blockade/knockdown.

Pass only if:
- cargo clearance increases by at least 30% versus vehicle in at least one
  disease-relevant macrophage system;
- effect is abolished or strongly reduced by FPR2 blockade/knockdown;
- lipid-inflammatory readouts such as `S100A8`, `S100A9`, `IL1B`, `CXCL8`, or
  foam-cell stress markers fall;
- broad antiviral IFN and HLA-II/CD74 antigen-presentation capacity are not
  globally collapsed;
- profibrotic `TGFB1`/collagen programs do not increase in LN/IBD contexts;
- and at least one independent disease context replicates.

Fail if benefit is ligand-nonspecific, chemotactic/pro-inflammatory,
FPR2-independent, fibrosis-associated, or absent in MS myelin-loaded microglia.
