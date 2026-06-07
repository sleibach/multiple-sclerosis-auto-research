# Lead Inventory V29

Date: 2026-06-07

## Scope

V29 performs a grounded dormant-lead reactivation and cross-domain reframing
pass after V28 settled the bounded APC/HLA-II monitoring lead computationally.
No locked rule was edited. No fresh validation cohort was present or read.

Cross-lineage sub-model status:

- `ANTHROPIC_API_KEY`: absent.
- `GOOGLE_API_KEY`: absent.
- `GEMINI_API_KEY`: absent.

Therefore Workstream A is queued in
`meta/INDEPENDENT_REVIEW_QUEUE_V29.md`; no independent sub-model proposals were
used in this run.

RAG query before analysis:

```bash
.venv_v3_py312/bin/python scripts/query_knowledge_index.py \
  "V29 dormant leads NAMPT MIF CD74 PTGER4 ZMIZ1 KIF21B GPR25 ZFP36L1 TYK2 reactivation" 12
```

Top hits included `meta/NEXT_ACTIONS.md`, `knowledge/candidates/KIF21B.md`,
`knowledge/candidates/GPR25.md`, MIF/CD74 sidecars, V18 data acquisition, and
V16 ZMIZ1/PTGER4 reports. V29 therefore does not re-derive completed cells.

## Workstream B: Dormant-Lead Reactivation

### Summary Table

| Lead | Prior status | V29 re-grade | Reactivated? | Reason |
|---|---|---|---|---|
| APC/HLA-II treatment-response scalar | provisional bounded monitoring lead | top active computational lead, awaiting fresh validation | yes, already active | V28 confirmed statistical tool-robustness; complexity does not improve it. |
| MIF/CD74 axis | demoted as therapeutic mechanism | reactivated only as coupled-axis context / mechanism covariate | partial | V26 shows HLA-II/MIF-CD74 coupling is real, but V27/V28 show receptor/coupled features do not improve prediction. |
| NAMPT/eNAMPT | demoted to marker/readout | remains demoted marker/readout | no | V4/V5 issue was not only prior art; local evidence lacks MS/non-IBD retained residual and no eNAMPT-specific modality evidence. |
| KIF21B chr1 MS-UC | real shared genetics, hard target | remains real biology / difficult target | partial | Current standards strengthened, not weakened, the conclusion: causal evidence favors KIF21B, but risk lowers expression and restoration/up-function is hard. |
| GPR25 chr1 MS-UC | live but weakened causal candidate | remains conditional lead pending controlled data | partial | eQTLGen supports it, but V18 public immune-QTL and atlas evidence do not; agonism/restoration remains immature. |
| ZMIZ1 chr10 MS-Crohn | opposite-direction decoupling | robust decoupling/transfer-validity finding | yes as finding, not target | Same alleles increase ZMIZ1 expression, raise MS risk, and protect Crohn; blocks Crohn-to-MS target transfer. |
| PTGER4 chr5 MS-UC | closed mixed signal | remains closed / transfer warning | no | Mixed shared/distinct components and opposite disease-direction implications still block direction discipline. |
| ZFP36L1 chr14 MS-Crohn | V20 promising, V21 parked suggestive | remains parked suggestive | no | Bounded SuSiE PP.H4 `0.6877` is below robust threshold and direction/QTL coloc absent. |
| REL/PUS10/USP34 chr2 MS-UC | V20 promising, V21 closed | remains closed/not-now | no | Disease SuSiE produced no credible-set summary; expression/QTL context cannot rescue failed disease coloc. |
| TYK2 allosteric subgroup | negative/not-now | remains negative/not-now | no | Druggable class exists, but no MS-specific direction/subgroup anchor independent of generic IFN/JAK biology. |
| FPR2/ALX biased agonism | hard-target real biology | reactivated as wet-lab comparator only | partial | First-principles GPCR tractability exists, but ligand/cargo/context direction must be tested experimentally. |
| Postpartum HLA-II/CD64 APC split | promising natural experiment | reactivated as biomarker/natural-experiment lead | yes as Tier -1/Tier 0 biology | It may connect pregnancy/postpartum flare timing to APC-axis bifurcation; needs postpartum MS cohort. |

