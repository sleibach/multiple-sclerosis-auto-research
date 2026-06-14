# V37 External Coverage Gap Priority V48

Status: sourcing/navigation only. This table prioritizes external-record hunting for V37 findings that currently lack a V48 relationship row; it does not change any V37 score or grounded finding.

- uncovered V37 findings prioritized: `9`
- high-priority sourcing gaps: `0`
- score formula: `2*relevance + novelty + evidence_weight + rationale_weight + category_weight`

## Priority Counts

| tier | count |
|---|---:|
| `medium` | 9 |

## Prioritized Gaps

| rank | finding | tier | score | relevance | novelty | evidence | rationale | safe source requirement | next action |
|---:|---|---|---:|---:|---:|---|---|---|---|
| 1 | Lysosomal APC bottleneck not proven | `medium` | 13 | 3 | 3 | `provisional` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 2 | Sjogren antigen-presentation but not lysosomal/APC lesion-rim transfer | `medium` | 13 | 2 | 3 | `supported` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 3 | IFN-beta HLA-II/CD74 branch | `medium` | 12 | 3 | 3 | `provisional` | `avoid_false_corroboration` | Do not add broad context; require a concrete predefined dataset/test source before queueing external-verifiable work. | Queue a future external-verifiable task only if a source points to a concrete dataset or predefined test. |
| 4 | Metabolic/sterol setpoint is context/confounder axis, not intervention-grade | `medium` | 12 | 3 | 2 | `provisional` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 5 | Complement/lipid progressive axis downgraded | `medium` | 12 | 2 | 3 | `negative-established` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 6 | Multi-lineage and RPT lenses add prioritization, not evidence | `medium` | 11 | 2 | 3 | `supported` | `method_specific_external_context_absent` | Require a method-specific source about the same procedure or governance issue; broad disease biology is not sufficient. | Add only method-specific external context, not broad biological context. |
| 7 | NAMPT/eNAMPT not reactivated as target | `medium` | 11 | 2 | 2 | `negative-established` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 8 | REL/PUS10/USP34 chr2 closed | `medium` | 11 | 2 | 2 | `negative-established` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |
| 9 | ZFP36L1 chr14 parked | `medium` | 10 | 2 | 2 | `provisional` | `targeted_external_record_needed` | Require a source that addresses the same direction, locus, failure mode, or definition; generic disease context is insufficient. | Only add external context if a source directly discusses the same locus/lead/failure mode and can be classed without changing the grounded result. |

## Interpretation

- High priority means the next external-knowledge pass should look first for specific, source-backed context for that grounded V37 item.
- A priority row is not convergence, contradiction, validation, or biological evidence.
- Generic external context must not be added when the safe source requirement demands a same-definition source.
- Grounded project artifacts remain the evidence for every V37 item.
