# External Knowledge Corpus

Status: external-knowledge storage boundary. This tree is separate from the
project-grounded corpus.

External knowledge records may be placed here only if they pass
`scripts/v47_provenance_gate.py`.

Required principle:

- every external claim is explicitly marked as `external-verifiable` or
  `external-unverifiable`;
- every external claim has a source and date accessed;
- every external claim carries `not_project_grounded_marker:
  "NOT_PROJECT_GROUNDED"`;
- no external record is a project finding;
- no external record changes locked rules, preregistrations, or grounded
  conclusions.

Machine-readable external claim records belong under `knowledge_external/records/`.
Structural-prediction records and their confidence payloads belong under
`knowledge_external/structures/` and must also pass the V51 structural gate.
Class-aware syntheses and catalogues belong under `knowledge_external/synthesis/`
or a dedicated subdirectory created with the same provenance fields.