### Dormant-Lead Details

#### MIF/CD74

V5 demoted MIF/CD74 as a therapeutic mechanism because receptor-only or full
MIF/CD74 components did not retain adjusted FDR and CD74 collapsed into broad
APC/cell-size context. V26 changes the interpretation, not the therapeutic
verdict: HLA-II and MIF/CD74 receptor-state are strongly coupled across
modalities, so MIF/CD74 is a useful context variable for APC remodeling. V27
and V28 prevent over-promotion: adding receptor/coupling terms diluted or failed
to improve the locked scalar.

V29 verdict: **partial reactivation as mechanism context only**. Do not revive
MIF/CD74 as a direct target or standalone predictor without new perturbation or
compartment evidence.

#### NAMPT

NAMPT was vulnerable to prior-art over-gating earlier, but V4/V5 already
separated generic intracellular NAMPT inhibition from constrained eNAMPT or
marker biology. The retained local facts still kill active nomination:

- MS white-matter delta log2 `-0.214`, p `0.543`.
- Non-IBD retained positive disease count `0`.
- Strict core-covariate surviving disease count `0`.
- OpenTargets genetics score `0.0`.

V29 verdict: **no reactivation**. The corrected modern status is marker/readout
for HIF/NAD/eNAMPT inflammatory metabolism, not a therapeutic lead.

#### KIF21B / GPR25 chr1

V19 corrected the druggability-prior-art trap. The data-favored gene is no
longer dismissed for class reasons:

- KIF21B dense QTD000021 coloc: MS/eQTL PP.H4 `0.8749`, UC/eQTL PP.H4
  `0.8687`.
- Exact shared credible-set variants: risk lowers KIF21B expression `11/11` in
  both MS and UC.
- Direction-matched intervention would require restoration/up-function, not
  simple inhibition.

GPR25 remains live only conditionally:

- eQTLGen/GTEx support protective higher expression.
- Public V18 immune-QTL sources and local atlases do not support measurable
  GPR25 in the relevant compartments.
- Agonism/restoration of a sparsely tooled orphan GPCR remains difficult.

V29 verdict: **reactivated as real biology / controlled-data handoff, not as
current computational target**. The next step remains genotype-linked immune or
CSF protein/cell data, not more local computation.

#### ZMIZ1

V16 established an opposite-direction decoupling:

- shared chr10 variants increase ZMIZ1 expression;
- those alleles are MS-risk and Crohn-protective.

V29 verdict: **reactivated/preserved as a robust transfer-validity finding**.
It should be used to prevent Crohn-to-MS transfer assumptions, not as a direct
therapeutic target.

#### PTGER4

PTGER4 looked attractive because it is druggable and first-pass coloc was high.
Current evidence still blocks it:

- shared component and distinct component coexist;
- disease-direction implications conflict;
- shared causal signal does not map to a clean same-direction intervention.

V29 verdict: **no reactivation**. It remains a negative example: druggability
does not rescue direction-conflicted genetics.

#### ZFP36L1 and REL/PUS10/USP34

These were V20 next-tier genetics leads. V21 already applied the stricter
post-chr1 front-loaded vetting:

- ZFP36L1 chr14: bounded SuSiE max PP.H4 `0.6877`, suggestive but below robust.
- REL/PUS10/USP34 chr2: no SuSiE credible-set summary.

V29 verdict: **no reactivation without new fine-mapped/QTL data**.

## Workstream C: Cross-Domain Reframing

### Metabolic / Immunometabolism Lens

The metabolic lens does not revive NAMPT as a target. It reframes NAMPT as a
readout of inflammatory HIF/NAD stress biology that may covary with APC
remodeling. The actionable use is negative-control or covariate adjustment in
future APC/HLA-II monitoring cohorts:

- If NAMPT/HIF/glycolysis explains the V22 scalar in a fresh cohort, the scalar
  is a generic stress marker.
- If the scalar remains after NAMPT/HIF/glycolysis adjustment, confidence in a
  specific immune-remodeling readout increases.

