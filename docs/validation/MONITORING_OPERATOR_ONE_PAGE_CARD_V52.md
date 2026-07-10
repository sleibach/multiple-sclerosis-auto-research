# Monitoring Operator One-Page Card V52

Date: 2026-07-10

Status: operator quick card. This document adds no evidence and changes no
validation rule. It is a compact pointer to the frozen package receipt,
command, and interpretation artifacts.

## Use Only For

Gafson/Karolinska-style or equivalent DMF-like MS treatment-response packages
with paired baseline and early on-treatment PBMC expression plus subject-level
response labels.

Do not use this card for chr1 target-development, postpartum, T/B compartment,
or pharmacodynamic-only packages.

## Stop Before Scoring Unless All Are True

| check | required state |
|---|---|
| access terms | approved for intended local analysis |
| quarantine | files under non-committed `data/quarantine/<package_id>/` or equivalent |
| checksums | `SHA256_MANIFEST.tsv` verifies |
| raw git risk | no raw/private/quarantine file tracked or staged |
| package type | classified as paired treatment-response monitoring package |
| fields | baseline sample, early sample, subject ID, response label, feature annotation, module coverage |

If any item fails, use the incoming-package communication templates and do not
score.

## Command Sequence

Run only the command sequence in:

`docs/validation/MONITORING_VALIDATION_COMMAND_MANIFEST_V52.md`

The sequence is:

1. interpreter precheck;
2. receipt/quarantine and checksum verification;
3. outcome dictionary validation;
4. intake preflight;
5. module coverage;
6. subject map;
7. preregistration confirmation;
8. synthetic harness self-test;
9. frozen primary harness.

## Result Class

Map the output to exactly one:

| class | meaning |
|---|---|
| `PASS_CLEAN` | externally supported early pharmacodynamic monitor in that context |
| `PASS_IMMUNE_TONE_BOUNDED` | useful only as immune-tone-aware bounded monitor |
| `PASS_NON_SPECIFIC` | dynamic signal exists but intended biology not validated |
| `INCONCLUSIVE_UNDERPOWERED` | effect estimate only; neither pass nor kill |
| `FAIL_ADEQUATE_POWER` | materially weakens the DMF/MS monitoring branch |
| `UNSCOREABLE_DATA` | no biological inference; package cannot test the rule |

Use:

- `docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`
- `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md`
- `docs/validation/MONITORING_VALIDATION_RESULT_REPORT_TEMPLATE_V52.md`

## Never Do

- do not tune the score, sign, threshold, feature set, endpoint, or timepoint;
- do not treat an underpowered estimate as pass or kill;
- do not call validation clinical utility;
- do not use target-development data as monitoring validation;
- do not run exploratory rescue analyses in the validation report;
- do not commit private/raw/quarantined data.

## Final Output

Fill:

`docs/validation/MONITORING_VALIDATION_RESULT_REPORT_TEMPLATE_V52.md`

Then update route status only through:

`docs/reports/THERAPEUTIC_ROUTE_DECISION_LOG_TEMPLATE_V52.md`

## Source Artifacts

- `docs/validation/PACKAGE_CHECKSUM_INTAKE_CHECKLIST_V52.md`
- `docs/validation/MONITORING_VALIDATION_COMMAND_MANIFEST_V52.md`
- `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md`
- `docs/validation/MONITORING_VALIDATION_RESULT_REPORT_TEMPLATE_V52.md`
- `docs/validation/INCOMING_PACKAGE_COMMUNICATION_TEMPLATES_V52.md`
