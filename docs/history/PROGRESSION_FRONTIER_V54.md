# V54 Progression Frontier

Status: in progress. This report is cumulative and is updated as each
progression-focused probe reaches a grounded, resumable result.

## North-Star Boundary

The clinical objective is to halt disability accumulation in progressive MS.
The held public corpus does **not** contain a transcriptomic cohort with a
longitudinal disability outcome, so no V54 computation can establish that a
state predicts, causes, or can halt progression. V54 can still test bounded
necessary context: cross-sectional progressive subtype differences and
donor-aware chronic-active lesion states. Those are progression-adjacent
associations, not efficacy evidence.

Discovery remains closed under the V41 boundary. V54 performs targeted tests of
pre-existing modules and progression questions; it does not promote an
unexpected public-data pattern as a new finding.

## Progression Data Inventory

Status: **complete; coverage audit, not a biological result**.

Executable audit:

- `scripts/v54_progression_data_inventory.py`
- `analysis/v54_progression_data_inventory/REPORT.md`
- `analysis/v54_progression_data_inventory/progression_data_inventory.tsv`
- `analysis/v54_progression_data_inventory/progression_question_semantic_contract.tsv`

Seven held datasets or packages were audited. Only two bounded question types
are currently testable:

1. Cross-sectional PPMS-versus-SPMS module differences in the Macnair discovery
   package, restricted to Amsterdam and UK sources where both stages occur.
2. Small-donor chronic-active lesion-state contrasts in GSE180759.

Four clinically decisive questions are blocked or non-identifiable: repeated
disability prediction, RRMS-to-progressive transition, treatment-mediated
slowing, and a well-powered RRMS-versus-progressive brain comparison.

The highest-value first test is the source-overlap-restricted PPMS-versus-SPMS
comparison. It has 21 PPMS and 30 SPMS donors after excluding the one Edinburgh
SPMS donor whose source has no PPMS comparator. It remains cross-sectional and
cannot measure progression rate or transition.

## Outcome Ledger

| probe | result | evidence boundary |
|---|---|---|
| Progression-data semantic inventory | complete | Coverage and identifiability audit only; no biological claim. |
| Source-balanced PPMS versus SPMS module comparison | no portable association; CD44/CXCR4 and IFN/APC inconclusive | Cross-sectional disease-stage association only; no transition or progression-rate inference. |
| Chronic-active edge plus foamy-morphology module test | no orthogonally supported module | Non-identical pathology contexts; no disability or treatment inference. |
| Post-result lysosomal morphology specificity | survives tested transcript-state adjustment | Bounded foamy-morphology association only; no orthogonal chronic-active, progression, causal, or therapeutic support. |
| RRMS-to-progressive transition identifiability | not identifiable in seven held datasets | Coverage boundary: no dataset has time-varying stage plus repeated disability/conversion; not a biological null. |
| Second progression-lesion module family | no orthogonally supported module | OXPHOS is lower in foamy morphology but direction-discordant at chronic-active edges; resolution/MOCCI are inconclusive. |
| OXPHOS-lysosomal foamy-state coupling | both survive mutual adjustment | Two separable transcript associations in one morphology cohort; neither has orthogonal progression support. |
| CNS-versus-peripheral progression localization | not identifiable | No held CNS/peripheral pair has a matched phenotype and complete design; GSE228330 baseline subtype is activity-confounded and lacks critical fields. This is not a peripheral null. |
| Progression intervention-direction map | no direction-resolved route | Zero of nine candidates passes the progression-specific first gate; held perturbations supply zero replicated selective control nodes or corrected additive-pair passes. AlphaFold is ineligible at this stage. |
| Foamy-state lesion-stratum transport | not supported | In eligible lesion classes 2 and 3, neither OXPHOS nor lysosomal state passes the four-test family gate; lysosomal direction reverses in class 2. The pooled morphology association is not lesion-stratum portable. |
| Foamy morphology-by-lesion interaction | heterogeneity not supported | Direct class-3-versus-class-2 interactions are near zero with wide intervals and unstable LODO signs. This does not establish homogeneity; the pooled result remains context-bounded and under-resolved. |
| Progression-cohort acquisition contract | complete | Three roles and 64 required fields convert the transition, localization, and intervention-direction blockers into a fail-closed intake specification. No biological claim. |
| Progression-package eligibility validator | synthetic-verified | Six synthetic inventories behave as expected: complete P1/P2/P3 pass and malformed role packages fail closed. Method behavior only. |
| Progression-event power design | synthetic assumption grid complete | 288,000 synthetic cohorts, three seeds; null FPR median 0.043/max 0.060. Only 7/24 non-null scenarios reached 80%; OR 1.25/1.5 did not by n=240. Not an empirical effect. |

