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
| Source-by-stage interaction audit | no supported interaction | Five-module, 300,000-null sensitivity. Same-sign source effects remain descriptive; source/tissue equivalence is not established. |
| Chronic-active edge plus foamy-morphology module test | no orthogonally supported module | Non-identical pathology contexts; no disability or treatment inference. |
| Post-result lysosomal morphology specificity | exploratory after global sequential-family correction | Fully adjusted endpoint passes its local family but not Holm across all 12 post-result morphology tests (`p=0.0861`). |
| RRMS-to-progressive transition identifiability | not identifiable in seven held datasets | Coverage boundary: no dataset has time-varying stage plus repeated disability/conversion; not a biological null. |
| Second progression-lesion module family | no orthogonally supported module | OXPHOS is lower in foamy morphology but direction-discordant at chronic-active edges; resolution/MOCCI are inconclusive. |
| OXPHOS-lysosomal foamy-state coupling | exploratory after global sequential-family correction | Local mutual-adjustment gates pass, but neither endpoint passes Holm across the complete 12-test post-result family. |
| CNS-versus-peripheral progression localization | not identifiable | No held CNS/peripheral pair has a matched phenotype and complete design; GSE228330 baseline subtype is activity-confounded and lacks critical fields. This is not a peripheral null. |
| Progression intervention-direction map | no direction-resolved route | Zero of nine candidates passes the progression-specific first gate; held perturbations supply zero replicated selective control nodes or corrected additive-pair passes. AlphaFold is ineligible at this stage. |
| Foamy-state lesion-stratum transport | not supported | In eligible lesion classes 2 and 3, neither OXPHOS nor lysosomal state passes the four-test family gate; lysosomal direction reverses in class 2. The pooled morphology association is not lesion-stratum portable. |
| Foamy morphology-by-lesion interaction | heterogeneity not supported | Direct class-3-versus-class-2 interactions are near zero with wide intervals and unstable LODO signs. This does not establish homogeneity; the pooled result remains context-bounded and under-resolved. |
| Foamy within-donor estimand audit | not supported | Only 6/21 donors and 3/43 donor-by-lesion blocks vary in morphology. OXPHOS is direction-retained but unstable/null within donors; lysosomal reverses near zero. |
| Progression-cohort acquisition contract | complete | Three roles and 64 required fields convert the transition, localization, and intervention-direction blockers into a fail-closed intake specification. No biological claim. |
| Progression candidate role matrix | 0/10 candidates eligible for P1/P2/P3 | Metadata-only classification keeps monitoring, pharmacodynamic, pathology, and progression roles separate. Acquisition boundary, not biological null. |
| Progression-package eligibility validator | synthetic-verified and path bug fixed | Fourteen synthetic inventories cover roles, malformed schemas, aliases, verification, nonmissing counts, and real-path behavior. A discovered missing-path pass bug was fixed. Method behavior only. |
| Blinded P1/P2 pre-registration and endpoint semantic gate | synthetic-verified | Three valid disability declarations pass and nine proxy, incomplete, unconfirmed, or unblinded declarations fail closed. Method behavior only. |
| Progression-event power design | synthetic assumption grid complete | 288,000 synthetic cohorts, three seeds; null FPR median 0.043/max 0.060. Only 7/24 non-null scenarios reached 80%; OR 1.25/1.5 did not by n=240. Not an empirical effect. |
| Progression-power null calibration | acceptable | The 0.060 maximum is 90/1,500 (Wilson 0.049-0.073); no cell's lower bound exceeds 0.05 and the 48-cell reference maximum tail is 0.895. Method behavior only. |
| Progression label-noise sensitivity | material power loss | 576,000 additional synthetic cohorts. Scenarios reaching 80% fall from 7/24 to 4/24 at 5% and 3/24 at 10% symmetric label error. Assumption sensitivity only. |
| Progression event-time/covariate power extension | synthetic method guard established | 90,000 cohorts and 180,000 route evaluations. Source/treatment stratification restores near-nominal null behavior under deliberate confounding; the unadjusted route is inflated. Not biological evidence. |
| Progression competing-risk/death robustness | one invalid dependence boundary; power remains event-limited | 129,600 synthetic cohorts. Joint score/progression-risk death creates false protective associations; independent death is family-compatible but fails one strict cell and is excluded from power. Only 4/10 calibrated non-null scenarios reach 80%. Method behavior only. |
| Progression visit-schedule robustness | informative attendance invalid; sparse confirmation loses power | 172,800 cohorts and 691,200 route evaluations. Complete/independent attendance calibrates; score-dependent attendance creates false protective calls. Only complete quarterly observation at the high event setting reaches 80% by n=320. Method behavior only. |
| Repeated molecular-score reliability | useful only from a low-reliability starting point | 216,000 synthetic cohorts. Sixteen of 96 repeat-gain cells meet the frozen 0.10 aggregate/every-seed gain rule, all at starting reliability 0.40; correlated error sharply limits gain. Method behavior only. |
| Multi-site progression transportability | only high-event balanced-site design passes | 115,200 synthetic cohorts. Site stratification repairs deliberate pooled site confounding. Only n=450, event probability 0.30, balanced allocation passes global, site-direction, leave-site-out, event-count, heterogeneity, and negative-control gates. Method behavior only. |
| Multi-site score-scale harmonization | conditionally required under severe scale mismatch | 129,600 cohorts and 259,200 routes. Blinded within-site scaling materially improves transport in 6/36 comparisons, all under 0.5/1/2 site scales; it does not rescue imbalanced recruitment. Method behavior only. |
| Prospective progression cohort design synthesis | complete; no current eligible cohort | Sixteen requirements trace 14 artifacts into one reference design. The n=450/balanced/30%-event/quarterly specification is assumption-labeled, not a universal minimum; candidate role inventory remains 0 P1/P2/P3. |
| P2 compartment-interaction power design | conditionally ready with measured composition | 288,000 cohorts and 576,000 route evaluations. Direct interaction is calibrated only with high-fidelity composition or absent composition imbalance; noisy adjustment under true imbalance remains anti-conservative. Method behavior only. |
| P2 composition-method acceptance gate | synthetic-verified | Nine declarations distinguish direct measurement, direct-reference-validated sensitivity proxies, and fail-closed expression-only/unlinked/outcome-selected methods. Method behavior only. |
| Event-time assumption robustness | two failure boundaries established | 225,000 cohorts and 675,000 window evaluations. Joint score/event-risk dropout makes Cox anti-conservative; crossing effects can cancel in the whole-follow-up coefficient. Synthetic method behavior only. |
| Event-time blind receipt gate | synthetic-verified | Eight declarations verify that complete censoring metadata and pre-score sensitivities are mandatory; unknown/outcome-related loss and post-hoc window substitution fail closed. Method behavior only. |
| CDP/PIRA endpoint adjudicator | synthetic-verified | Sixteen edge cases preserve confirmed, transient, later-valid, context-excluded, missing-confirmation, censored, malformed, duplicate, and invalid states. CDP and PIRA decisions remain separate. Method behavior only. |
| Consolidated progression regression suite | 16/16 commands and 28/28 invariants pass | Fast gates, numerical references, negative claim boundaries, provenance/structure, and repository guards execute from one command. No biological claim. |
| V37 progression evidence delta | complete and artifact-checked | Twelve V37 items carried and six post-V37 items classified. No item becomes progression evidence or a target; scope and negative/method changes are explicit. |
| Combined P1/P2 intake gate | synthetic-verified | Nine cross-gate fixtures bind inventory, endpoint semantics, package ID, role, endpoint, and blindness into one fail-closed decision. Method behavior only. |
| Two-lineage adversarial review | 12/12 objections grounded; two change morphology grade | Review added value by exposing global multiplicity and within-donor estimand weaknesses. No progression or target verdict changed. |

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

