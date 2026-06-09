# Joint Inference V41

Status: **value-complete corpus-level joint inference pass**.

V41 built one integrated evidence frame across committed project results and
ran a conservative multi-view aggregation. The held-out split was written before
fitting and holds out `treatment_response`, the clinically most important
modality.

## Integrated Frame

- Evidence rows: `985`.
- Unique entities: `71`.
- Modalities represented: `14`.
- P-valued evidence rows: `907`.
- Joint-model matrix rows: `229` entity-by-modality summaries.

Coverage:

| modality | rows | entities | p_valued_rows |
| --- | --- | --- | --- |
| cell_state_h5ad | 149 | 41 | 149 |
| cross_disease_summary | 149 | 41 | 112 |
| treatment_pharmacodynamic | 149 | 41 | 149 |
| treatment_response | 114 | 10 | 108 |
| deep_structure | 90 | 13 | 90 |
| corpus_synthesis | 63 | 28 | 63 |
| failure_structure | 61 | 29 | 61 |
| treatment_response_tests | 55 | 19 | 55 |
| exploratory | 40 | 12 | 26 |
| perturbation_mixscale | 32 | 13 | 32 |
| perturbation | 26 | 7 | 26 |
| lead_slate | 21 | 13 | 0 |
| network_topology | 21 | 14 | 21 |
| genetics | 15 | 6 | 15 |

The frame joins genetics, deep-structure/module-dependency, perturbation,
network-topology, treatment-response, exploratory, failure-structure, and corpus
synthesis evidence over a shared entity/module/axis vocabulary. Corpus synthesis
and lead-slate rows are retained for recurrence/meta-inference but excluded
from the train-side discovery model to reduce circularity.

## Held-Out Split

- Train modalities: `cell_state_h5ad;cross_disease_summary;deep_structure;exploratory;failure_structure;genetics;network_topology;perturbation;perturbation_mixscale;treatment_pharmacodynamic;treatment_response_tests`.
- Held-out modalities: `treatment_response`.
- Excluded from joint discovery model: `corpus_synthesis;lead_slate`.
- Split file: `analysis/v41_joint_inference/heldout_modality_split.json`.

## Workstream A: Joint Multi-Modality Inference

Method: for each entity, positive p-valued evidence was summarized per modality
as a maximum z-score, then train modalities were combined by Stouffer-style
aggregation. The null permutes support z-scores within each train modality and
records entity-level and family-wise empirical p-values across `10000`
permutations. Treatment-response evidence was then used only as held-out
validation.

Top joint entities:

| entity | train_support_modalities | train_joint_z | train_empirical_fwer_p | train_joint_q_bh | holdout_support_z | holdout_supported_p_lt_0_05 |
| --- | --- | --- | --- | --- | --- | --- |
| apc_hla_ifn_monitoring | 8 | 8.054844913966898 | 0.0683931606839316 | 2.6659180916293066e-14 | 5.000961463621753 | True |
| apc_axis | 8 | 7.773585031963566 | 0.18698130186981302 | 1.277947896518686e-13 | 2.324857177760912 | True |
| hla_ii_apc | 7 | 7.601908274821308 | 0.3210678932106789 | 3.2583834736482245e-13 | 2.324857177760912 | True |
| genetic_backdrop_ms_uc | 1 | 7.535167067614062 | 0.7115288471152885 | 3.2676570000000113e-13 | 0.0 | False |
| ms_uc_genetic_backdrop | 1 | 7.535167067614062 | 0.7115288471152885 | 3.2676570000000113e-13 | 0.0 | False |
| coupled_apc_axis | 7 | 7.487342430479729 | 0.7776222377762224 | 3.363503484393806e-13 | 2.324857177760912 | True |
| mif_cd74_receptor_state | 7 | 7.487342430479729 | 0.7776222377762224 | 3.363503484393806e-13 | 2.324857177760912 | True |
| ifn_apc | 7 | 7.154916583327206 | 0.926907309269073 | 3.505934879948442e-12 | 2.0329343228866392 | True |
| hla_ii_apc__mif_cd74_receptor_state | 4 | 5.992856382807678 | 1.0 | 7.674735789717005e-09 | 0.0 | False |
| mixscale_validated_ifng_readout | 5 | 5.6410936604953115 | 1.0 | 5.6606092120155985e-08 | 0.0 | False |
| lysosomal_apc | 5 | 5.266123250414903 | 1.0 | 4.243376720867788e-07 | 0.0 | False |
| ifn_apc__mixscale_validated_ifng_readout | 3 | 4.72193468757868 | 1.0 | 6.521660184302918e-06 | 0.0 | False |
| ifn_apc__lysosomal_apc | 3 | 4.290181664612609 | 1.0 | 4.600504006355015e-05 | 0.0 | False |
| ifn_apc__mif_cd74_receptor_state | 3 | 4.048969439950566 | 1.0 | 0.0001230973316324698 | 0.0 | False |
| hla_ii_apc__ifn_apc | 2 | 4.006737781595028 | 1.0 | 0.00013749102350006184 | 0.0 | False |

