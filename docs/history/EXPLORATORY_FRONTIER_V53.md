# Exploratory Frontier V53

Date started: 2026-07-10

Status: in progress. V53 is targeted exploratory re-examination and grounded
triage; it does not reopen V41's exhausted public-data discovery search as a
source of findings.

## Evidence Boundary

- Project-data claims below trace to committed, rerunnable tables and scripts.
- Predicted structures are confidence-qualified prediction context, never
  project-grounded evidence or intervention-grade support alone.
- Literature/database knowledge and model/RPT output are proposal/context
  sources only.
- No locked rule or pre-registration is changed.

## Workstream B: MIF/CD74 Therapeutic Angle

### Grounded result: not supported as a therapeutic target

Status: **not-supported for target promotion; retained as a tone-loaded APC
state readout**.

Executable audit:

- `scripts/v53_mif_cd74_grounded_audit.py`
- `analysis/v53_mif_cd74_grounded_audit/REPORT.md`
- `analysis/v53_mif_cd74_grounded_audit/evidence_ledger.tsv`
- `analysis/v53_mif_cd74_grounded_audit/module_definition_audit.tsv`
- `analysis/v53_mif_cd74_grounded_audit/direction_consistency.tsv`
- `analysis/v53_mif_cd74_grounded_audit/summary.json`

The V53 corpus review corrected the initial premise: MIF/CD74 was not wholly
unexamined. Earlier Tier-0/Tier-1 analyses already demoted it after
component-resolved tests. V53 formalized those results against the mature
V26/V36/V38 evidence layers.

Grounded findings:

| question | result | grade |
|---|---|---|
| Is the project module a direct MIF measurement? | No. `MIF` is present in only `3/9` recovered literal module definitions; central V26/V36 source definitions combine CD74/CD44/CXCR4 with HLA-II genes and omit MIF. | negative-established provenance correction |
| Is there an MS state association? | Yes. White-matter microglial receptor-state module delta `0.614`, FDR `0.0192`; the separate MIF-ligand axis is not supported (FDR `0.468`). | supported observational state association only |
| Does receptor state survive broad IFN/APC adjustment across systems? | No Tier-0 residual test survives FDR `<=0.10`; minimum residual FDR `0.442`. | not-supported |
| Does immune CD74 survive APC/size adjustment in MS lesion pseudobulk? | No immune contrast survives correction; minimum residual FDR `0.742`. | not-supported |
| Does receptor/CD74/full state predict treatment response after IFN/APC adjustment? | No adjusted receptor-specific test survives FDR `<=0.10`; minimum adjusted FDR `0.900`. | not-supported |
| Is cross-modality coupling real? | V26 originally supported it, but V53's source-level de-overlap audit retained HLA-II/receptor coupling only in the pharmacodynamic layer; perturbation, cell-state, and response-prediction layers fail their disjoint-readout gates. | context-specific pharmacodynamic coupling; cross-modal two-arm architecture not supported |
| Is the treatment direction stable? | No. With `|Hedges g| >= 0.2`, three therapy cohorts yield one positive, one negative, and one near-null direction; exact and empirical majority-sign p are both `1.0` (`20,000` seeded null draws). | not-supported |

Interpretation:

The grounded project signal is a recurrent CD74/HLA-II APC state, not MIF
ligand causality and not a direction-resolved therapeutic mechanism. Physical
tractability cannot repair missing causal specificity or the therapy-direction
conflict. The prior Tier-1 demotion stands.

A separately segregated source-specific convergence/contradiction check is at
`knowledge_external/synthesis/V53_MIF_CD74_CONVERGENCE_CONTRADICTION.json`.
It identified no same-definition external contradiction and made no change to
the grounded verdict.

Exact data that could change the verdict:

1. An MS lesion or treatment cohort measuring MIF, CD74, CD44, CXCR4, HLA-II,
   cell composition, and clinical outcome together.
2. A pre-specified component-resolved analysis showing MIF/receptor-specific
   signal after HLA-II, IFN/APC, and composition adjustment.
3. A perturbation with a clinically favorable phenotype and the same direction
   in at least one independent MS-relevant system.

## Workstream A: Structure-First APC/HLA-II Angles

Status: complete. Structure was used to assess physical tractability and
interface confidence only; it did not promote MIF/CD74 or any other axis node
without grounded direction and mechanism.

The segregated structure-context pass is recorded at:

