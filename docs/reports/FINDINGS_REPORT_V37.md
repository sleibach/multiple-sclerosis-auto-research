# Findings Report V37

Date: 2026-06-07

Scope: synthesis and scoring only. No new hypotheses, no new analysis, and no
rule changes were made for this report. Scores trace to committed project
artifacts and separate scientific relevance from novelty.

## Executive Summary

The project has not produced an intervention-grade MS target or a clinically
validated biomarker. Its strongest current result is a **provisional,
pre-locked early-treatment monitoring signal**: the bounded APC/HLA-II scalar
from V22/V23, later shown in V28/V32 to be statistically tool-robust and not
explained away by glucocorticoid or simple composition artifacts, but still
small-n, immune-tone bounded, and awaiting external validation.

The most novel supported contribution is not a single target. It is the
project's layer-specific transfer-validity map and deep APC-axis structure:
MS-adjacent autoimmune biology transfers by biological layer, not by disease
label, and the most reproducible held-data structure is a coupled APC
remodeling architecture linking HLA-II, IFN/APC, MIF/CD74 receptor state, IFN
readout, and lysosomal processing.

The candid bottom line: the project has a useful, disciplined map of what is
real, what is promising, and what is dead. It has a primary validation lead and
several mechanistic contexts. It does **not** yet have a cure-class finding, a
direction-matched druggable genetics target, a validated simulator, or a
prospective clinical rule.

## Scoring Rubric

Scientific relevance:

- `5`: could materially affect MS clinical decision-making or therapeutic
  strategy if validated.
- `4`: materially improves MS mechanism or transfer-validity interpretation.
- `3`: useful biological or translational context, but not directly actionable.
- `2`: minor or mainly cautionary result.
- `1`: low MS relevance, retained for audit completeness.

Novelty:

- `5`: likely highly novel under the project's prior-art standard.
- `4`: non-obvious cross-axis or negative/decoupling contribution.
- `3`: useful reframing or rigorous test of partly known biology.
- `2`: largely known biology re-derived or operationalized.
- `1`: routine or mostly operational.

Evidence grade:

- `robust`: formal or repeated evidence with appropriate controls for the
  stated claim.
- `supported`: grounded in committed data analyses, but not definitive external
  validation.
- `provisional`: promising, small-n, data-limited, or missing a required
  external replication.
- `negative-established`: a lead or claim was tested sufficiently to close,
  kill, or downgrade under current standards.
- `speculative`: proposal-only or insufficiently grounded. No speculative item
  is promoted in the scored table.

## Scored Findings Table

