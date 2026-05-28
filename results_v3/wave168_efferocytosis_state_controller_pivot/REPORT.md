# Wave168 Efferocytosis State-Controller Pivot

## Branch call
`NO_EFFEROCYTOSIS_STATE_CONTROLLER_PROMOTION`

## Result
- Screen hits tested: `128`.
- Promoted candidates: `0`.
- Best gene: `YWHAE`.
- Best score: `6.003778205404065`.
- Best blockers: `no_ms_anchor;no_intervention_handle;no_genetic_anchor_annotation`.

## Interpretation
This branch treats efferocytosis as a repair phenotype rather than a genetic
target. It does not produce a V3 target yet because the top functional hits
still fail one or more of state recurrence, MS anchoring, intervention handle,
or prior/modality safety.