- `knowledge_external/structures/alphafold/MIF_P14174/record.json`
- `knowledge_external/structures/alphafold/CD74_P04233/record.json`
- `knowledge_external/synthesis/v53_mif_cd74_structure_context/record.json`
- `knowledge_external/synthesis/V53_MIF_CD74_DIRECTION_MATCHED_ASSESSMENT.json`
- `knowledge_external/synthesis/v53_apc_structure_scout/record.json`
- `knowledge_external/synthesis/v53_apc_structure_scout/apc_structure_scout.tsv`

It does not change the grounded target verdict. The binding constraint remains
the held-data result: no component-specific adjusted support and no stable
therapy direction. Across the broader target-gated map, structural availability
did not remove any existing causal, directional, selectivity, or modality
blocker.

## Workstream C: Combinatorial Intervention Logic

Status: **not-supported for pair prioritization**.

Executable audit:

- `scripts/v53_combinatorial_intervention_probe.py`
- `analysis/v53_combinatorial_intervention_probe/REPORT.md`
- `analysis/v53_combinatorial_intervention_probe/combination_tests.tsv`
- `analysis/v53_combinatorial_intervention_probe/summary.json`

The test used 24 held perturbation-module signatures across IFN-beta,
IFN-gamma, and TNF-alpha contexts. It compared every within-context two-node
pair with the best single node under full-additive and fixed-total assumptions,
using HLA-II plus receptor-state suppression as the target and IFN/APC plus
lysosomal suppression as collateral guardrails.

Across 12 pre-specified tests and 20,000 seeded within-row module-label
permutations, no pair passed BH plus max-T family-wise correction. The strongest
nominal fixed-total TNF-alpha improvement was only `0.0266` (raw `p=0.0138`,
`q=0.166`, max-T FWER `0.9999`). In the IFN-gamma context, `RFX5` remained the
best selective single signature and no pair improved it.

This is not a synergy experiment. It establishes only that the current
single-node perturbation data do not justify prioritizing an additive
combination experiment or a multi-target therapeutic upgrade.

## Workstream D: Cross-Domain Methods

Status: **not-supported for control-node nomination**.

Executable audit:

- `scripts/v53_network_control_probe.py`
- `analysis/v53_network_control_probe/REPORT.md`
- `analysis/v53_network_control_probe/network_edges.tsv`
- `analysis/v53_network_control_probe/stable_adjacency_matrix.tsv`
- `analysis/v53_network_control_probe/control_signature_tests.tsv`
- `analysis/v53_network_control_probe/summary.json`

The bounded control-systems import used the replicated V26 module-dependency
network and 24 held perturbation signatures. The network is explicitly a
symmetric association network, not a causal graph. A control candidate had to
align with selective HLA-II plus receptor-state suppression, spare IFN/APC and
lysosomal collateral, survive 20,000 module-label permutations with BH
correction, and replicate across stimuli.

No perturbation passed the preliminary corrected gate and no node replicated.
`RFX5` was the best fixed-direction signature (goal cosine `0.905`, selective
score `0.588`) but was single-context and non-significant after correction
(`q=0.678`). IFNGR/JAK signatures achieved large target movement only with
larger collateral IFN suppression. The method therefore recovers the existing
selectivity boundary rather than nominating a new control point.

The RFX5 boundary was then made explicit in
`analysis/v53_rfx5_replication_boundary/REPORT.md`. Its single held IFN-gamma
signature is descriptively selective (`HLA-II/APC=-0.706`, receptor-state
`=-0.573`, IFN/APC `=-0.050`), but the network selective-score and cosine
q-values are `0.678` and `0.903`; the older therapeutic route audit passes only
`2/8` gates. It is therefore a nominal mechanism comparator, not a control-node
result and not a target.

The committed follow-up specification requires donor-level RFX5 CRISPRi to
pass the same molecular and collateral gates independently in two primary-human
APC contexts. A three-seed, 450,000-cohort synthetic design map shows that the
two-context design needs 48 donors per context under an assumed standardized
effect of `0.8`, or 32 under effects of `1.0-1.5`, to exceed 80% joint success
probability; an effect of `0.5` does not reach 80% by 96 donors. These are
assumption-labeled method-design results, not an empirical RFX5 effect estimate.
Even molecular replication would not establish a therapeutic route without a
practical partial-modulation modality, functional host-defense preservation,
and an independent MS-relevant anchor.

## Workstream E: Multi-Lineage And RPT Proposals

Status: complete for the first divergent round. Model outputs remained
proposal-only and were grounded before status assignment.

