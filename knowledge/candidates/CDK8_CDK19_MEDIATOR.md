# CDK8 / CDK19 Mediator Kinases

Status: parked  
V4 tier: Tier 0  
Last updated: 2026-05-28

## V3 History

Mediator-kinase MHC-II decoupling was identified as promising but under-budgeted
relative to weaker candidates. V3 did not mature it through Tier-like causal or
translational validation.

## V4 Recalibration Question

Can CDK8/CDK19 inhibition selectively reduce pathogenic APC/MHC-II programs
without broad IFN/JAK immunosuppression?

## Current V4 Contribution

Verdict: **Demotion was prior-art-driven but V4 contribution exists.**

V4 contribution:

Low-dose or context-selective CDK8/CDK19 Mediator-kinase modulation to decouple
pathogenic IFN-gamma-induced `CIITA`/MHC-II/`CD74` antigen-presentation
programs in inflammatory APC states. This is distinct from prior IL-10/Treg
centered CDK8/19 autoimmune claims.

Prior-art grade: `P1 high crowding`, not target-invalidating.

## Recalibration Evidence

Local V3 support:

- `results_v3/wave15_perturbation_drug_response/gse162464_mouse_rna_selectivity.tsv`:
  `Med16_KO` in IFN-gamma-stimulated mouse macrophages suppresses the target
  antigen-presentation module with `target_module_effect=-3.1395`, generic IFN
  effect `-0.7979`, and selectivity score `2.3051`.
- `results_v3/wave17_mediator_kinase_route/local_perturbation_evidence.tsv`:
  `Med16_KO` has mean target module log2FC `-3.74`, generic IFN core `-0.46`,
  `Ciita -3.34`, `Cd74 -2.46`, `H2-Aa -7.33`, `H2-Ab1 -4.71`.
- `results_v3/wave17_mediator_route_gate/summary.json`: V3 verdict
  `PARK_AS_PERTURBATION_DERIVED_INTERVENTION_HYPOTHESIS`, not no-go.
- `results_v3/wave17_mediator_kinase_route/compound_landscape.tsv`: real
  CDK8/19 chemical matter exists, including cortistatin A, CCT251921,
  MSC2530818, Senexin B/BCD-115, and RVU120.
- `results_v3/wave53_perturbation_first_pivot/decision_matrix.tsv`:
  `MED16_MEDIATOR_MODULE` passes `real_perturbation_selectivity` and
  `tractable_druggability`, but failed V3 on MS anchor, safe-selective
  direction, and novelty.
- `subagents_v3/wave53g_med16_mediator_review.md`: decisive blocker is missing
  pharmacologic CDK8/CDK19 phenocopy of `MED16`, not target-invalidating prior
  art.

Prior-art context:

- Johannessen et al. identified CDK8/CDK19 as regulators of IL-10 in myeloid
  cells via BRD6989 and related inhibitors:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC5693369/>.
- Akamatsu et al. reported CDK8/CDK19 inhibition with CCT251921 promoted Treg
  differentiation and suppressed EAE:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6736578/>.

These establish crowding and feasibility, but not an equivalent clinical
failure of APC MHC-II decoupling in MS or a biomarker-defined autoimmune
subgroup.

## Key Cautions

- The strongest perturbation is `MED16`, a Mediator structural subunit, not a
  clean drug target.
- Local `Cdk8`, `Cdk19`, and `Ccnc` genetic loss did not clearly phenocopy
  `Med16_KO` in the MHC-II FACS screen.
- CDK8/19 inhibitors can affect broad IFN transcription, Treg biology, IL-10,
  cytokines, metabolism, and potentially safety-relevant transcriptional
  programs.
- Novelty must not be "CDK8/19 for autoimmunity"; it must be the defined APC
  MHC-II decoupling mechanism in a disease state or subgroup.

## Next Tier 0 Test

Run a pharmacologic phenocopy audit for cortistatin A, CCT251921, MSC2530818,
RVU120, Senexin B/BCD-115, and related CDK8/19 inhibitors.

Pass criterion:

- CDK8/19 perturbation suppresses `CIITA`/`HLA-DRA`/`CD74` more strongly than
  generic IFN genes (`STAT1`, `IRF1`, `CXCL10`, `GBP1`).
- Selectivity ratio should approach the `Med16_KO` benchmark from V3
  (`2.3051`).

If no public pharmacologic dataset exists, keep candidate alive but parked at
Tier 0 pending wet-lab phenocopy. Do not demote on prior-art grounds alone.

## V4 Tier 0 Audit

Audit completed: `analysis/tier_0_triage/ciita_mediator_selectivity/decision.json`.

Call: `PARK_ALIVE_PENDING_PHARMACOLOGIC_PHENOCOPY`.

Result:
- `Med16_KO` remains the only full benchmark pass: target suppression 3.139501,
  generic IFN suppression 0.797855, target/IFN ratio 3.934928, selectivity
  score 2.305117, no stress induction.
- `Gsk3b_KO` is partial: target/IFN ratio 2.040187 but selectivity score only
  0.777956.
- `Cdk8`, `Cdk19`, and `Ccnc` sgRNA evidence in the local MHC-II FACS screen
  does not phenocopy `Med16`.
- The local archive has CDK8/CDK19 chemical matter, but no disease-relevant APC
  pharmacologic dataset proving MED16-like selectivity.

Interpretation: the mechanism survives as a high-priority parked Tier 0 branch,
but it does not advance to Tier 1 until pharmacologic phenocopy is shown.
