# NAMPT

Status: demoted  
V4 tier: Tier 0  
Last updated: 2026-05-28

## V3 History

V3 demoted NAMPT because NAMPT biology/inhibitors are well known, systemic
inhibition has safety concerns, and local evidence did not establish a
selective autoimmune therapeutic window.

## V4 Recalibration Question

Does V4 have a contribution beyond generic NAMPT inhibition, such as
biomarker-defined transient immunometabolic reset, tissue-targeted modality, or
combination therapy?

## Current V4 Contribution

Narrowly alive only as an eNAMPT or biomarker-defined transient NAMPT-axis
branch.

Closed:
- generic systemic intracellular NAMPT catalytic inhibition;
- FK866/APO866-style NAD-depletion logic for broad MS or pan-autoimmune use;
- NAMPT as a common-variant genetically anchored pan-autoimmune target.

V4 contribution:
- separate extracellular NAMPT / inflammatory eNAMPT biology from intracellular
  NAD-depletion biology;
- test whether NAMPT-high inflammatory myeloid/metabolic states define a
  treatment-resistance or remission-reversal subgroup;
- require a non-NAD-depleting or tightly time/tissue-bounded modality before
  promotion beyond Tier 0.

## V4 Recalibration Verdict

Verdict 2: demotion was partly prior-art-driven, but a constrained V4
contribution exists.

Prior-art grade: P1 high crowding for generic NAMPT/NAD intervention. It is not
P0 target-invalidating because no local evidence showed an equivalent autoimmune
clinical failure with adequate NAMPT target engagement. The live branch is not
generic NAMPT inhibition; it is eNAMPT/subgroup/transient-modulation biology.

## Evidence Ledger

- `EXHAUSTION.md`: NAMPT was the top computational successor after ACSL1, with
  MS foamy proteome/snRNA convergence, recurrence in RA/psoriasis/IBD/SLE,
  ChEMBL tractability, and AlphaFold pLDDT 94.25; rejected for prior art,
  direction ambiguity, and systemic safety.
- `results_v3/cross_disease_gene_summary.tsv`: NAMPT tested in 7 diseases;
  supportive/trend signal only in Crohn and UC; no strong disease count.
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`: NAMPT
  residual support retained only in IBD; `non_ibd_retained_positive_disease_count
  = 0`, `strict_core_covariate_surviving_disease_count = 0`, MS white-matter
  delta -0.214, p 0.543.
- `results_v3/wave20_genetic_druggable_altaxis/local_opentargets_genetics_summary.tsv`:
  NAMPT OpenTargets score 0.0, no disease genetics support.
- `results_v3/wave96_c15orf48_controller_search/pre_donor_controller_rank.tsv`:
  NAMPT had positive contexts in Crohn myeloid, UC myeloid, and T1D acinar
  cell, but failed MS anchor, genetics, perturbation, foundation, and modality
  gates.
- `results_v3/wave126_l1000_upstream_regulator_reopener/l1000_upstream_regulator_decisions.tsv`:
  withaferin-A/NAMPT did not reopen because the compound signal was high-risk
  cytotoxic/steroid/stress biology.
- `subagents_v3/genetics_james_report.md`: NAMPT weak as a common-variant
  cross-autoimmune anchor; genetics favored HLA-II/IFI30/IRF1 instead.
- `subagents_v3/wave19_hostile_critique.md`: local prior art cites FK866/NAMPT
  inhibition reducing EAE disability via NAD depletion (PMID 19936064) and
  protective NAD biology (PMID 25290058), supporting direction ambiguity.

## Next Tier 0 Test

Run an eNAMPT-vs-iNAMPT separation screen.

Question:
- Is the NAMPT signal in MS lesion, CSF extracellular vesicle/protein, or
  disease-relevant myeloid datasets specifically extracellular/inflammatory
  state-associated rather than generic hypoxia/stress/NAD metabolism?

Pass Tier 0 only if:
- eNAMPT/NAMPT-high state is enriched in MS lesion-relevant myeloid or
  CSF-EV/protein data;
- signal survives adjustment for `HIF1A`, glycolysis, generic IFN/NF-kB, and
  myeloid density;
- at least one non-IBD disease replicates;
- and a non-NAD-depleting or tightly bounded modality is plausible.

Fail if NAMPT remains an IBD-biased stress/metabolism marker or only reopens via
systemic catalytic inhibition.

## V4 Tier 0 Audit

Audit completed: `analysis/tier_0_triage/nampt_enampt_separation/decision.json`.

Call: `DEMOTE_TO_PARKED_MARKER_BRANCH`.

Result:
- MS white-matter delta log2 `-0.2143688948990014`, p `0.5434156214094958`.
- Non-IBD retained positive disease count `0`.
- Strict core-covariate surviving disease count `0`.
- OpenTargets max genetics score `0.0`.
- C15-like positive contexts were `ibd_crohn_myeloid`,
  `ibd_uc_myeloid`, and `t1d_acinar_cell`, not MS.

Interpretation: the constrained eNAMPT branch does not pass Tier 0 as an
active therapeutic candidate. This is not a P0 prior-art kill; it is an
evidence kill for active nomination because the local evidence does not
separate a druggable extracellular NAMPT mechanism from generic intracellular
NAMPT/NAD stress-metabolism biology. Retain NAMPT only as a marker/readout for
HIF/NAD/eNAMPT inflammatory metabolism.