Proposal records and grounding:

- `knowledge_external/model_outputs/v53_unconventional_generation/claude_record.json`
- `knowledge_external/model_outputs/v53_unconventional_generation/gemini_record.json`
- `knowledge_external/model_outputs/v53_unconventional_generation/consolidated_proposals.tsv`
- `scripts/v53_model_proposal_grounding.py`
- `analysis/v53_model_proposal_grounding/REPORT.md`
- `analysis/v53_model_proposal_grounding/proposal_triage.tsv`
- `analysis/v53_causal_identifiability_sensitivity/REPORT.md`
- `knowledge_external/model_outputs/v53_rpt_proposal_lens/record.json`

Claude and Gemini each generated eight proposals. Grounded outcomes across all
16 were: one supported methodological negative, two not-supported, two
inconclusive, and 11 untestable with current data. The high untestable count is
substantive: the V26 matrices contain aggregate contrasts and context summaries,
not patient-level trajectories, temporal series, or complex-structure
predictions.

The one supported item formalized causal non-identifiability. The three-edge
HLA-II/IFN-APC/receptor-state skeleton admits six acyclic orientations in one
Markov-equivalence class, with zero consensus-oriented edges. This establishes
that current summary dependencies cannot identify causal direction; it does not
claim that biological direction is absent.

Sensitivity analysis tested 10 pre-specified strict, permissive,
perturbation-only, replicated, and leave-one-modality-out skeleton rules
spanning three to six edges. Every resulting K3 or K4 variant retained zero
consensus-oriented edges. The methodological negative is therefore not an
edge-threshold artifact within those rules. It is explicitly conditional on a
DAG representation without extra functional-form, invariance, or background
assumptions; cycles and latent common causes were not enumerated and would
broaden current ambiguity.

Claude and Gemini then adversarially reviewed the exact bound. Their seven
objections were proposal-only and were adjudicated in
`analysis/v53_identifiability_critique/REPORT.md`. Six valid wording or
assumption disclosures were incorporated, but zero objections changed a
module-edge verdict. The only new data challenge asked whether perturbing an
exclusive module-member gene could orient the module graph. A committed
membership sensitivity tested all 12 ordered module pairs: zero passed strict
coverage, sign-consistency, magnitude, and readout-nonoverlap requirements.
Gene intervention is not `do(module)`, and the HLA-II/receptor-state modules
share five genes. Current aggregate gene-perturbation signatures therefore do
not repair module-level non-identifiability.

The corrected acquisition boundary is broader and more precise: direction
requires additional direction-informative data or justified identifying
assumptions. True module-level intervention and temporal data are examples;
sample-level identifiable functional-form or cross-environment invariance
models are other possible routes.

V53 then computed the minimal intervention design in
`analysis/v53_causal_orientation_design/REPORT.md`. For the strict complete K3,
one perfect module intervention yields four reachability signatures for six
orders; two interventions distinguish all six. For permissive complete K4,
three interventions are minimal for all 24 orders. Across 594,000 three-seed
synthetic order/design replicates, worst-order recovery first exceeds 80% at
128 donors per arm under an assumed edge coefficient of `0.8` and 192 under
`0.5`; `0.3` does not reach the threshold through 256 donors per arm. This is
method-design characterization, not an empirical APC effect estimate.

The design is not presently executable: RFX5 is not a validated selective
`do(HLA-II/APC)` instrument, IFNGR/JAK perturbs broad IFN tone, and MIF/CD74 has
no component-specific validated intervention. The next causal acquisition
problem is instrument validation, not a more complex orientation algorithm on
the existing summaries.

A cross-environment invariance route was also audited against actual raw-table
headers and row counts. Zero of five candidate routes is orientation-eligible.
The direct-h5ad donor table has five physical environments but incompatible
tissues, compartments, and disease outcomes, with environment directly driving
all module states. RA/IBD has only two non-harmonized response environments.
Mixscale and pharmacodynamic matrices are aggregate and lack validated selective
module interventions. No invariance algorithm was run because it would convert
study/tissue differences into unjustified causal direction. The minimum future
design is at least three exogenous environments, 30 independent donors per
environment, one purified compartment and outcome, the same disjoint scores,
and validated selective perturbations. See
`analysis/v53_invariance_feasibility_audit/REPORT.md`.

