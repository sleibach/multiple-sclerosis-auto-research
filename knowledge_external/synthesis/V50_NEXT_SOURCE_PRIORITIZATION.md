# V50 Next Source Prioritization

Status: synthesis/navigation only. This ranking prioritizes external-source
routes for future work while OpenGWAS is expired. It does not execute grounding,
add biological evidence, or change any project finding.

Primary inputs:

- `knowledge_external/synthesis/FUTURE_GROUNDING_QUEUE_V50.md`
- `knowledge_external/synthesis/V50_GWAS_CATALOG_ALLELE_ROUTING.md`
- `knowledge_external/synthesis/V50_ALLELE_HARMONIZATION_CHECKLIST.md`
- `knowledge_external/synthesis/V50_GSE255952_IMPORT_CHECKLIST.md`
- `knowledge_external/synthesis/V50_V22_V32_CONTRADICTION_TRIGGER_PACKET.md`
- `knowledge_external/synthesis/V50_CANDIDATE_SOURCE_PARKING_QUEUE.md`

OpenGWAS status: expired. All priorities below avoid OpenGWAS unless explicitly
marked blocked until renewal.

## Ranking Rules

Scores are routing scores, not evidence scores.

| field | scale | meaning |
|---|---:|---|
| decision value | 1-5 | How much the route could change validation readiness, contradiction surveillance, or source-specific interpretation if grounded. |
| executability now | 1-5 | How feasible the route is without OpenGWAS and without restricted validation data. |
| boundary risk | 1-5 | Risk that the route will be overread as evidence before rerun; higher means stricter wording/checklists needed. |

Priority order favors high decision value and executability, with boundary risk
managed by explicit checklists.

## Immediate Non-OpenGWAS Routes

| rank | route | queue id(s) | decision value | executability now | boundary risk | recommended next action |
|---:|---|---|---:|---:|---:|---|
| 1 | GWAS Catalog rsid fetcher + allele-harmonization inputs | `V50_FG_001`, `V50_FG_002`, `V50_FG_003` | 4 | 5 | 3 | Implement reusable GWAS Catalog fetcher, validate against the existing V50 TSV, then run allele-harmonization as a separate grounded task. |
| 2 | GSE255952 metadata-to-import readiness for steroid-panel stress testing | `V50_FG_012` | 4 | 3 | 4 | Keep as metadata/checklist until a scoped import task satisfies the stop/go checklist; do not route as V22 validation. |
| 3 | V22/V32 contradiction trigger packet application to new treatment-response hits | `V50_FG_004`, `V50_FG_005` plus future hits | 5 | 2 | 5 | Use trigger packet to classify sources, but run no validation claims until authorized expression/label packages are available. |
| 4 | Held B-cell MIF/CD74/CXCR4 context check if indexed held data are already available | `V50_FG_009` | 3 | 3 | 3 | First confirm held-data availability without new source intake; if unavailable, keep context-only. |
| 5 | Candidate-source release review for T/B and EBV parked hits | parking queue | 3 | 2 | 4 | Review one source at a time only if it can meet same-definition release conditions; do not add relationship rows from broad context. |

## Blocked But High-Value Routes

| route | queue id(s) | blocker | why it matters |
|---|---|---|---|
| Gafson DMF PBMC/NEDA-4 frozen harness | `V50_FG_004` | Authorized usable expression/label package not available or quarantined until approved. | Primary V22 validation route; highest clinical relevance. |
| GSE235357 DMF PBMC response context | `V50_FG_005` | Needs repository data retrieval, paired/sample-label verification, module gene coverage, and valid routing through a pre-registered harness. | Could reduce single-cohort dependence if it has usable paired response data. |
| PANTS Crohn anti-TNF expression route | `V50_FG_006` | Source data locator/access and permitted reuse review. | Could test downstream IFN/APC transfer in a non-MS comparator layer. |
| IMID anti-TNF single-cell atlas | `V50_FG_007` | Data access/reuse and mapping review. | Could externally stress the layer-specific transfer-validity map. |
| EBV anti-CNS B-cell APC source | `V50_FG_008` | Data access, source status, and comparator controls. | Could eventually test EBV/APC specificity rather than broad EBV relevance. |

## Do-Not-Spend-Now Routes

| route | reason to defer |
|---|---|
| Generic DMF immune monitoring sources without frozen V22 fields | They sharpen context but cannot classify V22 convergence/contradiction under the trigger packet. |
| Steroid/composition papers without rerunnable expression data | They support validation guards but do not change V32. |
| Orphan target/database context for GPR25 | Already sufficient for caution; no new disease-direction evidence. |
| Broad EBV-MS papers without autoimmune comparator expression data | They risk reopening an already downgraded specificity row without the necessary control. |
| Additional governance artifacts | Current provenance and boundary controls are enough; content work has higher value. |

## Recommended Execution Order

1. Build `scripts/v50_fetch_gwas_catalog_associations.py`.
2. Validate the fetcher against
   `analysis/v50_gwas_catalog_allele_routing/gwas_catalog_rsid_rows_v50.tsv`.
3. Use the allele-harmonization checklist to decide whether a grounded
   non-OpenGWAS direction check is possible without missing required fields.
4. If still working without OpenGWAS and without validation data, prepare the
   GSE255952 import manifest only after the import checklist is explicitly
   satisfied.
5. Keep Gafson/GSE235357 blocked until authorized data packages are available;
   do not substitute literature context for validation.

## Decision

While OpenGWAS is expired, the most valuable executable path is the GWAS Catalog
fetcher and reproducibility validation. The highest-value blocked path remains
the frozen validation harness on Gafson or an alternative paired DMF cohort.
Treatment-response and confounder literature should be used to sharpen
classification and guard design, not to infer validation outcomes.
