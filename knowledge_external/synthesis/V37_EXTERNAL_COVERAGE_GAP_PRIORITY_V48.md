# V37 External Coverage Gap Priority V48

Status: sourcing/navigation only. This table prioritizes external-record hunting for V37 findings that currently lack a V48 relationship row; it does not change any V37 score or grounded finding.

- uncovered V37 findings prioritized: `20`
- high-priority sourcing gaps: `11`
- score formula: `2*relevance + novelty + evidence_weight + rationale_weight + category_weight`

## Priority Counts

| tier | count |
|---|---:|
| `high` | 11 |
| `medium` | 9 |

## Prioritized Gaps

| rank | finding | tier | score | relevance | novelty | evidence | rationale | safe source requirement | next action |
|---:|---|---|---:|---:|---:|---|---|---|---|
| 1 | Mucosal IBD early IFN/APC downshift validates while baseline fallback fails | `high` | 18 | 4 | 3 | `supported` | `no_relevant_external_record_imported` | Require a source directly overlapping the grounded finding before adding a V48 relationship row. | Future V47-style intake can add a sourced external record if it directly overlaps the finding. |
| 2 | UC genetics vs treatment-response layer split | `high` | 17 | 4 | 3 | `supported` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 3 | First-principles druggability discipline changed target interpretation | `high` | 16 | 4 | 4 | `supported` | `method_specific_external_context_absent` | Require a method-specific source about the same procedure or governance issue; broad disease biology is not sufficient. | Add only method-specific external context, not broad biological context. |
| 4 | Locked V7 general cross-disease baseline fallback killed | `high` | 16 | 4 | 3 | `negative-established` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 5 | Tool-robust but simple V22 scalar | `high` | 15 | 4 | 3 | `supported` | `method_specific_external_context_absent` | Require a method-specific source about the same procedure or governance issue; broad disease biology is not sufficient. | Add only method-specific external context, not broad biological context. |
| 6 | Crohn downstream IFN/APC convergence exceeds genetic proximity | `high` | 15 | 3 | 3 | `supported` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 7 | RA pregnancy comparator but blood APC treatment-response nontransfer | `high` | 15 | 3 | 3 | `supported` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 8 | EBV/IFN APC imprint downgraded by specificity control | `high` | 14 | 3 | 3 | `negative-established` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 9 | GPR25 demoted from protected favorite | `high` | 14 | 3 | 3 | `negative-established` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 10 | MHC overlap is distinct-signal, not simple shared biology | `high` | 14 | 3 | 2 | `negative-established` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 11 | No load-bearing invariant found in V26 | `high` | 14 | 2 | 4 | `negative-established` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 12 | Lysosomal APC bottleneck not proven | `medium` | 13 | 3 | 3 | `provisional` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 13 | Sjogren antigen-presentation but not lysosomal/APC lesion-rim transfer | `medium` | 13 | 2 | 3 | `supported` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 14 | IFN-beta HLA-II/CD74 branch | `medium` | 12 | 3 | 3 | `provisional` | `avoid_false_corroboration` | Do not add broad context; require a concrete predefined dataset/test source before queueing external-verifiable work. | Queue a future external-verifiable task only if a source points to a concrete dataset or predefined test. |
| 15 | Metabolic/sterol setpoint is context/confounder axis, not intervention-grade | `medium` | 12 | 3 | 2 | `provisional` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 16 | Complement/lipid progressive axis downgraded | `medium` | 12 | 2 | 3 | `negative-established` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 17 | Multi-lineage and RPT lenses add prioritization, not evidence | `medium` | 11 | 2 | 3 | `supported` | `method_specific_external_context_absent` | Require a method-specific source about the same procedure or governance issue; broad disease biology is not sufficient. | Add only method-specific external context, not broad biological context. |
| 18 | NAMPT/eNAMPT not reactivated as target | `medium` | 11 | 2 | 2 | `negative-established` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 19 | REL/PUS10/USP34 chr2 closed | `medium` | 11 | 2 | 2 | `negative-established` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 20 | ZFP36L1 chr14 parked | `medium` | 10 | 2 | 2 | `provisional` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |

## Interpretation

- High priority means the next external-knowledge pass should look first for specific, source-backed context for that grounded V37 item.
- A priority row is not convergence, contradiction, validation, or biological evidence.
- Generic external context must not be added when the safe source requirement demands a same-definition source.
- Grounded project artifacts remain the evidence for every V37 item.
