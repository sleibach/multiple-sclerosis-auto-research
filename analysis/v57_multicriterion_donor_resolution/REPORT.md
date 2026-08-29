# V57 Multi-Criterion Donor Resolution

Status: **FAIL** as seeded synthetic method behavior.
No observation in this report is biological evidence.

## Frozen Extension

- Parent method and all thresholds: commit `5c407480`.
- Synthetic screens: `36,000`.
- Candidate evaluations: `864,000` per method.
- New donor counts only: `9`, `10`, `11`; effects `0.80`, `1.00`; three seeds.

## Result

- `9` donors: **FAIL** across all seeds and effects.
- `10` donors: **FAIL** across all seeds and effects.
- `11` donors: **FAIL** across all seeds and effects.

None of 9-11 donors passes every check; 12 remains the first tested passing count.

There were `25` failed checks among
`90`. `gate_checks.tsv` preserves every cell-level
decision. No endpoint, margin, multiplicity rule, effect, or noise parameter
was changed after the parent result.

## Meaning

This result can size the proposed synthetic-design analogue of a future pilot.
It does not establish biological effect sizes, prove that any perturbation is
beneficial, or replace empirical pilot variance estimates. A real pilot should
use an internal variance checkpoint without outcome-driven threshold changes.