A separate definition-overlap sensitivity rebuilt the Mixscale perturbation
matrix from held gene-level effects, matching V26 to maximum absolute error
`4.44e-16`, then removed every gene shared by two modules. The HLA-II/APC versus
receptor-state correlation fell from `rho=0.798` to `0.647`. It remains
significant under a global shuffle (`q=0.0099`) but fails the required
within-stimulus permutation null (`q=0.7665`; original overlapping score
`q=0.0709`). Its paired-bootstrap attenuation interval is `-0.413` to `0.002`,
so attenuation itself narrowly misses establishment.

Interpretation: in the perturbation modality, the disjoint HLA/receptor global
correlation is largely cytokine-context structured and does not establish
within-stimulus coupling. Of the six disjoint module pairs, only GILT/lysosomal
versus IFN/APC survives the context-preserving gate. This weakens the
perturbation-layer formulation of the coupled receptor-state axis but does not,
by itself, re-estimate or demote the V26 architecture supported across four
modalities. No frozen module or locked rule was changed. See
`analysis/v53_deoverlapped_module_sensitivity/REPORT.md`.

The same sensitivity was then executed from the five held cell-state h5ad files
across all 12 V26 donor-level contexts. The original pipeline was reproduced to
maximum donor-score error `9.71e-17` and V26-matrix error `8.33e-17`. After
removing all shared readout genes, the HLA-II/APC versus receptor-state edge
collapses from `rho=0.832` to `0.175` (`q=0.582`); the paired attenuation CI is
`-1.380` to `-0.051`. This establishes that the original cell-state dependency
is materially definition-overlap-sensitive.

This second layer failure triggers a global re-assessment of the coupled-axis
formulation. It does not erase the separately grounded recurrence of an APC
state, but the claim that HLA-II/APC and receptor-state are independently
coupled cannot remain robust without comparable disjoint-readout support in the
treatment-response layers. Those rebuilds are now the highest-priority open
V53 work. No module definition or locked rule has been edited.

The RA/IBD treatment-response layer was then reprocessed from held gene-level
counts and pseudobulk inputs: 46 RA and 30 IBD patients, with the original
20-row V26 matrix reproduced to maximum error `2.22e-16`. HLA-II/APC versus
receptor-state coupling collapses from `rho=0.878` to `-0.059`; disjoint global
and dataset/endpoint-stratified q-values are `0.807` and `0.671`, and the paired
attenuation CI is `-1.361` to `-0.411`.

Three of the four modalities that supported the original edge now fail a
disjoint-readout test. The V26 claim must therefore be regraded now: the data
support a recurrent broad APC/immune-state architecture, but not an
independently coupled HLA-II versus MIF/CD74 receptor-state two-arm architecture
as originally operationalized. The remaining pharmacodynamic rebuild can refine
the scope but cannot restore cross-modality robustness by itself. This regrade
does not edit or retune the locked V22 monitoring rule; it changes the mechanistic
interpretation around that rule.

A direct V22 interface audit confirms that separation mechanically. The locked
file SHA-256 remains
`6373857789e3a538481cebe313ef041792740e4779c7bc705d86494c830e152a`, matching
the V45 baseline. All frozen harness module lists and the Class-C formula
`delta_HLAII - delta_IFN_APC` match; CD74/CD44/CXCR4 remains a negative control
only. V53 changes no score, threshold, preregistration, or result class. Even a
future clean V22 pass could support monitoring performance but not MIF
causality or the demoted independent two-arm architecture. See
`analysis/v53_v22_interpretation_boundary/REPORT.md`.

The final source-level pharmacodynamic rebuild then covered all 24 V26 contexts
across six datasets. It explicitly normalizes two label-only changes in the live
GSE106992 analyzer and reproduces every original matrix cell to maximum error
`2.22e-16`. Unlike the other three layers, the disjoint HLA-II/receptor-state
edge persists: `rho=0.535`, global `q=0.0150`, and dataset-stratified
`q=0.0231`. The matched-context change from the original `rho=0.758` is not
established by paired bootstrap (delta CI `-0.512` to `0.038`).

This positive exception narrows rather than reverses the regrade. It supports a
context-specific pharmacodynamic co-response across heterogeneous therapies,
but one of four source-level modalities cannot establish a robust cross-modal,
independently coupled two-arm architecture. The defensible formulation is now:
a recurrent broad APC state, plus pharmacodynamic HLA-II/receptor co-movement
that requires independent replication and component-resolved mechanism. See
`analysis/v53_pharmacodynamic_deoverlap_sensitivity/REPORT.md`.

