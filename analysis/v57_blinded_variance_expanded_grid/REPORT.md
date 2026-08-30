# V57 Expanded Blinded-Variance Grid

Status: **PASS** as seeded synthetic method behavior;
no biological or MS claim.

## Frozen Remediation

- Blinded pilot residual degrees of freedom: `96`.
- Donor grid per context: `12, 16, 20, 24, 32, 40, 48`.
- All efficacy, safety, multiplicity, and adaptation rules are unchanged.

## Scale

- Synthetic screens: `12,000`.
- Candidate evaluations: `288,000` per method.
- Resizing uses a blinded variance estimate only; candidate means and outcomes
  are unavailable to the rule.

## Frozen Result

- true noise multiplier `0.75`: **PASS**.
- true noise multiplier `1.00`: **PASS**.
- true noise multiplier `1.25`: **PASS**.
- true noise multiplier `1.50`: **PASS**.

Adaptive donor counts ranged from mean
`12.0` to
`37.5` per context; abstention ranged
`0.000`-`0.004`.
Failed checks: `0` of `120`.

## Meaning

A passing regime would license blinded nuisance-based resizing under these
synthetic assumptions. A failed regime identifies where the donor grid or
pilot precision is inadequate; it cannot be fixed by looking at candidate
effects. Real pilot variance and assay diagnostics remain prerequisites.
