# V50 Public MS Knowledge-Base Position Card

Status: external resource navigation only. This card answers the public-source
comparison question using segregated external-resource metadata and a current
source check. It is not project-grounded evidence, does not alter any finding,
and does not make biological claims.

Question:

> Is there any other public source that offers a similarly comprehensive
> collection of MS information as this repository?

Short answer:

No public 1:1 equivalent was identified in the V47/V50 external-resource
catalog or this V50 source check. Several public or partly public resources are
larger in one dimension, but they are narrower in purpose:

- MSGD is the closest public MS-specific molecular knowledgebase.
- MSDA, MSBase, and NARCOMS are deeper for registry/cohort/clinical metadata or
  longitudinal clinical data, but they are not public rerunnable molecular
  analysis corpora.
- GWAS Catalog, GEO, SRA/ENA, PubMed/Europe PMC, and general repositories are
  broader source archives, not an MS-specific synthesized evidence repository.

The distinctive public position of this repository is the combination of:

1. grounded rerunnable project analyses;
2. locked rules and pre-registrations;
3. explicit negative/kill records;
4. validation-readiness and synthetic harness tests;
5. a segregated external-knowledge layer with machine-enforced provenance.

That combination was not found in a single public MS resource.

## Closest Public Comparators

| resource | public status | what it is stronger at | why it is not a 1:1 equivalent |
|---|---|---|---|
| MSGD / Multiple Sclerosis Gene Database | public database / publication | MS-specific gene-level curated evidence across variant, RNA, protein, knockout, drug, and high-throughput entries. Source check: https://academic.oup.com/database/article/doi/10.1093/database/baae037/7681856 | It is a curated gene-entry database, not a rerunnable project corpus with locked rules, validation harnesses, negative lead history, and confounder-audited biomarker workflow. |
| MS Data Alliance Catalogue | public with account / metadata catalogue | Discovery of MS real-world-data cohort metadata; the catalogue reports metadata/descriptive data rather than showing the real data. Source check: https://msda.emif-catalogue.eu/ and https://www.ijmsc.org/view/the-multiple-sclerosis-data-alliance-catalogue | It is a cohort/registry metadata discovery system, not a public molecular-analysis evidence corpus. |
| MSBase Registry | application / clinician registry | Large international longitudinal clinical outcomes registry. Source check: https://www.msbase.org/ and https://www.msbase.org/about-us/ | It is deeper clinically and longitudinally, but not publicly downloadable as a cross-modal analysis repository and not a locked-rule validation corpus. |
| NARCOMS Registry | participant registry / researcher access | Patient-reported longitudinal MS experience, symptoms, treatments, and outcomes. Source check: https://www.narcoms.org/ and https://clinicaltrials.gov/study/NCT01018537 | It is a registry resource, not a public integrated omics/genetics/transcriptomics analysis corpus. |
| NHGRI-EBI GWAS Catalog | public | Curated association records across traits and diseases. Source check: https://www.ebi.ac.uk/gwas/ | It is broader and better for association lookup, but not MS-specific synthesis with direction-matched project interpretation and kill records. |
| GEO / SRA / ENA / ArrayExpress / BioStudies | public archives | Raw and processed study-level data discovery. Source check: `knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md` | They are input archives. They do not provide the project-level synthesis, locked rules, or validation-readiness layer. |
| PubMed / Europe PMC | public literature search | Literature discovery and data-availability mining. Source check: `knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md` | They are literature indexes, not rerunnable analysis artifacts. |

## What This Repository Does Not Replace

This repository is not the best public source for every MS question:

- For exhaustive MS gene-entry lookup, start with MSGD.
- For registry/cohort discovery, start with MSDA Catalogue.
- For real-world longitudinal outcomes, MSBase and NARCOMS are deeper, subject
  to their access models.
- For raw data discovery, use GEO/SRA/ENA/ArrayExpress/BioStudies.
- For literature search, use PubMed and Europe PMC.
- For association lookup, use GWAS Catalog and IMSGC publications/resources.

The repository's value is not replacing those resources. Its value is the
cross-resource, project-grounded interpretation layer, including negative
results and validation machinery.

## Why The Repository Is Unusual Publicly

Most public MS resources are optimized for one of these roles:

- archive data;
- catalogue cohorts;
- curate genes/targets;
- collect registry outcomes;
- index literature;
- provide clinical or regulatory context.

This repository is closer to a transparent research operating system:

- It records live hypotheses, kills, demotions, and locked rules.
- It separates grounded project outputs from external context.
- It keeps validation harnesses and pre-registrations alongside findings.
- It treats negative results as first-class outputs.
- It records operational constraints such as token expiry, data quarantine,
  batch-risk handling, and push/hygiene state.

That breadth is useful, but the evidence classes differ. The grounded core is
rerunnable project evidence. The external layer is navigation/context only.

## Current Position Statement

Use this conservative wording:

> I do not know of a public MS resource that combines this repo's breadth of
> cross-modal grounded analyses, locked validation machinery, negative-result
> ledger, and provenance-segregated external knowledge. MSGD is the closest
> public MS molecular knowledgebase; MSDA/MSBase/NARCOMS are deeper for clinical
> cohort or registry dimensions; public archives are broader inputs. None is a
> 1:1 replacement for this repository's integrated, rerunnable research record.

Avoid this wording:

> This is the most comprehensive public MS source.

That would overstate the comparison. Other resources are more comprehensive
within their own domains; the repo is unusual because it integrates grounded
analysis, validation discipline, and external context in one public record.

## Provenance

- Internal comparator source:
  `knowledge_external/catalogs/indexes/EXTERNAL_RESOURCE_COMPARATOR_MATRIX_V48.md`
- Internal source-domain/index sources:
  `knowledge_external/INDEX.md`
- MSGD source check:
  https://academic.oup.com/database/article/doi/10.1093/database/baae037/7681856
- MSDA source checks:
  https://msda.emif-catalogue.eu/
  https://www.ijmsc.org/view/the-multiple-sclerosis-data-alliance-catalogue
- MSBase source checks:
  https://www.msbase.org/
  https://www.msbase.org/about-us/
- NARCOMS source checks:
  https://www.narcoms.org/
  https://clinicaltrials.gov/study/NCT01018537
- GWAS Catalog source:
  https://www.ebi.ac.uk/gwas/

Date accessed: 2026-06-28.
