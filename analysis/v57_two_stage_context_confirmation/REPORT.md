# V57 Two-Stage Context Confirmation

Status: **FAIL** as seeded synthetic method behavior;
no biological or MS claim.

## Design

- Discovery: 12 donors, pooled replicated gate, at most four nominees.
- Confirmation: fresh, balanced donor contexts; no discovery data reused.
- Synthetic screens: `18,000`.
- Candidate evaluations: `432,000` per stage.

## Frozen Result

- `6` fresh donors per context (`12` total): **FAIL**.
- `8` fresh donors per context (`16` total): **FAIL**.

First passing panel: `None` donors per
context (`None` total).
Failed checks: `24` of `60`.

Among nominated uniform-rescue candidate instances, the efficacy component
passed in `0.000`-`0.777` of cases and the viability component in
`0.000`-`0.042`. These post-result diagnostics do not change the frozen gate; they localize the
precision requirement for a future assay-design test.

## Meaning

This test asks whether independent confirmation can reject a candidate that
looks broadly favorable in discovery but harms one functional endpoint in a
prespecified donor context. A pass licenses only the staged method under this
synthetic variance model. It does not discover a context, candidate, target, or
treatment, and empirical pilot variance remains necessary.