A frozen follow-up explicitly tested all five source-by-stage interactions
(`docs/plans/PROGRESSION_STAGE_SOURCE_INTERACTION_V54.md`;
`analysis/v54_progressive_stage_source_interaction/`). None passed HC3,
three-seed 300,000 wild-bootstrap, BH, and max-T gates. CD44/CXCR4 had nearly
identical descriptive source effects (Amsterdam `0.319`, UK `0.372`;
interaction `0.053`, 95% CI `-1.155` to `1.262`, wild `p=0.928`, max-T
`p=1.000`). Lysosomal source heterogeneity remained inconclusive rather than
supported (interaction `0.917`, CI `-0.373` to `2.208`, wild `p=0.153`). A
null interaction with broad intervals is not evidence that source/tissue
effects are equivalent.

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

Status: **local sensitivity passes; globally exploratory after correction for
the complete post-result sequence**.

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

The coefficient is stable within this local, post-result sensitivity, but the
fully adjusted endpoint does not pass the later global 12-test sequential-
family audit (Holm `p=0.0861`). It must therefore be described as an
exploratory post-result association rather than robust or gate-passing across
V54. It does **not**
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

Status: **both pass the local mutual-adjustment gate but are globally
exploratory after sequential-family correction**.

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

The local models show separability under measured covariates, but the later
global 12-test audit gives Holm `p=0.0960` for both endpoints. The two-endpoint
state therefore does not retain global post-result family support and is
exploratory. It does not
establish independent biological pathways, metabolic or lysosomal flux,
progression, causality, or an intervention direction. Both remain unreplicated
in the paired chronic-active-edge context.

## Global Post-Result Morphology Multiplicity Audit

Status: **claim-level morphology results downgraded to exploratory**.

Artifacts:

- frozen plan:
  `docs/plans/POST_RESULT_MORPHOLOGY_MULTIPLICITY_AUDIT_V54.md`
- script: `scripts/v54_post_result_morphology_multiplicity.py`
- report: `analysis/v54_post_result_morphology_multiplicity/REPORT.md`
- complete family:
  `analysis/v54_post_result_morphology_multiplicity/global_post_result_family.tsv`

