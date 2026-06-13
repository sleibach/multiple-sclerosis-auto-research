# External Source Catalogs

This directory is the only allowed home for V47 external-source catalog records.
Catalog records are navigation/provenance metadata, not project-grounded
findings.

Every resource record must:

- use an external epistemic class;
- include a source URL, DOI, or other verifiable citation;
- include `date_accessed`;
- include `not_project_grounded_marker: "NOT_PROJECT_GROUNDED"`;
- state whether the resource relationship to project findings is `supports`,
  `contradicts`, `orthogonal`, or `untested`;
- state whether any claim is externally testable later or remains unverifiable.

No resource catalog entry may be copied into grounded report, validation,
locked-rule, workup, or history trees. If a resource raises a testable idea, it
is queued for future grounding; until grounded, it remains external context only.

Subdirectories:

- `resources/`: one JSON record per external public MS resource or database.
- `indexes/`: generated class-aware indexes over external resource records.

