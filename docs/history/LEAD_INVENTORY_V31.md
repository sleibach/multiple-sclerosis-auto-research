# Lead Inventory V31

Date: 2026-06-07

## Scope

V31 completes the V30 access blocker by reaching Claude through SAP AI Core
Orchestration, runs the queued independent review across Claude and Gemini, and
grounds the resulting proposals as far as current local artifacts allow. Model
outputs are proposal queues only; evidence comes from local data checks.

No locked rule was edited. No reserved fresh validation cohort was present or
read.

## Access Status

Detailed access report: `meta/SAP_AI_CORE_ACCESS_V30.md`.

Working lineages:

- Claude 4.7 Opus through SAP AI Core Orchestration:
  - orchestration deployment `d65236404bbfb6b2`
  - model deployment `def854013c7ac379`
  - smoke response: `OK`
- Gemini 2.5 Pro through native Gemini endpoint:
  - model deployment `d6dc532885507ac7`
  - smoke response: `OK`

Still blocked / optional:

- Mistral `mistralai--mistral-medium-instruct` is discoverable but timed out
  again on `/chat/completions`.

Reusable client:

- `scripts/sap_ai_core_client.py`

## Multi-Lineage Review Artifacts

- Prompt:
  `analysis/v31_multi_lineage_review/independent_review_prompt.md`
- Claude raw/parsed:
  - `analysis/v31_multi_lineage_review/claude_opus_review.json`
  - `analysis/v31_multi_lineage_review/claude_opus_review.parsed.json`
- Gemini raw/parsed:
  - `analysis/v31_multi_lineage_review/gemini_2_5_pro_review.json`
  - `analysis/v31_multi_lineage_review/gemini_2_5_pro_review.parsed.json`

Both parsed outputs are valid JSON.

## Consolidated Proposal Grounding

| Theme | Proposed by | Grounded outcome | Evidence / action |
|---|---|---|---|
| Baseline immune-remodeling potential may explain V22 dynamics | Claude | queued, not resolved | Existing V22/V23 reusable tables contain paired deltas and locked scores, not baseline module scores. Raw expression exists locally, so this is executable as a focused raw-expression analysis. |
| Sex/age/cohort imbalance may drive bounded signal | Claude | blocked pending metadata extraction | V28 adjusted for cohort but not age/sex. GEO metadata must be parsed from local SOFT/series files before refit. |
| Cell composition/proliferation artifact may explain APC/HLA-II score | Claude | queued | V28 receptor-only control failed, but monocyte/DC/proliferation controls were not scored. Raw data exists; needs signature scoring. |
| LDSC partitioned heritability for APC/HLA-II module genes | Claude | queued | LDSC panel is available; custom annotation for V22 module genes has not been built. This would test genetic anchoring of the transcriptomic axis. |
| Steroid / glucocorticoid / IFN-suppression mimic | Claude and V30 Gemini | partially blocked | No local pre/post high-dose steroid MS relapse cohort is present. Glucocorticoid and IFN-suppression signatures can still be scored on V22/V23 cohorts. |
| Metabolic confounding / NAMPT-as-covariate | Gemini and V30 Gemini | queued | V29 proposed NAMPT/HIF/glycolysis covariate adjustment. Existing V28 did not score metabolic pathway signatures. Needs raw-expression pathway scoring. |
| STAT1 master-axis reduction | Gemini | queued | Directly testable by scoring STAT1 targets and comparing against V26/V22 module axes; not yet run. |
| Cell-type mismatch explains psoriasis/adalimumab failure | Gemini | partly unsupported / risky | V23 exact UC compartment signal is strongest in T/B-like compartments, but deriving a T-cell response signature from UC and testing psoriasis skin would be highly overfit and cross-tissue. Keep as hypothesis, not grounded finding. |
| Chr1 cell-type-specific antagonistic eQTL | Gemini | mostly failed in local DICE significant-eQTL data | DICE scan found 371 chr1 candidate/credible-set hits: `DDX59` 361, `CAMSAP2` 5, `RP11-532L16.1` 3, `KIF21B` 1, `GPR25` 0. The only KIF21B DICE hit was NK at `rs141492016` and was not an exact credible-set hit. No local evidence for antagonistic GPR25/KIF21B cell-type eQTL. |
| KIF21B trans/pathway analysis | V30 Gemini / related | queued, data-limited | Local V19 supports KIF21B cis regulation. No local genome-wide trans-eQTL summary scan is present. |

## Grounded Vulnerability Tests

### V22 Bounded Scalar: Cross-Cohort Generalization

Models converged on the risk that the bounded n=19 signal is a pooled small-n
artifact.

Fast grounding used existing paired-score tables:

- `analysis/v31_multi_lineage_review/v31_cross_cohort_score_grounding.tsv`

Results:

| Test | Result |
|---|---|
| Within `GSE235357` DMF AUC | `0.72` |
| Within `GSE253006_TOF_exact` AUC | `0.95` |
| Median threshold trained on DMF, tested on UC | accuracy `0.667`; UC rank AUC remains `0.95` |
| Median threshold trained on UC, tested on DMF | accuracy `0.600`; DMF rank AUC remains `0.72` |

Interpretation: the score direction is positive in both cohorts, but fixed
threshold transfer is weak. This supports the V28/V30 limitation: the scalar is
directionally robust but not yet a calibrated clinical decision threshold.

### V26 Deep-Structure Artifact Risk

Both models flagged that the V26 coupled axis may partly reflect shared module
construction.

Fast grounding:

- `analysis/v31_multi_lineage_review/v31_v26_shared_module_overlap.tsv`

Result: the modalities that can show strong similarity share the same module
columns by construction. Treatment pharmacodynamic, cell-state, and
cross-disease matrices share all eight module labels; perturbation comparisons
share the three core APC modules.

Interpretation: this does not kill V26, because V26 already used permutation
and replication gates, but it is a real vulnerability. A stronger test requires
gene-overlap-removed and normalization-sensitivity reruns.

### Chr1 GPR25/KIF21B eQTL Ambiguity

Both models challenged the GPR25/KIF21B framing from different angles.

Fast local DICE scan:

- `analysis/v31_multi_lineage_review/v31_dice_chr1_candidate_hits.tsv`
- `analysis/v31_multi_lineage_review/v31_dice_chr1_candidate_gene_counts.tsv`

Result: DICE significant immune eQTLs in the chr1 candidate/credible-set scan
are dominated by `DDX59`, not GPR25 or KIF21B:

- `DDX59`: 361 rows
- `CAMSAP2`: 5 rows
- `RP11-532L16.1`: 3 rows
- `KIF21B`: 1 row
- `GPR25`: 0 rows

Interpretation: no local DICE evidence supports a clean antagonistic
GPR25/KIF21B cell-type eQTL model. This does not overturn V19's dense
eQTL-Catalogue KIF21B cis-coloc, but it reinforces that chr1 is a
controlled-data handoff, not an intervention-ready computational lead.

## Did Multi-Lineage Review Add Value?

Yes, but mostly by sharpening the next negative-control analyses, not by
reactivating a lead.

New or sharpened beyond V30:

1. Baseline-vs-dynamic APC/HLA-II test.
2. Explicit age/sex metadata adjustment for the bounded V22 scalar.
3. Proliferation/cell-composition controls.
4. Partitioned LDSC heritability for V22 module genes.
5. V26 module-overlap / normalization-sensitivity critique.
6. STAT1 master-axis reduction test.

No model-proposed item becomes evidence or an upgraded lead in V31.

## Refreshed Ranked Inventory

| Rank | Lead / work item | V31 status | Next requirement |
|---:|---|---|---|
| 1 | V22 bounded APC/HLA-II scalar | active validation lead, directionally robust but threshold-uncalibrated | Fresh paired cohort plus V32 confounder scoring. |
| 2 | V22/V23 raw-expression confounder panel | top computational next action | Score baseline APC/HLA-II, metabolic, inflammatory, glucocorticoid, IFN-suppression, STAT1, proliferation/cell composition. |
| 3 | Postpartum HLA-II/CD64 APC split | best dormant biology lead | Postpartum MS blood/CSF cohort or steroid-pulse mimic data scout. |
| 4 | V26 coupled APC axis | mechanistic context with artifact vulnerability | Gene-overlap-removed and normalization-sensitivity rerun. |
| 5 | ZMIZ1 opposite-direction MS/Crohn locus | robust transfer-validity finding | No immediate computational change. |
| 6 | chr1 KIF21B/GPR25 | real genetics / controlled-data handoff | Controlled immune/CSF expression/protein data or genome-wide trans-eQTL scan. |
| 7 | NAMPT/metabolic stress | covariate / negative-control axis | Pathway scoring in V22/V23 cohorts. |

## V31 Verdict

V31 completes the intended multi-lineage access step: Claude and Gemini both
work through SAP AI Core, and both independently point to the same broad risk
class: the treatment-response lead may be a small-n, pooled, baseline,
cell-composition, metabolic/STAT1, or generic immunosuppression signal rather
than a specific APC/HLA-II pharmacodynamic monitor.

The grounded checks do not kill the lead. They do narrow it:

- direction is positive in both bounded cohorts;
- fixed threshold transfer is weak;
- V26 coupled-axis structure has a real module-overlap vulnerability;
- chr1 does not reactivate from DICE cell-type eQTL evidence.

No intervention-grade lead is promoted. The next highest-value computation is
the V32 raw-expression confounder panel against the exact V22/V23 cohorts.
