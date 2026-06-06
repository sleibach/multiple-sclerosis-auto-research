# Wave102 SEL1L3 / FXYD5 Perturbation And Model Sidecar

Timestamp: 2026-05-27 21:38 CEST

Role: narrow sidecar scout for direct perturbation evidence, public perturbation-resource hits, and local foundation-model support for `SEL1L3` and `FXYD5` after Wave101 parked both candidates.

## Verdict

Call: `NO_REOPEN_SEL1L3_FXYD5_FROM_PERTURBATION_OR_MODEL_EVIDENCE`.

Neither candidate has enough perturbation or model evidence to reopen as a therapeutic target. `SEL1L3` remains an undercharacterized accessible expression marker with a sparse and non-actionable Geneformer signal. `FXYD5` has real perturbation literature, but it is mostly cancer, epithelial injury, and non-autoimmune inflammation biology; it does not supply a public immune/stromal/autoimmune disease-state rescue signature, a foundation-model perturbation prediction in this repo, or a tractable drug-like target-engagement route.

## Local Evidence Checked

### Wave101 parked-candidate state

Source: `results_v3/wave101_accessible_survivor_forcing_triage/REPORT.md`.

| gene | Wave101 call | relevant missing gates | Wave101 facts |
| --- | --- | --- | --- |
| `SEL1L3` | `PARK_NEEDS_PERTURBATION_AND_GENETIC_ANCHOR` | `perturbation_or_model;genetic_anchor` | score `22.78`; MS delta `0.9225`, p `0.01814`; positive diseases `3`; direct perturbation `0`; foundation support `0`; strong L2G/QTL disease counts `0/0` |
| `FXYD5` | `PARK_NEEDS_PERTURBATION_AND_GENETIC_ANCHOR` | `perturbation_or_model;genetic_anchor;direction_not_conflicted` | score `17.23`; MS delta `0.3525`, p `0.05871`; positive diseases `4`, negative diseases `1`; direct perturbation `0`; foundation support `0`; strong L2G/QTL disease counts `0/0` |

Interpretation: Wave101 did not miss a buried supportive perturbation/model flag. Both were explicitly parked because this evidence class was absent.

### Wave81 perturbation-first rescue

Files checked:

- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_candidate_universe.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave57_rows.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_wave37_rows.tsv`

Exact result: `SEL1L3` and `FXYD5` had `0` rows in all four Wave81 perturbation-first tables. This means neither candidate entered the prior rescue set as a direct perturbation-supported or foundation-model-supported candidate.

### Wave37 GSE212008 CRISPR efferocytosis screen

Source: `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`.

This is the one local direct functional screen where both genes are present. Both are null.

| gene | n sgRNA | median efficient LFC | median noneater LFC | efficient-minus-noneater LFC | efficient FDR | noneater FDR | contrast FDR | call |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `SEL1L3` | 4 | `-0.153901` | `-0.052048` | `-0.101853` | `1.0` | `1.0` | `1.0` | `UNRESOLVED` |
| `FXYD5` | 3 | `-0.210025` | `-0.159337` | `-0.217887` | `1.0` | `0.988974` | `1.0` | `UNRESOLVED` |

Interpretation: neither knockout enhances or impairs macrophage efferocytosis in this screen. This is not a full autoimmune perturbation test, but it is direct functional evidence against using either as an efferocytosis-control node.

### Wave57 Geneformer intervention-first screen

Files checked:

- `results_v3/wave57_intervention_first_geneformer_screen/wave57_geneformer_gene_summary.tsv`
- `results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv`

Exact result: `SEL1L3` and `FXYD5` had `0` rows in both Wave57 files. Neither was nominated by the intervention-first Geneformer pass.

### Other local foundation-model outputs

Files checked included:

- `results_v3/geneformer_broad_residual_delete/geneformer_broad_residual_gene_summary.tsv`
- `results_v3/geneformer_unrestricted_survivor_delete/geneformer_unrestricted_survivor_gene_summary.tsv`
- `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
- `results_v3/wave18_foundation_rescue/geneformer_source_gene_summary.tsv`
- `results_v3/wave79_targetability_shortlist_audit/targetability_foundation_summary.tsv`
- `results_v3/wave94_accessible_state_rerank/candidate_foundation_summary.tsv`
- `results_v3/wave95_cd300_vs_accessible_top_forcing_triage/foundation.tsv`
- `results_v3/state_parse_cd14*`

