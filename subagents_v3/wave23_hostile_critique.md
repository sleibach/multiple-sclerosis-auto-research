# Wave23 Hostile Critique

Date: 2026-05-27

Role: hostile peer review of the current Wave23 direction. This is not a final
finding or target nomination.

## Bottom-Line Attack

Wave23 did not generate a new evidentiary axis. It mostly re-labeled three
already weak branches:

- `GPR65`: a genetically plausible, druggable-looking GPCR whose local disease
  signal is weak/contradictory and whose IBD/autoimmune modulator space was
  already flagged as crowded.
- `PTPN2`: a strong autoimmune locus whose required therapeutic direction is
  restoration, while the available chemical evidence is inhibitor/wrong-direction
  oncology logic.
- baseline module-response biomarker: already tested in Wave18/Wave19 and failed
  corrected baseline prediction.

`CONVERGENCE_CHECK_6.md:61-64` correctly closed the residual-expression rescue
branch because survivors were tissue-repair, sterol, matrix, complement, or core
inflammatory machinery signals without causal direction. Wave23 risks repeating
that pattern with route-level labels.

## 1. `GPR65` Is Still Weak And Probably Non-Novel

The Wave23 table itself says this is not a promotion-grade route:
`results_v3/wave23_orchestrator_nonexpression_axis_triage/wave23_route_triage.tsv:2`
calls `GPR65_pH_endolysosomal_gpcr` only `PARK_REVIEW`, with
`no_positive_independent_perturbation_or_model_alignment` and
`crowded_or_approved_prior_art`.

Local support is thin. `wave23_gene_evidence.tsv:2` has only one expression-positive
disease (`Sjogren syndrome`), two expression-negative diseases, no strict residual
support, no Geneformer support, `no_rescue`, and an unconvincing MS white-matter
trend (`ms_wm_delta_log2=0.0904`, `p=0.624`). This is not a cross-autoimmune
module controller signal.

The genetic breadth is also narrower than the rhetoric. The OT credible rows for
`GPR65` are concentrated in MS/Crohn/UC/psoriasis/AS, with zeroes for RA, T1D,
Sjogren, AITD, celiac, and PBC in the local file
`tmp_v3/wave13_opentargets_gwas_credible_sets.tsv:374-385`.

Non-novelty was already identified before Wave23. Wave20 ranked `GPR65` only sixth
and called it `NO_GO`: weak/contradictory local support plus public IBD/GPR65
therapeutic literature and modulator patents
(`results_v3/wave20_genetic_druggable_altaxis/negative_ranked_shortlist.tsv:7`).
The source interpretation is more direct: GPR65 experimental colitis biology
already suggests it as an IBD intervention target, and WO2023067322A1 already
contains autoimmune/MS/AS/IBD/Crohn language
(`results_v3/wave20_genetic_druggable_altaxis/public_source_interpretation.tsv:2-3`).

Operationalization problem: Wave23 treats ChEMBL activity as druggability, but not
as correct-direction biology. `chembl_api_target_snapshot.tsv:23` says 99 scanned
records and best value `364.84 nM`; it does not establish agonist vs antagonist,
PAM vs NAM, pH dependence, immune-cell context, or anti-inflammatory direction.
The route needs pH-specific functional modulation evidence, not generic GPCR
ligand existence.

## 2. `PTPN2` Restoration Is A Modality Story Without A Modality

PTPN2 survived Wave23 because the route table gives it genetics, expression, and
model bookkeeping points. The same row also contains the fatal blocker:
`results_v3/wave23_orchestrator_nonexpression_axis_triage/wave23_route_triage.tsv:3`
states the required direction is TCPTP restoration and the failure is
`modality_blocker_wrong_direction`.

The gene-level evidence is weaker than the route score implies.
`wave23_gene_evidence.tsv:38` shows four expression-positive diseases, but zero
strict residual diseases, no corrected treatment-response signal, no L1000 hits,
and an absent MS anchor (`ms_wm_p=0.984`). The ChEMBL best value (`3.0 nM`) is
not useful unless it is a restorer/activator; the prior Wave20 call already warned
that available chemical feasibility is inhibitor-led and directionally unsafe for
autoimmunity
(`results_v3/wave20_genetic_druggable_altaxis/negative_ranked_shortlist.tsv:2`;
`results_v3/wave20_genetic_druggable_altaxis/public_source_interpretation.tsv:4`).

The foundation/perturbation support is easy to overstate. `foundation_rescue_candidate_rank.tsv:7`
labels PTPN2 as `triage_only_gse162463_not_promotion_grade`; the direct
perturbation columns are empty. `direct_perturbation_evidence_by_candidate.tsv:7`
also lacks a PTPN2 perturbation source/dataset/perturbation and only inherits a
relative MHC-II screen call. That is not a restoration experiment.

