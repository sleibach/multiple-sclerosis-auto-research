# V54 Progression Endpoint Adjudication Fixture Plan

Status: frozen before implementation on 2026-07-21T23:13:52Z.

## Boundary

This is a synthetic regression of endpoint-processing behavior. It contains no
patient data, makes no biological claim, and does not define a universal CDP or
PIRA protocol. A real cohort must provide and freeze its own documented
thresholds and windows before scores are accessed. The fixture engine proves
that those frozen rules are executed consistently.

## Frozen Synthetic Protocol

The synthetic protocol uses:

- baseline at day 0;
- EDSS absolute worsening of at least 1.0;
- T25FW relative worsening of at least 20%;
- `all_components` combination, so both components must cross threshold at
  onset and confirmation;
- confirmation from 180 through 240 days after onset;
- for PIRA, no relapse from 90 days before through 30 days after onset and no
  steroid exposure from 30 days before through 30 days after onset;
- censoring at treatment switch, death, or dropout before confirmation.

These numbers are synthetic test parameters, not a recommendation or statement
of the Gafson/Karolinska endpoint.

## Frozen Outcomes

The adjudicator must distinguish:

1. `CONFIRMED_EVENT`: threshold crossed and retained in-window with all frozen
   components; PIRA context also clean when PIRA is requested.
2. `NO_EVENT_THRESHOLD_NOT_MET`: no assessment crosses the frozen combined
   threshold.
3. `NO_EVENT_TRANSIENT_OR_COMPONENT_DISCORDANT`: onset crosses, but an
   in-window assessment fails confirmation or component concordance.
4. `NO_PIRA_EVENT_CONTEXT_EXCLUDED`: a confirmed disability event overlaps a
   frozen relapse or steroid window; it is not relabeled PIRA.
5. `INCONCLUSIVE_MISSING_CONFIRMATION`: onset crosses but no assessment exists
   in the confirmation window.
6. `INCONCLUSIVE_CENSORED_BEFORE_CONFIRMATION`: switch, death, or dropout occurs
   before a valid confirmation could be observed.
7. `INVALID_INPUT`: missing/duplicate baseline, malformed dates, missing frozen
   components, or an unknown endpoint/protocol.

The processor may search later candidate onsets after an excluded or transient
candidate, but may never alter thresholds, component logic, or windows. The
earliest fully qualifying event is returned. CDP and PIRA decisions are
separate; a relapse-associated confirmed disability event can be CDP under a
declared CDP endpoint while remaining ineligible as PIRA.

## Synthetic Regression Cases

At minimum, fixtures cover:

- confirmed clean PIRA;
- transient worsening;
- missing confirmation;
- confirmation too early without an in-window assessment;
- relapse overlap;
- steroid overlap;
- component disagreement at onset or confirmation;
- treatment switch before confirmation;
- missing baseline;
- the same relapse-associated confirmed event under a CDP declaration.

Every fixture records its expected status before execution. All artifacts must
carry a synthetic marker and state that adjudication behavior is not MS
evidence.