| # | Item | Category | Relevance | Novelty | Evidence grade | Supporting artifact(s) | Status / next need |
|---:|---|---|---:|---:|---|---|---|
| 1 | Bounded APC/HLA-II early treatment-response monitoring scalar | Positive | 5 | 4 | provisional | `docs/findings/FINDING_V22.md`; `docs/locked_rules/LOCKED_RULE_V22.md` | Primary validation lead; needs fresh paired MS DMT cohort. |
| 2 | Tool-robust but simple V22 scalar | Methodological | 4 | 3 | supported | `docs/workups/treatment_response/ROBUSTNESS_MAP_V28.md` | Validate scalar; do not add flexible ML/coupled complexity. |
| 3 | V22 scalar is immune-tone bounded, not steroid/composition artifact | Methodological | 4 | 3 | supported | `docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md` | Future validation must report confounder-adjusted panels. |
| 4 | Coupled APC remodeling architecture | Positive | 4 | 4 | supported | `docs/findings/DEEP_STRUCTURE_V26.md` | Mechanistic context; not a drug target or clinical rule. |
| 5 | MS-UC is strongest tested genome-wide genetics comparator | Positive | 4 | 2 | robust | `docs/history/LEAD_SLATE_V21.md` | Backdrop result; important but low novelty. |
| 6 | Layer-specific autoimmune transfer-validity map | Positive | 4 | 4 | supported | `docs/findings/AXIS_DISAGREEMENT_FINDINGS_V12.md` | Use axes, not disease labels, for transfer claims. |
| 7 | Mucosal IBD early IFN/APC downshift validates while baseline fallback fails | Positive / negative split | 4 | 3 | supported | `docs/findings/KILL_HYP_V6_006.md` | Dynamic readout survives in mucosa; baseline fallback killed. |
| 8 | IFN-beta HLA-II/CD74 branch | Positive | 3 | 3 | provisional | `docs/history/HYPOTHESIS_SLATE_V36.md`; `analysis/v36_ms_ifnb_longitudinal_audit/` | Therapy-specific context; not primary monitoring rule. |
| 9 | T/B-readable early IFN/APC/STAT1 monitoring state | Positive | 3 | 4 | provisional | `docs/history/HYPOTHESIS_SLATE_V36.md` | Secondary audit layer; replication-gated and composition/QC-conditioned. |
| 10 | Postpartum HLA-II/CD64 APC-arm imbalance | Positive | 3 | 4 | provisional | `docs/history/HYPOTHESIS_SLATE_V35.md`; `docs/history/HYPOTHESIS_SLATE_V36.md` | Clinically anchored natural experiment; needs MS postpartum relapse data. |
| 11 | ZMIZ1 opposite-direction MS/Crohn decoupling | Decoupling | 3 | 4 | supported | `docs/workups/genetics/GENETICS_EQTL_WORKUP_V16.md`; `docs/history/LEAD_INVENTORY_V29.md` | Transfer-validity finding; not a target. |
| 12 | chr1 KIF21B/GPR25 locus is real biology but hard target | Decoupling / hard target | 3 | 3 | supported | `docs/workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md` | Controlled-data handoff; no intervention claim. |
| 13 | PTGER4 mixed shared/distinct signal closes naive transfer | Closed lead | 3 | 3 | negative-established | `docs/workups/genetics/GENETICS_EQTL_WORKUP_V16.md`; `docs/history/LEAD_INVENTORY_V29.md` | Closed unless signal-specific cell-type QTL resolves direction. |
| 14 | MHC overlap is distinct-signal, not simple shared biology | Negative relationship | 3 | 2 | negative-established | `analysis/v14_locus_landscape/REPORT.md`; `analysis/v14_susie_coloc/REPORT.md` | Do not overread HLA overlap as shared causal variant. |
| 15 | UC genetics vs treatment-response layer split | Decoupling | 4 | 3 | supported | `docs/findings/AXIS_DISAGREEMENT_FINDINGS_V12.md` | Genetic proximity does not imply baseline biomarker transfer. |
| 16 | Crohn downstream IFN/APC convergence exceeds genetic proximity | Decoupling | 3 | 3 | supported | `docs/findings/AXIS_DISAGREEMENT_FINDINGS_V12.md` | Crohn informs response-monitoring analogies, not genetic targets. |
| 17 | RA pregnancy comparator but blood APC treatment-response nontransfer | Decoupling | 3 | 3 | supported | `docs/findings/AXIS_DISAGREEMENT_FINDINGS_V12.md` | Use RA for postpartum timing, not blood APC biomarker transfer. |
| 18 | Sjogren antigen-presentation but not lysosomal/APC lesion-rim transfer | Decoupling | 2 | 3 | supported | `docs/findings/AXIS_DISAGREEMENT_FINDINGS_V12.md` | Limited comparator role. |
| 19 | No load-bearing invariant found in V26 | Negative | 2 | 4 | negative-established | `docs/findings/DEEP_STRUCTURE_V26.md` | Do not claim conserved invariant. |
| 20 | No validated broad immune-state simulator from held data | Kill / negative | 4 | 3 | negative-established | `docs/workups/treatment_response/MODEL_CARD_V25.md`; `analysis/v25_immune_state_model/model_validation_summary.json` | Use only low-resolution bounded-domain priors. |
| 21 | Coupled-axis successor rule does not beat scalar | Kill / negative | 4 | 3 | negative-established | `analysis/v27_coupled_axis/v27_scalar_vs_coupled_metrics.tsv`; `docs/history/LEAD_INVENTORY_V29.md` | No V27 successor locked. |
| 22 | Locked V7 general cross-disease baseline fallback killed | Kill | 4 | 3 | negative-established | `docs/findings/KILL_HYP_V6_006.md` | Baseline fallback rejected; dynamic mucosal IBD retained. |
| 23 | GPR25 demoted from protected favorite | Closed / demoted | 3 | 3 | negative-established | `docs/workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md` | Conditional candidate only; no current intervention-grade status. |
| 24 | NAMPT/eNAMPT not reactivated as target | Closed | 2 | 2 | negative-established | `docs/history/LEAD_INVENTORY_V29.md` | Marker/covariate only. |
| 25 | ZFP36L1 chr14 parked | Parked | 2 | 2 | provisional | `docs/history/LEAD_SLATE_V21.md` | Needs robust coloc and allele-aligned QTL direction. |
| 26 | REL/PUS10/USP34 chr2 closed | Closed | 2 | 2 | negative-established | `docs/history/LEAD_SLATE_V21.md` | No disease SuSiE-coloc summary. |
| 27 | EBV/IFN APC imprint downgraded by specificity control | Closed / downgraded | 3 | 3 | negative-established | `docs/history/HYPOTHESIS_SLATE_V35.md`; `docs/history/HYPOTHESIS_SLATE_V36.md` | Reopen only with EBV-stratified B-cell/APC data. |
| 28 | Complement/lipid progressive axis downgraded | Closed / downgraded | 2 | 3 | negative-established | `docs/history/HYPOTHESIS_SLATE_V35.md`; `docs/history/HYPOTHESIS_SLATE_V36.md` | Weak lipid context only. |
| 29 | Lysosomal APC bottleneck not proven | Parked | 3 | 3 | provisional | `docs/history/HYPOTHESIS_SLATE_V35.md`; `docs/history/HYPOTHESIS_SLATE_V36.md` | Strong coupling, no bottleneck proof. |
| 30 | Metabolic/sterol setpoint is context/confounder axis | Parked | 3 | 2 | provisional | `docs/history/HYPOTHESIS_SLATE_V35.md`; `docs/history/HYPOTHESIS_SLATE_V36.md` | Use as covariate/context, not target. |
| 31 | Multi-lineage and RPT lenses add prioritization, not evidence | Methodological | 2 | 3 | supported | `docs/history/LEAD_INVENTORY_V31.md`; `docs/history/HYPOTHESIS_SLATE_V36.md` | Keep model output proposal-only. |
| 32 | First-principles druggability discipline changed target interpretation | Methodological | 4 | 4 | supported | `docs/workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md` | Do not use class precedent as druggability shortcut. |