The full sequence contains 12 inferential endpoints: four lysosomal
specificity variants, two mutual-adjustment endpoints, four stratum-transport
tests, and two lesion-class interactions. Holm correction was applied to the
committed donor-wild p-values and remains valid under arbitrary dependence.

Only the partial `resident_adjusted` lysosomal model passes globally (Holm
`p=0.0145`). It is not the fully adjusted endpoint required by the specificity
claim. The fully adjusted lysosomal endpoint has Holm `p=0.0861`; mutually
adjusted OXPHOS and lysosomal each have Holm `p=0.0960`. Thus neither the
specificity claim nor the two-endpoint state retains global family support.
The numerical coefficients remain useful descriptive context, but the correct
evidence label is **exploratory post-result morphology association**.

## Foamy Morphology Within-Donor Estimand

Status: **within-donor estimand not supported**.

Artifacts:

- frozen plan: `docs/plans/FOAMY_DONOR_ESTIMAND_AUDIT_V54.md`
- script: `scripts/v54_foamy_donor_estimand_audit.py`
- report: `analysis/v54_foamy_donor_estimand_audit/REPORT.md`
- tests: `analysis/v54_foamy_donor_estimand_audit/within_donor_tests.tsv`

The proposed donor-by-lesion Fisher test was rejected because repeated,
multi-category samples violate that test's independence and table semantics.
The relevant coverage is sparse: only 6/21 donors contain both morphology
labels, and only 3/43 donor-by-lesion blocks contain both. An initially
specified all-sample donor-fixed-effect model failed before endpoint estimation
because non-varying singleton donor strata produced unit leverage; the frozen
fail-closed amendment restricted inference to the 23 samples from the six
informative donors.

Neither mutually adjusted endpoint passed the within-donor gate. OXPHOS
retained its pooled direction (beta `-0.184`) but had HC3 CI `-1.941` to
`1.573`, donor-wild `p=0.563`, max-T `p=0.719`, and a LODO range crossing zero
(`-1.614` to `0.422`). Lysosomal reversed near zero (beta `-0.057`, CI
`-1.884` to `1.770`, wild `p=0.814`, max-T `p=0.938`). In the three
same-donor, same-lesion blocks, pooled direction matched only 1/3 OXPHOS and
2/3 lysosomal contrasts; these counts are descriptive with minimum exact
two-sided `p=0.25`.

The pooled coefficients are therefore substantially between-donor or
unresolved under the held design. This further narrows them; it cannot restore
global family support or establish progression, flux, causality, or an
intervention direction.

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
specific. OXPHOS-low and lysosomal-high are exploratory post-result
foamy-morphology coefficients after the global sequential-family audit;
neither transfers across the chronic-active context, measures flux, or
identifies whether the state is damaging, compensatory, or reparative.

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
together with failed stratum transport and the later global multiplicity
audit, the correct label is **exploratory pooled morphology association with
unresolved lesion transport**, not a portable lesion program.

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
`docs/validation/PROGRESSION_PACKAGE_ELIGIBILITY_VALIDATOR_V54.md`. Fourteen
seeded, clearly labeled synthetic inventory regressions all behave as
specified: six cover complete or scientifically incomplete P1/P2/P3 roles and
eight cover malformed schemas, unknown additions versus substitutions,
verification, zero nonmissing values, and existing versus nonexistent source
paths. The new path fixture exposed and fixed a real bug: a nonexistent path
was recorded as an issue but did not previously enter `field_gate_pass`.
Real-package source paths now fail closed when absent. A pass means only
inventory-complete enough for blinded pre-registration and data-level
validation; it is not a data-quality or biological result.

The contracts were also applied to every known candidate without opening
expression values or quarantined packages. The generated matrix is
`analysis/v54_progression_candidate_role_matrix/candidate_role_matrix.tsv`,
with the operator summary at
`docs/validation/PROGRESSION_COHORT_ROLE_MATRIX_V54.md`. None of ten candidates
qualifies for P1, P2, or P3. In particular, Gafson and Karolinska remain
monitoring-validation routes rather than disability-progression cohorts;
GSE24427 has verified repeated expression but only baseline EDSS and relapse
follow-up; GSE228330 remains unmapped and outcome-incomplete; and postmortem
brain cohorts cannot supply living-person event time. The shortest path is a
longitudinal molecular cohort with raw repeated disability and adjudication,
not another cross-sectional public expression set.

Inventory presence does not establish endpoint meaning. A second, blinded
contract is now committed at
`docs/validation/PROGRESSION_P1_P2_BLINDED_PREREGISTRATION_V54.md`, with a
machine-readable declaration schema and
`scripts/v54_progression_outcome_semantic_checker.py`. Twelve clearly labeled
synthetic fixtures behave as required: valid CDP, PIRA, and paired-compartment
declarations pass, while relapse-only, stage-only, morphology-only,
pharmacodynamic-only, unconfirmed, undocumented-derived-label, date-incomplete
PIRA, interaction-free P2, and score-unblinded declarations fail closed. A pass
only establishes that the declared analysis is semantically eligible and
frozen before score access; it is not progression evidence.

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

