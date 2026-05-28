# Wave18-C Foundation-Model Candidate Rescue

Returned: 2026-05-27

Scope: re-examine existing Geneformer V2-104M token-deletion screens and State Parse CD14 outputs for candidates stronger than `CTSH`, then compare those model signals against real perturbation evidence from Mixscale/GSE281048, GSE162463, GSE162464, and GSE294918 where locally available.

## Executive Verdict

No candidate meets the strict rescue bar.

There are many genes with stronger Geneformer token-deletion scores than `CTSH`, but none has both:

- stronger-than-`CTSH` Geneformer support, and
- independent direct real perturbation validation from Mixscale/GSE162464/GSE294918.

The candidates with direct real perturbation support (`MED16`, `GSK3B`, `RFX5`, IFN/JAK/`STAT1`) are not rescued by Geneformer as primary evidence. Conversely, the candidates with stronger Geneformer scores mostly lack direct perturbation evidence or are contradicted by the GSE162463 macrophage MHC-II screen.

Recommendation: abandon foundation-model promotion as primary evidence for V3. Keep Geneformer only as triage. Use real perturbation data as the primary evidence channel.

## Reproducible Outputs

I added `scripts/v3_wave18_foundation_rescue.py` and wrote:

- `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
- `results_v3/wave18_foundation_rescue/geneformer_source_gene_summary.tsv`
- `results_v3/wave18_foundation_rescue/geneformer_consolidated_context_metrics.tsv`
- `results_v3/wave18_foundation_rescue/direct_perturbation_evidence_by_candidate.tsv`
- `results_v3/wave18_foundation_rescue/readout_concordance_by_candidate.tsv`
- `results_v3/wave18_foundation_rescue/state_parse_status.tsv`
- `results_v3/wave18_foundation_rescue/summary.json`

## Model Provenance

Geneformer provenance is identical across the local deletion screens:

- Model: `Geneformer V2-104M`
- Repo: `ctheodoris/Geneformer`
- Revision: `04c2b2e84da7c0f385c3f9ad8f3ec24bab6650e5`
- Local checkpoint: `tmp_v3/foundation_wave6/geneformer_assets/Geneformer-V2-104M`
- Encoder parameters loaded: `104,365,056`
- Max sequence length: `512`
- Metric: delete candidate token; positive cosine/projection shift means the disease-cell embedding moved toward the matched control centroid.
- Guardrail: custom lightweight embedding-deletion screen, not official `InSilicoPerturberStats`; candidate-expressing cells were enriched; effects are model hypotheses, not expression log2FC or causal perturbation evidence.

Run-specific settings:

| screen | disease/control cells per context | random deletion reps | seed |
|---|---:|---:|---:|
| `geneformer_candidate_delete` | 24/24 | 3 | 20260526 |
| `geneformer_pivot_panel_delete` | 30/30 | 4 | 20260526 |
| `geneformer_unrestricted_survivor_delete` | 30/30 | 4 | 20260526 |
| `geneformer_broad_residual_delete` | 30/30 | 4 | 20260526 |
| `wave14_geneformer_narrowed_candidate_delete` | 24/24 | 3 | 20260526 |
| `wave15_geneformer_loader_dependency_delete` | 24/24 | 3 | 20260526 |

State provenance:

- Model repo: `arcinstitute/ST-HVG-Parse`
- SHA: `a69af46d5b8c6f8c036c489a8f71354f321d968b`
- Split: `fewshot/split_4`
- Cell type: `CD14_Mono`
- Output features: `2000`
- Named-gene candidate status: blocked. Local axis scoring has `0` named genes and `state_parse_cd14_transition_target_rank.tsv` has `0` rows.
- Feature-agnostic validation is usable only as model sanity check: top focused target `IFN-gamma`, Spearman `0.4793`, direction match `0.7087`; focused median Spearman `0.2801`.

Real perturbation provenance used locally:

- Mixscale/GSE281048, Zenodo `14035992`: stimulated human cancer-cell pathway Perturb-seq.
- GSE162463: mouse macrophage IFN-gamma MHC-II/CD40/PD-L1 CRISPR/FACS screen.
- GSE162464: primary mouse macrophage `NTC/Gsk3b/Med16 +/- IFN-gamma` RNA-seq.
- GSE294918: human macrophage IFN-gamma memory/ruxolitinib CPM table.

## CTSH Baseline

`CTSH` remains weak.

Geneformer loader-dependency screen:

- contexts with token: `9`
- disease cells with token: `43`
- mean cosine shift: `-8.09e-05`
- mean projection shift: `0.00713`
- mean cosine z vs random: `0.0112`
- support contexts: `3`
- strong support contexts: `0`
- best context: `psoriasis_macrophage`, z `0.3572`, projection-minus-random `0.0228`

GSE162463 MHC-II screen comparator:

- `Ctsh` MHC-II low-vs-high median log2: `1.1391`
- rank: `1383`
- positive sgRNA fraction: `0.75`
- FDR: `0.9654`

No direct Mixscale/GSE162464/GSE294918 `CTSH` perturbation evidence was available locally.

## Candidate Rescue Ranking

Strict model-plus-direct rescue candidates: **none**.

Screen-only relative candidates that beat `CTSH` in Geneformer and in the GSE162463 MHC-II screen:

| candidate | Geneformer support | best Geneformer context | GSE162463 MHC-II rank / median | interpretation |
|---|---:|---|---:|---|
| `TMSB10` | 2 strong, 4 support | `IBD_stromal`, z `1.090` | rank `1166`, median `1.234` | screen-only; no Mixscale/GSE162464/GSE294918 direct perturbation |
| `SEC61A1` | 2 strong, 4 support | `t1d_stellate`, z `0.568` | rank `80`, median `2.958` | likely housekeeping/translocon liability; not promotion-grade |
| `CD74` | 1 strong, 2 support | `IBD_epithelial`, z `2.184` | rank `651`, median `1.564` | downstream state marker/readout, not a validated controller |
| `CD300E` | 1 strong, 1 support | `IBD_myeloid`, z `0.945` | rank `1262`, median `1.188` | barely above `CTSH`; no independent direct validation |
| `PTPN2` | 1 strong, 5 support | `ra_classical_monocyte`, z `0.864` | rank `803`, median `1.445` | screen-only; therapeutic direction is problematic for inhibition |

These are triage hits only. The GSE162463 screen FDRs are high across these rows, and none has the required independent Mixscale/GSE162464/GSE294918 direct perturbation support.

## Direct Perturbation Hits Not Rescued By Geneformer

These remain stronger as real perturbation evidence than as foundation-model evidence:

| candidate | real perturbation evidence | Geneformer result | recommendation |
|---|---|---|---|
| `MED16` | GSE162464 rank `1`, selectivity score `2.305`; GSE162463 rank `42`, median `3.349` | not in existing Geneformer candidate panels | real-data comparator only |
| `GSK3B` | GSE162464 rank `2`, selectivity score `0.778`; target module effect `-1.622`; margin vs IFN `0.827`; GSE162463 rank `39`, median `3.386` | 0 strong, 0 support; best context z `0.702` with sparse detections | use real perturbation, not foundation rescue |
| `RFX5` | Mixscale direct rank `4`, weak selective score `0.523`; transition rank `9`, score `0.501`; GSE162463 rank `153`, median `2.543` | 0 strong, 0 support; only 2 disease cells with token across source summary | use real perturbation, not foundation rescue |
| `STAT1` | Mixscale transition rank `4`, score `1.900`; GSE162463 rank `44`, median `3.337`; GSE294918 rux readout min `-3.353` | 1 strong, 2 support | positive control for broad IFN/JAK collapse, not selective candidate promotion |

## Contradictions And Readout-Only Rows

Several genes beat `CTSH` in Geneformer but fail real perturbation agreement:

- `CTSB`: 2 strong Geneformer contexts and 7 support contexts, but GSE162463 `Ctsb` is contradictory: rank `7028`, median `-0.0717`.
- `LGALS3`: 2 strong Geneformer contexts, but GSE162463 `Lgals3` is contradictory: rank `10774`, median `-1.0648`.
- `CTSL`: 1 strong context, but GSE162463 `Ctsl` is contradictory: rank `7848`, median `-0.2243`.
- `HIF1A`, `IFITM2`, `IFITM3`, `LIPA`, `CBX3`, and others also show Geneformer-positive rows with negative or weak GSE162463 direction.

Readout-only concordance should not be upgraded to candidate perturbation:

- `LAMP3`, `CTSS`, `IFI30`, `HLA-DMB`, and HLA/readout genes are reduced by some real controllers, but there is no direct candidate perturbation showing that perturbing the candidate itself causes the desired selective state shift.

## Recommendation

Do not promote a foundation-model-rescued candidate in V3.

The honest synthesis is:

1. Geneformer is useful for triage but too inconsistent and too weak to serve as primary evidence.
2. State Parse remains blocked for named-gene candidate promotion; feature-agnostic validation does not rescue any named target.
3. Real perturbation evidence still points to `MED16/GSK3B/RFX5` and IFN/JAK controls, but the foundation-model channel does not independently validate them.
4. `CTSH` should not be rescued. It remains weaker than multiple Geneformer candidates but lacks promotion-grade real perturbation alignment.

V3 should keep foundation-model output as a secondary screen only and anchor any intervention claim on reproducible real perturbation data plus disease-cell validation.
