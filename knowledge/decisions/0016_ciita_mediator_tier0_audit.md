# Decision 0016: CIITA/Mediator Tier 0 Audit

Date: 2026-05-28

## Decision

`CIITA_SELECTIVE` and `CDK8_CDK19_MEDIATOR` are parked at Tier 0 pending
pharmacologic phenocopy. They remain high-priority mechanisms but do not advance
to Tier 1 yet.

## Evidence

Reproducible audit:

- Script: `scripts/tier0_ciita_mediator_audit.py`
- Output directory: `analysis/tier_0_triage/ciita_mediator_selectivity/`
- Decision file: `analysis/tier_0_triage/ciita_mediator_selectivity/decision.json`
- Evidence table: `analysis/tier_0_triage/ciita_mediator_selectivity/selectivity_evidence.tsv`

Key outputs:

- `benchmark_non_druggable_pass_count`: 1.
- `druggable_or_pharmacologic_phenocopy_pass_count`: 0.
- `local_pharmacologic_cdk8_19_apc_dataset_found`: false.
- `tier0_call`: `PARK_ALIVE_PENDING_PHARMACOLOGIC_PHENOCOPY`.

## Rationale

The strongest selective perturbation remains `Med16_KO`, which is not directly
druggable. `Gsk3b_KO` is partial but pleiotropic. `Cdk8`, `Cdk19`, and `Ccnc`
sgRNA evidence in the local MHC-II screen does not phenocopy `Med16`. Existing
CDK8/CDK19 chemical matter is real, but the local archive lacks an APC-relevant
pharmacologic expression dataset demonstrating MED16-like selectivity.

## Next Action

Search externally for APC/myeloid pharmacologic CDK8/CDK19 perturbation data.
If unavailable, the required next experiment is a wet-lab IFN-gamma-stimulated
human monocyte-derived macrophage or microglia-like assay comparing MED16
CRISPRi, CDK8-selective inhibition, CDK19-selective inhibition, dual CDK8/19
inhibition, inactive analog, and JAK inhibitor control.
