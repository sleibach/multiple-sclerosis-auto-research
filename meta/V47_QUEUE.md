# V47 Queue: External Knowledge Segregation and Expansion

Block start UTC: 2026-06-13T18:35:06Z
Target UTC (+360 min): 2026-06-14T00:35:06Z

## Stop Conditions

Valid stops only:

1. cumulative measured runtime >= 360 minutes and clean resumable point;
2. external termination;
3. documented all-fronts block after every internally executable alternative is exhausted.

Backlog exhaustion is not a stop. When executable todo items drop below five,
generate more internally executable tasks before continuing.

## Phase 0 Rule

No external knowledge integration occurs until:

- `docs/knowledge/EPISTEMIC_CLASSES.md` exists;
- `knowledge_external/` exists;
- `scripts/v47_provenance_gate.py synthetic-check --fail-on-error` passes;
- `scripts/v47_provenance_gate.py audit --fail-on-error` passes.

## Iterations

| Iteration | Start UTC | End UTC | Status | Notes |
|---|---:|---:|---|---|
| 1 | 2026-06-13T18:35:06Z | 2026-06-13T18:43:20Z | done | Built Phase 0 epistemic-class definitions, separate external storage tree, JSON schema, and provenance gate with synthetic and real audit PASS before external integration. |
| 2 | 2026-06-13T18:43:20Z | 2026-06-13T18:46:31Z | done | Integrated the V47 provenance gate into the generated-checker registry, stale-output detector, and synthetic/method artifact index. Regenerated governance outputs; registry PASS (`118` scripts), stale detector PASS (`65` artifacts, `0` stale), generated-doc freshness PASS (`34` checks), provenance audit PASS. |
| 3 | 2026-06-13T18:47:37Z | 2026-06-13T18:49:00Z | done | Added the empty external source-catalog skeleton under `knowledge_external/catalogs/` plus a resource-record schema. Fixed the provenance gate to skip catalog schemas and structural catalog README files while still auditing real JSON records. Synthetic and real provenance audits PASS; no external source records added. |
| 4 | 2026-06-13T18:49:00Z | 2026-06-13T18:53:56Z | done | Added `scripts/v47_external_knowledge_index.py`, a class-aware external-record index generator with synthetic fixtures. Real index generated under `knowledge_external/catalogs/indexes/` with `0` records; synthetic aggregation PASS (`2` fixture records, class counts preserved). Governance outputs refreshed: registry PASS (`119` scripts), stale detector PASS (`66` artifacts), provenance audit PASS. |
| 5 | 2026-06-13T18:53:56Z | 2026-06-13T18:59:15Z | done | Verified official/primary public pages and added 8 external-unverifiable resource records: MSGD, MS Data Alliance Catalogue, MSBase, NARCOMS, IMSGC, GWAS Catalog, DISGENET, and Open Targets. Real external index PASS (`8` records, `0` missing source/marker); provenance audit PASS (`73` checks, `8` records, `0` failures). |
| 6 | 2026-06-13T18:59:15Z | 2026-06-13T19:04:33Z | done | Verified official/primary public pages and added 13 external-unverifiable resource records for literature, functional genomics, controlled genomics, sequencing archives, clinical trials, and general repositories: PubMed, Europe PMC, GEO, EGA, ArrayExpress/BioStudies, BioStudies, SRA, ENA, ClinicalTrials.gov, Zenodo, Figshare, Dryad, and OSF. Real external index PASS (`21` records total); provenance audit PASS (`190` checks, `21` records, `0` failures); stale detector PASS. |
| 7 | 2026-06-13T19:04:33Z | 2026-06-13T19:09:22Z | done | Added dependency-free external-record schema linter because local `jsonschema` is unavailable. Synthetic fixture PASS (`4/4` assertions; bad records intentionally fail lint); real lint PASS (`21` records, `420` checks, `0` failures). Governance refreshed: registry PASS (`120` scripts), stale detector PASS (`67` artifacts), provenance audit PASS (`190` checks). |
| 8 | 2026-06-13T19:10:54Z | 2026-06-13T19:17:53Z | done | Added class-preserving external resource category rollup. Synthetic fixture PASS (`4/4` checks); real rollup PASS (`21` resources, `7` categories, `0` missing not-grounded markers). Corrected category routing with explicit resource-token mappings. Governance refreshed: generated-checker registry PASS (`121` scripts), stale detector PASS (`68` artifacts), doc freshness PASS, provenance audit PASS (`190` checks). |
| 9 | 2026-06-13T19:19:39Z | 2026-06-13T19:23:08Z | done | Added class-aware convergence/contradiction placeholder skeleton. Synthetic fixture PASS (`5/5` checks); real skeleton PASS (`21` placeholder rows, `0` linked rows, `0` missing sources/markers). Provenance audit PASS (`190` checks), stale detector PASS (`69` artifacts). |
| 10 | 2026-06-13T19:23:54Z | 2026-06-13T19:26:56Z | done | Added relationship-to-project-finding controlled vocabulary docs and linter. Synthetic fixture PASS (`4/4` checks; bad fixtures intentionally fail underlying lint); real lint PASS (`21` records, `63` checks, `0` failures). Provenance audit PASS and stale detector PASS (`70` artifacts). |
| 11 | 2026-06-13T19:27:43Z | 2026-06-13T19:31:31Z | done | Added 5 source-verified public MS clinical/reference resource records: National MS Society, MSIF Atlas of MS, NICE NG220, NINDS MS CDE, and MS Society UK. All are `external-unverifiable` and `NOT_PROJECT_GROUNDED`. Index PASS (`26` records), category rollup PASS (`26` resources, `9` categories), schema lint PASS (`520` checks), relationship lint PASS (`78` checks), provenance audit PASS (`235` checks). |

