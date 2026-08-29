# V57 Multi-Criterion Perturbation Gate

Status: **FAIL** as a synthetic method test. This report contains no
biological observations and makes no MS, target, or treatment claim.

## Scale

- Seeded synthetic screens: `18,000`.
- Candidate evaluations: `432,000` per method.
- Methods compared: multiplicity-controlled averaged efficacy endpoint versus
  the preregistered partial-conjunction, viability, donor, and guide gate.

## Preregistered Operating Region

Across donor counts `>=8` and broad-rescue effects `>=0.80`, the averaged
endpoint had mean probability of any true rescue
`1.000`, false promotion
`0.767`, recall
`0.992`, and precision
`0.708`.

The replicated broad-rescue gate had corresponding values
`0.702`,
`0.000`,
`0.341`, and
`1.000`.

Preregistered checks failed: `12` of `60`. Full
cell-level checks are in `gate_checks.tsv`; no threshold was changed after
simulation.

The eight-donor design is `FAIL` and the
twelve-donor design is `PASS` across all
frozen seeds and tested effects. Thus `12` is the first **tested** donor count
with a fully passing operating region; this sweep does not establish whether
`9`, `10`, or `11` donors suffice.

## Interpretation

The averaged endpoint was sensitive but frequently promoted narrow or tradeoff
effects. The replicated gate eliminated false promotions in this synthetic
design but was underpowered at eight donors. The gate is useful only within an
operating region that passed every frozen criterion. A failure must not be
rescued by changing endpoints, margins, or multiplicity rules afterward. Even
a method pass only defines how a future human-cell experiment would select a
broadly beneficial, non-toxic, donor-replicated perturbation; it does not
establish that such a perturbation exists.

## Files

- `performance.tsv`: screen-level operating characteristics aggregated by
  seed, donor count, effect scale, and method.
- `class_selection.tsv`: selection frequency by synthetic truth class.
- `gate_checks.tsv`: frozen pass/fail criteria.
- `synthetic/simulation_config.json`: exact seeded design declaration.
