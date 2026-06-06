# Deep Structure V26

Date: 2026-06-07

## Scope

V26 tested whether the project's held data contain a deeper module-level structure that was missed by prior single-locus and single-modality analyses. The analysis used existing summarized artifacts only; no new datasets were fetched and no OpenGWAS analysis was run beyond token verification.

The executable analysis is `scripts/v26_deep_structure_analysis.py`. Outputs are under `analysis/v26_deep_structure/`.

Fixed seed: `26026`.

Permutation count: 2,000 per null test.

## Modality Inventory

All required V26 artifacts were present. The modality manifest with checksums is:

`analysis/v26_deep_structure/modality_manifest_v26.tsv`

Usable module-level matrices:

| Matrix | Rows | Modules |
|---|---:|---:|
| perturbation Mixscale | 24 | 4 |
| treatment pharmacodynamics | 24 | 8 |
| treatment response tests | 20 | 5 |
| cross-disease h5ad cell-state comparisons | 12 | 8 |
| cross-disease module summary | 6 | 8 |

Genetics/eQTL artifacts were inventoried and retained for interpretation, but not forced into the module latent-factor test because the current held summaries do not provide a dense shared module representation for genetics/eQTL. This is a limitation, not a reason to fabricate a cross-modal axis.

## Workstream A: Cross-Modal Shared Latent Structure

Method: for each modality matrix, rows were contexts and columns were shared modules. Rows were z-scored and the first right singular vector was treated as the first module-loading axis. Pairwise cross-modality similarity used cosine similarity between module loadings. Null testing permuted module labels 2,000 times; BH correction was applied across tested modality pairs.

Supported pairings:

| Modality A | Modality B | Shared Modules | Cosine | Permutation p | BH q | Grade |
|---|---|---:|---:|---:|---:|---|
| treatment pharmacodynamic | cell-state h5ad | 8 | 0.934 | 0.0010 | 0.0100 | supported |
| cell-state h5ad | cross-disease summary | 8 | 0.879 | 0.0035 | 0.0175 | supported |

Top loadings on the supported pharmacodynamic/cell-state axis:

- Positive: `ifn_apc`, `hla_ii_apc`, `mif_cd74_receptor_state`, `mixscale_validated_ifng_readout`.
- Negative: `complement_phagocytosis`, `lipid_loader_repair`, `lysosomal_apc`.

Interpretation: the held data support a recurrent **immune-remodeling / antigen-presentation module axis** linking cross-disease cell-state differences and treatment pharmacodynamic movement. This is not a full all-modality factor: perturbation Mixscale and response-outcome tests did not pass the shared-latent-axis gate against the other modalities.

Unsupported pairings are retained in `workstream_a_latent_axes.tsv`; notably perturbation-vs-treatment and treatment-response-vs-pharmacodynamic axes did not survive the V26 null gate.

## Workstream B: Higher-Order Module Dependency Structure

Method: within each modality matrix, all module pairs were tested by Spearman correlation across contexts, with 2,000 row-permutation nulls and BH correction within modality. A dependency was called supported only if it was significant or near-significant after correction and replicated with the same sign in at least two modalities.

Supported replicated dependencies:

| Module A | Module B | Replicated Modalities | Median r | Minimum q |
|---|---|---:|---:|---:|
| `hla_ii_apc` | `mif_cd74_receptor_state` | 4 | 0.853 | 0.0015 |
| `ifn_apc` | `mixscale_validated_ifng_readout` | 3 | 0.962 | 0.0020 |
| `ifn_apc` | `lysosomal_apc` | 3 | 0.899 | 0.0025 |
| `ifn_apc` | `mif_cd74_receptor_state` | 3 | 0.529 | 0.0082 |
| `hla_ii_apc` | `ifn_apc` | 2 | 0.711 | 0.0020 |
| `hla_ii_apc` | `mixscale_validated_ifng_readout` | 2 | 0.909 | 0.0020 |
| `mif_cd74_receptor_state` | `mixscale_validated_ifng_readout` | 2 | 0.803 | 0.0031 |
| `lysosomal_apc` | `mixscale_validated_ifng_readout` | 2 | 0.622 | 0.0330 |
| `hla_ii_apc` | `lysosomal_apc` | 2 | 0.653 | 0.0406 |
| `lipid_loader_repair` | `lysosomal_apc` | 2 | 0.469 | 0.0412 |