## Live Backlog

| Priority | Front | Item | Status | Notes |
|---:|---|---|---|---|
| 1 | Phase 0 segregation | Define epistemic classes and external storage boundary | done | `docs/knowledge/EPISTEMIC_CLASSES.md`, `knowledge_external/README.md`, schema, and placeholder external record/synthesis dirs added. |
| 2 | Phase 0 segregation | Implement provenance gate with synthetic pass/fail fixtures | done | `scripts/v47_provenance_gate.py`; synthetic check PASS (`4` cases, `3` expected failures caught); real audit PASS (`0` failures, `0` external records). |
| 3 | Phase 0 segregation | Integrate provenance gate into generated-checker/stale-output governance | done | V47 gate now appears in generated-checker, stale-output, and V43-V47 artifact-governance indices; all regenerated checks PASS. |
| 4 | Competitor/source cataloging | Create classed competitor-source catalog skeleton without external claims | done | Added `knowledge_external/catalogs/README.md`, `resource_record.schema.json`, `resources/`, and `indexes/`; no source facts integrated yet. |
| 5 | Navigation/index | Create class-aware external knowledge index generator | done | `scripts/v47_external_knowledge_index.py`; real empty index under `knowledge_external/catalogs/indexes/`; synthetic fixture PASS. |
| 6 | External integration | MSGD resource metadata record and source catalog entry | done | `knowledge_external/catalogs/resources/msgd_database_commons.json`; source verified via Database Commons. |
| 7 | External integration | MS Data Alliance Catalogue resource metadata record and source catalog entry | done | `knowledge_external/catalogs/resources/msda_catalogue.json`; source verified via MSDA Catalogue page. |
| 8 | External integration | MSBase/NARCOMS/IMSGC/GWAS Catalog comparator records | done | Records added for MSBase, NARCOMS, IMSGC, and GWAS Catalog after source verification. |
| 9 | Governance | Add an external-record index generator and synthetic fixtures proving class labels survive aggregation | done | Same output as item 5; synthetic fixture proves class labels survive aggregation. |
| 10 | External integration | DisGeNET and Open Targets comparator records | done | Records added after source verification; both retained as external-unverifiable resource metadata. |
| 11 | External integration | PubMed/Europe PMC, GEO, EGA, and ArrayExpress/BioStudies source records | done | Records added after source verification; includes BioStudies as its own resource record. |
| 12 | Synthesis | Create class-aware convergence/contradiction skeleton that reads the external index but contains no claims until records exist | done | `scripts/v47_convergence_contradiction_skeleton.py`; real skeleton has `21` placeholder rows, `0` linked rows, and no convergence/contradiction conclusions. |
| 13 | External integration | ClinicalTrials.gov, Zenodo, Figshare, Dryad, and OSF source records | done | Records added after source verification; SRA and ENA added as additional sequence-archive acquisition routes. |
| 14 | Governance | Add optional resource-record JSON schema validation checker when `jsonschema` is available, with graceful unavailable status | done | Implemented dependency-free required-field/schema linter instead: `scripts/v47_external_record_schema_linter.py`; real records PASS (`420` checks, `0` failures). |
| 15 | External integration | MS-specific landmark external knowledge records for current disease-course and DMT mechanisms | todo | Must be external-classed with sources; no changes to grounded conclusions. |
| 16 | Navigation/index | Add resource-category rollup for external records so public readers can browse by literature / registry / genetics / data repository | done | `scripts/v47_external_resource_category_rollup.py`; outputs under `knowledge_external/catalogs/indexes/`; synthetic and real rollups PASS. |
| 17 | External integration | MS society/clinical-reference resources for public-reader disease-course context | done | Added source-verified external-unverifiable records for National MS Society, MS Society UK, MSIF Atlas, NICE NG220, and NINDS MS CDE. |
| 18 | Governance | Add relationship-to-project-finding controlled vocabulary documentation and lint examples | done | `docs/knowledge/RELATIONSHIP_TO_PROJECT_FINDINGS_V47.md`; `scripts/v47_relationship_vocabulary_linter.py`; real lint PASS (`21` records, `63` checks). |
| 19 | Navigation/index | Add source-access-tier rollup for open / registration / application / controlled / mixed resources | todo | Reads `knowledge_external` only; preserves class/source markers; helps readers distinguish immediately usable public resources from controlled resources. |
| 20 | Governance | Add markdown index linter to verify generated external index tables retain source URLs or labels per external row | todo | Should catch classed rows rendered without provenance in generated navigation docs. |
| 21 | External integration | Add authoritative public clinical-reference resource records for MS disease course and relapse/progression context | done | Covered by iteration 11 public clinical/reference resource records; no grounded findings changed. |
| 22 | External integration | Add public DMT mechanism/reference resource records for FDA/EMA labels or authoritative drug monographs | todo | External context only; no treatment-response rule changes. |
| 23 | Synthesis | Build class-aware convergence/contradiction skeleton with empty grounded-link rows until specific claim records exist | todo | Must live under `knowledge_external/synthesis/` and label every row by epistemic class. |