`SEL1L3` has sparse Geneformer rows, but the prior integration already marked them non-promotable:

- Broad residual delete summary: contexts with token `2`, disease cells with token `4`, mean cosine z vs random `0.339272`, support contexts `1`, strong support contexts `1`.
- Unrestricted survivor delete summary: contexts with token `4`, disease cells with token `11`, mean cosine z vs random `0.477365`, support contexts `0`, strong support contexts `0`.
- Wave18 foundation rescue row: `real_perturbation_alignment_call = model_only_no_real_perturbation_alignment`; `foundation_rescue_recommendation = do_not_promote_from_foundation_model`; Wave18 rank `22`.
- Best context from Wave18: `IBD_epithelial`, best context cells with token `3`, best context cosine z `0.663909`, best context projection-minus-random `0.009901`.

`FXYD5` has no local Geneformer/foundation rows in the searched model outputs. Neither `SEL1L3` nor `FXYD5` appears in local `state_parse_cd14*` outputs, and no local Evo/Stack result file exists for either candidate.

Interpretation: the only model evidence is a weak, sparse `SEL1L3` in-silico deletion signal without real perturbation alignment. It cannot support a target claim.

## Public Perturbation Resource Search

Raw query outputs were saved under:

- `results_v3/wave102_sel1l3_fxyd5_perturbation_model_sidecar/public_perturbation_resource_queries.tsv`
- `results_v3/wave102_sel1l3_fxyd5_perturbation_model_sidecar/targeted_public_perturbation_queries.tsv`
- `results_v3/wave102_sel1l3_fxyd5_perturbation_model_sidecar/perturbseq_queries.tsv`
- `results_v3/wave102_sel1l3_fxyd5_perturbation_model_sidecar/raw_api/`

### GEO / NCBI GDS

Exact results:

| query family | `SEL1L3` | `FXYD5` | `dysadherin` alias |
| --- | ---: | ---: | ---: |
| NCBI GDS all-field perturbation query | `0` | `0` | `0` |
| NCBI GDS immune/stromal/epithelial perturbation query | `0` | `0` | not separately positive |
| NCBI GDS title perturbation query | `0` | `0` | not positive |
| NCBI GDS Perturb-seq/single-cell CRISPR query | `0` | `0` | `0` |

Interpretation: I found no GEO/GDS dataset indexed as a direct `SEL1L3`, `FXYD5`, or dysadherin perturbation dataset.

### LINCS / CMap-adjacent metadata

LINCS Data Portal entity API:

- `SEL1L3`: status `200`, `totalDocuments = 0`.
- `FXYD5`: status `200`, `totalDocuments = 0`.

SigCom LINCS metadata API:

- `SEL1L3`: endpoint returned HTTP `500`.
- `FXYD5`: endpoint returned HTTP `500`.

Interpretation: the accessible LINCS Data Portal metadata did not identify either gene as an indexed entity. SigCom could not be used in this run because the public endpoint returned server errors, so I am not treating it as a negative biological result.

### Perturb-seq / single-cell CRISPR search

Exact results:

| resource | `SEL1L3` | `FXYD5` | `dysadherin` |
| --- | ---: | ---: | ---: |
| PubMed query for Perturb-seq/single-cell CRISPR | `0` | `0` | `0` |
| NCBI GDS query for Perturb-seq/single-cell CRISPR | `0` | `0` | `0` |
| Europe PMC query for Perturb-seq/single-cell CRISPR | `0` | `0` | `1` conference-abstract hit, not a usable public perturbation dataset |

Interpretation: no usable public Perturb-seq evidence was found for either candidate.

### PubMed / Europe PMC perturbation literature

`SEL1L3`:

- PubMed title/abstract perturbation query returned `1` hit: PMID `34993975`, a periodontitis hub-gene bioinformatics paper. This is not a direct `SEL1L3` perturbation experiment.
- PubMed all-field perturbation query returned `3` hits, all compatible with marker/bioinformatics context rather than target perturbation.
- Europe PMC title/abstract perturbation query returned `9` hits; the closest titles are renal cancer/atherosclerosis, senescence/atherosclerosis, cancer biomarker, periodontitis, and other bioinformatic analyses. None is a public immune/stromal autoimmune perturbation-rescue dataset.

`FXYD5`:

