# V50 Validation-Context Boundary Card

Status: synthesis/navigation only. This card explains why V50 DMF,
steroid/glucocorticoid, and cell-composition sources are useful for validation
planning but do not validate the locked V22 scalar.

Primary sources:

- `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V50.md`
- `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V50.md`
- `docs/validation/PREREGISTRATION_V42.md`
- `docs/workups/treatment_response/CONFOUNDER_AUDIT_V32.md`

## Boundary Statement

V50 added sharper treatment-response and confounder sources. They improve the
validation context, but they are not validation evidence for the locked V22 rule.

The only path that validates the locked V22 scalar is a pre-registered harness
run on an authorized, usable cohort with the required expression, timing,
response labels, and confounder fields.

## Source Classes In V50

| source group | examples | what it can do | what it cannot do |
|---|---|---|---|
| DMF validation-context sources | Gafson 2018, GSE235357, DMF immune-monitoring studies | Identify potentially relevant cohorts or marker contexts. | Validate the frozen V22 scalar without running the harness. |
| Steroid/glucocorticoid sources | methylprednisolone immune-gene suppression, glucocorticoid resistance, B/T-cell methylprednisolone transcriptomes | Support the need for glucocorticoid-response scoring and future steroid-panel stress testing. | Prove the V22 scalar survives steroid adjustment. |
| Cell-composition sources | DMF immune-cell composition shifts, leukocyte ratios, lymphocyte subsets | Support the need for composition diagnostics and deconvolution. | Prove the V22 scalar is not composition-driven. |
| GWAS Catalog allele sources | ZMIZ1, PTGER4, chr1 rsid rows | Provide non-OpenGWAS route inputs for future allele harmonization. | Become project genetics evidence without rerun and harmonization. |

## Correct Wording

Use:

- V50 sharpened the validation context.
- V50 identified steroid and composition sources that support the V32 guard
  design.
- V50 found no external source that independently tests the frozen V22 scalar.
- V50 found no same-definition contradiction.

Avoid:

- V50 externally validated the V22 rule.
- The literature proves the scalar survives confounders.
- Gafson or GSE235357 are evidence before the frozen harness runs.
- Steroid and composition papers settle the confounder audit.

## Practical Implication

The medical-team interpretation should be:

1. V22 remains the locked rule pending real validation.
2. V42/V44 remain the validation plan.
3. V50 improves readiness by identifying specific external source routes and
   diagnostic guard context.
4. V50 does not reduce the need for the actual Gafson or alternative cohort
   harness run.

## Decision

Keep all V50 treatment-response external sources in the external layer as
context, routes, or future-grounding candidates. Do not move them into grounded
findings and do not use them to tune the locked rule.