Machine-readable version: `docs/reports/FINDINGS_SCORES_V37.tsv`.

## Grouped Narrative

### Positive / Supported Results

The most clinically relevant positive result is the V22/V23 bounded
APC/HLA-II early-treatment monitoring scalar. It was locked before validation
and then tested without tuning. The outcome is mixed: DMF passes
directionally, fingolimod and adalimumab fail, and tofacitinib is numerically
strong but caveated by module/compartment issues. V28 then showed the scalar is
more robust than receptor-only, coupled, dynamic-vector, or flexible ML
variants. V32 showed it is not explained by the highest-risk steroid or simple
composition controls, although broad immune-tone/STAT1/metabolic adjustment
attenuates it. This is the primary validation lead, but it is not a validated
clinical rule.

V26 adds a mechanistic backbone: a recurrent APC remodeling architecture links
HLA-II, IFN/APC, MIF/CD74 receptor state, IFN readout, and lysosomal processing
across held module matrices. This supports interpreting the monitoring signal
as coordinated immune remodeling rather than a single-gene target. It does not
create a successor rule, and V27/V28 explicitly argue against adding
complexity before fresh validation.

The genetics backdrop is now clear enough to contextualize loci. V21 LDSC
places MS-UC as the strongest tested genome-wide genetic relationship
(`rg = 0.3342`), with SLE, RA, and Crohn lower. This is relevant but not highly
novel: MS-UC/autoimmune genetic proximity is already expected. The project's
novel value is integrating this backdrop with locus-specific transfer failures.

V12's axis-disagreement map is one of the project's more novel supported
products. It established that mechanisms transfer by biological layer rather
than disease label: UC is genetically close to MS, Crohn and UC support
downstream mucosal IFN/APC response-monitoring analogies, RA is useful for
pregnancy/postpartum timing but not blood APC treatment-response transfer, and
Sjogren supports antigen-presentation comparison without proving
lysosomal/lesion-rim biology.