The apparent `0.060` maximum was separately calibrated in
`analysis/v54_progression_power_calibration_audit/`. It represents 90/1,500
false passes with Wilson 95% CI `0.049` to `0.073`; none of 48 aggregate null
cells had a lower Wilson bound above nominal `0.05`. Under a 48-cell
Binomial(1500, 0.05) reference, a maximum at least this large has probability
`0.895`. The grid is not detectably anti-conservative; the maximum is expected
finite-simulation variation.

A frozen 576,000-cohort label-noise extension is in
`analysis/v54_progression_power_label_noise/`. Scenarios meeting the 80%
criterion fell from 7/24 at zero noise to 4/24 at 5% and 3/24 at 10% symmetric
outcome-label error. No OR `1.25` or `1.5` scenario reached 80% by `n=240` at
any level. At 15% events, even OR `2.0` failed once 5% label error was added.
These rates are design assumptions, not empirical PIRA-label estimates; they
make endpoint adjudication and blinded package-specific parameterization a
hard acquisition requirement.

A separately frozen event-time extension is in
`analysis/v54_progression_event_time_power_design/`, with its pre-run plan at
`docs/plans/PROGRESSION_EVENT_TIME_POWER_EXTENSION_V54.md`. It generated
90,000 unique synthetic cohorts and evaluated each with an unadjusted and a
source-by-treatment-stratified Cox score test, for 180,000 route evaluations.
An independent numerical check against `statsmodels.PHReg` score and Hessian
values passed four fixtures with maximum absolute difference `2.67e-15`.

Under deliberate score-source-treatment imbalance, the unadjusted null pass
rate had median `0.0887` and maximum `0.1907`. The pre-specified stratified
route had median `0.0460` and maximum `0.0653`; that maximum is 49/750 (Wilson
95% CI `0.0498-0.0853`), and a 40-cell binomial reference gives probability
`0.776` of a maximum at least that large. The stratified route is therefore
compatible with nominal calibration in this generator, while the unadjusted
route is not safe under the deliberate confounding regime.

Only 10/16 adjusted non-null assumption scenarios reached the frozen 80%
planning threshold. HR `1.5` at 15% pre-dropout event probability never reached
80% by `n=320`; with deliberate covariate imbalance it also failed at the 30%
event setting. HR `2.0` required `n=120-320`, depending on event probability,
dropout, and imbalance. These are synthetic design assumptions, not empirical
MS hazards or universal recruitment targets. They make pre-score event-time
modeling and source/treatment control mandatory when a received package has
variable follow-up or covariate imbalance.

## P2 Compartment-Interaction Power Design

Status: **conditionally ready only with high-fidelity composition measurement;
no biological claim**.

Artifacts:

- frozen plan: `docs/plans/PROGRESSION_P2_INTERACTION_POWER_V54.md`
- simulator: `scripts/v54_progression_p2_interaction_power.py`
- report: `analysis/v54_progression_p2_interaction_power/REPORT.md`
- trusted thresholds:
  `analysis/v54_progression_p2_interaction_power/trusted_threshold_summary.tsv`
- independent numerical check:
  `analysis/v54_progression_p2_interaction_power/reference_check/summary.json`

The frozen simulator generated 288,000 unique synthetic cohorts over paired and
unpaired designs and evaluated 576,000 direct interaction routes. It never uses
difference-of-significance localization. Four independent `statsmodels.OLS`
fixtures reproduce the batched interaction implementation, with maximum
absolute discrepancy `2.22e-15`.

The adjusted route is compatible with nominal null calibration when composition
is measured perfectly (48-cell median `0.048`, maximum `0.0653`, family
max-tail `0.834`) and when composition is noisy but there is no true
outcome-associated composition imbalance (24-cell median `0.0493`, maximum
`0.0613`, family max-tail `0.904`). It is not calibrated when noisy composition
measurement leaves true imbalance unresolved: the adjusted null maximum rises
to `0.2227` (167/750, Wilson 95% CI `0.1943-0.2538`). Omitting composition under
imbalance is worse, with a maximum null pass rate of `0.5827`.

Only calibration-eligible regimes are used for planning. Twenty-seven of 36
trusted non-null scenarios reached the frozen 80% criterion. In paired designs,
a `0.7` SD interaction reached 80% in all nine trusted scenarios, with the
smallest qualifying group size `15`; a `0.4` SD interaction passed only 3/9 and
could require at least `50` per outcome group. In unpaired designs, a `0.7` SD
interaction required `80` per outcome-by-compartment group, while `0.4` SD did
not reach 80% by that maximum. These are conditional synthetic assumptions,
not empirical MS effects or universal sample-size requirements.

The operational conclusion is stricter than merely adding a composition proxy:
if outcome-associated compartment composition is possible, P2 localization
requires direct, validated high-fidelity composition measurements or an
independently demonstrated no-imbalance condition. A noisy expression-derived
proxy cannot rescue the interaction. Any received package must rerun this grid
from blinded pairing, outcome, compartment, composition reliability, and
imbalance metadata before scores are accessed.