## Source/Tissue-Balanced PPMS Versus SPMS Test

Status: **no portable cross-sectional stage association**.

Executable audit:

- frozen plan: `docs/plans/PROGRESSION_STAGE_TEST_V54.md`
- script: `scripts/v54_progressive_stage_modules.py`
- report: `analysis/v54_progressive_stage_modules/REPORT.md`
- machine-readable tests: `analysis/v54_progressive_stage_modules/module_tests.tsv`

The analysis used 44 donors: Amsterdam white matter (12 PPMS, 12 SPMS) and UK
grey matter (8 PPMS, 12 SPMS). Deposited lesion context, age, sex, and
microglial yield were nuisance-adjusted before donor averaging. Three fixed
seeds supplied 300,000 within-source label permutations.

No module passed the frozen HC3, permutation, BH, max-T, and cross-source
direction gate. The primary CD44/CXCR4 score was positive in both sources but
inconclusive: pooled standardized SPMS-minus-PPMS beta `0.343`, HC3 95% CI
`-0.253` to `0.938`, permutation `p=0.279`, BH `q=0.607`, max-T `p=0.787`.
The IFN/APC score was also same-direction but inconclusive. HLA regulation,
MIF ligand, and lysosomal scores changed direction between sources and were
not supported.

This result does not establish equivalence or absence: intervals remain wide.
It does prevent upgrading the V53 CD44/CXCR4 state into a portable progressive-
stage marker from this package. Independent source-balanced tissue with
longitudinal disability remains necessary.

## Chronic-Active Edge And Foamy-Morphology Test

Status: **no orthogonally supported progression-lesion module**.

Executable audit:

- frozen plan: `docs/plans/PROGRESSION_LESION_STATE_TEST_V54.md`
- script: `scripts/v54_progression_lesion_state.py`
- report: `analysis/v54_progression_lesion_state/REPORT.md`
- cross-context outcomes:
  `analysis/v54_progression_lesion_state/cross_context_outcomes.tsv`

GSE180759 was rebuilt from deposited counts as donor x pathology immune
pseudobulks with at least 20 nuclei. Only three donors had paired chronic-active
and chronic-inactive edges, making `0.25` the smallest possible exact two-sided
p-value. GSE279972 contributed 54 foamy/non-foamy MS samples from 21 donors;
models adjusted deposited lesion class and B-cell/APC composition and used
300,000 donor-wild nulls.

No module passed the frozen cross-context rule:

- CD44/CXCR4 was higher at the active edge in all three paired donors (mean
  standardized difference `1.148`, exact `p=0.25`) but was null in the larger
  morphology cohort (adjusted beta `0.025`, wild `p=0.912`).
- Lysosomal state passed the GSE279972 family-wise morphology gate (beta
  `0.493`, wild `p=0.00452`, BH `q=0.0271`, max-T `p=0.0500`, leave-one-donor
  direction retained) but changed active-edge direction across the three
  GSE180759 donors, so it is not an orthogonally supported progression signal.
- Lipid repair was positive in all three active-edge pairs and positive in the
  morphology cohort, but failed max-T control there (`p=0.223`) and remains
  inconclusive.
- HLA regulation, IFN/APC, and complement were direction-discordant or null.

The isolated lysosomal morphology association is a pathology-context result,
not a progression or target result. Because foamy morphology can encode
microglial abundance/state by construction, a post-result composition-
specificity sensitivity is required before even that bounded interpretation is
led with.