The sole positive layer was then stress-tested for portability rather than left
at its pooled result. With 50,000 context-preserving permutations per view, the
global edge remains non-null (`p=0.0131`) and pooled within-dataset ranks remain
concordant (`rho=0.511`, `p=0.0281`). However, after removing dataset means the
association is `rho=0.087` (`p=0.808`), and its 20,000-replicate dataset-cluster
bootstrap interval is `-0.617` to `0.894`. All leave-one-dataset-out global
rhos remain positive (`0.327` to `0.671`), but omitting GSE253006 yields
`p=0.124`, and centered leave-one-out effects include negative values.

The pre-specified portability gate therefore fails. The pharmacodynamic result
is best described as suggestive within-dataset rank concordance embedded in
strong dataset-scale heterogeneity, not a stable common-effect mechanism and
not a therapeutic route. See
`analysis/v53_pharmacodynamic_edge_robustness/REPORT.md`.

Context-semantic decomposition narrows it further. The pooled 24-context edge
has five-partition BH `q=0.0651`, but bulk response strata have `rho=0.109`
(`q=0.463`), while marker-compartment contexts have `rho=0.555` (`q=0.124`)
and GSE253006 alone has `rho=0.624` (`q=0.124`). Excluding GSE253006 gives
`rho=0.327` (`q=0.153`). Across ten favorable-minus-unfavorable response
contrasts, HLA-II and receptor-state changes correlate at only `rho=0.127`
(`q=0.734`), with same-sign changes in `5/10` (`q=0.734`).

The pharmacodynamic relationship is therefore not response-structured. Its
stronger ordering is concentrated in marker-compartment contexts and cannot be
used as response evidence, a monitoring successor, or therapeutic support. See
`analysis/v53_pharmacodynamic_context_decomposition/REPORT.md`.

Finally, the V26 cross-disease summary was rebuilt and source-lineage audited.
Its committed matrix reproduces to `2.22e-16`, but it is not an independent
fifth modality: `108/170` source rows (`63.5%`) reuse the direct-h5ad cell-state
analyses, while the matrix rows are six support-count/positive-effect summaries
derived from those rows. Correlating module columns across those six unlike
summary metrics does not add independent observations. The remaining 62 rows
come from GSE111972, GSE248205, and GSE315138 and are retained for a separate
source-level broad-recurrence audit; they do not make the aggregate matrix an
independent corroboration. See
`analysis/v53_cross_disease_summary_lineage_audit/REPORT.md`.

That source-level audit was then completed with canonical-original and globally
disjoint module rescoring. Exact checks against the unchanged committed source
outputs have zero numerical error. To avoid compartment pseudo-replication and
incomparable effect scales, effects were averaged within each of eight physical
datasets and tested only by direction. IFN/APC and the unique CD44/CXCR4
receptor-state score are each positive in `7/8` datasets (one-sided exact
`p=0.0352`, BH `q=0.0703`, leave-one-out minimum `6/7`). HLA-II is positive in
only `5/8` (`q=0.363`) and lysosomal/APC in `6/8` (`q=0.193`).

Thus a broad cross-disease IFN/receptor-state recurrence survives the overlap
audit, but HLA-II recurrence does not pass the same physical-dataset gate. This
supports a non-specific immune-state backdrop, not the demoted independently
coupled HLA-II/receptor architecture, MS specificity, causal direction, or a
therapeutic target. See
`analysis/v53_additional_atlas_disjoint_rescoring/REPORT.md`.

The independent MS microglia component was then tested more strictly because
its globally unique CD44/CXCR4 score remained elevated after HLA genes were
removed. In 31 GSE111972 sorted-microglia samples from 21 patients, a model
adjusted for region, age, and sex with patient-clustered inference and 100,000
wild-cluster null replicates per outcome gives CD44/CXCR4 disease beta `0.714`
(BH `q=0.0790` across seven pre-specified tests). The state difference is
positive in both white and gray matter.

The stronger decoupling hypothesis fails: CD44/CXCR4 minus CIITA/RFX5 has
`q=0.199`, and CD44/CXCR4 minus MIF/DDT has `q=0.648`; the HLA difference is
not directionally stable across regions. Retain CD44/CXCR4 only as a
provisional single-cohort MS microglial state association requiring independent
replication. It does not establish a distinct causal mechanism, beneficial
intervention direction, selectivity, or a target. See
`analysis/v53_ms_microglia_receptor_decoupling/REPORT.md`.