Outcome: **testable covariate proposal**, not lead reactivation.

### Systems / Dynamics Lens

The systems lens has already been partially tested:

- V26 found a coupled APC architecture.
- V27 showed coupled-axis successors do not beat the scalar.
- V28 showed generic vector/angle/product dynamic features do not beat the
  scalar.

Outcome: **supports simplicity**. The best current dynamical statement is that
therapy-class-aware scalar module movement is more informative than generic
trajectory geometry in the held cohorts.

### Structural / First-Principles Lens

The structural lens changes prioritization only where causality and direction
already exist:

- GPR25: GPCR fold is structurally plausible, but required direction is
  agonism/restoration and chemical matter is immature.
- KIF21B: motor-domain ligandability is plausible by first principles, but the
  needed direction is restoration/up-function, making inhibition/degradation
  wrong-direction.
- FPR2/ALX: GPCR biased agonism is structurally plausible and potentially
  druggable, but without cargo/context-specific perturbation it remains a
  wet-lab comparator, not a computational MS target.

Outcome: **no new intervention-grade target**, but FPR2/ALX remains the
cleanest structural wet-lab comparator for pro-resolution biology.

## Refreshed Ranked Inventory

| Rank | Lead | Current class | What V29 changed | Next requirement |
|---:|---|---|---|---|
| 1 | V22 APC/HLA-II early monitoring scalar | active validation lead | unchanged top lead; V28/V29 argue against added complexity | Fresh paired DMF or immune-remodeling cohort, preferably Gafson/NEDA-4. |
| 2 | Postpartum HLA-II/CD64 APC-axis split | natural-experiment biology lead | promoted as best dormant biology reactivation | Postpartum MS blood/CSF cohort with relapse timing. |
| 3 | ZMIZ1 opposite-direction MS/Crohn locus | transfer-validity finding | preserved as robust decoupling | Publication-grade full-QTL coloc only if writing up. |
| 4 | chr1 KIF21B/GPR25 locus | real genetics / hard-target handoff | reframed as controlled-data problem, not computational target | Genotype-linked immune/CSF expression or protein data. |
| 5 | MIF/CD74 receptor-state coupling | mechanism context | partially reactivated as coupled APC context | Perturbation or compartment evidence; do not use as standalone target. |
| 6 | FPR2/ALX biased pro-resolution agonism | wet-lab comparator | structurally plausible comparator retained | Cargo-specific myelin/efferocytosis perturbation with ligand-bias readout. |
| 7 | NAMPT/eNAMPT | marker/covariate | no target reactivation; useful metabolic stress covariate | Include NAMPT/HIF/glycolysis adjustment in future cohorts. |
| 8 | ZFP36L1 chr14 | parked suggestive genetics | no change | New robust disease-coloc plus allele-aligned QTL direction. |
| 9 | PTGER4 | negative transfer warning | no change | Reopen only with signal-specific cell-type QTL resolving shared component. |
| 10 | REL/PUS10/USP34 chr2 | closed/not-now | no change | New fine-mapped disease signal. |
| 11 | TYK2 allosteric subgroup | negative/not-now | no change | Independent MS subgroup/response anchor. |

## Integrated V29 Verdict

No dormant lead becomes an intervention-grade finding. V29 does sharpen the
project's queue:

1. The top computational/clinical path remains the immutable V22 scalar,
   externally validated on fresh paired treatment-response data.
2. The best dormant biology lead is the postpartum HLA-II/CD64 APC split,
   because it addresses MS natural history and may connect to flare timing.
3. The most important genetics decoupling finding remains ZMIZ1.
4. MIF/CD74 is no longer merely a failed target; it is a useful component of the
   coupled APC architecture, but not a standalone predictor or drug target.
5. NAMPT, PTGER4, ZFP36L1, REL/PUS10/USP34, and generic TYK2 do not reactivate
   under current standards.

The independent cross-lineage model review remains queued and should be run as
soon as `ANTHROPIC_API_KEY` or `GOOGLE_API_KEY` is supplied.
