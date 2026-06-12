# Batch/QC/Steroid Metadata Dictionary V45

Status: incoming-cohort metadata template. No data received or analyzed.

Purpose: define the technical, QC, cell-composition, and steroid-exposure fields
needed to interpret V22 validation results under the V32/V44 confounder and
batch guardrails.

Machine-readable template:

`docs/validation/input_schemas/V45_batch_qc_steroid_metadata_dictionary.tsv`

## Field Priority

- `required`: needed for basic intake or pairing.
- `strongly_required`: not always available historically, but absence weakens
  interpretation and may prevent a clean pass.
- `optional`: useful for diagnosis but not mandatory.

## Guardrail

Missing batch/QC/steroid fields do not justify post-hoc batch correction of the
primary locked score. They affect interpretation through the preregistered
confounder/batch audit.
