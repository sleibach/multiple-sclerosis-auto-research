# V48 Convergence / Contradiction Analysis

Status: class-aware synthesis. This document compares project-grounded findings to segregated external records.

Boundary rule: each external row is marked with its epistemic class, source, and explicit not-grounded marker. External agreement is corroboration context only; project artifacts remain the evidence. External disagreement would flag a future-grounding task, not override the grounded result.

## Summary

- relationship rows: `12`
- convergences asserted: `2`
- contradictions flagged: `0`
- insufficient-overlap/context rows: `10`
- missing-input rows: `0`

## Decision-Relevant Convergences

- Grounded: `MS-UC is strongest tested genome-wide genetics comparator` (robust; source artifact: `docs/history/LEAD_SLATE_V21.md`). External: `claim.nature.ms_uc_greater_genetic_correlation_context.2026-06-14` (external-unverifiable; source: https://www.nature.com/articles/s41467-021-25768-0; marker: `NOT_PROJECT_GROUNDED`). Status: `CORROBORATION_FROM_INDEPENDENT_SOURCE`. The external literature claim independently reports stronger MS-UC than MS-CD genetic correlation. This aligns with the project's rerunnable MS-UC genetics backdrop; the project artifact remains the evidence.
- Grounded: `Layer-specific autoimmune transfer-validity map` (supported; source artifact: `docs/findings/AXIS_DISAGREEMENT_FINDINGS_V12.md`). External: `claim.ms_ibd.treatment_transfer_caution_context.2026-06-14` (external-unverifiable; source: https://www.nature.com/articles/s41467-021-25768-0; marker: `NOT_PROJECT_GROUNDED`). Status: `CORROBORATION_FROM_INDEPENDENT_SOURCE`. The external literature context warns that treatment effects do not transfer naively between MS and IBD. This aligns with the project's axis-specific transfer-validity map; the project artifact remains the evidence.

## Contradictions Flagged

- None in this pass. No external record currently overrides or directly contradicts a grounded finding.

## Relationship Matrix

| grounded finding | external record | class | source | relationship | status | interpretation |
|---|---|---|---|---|---|---|
| MS-UC is strongest tested genome-wide genetics comparator | `claim.nature.ms_uc_greater_genetic_correlation_context.2026-06-14` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://www.nature.com/articles/s41467-021-25768-0 | `converges` | `CORROBORATION_FROM_INDEPENDENT_SOURCE` | The external literature claim independently reports stronger MS-UC than MS-CD genetic correlation. This aligns with the project's rerunnable MS-UC genetics backdrop; the project artifact remains the evidence. |
| Layer-specific autoimmune transfer-validity map | `claim.ms_ibd.treatment_transfer_caution_context.2026-06-14` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://www.nature.com/articles/s41467-021-25768-0 | `converges` | `CORROBORATION_FROM_INDEPENDENT_SOURCE` | The external literature context warns that treatment effects do not transfer naively between MS and IBD. This aligns with the project's axis-specific transfer-validity map; the project artifact remains the evidence. |
| Bounded APC/HLA-II early treatment-response monitoring scalar | `claim.dailymed.dimethyl_fumarate_mechanism_context.2026-06-13` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=6c42107a-2a42-4263-97b6-ae0d7675c92a | `insufficient-overlap` | `NO_DIRECT_EXTERNAL_CORROBORATION` | The DMF label provides treatment-context and mechanism-uncertainty context, but it does not independently assert an APC/HLA-II early-response monitoring rule. |
| V22 scalar is immune-tone bounded, not steroid/composition artifact | `claim.dailymed.dimethyl_fumarate_mechanism_context.2026-06-13` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=6c42107a-2a42-4263-97b6-ae0d7675c92a | `insufficient-overlap` | `NO_DIRECT_EXTERNAL_CORROBORATION` | The label context does not test glucocorticoid, composition, metabolic, or STAT1 confounding of the project score. |
| Coupled APC remodeling architecture | `resource.msgd.database_commons.2026-06-13` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://ngdc.cncb.ac.cn/databasecommons/database/id/9285 | `insufficient-overlap` | `NO_DIRECT_EXTERNAL_CORROBORATION` | A curated MS gene database can provide gene-level context, but the current resource metadata does not independently assert the project's coupled HLA/IFN-APC and MIF-CD74 architecture. |
| T/B-readable early IFN/APC/STAT1 monitoring state | `claim.dailymed.ocrelizumab_mechanism_context.2026-06-13` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=9da42362-3bb5-4b83-b4bb-b59fd4e55f0d | `insufficient-overlap` | `NO_DIRECT_EXTERNAL_CORROBORATION` | The ocrelizumab label contextualizes CD20-directed therapy, but it does not corroborate the project's early IFN/APC/STAT1 monitoring-state readout. |
| Postpartum HLA-II/CD64 APC-arm imbalance | `claim.national_ms_society.rrms_course_context.2026-06-13` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://www.nationalmssociety.org/understanding-ms/what-is-ms/types-of-ms | `insufficient-overlap` | `NO_DIRECT_EXTERNAL_CORROBORATION` | The disease-course context is relevant to relapse/remission terminology, but it does not address postpartum APC-arm trajectories. |
| ZMIZ1 opposite-direction MS/Crohn decoupling | `resource.disgenet.platform.2026-06-13` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://disgenet.com/ | `insufficient-overlap` | `RESOURCE_CAN_QUEUE_FUTURE_CHECK` | The resource may contain disease-gene assertions, but the current resource metadata record does not contain a ZMIZ1 directionality claim. |
| chr1 KIF21B/GPR25 locus resolves to real biology but hard target | `resource.gwas_catalog.ms.2026-06-13` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://www.ebi.ac.uk/gwas/ | `insufficient-overlap` | `RESOURCE_CAN_QUEUE_FUTURE_CHECK` | The resource metadata confirms a public association catalog exists, but it does not itself confirm the project's chr1 causal-gene/direction assessment. |
| PTGER4 mixed shared/distinct signal closes naive transfer | `claim.ms_ibd.treatment_transfer_caution_context.2026-06-14` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://www.nature.com/articles/s41467-021-25768-0 | `insufficient-overlap` | `GENERAL_CONTEXT_NOT_LOCUS_CORROBORATION` | The treatment-transfer caution supports the general need for mechanism-specific transfer, but it does not speak to PTGER4 fine-mapping or signal conflict. |
| No validated broad immune-state simulator from held data | `resource.msgd.database_commons.2026-06-13` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://ngdc.cncb.ac.cn/databasecommons/database/id/9285 | `insufficient-overlap` | `NO_DIRECT_EXTERNAL_CORROBORATION` | A curated MS gene database is a useful external resource, but it does not validate the project's held-out simulator negative or supply perturbation validation. |
| Coupled-axis successor rule does not beat scalar | `claim.dailymed.dimethyl_fumarate_mechanism_context.2026-06-13` | `external-unverifiable` / `NOT_PROJECT_GROUNDED` | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=6c42107a-2a42-4263-97b6-ae0d7675c92a | `insufficient-overlap` | `NO_DIRECT_EXTERNAL_CORROBORATION` | The DMF label offers treatment context but does not evaluate whether a coupled-axis response rule improves over the locked scalar. |

## Follow-Up Queue

- `MS-UC is strongest tested genome-wide genetics comparator` x `claim.nature.ms_uc_greater_genetic_correlation_context.2026-06-14`: No action needed for current interpretation; future refresh should hash and rerun the external summary-statistic inputs if imported.
- `Layer-specific autoimmune transfer-validity map` x `claim.ms_ibd.treatment_transfer_caution_context.2026-06-14`: If pursued clinically, ground specific treatment-transfer claims in predefined patient-level or pharmacovigilance data.
- `Bounded APC/HLA-II early treatment-response monitoring scalar` x `claim.dailymed.dimethyl_fumarate_mechanism_context.2026-06-13`: Validate with the frozen V42/V44 harness on a paired labeled DMF cohort; do not use label context as validation.
- `V22 scalar is immune-tone bounded, not steroid/composition artifact` x `claim.dailymed.dimethyl_fumarate_mechanism_context.2026-06-13`: Use the V42/V44 confounder and batch diagnostics when real validation data arrive.
- `Coupled APC remodeling architecture` x `resource.msgd.database_commons.2026-06-13`: Import specific CD74, MIF, HLA, and APC-axis external records only as segregated future-grounding context before comparing them to V26.
- `T/B-readable early IFN/APC/STAT1 monitoring state` x `claim.dailymed.ocrelizumab_mechanism_context.2026-06-13`: Ground only in paired response data with compartment-resolved or deconvolved readouts.
- `Postpartum HLA-II/CD64 APC-arm imbalance` x `claim.national_ms_society.rrms_course_context.2026-06-13`: Acquire true postpartum MS immune trajectory data with relapse-window timing.
- `ZMIZ1 opposite-direction MS/Crohn decoupling` x `resource.disgenet.platform.2026-06-13`: Create a future-grounding task only after importing specific ZMIZ1 records with source snapshots and hashes.
- `chr1 KIF21B/GPR25 locus resolves to real biology but hard target` x `resource.gwas_catalog.ms.2026-06-13`: Import specific GWAS Catalog associations only as future-grounding records before comparison.
- `PTGER4 mixed shared/distinct signal closes naive transfer` x `claim.ms_ibd.treatment_transfer_caution_context.2026-06-14`: Leave PTGER4 closed unless signal-specific external data are imported and grounded.
- `No validated broad immune-state simulator from held data` x `resource.msgd.database_commons.2026-06-13`: Do not reopen simulator claims without a held-out perturbation dataset and frozen split.
- `Coupled-axis successor rule does not beat scalar` x `claim.dailymed.dimethyl_fumarate_mechanism_context.2026-06-13`: Keep V27 negative-established unless a future external cohort is tested with the frozen scalar and any pre-locked successor under a preregistered comparison.
