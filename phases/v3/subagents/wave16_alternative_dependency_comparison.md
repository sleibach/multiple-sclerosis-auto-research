# Wave16-C Alternative Dependency Comparison

Returned: 2026-05-27

Role: alternatives worker for the V3 autonomous autoimmune research session.
Scope is limited to alternative dependency comparison. This is not a final V3
finding.

## Question

Compare Wave15 survivor/near-survivor candidates `LAPTM5`, `LGALS9`, `CTSS`,
`ITGAM`, and stronger overlooked HLA-II/lysosomal dependency nodes against the
current `CTSH` scout for:

- cross-autoimmune breadth
- novelty / prior-art blocking
- druggability and feasibility
- genetics / prior-art support
- pivot versus continue recommendation

## Inputs Used

Local:

- `results_v3/wave15_surface_trafficking_dependency/candidate_ranked.tsv`
- `results_v3/wave15_orchestrator_dependency_scan/candidate_dependency_priority_summary.tsv`
- `results_v3/wave15_geneformer_loader_dependency_delete/wave15_geneformer_loader_dependency_gene_summary.tsv`
- `subagents_v3/wave15_surface_trafficking_dependency.md`
- `subagents_v3/wave15_prior_art_feasibility.md`
- `subagents_v3/wave15_perturbation_drug_response.md`
- `results_v3/wave14_target_level_genetics/*`

Targeted external checks:

- Europe PMC query counts for candidate + autoimmune terms.
- ClinicalTrials.gov v2 API for cathepsin-S, galectin-9, CD11b, cathepsin-H,
  LAPTM5, and HLA-DM autoimmune terms.
- Open Targets GraphQL search for target identifiers. Association query timed
  out during this run, so I did not use live Open Targets association scores
  beyond the local Wave14 output and target ID resolution.
- PubMed/PMC/ClinicalTrials pages for CTSS and ITGAM prior art.
- NCBI Gene pages for CTSH and LAPTM5 function / gene context.

## Executive Read

No alternative cleanly beats `CTSH` as a cross-autoimmune dependency scout.

`CTSH` is still the best continue candidate because it has the strongest
combined local breadth among actionable nodes and less direct autoimmune
clinical blocking than `CTSS`. The weakness is unchanged: `CTSH` is not yet a
genetics-backed or chemistry-backed target, and its enzyme biology is
lysosomal/housekeeping enough that feasibility remains unproven.

Best alternative if forced to pivot for novelty: `LAPTM5`, but only as a
biology/biomarker scout. It is cleaner from a prior-art standpoint than
`CTSS`/`LGALS9`, but its modality is poor.

Best alternative if forced to pivot for tractable enzyme pharmacology: `CTSS`,
but it is novelty-blocked by direct autoimmune clinical trials and should remain
an assay comparator.

Best overlooked biology: `HLA-DMA/HLA-DMB` and core HLA-II chains. They are
stronger state markers than `CTSH`, but fail the intervention-target test.

## Local Breadth Comparison

| candidate | Wave15 surface call | surface breadth | orchestrator rank | orchestrator support | Geneformer loader deletion |
|---|---:|---|---:|---|---|
| `CTSH` | rank 1 GO_SCOUT | delta trend 5 diseases; residual state coupling 8 diseases | 5 | priority 13.5; expression 3; residual 4 | weak-positive; 3 support contexts, no strong contexts |
| `CTSS` | rank 2 GO_SCOUT | delta trend 4; residual 6 | 10 | priority 12.0; expression 4; residual 2 | weak-negative overall; projection shift -0.0079 |
| `LGALS9` | rank 3 GO_SCOUT | delta trend 4; residual 7 | 27 | priority 7.5; expression 3; residual 2 | near-null; projection shift 0.00065 |
| `LAPTM5` | rank 4 GO_SCOUT | delta trend 3; residual 6 | 14 | priority 10.0; expression 3; residual 4 | weak-positive; projection shift 0.0039 |
| `ITGAM` | WATCHLIST | delta trend 2; residual 6; confounder-dominant 4 | 71 | priority 3.25; residual 2; negative MS | not in loader panel |
| `HLA-DMA` | local NO_GO | delta trend 6; residual 7 | 8 | priority 12.5; expression 4; residual 4 | weak-negative; no support contexts |
| `HLA-DMB` | local NO_GO | delta trend 5; residual 7 | 13 | priority 11.0; expression 4; residual 3 | isolated weak signal; 1 support context |

Interpretation:

- The surface screen is generous to `LGALS9`, `CTSS`, and `LAPTM5`.
- The orchestrator is harsher and preserves `CTSH` over the named alternatives.
- HLA-DM/HLA-II genes are stronger state labels, not better intervention nodes.
- Geneformer does not rescue any alternative. Its strongest-looking lysosomal
  signals (`CTSB`, `LAMP3`, `IFI30`) are too context-limited and do not overcome
  weaker local/orchestrator evidence.

## Candidate Notes

### Reference: `CTSH`

Local upside:

- Best actionable local dependency rank in Wave15 surface screen.
- Residual HLA/CD74-state coupling spans 8 diseases in the surface screen.
- Orchestrator keeps `CTSH` above `CTSS`, `LAPTM5`, `LGALS9`, and `ITGAM`.

External / feasibility:

- NCBI Gene describes CTSH as a lysosomal cysteine proteinase with aminopeptidase
  and endopeptidase activity, broadly expressed across tissues.
- NCBI also links CTSH-region GWAS/GeneRIF evidence to type 1 diabetes-related
  work, but this is not a broad cross-autoimmune target-level genetic anchor.
- Compared with `CTSS`, I did not find direct CTSH autoimmune clinical trial
  blocking in targeted checks.

Liability:

- Less clinically de-risked than `CTSS`.
- Need CTSH-selective tool compounds or genetics/perturbation confirmation
  before any target claim.

### `LAPTM5`

Why it is the best novelty-first alternative:

- Local GO_SCOUT in Wave15 surface screen.
- Orchestrator keeps it in the upper middle of the dependency list.
- ClinicalTrials.gov LAPTM5-autoimmune query returned no interventional study
  in the targeted check.
- NCBI Gene confirms `LAPTM5` as lysosomal protein transmembrane 5; recent
  literature reviews frame it as an immune/lysosomal regulator, but that is not
  yet a mature therapeutic lane.

Why it does not beat `CTSH`:

- Less local breadth than `CTSH`.
- No convincing genetics anchor in the local genetics audit.
- Multi-pass lysosomal membrane protein: no obvious selective small-molecule or
  biologic modality for chronic autoimmune use.

Worker call: keep as contingency and mechanistic readout; do not pivot now.

### `LGALS9`

Why it remains interesting:

- Strong surface-screen breadth: residual state coupling in 7 diseases.
- Extracellular/secreted checkpoint biology makes it more accessible than
  intracellular lysosomal proteins.

Why it is not a clean alternative:

- Orchestrator demotes it sharply: only 2 residual-support diseases.
- Geneformer is near-null.
- Europe PMC query for `LGALS9`/galectin-9 + autoimmune returned a very large
  literature footprint, and ClinicalTrials.gov returned autoimmune Gal-9
  observational biomarker records.
- Wave15 prior-art audit already flagged broad Gal-9/TIM-3 autoimmune prior art
  and direction complexity.

Worker call: use as PD/stratification marker or biology comparator, not as a
novel cross-autoimmune dependency pivot.

### `CTSS`

Why it is the closest enzyme comparator:

- Surface screen rank 2 GO_SCOUT behind `CTSH`.
- Enzyme class is tractable; inhibitors exist.
- Mechanistically fits MHC-II invariant-chain processing.

Why it is blocked:

- Direct autoimmune clinical prior art is heavy:
  - `NCT00425321`: Phase IIa RWJ-445380 cathepsin-S inhibitor in active RA.
  - `NCT02701985`: RO5459072 / petesicatib in primary Sjogren.
  - `NCT02679014`: RO5459072 in celiac disease.
- PubMed celiac trial report states RO5459072 did not show clear effect on
  gluten-challenge response, making the clinical precedent not just crowded but
  directionally discouraging.
- Orchestrator support is weaker than the surface screen: only 2 residual-state
  support diseases.

Worker call: assay comparator / positive-control biology only. No novelty pivot.

### `ITGAM`

Why it deserves mention:

- Strong human genetics for SLE. The rs1143679/R77H CD11b variant is a
  repeatedly studied functional SLE risk allele; the PMC functional paper
  reports impaired CR3 phagocytosis/adhesion and altered inflammatory regulation
  in human monocytes.
- Surface targetability is better than for intracellular lysosomal nodes.

Why it fails this task:

- Local cross-autoimmune HLA/lysosomal dependency evidence is weak.
- Orchestrator ranks it near the bottom with negative MS evidence.
- Genetics are SLE-heavy rather than broad across the V3 tissue-state panel.
- Integrin/complement modulation is crowded and carries myeloid adhesion and
  phagocytosis risk.

Worker call: SLE-specific comparator, not a CTSH replacement.

### Overlooked HLA-II / Lysosomal Nodes

`HLA-DMA/HLA-DMB`:

- Strong local HLA-II state coupling.
- `HLA-DMA` has the highest surface-screen rank score if pure state biology is
  counted.