## Lysosomal Morphology Specificity Sensitivity

Status: **survives the tested transcript-state adjustments, within a narrow
foamy-morphology boundary**.

Executable audit:

- frozen post-result plan:
  `docs/plans/LYSOSOMAL_MORPHOLOGY_SPECIFICITY_V54.md`
- script: `scripts/v54_lysosomal_morphology_specificity.py`
- report: `analysis/v54_lysosomal_morphology_specificity/REPORT.md`
- model table:
  `analysis/v54_lysosomal_morphology_specificity/specificity_models.tsv`

The base GSE279972 coefficient reproduced exactly. Four fixed models then
added a four-gene resident-microglia identity score, an eight-gene
de-overlapped MIMS score, or both. The fully adjusted foamy-minus-nonfoamy
coefficient was `0.517` (donor-clustered 95% CI `0.199` to `0.834`, donor-wild
`p=0.00861`, max-variant `p=0.0453`). Three independently seeded sets of
100,000 donor-wild replicates agreed, and all 21 leave-one-donor coefficients
were positive (minimum `0.420`).

This supports a reproducible association between the fixed lysosomal score and
foamy morphology after the tested expression-state adjustments. It does **not**
establish measured cell-fraction independence: resident identity and MIMS are
transcript-state proxies and are biologically entangled with foamy activation.
More importantly, the association did not reproduce directionally in the three
paired chronic-active edges. It therefore remains an isolated morphology result,
not a progression-rate marker, causal mechanism, intervention direction, or
route to halting disability.

## RRMS-To-Progressive Transition Identifiability

Status: **not identifiable in the held corpus**.

Executable audit:

- frozen plan:
  `docs/plans/PROGRESSION_TRANSITION_IDENTIFIABILITY_V54.md`
- script: `scripts/v54_transition_identifiability_audit.py`
- report: `analysis/v54_transition_identifiability/REPORT.md`
- dataset matrix:
  `analysis/v54_transition_identifiability/transition_identifiability.tsv`

Seven held progression-adjacent or longitudinal MS datasets were audited
against a five-field contract. Five have a verified subject/donor identifier
and two contain repeated transcriptomes. None contains time-varying MS stage,
and none contains repeated disability or an adjudicated conversion event.

GSE24427 is the nearest longitudinal transcriptomic resource: 25 subjects have
repeated blood measurements during IFN-beta therapy, baseline EDSS, and
two-year relapse outcomes. EDSS is baseline-only, no subtype conversion is
observed, and relapse is not a substitute for disability accumulation.
GSE228330 has nominal baseline, week-2, and month-6 anti-CD20 samples but lacks
a public subject map and disability/outcome labels. The postmortem, pregnancy,
and microbiome datasets answer different bounded questions.

No transition-association analysis is therefore permitted. This is a semantic
and coverage boundary, not evidence that transition biology is absent.

## Second Progression-Lesion Module Family

Status: **no orthogonally supported module**.

Executable audit:

- frozen plan: `docs/plans/PROGRESSION_LESION_MODULE_PANEL_V54.md`
- script: `scripts/v54_progression_lesion_module_panel.py`
- report: `analysis/v54_progression_lesion_module_panel/REPORT.md`
- cross-context outcomes:
  `analysis/v54_progression_lesion_module_panel/cross_context_outcomes.tsv`

Five project-pre-existing modules were tested in the same three paired
chronic-active/chronic-inactive donors and 54 foamy/nonfoamy samples from 21
donors. The morphology models adjusted lesion class, B/APC composition,
resident-microglia identity, and de-overlapped MIMS state, with 300,000
donor-wild nulls and family-wise control.

No module passed the frozen orthogonal-context gate:

- OXPHOS was lower in foamy samples (adjusted beta `-0.622`, clustered 95% CI
  `-1.002` to `-0.242`, donor-wild `p=0.00907`, BH `q=0.0453`, max-module
  `p=0.0357`, leave-one-donor direction retained), but only two of three
  chronic-active pairs had a positive active-minus-inactive difference. The
  contexts are direction-discordant, so this is a bounded morphology result,
  not progression support.
