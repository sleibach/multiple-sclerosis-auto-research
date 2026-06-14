# V49 Uncovered Finding Triage

Status: source-intake planning only. This document does not add external records, assert convergence, or change any grounded finding.

Boundary: remaining uncovered findings should not be padded with broad context. A future source is useful only when it addresses the exact failure mode, direction, data type, or method-governance question named here.

## Summary

- uncovered findings triaged: `9`
- dataset/test-only or direct-source rows: `4`
- low-priority/optional rows: `5`

## Triage Table

| finding | priority | intake decision | safe source type | avoid | rationale |
|---|---|---|---|---|---|
| IFN-beta HLA-II/CD74 branch | `medium` | `dataset_or_predefined_test_only` | paired IFN-beta response transcriptomic dataset or predefined validation protocol | broad IFN-beta mechanism reviews or therapy labels | The project finding is provisional and therapy-specific; context could easily overstate it unless it points to a concrete validation route. |
| Sjogren antigen-presentation but not lysosomal/APC lesion-rim transfer | `low` | `narrow_direct_source_only` | source directly comparing Sjogren antigen presentation with lysosomal/APC lesion-rim biology | generic Sjogren antigen-presentation literature | Generic antigen-presentation context would not address the project's negative transfer boundary. |
| NAMPT/eNAMPT not reactivated as target | `low` | `do_not_expand_without_direction_matched_target_evidence` | MS-specific NAMPT/eNAMPT direction, safety, and intervention evidence that matches the project failure mode | general NAMPT immunometabolism or cancer-metabolism sources | The project already demoted NAMPT to marker/covariate; broad target enthusiasm would be a false-corrobation risk. |
| ZFP36L1 chr14 parked | `medium` | `source_specific_genetics_only` | fine-mapping, QTL, or colocalization source resolving chr14 ZFP36L1 direction and robustness | gene-function or immune-regulation context without locus direction | The parked status is about weak coloc/QTL direction, so only signal-level sources are useful. |
| REL/PUS10/USP34 chr2 closed | `low` | `source_specific_genetics_only` | disease SuSiE-coloc or equivalent signal-specific summary resolving the chr2 closure reason | general NF-kB/REL biology or pathway context | The closure reason is absence of disease SuSiE-coloc support, not lack of pathway plausibility. |
| Complement/lipid progressive axis downgraded | `medium` | `direct_progressive_lesion_dataset_preferred` | progressive MS or chronic-active lesion dataset/source with complement and lipid-axis measurements | broad complement or lipid reviews without progressive/lesion specificity | This is one of the remaining biological hypotheses where a direct progressive-lesion source could be decision-useful. |
| Lysosomal APC bottleneck not proven | `medium` | `direct_apc_perturbation_or_flux_source_only` | APC cathepsin/V-ATPase/lysosomal-flux perturbation data or source tied to MS-relevant antigen processing | generic lysosome or antigen-processing pathway context | The project observed coupling but not a bottleneck; only perturbation/flux evidence can address the missing causal step. |
| Metabolic/sterol setpoint is context/confounder axis, not intervention-grade | `low` | `covariate_context_only` | sources that specify metabolic/sterol signatures as covariates or confounders in MS immune profiling | therapeutic repurposing claims based only on metabolic pathway overlap | The project treats this as context/confounding, not an intervention-grade target; external intake should preserve that boundary. |
| Multi-lineage and RPT lenses add prioritization, not evidence | `low` | `method_governance_source_optional` | method literature on model-assisted review, provenance, or human/AI evidence boundaries | vendor/model capability claims | The project governance is already explicit; additional method context is optional and must not inflate model output into evidence. |

## Operational Rule

- Intake is warranted only for sources matching the row's safe source type.
- Broad biological plausibility should stay out of the convergence matrix for these findings.
- Any accepted future source still enters as segregated context and requires a later grounded test before it can affect project conclusions.
