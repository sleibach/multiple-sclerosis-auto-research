# V57 Blinded Variance Adaptation

Status: **FAIL** as seeded synthetic method behavior;
no biological or MS claim.

## Scale

- Synthetic screens: `12,000`.
- Candidate evaluations: `288,000` per method.
- Resizing uses a blinded variance estimate only; candidate means and outcomes
  are unavailable to the rule.

## Frozen Result

- true noise multiplier `0.75`: **PASS**.
- true noise multiplier `1.00`: **PASS**.
- true noise multiplier `1.25`: **FAIL**.
- true noise multiplier `1.50`: **FAIL**.

Adaptive donor counts ranged from mean
`8.4` to
`25.1` per context; abstention ranged
`0.000`-`0.728`.
Failed checks: `22` of `120`.

## Meaning

A passing regime would license blinded nuisance-based resizing under these
synthetic assumptions. A failed regime identifies where the donor grid or
pilot precision is inadequate; it cannot be fixed by looking at candidate
effects. Real pilot variance and assay diagnostics remain prerequisites.
