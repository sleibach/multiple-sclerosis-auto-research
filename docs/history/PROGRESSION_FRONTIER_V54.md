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
