# V42 Synthetic Harness Validation

These data are synthetic and were generated only to test the frozen validation mechanics.

| Scenario | Expected | Verdict | AUC | Hedges g | Receptor AUC |
|---|---|---|---:|---:|---:|
| null | must not pass | `FAIL_ADEQUATE_POWER` | 0.520 | 0.029 | 0.309 |
| planted | must pass | `PASS_CLEAN` | 1.000 | 6.979 | 0.282 |

Pass criteria for this harness self-test:

- null synthetic cohort final verdict is not `PASS_CLEAN` or `PASS_PROVISIONAL_SMALL_N`;
- planted synthetic cohort final verdict is `PASS_CLEAN`;
- both cohorts write the same core artifacts expected from a future Gafson run.