## Running Notes

- 2026-06-13T18:35:06Z: V47 started. OpenGWAS check passed with JWT valid to
  `2026-06-19 12:28 UTC` (`RENEW_SOON`). SAP AI Core health passed for Claude,
  Gemini, and RPT. No external knowledge has been integrated.
- 2026-06-13T18:43:20Z: Phase 0 segregation verification complete. Provenance
  gate synthetic check PASS (`4` synthetic cases, `3` intentional failure
  cases caught: missing source, external marker in grounded tree, and external
  as project evidence). Real repository audit PASS (`1` check, `0` failures,
  `0` external JSON records). External integration is now permitted only under
  `knowledge_external/` with the gate passing every iteration.
- 2026-06-13T18:46:31Z: Governance integration complete. V47 provenance gate is
  now tracked by `scripts/v45_generated_checker_registry.py`,
  `scripts/v45_readiness_stale_output_detector.py`, and
  `scripts/v45_synthetic_artifact_index.py`. Regenerated outputs pass:
  generated-checker registry `PASS` (`118` scripts), stale-output detector
  `PASS` (`65` artifacts, `0` stale/missing), generated-doc freshness `PASS`
  (`34` checks), and V47 provenance audit `PASS`.
- 2026-06-13T18:49:00Z: External source-catalog skeleton added without any
  external source records. Provenance gate skip rules tightened so
  `*.schema.json` catalog schemas and known structural external READMEs are not
  mistaken for claim records; synthetic fixtures and real audit pass.
- 2026-06-13T18:53:56Z: External knowledge index generator added. Synthetic
  aggregation fixture PASS (`2` synthetic records, `4/4` checks), real external
  index PASS with `0` records because no external sources have been integrated
  yet. Governance refreshed: generated-checker registry `PASS` (`119` scripts),
  stale-output detector `PASS` (`66` artifacts, `0` stale/missing), generated
  doc freshness `PASS`, provenance audit `PASS`.