The retained association survives a pre-specified age, repeated-region, and
influence gate. The patient-level age imbalance is substantial (MS-minus-control
SMD `-0.717`), but patient-equal quadratic-age beta is `0.796` (100,000-draw
wild `p=0.00258`) and common-age-support beta is `0.823` (`p=0.00348`). Every
leave-one-patient-out quadratic beta stays positive (minimum `0.693`), raw
effects are positive in both regions, and the disease-by-region interaction is
not detected (`p=0.814`). This strengthens within-cohort robustness only; it
does not remove the independent-replication, cell-intrinsic, causal, or
therapeutic-direction blockers. See
`analysis/v53_ms_microglia_age_region_robustness/REPORT.md`.

Component specificity does not survive the next gate. CD44 and CXCR4 each have
positive patient-equal quadratic-age effects and focused two-gene BH
`q=0.0225`. However, joint adjustment for CIITA/RFX5, MIF/DDT, unique IFN/APC,
and unique lysosomal scores attenuates the receptor beta by `57.0%`, from
`0.796` to `0.342`, with wild `p=0.105`. The design is numerically stable
(condition number `5.55`) and every leave-one-patient-out adjusted beta remains
positive, but the pre-specified component-specificity gate fails. The retained
label is therefore **broad-state-bounded CD44/CXCR4 association**, not an
independent receptor mechanism. See
`analysis/v53_ms_microglia_component_specificity/REPORT.md`.

A segregated source-specific prior-art audit further narrows novelty without
changing the evidence grade. It classifies the individual CD44/CXCR4
lesion-state biology as low novelty and the exact patient-equal, age/region-
aware, broad-state-adjusted reanalysis as moderate novelty at most. None of the
reviewed sources independently reproduces the frozen two-gene analysis, and no
source supplies an MS-beneficial intervention direction. See
`knowledge_external/synthesis/V53_CD44_CXCR4_MS_MICROGLIA_PRIOR_ART.md`.

The frozen independent-cohort test is now complete on two analyzed partitions
of the public Macnair package, extracted from `2,012,213,369` real sparse-matrix entries without
storing the multi-gigabyte inputs. In the validation composite, deterministic
cross-study donor de-duplication leaves 18 MS and 13 control donors with 11,222
microglia. The frozen primary gives beta `1.414`, standardized effect `2.212`,
wild `p<0.00001`, and HC3 CI `0.806-2.022`; explicit microglia-count adjustment
remains positive (beta `1.075`, wild `p=0.00480`). In the larger discovery
cohort (54 MS, 26 controls; 51,677 microglia), the frozen primary also passes
(beta `0.510`, standardized effect `0.669`, wild `p=0.00461`, CI
`0.142-0.879`). Every fixed 10-100-cell threshold remains positive and
corrected, but explicit log-microglia-count adjustment is borderline (beta
`0.341`, wild `p=0.05398`, CI crossing zero). Joint HLA/MIF/IFN/lysosomal
adjustment remains positive in both matrices (`p=0.00335` and `0.00751`).

This rejects a single-cohort-artifact explanation for the **CD44/CXCR4 state
association**, while retaining a quality qualification for the larger cohort.
It does not establish a receptor-specific causal mechanism: GSE111972 failed
its component-specificity gate, MIF/DDT is sparsely detected in the Macnair
matrices, and therapeutic direction remains absent. See
`analysis/v53_ms_microglia_independent_cohort_scout/REPORT.md`.

The source-lineage audit found zero exact normalized donor-token collisions and
confirmed that three duplicated validation control donors were removed before
modeling. It also establishes a counting limit: the Macnair partitions share
one Zenodo/manuscript package, and cohort-specific anonymized IDs cannot prove
person-level non-overlap. Current wording therefore counts a separate GSE111972
source family plus one Macnair package with two analyzed partitions and three
named validation source studies, not two unqualified publication-independent
Macnair replications. See
`analysis/v53_microglia_source_lineage_audit/REPORT.md`.

A commensurate donor-level synthesis standardized each cohort score and fit the
same disease, age, quadratic-age, and sex adjustment, with study/source fixed
effects for both Macnair partitions. Adjusted effects are positive in GSE111972
(`1.317`), Macnair validation (`1.635`), and Macnair discovery (`0.427`). The
three-partition random-effects estimate is `1.130` (CI `0.419-1.841`), but
heterogeneity is substantial (`I2=65.3%`). A package-aware sensitivity varies
the unknown correlation between Macnair partitions from zero to one; its lowest
pooled CI bound is `0.654`. The exact sign test has only two package-level signs
and is necessarily uninformative (`p=0.5`), so individual frozen wild-null tests
remain primary. See `analysis/v53_microglia_cross_cohort_meta/REPORT.md`.

