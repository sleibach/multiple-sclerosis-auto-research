# Analogy Safety Review V55

This is a communication-maintenance review, not scientific evidence. It checks
whether the onboarding layer uses familiar comparisons without turning those
comparisons into biological models or stronger evidence claims.

The scientific boundaries being protected are defined by the onboarding claim
contract, including monitoring-not-target `[M05]`, progression-design limits
`[P01]`, and evidence-class separation `[E01]`.

## Review Standard

Each teaching metaphor must satisfy four conditions:

1. It has a narrow, stated teaching purpose.
2. Its important limits are stated near first use or in the visual guide.
3. It does not imply causality, effect size, mechanism, priority, or validation
   that the source artifacts do not establish.
4. A reader can remove the metaphor and still recover the precise claim from
   literal text and source references.

## Reviewed Comparisons

| comparison | where used | intended distinction | explicit limit | result |
|---|---|---|---|---|
| Gauge/thermometer versus control knob | [Monitor vs Target](CASE_STUDY_MONITOR_VS_TARGET.md), [layered narrative](MS_RESEARCH_EXPLAINED.md), monitoring visual | A predictive readout and a causal intervention require different evidence. | Immune systems are not heating systems; a readout can correlate with response without explaining mechanism; no measured gene becomes a target. | pass |
| Dashboard indicator versus steering control | [layered narrative](MS_RESEARCH_EXPLAINED.md) | Monitoring is observation, not treatment selection or intervention. | The text limits the comparison to association and says it does not explain mechanism. | pass |
| Snapshot versus movie | [progression case study](CASE_STUDY_PROGRESSION_SNAPSHOT_VS_MOVIE.md), [visual guide](VISUAL_INDEX.md), [open problem 3](OPEN_PROBLEMS_FOR_COLLABORATORS.md) | Cross-sectional observations cannot replace linked, time-ordered molecular and confirmed-disability measurements. | The comparison is only about study design; it does not imply smooth change, complete observation, or causality from repeated measurement. | pass after clarification |
| Research terrain/map | [research map](visuals/RESEARCH_MAP_V55.svg), [visual guide](VISUAL_INDEX.md) | Show the statuses and open edges of several work areas at once. | Layout and distance do not encode causal proximity, effect size, or priority. | pass after clarification |
| Evidence lanes | [evidence-lanes visual](visuals/EVIDENCE_LANES_V55.svg), [visual guide](VISUAL_INDEX.md) | Keep rerunnable project evidence separate from outside-source context. | Lanes are provenance categories, not biological pathways or an importance ranking; a new test must be run before status can change. | pass after clarification |
| Evidence journey/path | [evidence-journey visual](visuals/EVIDENCE_JOURNEY_V55.svg), [visual guide](VISUAL_INDEX.md) | Make eligibility, identifiability, precommitment, testing, and decision consequences visible. | It is a review workflow, not a disease mechanism, linear guarantee, or claim that every project follows one pass. | pass after clarification |
| Evidence ladder | [Monitor vs Target](CASE_STUDY_MONITOR_VS_TARGET.md) | Keep monitoring requirements distinct from intervention requirements. | A ladder is neither a score nor automatic promotion; monitoring evidence cannot fill intervention requirements. | pass after clarification |
| Wall | [layered narrative](MS_RESEARCH_EXPLAINED.md), [research timeline](RESEARCH_EVOLUTION_TIMELINE.md) | Name a current evidence or data-design boundary and what would move it. | It is not a permanent biological impossibility. The table supplies a concrete reopening requirement. | pass after clarification |
| Bridge from context to test | [Outside Context To Test](CASE_STUDY_CONTEXT_TO_TEST.md) | Show the conversion of an outside statement into a falsifiable proposal. | “Bridge” was replaced by literal language so no authority transfer is implied. | pass after wording change |

## Remaining Safe-Use Rules

- Do not use route, path, ladder, or journey position as an evidence grade.
- Do not use spatial distance in a visual as biological similarity unless a
  source analysis explicitly defines that encoding.
- Do not use “movie” as a substitute for the actual required fields: linked
  people, repeated compatible molecular measures, repeated confirmed
  disability, event timing, treatment, source, quality, and censoring.
- Do not extend the heating-system comparison to immune control architecture.
- Do not call a boundary permanent when the repository states what evidence
  could move it.

## Verdict

All material analogies have a bounded teaching role and a literal text
equivalent. Five comparisons received clearer limits during this review, and
one metaphorical phrase was replaced with literal provenance language. The
review does not establish comprehension; that still requires testing with
newcomers using the [comprehension kit](COMPREHENSION_TEST_KIT.md).