Interpretation: the strongest higher-order result is not an isolated IFN/APC feature. It is a coupled APC architecture linking HLA-II, MIF/CD74 receptor-state, IFN readout, and lysosomal processing. This supports the V22/V23 monitoring interpretation: the response signal is likely a coordinated remodeling state, not one gene or one module alone.

## Workstream C: Invariant / Negative-Space Analysis

Method: supported or near-supported module-pair correlations were tested for sign consistency across modalities. The null model randomly flipped signs 2,000 times, and BH correction was applied.

Result: **zero load-bearing invariants passed the V26 invariant gate.**

Closest but unsupported examples:

| Module A | Module B | Modalities | Sign Consistency | Median abs r | Active Modalities | q | Grade |
|---|---|---:|---:|---:|---:|---:|---|
| `hla_ii_apc` | `ifn_apc` | 4 | 1.00 | 0.556 | 4 | 0.340 | not supported |
| `hla_ii_apc` | `mif_cd74_receptor_state` | 4 | 1.00 | 0.853 | 4 | 0.340 | not supported |
| `ifn_apc` | `lysosomal_apc` | 4 | 1.00 | 0.736 | 4 | 0.340 | not supported |
| `ifn_apc` | `mif_cd74_receptor_state` | 4 | 1.00 | 0.551 | 4 | 0.340 | not supported |

Interpretation: the signs are visually consistent, but with only 3-4 modality observations the sign-flip null is discrete and underpowered. V26 therefore cannot claim a conserved invariant. It can claim replicated module dependency where the permutation and replication gates passed.

## Workstream D: Re-Reading Stalled Leads

| Lead | V26 Status | Interpretation |
|---|---|---|
| bounded APC/HLA-II monitoring | strengthened as monitoring structure | IFN/APC-HLA-II-MIF/CD74 coupling survives replicated dependency testing. It remains an early monitoring signal, not a validated baseline stratifier. |
| chr1/KIF21B | unchanged hard target | Deep module analysis does not alter V19: KIF21B remains causal-favored and wrong-direction for tractable inhibition. |
| GPR25 | unchanged unsupported causal gene | No held module-level data provide new GPR25 causal expression/QTL support; still requires genotype-linked cell/protein data. |
| ZMIZ1 | unchanged decoupling | V26 does not reverse the allele-aligned opposite-direction MS/Crohn decoupling finding. |
| PTGER4 | remains closed | No V26 structure rescues the mixed/distinct signal. |

## Best Structurally Grounded Hypothesis

Supported hypothesis:

**The most reproducible deep structure in the held data is a coordinated APC remodeling architecture coupling HLA-II, IFN/APC, MIF/CD74 receptor-state, IFN-response readout, and lysosomal processing. The clinical implication is measurement of coupled early on-treatment movement, not isolated baseline level or single-gene targeting.**

Evidence:

- Supported latent-axis replication between treatment pharmacodynamics and cell-state h5ad summaries (cosine 0.934, BH q 0.010).
- Supported latent-axis replication between cell-state h5ad and cross-disease summary (cosine 0.879, BH q 0.017).
- Replicated module dependencies across multiple modalities, strongest for `hla_ii_apc` with `mif_cd74_receptor_state` across four modalities.

Limitations:

- No perturbation-to-treatment shared latent axis passed the V26 null gate.
- No load-bearing invariant passed BH correction.
- Genetics/eQTL summaries are not dense enough in module space for a true all-modality factor.
- This is not a cure-class target finding. It is a bounded, structurally supported monitoring-mechanism hypothesis.

## Falsification Path

1. In a fresh paired-treatment cohort, measure early module deltas for HLA-II, IFN/APC, MIF/CD74 receptor-state, IFN readout, and lysosomal APC.
2. Test whether the coupled-axis score predicts response better than any single module and better than the V22 locked scalar alone.
3. In APC/T/B compartment-resolved perturbation data, perturb HLA-II/MIF-CD74/IFN regulators and test whether the coupled modules move coherently.
4. Reject the hypothesis if the coupled-axis score fails to outperform single-module baselines in a fresh cohort, or if perturbation breaks the predicted coupling.

## Verdict

V26 found a **supported shared APC remodeling structure**, but not a broad validated immune simulator and not a load-bearing invariant. The prior treatment-response lead is strengthened mechanistically as a coupled early-monitoring signal. The stalled genetics targets remain unchanged.