- PubMed title/abstract perturbation query returned `23` hits.
- PubMed title/abstract immune/inflammation perturbation query returned `10` hits.
- Closest mechanistic hits include:
  - PMID `40912610`: `Fxyd5` downregulation in ischemia/reperfusion heart inflammation.
  - PMID `35191523`: `Fxyd5` and NF-kB/inflammatory extracellular-matrix degradation in chondrocytes.
  - PMID `28620381`: `FXYD5` as an inflammatory-response mediator in lung injury.
  - PMID `27006401`: `FXYD5` with a pro-inflammatory role in epithelial cells.
  - PMID `36621663`: anti-`FXYD5` monoclonal antibody generation for pancreatic/lung cancer diagnosis.
- Europe PMC title/abstract perturbation query returned `41` `FXYD5` hits and `34` dysadherin-alias hits. Most top hits are cancer, tumor microenvironment, epithelial migration, matrix remodeling, or therapy-resistance contexts.

Interpretation: `FXYD5` has real perturbation biology, but the direction is not enough for this autoimmune target question. The literature supports `FXYD5` as a pleiotropic epithelial/adhesion/injury/cancer regulator, not as a selective autoimmune lipid-lysosomal myeloid-state controller. It also reinforces Wave94/Wave101 safety concerns around epithelial barrier, Na/K-ATPase coupling, adhesion, and oncology-style targeting.

### Druggability / direct drug modulation

ChEMBL target search:

- `SEL1L3`: `0` targets.
- `FXYD5`: `0` targets.

DGIdb API attempts returned the DGIdb web-app shell rather than parseable interaction data, so I do not count that as evidence. Prior local ChEMBL/Wave39/Wave51 searches already found no exact `FXYD5` druggability target and no `SEL1L3` small-molecule route.

Interpretation: I found no small-molecule target entry or drug modulation handle for either gene. `FXYD5` antibody feasibility exists in oncology/diagnostic literature, but the autoimmune-relevant route would have to be non-depleting and barrier-preserving, which is exactly the unproven piece.

## Candidate-Specific Conclusion

### `SEL1L3`

Evidence for reopening:

- Accessible/membrane expression signal in Wave101.
- Sparse Geneformer in-silico deletion signal in one epithelial context.

Evidence against reopening:

- No Wave81 perturbation-first presence.
- Null in GSE212008 efferocytosis CRISPR screen.
- No Wave57 intervention-first Geneformer row.
- No public GEO/GDS perturbation dataset found.
- No PubMed/EuropePMC direct autoimmune perturbation evidence found.
- No LINCS Data Portal entity and no ChEMBL target.
- Prior model integration already concluded `model_only_no_real_perturbation_alignment` and `do_not_promote_from_foundation_model`.

Verdict: `SEL1L3` remains a marker/assay candidate only. It is not promotable as a target from perturbation or model evidence.

### `FXYD5`

Evidence for reopening:

- More interpretable surface biology than `SEL1L3`: FXYD/dysadherin, Na/K-ATPase coupling, epithelial adhesion/injury axis.
- Multiple public perturbation papers exist, including inflammation-adjacent epithelial/chondrocyte/lung/heart contexts.

Evidence against reopening:

- No Wave81 perturbation-first presence.
- Null in GSE212008 efferocytosis CRISPR screen.
- No Wave57 or other local foundation-model support.
- No public GEO/GDS perturbation dataset found.
- No public Perturb-seq/single-cell CRISPR hit found.
- No LINCS Data Portal entity and no ChEMBL target.
- Public perturbation literature is not autoimmune disease-state rescue evidence and does not resolve directionality.
- Existing biology increases, rather than removes, the barrier/safety concern: epithelial barrier, adhesion, Na/K-ATPase regulation, and cancer-associated targeting.

Verdict: `FXYD5` should not be promoted. It remains suitable only for a bounded wet-lab kill test: non-depleting target engagement in disease-relevant epithelial/stromal tissue that reverses inflammatory state while preserving barrier and repair function.

## Final Sidecar Decision

Do not reopen `SEL1L3` or `FXYD5` as Wave102 therapeutic candidates based on perturbation or foundation-model evidence.

Operational implication for the orchestrator: if this branch continues, it should not spend more computation on `SEL1L3`/`FXYD5` unless a genuinely new target-specific perturbation dataset appears. The next productive route is either:

1. use `SEL1L3`/`FXYD5` only as accessible-state markers in a residual compartment assay, or
2. pivot to a successor node with direct perturbation/model/genetic evidence already in hand.
