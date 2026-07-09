# Epistemic Classes

Status: V47 governance architecture. No external knowledge is integrated by this
document.

## Purpose

The repository now supports two broad knowledge families:

- the existing project-grounded corpus, produced by rerunnable project analyses;
- a separate external-knowledge corpus, read from public resources or literature
  and never treated as project evidence until independently grounded.

The purpose of this document is to define the classes and the storage boundary
before any external knowledge is added.

## Classes

### `grounded`

Produced by this project, rerunnable on held data, and governed by the existing
locked-rule, validation, null-testing, and synthetic-quarantine discipline.

Rules:

- stored in the existing project trees such as `docs/`, `analysis/`,
  `knowledge/`, `meta/`, `scripts/`, and `data/`;
- unchanged by V47;
- may cite external records only as context, never as evidence unless the claim
  has been independently grounded by a committed project analysis.

### `external-verifiable`

An external claim from a public source that the project could test later on
reachable data, but has not yet grounded.

Rules:

- stored only under `knowledge_external/`;
- must have source, access date, relationship-to-project tag, and
  `not_project_grounded_marker: "NOT_PROJECT_GROUNDED"`;
- must include a future grounding route;
- is a queued context/hypothesis item, not a project finding.

### `external-unverifiable`

External knowledge the project cannot currently reground, such as literature
assertions, database annotations, curated resource metadata, expert consensus,
model-generated review text, or predicted protein structures.

Rules:

- stored only under `knowledge_external/`;
- must have source, access date, relationship-to-project tag, and
  `not_project_grounded_marker: "NOT_PROJECT_GROUNDED"`;
- must include a `why_unverifiable` field;
- is useful context only and is never evidence for a project conclusion.

## Structural-Prediction Records

AlphaFold and related predicted structures are a specialized
`external-unverifiable` record type. They are predictions, not experimental
structures and not project-grounded findings.

Required fields for every structural-prediction record:

- `record_type: "structural_prediction"`;
- `epistemic_class: "external-unverifiable"`;
- `not_project_grounded_marker: "NOT_PROJECT_GROUNDED"`;
- `predicted_structure_not_experimental_marker:
  "PREDICTED_STRUCTURE_NOT_EXPERIMENTAL"`;
- `protein.uniprot_id`, `protein.gene_symbol`, `protein.sequence`, and
  `protein.sequence_source`;
- `model.source`, `model.model_entity_id`, `model.model_version`,
  `model.source_url`, and `model.retrieval_date`;
- confidence metadata with per-residue pLDDT and PAE provenance:
  `confidence.plddt.mean`, `confidence.plddt.per_residue_path`,
  `confidence.pae.mean`, and `confidence.pae.matrix_path` or a source URL for
  the full PAE matrix if the matrix is too large to commit safely;
- a source citation or URL and access date;
- `why_unverifiable`, explaining that the structure is a computational
  prediction unless corroborated by an experimental PDB structure.

Rules:

- stored only under `knowledge_external/structures/`;
- never copied into grounded trees;
- never cited as evidence for a project conclusion;
- may inform a druggability-direction assessment only as prediction-informed
  context, with confidence attached;
- low-confidence regions must be flagged before any downstream use;
- if an experimental PDB structure exists later, it is a separate record and
  does not make the prediction ground truth.

## Storage Boundary

External records live only in:

- `knowledge_external/records/`
- `knowledge_external/structures/` for structural-prediction records and their
  referenced confidence payloads
- `knowledge_external/synthesis/`
- `knowledge_external/catalogs/` when created later

External claims must not be added to grounded trees. If a synthesis needs to
compare grounded and external classes, it belongs under `knowledge_external/`
and must label every external claim with its class and source.

## Machine Enforcement

The V47 provenance gate is:

```bash
.venv/bin/python scripts/v47_provenance_gate.py audit --fail-on-error
```

Synthetic gate verification is:

```bash
.venv/bin/python scripts/v47_provenance_gate.py synthetic-check --outdir analysis/v47_provenance_gate --fail-on-error
```

The gate must pass before any external knowledge is integrated and after every
V47 iteration.

The V51 structural-prediction gate is:

```bash
.venv/bin/python scripts/v51_structural_prediction_gate.py audit --fail-on-error
```

Synthetic structural gate verification is:

```bash
.venv/bin/python scripts/v51_structural_prediction_gate.py synthetic-check --outdir analysis/v51_structural_prediction_gate --fail-on-error
```