The measurement eligibility contract is now explicit in
`docs/validation/PROGRESSION_P2_COMPOSITION_ACCEPTANCE_V54.md` and enforced by
`scripts/v54_progression_p2_composition_gate.py`. Nine synthetic declarations
pass expected behavior. Direct sample-linked measurements can enter the
cohort-specific null/power calibration. A deconvolution proxy is only
conditionally eligible when a blinded, sample-linked direct-reference subset
provides compartment-specific reliability and the null simulation passes at
that reliability and observed imbalance; it remains sensitivity-only.
Expression-module proxies alone, unlinked references, outcome-selected
methods, or unresolved differential missingness fail closed.

## Event-Time Assumption Robustness

Status: **the Cox route is calibrated only under compatible censoring and a
single coefficient cannot exclude time-varying effects**.

Artifacts:

- frozen plan:
  `docs/plans/PROGRESSION_EVENT_TIME_ASSUMPTION_ROBUSTNESS_V54.md`
- simulator:
  `scripts/v54_progression_event_time_assumption_robustness.py`
- report:
  `analysis/v54_progression_event_time_assumption_robustness/REPORT.md`
- full grid:
  `analysis/v54_progression_event_time_assumption_robustness/assumption_grid.tsv`
- independent reference checks:
  `analysis/v54_progression_event_time_assumption_robustness/reference_check/summary.json`

The audit generated 225,000 unique synthetic piecewise-hazard cohorts and
675,000 whole-follow-up, early-window, and late-landmark evaluations. It varied
five fixed molecular-effect patterns, five censoring mechanisms, two event
probabilities, three sample sizes, and three seeds. Scalar piecewise inversion,
event/dropout calibration equations, and `statsmodels.PHReg` supplied four
independent numerical checks; all pass, with maximum discrepancy `2.94e-15`.

Administrative-only, independent, score-dependent, and event-risk-only
censoring passed the frozen whole-follow-up null rule. Their family median null
rates were `0.039-0.053`, maxima `0.053-0.057`, and family maximum-reference
tails `0.497-0.875`. Covariate-dependent censoring is therefore not
automatically invalid in this generator.

Joint dependence on molecular state and latent event risk is different. It
violates conditional independent censoring and creates reproducible false
protective associations: the six null cells have median false-call probability
`0.544`; the maximum is `0.795` (1193/1500, Wilson 95% CI
`0.774-0.815`), and every significant call in that maximum cell is negative.
Across sample-size/event cells the false-call rate rises from `0.101` to
`0.795` as information accumulates. More data therefore reinforces the bias
rather than repairing it.

Non-proportionality creates a separate interpretation failure. At `n=320` and
pre-censoring event probability `0.30`, the crossing HR pattern (`2.0` early,
`0.5` late) is detected by the whole-follow-up coefficient only
`0.127-0.157` across calibrated censoring regimes. The fixed diagnostics recover
the expected early-positive direction in `0.412-0.894` and late-negative
direction in `0.631-0.807`. The whole coefficient is averaging opposing
associations; its null cannot establish absence of a time-varying effect.
Window diagnostics themselves can be unfit at low event counts, so they are not
a post-hoc rescue route.

The operational boundary is two-part: a future P1 event-time package needs a
blinded censoring audit capable of ruling out joint molecular-state/event-risk
loss, and proportionality/time-variation diagnostics must be reported alongside
the frozen whole-follow-up result. Any confirmatory time-varying coefficient or
window contrast requires its own pre-score specification; comparing window
p-values is prohibited.

The additive operator guard is documented in
`docs/validation/PROGRESSION_EVENT_TIME_ASSUMPTION_GATE_V54.md` and enforced by
`scripts/v54_progression_event_time_assumption_gate.py`. Eight clearly labeled
synthetic declarations behave as specified: administrative-only data pass with
mandatory diagnostics; fully documented nonadministrative loss passes only
with the sensitivity panel required; unknown or outcome-related loss, missing
censoring dates, missing time-variation diagnostics, prior score access, and
window-p-value substitution all fail closed. This gate tightens receipt
handling without modifying the frozen P1/P2 contract.

Endpoint values themselves are handled by
`scripts/v54_progression_endpoint_adjudication.py`, under the frozen synthetic
test plan `docs/plans/PROGRESSION_ENDPOINT_ADJUDICATION_FIXTURES_V54.md`.
Sixteen synthetic fixtures pass their predeclared outcomes. The processor does
not convert transient or component-discordant worsening into an event, does not
convert missing or mistimed confirmation into a negative, and reports
treatment-switch censoring before confirmation as inconclusive. A confirmed
relapse-associated disability event remains eligible as CDP under the synthetic
CDP declaration but is not relabeled PIRA. The embedded thresholds are fixture
parameters only; a real cohort must supply its documented protocol before score
access. The added malformed-input regressions return explicit `INVALID_INPUT`
for duplicate assessment days, malformed component/day values, and an unknown
endpoint. A separate fixture proves that an earlier transient candidate does
not prevent the frozen search from returning a later qualifying onset (day 300,
confirmed day 480).