- Still NO_GO locally because peptide-loading chaperones are intracellular,
  broad antigen-presentation machinery with poor direct targetability.
- Use for patient/state stratification and peptidome assays, not intervention.

Core HLA-II chains (`HLA-DRA`, `HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`):

- Orchestrator ranks several above or near `CTSH` as state markers.
- Not useful as conventional drug targets because they are antigen-presentation
  identity molecules with HLA-region genetics and broad immune safety risk.

`CTSB`, `CTSL`, `LAMP3`, `IFI30`:

- Geneformer shows isolated support for `CTSB`, `LAMP3`, or `IFI30`, but local
  expression/state evidence is weaker and/or confounder-heavy.
- `IFI30` remains a useful antigen-processing/GILT readout but has poor
  modality and ambiguous direction.
- `CTSB/CTSL` have broader lysosomal housekeeping and selectivity liabilities.

Worker call: no overlooked lysosomal node currently outranks `CTSH` as an
alternative dependency target.

## Ranked Alternatives Against `CTSH`

| rank | alternative | overall call | reason |
|---:|---|---|---|
| 1 | `LAPTM5` | best contingency, not pivot | Cleanest novelty profile, local recurrence, but poor modality and weaker breadth. |
| 2 | `LGALS9` | accessible but crowded | Surface/secreted biology and Wave15 breadth, but prior art and orchestrator demotion are major problems. |
| 3 | `CTSS` | comparator only | Strong enzyme tractability and local signal, but direct autoimmune trial prior art blocks novelty. |
| 4 | `HLA-DMA/HLA-DMB` | state readout only | Stronger biology than many candidates, but targetability and safety are poor. |
| 5 | `ITGAM` | SLE-specific comparator | Strong SLE genetics, weak cross-autoimmune state fit. |
| 6 | `CTSB/CTSL/LAMP3/IFI30` | controls/readouts | Isolated or confounded signals; no better overall than `CTSH`. |

## Pivot / Continue Recommendation

Continue with `CTSH` as the lead scout/reference, but keep the language modest:
`CTSH` is a locally nominated dependency candidate, not a validated therapeutic
target.

Do not pivot to `CTSS`, `LGALS9`, `ITGAM`, or HLA-DM/HLA-II nodes for the main
cross-autoimmune dependency story.

Practical next-use split:

- `CTSH`: primary scout to test with selective tools, CRISPR perturbation, and
  peptidome/HLA-II processing readouts.
- `CTSS`: positive-control cathepsin/MHC-II processing comparator.
- `HLA-DMA/HLA-DMB`: HLA-II peptide-loading state markers and assay controls.
- `LAPTM5`: novelty-first backup if CTSH fails chemistry or prior-art review.
- `LGALS9`: extracellular checkpoint/PD marker, not target.
- `ITGAM`: SLE genetics comparator, not cross-autoimmune dependency node.

## Source Links

Output files created:

- `results_v3/wave16_alternative_dependency_comparison/ranked_alternative_summary.tsv`
- `results_v3/wave16_alternative_dependency_comparison/targeted_api_check_log.tsv`

Local artifacts:

- `subagents_v3/wave15_surface_trafficking_dependency.md`
- `subagents_v3/wave15_prior_art_feasibility.md`
- `subagents_v3/wave15_perturbation_drug_response.md`
- `results_v3/wave15_surface_trafficking_dependency/candidate_ranked.tsv`
- `results_v3/wave15_orchestrator_dependency_scan/candidate_dependency_priority_summary.tsv`
- `results_v3/wave15_geneformer_loader_dependency_delete/wave15_geneformer_loader_dependency_gene_summary.tsv`

External:

- CTSH NCBI Gene: <https://www.ncbi.nlm.nih.gov/gene/1512>
- LAPTM5 NCBI Gene: <https://www.ncbi.nlm.nih.gov/gene/7805>
- CTSS RA ClinicalTrials.gov `NCT00425321`: <https://clinicaltrials.gov/study/NCT00425321>
- CTSS Sjogren ClinicalTrials.gov `NCT02701985`: <https://clinicaltrials.gov/study/NCT02701985>
- CTSS celiac ClinicalTrials.gov `NCT02679014`: <https://clinicaltrials.gov/study/NCT02679014>
- CTSS celiac PubMed `39739628`: <https://pubmed.ncbi.nlm.nih.gov/39739628/>
- ITGAM R77H functional paper: <https://pmc.ncbi.nlm.nih.gov/articles/PMC3488763/>
- Open Targets Platform / API documentation: <https://platform.opentargets.org/> and <https://platform-docs.opentargets.org/evidence>