### Decoupling And Negative-Relationship Findings

ZMIZ1 is the cleanest genetics decoupling. V16 established that the same
expression-increasing alleles are MS-risk and Crohn-protective at the chr10
shared locus. This is not a therapeutic target claim; it is a transfer-validity
warning. It matters because it prevents naive Crohn-to-MS therapeutic transfer
at that locus.

The chr1 MS-UC locus is real but not intervention-ready. The project trajectory
is important: GPR25 initially looked like the attractive GPCR lead, but V18/V19
shifted the evidence toward KIF21B in public immune-QTL data and exposed that
both plausible directions require restoration/up-function rather than easy
inhibition. V19 also corrected the project's earlier class-precedent bias:
GPCR status does not make GPR25 actionable, and kinesin class difficulty does
not make KIF21B ignorable. The result is a real biology / hard-target handoff,
not a medical-team therapeutic candidate.

PTGER4 is the clearest cautionary example. It began as the exciting druggable
MS-UC locus, but multi-signal and allele-aligned direction work showed mixed
shared and distinct components with conflicting disease-direction implications.
Druggability does not rescue a direction-conflicted genetics signal. PTGER4 is
therefore closed as a naive transfer target.

The MHC/HLA overlap is also a negative relationship: overlapping autoimmune
signals favored distinct causal variants in MHC windows rather than a simple
shared causal variant. This is lower novelty, but high caution value because
HLA overlap is easy to overinterpret.

### Kills, Closed Leads, And Parked Results

The V7 general cross-disease baseline fallback is killed. Three independent
in-scope cohorts failed the baseline/general rule, while mucosal IBD dynamic
IFN/APC downshift remained supported. This is a useful kill: it converted a
failed broad stratifier into a narrower dynamic-monitoring principle.

V25 is a negative-established modeling result. The project attempted a bounded
in-silico immune-state model and found only low-resolution directional utility
inside Mixscale-like IFNB/IFNG/TNFA pathway contexts. It is not valid for
patient-level response prediction, single-cell simulation, genetics-only
expression-direction hypotheses, or unseen pathways. That negative prevents
overtrusting a simulator the current data cannot support.

V26 found no load-bearing invariant, despite visually consistent relationships.
This matters because deep methods are prone to attractive artifacts. The report
therefore keeps the supported shared APC remodeling axis but rejects invariant
claims.

V27/V28 closed the coupled-axis successor-rule idea. Coupled features are
mechanistically interesting, but they did not fairly beat the scalar after
small-n and flexibility concerns. No V27 successor was locked.

The exploratory slates contain many honest downgrades. EBV/IFN APC imprint
failed module-specificity controls and should not be revived without
EBV-stratified B-cell/APC data. Complement/lipid progressive-axis evidence
downgraded under donor-aware lesion analysis. Lysosomal APC remains a strong
coupling idea but lacks bottleneck proof. Metabolic/sterol is useful as
context and confounder control, not an intervention-grade axis. NAMPT/eNAMPT
remains a marker/covariate, not a target. ZFP36L1 is parked below robust
colocalization threshold; REL/PUS10/USP34 is closed because the disease coloc
screen failed.

### Methodological / Operational Findings

The project repeatedly found that complexity is not credibility. Flexible ML,
coupled-axis features, receptor-only controls, RPT predictions, and
multi-lineage model suggestions generated useful critiques and prioritization,
but none became evidence without real-data grounding. In V36, post-hoc
perfect-AUC features appeared in tiny cohorts often enough under permutation
that they were demoted to secondary audits.

The most important methodological correction was the first-principles
druggability discipline in V19. The project stopped treating "GPCR" as
actionable by default and stopped treating "kinesin" as undruggable by default.
Targetability now requires causal-gene support, direction, structural
tractability, modality fit, and evidence that the tractable modality moves the
disease-protective direction.

Multi-lineage and RPT tools added value, but mostly by sharpening failure
modes. Claude/Gemini review led directly to the V32 confounder audit. RPT in
V36 surfaced structural tensions in the slate. None of those model outputs are
facts; they are ranked proposals. This methodological result is important
because it keeps the expanded toolchain useful without lowering the evidence
bar.

## Honest Bottom Line

Validated:

- No prospective clinical rule is validated.
- No intervention-grade target is validated.
- The LDSC genetic-correlation backdrop and several negative/decoupling
  genetics conclusions are robust enough for internal decision-making.

Provisional:

- The bounded APC/HLA-II early monitoring scalar is the primary provisional
  clinical/translational lead.
- The T/B-readable IFN/APC/STAT1 state, IFN-beta HLA-II/CD74 branch, and
  postpartum APC-arm imbalance are promising but replication/data-gated.

Negative-established:

- The V7 baseline fallback is killed.
- PTGER4 is closed as a naive transfer target.
- GPR25 is demoted from protected favorite.
- No broad simulator is validated from current data.
- Coupled-axis successors do not beat the scalar.
- EBV-specific, complement/lipid, NAMPT, REL/PUS10/USP34, and generic TYK2
  directions are not active leads under current evidence.

Awaiting external data:

- Gafson et al. 2018 DMF PBMC RNA-seq with NEDA-4 labels is the highest-leverage
  validation dataset for the locked V22 scalar and V32/V36 audits.
- A compartment-resolved paired response cohort is needed to replicate or kill
  the T/B-readable monitoring state.
- Postpartum MS blood/CSF immune data with relapse timing are needed to test
  the postpartum APC-arm hypothesis.
- Genotype-linked immune/CSF expression or protein data are needed to resolve
  chr1 KIF21B/GPR25 publication-grade causality.

Not achieved:

- No cure-class or intervention-grade MS therapeutic hypothesis.
- No direction-matched druggable genetics target ready for wet-lab pursuit.
- No validated baseline treatment stratifier.
- No validated immune-state simulator.
- No new locked successor rule beyond the immutable V22 scalar.

## For The Medical Team

Priority is sorted by relevance times evidence, not by novelty alone.

1. **Validate the V22/V23 bounded APC/HLA-II scalar.**
   - Why it matters: highest relevance; could become an early monitoring rule
     for DMF-like immune-remodeling contexts.
   - Evidence: V22 locked validation mixed; V28 tool-robust; V32 not explained
     by steroid/composition; V36 clarified audits.
   - Need: Gafson DMF PBMC RNA-seq processed counts plus NEDA-4 labels.

2. **Treat the V36 IFN/APC/STAT1/T/B-readable state as secondary audit, not as
   a new rule.**
   - Why it matters: may explain which compartments carry the monitoring
     signal.
   - Evidence: internally supported but small-n and post-hoc; multiplicity
     stress demotes it.
   - Need: independent compartment-resolved paired response cohort.

3. **Use ZMIZ1 as a transfer-validity warning.**
   - Why it matters: prevents Crohn-to-MS therapeutic inference at a real
     shared locus.
   - Evidence: allele-aligned opposite-direction eQTL/disease result.
   - Need: only publication-grade full-QTL colocalization if writing up.

4. **Keep chr1 KIF21B/GPR25 as a controlled-data handoff, not a therapeutic
   lead.**
   - Why it matters: real shared MS-UC genetics; target direction/druggability
     unfavorable.
   - Evidence: V19 dense QTL and druggability re-evaluation.
   - Need: genotype-linked immune/CSF expression/protein data.

5. **Acquire postpartum MS relapse-window immune data if natural-history
   biology is a priority.**
   - Why it matters: best dormant biology lead, clinically anchored to relapse
     timing.
   - Evidence: cross-disease and MS pregnancy-phase support, but no postpartum
     MS relapse-labeled validation.
   - Need: postpartum blood/CSF immune profiles with DMT restart/stop, steroids,
     lactation, infection, cell counts, and relapse timing.

6. **Do not spend wet-lab budget on closed target claims without new data.**
   - PTGER4, NAMPT, REL/PUS10/USP34, generic TYK2, EBV-specific imprint, and
     complement/lipid progressive claims are closed, downgraded, or data-gated
     under current evidence.

## Model Review

Optional Claude/Gemini review was not used for V37 scoring. `SAP_AI_CORE_API_KEY`
was present after explicitly loading `.env`, but this iteration's mandate was
synthesis from committed artifacts, and the scores were assigned directly from
those artifacts. Prior model/RPT outputs remain proposal/prioritization signals
only, never evidence.