## Progression Competing-Risk And Death Robustness

Status: **cause-specific inference requires a pre-score competing-event
dependence audit**.

Executable audit:

- frozen plan: `docs/plans/PROGRESSION_COMPETING_RISK_ROBUSTNESS_V54.md`
- script: `scripts/v54_progression_competing_risk_robustness.py`
- results: `analysis/v54_progression_competing_risk_robustness/`

The seeded simulation generated 129,600 unique synthetic cohorts across two
pre-competing-risk event rates, three sample sizes, two molecular effects, and
five competing-death mechanisms. These results characterize method behavior;
they contain no empirical MS mortality, progression, or treatment evidence.

No-death, score-dependent death, and progression-risk-dependent death passed
the frozen null-calibration rule. Independent death had median null rejection
`0.0508` and maximum `0.0633` (76/1,200; Wilson 95% CI `0.0509-0.0786`). Its
strict single-cell lower-bound rule therefore flags, but the predeclared
12-cell family maximum-reference tail is `0.243` and significant directions
are balanced. It is reported as family-compatible but inconclusive and is
excluded from all power summaries, not relabeled as a directional bias.

Joint dependence of death on molecular score and latent progression risk
invalidates ordinary cause-specific censoring in this generator. Its median
null rejection is `0.0671`, the maximum is `0.1192` (143/1,200; Wilson 95% CI
`0.1020-0.1387`), and the family maximum-reference tail is effectively zero.
The maximum cell is predominantly false protective (`0.1192` negative versus
`0.0183` positive). A future P1 package must therefore disclose mortality and
competing-event timing and causes before score access; plausible joint
score/risk dependence triggers a pre-specified competing-risk sensitivity or
a fail-closed result. Death is not folded into the disability endpoint post
hoc.

Power remains event-limited even in calibrated mechanisms. Only 4/10 non-null
scenarios meet the 80% and seed-stability gates. No scenario with pre-death
event probability `0.15` reaches 80% by `n=320`; at event probability `0.30`,
four scenarios reach the threshold at `n=320`, while score-dependent death at
probability `0.25` reaches only `0.737`. These are design assumptions, not
empirical effect-size estimates.

## Visit Schedule And Interval Observation

Status: **informative attendance invalidates the observed route; sparse but
noninformative schedules remain calibrated and lose substantial power**.

Executable audit:

- frozen plan: `docs/plans/PROGRESSION_VISIT_SCHEDULE_ROBUSTNESS_V54.md`
- script: `scripts/v54_progression_visit_schedule_robustness.py`
- tied-time reference:
  `scripts/v54_visit_schedule_breslow_reference_check.py`
- results: `analysis/v54_progression_visit_schedule_robustness/`

The two-year seeded simulation generated 172,800 unique cohorts and 691,200
route evaluations across quarterly, semiannual, and annual observation;
complete, independently missing, score-dependent, and joint score/risk
attendance; and fixed detection-time, midpoint, and audit-only oracle routes.
The Breslow tie-aware implementation agrees with four independent
`statsmodels.PHReg` score/Hessian fixtures to `3.55e-15`.

Complete and 20% independently missing attendance calibrated for both observed
routes. Detection-time null maxima were `0.0542` and `0.0600`, with fixed-family
maximum-reference tails `0.997` and `0.712`. Midpoint null maxima were `0.0542`
and `0.0617`, with tails `0.997` and `0.522`. Coarsened time alone therefore
does not create a false molecular association in this generator.

Informative ascertainment does. Score-dependent 20% visit missingness produced
null maxima `0.1583` for both routes, with predominantly false protective calls
(`0.1567` negative versus at most `0.0083` positive). Joint score/progression-
risk missingness produced null maxima `0.1650` and similarly false protective
calls (`0.1625` negative). Both fixed observed routes are invalid. Midpoint
imputation changes timing but does not restore events that were selectively
unconfirmed, so it cannot repair this bias.

Even calibrated attendance loses substantial information through delayed or
absent confirmation. At `n=320`, latent event probability `0.30`, and synthetic
HR `1.7`, complete quarterly observation confirms a median 79/87 latent events
and reaches power `0.829`; this is the only design reaching the 80% gate (twice
only because detection and midpoint are fixed parallel routes). Complete annual
observation confirms 51/86 and reaches `0.592`; annual observation with 20%
independent missingness confirms 33/86 and reaches `0.399`. At latent event
probability `0.15`, no calibrated schedule reaches 80% by `n=320`.

The acquisition consequence is pre-score and operational: visit dates,
expected windows, missed-visit indicators/reasons, first worsening, and later
confirmation must be complete enough to audit whether attendance depends on
the molecular score or progression risk. Sparse schedules yield an
underpowered/inconclusive result; informative attendance makes the ordinary
route invalid. Neither condition may be interpreted as absence of a molecular
association. These are synthetic design results, not empirical MS effects or
attendance estimates.

## Repeated Molecular-Score Reliability Design

Status: **repeat measurement is conditionally useful only when starting
reliability is low and errors are sufficiently independent**.

Executable audit:

- frozen plan: `docs/plans/PROGRESSION_REPEATED_SCORE_RELIABILITY_V54.md`
- script: `scripts/v54_progression_repeated_score_reliability.py`
- results: `analysis/v54_progression_repeated_score_reliability/`

The seeded simulation generated 216,000 synthetic cohorts across two starting
reliabilities, one/two/three baseline measurements, independent or
0.50-correlated error, 10% per-measurement missingness, three sample sizes, two
event rates, and null plus two non-null effects. Six of ten measurement plans
pass the strict null rule. Four have an isolated strict-cell flag but remain
compatible with their fixed family-maximum reference; they are conservatively
excluded from power interpretation rather than called biased. No plan is
directionally invalid.

Only 16/96 repeat-gain cells meet the frozen requirement of at least 0.10
absolute gain both in aggregate and in every seed. Every such cell starts from
single-measurement reliability `0.40`. The eligible plan families are two
independent-error measurements, three independent-error measurements, and
selected three-measure settings with 0.50-correlated error. No plan starting at
reliability `0.70` clears calibration plus the aggregate/every-seed utility
rule.

The highest-information fixed scenario illustrates the magnitude and the
diminishing return. At `n=320`, latent event probability `0.30`, and synthetic
HR `1.7`, one measurement has empirical reliability `0.398` and power `0.578`;
two independent-error measurements reach reliability `0.531` and power
`0.781`; three reach `0.634` and `0.847`. With 0.50-correlated error, three
measurements reach only reliability `0.491` and power `0.748`. At the lower
event rate, even the same low-reliability three-repeat plan reaches only
`0.613` power for HR `1.7` at `n=320`.

The prospective implication is conditional: obtain a blinded pilot/test-retest
reliability estimate before imposing repeat collection. Repeats are justified
by this design only if single-measure reliability is poor and technical/
temporal errors are demonstrably not strongly shared. Repetition cannot repair
sparse progression events, endpoint error, informative attendance, or a
non-progression-qualified cohort. These values are synthetic method behavior,
not evidence that the project's molecular state has any particular stability.

## Multi-Site Progression Transportability

Status: **site-stratified inference calibrates, but full transport requires
high event yield and balanced site allocation**.

Executable audit:

- frozen plan: `docs/plans/PROGRESSION_MULTISITE_TRANSPORTABILITY_V54.md`
- script: `scripts/v54_progression_multisite_transportability.py`
- numerical reference: `scripts/v54_multisite_cox_reference_check.py`
- results: `analysis/v54_progression_multisite_transportability/`

The seeded simulation generated 115,200 synthetic cohorts across three total
sample sizes, two event rates, balanced versus 60/30/10 site allocation, two
site-score structures, and null/homogeneous/site-only/reversed effects. Four
pooled and site-stratified score/information fixtures agree with independent
`statsmodels.PHReg` calculations to `2.56e-13`.

Pooled inference fails exactly where designed to fail. When molecular-score
means align with ordered site baseline hazards, pooled null rejection reaches
`0.685` under balanced allocation and `0.482` under 60/30/10 allocation; both
fixed families are invalid. All four site-stratified null families calibrate,
with maxima `0.053-0.059`. A large pooled association can therefore be entirely
site structure even when the within-site molecular effect is null.

Only 2/24 design variants pass the complete transport gate. Both use `n=450`,
latent event probability `0.30`, and balanced site allocation; the two variants
are the balanced-score and hazard-aligned-score settings. Their homogeneous-
effect transport-pass probabilities are `0.801` and `0.817`, with every-seed
minima `0.787` and `0.785` and median minimum-site event count 26. The
corresponding 60/30/10 designs, despite the same total sample size, reach only
`0.758` and `0.748` (every-seed minima `0.748` and `0.733`) and fail.

The transport gate remains selective in the fixed heterogeneous negative
controls: maximum false-transport probability is `0.0225` for an effect at one
site only and `0.0333` when one site reverses direction. At event probability
`0.15`, no design passes even at `n=450`; global stratified significance can be
high while leave-site-out/event-count transport remains low.

The acquisition consequence is stronger than a total-`n` target. A future
multi-site progression cohort needs predeclared sites, site-stratified primary
inference, balanced recruitment or explicit minimum events per site, signed
site estimates, leave-one-site-out tests, and heterogeneity reporting. Pooled
significance alone is invalid for transport. These are synthetic design
requirements, not empirical claims about site effects or an MS biomarker.

## Prospective Cohort Design Synthesis

Status: **reference design specified; no known cohort is currently eligible**.

The medical-team brief is
`docs/validation/PROGRESSION_PROSPECTIVE_DESIGN_V54.md`. Its rerunnable source
checker, `scripts/v54_progression_design_synthesis.py`, emits 16 requirements
traced to 14 artifacts under `analysis/v54_progression_design_synthesis/`.

The reference combines the only transport-ready synthetic setting (`n=450`,
three balanced sites, event probability `0.30`, median minimum 26 events/site)
with quarterly observation, raw confirmed CDP/PIRA components, pre-score
attendance/censoring/competing-event audits, reliability-conditioned molecular
repeat collection, site-stratified and leave-site-out inference, and direct P2
composition measurement. It also freezes the interpretive sequence: P1
prediction, optional P2 localization, and only then a separate P3 functional-
direction program.