The pre-declared GSE301908 third-cohort sensitivity is an honest null. The held
object has 14 MS and only 3 control donors, 25,036 deposited Micro nuclei, and a
normalized `data` layer without raw counts. Its adjusted point estimate is
positive (`0.438`), but the HC3 CI is `-1.546` to `2.422` (`p=0.665`) and exact
enumeration of all 680 three-control assignments gives `p=0.478`. It neither
corroborates nor contradicts the association and is not counted as replication.
See `analysis/v53_gse301908_low_control_sensitivity/REPORT.md`.

A final source-family influence test materially downgrades the Macnair discovery
partition. Its 80 donors come from Amsterdam, Edinburgh, and UK MS brain banks,
with strong disease/source association (Cramer's V `0.773`, chi-square
`p=4.18e-11`); the UK source contributes 27 MS and zero controls. Adding source
fixed effects attenuates the standardized discovery beta to `0.427` (HC3 CI
`-0.305` to `1.159`, wild `p=0.245`), and estimable leave-one-bank tests do not
restore correction. In contrast, validation has negligible disease/study
association (V `0.062`), retains beta `1.635` (wild `p<0.00001`), and all three
leave-one-study effects remain positive. The association remains replicated by
GSE111972 plus the validation composite, but discovery is supportive only before
brain-bank adjustment. See `analysis/v53_macnair_source_influence/REPORT.md`.

Fixed-score context localization further shows that the signal is not simply
an overt-lesion readout. In the discovery cohort, normal-appearing white matter
versus control white matter gives adjusted beta `0.783` and context-family
`q=0.01197`, while normal-appearing and lesional grey-matter contrasts are
null. Chronic-active lesion contrasts are positive in both Macnair matrices,
but within-MS paired lesion-minus-NAWM amplification is not detected. SPMS
versus control is positive in both cohorts; however, the direct adequately
sized discovery SPMS-minus-PPMS contrast does not survive its family correction
(`q=0.115`), and validation has only two PPMS donors. Therefore the state is
white-matter-localized and can precede overt lesions, but disease-stage
specificity is not established. See
`analysis/v53_macnair_stage_lesion_heterogeneity/REPORT.md`.

The negative-space proposal failed: among the three module pairs assessable in
all five modalities, there were zero strict forbidden edges (permutation
enrichment `p=1.0`). The bounded transfer-error proposal also failed: across
nine matched aggregate R/NR pairs, nonresponder-minus-responder absolute error
was `-0.0201` for HLA-II and `-0.0135` for receptor-state, with both confidence
intervals crossing zero and corrected one-sided `q=0.641`.

RPT ran 16 leave-one-proposal-out tabular feasibility calls and agreed with all
explicit schema classifications. Because `HELD_SCHEMA_MATCH` directly encodes
the decisive constraint, this is a tooling/consistency check, not independent
scientific corroboration and not a new hypothesis.

The proposal triage exposed a reusable data-semantics risk: aggregate context,
contrast, and dependency rows can look like observations while lacking patient,
time, or intervention identity. V53 therefore froze a machine-readable semantic
contract for all six V26 matrices and audited their current hashes, schemas,
row keys, and allowed capabilities. All 72 real checks pass, and the synthetic
test rejects a patient-level temporal request while accepting a valid
context-level perturbation request. Applied to the proposal set, 12 of 16
matrix-dependent requests are correctly blocked and four pass. This is a
methodological guard only: a blocked request is untestable with these summaries,
not evidence that its biological premise is false. See
`analysis/v53_matrix_semantic_contract/REPORT.md`.

The guard is now fail-closed in the actual proposal-grounding runner. The three
executed proposals declare four matrix/capability requests in
`meta/V53_PROPOSAL_GROUNDING_REQUIREMENTS.json`; all four pass before analysis.
The synthetic regression accepts a valid context-level perturbation request and
rejects an invalid patient-level temporal request. Any future missing capability
now raises before grounding computation starts. This changes execution safety,
not any proposal verdict.

Multi-lineage value verdict: **yes for one methodological boundary, no for a
new biological or therapeutic lead**. The replicated state association instead
arose from the agent-native source-level audit and independent public-cohort
scout. Model confidence played no role. The current client does not expose
monetary spend or token-usage telemetry, so spend is recorded as unavailable
rather than estimated.