Permutation/null summary:

- Observed max train joint z: `8.0548`.
- Null max-z 95th percentile: `8.1547`.
- Null max-z 99th percentile: `8.4876`.
- Train entities passing FWER < 0.10:
  `apc_hla_ifn_monitoring`.

Held-out treatment-response validation of the BH/FWER-selected train-side top
set. Only `apc_hla_ifn_monitoring` passes the stricter train-side family-wise
permutation gate; the larger table below is used only as a rank-enrichment
check:

| gate | universe_entities | holdout_supported_entities | top_entities | top_holdout_supported | hypergeom_p_top_enrichment | spearman_train_z_vs_holdout_z | spearman_p |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bh_or_fwer_train_signal | 67 | 10 | 26 | 8 | 0.0057036859875542936 | 0.402980143899722 | 0.000722111258658304 |

Verdict: joint inference **recovers the already-known APC/HLA/IFN/coupled-axis
structure**, but it does not surface a new non-APC, held-out-validated signal.
The result is useful because the known APC-axis signal survives a stricter
cross-modality gate, but it is not a new target, not a successor rule, and not
an intervention-grade discovery.

## Workstream B: Evidence-Structure Meta-Inference

The recurrence analysis treats each positive source/evidence row as a corpus
observation and tests whether entities recur across independent source units
more often than expected under source-preserving random reassignment.

Top recurrent entities:

| entity | positive_source_units | positive_modalities | recurrence_empirical_fwer_p | recurrence_q_bh | train_joint_z | holdout_support_z | holdout_supported_p_lt_0_05 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| apc_hla_ifn_monitoring | 78 | 11 | 9.999000099990002e-05 | 0.0006166050061660501 | 8.054844913966898 | 5.000961463621753 | True |
| apc_axis | 45 | 12 | 9.999000099990002e-05 | 0.0006166050061660501 | 7.773585031963566 | 2.324857177760912 | True |
| ifn_apc | 21 | 11 | 9.999000099990002e-05 | 0.0006166050061660501 | 7.154916583327206 | 2.0329343228866392 | True |
| hla_ii_apc | 20 | 11 | 9.999000099990002e-05 | 0.0006166050061660501 | 7.601908274821308 | 2.324857177760912 | True |
| coupled_apc_axis | 18 | 10 | 9.999000099990002e-05 | 0.0006166050061660501 | 7.487342430479729 | 2.324857177760912 | True |
| mif_cd74_receptor_state | 16 | 9 | 0.0008999100089991 | 0.0006166050061660501 | 7.487342430479729 | 2.324857177760912 | True |
| lysosomal_apc | 13 | 7 | 0.0382961703829617 | 0.002114074306855029 | 5.266123250414903 | 0.0 | False |
| metabolic_sterol | 13 | 4 | 0.0382961703829617 | 0.0036996300369963007 | 3.5979862551011634 | 3.4808903002570455 | True |
| mixscale_validated_ifng_readout | 12 | 5 | 0.12438756124387561 | 0.0078103300781033015 | 5.6410936604953115 | 0.0 | False |
| tb_readable_compartment | 9 | 3 | 0.9577042295770423 | 0.1428057194280572 | 2.6547590333403277 | 2.483947308581782 | True |
| layer_transfer_map | 8 | 3 | 1.0 | 0.24901356018244328 | 0.0 | 0.0 | False |
| cell_composition | 8 | 2 | 1.0 | 0.24901356018244328 | 0.0 | 3.0903807621810726 | True |
| genetic_backdrop_ms_uc | 8 | 2 | 1.0 | 0.24901356018244328 | 7.535167067614062 | 0.0 | False |
| complement_lipid_axis | 5 | 4 | 1.0 | 0.9918008199180082 | 3.6262044667180313 | 0.0 | False |
| hla_ii_apc__mif_cd74_receptor_state | 4 | 4 | 1.0 | 0.9918008199180082 | 5.992856382807678 | 0.0 | False |