- Resolution/efferocytosis was higher in all three active-edge pairs but null
  in the morphology cohort (beta `0.076`, wild `p=0.693`) and remains
  inconclusive.
- The signed MOCCI switch was higher in all three active-edge pairs and weakly
  positive in morphology (beta `0.303`, wild `p=0.241`), also inconclusive.
- NRF2 antioxidant response and stress/cytotoxicity did not transfer across
  contexts.

Iron handling and cellular senescence remain untested because no frozen
project-local module exists. Resolution/efferocytosis is a transcript proxy,
not measured myelin clearance or remyelination. No disability, causal, target,
or therapeutic-direction claim is supported.

## OXPHOS-Lysosomal Foamy-State Coupling

Status: **both associations survive mutual adjustment in GSE279972**.

Executable audit:

- frozen post-result plan: `docs/plans/OXPHOS_LYSOSOMAL_COUPLING_V54.md`
- script: `scripts/v54_oxphos_lysosomal_coupling.py`
- report: `analysis/v54_oxphos_lysosomal_coupling/REPORT.md`
- tests:
  `analysis/v54_oxphos_lysosomal_coupling/mutual_adjustment_tests.tsv`

After adding the disjoint lysosomal score, the foamy OXPHOS coefficient retained
`90.2%` of its magnitude (beta `-0.562`, clustered 95% CI `-1.003` to
`-0.120`, donor-wild `p=0.0107`, max-endpoint `p=0.0114`). After adding OXPHOS,
the lysosomal coefficient retained `89.7%` (beta `0.463`, CI `0.111` to `0.816`,
wild `p=0.0108`, max-endpoint `p=0.0518`). All 21 leave-one-donor fits retained
both directions, and all three 100,000-replicate seeds agreed.

This establishes only model-level separability of two transcript associations
within one foamy-morphology cohort under the measured covariates. It does not
establish independent biological pathways, metabolic or lysosomal flux,
progression, causality, or an intervention direction. Both remain unreplicated
in the paired chronic-active-edge context.

## CNS-Versus-Peripheral Progression Localization

Status: **not identifiable in the held corpus; coverage/design boundary**.

Executable audit:

- frozen plan: `docs/plans/CNS_PERIPHERAL_PROGRESSION_SEPARATION_V54.md`
- script: `scripts/v54_cns_peripheral_identifiability.py`
- report: `analysis/v54_cns_peripheral_identifiability/REPORT.md`
- evidence matrix:
  `analysis/v54_cns_peripheral_identifiability/compartment_evidence_matrix.tsv`

Zero of four candidate compartment resources forms an eligible
cross-compartment pair. The source-restricted Macnair analysis tests
cross-sectional PPMS versus SPMS in postmortem microglia, but no compatible
peripheral PPMS-versus-SPMS resource exists. The lesion resources encode
pathology morphology rather than clinical stage and have no peripheral
analogue or disability trajectory.

GSE228330 has 15 nominal pretreatment PBMC samples: 10 RRMS and 5 SPMS. Its
deposited activity suffix is strongly imbalanced by subtype (RRMS: 1 active and
9 stable; SPMS: 4 active and 1 stable; two-sided Fisher OR `0.0278`,
`p=0.01698`). The public subject map is unverified, and processed expression,
batch, age, measured cell composition, and disability outcomes are not held.
The comparison therefore fails the frozen eligibility gate before expression
scoring. Processing its public arrays would not repair those design failures.

No peripheral module test was run, so there is no peripheral null. Conversely,
the brain associations cannot be called CNS-intrinsic merely because no
eligible peripheral comparison exists. A valid localization test needs the
same stage or longitudinal disability contrast in CNS/CSF and blood, verified
subjects, adequate group sizes, source/activity/treatment and composition
controls, and a formal compartment interaction.

## Progression Intervention-Direction Map

Status: **no progression-direction-resolved intervention route**.