- 2026-06-13T18:59:15Z: First external resource batch integrated under strict
  segregation. Eight records added under `knowledge_external/catalogs/resources/`
  only: MSGD, MSDA Catalogue, MSBase, NARCOMS, IMSGC, GWAS Catalog, DISGENET,
  and Open Targets. All are `external-unverifiable` resource metadata and
  explicitly `NOT_PROJECT_GROUNDED`. Real index reports `8` records with
  `0` missing source/marker; provenance gate reports `73` checks, `8` external
  JSON records, `0` failures. Local `jsonschema` module was unavailable; the
  committed provenance gate and index required-field checks were used.
- 2026-06-13T19:04:33Z: Second external resource batch integrated under strict
  segregation. Thirteen records added for PubMed, Europe PMC, GEO, EGA,
  ArrayExpress/BioStudies, BioStudies, SRA, ENA, ClinicalTrials.gov, Zenodo,
  Figshare, Dryad, and OSF. All are `external-unverifiable` resource metadata
  and explicitly `NOT_PROJECT_GROUNDED`. Real external index reports `21`
  records total with `0` missing source/marker; provenance gate reports `190`
  checks, `21` external JSON records, `0` failures; stale-output detector
  `PASS`.
- 2026-06-13T19:09:22Z: Dependency-free external-record schema linter added:
  `scripts/v47_external_record_schema_linter.py`. Synthetic assertions PASS
  (`4/4`, with missing-source and bad-marker records intentionally failing the
  underlying lint). Real linter PASS (`21` records, `420` checks, `0` failures).
  Governance refreshed: generated-checker registry `PASS` (`120` scripts),
  stale-output detector `PASS` (`67` artifacts), generated-doc freshness
  `PASS`, provenance audit `PASS` (`190` checks).
- 2026-06-13T19:17:53Z: Class-preserving external resource category rollup
  added. The rollup is navigation only, reads only
  `knowledge_external/catalogs/resources/*.json`, and preserves epistemic class,
  source, relationship, access tier, and `NOT_PROJECT_GROUNDED`. Synthetic
  fixture PASS (`4/4` checks); real rollup PASS (`21` resources, `7`
  categories, `0` missing markers). Provenance audit PASS (`190` checks, `21`
  records, `0` failures); stale detector PASS (`68` tracked artifacts).
- 2026-06-13T19:23:08Z: Class-aware convergence/contradiction skeleton added
  under `knowledge_external/synthesis/`. It is placeholder-only: `21` external
  resource rows, `0` linked project findings, `0` missing sources, `0` missing
  `NOT_PROJECT_GROUNDED` markers. Synthetic fixture PASS (`5/5` checks).
  Provenance audit PASS (`190` checks, `21` records, `0` failures); stale
  detector PASS (`69` tracked artifacts).
- 2026-06-13T19:26:56Z: Relationship-to-project-finding vocabulary
  documentation and linter added. `supports` and `contradicts` now require a
  concrete `project_finding_reference` in the linter before they can be used;
  `orthogonal` and `untested` do not create convergence claims. Synthetic
  fixture PASS (`4/4` checks; bad relationship and unsupported `supports`
  fixtures intentionally fail the underlying lint). Real lint PASS (`21`
  records, `63` checks, `0` failures); stale detector PASS (`70` artifacts).
- 2026-06-13T19:31:31Z: Five public MS clinical/reference resource records
  added after source verification: National MS Society Types of MS, MSIF Atlas
  of MS, NICE NG220, NINDS MS Common Data Elements, and MS Society UK Types of
  MS. All are `external-unverifiable` resource metadata and explicitly
  `NOT_PROJECT_GROUNDED`. Real external index PASS (`26` records), category
  rollup PASS (`26` resources, `9` categories), schema lint PASS (`520`
  checks), relationship lint PASS (`78` checks), convergence skeleton PASS
  (`26` placeholder rows, `0` linked rows), provenance audit PASS (`235`
  checks, `26` records, `0` failures), stale detector PASS (`70` artifacts).
