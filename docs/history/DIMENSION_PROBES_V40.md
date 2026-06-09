# Dimension Probes V40

Status: **value-complete after two grounded probes**.

This report follows `meta/DIMENSION_SCOUT_V40.md`. It probes new computational
dimensions quickly and conservatively. No locked rule was edited, no fresh
validation cohort was read, and no model output is treated as evidence.

## Probe 1: Protective / Resilience-Direction Genetics

Prediction: reorienting held genetics around protective/resilience direction
will reveal at least one right-direction, tractable target candidate.

Grounding artifacts:

- Script: `scripts/v40_dimension_probes.py`
- Input: `analysis/v39_failure_structure_exclusion/v39_failure_catalogue.tsv`
- Output:
  `analysis/v40_dimension_probes/protective_resilience_genetics_probe.tsv`

Result:

- Genetics-or-target-like rows tested: `8`.
- Target-nomination-like rows tested: `6`.
- Right-direction tractable targets found: `0`.
- 95% upper bound with zero successes in genetics/target-like rows:
  `0.312`.
- 95% upper bound with zero successes in target-like rows:
  `0.393`.

Class breakdown:

| class | count |
| --- | --- |
| opposite_or_invalid_cross_disease_direction | 2 |
| protective_direction_requires_hard_restoration_or_agonism | 2 |
| not_shared_causal_signal | 2 |
| marker_or_covariate_not_target | 1 |
| direction_or_coloc_unresolved | 1 |

Verdict: **not supported in the held frame**. The dimension remains conceptually
valuable because it asks a different question than risk-first genetics, but the
held project genetics do not contain an intervention-ready protective target.
The probe mostly recovers V39 failure modes: opposite transfer direction, hard
restoration/agonism, signal conflict, failed coloc, or unresolved QTL direction.

Future dedicated run: only worthwhile after richer full-summary QTL/drug-target
MR instruments or controlled genotype-linked immune/CSF expression arrive.

## Probe 2: APC-Axis Network Topology / Controllability

Prediction: the V26 APC-axis module dependency graph has a non-random central
hub among supported cross-modality dependency edges.

Grounding artifacts:

- Script: `scripts/v40_dimension_probes.py`
- Input: `analysis/v26_deep_structure/workstream_b_module_dependencies.tsv`
- Output: `analysis/v40_dimension_probes/apc_network_topology_probe.tsv`

Method:

Supported dependency edges from V26 were converted into an undirected module
graph. The null preserves each modality's number of supported edges and samples
random edges among modules observed in that modality (`10000`
permutations). This tests topology only, not causality.

Result:

| module | observed_supported_edge_degree | null_mean_degree | empirical_p_degree_ge_observed | bh_q |
| --- | --- | --- | --- | --- |
| ifn_apc | 11 | 7.6057 | 0.0654934506549345 | 0.27117288271172885 |
| hla_ii_apc | 10 | 7.6172 | 0.15778422157784222 | 0.355014498550145 |
| mixscale_validated_ifng_readout | 9 | 4.4901 | 0.006999300069993001 | 0.062993700629937 |
| lysosomal_apc | 9 | 6.1223 | 0.0903909609039096 | 0.27117288271172885 |
| mif_cd74_receptor_state | 9 | 7.6013 | 0.31056894310568944 | 0.559024097590241 |
| lipid_loader_repair | 2 | 6.0856 | 0.9965003499650035 | 1.0 |
| complement_phagocytosis | 0 | 4.4802 | 1.0 | 1.0 |
| gilt_lysosomal_apc | 0 | 1.507 | 1.0 | 1.0 |
| hif_nampt_metabolic | 0 | 4.4906 | 1.0 | 1.0 |

Verdict: **supported_as_readout_topology_signal**. The corrected signal is not a
clean controllability result: the only module with BH q < 0.10 is
`mixscale_validated_ifng_readout`. `ifn_apc` has the highest raw degree but does
not survive correction, and `hla_ii_apc` also does not survive correction.
This supports a dedicated mechanism-mapping dimension, not target nomination.

## Ranked New-Dimension Shortlist After Grounding

| Rank | Dimension | Grounded outcome | Dedicated-run priority | Reason |
|---:|---|---|---|---|
| 1 | APC-axis network topology / mechanism mapping | supported_as_readout_topology_signal | Medium-high | Orthogonal to scalar biomarkers; grounded on V26 network with permutation null, but the corrected hub is a readout rather than a target. |
| 2 | Protective/resilience-direction genetics | not_supported_in_held_frame | Low until new data | Conceptually important, but no right-direction tractable target emerges from held genetics. |
| 3 | Cell-cell interaction / niche communication | not yet probed | Medium | High novelty and held h5ad data, but requires dedicated LR pipeline and composition controls. |
| 4 | Perturbation causal-discovery / module direction | partially covered by topology probe | Medium | Feasible on held perturbation matrices; needs stricter directed-perturbation assumptions before claims. |
| 5 | Microbiome/metabolome-host immune-tone join | not yet probed | Low-medium | Held data exist, but cross-cohort comparability and V39 context-dependence risk are high. |

## Bottom Line

V40's first grounded probes did not produce a new therapeutic lead. The
protective/resilience genetics dimension is mostly blocked by the same
direction/modality and evidence-resolution constraints V39 identified. The
network-topology dimension is the more promising computational angle, but the
correction-surviving signal is a validated IFNG readout hub rather than a
druggable APC control node. It should be pursued as mechanism mapping, not
target nomination.
