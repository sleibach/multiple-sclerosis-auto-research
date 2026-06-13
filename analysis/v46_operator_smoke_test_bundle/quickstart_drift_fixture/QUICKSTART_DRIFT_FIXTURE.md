# Quickstart Drift Fixture V46

Status: synthetic documentation-regression fixture. No validation result and no biological claim.

Overall status: `PASS`; cases: `4`; expectation failures: `0`.

| Case | Mutation | Expected | Observed | Missing commands |
|---|---|---|---|---:|
| `exact_generated_quickstart` | none | `PASS` | `PASS` | `0` |
| `edited_handoff_command` | changed first handoff command outdir | `FAIL` | `FAIL` | `1` |
| `edited_receipt_branch_command` | changed scoreable receipt-branch expectation | `FAIL` | `FAIL` | `1` |
| `removed_boundary_text` | removed no-biological-claim boundary | `FAIL` | `FAIL` | `0` |

Boundary: these fixtures mutate copied quickstart Markdown only. They do not
read returned score values or change the generated quickstart source tables.