This is deliberately not called a universal minimum. The synthetic reference
assumes HR `1.7`, reliability `0.70`, and a high event setting; weaker effects,
rarer events, informative missingness, site imbalance, or correlated
measurement error can make `n=450` insufficient. The checker confirms that the
known candidate inventory still contains zero P1-, P2-, or P3-eligible cohorts.

## Site-Score Scale Harmonization

Status: **blinded within-site scaling is conditionally necessary under severe
assay-scale mismatch, but cannot rescue site imbalance or sparse events**.

Executable audit:

- frozen plan: `docs/plans/PROGRESSION_SITE_SCORE_HARMONIZATION_V54.md`
- script: `scripts/v54_progression_site_score_harmonization.py`
- results: `analysis/v54_progression_site_score_harmonization/`

The seeded audit generated 129,600 unique cohorts and 259,200 route evaluations
across uniform, moderate, and severe (`0.5/1.0/2.0`) site scale patterns. Both
routes stratify by site; one uses one global score standardization and the other
uses an outcome-blind within-site standardization. No null family is invalid.
Two within-site families have isolated strict-cell flags while remaining
compatible with their fixed family maxima; those families are conservatively
excluded from gain claims.

Six of 36 comparisons meet the frozen 0.10 aggregate and every-seed transport-
gain rule, all under severe scale mismatch. In the balanced `n=450`, event
probability `0.30` design, global scaling passes transport in only `0.466` of
cohorts (every-seed minimum `0.398`), while within-site scaling reaches `0.809`
(minimum `0.800`). Under uniform scales the same comparison is `0.807` versus
`0.804`, showing no manufactured benefit. The severe 60/30/10 design improves
`0.391 -> 0.755` but still fails the 0.80/every-seed transport requirement.

The reversed-effect negative control remains selective after within-site
scaling (maximum false transport `0.0325`). The acquisition implication is to
capture exact site/platform/calibration identifiers and freeze score scaling
from blinded metadata. Within-site scaling is justified when measurement scale
differs, not selected because it improves an outcome. It cannot compensate for
an underrepresented site, too few events, or an unknown site map. These are
synthetic assay-method results, not evidence that any real cohort has scale
mismatch.

## Consolidated Regression Suite

Status: **pass**.

Run:

```bash
.venv/bin/python scripts/v54_progression_regression_suite.py
```

The final suite executes 19 checks and asserts 53 committed artifact/claim
invariants. All pass. It covers Python compilation; inventory, semantic,
combined-intake, endpoint-adjudication, event-time, and composition regressions;
four independent numerical references; the candidate role matrix; provenance
and structural gates; whitespace; tracked-file size; and tracked temporary
paths. Its invariants explicitly retain zero portable stage modules, zero
transition-identifiable datasets, zero target revisits, both morphology
downgrades, the event-time and competing-risk invalid regimes, the independent-
death strict-cell flag, both informative-attendance invalid regimes, the
bounded repeated-measurement utility result, pooled-site invalidation and the
two transport-ready synthetic designs, the prospective reference-design
boundary, and 0/10 P1/P2/P3 candidate eligibility.

The first suite run exposed a real execution defect: resolving the virtualenv
interpreter symlink caused child processes to use bare Homebrew Python without
the analysis packages. The runner now preserves the active virtualenv entry
point. Full results are in `analysis/v54_progression_regression_suite/`.

## Multi-Lineage Adversarial Review

Status: **complete; independent review changed one bounded evidential grade,
not a progression or target verdict**.

Artifacts:

- prompt: `analysis/v54_multilineage_progression_review/review_prompt.md`
- segregated model records:
  `knowledge_external/model_outputs/v54_progression_review/`
- grounded report: `analysis/v54_multilineage_progression_review/REPORT.md`
- all dispositions:
  `analysis/v54_multilineage_progression_review/objection_grounding.tsv`

Claude and Gemini each supplied six proposal-only objections. All 12 were
checked against committed artifacts. Two changed the evidential grade:

1. The complete 12-test post-result morphology sequence does not retain the
   fully adjusted lysosomal or two-endpoint coupling claims after Holm control.
2. A valid donor-estimand replacement for the proposed repeated-sample Fisher
   test found only six informative donors and no supported within-donor
   endpoint.

The shared source-by-stage concern was tested formally across all five modules
and did not support a positive interaction. The null-power maximum was
calibrated rather than assumed problematic, while separate label-error runs
materially tightened acquisition requirements. The proposed peripheral test
remains fail-closed because the model itself requires artifacts that are not
available.

The independent lenses therefore added methodological value: they caused the
foamy OXPHOS/lysosomal pattern to be downgraded to exploratory and substantially
between-donor or unresolved. They did not surface a progression-associated
state, intervention direction, or tractable target. Agreement prioritized the
checks; only the data and committed method audits determined these outcomes.
