# V57 Multi-Criterion Positive Region

Status: **PASS** as seeded synthetic method behavior;
no biological or MS claim.

## Frozen Extension

- Parent gate: commit `5c407480`; no method parameter changed.
- Synthetic screens: `36,000`.
- Candidate evaluations: `864,000` per method.
- Donor counts `12`, `14`, `16`; effects `0.80`, `1.00`; three seeds.

## Result

- `12` donors: **PASS** across all seeds and effects.
- `14` donors: **PASS** across all seeds and effects.
- `16` donors: **PASS** across all seeds and effects.

`12` is the first high-precision tested passing donor count.

Failed checks: `0` of `90`.
All decisions are retained in `gate_checks.tsv`.

## Boundary

This verifies only a synthetic operating region under the committed variance
model. It is not biological power, does not assert a rescue exists, and must be
recalibrated prospectively from blinded pilot variance before an empirical
screen is sized.
