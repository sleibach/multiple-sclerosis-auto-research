# Wave82 Cross-Disease Residual Stress Test

Returned: 2026-05-27 18:18 CEST

Role: strict sidecar audit of residual Wave81 candidates. This artifact does
not edit code and does not claim a therapeutic finding.

## Inputs Read

- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/raw_remission_response_gene_tests.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/paired_gene_delta_tests.tsv`
- `DATA_V3.md`

Candidate set: `DAB2`, `CD9`, `PSAP`, `LYN`, `FAM49B`, `LRRC61`,
`HEXA`, `HEXB`, `DAP`, `PARK7`, `FMNL2`.

## Strict Bottom Line

No Wave81 residual candidate has a real pan-autoimmune lipid-lysosomal/myeloid
mechanism by the V3 standard. The best residuals are mechanistic controls or
parked readouts, not promotable targets. The main failure modes are:

- no candidate combines positive perturbation/model support, MS anchoring,
  target-resolved genetics, cross-disease myeloid replication, and response
  direction;
- all MS white-matter signals in `GSE111972` fail FDR correction;
- Wave62 target-resolution contains only `PARK7` from this candidate set, and
  even `PARK7` is `NO_GO_WAVE62_TARGET_RESOLUTION`;
- Wave68 IBD anti-TNF response rows are nominal at best and all candidate rows
  fail FDR10;
- broad disease recurrence often maps to epithelial, stromal, endothelial,
  keratinocyte, or pancreatic stellate compartments rather than myeloid/APC.

## Candidate Audits

### `DAB2`

Support:

- Wave81: `PARK_PERTURBATION_FIRST_CANDIDATE`, score `9`.
- Direct perturbation: Wave37 `KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR`.
- MS white matter: `delta_log2=0.538`, p `0.0111`, FDR `0.835`.
- IBD response: Wave81 nominal response flag true; Wave68 raw response does not
  pass p<0.05 (`Mono_macro` p `0.0837`, `DC` p `0.610`).
- Paired IBD delta: `DC mean_delta=0.396`, p `0.0472`, FDR `1.0`.

Contradictions / confounders:

- Broad h5ad has no positive nominal disease contexts and three negative
  nominal contexts.
- Strongest broad myeloid signals are negative: UC colon myeloid
  `delta=-2.62`, p `0.00270`, FDR `0.146`; Crohn colon myeloid
  `delta=-1.72`, p `0.0311`, FDR `0.338`.
- No Wave62 target-resolution/genetic row.
- Efferocytosis KO is mechanistically relevant but is not yet a human
  autoimmune disease-state perturbation.

Disposition: park as an efferocytosis assay control; no pan-autoimmune target
claim.

### `CD9`

Support:

- Wave81: `PARK_PERTURBATION_FIRST_CANDIDATE`, score `8`.
- Direct perturbation: Wave37 `KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR`.
- MS white matter: `delta_log2=1.110`, p `0.00197`, FDR `0.834`.

Contradictions / confounders:

- Broad h5ad has no positive nominal contexts and three negative nominal
  contexts.
- Crohn colon myeloid is negative (`delta=-1.34`, p `0.00290`, FDR `0.149`);
  UC colon myeloid is negative (`delta=-1.16`, p `0.00605`, FDR `0.194`).
- Wave68 response is unsupported: raw `DC` p `0.178`, `Mono_macro` p `0.493`;
  paired deltas both FDR `1.0`.
- No Wave62 target-resolution/genetic row.

Disposition: no-go for pan-autoimmune lipid-lysosomal/myeloid mechanism; keep
only as a local efferocytosis/MS-lesion comparator.

### `PSAP`

Support:

- Wave81: `PARK_PERTURBATION_FIRST_CANDIDATE`, score `7`.
- Foundation-model support: Wave57 `support=1`, `strong=0`,
  `token_contexts=6`.
- MS white matter: `delta_log2=0.473`, p `0.0223`, FDR `0.845`.
- Biological proximity is plausible because `PSAP` is a lysosomal
  sphingolipid/prosaposin node, but this local audit does not establish it as
  causal.

Contradictions / confounders:

- Broad h5ad has only one positive nominal context: T1D pancreatic ductal
  cell `delta=0.319`, p `0.0454`, FDR `0.471`.
- Myeloid disease contexts trend negative or nonsignificant: Crohn colon
  myeloid `delta=-0.869`, p `0.0901`, FDR `0.473`; UC colon myeloid
  `delta=-0.769`, p `0.117`, FDR `0.511`.
- Wave68 response is unsupported: raw `DC` p `0.355`, `Mono_macro` p `0.977`;
  paired deltas both FDR `1.0`.
- No Wave62 target-resolution/genetic row.

Disposition: park as a lysosomal-neurobiology hypothesis, not a
cross-autoimmune myeloid target.

### `LYN`

Support:

- Wave81: `PARK_PERTURBATION_FIRST_CANDIDATE`, score `6`.
- Foundation-model support: Wave70C `support=3`, `strong=1`,
  `token_contexts=6`.
- Broad h5ad positive nominal diseases: Crohn, psoriasis, UC.
- Best broad contexts: Crohn colon epithelial `delta=1.07`, p `0.00149`,
  FDR `0.104`; psoriasis keratinocyte `delta=2.43`, p `0.0112`,
  FDR `0.385`; UC colon myeloid `delta=0.974`, p `0.0139`, FDR `0.257`;
  Crohn colon myeloid `delta=0.965`, p `0.0145`, FDR `0.260`.
- Wave68 raw response: `Mono_macro delta=-0.556`, p `0.0125`, FDR `0.736`.

Contradictions / confounders:

- No MS anchor: Wave81 `ms_anchor=0`; MS white matter `delta=0.100`,
  p `0.451`, FDR `0.923`.
- No Wave62 target-resolution/genetic row.
- Broad positives are nominal and do not pass FDR10; several strongest
  contexts are epithelial/keratinocyte rather than myeloid.
- `LYN` is a broad immune kinase node; current local evidence does not separate
  lipid-lysosomal myeloid biology from generic inflammatory cell abundance.

Disposition: park only as a pathway comparator. It is the best residual
cross-disease signal numerically, but fails MS/genetic specificity.

### `FAM49B`

Support:

- Wave81: `PARK_PERTURBATION_FIRST_CANDIDATE`, score `6`.
- Direct perturbation: Wave37 `KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR`.
- Broad h5ad positive nominal diseases: Crohn, psoriasis, UC.
- Best myeloid/supporting rows: Crohn colon myeloid `delta=0.623`,
  p `0.00327`, FDR `0.154`; UC colon myeloid `delta=0.438`, p `0.0230`,
  FDR `0.302`.

Contradictions / confounders:

- No MS anchor: MS white matter `delta=0.105`, p `0.346`, FDR `0.914`.
- No Wave62 target-resolution/genetic row.
- No Wave68 response support: raw rows p `0.112` and `0.230`; paired rows FDR
  `1.0`.
- Broad signal is nominal only and could reflect generic inflamed tissue or
  macrophage abundance.

Disposition: park as a low-priority efferocytosis/cytoskeleton control; no
promotable mechanism.

### `LRRC61`

Support:

- Wave81: `PARK_PERTURBATION_FIRST_CANDIDATE`, score `6`.
- Direct perturbation: Wave37 `KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR`.
- Broad h5ad positive nominal diseases: Crohn, Sjogren, T1D, UC.
- One broad FDR10 row: T1D pancreatic stellate cell `delta=2.63`,
  p `0.000681`, FDR `0.0988`.
- Crohn colon myeloid: `delta=1.88`, p `0.0126`, FDR `0.245`.

Contradictions / confounders:

- No MS anchor: MS white matter `delta=0.697`, p `0.582`, FDR `0.946`.
- No Wave62 target-resolution/genetic row.
- Wave68 response fails FDR10; raw `Mono_macro` p `0.0653`, FDR `0.967`.
- The only FDR10 broad context is pancreatic stellate, not myeloid/APC.
- Gene biology is poorly actionable from these artifacts.

Disposition: no-go as therapeutic target; possible broad-state marker only.

### `HEXA`

Support:

- Wave81: `PARK_PERTURBATION_FIRST_CANDIDATE`, score `5`.
- Foundation-model support: Wave57 `support=1`, `strong=1`,
  `token_contexts=3`.
- Broad h5ad positive nominal disease: Crohn colon epithelial
  `delta=0.366`, p `0.0120`, FDR `0.177`.
- Paired IBD delta: `DC mean_delta=0.400`, p `0.00138`, FDR `0.542`.

Contradictions / confounders:

- No MS anchor: MS white matter `delta=-0.233`, p `0.378`, FDR `0.914`.
- Broad myeloid rows are negative or nonsignificant: Crohn colon myeloid
  `delta=-0.731`, p `0.120`, FDR `0.505`; UC colon myeloid `delta=-0.721`,
  p `0.132`, FDR `0.529`.
- No Wave62 target-resolution/genetic row.
- The lysosomal-enzyme identity is biologically close to the module but too
  nonspecific, with no disease-genetic or direction evidence here.

Disposition: no-go target; keep as lysosomal pathway readout/control.

### `HEXB`

Support:

- Wave81: `PARK_PERTURBATION_FIRST_CANDIDATE`, score `5`.
- Foundation-model support: Wave57 `support=1`, `strong=1`,
  `token_contexts=4`.
- Paired IBD delta: `DC mean_delta=0.218`, p `0.0352`, FDR `1.0`.

Contradictions / confounders:

- No MS anchor: MS white matter `delta=0.244`, p `0.202`, FDR `0.899`.
- Broad h5ad has no positive nominal context and two negative nominal
  contexts: UC colon myeloid `delta=-0.902`, p `0.0116`, FDR `0.242`;
  Crohn colon myeloid `delta=-0.838`, p `0.0177`, FDR `0.275`.
- No Wave62 target-resolution/genetic row.

Disposition: no-go target; lysosomal readout/control only.

### `DAP`

Support:

- Wave81: `NO_GO_NO_PERTURBATION_SUPPORT`, score `7`.
- MS white matter: `delta_log2=0.393`, p `0.00807`, FDR `0.834`.
- Broad h5ad positive nominal diseases: Crohn, psoriasis, UC.
- Best broad rows: UC colon epithelial `delta=0.851`, p `0.00224`,
  FDR `0.103`; psoriasis stromal `delta=0.636`, p `0.00254`,
  FDR `0.491`; psoriasis APC `delta=0.662`, p `0.00689`, FDR `0.730`;
  Crohn colon epithelial `delta=0.889`, p `0.00758`, FDR `0.154`.
- Paired IBD delta: `Mono_macro mean_delta=-0.536`, p `0.00226`,
  FDR `0.423`.

Contradictions / confounders:

- Wave81 says it lacks direct perturbation or positive foundation-model
  support.
- No Wave62 target-resolution/genetic row.
- Cross-disease positives are largely epithelial/stromal and FDR-failing.
- IBD response is nominal only and direction is not tied to remission biology
  after FDR correction.

Disposition: no-go for Wave82; expression residual without perturbation is
not enough.

### `PARK7`

Support:

- Wave81: `NO_GO_PERTURBATION_FIRST_BLOCKED`, score `6`.
- Foundation-model support: Wave57 `support=2`, `strong=0`,
  `token_contexts=3`.
- Broad h5ad positive nominal diseases: Sjogren, psoriasis, UC.
- Best broad rows: UC colon myeloid `delta=0.324`, p `0.0112`, FDR `0.239`;
  UC colon epithelial `delta=0.569`, p `0.0124`, FDR `0.201`; psoriasis
  keratinocyte `delta=0.872`, p `0.0355`, FDR `0.401`; Sjogren salivary APC
  `delta=0.335`, p `0.0381`, FDR `0.941`.
- Wave62 is the only target-resolution row among the candidate set, but it is
  weak: `wave62_score=2.59`, `NO_GO_WAVE62_TARGET_RESOLUTION`, max L2G
  `0.128`, no strong/supporting L2G disease, max QTL H4 `0.963` in UC,
  local positive disease count `3`, residual-retained disease count `0`.

Contradictions / confounders:

- No MS anchor: MS white matter `delta=0.171`, p `0.447`, FDR `0.922`;
  Wave62 `ms_max_l2g_score=0`.
- Wave68 response is unsupported after FDR: raw rows p `0.624` and `0.788`;
  paired `Mono_macro mean_delta=-0.208`, p `0.00730`, FDR `0.616`.
- Oxidative-stress biology could be a generic injury/readout axis, not a
  specific lipid-lysosomal myeloid controller.

Disposition: park as a stress-resilience comparator; do not promote.

### `FMNL2`

Support:

- Wave81: `NO_GO_NO_PERTURBATION_SUPPORT`, score `7`.
- MS white matter: `delta_log2=0.412`, p `0.0324`, FDR `0.851`.
- Broad h5ad positive nominal diseases: Crohn, psoriasis, T1D, UC.
- Best broad rows: UC colon epithelial `delta=1.27`, p `0.00288`,
  FDR `0.117`; Crohn colon epithelial `delta=0.603`, p `0.0102`,
  FDR `0.165`; psoriasis keratinocyte `delta=1.46`, p `0.0152`,
  FDR `0.392`; T1D pancreatic endothelial `delta=1.33`, p `0.0188`,
  FDR `0.323`.
- Wave68 raw response: `DC delta=-1.45`, p `0.0406`, FDR `1.0`.

Contradictions / confounders:

- Wave81 says it lacks direct perturbation or positive foundation-model
  support.
- No Wave62 target-resolution/genetic row.
- Broad myeloid/APC contexts contradict the pan-myeloid claim: UC colon
  myeloid `delta=-1.36`, p `0.157`, FDR `0.560`; psoriasis APC
  `delta=-0.938`, p `0.139`, FDR `0.730`; Sjogren APC `delta=-0.769`,
  p `0.0789`, FDR `0.941`.
- Recurrence is dominated by epithelial/endothelial/keratinocyte contexts.

Disposition: no-go for pan-autoimmune myeloid mechanism; possible non-myeloid
inflammation marker.

## Cross-Candidate Pattern

The residuals split into four non-promotable classes:

1. Direct efferocytosis perturbation plus nominal MS expression but
   cross-disease myeloid contradiction: `DAB2`, `CD9`.
2. Foundation/model or lysosomal proximity with no MS/genetic/cell-state
   convergence: `PSAP`, `HEXA`, `HEXB`, `PARK7`.
3. Cross-disease nominal expression but tissue-cell mismatch and no
   perturbation/model support: `DAP`, `FMNL2`.
4. Cross-disease nominal immune signal without MS/genetic specificity:
   `LYN`, `FAM49B`, `LRRC61`.

This argues against a single residual gene target being hidden in the Wave81
parked list. The module remains real as a disease-state pattern, but the
residual candidates do not establish a tractable central node.

## Ranked Promote / Park / No-Go Table

| Rank | Candidate | Call | Reason |
|---:|---|---|---|
| 1 | `LYN` | PARK | Best nominal cross-disease breadth plus model support, but no MS anchor, no Wave62 genetic row, and likely generic immune-kinase/macrophage-abundance confounding. |
| 2 | `PSAP` | PARK | Closest to lipid-lysosomal biology and nominal MS signal, but cross-disease myeloid evidence is weak/negative and there is no target-resolution genetics. |
| 3 | `PARK7` | PARK | Model support and weak target-resolution row, but no MS anchor, no strong L2G disease, no FDR10 response, and likely generic oxidative-stress biology. |
| 4 | `DAB2` | PARK | Direct efferocytosis perturbation plus nominal MS signal, but Crohn/UC myeloid expression is directionally negative and no genetics/modality support exists. |
| 5 | `FAM49B` | PARK | Direct efferocytosis perturbation and nominal Crohn/UC/psoriasis expression, but no MS anchor, no genetics, no response, and no FDR10 broad support. |
| 6 | `LRRC61` | NO-GO | Broad nominal expression and one FDR10 T1D stellate row, but no MS/genetic support and tissue-cell mismatch dominates. |
| 7 | `CD9` | NO-GO | Direct efferocytosis perturbation and nominal MS signal are contradicted by negative Crohn/UC myeloid expression and no response/genetics. |
| 8 | `FMNL2` | NO-GO | Nominal MS and broad disease expression are mostly non-myeloid; direct/model support is absent. |
| 9 | `DAP` | NO-GO | Nominal MS/broad expression without direct/model support or genetics. |
| 10 | `HEXA` | NO-GO | Lysosomal enzyme/model signal, but no MS anchor, no genetics, and contradictory myeloid disease-state expression. |
| 11 | `HEXB` | NO-GO | Lysosomal enzyme/model signal, but no MS anchor and negative Crohn/UC myeloid expression. |

Promotion count: `0`.
