# V48 Contradiction Surveillance Checklist

Status: future intake/navigation only. This checklist defines how future candidate tensions are triaged; it does not assert current contradictions.

- checklist rows: `16`
- current matrix surveillance rows: `7`
- future sourcing surveillance rows: `9`
- current contradiction rows: `0`

## Checklist

| scope | source class | finding category | rows | current contradiction rows | surveillance trigger | safe action |
|---|---|---|---:|---:|---|---|
| `current_matrix` | external_claim | `decoupling_negative` | 1 | 0 | Candidate says a project decoupling/negative relationship is actually shared, same-direction, or transferable under the same definition. | Add or update a contradiction-intake row only if the candidate has source-specific overlap; queue future grounding before any interpretation change. |
| `current_matrix` | external_resource_catalog | `decoupling_negative` | 2 | 0 | Candidate says a project decoupling/negative relationship is actually shared, same-direction, or transferable under the same definition. | Add or update a contradiction-intake row only if the candidate has source-specific overlap; queue future grounding before any interpretation change. |
| `current_matrix` | external_claim | `kills_closed` | 1 | 0 | Candidate says a killed or closed lead succeeds under the same rule, direction, or validation domain. | Add or update a contradiction-intake row only if the candidate has source-specific overlap; queue future grounding before any interpretation change. |
| `current_matrix` | external_resource_catalog | `kills_closed` | 1 | 0 | Candidate says a killed or closed lead succeeds under the same rule, direction, or validation domain. | Add or update a contradiction-intake row only if the candidate has source-specific overlap; queue future grounding before any interpretation change. |
| `current_matrix` | external_claim | `methodological` | 1 | 0 | Candidate challenges a project method result or governance rule under the same procedure. | Add or update a contradiction-intake row only if the candidate has source-specific overlap; queue future grounding before any interpretation change. |
| `current_matrix` | external_claim | `positive_supported` | 5 | 0 | Candidate says the grounded positive does not hold under the same definition, population, layer, or direction. | Add or update a contradiction-intake row only if the candidate has source-specific overlap; queue future grounding before any interpretation change. |
| `current_matrix` | external_resource_catalog | `positive_supported` | 1 | 0 | Candidate says the grounded positive does not hold under the same definition, population, layer, or direction. | Add or update a contradiction-intake row only if the candidate has source-specific overlap; queue future grounding before any interpretation change. |
| `future_sourcing_plan` | IBD/MS transfer-specific literature or datasets | `decoupling_negative` | 2 | 0 | Candidate says a project decoupling/negative relationship is actually shared, same-direction, or transferable under the same definition. | If a source is found, ingest it through V47 segregation first, then classify overlap before creating any contradiction row. |
| `future_sourcing_plan` | locus/signal-specific genetics source | `decoupling_negative` | 1 | 0 | Candidate says a project decoupling/negative relationship is actually shared, same-direction, or transferable under the same definition. | If a source is found, ingest it through V47 segregation first, then classify overlap before creating any contradiction row. |
| `future_sourcing_plan` | pregnancy/postpartum comparator literature or datasets | `decoupling_negative` | 1 | 0 | Candidate says a project decoupling/negative relationship is actually shared, same-direction, or transferable under the same definition. | If a source is found, ingest it through V47 segregation first, then classify overlap before creating any contradiction row. |
| `future_sourcing_plan` | same-failure-mode source | `decoupling_negative` | 1 | 0 | Candidate says a project decoupling/negative relationship is actually shared, same-direction, or transferable under the same definition. | If a source is found, ingest it through V47 segregation first, then classify overlap before creating any contradiction row. |
| `future_sourcing_plan` | EBV-stratified immune-data source | `kills_closed` | 1 | 0 | Candidate says a killed or closed lead succeeds under the same rule, direction, or validation domain. | If a source is found, ingest it through V47 segregation first, then classify overlap before creating any contradiction row. |
| `future_sourcing_plan` | locus/signal-specific genetics source | `kills_closed` | 1 | 0 | Candidate says a killed or closed lead succeeds under the same rule, direction, or validation domain. | If a source is found, ingest it through V47 segregation first, then classify overlap before creating any contradiction row. |
| `future_sourcing_plan` | same-failure-mode source | `kills_closed` | 1 | 0 | Candidate says a killed or closed lead succeeds under the same rule, direction, or validation domain. | If a source is found, ingest it through V47 segregation first, then classify overlap before creating any contradiction row. |
| `future_sourcing_plan` | method/governance literature | `methodological` | 2 | 0 | Candidate challenges a project method result or governance rule under the same procedure. | If a source is found, ingest it through V47 segregation first, then classify overlap before creating any contradiction row. |
| `future_sourcing_plan` | IBD/MS transfer-specific literature or datasets | `positive_supported` | 1 | 0 | Candidate says the grounded positive does not hold under the same definition, population, layer, or direction. | If a source is found, ingest it through V47 segregation first, then classify overlap before creating any contradiction row. |

## Interpretation Boundary

- The current V48 matrix still has zero contradiction rows.
- A future tension is a routing event: intake, overlap check, future grounding queue; it is not an override of a grounded finding.
- This checklist prevents ad hoc interpretation if a future source appears to disagree with the project.
