# Sample-ID Canonicalization and De-Identification Template V45

Status: metadata-repair template. No data received or analyzed.

Purpose: define allowed sample/subject ID repair and de-identification steps
before intake preflight or subject-map sanity.

Machine-readable template:

`docs/validation/input_schemas/V45_sample_id_canonicalization_template.tsv`

## Allowed Transformations

Allowed when documented before scoring:

- trim whitespace;
- remove harmless file suffixes/prefixes if source documentation proves mapping;
- strip Ensembl version suffixes for feature IDs under V42 preprocessing rules;
- map private subject IDs to study-local pseudonyms;
- map sample file names to sample IDs using an author-provided manifest.

## Disallowed Transformations

Not allowed:

- infer sample pairing from public sample order;
- choose between ambiguous samples using outcome or module scores;
- drop samples because they weaken the result;
- reassign response labels based on expression;
- commit private identifiers when a pseudonym is sufficient.

## Required Mapping Columns

Every repair map should contain:

- raw ID;
- canonical ID;
- ID type;
- transformation rule;
- evidence source;
- whether private ID is retained outside git;
- operator/date.

## Guardrail

The mapping is metadata infrastructure. It does not certify that subject pairs
are valid; subject-map sanity must still pass after canonicalization.
