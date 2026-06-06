# Milestone 1 - Hour 2

Timestamp: 2026-05-26 20:41 UTC

## Milestone Requirements

Requirement status:

- Disease-specialist subagents returned first-pass module characterization for
  at least six diseases: met. Returned/preserved reports cover MS context plus
  rheumatoid arthritis, systemic lupus/lupus nephritis, Crohn disease,
  ulcerative colitis, psoriasis, Sjogren syndrome, autoimmune thyroid disease,
  type 1 diabetes, myasthenia gravis, ankylosing spondylitis/psoriatic
  arthritis, celiac disease, and primary biliary cholangitis.
- Foundation-model environment provisioned: partially met. `arc-state` and
  `arc-stack` are installed in `.venv_v3_py312`; State CLI runs. Evo 2 local
  inference is blocked by macOS CPU/no CUDA/no hosted credentials. State
  released CD14 prediction/real outputs were analyzed feature-agnostically, but
  gene-specific State module scoring remains blocked by missing HVG
  feature-to-gene mapping unless the 9.1 GB AnnData completes.
- First convergence map produced: met. Current map uses disease-specialist
  evidence, OpenTargets evidence, MS lesion/microglia data, Mixscale CRISPRi
  perturb-seq, L1000FWD reversal, and direct h5ad donor-level validation in
  gut, skin, and salivary gland.

## First Convergence Map

The old V2 phrase "lipid-lysosomal myeloid module" is now too broad. The
convergent signal is sharper:

`IFNG -> IFNGR1/IFNGR2 -> JAK1/JAK2 -> STAT1 -> CIITA/NLRC5/RFX5 -> HLA-II/CD74 + IFI30/CTSS/TAP/B2M antigen-processing state`

The central object is therefore an IFN-gamma-licensed antigen-processing/APC
transition. It can appear in myeloid cells, epithelial cells, and tissue APC
compartments depending on disease and tissue.

Axis-level breadth from `phases/v3/results/disease_axis_convergence_rank.tsv`:

- `ifn_apc`: weighted score 21.8, strong in 12 disease contexts, supportive in
  14, no weak/contradictory disease calls.
- `lysosomal_apc`: weighted score 18.3, strong in 8, supportive in 14, no
  weak/contradictory disease calls.
- `hif_nampt_metabolic`: weighted score 11.9, strong in 3, but weak or
  contradictory in 3.
- `complement_phagocytosis`: weighted score 10.2, strong in 3, weak or
  contradictory in 5.
- `lipid_loader_repair`: weighted score 5.7, strong in 1 and weak or
  contradictory in 9.

Interpretation: the primary track is no longer generic lipid loading, ACSL1, or
NAMPT. It is the IFN/APC plus lysosomal antigen-processing transition.

## Modality Agreement

Expression and cell-state evidence:

- MS sorted microglia (`GSE111972`) show increased `CD74/CD44/CXCR4/HLA-II`
  receptor/APC state in MS white matter versus control white matter
  (delta=0.614, Hedges g=1.341, p=0.00547, FDR=0.0192), while the MIF ligand
  axis is not significant.
- IBD direct h5ad validation reproduces IFN/APC and Mixscale-validated
  IFN-gamma readouts in Crohn and UC colon myeloid cells, with strongest UC
  myeloid Mixscale-readout effect delta=0.443, Hedges g=3.271, p=0.000116,
  FDR=0.00928 after the expanded direct-h5ad run.
- Psoriasis direct h5ad validation supports the skin APC IFN/APC state
  (delta=0.449, Hedges g=2.817, p=0.0197, FDR=0.0591 after the expanded
  multi-analysis run).
- Sjogren direct h5ad validation supports epithelial HLA-II/CD74 state
  (HLA-II/APC mean-score delta=0.204, Hedges g=1.034, p=0.0206, FDR=0.0591;
  `CD74/CD44/CXCR4/HLA-II` mean-score delta=0.207, Hedges g=1.075,
  p=0.0207, FDR=0.0591).

Perturbation evidence:

- Mixscale CRISPRi under IFN-gamma stimulation shows that perturbing
  `IFNGR1`, `IFNGR2`, `JAK1`, `JAK2`, and `STAT1` suppresses the IFN/APC and
  HLA-II/CD74/lysosomal readouts across six cell lines.
- `IFNGR1` knockdown: `ifn_apc` mean module log2FC=-1.492, `hla_ii_apc`=-1.605,
  `gilt_lysosomal_apc`=-0.266, `mif_cd74_receptor_state`=-0.534.
- Gene-level `IFNGR1` knockdown lowers `CD74`, `CIITA`, `CTSS`, `IFI30`, `B2M`,
  `TAP1`, `GBP1`, and `CXCL10`.
- `RFX5` is narrower: it reduces HLA-II/CD74 but not the broad IFN/APC state.

Genetics:

- Genetics subagent evidence supports `IFI30` in MS and `IRF1` in
  IBD/psoriasis, with broad but complex HLA-II/MHC anchoring.
- This is enough to keep the IFN/APC transition as a genetics-compatible
  mechanism, but it is not yet enough to claim a single non-MHC gene has clean
  genetic anchoring across four autoimmune diseases.

Drug-response and prior-art:

- L1000FWD does not nominate a clean generic disease-signature reversal drug.
  Curated module reversals are significant but dominated by broad stress or
  oncology probes, so they are not translational leads.
- CD74/MIF/ibudilast as a broad progressive MS therapeutic claim is blocked by
  prior art. It survives only as a possible stratification biomarker axis.
- CTSS is druggable but heavily prior-arted and clinically underwhelming in
  related autoimmune trials.

## Agreement And Disagreement

Tracks agree on:

- IFN/APC is the broadest cross-autoimmune axis.
- The older lipid-loader module is not the pan-autoimmune causal anchor.
- NAMPT/HIF1A is not strong enough as the V3 central node.
- CD74/HLA-II/IFI30/CTSS are better interpreted as downstream antigen-processing
  state readouts/effectors than as independent proof of MIF ligand activation.

Tracks disagree or remain unresolved on:

- Whether the best central node should be the upstream IFNGR/JAK/STAT1 control
  point, the CIITA/RFX5 HLA-II transcriptional gate, or the downstream lysosomal
  effector `IFI30`.
- Whether any intervention point can be novel and selective enough. Direct
  IFN-gamma/JAK blockade is mechanistically obvious but likely prior-arted and
  immunosuppressive. `IFI30` may be more novel but has weaker broad genetics and
  less existing chemical matter.
- Whether the final product should be a new target nomination or a
  pathway-specific stratification biomarker for existing pathway modulators.

## Next Forcing Question

Before Hour 4, rank central-node candidates by convergent evidence and
therapeutic feasibility:

1. `IFNGR1/IFNGR2-JAK1/JAK2-STAT1` upstream control.
2. `CIITA/RFX5/NLRC5` antigen-presentation transcriptional gate.
3. `IFI30/CTSS` lysosomal antigen-processing effector arm.
4. `CD74/HLA-II/CD44/CXCR4` receptor/APC state as stratification biomarker.

The next analysis must separate "central biological controller" from
"tractable intervention point"; they may not be the same molecule.