Executable audit:

- frozen plan: `docs/plans/PROGRESSION_INTERVENTION_DIRECTION_MAP_V54.md`
- script: `scripts/v54_progression_intervention_direction_map.py`
- report: `analysis/v54_progression_intervention_direction_map/REPORT.md`
- candidate map:
  `analysis/v54_progression_intervention_direction_map/progression_intervention_direction_map.tsv`

Nine pre-existing candidate states were tested through a sequential target
gate: progression-specific association, pathogenic direction, causal-node
specificity, selective perturbation, collateral guardrails, and modality fit.
None passed the first gate. CD44/CXCR4 remains a replicated MS microglial
disease-state association but is not progression-specific or component-
specific. OXPHOS-low and lysosomal-high are separable foamy-morphology
associations, but neither transfers across the chronic-active context, measures
flux, or identifies whether the state is damaging, compensatory, or reparative.

The held perturbation layer does not rescue the candidates: 24 signatures
yielded zero replicated selective control nodes, the additive-pair audit had
zero corrected prioritization passes, and ten frozen causal skeleton variants
had zero consensus edge orientations. These are current-data boundaries, not
proof that intervention cannot work.

AlphaFold context was not invoked because no candidate reached the modality-fit
gate. Predicted structure would not resolve progression association, pathogenic
direction, or causal specificity. No V52/V53 target closure changes.

## Foamy-State Lesion-Stratum Transport

Status: **not supported; pooled morphology interpretation narrowed**.

Executable audit:

- frozen plan: `docs/plans/FOAMY_STATE_LESION_STRATUM_TRANSPORT_V54.md`
- script: `scripts/v54_foamy_state_lesion_stratum_transport.py`
- report: `analysis/v54_foamy_state_lesion_stratum_transport/REPORT.md`
- tests: `analysis/v54_foamy_state_lesion_stratum_transport/stratum_tests.tsv`

Deposited lesion classes 2 and 3 passed the frozen pre-score eligibility gate;
NAWM was ineligible because only four foamy donors were available. Four tests
used mutually adjusted OXPHOS/lysosomal scores, donor-clustered intervals,
300,000 donor-wild nulls preserving signs across strata, max-family correction,
and leave-one-donor checks.

Neither endpoint transported. OXPHOS remained lower in foamy samples in both
eligible strata, but class 2 was beta `-0.258` (95% CI `-0.842` to `0.326`,
max-family `p=0.817`) and class 3 was beta `-0.616` (CI `-1.527` to `0.294`,
max-family `p=0.166`). Lysosomal state reversed direction in class 2 (beta
`-0.017`) and was positive but inconclusive in class 3 (beta `0.297`,
max-family `p=0.739`).

The prior pooled, lesion-main-effect-adjusted coefficients therefore do not
support a portable foamy state across adequately represented lesion strata.
This does not prove absence of a morphology association; subgroup intervals are
wide. It further weakens progression and intervention interpretations and
motivates a formal, bounded lesion-by-morphology heterogeneity test rather than
target work.

## Foamy Morphology-By-Lesion Heterogeneity

Status: **heterogeneity not supported; homogeneity not established**.

Executable audit:

- frozen plan: `docs/plans/FOAMY_LESION_HETEROGENEITY_V54.md`
- script: `scripts/v54_foamy_lesion_heterogeneity.py`
- report: `analysis/v54_foamy_lesion_heterogeneity/REPORT.md`
- tests: `analysis/v54_foamy_lesion_heterogeneity/interaction_tests.tsv`

A direct class-3-minus-class-2 foamy interaction was fitted for each mutually
adjusted endpoint over 35 samples from 21 donors, with donor-clustered
intervals, 300,000 no-interaction donor-wild nulls, two-endpoint max-family
control, and leave-one-donor checks. OXPHOS interaction beta was `0.115` (95%
CI `-0.857` to `1.088`, max-family `p=0.940`); lysosomal interaction beta was
`0.004` (CI `-0.677` to `0.686`, max-family `p=1.000`). Neither retained a
stable leave-one-donor sign.