Recurring-signal null:

- Positive source units: `104`.
- Entities in recurrence universe: `71`.
- Observed top recurrence: `78`.
- Null 95th percentile of max recurrence:
  `12.000`.
- Formal recurrent entities at FWER < 0.10:
  `apc_hla_ifn_monitoring;apc_axis;ifn_apc;hla_ii_apc;coupled_apc_axis;mif_cd74_receptor_state;lysosomal_apc;metabolic_sterol`.

The recurring entities are dominated by APC-axis and treatment-response terms.
`metabolic_sterol` also passes recurrence plus held-out support, but this is a
known immune-tone/confounder/context axis from V32/V35/V39 rather than a new
target or biomarker. No unexpected non-context entity passed both the recurrence
gate and held-out treatment-response validation.

## Quantitative Exhaustion Bound

Unexpected/new-signal entities tested against the recurrence-plus-held-out gate
after excluding known APC, metabolic/immune-tone, composition/steroid, genetic
backdrop, layer-transfer, and protective-resilience context entities:
`22`.

Known context entities passing recurrence FWER < 0.10 and held-out
treatment-response support: `apc_hla_ifn_monitoring;apc_axis;ifn_apc;hla_ii_apc;coupled_apc_axis;mif_cd74_receptor_state;metabolic_sterol`.

Unexpected entities passing recurrence FWER < 0.10 and held-out
treatment-response support: `0`.

With zero successes among those unexpected candidates, the simple zero-success
95% upper bound on the fraction of such entities that could still hide a
joint-validated signal in this held corpus is
`0.127`.
This bound is not a biological universal; it is a corpus-level computational
bound for the entity vocabulary and evidence rows assembled here.

## Exhaustion Verdict

Verdict: **exhausted for unexpected new public-data discovery under this corpus-level gate**.

The held public corpus supports two repeatable structures: the bounded
APC/HLA-II/IFN/MIF-CD74/IFNG-readout monitoring axis, and the already-known
metabolic/immune-tone context that conditions that axis. V41 does not find an
additional unexpected joint signal that was invisible to per-dimension analyses.
The rational next step is therefore not more unconstrained public-data mining
for new targets. It is external data: the Gafson/DMF NEDA-labeled cohort for
the locked V22 scalar, plus any future genotype-linked immune/CSF/protein data
needed for genetics questions.

## Workstream D: RPT Joint Structural Pass

SAP RPT ran on `analysis/v41_joint_inference/v41_rpt_joint_payload.json` and returned `19` predictions. Prediction class counts: `known_context`=9, `not_validated`=10. Example predictions: genetic_backdrop_ms_uc -> known_context (0.62); ms_uc_genetic_backdrop -> not_validated (1.0); hla_ii_apc__mif_cd74_receptor_state -> not_validated (0.51); ifn_apc__mixscale_validated_ifng_readout -> known_context (0.61); ifn_apc__lysosomal_apc -> known_context (0.6); ifn_apc__mif_cd74_receptor_state -> known_context (0.6); hla_ii_apc__ifn_apc -> not_validated (0.59); hla_ii_apc__mixscale_validated_ifng_readout -> not_validated (0.59). RPT output is treated only as a proposal/ranking lens and did not change the evidence verdict.

## Single Most Defensible Next Step

Acquire Gafson et al. 2018 DMF PBMC RNA-seq processed counts plus sample-level
NEDA-4 labels and run the frozen V22 validation harness with V32/V36/V38/V39/V41
secondary audits. Do not fit a successor rule on that cohort.
