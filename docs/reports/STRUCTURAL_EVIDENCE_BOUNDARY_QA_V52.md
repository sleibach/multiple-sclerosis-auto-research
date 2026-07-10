# Structural Evidence Boundary QA V52

Date: 2026-07-10

Status: wording and evidence-boundary audit. This document adds no biological
evidence and does not alter any target verdict. It checks that V52 structural
language keeps AlphaFold DB predictions as confidence-qualified context rather
than project-grounded therapeutic evidence.

## Scope

Audited V52 therapeutic and genetics-facing documents:

- `docs/reports/THERAPEUTIC_PATH_V52.md`
- `docs/reports/THERAPEUTIC_PATH_SUMMARY_CARD_V52.md`
- `docs/reports/THERAPEUTIC_TARGET_EVIDENCE_MATRIX_V52.tsv`
- `docs/validation/MEDICAL_TEAM_THERAPEUTIC_DATA_REQUEST_V52.md`
- `docs/workups/genetics/STRUCTURE_AWARE_NO_GO_TABLE_V52.md`
- `docs/workups/genetics/GPR25_DIRECTION_MATCHED_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/KIF21B_RESTORATION_MODALITY_SPEC_V52.md`
- `docs/workups/genetics/PTGER4_SIGNAL_SPECIFIC_REOPEN_SPEC_V52.md`

## Search Terms Used

The audit searched for structural-promotion risk terms:

- `AlphaFold`
- `predicted structure`
- `structural prediction`
- `structure.*evidence`
- `evidence.*structure`
- `intervention-grade`
- `druggability`
- `tractability`
- `project-grounded evidence`
- `target evidence`
- `structure confirms`
- `ligandability`

## Findings

| finding | result | action |
|---|---|---|
| Direct predicted-structure-as-evidence claims | No unacceptable claim found. Documents repeatedly state predicted structures are context only and not project-grounded evidence. | No verdict change. |
| Structure as target rescue | No target rescue language found. GPR25, KIF21B, PTGER4, and ZMIZ1 all remain no-go or conditional under direction/modality gates. | No verdict change. |
| Over-strong wording | Two uses of "confirms" around AlphaFold context could be misread as stronger than prediction context. | Reworded to "supports" / "is consistent with" prediction-context language. |
| Missing warning in request packet | Present. The request packet explicitly says the project will not treat AlphaFold predicted structure as target evidence. | No change needed. |
| Machine-readable matrix boundary | Present. Matrix includes "prediction context only" and closed/no-promote verdicts. | No change needed. |

## Tightened Wording

The audit changed V52 language from:

- "structure confirms" for GPR25 receptor-core context;
- "AlphaFold confirms receptor-core structural context" for PTGER4.

to:

- "structural prediction context supports";
- "AlphaFold supports receptor-core structural context".

This keeps the same scientific meaning while avoiding any implication that a
predicted structure is experimental proof or disease evidence.

## Verdict

V52 structural language passes the evidence-boundary QA after the wording
tightening. AlphaFold DB records are used only to sharpen feasibility context.
They do not:

1. validate MS disease relevance;
2. resolve causal gene;
3. resolve protective direction;
4. create a direction-matched modality;
5. reopen a closed lead as a finding.

The V52 therapeutic-path headline is unchanged: near-term impact is monitoring /
stratification validation; no intervention-grade target is currently supported.
