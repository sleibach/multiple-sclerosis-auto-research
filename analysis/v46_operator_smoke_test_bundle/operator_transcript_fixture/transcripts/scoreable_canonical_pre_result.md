# Operator Transcript Fixture: scoreable_canonical_pre_result

Status: synthetic operator-navigation fixture. No validation result and no biological claim.

Cohort token: `synthetic_scoreable_v46`
Final operator state: `REPORT_SKELETON_READY_NO_VALUES`
Report skeleton: `analysis/v46_operator_smoke_test_bundle/operator_transcript_fixture/report_skeletons/scoreable_canonical_pre_result.md`

| Step | Phase | Observation | Next action |
|---:|---|---|---|
| 1 | `receipt_manifest` | Receipt manifest schema status is `PASS` with `0` schema failures. | Stop for manifest repair if schema failed; otherwise continue to package-shape and command-plan branch. |
| 2 | `first30_status_board` | Status board route is `ROUTE_READY_FOR_GATED_REVIEW`; blocker is `none`. | Returned package is in pre-result gated review; no validation interpretation is available yet. |
| 3 | `safe_class_report_readiness` | Safe class `ELIGIBLE_FOR_PREREGISTERED_INTERPRETATION` maps to report mode `RESULT_SKELETON_ALLOWED_AFTER_GATES`. | Mechanical V42 interpretation skeleton is available. |
| 4 | `report_skeleton` | Report skeleton contains the required locked-rule provenance header before any body text. | A locked-rule report skeleton can be prepared after gates, but this transcript fixture does not populate any result fields. |

Boundary: every step in this transcript is pre-score or stop-only. The
fixture does not open returned score values, labels, expression matrices,
or quarantined real cohort data.