This avoids the error of treating one subgroup's nominal direction and another
subgroup's p-value as formal heterogeneity. The null interactions do not prove
equal effects: intervals are broad and the same data triggered the test. Taken
together with failed stratum transport, the correct label is **pooled,
lesion-context-bounded morphology association with unresolved transport**, not
a portable lesion program.

## Progression-Cohort Acquisition Contract

Status: **complete operational specification; no biological claim**.

Artifacts:

- `docs/validation/PROGRESSION_COHORT_ACQUISITION_SPEC_V54.md`
- `docs/validation/input_schemas/V54_progression_cohort_required_fields.tsv`

The contract separates three roles that the held corpus cannot currently
support: longitudinal disability/PIRA association, paired CNS/CSF-versus-blood
localization, and functional intervention direction. Its 64 unique required
fields include verified subject/visit links, raw disability components and
protocol definitions, relapse/steroid/infection and treatment history, MRI and
optional paramagnetic-rim lesion time, expression/QC/batch/composition, paired
compartment links, and perturbation functional/collateral readouts.

Relapse, cross-sectional stage, lesion morphology, and pharmacodynamics are
explicitly prohibited as substitutes for disability accumulation. The contract
does not assert a powered progression sample size from the current data; fewer
than 10 independent events is descriptive-only, while every larger received
cohort still requires a pre-score power simulation and frozen outcome/timepoint
plan. Missing critical fields fail the relevant role closed rather than
becoming a biological null.

The nearest open peripheral candidate now has a precise unsent addendum:
`docs/validation/outbound_requests/gse228330_progression_metadata_addendum_V54.md`.
Its 29-field request asks for the verified subject map, activity-suffix
definition, age, disability/PIRA components and protocol, relapse/steroid and
treatment timing, imaging, cell counts, batch/QC, and processed expression. The
document preserves GSE228330 as pharmacodynamic context unless the returned
package independently passes the P1/P2 role gates; it cannot substitute for the
DMF/Gafson validation route.

The field contract is machine-enforced by
`scripts/v54_progression_package_eligibility_validator.py`, documented in
`docs/validation/PROGRESSION_PACKAGE_ELIGIBILITY_VALIDATOR_V54.md`. Six seeded,
clearly labeled synthetic inventory regressions all behave as specified: three
complete P1/P2/P3 fixtures pass and three fixtures missing outcome, pairing, or
functional/prequalification fields fail closed. Real-package source paths must
exist. A pass means only inventory-complete enough for blinded pre-registration
and data-level validation; it is not a data-quality or biological result.

## Progression-Event Power Design

Status: **synthetic assumption grid complete; no biological claim**.

Artifacts:

- script: `scripts/v54_progression_event_power_design.py`
- documentation: `docs/validation/PROGRESSION_EVENT_POWER_DESIGN_V54.md`
- report: `analysis/v54_progression_event_power_design/REPORT.md`
- full grid: `analysis/v54_progression_event_power_design/power_grid.tsv`

The parameterized simulator generated 288,000 synthetic cohorts over 192 grid
cells and three seeds, varying N, progression-event rate, assumed odds ratio,
20% molecular missingness, and one versus two noisy molecular measurements at
reliability 0.70. It fits one frozen logistic Wald test and treats cohorts with
fewer than five events or non-events as inconclusive.

Null calibration was acceptable for this synthetic design (median grid-cell
false-positive rate `0.043`, maximum `0.060`). Only 7 of 24 non-null assumption
scenarios reached the pre-declared 80% conclusive threshold with every seed at
least 75%. No OR `1.25` or `1.5` scenario reached 80% by `n=240`. OR `2.0`
required `n=120-240` in the scenarios that passed; 15% event rate plus 20%
missingness and one repeat still did not reach 80% at `n=240`.

These are conditional method-design results, not empirical MS effect sizes or a
universal recruitment target. The interface must be rerun from blinded receipt
metadata using the actual event rate, missingness, repeat structure, endpoint,
and multiplicity plan before any molecular score is viewed.
