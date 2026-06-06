# Wave104 Genetics / Colocalization Sidecar

Timestamp: 2026-05-27 21:58 CEST

Role: target-resolved genetics sidecar for the Wave104 genetics-first V3
autoimmune/MS branch. Scope is limited to `IFI30`, `SP140`, `GALC`, `CD58`,
and `IL7R`. This sidecar does not claim a finding.

## Bottom Line

No target receives a therapeutic `GO`.

| Gene | Genetics-sidecar call | Main reason |
| --- | --- | --- |
| `IFI30` | `PARK_MS_BENCHMARK_ONLY`; `NO_GO` as direct target | Real MS L2G plus monocyte QTL-coloc, but Wave62 L2G breadth is MS-only and direct antigen-processing/host-defense targeting is blocked. |
| `SP140` | `PARK_COMPARATOR_STRATIFICATION_ONLY` | Credible MS/Crohn/psoriasis target resolution, but strict cross-disease breadth misses the Wave62 gate and direction is mixed/prior-art blocked. |
| `GALC` | `PARK_DIRECTION_AND_LOCUS_REVIEW_ONLY` | MS GALC support exists, but one MS locus ranks `GPR65` above `GALC`; non-MS support is weaker/less relevant and restoration direction is unresolved. |
| `CD58` | `PARK_MS_GENETICS_ONLY` | Strong MS L2G/QTL-coloc, but Wave62 L2G breadth is MS-only and direction/modality remain unresolved. |
| `IL7R` | `NO_GO_V3_PROMOTION`; `PARK_COMPARATOR_ONLY` | Strongest broad target-resolved genetics in this set, but CD127/IL7R is prior-art crowded and direction/cell mechanism is not V3-specific. |

## Inputs Read

- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave62_opentargets_target_resolution/opentargets_l2g_rows.tsv`
- `results_v3/wave62_opentargets_target_resolution/opentargets_qtl_coloc_rows.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_gate_matrix.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_candidate_audit.tsv`
- `results_v3/wave104_genetics_first_lipid_state_convergence_audit/genetics_first_lipid_state_rank.tsv`
- `subagents_v3/wave56j_sp140_genetics_prior_art.md`
- `subagents_v3/wave58n_il7r_therapeutic_audit.md`

Internet verification was not used; local artifacts were sufficient.

## Interpretation Rules

- Wave62 is an Open Targets L2G/QTL-coloc triage, not raw-summary-statistic
  colocalization or MR. Its own report states: "Target-resolution triage only.
  L2G/QTL colocalisation is not therapeutic causality."
- Direction proxy values are the Wave62 field
  `risk_qtl_direction_proxy = disease_beta * betaRatioSignAverage`. I treat the
  sign as a proxy only, not as a therapeutic increase/decrease instruction.
- `strong_l2g_disease_count` and `strong_qtl_coloc_disease_count` are from
  `target_resolution_summary.tsv`; detailed H4/CLPP/cell values are from
  `opentargets_qtl_coloc_rows.tsv`.

## Traceable Evidence Summary

| Gene | MS L2G | MS relevant QTL H4 | Strong L2G diseases | Strong QTL-coloc diseases | Wave55 broader genetics | Wave104 call |
| --- | ---: | ---: | --- | --- | --- | --- |
| `IFI30` | 0.6501 | 0.9959 | MS | Celiac;Crohn;MS | none recorded; score 0.0 | `PARK_GENETICS_STATE_DIRECTION_NO_MODALITY` |
| `SP140` | 0.8755 | 0.9868 | Crohn;MS;Psoriasis | Crohn;MS;Psoriasis | AS;Crohn;MS;Psoriasis;RA;UC; score 26.0 | `PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY` |
| `GALC` | 0.7025 | 0.9873 | Crohn;MS | AS;Crohn;MS | AS;Crohn;MS;SLE;UC; score 21.0 | `PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY` |
| `CD58` | 0.9514 | 0.9945 | MS | Crohn;MS | MS;PBC;SLE; score 17.0 | `PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY` |
| `IL7R` | 0.9448 | 0.9845 | Crohn;MS;PBC;T1D | Crohn;MS;PBC;T1D | AITD;Crohn;MS;PBC;Psoriasis;SLE;T1D; score 26.0 | `PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY` |

## Gene Reviews

### `IFI30`

MS genetic anchor strength: moderate but real. Wave62 reports MS max L2G
`0.6501023173332214`, with two MS L2G loci in `opentargets_l2g_rows.tsv`:
`d8042fac4818035ae4af8557e0cbf623` at L2G `0.6501023173332214` and
`de33a8d331b36c85e3316c1161bd8dc3` at L2G `0.6446198225021362`. In both
MS loci, `IFI30` is L2G rank 1 ahead of `MPV17L2` and `PDE4C`.

Cross-autoimmune breadth: weak for target-resolved L2G. Wave62 strong L2G
disease count is `1` (`MS`). Wave62 same-target QTL-coloc diseases are
`Celiac;Crohn;MS`, but the Celiac and Crohn rows are blood-plasma QTL rows
without matching `IFI30` L2G disease breadth in the local L2G table.
Wave55 contributes no broader genetic disease list for `IFI30` and has score
`0.0`.

QTL/coloc tissue/cell support: strongest in MS CD14-positive classical
monocytes. Detailed QTL rows show MS `4` relevant rows, all `4` myeloid, with
max H4 `0.9959013728724722`, CLPP `0.1771060825159371`, biosample
`CD14-positive, CD16-negative classical monocyte`. Non-MS detailed rows:
Celiac blood plasma max H4 `0.9969048401100167`, Crohn blood plasma max H4
`0.838268`.

Direction proxy: MS monocyte proxies are negative in the detailed rows
(`-0.0182355948105376` and `-0.1414483635843748`). Celiac blood-plasma proxies
are negative; Crohn blood plasma is `0.0`. This does not define an intervention
direction.

Target-resolution assessment: credible for an MS `IFI30` target-resolution
benchmark, not credible as a cross-autoimmune actionable target. Wave62 also
sets manual blocker `direct_antigen_processing_host_defense_and_druggability`.

Sidecar recommendation: `PARK_MS_BENCHMARK_ONLY`; `NO_GO` for direct therapeutic
targeting.

### `SP140`

MS genetic anchor strength: strong. Wave62 reports MS max L2G
`0.8754889965057373` at study locus `d500cf1bf626a4da032d49faaba8ea22`
(`rs13426106`), where `SP140` is L2G rank 1 and `SP110` is rank 2 at
`0.15932774543762207`.

Cross-autoimmune breadth: credible but not broad enough for the strict Wave62
cross-disease gate. Wave62 strong L2G disease count is `3`
(`Crohn;MS;Psoriasis`), and strong/relevant QTL-coloc diseases are also
`Crohn;MS;Psoriasis`. Wave55 broader associated-target genetics lists
`AS;Crohn;MS;Psoriasis;RA;UC` with score `26.0`, but the Wave62 gate
`cross_disease_l2g_ge_4_or_supporting_ge_5` is `False`.

QTL/coloc tissue/cell support: immune-cell support is real but heterogeneous.
Detailed relevant QTL rows show:

- MS: `19` relevant rows, `2` myeloid rows, max H4 `0.9868116204726999`,
  top biosample `lymphoblastoid cell line`.
- Crohn: `18` relevant rows, `4` myeloid rows, max H4 `0.9891974580445424`,
  top biosample `lymphoblastoid cell line`.
- Psoriasis: `23` relevant rows, `6` myeloid rows, max H4 `0.978430`, top
  biosample `macrophage`.

Direction proxy: mixed. MS has `-0.15443635330441896`, `0.0`, and
`0.15443635330441896` proxies across relevant rows. Crohn has both
`0.03614526526895776` and `-0.03614526526895776`; psoriasis has `0.0`,
`0.0725`, and `-0.0725`. The local Wave56-J audit additionally blocks generic
SP140 modulation because genetic loss/reduced full-length SP140 and published
SP140 inhibition can point in opposite directions.

Target-resolution assessment: credible for a target-resolved MS/Crohn/psoriasis
genetics comparator, not a clean intervention target. Direction, prior art, and
strict breadth prevent promotion.

Sidecar recommendation: `PARK_COMPARATOR_STRATIFICATION_ONLY`.

### `GALC`

MS genetic anchor strength: moderate. Wave62 reports MS max L2G
`0.7024610638618469`, with two MS target rows: `GALC` L2G `0.5347843170166016`
at `5a6af436f7838697327eeeeb801fc248` and `0.7024610638618469` at
`877cf385878d6d4b6c01cb3acd784536`.

Cross-autoimmune breadth: limited. Wave62 strong L2G diseases are
`Crohn;MS` (`2`), supporting L2G diseases are `AS;Crohn;MS` (`3`), and strong
QTL-coloc diseases are `AS;Crohn;MS` (`3`). However, Wave62 relevant QTL-coloc
disease count is only `1` (`MS`), and the gate `qtl_coloc_multiple_diseases` is
`False`. Wave55 broader associated-target genetics lists `AS;Crohn;MS;SLE;UC`
with score `21.0`.

QTL/coloc tissue/cell support: MS-relevant support is strong in myeloid-relevant
rows, but not cross-disease. Detailed MS rows show `13` relevant rows, `3`
myeloid rows, max H4 `0.9873343718864264`, CLPP `0.06531947037573549`, top
biosample `CD14-positive, CD16-negative classical monocyte`. Other MS-relevant
biosamples include fibroblast, neutrophil, thyroid gland, and CD4-positive T
cell.

Direction proxy: MS monocyte top proxy is positive
`0.270759405255873`; neutrophil/thyroid-related proxies include
`0.2334464443101069`, while fibroblast rows include `-0.0`. This is not enough
to decide restoration, activation, or substrate-handling direction.

Target-resolution assessment: partially credible but locus-level ambiguous.
At one MS locus (`877cf...`) `GALC` is L2G rank 1 and `GPR65` rank 2
(`0.23583291471004486`); at the other (`5a6a...`) `GPR65` is rank 1
(`0.6238155364990234`) and `GALC` rank 2. Same-target QTL support upgrades
`GALC`, but the 14q locus should not be treated as uniquely resolved without
further fine-mapping and functional direction.

Sidecar recommendation: `PARK_DIRECTION_AND_LOCUS_REVIEW_ONLY`.

### `CD58`

MS genetic anchor strength: strong and target-resolved in MS. Wave62 reports
MS max L2G `0.9513845443725586`, with three MS L2G loci:
`b019fe75b51b088838b09c72216af801` at `0.9513845443725586`,
`60eccbb51a18714ae52e2d150431c093` at `0.9327451586723328`, and
`255d4d28fee11d6c5a0a4fb1d35becf0` at `0.9437225461006165`. `CD58` is rank 1
at all three loci in `opentargets_l2g_rows.tsv`.

Cross-autoimmune breadth: narrow. Wave62 strong L2G disease count is `1`
(`MS`). Strong/relevant QTL-coloc diseases are `Crohn;MS`, but the Crohn row is
blood plasma only and does not establish a matched Crohn L2G package for CD58
in the local L2G rows. Wave55 broader associated-target genetics lists
`MS;PBC;SLE` with score `17.0`.

QTL/coloc tissue/cell support: strong MS but mostly lymphoblastoid/plasma
contexts. Detailed relevant QTL rows show MS `25` relevant rows, `2` myeloid
rows, max H4 `0.9944626523267263`, CLPP `0.1377120249772093`, top biosample
`lymphoblastoid cell line`; MS-relevant biosamples also include
CD14-positive classical monocyte and blood plasma. The Crohn same-target QTL
row has blood-plasma H4 `0.9968008858981062`.

Direction proxy: mixed in MS. Detailed rows include `-0.0`,
`0.16334279819617337`, `0.055526789601966914`,
`-0.055526789601966914`, and `0.2926276148447954`. The direction package is
therefore not target-actionable.

Target-resolution assessment: credible for MS CD58, not credible as a broad
cross-autoimmune target. The Wave104 rank also marks missing
`directional_or_perturbation_support`, `reachable_modality`, and
`prior_or_safety` gates.

Sidecar recommendation: `PARK_MS_GENETICS_ONLY`.

### `IL7R`

MS genetic anchor strength: very strong. Wave62 reports MS max L2G
`0.9447864890098572` at study locus `da961026624084f1518c046f355ad310`
(`rs6881706`), where `IL7R` is L2G rank 1 and `CAPSL` rank 2 at
`0.05462577939033508`.

Cross-autoimmune breadth: strongest in this five-gene set. Wave62 strong L2G
and strong/relevant QTL-coloc diseases are `Crohn;MS;PBC;T1D` (`4`), with
myeloid QTL-coloc disease count `4`. Wave55 broader associated-target genetics
lists `AITD;Crohn;MS;PBC;Psoriasis;SLE;T1D` and score `26.0`. The Wave62 gate
matrix shows all genetics and QTL gates passing, but `no_manual_blocker` is
`False` because of `prior_art_CD127_autoimmune_axis`.

QTL/coloc tissue/cell support: broad and immune-relevant, but not cleanly V3
myeloid-specific. Wave62 summary lists MS-relevant biosamples
`CD14-positive, CD16-negative classical monocyte;CD4-positive, alpha-beta T cell;blood;fibroblast;macrophage`.
Detailed relevant rows show:

- MS: `24` relevant rows, `19` myeloid rows, max H4 `0.9844688660839737`,
  top biosample `CD4-positive, alpha-beta T cell`.
- Crohn: `23` relevant rows, `18` myeloid rows, max H4 `0.979416`, top
  biosample `CD4-positive, alpha-beta T cell`.
- T1D: `21` relevant rows, `14` myeloid rows, max H4 `0.9898081488921829`,
  top biosample `CD14-positive, CD16-negative classical monocyte`.
- PBC: `59` relevant rows, `42` myeloid rows, max H4 `0.9936375660009308`,
  top biosample `macrophage`.

Direction proxy: mixed across diseases and cells. MS includes
`0.11059642134202675`, `-0.11059642134202675`, and `-0.0`; T1D includes
`-0.10710761982213346`, `0.10710761982213346`, and `-0.0`; PBC includes
negative, positive, and zero proxies across loci. This supports comparator use,
not a single intervention direction.

Target-resolution assessment: credible target-resolved genetics, not
locus-level ambiguous in the MS row. The blocker is translational: the local
Wave58-N audit documents CD127/IL7R clinical and patent prior art, and Wave104
flags `prior_or_safety`.

Sidecar recommendation: `NO_GO_V3_PROMOTION`; retain only as
`PARK_COMPARATOR_OR_STRATIFICATION_AXIS`.

## Integrated Decision

The genetics/coloc sidecar agrees with Wave104's branch call:
`NO_PROMOTABLE_TARGET_BUT_DISPATCH_GENETICS_STATE_SIDECARS`.

Use these genes as follows:

- `IL7R`: positive-control target-resolved autoimmune genetics with strong
  prior-art saturation.
- `SP140`: positive-control chromatin/genotype-stratification comparator with
  direction conflict.
- `IFI30`: MS APC/lysosomal target-resolution benchmark, not a direct target.
- `GALC`: lipid/lysosomal locus to keep only for direction and locus-resolution
  review.
- `CD58`: MS genetics comparator for costimulatory/adhesion biology, not a V3
  therapeutic nomination.

No row should be advanced to `FINDING_V3` from this sidecar.