Machine-readable navigation is in
`knowledge_external/synthesis/V53_OUTCOME_LEDGER.tsv`: 34 rows carry proposal
source, epistemic class, current outcome, artifact path, SHA-256, and an explicit
interpretation boundary. It lives in the segregated external tree because it
indexes mixed epistemic classes; it is navigation, not evidence. The final V53
regression suite passes 18/18 checks in
`analysis/v53_regression_suite/REPORT.md`.

## Current Ranked Slate

### Grounded-and-promising

1. **Replicated MS microglial CD44/CXCR4 state association, not a target.** The
   original GSE111972 association has same-direction support in the Macnair
   validation composite, which passes frozen, depth-QC, and source-study gates.
   The larger discovery partition passes the frozen and fixed minimum-cell
   tests but attenuates after both cell-count and brain-bank adjustment. This is
   a replicated state marker with a quality qualification, low biological
   novelty, and no intervention direction. It is detectable in normal-appearing
   white matter, but direct stage specificity and paired lesion amplification
   are not established. Next: a donor-balanced third cohort with a pre-specified
   minimum microglial yield and selective functional perturbation.

### Grounded Methodological Boundary

1. Current APC module summaries do not identify causal edge direction. The
   exact equivalence-class result is worth carrying into future experiment
   design, but it is not a therapeutic lead.
2. Cross-environment invariance cannot orient the held data: 0/5 candidate
   routes combine harmonized sample-level variables/outcomes with at least
   three valid exogenous environments or selective interventions.
3. Perturbation-layer HLA-II/receptor-state coupling is not robust to both
   globally disjoint readouts and a cytokine-stratified null.
4. Cell-state HLA-II/receptor-state coupling is definition-overlap-sensitive:
   the disjoint score collapses from `rho=0.832` to `0.175`, with attenuation
   established by paired bootstrap. The recurrent APC state remains distinct
   from an independently coupled two-arm architecture.
5. Treatment-response HLA-II/receptor-state coupling is also
   definition-overlap-sensitive (`rho=0.878` to `-0.059`, attenuation CI wholly
   below zero). With three of four original modalities failing de-overlap, the
   independent two-arm coupled-axis formulation is demoted; broad APC-state
   recurrence remains.
6. Pharmacodynamic HLA-II/receptor-state coupling is the sole disjoint-readout
   exception (`rho=0.535`, global `q=0.0150`, dataset-stratified `q=0.0231`
   across all 24 contexts), but it fails the harder portability gate: centered
   `rho=0.087`, `p=0.808`, cluster-bootstrap CI `-0.617` to `0.894`. Retain it
   only as suggestive rank concordance, not a common-effect mechanism. A
   context decomposition also finds no response structure: ten response
   contrasts give `rho=0.127`, `q=0.734`.
7. The V26 cross-disease summary is a descriptive derived atlas, not a fifth
   independent modality: 63.5% of its source rows duplicate the audited
   direct-h5ad layer, and its six matrix rows are aggregate support metrics.
8. Source-level disjoint rescoring supports broad cross-disease IFN/APC and
   CD44/CXCR4 receptor-state direction recurrence (7/8 physical datasets each,
   BH `q=0.0703`), but not HLA-II (5/8, `q=0.363`). This is a non-specific state
   backdrop, not an MS mechanism or target.

### Promising-but-needs-data

1. **CD44/CXCR4 component specificity and direction.** The state association is
   no longer single-cohort, but GSE111972 component adjustment fails, Macnair
   MIF/DDT controls are sparse, and no selective perturbation identifies causal
   direction. A mechanism or target claim still needs donor-balanced tissue,
   reliable component detection, and selective functional intervention.

MIF/CD74 remains below this tier as a target; its retained value is
state-readout context.

### Not-supported

1. MIF/CD74 as a direction-resolved therapeutic target from currently held
   project data.
2. Additive two-node APC-axis combinations as superior to the best single-node
   signature under the current held perturbation matrix.
3. A replicated selective APC-axis network-control node under the current held
   perturbation and dependency matrices.
4. RFX5 as a corrected, cross-context control node or therapeutic target; its
   current value is limited to a nominal single-context mechanism comparator.
5. The original independently coupled HLA-II/MIF-CD74 two-arm architecture;
   strict disjoint-readout recomputation fails in three supporting modalities.