The deeper genetics problem remains unresolved. Wave14 explicitly said PTPN2 has
broad disease locus evidence but not target-level causal evidence because full
SNP-level eQTL/GWAS summary data and paired coloc/MR were not available
(`results_v3/wave14_target_level_genetics/target_level_genetics_truth_table.tsv:5`).
Wave23 reused OT disease counts; it did not solve target-resolved causality.

## 3. Baseline Module-Response Biomarker Is Still A No-Go

Wave23 correctly demoted the route to `NO_GO`, but the route is still being kept
alive by nominal-count language. `wave23_route_triage.tsv:7` reports 10 nominal
baseline associations, zero corrected baseline associations, and one corrected
pharmacodynamic signal. That is not a stratification result.

The underlying tables are negative:

- RA anti-TNF `GSE138746`: best visible nominal row is CD4 T `ifn_apc`,
  `p=0.00763`, but `FDR=0.6056`
  (`results_v3/wave18_treatment_response/wave18_gse138746_ra_baseline_response_tests.tsv:23`).
  CD14 monocyte `lysosomal_apc` goes the opposite practical direction and still
  fails correction (`FDR=0.6678`, same table `:17`).
- UC tofacitinib `GSE253006`: baseline rows all sit at `FDR=0.976`
  (`results_v3/wave18_treatment_response/wave18_existing_gse253006_uc_summary.tsv:2-21`).
  The one corrected-ish signal is pharmacodynamic and T-cell/IFN-like, not a
  baseline myeloid/APC stratifier (`:22`).
- Wave18's own recommendation was explicit no-go for baseline prediction from
  current V3 module readouts
  (`subagents_v3/wave18_treatment_response_scout.md:170-184`), and Wave19 set a
  stricter bar requiring two independent response-labeled cohorts and a
  pre-registered interaction model
  (`subagents_v3/wave19_hostile_critique.md:348-367`).

Operationalization problem: a baseline biomarker should be scored on predictive
increment, calibration, treatment-by-module interaction, and external validation.
Wave23 still carries irrelevant target-style fields for this route, including
ChEMBL/L1000 counts (`wave23_route_triage.tsv:7`). Those numbers make a biomarker
look more "druggable" without adding prediction.

## 4. Wave23 Scoring Can Launder Weak Evidence

The script scores any route with `max_geneformer >= 3` as positive perturbation
support (`scripts/v3_wave23_orchestrator_nonexpression_axis_triage.py:476-483`),
even when the supporting table says "triage only" or lacks a direct perturbation.
This matters for PTPN2.

The ChEMBL API handler chooses the first human target returned by search and scans
up to 100 records (`scripts/v3_wave23_orchestrator_nonexpression_axis_triage.py:260-289`).
The output contains obvious target-name oddities, e.g. `APOE` mapping to
`Apolipoprotein B-100` and `IL10RB` mapping to `IL22 Receptor`
(`chembl_api_target_snapshot.tsv:6,28`). That is acceptable for a rough API
snapshot, not for route-level druggability claims.

The response-biomarker gate only counts corrected/nominal rows and pharmacodynamic
rows (`scripts/v3_wave23_orchestrator_nonexpression_axis_triage.py:452-474`).
It does not model clinical covariates, treatment interaction, cohort dependence,
or same-direction replication. That is why nominal RA hits can still decorate a
route that has already failed correction.

## 5. Non-Redundant Route Being Neglected

The neglected route is **target-resolved causal genetics to module state**, not
another target or route table.

Wave20 already specified the next useful data: full summary-stat multi-signal
coloc for `PTPN2`, `GPR65`, `CLEC16A`, `SH2B3`, and `IRF5`; cell-type eQTL/pQTL
instruments; and correct-direction perturbation assays
(`subagents_v3/wave20_genetic_druggable_altaxis.md:242-253`). Wave23 did not run
that route. It counted OT credible disease support from an existing table
(`scripts/v3_wave23_orchestrator_nonexpression_axis_triage.py:350-367`) and then
mixed it with druggability/prior-art penalties.

A non-redundant next test would ask: do disease-risk alleles at `PTPN2` or
`GPR65` actually move the lipid-lysosomal/APC module in the predicted cell type
and direction, after separating locus-level association from target-level
causality? If not, both PARK routes collapse to generic autoimmune genetics plus
weak expression context.

## Short Action List

1. Do not upgrade `GPR65` without pH-dependent agonist/PAM functional evidence in
   disease-relevant human cells and a non-IBD/MS/psoriasis novelty delta over
   existing patents.
2. Do not score PTPN2 inhibitors as autoimmune druggability; require a real
   TCPTP restoration/stabilization or allele-correction modality plus disease-cell
   rescue.
3. Keep the baseline biomarker branch closed unless two independent
   response-labeled cohorts meet a pre-specified interaction/prediction bar.
4. Patch future route scoring to separate generic ligand existence from
   correct-direction modality, and validate ChEMBL target mappings manually for
   top rows.
5. Launch or explicitly block the target-resolved causal-genetics-to-module route
   before spending more effort on PARK labels.

## Changed Files

- `subagents_v3/wave23_hostile_critique.md`
