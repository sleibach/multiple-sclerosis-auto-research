# Lab Notebook V3

## 2026-05-26 18:41 UTC

Restarted after interruption with the user's V3 specification. The working rule is that exhaustion is unavailable before twelve hours and the only stopping condition during this turn is breakthrough or external interruption.

Key methodological correction from the review: do not satisfy weak surrogates. Bulk expression is allowed for breadth screening only. A target claim needs cell state, genetics, perturbation/model, druggability, prior-art, and mechanistic grounding.

Initial local environment check:

- Python `3.13.3`.
- Available: `numpy`, `pandas`, `scipy`, `statsmodels`.
- Missing initially: `requests`, `Bio`, `scikit-learn`, `anndata`, `scanpy`, `torch`, `transformers`, `huggingface_hub`, `rdkit`, `networkx`.

Immediate interpretation: true State/Stack/Evo 2 model execution may require new installation and possibly Linux/CUDA or hosted access. This is a feasibility gate, not something to assume.

Initial decision: write `REFRAME_V3.md`, `TOOLS_V3.md`, `SUBAGENTS_V3.md`, then dispatch broad subagent wave while locally provisioning tools and building a reusable V3 cross-disease ranking pipeline.

## 2026-05-26 18:51 UTC

Added `PLAN_V3.md` because the run needs predeclared branch logic even though the latest prompt emphasized reframe/tooling/subagents/milestones over a named plan file.

Foundation-model feasibility notes from official sources:

- State: public `ArcInstitute/state`, package `arc-state`, requires Python `>=3.10,<3.13`, includes State Transition (`state tx`) perturbation workflows and State Embedding (`state emb`) workflows.
- Stack: public `ArcInstitute/stack`, package `arc-stack`, tested on Ubuntu/Python 3.10/CUDA/H100 but pip-installable in principle; checkpoints still need to be located.
- Evo 2: public `ArcInstitute/evo2`, but official local requirements are Linux/WSL2, CUDA 12.1+, cuDNN 9.3+, Python 3.11/3.12, and GPU. This macOS ARM CPU environment is not a match; Docker is installed but daemon is not running.

## 2026-05-26 18:52 UTC

Ran `scripts/v3_prioritize_module_nodes.py` on existing evidence. Result: the first-pass axes rank `interferon_chemokine`, `lysosome_antigen_processing`, `complement_phagocytosis`, `metabolic_licensing`, `lipid_droplet_efflux`, `tissue_remodeling`. This is not yet causal, but it supports reformulating the module away from a foamy-lipid core toward an IFN/HIF-licensed lysosomal inflammatory myeloid transition.

Top gene scores: `NAMPT`, `IFI30`, `CXCL10`, `C1QB`, `CTSB`, `SPP1`, `IL1B`, `C1QA`, `TNF`, `MSR1`.

Interpretation decision:

- Keep `NAMPT` as positive comparator because it is broad and druggable, but prior art and NAD toxicity remain blockers.
- Move `IFI30` up because it is repeatedly present in MS, UC, Crohn, lupus nephritis, and psoriasis and is less obviously blocked by prior art.
- Do not claim `IFI30` is an inhibition target yet. Its enzyme function in antigen processing could be protective or pathogenic depending on context; intervention might be upstream (`STAT1/IRF1`, HLA-II/APC transition, antigen-processing state control) or downstream antigen-presentation readout.

Downloaded official State released outputs from `arcinstitute/ST-HVG-Parse`, split 4 CD14 monocyte:

- `data/raw_v3/state_parse_split4/CD14_Mono_pred_de.csv`
- `data/raw_v3/state_parse_split4/CD14_Mono_real_de.csv`
- `data/raw_v3/state_parse_split4/CD14_Mono_agg_results.csv`
- `tmp_v3/var_dims_split4.pkl`
- `tmp_v3/data_module_split4.torch`

These are model-produced prediction files and matched real perturbation files released by Arc. They are not yet a de novo perturbation run, but they can validate model accuracy and test cytokine perturbations relevant to IFN/IL-1/IL-17/TNF/C5a/GM-CSF axes in CD14 monocytes.

## 2026-05-26 18:56 UTC

Important correction: the initial `scripts/v3_analyze_state_parse_cd14.py` version guessed that feature IDs `0..1999` mapped to the first 2,000 entries of `var_dims.pkl["gene_names"]`. That was wrong: candidate genes such as `IFI30`, `NAMPT`, `CXCL10`, and `CTSD` land outside the first 2,000 names, while the DE CSVs only expose numeric feature IDs. The exact HVG feature order appears to require the released `adata_real.h5ad` / `adata_pred.h5ad` files, each `9.1 GB`.

Action taken: block gene-module conclusions from the State released DE files until HVG order is recovered. The script now preserves `FEATURE_n` IDs and records `gene_mapping_status`. Current State output can prove package/model-output availability and benchmark-level prediction existence, but it cannot yet support the biological `IFI30`/`NAMPT` module claim.

This is a proxy-satisficing catch: using the guessed mapping would have produced plausible-looking but invalid module scores.

## 2026-05-26 19:03 UTC

Ran independent MS microglia validation in `GSE111972`, sorted human microglia
RNA-seq from normal-appearing white and grey matter. The analysis uses
log2(DESeq2-normalized count + 1), which is acceptable for validation-scale
contrasts but not a raw-count DESeq2 reanalysis.

Primary contrast: MS white matter microglia vs control white matter microglia,
n=10 vs n=11. Initial run did not include the MIF receptor complex.

Key results:

- Lipid-loader/repair module: delta=0.478 log2 units, Hedges g=1.379,
  Welch p=0.00528, BH FDR=0.0264; adjusted disease beta=0.524, p=0.00117.
- Lysosomal antigen-processing module: delta=0.513, g=0.947, p=0.0413,
  FDR=0.103; adjusted disease beta=0.438, p=0.110.
- IFN/APC module: delta=0.219, g=0.458, p=0.286, FDR=0.477.
- `GPNMB`: delta=1.434, g=1.356, p=0.00491, FDR=0.179; adjusted disease
  beta=1.744, p=0.000592.
- `IFI30`: delta=0.210, g=0.373, p=0.380, FDR=0.563.
- `NAMPT`: delta=-0.214, g=-0.269, p=0.543, FDR=0.725.

Interpretation: GSE111972 supports an MS normal-appearing white-matter
microglial lipid-loader/repair state and gives nominal lysosomal-module support.
It does not support claiming `IFI30` or `NAMPT` as the MS microglia-wide
central node. This forces a stronger compartment distinction: lesion-associated
and cross-disease inflammatory APC states may still use `IFI30`, but MS
normal-appearing microglia are more `GPNMB`/lipid-loader weighted.

Updated the GSE111972 script to include `CD74`, `CD44`, `CXCR4`, `MIF`, and
`DDT`. Re-run result: the `mif_cd74_receptor_state` module
(`CD74/CD44/CXCR4/HLA-II`) is increased in MS white matter microglia with
delta=0.614, Hedges g=1.341, p=0.00547, FDR=0.0192, adjusted disease beta=0.652,
p=0.00872. The `mif_ligand_axis` is not significant (delta=0.286, Hedges
g=0.420, p=0.337, FDR=0.468). Individual
genes: `CD44` delta=1.345, g=0.954, p=0.0332, adjusted p=0.0200; `CXCR4`
adjusted p=0.0447; `DDT` delta=0.350, g=0.743, p=0.092; `CD74` and `MIF`
positive but not significant.

Interpretation correction: the local MS support is for a MIF-responsive
CD74/CD44/CXCR4/HLA-II receptor/APC state, not elevated MIF ligand expression.
This fits a stratification hypothesis for ibudilast/MIF-axis modulation better
than a simple "block overexpressed MIF" claim.

State Parse feature-agnostic validation update: using the released CD14 monocyte
predicted and real DE files without gene mapping, per-perturbation Spearman
correlation across anonymous HVG features is strongest among relevant
perturbations for IFN-gamma (rho=0.479, direction match=0.709, significant
feature recall=0.817), IL-1-alpha (rho=0.421), IFN-alpha1 (rho=0.413), and
GM-CSF (rho=0.387). This supports State's ability to rank broad CD14 monocyte
cytokine responses, but does not yet provide gene-specific `IFI30`/`NAMPT`
perturbation predictions.

Genetics integration: the genetics subagent found candidate-specific support
for `IFI30` in MS and `IRF1` in IBD/psoriasis, with broad HLA-II anchoring but
MHC LD complexity. This resolves a major ambiguity: the central node is not
`NAMPT`, and the original lipid-loader module is not the pan-autoimmune causal
anchor. The working central mechanism is now an IFN/IRF1-licensed HLA-II/GILT
lysosomal antigen-processing APC transition. The intervention point remains
unresolved because qTL colocalization does not define whether to inhibit or
restore `IFI30`.

Intervention integration: CTSS is the cleanest enzymatic handle on lysosomal
MHC-II antigen processing, but it is heavily prior-arted and has negative or
underwhelming clinical history in Sjogren, celiac, RA, and psoriasis-like
contexts. CD74/MIF is less clean mechanistically but has the key translational
advantage: CNS-relevant human progressive MS signal through ibudilast plus
strong APC-state recurrence. Current lead concept is therefore stratification
and mechanism sharpening for CD74/MIF-high progressive MS, not generic
pan-autoimmune CTSS inhibition.

## 2026-05-26 19:30 UTC

Ran `scripts/v3_l1000fwd_reversal.py` against the public L1000FWD API using
three GSE111972-derived signatures: full MS white-matter microglia top-150
up/down genes, a `CD74/CD44/CXCR4/HLA-II` receptor/APC state, and an
IFN/lysosomal APC state. Re-ran after adding CLUE LINCS2020 compound metadata
resolution.

Results:

- Full MS white-matter microglia signature: top opposite hits are not
  significant after L1000FWD q-value correction (top q=0.567). This argues
  against claiming a robust generic drug-reversal signature from the full
  sorted-microglia contrast.
- Curated receptor/APC and IFN/lysosomal module queries produce significant
  opposite signatures, but the top resolved compounds are mostly broad
  stress/toxicity or oncology probes (`thapsigargin`, HSP90 inhibitors,
  tubulin/PLK probes, ATPase/stress-pathway compounds). These are useful as
  perturbational evidence that the module is pharmacologically movable in
  LINCS cell lines, but they are not acceptable translational candidates for
  autoimmune disease.
- The strongest therapeutic inference from L1000FWD is negative: signature
  reversal does not currently nominate a clean CNS-autoimmune repurposing
  agent for the CD74/MIF receptor-state concept. It also warns that small
  curated up-only module queries can look much cleaner than the full disease
  signature and should not drive target selection alone.

Decision: keep L1000FWD as a perturbation-channel sanity check, not as a lead
selection engine. Next priority is gene-specific foundation-model recovery from
State outputs or a defensible alternative model/perturbation dataset.

## 2026-05-26 20:25 UTC

Reproducibility update: patched `run_v3_analysis.sh` so the entry point now runs
the Mixscale perturb-seq analysis and direct h5ad disease-atlas validation when
their raw files are present. The fragile remote CELLxGENE Census expression
query remains opt-in via `RUN_CELLXGENE_CENSUS=1`. Refreshed
`environment/python_v3_freeze.txt` after installing the V3 data/model stack.
Minor execution note: the shell has no `python` command on PATH, so all V3
analysis commands must use `.venv_v3_py312/bin/python` or `PYTHON_BIN`.

Mixscale perturb-seq result: parsed the public Mixscale CRISPRi differential
expression package (`GSE281048` / Zenodo `10.5281/zenodo.14035992`) for
IFN-gamma, IFN-beta, and TNF pathway perturbations. Under IFN-gamma stimulation,
CRISPRi of the receptor/JAK/STAT axis strongly reduces the autoimmune APC
readout across six human cell lines:

- `IFNGR1`: `ifn_apc` mean module log2FC=-1.492 across six cell lines,
  `hla_ii_apc`=-1.605 across four cell lines, `gilt_lysosomal_apc`=-0.266,
  `mif_cd74_receptor_state`=-0.534.
- `IFNGR2`: `ifn_apc`=-1.451, `hla_ii_apc`=-1.546,
  `gilt_lysosomal_apc`=-0.235, `mif_cd74_receptor_state`=-0.515.
- `JAK2`: `ifn_apc`=-1.149, `hla_ii_apc`=-1.251,
  `gilt_lysosomal_apc`=-0.238, `mif_cd74_receptor_state`=-0.449.
- `STAT1`: `ifn_apc`=-1.253, `hla_ii_apc`=-1.107,
  `gilt_lysosomal_apc`=-0.181, `mif_cd74_receptor_state`=-0.282.
- `IRF1` is much weaker (`ifn_apc`=-0.202; `hla_ii_apc`=-0.109), so `IRF1`
  looks more like a genetics/regulatory susceptibility node than the best
  intervention point in this perturbation system.
- `RFX5` specifically reduces the HLA-II/CD74 component (`hla_ii_apc`=-0.706;
  `CD74` mean log2FC=-1.649), but does not suppress the broad IFN/APC module.

Gene-level IFN-gamma effects are mechanistically coherent: `IFNGR1` knockdown
lowers `CD74` by mean log2FC=-1.691, `CIITA`=-1.584, `CTSS`=-1.442,
`IFI30`=-1.335 in the measured cell type, `B2M`=-1.260, `TAP1`=-1.590,
`GBP1`=-1.658, and `CXCL10`=-1.763. The same pattern is directionally repeated
for `IFNGR2`, `JAK1`, `JAK2`, and `STAT1`.

Interpretation: the strongest causal perturbation evidence now supports the
chain `IFNG -> IFNGR1/IFNGR2 -> JAK1/JAK2 -> STAT1 -> CIITA/NLRC5/HLA-II/CD74
+ IFI30/CTSS/TAP/B2M antigen-processing state`. This is a better central
mechanism than the earlier vague lipid-lysosomal module. It is not yet a clean
drug target because direct receptor/JAK/STAT blockade is broad and likely
prior-arted across autoimmunity.

Direct h5ad validation result: analyzed downloaded CZI h5ad atlases for human
IBD colon and psoriasis skin using donor-level module comparisons against
healthy controls. Important replicated signals:

- Crohn colon myeloid cells: `ifn_apc` delta=0.585, Hedges g=2.087,
  p=0.00443, FDR=0.0332; Mixscale-validated IFN-gamma readout delta=0.412,
  g=2.115, p=0.00389, FDR=0.0332.
- UC colon myeloid cells: Mixscale-validated IFN-gamma readout delta=0.443,
  g=3.271, p=0.000116, FDR=0.00696; `ifn_apc` delta=0.485, g=2.359,
  p=0.00130, FDR=0.0259.
- Crohn and UC epithelial compartments also show IFN/APC or CD74/HLA-II
  increases, indicating that the state is not purely myeloid in gut tissue.
- Psoriasis skin APC compartment: `ifn_apc` delta=0.449, g=2.817, p=0.0197,
  FDR=0.0456; Mixscale-validated IFN-gamma readout delta=0.299, g=2.384,
  p=0.0314, FDR=0.0649.

Self-critique: these direct h5ad analyses strengthen cross-tissue replication
but do not by themselves prove causality. The psoriasis donor count is only
three cases and three controls, and canonical HLA genes are incomplete in the
downloaded object, so psoriasis should support the IFN/APC branch rather than a
strong HLA-II-specific claim. The Mixscale perturbation evidence is real
gene-specific CRISPRi, but it comes from stimulated cancer/immortalized cell
lines, not primary autoimmune tissue. Next forcing question: can a third
primary tissue atlas beyond brain, gut, and skin reproduce the same IFN/APC
state, and can the intervention point be made narrower than pan-JAK blockade?

## 2026-05-26 20:29 UTC

Downloaded direct CZI h5ad for Sjogren syndrome labial gland
(`data/raw_v3/cell_state/sjogren_salivary.h5ad`, 94,227 cells, 31,969 genes).
Metadata is usable: disease labels are `normal` and `Sjogren syndrome`, donor
IDs are present, and relevant cell types include acinar/duct epithelial cells,
inflammatory macrophages, alternatively activated macrophages, and dendritic
cells. Added `sjogren_gland_apc` and `sjogren_gland_epithelial` configs to
`scripts/v3_analyze_direct_h5ad_cell_states.py` and re-ran the direct h5ad
analysis.

Sjögren result:

- Salivary gland epithelial compartment (11 Sjogren donors, 14 controls):
  `hla_ii_apc` mean-score delta=0.204, Hedges g=1.034, p=0.0206,
  global FDR=0.0591; `mif_cd74_receptor_state` mean-score delta=0.207,
  g=1.075, p=0.0207, FDR=0.0591; Mixscale-validated IFN-gamma readout
  high-fraction delta=0.137, g=0.924, p=0.0407, FDR=0.0905.
- Salivary gland APC compartment (9 Sjogren donors, 13 controls): positive but
  not globally significant; `mif_cd74_receptor_state` mean-score delta=0.099,
  g=0.747, p=0.0831, FDR=0.1546; `ifn_apc` mean-score delta=0.083,
  g=0.687, p=0.101, FDR=0.184.
- All target module genes are present in the Sjogren object, including
  `STAT1`, `IRF1`, `CXCL10`, `GBP1`, `CD74`, `IFI30`, HLA-II genes, `CIITA`,
  `RFX5`, `CTSS`, `TAP1`, `TAP2`, `B2M`, and `NLRC5`.

Interpretation: Sjogren supports the same antigen-processing receptor/APC state,
but the strongest disease-vs-control recurrence is epithelial rather than
myeloid. This matters mechanistically: the central transition is better stated
as an IFN-gamma-licensed antigen-processing/APC program that appears in
different tissue-resident compartments, not as a strictly myeloid-only state.
This reformulation avoids overfitting the earlier lipid-lysosomal myeloid label.

## 2026-05-26 20:55 UTC

Expanded `scripts/v3_prior_art_intervention_audit.py` to include explicit
`IFNG/IFNGR` and `CIITA/RFX5` branches, then ran it against Europe PMC and
ClinicalTrials.gov. Added `scripts/v3_rank_central_and_intervention_candidates.py`
to rank central biological controllers separately from therapeutic handles.

Ranking result:

- `IFNGR_JAK_STAT1_upstream_control`: highest centrality score (38.876) because
  it explains Mixscale CRISPRi suppression of IFN/APC, HLA-II, CD74, CTSS, and
  IFI30 readouts across IFN-gamma-stimulated cell types. Intervention score is
  penalized by large prior-art/trial burden and low selectivity.
- `CD74_HLAII_receptor_APC_state_biomarker`: second centrality score (31.004),
  but direct CD74/MIF therapeutic use remains prior-art blocked. This looks more
  like a biomarker/state definition than the final intervention.
- `CIITA_RFX5_HLAII_transcriptional_gate`: narrower HLA-II/CD74 gate. `RFX5`
  perturbation reduces HLA-II/CD74 in Mixscale, but broad druggability is poor.
- `IFI30_GILT_lysosomal_feedback_effector`: lower centrality (15.293) but
  competitive intervention score (15.701) because prior-art/trial burden is much
  lower and the protein is an enzyme-like lysosomal effector. Mixscale shows
  upstream IFNGR/JAK/STAT1 perturbations lower `IFI30` strongly, and MS
  OpenTargets evidence gives `IFI30` disease genetic support.
- `CTSS_cathepsinS_lysosomal_effector`: similar biology to `IFI30`, but worse
  translational position because CTSS inhibitors have extensive autoimmune prior
  art and underwhelming clinical history.

Decision: keep IFNGR/JAK/STAT1 as the central biological control axis, but test
whether `IFI30/GILT` can serve as the tractable intervention point. This is a
more defensible pivot than claiming pan-JAK or anti-IFN-gamma as novel.

Self-critique: the IFI30 move may be attractive because it dodges prior art, not
because it is fully validated. The weak points are (1) limited cross-disease
genetic anchoring for IFI30 itself, (2) no direct IFI30 perturb-seq in the
Mixscale branch, and (3) uncertain chemical matter/selectivity. Next tests must
attack those points rather than polishing the IFI30 story.

## 2026-05-26 21:03 UTC

Added and ran `scripts/v3_analyze_direct_h5ad_gene_replication.py`, a
donor-level target-gene analysis across the same direct h5ad atlases. This was
needed because module recurrence can hide whether `IFI30` itself is actually
recurring.

Key individual-gene results:

- `IFI30` is not a clean direct-h5ad pan-autoimmune expression hit. It is
  positive in UC myeloid cells (delta=0.765, Hedges g=1.402, p=0.0365) and
  directionally positive in Crohn myeloid/psoriasis compartments, but null or
  negative in Sjogren and UC epithelial compartments; global FDR across the
  target-gene screen is not significant.
- `CD74` is more recurrent at the individual-gene level: positive in Crohn
  epithelial, UC epithelial, psoriasis APC/keratinocyte, Sjogren epithelial,
  and other compartments; strongest Sjogren epithelial p=0.00173 before global
  target-gene FDR.
- `CTSS` is strongest in IBD myeloid compartments: UC myeloid delta=0.584,
  Hedges g=2.286, p=0.00179; Crohn myeloid delta=0.374, g=1.541, p=0.0182.
- `STAT1`, `IRF1`, `TAP1/TAP2`, `B2M`, `NLRC5`, and HLA-II genes show more
  consistent directional support for the broader IFN/APC transition than
  `IFI30` alone.

External mechanistic literature checkpoint:

- Verified foundational GILT biology: IFI30/GILT is an IFN-gamma-inducible
  lysosomal thiol reductase active at acidic pH and involved in MHC-II antigen
  processing of disulfide-containing antigens.
- Verified EAE caution: GILT deficiency in MOG-induced EAE changes pathogenic
  mechanism rather than simply abolishing disease; GILT knockout mice are
  relatively resistant to MOG35-55 peptide EAE but can be susceptible to whole
  MOG protein EAE with antibody/plasma-cell involvement. This is a serious
  failure mode for therapeutic IFI30 inhibition.
- Verified oncology cross-domain lead: a 2026 melanoma paper reports that
  IFI30 depletion can reduce IFNGR1, HLA-DR, and PD-L1 under IFN-gamma
  stimulation by promoting lysosomal degradation. This supports the idea that
  IFI30 may participate in a positive feedback loop sustaining IFN-gamma/HLA
  state, but it is tumor-cell evidence, not autoimmune tissue validation.

Decision: do not promote `IFI30` alone yet. The stronger current claim is a
central IFN-gamma/HLA-II antigen-processing transition with `IFI30` as one
candidate feedback effector. The lead therapeutic handle remains unresolved
between (a) IFI30/GILT if structural/druggability and disease specificity can be
strengthened, (b) CTSS if prior-art/clinical failures can be stratified around,
or (c) a CD74/HLA-II/IFI30/CTSS biomarker that selects for existing IFN/JAK or
antigen-processing modulators.

## 2026-05-26 21:01 UTC

Added and ran `scripts/v3_druggability_audit.py` using UniProt, AlphaFold DB,
and ChEMBL. UniProt live lookup initially had DNS trouble but the rerun
succeeded; reviewed accessions are preserved in the output.

Druggability result:

- `IFI30` / GILT: UniProt reviewed accession `P13284`; AlphaFold model
  downloaded with mean pLDDT=83.23 and median pLDDT=97.25, but 26.8% of
  residues have pLDDT<70, likely reflecting flexible propeptide/terminal
  regions. UniProt annotates a redox-active disulfide feature at residues
  72-75, consistent with a CXXC-like catalytic motif. ChEMBL target search
  returned no IFI30 activity summary rows, so there is no obvious existing
  medicinal chemistry package.
- `CTSS`: reviewed accession `P25774`; AlphaFold mean pLDDT=94.30; ChEMBL has
  dense human Cathepsin S activity data (1,000 returned records, 896 unique
  molecules, best returned standard value 0.1 nM, median 188 nM). This confirms
  tractability but also reinforces prior-art crowding.
- `CTSL`, `CTSB`, and `CTSD` all have dense activity data, confirming the
  selectivity problem for cathepsin-family intervention.
- `JAK1`/`JAK2` have dense chemical matter and high-confidence structures, but
  this is expected and does not help novelty/selectivity.
- `CIITA` and `RFX5`: structures are low-confidence or partly disordered
  (CIITA mean pLDDT=68.75; RFX5 mean pLDDT=57.13, 70.6% residues <70) and
  ChEMBL returned no tractable target rows. This weakens direct small-molecule
  targeting of the transcriptional HLA-II gate.

Decision update: IFI30 is not repurposing-ready. If it remains in the final
claim, it should be framed as a target-discovery nomination requiring assay and
chemical-matter generation. CTSS is ready-to-drug but not novel. The likely
translational contribution may need to combine a state biomarker with an
existing broad pathway drug, or nominate IFI30 only as a longer-horizon,
selectivity-seeking target.

## 2026-05-26 21:03 UTC

Added `scripts/v3_model_ifng_apc_feedback.py`, an explicit ODE sensitivity
model for the IFN-gamma/HLA-II/GILT antigen-processing transition. Variables:
effective IFNGR availability, JAK/STAT activity, HLA-II/CD74 state, IFI30/GILT
activity, and CTSS-like lysosomal protease activity. Assumptions are stated in
the script. The model is not fit to kinetic data; it is a falsification/stress
test of the IFI30 intervention idea.

Result:

- A 70% upstream IFNGR/JAK suppression produces broad readout reductions
  qualitatively similar to Mixscale: IFN/APC log2FC about -1.1 and HLA-II/CD74
  log2FC about -0.6 in the model.
- IFI30 suppression, even at 95%, does not reproduce broad upstream IFN/APC or
  HLA-II/CD74 suppression over feedback strengths 0 to 10. It mainly reduces
  the `gilt_lysosomal_readout` (for example, at feedback=2 and 95% IFI30
  suppression: IFN/APC log2FC=-0.175, HLA-II/CD74 log2FC=-0.060, lysosomal
  readout log2FC=-0.558).
- CTSS suppression behaves similarly as a downstream effector-only intervention:
  it reduces the lysosomal readout but not upstream IFN/APC or HLA-II/CD74.

Decision: IFI30 inhibition cannot be claimed to arrest the whole cross-disease
IFN/APC state unless future real perturbation data prove a stronger feedback
than this model allows. The model pushes the therapeutic contribution away from
"IFI30 broadly shuts down the inflammatory APC transition" and toward either
(1) selective antigen/epitope processing modulation, (2) combination or
stratification with upstream pathway drugs, or (3) a biomarker-defined subgroup
for existing JAK/IFN-axis intervention.

## 2026-05-26 21:19 UTC

Integrated Wave 3 subagent returns:

- Disease-breadth scout recommends RA synovium/macrophage `E-MTAB-8322` as the
  next best tissue download, followed by T1D HPAP `GSE148073`. This gives a
  clear route to broaden beyond brain/gut/skin/salivary gland.
- Novelty scout blocks broad `IFI30/GILT` inhibition, activation, or generic
  modulation for MS/autoimmunity. IFI30/GILT is already prior-arted in MS/EAE
  mechanism, MS therapy response biomarker panels, RA macrophage arthritis
  biology, Sjogren/SLE biomarkers, and general IFN/MHC-II antigen-processing
  biology. The only surviving narrow novelty lane is a combined cell-state
  companion biomarker: `IFN-gamma/HLA-II/CD74/IFI30-GILT`, used to predict
  treatment response or enrichment, not diagnosis.
- Genetics scout confirms pathway-compatible but not single-gene
  cross-autoimmune genetics. HLA-II/MHC is broad but non-specific;
  `IRF1/CARINH` is the best non-MHC cross-disease regulatory anchor; `IFI30` is
  MS-specific coloc-grade support, not a pan-autoimmune target. Do not claim
  MR/coloc support for `CD74`, `CTSS`, `STAT1`, `CIITA`, `RFX5`, `IFNGR1`,
  `JAK1`, or pan-disease `IFI30`.

Downloaded `GSE253006_RAW.tar` for UC tofacitinib treatment response
(409 MB, MD5 `ea106b3ab755538a2c863f53b240e0f2`) and GEO family metadata. The
sample metadata include 11 baseline samples (5 responders, 6 non-responders)
and 12 post-treatment samples. The raw archive contains per-sample 10x matrices
only, with no GEO cell-type annotation file.

Ran `scripts/v3_analyze_gse253006_tofacitinib_uc.py`, a deliberately weak
all-cell sample-level module analysis. Result: baseline responder samples are
directionally higher for `ifn_apc` (delta=0.045, Hedges g=0.262, p=0.677) and
`CD74` (delta=0.128, g=0.345, p=0.573), but no tested target/module survives
FDR. `NLRC5` has the strongest nominal baseline responder-high trend
(delta=0.036, g=1.399, p=0.0655), still FDR=0.978.

Interpretation: do not use this as a positive proof. The published GSE253006
paper already reports higher baseline JAK-STAT activity in responders, so the
general JAK-STAT response-biomarker angle is prior art. Our all-cell module
replication is underpowered and lacks cell-type resolution. It can only support
the statement that a narrow cell-state biomarker would need prospective,
cell-type-resolved validation beyond the public GEO supplement.

## 2026-05-26 21:30 UTC

Routed around the RA `E-MTAB-8322` transfer blocker by analyzing the smaller
autoimmune thyroid spatial dataset `GSE248205`.
`scripts/v3_analyze_gse248205_thyroid_spatial.py` treats each Visium sample as
the statistical unit, not each spot, and compares two controls with three
Hashimoto thyroiditis and three Graves disease samples. Added the script to
`run_v3_analysis.sh` so this evidence is reproducible when the extracted
processed matrices are present.

Result:

- Hashimoto thyroiditis strongly reproduces the IFN-gamma/HLA-II/CD74/GILT/TAP
  antigen-processing state relative to control thyroid:
  `mixscale_validated_ifng_readout` delta=0.933, Hedges g=19.687, p=5.84e-05,
  FDR=0.00169; `mif_cd74_receptor_state` delta=1.790, g=19.590, p=0.000327,
  FDR=0.00271; `hla_ii_apc` delta=1.699, g=30.190, p=0.00537, FDR=0.02197;
  `ifn_apc` delta=1.229, g=17.340, p=0.00568, FDR=0.02197.
- Individual Hashimoto thyroid genes that survive FDR include `HLA-DPA1`,
  `HLA-DRA`, `CTSS`, `TAP2`, `IRF1`, `IFI30`, `HLA-DRB1`, `HLA-DPB1`, `B2M`,
  `TAP1`, and `STAT1`. `CD74` is directionally large but not FDR-significant
  in the sample-level test (delta=2.583, g=10.062, p=0.0514, FDR=0.149).
- Graves disease shows only weak trends for the same axis; no feature in the
  Graves-vs-control contrast survives FDR in this small sample-level analysis.

Guardrail: the Hashimoto effect sizes are implausibly large as population
effect estimates because n=2 controls and n=3 cases with low within-group
variance inflate standardized effects. This is valid as cross-tissue recurrence
support, not as a precise effect-size estimate or a clinical biomarker
performance claim.

Decision: add autoimmune thyroid disease as an additional disease/tissue
supporting the state, but distinguish Hashimoto from Graves. This strengthens
the "shared cell/tissue state" claim and simultaneously argues against a
one-size-fits-all autoimmune-thyroid intervention.

## 2026-05-26 21:34 UTC

Added `scripts/v3_build_cross_disease_convergence_tables.py` and updated
`scripts/v3_rank_central_and_intervention_candidates.py` to include the
Hashimoto spatial route-around with a hard per-module cap so the small-n Visium
dataset cannot dominate scoring.

Cross-disease convergence output:

- `IFNG_HLAII_CD74_GILT_TAP_transition`: tested in 7 diseases from local
  quantitative outputs; strong in Crohn disease, Hashimoto thyroiditis, MS, and
  ulcerative colitis; supportive in Sjogren syndrome and psoriasis; Graves
  disease is positive-null only. No negative-trend disease in the local
  measurement set.
- Top module by disease breadth is `mif_cd74_receptor_state`: tested in 7
  diseases; strong in 3; supportive-or-strong in 5; trend-or-better in 5;
  supporting diseases Crohn disease, Hashimoto thyroiditis, MS, Sjogren
  syndrome, and ulcerative colitis.
- `ifn_apc` and `mixscale_validated_ifng_readout` each support Crohn disease,
  Hashimoto thyroiditis, Sjogren syndrome, psoriasis, and ulcerative colitis at
  trend-or-better in the local quantitative tables.

Updated first-pass central/intervention ranking after thyroid evidence:

- `IFNGR_JAK_STAT1_upstream_control`: centrality 43.376, intervention 34.000.
- `CD74_HLAII_receptor_APC_state_biomarker`: centrality 34.004, intervention
  30.882.
- `CIITA_RFX5_HLAII_transcriptional_gate`: centrality 22.563, intervention
  20.407.
- `IFI30_GILT_lysosomal_feedback_effector`: centrality 17.918, intervention
  18.326.
- `CTSS_cathepsinS_lysosomal_effector`: centrality 17.439, intervention
  17.260.

Interpretation: the central node is now better described as a cell-state
transition (`IFNG/HLA-II/CD74/GILT/TAP antigen-processing transition`) than as a
single drug target. The intervention point remains unsolved because the highest
centrality controller (`IFNGR/JAK/STAT1`) is broad and heavily prior-arted, while
the narrower enzymatic effectors (`IFI30`, `CTSS`) fail or weaken under
mechanistic and novelty scrutiny.

Parallel action: resumed the 9.1 GB State `adata_real.h5ad` download from
Hugging Face. If it completes, rerun State CD14 analysis with real gene mapping;
if not, maintain the current foundation-model blocker and use Mixscale as the
gene-specific perturbation substitute.

## 2026-05-26 21:37 UTC

Added `scripts/v3_rank_mixscale_transition_controllers.py` to avoid only testing
pre-selected targets in Perturb-seq. The script ranks every analyzed
cytokine-context perturbation by suppression of the four transition readouts:
`ifn_apc`, `hla_ii_apc`, `mif_cd74_receptor_state`, and
`gilt_lysosomal_apc`.

Controller-ranking result:

- `IFNG/IFNGR1`: transition suppression score 2.486; all 4 modules suppressed;
  75 significant negative gene-by-cell-type readouts.
- `IFNG/IFNGR2`: score 2.376; all 4 modules suppressed.
- `IFNG/JAK2`: score 1.950; all 4 modules suppressed.
- `IFNG/STAT1`: score 1.900; all 4 modules suppressed.
- `IFNG/JAK1`: score 1.591; all 4 modules suppressed.
- `IFNB/TYK2`: score 1.113; strongly suppresses `ifn_apc`
  (mean log2FC -0.969) and `gilt_lysosomal_apc` (-0.321), but does not suppress
  `hla_ii_apc` or `mif_cd74_receptor_state` in this readout panel.
- `IFNG/RFX5`: score 0.501; narrower suppression of HLA-II/CD74-state modules,
  not broad IFN/APC suppression.

Interpretation: the perturbation data reinforce a real IFN-gamma receptor/JAK/
STAT controller for the full transition. TYK2 is a plausible type-I-IFN
controller with better genetics/drug precedent, but it is not a full substitute
for the IFN-gamma/HLA-II/CD74 arm in Mixscale. RFX5 remains mechanistically
narrower and less druggable.

## 2026-05-26 21:38 UTC

Stress-checked the thyroid spatial result at sample level. All three Hashimoto
samples are consistently high for the state:

- `module_ifn_apc`: controls 0.285 and 0.379; Hashimoto 1.569, 1.600, 1.516.
- `module_hla_ii_apc`: controls 0.360 and 0.442; Hashimoto 2.133, 2.088,
  2.079.
- `module_mixscale_validated_ifng_readout`: controls 0.478 and 0.511;
  Hashimoto 1.440, 1.459, 1.384.
- `IFI30`: controls 0.121 and 0.109; Hashimoto 1.324, 1.337, 1.167.

Graves is heterogeneous: GD1 and GD2 are elevated for many state scores, while
GD3 is close to control for IFN/HLA/CD74 markers. That explains the weaker
Graves statistics and supports keeping it as non-positive rather than forcing a
thyroid-wide autoimmune claim.

## 2026-05-26 21:44 UTC

Integrated hour-3 hostile critique from
`subagents_v3/critique_hour3_report.md`. The critique correctly attacked the
current central mechanism as canonical IFN/APC activation and demanded
adversarial residualization against generic IFN intensity.

Added and ran `scripts/v3_residualize_antigen_processing_vs_ifn.py`.

Result:

- Inputs: 148 donor/sample units from direct h5ad analyses, thyroid spatial, and
  GSE111972 MS microglia.
- Tests: 44 target-module contrasts.
- Raw nominal support: 23 tests.
- IFN-residual nominal support: 3 tests.
- No residual test survives global FDR.

The only nominal residual positives are:

- MS GSE111972 white-matter microglia `mif_cd74_receptor_state`: raw delta
  0.614, p=0.00547; residual after `ifn_apc` delta 0.456, p=0.00789.
- MS GSE111972 white-matter microglia `lysosomal_apc`: raw delta 0.513,
  p=0.0413; residual delta 0.404, p=0.0800.
- Sjogren salivary epithelial `mif_cd74_receptor_state`: raw delta 0.207,
  p=0.0207; residual delta 0.0447, p=0.0734.

Decision: the broad pan-autoimmune IFN/APC transition claim is demoted. The
current package now supports recurrence of a canonical IFN/APC state, not a
validated residual pan-autoimmune mechanism. Any surviving translational claim
must either become much narrower (e.g. MS/Sjogren CD74/HLA receptor-state
stratification) or pivot to a different cross-disease mechanism that survives
orthogonalization against generic IFN.

## 2026-05-26 21:45 UTC

Attempted a pivot away from IFN/HLA by extending
`scripts/v3_analyze_direct_h5ad_cell_states.py` with non-IFN modules:
`lipid_loader_repair`, `complement_phagocytosis`, `hif_nampt_metabolic`, and
`inflammatory_nfkb`. Reran direct h5ad module analysis and gene replication.

Result in direct h5ad donor-level module comparisons:

- `hif_nampt_metabolic` is strongest in IBD compartments, not broadly
  pan-autoimmune: Crohn colon epithelial delta=0.247, Hedges g=2.228,
  p=0.00350, FDR=0.0431; UC colon epithelial delta=0.396, g=2.204,
  p=0.00637, FDR=0.0506; UC myeloid delta=0.695, g=2.061, p=0.00843,
  FDR=0.0527.
- `inflammatory_nfkb` is also IBD-dominant: UC colon epithelial delta=0.186,
  g=3.330, p=0.000340, FDR=0.0182; UC myeloid delta=0.952, g=2.169,
  p=0.00778, FDR=0.0520.
- `lipid_loader_repair` remains weak in direct h5ad cell-resolved data:
  Crohn epithelial delta=0.066, g=1.522, p=0.0326, FDR=0.102; other direct
  disease compartments are weaker.
- `complement_phagocytosis` does not replicate as a broad direct h5ad module.

Updated cross-disease module summary after the extended module panel:

- `hif_nampt_metabolic`: tested in 5 diseases, supportive-or-strong in 2,
  supporting diseases Crohn disease and ulcerative colitis.
- `inflammatory_nfkb`: tested in 4 diseases, supportive-or-strong in 1,
  trend-or-better in 2, supporting diseases Crohn disease and ulcerative
  colitis.
- `lipid_loader_repair`: tested in 5 diseases, supportive-or-strong in 1,
  supporting diseases Crohn disease and MS.
- `complement_phagocytosis`: no trend-or-better support in the direct h5ad
  measurement set.

Decision: the non-IFN pivot does not currently outperform the demoted IFN/APC
state as a cross-autoimmune mechanism. `HIF/NAMPT` and `inflammatory NF-kB` are
potential IBD-specific leads, not a V3 pan-autoimmune solution.

## 2026-05-26 21:57 UTC

Reran direct h5ad analysis after adding T1D pancreatic compartments.

Important T1D results:

- `t1d_acinar_cell` `inflammatory_nfkb` high-fraction: delta 0.527,
  Hedges g 3.842, p=0.00246, FDR=0.0482.
- `t1d_ductal_cell` `mif_cd74_receptor_state` mean-score: delta 0.172,
  Hedges g 1.142, p=0.00364, FDR=0.0482.
- `t1d_ductal_cell` `mixscale_validated_ifng_readout` mean-score:
  delta 0.272, Hedges g 1.952, p=0.0193, FDR=0.0837.
- `t1d_acinar_cell` `lipid_loader_repair` mean-score: delta 0.205,
  Hedges g 2.003, p=0.0212, FDR=0.0839.

Gene-level note from the T1D run:

- `LIPA` is the top positive mean-z gene in T1D ductal cells among the tracked
  candidate genes: delta 0.316, Hedges g 2.606, p=0.00157, FDR=0.175 across
  the broad tracked-gene panel.

Interpretation:

The T1D extension strengthens two different lanes:

1. The recurrent IFN/HLA/CD74 state appears in pancreatic ductal/acinar cells,
   but this remains vulnerable to the generic IFN critique.
2. `LIPA` revives the lipid-lysosomal lane as a candidate central-node test,
   because it is mechanistically closer to lipid handling than CD74/HLA-II and
   has signals in multiple non-brain epithelial/stromal compartments.

Immediate decision: do not collapse these lanes into one story. Test them
against each other.

## 2026-05-26 21:58 UTC

Reran `scripts/v3_build_cross_disease_convergence_tables.py`,
`scripts/v3_rank_central_and_intervention_candidates.py`, and
`scripts/v3_residualize_antigen_processing_vs_ifn.py`.

Updated convergence:

- `mif_cd74_receptor_state`: tested in 8 diseases; 3 strong; 6
  supportive-or-strong.
- `ifn_apc`: tested in 8 diseases; 2 strong; 4 supportive-or-strong.
- `mixscale_validated_ifng_readout`: tested in 7 diseases; 3 strong; 4
  supportive-or-strong.
- `lipid_loader_repair`: tested in 6 diseases; 1 strong; 2
  supportive-or-strong; supporting diseases Crohn disease, MS, and T1D under
  trend-or-better criteria.

Updated residualization:

- 217 donor/sample units.
- 56 tests.
- 30 raw nominal supports.
- 4 IFN-residual nominal supports.
- No residual FDR-significant support.

Residual positives:

- MS white-matter microglia `mif_cd74_receptor_state`: raw delta 0.614,
  p=0.00547; IFN-residual delta 0.456, p=0.00789, residual FDR 0.442.
- Sjogren epithelial `mif_cd74_receptor_state`: raw delta 0.207, p=0.0207;
  IFN-residual delta 0.0447, p=0.0734, residual FDR 0.974.
- MS white-matter microglia `lysosomal_apc`: IFN-residual delta 0.404,
  p=0.0800, residual FDR 0.974.
- T1D acinar `mixscale_validated_ifng_readout`: IFN-residual delta 0.108,
  p=0.0821, residual FDR 0.974.

Decision:

Broad cross-disease HLA/CD74 recurrence is real enough to keep mapping, but too
generic to be the central therapeutic claim. The next forcing question is
whether the lipid-lysosomal `LIPA`/acid-lipase sublane has better disease breadth
and intervention tractability than the residual CD74/HLA receptor-state lane.

## 2026-05-26 22:05 UTC

Audited the intervention scout's PDE4/cAMP-PKA suggestion against the existing
L1000FWD output.

Added `scripts/v3_pde4_camp_l1000_audit.py` and added it to
`run_v3_analysis.sh`.

Result:

- LINCS2020 metadata contains 85 rows and 34 unique perturbagen IDs matching
  PDE4/cAMP terms.
- Core compounds present in LINCS metadata include apremilast, roflumilast,
  rolipram, cilomilast, ibudilast, piclamilast, forskolin, and bucladesine.
- Existing L1000FWD top-hit outputs contain 0 rows matching the core PDE4
  compounds.
- Only 2 rows match broad cAMP terms: both are `colforsin` / ADCY2 adenylyl
  cyclase activator signatures, and both appear in the `similar` direction,
  not the `opposite` reversal direction.

Interpretation:

This is a weak/negative perturbational support result for PDE4/cAMP as a
signature reversal candidate. It does not prove PDE4/cAMP cannot reduce
CIITA/MHC-II in tissue, because L1000FWD is cell-line and top-hit-limited, but
it prevents me from using L1000FWD as independent support for the PDE4 lead.

## 2026-05-26 22:04 UTC

Integrated foundation-model gate report from Mill:
`subagents_v3/wave4_foundation_gate_report.md`.

Independent check confirmed:

- `data/raw_v3/state_parse_split4/adata_real.h5ad` is still truncated:
  5,619,356,404 bytes local vs 9,112,404,896 bytes stored EOF.
- `anndata.read_h5ad(..., backed="r")` fails with HDF5 truncation.
- Existing State output tables contain `FEATURE_n` placeholders and no named
  genes among checked targets.

Decision:

Do not use State as foundation-model evidence for the current claim. The
resumed download continues, but until the file opens and rerunning
`scripts/v3_analyze_state_parse_cd14.py` yields named-gene module scores,
foundation-model perturbation remains an unmet DoD element. Mixscale CRISPRi is
the valid perturbation substitute; Geneformer is a possible later
model-hypothesis fallback.

## 2026-05-26 22:08 UTC

Added `scripts/v3_residualize_lipa_vs_stress.py` and added it to
`run_v3_analysis.sh`.

Question: can the revived `LIPA` lipid-lysosomal lane survive simple
same-compartment residual controls against `ifn_apc`, `inflammatory_nfkb`,
`hif_nampt_metabolic`, `lipid_loader_repair`, and `lysosomal_apc`?

Raw `LIPA` direct h5ad pattern:

- Positive nominal: Crohn epithelial delta 0.102, Hedges g 1.362, p=0.0463.
- Positive nominal: psoriasis keratinocyte delta 0.304, Hedges g 3.639,
  p=0.00722.
- Positive nominal: T1D ductal delta 0.316, Hedges g 2.606, p=0.00157.
- Negative nominal: Crohn myeloid delta -0.333, Hedges g -1.348, p=0.0383.
- Negative nominal: UC myeloid delta -0.360, Hedges g -1.500, p=0.0278.

Residual result:

- Psoriasis keratinocyte remains nominal after residualizing against
  `inflammatory_nfkb`: residual delta 0.271, Hedges g 2.572, p=0.0225,
  residual FDR 0.385.
- T1D ductal remains nominal after residualizing against `hif_nampt_metabolic`:
  residual delta 0.233, Hedges g 1.839, p=0.00164, residual FDR 0.116.
- T1D ductal remains nominal after residualizing against `lipid_loader_repair`:
  residual delta 0.275, Hedges g 2.225, p=0.000314, residual FDR 0.0863.
- T1D ductal remains nominal after residualizing against `lysosomal_apc`:
  residual delta 0.148, Hedges g 1.414, p=0.00703, residual FDR 0.227.

Interpretation:

This does not promote `LIPA`. Direction inconsistency across myeloid vs
epithelial/ductal compartments is a major warning. The useful signal is a
narrower possibility: `LIPA` may mark epithelial/ductal lipid-lysosomal stress
in T1D/psoriasis/Crohn epithelial tissue, while myeloid compartments move in
the opposite direction. That is not currently a pan-autoimmune central node.

## 2026-05-26 22:09 UTC

Integrated residual CD74/HLA receptor-state scout report from Leibniz.

Conclusion accepted:

- Demote residual CD74/HLA receptor-state to biomarker-only.
- MS white-matter microglia is the only credible residual signal.
- Sjogren residual signal is weak and mostly IFN-explained.
- T1D ductal/acinar raw support collapses under IFN residualization.
- CD74/MIF, anti-CD74, CIITA/MHC-II gate, CTSS, PDE4/cAMP, and MIF-blocking
  handles are either prior-arted, too broad, or not currently supported by
  strong in-silico reversal.

Updated candidate-status result:

- Active lanes: `LIPA_lipid_lysosomal` only.
- Demoted/hold lanes: IFNG/HLA/CD74 transition, residual CD74/HLA
  receptor-state, HIF/NAMPT inflammatory metabolism, PDE4/cAMP local CIITA
  gate.

This is uncomfortable but useful: the session has not found a DoD-grade
central target by hour 4. The remaining `LIPA` lane is mechanistically closer to
the original lipid-lysosomal hypothesis but currently looks
compartment-specific and directionally mixed.

## 2026-05-26 22:11 UTC

Integrated `LIPA` scout report from Boole.

Conclusion accepted:

- Demote `LIPA` as a V3 central cross-autoimmune node.
- Keep `LIPA` as a secondary epithelial/ductal/keratinocyte lipid-lysosomal
  repair/stress marker only.

Why:

- MS support is lipid-repair module-level; `LIPA` itself is not significant in
  GSE111972 white-matter microglia.
- Strongest positives are T1D ductal and psoriasis keratinocyte, not myeloid.
- Crohn and UC myeloid compartments are nominally negative.
- Genetics is weak.
- Broad MS repair novelty is constrained by recent LAL/Lipa white-matter repair
  prior art.

Decision:

All candidate lanes active at hour 4 are demoted or on hold. This does not end
the session. It forces a pivot away from single-gene rescue of the V2 lipid
module. Next candidate search should look for a different cross-disease node
that can explain tissue-resident stress/repair and inflammatory myeloid
recurrence with better direction stability, genetic support, and druggability.

## 2026-05-26 22:23 UTC

Wave-5 OSM/OSMR and complement integration.

Inputs reviewed:

- `subagents_v3/wave5_complement_scout_report.md`
- `subagents_v3/wave5_local_quant_report.md`
- `subagents_v3/wave5_osmr_scout_report.md`
- `results_v3/wave5_local_quant/*`
- `results_v3/osmr_complement_axes/*`

Complement/C1q result:

- No-go as central node.
- MS chronic-active-rim and lupus nephritis C1q biology are real, but local
  direct h5ad and GSE111972 evidence is directionally inconsistent for a
  pan-autoimmune resident-myeloid state.
- Anti-C1q/classical-complement intervention is biologically double-edged and
  prior-arted.

OSM/OSMR result:

- Continuation signal in Crohn/UC/T1D epithelial or ductal-like compartments.
- Myeloid `OSM` is nominally increased in Crohn and UC; stromal/epithelial
  receptor/response signals are compartmental.
- Supplemental script `scripts/v3_analyze_osmr_complement_axes.py` added
  stromal/endothelial compartments. It found UC epithelial OSM-ligand module
  delta 0.186, p 0.000340, FDR 0.0254; Crohn epithelial
  `osmr_signal_response` delta 0.201, p 0.00721, FDR 0.0805; T1D acinar
  OSM-ligand module delta 0.491, p 0.0104, FDR 0.0884.
- Residual support is nominal and not global-FDR strong. MS support is absent,
  and external MS OSM literature is directionally ambiguous/protective in some
  models.

Foundation-model update:

- Full `adata_real.h5ad` now opens, shape `(1125352, 2000)`, but `var_names`
  are numeric strings and `var` has no gene-symbol columns.
- Re-running `scripts/v3_analyze_state_parse_cd14.py` still reports
  `module_scoring_status: blocked_no_gene_symbols_for_feature_ids`.
- State remains feature-agnostic perturbation calibration only. OSM perturbation
  validation is measurable (Spearman 0.262, direction match 0.654) but not
  gene-module interpretable.

Decision:

Do not promote OSM/OSMR or complement. The next analysis should stop
hand-picking plausible immunology nodes and run a broader gene-level discovery
screen across the local h5ad disease compartments, then intersect hits with MS
evidence, genetics, druggability, and prior art.

## 2026-05-26 22:31 UTC

Broad h5ad gene-discovery screen completed.

Script:

- `scripts/v3_broad_h5ad_gene_discovery.py`

Outputs:

- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_lipid_lysosomal_neighborhood_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_ms_positive_rank.tsv`

Run statistics:

- 17 local h5ad disease/compartment analyses.
- 282,630 donor-level gene contrasts.
- 25,176 ranked genes.

Initial interpretation:

- Top score genes are mostly generic antiviral/chromatin/tissue-stress genes:
  `CBX3`, `IFITM3`, `IFITM2`, `TIMP1`, `PSME2`, `CFB`, `MMP7`.
- Broadest five-disease signals (`IFITM2/3`, `PSME1/2`) are IFN/antiviral or
  proteasome-like and do not align cleanly with the lipid-lysosomal myeloid
  mechanism; `IFITM2/3` are also not MS-positive in GSE111972 white matter.
- Best druggable lipid/injury candidate emerging from the screen is `LTA4H`:
  Crohn myeloid delta 1.229, p 0.00719; UC myeloid delta 1.177, p 0.0196;
  T1D acinar delta 0.427, p 0.00872; MS white-matter microglia delta 0.809,
  Hedges g 1.357, p 0.00636.
- `CHI3L1` is MS-positive and tissue-injury/lysosomal adjacent but looks more
  like a secreted biomarker/fibrosis marker than an obvious intervention point:
  UC stromal delta 5.936, p 0.000562; Crohn stromal delta 4.697, p 0.0112;
  T1D endothelial delta 2.712, p 0.0378; MS white matter delta 2.007,
  p 0.00461.
- `C15ORF48` and `SNX10` are strong MS-positive inflammatory/myeloid markers,
  but current intervention tractability is weak.

Decision:

Advance `LTA4H` and `CHI3L1` into focused scrutiny. `LTA4H` gets priority
because it is an enzyme in lipid mediator biology with existing chemical matter.
`CHI3L1` is retained as a biomarker/tissue-damage comparator. Added
`scripts/v3_geneformer_candidate_delete_screen.py` to rerun the Wave-6
Geneformer route on these broader candidates.

## 2026-05-26 22:34 UTC

Geneformer candidate deletion screen completed.

Script:

- `scripts/v3_geneformer_candidate_delete_screen.py`

Outputs:

- `results_v3/geneformer_candidate_delete/geneformer_candidate_delete_metrics.tsv`
- `results_v3/geneformer_candidate_delete/geneformer_candidate_delete_gene_summary.tsv`
- `results_v3/geneformer_candidate_delete/geneformer_candidate_delete_summary.json`

Key results:

- `LTA4H`: 4 contexts with token, 6 disease cells with token, mean cosine shift
  -0.000289, mean projection shift -0.00278, support contexts 0. This does not
  support `LTA4H` deletion as disease-to-control normalizing in this model.
- `CHI3L1`: 4 contexts, 18 disease cells, mean cosine shift -0.000146, mean
  projection shift 0.0441, support contexts 1. Mixed/weak.
- `IFITM3`: 8 contexts, 45 disease cells, mean cosine shift 0.000189,
  projection shift 0.0239, support contexts 3. This is the strongest
  model-normalization signal but it is not MS-positive in GSE111972 and is
  biologically generic antiviral/IFN biology.
- `CBX3`: 8 contexts, 34 disease cells, support contexts 3, but it is a nuclear
  chromatin/proliferation-associated candidate without a clear lipid-lysosomal
  intervention path.

Prior-art sanity from web/PubMed during this step:

- LTA4H/LTB4 is directly prior-arted in MS/EAE, including a Journal of
  Immunology abstract reporting LTA4H inhibitors reducing EAE clinical scores.
- LTA4H inhibitors have clinical and patent prior art in inflammatory diseases,
  including acebilustat and LYS006 programs and patents with inflammatory/IBD/MS
  claims.
- CHI3L1/YKL-40 is heavily prior-arted as an MS biomarker and broader
  inflammatory-disease marker; recent reviews explicitly frame it as biomarker
  and therapeutic target.

Decision:

Demote `LTA4H` as V3 central node despite local MS/Crohn/UC/T1D expression
support, because foundation-model support is negative/weak and prior art is
blocking. Keep `CHI3L1` as injury/fibrosis comparator only. Current strongest
model-supported broad marker is `IFITM3`, but lack of MS positivity and
generic IFN biology make it unsuitable as final target.

## 2026-05-26 22:41 UTC

Wrote actual hour-4 milestone `MILESTONE_2.md`.

Self-critique at this point:

- The broad screen is statistically useful but still a donor-level pseudobulk
  screen with no covariate adjustment. It is not causal.
- The current MS anchor is imported GSE111972 white-matter microglia/macrophage
  statistics, so MS positivity must be independently replicated before a final
  claim.
- Geneformer deletion shifts are very small embedding movements. They can veto
  an expression-only candidate when negative, but should not be treated as
  strong proof when positive unless compared with real perturbation data.
- The top broad hits are largely generic IFN/stress/chromatin markers. If I
  force those into a therapeutic target, I will repeat the prior
  proxy-satisficing error.

Decision:

The next block must focus on candidates where mechanism and intervention are
credible, not merely where expression rank is high. I will prioritize `FABP5`,
`MSR1`, `SCARB2`, and glycan-checkpoint comparators and require local
replication, prior-art clearance, and either foundation-model or real
perturbation support before promotion.

## 2026-05-26 22:56 UTC

Ran the wave-7 LGALS3 fail-fast analysis.

Script:

- `scripts/v3_lgals3_glycan_checkpoint_analysis.py`

Outputs:

- `results_v3/lgals3_glycan_checkpoint/lgals3_summary.json`
- `results_v3/lgals3_glycan_checkpoint/lgals3_candidate_crosswalk.tsv`
- `results_v3/lgals3_glycan_checkpoint/lgals3_disease_summary.tsv`
- `results_v3/lgals3_glycan_checkpoint/lgals3_residual_tests.tsv`

Key result:

- `LGALS3` fails cross-autoimmune central-node status. It has MS foamy/MIMS2
  support from prior local evidence, but direct local h5ad signal is negative
  in four autoimmune diseases and no residualized positive test survives.
- Crosswalk: direct positive disease count 0; direct negative disease count 4;
  direct negative compartment count 5; residual-retained positive test count 0;
  broad MS white-matter delta 0.778 with p=0.0509.

Interpretation:

This is a useful falsification. The scout's mechanistic reasoning was plausible,
but the stronger operationalization contradicts the cross-disease claim. I will
not rescue `LGALS3` with literature plausibility.

Next pivot:

The residual analysis surfaced `CD44`, `TYROBP`, and cathepsin signals as
survivors, but all have serious targetability/prior-art/repair-risk problems.
The next step is to determine whether a broader `TYROBP`/DAP12 phagolysosomal
transition or a matrix-retention transition is more defensible than single-gene
LGALS3.

## 2026-05-26 22:50 UTC

Avicenna wave-8 breadth report returned.

Important correction to my local crosswalk: I initially undercounted existing
evidence because I looked for columns named `positive` / `negative` in
`existing_evidence_candidate_matrix.tsv`; the actual columns are
`positive_nominal` / `negative_nominal`. I patched
`scripts/v3_lgals3_glycan_checkpoint_analysis.py` and reran the analysis.

Corrected crosswalk preserves the LGALS3 demotion:

- `LGALS3`: existing positive disease count 1 (MS), direct local positive
  disease count 0, direct local negative disease count 4.
- `FABP5`: existing positives 5, negatives 2, but direct local positives 0 in
  the residualized crosswalk and direct broad contradictions in UC.
- `MSR1`: existing positives 5, but direct local positives 0.
- `CD44`: direct local positive disease count 2, residual-retained positive
  disease count 2, MS white-matter positive.

Started a dedicated Geneformer screen:

- `scripts/v3_geneformer_phagolysosomal_matrix_screen.py`

Purpose: test whether deleting `CD44`, `TYROBP`, cathepsins, and conflicted
lipid/glycan comparators moves disease-cell embeddings toward matched control
centroids in real local h5ad cells.

## 2026-05-26 23:00 UTC

Geneformer phagolysosomal/matrix screen completed.

Outputs:

- `results_v3/geneformer_phagolysosomal_matrix_delete/geneformer_phagolysosomal_matrix_gene_summary.tsv`
- `results_v3/geneformer_phagolysosomal_matrix_delete/geneformer_phagolysosomal_matrix_delete_metrics.tsv`
- `results_v3/geneformer_phagolysosomal_matrix_delete/geneformer_phagolysosomal_matrix_summary.json`

Interpretation:

- `CD44` has the best local residualized expression among the recent pivots,
  but the model screen is negative: support contexts 0 across 9 contexts and
  75 disease cells with token. I will not promote `CD44`.
- `TYROBP` is not ready: only 2 contexts with token and aggregate shifts are
  negative.
- `LGALS3` remains demoted.
- `CTSB` and `CTSL` are the only candidates with repeated model support, but
  cathepsins are high-risk as final targets because they are generic lysosomal
  proteases with repair/debris-clearance and prior-art concerns.

Decision:

Treat cathepsins as a model-supported comparator axis, not a finding. Next
local test should evaluate the broader pivot panel from wave 8:
`ACSL3`, `APOC1`, `CD44`, `LAMP3`, `CTSL`, `CHI3L1` benchmark, plus `LGALS8`,
`UGCG`, `GBA2`, and `CD300F`.

## 2026-05-26 23:01 UTC

Implemented pivot-panel triage.

Script:

- `scripts/v3_pivot_panel_triage.py`

Outputs:

- `results_v3/pivot_panel_triage/pivot_panel_summary.tsv`
- `results_v3/pivot_panel_triage/pivot_panel_summary.json`

Decision:

- `APOC1` is the only candidate routed to a new foundation-model perturbation
  test. It passes the current local gates because it has MS white-matter
  positivity (`delta_log2=0.806`, `p=0.0333`) and direct positives in three
  non-MS disease contexts (`t1d_acinar_cell`, `sjogren_gland_epithelial`,
  `ibd_uc_epithelial`) with one contradiction (`ibd_uc_stromal` negative).
- This is not a target nomination. It is a routing decision requiring
  Geneformer perturbation support, genetics review, prior-art review, and
  independent MS replication.
- Cathepsins `CTSB/CTSL` stay as comparator biology. The triage script was
  patched after first run so manual `hold` candidates are not mislabeled as
  target-advancement candidates.

Started:

- `scripts/v3_geneformer_pivot_panel_screen.py`, using Geneformer V2-104M
  lightweight token deletion across IBD epithelial/stromal/myeloid, psoriasis
  keratinocyte/APC, Sjogren epithelial/APC, and T1D acinar/ductal/stellate/
  endothelial contexts.

## 2026-05-26 23:09 UTC

APOC1 failed the foundation-model gate.

Script:

- `scripts/v3_geneformer_pivot_panel_screen.py`

Outputs:

- `results_v3/geneformer_pivot_panel_delete/geneformer_pivot_panel_gene_summary.tsv`
- `results_v3/geneformer_pivot_panel_delete/geneformer_pivot_panel_delete_metrics.tsv`

Key result:

- `APOC1`: contexts with token = 3, disease cells with token = 4, support
  contexts = 0, mean cosine z vs random = -1.0917, mean projection shift =
  -0.0171.
- This is not compatible with promoting APOC1 as a perturbable central node in
  the available Geneformer route. It may still be a low-frequency local marker,
  but not a model-supported intervention hypothesis.

Reopened unrestricted broad h5ad discovery:

- Added `scripts/v3_unrestricted_survivor_scan.py`.
- Added `scripts/v3_geneformer_unrestricted_survivor_screen.py`.

Second-pass survivor result:

- `SNX10` is now the strongest model-supported survivor: MS white-matter
  `delta_log2=0.712`, `p=0.0127`; direct positives in Crohn myeloid, UC
  myeloid, T1D endothelial, and T1D stellate contexts; Geneformer contexts with
  token = 7, disease cells with token = 25, support contexts = 4, strong support
  contexts = 1.
- Prior wave-8 treated SNX10 as weak because the earlier candidate-delete
  screen used fewer contexts and fewer cells. The new result does not prove
  causality, but it justifies a focused SNX10 targetability/prior-art check.

Guardrail:

- `C15ORF48` is a strong expression marker but absent from the current
  Geneformer token dictionary, so it is held as model-blocked rather than
  promoted.

## 2026-05-26 23:20 UTC

Restarted the post-APOC1 pivot.

Decision:

- Do not rescue `APOC1`.
- Do not promote `SNX10` yet: it is the strongest current Geneformer survivor,
  but direct IBD prior art and disease-breadth gaps make it unsuitable as a V3
  final intervention point unless a narrower, novel, non-IBD or downstream
  mechanism emerges.
- Re-examine enzymatic or druggable neighbors (`LIPA`, `IFI30`, cathepsins) and
  model-supported broad survivors (`SDC4`, `DAP`, `MMADHC`, `LIMS1`) with the
  same strict gates: local cross-disease signal, perturbation support, genetics
  or causal plausibility, tractable intervention, and novelty.

Self-critique:

- The strongest local rows are still mostly observational donor-level expression
  plus lightweight token-deletion screens. This is not enough for a therapeutic
  claim.
- The analysis is vulnerable to tissue-composition artifacts: epithelial,
  stromal, myeloid, and endothelial contexts are being compared across diseases
  with different sampling strategies.
- A valid next target may not be the highest-expression marker. It may be an
  upstream or downstream controller whose perturbation normalizes the state.

## 2026-05-26 23:35 UTC

Post-APOC1 survivor gate executed.

New script:

- `scripts/v3_snx10_c15orf48_residual_gate.py`

Method:

- Built donor-level selected-gene pseudobulk from all 17 direct h5ad
  compartments using the same `CONFIGS` as the OSMR/complement analysis.
- Tested raw case-vs-control effects for `SNX10`, `C15ORF48`, and sentinels.
- Residualized each gene's donor-level mean z-score against same-compartment
  IFN/APC, NF-kB, HIF/NAMPT, HLA-II, lysosomal/APC, lipid-loader/repair, C1q/
  complement, MIF/CD74, and Mixscale IFN-gamma readout modules when available.
- Patched the script after the first run because the initially reused
  `direct_h5ad_cell_state` module table only covered 11 of 17 compartments.
  The corrected version prefers
  `results_v3/osmr_complement_axes/osmr_complement_donor_module_scores.tsv`,
  which covers all 17 compartments, and uses the older direct table only for
  extra modules.

Key output:

- `results_v3/snx10_c15orf48_residual_gate/snx10_c15orf48_residual_gate.tsv`

Result:

- `SNX10`: raw positive in Crohn myeloid and UC myeloid only. Retained residual
  positives remain IBD-only. Strict core-covariate surviving analysis count =
  0.
- `C15ORF48`: raw positive in Crohn myeloid, UC myeloid, and T1D endothelial.
  It has one non-IBD retained residual signal in T1D endothelial, but strict
  core-covariate surviving analysis count = 0.

Interpretation:

- This weakens the survivor-rescue route rather than strengthening it.
- `SNX10` is an IBD myeloid comparator with direct prior art, not a broad
  autoimmune node.
- `C15ORF48` remains a state marker with a possible T1D endothelial signal, but
  it fails the strict gate and still lacks Geneformer token support, target
  genetics, and a clear intervention modality.

Self-critique:

- The strict gate is deliberately conservative; it can discard true biology if
  the covariate modules absorb mechanistically relevant variance.
- That conservatism is appropriate here because the task requires a therapeutic
  claim, not a state-marker catalogue.
- The current failure pattern suggests that local expression breadth is being
  driven by inflammation/repair context and IBD sampling richness more than by
  one tractable pan-autoimmune lipid-lysosomal target.

Next forcing question:

- Identify a new intervention point from an upstream or downstream circuit that
  is not just a survivor expression marker: either a genetically anchored
  pathway with a selective non-saturated handle, or a cell-state transition
  controller with independent perturbation evidence.

## 2026-05-26 23:47 UTC

Broad residual-gated panel tested and demoted.

New scripts:

- `scripts/v3_broad_residual_gate.py`
- `scripts/v3_geneformer_broad_residual_screen.py`

Broad residual gate:

- Candidate panel size: 271 genes.
- Selection combined top broad h5ad rank, five-disease rows, four-disease
  low-contradiction rows, MS-positive three-disease rows, lipid/lysosomal
  two-disease rows, and manual mechanistic scout genes.
- Top residual-gate rows: `ATOX1`, `SQLE`, `TPM4`, `LDLRAD3`, `C1QTNF1`,
  `HIF1A`, `CBX3`, `CFB`, `TIMP1`.
- The strict survivors were dominated by IBD stromal analyses. This is a major
  warning because the same IBD-rich local panel has repeatedly produced
  plausible-looking rescue candidates after stronger hypotheses failed.

Geneformer broad residual screen:

- Candidate genes tested: 52.
- Top model-supported rows:
  - `SEC61B`: support contexts 5, strong support contexts 5.
  - `MTHFD2`: support contexts 3, strong support contexts 3.
  - `HIF1A`: support contexts 5, strong support contexts 2.
  - `SEC61A1`: support contexts 4, strong support contexts 2.
  - `TMSB10`: support contexts 4, strong support contexts 2.
  - `RPL17`: support contexts 3, strong support contexts 2.
  - `TPM4`: support contexts 5, strong support contexts 1.
  - `SQLE`: support contexts 3, strong support contexts 1.
- Interpretation: this is not target convergence. It is a generic
  ER-translocation / one-carbon metabolism / hypoxia / cytoskeletal stress
  pattern. The model did not rescue `ATOX1`, `SQLE`, `TPM4`, `CFB`, or
  `TIMP1` as clean central therapeutic nodes.

Wave-12 sidecar integration:

- Genetics/prior-art scout found no broad residual-gate candidate with all
  required properties: cross-autoimmune genetics, plausible modality, and
  non-blocking prior art.
- Hostile critique called the pivot hypothesis drift and identified IBD
  stromal dominance, weak MS anchoring, repair-state capture, and residualized
  expression over-interpretation as the main failure modes.

Decision:

- Do not promote broad residual-gate candidates.
- Stop spending cycles on the same local panel until the disease breadth is
  improved. The strongest next test is not another candidate screen; it is an
  independent-disease expansion, especially RA/SLE or other missing autoimmune
  atlases.

## 2026-05-26 23:55 UTC

Independent RA expansion started.

Reasoning:

- The prior pivot was failing because the same local panel kept over-producing
  IBD-rich or generic stress candidates. A credible next test needs independent
  disease breadth, preferably cell-resolved RA or SLE, before another central
  node can be trusted.
- Guessed CELLxGENE REST endpoints returned 404/405, but the official Census
  metadata table exposed source h5ad paths. This corrected the data-access
  operationalization rather than treating the route failure as a dataset
  blocker.

Actions:

- Resolved and downloaded the Binvignat et al. RA blood h5ad:
  `data/raw_v3/cell_state/ra_binvignat_blood.h5ad`.
- File details: 108,717 cells, 21,648 genes, local size 256 MB, MD5
  `e66d70ceffdaa99f824181d06cd76302`.
- Metadata inspection found 48,637 rheumatoid arthritis cells and 60,080 normal
  cells; monocyte/APC labels include classical monocyte, non-classical monocyte,
  and myeloid dendritic cell.
- Added `ra_blood_myeloid` to
  `scripts/v3_analyze_direct_h5ad_cell_states.py` using actual observed labels
  and `feature_name` gene symbols.
- SLE Perez et al. PBMC source h5ad is available but 11.3 GB; it is kept as a
  targeted-extraction branch rather than an immediate full download.

Self-critique:

- RA blood myeloid is not synovium. It improves independent disease breadth but
  may miss tissue-resident pathology and treatment-response biology.
- RA case/control donors may differ by age, sex, medication, and activity; the
  direct h5ad script currently tests donor-level case-vs-control but does not
  residualize these covariates.
- The next analysis must inspect RA direction and decide whether it reinforces
  or contradicts the lipid-lysosomal/myeloid module. If RA only supports generic
  IFN/HLA biology, it should not rescue the target nomination.

## 2026-05-27 00:03 UTC

Wave-13 genetics/prior-art reopen completed.

Method:

- Queried Open Targets Platform GraphQL for scoped `gwas_credible_sets`
  evidence across the V3 autoimmune disease panel.
- Preserved query output at
  `tmp_v3/wave13_opentargets_gwas_credible_sets.tsv`.
- Cross-checked candidate-specific druggability and prior-art blockers using
  PubMed/PMC, ClinicalTrials.gov, Google Patents, and selected primary or
  database sources.
- Wrote `subagents_v3/wave13_genetics_prior_art_reopen.md`.

Result:

- `GPR65` is the cleanest fail-fast scout after the demoted expression-hit
  route: broad-enough genetics, GPCR tractability, and direct pH/endolysosomal
  biology. The biology is not yet directionally safe because IBD macrophage
  protection and EAE/Th17 contexts may point in different directions.
- `SLC15A4`/`TASL`/`IRF5` is the strongest endolysosomal APC checkpoint branch,
  but `SLC15A4` itself is SLE-heavy in scoped genetic evidence and the
  therapeutic lane is already prior-arted.
- `TNFAIP3`, `PTPN2`, `CLEC16A`, `SH2B3`, and `IL10` are better read as genetic
  anchors for module validation than as direct targets.
- `OSMR`, `IL6R`, `TYK2`, `CFB`, `CTSS`, and `MIF/CD74` are useful positive
  controls or stratification comparators, but direct target novelty is blocked.

Self-critique:

- Open Targets credible-set rows are not coloc or MR. They are a consistent
  triage layer, not causal proof.
- Prior-art search was targeted rather than attorney-grade exhaustive. It is
  enough to prevent obvious false novelty, not enough to clear IP.
- `GPR65` could be a pH/context marker rather than a central module controller.
  Its next test must be perturbational and must include non-IBD contexts.

## 2026-05-27 00:07 UTC

RA expansion result interpreted; SLE targeted extraction started.

RA result:

- `scripts/v3_analyze_direct_h5ad_cell_states.py`,
  `scripts/v3_analyze_direct_h5ad_gene_replication.py`, and
  `scripts/v3_analyze_osmr_complement_axes.py` were rerun after adding
  `ra_blood_myeloid`.
- RA blood myeloid did not support the previously suspected lipid-lysosomal /
  IFN-HLA positive module pattern:
  - lipid-loader mean-score delta = 0.0126, Hedges g = 0.263, p = 0.426;
    high-fraction delta = 0.0224, g = 0.222, p = 0.501.
  - IFN/APC mean-score delta = -0.0460, g = -0.249, p = 0.450.
  - HLA-II/APC mean-score delta = -0.0678, g = -0.450, p = 0.176.
  - MIF/CD74 receptor-state mean-score delta = -0.0451, g = -0.266, p = 0.420.
- Gene-level RA direction was mixed and weak: `HIF1A`, `CXCR4`, `PLIN2`,
  `LDHA`, `ACSL1`, and `CD68` were slightly higher in RA cells, while
  `CD74`, HLA-II genes, `NAMPT`, `IL1B`, `CTSS`, and `LIPA` were lower by the
  simple cell-level mean comparison.
- The OSMR/complement-axis summary now includes RA and reports zero nominal
  RA positives for both `osm_osmr` and `complement_c1q`.

Interpretation:

- RA is an actual contradiction, not a missing data point.
- This demotes any "pan-autoimmune myeloid lipid-lysosomal target" claim that
  requires RA blood myeloid recurrence.
- A surviving claim would need to be narrower, e.g. tissue-resident epithelial /
  stromal complement-OSM response in IBD/T1D/psoriasis/Sjogren, or a stratified
  IFN/APC-high subset rather than all autoimmune diseases.

SLE route:

- The SLE Perez et al. full h5ad is reachable but 11.3 GB. I implemented
  `scripts/v3_analyze_sle_census_targeted.py` to use Census selected-gene
  extraction instead of a full download.
- Census metadata shows 777,258 SLE and 486,418 normal PBMCs with classical
  monocyte, non-classical monocyte, conventional dendritic cell, and
  plasmacytoid dendritic cell compartments.
- The selected-gene extraction is running. If it stalls, the logged
  alternative is a smaller donor/cell cap or full download only if the branch
  becomes central enough to justify the resource cost.

Self-critique:

- RA blood myeloid may not represent synovial disease; however, because the V3
  DoD asks for breadth, a contradiction in a large independent RA myeloid PBMC
  dataset must be weighted heavily.
- A broad cross-disease claim can no longer be built by only counting diseases
  that agree. The next milestone must explicitly state which diseases disagree
  and whether the mechanism is being reframed as subset-specific.

## 2026-05-27 00:36 UTC

Celiac disease breadth branch integrated.

Data route:

- Downloaded and analyzed `GSE315138`, active celiac disease and healthy
  control duodenal biopsy single-cell RNA-seq.
- Local raw archive:
  `data/raw_v3/gse315138/GSE315138_RAW.tar`, 365 MB, MD5
  `09b698d5e5bce143f2b38574420747cb`.
- GEO supplement exposed raw 10x matrices but no curated cell annotations.
  I therefore used marker-derived compartments in
  `scripts/v3_analyze_gse315138_celiac_marker_compartments.py`.

Result:

- 113,427 total cells across 4 active celiac and 2 control donors.
- Marker compartments: epithelial_like 35,888 cells, myeloid_apc_like 11,061,
  b_plasma_like 26,942, t_cell_like 28,579, stromal_endothelial_like 2,726,
  ambiguous 8,231.
- The strongest celiac effect sizes were epithelial-like IFN/HLA/CD74 signals:
  `mif_cd74_receptor_state` high-fraction delta 0.332, Hedges g 2.205,
  p=0.0124, FDR=0.740; `hla_ii_apc` high-fraction delta 0.338, Hedges g 1.908,
  p=0.0436, FDR=0.781; `ifn_apc` mean-score delta 0.388, Hedges g 1.204,
  p=0.0956, FDR=0.781.

Interpretation:

- Celiac adds trend-level effect-size support for an epithelial
  IFN/HLA/CD74 transition. It does not provide FDR-significant standalone
  evidence because donor n is tiny and compartments are marker-derived.
- This branch reinforces the transition-state framing but cannot rescue a
  drug-target claim by itself.

Wave-13 local candidate validation integrated.

Script:

- `scripts/v3_wave13_candidate_gene_local_validation.py`

Output:

- `results_v3/wave13_candidate_gene_local_validation/`

Key results:

- `CD74`: trend-or-better in 5/7 diseases, no negative-trend disease, but no
  FDR10 disease and direct therapeutic novelty is prior-art constrained.
- `SLC15A4`: trend-or-better in 4/7 diseases (Crohn, MS, psoriasis, UC), no
  negative-trend disease, but no FDR10 disease and SLE-heavy genetics/prior art
  remain unresolved.
- `CIITA` and `RFX5`: trend-or-better in 3/7 diseases, mainly Crohn,
  psoriasis, and T1D; RA and Sjogren are negative/null for these genes.
- `GPR65`: only one trend-positive disease (Sjogren) in local expression
  recurrence; demoted as a central expression node despite genetic/druggability
  interest.

Updated convergence:

- `scripts/v3_build_cross_disease_convergence_tables.py` and
  `scripts/v3_rank_central_and_intervention_candidates.py` now include celiac
  marker-derived evidence with an explicit capped contribution.
- The `IFNG_HLAII_CD74_GILT_TAP_transition` is now trend-or-better in 8/10
  diseases and supportive-or-strong in 7/10. RA remains null/negative and
  Graves is positive-null.

Self-critique:

- The apparent breadth is partly a canonical IFN/APC state recurring in
  inflamed barrier tissues. It may be therapeutically unoriginal.
- Celiac evidence is marker-derived and should be weighted below curated h5ad
  datasets.
- GPR65 was tempting because of genetics and GPCR druggability, but local
  recurrence does not support it as the central node.
- The next forcing question is intervention specificity: can any narrower
  controller downshift HLA-II/CD74 without broad JAK/STAT immunosuppression and
  without being blocked by prior art?

## 2026-05-27 00:46 UTC

Hour-6 critique and gate matrix integrated.

Critique:

- `subagents_v3/wave14_hour6_hostile_critique.md` returned and explicitly
  rejected the current IFNG/HLA-II/CD74 direction as a therapeutic central node
  without additional selective-intervention evidence.
- I accepted all major criticisms in `CRITIQUE_V3.md`: IFN confounding, RA
  contradiction, celiac weakness, missing DoD-grade foundation-model evidence,
  missing target-level genetics, and lack of a surviving intervention point.

Candidate gate matrix:

- Added and ran `scripts/v3_wave14_candidate_gate_matrix.py`.
- Output:
  `results_v3/wave14_candidate_gate_matrix/wave14_candidate_gate_matrix.tsv`.
- The matrix combines local expression recurrence, wave-13 Open Targets
  credible-set evidence, Europe PMC counts, ClinicalTrials.gov counts, and
  patent-search URLs.
- Only `SLC15A4_TASL_IRF5_endolysosomal_checkpoint` and
  `PTPN2_JAKSTAT_negative_regulator` passed both the simple expression and
  genetics gates.
- `PTPN2` has the wrong intervention direction for autoimmunity because
  restoring phosphatase function would be desired while current drug modality
  precedent is inhibition in oncology.
- `SLC15A4/TASL/IRF5` is the active fail-fast branch, but the pass is partly
  composite: expression breadth comes mostly from `SLC15A4`/`TASL` trends,
  whereas broad genetics is largely `IRF5`. This is a mechanism-circuit gate,
  not proof that one drug target has causal cross-disease support.

Focused Geneformer narrowed-candidate screen:

- Added and ran
  `scripts/v3_wave14_geneformer_narrowed_candidate_screen.py`.
- Output:
  `results_v3/wave14_geneformer_narrowed_candidate_delete/`.
- Model: Geneformer V2-104M, revision
  `04c2b2e84da7c0f385c3f9ad8f3ec24bab6650e5`, 104,365,056 encoder
  parameters loaded.
- Contexts: IBD myeloid/epithelial, psoriasis macrophage/dendritic, Sjogren
  APC, T1D ductal/acinar, RA classical monocyte, RA non-classical monocyte, RA
  myeloid dendritic cell.
- Main result: active intervention scouts did not show broad control-like
  embedding normalization.
  - `SLC15A4`: 7 contexts with token, 16 disease cells with token,
    0 support contexts, 0 strong support contexts, mean projection shift
    -0.00975.
  - `IRF5`: 2 contexts, 3 disease cells, 0 support contexts.
  - `GPR65`: 5 contexts, 8 disease cells, 0 support contexts, mean projection
    shift -0.0318.
  - `GSK3B`: 5 contexts, 7 disease cells, 0 support contexts.
  - `CIITA`: 6 contexts, 12 disease cells, 0 support contexts.
  - `RFX5`: 2 contexts, 2 disease cells, 0 support contexts.
  - `CD74`: 8 contexts, 87 disease cells, 0 support contexts.
- Top Geneformer-supported genes were `PTPN2` (3 support contexts, 1 strong),
  `SH2B3` (2 support, 1 strong), and `TNFAIP3` (2 support, 1 strong), all of
  which are better interpreted as genetic negative-regulator anchors than
  tractable direct targets.

Interpretation:

- The focused foundation-model channel demotes `SLC15A4/TASL/IRF5`, `GPR65`,
  `GSK3B`, and `CIITA/RFX5` as model-supported broad intervention points.
- This does not falsify them biologically, but it prevents using Geneformer as
  positive evidence for the current lead candidates.
- The run is now pushed toward a harder question: can a genetic negative
  regulator circuit (`PTPN2`/`TNFAIP3`/`SH2B3`) yield a druggable downstream
  control point, or should the cross-disease module be demoted to biomarker
  biology?

## 2026-05-27 00:49 UTC

Wave-14 SLC15A4/TASL/IRF5 fail-fast returned.

Report:

- `subagents_v3/wave14_slc15a4_tasl_failfast.md`

Script and outputs:

- `scripts/v3_wave14_slc15a4_tasl_failfast.py`
- `results_v3/wave14_slc15a4_tasl_failfast/`

Verdict accepted:

- No-go as a cross-autoimmune central/intervention candidate.

Key evidence:

- Local branch genes/modules had 0 FDR10-positive diseases.
- `SLC15A4` was trend-or-better in 4/7 diseases but no FDR10 positives;
  `TASL_CXorf21` in 3/7; `IRF5` in 0/7 despite broad genetics.
- Branch modules were weaker than the already-known IFN/HLA/CD74 state:
  `full_slc15a4_tasl_tlr_irf5_branch`, `endosomal_tlr_sensor_chaperone`, and
  `slc15a4_tasl_irf5_core` were trend-or-better in only 2/6 diseases.
- Genetics were branch-imbalanced: `IRF5` had Open Targets evidence in 9/12
  queried diseases, but `SLC15A4` only in SLE and `TASL_CXorf21` only in RA/SLE.
- Perturbation artifacts had 0 direct branch perturbation rows; Mixscale only
  supported downstream IFN/JAK/STAT controls.
- Prior art is crowded for lupus and endosomal TLR biology.

Integration:

- `SLC15A4/TASL/IRF5` is demoted to lupus-biased mechanistic comparator.
- It cannot be the V3 cross-autoimmune central node unless future direct
  perturbation data show non-lupus APC contexts are controlled by this branch.
- This demotion is consistent with the focused Geneformer screen, where
  `SLC15A4` and `IRF5` had 0 support contexts and `TASL` had only one
  low-cell-count support context.

## 2026-05-27 00:53 UTC

Negative-regulator feedback test completed.

Script:

- `scripts/v3_wave14_negative_regulator_feedback_test.py`

Outputs:

- `results_v3/wave14_negative_regulator_feedback/`

Question:

- `PTPN2`, `TNFAIP3`, and `SH2B3` have broad genetics and the strongest
  focused Geneformer support, but they are hard direct targets. I tested
  whether their donor-level expression anticorrelates with IFN/HLA/CD74
  modules, as a brake might, or positively tracks the modules, as feedback
  markers often do.

Result:

- 4,320 donor-level gene-module correlations were computed.
- `PTPN2`: median Spearman rho 0.337 across all-donor tests, 62
  feedback-like positive tests vs 6 brake-like negative tests.
- `SH2B3`: median rho 0.287, 56 feedback-like positive vs 9 brake-like
  negative.
- `TNFAIP3`: median rho 0.142, mixed but not a clean brake: 29
  feedback-like positive vs 12 brake-like negative.
- Positive-control state genes behaved as expected: `CD74` median rho 0.771,
  `CTSS` 0.620, `CIITA` 0.561.

Interpretation:

- The negative-regulator genes are not behaving like simple opposing brakes in
  local donor-level expression. They mostly track the inflammatory/APC state,
  likely as induced feedback or cell-state markers.
- This weakens the idea that a direct expression-based `PTPN2`/`TNFAIP3`/`SH2B3`
  state can be a therapeutic intervention point.
- Their strongest role remains genetic anchoring of cytokine/NF-kB/JAK
  dysregulation, not direct druggability.

## 2026-05-27 00:56 UTC

Wave-14 GSK3B/CIITA perturbation scout returned and was vetted.

Report:

- `subagents_v3/wave14_gsk3b_ciita_perturbation.md`

Script and outputs:

- `scripts/v3_wave14_gsk3b_ciita_perturbation.py`
- `results_v3/wave14_gsk3b_ciita_perturbation/`

Data:

- `GSE162463`: mouse macrophage IFN-gamma MHCII/CD40/PD-L1 CRISPR screen,
  processed normalized sgRNA counts.
- `GSE162464`: mouse macrophage NTC, `Gsk3b` KO, and `Med16` KO RNA-seq with
  and without IFN-gamma, triplicates.
- `GSE294918`: human macrophage IFN-gamma memory/ruxolitinib CPM table,
  descriptive only because one processed column per condition/timepoint is
  exposed.

Key result:

- `Gsk3b` knockout is a credible perturbation scout for preferentially reducing
  the IFN-gamma-induced CIITA/MHC-II/CD74 state in mouse macrophages.
- In `GSE162463`, `Gsk3b` ranked 39/11,701 for MHCII-low gate enrichment;
  median MHCII low/high log2 = 3.386, but genome-wide FDR was not significant
  under the worker's crude sgRNA summary.
- In `GSE162464`, `Gsk3b_IFNg_vs_NTC_IFNg` reduced the CIITA/MHC-II/CD74 module
  by -1.856 mean log2FC and the generic IFN core by -0.483, giving an absolute
  MHC/IFN ratio of 3.84.
- Gene-level effects included `Ciita` -1.791, `Cd74` -0.920, `H2-Aa` -3.497,
  `H2-Ab1` -2.143, `Stat1` -0.239, `Irf1` -0.379, and `Cxcl10` -1.452.
- Human ruxolitinib in `GSE294918` was broader: at D4/LPS0, CIITA/HLA-II/CD74
  module -1.079 and generic IFN core -3.184.

Interpretation:

- This is the first nontrivial intervention-controller evidence since the
  SLC15A4/TASL branch failed.
- It is not final target evidence. `GSK3B` is not IFN-neutral, has PD-L1 screen
  signal, is a broad kinase, and the positive perturbation data are mouse
  macrophage plus a human broad-JAK comparator rather than autoimmune tissue
  validation.
- Promotion would require human primary macrophage/DC replication, selectivity
  over WNT/metabolic/stress outputs, disease-breadth support, and prior-art
  clearance.

## 2026-05-27 01:00 UTC

Ran local recurrence and novelty gate for `GSK3B`/CIITA.

Script:

- `scripts/v3_wave14_gsk3b_local_gate.py`

Outputs:

- `results_v3/wave14_gsk3b_local_gate/gsk3b_local_gate_gene_summary.tsv`
- `results_v3/wave14_gsk3b_local_gate/gsk3b_local_gate_module_correlations.tsv`
- `results_v3/wave14_gsk3b_local_gate/gsk3b_prior_art_detail.json`
- `results_v3/wave14_gsk3b_local_gate/summary.json`

Result:

- `GSK3B` local disease recurrence is narrow: 1 FDR10-positive disease and
  2 trend-or-better diseases, both IBD (`Crohn disease`, `ulcerative colitis`).
- `GSK3B` did not reproduce as an MS microglial expression anchor in
  `GSE111972` (`delta_log2 = -0.132`, `hedges_g = -0.311`, `p = 0.475`).
- Correlation with IFN/HLA/CD74 modules is modest (`median Spearman r = 0.262`)
  and weaker than state markers (`CD74` median r = 0.829; `CIITA` median
  r = 0.575).
- Prior art is crowded for the target class and mechanism: 3,576 Europe PMC
  hits for `GSK3B`+autoimmune; 13,366 for `GSK3 inhibitor`+autoimmune; 1,073
  for `GSK3B`+CIITA/MHC-II/CD74.

Decision:

- `GSK3B` is not promoted. It remains a positive perturbation comparator for
  selective dampening of macrophage CIITA/MHC-II/CD74, not a V3 therapeutic
  claim.
- This demotion is important: the best perturbation result so far still fails
  breadth and novelty gates, so the next search must prioritize intervention
  points downstream/upstream of the recurrent state rather than expression of
  the controller itself.

## 2026-05-27 01:14 UTC

Integrated no-go target-level genetics audit.

Report:

- `subagents_v3/wave14_target_level_genetics.md`

Main outputs:

- `results_v3/wave14_target_level_genetics/target_level_genetics_truth_table.tsv`
- `results_v3/wave14_target_level_genetics/target_level_genetics_summary.json`

Result:

- No narrowed candidate has target-level coloc/MR support across the required
  autoimmune disease breadth.
- `IRF5`, `PTPN2`, `CLEC16A`, `SH2B3`, and `GPR65` are broad locus-level
  genetics priorities only.
- `CIITA`, `RFX5`, `GSK3B`, and `CD74` lack sufficient disease genetics for a
  target claim.

Decision:

- Treat the genetics channel as insufficient for all current direct target
  candidates unless new full GWAS/eQTL/pQTL summary-stat inputs are obtained.

## 2026-05-27 01:14 UTC

Integrated Wave15-B perturbation/drug-response scan.

Report:

- `subagents_v3/wave15_perturbation_drug_response.md`

Main outputs:

- `results_v3/wave15_perturbation_drug_response/ranked_direct_perturbations.tsv`
- `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`
- `results_v3/wave15_perturbation_drug_response/summary.json`

Result:

- No compound is nominated.
- `Med16_KO`, `RFX5` CRISPRi, and `Gsk3b_KO` define a desirable perturbation
  profile: reduce antigen-presentation module more selectively than generic
  IFN/JAK.
- Available chemical/L1000 evidence is too nonspecific and too far from
  autoimmune antigen-presentation assays.

Decision:

- Use this perturbation channel as a comparator constraint for any future
  target: a real intervention point should resemble `RFX5`/`MED16`/`GSK3B`
  selectivity without their druggability or prior-art liabilities.

## 2026-05-27 01:14 UTC

Ran orchestrator dependency and external gates around the recurrent HLA-II
state.

Scripts:

- `scripts/v3_wave15_orchestrator_dependency_scan.py`
- `scripts/v3_wave15_geneformer_loader_dependency_screen.py`
- `scripts/v3_wave15_loader_external_gate.py`

Outputs:

- `results_v3/wave15_orchestrator_dependency_scan/`
- `results_v3/wave15_geneformer_loader_dependency_delete/`
- `results_v3/wave15_loader_external_gate/`

Result:

- `CTSH` is the leading new fail-fast candidate among HLA-II loading /
  lysosomal dependency genes.
- Local scan: `CTSH` had 1 FDR10-positive disease, 3 trend-or-better
  expression diseases, 4 residual state-support diseases, and 5 raw
  state-support diseases.
- Expression support details:
  - Crohn epithelial: `delta = 0.0259`, `hedges_g = 2.049`, `p = 0.00766`,
    FDR within screen `0.1595`.
  - T1D acinar: `delta = 0.1364`, `hedges_g = 1.820`, `p = 0.0425`, FDR
    `0.6399`.
  - UC myeloid: `delta = 0.4187`, `hedges_g = 3.336`, `p = 0.000134`,
    FDR `0.0120`.
  - MS microglia: `delta = 0.1857`, `hedges_g = 0.419`, `p = 0.320`,
    FDR `0.912`, positive but not significant.
- Geneformer loader-dependency screen: `CTSH` had 3 support contexts
  (`psoriasis_macrophage`, `t1d_ductal`, `sjogren_APC`) but 0 strong support
  contexts.
- External gate: Open Targets `gwas_credible_sets` returned `CTSH` rows in
  T1D and MS, max score `0.974`, all locus-level only. ClinicalTrials.gov
  returned 0 hits for `CTSH OR "cathepsin H"`.

Interpretation:

- `CTSH` is interesting because it is an enzyme near HLA-II loading with some
  local dependency signal and MS/T1D locus-level genetics, while `CTSS` is
  saturated and `HLA-DM` is non-druggable.
- `CTSH` is not yet a finding. The foundation-model result is weak, local
  expression is not broad enough alone, genetics is not coloc/MR, and prior-art
  examples already include cathepsin-autoimmune MR papers.

Next step:

- Perform close prior-art and mechanism specificity review for `CTSH`:
  determine whether any published/preprint/patent already proposes cathepsin H
  modulation for MS/T1D or cross-autoimmune HLA-II antigen-presentation control.

## 2026-05-27 01:19 UTC

Integrated Wave15-A surface/trafficking dependency screen.

Script and report:

- `scripts/v3_wave15_surface_trafficking_dependency.py`
- `subagents_v3/wave15_surface_trafficking_dependency.md`
- `results_v3/wave15_surface_trafficking_dependency/`

Important correction from worker:

- A first thyroid Visium implementation used two-control sample-level z-scores,
  which inflated spatial deltas. The worker reran spot-level z-scoring against
  pooled control spots before sample aggregation. I accept the corrected output
  only.

Result:

- `CTSH` ranked as the top local `GO_SCOUT`: 5 trend-or-better disease-control
  diseases, 1 FDR10-positive disease, 8 residual state-coupling diseases, and 8
  raw state-coupling diseases.
- Biological anchors `HLA-DMA/HLA-DMB` were stronger for state biology but
  rejected as direct therapeutic intervention points.
- `CTSS`, `LGALS9`, and `LAPTM5` were also local scouts; prior-art and
  tractability keep them behind CTSH for the next fail-fast step.

Self-critique:

- The strongest CTSH evidence is residual coupling to the CD74/HLA state, not
  disease-control separation across all diseases. This is a dependency/state
  proximity signal, not causal proof.
- The celiac and thyroid routes remain weaker than curated single-cell disease
  atlases because celiac compartments are marker-derived and thyroid spatial
  sample counts are small.
- CTSH must survive novelty/prior-art and target-level genetics checks before
  any therapeutic language is justified.

## 2026-05-27 01:22 UTC

CTSH prior-art stress test changed the status from "active fail-fast lead" to
"active but heavily prior-art-shadowed scout."

Verified literature and metadata:

- Wu et al. 2024, `Medicine`, DOI `10.1097/MD.0000000000040268`, PMID
  `39470488`, "Cysteine cathepsins and autoimmune diseases: A bidirectional
  Mendelian randomization." Europe PMC metadata and abstract retrieved by code.
  Key reported effects: cathepsin H protective for celiac disease
  (`WR OR=0.881`, `95% CI=0.838-0.926`, `P=6.5e-7`) but risk-increasing for T1D
  (`IVW OR=1.121`, `95% CI=1.053-1.194`, `P=.0003`) and PBC (`WR OR=1.792`,
  `95% CI=1.062-3.024`, `P=.0288`).
- Lin et al. 2024, medRxiv DOI `10.1101/2024.09.05.24313125`, "The causal
  relationship between cathepsins and multiple sclerosis: a mendelian
  randomization study." Europe PMC preprint metadata retrieved by code. Reported
  cathepsin H/MS association: `IVW P=0.036`, `OR=1.095`,
  `95% CI=1.006-1.192`.
- Faraco et al. 2013, PLoS Genetics DOI `10.1371/journal.pgen.1003270`, already
  linked CTSH to antigen presentation in an autoimmune-like narcolepsy context.

Patent/tooling note:

- PatentsView API route failed by DNS resolution. This is a blocker for that
  specific patent API, not evidence of absence. Google Patents web search found
  broad CTSH/protease and immune-cell-activation patent mentions, but no
  immediate direct CTSH-for-MS/T1D/IBD treatment claim in the first pass.

Decision:

- Do not claim novelty for "CTSH genetically linked to autoimmune disease" or
  "CTSH genetically linked to MS."
- If CTSH remains, the claim must be sharply narrower: cross-disease HLA-II
  loading-state dependency plus intervention feasibility. That narrower claim
  currently has weak foundation-model support and no selective compound.

## 2026-05-27 01:26 UTC

Integrated GSE227835 myasthenia breadth worker.

Script/report/output:

- `scripts/v3_wave14_gse227835_myasthenia_marker.py`
- `subagents_v3/wave14_myasthenia_breadth.md`
- `results_v3/wave14_gse227835_myasthenia/`

Result:

- 40 processed PBMC matrices and 444,357 cells parsed.
- Marker-derived B/APC-like PBMCs show strong lysosomal/APC module recurrence:
  AChR-positive MG vs healthy `g=2.252`, `FDR=0.0111`; untreated MG vs healthy
  `g=1.729`, `FDR=0.0111`.
- Seronegative MG myeloid/APC-like cells show lipid-loader support.
- Seronegative pre-treatment B/APC-like and plasmablast-like compartments show
  negative HLA-II/CD74 and IFNG/HLA-II/CD74 trends.

Interpretation:

- MG extends disease breadth for a compartment-specific lysosomal/APC axis.
- MG is a boundary condition against a universal HLA-II/CD74 model and against
  any therapeutic claim that assumes all autoimmune compartments share the same
  APC gate.

## 2026-05-27 01:31 UTC

Accepted Wave16 CTSH critique and alternatives comparison.

Decision:

- Demote `CTSH` from active intervention lead to local dependency scout/reference.
- Keep `CTSH` useful as a future wet-lab peptidome perturbation comparator
  because it is near HLA-II loading and less clinically saturated than `CTSS`.
- Do not use `CTSH` to satisfy the V3 central-node/intervention DoD.

Reasons:

- Direct cathepsin/autoimmune MR prior art exists for CTSH, including MS,
  T1D/PBC/celiac.
- Direction is conflicted: published MR reports CTSH protective in celiac but
  risk-increasing in T1D/PBC.
- Geneformer support is weak: 3 support contexts, 0 strong contexts, and mixed
  projection directions.
- Disease-control recurrence is not broad enough; the strongest CTSH evidence
  remains coupling to the existing HLA/CD74 state.
- ChEMBL scratch pull indicates CTSH has fewer public molecules than CTSS/CTSB/
  CTSL and substantial cross-cathepsin molecule overlap; a formal reproducible
  script is being run as `scripts/v3_wave16_ctsh_chembl_feasibility.py`.

Alternative routes:

- `LAPTM5`: best novelty-first contingency but poor modality.
- `CTSS`: best enzyme comparator but prior-art/clinical-history blocked.
- `LGALS9`: accessible extracellular checkpoint, but crowded and directionally
  complex.
- Perturbation-derived route now looks more honest: `Med16_KO` produces the
  desired selective target-module suppression. Test whether Mediator kinase
  (`CDK8/CDK19`) or another druggable Mediator-module handle can mimic that
  profile without broad IFN collapse.

## 2026-05-27 01:35 UTC

Formal CTSH ChEMBL feasibility audit completed.

Script/output:

- `scripts/v3_wave16_ctsh_chembl_feasibility.py`
- `results_v3/wave16_ctsh_chembl_feasibility/`

Result:

- ChEMBL targets pulled: CTSH (`CHEMBL2225`), CTSS (`CHEMBL2954`), CTSB
  (`CHEMBL4072`), CTSL (`CHEMBL3837`), CTSK (`CHEMBL268`), CTSZ
  (`CHEMBL4160`).
- Summary no-go reasons from the script:
  - CTSH has fewer public ChEMBL molecules than CTSS/CTSB/CTSL.
  - Median retained CTSH potency is micromolar-to-weak.
  - A substantial fraction of CTSH molecules also have records against other
    cysteine cathepsins.
  - Only 3 pulled molecules met an observed >=10x CTSH selectivity heuristic,
    and absence of comparator records is not proof of selectivity.

Interpretation:

- This reinforces CTSH demotion. CTSH remains enzyme-druggable in principle,
  but the public chemistry/selectivity package is too weak for V3 intervention
  promotion.

## 2026-05-27 01:38 UTC

Mediator/CDK8-CDK19 route gate completed.

Script/output:

- `scripts/v3_wave17_mediator_route_gate.py`
- `results_v3/wave17_mediator_route_gate/`

Result:

- Verdict: `PARK_AS_PERTURBATION_DERIVED_INTERVENTION_HYPOTHESIS`.
- The positive clue remains strong: `Med16_KO` in GSE162464 has target-module
  effect `-3.140`, generic IFN effect `-0.798`, selectivity score `2.305`.
- ChEMBL supports druggability of the Mediator kinase route:
  - CDK8 `CHEMBL5719`: 953 retained activity rows, 848 unique molecules,
    median potency 396 nM.
  - CDK8/Cyclin C complex `CHEMBL3038474`: 714 rows, 689 molecules, median
    21.8 nM.
  - CDK19/Cyclin C complex `CHEMBL3883323`: 159 rows, 156 molecules, median
    11.0 nM.
- The gate blocks promotion:
  - CDK8/CDK19 local expression recurrence is weak, max 1 positive disease.
  - No direct CDK8/CDK19 inhibitor perturbation dataset is integrated that
    proves Med16_KO phenocopy in autoimmune APCs.
  - Mediator kinase inhibition likely affects broad transcriptional and
    inflammatory programs; selectivity over generic IFN remains unproven.

Interpretation:

- This route is more mechanistically causal than CTSH because it starts from a
  perturbation, but it still fails current DoD promotion. It should be held for
  an ex vivo APC assay or perturbation-data search, not turned into a target
  claim.

## 2026-05-27 01:39 UTC

ACOD1/IRG1-itaconate cross-domain fail-fast.

Reason for test:

- Europe PMC returned recent work linking IRG1/itaconate immunometabolism with
  autoimmune/inflammatory disease, including EAE/MHC-II/macrophage biology.

Local check:

- `ACOD1` in `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
  is positive in only 2 diseases: Crohn disease and ulcerative colitis.
- Best compartments: Crohn myeloid delta `5.08`, p `0.0018`; UC myeloid delta
  `3.69`, p `0.037`.
- No MS anchor in local table; no broad cross-autoimmune recurrence in the
  current datasets.

Decision:

- Do not pivot the V3 central node to ACOD1/itaconate. It remains an IBD-biased
  immunometabolism comparator and possible cross-domain mechanistic note.

## 2026-05-27 01:47 UTC

Integrated formal CTSH chemistry/selectivity worker return.

Report/output:

- `subagents_v3/wave16_ctsh_chemistry_selectivity.md`
- `scripts/v3_wave16_ctsh_chemistry_selectivity.py`
- `results_v3/wave16_ctsh_chemistry_selectivity/`

Accepted result:

- `CTSH` public chemistry is not selective enough for a V3 therapeutic route.
- ChEMBL retained 47 CTSH potency molecules; 41 had at least one requested
  cathepsin comparator assay; 0 had an observed 100x margin over all assayed
  comparators and only 1 had an observed 10x margin.
- IUPHAR/GtoPdb lists only two curated CTSH inhibitor interactions and both
  lack determined selectivity.
- AlphaFold/PDB coverage is adequate for assay design but does not overcome
  papain-family catalytic-site conservation or safety concerns.

Decision:

- Keep CTSH only as a lysosomal/APC-state biology marker and possible future
  wet-lab readout.
- Do not nominate CTSH inhibition or activation as the intervention point.

## 2026-05-27 01:49 UTC

Integrated marker-compartment GSE253006 tofacitinib analysis.

Script/output:

- `scripts/v3_analyze_gse253006_tofacitinib_marker_compartments.py`
- `results_v3/gse253006_tofacitinib_marker/`

Result:

- Dataset processed: 23 samples, 97,004 cells, 11 baseline samples
  (5 responders, 6 nonresponders), 103 selected genes.
- Marker-derived compartments: ambiguous 8,427 cells; B/plasma-like 40,209;
  epithelial-like 14,585; myeloid/APC-like 11,712; stromal/endothelial-like
  6,353; T-cell-like 15,718.
- Baseline responder vs nonresponder separation failed after correction. Top
  responder-high result was stromal/endothelial JAK/STAT mean score
  delta `0.160`, Hedges g `1.002`, p `0.256`, FDR `0.976`.
- Paired responder pre/post testing showed pharmacodynamic decreases, strongest
  in T-cell-like `mixscale_validated_ifng_readout` high fraction:
  mean delta `-0.114`, p `0.000395`, FDR `0.0869`.

Interpretation:

- This is a stronger operationalization than the earlier sample-level score
  because it separates marker-derived compartments.
- It does not support a baseline stratification biomarker.
- It weakly supports that successful tofacitinib exposure can reduce the IFN/
  antigen-presentation readout in responders, but the effect is not sufficient
  for a new therapeutic-relevant V3 claim.

## 2026-05-27 05:53 UTC

Integrated Wave18-A treatment-response scout after local verification.

Script/output:

- `scripts/v3_wave18_treatment_response_scout.py`
- `results_v3/wave18_treatment_response/`
- `subagents_v3/wave18_treatment_response_scout.md`

Verified result:

- `GSE138746` rheumatoid arthritis anti-TNF sorted bulk produced 2,115
  sample-module rows and 162 response tests. No baseline predictor survived
  correction; minimum FDR was `0.6056`. Top nominal row: CD4 T-cell
  adalimumab `ifn_apc`, 19 responders vs 18 nonresponders, delta `+0.586`,
  Hedges g `+0.913`, p `0.00763`, FDR `0.606`.
- `GSE253006` ulcerative colitis tofacitinib marker-compartment baseline
  predictor remained negative; minimum baseline FDR was `0.976`.
- `GSE183047` psoriasis secukinumab pharmacodynamics was analyzable after
  downloading and extracting `GSE183047_RAW.tar` (`286,566,400` bytes).
  Myeloid/APC `lysosomal_apc` mean score decreased nominally in 4 paired
  patients (mean delta `-0.208`, p `0.0198`, FDR `0.743`), while the expected
  keratinocyte IL-17 inflammation decrease was also only nominal at this
  module-test scope (mean delta `-0.524`, p `0.0157`, FDR `0.743`).

Decision:

- Do not pursue a baseline treatment-response biomarker claim from the current
  V3 module readouts.
- Retain tofacitinib/secukinumab pharmacodynamic decreases only as weak
  mechanism-supporting comparator evidence.

## 2026-05-27 05:55 UTC

Integrated Wave18-B accessible/druggable state-component rescue.

Script/output:

- `scripts/v3_wave18_accessible_target_rescue.py`
- `results_v3/wave18_accessible_target_rescue/`
- `subagents_v3/wave18_accessible_target_rescue.md`

Verified result:

- 24 candidates screened; `0 GO`, `11 PARK`, `13 NO_GO`.
- Top parked comparators/readouts: `ITGAM`, `CD44`, `CD274`, `ITGAX`,
  `TYROBP`, `CD24`, `MSR1`, `LILRB2`, `SIRPA`, `GPNMB`, `CHI3L1`.
- The best accessible routes fail for different reasons: recurrence below
  threshold (`ITGAM`), crowded/directionally ambiguous axis (`CD44`, `CD274`),
  confounder dominance (`ITGAX`, Fc/complement), weak state coupling (`CD24`,
  `LILRB2`, `SIRPA`), or direct local contradiction (`GPNMB`, TAM/galectin
  routes).

Decision:

- No accessible extracellular/surface/enzyme target is currently promotable as
  the V3 intervention point.
- Next pivot must leave the obvious accessible-state-marker space and ask for
  upstream tolerogenic controllers, lysosomal stress regulators, or a narrower
  lead-indication mechanism that still has cross-disease breadth.

## 2026-05-27 05:57 UTC

Integrated Wave18-C foundation-model rescue.

Script/output:

- `scripts/v3_wave18_foundation_rescue.py`
- `results_v3/wave18_foundation_rescue/`
- `subagents_v3/wave18_foundation_rescue.md`

Verified result:

- 109 candidates had Geneformer token coverage.
- 46 candidates were stronger than the previous `CTSH` Geneformer baseline by
  relative embedding-deletion metrics.
- Strict intersection of stronger-than-CTSH Geneformer support with direct
  real perturbation rescue was empty.
- Screen-only relative Geneformer candidates: `TMSB10`, `SEC61A1`, `CD74`,
  `CD300E`, `PTPN2`.
- Real perturbation-supported but not Geneformer-rescued candidates:
  `GSK3B`, `RFX5`.

Decision:

- Foundation-model outputs remain useful as triage/veto evidence, not as
  promotion evidence.
- Do not elevate `CD300E`, `PTPN2`, or `GPR65`; local breadth/residual and
  Geneformer checks already contradict them as central cross-disease nodes.

## 2026-05-27 06:04 UTC

Ran orchestrator-side Wave19 controller triage.

Script/output:

- `scripts/v3_wave19_orchestrator_controller_triage.py`
- `results_v3/wave19_orchestrator_controller_triage/`

Result:

- 69 checkpoint, lysosomal/lipid-controller, SHP/SOCS/JAK, NRF2, and nuclear
  lipid-sensor genes screened against existing V3 local evidence tables.
- Calls: `66 DEMOTE_LOCAL_TRIAGE`, `3 PARK_FOR_WORKER_REVIEW`, `0
  FOLLOW_UP_NOW`.
- Parked genes:
  - `LIPA`: local score `15.25`, 3 broad positive diseases and 1 negative,
    surface residual support in 5 diseases, but confounder-dominant in 6 and
    Wave18 foundation table says model support is contradicted by the
    `GSE162463` screen.
  - `CD274`: local score `12.75`, broad positive in 4 diseases and no broad
    negative disease, but Wave18-B already parked it for below-threshold state
    support and extreme checkpoint prior-art saturation.
  - `NPC1`: local score `10.25`, surface residual support in 7 diseases, but
    broad expression recurrence is weak, MS white-matter direction is negative,
    and confounder dominance is high.

Decision:

- No local immediate-promotion candidate. Wave19 workers should treat these as
  stress-test candidates, not leads.
- The added SHP-1/PTPN6, SOCS, JAK/TYK2, NRF2, BCL6, PPAR/RXR, and macrophage
  transcription-factor branch did not add a survivor. `JAK1/JAK2/TYK2` remain
  generic IFN/JAK controls; `BCL6`/`NFE2L2` are IBD/T1D-skewed locally;
  `PTPN6` has MS literature plausibility but no local cross-disease expression
  recurrence in this V3 table.

## 2026-05-27 06:08 UTC

Ran orchestrator-side Wave20 unrestricted survivor triage.

Script/output:

- `scripts/v3_wave20_orchestrator_unrestricted_triage.py`
- `results_v3/wave20_orchestrator_unrestricted_triage/`

Result:

- 13 prior unrestricted `hold` or `test_or_scout` candidates screened against
  recurrence, MS anchor, residual gate, Geneformer/foundation support, ChEMBL
  local activity counts, and OpenTargets local genetics.
- Calls: `8 DEMOTE_LOCAL_TRIAGE`, `5 PARK_FOR_WORKER_REVIEW`, `0
  FOLLOW_UP_NOW`.
- Parked stress-test candidates:
  - `DAP`: score `18.0`, 3 positive diseases, nominal MS anchor, combined
    Geneformer support 7 contexts / 2 strong contexts, residual retained
    positive diseases 2, but no ChEMBL nM activity and Wave18 foundation says
    model support is contradicted by `GSE162463`.
  - `SNX10`: score `14.5`, 3 positive diseases, nominal MS anchor, combined
    Geneformer support 6 contexts / 1 strong context, residual retained
    positive diseases 2, but no ChEMBL activity and no real perturbation
    alignment.
  - `FMNL2`: score `12.5`, 4 positive diseases, nominal MS anchor, weak
    Geneformer support and no real perturbation or ChEMBL activity.
  - `C15ORF48`: score `12.0`, 3 positive diseases, nominal MS anchor and 3
    retained residual positive diseases, but absent from current Geneformer
    token route and no ChEMBL activity.
  - `CBX3`: score `11.0`, 4 positive diseases and 3 retained residual positive
    diseases, but generic chromatin/proliferation biology and model
    contradiction.

Decision:

- Wave20 survivor branch has candidates worth worker review, but none are
  currently promotable because the modality/perturbation gate is empty.

## 2026-05-27 06:09 UTC

Tested `C15ORF48/MOCCI` versus `NDUFA4` complex-IV subunit-switch pattern.

Reason:

- `C15ORF48` emerged from the unrestricted survivor branch and public work
  links MOCCI/C15ORF48 to mitochondrial complex-IV remodeling, autophagy,
  oxidative-stress control, and autoimmunity.
- A stronger mechanistic claim would require not just `C15ORF48` induction but
  the predicted reciprocal `NDUFA4` repression.

Script/output:

- `scripts/v3_wave20_c15orf48_ndufa4_switch.py`
- `results_v3/wave20_c15orf48_ndufa4_switch/`

Result:

- 17 local compartments tested using existing broad h5ad contrasts plus MS
  white-matter microglia.
- Switch calls:
  - `canonical_switch_c15_up_ndufa4_down`: 1 compartment.
  - `c15_up_no_ndufa4_up`: 5 compartments.
  - `ndufa4_up_without_c15`: 3 compartments.
  - `both_up_not_switch`: 1 compartment.
  - `no_switch_signal`: 7 compartments.
- Only Crohn colon myeloid showed the canonical switch:
  `C15ORF48` delta `+3.882`, p `0.000614`, FDR `0.0848`;
  `NDUFA4` delta `-0.292`, p `0.0794`, FDR `0.457`.
- UC myeloid had stronger `C15ORF48` induction (`+4.446`, p `2.95e-05`,
  FDR `0.0287`) but `NDUFA4` was essentially unchanged (`-0.088`, p `0.630`).
- T1D endothelial/stellate/ductal/acinar compartments showed `C15ORF48`
  induction without `NDUFA4` repression.

Decision:

- `C15ORF48/MOCCI` remains a plausible inflammation-resolution/autophagy
  biology note, but the local data do not support a broad autoimmune
  complex-IV subunit-switch mechanism.
- Do not promote `C15ORF48` as V3 central node or intervention point without
  direct perturbation and a modality.

## 2026-05-27 06:14 UTC

Integrated Wave19-B lysosomal/lipid-controller audit.

Report/output:

- `subagents_v3/wave19_lysosomal_controller.md`
- `scripts/v3_wave19_lysosomal_controller.py`
- `results_v3/wave19_lysosomal_controller/`

Vetting:

- `summary.json` gives 35 candidates, 12 routes, and no promoted GO route.
- `route_summary.tsv` matches the report: `LIPA/LAL_enhancement` is `PARK`;
  `NPC1/NPC2_cholesterol_egress` is `PARK_READOUT`; `LRRK2_inhibition` is
  `PARK_DISEASE_SPECIFIC`; TFEB/TFE3, MCOLN1/TRPML1, PIKFYVE, PPAR/LXR,
  GBA/GBA2, and generic mTOR/autophagy routes are `NO_GO`.

Decision:

- Accept the negative call. The local module is detectable, but upstream
  lysosomal/lipid-controller routes either lack local recurrence/state support,
  are confounded by generic APC/myeloid state, have wrong intervention
  direction, or are blocked by broad prior art/liability.
- Keep LIPA/NPC1/NPC2 as perturbation/readout controls only; do not use them as
  V3 therapeutic central nodes.

## 2026-05-27 06:17 UTC

Integrated Wave19-A tolerogenic/checkpoint-controller audit.

Report/output:

- `subagents_v3/wave19_tolerogenic_checkpoint.md`
- `scripts/v3_wave19_tolerogenic_checkpoint.py`
- `results_v3/wave19_tolerogenic_checkpoint/`

Vetting:

- Reran the script locally. The regenerated `summary.json` reports 29
  candidates and no promoted candidates.
- Counts match the report: `PROMOTE: 0`, `PARK: 5`, `PARK_LOW: 6`,
  `NO_GO: 18`.
- Parked comparator axes are `CD274`, `CD24`, `BTLA`, `CD200`, and `CD47`.

Decision:

- Accept the negative call. Checkpoint pharmacology is plausible in general,
  but the V3 evidence does not support a novel cross-autoimmune
  lipid-lysosomal/APC intervention through these axes.
- Reasons: missing state coupling for most axes, intervention direction
  mismatch for phagocytosis checkpoints, weak perturbation/foundation support,
  and heavy prior-art saturation for PD-1/PD-L1, CD24Fc/SIGLEC10,
  CD200/CD200R, CD47/SIRPA, and TIM-3/TIGIT-related routes.

## 2026-05-27 06:18 UTC

Integrated Wave20-A unrestricted survivor stress test.

Correction:

- An earlier `wait_agent` call used a mistyped path ending in `bb3c`; the
  correct Wave20-A path is `019e6809-cdca-7821-bbba-dd1a1d6668ef`.
- The correct agent returned, so this is not a silent subagent loss.

Report/output:

- `subagents_v3/wave20_unrestricted_survivor.md`
- `scripts/v3_wave20_unrestricted_survivor.py`
- `results_v3/wave20_unrestricted_survivor/`

Vetting:

- Reran the script locally.
- `summary.json` reports `promoted_targets: []`, `least_bad_comparator:
  SNX10`, and no strict core-residual survivor except adjacent `CBX3` in one
  UC stromal analysis.

Decision:

- Accept the negative call. `SNX10` is the least-bad fail-fast comparator
  because it has Crohn/UC myeloid recurrence, weak Geneformer support, and
  public macrophage/colitis perturbation literature, but it fails strict
  residual specificity, tractable modality, safety/repair, and novelty.
- Do not promote `C15ORF48`, `DAP`, `FMNL2`, `NCK1`, `TNFAIP8L1`, `PPIL3`,
  `PLEK2`, `SEL1L3`, `AQR`, or adjacent `CBX3/CHI3L1/LTA4H/PPP3CA/CXCL9`.

## 2026-05-27 06:23 UTC

Integrated Wave20-B genetic/druggable alternate-axis scout.

Report/output:

- `subagents_v3/wave20_genetic_druggable_altaxis.md`
- `scripts/v3_wave20_genetic_druggable_altaxis.py`
- `results_v3/wave20_genetic_druggable_altaxis/`

Vetting:

- Reran the script locally. It completed with `promoted_count: 0`; the only
  runtime issue was a pandas mixed-type warning when reading a TSV, not an
  analysis failure.
- `negative_ranked_shortlist.tsv` ranks `PTPN2`, `SH2B3`, `CLEC16A`,
  `ATG16L1`, `OSMR`, `GPR65`, `IRF5`, `CARD9`, `IL10`, `TNFAIP3`, `IL6R`, and
  `TYK2`; all are `NO_GO`.

Decision:

- Accept the negative call. Genetics-first breadth exists, especially for
  `SH2B3`, `PTPN2`, `IRF5`, `ATG16L1`, `CLEC16A`, `IL10`, `TNFAIP3`, and
  `TYK2`, but none supplies the required intersection of target-level
  specificity, correct-direction druggability, perturbation support, and
  novelty.
- Do not pivot to generic TYK2/JAK/IFN, IL-6R, IL-10, IRF5, PTPN2 inhibitor,
  or broad autophagy/mitophagy claims without a new modality or
  biomarker-defined population delta.

## 2026-05-27 06:24 UTC

Wrote `CONVERGENCE_CHECK_5.md`.

Decision:

- Current evidence supports a recurring autoimmune tissue state, not a target.
- The next non-redundant move is a programmatic scan for strict-residual,
  externally druggable candidates outside the exhausted candidate lists.
- Guardrail: demote generic IFN/JAK/proteasome/core-machinery hits unless a
  new population, delivery, or intervention-direction delta is explicit.

## 2026-05-27 06:26 UTC

Dispatched Wave21.

- Wave21-A / Pauli:
  `019e681b-d8c0-70b0-b47d-fa09ae1bd75b`, independent local/API
  residual-druggability scan.
- Wave21-B / Hooke:
  `019e681c-23d7-75c1-aefc-51cf7068cd1e`, hostile novelty/modality review for
  residual candidates.

Dispatch notes:

- First spawn attempt failed because full-history fork cannot override worker
  settings.
- Second Wave21-B attempt initially hit the thread limit; closed already-vetted
  completed agents and retried successfully.

## 2026-05-27 06:31 UTC

Ran orchestrator-side Wave21 residual-druggability scan.

Script/output:

- `scripts/v3_wave21_residual_druggability_scan.py`
- `results_v3/wave21_residual_druggability_scan/`

Result:

- 271 residual candidates considered.
- Top 80 were checked against ChEMBL and UniProt APIs with cached raw responses.
- Calls: `0 FOLLOW_UP_NOW`, `0 PARK_PRIOR_ART_REVIEW`,
  `8 PARK_LOCAL_RESIDUAL_ONLY`, `72 DEMOTE_WAVE21`.
- Parked residual-only genes:
  - `ATOX1`, `TPM4`, `LDLRAD3`, `SQLE`: two strict residual diseases, both IBD
    stromal analyses, retained positive disease count 3.
  - `CFB`, `TIMP1`, `COL4A1`, `CBX3`: one strict residual disease each or
    prior generic demotion.

Decision:

- Do not promote any Wave21 local candidate. The best residual genes fail
  breadth and/or modality gates. `SQLE` is enzymatic and has ChEMBL evidence,
  but the local strict residual signal is IBD-stromal only and MS white matter
  trends negative. `LDLRAD3` is membrane-localized but has unclear biology and
  no ChEMBL support. `ATOX1` lacks an autoimmune-safe modality and implicates
  copper homeostasis. `CFB/TIMP1/COL4A1` are complement/remodeling readouts
  without a cross-autoimmune causal package.

## 2026-05-27 06:32 UTC

Performed narrow local fail-fast on residual-adjacent druggable-looking genes.

Genes checked from local tables:

- `IL15`, `CD82`, `IFITM2`, `IFITM3`, `PSME1`, `PSME2`, `POMP`
- `SQLE`, `ATOX1`, `LDLRAD3`

Result:

- `IL15`, `CD82`, `IFITM2/3`, `PSME1/2`, and `POMP` show five-disease
  expression breadth in the broad h5ad table, but they lose strict residual
  specificity after core module adjustment.
- `IL15` has retained residual support in only two diseases and no strict
  core-covariate survival; local signal is compatible with tissue stress or
  inflammatory NF-kB/HIF/APC coupling rather than a central cross-autoimmune
  node.
- `CD82` has one retained residual disease and no strict survival.
- `IFITM2/3` and `PSME1/2/POMP` are consistent with IFN/proteasome stress
  programs; the Wave21 guardrail demotes them unless a new selective modality
  or population delta emerges.
- `SQLE`, `ATOX1`, and `LDLRAD3` have stricter residual support but mainly in
  Crohn/UC stromal analyses. That is not enough for a V3 cross-autoimmune
  therapeutic claim.

Decision:

- Do not pivot to IL-15, tetraspanin CD82, IFITM antiviral proteins,
  immunoproteasome/proteasome maturation, SQLE sterol synthesis, ATOX1 copper
  chaperoning, or LDLRAD3 without new evidence from the Wave21 workers.

## 2026-05-27 06:36 UTC

Integrated Wave21-A / Pauli residual-druggability worker return.

Report/output:

- `subagents_v3/wave21_residual_druggability_scan.md`
- `scripts/v3_wave21_residual_druggability_scan.py`
- `results_v3/wave21_residual_druggability_scan/`

Vetting:

- The worker refined and overwrote the rough orchestrator-side script/output in
  the same assigned write scope. This is acceptable because the worker owned
  that Wave21-A path, but it means the retained `summary.json` now reflects the
  worker's stricter scan rather than my first 80-candidate API pass.
- The current `summary.json` reports 26 strict-residual candidates:
  `1 GO_REVIEW`, `5 PARK_REVIEW`, `20 NO_GO`.
- `GO_REVIEW` is explicitly defined as hostile-review routing, not a target
  promotion.

Result:

- `SQLE` is the only `GO_REVIEW` candidate. Evidence: strict residual in Crohn
  and UC stromal compartments, retained positives in 3 diseases, broad
  positives in 4 diseases, ChEMBL `CHEMBL3592` with 99 activity records, and
  UniProt enzyme annotation.
- SQLE blockers: no local genetics, no perturbation support, no MS anchor, and
  strict survival is IBD-stromal only.
- `LDLRAD3`, `C1QTNF1`, `TGM2`, `REG1A`, and `PTPRE` are `PARK_REVIEW` but
  have incomplete direction, modality, genetics/MS support, or perturbation.

Decision:

- Send `SQLE` and the parked review candidates through Hooke's hostile
  prior-art/modality review. Do not promote them without a direct rebuttal of
  the current blockers.

## 2026-05-27 06:38 UTC

Corrected time accounting.

- User clarified that usage-limit waiting time does not count as working time.
- I wrote `TIME_ACCOUNTING_V3.md`.
- The major observed non-working gap is approximately 2026-05-27 01:53 UTC to
  05:53 UTC.
- Current active-work estimate is about 7 hours 57 minutes, so the Hour 12
  milestone is not yet due despite the wall-clock approaching 06:41 UTC.

Decision:

- Continue active research. Do not write Hour 12 milestone documents until
  active-time accounting reaches twelve hours or a true breakthrough is ready.

## 2026-05-27 06:39 UTC

Integrated Wave21-B / Hooke hostile prior-art/modality review.

Report/output:

- `subagents_v3/wave21_residual_candidate_prior_art.md`
- `results_v3/wave21_residual_candidate_prior_art/`

Vetting:

- `candidate_prior_art_gate.tsv` has 18 reviewed candidates plus header.
- `external_query_log.tsv` has 126 exact source-query rows plus header.
- Raw API/HTML captures exist under `raw_api/`.

Result:

- No candidate promoted.
- `SQLE` remains only a conditional stress-test comparator. It has an enzyme
  modality but is IBD/stromal-skewed, MS-negative, sterol-repair-confounded,
  and prior-arted outside the V3 biology.
- `CFB`, `IL15`, `IL7R`, `CXCL8`, and `HIF1A` are useful comparator controls
  for "druggable but prior-art/generic" failures, not target openings.
- `PSME1/2`, `POMP`, and `IFITM2/3` are demoted as proteasome/IFN machinery.
- `ATOX1`, `LDLRAD3`, `CD82`, `TIMP1`, `PDPN`, `PTPRE`, and `C1QTNF1` lack a
  clean intervention direction or mature autoimmune-ready modality.

Decision:

- Wave21 closes without a target. The next non-redundant move is not another
  expression/prior-art rank. If `SQLE` is kept alive, it must be killed or
  strengthened by perturbation/foundation evidence and non-IBD replication.

## 2026-05-27 06:55 UTC

Wave22 SQLE fail-fast stress test completed.

- Script: `scripts/v3_wave22_sqle_failfast.py`.
- Output: `results_v3/wave22_sqle_failfast/`.
- Runner: added to `run_v3_analysis.sh`.
- Decision: `NO_GO_SQLE_FAILFAST`.

Traceable generated numbers:

- Broad SQLE positivity: 4 diseases, 0 negative diseases.
- Strict core-covariate residual survival: 2 diseases, limited to Crohn
  disease stromal and ulcerative colitis stromal.
- Non-IBD retained residual support: 1 disease.
- MS white-matter anchor: `ms_wm_delta_log2 = -0.3408177110309154`,
  `ms_wm_p = 0.3307572199460259`.
- Geneformer triage: 3 support contexts, 1 strong context, but real
  perturbation alignment is `model_contradicted_by_gse162463_screen`.
- GSE162463 MHC-II direction: `mhcii_low_enrichment_contradictory`.
- LINCS compound metadata includes 5 known SQLE inhibitor names, but 0 SQLE-like
  rows appear in existing L1000 disease-signature reversal outputs and the
  LINCS metadata rows lack target/MOA annotation.
- Prior-art review: `CONDITIONAL_NO`; old antifungal/oncology/metabolic SQLE
  inhibitor art and no V3-specific autoimmune delta.

Decision:

- SQLE is a useful stress-test comparator, not a target nomination.
- Close the residual/druggability rescue branch. The next wave must use
  independent channels rather than re-ranking residual expression.

## 2026-05-27 07:08 UTC

Wave23 orchestrator-side non-expression route triage completed.

- Script: `scripts/v3_wave23_orchestrator_nonexpression_axis_triage.py`.
- Output: `results_v3/wave23_orchestrator_nonexpression_axis_triage/`.
- Runner: added to `run_v3_analysis.sh`.
- Scope: 16 route-level hypotheses spanning metabolite/barrier circuits,
  genetics-first restoration, and treatment-response stratification; 56 genes
  checked; ChEMBL API snapshots cached under `raw_api/`.

Initial bug/reformulation:

- The first run over-counted treatment-response evidence by counting arbitrary
  p-value columns. I inspected the Wave18 treatment-response tables and
  tightened the gate to corrected baseline response signals only. This demoted
  the biomarker route from `PARK_REVIEW` to `NO_GO`.

Corrected result:

- Route calls: `2 PARK_REVIEW`, `14 NO_GO`, `0 GO_REVIEW`.
- `GPR65_pH_endolysosomal_gpcr`: `PARK_REVIEW`; 5 OpenTargets credible-set
  diseases at score >= 0.5, 2 at >= 0.8; ChEMBL target with 99 scanned activity
  records and best observed activity 364.84 nM; no positive perturbation/model
  alignment and prior-art/crowding blocker remains.
- `PTPN2_TCPTP_restoration`: `PARK_REVIEW`; 8 OpenTargets credible-set diseases
  at score >= 0.5, 4 at >= 0.8; 4 broad-positive expression diseases; 5
  Geneformer support contexts; model/GSE162463 alignment relative to CTSH; but
  the therapeutic direction is restoration, while available chemical matter is
  inhibitory/wrong-direction.
- Baseline module-response biomarker route: `NO_GO`; 10 nominal RA baseline
  associations, 0 corrected baseline associations, and 1 corrected
  pharmacodynamic signal. This is not a stratification finding.

Decision:

- The next useful focus is not a broad route table. It is a hostile feasibility
  test of the two PARK routes: can GPR65 overcome prior art and perturbation
  absence, or can PTPN2 restoration be made feasible with current biotech
  modality?

## 2026-05-27 07:18 UTC

Integrated Wave23-B / Wegener genetics-restoration modality scout.

Report/output:

- `subagents_v3/wave23_genetics_restoration_modality.md`
- `scripts/v3_wave23_genetics_restoration_modality.py`
- `results_v3/wave23_genetics_restoration_modality/`

Vetting:

- `py_compile` passed for the worker script.
- The report is internally consistent and does not promote a target.
- Worker call counts: `0 GO`, `2 PARK`, `12 NO_GO`.
- Worker parks `GPR65` and `IL10`; all other restoration candidates are
  `NO_GO`.

Integrated interpretation:

- `GPR65`: still a parked comparator. It has a feasible GPCR agonist/PAM
  modality and broad-ish genetics, but local evidence is weak/contradictory and
  IBD/GPR65 modulator prior art is direct.
- `IL10`: worker parks it because augmentation is technically feasible, but it
  remains blocked by recombinant/engineered IL-10 prior art and no local V3
  biomarker or disease-cell rescue delta. I keep it below `GPR65`/`PTPN2` for
  V3 purposes.
- `PTPN2`: worker demotes it more harshly than the orchestrator table. I accept
  the demotion as the stronger call because the available chemistry is
  inhibitor/wrong-direction and no TCPTP activator/restorer was found.

Decision:

- No genetics-restoration route is a therapeutic nomination.
- `GPR65`, `IL10`, and `PTPN2` can remain as named comparator branches for
  future wet-lab/tooling needs, but none currently satisfies the V3 DoD.

## 2026-05-27 07:24 UTC

Wave24 perturbation-first recurrent L1000 reversal triage completed.

- Script: `scripts/v3_wave24_l1000_recurrent_reversal_triage.py`.
- Output: `results_v3/wave24_l1000_recurrent_reversal/`.
- Runner: added to `run_v3_analysis.sh`.
- Inputs: `results_v3/l1000fwd_compound_summary.tsv`,
  `results_v3/wave15_perturbation_drug_response/l1000fwd_selectivity_compound_rank.tsv`,
  and `results_v3/pde4_camp_l1000_audit_summary.json`.

Result:

- 284 L1000 compound rows, 144 opposite-mode rows, 123 grouped compounds.
- 20 compounds recur across at least two opposite-mode queries.
- Promotion gates: `62 NO_GO`, `61 PARK_UNKNOWN_ONLY`, `0 PARK_REVIEW`.
- Known recurrent opposite hits are dominated by HSP90/cell-cycle/stress
  targets, ATPase/cytotoxic compounds, glucocorticoids, and generic/prior
  inflammatory targets (`CXCR2`, `PPARA`, `CTSB`).
- Unknown recurrent BRD compounds exist, but without target/MOA deconvolution
  they cannot support a therapeutic claim.
- PDE4/cAMP remains weak: core PDE4/cAMP compounds are present in LINCS
  metadata but absent from top opposite hits in the existing audit.

Decision:

- Perturbation-first L1000 recurrence does not nominate a drug.
- This is a useful negative result because it rules out a superficially strong
  "recurring reversal" shortcut: the recurrence is mostly cytotoxic/stress or
  unresolved chemistry, not a translational autoimmune mechanism.

## 2026-05-27 07:31 UTC

Integrated Wave23-D / Carver hostile critique.

Report:

- `subagents_v3/wave23_hostile_critique.md`

Accepted criticisms:

- `GPR65` remains weak: local disease/module evidence is weak or contradictory,
  no perturbation/model rescue exists, and IBD/GPR65 modulator prior art is
  direct.
- `PTPN2` remains a modality failure: inhibitor chemistry cannot be counted as
  autoimmune druggability when the required direction is TCPTP restoration.
- The baseline biomarker branch should remain closed unless two independent
  response-labeled cohorts pass a pre-specified interaction/prediction bar.
- My route triage scoring can launder weak evidence if Geneformer support or
  ChEMBL ligand existence is counted without direct perturbation and
  correct-direction modality.
- The neglected non-redundant route is target-resolved causal genetics to
  module state.

Action:

- Wrote `CONVERGENCE_CHECK_7.md`.
- Demote all current PARK labels (`GPR65`, `PTPN2`, `IL10`, unknown L1000 BRDs)
  to comparator/future-data-needed.
- Next forcing question: can available local/public data resolve target-level
  genetic causality and direction to module state for any plausible node?

## 2026-05-27 07:05 UTC

Integrated Wave23-A / Noether metabolite-barrier circuit scout.

Report/output:

- `subagents_v3/wave23_metabolite_barrier_circuit.md`
- `scripts/v3_wave23_metabolite_barrier_circuit.py`
- `results_v3/wave23_metabolite_barrier_circuit/`

Result:

- 7 metabolite/barrier routes audited.
- Calls: `7 NO_GO`, `0 PARK`, `0 GO`.
- Closest biological signal: AHR/tryptophan via `IDO1`/`KYNU`, but it lacks
  strict residual survival, local genetics, and L1000 reversal support.
- Least crowded route: FXR/TGR5 bile-acid sensing, but it is locally
  unsupported and has weak CNS/MS relevance in the current data.

Decision:

- Treat metabolite/barrier circuits as a negative gate, not as a target source.
- Do not use AHR/tryptophan, FXR/TGR5, PPAR/LXR, SCFA/HCAR/FFAR, S1P,
  retinoid/VDR, or eicosanoid routes for a V3 therapeutic claim without new
  direct perturbation and target-level evidence.

## 2026-05-27 07:07 UTC

Wave25 target-resolved genetics-to-module proxy audit completed.

- Script: `scripts/v3_wave25_causal_genetics_module_proxy.py`.
- Output: `results_v3/wave25_causal_genetics_module_proxy/`.
- Runner entry added: `run_v3_analysis.sh`.
- Validation: `py_compile` passed and the script ran to completion.

Result:

- 206 candidates audited.
- Proxy calls:
  - `1 COLOC_NEEDED_NOT_CLAIMABLE`
  - `14 MODULE_MARKER_NOT_GENETICALLY_ANCHORED`
  - `191 NO_GO_CAUSAL_PROXY`
- `0` candidates have proper target-resolved coloc/MR feasibility in the local
  evidence table.
- The local GWAS Catalog parquet is readable (`1,067,194` rows, `38` columns)
  but remains top-association/catalog schema, not coloc-sufficient SNP-level
  summary statistics.
- `PTPN2` is the only `COLOC_NEEDED_NOT_CLAIMABLE` candidate: broad autoimmune
  locus/eQTL/module evidence exists, but no target-resolved SNP-level causal
  result and no correct-direction TCPTP restoration modality are available.

Decision:

- Do not claim cross-disease genetic anchoring for any central node.
- Current best interpretation: the lipid-lysosomal/APC module is replicated as
  a disease cell state, but target causality remains unresolved. `PTPN2` is a
  future coloc/restoration-modality work item, not a therapeutic nomination.
- The next pivot should not be another mapped-gene genetics score. It should
  either use a truly independent response-labeled cohort / perturbation dataset
  or seek an intervention point whose causal direction is already supported by
  real perturbation data.

## 2026-05-27 07:13 UTC

Wave26 strict treatment-response audit completed.

- Script: `scripts/v3_wave26_treatment_response_strict_audit.py`.
- Output: `results_v3/wave26_treatment_response_strict_audit/`.
- Runner entry added: `run_v3_analysis.sh`.
- Validation: `py_compile` passed and the script ran to completion.

Reason for audit:

- Wave18 said no RA baseline predictor survived global correction.
- Wave23-C output contained a `GO` for `GSE138746` anti-TNF / adalimumab
  `CD4_T_cell` `ifn_apc`, based on within-analysis-scope FDR.
- This was a likely proxy-satisficing risk, so I re-scored it under global
  baseline-search correction and independent replication requirements.

Result:

- Baseline rows audited: 207.
- Prior Wave23 `GO` rows: 1.
- Strict claim-allowed rows: 0.
- The prior `GO` row is demoted:
  - within-scope p = 0.007628, within-scope FDR = 0.068654
  - global baseline FDR = 0.773794
  - global generic-adjusted FDR = 0.971730
  - independent same-module/direction replication count = 0

Decision:

- The RA anti-TNF IFN/APC baseline signal is a future hypothesis, not a V3
  stratification biomarker finding.
- Treatment-response does not currently provide a therapeutic-relevant claim.

## 2026-05-27 07:20 UTC

Wave27 L1000 unknown perturbagen deconvolution completed.

- Script: `scripts/v3_wave27_l1000_unknown_deconvolution.py`.
- Output: `results_v3/wave27_l1000_unknown_deconvolution/`.
- Runner entry added: `run_v3_analysis.sh`.
- Validation: first run failed because merging LINCS metadata created duplicate
  `cmap_name` columns; fixed by using `class_cmap_name`. `py_compile` and rerun
  then passed.

Result:

- Unknown Wave24 parked compounds audited: 62.
- Recurrent unknown compounds audited: 6.
- Candidate promotion calls:
  - `61 NO_GO`
  - `1 PARK_EXTERNAL_TARGET_LOOKUP_ONLY`
- Recurrent unknown compounds resolve as:
  - `BRD-A20131130`: 2',5'-dideoxyadenosine / purine-cAMP class, no-go
  - `BRD-K53561341`: Aurora-A inhibitor, no-go oncology/cell-cycle
  - `BRD-K92301463`: 16,16-dimethyl-PGE2, no-go prostanoid prior/generic
  - `BRD-K33583600`: isoliquiritigenin, no-go pleiotropic natural product
  - `BRD-K05197617` and `BRD-K35024477`: unresolved BRD structures, no-go
    because target/MOA cannot be inferred locally

Decision:

- The L1000 unknown-BRD escape route does not yield a repurposing or target
  claim.
- No perturbagen route currently connects selective target engagement to
  reversal of the cross-autoimmune lipid-lysosomal/APC module.

## 2026-05-27 07:26 UTC

Wave28 target-first rescue audit completed.

- Script: `scripts/v3_wave28_target_first_rescue.py`.
- Output: `results_v3/wave28_target_first_rescue/`.
- Runner entry added: `run_v3_analysis.sh`.
- Validation: `py_compile` passed and the script ran to completion twice. The
  first run exposed a ClinicalTrials.gov v2 parsing weakness: `totalCount` is
  absent unless `countTotal=true` is requested. I fixed the query to use
  target-specific `query.term`, autoimmune `query.cond`, and `countTotal=true`,
  then reran.

Reason for pivot:

- The module-first route keeps returning state markers rather than intervention
  handles. Wave28 reverses the search: start from druggable target-first axes
  (`LRRK2`, `RIPK1`, `NLRP3`, `IRAK4`, `BTK`, `CSF1R`, `SYK`, `PDE4B/D`,
  `PIK3CG`, `FAAH`, `TSPO`, `PTGER4`, `ALOX5`, and the strongest local
  genetics/module candidates) and require them to reconnect to the V3 module
  through genetics, local cell-state evidence, perturbation/foundation support,
  correct-direction modality, and novelty/prior-art gates.

Result:

- Candidates audited: 26.
- Promotion calls:
  - `0 GO_TO_HOSTILE_NOVELTY_REVIEW`
  - `1 PARK_REQUIRES_TARGET_CAUSALITY_OR_PERTURBATION`
  - `25 NO_GO_TARGET_FIRST`
- The only parked target is `SQLE`, and the park is not a finding:
  - broad positive disease count = 4
  - strict residual disease count = 2
  - target-level genetics gate = false
  - perturbation/foundation gate = false
  - gate failures: `no_target_level_genetic_anchor`;
    `no_real_selective_perturbation_or_validated_foundation_support`
- `PTPN2` remains the best mechanistic genetics-proxy comparator but still
  fails the promotion bar:
  - genetics diseases >= 0.5 = 8
  - module gate = true
  - perturbation/foundation gate = true only in the weak
    `triage_only_gse162463_not_promotion_grade` sense
  - hard failures: `no_correct_direction_druggable_modality`;
    `prior_art_or_clinical_saturation`

Decision:

- Target-first rescue does not currently yield a therapeutic-relevant claim.
- `SQLE` is now a clearly bounded future branch: it would need target-level
  genetics or real perturbation evidence, not more residual expression.
- `PTPN2` remains the causal-genetics/restoration-modality benchmark, but a
  TCPTP activator/restorer and target-resolved coloc/MR are both missing.
- Continue; active time is still below the twelve-hour floor after excluding
  usage-limit waiting time.

## 2026-05-27 07:34 UTC

Wave29 PTPN2 restoration model completed, after one downscope.

- Script: `scripts/v3_wave29_ptpn2_restoration_model.py`.
- Output: `results_v3/wave29_ptpn2_restoration_model/`.
- Runner entry added: `run_v3_analysis.sh`.
- Validation: `py_compile` passed and the reduced script ran to completion.

Failed attempt:

- Initial version used 750 parameter samples per condition. With 5 inflammatory
  input settings, 3 baseline PTPN2-activity settings, and 8 interventions, that
  implied 90,000 ODE solves. It was still running after about 90 seconds.
- I killed the process and reduced the sweep to 125 samples per condition,
  explicitly documenting the downscope in the script. Final outputs contain
  1,875 effect rows per intervention.

Result:

- Under the predefined selective-window rule, no intervention reaches a
  selective therapeutic window:
  - `ptpn2_restore_to_75pct`: selective-window fraction = 0.0; median
    APC/lipid-module drop = 0.051; median host-defense drop = 0.166
  - `ptpn2_restore_to_100pct`: selective-window fraction = 0.0; median
    module drop = 0.094; median host-defense drop = 0.281
  - `ptpn2_restore_to_125pct`: selective-window fraction = 0.0; median
    module drop = 0.130; median host-defense drop = 0.365
  - `jak_70pct_inhibition`: selective-window fraction = 0.0; median module
    drop = 0.161; median host-defense drop = 0.362
- Even supranormal PTPN2 restoration does not suppress the APC/lipid module by
  >=30% without excessive generic IFN/TNF host-defense suppression in this
  model.

Decision:

- PTPN2 is further demoted from therapeutic target nomination to
  genetics/mechanism benchmark. It remains biologically important, but the
  model does not support a plausible selective restoration window under current
  assumptions.
- This is not a proof that PTPN2 is non-causal. It is a stop-loss on claiming a
  feasible intervention without a real TCPTP-restoration perturbation dataset or
  target-resolved coloc/MR.

## 2026-05-27 07:44 UTC

Wave30 upstream niche-driver audit and reformulation.

Question after Wave28/Wave29 failures: can an upstream ligand/receptor or niche
driver explain the recurrent cross-autoimmune IFN/HLA-II/CD74/GILT/APC state and
provide a more selective intervention point than direct module markers?

Added and ran `scripts/v3_wave30_niche_driver_audit.py`.
Output directory: `results_v3/wave30_niche_driver_audit/`.

First run exposed a bad operationalization: I let global `ifn_apc` module
breadth count as support for every upstream axis annotated to that state. That
inflated OSM/OSMR, CD40/CD40LG, CD24/SIGLEC10, CCL2/CCR2, and similar branches
despite little candidate-specific recurrence. I patched the script so
candidate-specific ligand/receptor evidence is required separately from global
module breadth. This is the same failure mode the medical review warned about:
a statistically tidy surrogate was biologically too weak.

Corrected Wave30 result:

- `18` upstream/niche axes audited.
- `0` `GO_TO_HOSTILE_NOVELTY_REVIEW`.
- `4` `CENTRAL_STATE_DRIVER_NOT_SELECTIVE_THERAPEUTIC`.
- `14` `NO_GO_NICHE_DRIVER`.

Corrected top centrality axes:

- `IFNG_IFNGR_JAK_STAT1_CIITA`: candidate-specific breadth `7`, global module
  breadth `14`, centrality score `20.64`; fails selectivity and prior-art gates.
- `MIF_CD74_CXCR4_CD44`: candidate-specific breadth `6`, global breadth `14`,
  centrality score `18.33`; fails selectivity and prior-art gates.
- `LILRB_HLA_INHIBITORY_MYLOID_CHECKPOINT`: candidate-specific breadth `7`,
  centrality score `18.07`; fails target-causality, druggable-direction, and
  selectivity gates.
- `SPP1_CD44_INTEGRIN_RETENTION`: candidate-specific breadth `5`, centrality
  score `12.01`; fails target-causality, selectivity, and prior-art gates.

High intervention-score comparators still fail:

- `PTPN2_TCPTP_RESTORATION`: intervention score `5.10`, but after the
  candidate-specific correction it has candidate-specific breadth `0` in this
  ligand/receptor audit and keeps the Wave29 modality/selectivity failures.
- `SLC15A4_TASL_IRF5_ENDOLYSOSOMAL_TLR`: intervention score `4.85`, but lacks
  candidate-specific cross-disease local support and target-selective
  perturbation.
- `GPR65_ENDOLYSOSOMAL_PH_CAMP`: intervention score `3.50`, but lacks local
  residual/state and perturbation support.

Interpretation: the upstream-niche framing strengthens the mechanistic story
that the recurrent module is an IFN/HLA-II/CD74/GILT antigen-presentation state
with MIF/CD74, LILRB/HLA, and SPP1/CD44/integrin neighborhoods. It does not
produce a therapeutic target under the V3 DoD. The next viable route should not
be another static ligand/receptor score; it should look for a dynamic transition
controller that can decouple HLA-II/CD74 antigen presentation from generic
IFN/JAK host-defense collapse, or else pivot out of this module.

## 2026-05-27 07:53 UTC

Wave31 dynamic transition-controller audit completed.

Question after Wave30: can any perturbation selectively decouple the recurrent
HLA-II/CD74/GILT antigen-presentation transition from generic IFN/JAK
host-defense genes, while mapping to a tractable cross-autoimmune intervention?

Added and ran `scripts/v3_wave31_dynamic_transition_controller_audit.py`.
Output directory:
`results_v3/wave31_dynamic_transition_controller_audit/`.
Runner entry added to `run_v3_analysis.sh`.

Inputs integrated:

- Wave15 direct perturbation/drug-response tables.
- Wave17 Mediator kinase route verdict.
- Wave24 recurrent L1000 reversal audit.
- Wave25 causal genetics/module proxy matrix.
- Wave28 target-first rescue matrix.
- Wave14 local cross-disease gene summary.

Result:

- `17` dynamic-controller/intervention candidates audited.
- `0` `GO_TO_HOSTILE_NOVELTY_REVIEW`.
- `1` `PARK_STRONG_PERTURBATION_NO_DRUGGABLE_HANDLE`.
- `2` `PARK_SELECTIVE_PERTURBATION_BUT_TRANSLATION_BLOCKED`.
- `9` `NO_GO_L1000_ONLY_CONTROLLER`.
- `5` `NO_GO_DYNAMIC_CONTROLLER`.

Top candidates:

- `MED16`: dynamic-controller score `7.36`; primary mouse macrophage `Med16_KO`
  suppresses the target antigen-presentation module by `3.14` mean log2FC units
  while suppressing the generic IFN module by `0.80`; margin `2.34`. It fails
  because MED16 has no direct druggable handle, no translational phenocopy, and
  no cross-disease target support.
- `CDK8_CDK19_MEDIATOR_KINASE`: score `7.11`; inherits the MED16 perturbation
  clue as a hypothetical Mediator-kinase handle, but Wave17 already found no
  direct autoimmune APC inhibitor phenocopy plus broad IFN/IL-10/Treg prior art.
  It fails translational phenocopy, cross-disease target support, and prior-art
  gates.
- `GSK3B`: score `1.93`; primary macrophage `Gsk3b_KO` partially suppresses the
  target module (`1.62`) with generic IFN suppression (`0.80`), but fails
  cross-disease support and prior-art gates.
- L1000 top-ranked targets (`LRRK2`, `CTSB`, `FAAH`, `CTNNB1`, `MKNK1`,
  `CXCR2`, `PIK3CG`, `MAPK14`, `PLK1`, `RARG`, `HSP90AA1`) fail because the
  signal is L1000-only, cytotoxic/stress-prone, lacks immune-cell perturbation
  support, lacks cross-disease target support, or is prior-art saturated.

Decision:

- The dynamic-controller route does not produce a therapeutic claim.
- The strongest mechanistic perturbation remains `MED16_KO`, but the absence of
  a druggable, validated phenocopy prevents nomination.
- I will not convert a strong perturbation comparator into a therapeutic target
  by assuming CDK8/CDK19 inhibitors are equivalent; the existing data explicitly
  do not show that.
- Next pivot: move away from direct suppression of the IFN/HLA-II/CD74 module
  and search for a cross-disease intervention that changes lesion/tissue
  outcome downstream of the state, especially efferocytosis, lipid clearance,
  resolution macrophage switching, or tissue repair. This is a different
  therapeutic question: not "turn off antigen presentation," but "make the
  inflammatory lipid-lysosomal state resolve without host-defense collapse."

## 2026-05-27 08:12 UTC

Wave32-C prior-art and translational-feasibility attack completed for
downstream resolution-axis interventions.

Question: among efferocytosis/lipid-clearance/resolution routes, which are not
already blocked by prior art, wrong therapeutic direction, tissue-delivery
failure, or unavailable modality?

Added and ran `scripts/v3_wave32c_resolution_prior_art_audit.py`; output:
`results_v3/wave32c_resolution_prior_art_audit/`. Added runner entry to
`run_v3_analysis.sh`.

The script queried PubMed, Europe PMC, ClinicalTrials.gov, ChEMBL, PubChem, and
generated Google Patents/Espacenet search URLs. It produced `70` source
queries, `146` target/drug database rows, and `46` patent-search URLs. A first
ClinicalTrials query for `AL002 TREM2` was too restrictive; I patched the script
to query `AL002` and `INVOKE-2` separately. The rerun correctly captured AL002
phase 1/2 Alzheimer trials (`NCT03635047`, `NCT04592874`) as translational
precedent for TREM2 agonism.

Curated outputs:

- `WAVE32C_PRIOR_ART_AUDIT.md`
- `results_v3/wave32c_resolution_prior_art_audit/route_feasibility_ranked.tsv`

Ranked result:

1. `specialized_pro_resolving_mediator_FPR2_axis`: least blocked, but immature.
   PubMed query count `545`; no `FPR2 agonist` autoimmune trial found. Needs
   biased agonist, tissue PK/PD, and efferocytosis/lipid-resolution perturbation
   data.
2. `CD300_family_modulation`: not blocked, but direction-ambiguous. No
   ClinicalTrials.gov autoimmune CD300 antibody trials found; receptor-specific
   direction is unresolved.
3. `NPC1_NPC2_cholesterol_egress`: not autoimmune-prior-art blocked, but
   translationally weak and readout-like.
4. `LIPA_LAL_enhancement`: no autoimmune sebelipase trial found, but existing
   LAL-D modality does not solve immune selectivity or CNS delivery.
5. `MERTK_AXL_TAM_GAS6_PROS1_agonism`: mechanistically relevant but partly
   blocked/crowded by TAM autoimmune literature and MERTK antibody patents.
6. `GPNMB_non_depleting_repair_handle`: marker/handle only; direct MS repair
   route crowded by PPARgamma-GPNMB remyelination prior art.
7. `TREM2_agonism`: blocked for novelty by EAE/MS remyelination biology, AL002
   clinical precedent, and TREM2 agonist patents.
8. `LXR_ABCA1_ABCG1_activation`: blocked by EAE prior art and LXR metabolic
   safety liabilities.
9. `PPAR_RXR_retinoid_modulation`: blocked by saturated autoimmunity/remyelination
   prior art and broad metabolic/retinoid toxicity.
10. `TAM_receptor_inhibition`: oncology chemical matter exists but direction is
    wrong for resolution/efferocytosis.
11. `GPNMB_depletion_ADC`: oncology route; wrong direction for autoimmune repair.

Decision:

- Do not spend more V3 effort on generic LXR, PPAR/RXR, TREM2, TAM inhibition,
  or GPNMB depletion.
- If Wave32 continues, the only downstream routes with plausible novelty
  whitespace are FPR2/SPM-biased agonism and receptor-specific CD300 modulation.
- These routes still need real perturbation evidence in disease-relevant myeloid
  systems. A clean literature whitespace audit is not enough for a therapeutic
  finding.

## 2026-05-27 08:01 UTC

Wave32 downstream-resolution rescue audit completed.

Question after Wave31: if direct HLA-II/CD74/GILT suppression is not tractable,
can the downstream lipid-lysosomal inflammatory state be pushed into
efferocytosis, lipid clearance, and tissue repair without collapsing generic
host defense?

Added and ran `scripts/v3_wave32_resolution_rescue_audit.py`.
Output directory: `results_v3/wave32_resolution_rescue_audit/`.
Runner entry added to `run_v3_analysis.sh`.

Inputs integrated:

- Existing V3 cross-disease gene summaries, broad h5ad rank, residual gate,
  surface/dependency screens, accessible target rescue, foundation rescue,
  checkpoint audit, lysosomal-controller audit, controller triage, Wave25
  genetics proxy matrix, Wave28 target-first matrix, direct perturbation
  synthesis, and L1000 summaries.
- Fresh cached snapshots from Europe PMC, ClinicalTrials.gov, and ChEMBL for
  audited route genes. These are saturation/druggability snapshots, not proof
  of novelty or causal support.

Audited routes:

- TAM/MERTK/AXL/TYRO3/GAS6/PROS1 efferocytosis agonism.
- TREM2/APOE/TYROBP/LPL lipid repair.
- LXR/ABCA1/ABCG1 cholesterol efflux.
- PPAR/RXR resolution.
- LIPA/LAL enhancement.
- NPC1/NPC2 cholesterol egress.
- GPNMB repair-state handle.
- CD200/CD200R, CD300 family, SIRPA/CD47, IL10, NRF2, MAF/KLF4 routes.

Result:

- `14` routes audited.
- `0` `GO_TO_HOSTILE_NOVELTY_REVIEW`.
- `1` `PARK_RESOLUTION_BIOLOGY_NO_CAUSAL_ANCHOR`.
- `1` `NO_GO_RESOLUTION_PRIOR_ART_BLOCKED`.
- `8` `NO_GO_RESOLUTION_MARKER_OR_UNVALIDATED_ROUTE`.
- `4` `NO_GO_RESOLUTION_ROUTE`.

Top route interpretations:

- `NPC1_NPC2_CHOLESTEROL_EGRESS` has the highest numeric score (`9.33`) only
  because it shares state-coupling/readout structure. It fails local breadth,
  MS anchor, density/confounder, causal/perturbation, and validation gates.
  This is a readout route, not an intervention claim.
- `TREM2_APOE_LIPID_REPAIR` is the only parked branch. It has local breadth
  `4`, state coupling `5`, and an MS anchor, but it fails density/confounder,
  genetic/real perturbation, prior-art, and independent-validation gates. It is
  a strong repair-biology comparator, not a V3 therapeutic claim.
- `LIPA_LAL_ENHANCEMENT` again shows local breadth/state evidence (`4`/`5`)
  but lacks an MS anchor, fails density/confounder and causal/perturbation
  gates, and remains blocked by prior V3 delivery/repair-prior-art issues.
- `TAM_EFFEROCYTOSIS_AGONISM` and `MERTK_CENTERED_EFFEROCYTOSIS` remain
  mechanistically attractive but fail local breadth, MS anchor, density,
  causal/perturbation, correct-direction modality maturity, and prior-art gates.

Decision:

- The downstream-resolution route is biologically plausible but not promotable.
- I will preserve `TREM2_APOE_LIPID_REPAIR`, `NPC1/NPC2`, `LIPA`, and
  `MERTK/TAM` as comparators and wet-lab-experiment suggestions, but none meets
  the V3 DoD as a target.
- Pending: integrate Wave32 subagent reports and use them either to reopen a
  route with specific perturbation/prior-art evidence or to pivot again.

## 2026-05-27 08:04 UTC

Wave32-A cross-autoimmune efferocytosis/lipid-clearance target scan completed
as a scoped evidence-synthesis branch, not a V3 finding.

Report: `WAVE32A_EFFEROCYTOSIS_RESOLUTION_SCAN.md`.

Question: among downstream resolution/tissue-repair nodes for the shared
lipid-lysosomal inflammatory myeloid/APC module, is there a tractable
intervention point that avoids broad suppression of IFN/HLA-II host defense?

Integration with existing V3 evidence:

- Automated Wave32 local audit still promotes no target. Its only parked route
  is `TREM2_APOE_LIPID_REPAIR`; `LIPA`, `NPC1/NPC2`, `GPNMB`, `CD300`, and TAM
  efferocytosis routes remain no-go/readout/marker branches under local gates.
- Wave32-A adds an external literature synthesis and identifies `FPR2/ALX` plus
  `ANXA1` biased pro-resolution agonism as the best new follow-up branch, not
  because it is pan-autoimmune proven, but because it has a druggable GPCR,
  direct colitis efferocytosis pharmacology, lupus-nephritis macrophage
  mechanistic support, and local V3 Crohn/UC myeloid `FPR2` signal.
- `FPR2` is not claimable for MS: local Wave23 table has MS white-matter delta
  `-0.93`, p `0.372`, and there is no MS lesion perturbation anchor.

Ranked conclusion:

- Best follow-up branch: biased `FPR2/ALX` pro-resolution agonism, with IBD or
  lupus nephritis as lead-indication validation before any MS bridge.
- Strongest cross-disease efferocytosis mechanism: `MERTK/GAS6/PROS1` TAM
  restoration, but modality is inverted because mature chemical matter mostly
  inhibits TAM receptors.
- Strongest MS repair comparator: `TREM2/APOE/LPL`, but TREM2 agonist antibody
  results are conflicted and cross-autoimmune support is marker/confounder
  dominated.
- `GPNMB`, `LIPA`, `NPC1/2`, `APOE`, `LPL`, and `ABCA1/ABCG1` remain readouts
  or state markers unless direct perturbation proves controller status.

## 2026-05-27 08:16 UTC

Wave32-B dataset availability scan completed.

Question: is there enough real public perturbation data to test downstream
resolution/efferocytosis/lipid-clearance candidates locally, without repeating
the weak expression-only operationalization that prior reviews criticized?

Outputs:

- `subagents_v3/wave32b_perturbation_dataset_availability_scan.md`
- `results_v3/wave32b_dataset_availability_scan/candidate_dataset_matrix.tsv`

Searches:

- GEO/NBCI E-utilities and GEO FTP for candidate-target terms.
- ArrayExpress/BioStudies API; useful hits were mainly GEO mirrors for TREM2.
- Local LINCS/CMap metadata and prior V3 L1000 outputs.
- Local State/Geneformer availability notes.

Result:

- `32` datasets/resources catalogued and TSV-validated.
- `15` rows are primary or primary-screen grade for immediate analysis.
- Best local test stack:
  - `GSE156234`: MerTK+/+ vs MerTK-/- efferocytosis single-cell transcriptome.
  - `GSE212008`: primary BMDM genome-wide CRISPR efferocytosis screen.
  - `GSE169160`: human CD14 macrophage apoptotic-cell efferocytosis and
    LXR/PPARD program.
  - `GSE325329`: IFNg/IL10-polarized BMDM apoptotic Treg/Tconv phagocytosis;
    key safety dataset for "resolution without generic IFN collapse."
  - `GSE302857` with `GSE66926`/`GSE70475`: Trem2KO demyelination microglia.
  - `GSE100260`, `GSE243117`, `GSE285961`: LIPA loss/gain.
  - `GSE274954`: GPNMB mutant BMDMs +/- OxLDL.
  - `GSE254406`/`GSE273340`/`GSE287142`: LXR/RXR/RAR mechanism comparators.

Negative/weak availability:

- No credible `CD300*` macrophage perturbation transcriptome found.
- Direct `AXL`, `TYRO3`, and `PROS1` perturbation transcriptomes remain weak or
  absent; `GSE205267` is only a bulk tissue GAS6/AXL context.
- LINCS/CMap and Geneformer/State can be used only as low-weight triage or
  veto layers; they cannot substitute for the real perturbation datasets above.

Decision:

- Next implement a Wave32-B analysis script against the primary datasets,
  scoring resolution/efferocytosis gain, lipid-lysosomal/APC reduction, generic
  IFN preservation, and stress penalty.

## 2026-05-27 08:21 UTC

Wave34-A genetics-first target rescue completed locally.

Scope: scan broad autoimmune genetics surfaces for druggable targets missed by
expression-first screens, while treating GWAS Catalog mapped-gene overlap as
weak unless backed by local credible-set/eQTL/coloc-like evidence.

Outputs:

- Script: `scripts/v3_wave34a_genetics_first_target_rescue.py`.
- Report: `subagents_v3/wave34a_genetics_first_target_rescue.md`.
- Results: `results_v3/wave34a_genetics_first_target_rescue/`.
- Runner: added to `run_v3_analysis.sh`.

Inputs:

- Local OpenTargets credible-set and disease-score TSVs.
- Local GWAS Catalog parquet autoimmune subset (`15,875` rows scanned).
- Wave14, Wave20, Wave23, Wave25, Wave28, and Wave33 V3 genetics/target
  tables.
- ChEMBL, GTEx, Europe PMC, and ClinicalTrials.gov lightweight public APIs.

Result:

- `23` genetics-first/druggable candidates audited.
- Calls: `0` promoted, `7` parked, `16` demoted.
- Parked candidates: `IRF5`, `IL10`, `PTPN22`, `FAP`, `GPR65`, `CCR6`,
  `TNFRSF14`.
- `CD226` did not pass the strict rescue gate despite 14 local GWAS Catalog
  autoimmune trait labels, because it lacks local OpenTargets credible-set
  support, GTEx eQTL support in the queried relevance panel, and V3 local
  cell-state support.

Interpretation:

- The genetics-first route did not produce a claim-ready target.
- `CD226` remains a reviewer-suggested validation question, not a promoted
  target: the next requirement is formal disease GWAS/cis-eQTL or pQTL coloc
  plus T/NK cell-state validation.
- `SH2B3`, `PTPN2`, `TNFAIP3`, `CLEC16A`, and `ATG16L1` reinforce broad
  autoimmune genetics but fail correct-direction druggability.
- `TYK2`, `IL23R`, `IL2RA`, `CTLA4`, `IL6R`, and `CD6` are positive controls
  for genetic/druggability convergence but demoted for direct prior-art
  saturation.

## 2026-05-27 08:47 UTC

Corrected Wave35 perturbation analysis after finding a gene-mapping artifact.

Problem found:

- Ensembl-indexed perturbation datasets in Wave35 originally had very low
  module gene coverage: 9/28 resolution genes and 3/27 lipid/APC genes in
  several datasets.
- Inspection showed that Ensembl REST timeouts had been cached as empty mapping
  responses. This is a computational artifact, not biological absence.

Fix:

- Patched `scripts/v3_wave35_resolution_perturbation_analysis.py`.
- Added exact-symbol MyGene.info fallback mapping for mouse symbols.
- Changed mapping logic so failed Ensembl cache entries are not treated as
  successful mappings.
- Reran the script in the pinned V3 Python environment
  `./.venv_v3_py312/bin/python`.

Corrected coverage:

- `GSE253577`, `GSE325329`, `GSE274954`, and `GSE287142` now recover 28/28
  resolution genes, 21/27 lipid/APC genes, 13/15 IFN genes, 11/11 stress
  genes, and 6/7 fibrosis genes.
- Mapping entries increased from 12 to 78.

Corrected result:

- Datasets analyzed: 10.
- Contrasts: 29.
- Module contrast rows: 145.
- Strict controller-like contrasts: 0.
- Resolution-without-IFN-collapse contrasts: 5, led by cuprizone microglia
  lesion-state comparisons, IL10-polarized phagocytic macrophages, and aged
  CNS myeloid bexarotene response.

Interpretation:

- The corrected analysis strengthens the negative conclusion: no tested
  downstream perturbation produces the desired pattern of resolution gain,
  lipid/APC-state reduction, IFN preservation, no stress, and no profibrosis.
- The positive-looking contexts are not clean intervention points:
  cuprizone microglia increase resolution together with lipid/APC and IFN;
  IL10 phagocytic macrophages increase resolution modestly but do not reduce
  lipid/APC; aged CNS myeloid bexarotene has modest resolution gain but RXR
  agonism is broad and prior-art crowded.

Next decision:

- Dispatch Wave36 to test whether a gene-level controller is hidden by module
  averaging and to run a hostile critique of the corrected perturbation route.

## 2026-05-27 08:58 UTC

Integrated Wave36, Wave37, and Wave38.

Wave36-B hostile critique:

- Report: `subagents_v3/wave36b_hostile_critique.md`.
- Verdict: pivot away from active resolution/efferocytosis target discovery.
- Key criticism accepted: corrected Wave35 fixes mapping but still tests mixed
  state modules; several mapped datasets are effectively panel-normalized after
  mapping and are therefore acceptable for negative stress testing but not for
  subtle target promotion.

Wave36-A gene-level controller rescue:

- Script: `scripts/v3_wave36a_gene_level_controller_rescue.py`.
- Results: `results_v3/wave36a_gene_level_controller_rescue/`.
- Report: `subagents_v3/wave36a_gene_level_controller_rescue.md`.
- Result: no gene-level perturbation controller rescued. The permissive scan
  found 9 submodule-gate contexts and 13 gene-rescue-shaped contexts but 0
  promotion-ready target routes. `RXR/LXR` is one-dataset-only; `LIPA` lacks
  direction consistency across 3 datasets; `GPNMB`, `IL10`, `MERTK/TAM`, and
  `TREM2` fail replication, direction, stress/fibrosis, or route plausibility.

Wave37 direct efferocytosis CRISPR screen:

- Script: `scripts/v3_wave37_gse212008_crispr_efferocytosis_screen.py`.
- Data: `GSE212008`, 74,674 sgRNAs, 19,672 genes.
- Results: 214 genes passed a permissive KO-enhances-efferocytosis consistency
  gate; 54 passed a KO-impairs-efferocytosis consistency gate.
- Canonical resolution candidates did not rescue the route: `MERTK`, `TREM2`,
  `FPR2`, `ANXA1`, `LIPA`, `GPNMB`, `RXRA`, and `IL10` were unresolved rather
  than clean KO-enhancer hits.
- `FCGRT` emerged as a superficially tractable KO-enhancer signal
  (median efficient-minus-non-eater LFC 1.049), but this was single-screen,
  not FDR-significant after the guide-level Wilcoxon/FDR guardrail, and needed
  disease-state/druggability/prior-art checks.

Wave38 CRISPR-state-druggability rescue:

- Script: `scripts/v3_wave38_crispr_state_druggability_rescue.py`.
- Results: 184 screen-derived candidates scanned; 184 `NO_GO_CRISPR_RESCUE`;
  0 promoted.
- `FCGRT` failed because disease-state direction conflicts with the desired
  inhibition route: directional disease support count 0, directional conflict
  count 3, no MS directional anchor, and heavy FcRn prior-art/trial crowding.

Decision:

- Resolution/efferocytosis remains valuable as a biomarker and assay panel, but
  it is no longer an active V3 therapeutic-discovery route.
- Next pivot must be outside this branch.

## 2026-05-27 09:20 UTC

Executed Wave39 and Wave40 after the forced pivot outside the
resolution/efferocytosis branch.

Wave39 accessibility-first rescue:

- Script: `scripts/v3_wave39_surfaceome_rescue_after_resolution_pivot.py`.
- Results: `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/`.
- Initial run produced one apparent `GO_REVIEW`: `PSMA3`.
- Interrogation showed this was a bug, not biology. `PSMA3` is a proteasome
  core subunit with UniProt locations `Cytoplasm;Nucleus`; the accessibility
  classifier had incorrectly matched incidental text and had not hard-excluded
  proteasome core machinery.
- Patch: removed generic function-text receptor matching from accessibility and
  added proteasome-core hard exclusions.
- Corrected Wave39 result: 224 broad recurrent candidates, 224 UniProt
  lookups, 90 ChEMBL target/activity queries, 60 Europe PMC/ClinicalTrials.gov
  prior-art queries, `0` `GO_REVIEW`, 6 `PARK_REVIEW`, and 218
  `NO_GO_SURFACEOME_RESCUE`.
- Parked candidates after corrected Wave39: `MMP7`, `CD82`, `FXYD5`, `SCD`,
  `CCL20`, and `IL23A`.

Wave39-B hostile critique:

- Report: `subagents_v3/wave39b_accessibility_prior_art_critique.md`.
- Main warning accepted: accessibility must not substitute for causal target
  evidence. The route should start with hard exclusions for HLA-II/APC markers,
  cathepsins/lysosomal loading, complement/Fc/TAM/TREM/efferocytosis,
  checkpoint/glycan/adhesion axes, secreted injury markers, generic cytokines,
  and core machinery.

Wave40 parked surface fail-fast:

- Script: `scripts/v3_wave40_parked_surface_failfast.py`.
- Results: `results_v3/wave40_parked_surface_failfast/`.
- Outcome: 5 `NO_GO_PARKED_SURFACE_FAILFAST` and 1
  `PARK_ONLY_IF_NEW_PERTURBATION`.
- `FXYD5` is not promoted. It is a narrow reopen-only artifact check because it
  is membrane-localized and less prior-art saturated, but it lacks ChEMBL
  activity or a defined modality, has a conflicting Crohn signal, has no strict
  residual survival, and lacks target-level causal or perturbation evidence.

Decision:

- The accessibility-first rescue does not yield a V3 target. It did catch a
  useful classifier failure and reinforced that most broad accessible rows are
  markers, crowded biology, or generic tissue injury/immune trafficking axes.

## 2026-05-27 09:32 UTC

Executed Wave41 to close the last unresolved perturbation-first candidate.

Question:

- Wave27 left exactly one compound as
  `PARK_EXTERNAL_TARGET_LOOKUP_ONLY`: `BRD-A72180425` / `K784-3188`.
- This needed external target/MOA deconvolution before the L1000 branch could
  be considered closed.

Failed attempt:

- First run of `scripts/v3_wave41_l1000_external_unknown_deconvolution.py`
  completed the API lookups but failed during report generation because
  `pandas.to_markdown()` requires the optional `tabulate` dependency, which is
  not installed in the pinned environment.
- Patch: replaced `to_markdown()` with a small local markdown-table renderer
  so no dependency change was needed.

Successful run:

- Script: `scripts/v3_wave41_l1000_external_unknown_deconvolution.py`.
- Outputs: `results_v3/wave41_l1000_external_unknown_deconvolution/`.
- Public sources queried and cached: PubChem PUG-REST, ChEMBL, Europe PMC,
  ClinicalTrials.gov, L1000FWD DMOA, and NCBI Bookshelf.
- `BRD-A72180425` resolved to PubChem CID `3689416` and ChEMBL
  `CHEMBL1472126`.
- ChEMBL activity rows: 57.
- ChEMBL mechanism rows: 0.
- L1000FWD DMOA known MOA/targets: `Unknown` / `Unknown`.
- NCBI Bookshelf table context: `BRD-A72180425` appears in the ML162
  RAS-selective-lethal probe SAR table.
- Structural red flag: chloroacetamide-like electrophile motif.

Decision:

- Wave41 call: `NO_GO_CYTOTOXIC_PROBE_ANALOG`.
- The L1000/repurposing branch is now closed: no promoted drugs, targets, or
  unresolved unknown-compound exceptions remain.
- Next pivot: genetics-first lipid biology that may not be captured by
  differential-expression state tests. The most concrete unresolved candidate
  is the `FADS1/FADS2` desaturation locus.

## 2026-05-27 09:45 UTC

Executed Wave42 genetics-first lipid-desaturation audit.

Reasoning:

- `FADS1/FADS2` should not be judged only as a differential-expression
  candidate. A desaturation/lipid-mediator mechanism could be driven by
  inherited enzyme activity, diet, or substrate flux while showing weak
  disease-cell expression changes.
- This made it a fair test after expression, perturbation, and accessibility
  branches failed.

Local execution:

- Script: `scripts/v3_wave42_fads_lipid_desaturation_axis.py`.
- Outputs: `results_v3/wave42_fads_lipid_desaturation_axis/`.
- Inputs: Wave34 genetics-expression-druggability scan, broad h5ad
  cell-state scan, residual-gate tables, local GWAS Catalog parquet, LINCS
  compound metadata, ChEMBL, Europe PMC, ClinicalTrials.gov, and patent-search
  URL generation.
- Patch during execution: ClinicalTrials.gov count parsing initially wrote
  blanks when the API returned `{"studies": []}` without `totalCount`. Fixed
  to count empty `studies` as zero and added `AMG 786` / `D5D inhibitor`
  queries.

Key results:

- GWAS Catalog autoimmune FADS-locus rows: 39.
- Distinct autoimmune/immune-related traits: 18.
- Rows naming FADS genes: 27.
- Rows also naming non-FADS locus genes such as `TMEM258`, `MYRF`, or `FEN1`:
  15.
- Local cell-state support: `FADS1` positive in psoriasis/UC only and
  down in MS white matter microglia (`delta=-0.558`, `p=0.0303`,
  `FDR=0.851`); `FADS2` positive in Crohn/UC only and also down in MS
  (`delta=-1.512`, `p=0.130`, `FDR=0.899`).
- Residual gate rows for `FADS1/FADS2/FADS3`: 0.
- ChEMBL: `FADS1`/`CHEMBL5840` has 145 activity rows, 61 nM-valued rows, best
  0.52 nM in a HepG2 D5D assay; `FADS2`/`CHEMBL6097` has weaker binding
  activity, best 407.65 nM.
- LINCS FADS1/FADS2 perturbagen rows: 0.
- ClinicalTrials.gov: no FADS-autoimmune, D5D-inhibitor, or FADS1-inhibitor
  trial hits; `AMG 786` returns 1 clinical-development hit.

Wave42-B hostile critique:

- Agent `019e68ca-40be-78a1-997b-1fe65cecfe12` (`Kuhn`) returned
  `subagents_v3/wave42b_fads_lipid_axis_critique.md`.
- Verdict: `DEMOTE`.
- I verified that the key cited web endpoints are reachable where not blocked
  by publisher access controls; the local demotion does not depend on the
  subagent's literature claims.

Decision:

- Wave42 call: `PARK_ONLY_IF_COLOC_DIRECTION_AND_PERTURBATION_APPEAR`.
- No therapeutic claim. The FADS route remains a future fine-mapping and
  lipidomics hypothesis, not a V3 target.

## 2026-05-27 09:47 UTC

Executed Wave43 genetic-druggable fail-fast.

Reasoning:

- Wave34 had four `PARK_GENETIC_DRUGGABLE_NEEDS_CELL_STATE` rows:
  `FADS1`, `TYK2`, `NOD2`, and `JAK2`.
- After Wave42 demoted `FADS1`, the remaining question was whether this parked
  class had any target that could be reframed as a stratified pathway
  intervention despite weak local cell-state evidence.

Results:

- Script: `scripts/v3_wave43_genetic_druggable_failfast.py`.
- Outputs: `results_v3/wave43_genetic_druggable_failfast/`.
- `FADS1`: `NO_GO_ALREADY_DEMOTED_WAVE42`.
- `TYK2`: `NO_GO_PRIOR_ART_AND_GENERIC_IMMUNOSUPPRESSION`.
- `JAK2`: `NO_GO_PRIOR_ART_AND_GENERIC_IMMUNOSUPPRESSION`.
- `NOD2`: `NO_GO_DIRECTION_AND_CONTEXT_MISMATCH`.

Decision:

- The full Wave34 genetics-plus-druggability parked class is closed for V3
  promotion.
- Next branch: audit complement factor B / alternative-complement biology as a
  biomarker-selected repurposing or stratification possibility, because it has
  genetics, druggability, and residual recurrence but likely severe prior-art
  and safety constraints.

## 2026-05-27 09:52 UTC

Executed Wave44 CFB / alternative-complement stratification audit.

Reasoning:

- `CFB` was one of the strongest remaining comparator routes: broad local
  recurrence, retained residual signal, a secreted enzymatic target, ChEMBL
  druggability, and existing factor-B inhibitors.
- The question was whether this could be reframed as a biomarker-selected
  repurposing/stratification claim rather than dismissed as generic complement.

Execution:

- Script: `scripts/v3_wave44_cfb_complement_stratification_audit.py`.
- Outputs: `results_v3/wave44_cfb_complement_stratification_audit/`.
- Inputs: Wave34, broad h5ad, broad residual, Wave21 prior-art gate, Wave25
  causal proxy, and OSMR/complement summary.
- Public API queries: Europe PMC and ClinicalTrials.gov; patent search URLs
  generated for follow-up.
- Patch during execution: Wave21 prior-art table used `candidate`, not `gene`,
  so the first run omitted CFB prior blockers. Patched the join and reran.

Key results:

- Local recurrence: 4 positive diseases (`Crohn disease`, `psoriasis`,
  `type 1 diabetes mellitus`, `ulcerative colitis`).
- Residual retained diseases: 4, but strict-core residual survival only
  `ibd_crohn_stromal:Crohn disease`.
- MS white-matter microglia: `delta=-0.982`, `p=0.287`; no MS anchor.
- ChEMBL target: `CHEMBL5731`; best nM value from Wave34: 1.0.
- Wave25 causal proxy: `NO_GO_CAUSAL_PROXY`; cell-state/module evidence is
  stronger than genetics and perturbation/foundation evidence is do-not-promote.
- Wave21 prior blockers: direct iptacopan/LNP023 and factor-B inhibitor method
  claims; recommendation was comparator only.
- Europe PMC counts: complement factor B autoimmune cluster query 1148 hits;
  factor-B inhibitor autoimmune query 190 hits; iptacopan autoimmune query 300
  hits.
- ClinicalTrials.gov counts: iptacopan MS query 0; broader factor-B/autoimmune
  queries returned hits, consistent with clinical crowding rather than novelty.

Decision:

- Wave44 call: `NO_GO_COMPLEMENT_STRATIFICATION_PRIOR_ART_BLOCKED`.
- CFB remains a useful positive-control comparator for a complement-high
  disease-state assay, but not a V3 target or biomarker-selected repurposing
  claim.

## 2026-05-27 09:55 UTC

Executed Wave45 regulatory/restoration controller audit.

Reasoning:

- After genetic-druggable and CFB branches failed, the remaining plausible
  routes were target classes that are biologically strong but hard to drug:
  A20/TNFAIP3 restoration, `SBNO2`/`SP140` regulatory programs, and the
  `MED16` perturbation comparator from Wave31.
- I combined these into one audit to avoid repeatedly re-opening separate
  undruggable-controller narratives.

Execution:

- Script: `scripts/v3_wave45_regulatory_controller_audit.py`.
- Outputs: `results_v3/wave45_regulatory_controller_audit/`.
- Inputs: Wave34, broad h5ad, broad residual, Wave23 restoration-modality
  scout, Wave31 dynamic-controller audit, and Wave25 causal proxy.

Key results:

- `TNFAIP3`: strong restoration biology but no selective current restoration
  modality and no target-resolved coloc/MR in this run.
- `SBNO2`: good cross-disease state recurrence but no MS anchor, perturbation,
  or druggable handle.
- `SP140`: genetic/state signal but no mature correct-direction degrader or
  inhibitor package.
- `MED16`: strongest selective perturbation comparator, but no direct drug
  target.
- `CDK8/CDK19`: chemical matter exists but surrogate translation failed;
  no local APC autoimmune phenocopy strong enough to claim.
- `GSK3B`: partial selectivity, pleiotropic safety, weak genetics/local breadth.
- `GPR65` and `IL10`: current-modality concepts exist in principle but remain
  blocked by weak local support and prior art.

Decision:

- Wave45 promoted count: 0.
- The regulatory/restoration-controller branch is closed for V3 promotion.

## 2026-05-27 10:02 UTC

Executed Wave46 central-axis closure audit.

Reasoning:

- The run had repeatedly circled back to the same central
  `IFN-gamma/HLA-II/CD74/IFI30/CTSS` module.
- Re-opening IFI30, CTSS, CD74, CIITA/RFX5, or upstream IFNGR/JAK control
  without new evidence would be proxy-satisficing. I wrote a closure audit to
  consolidate the prior code-backed tests and make the remaining blockers
  explicit.

Execution:

- Script: `scripts/v3_wave46_central_axis_closure_audit.py`.
- Outputs: `results_v3/wave46_central_axis_closure_audit/`.
- Inputs: central axis rank, mechanistic ODE model outputs, Wave14 target-level
  genetics, Wave15 loader external gate, Wave19 lysosomal controller tables,
  Wave31 dynamic controller audit, Wave34 genetics/expression/druggability,
  Wave43 genetic-druggable fail-fast, and Wave45 regulatory-controller audit.

Key results:

- `IFNGR_JAK_STAT1_upstream_control`: `NO_GO_GENERIC_IFN_JAK_CONTROL`.
  The model supports upstream state control (`IFN/APC` minimum log2FC
  -1.123; `HLA-II/CD74` -0.638; `GILT` -0.635 under 70% suppression), but the
  intervention is generic IFN/JAK immunosuppression and heavily prior-arted.
- `CD74_HLAII_receptor_APC_state_biomarker`: `NO_GO_BIOMARKER_NOT_TARGET`.
  Strong state biology, weak target-level genetics, and better suited to
  stratification/readout than direct therapy.
- `CIITA_RFX5_HLAII_transcriptional_gate`:
  `NO_GO_HLAII_TF_GATE_UNDRUGGABLE`. Mechanistically narrow, but no current
  selective clinical modality and no target-level coloc/MR package.
- `IFI30_GILT_lysosomal_feedback_effector`:
  `NO_GO_IFI30_DOWNSTREAM_AND_UNTRACTABLE`. Even 95% modeled IFI30 suppression
  has weak upstream effects (`IFN/APC` minimum log2FC -0.182; `HLA-II/CD74`
  -0.060) compared with its lysosomal readout effect (`GILT` -0.558).
- `CTSS_cathepsinS_lysosomal_effector`:
  `NO_GO_CTSS_PRIOR_ART_DOWNSTREAM_EFFECTOR`. Modeled 70% CTSS suppression is
  essentially null on `IFN/APC` and `HLA-II/CD74` while affecting only the
  lysosomal readout (`GILT` -0.306), and CTSS autoimmune prior art is heavy.

Decision:

- The original central IFN/HLA-II/lysosomal antigen-processing axes remain
  biologically central but are closed for V3 therapeutic promotion.
- Next pivot must search outside direct central-axis modulation. A plausible
  path is a meta-analysis of repeatedly demoted but biologically coherent
  branches to identify a readout/assay or upstream tissue-circuit intervention
  that is not just the same module under a new name.

## 2026-05-27 10:20 UTC

Executed Wave47 late-stage survivor map and Wave48 resolution-reopener audit.

Reasoning:

- Wave46 closed the direct central axes, so the next risk was accidentally
  reopening already-demoted biology under a new label.
- Wave47 consolidated all late-stage park/reopen rows and found no immediately
  promotable candidate. It left only assay-reopen branches.
- Wave47-G independently highlighted `FPR2/ANXA1` and receptor-specific
  `CD300` as the only non-relabel reopeners. I therefore wrote Wave48 as a
  strict route audit rather than accepting either branch narratively.

Execution:

- Wave47 script: `scripts/v3_wave47_late_stage_survivor_map.py`.
- Wave47 outputs: `results_v3/wave47_late_stage_survivor_map/`.
- Wave48 script: `scripts/v3_wave48_resolution_reopener_audit.py`.
- Wave48 outputs: `results_v3/wave48_resolution_reopener_audit/`.
- First Wave48 run failed because `gene_contrast_scores.tsv` uses `p` and
  `contrast_type`, not always `p_value` and `comparison_type`. I patched the
  parser and reran successfully.
- I also patched Wave48 after review to separate `prior_art_not_blocking` from
  `novelty_delta_sufficient`, because a crowded literature count is not the
  same as a blocking patent/clinical prior-art status.

Key results:

- Wave47 scanned 75 late-stage routes: 0 promotable now, 15
  `REOPEN_WITH_NEW_TEST_ONLY`, 15 `PARK_BUT_LIKELY_BLOCKED`, 43 closed/no-go,
  and 2 closed prior-wave excluded axes.
- Wave48 `FPR2_ANXA1_BIASED_RESOLUTION`:
  `REOPEN_WITH_WETLAB_TEST_ONLY_NOT_V3_PROMOTION`; 4/7 critical gates passed.
  It passes specific directionality, cross-autoimmune local signal,
  druggability, and non-blocking prior-art status, but fails strict MS anchor,
  real perturbation anchor, and novelty delta.
- Wave48 `CD300_RECEPTOR_SPECIFIC_TUNING`:
  `REOPEN_ONLY_IF_RECEPTOR_SPECIFIC_PERTURBATION_NOT_V3_PROMOTION`; 2/7
  critical gates passed. It has IBD/psoriasis local signal and a small
  Geneformer support context, but fails receptor-specific directionality,
  strict MS anchor, real perturbation anchor, druggability/selectivity, and
  novelty delta.

Decision:

- Do not promote either resolution branch.
- `FPR2/ANXA1` is a wet-lab assay idea, not a V3 target claim.
- `CD300` requires receptor-specific perturbation evidence before it can be
  reopened; family-level CD300 modulation remains unsafe and under-specified.
- Continue searching for a branch with target-level perturbation/genetic
  evidence rather than additional expression-recognition routes.

## 2026-05-27 10:28 UTC

Executed Wave49 `PTPN22` directionality and modality audit.

Reasoning:

- Wave47 ranked `PTPN22` as the top reopen-only route because it has broad
  autoimmune genetics and tractable phosphatase chemistry.
- This is a high-risk proxy trap: broad mapped genetics plus inhibitors does
  not establish whether inhibiting or restoring PTPN22 is the right,
  disease-safe direction.

Execution:

- Script: `scripts/v3_wave49_ptpn22_directionality_audit.py`.
- Outputs: `results_v3/wave49_ptpn22_directionality_audit/`.
- Sources: Wave47, Wave34A, Wave34, broad h5ad gene discovery, broad residual
  gate, Wave23 restoration-modality table, live Europe PMC,
  ClinicalTrials.gov, ChEMBL target/activity APIs, and patent-search URLs.
- The script also pulled top PTPN22 ChEMBL activity rows and scanned those
  molecules against related phosphatases `PTPN2`, `PTPN1`, and `PTPN11`.

Key results:

- `PTPN22` call:
  `NO_GO_BROAD_GENETICS_WITH_UNRESOLVED_DIRECTION_AND_SELECTIVITY`.
- Gate pass count: 2/9.
- Passed gates: cross-autoimmune genetic breadth (28 GWAS Catalog traits,
  minimum p approximately 5e-174) and chemical matter exists (100 ChEMBL nM
  rows in the bounded pull; best nM 270).
- Failed gates: target-resolved direction, strict MS anchor, cross-disease
  cell-state support, disease-relevant perturbation anchor, phosphatase
  selectivity, disease-safe modulation direction, and novelty/prior art.
- MS support is nominal only in the local broad table:
  white-matter delta 0.820, p 0.031, FDR 0.851, and no MS GWAS trait in the
  local PTPN22 GWAS Catalog trait text.
- Off-target scan found at least one top PTPN22 molecule with stronger PTPN1
  activity than PTPN22 activity (`min_offtarget_over_ptpn22_ratio` 0.417),
  supporting the selectivity-blocker call.

Decision:

- Do not promote `PTPN22`.
- Keep it only as a future allele-direction/coloc and selective-modality
  problem. It is not a V3 therapeutic finding under the current evidence.

## 2026-05-27 10:35 UTC

Executed Wave50 `GPR65` acid-sensing GPCR audit.

Reasoning:

- `GPR65` was the next most tractable reopen-only branch after `PTPN22`:
  a membrane GPCR with cross-autoimmune genetics and a plausible agonist/PAM
  direction.
- This branch could only promote if it overcame two known blockers:
  local cell-state mismatch and direct IBD/autoimmune prior art.

Execution:

- Script: `scripts/v3_wave50_gpr65_acid_sensing_gpcr_audit.py`.
- Outputs: `results_v3/wave50_gpr65_acid_sensing_gpcr_audit/`.
- Sources: Wave47, Wave34A, Wave34, Wave20 genetic-druggable alt-axis,
  Wave23 restoration-modality table, broad h5ad table, live Europe PMC,
  ClinicalTrials.gov, ChEMBL, and patent-search URLs.

Key results:

- `GPR65` call:
  `NO_GO_GPR65_PRIOR_ART_AND_LOCAL_CELLSTATE_MISMATCH`.
- Gate pass count: 3/8.
- Passed gates: cross-disease genetic breadth, selective modality exists, and
  clinical whitespace.
- Failed gates: target-resolved coloc/MR, strict MS anchor, local cell-state
  alignment, real perturbation anchor, and novelty/prior-art gate.
- Quantitative details:
  - 5 OpenTargets diseases in the local summary: AS, Crohn, MS, psoriasis, UC.
  - 5 GWAS Catalog traits, minimum p 4e-18.
  - Local disease-state support is contradictory: 1 positive disease and 2
    negative diseases.
  - MS white-matter delta 0.090, p 0.624, FDR 0.949.
  - ChEMBL target `CHEMBL3714081`; bounded activity pull had 99 rows, best
    nM 364.84.
  - ClinicalTrials.gov direct GPR65 autoimmune/agonist queries returned 0.

Decision:

- Do not promote `GPR65`.
- The branch remains plausible biology but is no-go for V3 because a
  patent/literature-covered IBD/autoinflammatory GPCR route plus contradictory
  local cell-state data is not a novel cross-autoimmune finding.

## 2026-05-27 10:39 UTC

Executed Wave51 reachable stromal/surface audit for `FAP` and `FXYD5`.

Reasoning:

- After `PTPN22` and `GPR65` failed, the remaining reopen-only candidates with
  plausible tractability were reachable surface/stromal routes.
- These are prone to false promotion because accessibility and disease
  expression can reflect remodeling or epithelial stress rather than causal
  therapeutic leverage.

Execution:

- Script: `scripts/v3_wave51_reachable_stromal_surface_audit.py`.
- Outputs: `results_v3/wave51_reachable_stromal_surface_audit/`.
- Sources: Wave47, Wave34A, Wave34, Wave39 surfaceome rescue, Wave40 parked
  surface fail-fast, broad h5ad, broad residual gate, live Europe PMC,
  ClinicalTrials.gov, ChEMBL, and patent-search URLs.

Key results:

- `FAP`: `NO_GO_REACHABLE_SURFACE_STROMAL_ROUTE`, 2/8 gates passed.
  It has target/locus genetics and tractable modality evidence, but fails
  cross-disease local breadth, strict MS anchor, residual survival, direction
  and safety, perturbation anchor, and novelty/prior-art gate.
- `FAP` quantitative context: 15 GWAS Catalog traits, minimum p 6e-25;
  local positives 2, negatives 0; no MS signal in the joined local tables;
  strict residual 0; Europe PMC max count 218; ClinicalTrials.gov direct
  `FAP autoimmune` count 5; ChEMBL `CHEMBL4683`, bounded best nM 4.6.
- `FXYD5`: `NO_GO_REACHABLE_SURFACE_STROMAL_ROUTE`, 1/8 gates passed.
  It only passes novelty/prior-art not-blocking, but fails local
  non-contradiction, strict MS anchor, target genetics, residual survival,
  direction/safety, perturbation, and modality.
- `FXYD5` quantitative context: local positives 4 and negatives 1; MS
  white-matter delta 0.352, p 0.0587, FDR 0.899; no target-level genetics;
  no ChEMBL target activity; Europe PMC autoimmune query 0 but broader
  antibody/inflammation query 101.

Decision:

- Do not promote `FAP` or `FXYD5`.
- Both are retained only as future tissue-perturbation assay ideas, not V3
  findings.

## 2026-05-27 10:43 UTC

Integrated Wave50-G and closed the agent.

- Preserved report:
  `subagents_v3/wave50g_gpr65_critique.md`.
- Independent critique agrees with the local GPR65 audit:
  `NO_GO`, not a V3 therapeutic candidate.
- Added blockers from the subagent to the orchestrator reasoning:
  Pathios GPR65 modulator patent families appear to claim autoimmune/MS uses,
  while the strongest functional PAM biology is IBD-risk-variant centered and
  not target-resolved for MS or non-IBD autoimmune disease.

## 2026-05-27 10:48 UTC

Started Wave52 consolidated audit of the remaining mechanistic reopeners:
`CCR6_TH17_TRAFFICKING`, `TREM2_APOE_LIPID_REPAIR`, `SQLE_STEROL_STROMAL`,
and `LOCALIZED_IL10_RESTORATION`.

Reasoning:

- These are the remaining routes that still have a mechanistic story after the
  Wave47 survivor map but have not met V3 promotion criteria.
- The operationalization is deliberately stricter than a signature score:
  cross-autoimmune breadth, cross-dataset cell-state replication, target-
  specific MS anchoring, target-resolved genetics/coloc, foundation-model plus
  real perturbation alignment, tractable intervention, safe direction, and
  novelty/prior-art status are scored separately.
- This prevents route-level plausibility from being silently converted into a
  therapeutic claim.

## 2026-05-27 10:51 UTC

Executed Wave52.

Execution:

- Script: `scripts/v3_wave52_remaining_mechanistic_reopeners.py`.
- Outputs: `results_v3/wave52_remaining_mechanistic_reopeners/`.
- Sources: Wave47, Wave23 restoration, Wave28 target-first rescue, Wave32
  resolution rescue, Wave34/Wave34A genetics-expression audits, Wave22 SQLE
  fail-fast, broad h5ad discovery, broad residual gate, live Europe PMC,
  ClinicalTrials.gov, ChEMBL, and patent-search URLs.

Key results:

- `CCR6_TH17_TRAFFICKING`:
  `NO_GO_CROWDED_TRAFFICKING_NO_COLOC_LOCAL_SUPPORT`, 2/8 gates passed.
  It passes broad GWAS Catalog breadth and tractable intervention point but
  fails cell-state replication, MS anchor, target-resolved genetics, real
  perturbation/foundation alignment, safe selective direction, and novelty.
- `TREM2_APOE_LIPID_REPAIR`:
  `NO_GO_TREM2_PRIOR_ART_MARKER_CONFOUNDER`, 3/8 gates passed. It has
  route-level cross-disease biology and chemical matter, but fails target-
  specific MS anchoring, target-resolved genetics, perturbation alignment,
  safe direction, and novelty.
- `SQLE_STEROL_STROMAL`:
  `NO_GO_SQLE_FAILFAST_RECONFIRMED`, 2/8 gates passed. The prior fail-fast
  remains decisive: MS signal is negative, foundation-model support is
  contradicted by real perturbation, and no novel autoimmune-use delta exists.
- `LOCALIZED_IL10_RESTORATION`:
  `NO_GO_IL10_PRIOR_ART_SYSTEMIC_CYTOKINE_DELIVERY`, 2/8 gates passed. Broad
  genetics and a plausible biologic modality do not overcome weak local
  subgroup evidence and extensive IL-10 autoimmune prior art.

Decision:

- Do not promote any remaining Wave47 reopen-only mechanism.
- The next pivot must stop asking whether named late-stage candidates can be
  rescued and instead search for an intervention point from a different
  evidence axis, with treatment-response stratification and real perturbation
  effects prioritized over expression prominence.

## 2026-05-27 11:04 UTC

Started local Wave53 perturbation-first pivot.

Reasoning:

- The strongest non-expression signal in existing artifacts is real
  perturbation: `Med16_KO` and `Gsk3b_KO` suppress antigen-processing/MHC-II
  readouts more selectively than broad IFN/JAK controls.
- This is scientifically more meaningful than another expression-rescue
  attempt, but it creates a new translational problem: the strongest hit
  (`MED16`) is not obviously druggable and available Mediator/GSK3B/TNF/RFX5/
  CHUK routes may fail on safety, prior art, and MS direction.

Execution:

- Added `scripts/v3_wave53_perturbation_first_pivot.py`.
- Candidate routes: `MED16_MEDIATOR_MODULE`, `GSK3B_INHIBITION`,
  `TNFRSF1A_DAMPING`, `RFX5_MHCII_PARTIAL_SUPPRESSION`,
  `CHUK_IKK_MODULATION`.

## 2026-05-27 11:08 UTC

Integrated Wave53 local audit and subagents.

Subagents:

- Wave53-G returned `WETLAB_ONLY` for the `MED16` branch and was closed.
  Report: `subagents_v3/wave53g_med16_mediator_review.md`.
- Wave53-H returned `NO_GO` for treatment-response stratification and was
  closed. Report: `subagents_v3/wave53h_treatment_response_review.md`.
- Wave53-I returned no therapeutic shortlist and was closed. It identified
  `MFGE8` augmentation as one `PARK_EX_VIVO_ONLY` reopener. Report:
  `subagents_v3/wave53i_cross_domain_scout.md`.

Local Wave53:

- Script: `scripts/v3_wave53_perturbation_first_pivot.py`.
- Outputs: `results_v3/wave53_perturbation_first_pivot/`.
- Calls:
  - `MED16_MEDIATOR_MODULE`:
    `WETLAB_ONLY_MED16_SELECTIVE_NONDRUGGABLE_ROUTE`, 2/8 gates passed.
  - `GSK3B_INHIBITION`:
    `NO_GO_GSK3B_REAL_PERTURBATION_PRIOR_ART_PLEIOTROPY`, 2/8 gates passed.
  - `TNFRSF1A_DAMPING`: `NO_GO_PERTURBATION_FIRST_PIVOT`, 3/8 gates passed.
  - `RFX5_MHCII_PARTIAL_SUPPRESSION`: `NO_GO_PERTURBATION_FIRST_PIVOT`, 2/8
    gates passed.
  - `CHUK_IKK_MODULATION`: `NO_GO_PERTURBATION_FIRST_PIVOT`, 2/8 gates passed.

Decision:

- Do not promote perturbation-first routes.
- `MED16` is the strongest real perturbation result in the run, but it is not
  a V3 therapeutic finding without a druggable phenocopy and safe
  cell-specific transcriptional modulation.
- Run a narrow Wave54 `MFGE8` audit because it is the only new cross-domain
  reopener not already closed by prior V3 gates.

## 2026-05-27 11:13 UTC

Started Wave54 `MFGE8` debris-opsonin audit.

Reasoning:

- Wave53-I identified `MFGE8` as a non-obvious cross-domain reopener:
  soluble phosphatidylserine/myelin-debris bridging, not the already-closed
  `MERTK`, `TREM2`, `CD300`, or `FPR2` branches.
- Local evidence is weak enough that promotion would be premature: one T1D
  positive compartment, nominal MS trend but FDR high, and unresolved CRISPR
  efferocytosis screen.
- The audit must therefore focus on whether this is more than an ex vivo assay
  idea, with bystander phagocytosis toxicity as a first-class gate.

Execution:

- Added `scripts/v3_wave54_mfge8_debris_opsonin_audit.py`.
- Inputs: broad h5ad gene discovery, broad residual gate, Wave37
  efferocytosis CRISPR screen, Wave34 genetics-expression scan, live Europe
  PMC, ClinicalTrials.gov, ChEMBL, and patent-search URLs.

## 2026-05-27 11:16 UTC

Executed Wave54 `MFGE8` audit.

Results:

- Script: `scripts/v3_wave54_mfge8_debris_opsonin_audit.py`.
- Outputs: `results_v3/wave54_mfge8_debris_opsonin_audit/`.
- Call: `PARK_EX_VIVO_ONLY_MFGE8_DEBRIS_OPSONIN`, 3/8 gates passed.
- Passed gates: cross-domain mechanistic anchor, tractable modality, and
  no obvious direct clinical therapeutic crowding.
- Failed gates: local cross-autoimmune cell-state support, strict MS anchor,
  efferocytosis screen support, bystander-phagocytosis safety resolution, and
  promotion-grade package.
- Key numbers:
  - Local positive diseases: 1 (`type 1 diabetes mellitus`).
  - MS white-matter delta 0.559, p 0.0686, FDR 0.899.
  - Wave37 efferocytosis contrast log fold-change 0.159, FDR 1.0,
    screen call `UNRESOLVED`.
  - Europe PMC query hits: myelin/remyelination 62, autoimmunity/apoptotic
    cell clearance 294, phagoptosis/neuron inflammation 39.

Decision:

- Do not promote `MFGE8`.
- Keep it only as an ex vivo assay idea with an explicit bystander toxicity
  gate.

## 2026-05-27 11:18 UTC

Started Wave55 external genetics and druggability sweep.

Reasoning:

- Convergence Check 17 identified target-specific intervention causality as
  the recurring missing evidence.
- Live Open Targets associated-target tables can provide a wider genetics
  sweep than the local handpicked candidates, across 12 autoimmune diseases.
- This is still not coloc/MR, so the script explicitly keeps a separate
  `coloc_or_mr_grade_target_resolution` gate that cannot pass in this wave.

Execution:

- Added `scripts/v3_wave55_external_genetics_druggability_sweep.py`.
- Diseases: MS, RA, Crohn, UC, psoriasis, SLE, T1D, Sjogren, ankylosing
  spondylitis, autoimmune thyroid disease, celiac disease, and primary
  biliary cholangitis.
- Evidence channels: live Open Targets associated targets, local broad h5ad
  cell-state tables, local perturbation/foundation outputs, ChEMBL, and live
  Europe PMC literature counts for top candidates.

## 2026-05-27 11:20 UTC

Executed Wave55 external genetics and druggability sweep.

Results:

- Script: `scripts/v3_wave55_external_genetics_druggability_sweep.py`.
- Outputs: `results_v3/wave55_external_genetics_druggability_sweep/`.
- Live Open Targets raw rows: 6000 across 12 autoimmune diseases.
- Non-closed ranked targets: 2815.
- Promoted targets: 0.
- Reopen-priority targets: 2.
- Reopen candidates:
  - `SP140`: `REOPEN_COLOC_OR_PERTURBATION_PRIORITY_ONLY`, 4/8 gates.
    Passed cross-disease Open Targets genetic breadth, MS Open Targets
    genetic anchor, local cross-disease cell-state replication, and low
    early literature-crowding flag. Failed coloc/MR-grade target resolution,
    strict local MS anchor, real perturbation support, and druggability.
  - `IL12A`: `REOPEN_COLOC_OR_PERTURBATION_PRIORITY_ONLY`, 4/8 gates.
    Passed cross-disease Open Targets genetic breadth, MS Open Targets
    genetic anchor, druggability/modality precedent, and early
    literature-crowding flag. Failed local cross-disease cell-state
    replication, strict local MS anchor, real perturbation support, and
    coloc/MR-grade target resolution.

Decision:

- Do not promote any Wave55 target. The explicit `coloc_or_mr_grade` gate
  remained false because Open Targets associated-target scores are not
  paired disease/eQTL or disease/pQTL colocalization.
- Treat `SP140` as the next forcing target because it is the only Wave55
  candidate combining MS/cross-autoimmune external genetics with local
  cross-disease cell-state replication and comparatively lower literature
  saturation.
- Treat `IL12A` as a comparator/control branch: it is pharmacologically
  tractable, but its weak local module support and well-developed IL-12/23
  autoimmune prior art make it less likely to yield a novel V3 claim.

## 2026-05-27 11:23 UTC

Started Wave56 targeted `SP140` audit.

Reasoning:

- `SP140` is the cleanest Wave55 reopener by breadth because it combines
  Open Targets genetic signal across six autoimmune diseases with local
  cross-disease cell-state replication.
- Prior Wave45 already warned that `SP140` is likely an undruggable chromatin
  controller. The targeted audit must therefore test the hard failure modes:
  target-resolved causality, strict MS anchor, real perturbation, and a
  correct-direction intervention point.
- `IL12A` and `GALC` are included as comparators: `IL12A` is a tractable but
  likely crowded cytokine branch; `GALC` is a lysosomal lipid enzyme with
  weaker Wave55 rank but better mechanistic proximity to the lipid-lysosomal
  module.

Execution:

- Added `scripts/v3_wave56_sp140_targeted_reopener_audit.py`.
- Added the script to `run_v3_analysis.sh`.
- Inputs: Wave55 external genetics rank/raw rows, broad h5ad discovery,
  broad residual gate, Wave37 efferocytosis CRISPR screen, Wave45 regulatory
  audit, Wave18 foundation/perturbation summaries, Wave15 perturbation
  synthesis, live Europe PMC, ClinicalTrials.gov, ChEMBL, UniProt, and patent
  search URLs.

## 2026-05-27 11:29 UTC

Executed Wave56 targeted `SP140` audit.

Results:

- Script: `scripts/v3_wave56_sp140_targeted_reopener_audit.py`.
- Outputs: `results_v3/wave56_sp140_targeted_reopener_audit/`.
- Call: `NO_GO_SP140_TARGETED_AUDIT`, 2/10 gates passed.
- Passed gates: cross-disease external genetics breadth and local
  cross-disease cell-state replication.
- Failed gates: target-resolved coloc/MR, strict core module-specific
  residual signal, strict MS white-matter anchor, real perturbation support,
  foundation-model support, direct druggable handle, early crowding, and
  correct-direction intervention.
- Key numbers:
  - Open Targets genetic association >=0.25 in six diseases:
    `AS;Crohn;MS;Psoriasis;RA;UC`.
  - Local positive diseases: 4 (`Crohn disease;Sjogren syndrome;psoriasis;ulcerative colitis`).
  - MS white-matter delta -0.087, p 0.726, FDR 0.968.
  - Wave37 efferocytosis contrast log fold-change 1.055, contrast FDR 0.920,
    screen call `UNRESOLVED`.
  - ChEMBL activity rows for `SP140`: 0.
  - UniProt domain-like features include HSR, SAND, bromodomain, and PHD-type
    regions, but no direct selective chemical matter was found.

Decision:

- Demote `SP140` from lead therapeutic target to genetic/cell-state marker
  and mechanistic wet-lab reopener.
- The result strengthens the conclusion that the cross-autoimmune module is
  real, but the central therapeutic node is not a nuclear marker without a
  restoration modality.
- Next pivot should not be another chromatin-marker audit unless a direct
  perturbation or degrader/restoration modality is available.

## 2026-05-27 11:33 UTC

Integrated Wave56-L `IL12A` comparator sidecar.

Result:

- Report: `subagents_v3/wave56l_il12a_comparator_prior_art.md`.
- Verdict: `DEMOTE_IL12A_TO_COMPARATOR_CONTROL`.
- Key reasons:
  - Selective IL-12p35 antagonism is real and druggable but already covered
    by DM618 and `WO2025166228A1`.
  - MS p40 blockade precedent does not support monotherapy development.
  - IL-12 may have CNS-protective biology, creating an on-target risk for
    chronic MS blockade.
  - IL-12p35/IL-35-like agonism is scientifically interesting but is a
    different biologic-restoration route with no local V3 module support.

Decision:

- `IL12A` stays as comparator/control, not a candidate for promotion.

## 2026-05-27 11:33 UTC

Started Wave57 intervention-first Geneformer screen.

Reasoning:

- Repeated failures are marker-centric. The next screen asks whether any
  intervention-addressable module-proximal candidate has foundation-model
  rescue-like behavior across disease contexts.
- Candidate set includes lysosomal lipid enzymes (`GALC`, `LIPA`, `CTSD`,
  `SMPD1`, `GBA1`, `GLA`, `HEXA`, `HEXB`, `PSAP`, `ASAH1`), Wave55 local
  recurrence axes (`SP140`, `IL7R`, `CCL20`, `PTPN2`, `DAP`, `PARK7`), and
  druggable comparators (`CXCR2`, `PRKCB`, `HDAC7`, `STAT4`, `CD40`).
- This is explicitly foundation-model triage only. A model-positive result
  must still be joined to genetics, local recurrence, perturbation, and
  modality evidence.

Execution:

- Added `scripts/v3_wave57_intervention_first_geneformer_screen.py`.
- Added the script to `run_v3_analysis.sh`.

## 2026-05-27 11:34 UTC

Integrated Wave56-J `SP140` genetics/prior-art sidecar.

Result:

- Report: `subagents_v3/wave56j_sp140_genetics_prior_art.md`.
- Verdict: demote `SP140` as a V3 therapeutic target.
- Key reasons:
  - MS and Crohn genetics are real and target-resolved.
  - Wider RA/AS/psoriasis/Sjogren support is not target-resolved.
  - Direction is conflicted: MS/Crohn risk can involve reduced full-length
    SP140/protein, whereas published drug strategy inhibits SP140.
  - Direct SP140 modulation is already published and patented for
    autoimmune/inflammatory disease, including GSK761 literature and
    `US9018184B2`.

Decision:

- Keep `SP140` as a positive-control comparator and possible
  genotype-stratification axis.
- Do not use direct SP140 modulation as the V3 finding.

## 2026-05-27 11:40 UTC

Integrated Wave56-K `SP140` perturbation/druggability sidecar.

Result:

- Report: `subagents_v3/wave56k_sp140_perturbation_druggability.md`.
- Support script:
  `scripts/v3_wave56k_sp140_perturbation_druggability_audit.py`.
- Outputs:
  `results_v3/wave56k_sp140_perturbation_druggability/`.
- Verdict:
  `DEMOTE_FOR_V3_PROMOTION; PARK_AS_SP140_HIGH_IBD_TOOL_COMPOUND_AND_STRATIFICATION_ROUTE`.

Important correction:

- The earlier local Wave56 statement that `SP140` lacked perturbation support
  was too narrow. Published `SP140` siRNA and GSK761 data do provide
  target-specific perturbation evidence.
- The perturbation still does not support V3 promotion: the main signal is
  early IFN/NF-kB suppression in macrophages, not coherent lipid-lysosomal
  module rescue; MS local support is null; GSK761 is poor for CNS/lead-like
  feasibility; and direct SP140 inhibition is prior art.

Decision:

- Keep `SP140` closed for V3 therapeutic promotion.
- Add Wave56-K support script to the end-to-end runner for reproducibility.

## 2026-05-27 11:40 UTC

Executed and integrated Wave57 intervention-first Geneformer screen.

Results:

- Script: `scripts/v3_wave57_intervention_first_geneformer_screen.py`.
- Outputs: `results_v3/wave57_intervention_first_geneformer_screen/`.
- Model: Geneformer V2-104M, revision
  `04c2b2e84da7c0f385c3f9ad8f3ec24bab6650e5`.
- Candidate genes: 26.
- Contexts: 11.
- Promotions: 0.
- Reopeners: 2.
  - `CXCR2`: `REOPEN_MODEL_SUPPORTED_INTERVENTION_FIRST`.
    Strong model context `IBD_myeloid`, 3 disease cells with token,
    cosine-shift z 1.197, projection-minus-random 0.0288. External genetics
    in AS/Crohn/psoriasis/RA/UC; local positives in Crohn/psoriasis/UC; no
    MS genetic anchor.
  - `IL7R`: `REOPEN_MODEL_SUPPORTED_INTERVENTION_FIRST`.
    Strong model context `ra_myeloid_dendritic`, 12 disease cells with token,
    cosine-shift z 0.529, projection-minus-random 0.0318. External genetics
    in seven diseases including MS; local positives in Crohn/T1D/UC; strict
    MS local anchor failed.

Decision:

- No Wave57 finding is promotable directly. Foundation-model support is a
  triage signal only.
- Run focused audits for `CXCR2` and `IL7R`.

## 2026-05-27 11:42 UTC

Started Wave58 targeted `CXCR2`/`IL7R` audit.

Reasoning:

- `CXCR2` and `IL7R` are the only Wave57 model-supported reopeners. Both are
  plausible intervention points but have opposite weaknesses:
  - `CXCR2` is druggable and local/model-supported but has no MS genetic
    anchor and may be generic neutrophil chemotaxis.
  - `IL7R` has strong MS/cross-autoimmune genetics and model support but is
    likely a crowded lymphocyte survival axis rather than the
    lipid-lysosomal myeloid module.
- The audit includes manual hard gates for these generic-biology failure
  modes because automated API evidence can easily over-score canonical immune
  targets.

Execution:

- Added `scripts/v3_wave58_cxcr2_il7r_targeted_audit.py`.
- Added the script to `run_v3_analysis.sh`.

## 2026-05-27 11:47 UTC

Executed and integrated Wave58 targeted `CXCR2`/`IL7R` audit.

Results:

- Script: `scripts/v3_wave58_cxcr2_il7r_targeted_audit.py`.
- Outputs: `results_v3/wave58_cxcr2_il7r_targeted_audit/`.
- `CXCR2`: `NO_GO_WAVE58_TARGETED_AUDIT`, 4/9 gates passed.
  - Passed: cross-disease external genetics breadth, local cross-disease
    cell-state recurrence, Geneformer reopener, and direct druggability.
  - Failed: MS external genetics, strict MS white-matter anchor, real
    perturbation/efferocytosis, module-specific biology, and prior-art gates.
  - Key values: ChEMBL activity rows 100, best nM 6.0, ClinicalTrials relevant
    max count 1, Europe PMC `"CXCR2 inhibitor" autoimmune` hits 153.
- `IL7R`: `NO_GO_WAVE58_TARGETED_AUDIT`, 5/9 gates passed.
  - Passed: cross-disease external genetics breadth, MS external genetics,
    local cross-disease cell-state recurrence, Geneformer reopener, and
    biologic/clinical modality precedent.
  - Failed: strict MS white-matter anchor, real perturbation/efferocytosis,
    module-specific biology, and prior-art gates.
  - Key values: MS Open Targets genetic score 0.789, ClinicalTrials relevant
    max count 10, Europe PMC `"anti-CD127" autoimmune` hits 947.

Decision:

- Close both `CXCR2` and `IL7R` for V3 promotion.
- The next pivot must avoid canonical trafficking/survival immune targets
  unless a stratified mechanism links them directly to the lipid-lysosomal
  myeloid state and a specific intervention gap.

## 2026-05-27 11:48 UTC

Integrated Wave58-O hostile review.

Result:

- Report: `subagents_v3/wave58o_hostile_review_cxcr2_il7r.md`.
- Verdict: close both `CXCR2` and `IL7R` for V3 therapeutic promotion.
- Added critique:
  - `CXCR2` is MS-genetics negative, likely composition/neutrophil-driven,
    and directly prior-arted in demyelination/CXCR2 blockade.
  - `IL7R` has real autoimmune/MS genetics, but the mechanism is canonical
    adaptive-immune/CD127 biology with direct clinical and patent prior art,
    not a lipid-lysosomal myeloid mechanism.

Decision:

- Treat local Wave58 closure as confirmed.

## 2026-05-27 11:48 UTC

Started Wave59 lysosomal/sphingolipid model reopener audit.

Reasoning:

- Wave57’s strongest model scores were not `CXCR2`/`IL7R`; they were
  lysosomal enzymes such as `CTSB`, `ASAH1`, `HEXB`, and `HEXA`.
- These failed broad gates, but they are closer to the original
  lipid-lysosomal module than canonical chemokine/lymphocyte axes.
- The risk is directionality: inhibiting or enhancing housekeeping lysosomal
  enzymes can be harmful or nonspecific. Wave59 therefore has a hard manual
  directionality/selectivity gate.

Execution:

- Added `scripts/v3_wave59_lysosomal_sphingolipid_model_reopener_audit.py`.
- Added the script to `run_v3_analysis.sh`.

## 2026-05-27 11:54 UTC

Integrated returned Wave58 sidecars and closed their agents.

Reports:

- `subagents_v3/wave58m_cxcr2_therapeutic_audit.md`.
- `subagents_v3/wave58n_il7r_therapeutic_audit.md`.
- `subagents_v3/wave58o_hostile_review_cxcr2_il7r.md`.

Decision:

- `CXCR2` is demoted for V3 therapeutic promotion. It remains a useful
  comparator because it is druggable and biologically real in neutrophil/
  remyelination contexts, but it lacks a V3-grade MS genetic/local anchor,
  appears compatible with neutrophil/epithelial composition effects, and is
  directly prior-arted for demyelination and autoimmune/inflammatory uses.
- `IL7R` is demoted for V3 therapeutic promotion. It has real autoimmune and
  MS genetics, but the strongest mechanism is canonical CD127/sIL7R
  adaptive-immune biology. The V3 local MS signal is null, model support is
  single-context and weak, and anti-CD127/sIL7R-splicing intervention space is
  already crowded with trials and patents.

Self-critique:

- The Geneformer reopener threshold was useful for triage but too permissive
  for claim support. A one-context token-deletion signal with sparse token
  coverage should not resurrect canonical inflammatory targets without
  donor-blocked validation and tissue/cell protein evidence.

## 2026-05-27 11:55 UTC

Integrated Wave59 lysosomal/sphingolipid model reopener audit.

Results:

- Script: `scripts/v3_wave59_lysosomal_sphingolipid_model_reopener_audit.py`.
- Outputs: `results_v3/wave59_lysosomal_sphingolipid_model_reopener_audit/`.
- Candidate genes: `CTSB`, `ASAH1`, `HEXB`, `HEXA`, `CTSS`, `CTSD`, `PSAP`,
  `LIPA`, `GALC`, `GBA1`, `SMPD1`.
- Promotions: 0.
- Parked: 0.
- Best numerical gate count: `GALC`, 4/10 gates.
- Strongest model-specific rows: `CTSB` passed foundation-model support in
  multiple contexts and `ASAH1` had one strong plus five supporting contexts,
  but both failed cross-disease/MS genetics, strict MS local support,
  perturbation/efferocytosis, directionality, and prior-art gates.

Interpretation:

- The lysosomal branch is biologically closer to the original module than
  `CXCR2`/`IL7R`, but single enzyme intervention is the wrong level of control
  for the current evidence. The dominant failure is directionality and
  selectivity: broad cathepsin, ceramidase, sphingomyelinase, or lysosomal
  hydrolase modulation risks damaging normal debris clearance, antigen
  processing, or neuro/glial lysosomal function.

Decision:

- Close the direct lysosomal/sphingolipid enzyme reopener branch for now.
- Pivot to circuit-level tests and response-stratification analysis: identify
  controllers upstream of the lipid-lysosomal myeloid module that can change
  disease state without generic organelle inhibition or canonical immune-cell
  trafficking/survival blockade.

## 2026-05-27 11:55 UTC

Updated time accounting after user correction.

The user clarified that the usage-limit waiting gap in the logs does not count
as active working time and that twelve active hours have not yet been reached.
The session therefore continues and `EXHAUSTION.md` remains unavailable.

## 2026-05-27 12:01 UTC

Started Wave60 circuit-coupling pivot.

Reasoning:

- Wave58 closed canonical receptor reopeners.
- Wave59 closed direct lysosomal/sphingolipid enzymes.
- The plausible remaining claim shape is circuit-level: an upstream
  state-transition controller that explains the lipid-lysosomal/APC module
  without generic organelle inhibition or generic immune trafficking/survival
  blockade.

Execution:

- Dispatched Wave60-P `C15ORF48/MOCCI` audit.
- Dispatched Wave60-Q `OSM/OSMR/IL6ST` audit.
- Dispatched Wave60-R hostile methods review.
- Added `scripts/v3_wave60_circuit_coupling_pivot.py`.
- Added the script to `run_v3_analysis.sh`.

## 2026-05-27 12:06 UTC

Executed and integrated local Wave60 circuit-coupling pivot.

Results:

- Outputs: `results_v3/wave60_circuit_coupling_pivot/`.
- Donor-context rows: 309.
- Predictors ranked: 276.
- Full reopeners: 0.
- Parked expression-coupling hypotheses: 63.
- Top coupling rows:
  - `FCGR2B`: FDR 0.000887, five diseases, but only one disease with nominal
    disease-up recurrence and no MS/perturbation support.
  - `GPNMB`: FDR 0.00209 and positive coupling in all five local diseases,
    but no disease-up recurrence in this scoring and efferocytosis screen is
    unresolved.
  - `C15ORF48`: disease-up recurrence and nominal MS support, but circuit
    coupling fails after the residualized cross-context gate.
  - `OSM`: disease-up recurrence in Crohn/UC only, but no circuit coupling or
    MS support.
  - `OSMR`: circuit coupling and disease-up recurrence, but no MS or
    perturbation support.

Decision:

- Do not promote any circuit from donor-level expression coupling.
- Treat Wave60 as a falsification of the expression-only circuit pivot.
- Move to external perturbation-first intervention mining, using the V3 module
  only as a readout rather than as a target-discovery engine.

## 2026-05-27 12:06 UTC

Integrated Wave60-R hostile methods review.

Report:

- `subagents_v3/wave60r_circuit_pivot_hostile_review.md`.

Verdict:

- `NO_GO` for promoting any current donor-level circuit-coupling result.

High-severity criticisms accepted:

- Donor-level coupling is vulnerable to pseudo-replication, tissue
  non-comparability, module collinearity, and residual generic inflammation.
- OSM/OSMR is a useful stress test but likely collapses to known IBD-heavy
  tissue-licensing biology unless spatial/source-target and perturbation data
  show otherwise.
- Treatment-response artifacts remain underpowered and not globally corrected.
- Foundation-model token deletion remains triage unless validated by real
  perturbation.

Action:

- Close expression-only circuit coupling for promotion.
- Continue with perturbation-first intervention-level mining.

## 2026-05-27 12:15 UTC

Integrated Wave60-P C15ORF48/MOCCI audit.

Report:

- `subagents_v3/wave60p_c15orf48_mocci_circuit_audit.md`.

Result:

- `C15ORF48`/MOCCI is biologically real but assay-only for this session.
- Local expression recurrence supports `C15ORF48` as a high-intensity
  inflammatory mitochondrial adaptation marker.
- The actual `C15ORF48`/`NDUFA4` switch is sparse: canonical switch in 1/17
  compartments.
- No usable Geneformer perturbation route, no strong MS-specific support, no
  target genetics, and no clean druggable/safe direction.

Decision:

- Do not promote `C15ORF48` or `NDUFA4`.
- Use the switch only as a possible wet-lab readout for interventions found by
  stronger perturbation-first evidence.
- Continue Wave61 intervention-level mining.

## 2026-05-27 12:19 UTC

Integrated Wave60-Q OSM/OSMR tissue-niche audit.

Report:

- `subagents_v3/wave60q_osm_osmr_circuit_audit.md`.

Result:

- `OSM`/`OSMR`/`IL6ST` is biologically real but IBD-centered.
- It is useful as a comparator or possible OSM-high IBD stratification axis.
- It is not promotable as a cross-autoimmune V3 therapeutic mechanism because
  MS support is absent/unsafe, RA/Sjogren/psoriasis support is weak or null,
  and direct OSM/OSMR clinical/prior-art status is unfavorable.

Decision:

- Close `OSM`/`OSMR` for V3 promotion.
- Do not use OSM biology to rescue the circuit-coupling branch.

## 2026-05-27 12:20 UTC

Failed Wave61 local scorer run.

Script:

- `scripts/v3_wave61_intervention_guardrail_scorer.py`.

Failure:

- Report generation called `DataFrame.to_markdown()` and failed because
  optional dependency `tabulate` is absent in `.venv_v3_py312`.

Action:

- Patched the script with a small local Markdown table renderer.
- Reran without adding dependencies, preserving the pinned environment.

## 2026-05-27 12:24 UTC

Executed and integrated Wave61 perturbation-first guardrail scorer.

Outputs:

- `results_v3/wave61_perturbation_first_guardrail/`.

Results:

- Evidence rows: 395.
- Direct perturbation rows: 186.
- L1000 rows: 180.
- Resolution perturbation rows: 29.
- Promotion candidates: 0.
- Reopened perturbation candidates: 0.

Interpretation:

- Perturbation-first is not a V3 finding route under current evidence.
- `MED16` and `GSK3B` are the strongest real perturbation comparators, but both
  fail disease/MS, repair, genetics, druggability, and safety gates.
- L1000-only rows remain support-only and are not claimable.
- Efferocytosis negative-regulator rows lack disease/MS/druggability support
  and have weak screen statistics.

Decision:

- Close current perturbation-first branch for promotion.
- Continue with a genetics-first target-resolution pivot, because additional
  perturbation ranking without target-resolved causal anchoring would repeat a
  weak operationalization.

## 2026-05-27 12:25 UTC

Wave61-T translational/prior-art sidecar failed.

Notification:

- Agent `019e695a-0760-7842-b806-107d1522eba4` exhausted its model context
  window and did not produce an owned report.

Decision:

- Do not use any result from Wave61-T.
- Do not retry the broad translational audit immediately; it is too wide and
  currently unnecessary because Wave61 found no perturbation survivor.
- If genetics-first identifies a candidate, dispatch a narrower replacement
  audit around that single candidate.

## 2026-05-27 12:31 UTC

Integrated Wave61-S intervention mining audit.

Report:

- `subagents_v3/wave61s_intervention_mining.md`.

Result:

- No perturbation candidate earns promotion.
- `MED16`/Mediator and `GSK3B` are the strongest real perturbation-first
  comparators.
- `TNFRSF1A`, `RFX5`, and `CHUK` are weaker or unsafe.
- RXR/bexarotene and efferocytosis rows are guardrails, not nominations.
- L1000-only, generic IFN/JAK/NF-kB collapse, broad transcriptional hits, and
  prior-demoted targets remain no-go.

Decision:

- Perturbation-first branch is closed for promotion by local code, supportive
  sidecar audit, and hostile review.

## 2026-05-27 12:32 UTC

Opened Wave62 genetics-first target-resolution branch.

Reason:

- Earlier genetics branches were blocked because OpenGWAS authentication and
  local paired SNP-level summary statistics were unavailable.
- A current Open Targets Platform GraphQL probe showed precomputed
  `credibleSet`, `l2GPredictions`, and `colocalisation` fields are available.

Manual probe:

- Disease: `MONDO_0005301` multiple sclerosis.
- Study: `FINNGEN_R12_G6_MS`.
- Credible set: `d8042fac4818035ae4af8557e0cbf623`.
- Lead variant: `19_18181472_C_T`.
- L2G rows include `IFI30` score 0.650.
- QTL colocalisation rows include monocyte `IFI30` eQTL rows.

Decision:

- Try a reproducible Open Targets target-resolution analysis before accepting
  genetics as blocked.

## 2026-05-27 12:36 UTC

Failed first Wave62 local target-resolution run.

Script:

- `scripts/v3_wave62_opentargets_target_resolution.py`.

Failure:

- API retrieval succeeded far enough to write partial output files, but
  summarization failed with `KeyError: 'biosample_name'` when an empty
  MS-relevant QTL-colocalisation subset had no columns.

Action:

- Patched a defensive `unique_join()` helper for empty dataframes.
- Rerun will use cached Open Targets API JSON where available.

## 2026-05-27 12:38 UTC

Completed stricter Wave62 Open Targets target-resolution rerun.

Script:

- `scripts/v3_wave62_opentargets_target_resolution.py`.

Reproducibility:

- Added to `run_v3_analysis.sh`.
- Random seed: `20260527`.
- Uses cached/raw Open Targets Platform GraphQL responses under
  `results_v3/wave62_opentargets_target_resolution/raw_api/`.

Patch before rerun:

- Promoted inherited prior-branch blockers into explicit gates:
  `prior_context_blocker` and `no_prior_context_blocker`.
- Added blockers for targets that previously looked high-scoring but are
  not intervention-grade in the required direction: `TNFAIP3`, `PTPN2`,
  `IL23R`, `IRF5`, `FCGR2A`, `PTPN22`, `STAT4`, `IL2RA`, `TNFRSF1A`,
  `IL6R`, and `PDCD1`.
- Changed report ordering so parked/reopened target-resolution rows are shown
  before high-scoring no-go rows.

Key output:

- Studies queried: 539.
- Eligible GWAS studies with summary statistics and credible sets: 95.
- Credible sets retrieved: 2506.
- L2G rows: 4821.
- QTL colocalisation rows: 16823.
- Targets summarized: 2028.
- Reopen calls: 0.
- Park calls: 32.

Important parked rows:

- `RGS1`, `INAVA`, and `ANKRD55` have MS-resolved L2G plus relevant QTL
  colocalisation and cross-disease genetic recurrence, but lack local
  lipid-lysosomal myeloid module evidence and druggable modality.
- `SP140` has MS/Crohn/psoriasis target-resolved genetics plus local
  cross-disease expression support, but no clean druggable intervention
  route yet.
- `GALC` has MS/Crohn genetic resolution and local expression support, but
  narrow cross-disease breadth and no current modality.
- `IFI30` is module-linked and MS target-resolved, but remains blocked by
  direct antigen-processing host-defense biology and druggability.

API limitation:

- One ankylosing spondylitis study, `GCST90480502`, was skipped because the
  Open Targets GraphQL response was rejected as too expensive even at the
  current request size. This does not affect the zero-reopen conclusion but
  should be handled with smaller paging if AS becomes central.

Decision:

- Genetics-first target resolution is useful as a prioritization layer, not
  as a V3 therapeutic finding.
- Next branch should test whether the strongest parked rows converge on a
  controllable cellular transition or pathway, rather than trying to promote
  one unmodified genetics row.

## 2026-05-27 12:42 UTC

Integrated Wave62-V subagent return.

Report:

- `subagents_v3/wave62v_opentargets_target_resolution.md`.

Accepted:

- The sidecar independently found no promotable Open Targets
  target-resolution candidate.
- `IFI30` is the closest module-relevant target-resolution row, but it is
  MS-only and host-defense/druggability blocked.
- `BACH2` and `IRF5` are useful positive controls for cross-autoimmune
  target-resolved genetics, not V3 candidates.
- `IL7R`, `SP140`, `IL12A`, `STAT4`, and `CD40` remain genetics comparators
  blocked by prior art, mixed direction, tissue relevance, or druggability.

Decision:

- Proceed with a transition-controller integrator that treats Wave62 genetics
  rows as anchors and asks whether any upstream/downstream intervention node
  is more tractable than the genetics gene itself.

## 2026-05-27 12:51 UTC

Closed Wave63 transition-controller integration branch for promotion.

Local script:

- `scripts/v3_wave63_transition_controller_integrator.py`.
- Added to `run_v3_analysis.sh`.
- Output directory: `results_v3/wave63_transition_controller_integrator/`.

Execution history:

- Initial integrator output had 0 promotions and 4 parked rows.
- Hostile review identified two methodological problems:
  - `gate_pass_count` leaked into the gate matrix as a pseudo-gate.
  - druggability was too permissive because target annotation and inherited
    SP140 chemistry could make unrelated intervention routes look tractable.
- Patched:
  - excluded `gate_pass_count` from the gate matrix.
  - stopped treating SP140/TOP literature support as real perturbation or
    ChEMBL activity.
  - added Wave45 regulatory-controller blockers.
  - added Wave59 lysosomal/sphingolipid no-go decisions and directionality
    blockers.
  - required actual activity/modality scores rather than ChEMBL target
    annotation alone for `druggable_or_modality`.

Final Wave63 output:

- Candidates evaluated: 55.
- Promotion calls: 0.
- Park calls: 2.
- Parked rows: `IL7R`, `GALC`.

Interpretation:

- `IL7R` remains parked only as a strong target-resolved genetics/foundation
  comparator, blocked by CD127 prior art, missing real disease-cell
  perturbation, missing repair/efferocytosis guardrail, and missing
  druggability evidence in this table.
- `GALC` remains parked only because it has MS genetic/QTL support, local
  expression recurrence, and enzyme chemistry; it is blocked by weak
  cross-disease target resolution, absent perturbation/foundation support,
  no strict MS/residual expression, and Wave59 directionality/prior-art
  blockers.
- `SP140` and `SP140_TOP1_TOP2_RESCUE` are demoted to no-go for V3 promotion
  after Wave45, Wave63-X, and Wave63-Z.

Subagent integration:

- Wave63-Y `subagents_v3/wave63y_broad_genetics_benchmark.md`: accepted.
  Broad genetics hits (`BACH2`, `IRF5`, `IL7R`, `STAT4`, `SP140`, `IFI30`,
  `CD40`, `IL12A`) are calibration controls, not less-blocked intervention
  routes.
- Wave63-Z `subagents_v3/wave63z_transition_controller_hostile.md`: accepted.
  Minimum promotion bar now requires independent evidence accounting, direct
  human disease-relevant perturbation, held-out state readout, functional
  repair and host-defense guardrails, correct directionality, non-pseudo-
  replicated cross-disease breadth, correct-direction druggability, frozen
  claim-specific prior-art search, and effect-size thresholds.
- Wave63-X `subagents_v3/wave63x_sp140_topoisomerase_transfer.md`: accepted.
  SP140/TOP is demoted for V3 promotion and parked only as Crohn SP140-loss
  stratification/mechanistic comparator.

Decision:

- Do not use transition-controller intersections as `FINDING_V3.md`.
- Next pivot must add genuinely new evidence, preferably a disease-relevant
  perturbation/response dataset or a non-expression modality, rather than
  another reweighting of existing module tables.

## 2026-05-27 12:55 UTC

Wave64 pivot decision.

What I checked:

- Re-read Wave26 strict treatment-response audit output. The best apparent RA
  anti-TNF baseline rows are nominal but fail global baseline FDR, global
  generic-adjusted FDR, and independent same-module replication.
- Pharmacodynamic rows in UC tofacitinib and psoriasis secukinumab are
  underpowered, marker-compartment-derived, and not adequate as therapeutic
  claims.

Decision:

- Do not rerun the same baseline-response audit as if it were new evidence.
- Open a perturbation-first branch that requires real intervention direction
  in human disease-relevant cells or tissues.
- Dispatch sidecar scouts for public perturbation datasets and orthogonal
  non-expression resources, plus a hostile gate reviewer.

## 2026-05-27 12:56 UTC

Dispatch failure noted.

- The first Wave64 subagent spawn attempt failed because full-context agents
  cannot be launched with explicit reasoning-effort overrides.
- Retrying without overrides; no scientific interpretation affected.

## 2026-05-27 12:57 UTC

Wave64 agents are running:

- Wave64-A: perturbation/treatment-response dataset scout.
- Wave64-B: non-expression modality scout.
- Wave64-C: hostile perturbation-gate reviewer.

Operational note:

- The hostile reviewer initially hit the agent thread limit. I closed completed
  Wave62/Wave63 agents and relaunched it. This does not affect prior accepted
  subagent outputs, which remain preserved under `subagents_v3/`.

## 2026-05-27 13:06 UTC

Wave64 SLAMF7 perturbation audit completed.

Script:

- `scripts/v3_wave64_slamf7_perturbation_audit.py`.
- Added to `run_v3_analysis.sh`.
- Output directory: `results_v3/wave64_slamf7_perturbation_audit/`.

Inputs:

- `GSE185509` human monocyte-derived macrophages, IFN-g pre-incubated, then
  unstimulated versus anti-SLAMF7 or recombinant SLAMF7 stimulation.
- Wave62 Open Targets QTL colocalisation rows.
- Local broad h5ad and MS white-matter SLAMF7 expression rows.

Key results:

- `GSE185509` count matrix: 35,203 genes, 11 samples.
- SLAMF7 QTL colocalisation rows from Wave62: 17 rows across UC, T1D, SLE,
  psoriasis, ankylosing spondylitis, and Crohn.
- Direct SLAMF7 engagement strongly increases generic inflammatory modules:
  - anti-SLAMF7 `tnf_autocrine_nfkb`: mean treated-minus-unstimulated 1.628,
    paired FDR 0.0162.
  - r-SLAMF7 `tnf_autocrine_nfkb`: mean treated-minus-unstimulated 1.560,
    paired FDR 0.0173.
  - anti-SLAMF7 `inflammatory_nfkb`: mean treated-minus-unstimulated 1.615,
    paired FDR 0.0181.
- r-SLAMF7 suppresses several module components:
  - `lipid_loader_repair`: -0.859, paired FDR 0.0162.
  - `lysosomal_apc`: -1.182, paired FDR 0.0184.
  - `complement_phagocytosis`: -1.476, paired FDR 0.0181.
- The target-to-generic effect ratio from the Wave64-C gate row is 0.992,
  below the required >=2.0 module-specific threshold.
- Local disease-cell anchor is insufficient:
  - broad h5ad positive diseases: Crohn disease and Sjogren syndrome only.
  - MS white-matter delta 0.248, FDR 0.976.

Decision:

- Call: `PARK_AS_DIRECTIONAL_INFLAMMATORY_RECEPTOR_NOT_V3_TARGET`.
- Interpretation: SLAMF7 is a useful receptor biology comparator. It is not a
  V3 therapeutic nomination because direct stimulation is generic-inflammatory,
  antagonist/signaling-bias direction is untested, MS tissue anchor is absent,
  repair/host-defense guardrails are absent, and published MS/EAE direction is
  conflicted.

Subagent integration:

- Wave64-A recommends `GSE198520` as an immediate RA paired synovial tissue
  analysis and `GSE282122` as the stronger but compute-heavy IBD single-cell
  analysis.
- Wave64-B recommends a non-expression metabolomics/lipidomics class-level
  meta-analysis as the best orthogonal branch.
- Wave64-C gates are now accepted: no perturbation route can promote without
  disease-cell anchor, direct human perturbation, direction, generic
  inflammation specificity, composition/batch controls, held-out readouts,
  repair and host-defense guardrails, cross-disease replication, and prior-art
  freeze.

Next pivot:

- Run `GSE198520` first because it is disease tissue, paired anti-TNF,
  lightweight, and response-labeled. Treat it as tissue-level perturbation
  evidence only; residualize against generic inflammation and do not claim
  cell-intrinsic myeloid biology from bulk synovium.

## 2026-05-27 15:14 CEST

Wave65 `GSE198520` RA paired synovium anti-TNF audit completed.

Script:

- `scripts/v3_wave65_gse198520_ra_synovium_antitnf_audit.py`.
- Added to `run_v3_analysis.sh`.
- Output directory:
  `results_v3/wave65_gse198520_ra_synovium_antitnf_audit/`.

Run issue and correction:

- First run failed because the GEO series matrix also contained a `timepoint`
  characteristic, so the merge produced `timepoint_x/timepoint_y` and the
  paired-delta function could not find `timepoint`.
- Patched the script to keep parsed count-column `timepoint` as canonical and
  store GEO timepoint separately as `geo_timepoint`.
- Also patched the generic/pathotype-adjusted response model to include only
  available non-target generic covariates, avoiding target/covariate overlap.

Inputs:

- `GSE198520_Raw_gene_count_matrix.txt.gz`.
- `GSE198520_series_matrix.txt.gz`.
- 92 samples from 46 RA patients; paired pre-treatment and week-12
  post-anti-TNF synovial bulk RNA-seq.
- Response classes: 19 good, 13 moderate, 14 none.
- Pathotypes: 21 Myeloid, 17 Lymphoid, 8 Fibroid.

Key results:

- All modules failed Wave65 gates; no module was promoted.
- Strong paired all-patient pharmacodynamic decreases were seen, but they did
  not exceed generic inflammation controls:
  - `mif_cd74_receptor_state`: mean post-pre -0.346, FDR 0.00927,
    target/generic ratio 0.985.
  - `mixscale_validated_ifng_readout`: -0.404, FDR 0.00927,
    target/generic ratio 1.148.
  - `hif_nampt_metabolic`: -0.278, FDR 0.00927, ratio 0.790.
  - `lysosomal_apc`: -0.291, FDR 0.0340, ratio 0.827.
  - `lipid_loader_repair`: -0.0967, FDR 0.238, ratio 0.275.
- No module survived good-responder versus other response-specific testing after
  generic/pathotype adjustment:
  - adjusted FDRs were 0.655 to 0.999.

Decision:

- Call: all rows `NO_GO_GSE198520_BULK_TISSUE`.
- Interpretation: anti-TNF-responsive RA synovium shows broad inflammatory
  state contraction. This is useful tissue-level pharmacodynamic evidence but
  does not identify a lipid-lysosomal/APC-specific intervention point.
- Do not continue bulk treatment-response signature scoring as the primary
  route. Next routes should be either cell-resolved perturbation
  (`GSE282122`, compute permitting) or the orthogonal metabolomics/lipidomics
  branch from Wave64-B.

## 2026-05-27 15:32 CEST

Wave66 cross-autoimmune metabolomics/lipidomics class audit completed.

Script:

- `scripts/v3_wave66_metabolomics_class_convergence.py`.
- Added to `run_v3_analysis.sh`.
- Output directory: `results_v3/wave66_metabolomics_class_convergence/`.

Inputs:

- Metabolomics Workbench studies queried through REST endpoints:
  - `ST001949` RA plasma control/RA/RA+MTX.
  - `ST000899` Crohn/UC/control serum.
  - `ST002470` UC plasma severity/improvement.
  - `ST002732` SLE plasma lipidome/coronary calcification group.
  - `ST002949` ankylosing spondylitis/control serum.
  - `ST000422` T1D/control plasma.
  - `ST003328` patient stem-cell-derived MS model cellular lipidomics.
  - `ST000298` psoriasis biopsy steroid metabolites.
  - `ST001636` TEDDY lipidomics availability only.
  - `ST001386` TEDDY metabolomics summary only; factor fetch hung and was
    downscoped rather than blocking the session.

Run issue and correction:

- First run failed on an over-escaped regex in metabolite class harmonization.
  Fixed before inference.
- Second run hung on `ST001386` availability-only factor fetch. Terminated the
  run, marked `ST001386` summary-only, and reran.
- Patched feature-level tests to count finite observations before t-tests so
  sparse feature provenance rows do not dominate warnings.

Key results:

- Downloaded usable individual-level feature data for 8 studies.
- Produced 218 class-contrast rows and 7,835 feature-provenance rows.
- No biochemical class passed the candidate gate.
- Most relevant weak/descriptive lipid-class hints:
  - `ceramide`: tested in 6 diseases/model systems; 5 same direction;
    supportive in `MS_model`, `RA`, `SLE`; median Hedges g 0.712; one
    normalizing treatment/improvement hit.
  - `glycosphingolipid`: tested in 5; 4 same direction; supportive in
    `MS_model`, `RA`, `UC`; median Hedges g 0.640.
  - `lysophosphatidylcholine`: tested in 6; 4 same direction; supportive in
    `MS_model`, `RA`; one normalizing hit.
  - `phosphatidylcholine`: tested in 6; 4 same direction, but dominant
    direction lower in case/worse and supportive in `AS`, `Crohn`, `UC`.
- Stronger non-lipid class pattern:
  - `amino_acid`: supportive in `AS`, `Crohn`, `RA`, `UC`, but this does not
    map specifically to the lipid-lysosomal/APC therapeutic mechanism.

Decision:

- Call: biochemical audit is informative but not promotable.
- Interpretation: ceramide/glycosphingolipid abnormalities remain plausible
  orthogonal support for a sphingolipid/lysosomal stress axis, but not a
  therapeutic target. This branch should be used to prioritize cell-resolved
  myeloid perturbation endpoints rather than claim a serum biomarker.

Wave66-B subagent returned and was accepted as a feasibility result:

- Report: `subagents_v3/wave66b_gse282122_feasibility.md`.
- Key finding: `GSE282122` is feasible through Zenodo record `14007626`
  `myeloid_final.h5ad` (416,722,961 bytes, MD5
  `bdfe50345a11abdb1a72b2439bf9950e`) and `paired_sample_list.csv`.
- GEO-only route is demoted because GEO exposes per-sample 10x matrices, not
  the annotated myeloid object.
- The myeloid object reportedly contains 30,858 cells x 33,075 genes, broad
  states `Mono_macro` and `DC`, remission labels, patient/site/timepoint
  metadata, and 55 derived site-matched pre/post pairs.

Next pivot:

- Implement `GSE282122` myeloid pseudobulk analysis locally using only Zenodo
  `myeloid_final.h5ad` and `paired_sample_list.csv`.
- Primary endpoints: `Mono_macro` and `DC` module deltas in paired pre/post
  anti-TNF biopsies, with remission interaction and generic TNF/NF-kB controls.

## 2026-05-27 15:47 CEST

Wave67 `GSE282122` myeloid anti-TNF pseudobulk audit completed.

Script:

- `scripts/v3_wave67_gse282122_myeloid_pseudobulk.py`.
- Added to `run_v3_analysis.sh`.
- Output directory: `results_v3/wave67_gse282122_myeloid_pseudobulk/`.

Inputs:

- Zenodo record `14007626`.
- `myeloid_final.h5ad`, 416,722,961 bytes, MD5
  `bdfe50345a11abdb1a72b2439bf9950e`.
- `paired_sample_list.csv`, MD5 `3300a53889bb4b70c48ec66dbb66beea`.
- h5ad shape: 30,858 cells x 33,075 genes.
- Pseudobulk output: 754 strata and 4,059 site/state/module delta rows.

Key results:

- All six primary major-state target module gates failed or parked:
  - `NO_GO_GSE282122_MYELOID`: `Mono_macro complement_phagocytosis`,
    `DC lipid_loader_repair`, `Mono_macro lipid_loader_repair`.
  - `PARK_CELL_RESOLVED_PD_SIGNAL_ONLY`: `DC lysosomal_apc`,
    `Mono_macro lysosomal_apc`, `DC complement_phagocytosis`.
- `lipid_loader_repair` is essentially null:
  - `DC`: all-pair delta 0.0086, FDR 1.0, target/generic ratio 0.101,
    CD delta -0.0577, UC delta 0.0780.
  - `Mono_macro`: all-pair delta -0.0075, FDR 1.0, target/generic ratio
    0.041, CD delta -0.107, UC delta 0.079.
- `lysosomal_apc` has weak positive deltas but not enough specificity:
  - `DC`: all-pair delta 0.144, FDR 0.708, target/generic ratio 1.686,
    CD and UC same sign, but no remission interaction after adjustment.
  - `Mono_macro`: all-pair delta 0.122, FDR 0.836, target/generic ratio
    0.674.
- No target module had generic-adjusted remission-interaction FDR <= 0.10;
  adjusted FDRs were 0.976 to 1.0.
- The strongest non-target module signals were HLA-II/MIF-CD74-like:
  - `DC hla_ii_apc`, CD paired raw p 0.000333, global FDR 0.103.
  - `DC hla_ii_apc`, remission raw p 0.000201, global FDR 0.103.
  - `Mono_macro hla_ii_apc`, remission raw p 0.00174, global FDR 0.200.

Decision:

- The pre-specified lipid-lysosomal/APC target-module hypothesis is not
  supported by the strongest available cell-resolved anti-TNF perturbation
  dataset.
- This does not close the cross-autoimmune myeloid-state question, but it
  blocks direct promotion of lipid-loader, lysosomal-APC, or complement
  phagocytosis modules as intervention axes.
- Next pivot: use the same high-value `GSE282122` myeloid object for an
  unrestricted gene-level perturbation screen in `Mono_macro` and `DC`, then
  intersect any robust genes with Wave62 cross-autoimmune genetics and
  druggability. This avoids staying trapped in the prior module definition.

## 2026-05-27 15:54 CEST

Wave68 unrestricted `GSE282122` myeloid/DC gene screen completed and was
corrected after a reporting/triage bug.

Script:

- `scripts/v3_wave68_gse282122_unrestricted_gene_screen.py`.
- Output directory:
  `results_v3/wave68_gse282122_unrestricted_gene_screen/`.
- Added guardrail: `SP140` is now blocked by the already-completed V3
  SP140/topoisomerase audit rather than reopened by the unrestricted screen.
  The post-hoc blocker is
  `v3_sp140_prior_art_direction_conflict_ms_local_null`.
- Reporting sort fixed so `PARK_GENETIC_PERTURBATION_INTERSECTION` rows appear
  before generic descriptive rows.

Inputs:

- Reused `GSE282122` / Zenodo `14007626` myeloid object from Wave67.
- Cell states: `Mono_macro` and `DC`.
- Genes tested: 33,075.
- Primary paired rows before thresholding: 110; thresholded rows: 86.
- Patient units for remission-response tests: 29.

Key result:

- No gene is now called `REOPEN_GENE_LEVEL_TARGET_CANDIDATE`.
- Calls after correction:
  - `DESCRIPTIVE_GENE_SIGNAL`: 66,137.
  - `PARK_GENETIC_PERTURBATION_INTERSECTION`: 13.
- Top parked intersections:
  - `RGS14` in DC: adjusted remission delta 1.872, adjusted FDR 0.0113,
    Wave62 score 5.30, cross-autoimmune genetics true, but no druggability
    flag.
  - `CD274` in DC: adjusted delta -1.910, adjusted FDR 0.0243, broad QTL
    colocalization, but no direct druggability flag in Wave62 and checkpoint
    biology is likely prior-art/safety constrained.
  - `LPP`, `ARHGAP31`, `TNFSF15`, `NCF1`, `CD80`, `FCGR2B`, `IL7R`, `STAT4`,
    `TNFRSF9`, `DCLRE1B`, and `FCGR2A` remain parked, not promoted.
- `SP140` in `Mono_macro` had a nominal/adjusted remission-response signal
  before the guardrail (adjusted delta -1.508, adjusted FDR 0.0469), but it is
  now descriptive only because Wave56/Wave63 already rejected it for V3
  therapeutic promotion.

Interpretation:

- The unrestricted screen succeeded as a falsification tool: it prevents the
  session from overfitting the lipid-lysosomal module, but it does not yet
  provide a direct target.
- The current viable route is no longer direct module/gene promotion. The next
  forcing question is whether any parked gene-level signal points to a
  druggable upstream or downstream intervention point with less prior-art and
  safety blockage.

## 2026-05-27 16:15 CEST

Wave69 parked-gene/controller branch completed through controller ranking,
independent validation, feasibility audit, and a bounded Geneformer remission
centroid screen.

Subagent returns:

- Wave69-A (`subagents_v3/wave69a_parked_gene_controller_triage.md`):
  accepted. Verdict: none of the 13 Wave68 parked genes is a direct
  therapeutic anchor. The useful pattern is a blocked comparator panel of APC
  costimulation/checkpoint genes plus Fc/ROS myeloid-balance genes.
- Wave69-B (`subagents_v3/wave69b_independent_validation_scout.md` and
  `scripts/v3_wave69b_independent_validation_scout.py`): accepted. Verdict:
  no parked candidate should be reopened. `IL7R`, `CD274`, and `SP140` have
  the strongest cross-dataset expression recurrence but remain markers or
  blocked comparators. `FCGR2B` and `NCF1` move in bulk RA synovium after
  anti-TNF but not as a cell-resolved controller claim. `RGS14` does not
  validate independently.
- Wave69-C (`subagents_v3/wave69c_foundation_model_feasibility.md`):
  accepted. Verdict: Arc State remains blocked for named-gene claims because
  exposed features are numeric IDs; the runnable replacement is a narrow local
  Geneformer V2-104M token-deletion screen on `GSE282122` remission centroids.

Local controller rank:

- Script: `scripts/v3_wave69_parked_controller_rank.py`.
- First run wrote core outputs but failed at report generation because failed
  Enrichr rows lacked `adjusted_p`.
- Patch: use proper Enrichr multipart `files=` submission, tolerate partial
  enrichment schemas, and add blockers for broad kinase false leads
  (`FYN/SRC/LYN/MAPK14/GSK3A/GSK3B/INSR`).
- Final output: `results_v3/wave69_parked_controller_rank/`.
- Enrichr confirmed that the 13 parked genes are dominated by immune system,
  checkpoint/costimulation, Fc-gamma phagocytosis/phagosome, TNF receptor, and
  cytokine-signaling terms.
- After blockers, only `PRKDC` and `BLK` remained as
  `PARK_DRUGGABLE_CONTROLLER_SCOUT_NEEDS_DIRECT_VALIDATION`.

Foundation-model test:

- Script: `scripts/v3_wave69d_gse282122_geneformer_remission_centroid.py`.
- First run completed model computation but failed report generation because
  per-context metrics were not annotated with support flags. Patched and reran.
- Model: local Geneformer V2-104M, 104,365,056 encoder parameters, seed
  `20260527`.
- Contexts: post-treatment non-remission vs remission centroids in
  `GSE282122` `DC` and `Mono_macro`, combined CD/UC and disease-specific CD
  and UC contexts.
- Result: `PRKDC` and `BLK` were not rescued.
  - `PRKDC`: one usable context with token count >=3? No; best support row had
    only one non-remission cell with token, so `NO_GO_MODEL_REMISSION_SCREEN`.
  - `BLK`: no detectable token in selected myeloid/DC non-remission cells,
    `NO_GO_MODEL_REMISSION_SCREEN`.
- Model support occurred only for blocked comparators:
  - `FCGR2A`: 1 strong support context, 2 support contexts, best z 1.057.
  - `JAK1`: 1 strong support context, best z 0.719.
  - `IL7R`: 1 strong support context, best z 1.348.
  - `CD80`: 1 strong support context, best z 0.501.
  - `NCF1`: 3 support contexts, no strong context.

Decision:

- Do not promote `PRKDC`, `BLK`, or any direct Wave68 parked gene.
- The robust current biological pattern is not a clean target but a blocked
  comparator circuit: Fc receptor/ROS myeloid handling plus checkpoint/
  costimulation/JAK cytokine response in treatment-remission states.
- Next pivot must either find a less-blocked modality around Fc/ROS resolution
  or leave this branch as mechanistically informative but therapeutically
  blocked.

## 2026-05-27 16:23 CEST

Wave70 local Fc/ROS-resolution matrix completed.

Script and outputs:

- `scripts/v3_wave70_fc_ros_resolution_matrix.py`.
- `results_v3/wave70_fc_ros_resolution_matrix/`.
- Added to `run_v3_analysis.sh`.

Result:

- 29 candidate Fc/ROS/inhibitory-resolution nodes tested across existing V3
  evidence channels: `GSE282122`, broad h5ad recurrence, residual gate,
  `GSE111972` MS white matter, RA anti-TNF synovium pharmacodynamics,
  target-resolution genetics, efferocytosis CRISPR, Geneformer screens, and
  perturbation guardrails.
- No candidate was promoted. Calls were:
  - `NO_GO_BLOCKED_OR_BROAD_CLASS`: 14.
  - `NO_GO_INSUFFICIENT_CONVERGENCE`: 15.
- Strongest evidence nodes were blocked comparators:
  - `FCGR2A` and `NCF1`: evidence count 4 but blocked by Fc-receptor
    directionality/safety and NOX2 host-defense risk.
  - `NCF2`, `CYBB`, `LYN`, `SYK`, `BTK`, and `PIK3CD`: recurring but blocked
    by broad host-defense, kinase, or prior-art concerns.
- Less-blocked but insufficient nodes:
  - `LILRB2`: evidence count 2. Supported by `GSE282122` adjusted
    post-treatment remission/non-remission signal and broad Crohn/UC myeloid
    recurrence, but lacks MS replication, genetics, RA support, or model
    support.
  - `LILRB1`, `LILRB3`, `LILRB4`: `GSE282122` support only or weak broad
    support.
  - `INPP5D`: RA anti-TNF pharmacodynamic movement only.

Decision:

- Do not reopen an Fc receptor, NOX2, broad kinase, JAK, or checkpoint target.
- Treat `LILRB2` as a directional falsification target only. The observed
  pattern could mean either:
  - high `LILRB2` marks a maladaptive non-remission/inflamed myeloid state and
    suppression is beneficial; or
  - high `LILRB2` is a compensatory inhibitory brake and agonism/restoration is
    the biologically correct direction.
- The next test must directly evaluate perturbation direction in the
  `GSE282122` remission-centroid model. A clean expression association is not
  enough.

## 2026-05-27 16:27 CEST

Wave70-B local computational scout completed and reported.

Script and outputs:

- `scripts/v3_wave70b_fc_ros_computational_scout.py`.
- `results_v3/wave70b_fc_ros_computational_scout/`.
- Report: `subagents_v3/wave70b_fc_ros_computational_scout.md`.
- Added to `run_v3_analysis.sh`.

Scope:

- Candidate nodes: `INPP5D`, `PTPN6`, `LILRB1`, `LILRB2`, `LILRB4`,
  `LAIR1`, `SIGLEC10`, `CD300A`, `BTK`, `PIK3CD`, `PIK3CG`, `MERTK`,
  `AXL`, `TYRO3`, `GAS6`, `PROS1`, `CD300LF`, `PTPN11`, `SH2D1B`.
- Data used locally: direct `GSE282122` myeloid h5ad candidate pseudobulk,
  Wave68 integrated GSE282122 rows, `GSE111972`, broad h5ad recurrence,
  RA `GSE198520`, Wave37 efferocytosis CRISPR, and existing Geneformer
  outputs.

Run note:

- First complete run produced all tables but failed while rendering Markdown
  because pandas required the optional `tabulate` package. Patched the script
  with a dependency-free Markdown formatter and reran successfully.

Result:

- Integrated calls:
  - `PARK_BLOCKED_OR_DIRECTIONALLY_UNRESOLVED`: 16.
  - `DESCRIPTIVE_SIGNAL_ONLY`: 2.
  - `NO_GO_LOCAL_SUPPORT_WEAK`: 1.
- No candidate promoted.
- Strongest local signal:
  - `LILRB2`: support score 4; `GSE282122` DC adjusted beta `-0.949`, FDR
    `0.0191`; Wave68 adjusted delta `-0.884`, FDR `0.0224`; broad h5ad 2
    Crohn/UC positive compartments with 1 FDR10; MS `GSE111972` nominally down
    delta `-0.730`, p `0.00778`, FDR `0.834`; RA anti-TNF null, delta
    `-0.136`, FDR `0.278`.
  - `LILRB1` and `LILRB4` had strong `GSE282122` Mono_macro
    remission-response rows but no RA replication or genetic anchor.
- Comparator/readout signals:
  - `INPP5D`: RA anti-TNF paired decrease `-0.386`, FDR `0.0294`, and Wave37
    efferocytosis KO-enhancement trend LFC `0.477`.
  - `PTPN6`: RA anti-TNF paired decrease `-0.603`, FDR `0.0583`.
  - `CD300A`: Wave37 KO-enhancement trend LFC `1.338`, but no disease-state
    recurrence.
- TAM nodes stayed blocked: `AXL` had a `GSE282122` Mono_macro raw/adjusted
  signal, but broad recurrence was negative/contradictory and the plausible
  therapeutic direction remains agonism/restoration rather than available
  kinase inhibition.

Decision:

- Accept Wave70-B as a negative/comparator scout.
- Do not claim an Fc/ROS-resolution target.
- Keep `LILRB2` only as a falsification target requiring direct perturbation in
  disease-relevant human myeloid cells with phagocytosis/efferocytosis,
  TNF/IFN/APC, ROS, lipid handling, and viability readouts.

## 2026-05-27 16:33 CEST

Wave70-C inhibitory-receptor Geneformer directionality screen completed.

Script and outputs:

- `scripts/v3_wave70c_inhibitory_receptor_geneformer_direction.py`.
- `results_v3/wave70c_inhibitory_receptor_geneformer_direction/`.
- Added to `run_v3_analysis.sh`.

Model:

- Local Geneformer V2-104M checkpoint from
  `tmp_v3/foundation_wave6/geneformer_assets/Geneformer-V2-104M`.
- Loaded encoder parameters: 104,365,056.
- Random seed: `20260527`.
- Contexts: `GSE282122` post-treatment non-remission vs remission centroids in
  `DC` and `Mono_macro`, combined CD/UC and CD-only/UC-only subsets.

Result:

- Calls:
  - `MODEL_SUPPORT_BUT_BLOCKED_COMPARATOR`: 4.
  - `MODEL_OPPOSING_BUT_BLOCKED_COMPARATOR`: 4.
  - `NO_GO_MODEL_DIRECTION_SCREEN`: 13.
  - `NO_GO_LOW_TOKEN_SUPPORT`: 8.
- Model support concentrated on blocked Fc/NOX comparators:
  - `NCF1`: 2 strong support contexts, 3 support contexts.
  - `FCGR2A`: 2 strong support contexts, 3 support contexts.
  - `CYBB`: 1 strong support context, 2 support contexts.
  - `NCF2`: 3 support contexts, no strong support.
- Directionally opposite or mixed blocked comparator signals:
  - `FCGR2B` deletion moved away from the remission centroid in 2 contexts,
    consistent with a compensatory/restorative inhibitory-Fc direction, but
    direct Fc-receptor targeting remains blocked by directionality and safety.
  - `LYN` and `CYBA` were mixed/broad-class blocked.
- Less-blocked routes failed the reopener threshold:
  - `LILRB2`: 0 strong support contexts, 2 support contexts, 1 opposing
    context, 4 contexts with token support; call
    `NO_GO_MODEL_DIRECTION_SCREEN`.
  - `LILRB1`: 1 strong support context but only 2 contexts with token support
    and evidence count 1; call `NO_GO_MODEL_DIRECTION_SCREEN`.
  - `LILRB4`: weak restoration-like signal but only 1 token-supported context;
    call `NO_GO_MODEL_DIRECTION_SCREEN`.
  - `INPP5D`: 1 support context, no strong support, only 1 token-supported
    context; call `NO_GO_MODEL_DIRECTION_SCREEN`.
  - `SIGLEC10`: model support but no local evidence convergence.

Decision:

- Close the Fc/ROS-resolution target branch for now.
- Carry forward the mechanistic lesson only: the treatment-remission model is
  sensitive to Fc/NOX biology, but the actionable nodes are blocked and the
  less-blocked inhibitory-receptor/SHIP1/TAM alternatives do not converge.
- Next pivot must leave the Fc/ROS neighborhood and run a broader survivor
  search across prior V3 branches.

## 2026-05-27 16:49 CEST

Resumed after usage-limit reset. User clarified that waiting/log gaps do not
count toward active working hours, so the V3 session continues and
`EXHAUSTION.md` remains unavailable.

Integrated Wave71-B prior-branch synthesis:

- Artifact: `subagents_v3/wave71b_prior_branch_status_synthesis.md`.
- Accepted as a hostile memory artifact, not as a finding.
- Core rule reinforced: do not reopen a branch from expression recurrence,
  module coupling, mapped-gene genetics, ChEMBL availability, or Geneformer-only
  support. Reopen only with a new evidence channel that answers the decisive
  blocker.
- Branches explicitly not reopened from current evidence:
  `ACSL1`, `NAMPT`, cathepsins/`CTSH`, complement/`CFB`, `GPR65`,
  `MFGE8`, `PTPN2`/`PTPN22`, `CXCR2`, `IL7R`, `SP140`, `SLAMF7`,
  FADS/SQLE/lipid-metabolism, and Fc/ROS/LILRB/`INPP5D`.

Local vetting after Wave71-B:

- Checked Wave69 `PRKDC`/`BLK` parked controller scouts rather than starting a
  redundant new wave.
- They were already stress-tested in Wave69D/Wave70:
  - `PRKDC`: one weak Geneformer support row, no strong support, no remission
    expression response, no broad cell-state support.
  - `BLK`: no usable Geneformer token in relevant myeloid/DC non-remission
    contexts, no local myeloid expression anchor, and no remission-response
    replication.
- Decision: do not reopen `PRKDC` or `BLK`.

Orthogonal proteome/metabolome reroute:

- Inspected older MS foamy/MIMS proteome output
  `results/mims2_proteome_convergent_targets.tsv`.
- Top convergent proteins include `ASAH1`, `GPNMB`, `IFI30`, `TPP1`,
  `LAMP1`, `CTSD`, `ALDH1A1`, `ACSL1`, `NAMPT`, `SLC25A24`, and `CTSL`.
- This provides independent support that the lesion/MIMS state is lysosomal,
  ceramide/sphingolipid-adjacent, and antigen-processing enriched.
- It does not rescue a target:
  - `ASAH1`: Geneformer/druggability hints, but no cross-disease genetics,
    no MS genetic anchor, negative local recurrence in Crohn/UC, no
    perturbation support, and unresolved/toxic ceramide-axis direction.
  - `GALC`: strongest lysosomal genetic/local comparator, but failed
    Geneformer, strict MS white-matter, module-residual, perturbation, safe
    directionality, and prior-art gates in Wave59.
  - `IFI30`: module-relevant and MS target-resolution compatible, but already
    demoted as a downstream antigen-processing/state marker rather than a
    pan-autoimmune intervention point.

Integrated Wave71-A:

- Script/output:
  `scripts/v3_wave71_global_survivor_meta_rank.py`,
  `results_v3/wave71_global_survivor_meta_rank/`.
- Result: no candidate reopens. Top non-reopening rows are `CD58`,
  `CARMIL1`, `RAD51B`, `PARK7`, `ADCY3`, `FADS1`, `CCDC88B`, `PRR5L`, `YDJC`,
  and `ARID5B`, all blocked by insufficient independent convergence, missing
  perturbation/model support, missing actionable modality, or branch blockers.

Integrated Wave71-C and executed Wave72:

- Wave71-C suggested biochemical/context-stratified routes outside Fc/ROS:
  `NAAA`, `EPHX2`, `GPR183`, and `P2RX7`, with `MFGE8`, `GPR65`, and
  `SLC15A4` as comparators.
- Added and ran
  `scripts/v3_wave72_lipid_mediator_intervention_scout.py`.
- Outputs: `results_v3/wave72_lipid_mediator_intervention_scout/`.
- Reproducibility correction: initial Wave72 report generation failed because
  `pandas.to_markdown()` needed optional `tabulate`. Replaced it with an
  internal Markdown-table writer and reran successfully.
- Wave72 calls:
  - `NAAA`: `NO_GO_WAVE72`.
  - `EPHX2`: `PARK_ORTHOGONAL_BIOCHEMICAL_SCOUT`.
  - `GPR183`: `NO_GO_WAVE72`.
  - `P2RX7`: `PARK_ORTHOGONAL_BIOCHEMICAL_SCOUT`.

Decision:

- Do not write `FINDING_V3.md`.
- Do not reopen Wave71 expression/genetics survivors.
- Next forcing test is a bounded `P2RX7`/purine-inflammasome stratification
  branch, because Wave72 found broad purine biochemical disturbance across
  `AS`, `Crohn`, `RA`, `T1D`, and `UC` but no target-level gene convergence.

## 2026-05-27 16:59 CEST

Wave73 `P2RX7`/purine-inflammasome stratification branch completed.

- Script: `scripts/v3_wave73_p2rx7_stratification_test.py`.
- Outputs: `results_v3/wave73_p2rx7_stratification_test/`.
- Added to `run_v3_analysis.sh`.
- Validation:
  - `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave73_p2rx7_stratification_test.py`
  - `.venv_v3_py312/bin/python scripts/v3_wave73_p2rx7_stratification_test.py`
- Verdict: `PARK_P2RX7_STRATIFICATION_NEEDS_TARGET_LEVEL_DATA`.

Key result:

- Wave72 purine biochemistry is broad, but Wave73 does not resolve it to a
  target-level P2RX7 claim.
- Broad `p2rx7_inflammasome` signal appears in 5 of 17 contexts and 3 diseases
  (`Crohn disease`, `type 1 diabetes mellitus`, `ulcerative colitis`), but has
  zero specificity-pass contexts versus generic inflammatory modules.
- In MS GSE111972, the P2RX7 module is not positively anchored
  (mean effect `-0.214`, combined `p=0.0608`, FDR `0.0912`).
- In IBD GSE282122, the best remission-response row is not significant
  (DC mean effect `0.0884`, combined `p=0.223`, FDR `0.499`).
- In RA GSE198520, the module drops after anti-TNF but is not
  responder-specific (`good_vs_other_p=0.533`, `modgood_vs_none_p=0.491`).

Decision:

- Do not promote P2RX7.
- Wrote `CONVERGENCE_CHECK_34.md`.
- Next pivot: test `EPHX2` only with a direct epoxide/diol-ratio
  operationalization from raw metabolomics if those paired features exist.

## 2026-05-27 17:05 CEST

Wave74 `EPHX2` direct-ratio audit completed.

- Script: `scripts/v3_wave74_ephx2_direct_ratio_audit.py`.
- Outputs: `results_v3/wave74_ephx2_direct_ratio_audit/`.
- Added to `run_v3_analysis.sh`.
- Validation:
  - `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave74_ephx2_direct_ratio_audit.py`
  - `.venv_v3_py312/bin/python scripts/v3_wave74_ephx2_direct_ratio_audit.py`
- Initial implementation issue:
  - the first classifier counted generic `oxo` metabolites as oxylipins.
  - tightened the classifier to named EPHX2 substrate/product families and
    PUFA oxylipins only, then reran.

Key result:

- Corrected EPHX2-relevant feature count: 37.
- Same-study same-site epoxide/diol pairs: 0.
- Direct product/substrate ratio tests: 0.
- Proxy diol-supportive diseases: 2 (`T1D`, `UC`).
- Verdict: `NO_GO_EPHX2_DIRECT_RATIO_UNAVAILABLE`.

Decision:

- Do not promote EPHX2.
- Wrote `CONVERGENCE_CHECK_35.md`.
- Pivot away from single lipid-mediator enzyme candidates unless a new data
  channel gives target-level activity or perturbation evidence.



## 2026-05-27 16:58 CEST

Executed Wave73 `P2RX7`/purine-inflammasome stratification test.

Script/output:

- `scripts/v3_wave73_p2rx7_stratification_test.py`
- `results_v3/wave73_p2rx7_stratification_test/`

Question:

- Does the Wave72 broad purine metabolomics signal correspond to a
  cell-resolved `P2RX7`/`IL1B`/`NLRP3`/`CASP1` state that predicts treatment
  response beyond generic inflammatory modules?

Result:

- Integrated call:
  `PARK_P2RX7_STRATIFICATION_NEEDS_TARGET_LEVEL_DATA`.
- Gate count: 2/7.
- Positive gates:
  - biochemical purine support from Wave72.
  - broad cell-state support.
- Failed gates:
  - specificity against generic inflammatory modules.
  - MS white-matter module anchor.
  - IBD anti-TNF response prediction in `GSE282122`.
  - RA anti-TNF response prediction in `GSE198520`.
  - target-level `P2RX7` gene anchor.

Key numbers:

- Broad h5ad `p2rx7_inflammasome` module:
  - 17 tested contexts.
  - 5 positive contexts.
  - 5 FDR10 positive contexts.
  - 3 positive diseases: Crohn disease, type 1 diabetes, ulcerative colitis.
  - 0 specificity-pass contexts versus generic modules.
- MS `GSE111972` white matter:
  - `p2rx7_inflammasome` mean effect `-0.214`.
  - combined p `0.0608`, FDR `0.0912`.
  - call `NO_MS_MODULE_SUPPORT`.
- IBD `GSE282122` anti-TNF:
  - best response row was DC remission-delta difference.
  - mean effect `0.0884`, p `0.223`, FDR `0.499`.
  - expected-direction support false.
- RA `GSE198520` anti-TNF:
  - paired pre/post drop for `p2rx7_inflammasome` was significant
    (`mean_post_minus_pre=-0.140`, paired p `0.00374`, paired FDR `0.0100`),
    but responder separation failed (`good_vs_other_delta=-0.0633`,
    FDR `0.593`).

Decision:

- Do not promote `P2RX7` or a purinergic-inflammasome stratification claim.
- Keep only a weaker biological observation: extracellular purine metabolism
  is disturbed across several autoimmune inflammatory contexts, but local data
  do not identify `P2RX7` as the central or intervention node.
- The next pivot should test another orthogonal biochemical/context branch
  only if it has a stronger disease-specific measurement than the purine
  proxy did.

## 2026-05-27 17:00 CEST

Dispatched Wave74 sidecars.

Reasoning:

- I am not reopening `P2RX7` from purine metabolomics alone. Wave73 showed that
  this would be another weak operationalization.
- `EPHX2` remains the only Wave72 biochemical branch with more than one
  supportive disease and a normalization hit, but it requires a specificity
  audit against generic lipid disturbance.
- `GPR183` failed Wave72 but is mechanistically different: it may operate as an
  oxysterol niche/trafficking axis rather than a bulk abundance marker.
- A hostile prior-art/druggability scout is necessary because all three
  biochemical candidates have substantial existing immunology literature.

Sidecars:

- Wave74-A: `EPHX2`/oxylipin specificity audit.
- Wave74-B: `GPR183`/oxysterol-niche audit.
- Wave74-C: prior-art/druggability scout for `EPHX2`, `GPR183`, `P2RX7`.

Local work while they run:

- Audit post-Wave70 integrated tables for any candidate that survived for a
  reason stronger than recurrence, mapped-gene genetics, ChEMBL availability,
  or Geneformer-only direction.

## 2026-05-27 17:05 CEST

Wave74-C prior-art/druggability scout returned.

Artifact:

- `subagents_v3/wave74c_prior_art_druggability_scout.md`

Accepted parts:

- `EPHX2` broad autoimmune/MS/IBD use is prior-art blocked by old soluble
  epoxide hydrolase inhibitor autoimmune claims and direct EAE/IBD disease
  model publications.
- `GPR183` broad autoimmune/IBD/RA use is prior-art blocked by active
  `IPG11406` clinical programs in UC and lupus nephritis plus published RA
  antagonist medicinal chemistry.
- `P2RX7` is translation-blocked by prior RA and Crohn human trials and
  MS-specific antagonist-use patent coverage.

Verification:

- I independently checked primary or near-primary sources for the key claims:
  Google Patents `WO2000023060A2`, PubMed/PMC for sEH EAE, ClinicalTrials
  search results for `NCT07535489` and `NCT06717815`, RA GPR183 medicinal
  chemistry `PMID 38047891`, PubMed/ClinicalTrials for P2X7 RA/Crohn trials,
  and Google Patents `EP1655032B1`.

Decision:

- Treat `EPHX2`, `GPR183`, and `P2RX7` as unable to support a broad novelty
  claim.
- Continue Wave74-A/B only as data-specific narrow-delta tests. If they return
  positive, the claim must be reframed as a biomarker/compartment/delivery
  delta or routed to an upstream/downstream intervention point not already
  captured by the prior art.

## 2026-05-27 17:11 CEST

Integrated Wave74-B `GPR183`/oxysterol-niche audit.

Script/output:

- `scripts/v3_wave74_gpr183_oxysterol_niche.py`
- `results_v3/wave74_gpr183_oxysterol_niche/`

Result:

- Call: `PARK_GPR183_OXYSTEROL_NICHE`.
- Gate count: 5, but the decisive gates fail.
- Coherent-program disease count: 0.
- Ligand-positive diseases: type 1 diabetes only.
- `GPR183` receptor-positive diseases: Crohn disease, Sjogren syndrome,
  ulcerative colitis.
- Best broad-context effects are response/trafficking modules, not the full
  ligand-plus-receptor program.
- `GSE111972` MS white matter:
  - `GPR183` receptor-anchor mean effect `-0.136`, p `0.664`, FDR `0.744`.
  - IFN/APC and APC/lysosome comparators are positive instead.
- `GSE282122` IBD anti-TNF:
  - Mono/macrophage ligand-production response support FDR `0.000304`.
  - DC myeloid-migration response support FDR `0.00227`.
  - Direct `GPR183` receptor response is weaker, FDR `0.196`.
- `GSE198520` RA anti-TNF:
  - lymphoid-trafficking module responder support FDR `0.0348`.
  - direct `GPR183` responder support FDR `0.180`.
- Wave66 oxysterol-like feature support:
  - 6 candidate rows, 0 supportive feature rows after tightening loose matches.
- Target-resolution:
  - `GPR183` remains `NO_GO_WAVE62_TARGET_RESOLUTION`.

Decision:

- Do not promote `GPR183`.
- The local signal is best interpreted as inflammatory/lymphoid trafficking
  context in IBD/RA/Sjogren/T1D, not as a validated pan-autoimmune oxysterol
  receptor intervention point.
- Because Wave74-C found active GPR183 autoimmune/IBD clinical and patent
  prior art, any future GPR183 work would need a narrow MS spatial-niche delta
  with direct ligand/receptor localization and CNS/tissue target engagement.

## 2026-05-27 17:12 CEST

Integrated Wave74-A `EPHX2`/oxylipin specificity audit and direct-ratio audit.

Artifacts:

- `scripts/v3_wave74_ephx2_oxylipin_specificity.py`
- `results_v3/wave74_ephx2_oxylipin_specificity/`
- `scripts/v3_wave74_ephx2_direct_ratio_audit.py`
- `results_v3/wave74_ephx2_direct_ratio_audit/`

Validation:

- Compiled Wave74-A, direct-ratio audit, and Wave74-B under
  `.venv_v3_py312`.

Results:

- Wave74-A call: `NO_GO`.
- Direct-ratio call: `NO_GO_EPHX2_DIRECT_RATIO_UNAVAILABLE`.
- Direct-ratio audit:
  - 37 EPHX2-relevant epoxide/diol/oxylipin features.
  - 0 same-study same-site direct epoxide/diol pairs.
  - 0 direct ratio tests.
  - proxy diol support in 2 diseases, T1D and UC, treated as insufficient.
- Specificity audit:
  - EPHX2-specific feature matches: 19.
  - specific supportive disease count: 1.
  - specific normalizing treatment hit count: 1.
  - ratio proxy support count: 0.
  - target-support source count: 0.
  - specificity-pass context count: 0.
  - target-level EPHX2 support: 0.

Decision:

- Do not promote `EPHX2`.
- The branch fails for both biological and novelty reasons: local data cannot
  directly estimate sEH activity, cannot separate EPHX2-specific chemistry from
  generic lipid/inflammation, and Wave74-C shows broad autoimmune prior-art
  coverage for sEH inhibition.
- The Wave72 biochemical route is now closed for promotion:
  - `NAAA`: no-go in Wave72.
  - `P2RX7`: parked/translation-blocked in Wave73/Wave74-C.
  - `GPR183`: parked/prior-art blocked in Wave74-B/C.
  - `EPHX2`: no-go/prior-art blocked in Wave74-A/C plus direct-ratio audit.

## 2026-05-27 17:15 CEST

Pivot to Wave75 `ETS2` inflammatory macrophage regulatory program.

Why this branch:

- It is a different mechanism class than lipid mediators, Fc/ROS, cathepsins,
  complement, and broad cytokine/checkpoint signaling.
- Existing local caches repeatedly mention an `ETS2` macrophage gene-desert
  mechanism in AS/IBD context.
- It has a plausible cross-autoimmune breadth story, but also obvious traps:
  transcription-factor druggability, MEK/ERK prior art/toxicity, and possible
  absence of MS support.

Dispatch:

- Wave75-C hostile prior-art/directionality scout for `ETS2` and upstream
  routes.

Local forcing test:

- Build an `ETS2` local-data audit requiring MS support, cross-disease breadth,
  treatment-response signal, target-resolution evidence, and a non-blocked
  intervention route. If it collapses into MEK/NF-kB/APC prior art or lacks
  MS/response support, close it quickly.

## 2026-05-27 17:20 CEST

Integrated Wave75 `ETS2` branch.

Artifacts:

- `scripts/v3_wave75_ets2_macrophage_program_audit.py`
- `results_v3/wave75_ets2_macrophage_program_audit/`
- `subagents_v3/wave75c_ets2_prior_art_directionality.md`

Local-data result:

- Call: `PARK_IBD_MYELOID_PROGRAM_NOT_PROMOTABLE`.
- Gate count: 2/8.
- Passed gates:
  - broad direct `ETS2` support.
  - broad ETS2-macrophage-program support.
- Failed gates:
  - specificity versus generic inflammatory/APC modules.
  - MS support.
  - IBD response support after correction.
  - RA response support.
  - target-resolved genetics.
  - foundation-model support.

Key numbers:

- Broad direct `ETS2`:
  - 2 positive diseases: Crohn disease, ulcerative colitis.
  - best context: UC myeloid effect `1.972`, p `0.0002169`, FDR `0.00079`.
- Broad ETS2 macrophage program:
  - 3 positive diseases: Crohn disease, type 1 diabetes, ulcerative colitis.
  - 1 negative disease: psoriasis.
- MS `GSE111972`:
  - direct `ETS2` mean effect `-0.0608`, p `0.8649`, FDR `0.9802`.
  - ETS2 macrophage program mean effect `-0.0145`, p `0.8943`.
- IBD `GSE282122`:
  - mono/macrophage direct `ETS2` remission delta `-0.653`, p `0.0649`,
    raw FDR `0.967`.
  - paired post/pre direct `ETS2` has no decrease.
- RA `GSE198520`:
  - AP1/ETS and ETS2-program treatment drops exist, but responder separation
    fails and generic IFN/APC or NF-kB comparators are stronger or comparable.
- Target resolution:
  - `ETS2` remains `NO_GO_WAVE62_TARGET_RESOLUTION`.
- Foundation models:
  - `ETS2` absent or below threshold in Wave57/Wave69D.

Prior-art/directionality:

- Wave75-C call: `PARK_NARROW_DELTA_ONLY`.
- Broad ETS2 macrophage inflammatory mechanism is already published for
  IBD/AS/PSC/Takayasu.
- Direct ETS2 is not conventionally druggable; upstream MEK/ERK is too broad,
  toxic, prior-arted, and already tested in RA.

Decision:

- Do not promote `ETS2`.
- The branch is a useful control: strong IBD myeloid expression and genetics
  can still fail the therapeutic-discovery bar when MS support, specificity,
  response replication, modality, and novelty are enforced.

## 2026-05-27 17:24 CEST

Integrated the response-state reopening and stricter specificity stress test
that ran during the interrupted segment.

Artifacts:

- `scripts/v3_wave75_response_state_stratification.py`
- `results_v3/wave75_response_state_stratification/`
- `scripts/v3_wave76_adjusted_response_specificity.py`
- `results_v3/wave76_adjusted_response_specificity/`
- `scripts/v3_wave77_ets2_macrophage_axis_audit.py`
- `results_v3/wave77_ets2_macrophage_axis_audit/`

Wave75 response-state stratification:

- Call: `REOPEN_RESPONSE_STRATIFICATION`.
- Best candidate: IFN/APC-lysosomal/APC response stratification.
- Best module: `lysosomal_apc`.
- Endpoint: pretreatment baseline.
- RA anti-TNF baseline responder separation:
  - effect `1.018`, p `0.00113`, FDR `0.0319`.
- IBD anti-TNF DC baseline responder separation:
  - effect `0.888`, p `0.0204`, FDR `0.0984`.
- Interpretation:
  - this reopens a response-biomarker/readout possibility, but it is not yet a
    therapeutic target because it does not specify an intervention point.

Wave76 adjusted specificity:

- Call: `PARK_RESPONSE_SIGNAL_GENERIC_LIMITED`.
- Best adjusted module: `lysosomal_apc__resid_inflammatory_nfkb`.
- Endpoint: pretreatment baseline.
- RA adjusted coefficient `0.289`, p `0.0746`,
  target/generic ratio `3.72`.
- IBD DC adjusted coefficient `0.260`, p `0.0369`,
  target/generic ratio `1.70`.
- Frozen pass gate required same sign, adjusted p <= 0.10 in RA and IBD DC,
  target/generic absolute ratio >= 2 in both datasets, and non-generic module.
- It failed because the IBD target/generic ratio was below 2.
- Interpretation:
  - the signal survives covariate adjustment but is not specific enough to
    support a V3 claim.

Wave77 local `ETS2` audit:

- Call: `NO_GO_ETS2_LOCAL_AUDIT`.
- Gate count: 1.
- Broad direct `ETS2` positive diseases: Crohn disease and ulcerative colitis.
- MS `GSE111972` direct effect `-0.0608`, p `0.8649`, FDR `0.9802`.
- GSE282122 mono/macrophage remission delta `-0.653`, p `0.0649`,
  FDR `0.967`.
- RA direct `ETS2` baseline responder effect `0.958`, p `0.00105`,
  FDR `0.00524`.
- Wave62 call remains `NO_GO_WAVE62_TARGET_RESOLUTION`.
- No direct perturbation or Geneformer support.
- Interpretation:
  - confirms the existing Wave75 ETS2 branch: useful comparator, not a
    promotable V3 target.

Decision:

- Do not write `FINDING_V3.md`.
- Park response-state stratification as a possible biomarker/readout.
- Keep `ETS2` as a negative-control comparator for generic myeloid
  inflammatory programs.
- Next forcing branch: target-level LILRB inhibitory-receptor family audit,
  because the perturbation-first scout nominated this as the only bounded
  target family worth local follow-up.

## 2026-05-27 17:37 CEST

Wave78 LILRB inhibitory-receptor family audit completed.

Artifacts:

- `scripts/v3_wave78_lilrb_family_target_audit.py`
- `results_v3/wave78_lilrb_family_target_audit/`
- `subagents_v3/wave78a_lilrb_prior_art_feasibility.md`

Validation:

- `py_compile` passed.
- Script ran under `.venv_v3_py312`.
- Added to `run_v3_analysis.sh`.

Local-data result:

- Verdict: `NO_GO_LILRB_TARGET_LEVEL_CONVERGENCE`.
- Top local rows:
  - `LILRB1`: suppression gate count 3/7, restoration 2/7.
  - `LILRB3`: suppression 3/7, restoration 2/7.
  - `LILRB2`: suppression 3/7, restoration 1/7.
  - `LILRB4`: suppression 2/7, restoration 3/7.
- Strongest IBD anti-TNF adjusted response rows:
  - `LILRB1` mono/macrophage adjusted delta `-1.035`, p `0.000937`,
    FDR `0.0120`.
  - `LILRB4` mono/macrophage adjusted delta `-1.476`, p `0.000730`,
    FDR `0.0113`.
  - `LILRB2` DC adjusted delta `-0.884`, p `0.00505`, FDR `0.0224`.
  - `LILRB3` mono/macrophage adjusted delta `-0.884`, p `0.0208`,
    FDR `0.0384`.
- Blocking local evidence:
  - no LILRB gene beats activating LILRA paralogs in same disease/compartment
    specificity (`broad_specific_positive_disease_count = 0` for all).
  - `LILRB2` is nominally lower in MS white matter: delta `-0.730`,
    p `0.00778`, wrong direction for a suppression route.
  - RA response does not replicate for `LILRB1/2/3`; `LILRB4` shows a weak
    opposite restoration-like RA delta only.
  - target-level genetic breadth is absent or weak (`LILRB3` one Crohn proxy;
    `LILRB4` one IBD proxy; `LILRB1/2` absent from Wave34/Wave55/Wave62 local
    genetic ranks).
  - Wave70-C Geneformer directionality remains no-go or ambiguous.

Prior-art/druggability sidecar:

- Wave78-A call: `PARK_DIRECTIONALITY`.
- Biologics druggability is high, but directionality is not stable:
  tolerogenic autoimmune literature points toward agonism/induction of
  ILT3/ILT4/LILRB1/2-like programs, while oncology programs use antagonist or
  depletion approaches.
- Broad autoimmune agonism is blocked/crowded by ILT3-Fc and targeted
  immunotolerance patents; antagonist/depleter routes are oncology-crowded and
  biologically risky for autoimmunity.

Decision:

- Do not promote LILRB family.
- This branch is a useful falsification of the "inhibitory checkpoint" escape
  hatch: druggability alone does not solve directionality, specificity, MS
  guardrail, or genetics.
- Next pivot should use the Wave75-C strict targetability shortlist
  (`CD58`, `SPNS1`, `P4HB`, `SEL1L3`) or another target-first list, not another
  generic myeloid marker family.

## 2026-05-27 17:33 CEST

Completed Wave78 LILRB inhibitory-receptor family audit.

Artifacts:

- `scripts/v3_wave78_lilrb_inhibitory_receptor_audit.py`
- `results_v3/wave78_lilrb_inhibitory_receptor_audit/`
- `subagents_v3/wave78_lilrb_prior_art_directionality.md`

Validation:

- `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave78_lilrb_inhibitory_receptor_audit.py`
- `.venv_v3_py312/bin/python scripts/v3_wave78_lilrb_inhibitory_receptor_audit.py`
- `bash -n run_v3_analysis.sh`

Local audit:

- No LILRB-family member passed the strict target-level gate.
- `LILRB4`:
  - call `PARK_LILRB_DIRECTIONALLY_UNRESOLVED`.
  - gate count 2.
  - pQTL colocalization in psoriasis and RA.
  - IBD response p `0.00819`, target/generic ratio `5.19`.
  - RA response p `0.859`, target/generic ratio `0.454`.
  - MS delta `-0.0567`, p `0.886`, FDR `0.984`.
  - Wave70C direction call `NO_GO_MODEL_DIRECTION_SCREEN`.
- `LILRB2`:
  - call `PARK_LILRB_DIRECTIONALLY_UNRESOLVED`.
  - positive broad diseases: Crohn disease and ulcerative colitis.
  - pQTL colocalization in Crohn and T1D.
  - IBD response p `0.00867`, target/generic ratio `43.97`.
  - RA response p `0.561`, target/generic ratio `0.711`.
  - MS nominal down delta `-0.730`, p `0.00778`, FDR `0.834`, failing the
    nonnegative MS guardrail.
  - Wave70C direction call `NO_GO_MODEL_DIRECTION_SCREEN`.
- `LILRB1` and `LILRB3`:
  - parked only because of partial IBD/broad signal.
  - no adjusted RA/IBD response-specific pass, no MS anchor, no model-direction
    support.
- Comparator `FCGR2B`:
  - passes adjusted RA/IBD response specificity but is not a LILRB target and
    remains blocked as broad Fc/inhibitory-receptor biology.

Sidecar prior-art/directionality:

- Do not promote LILRBs as therapeutic targets.
- `LILRB2` is the only member worth retaining if the local audit is positive,
  and only as a bounded biomarker/falsification lead.
- Antagonist routes are crowded oncology immune-activation programs.
- Autoimmune-resolution logic would more likely require agonism/restoration,
  but direct agonist evidence in human autoimmune myeloid cells is missing.
- `LILRB4` has direct CNS/MS patent prior art and cell-context direction
  conflict.

Decision:

- Do not promote LILRB family.
- Retain `LILRB2` as a response-state comparator only.
- Pivot to Wave79: non-LILRB targetability shortlist from Wave75-C
  (`CD58`, `SPNS1`, `P4HB`, `SEL1L3`) with the same target-level gates.

## 2026-05-27 17:42 CEST

Completed Wave79 non-LILRB targetability shortlist audit.

Artifacts:

- `scripts/v3_wave79_targetability_shortlist_audit.py`
- `results_v3/wave79_targetability_shortlist_audit/`

Validation:

- `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave79_targetability_shortlist_audit.py`
- `.venv_v3_py312/bin/python scripts/v3_wave79_targetability_shortlist_audit.py`

Key results:

- `CD58`:
  - call `PARK_TARGETABILITY_SHORTLIST_NODE`.
  - gate count 8, but failed the decisive adjusted RA/IBD response-specificity
    gate and residual-survival gate.
  - MS anchor is genetic, not expression: `ms_max_l2g_score` `0.951`.
  - QTL strong-H4 diseases: Crohn and MS.
  - Broad positive diseases: Crohn disease, T1D, UC.
  - APC/myeloid positive diseases: Crohn disease and UC.
  - RA adjusted response p `0.00298`, target/generic ratio `11.71`.
  - IBD adjusted response p `0.173`, target/generic ratio `1.62`.
  - strict residual surviving disease count `0`.
  - Decision: not promotable, but worth one CD58-specific deepening because it
    is the only shortlist node with a strong MS genetic anchor and myeloid
    recurrence.
- `P4HB`:
  - call `NO_GO_TARGETABILITY_SHORTLIST_NODE`.
  - broad recurrence is mostly epithelial/stromal, no MS anchor, no genetics,
    no response specificity, and prior local calls already demote it as broad
    ER/redox biology despite ChEMBL activity.
- `SPNS1`:
  - call `NO_GO_TARGETABILITY_SHORTLIST_NODE`.
  - lysosomal transporter biology is mechanistically interesting, but there is
    no MS anchor, no target genetics, no chemical matter, and no response
    specificity.
- `SEL1L3`:
  - call `NO_GO_TARGETABILITY_SHORTLIST_NODE`.
  - MS expression is nominally positive, but recurrence is stromal/endothelial,
    Geneformer/foundation evidence is marked do-not-promote, and no modality
    or genetics exist.
- `IFI30` benchmark:
  - not a target; confirms that MS target-resolution and APC biology alone do
    not satisfy intervention feasibility or response gates.

Decision:

- Do not write `FINDING_V3.md`.
- Close `P4HB`, `SPNS1`, and `SEL1L3`.
- Run Wave80 as a narrow `CD58`/CD2-axis deepening: mechanism direction,
  prior-art, treatment-response, and cell-compartment checks.

## 2026-05-27 17:44 CEST

Completed Wave80 `CD58`/CD2-axis deepening.

Artifacts:

- `scripts/v3_wave80_cd58_cd2_axis_deepening.py`
- `results_v3/wave80_cd58_cd2_axis_deepening/`

Validation:

- `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave80_cd58_cd2_axis_deepening.py`
- `.venv_v3_py312/bin/python scripts/v3_wave80_cd58_cd2_axis_deepening.py`
- `bash -n run_v3_analysis.sh`

New local test:

- RA bulk synovium baseline `CD58` responder association was adjusted for:
  - generic inflammatory NF-kB module;
  - T-cell module (`12/13` genes present);
  - effector-memory T-cell module (`9/9` genes present);
  - pathotype, biologic, inflammatory score, and DAS28.
- Baseline `CD58` good-responder coefficient:
  - generic-only: coefficient `0.910`, p `0.00298`.
  - generic + T-cell: coefficient `0.886`, p `0.00697`.
  - generic + T-cell + effector-memory T-cell: coefficient `0.870`,
    p `0.00871`.
- Delta/post-pre CD58 association weakened with T-cell adjustment:
  - generic-only p `0.0801`.
  - full T-cell/effector-memory adjusted p `0.262`.

Interpretation:

- The RA baseline `CD58` signal is not explained by simple T-cell or
  effector-memory T-cell abundance in this dataset.
- That strengthens `CD58` as a biomarker/context signal.
- It does not rescue the therapeutic claim because:
  - Wave79 IBD replication remains weak: p `0.173`, target/generic ratio
    `1.62`.
  - intervention direction is conflicted:
    - MS genetics/literature point toward higher CD58/restored CD2 engagement
      and Treg function.
    - alefacept/CD58-Ig blocks CD2/CD58 interaction and depletes CD2-high
      memory T cells.
  - generic CD2/CD58 autoimmune intervention is already prior art in psoriasis
    and T1D.

Decision:

- Call `PARK_CD58_CD2_AXIS_PRIOR_ART_OR_IBD_LIMITED`.
- Do not promote `CD58`.
- The remaining actionable branch should not be another expression targetability
  pass; it should pivot to a modality with direct perturbation or clinical
  response data.

## 2026-05-27 17:50 CEST

Completed Wave81 perturbation-first rescue audit.

Artifacts:

- `scripts/v3_wave81_perturbation_first_rescue.py`
- `results_v3/wave81_perturbation_first_rescue/`

Validation:

- First run failed because `wave71` had duplicate gene rows and the script tried
  to index them as unique.
- Fixed by aggregating per gene and selecting the best row by the relevant
  score.
- Re-ran py_compile and the script successfully.

Key result:

- No candidate was reopened.
- Top blocked candidates:
  - `GALC`: direct/model/MS/genetics/modality signal, but blocked by prior
    sphingolipid-enzyme route closure and lack of translational specificity.
  - `IL7R`: strong genetics/model/response context, but blocked by prior
    audited broad T-cell biology and host-defense/prior-art concerns.
  - `NCF2`/`NCF1`/`CYBB`: NOX2 axis blocked by host-defense/CGD direction risk.
  - `TNFRSF1A`: MS genetics and perturbation, but TNF-axis direction is
    hazardous in MS.
  - `JAK1`/`JAK2`/`TYK2`/`STAT1`: broad JAK/IFN prior art.
  - `CD40`/`CD80`: checkpoint/costimulation prior art and broad immune
    activation; abatacept MS trial is a negative comparator for costimulation
    blockade.
- Least-bad unblocked parked candidates:
  - `DAP`: score `12`, direct/model signal, MS nominal expression, broad
    recurrence, IBD nominal response; no modality/genetics.
  - `PARK7`: score `11`, model/evidence/modality channel, but no MS anchor and
    insufficient convergence.
  - `FMNL2`: score `10`, perturbation plus MS expression and broad recurrence,
    but no modality/genetics.
  - `PSAP`: score `10`, model plus MS expression; no modality/genetics and weak
    cross-autoimmune recurrence.
  - `DAB2`: score `9`, efferocytosis perturbation plus MS expression and IBD
    nominal response; no modality/genetics.

Decision:

- Do not promote any Wave81 candidate.
- Run Wave82 on the unblocked parked set (`DAP`, `PARK7`, `FMNL2`, `PSAP`,
  `DAB2`) to test whether any has a credible intervention route rather than
  only perturbation/model signal.

## 2026-05-27 17:40 CEST

Integrated Wave79 hostile prior-art/directionality sidecar.

Artifact:

- `subagents_v3/wave79_targetability_prior_art_directionality.md`

What changed:

- The local Wave79 audit left `CD58` as the only partial survivor, but the
  sidecar makes it unsuitable for target promotion:
  - alefacept is a direct CD58/LFA-3-Fc CD2-interaction precedent in psoriasis
    and T1D;
  - CD2-CD58 inhibition for autoimmune/inflammatory disease has direct patent
    prior art;
  - MS genetics suggests higher/restored CD58 can be protective, conflicting
    with a simple blockade claim.
- `SPNS1` remains the cleanest novelty biology, but only as a lysosomal
  lipid-flux preclinical lead; no MS anchor, chemical matter, or perturbation
  direction exists.
- `P4HB` and `SEL1L3` are not worth additional V3 target effort.

Decision:

- Do not promote any Wave79 shortlist gene.
- Treat `CD58` as a possible comparator or stratification/falsification axis,
  not as a novel intervention point.
- Continue by pivoting away from expression-derived targetability toward
  perturbation-first or treatment-response-first evidence.

## 2026-05-27 18:02 CEST

Re-audited Wave81 after continuation and corrected a proxy-satisficing bug.

Artifacts changed:

- `scripts/v3_wave81_perturbation_first_rescue.py`
- `results_v3/wave81_perturbation_first_rescue/`
- `run_v3_analysis.sh`

What happened:

- The interrupted Wave81 note said no candidate reopened, but the script's
  implementation needed two corrections:
  - report ordering was alphabetical by call and could hide reopened rows;
  - support flags were based on table presence, not positive support metrics.
- After fixing ordering alone, `SP140`, `RGS14`, and `STAT4` appeared as
  `REOPEN_PERTURBATION_FIRST_TARGET`.
- I inspected source rows and rejected that as a weak operationalization:
  - `SP140`: Wave57 and Wave69D Geneformer rows had `support_contexts=0`;
    Wave37 efferocytosis screen call was `UNRESOLVED`, contrast FDR `0.920`.
  - `RGS14`: Wave69D Geneformer row had `support_contexts=0`; no direct
    perturbation support.
  - `STAT4`: Wave15 direct perturbation call was `null_or_wrong_direction`;
    Geneformer support was not positive.
- I then changed Wave81 so:
  - foundation-model support requires at least one positive support context
    with token coverage;
  - direct perturbation requires a non-unresolved efferocytosis CRISPR call or
    a non-not-nominated selective transcript perturbation call.

Corrected result:

- `REOPEN_PERTURBATION_FIRST_TARGET`: `0` candidates.
- `PARK_PERTURBATION_FIRST_CANDIDATE`: `89` candidates.
- `NO_GO_PERTURBATION_FIRST_BLOCKED`: `42` candidates.
- `NO_GO_NO_PERTURBATION_SUPPORT`: `150` candidates.
- Top parked rows:
  - `DAB2`: direct efferocytosis call, MS expression p `0.0111`, IBD nominal
    response, but no genetics/modality/foundation support.
  - `CD9`: direct efferocytosis call and MS expression p `0.00197`, but no
    genetics, breadth, modality, or model support.
  - `PARK7`: positive Geneformer support (`wave57:support=2`) plus modality
    channel and IBD nominal response, but no MS anchor.
  - `PSAP`: positive Geneformer support (`wave57:support=1`) and MS expression
    p `0.0223`, but no modality/genetics/breadth.

Decision:

- Wave81 remains non-promotable after stricter gates.
- Run Wave82 as an intervention-route stress test on the top parked candidates
  and on the false-positive controls (`SP140`, `RGS14`, `STAT4`) to prevent
  recurrence of table-presence proxy errors.

## 2026-05-27 18:13 CEST

Completed Wave82 parked perturbation intervention audit.

Artifacts:

- `scripts/v3_wave82_parked_perturbation_intervention_audit.py`
- `results_v3/wave82_parked_perturbation_intervention_audit/`
- `subagents_v3/wave82a_parked_perturbation_feasibility.md`
- `subagents_v3/wave82b_cross_disease_evidence_stress_test.md`

Validation:

- `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave82_parked_perturbation_intervention_audit.py`
- `.venv_v3_py312/bin/python scripts/v3_wave82_parked_perturbation_intervention_audit.py`
- `bash -n run_v3_analysis.sh`

Important correction:

- The first API table resolved `PSAP` through an ambiguous UniProt search. I
  pinned known human UniProt accessions and ChEMBL target IDs for all audited
  genes, then re-ran:
  - `PSAP`: UniProt `P07602`, ChEMBL `CHEMBL3580523`, 12 ChEMBL activity rows.
  - `PARK7`: UniProt `Q99497`, ChEMBL `CHEMBL5169188;CHEMBL6066048`, 142 rows.
  - `LYN`: UniProt `P07948`, ChEMBL `CHEMBL3905;CHEMBL6066565`, 6411 rows.
  - `SP140`: UniProt `Q13342`, ChEMBL `CHEMBL3108643;CHEMBL4105997`, 80 rows.
  - `STAT4`: UniProt `Q14765`, ChEMBL `CHEMBL4523296;CHEMBL4523706`, 27 rows.

Result:

- Verdict: `NO_PROMOTABLE_INTERVENTION_ROUTE`.
- Local code call counts:
  - `PARK_READOUT_OR_PRECLINICAL_PROBE`: `7`.
  - `NO_GO_WAVE82_BLOCKED`: `3`.
- Sidecar agreement:
  - Wave82-A: no candidate ranked because none has a defensible translational
    route.
  - Wave82-B: `STAT4` and `SP140` have real cross-autoimmune breadth but are
    blocked; `RGS14` has genetics without cross-disease state breadth; `LYN`
    has state/model signal without genetics; remaining candidates lack breadth.

Candidate disposition:

- `CD9`: MS expression and surface accessibility, but no cross-disease state
  breadth/genetics and CD9 biology is broad/conflicted.
- `PSAP`: MS expression/model support and a secreted/lysosomal route, but no
  cross-disease breadth or target-resolved genetics.
- `DAB2`: perturbation plus MS expression, but no druggability or breadth.
- `RGS14`: MS/Crohn/psoriasis genetic target resolution, but no positive
  perturbation/model support and only Crohn disease-state recurrence.
- `PARK7`, `HEXA`, `HEXB`: biology probes with insufficient MS/cross-disease
  and autoimmune-specific direction.
- `SP140`, `STAT4`, `LYN`: blocked controls by prior branch, directionality,
  or broad kinase/TF biology.

Decision:

- Close the parked perturbation rescue branch.
- Pivot to a genetics-first/druggable-survivor sweep over all target-resolved
  rows, not just Wave81 parked perturbation candidates.

## 2026-05-27 18:09 CEST

Completed corrected Wave82 parked intervention-route audit.

Artifacts:

- `scripts/v3_wave82_parked_intervention_route_audit.py`
- `results_v3/wave82_parked_intervention_route_audit/`

Validation:

- `py_compile` passed for Wave81 and Wave82 scripts.
- `bash -n run_v3_analysis.sh` passed.
- Re-ran Wave81 after fixing missing blocker parsing; missing values no longer
  create literal `nan; nan` blockers.
- Re-ran Wave82 against the corrected Wave81 table.

Important correction:

- The interrupted Wave82 draft used a stale candidate set and let `RGS14` rise
  on a modality/channel artifact. I replaced this with:
  - residual candidates: `DAB2`, `CD9`, `PSAP`, `PARK7`, `LYN`, `FAM49B`,
    `LRRC61`, `HEXA`, `HEXB`, `DAP`, `FMNL2`;
  - false-positive controls: `SP140`, `RGS14`, `STAT4`.

Result:

- `REOPEN_INTERVENTION_ROUTE`: `0`.
- `PARK_ROUTE_POSSIBLE_BUT_EVIDENCE_INCOMPLETE`: `1` (`PARK7`).
- `NO_GO_NO_CREDIBLE_INTERVENTION_ROUTE`: `10`.
- `NO_GO_FALSE_POSITIVE_CONTROL`: `3`.

Interpretation:

- `PARK7` has Geneformer support plus a modality channel, but fails MS anchor,
  cross-disease breadth, and response-FDR gates.
- `DAB2`, `CD9`, and `PSAP` remain mechanistically interesting readouts, not
  intervention-grade targets:
  - `DAB2`: efferocytosis signal plus MS expression, but no genetics,
    modality, broad recurrence, or response-FDR support.
  - `CD9`: efferocytosis plus MS expression, but no genetics/breadth and
    unclear tetraspanin direction.
  - `PSAP`: model plus MS expression, but weak cross-autoimmune recurrence and
    no route.
- `LYN`, `FAM49B`, `LRRC61`, `HEXA`, `HEXB`, `DAP`, and `FMNL2` fail at
  reachability, causal anchoring, or safe direction.
- False-positive controls (`SP140`, `RGS14`, `STAT4`) are explicitly closed for
  Wave82 promotion.

Decision:

- Do not promote any Wave82 residual candidate.
- Pivot away from residual perturbation candidates toward a broader
  intervention-class scan that starts from reachable modulators and only then
  asks whether they control the lipid-lysosomal/myeloid state.

## 2026-05-27 18:18 CEST

Completed the Wave82 cross-disease residual stress-test sidecar artifact after
continuation.

Artifact:

- `subagents_v3/wave82_cross_disease_residuals.md`

Method:

- Re-read the corrected Wave81 rank and local cross-disease inputs for
  `DAB2`, `CD9`, `PSAP`, `LYN`, `FAM49B`, `LRRC61`, `HEXA`, `HEXB`, `DAP`,
  `PARK7`, and `FMNL2`.
- Required per-candidate enumeration of supporting and contradictory diseases
  and modalities.
- Treated nominal p-values as weak unless supported by FDR, independent
  modality, and correct tissue-cell context.

Result:

- Promotion count: `0`.
- `LYN`, `PSAP`, `PARK7`, `DAB2`, and `FAM49B` are at most parked.
- `LRRC61`, `CD9`, `FMNL2`, `DAP`, `HEXA`, and `HEXB` are no-go for the
  pan-autoimmune lipid-lysosomal/myeloid target claim.

Key self-critique:

- The strongest residual cross-disease signals are mostly nominal and often in
  epithelial, stromal, endothelial, keratinocyte, or pancreatic stellate
  compartments rather than myeloid/APC.
- `DAB2` and `CD9` are tempting because they have efferocytosis perturbation
  plus nominal MS white-matter expression, but broad IBD myeloid expression is
  negative, which directly contradicts a simple pan-myeloid activation target
  interpretation.
- The residual gene branch risks chasing markers because no candidate has
  target-resolution genetics plus reachable modality plus cross-disease
  cell-state support.

Decision:

- Close Wave82 residual-gene target promotion.
- Open Wave83 as intervention-class-first: begin with reachable targets or
  modalities and only then ask whether they control the shared module.

## 2026-05-27 18:29 CEST

Implemented and ran Wave83 intervention-class-first scan.

Artifacts:

- `scripts/v3_wave83_intervention_class_first_scan.py`
- `results_v3/wave83_intervention_class_first_scan/`
- `run_v3_analysis.sh`

Validation:

- `py_compile` passed for Wave83.
- `bash -n run_v3_analysis.sh` passed.

Method:

- Inverted the prior search order.
- Candidate universe started from local reachability signals:
  - UniProt-accessible or ChEMBL-supported Wave39 targets;
  - Wave62 target-resolution rows with local ChEMBL/druggability;
  - Wave68 rows with any druggability flag;
  - L1000 mechanism targets;
  - Wave61 intervention rows with target/chemistry fields.
- Only after reachability did the script overlay cross-autoimmune recurrence,
  target-resolution genetics/QTL, MS white-matter signal, Geneformer support,
  direct perturbation, IBD response, and manual/prior blockers.
- Corrected report ordering after first run so parked/reopened rows appear
  before no-go rows rather than alphabetic calls.

Result:

- `REOPEN_REACHABLE_INTERVENTION_CANDIDATE`: `0`.
- `PARK_REACHABLE_BUT_EVIDENCE_INCOMPLETE`: `10`.
- `NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED`: `39`.
- `NO_GO_NOT_REACHABLE_FIRST_CLASS`: `152`.

Top parked reachable-first candidates:

- `MMP7`: reachability `5`, cross-autoimmune `7`, perturbation/response `2`,
  but no strong MS anchor and prior-art/trial saturation blocker.
- `CD274`: reachability `5`, cross-autoimmune `7.2`, response `2`, but no MS
  anchor and checkpoint prior-art/safety blocker.
- `IL15`, `CD74`, `HLA-DRB1`, `IL23A`: reachable and disease-recurrent, but
  prior-art/core immune axis blockers dominate.
- `CASP4`, `KCNJ2`, `APOL1`, `TIMP1`: reachable-state candidates without
  MS/genetic anchoring or a clean intervention direction.

Interpretation:

- Route-first scanning does not rescue a target from the current local
  evidence base.
- The parked candidates are useful as boundary cases: they are druggable enough
  to discuss, but the evidence points to broad inflammatory/cell-state markers
  rather than a novel MS-relevant module controller.

Decision:

- Do not promote a Wave83 candidate.
- Next branch should ask whether a stratification claim is more realistic than
  a direct target claim: reachable broad inflammatory axes may identify a
  patient/tissue state even when they are not novel targets.

## 2026-05-27 18:21 CEST

Continued after another external interruption. The interruption/waiting gap is
not counted as active work per user instruction.

Implemented and ran Wave83 intervention-class-first meta-rank.

Artifacts:

- `scripts/v3_wave83_intervention_class_meta_rank.py`
- `results_v3/wave83_intervention_class_meta_rank/`
- `run_v3_analysis.sh`

Validation:

- `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave83_intervention_class_meta_rank.py`
- `.venv_v3_py312/bin/python scripts/v3_wave83_intervention_class_meta_rank.py`
- `bash -n run_v3_analysis.sh`

Important failed intermediate:

- First meta-rank run reported `CD58_TARGETABILITY` as
  `REOPEN_INTERVENTION_CLASS`.
- I rejected this as a scoring bug because the same row carried
  `source_call=PARK_TARGETABILITY_SHORTLIST_NODE`, only one support channel,
  and Wave80 already documented CD58/CD2 prior-art and direction blockers.
- Patch: explicit parsing of boolean TSV fields for LILRB rows; reopen now
  requires at least two support channels and no source audit call starting with
  `PARK` or `NO_GO`.

Corrected result:

- `REOPEN_INTERVENTION_CLASS`: `0`.
- `PARK_INTERVENTION_CLASS_NEEDS_FORCING_TEST`: `1`
  (`GPR183_EBI2_OXYSTEROL_NICHE`).
- `NO_GO_INTERVENTION_CLASS_META_RANK`: `58`.

Interpretation:

- The target/intervention nomination branch remains unpromotable.
- The least-bad forcing route is `GPR183`, but it still lacks MS anchoring,
  target-resolution genetics, and a promotional source audit.
- `CD58` is useful as a response-stratification comparator, not a therapeutic
  intervention claim.

Decision:

- Do not promote any Wave83 intervention class.
- Open Wave84 as stratification-first: test whether the shared
  lipid-lysosomal/myeloid state predicts therapeutic response across independent
  autoimmune treatment datasets, adjusted for generic inflammation and cell
  composition.
## 2026-05-27 18:17 CEST

Continuation after usage-limit interruption. The user explicitly clarified that
the waiting gap does not count as working time; V3 remains active and the
twelve-hour floor has not been reached.

Wave83 local hardening:

- File edited: `scripts/v3_wave83_intervention_class_first_scan.py`.
- Added genetics-first survivor sources:
  - `results_v3/wave34a_genetics_first_target_rescue/genetics_first_candidate_rank.tsv`
  - `results_v3/wave71_global_survivor_meta_rank/global_survivor_meta_rank.tsv`
- Added explicit branch-closure dictionary for repeatedly rediscovered axes
  (`PTPN2`, `STAT4`, `PTGER4`, `TYK2`, `PTPN22`, `IL2RA`, `GPR65`, `CXCR2`,
  `CD40`, `CTLA4`, etc.).
- Replaced permissive live parking with a stronger rule: a reachable target
  cannot remain a live candidate if it lacks a strong MS anchor or is
  prior-blocked.

Verification:

- `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave83_intervention_class_first_scan.py`
- `.venv_v3_py312/bin/python scripts/v3_wave83_intervention_class_first_scan.py`
- `bash -n run_v3_analysis.sh`

Wave83 result:

- Candidate universe: `735`.
- `REOPEN_REACHABLE_INTERVENTION_CANDIDATE`: `0`.
- `PARK_TARGET_RESOLVED_BUT_PRIOR_CLOSED`: `10`.
- `NO_GO_REACHABLE_BUT_BIOLOGY_INCOMPLETE_OR_BLOCKED`: `63`.
- `NO_GO_NOT_REACHABLE_FIRST_CLASS`: `662`.

Top prior-closed comparators:

- `PTPN2`: broad cross-autoimmune signal and chemical matter, but the required
  direction is restoration/activation; inhibitor chemistry points the wrong way
  and MS anchor is absent in the local evidence used here.
- `STAT4`: strong cross-autoimmune genetics, but the therapeutic route collapses
  into broad JAK/STAT or transcription-factor intervention.
- `PTGER4`: tractable GPCR and MS/Crohn/psoriasis/T1D/UC genetic breadth, but
  EP4 directionality and prior art remain unresolved/blocked.
- `IL2RA`, `GPR65`, `CD40`, `CTLA4`, `TYK2`, `PTPN22`, and `CXCR2` recur but
  remain closed by prior V3 branch decisions.

Decision:

- Do not promote any reachable genetics-first target.
- Close the target-first survivor sweep unless a sidecar identifies a concrete
  new evidence route.
- Pivot next to mechanism-class search: instead of asking "which gene is already
  druggable?", ask whether an upstream physiological controller of the
  lipid-lysosomal/efferocytosis state has disease breadth, perturbation
  direction, and translational feasibility.

## 2026-05-27 18:36 CEST

Wave85 external anti-TNF validation completed.

Reason for branch:

- Wave84 parked a tissue-response stratification signal for
  `lysosomal_apc__resid_inflammatory_nfkb`, but the evidence was only two
  treatment datasets and no external GEO mucosal replication.
- The reviewer warning against proxy-satisficing applies here: a residual
  module score must be tested in real treatment-response cohorts before it can
  guide any therapeutic or biomarker claim.

Data downloaded and used:

- `data/raw_v3/wave84_external_geo/GSE12251_series_matrix.txt.gz`
- `data/raw_v3/wave84_external_geo/GSE14580_series_matrix.txt.gz`
- `data/raw_v3/wave84_external_geo/GSE16879_series_matrix.txt.gz`
- `data/raw_v3/wave84_external_geo/GPL570.annot.gz`

Code:

- Added `scripts/v3_wave85_external_geo_antitnf_validation.py`.
- Added the script to `run_v3_analysis.sh`.

Verification:

- `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave85_external_geo_antitnf_validation.py`
- `bash -n run_v3_analysis.sh`
- `.venv_v3_py312/bin/python scripts/v3_wave85_external_geo_antitnf_validation.py`

Failed/irrelevant command:

- I accidentally used system `python3` for a pandas inspection one-liner. It
  failed because pandas is not installed in that interpreter. Re-ran the same
  inspection with `.venv_v3_py312/bin/python`.

Primary result:

- Output directory:
  `results_v3/wave85_external_geo_antitnf_validation/`
- `summary.json` call:
  `WEAK_EXTERNAL_DIRECTIONAL_SUPPORT_NOT_STRATIFICATION_GRADE`.
- Primary module:
  `lysosomal_apc__resid_inflammatory_nfkb`.
- Independent overlap groups tested: `6`.
- Independent supportive nominal groups: `0`.
- Independent positive-direction groups: `2`.
- Independent-overlap weighted mean Hedges g: `-0.1285`.
- Median AUC across independent overlap groups: `0.4993`.

Interpretation:

- The Wave84 residual lysosomal/APC stratification endpoint does not externally
  replicate.
- The external IBD cohorts instead show a strong generic inflammatory/IFN-high
  nonresponse state:
  - `inflammatory_nfkb` is higher in nonresponders in ACT1 UC, Leuven UC,
    Crohn colitis, Crohn-all, and all-IBD tests.
  - `ifn_lysosomal_apc_composite` is also consistently higher in
    nonresponders.

Decision:

- Demote the residual lysosomal/APC endpoint as a V3-grade stratification
  candidate.
- Open Wave86 to decompose the external anti-TNF nonresponse state at gene
  level and ask whether a specific intervention/stratification node survives
  cross-cohort consistency and prior-art pressure.

## 2026-05-27 18:49 CEST

Wave86 and Wave87 completed.

Wave86:

- Added `scripts/v3_wave86_external_geo_antitnf_gene_driver.py`.
- Added the script to `run_v3_analysis.sh`.
- Verification:
  - `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave86_external_geo_antitnf_gene_driver.py`
  - `bash -n run_v3_analysis.sh`
  - `.venv_v3_py312/bin/python scripts/v3_wave86_external_geo_antitnf_gene_driver.py`
- Output directory:
  `results_v3/wave86_external_geo_antitnf_gene_driver/`
- Result:
  - `45` module genes tested.
  - `16` genes called `GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR`.
  - Top anchors: `IL1B`, `CXCL8`, `TREM1`, `CCL4`, `CCL3`, `CD44`,
    `CCL2`, `ACSL1`, `IFI30`, `OSM`.
  - `IL1B`: nonresponse-high in `4/4` primary external IBD contexts,
    `3/4` nominal p<0.05, `3/4` FDR<0.10, weighted mean Hedges g `-1.695`,
    median nonresponse AUC `0.897`.

Wave87:

- Added `scripts/v3_wave87_cross_system_antitnf_resistance_gene_check.py`.
- Added the script to `run_v3_analysis.sh`.
- Verification:
  - `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave87_cross_system_antitnf_resistance_gene_check.py`
  - `.venv_v3_py312/bin/python scripts/v3_wave87_cross_system_antitnf_resistance_gene_check.py`
- Hygiene correction:
  - initial Wave87 run retained zero-variance/missing RA genes as empty rows;
    patched `test_ra_baseline_gene()` to drop non-finite expression values and
    reran cleanly.
- Output directory:
  `results_v3/wave87_cross_system_antitnf_resistance_gene_check/`
- Result:
  - `25` Wave86 anchor/park genes considered.
  - `22` genes had usable RA synovium expression.
  - `2` cross-system parked genes:
    - `LAMP3`: RA Hedges g `-0.927`, p `0.00238`, FDR `0.0261`, nonresponse
      AUC `0.786`.
    - `IL1B`: RA Hedges g `-0.588`, p `0.0407`, FDR `0.0995`, nonresponse
      AUC `0.701`.
  - Several strong IBD genes reverse direction in RA (`TREM1`, `CCL2`,
    `STAT1`, `CD44`, `NFKBIA`), blocking a broad pan-autoimmune anti-TNF
    resistance claim.

Decision:

- Do not promote the full inflammatory/IFN anti-TNF resistance module as a
  cross-autoimmune mechanism.
- Carry only `IL1B` and `LAMP3` forward into prior-art and intervention
  feasibility pressure.
- Treat `LAMP3` as likely marker/state, not target, unless an intervention
  handle emerges.

## 2026-05-27 19:10 CEST

Wave89 completed.

- Added `scripts/v3_wave89_psoriasis_gse85034_response_validation.py`.
- Added the script to `run_v3_analysis.sh`.
- Downloaded and used:
  - `data/raw_v3/wave89_psoriasis_response/GSE85034_series_matrix.txt.gz`
  - `data/raw_v3/wave89_psoriasis_response/GPL10558.annot.gz`
- Verification:
  - `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave89_psoriasis_gse85034_response_validation.py`
  - `bash -n run_v3_analysis.sh`
  - `.venv_v3_py312/bin/python scripts/v3_wave89_psoriasis_gse85034_response_validation.py`
- Output directory:
  `results_v3/wave89_psoriasis_gse85034_response/`
- Design:
  - Reconstructed PASI75 at week 16 from GEO PASI fields.
  - Used baseline lesional skin only (`timepoint: LS`).
  - Treated adalimumab as the primary anti-TNF test and methotrexate as a
    therapy-specificity control.
  - Excluded Subject 28 from baseline-lesional response tests because GEO has
    `WK1_NL`/`WK1_LS`, not baseline `NL`/`LS`.
- Result:
  - Treatment counts: adalimumab `14` evaluable subjects (`9` PASI75
    responders, `5` nonresponders); methotrexate `13` evaluable subjects
    (`3` responders, `10` nonresponders).
  - Analysis call:
    `WEAK_DIRECTIONAL_THIRD_DISEASE_SUPPORT_ONLY`.
  - `IL1B` in adalimumab psoriasis is same-direction but weak:
    Hedges g responder-minus-nonresponder `-0.6325`, AUC for high-expression
    nonresponse `0.5556`, p `0.3940`.
  - `LAMP3` reverses in adalimumab psoriasis:
    Hedges g `0.4960`, AUC high-expression nonresponse `0.3556`,
    p `0.2968`.
  - Strongest adalimumab gene-level signal among tested module genes is `LPL`:
    Hedges g `-2.2089`, AUC high-expression nonresponse `0.9556`,
    p `0.0111`, FDR across tested genes `0.4998`.
  - The `lysosomal_apc` module is also nonresponse-high in adalimumab
    psoriasis with Hedges g `-1.017`, AUC `0.7778`, p `0.1237`.

Decision:

- Do not rescue the IL1B/LAMP3 branch as a three-disease anti-TNF
  stratification mechanism.
- Reformulate the next branch around the lipid/lysosomal myeloid state in
  adalimumab psoriasis, especially whether `LPL` is a reproducible lipid-load
  marker or an intervention-relevant node across MS/IBD/RA/psoriasis.
- Guardrail: the psoriasis arm is small, so `LPL` is a lead for falsification,
  not a finding.

## 2026-05-27 19:19 CEST

Wave90 completed.

- Added `scripts/v3_wave90_lpl_cross_disease_audit.py`.
- Added the script to `run_v3_analysis.sh`.
- Verification:
  - `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave90_lpl_cross_disease_audit.py`
  - `bash -n run_v3_analysis.sh`
  - `.venv_v3_py312/bin/python scripts/v3_wave90_lpl_cross_disease_audit.py`
- Output directory:
  `results_v3/wave90_lpl_cross_disease_audit/`
- Integrated evidence:
  - MS bulk white matter: `GSE111972` full MS white-matter signature.
  - direct donor-level h5ad case-control contrasts.
  - Wave86 external IBD anti-TNF response meta.
  - GSE198520 RA synovium anti-TNF baseline response, freshly computed for
    `LPL`.
  - Wave89 psoriasis GSE85034 baseline response.
- Result:
  - Analysis call:
    `PARK_LPL_RESPONSE_MARKER_WITH_CASE_CONTROL_CONFLICT`.
  - MS white matter: `LPL` is up in MS white matter, delta `1.7596`,
    Hedges g `1.8731`, p `0.000622`, FDR `0.7144`; the lipid-loader module
    is also up in MS white matter, delta `0.4784`, Hedges g `1.3791`,
    p `0.00528`, FDR `0.01916`.
  - Anti-TNF response directions:
    - IBD external meta: weighted Hedges g responder-minus-nonresponder
      `-0.2045`, median nonresponse AUC `0.5470`, min p `0.2508`.
    - RA synovium GSE198520: Hedges g `-0.3946`, AUC high-expression
      nonresponse `0.6362`, p `0.1578`.
    - Psoriasis GSE85034 adalimumab: Hedges g `-2.2089`, AUC `0.9556`,
      p `0.0111`.
  - Direct h5ad case-control conflict:
    - Crohn colon epithelial LPL is case-high, Hedges g `1.7189`,
      p `0.0231`.
    - Psoriasis skin APC LPL is control-high, Hedges g `-3.7045`,
      p `0.0158`.
- Decision:
  - Do not promote direct `LPL` modulation as a target.
  - Preserve `LPL` as a marker of lipid handling/uptake state and a clue
    toward upstream/downstream intervention handles.
  - Next branch should search the lipid-loader neighborhood for a tractable
    controller with better cross-disease stability and druggability.

## 2026-05-27 19:41 CEST

Wave91 completed.

- Added `scripts/v3_wave91_lipid_lysosomal_module_intervention_rank.py`.
- Added the script to `run_v3_analysis.sh`.
- Verification:
  - `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave91_lipid_lysosomal_module_intervention_rank.py`
  - `bash -n run_v3_analysis.sh`
  - `.venv_v3_py312/bin/python scripts/v3_wave91_lipid_lysosomal_module_intervention_rank.py`
- Output directory:
  `results_v3/wave91_lipid_lysosomal_module_intervention_rank/`
- Inputs:
  - Wave86 external IBD anti-TNF gene meta-rank.
  - Fresh all-candidate RA synovium baseline response tests from GSE198520.
  - Wave89 psoriasis adalimumab baseline response tests from GSE85034.
  - GSE111972 MS white-matter gene signature.
  - Direct donor-level h5ad case-control contrasts.
  - Wave55/Wave62 genetics and target-resolution outputs.
  - Wave81 perturbation-first rescue outputs.
- Result:
  - Analysis call:
    `NO_REOPEN_MODULE_WIDE_LIPID_LYSOSOMAL_INTERVENTION_NODE`.
  - Candidate genes tested: `45`.
  - Reopened genes: `0`.
  - Parked genes: `10`.
  - Top score: `CD44`, but it remains `NO_GO_ROUTE_BLOCKED` because the
    signal is not an unblocked therapeutic route despite MS white-matter
    expression and some cross-disease support.
  - `LPL` retained the three-disease anti-TNF nonresponse direction and MS
    white-matter-up signal, but failed on direct atlas contradiction and
    systemic lipolysis targetability.
  - Many inflammation/lysosome genes (`IL1B`, `TREM1`, `CTSB`, `CTSS`,
    `LAMP3`) fail because they lack a nominal MS white-matter single-gene
    anchor, reverse in RA, are route-blocked, or are only weak markers.
- Decision:
  - Stop trying to nominate a directly measured module gene as the target.
  - Reformulate toward regulators or transition controllers upstream/downstream
    of the lipid-loader myeloid state.
  - The next branch should ask which druggable regulatory systems control
    `LPL`/lipid-loader-high myeloid states without directly targeting systemic
    lipid metabolism or broad antigen presentation.

## 2026-05-27 19:38 CEST

Wave91 and Wave92 completed.

Wave91:

- Added `scripts/v3_wave91_lipid_neighborhood_controller_scan.py`.
- Added the script to `run_v3_analysis.sh`.
- Verification:
  - `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave91_lipid_neighborhood_controller_scan.py`
  - `bash -n run_v3_analysis.sh`
  - `.venv_v3_py312/bin/python scripts/v3_wave91_lipid_neighborhood_controller_scan.py`
- Output directory:
  `results_v3/wave91_lipid_neighborhood_controller_scan/`
- Initial run produced NaN scores for candidates with missing direct-context
  rows. Patched the scorer so missing evidence is zero evidence rather than
  undefined score, and added explicit call-order sorting.
- Final result:
  - `17` lipid-neighborhood candidates scanned.
  - Call counts:
    - `1` `PARK_CONTROLLER_FOR_DEEP_VALIDATION`
    - `3` `PARK_MARKER_OR_WEAK_CONTROLLER`
    - `13` `NO_GO_LIPID_NEIGHBORHOOD_NODE`
  - Top parked controller: `FABP5`, score `7.05`.
  - `FABP5` support:
    - MS white matter: delta `1.2651`, Hedges g `1.3549`, p `0.00414`.
    - Direct h5ad: positive nominal/trend contexts in psoriasis and UC, but
      also a negative UC epithelial context.
    - Response direction: RA and psoriasis are weakly nonresponse-high; IBD
      Wave86 is not convergent.
    - Geneformer pivot-panel deletion has `5` usable rows, including IBD
      contexts with deletion shifting embeddings toward control centroid.
  - `FABP5` failures:
    `case_control_negative_context_present;weak_or_inconsistent_response_direction`.

Wave92:

- Added `scripts/v3_wave92_fabp5_prior_art_audit.py`.
- Added the script to `run_v3_analysis.sh`.
- Verification:
  - `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave92_fabp5_prior_art_audit.py`
  - `.venv_v3_py312/bin/python scripts/v3_wave92_fabp5_prior_art_audit.py`
- Output directory:
  `results_v3/wave92_fabp5_prior_art_audit/`
- Result:
  - Analysis call:
    `FABP5_PRIOR_ART_BLOCKED_FOR_MS_THERAPEUTIC_NOVELTY`.
  - PubMed blocker PMIDs found:
    - `34624687`: "A novel fatty acid-binding protein 5 and 7 inhibitor
      ameliorates oligodendrocyte injury in multiple sclerosis mouse models."
      EBioMedicine 2021, DOI `10.1016/j.ebiom.2021.103582`.
    - `33124722`: "The Fabp5/calnexin complex is a prerequisite for
      sensitization of mice to experimental autoimmune encephalomyelitis."
      FASEB Journal 2020, DOI `10.1096/fj.202001539RR`.
  - ClinicalTrials API did not identify a clear FABP5 autoimmune interventional
    clinical trial, but PubMed prior art is already directly blocking for MS
    target novelty.

Decision:

- Do not promote `FABP5` as the V3 target.
- Keep `FABP5` as mechanistic support that the lipid-handling axis is real.
- Pivot again: the eventual target must avoid the already-occupied
  FABP5/FABP7-inhibition MS route while preserving the lipid-state biology.

## 2026-05-27 19:42 CEST

Continuation after external usage-limit interruption. Idle waiting time is not
counted as active work per user instruction.

Decision:

- Pivot from module-internal lipid genes to a druggable upstream
  state-transition controller.
- Selected first forcing test: `GPR183`/EBI2 oxysterol-guided immune niche,
  because Wave83 marked it as the least-bad intervention-class route and it
  has GPCR chemical tractability.
- Risk acknowledged before coding: Wave74 already failed ligand/receptor/MS
  coherence, so this branch can only reopen if target-level response,
  genetics/druggability, or prior-art data materially change the gate picture.

Subagents were dispatched for prior-art, druggability, and hostile-review
sidecar checks. Local orchestrator proceeded with Wave93.

## 2026-05-27 19:48 CEST

Wave93 implemented and completed.

Script:

- `scripts/v3_wave93_gpr183_oxysterol_forcing_test.py`

Runner:

- Added to `run_v3_analysis.sh`.

Verification:

- `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave93_gpr183_oxysterol_forcing_test.py`
- `bash -n run_v3_analysis.sh`
- `.venv_v3_py312/bin/python scripts/v3_wave93_gpr183_oxysterol_forcing_test.py`

Failed attempt:

- First run failed with `KeyError: 'sample'` in the IBD external anti-TNF
  patient aggregation path. Cause: the transposed gene-expression score matrix
  had no index name, so `patient_level_scores()` did not create a `sample`
  column after `reset_index()`.
- Patch: set `score_df.index.name = "sample"` before aggregation.

Output directory:

- `results_v3/wave93_gpr183_oxysterol_forcing_test/`

Result:

- Analysis call:
  `NO_GO_GPR183_NO_MS_RECEPTOR_OR_LIGAND_ANCHOR`.
- Gate count: `1/7`.
- Only passing gate: ChEMBL human target activity exists for `GPR183`
  (`CHEMBL3259470`, `396` reported IC50/Ki/Kd/EC50 activity rows).
- Failed gates:
  - `GPR183` MS white matter receptor anchor is negative:
    delta `-0.1364`, p `0.6637`.
  - Ligand-production module in MS white matter remains weak:
    mean effect `0.0711`.
  - No broad h5ad context passed the full ligand + receptor + response
    coherence rule.
  - `GPR183` target-resolved genetics breadth reaches only `2` autoimmune
    diseases in the local target-resolution stack.
  - Gene-level response support is only `1` system.
  - Direct MS/EAE-adjacent prior art exists.
- Important secondary result:
  - IBD external anti-TNF datasets show strong baseline `GPR183` nonresponse
    association: four primary contexts nonresponse-high, weighted Hedges g
    responder-minus-nonresponder `-1.108`, min p `0.000899`.
  - RA reverses direction for `GPR183`: weighted Hedges g `0.706`, p `0.0279`.
  - Psoriasis adalimumab is weak/null: Hedges g `-0.0637`, p `0.897`.
- Prior-art blockers retrieved by PubMed:
  - PMID `34145920`, DOI `10.1111/ejn.15359`
  - PMID `28147280`, DOI `10.1016/j.celrep.2017.01.020`
  - PMID `28052250`, DOI `10.1016/j.celrep.2016.12.006`

Decision:

- Close `GPR183` as a V3 therapeutic target/intervention route.
- Retain IBD `GPR183` as a disease-specific anti-TNF nonresponse marker, not
  as the cross-autoimmune lipid-lysosomal central node.
- Pivot again toward controllers whose evidence is not just response-marker
  strength in one disease and whose prior art is not already direct in MS/EAE.

## 2026-05-27 20:03 CEST

Wave94 implemented and completed.

Script:

- `scripts/v3_wave94_accessible_state_rerank.py`

Runner:

- Added to `run_v3_analysis.sh`.

Verification:

- `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave94_accessible_state_rerank.py`
- `bash -n run_v3_analysis.sh`
- `.venv_v3_py312/bin/python scripts/v3_wave94_accessible_state_rerank.py`

Output directory:

- `results_v3/wave94_accessible_state_rerank/`

Initial issue:

- The first run sorted `NO_GO` calls ahead of parked calls because the rank was
  lexicographic. It also failed to hard-penalize known closed genes and generic
  immune-marker symbols.
- Patch:
  - Added explicit call ordering.
  - Added hard penalties for known closed/saturated routes (`FABP5`, `GPR183`,
    `NAMPT`, `OSM`, `IL1B`, `LAMP3`, `TREM1`, `ACSL1`).
  - Added hard penalties for generic chemokine/cytokine/IFN/HLA-like markers.

Final result:

- `46` accessible or manually included state candidates ranked.
- Call counts:
  - `7` `PARK_FOR_NEXT_FORCING_TEST`
  - `13` `PARK_ACCESSIBLE_MARKER_OR_WEAK_ROUTE`
  - `26` `NO_GO_ACCESSIBLE_STATE_RERANK`
- Top parked candidates:
  - `SEL1L3`: score `12.17`, MS delta `0.9225`, p `0.0181`, broad positive
    disease count `4`, response support in IBD and RA, but weak genetics and
    little mechanism.
  - `NRCAM`: score `12.05`, MS delta `1.298`, p `0.0813`, response
    nonresponse-high across IBD/RA/psoriasis, but limited breadth and weak
    genetics; neural adhesion biology raises safety concerns.
  - `C15ORF48`: score `11.47`, MS delta `1.223`, p `0.00375`, myeloid-positive
    in `3` disease contexts, but response direction is responder-high rather
    than nonresponse-high and direct druggability is unclear.
  - `CD200`: score `10.59`, MS trend, myeloid-positive contexts, IBD/RA
    response support, but psoriasis reverses and CD200/CD200R prior biology is
    likely crowded.
- Closed or deprioritized:
  - `CXCL9` was demoted after generic-immune-marker penalty despite a high raw
    biology score.
  - `APOC1` remains no-go due directional negative contexts and response
    conflict.
  - `GPNMB` remains no-go due directional conflict despite MS expression.

Decision:

- Do not claim a finding from Wave94.
- Use Wave94 as branch selection only.
- Next local forcing test should compare `SEL1L3`, `NRCAM`, `C15ORF48`, and
  `CD200` on mechanism, prior art, druggability, foundation-model evidence, and
  whether the signal is compatible with lipid-lysosomal myeloid biology.

## 2026-05-27 20:19 CEST

Wave95 CD300-vs-accessible-top forcing triage.

Reason for the wave:

- Wave92 left `CD300_RECEPTOR_SPECIFIC_TUNING` as the most lipid/efferocytosis-
  relevant route, but it failed MS white-matter anchoring.
- Wave94 left `SEL1L3`, `NRCAM`, `PLEK2`, `C15ORF48`, `CD200`, `CHI3L1`, and
  `ROMO1` as accessible/statistical routes, but their mechanistic relationship
  to the lipid-lysosomal myeloid module was uneven.
- I needed one comparable gate matrix to avoid drifting between route-level
  biology and gene-level statistics.

Implementation:

- Added `scripts/v3_wave95_cd300_vs_accessible_top_forcing_triage.py`.
- Added it to `run_v3_analysis.sh`.
- Verification:
  - `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave95_cd300_vs_accessible_top_forcing_triage.py`
  - `bash -n run_v3_analysis.sh`
  - `.venv_v3_py312/bin/python scripts/v3_wave95_cd300_vs_accessible_top_forcing_triage.py`

Failed attempt / bug caught:

- First run incorrectly called `SEL1L3` `PROMOTABLE_TO_DEEP_VALIDATION`.
- Cause: promotion gates required MS anchor, breadth, response, targetability,
  and no safety/prior block, but did not require myeloid/module fit or
  genetics/foundation support.
- Fix: promotion now also requires `gate_myeloid_or_module_fit` and
  `gate_genetics_or_foundation`.

Current output:

- Output directory:
  `results_v3/wave95_cd300_vs_accessible_top_forcing_triage/`
- Analysis call:
  `NO_PROMOTABLE_ROUTE_AFTER_CD300_VS_ACCESSIBLE_TOP_FORCING_TRIAGE`.
- Entities tested: `8`.
- Call counts:
  - `NO_GO_WAVE95_FORCING_TRIAGE`: `5`
  - `PARK_AS_STATE_CONTROLLER_OR_BIOMARKER`: `2`
  - `PARK_FOR_NON_MS_LEAD_INDICATION_ONLY`: `1`
- Top entity:
  `C15ORF48`, call `PARK_AS_STATE_CONTROLLER_OR_BIOMARKER`, score `11.0`.
- `C15ORF48` evidence:
  - MS white-matter delta `1.223`, p `0.003753`.
  - Broad h5ad positive disease count `4`.
  - Myeloid-positive disease count `3`.
  - No broad directional-negative context.
  - Response evidence is not supportive for anti-TNF nonresponse:
    IBD responder-high (`g=0.547`, p `0.0346`), RA weak responder-high,
    psoriasis weak nonresponse-high.
  - No genetics or foundation-model support in current local artifacts.
  - Not directly druggable/accessibly targetable in current evidence stack.
- `CD300_RECEPTOR_SPECIFIC_TUNING`:
  - Parked for non-MS lead indication only.
  - Response support repeats across IBD and RA, but MS route delta is `-0.394`,
    p `0.2625`, and broad h5ad positive disease count is only `2`.
- `SEL1L3`:
  - No-go despite high raw score because it fails myeloid/module fit.
- `NRCAM`:
  - No-go despite response consistency because it is off-module and
    safety-blocked by neural adhesion biology.

Decision:

- Do not promote any Wave95 entity.
- `C15ORF48` is the strongest state-controller/biomarker branch left.
- Next branch should search for tractable intervention points upstream or
  downstream of the `C15ORF48` mitochondrial inflammatory-brake state rather
  than treating `C15ORF48` itself as the therapeutic target.

## 2026-05-27 19:56 CEST

Continuation audit and correction after interruption.

Wave92 controller-route audit:

- Added `scripts/v3_wave92_lipid_state_controller_route_audit.py`.
- Added the script to `run_v3_analysis.sh`.
- Verification:
  - `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave92_lipid_state_controller_route_audit.py`
  - `bash -n run_v3_analysis.sh`
  - `.venv_v3_py312/bin/python scripts/v3_wave92_lipid_state_controller_route_audit.py`
- Output directory:
  `results_v3/wave92_lipid_state_controller_route_audit/`
- Result:
  - Analysis call: `NO_REOPEN_CONTROLLER_ROUTE`.
  - Routes tested: `15`.
  - Top route: `CD300_RECEPTOR_SPECIFIC_TUNING`, call
    `NO_GO_NO_MS_WHITE_MATTER_ROUTE_ANCHOR`.
  - `CD300`, `AHR`, `SQLE`, `FPR2`, `GPR65`, and `GPR183` show some
    autoimmune response/atlas evidence but no MS white-matter route anchor.
  - `LXR_ABCA1_ABCG1_EFFLUX` is the only route with a strong MS white-matter
    route anchor but is `BLOCKED_BY_PRIOR_ART_AND_SAFETY` and weak/negative in
    broad h5ad support.

Wave93 rerun correction:

- Re-ran `scripts/v3_wave93_gpr183_oxysterol_forcing_test.py` after patching
  the IBD score orientation bug (`gene_z.loc[present].T`) and a missing-column
  empty ChEMBL result guard.
- Current reproducible output differs from the earlier notebook text for API
  subclaims: PubMed and ChEMBL calls failed with DNS errors in this sandboxed
  run, recorded in `pubmed_query_log.tsv` and `chembl_target_query.tsv`.
- The biological decision is unchanged:
  `NO_GO_GPR183_NO_MS_RECEPTOR_OR_LIGAND_ANCHOR`.
- Current gate count is `1/7`; the only passing gate is
  `no_direct_ms_or_eae_prior_art`, but that pass is not interpretable as a
  verified novelty statement because PubMed API access failed.
- The decisive failures are independent of network access:
  - `GPR183` MS white-matter delta `-0.1364`, p `0.6637`.
  - ligand-production mean effect `0.0711`.
  - coherent ligand/receptor/response disease count `0`.
  - target-resolved genetics breadth `2`.
  - response support systems `1`.

Decision:

- Keep `GPR183` closed.
- Do not use current Wave93 API-derived PubMed/ChEMBL fields for novelty or
  druggability claims.
- The next branch must either use browser-based verified sources for any
  external novelty/druggability claim or stay within local data for
  non-claim-generating triage.

## 2026-05-27 20:22 CEST

Corrected and ran the broader Wave95 mechanistic forcing triage after the
usage-limit interruption. The idle gap is excluded from working-time accounting.

Files:

- `scripts/v3_wave95_mechanistic_forcing_triage.py`
- `results_v3/wave95_mechanistic_forcing_triage/`

Corrections before using the output:

- Added missing Wave94 response fields into the gate matrix:
  `response_nonresponse_high_systems_p20`,
  `response_responder_high_systems_p20`, `response_direction_conflict`, and
  `response_summary`.
- Tightened the Wave37 perturbation gate so missing CRISPR FDR no longer
  counts as supportive real perturbation evidence.
- Corrected route prior-art parsing so `NOT_BLOCKED_BUT_*` is not classified
  as prior-art blocked by substring matching.
- Added the script to `run_v3_analysis.sh`; `bash -n run_v3_analysis.sh`
  passes.

Result:

- Analysis call: `NO_MECHANISTIC_THERAPEUTIC_PROMOTION`.
- Candidates tested: `15`.
- Promoted candidates: `0`.
- Call counts:
  - `NO_GO_MARKER_WITHOUT_RESIDUAL_OR_PERTURBATION_SUPPORT`: `8`.
  - `PARK_WETLAB_KILL_TEST_ONLY`: `4`.
  - `NO_GO_PRIOR_ART_OR_SAFETY_BLOCKED`: `3`.
- Top ranked direct candidates:
  - `SEL1L3`: critical gates `4`, support gates `2`; no residual controller or
    validated perturbation support.
  - `C15ORF48`: critical gates `4`, support gates `1`; strong MS/myeloid
    expression clue, but no residualized controller, genetics, perturbation, or
    modality package.
  - `PLEK2`: critical gates `4`, support gates `1`; same marker-without-controller
    failure mode.
- Wet-lab-only routes:
  - `MFGE8`, `FXYD5`, `FPR2_ANXA1_BIASED_RESOLUTION`,
    `CD300_RECEPTOR_SPECIFIC_TUNING`.

Decision:

- No Wave94/sidecar direct candidate is promotable.
- Do not continue with accessible-marker reranking.
- Wave96 will search for druggable upstream/downstream controllers of the
  `C15ORF48` mitochondrial inflammatory-brake state, using cell-resolved
  co-state relationships, MS lesion anchoring, cross-disease recurrence,
  genetics/druggability, and perturbation-response evidence.

## 2026-05-27 21:00 CEST

Continuation after usage-limit interruption. The idle gap is excluded from
working-time accounting.

Wave96/Wave97 status at resume:

- Wave96 had already run and reopened no C15ORF48 controller candidates.
- Wave96 parked 13 proximal candidates: `CCL20`, `IL23A`, `CD200`, `PLEK2`,
  `LITAF`, `FKBP1A`, `CASP4`, `JAK3`, `IL15`, `SLPI`, `PIK3R2`, `MTHFD2`,
  and `PDPN`.
- Wave97 residual donor-level co-state falsification reopened only `CCL20`.

Sidecar reconciliation:

- The old Wave97 runtime sidecar IDs were not retrievable (`not_found`), but
  the sidecar files existed in `subagents_v3/`:
  - `wave97_c15_prior_art_sidecar.md`
  - `wave97_c15_directionality_sidecar.md`
  - `wave97_hostile_critique.md`
- I also recovered and preserved the earlier Wave95 sidecar returns in
  `subagents_v3/wave95_sidecar_returns_integrated.md`.

Wave98 CCL20/CCR6 forcing audit:

- Added `scripts/v3_wave98_ccl20_ccr6_forcing_audit.py`.
- Added the script to `run_v3_analysis.sh`.
- First run failed because `pandas.to_markdown()` requires optional dependency
  `tabulate`, which is not installed/pinned in `.venv_v3_py312`.
- Patch: replaced `to_markdown()` with a small dependency-free markdown table
  writer in the script.
- Second run exposed a call-label bug: `numpy.bool_ is False` identity check
  failed, so the call was incorrectly labeled
  `NO_GO_CCL20_CCR6_AXIS_INCOMPLETE`.
- Patch: converted the novelty gate to a real bool and used `not novelty_gate`.

Verification:

- `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave98_ccl20_ccr6_forcing_audit.py`
- `bash -n run_v3_analysis.sh`
- `.venv_v3_py312/bin/python scripts/v3_wave98_ccl20_ccr6_forcing_audit.py`

Current output:

- Output directory:
  `results_v3/wave98_ccl20_ccr6_forcing_audit/`
- Analysis call:
  `NO_GO_CCL20_CCR6_PRIOR_ART_BLOCKED`.
- Claim-grade gates passed: `1/7`.
- Passed:
  - `ligand_state_recurrence`.
- Failed:
  - `receptor_coupled_to_c15_state`
  - `ms_claim_grade_anchor`
  - `target_resolved_genetics_or_coloc`
  - `directional_perturbation_or_foundation_support`
  - `novelty_not_blocked`
  - `therapeutic_feasibility_without_host_defense_penalty`
- Axis facts:
  - `CCL20`: Wave97 call `REOPEN_AFTER_RESIDUAL_COSTATE`,
    C15-positive disease count `3`, C15-state Pearson r `0.7105`,
    residual case-positive disease count `1`, MS delta `1.1469`,
    MS p `0.0611`, MS FDR `0.8989`, strong QTL/coloc disease count `1`,
    Geneformer strong-support contexts `0`, Wave81
    `NO_GO_NO_PERTURBATION_SUPPORT`.
  - `CCR6`: C15-positive disease count `0`, donor case-positive disease count
    `0`, MS delta `0.2230`, p `0.7785`, FDR `0.9742`.

Subagent integration:

- `wave98_hostile_c15_ccl20_branch_review.md`:
  do not promote; CCL20 is a known inflammatory chemokine passenger and the
  C15 anchor is not MS-specific.
- `wave98_ccl20_ccr6_prior_art_sidecar.md`:
  call `NO_AUTOIMMUNE_THERAPEUTIC_NOVELTY_FOR_CCL20_CCR6_AXIS`.
- `wave97_ccl20_ccr6_mechanistic_sidecar.md`:
  CCL20 is downstream/parallel inflammatory chemokine output; CCR6 is not
  locally C15-state coupled.

Decision:

- Close `CCL20/CCR6` as a V3 therapeutic nomination.
- Keep only as a positive-control trafficking axis for future C15-state
  perturbation-ordering experiments.
- Pivot to the upstream stress-generator class (`LITAF`, `CASP4`) with a
  perturbation-first forcing test.

## 2026-05-27 21:14 CEST

Wave99 upstream stress-generator audit.

Rationale:

- Wave97/sidecars suggested `LITAF` and `CASP4` were the most plausible
  upstream stress-generator class around C15ORF48/MOCCI.
- A further co-expression scan would be weak. I required actual perturbation or
  time-course ordering from real data already in the workspace.

Files:

- `scripts/v3_wave99_litaf_casp4_stress_generator_audit.py`
- `results_v3/wave99_litaf_casp4_stress_generator_audit/`
- Added to `run_v3_analysis.sh`.

Verification:

- `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave99_litaf_casp4_stress_generator_audit.py`
- `bash -n run_v3_analysis.sh`
- `.venv_v3_py312/bin/python scripts/v3_wave99_litaf_casp4_stress_generator_audit.py`

Data used:

- `GSE294918_IFNyRNAseq_CPM.csv.gz`: human macrophage IFN/LPS time course and
  ruxolitinib perturbation.
- `GSE162464_Normalized_Gene_Counts_Matrix.txt.gz`: mouse macrophage `Gsk3b`
  and `Med16` perturbations; note `C15orf48` is absent from the matrix.
- Local Wave96/Wave97/Wave37/Wave39/Wave57/Wave68/Wave81 summaries.

Current output:

- Analysis call: `NO_PROMOTABLE_LITAF_CASP4_STRESS_GENERATOR`.
- `LITAF`: `PARK_LITAF_UPSTREAM_STRESS_MARKER_NO_MODALITY`, `3/10` gates.
- `CASP4`: `PARK_CASP4_UPSTREAM_PYROPTOSIS_NODE_PRIOR_SELECTIVITY_BLOCKED`,
  `3/10` gates.

Key quantitative details:

- `LITAF`:
  - C15-positive diseases `3`; residual case-positive diseases `3`.
  - Human macrophage time course: LPS trajectories support temporal ordering:
    `LITAF` first rises at 3 h and peaks at 3 h / 6 h; `C15ORF48` peaks at
    12 h.
  - Ruxolitinib does not coherently suppress `LITAF` and `C15ORF48`
    (`rux_mean_3_6h_LITAF=-0.0569`; 6 h `C15ORF48=-0.3235`).
  - Mouse perturbation is weak/inconsistent (`Gsk3b` KO `-0.236`; `Med16` KO
    `-0.0928` under IFN-gamma).
  - MS anchor fails: delta `0.3084`, p `0.1716`, FDR `0.8994`.
  - No target-resolved genetics, no direct CRISPR/foundation support, no
    selective modality.
- `CASP4`:
  - C15-positive diseases `3`; residual case-positive diseases `2`.
  - Ruxolitinib suppresses `CASP4` strongly
    (`rux_mean_3_6h_CASP4=-1.081`) and suppresses `C15ORF48` switch features,
    but this is broad JAK/IFN confounding (`ifn_apc` 6 h `-1.306`).
  - Mouse perturbation is contradictory (`Gsk3b` KO lowers `Casp4`,
    `Med16` KO raises it).
  - MS anchor fails: delta `0.2067`, p `0.4927`, FDR `0.9272`.
  - No target-resolved genetics or direct CRISPR/foundation support.
  - ChEMBL activity count exists (`61`) but selectivity against CASP1/CASP5 and
    prior art remain blockers.

Decision:

- `LITAF` and `CASP4` stay useful for perturbation-ordering wet-lab design.
- Neither is a therapeutic nomination.
- Unless sidecar audits overturn this, leave the C15-proximal branch and return
  to broader cross-autoimmune intervention-first search.

## 2026-05-27 21:20 CEST

Wave99 sidecar integration.

Sidecar returns:

- `wave99_litaf_sidecar_audit.md`:
  - `LITAF` remains a perturbation-ordering hypothesis / inflammatory stress
    marker, not a target nomination.
  - Direct prior art in inflammatory arthritis/IBD: PMIDs `22160695`,
    `16804395`, `21984950`.
  - Patent prior art: `US11767283B2`, kava analogs for inflammatory/RA biology
    with Kava-241 reducing LITAF in macrophages.
  - No selective LITAF modality or LITAF-directed autoimmune clinical trial.
- `wave99_casp4_sidecar_audit.md`:
  - `CASP4` remains `PARK/NO-GO`.
  - Direct/close prior art: PMID `11136825`, PMID `34044393`, PMID
    `40044809`, Ventus `VENT-04`, `WO2026055444`, `US20230250067A1`.
  - CASP4/5 dual inhibition is feasible; CASP4-only selectivity is not a safe
    assumption.
- `sidecar_litaf_casp4_perturbation_modeling.md`:
  - No direct perturbation dataset in the workspace perturbs `LITAF` or `CASP4`
    and measures the C15/NDUFA4/MOCCI state.
  - `CASP4` is IFN/JAK-primed stress readout/control.
  - `LITAF` is late LPS/C15 co-state with weak rux effect and nonsignificant
    mouse IFN induction.

Decision after sidecars:

- Sidecars agree with Wave99.
- Close the C15-proximal therapeutic-target branch.
- Resume a broader intervention-first search across the lipid-lysosomal
  cross-autoimmune module.

## 2026-05-27 21:08 CEST

Wave99B endogenous inflammasome-brake audit.

Rationale:

- The upstream stress-generator branch left `CASP4` close to the biology but
  prior-art/safety blocked, and `LITAF` lacked a modality.
- Instead of directly drugging stress generators, I tested whether endogenous
  brakes of the same axis (`CARD16`, `SERPINB1`, `IL18BP`, `CARD17`,
  `CARD18`, `CARD8`) or nearby pyroptosis comparators could provide a more
  tractable intervention point.
- I treated disease-high brake expression as ambiguous. It could be protective
  compensation, failed compensation, a severity marker, or a driver depending
  on perturbation ordering.

Files:

- `scripts/v3_wave99_endogenous_inflammasome_brake_audit.py`
- `results_v3/wave99_endogenous_inflammasome_brake_audit/`
- Added to `run_v3_analysis.sh`.

Execution notes:

- First attempted `python3 scripts/v3_wave99_endogenous_inflammasome_brake_audit.py`;
  this failed before analysis because system Python lacks `numpy`.
- Re-ran with `.venv_v3_py312/bin/python`.
- Found a reporting/gating bug: the script initially read `delta_log2_cpm`
  from `gse111972_full_ms_wm_signature.tsv`, but that file uses `delta_log2`.
  Patched and re-ran. The no-go call held.

Result:

- Analysis call: `NO_REOPEN_ENDOGENOUS_INFLAMMASOME_BRAKE_TARGET`.
- Candidates tested: `17`.
- Reopened: `0`.
- Parked: `0`.
- Call counts:
  - `NO_GO_PRIOR_OR_SAFETY_BLOCKED`: `13`.
  - `NO_GO_COMPENSATORY_BRAKE_MARKER`: `2`.
  - `NO_GO_LOCAL_EVIDENCE_WEAK`: `2`.

Top result:

- `CARD16`: `NO_GO_COMPENSATORY_BRAKE_MARKER`.
  - Broad positive disease count `5`.
  - C15 trend-positive disease count `4`.
  - Residual C15 case-positive disease count only `1`.
  - MS white-matter delta `0.4271`, p `0.4948`, FDR `0.9274`.
  - Anti-TNF mono/mac remission-adjusted delta `-0.7672`, FDR `0.0339`.
  - No real perturbation direction, no genetics, and no selective modality.

Sidecar integration:

- Prior-art/druggability sidecar:
  no GO. `CARD16` is only a PARK-worthy local ordering hypothesis; `SERPINB1`,
  `IL18BP`, `NLRP3`, `CASP1`, `GSDMD`, `IL1B`, and related comparators are
  prior-arted, direction-conflicted, or safety/modality blocked.
- Directionality sidecar:
  `CARD16` is the strongest local C15-linked clue but directionally unsafe;
  `SERPINB1` has the cleanest published brake mechanism but weak local MS/C15
  support.

Decision:

- Close endogenous inflammasome-brake rescue as a therapeutic-nomination route.
- Keep `CARD16`, `SERPINB1`, and `IL18BP` as wet-lab ordering controls only.
- Pivot back to module-level / intervention-first search; do not continue
  adding expression-only C15 or pyroptosis adjacency tests.

## 2026-05-27 20:47 CEST

Wave96 and Wave97 C15ORF48-state branch integration.

Wave96:

- Added `scripts/v3_wave96_c15orf48_controller_search.py`.
- Added the script to `run_v3_analysis.sh`.
- First run failed before producing biological output because the C15 anchor
  merge created suffixed `disease_name` fields; patched the merge to keep the
  original broad contrast metadata.
- Final run output:
  `results_v3/wave96_c15orf48_controller_search/`.
- Analysis call: `C15_CONTROLLER_SEARCH_COMPLETED`.
- Genes ranked: `25175`.
- Donor-validated genes: `370`.
- Reopened controller candidates: `0`.
- Parked proximal intervention candidates: `13`:
  `CCL20`, `IL23A`, `CD200`, `PLEK2`, `LITAF`, `FKBP1A`, `CASP4`, `JAK3`,
  `IL15`, `SLPI`, `PIK3R2`, `MTHFD2`, `PDPN`.
- Known issue from hostile critique:
  - the Wave96 report sorting is misleading because `NO_GO_*` rows appear
    before `PARK_*` rows alphabetically;
  - `wave96_reason` underreports support-gate failures for `CCL20`;
  - Wave96 is a branch map, not a therapeutic claim.

Wave97 residual co-state falsification:

- Added `scripts/v3_wave97_c15_residual_costate_falsification.py`.
- Added the script to `run_v3_analysis.sh`.
- Output:
  `results_v3/wave97_c15_residual_costate_falsification/`.
- Analysis call:
  `C15_RESIDUAL_COSTATE_FALSIFICATION_COMPLETED`.
- Candidates tested: `13`.
- Reopened after residualization: `1`, `CCL20`.
- Parked residual co-state with modality:
  `LITAF`, `CASP4`, `CD200`, `SLPI`, `MTHFD2`, `PDPN`, `FKBP1A`, `PIK3R2`,
  `PLEK2`.
- Generic-inflammation-confounded:
  `JAK3`, `IL15`.
- Residual weak:
  `IL23A`.

Subagent integration:

- Hostile critique:
  Wave96 is useful as a negative branch map but not a valid controller-discovery
  assay. Required fixes include residualized co-state testing, better support
  failures, explicit report sorting, C15 module rather than single-gene anchor,
  and MS compartment validation.
- Directionality sidecar:
  no parked candidate is ready as a causal C15ORF48/MOCCI controller.
  `CD200`/`SLPI` are protective co-brake comparators; `LITAF`/`CASP4` are
  plausible upstream inflammatory stress generators; `CCL20`, `IL23A`, `JAK3`,
  and `IL15` are likely inflammatory-axis passengers.
- Prior-art sidecar:
  no candidate earned a GO call. `CCL20/CCR6`, `IL23A/IL-23`, `CD200/CD200R`,
  `FKBP1A`, `JAK3`, `IL15`, `SLPI`, and `MTHFD2` are novelty-blocked or
  saturated for autoimmune/MS therapeutic use. `PLEK2`, `LITAF`, `PIK3R2`, and
  `CASP4` remain only parked because the C15ORF48-state framing appears
  unpublished but causal support/actionability is inadequate.

Decision:

- Do not promote `CCL20` despite residual co-state survival; it is a known
  CCL20/CCR6 autoimmune/MS/EAE axis and likely a downstream inflammatory
  passenger.
- Do not claim a C15ORF48 therapeutic target from the current branch.
- Continue with a perturbation-first successor branch focused on novelty-open
  candidates, especially `LITAF` and `PLEK2`, while treating `CASP4` as close
  prior-art/pyroptosis comparator and `PIK3R2` as broad PI3K-adjacent weak
  route.

## 2026-05-27 21:19 CEST

Wave100 cAMP-restoration intervention-class audit.

Reason:

- After direct C15-proximal routes failed, cAMP restoration was the best
  intervention-class reopener because `ADCY3`, `GPR65`, `PDE4B/PDE4D`,
  `PTGER4`, adenosine receptors, and HCAR receptors recur across genetics,
  druggability, or C15/state-adjacent scans.
- I deliberately avoided a weak "cAMP signature score" test. The forcing
  question was whether any specific route clears modality, directionality,
  cross-disease cell-state support, MS anchoring, genetics, perturbation/model
  support, safety, and prior-art gates together.

Local code:

- Added `scripts/v3_wave100_camp_restoration_class_audit.py`.
- Added the script to `run_v3_analysis.sh`.
- Syntax check:
  `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave100_camp_restoration_class_audit.py`.
- Run:
  `.venv_v3_py312/bin/python scripts/v3_wave100_camp_restoration_class_audit.py`.

Outputs:

- `results_v3/wave100_camp_restoration_class_audit/camp_restoration_candidate_rank.tsv`
- `results_v3/wave100_camp_restoration_class_audit/camp_candidate_context_rows.tsv`
- `results_v3/wave100_camp_restoration_class_audit/summary.json`
- `results_v3/wave100_camp_restoration_class_audit/REPORT.md`

Key numeric result:

- Branch call:
  `NO_REOPEN_CAMP_RESTORATION_CLASS`.
- Candidates tested: `10`.
- Promoted candidates: `0`.
- Call counts:
  `NO_GO_PRIOR_ART_OR_BRANCH_BLOCKED=8`,
  `NO_GO_NO_SELECTIVE_ACTIONABLE_MODALITY=2`.
- `ADCY3` ranked highest but failed cross-disease cell-state, target-resolved
  breadth, MS genetic anchor, perturbation/model support, actionable modality,
  and direction gates.
- `PDE4B` was the best practical perturbation comparator:
  raw positive disease count `4`, retained positive disease count `3`,
  anti-TNF DC remission-adjusted delta `-0.4438`, FDR `0.0583`, but MS
  white-matter delta was `-0.4295` with p `0.2821`, target genetics were absent,
  L1000 core cAMP/PDE4 reversal support was absent, and prior-art/safety gates
  blocked promotion.
- PDE4/cAMP class L1000 audit carried forward:
  `85` LINCS metadata rows, `34` unique perturbagen IDs, `2` broad cAMP/PDE4
  top opposite-hit rows, `0` core PDE4/cAMP compounds among top opposite hits.

Sidecar integration:

- `subagents_v3/wave100_camp_directionality_model_sidecar.md`:
  no finding claimed. It independently ranked `PDE4B` as the best local
  perturbation hypothesis, `PTGER4` as the genetics-rich but direction-conflicted
  comparator, and rejected `ADCY3`, `GPR65`, `ADORA2A/B`, and `HCAR2` from
  current local evidence.
- `subagents_v3/wave100_camp_prior_art_sidecar.md`:
  no route is a GO. It found PDE4B/D local cAMP restoration only suitable as a
  prior-art-aware comparator or stratification branch, not as a novel class
  therapeutic claim. It kept `GPR65` as secondary PARK and called `ADCY3`,
  `PTGER4`, `ADORA2A/B`, `HCAR2`, and generic cAMP controls no-go for target
  promotion.

Decision:

- Close cAMP restoration as a V3 target-nomination route.
- Keep `PDE4B/D` only as a wet-lab comparator/stratification readout for
  CIITA-HLA-II-CD74/C15 state reversibility.
- Do not reopen `ADCY3`, `GPR65`, `PTGER4`, `ADORA2A/B`, `HCAR2`, `HCAR3`,
  or `FFAR2` without direct route-specific perturbation data.
- Write `CONVERGENCE_CHECK_56.md`.
- Pivot to the remaining intervention-first survivor space outside C15/cAMP
  adjacency.

## 2026-05-27 21:29 CEST

Wave101 accessible-survivor forcing triage.

Reason:

- After C15-proximal, inflammasome-brake, stress-generator, and cAMP branches
  failed, I tested whether the remaining accessible or membrane-associated
  survivors could justify a focused therapeutic branch.
- This was deliberately not a promotion test. The forcing question was whether
  any accessible survivor had enough MS anchoring, cross-disease recurrence,
  response specificity, perturbation/model evidence, genetics, safety, and
  modality to reopen a deeper target-specific branch.

Local code:

- Added `scripts/v3_wave101_accessible_survivor_forcing_triage.py`.
- Fixed a report-ordering bug before logging: the first run sorted by call
  string and put hard no-go candidates above parked candidates. I added explicit
  call priority and filled missing scoring fields with zero.
- Added the script to `run_v3_analysis.sh`.
- Syntax checks:
  `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave101_accessible_survivor_forcing_triage.py`
  and `bash -n run_v3_analysis.sh`.
- Run:
  `.venv_v3_py312/bin/python scripts/v3_wave101_accessible_survivor_forcing_triage.py`.

Outputs:

- `results_v3/wave101_accessible_survivor_forcing_triage/accessible_survivor_forcing_rank.tsv`
- `results_v3/wave101_accessible_survivor_forcing_triage/summary.json`
- `results_v3/wave101_accessible_survivor_forcing_triage/REPORT.md`

Key numeric result:

- Branch call:
  `NO_PROMOTABLE_ACCESSIBLE_SURVIVOR_YET`.
- Candidates tested:
  `12`.
- Call counts:
  `PARK_NEEDS_PERTURBATION_AND_GENETIC_ANCHOR=3`,
  `NO_GO_WEAK_MS_ANCHOR=3`,
  `NO_GO_PRIOR_OR_CROWDED_ROUTE=4`,
  `NO_GO_NO_ACTIONABLE_ACCESSIBILITY=1`,
  `NO_GO_SAFETY_BLOCKED_NEURAL_ADHESION=1`.
- Top forcing candidates:
  `SEL1L3`, `FXYD5`, `APOC1`.
- `SEL1L3`: score `22.78`, gate count `8`, MS white-matter delta `0.9225`,
  p `0.01814`, positive disease count `3`, missing gates
  `perturbation_or_model;genetic_anchor`.
- `FXYD5`: score `17.23`, gate count `7`, MS white-matter delta `0.3525`,
  p `0.05871`, positive disease count `4`, negative disease count `1`,
  missing gates `perturbation_or_model;genetic_anchor;direction_not_conflicted`.
- `APOC1`: score `14.41`, gate count `6`, MS white-matter delta `0.8063`,
  p `0.03335`, positive disease count `3`, negative disease count `1`,
  missing gates `response_signal;perturbation_or_model;genetic_anchor;direction_not_conflicted`.

Decision:

- Do not promote any accessible survivor.
- Do not return to broad marker ranking. The only defensible next step is a
  targeted, mechanistic forcing branch comparing `SEL1L3` and `FXYD5`, with
  `APOC1` as a lipid-state confounder comparator and `CD82`/`LAPTM5` as
  endolysosomal comparators.
- Dispatch sidecars for prior art, modality/topology, and mechanism/direction,
  then run local residual and tissue-compartment tests focused on whether
  `SEL1L3` or `FXYD5` remains disease-linked after lipid-lysosomal/stress
  module adjustment.

## 2026-05-27 21:40 CEST

Wave101 sidecar integration and Wave102 accessible-survivor closure.

Reason:

- A compacted-context gap exposed that Wave102 artifacts already existed in
  the tree: the residual compartment test and target-specific evidence audit
  had both closed `SEL1L3`/`FXYD5`.
- I wrote the missing Wave101 mechanism/directionality sidecar requested for
  `SEL1L3` versus `FXYD5`, with `APOC1`, `CD82`, and `LAPTM5` as comparators.
- I then added a stricter Wave102 controller check that the previous residual
  test did not explicitly do: same-donor tissue-resident candidate expression
  versus paired myeloid lipid/C15/inflammatory module state.

Local code and outputs:

- Added sidecar:
  `subagents_v3/wave101_accessible_survivor_mechanism_sidecar.md`.
- Added and ran:
  `scripts/v3_wave102_sel1l3_fxyd5_residual_controller_test.py`.
- Added the script to `run_v3_analysis.sh`.
- Syntax checks:
  `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave102_sel1l3_fxyd5_residual_controller_test.py`
  and `bash -n run_v3_analysis.sh`.
- Output directory:
  `results_v3/wave102_sel1l3_fxyd5_residual_controller_test/`.

Key result:

- Branch call:
  `NO_REOPEN_ACCESSIBLE_SURVIVOR_AFTER_RESIDUAL_TEST`.
- Completed direct h5ad configs:
  `18`; failed configs:
  `0`.
- All five tested candidates were called
  `NO_GO_RESIDUAL_CONTROLLER_NOT_PROVEN`.
- `SEL1L3`: no retained composite residual disease context, despite same-donor
  tissue-to-myeloid links in Crohn disease, ulcerative colitis, psoriasis, and
  Sjogren syndrome.
- `FXYD5`: raw positive disease count `3`, no retained composite residual
  disease context, residual negative context present, and same-donor links only
  in Crohn/UC gut contexts.
- `CD82` and `LAPTM5`: the only candidates with one retained composite
  residual disease context, both restricted to ulcerative-colitis stromal
  compartment and both still blocked by Wave101 gates.

Decision:

- Close the accessible-survivor route as a V3 therapeutic target route.
- Preserve `SEL1L3`, `FXYD5`, `CD82`, and `LAPTM5` only as localization or
  wet-lab comparator readouts.
- Pivot from "which accessible marker is targetable?" to "which sender-to-
  myeloid ligand/pathway explains the paired tissue-to-myeloid lipid/C15
  module?"

## 2026-05-27 21:34 CEST

Wave102 accessible-survivor residual compartment test.

Reason:

- Wave101 left `SEL1L3`, `FXYD5`, and `APOC1` parked because they had
  expression breadth/accessibility but no target-specific perturbation or
  genetics.
- The correct next question was not another surface-marker rank. I tested
  whether these candidates retain same-compartment disease association after
  donor-level residualization against the lipid-lysosomal, lysosomal/APC,
  IFN/APC, NF-kB, and HIF/NAMPT modules.

Local code:

- Added `scripts/v3_wave102_accessible_survivor_residual_compartment_test.py`.
- Added the script to `run_v3_analysis.sh`.
- Syntax checks:
  `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave102_accessible_survivor_residual_compartment_test.py`
  and `bash -n run_v3_analysis.sh`.
- Run:
  `.venv_v3_py312/bin/python scripts/v3_wave102_accessible_survivor_residual_compartment_test.py`.

Outputs:

- `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_donor_scores.tsv`
- `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_gene_presence.tsv`
- `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_raw_tests.tsv`
- `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_residual_tests.tsv`
- `results_v3/wave102_accessible_survivor_residual_compartment_test/accessible_survivor_residual_summary.tsv`
- `results_v3/wave102_accessible_survivor_residual_compartment_test/summary.json`
- `results_v3/wave102_accessible_survivor_residual_compartment_test/REPORT.md`

Key numeric result:

- Branch call:
  `NO_ACCESSIBLE_SURVIVOR_RESIDUAL_REOPEN`.
- Candidates tested:
  `12`.
- Completed direct-atlas analyses:
  `18`.
- Call counts:
  `PARK_WEAK_RESIDUAL_SIGNAL_ONLY=7`,
  `NO_GO_NO_DIRECT_H5AD_REPLICATION=5`.
- No candidate had strict core-covariate survival in any disease:
  `strict_core_covariate_surviving_disease_count=0` for all candidates.
- No candidate survived the multivariable `core_all` model:
  `core_all_multivariable_surviving_disease_count=0` for all candidates.
- `FXYD5` was the strongest focus candidate by raw replication:
  raw-positive disease count `3` and retained-positive disease count `2`, but
  strict core survival `0`, core-all survival `0`, one raw-negative analysis,
  and persistent Wave101 gaps in perturbation, genetics, and directionality.
- `SEL1L3` had only one raw-positive disease (`ulcerative colitis` stromal),
  one retained disease, no non-IBD retained positive disease, and no strict or
  core-all survival.
- `APOC1` had no direct h5ad replication and two raw-negative analyses.

Decision:

- Do not reopen `SEL1L3` as a target-specific branch from current in-silico
  evidence.
- Do not promote `FXYD5`; it remains, at most, a weak tissue-remodeling
  comparator unless sidecars find strong perturbation or modality evidence.
- Close `APOC1` as an accessible survivor in this branch.
- Await sidecar checks for any non-expression rescue, but the local residual
  evidence now argues against continuing the accessible-survivor route.

## 2026-05-27 21:49 CEST

Wave103 Fc/FcRn/efferocytosis intervention-route audit.

Reason:

- After the accessible-marker route failed, I pivoted to an intervention-first
  branch with real perturbation evidence: Fc receptor/FcRn/efferocytosis
  regulators.
- This branch tests a different failure mode. It does not require disease-high
  expression a priori if pharmacologic action is plausible, but it still must
  clear MS anchoring, cross-disease anchoring, genetics, directionality, safety,
  and prior-art gates before target nomination.

Local code:

- Added `scripts/v3_wave103_fc_receptor_efferocytosis_route_audit.py`.
- Added the script to `run_v3_analysis.sh`.
- Syntax checks:
  `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave103_fc_receptor_efferocytosis_route_audit.py`
  and `bash -n run_v3_analysis.sh`.
- Run:
  `.venv_v3_py312/bin/python scripts/v3_wave103_fc_receptor_efferocytosis_route_audit.py`.

Outputs:

- `results_v3/wave103_fc_receptor_efferocytosis_route_audit/fc_efferocytosis_route_rank.tsv`
- `results_v3/wave103_fc_receptor_efferocytosis_route_audit/summary.json`
- `results_v3/wave103_fc_receptor_efferocytosis_route_audit/REPORT.md`

Key numeric result:

- Branch call:
  `NO_REOPEN_FC_EFFEROCYTOSIS_ROUTE`.
- Candidates tested:
  `15`.
- Call counts:
  `NO_GO_FC_ROUTE_PRIOR_OR_DIRECTION_BLOCKED=12`,
  `PARK_EFFEROCYTOSIS_ROUTE_NO_MS_ANCHOR=2`,
  `PARK_EFFEROCYTOSIS_ROUTE_WEAK_CROSS_DISEASE_ANCHOR=1`.
- `FCGRT` had real efferocytosis-screen support
  (`wave37_contrast_lfc=1.049`) and an intervention-ready modality class, but
  local MS expression was null (`delta_log2=0.0232`, p `0.891`), broad h5ad
  expression was negative/contradictory (`0` positive and `3` negative
  diseases), genetics were absent in the local target-resolution tables, and
  prior art/safety burden is high.
- `DAB2` had MS white-matter expression (`delta_log2=0.5379`, p `0.0111`) and
  efferocytosis-screen support, but no cross-disease expression, no genetics,
  and no clean modality.
- `CD9` had MS white-matter expression (`delta_log2=1.11`, p `0.00197`) and
  efferocytosis-screen support, but no cross-disease expression, no genetics,
  and direction/selectivity blockers.

Decision:

- Do not reopen Fc/FcRn/efferocytosis as a V3 target route from local evidence.
- Keep `FCGRT` as a repurposing comparator only: it is translationally real but
  not supported as a cross-autoimmune lipid-lysosomal module anchor in the
  current data.
- Keep `DAB2` and `CD9` as wet-lab efferocytosis comparators, not target
  nominations.
- Write `CONVERGENCE_CHECK_59.md`.

## 2026-05-27 21:55 CEST

Wave104 matched-donor accessible-survivor niche-controller test.

Reason:

- The Wave101 mechanism sidecar argued that the proper test was not just
  disease-high candidate expression, but whether tissue-resident candidate
  expression predicts matched myeloid lipid-lysosomal state.
- Wave102 partly answered this by residualizing candidate disease expression,
  but it did not directly test tissue-to-myeloid matched-donor coupling.

Local code:

- Added `scripts/v3_wave104_accessible_survivor_niche_controller_test.py`.
- Added the script to `run_v3_analysis.sh`.
- First implementation problem:
  full covariate adjustment over-parameterized small IBD paired-donor tests,
  producing `NaN` adjusted estimates. I patched the script to use adaptive
  covariate trimming with explicit `covariate_mode`.
- Syntax checks:
  `.venv_v3_py312/bin/python -m py_compile scripts/v3_wave104_accessible_survivor_niche_controller_test.py`
  and `bash -n run_v3_analysis.sh`.
- Run:
  `.venv_v3_py312/bin/python scripts/v3_wave104_accessible_survivor_niche_controller_test.py`.

Outputs:

- `results_v3/wave104_accessible_survivor_niche_controller_test/matched_niche_pairs.tsv`
- `results_v3/wave104_accessible_survivor_niche_controller_test/niche_controller_tests.tsv`
- `results_v3/wave104_accessible_survivor_niche_controller_test/niche_controller_summary.tsv`
- `results_v3/wave104_accessible_survivor_niche_controller_test/summary.json`
- `results_v3/wave104_accessible_survivor_niche_controller_test/REPORT.md`

Key numeric result:

- Branch call:
  `REOPEN_ACCESSIBLE_SURVIVOR_NICHE_CONTROLLER`.
- Matched donor pairs:
  `520`.
- Tests:
  `120`.
- Top candidate:
  `CD82`.
- `CD82`: adjusted positive pair count `6`, adjusted positive disease count
  `3`, adjusted negative disease count `0`.
- Strongest `CD82` adjusted tests:
  `sjogren_gland_stromal -> sjogren_gland_apc | lysosomal_apc`,
  slope `0.500`, p `0.00335`, n `22`;
  `ibd_uc_epithelial -> ibd_uc_myeloid | lipid_loader_repair`,
  slope `0.296`, p `0.00400`, n `12`;
  `ibd_crohn_epithelial -> ibd_crohn_myeloid | lysosomal_apc`,
  slope `1.063`, p `0.0112`, n `12`;
  `ibd_crohn_epithelial -> ibd_crohn_myeloid | lipid_loader_repair`,
  slope `1.061`, p `0.0138`, n `12`.
- `SEL1L3`, `FXYD5`, `LAPTM5`, and `APOC1` had direction-conflicted niche
  signals and were not reopened.

Interpretation:

- This is a branch reopener, not a target claim.
- The signal is non-obvious because `CD82` failed earlier as a direct target
  marker, yet matched tissue-to-myeloid coupling is positive across three
  diseases.
- Immediate concern:
  IBD n is small (`12` matched donors), several adjusted models use
  `adaptive_top_8_*` covariates, and overfitting/shared-severity bias could
  create false positives.

Decision:

- Reopen `CD82` only for robustness, mechanism, prior-art, and modality attack.
- Do not promote `CD82` unless Wave105 robustness survives simpler covariate
  models, permutation/leave-one-out checks, and sidecar prior-art review.

## 2026-05-27 21:37 CEST

Wave102 SEL1L3/FXYD5 prior-art and translational sidecar.

Reason:

- The user explicitly asked for the prior-art/novelty/translational audit that
  Wave101 had dispatched as a sidecar.
- This is a necessary forcing check because a novelty-open surface marker is
  not useful if patents, clinical trials, or known biology already block the
  route.

External checks:

- Queried PubMed E-utilities across `SEL1L3`, `FXYD5`/dysadherin, and
  comparators against MS, RA, SLE, Crohn, UC, psoriasis, T1D, Sjogren, AS, MG,
  autoimmune thyroid disease, celiac, and PBC.
- Queried ClinicalTrials.gov v2 for `SEL1L3`, `"SEL1L family member 3"`,
  `FXYD5`, `dysadherin`, `APOC1`, `CD82`, and `LAPTM5`.
- Searched Europe PMC and web/patent sources for exact candidate plus
  autoimmune, antibody, patent, trial, and translational terms.

Output:

- `subagents_v3/wave102_sel1l3_fxyd5_prior_art_sidecar.md`.

Key result:

- `SEL1L3`: `PARK`. No direct autoimmune therapeutic prior art found, but
  mechanism/modality remain absent and PVRL literature identifies
  hyper-N-glycosylated SEL1L3 as an autoantigenic BCR target with immunotoxin
  feasibility, creating a safety caution.
- `FXYD5`: `PARK_KILL_TEST_ONLY`; `NO_GO` for promotion now. The route is
  encumbered by Na,K-ATPase/barrier/adhesion biology, oncology antibody and
  extracellular drug-conjugate prior art, glycoform-antibody prior art, and a
  Sjogren autoantibody diagnostic patent.
- `APOC1`, `CD82`, and `LAPTM5` remain comparators, not target routes.

Decision:

- The sidecar does not rescue the accessible-survivor branch.
- `FXYD5` may be retained only as a single-pass non-depleting,
  barrier-preserving wet-lab kill test.
- `SEL1L3` remains a staining/stratification marker until a mechanistic
  perturbation or genetic anchor appears.

## 2026-05-27 21:38 CEST

Wave102 SEL1L3/FXYD5 perturbation and model evidence sidecar.

Reason:

- The user explicitly requested a perturbation/model scout for `SEL1L3` and
  `FXYD5` because Wave101 parked both candidates for missing direct
  perturbation/model and genetic-anchor evidence.
- I treated public perturbation resources as the key decision layer, not broad
  expression recurrence.

Local checks:

- `SEL1L3` and `FXYD5` had `0` rows in Wave81 perturbation-first integrated,
  candidate-universe, Wave57, and Wave37 rescue tables.
- In the Wave37 GSE212008 CRISPR efferocytosis genome-wide table, both were
  present but null:
  - `SEL1L3`: `n_sgrna=4`, median efficient LFC `-0.153901`, median noneater
    LFC `-0.052048`, contrast LFC `-0.101853`, contrast FDR `1.0`,
    `UNRESOLVED`.
  - `FXYD5`: `n_sgrna=3`, median efficient LFC `-0.210025`, median noneater
    LFC `-0.159337`, contrast LFC `-0.217887`, contrast FDR `1.0`,
    `UNRESOLVED`.
- Wave57 intervention-first Geneformer had `0` rows for both candidates.
- Other Geneformer outputs contained sparse `SEL1L3` rows only; prior Wave18
  integration called them `model_only_no_real_perturbation_alignment` and
  `do_not_promote_from_foundation_model`. `FXYD5` had no local foundation-model
  support.

Public checks:

- Saved raw query outputs to
  `results_v3/wave102_sel1l3_fxyd5_perturbation_model_sidecar/`.
- NCBI GDS returned `0` perturbation datasets for `SEL1L3`, `FXYD5`, and
  dysadherin.
- LINCS Data Portal entity API returned `0` documents for both genes; SigCom
  LINCS returned HTTP `500` and is treated as unavailable rather than a
  biological negative.
- Perturb-seq/single-cell CRISPR searches returned no usable public dataset
  for either candidate.
- ChEMBL target search returned `0` exact targets for both genes.
- PubMed/Europe PMC found `FXYD5` perturbation literature, but it is mostly
  cancer, epithelial injury, chondrocyte/lung/heart inflammation, or diagnostic
  antibody work, not autoimmune disease-state rescue. `SEL1L3` hits are mostly
  bioinformatic marker papers.

Output:

- `subagents_v3/wave102_sel1l3_fxyd5_perturbation_model_sidecar.md`

Decision:

- `NO_REOPEN_SEL1L3_FXYD5_FROM_PERTURBATION_OR_MODEL_EVIDENCE`.
- This agrees with the residual and prior-art sidecars: close the
  `SEL1L3`/`FXYD5` accessible-survivor target branch unless genuinely new
  target-specific perturbation data appears.

## 2026-05-27 21:40 CEST

Integrated Wave102 `SEL1L3`/`FXYD5` convergence.

Inputs:

- Residual compartment test:
  `results_v3/wave102_accessible_survivor_residual_compartment_test/REPORT.md`
- Prior-art sidecar:
  `subagents_v3/wave102_sel1l3_fxyd5_prior_art_sidecar.md`
- Mechanism/modality sidecar:
  `subagents_v3/wave102_sel1l3_fxyd5_mechanism_modality_sidecar.md`
- Perturbation/model sidecar:
  `subagents_v3/wave102_sel1l3_fxyd5_perturbation_model_sidecar.md`

Output:

- `CONVERGENCE_CHECK_59.md`

Decision:

- All tracks reject therapeutic promotion.
- Close the accessible-survivor route for `SEL1L3` and `FXYD5`.
- Pivot next to intervention-first candidates where perturbation, model
  alignment, genetics, or druggability precede expression recurrence.

## 2026-05-27 21:50 CEST

Closed Wave103 intervention-first successor triage.

Output:

- `results_v3/wave103_intervention_first_successor_triage/REPORT.md`
- `CONVERGENCE_CHECK_60.md`

Decision:

- `NO_INTERVENTION_FIRST_SUCCESSOR_SURVIVES_ALL_GATES`.
- `CD9` and `DAB2` carry real local efferocytosis-screen biology, but both are
  wrong-direction or currently undruggable for therapeutic promotion.
- The next branch is genetics-first rather than expression-first or
  intervention-class-first: start from Wave62 target-resolved autoimmune loci,
  then intersect with lipid-lysosomal state evidence and only then audit
  modality and prior art.

## 2026-05-27 21:56 CEST

Ran Wave104 genetics-first lipid-state convergence audit.

Output:

- `scripts/v3_wave104_genetics_first_lipid_state_convergence_audit.py`
- `results_v3/wave104_genetics_first_lipid_state_convergence_audit/REPORT.md`

Local result:

- Branch call:
  `NO_PROMOTABLE_TARGET_BUT_DISPATCH_GENETICS_STATE_SIDECARS`.
- Call counts:
  - `NO_GO_NO_MS_GENETIC_ANCHOR`: 1913
  - `PARK_GENETICS_FIRST_NO_LIPID_STATE_CONVERGENCE`: 55
  - `PARK_GENETICS_STATE_DIRECTION_NO_MODALITY`: 1
  - `PARK_GENETICS_STATE_NEEDS_DIRECTION_OR_MODALITY`: 4
  - `PARK_MS_GENETICS_NARROW_OR_WEAK`: 55
- Sidecar set: `IFI30`, `IL7R`, `SP140`, `GALC`, `CD58`.

Interpretation:

- `SP140` remains the most interesting target-resolved genetics plus
  cross-disease state candidate, but modality and prior bromodomain/chromatin
  route concerns are unresolved.
- `IFI30` is more directly lipid/lysosomal but likely antigen-processing and
  host-defense blocked.
- `GALC` is mechanistically near sphingolipid/demyelination biology but lacks
  perturbation direction and has enzyme-deficiency safety constraints.
- `IL7R` and `CD58` are included as prior-art/control comparators rather than
  likely novel targets.

## 2026-05-27 22:01 CEST

Completed Wave104 genetics/colocalization sidecar.

Output:

- `subagents_v3/wave104_genetics_coloc_sidecar.md`

Result:

- No therapeutic `GO`.
- `IL7R` has the strongest broad target-resolved genetics, but remains
  `NO_GO` for V3 promotion because of CD127/IL7R prior art and mixed
  direction/cell mechanism.
- `SP140` remains a comparator/stratification axis; target resolution is real
  for MS/Crohn/psoriasis, but direction and prior art block promotion.
- `IFI30`, `GALC`, and `CD58` are parked as genetics benchmarks rather than
  target nominations.

## 2026-05-27 22:02 CEST

Ran Wave105 context decomposition for Wave104 sidecar genes.

Output:

- `scripts/v3_wave105_wave104_candidate_context_decomposition.py`
- `results_v3/wave105_wave104_candidate_context_decomposition/REPORT.md`

Result:

- `IFI30`: `PARK_STATE_SUPPORTED_BUT_ROUTE_BLOCKED`; broad positives in 3
  diseases, myeloid positives in 2, residual retention in 1 disease, and
  Wave91 nonresponse-high contexts = 4. The route remains antigen-processing /
  host-defense and druggability blocked.
- `SP140`: `PARK_STATE_SUPPORTED_BUT_ROUTE_BLOCKED`; broad positives in 4
  diseases, myeloid positives in 2, residual retention in 1 disease. The
  evidence is real but mostly Crohn myeloid residual signal plus target-resolved
  genetics, not yet causal intervention.
- `GALC`: `PARK_RAW_RECURRENCE_RESIDUAL_WEAK`; broad positives in 3 diseases
  but no residual retention.
- `IL7R` and `CD58`: calibration controls with known/prior-art immune-axis
  concerns.

## 2026-05-27 23:45 CEST

Resumed after interruption. The waiting/limit-reset gap is not counted as
active working time.

Reconciled accessible-survivor sidecar state:

- `subagents_v3/wave105_cd82_prior_art_sidecar.md` returned.
  - Call:
    `PARK_AS_NICHE_BIOMARKER_OR_MECHANISM_BRANCH_NO_GO_THERAPEUTIC_CD82`.
  - Direct CD82 therapeutic promotion is blocked by close colitis/NLRP3 prior
    art, RA synovial fibroblast prior art, and broader tetraspanin pleiotropy.
  - The narrow Wave104 claim, tissue-resident CD82 predicting matched myeloid
    lipid-lysosomal state across autoimmune tissues, was not found as directly
    published by the sidecar.
- `subagents_v3/wave101_accessible_survivor_prior_art_sidecar.md` returned.
  - Verdict: no Wave101 accessible-survivor candidate is promotable as a
    therapeutic target. `CD82`, `SEL1L3`, `APOC1`, and `LAPTM5` remain
    marker/readout/comparator nodes; `FXYD5` remains only a bounded wet-lab
    kill-test route.
- Kuhn Wave101 topology/modality sidecar did not return on a bounded wait and
  remains open.

Ran Wave105 CD82 niche robustness audit.

Output:

- `scripts/v3_wave105_cd82_niche_robustness_audit.py`
- `results_v3/wave105_cd82_niche_robustness_audit/REPORT.md`

First-pass bug/sanity issue:

- The initial M4 fully adjusted fixed models had too many covariates relative
  to n=12 and produced implausibly tiny residual-correlation p-values.
- I patched the script to require a stronger residual degrees-of-freedom buffer
  for fixed covariate models and to label saturated fits as underpowered rather
  than evidence.
- This was a concrete instance of the rule: if a result is too clean, suspect
  the model before believing biology.

Corrected result:

- Branch call: `REOPEN_CD82_ROBUST_NICHE_SIGNAL`.
- Model-grid rows: 168.
- Test contexts: 24.
- Robust positive contexts: 4.
- Robust positive diseases: 2.
- Robust negative contexts/diseases: 0.
- Robust contexts:
  - Crohn epithelial CD82 -> Crohn myeloid `lysosomal_apc`:
    M3 slope 1.211, p 0.00349, permutation p 0.001999,
    leave-one-out positive fraction 1.0.
  - Crohn epithelial CD82 -> Crohn myeloid `lipid_loader_repair`:
    M3 slope 0.641, p 0.0236, permutation p 0.0160,
    leave-one-out positive fraction 1.0.
  - Crohn epithelial CD82 -> Crohn myeloid `complement_phagocytosis`:
    M3 slope 1.055, p 0.0427, permutation p 0.0430,
    leave-one-out positive fraction 1.0.
  - Sjogren epithelial CD82 -> gland APC `lysosomal_apc`:
    M3 slope 0.426, p 0.0383, permutation p 0.0455,
    leave-one-out positive fraction 1.0.

Interpretation:

- CD82 survives as a cross-tissue niche-coupling mechanism/biomarker branch
  across Crohn and Sjogren.
- It does not satisfy therapeutic-target criteria because direct modulation is
  prior-art blocked and because the evidence remains matched-donor association,
  not causal perturbation.
- The next forcing question is whether any indirect, druggable intervention
  downstream/upstream of the CD82-associated niche coupling avoids the direct
  CD82 blockers.

## 2026-05-27 23:50 CEST

Integrated CD82 mechanism/modality sidecar.

Output:

- `subagents_v3/wave105_cd82_mechanism_modality_sidecar.md`

Result:

- Direct `CD82`: `NO_GO`.
- `CD82` as biomarker/stratifier: `PARK`.
- Indirect intervention candidates: `PARK`; no promotable `GO`.

Decision:

- Do not pursue CD82 as a target.
- Treat CD82 as a stress-test marker for tissue-to-myeloid coupling.
- Next local test: determine whether the Wave105 robust contexts survive
  stronger confounder/specificity adjustment or whether they collapse into
  generic epithelial inflammation, donor severity, or target APC activation.

## 2026-05-27 23:55 CEST

Integrated hostile methods review and ran Wave106 CD82 specificity/confounder
audit.

Sidecar:

- `subagents_v3/wave105_cd82_hostile_methods_review.md`

Hostile review conclusion:

- Downgrade `REOPEN_CD82_ROBUST_NICHE_SIGNAL`.
- Only one M3 context survives BH correction according to the sidecar.
- Crohn contributes three robust rows from the same 12 donors, so module rows
  are not disease-level replication.
- Underpowered M4 should not be counted as supportive.
- Residualization p-values are likely anti-conservative at small n.

Wave106 output:

- `scripts/v3_wave106_cd82_specificity_confounder_audit.py`
- `results_v3/wave106_cd82_specificity_confounder_audit/REPORT.md`

Wave106 result:

- Branch call: `CD82_SIGNAL_PARTLY_GENERIC_OR_CONTEXT_LIMITED`.
- Robust-specific contexts: 1.
- Robust-specific diseases: 1.
- Robust-generic contexts: 1.

Interpretation:

- Crohn epithelial-to-myeloid CD82 coupling is not specific: the same M3
  context has positive control modules `ifn_apc` and `hla_ii_apc`.
- Sjogren epithelial-to-APC has a nominal M3-specific `lysosomal_apc` signal,
  but under broader M7 context the primary signal is not positive and `ifn_apc`
  becomes positive.
- CD82 is downgraded to `CD82_PROVISIONAL_NICHE_BIOMARKER_SIGNAL_NOT_REOPENED`
  for therapeutic discovery.

Next action:

- Run a corrected multiplicity/disease-collapsed audit to formalize the
  downgrade and close the CD82 branch unless an independent indirect target
  emerges.

## 2026-05-28 00:02 CEST

Ran Wave107 CD82 multiplicity and disease-collapse audit.

Output:

- `scripts/v3_wave107_cd82_multiplicity_disease_collapse_audit.py`
- `results_v3/wave107_cd82_multiplicity_disease_collapse_audit/REPORT.md`

Result:

- Branch call:
  `CD82_PROVISIONAL_NICHE_BIOMARKER_SIGNAL_NOT_REOPENED`.
- Contexts:
  `24`.
- Disease/source-target units:
  `8`.
- Strict disease passes:
  `0`.
- Provisional disease passes:
  `1`.

Key details:

- Crohn epithelial-to-myeloid has strong module-combined evidence but is
  classified as `GENERIC_TARGET_ACTIVATION_COUPLING`; it is not specific to
  lipid-lysosomal biology.
- Sjogren epithelial-to-APC has one provisional disease-level pass, but no
  context-level BH-corrected permutation pass and no second disease.
- UC and psoriasis do not support the branch.

Decision:

- Close CD82 as a therapeutic-discovery branch.
- Retain CD82 only as a provisional ex vivo niche biomarker/readout.
- Pivot away from CD82 toward intervention-first candidates that can satisfy
  druggability and cross-disease specificity rather than marker-only coupling.

## 2026-05-28 00:18 CEST

Ran Wave108/Wave109 MFGE8-like local debris-opsonin safety-window modeling.

Motivation:

- MFGE8 was the most mechanistically aligned remaining repair/efferocytosis
  route because it has a tractable biologic/local-delivery modality.
- Prior Wave54 parked it because bystander phagocytosis risk was unresolved.
- This branch explicitly modeled that safety blocker rather than reopening
  MFGE8 from expression correlations.

Outputs:

- `scripts/v3_wave108_mfge8_debris_opsonin_safety_window_model.py`
- `results_v3/wave108_mfge8_debris_opsonin_safety_window_model/REPORT.md`
- `scripts/v3_wave109_mfge8_threshold_sensitivity_audit.py`
- `results_v3/wave109_mfge8_threshold_sensitivity_audit/REPORT.md`

Operational note:

- The Wave108 ODE uncertainty grid ran slower than expected but completed;
  no downscope was ultimately needed.
- A minor shell inspection command using `grep -P` failed because BSD grep
  lacks `-P`; this did not affect analysis outputs.

Wave108 result:

- Branch call:
  `MFGE8_LOCAL_OPSONIN_NO_THEORETICAL_SAFETY_WINDOW`.
- Grid points:
  `13200`.
- Safe grid points under strict criteria:
  `0`.
- Strict criterion was p10 debris-clearance gain >= 2.0, p90 viable loss <=
  5%, and p90 cytokine proxy <= 1.20.

Wave109 sensitivity result:

- Branch call:
  `MFGE8_MODEST_1_5X_WINDOW_ONLY`.
- Strict 2x / 5% / 1.20 points:
  `0`.
- Modest 1.5x / 5% / 1.20 points:
  `19`.
- Minimum selectivity for the 1.5x / 5% / 1.20 window:
  approximately `316x` debris-over-viable affinity.

Interpretation:

- MFGE8-like local opsonin is not promoted.
- The useful output is a quantitative wet-lab engineering constraint:
  a candidate must demonstrate very high debris-over-viable selectivity and a
  modest clearance benefit may be the realistic target.
- This does not satisfy V3 therapeutic DoD because it is simulation-only,
  lacks cross-disease target anchoring, and remains ex vivo/local-delivery
  constrained.

## 2026-05-28 00:35 CEST

Ran Wave110 route map and attempted Wave111 GPR183 spatial-proxy forcing test.

Wave110 outputs:

- `scripts/v3_wave110_post_closure_intervention_route_map.py`
- `results_v3/wave110_post_closure_intervention_route_map/REPORT.md`
- Sidecar: `subagents_v3/wave110_overlooked_intervention_route_scout.md`

Wave110 convergence:

- Local map and sidecar independently selected `GPR183/EBI2` as the next
  least-bad forcing test.
- Neither claimed a finding.

Wave111 outputs:

- `scripts/v3_wave111_gpr183_spatial_proxy_forcing_test.py`
- `results_v3/wave111_gpr183_spatial_proxy_forcing_test/REPORT.md`

Wave111 result:

- Branch call:
  `NO_REOPEN_GPR183_SPATIAL_PROXY`.
- Pairs:
  `0`.
- Tests:
  `0`.

Blocker:

- The donor-level gene-score table used by Wave102 was generated for the
  accessible-survivor candidate set, not for `GPR183` and oxysterol ligand-axis
  genes (`CH25H`, `CYP7B1`, `HSD3B7`, `CYP27A1`).
- Therefore the matched-donor spatial-proxy test cannot be run from the current
  precomputed donor-score table without rebuilding donor scores from h5ad.

Decision:

- Do not treat Wave111 as biological evidence.
- Run Wave112 as a weaker fallback using broad compartment-level h5ad contrasts
  already computed for the target genes.

## 2026-05-28 00:45 CEST

Ran Wave112 GPR183 compartment-contrast fallback.

Output:

- `scripts/v3_wave112_gpr183_compartment_contrast_fallback.py`
- `results_v3/wave112_gpr183_compartment_contrast_fallback/REPORT.md`

Result:

- Branch call:
  `NO_REOPEN_GPR183_COMPARTMENT_FALLBACK`.
- Coherent compartment disease count:
  `0`.
- `GPR183` response-support systems with p < 0.10:
  `2`.

Interpretation:

- The treatment-response signal exists in IBD and RA, but the receptor/ligand
  spatial-proxy requirement fails.
- UC has myeloid `GPR183` up nominally but no non-myeloid ligand-axis support.
- Crohn and T1D have ligand-axis signals but no myeloid receptor support.
- Psoriasis has negative myeloid `GPR183`.

Decision:

- Close GPR183/EBI2 locally.
- Rebuilding donor-level h5ad scores would be possible but is not justified
  by the weaker compartment fallback.

## 2026-05-28 00:55 CEST

Ran Wave113 PSAP recurrence/specificity audit.

Output:

- `scripts/v3_wave113_psap_recurrence_specificity_audit.py`
- `results_v3/wave113_psap_recurrence_specificity_audit/REPORT.md`

Sanity correction:

- First run incorrectly displayed the first CRISPR table row in the evidence
  table because the Wave37 gene column is `gene_symbol`, not `gene`.
- Patched and reran before integration.

Corrected result:

- Branch call:
  `NO_REOPEN_PSAP_WEAK_SINGLE_CONTEXT_MARKER`.
- Positive disease count at p < 0.10:
  `1`.
- Myeloid positive disease count at p < 0.10:
  `0`.
- Negative disease count at p < 0.10:
  `2`.
- MS nominal positive:
  `true`.
- Geneformer strong support:
  `false`.
- CRISPR/efferocytosis support:
  `false`.

Decision:

- Close PSAP locally.
- Nominal MS support and weak foundation-model support do not overcome absent
  cross-disease/myeloid recurrence and unresolved perturbation evidence.

## 2026-05-28 06:41 CEST

Ran Wave114 P2RX7 target-level closure audit after interruption/resume.

Output:

- `scripts/v3_wave114_p2rx7_target_level_closure_audit.py`
- `results_v3/wave114_p2rx7_target_level_closure_audit/REPORT.md`
- `results_v3/wave114_p2rx7_target_level_closure_audit/summary.json`
- `results_v3/wave114_p2rx7_target_level_closure_audit/p2rx7_closure_evidence.tsv`

Execution note:

- System `python3` compiled the script but could not run the analysis because
  pandas was absent.
- Reran in the pinned V3 environment:
  `./.venv_v3_py312/bin/python`.

Result:

- Branch call:
  `NO_REOPEN_P2RX7_TARGET_LEVEL_STRATIFICATION`.
- Specificity-pass context count:
  `0`.
- MS module support:
  `false`.
- RA response discrimination:
  `false`.
- IBD response discrimination:
  `false`.
- CRISPR/efferocytosis support:
  `false`.

Decision:

- Close P2RX7 locally as a therapeutic-discovery branch.
- The remaining defensible use is as a prior-art-rich comparator for
  purine/inflammasome stratification, not as a V3 intervention point.

## 2026-05-28 06:50 CEST

Ran Wave115 SPNS1 controller falsification audit.

Output:

- `scripts/v3_wave115_spns1_controller_falsification_audit.py`
- `results_v3/wave115_spns1_controller_falsification_audit/REPORT.md`
- `results_v3/wave115_spns1_controller_falsification_audit/summary.json`
- `results_v3/wave115_spns1_controller_falsification_audit/spns1_case_only_partial_controller_tests.tsv`
- `results_v3/wave115_spns1_controller_falsification_audit/spns1_controller_disease_summary.tsv`
- `results_v3/wave115_spns1_controller_falsification_audit/spns1_external_gate_evidence.tsv`

Result:

- Branch call:
  `NO_REOPEN_SPNS1_CONTROLLER_ROUTE`.
- Controller-pass diseases:
  `0`.
- Myeloid pass contexts:
  `0`.
- MS anchor:
  `false`.
- Response support:
  `false`.
- CRISPR support:
  `false`.
- Target-resolution support:
  `false`.
- Modality ready:
  `false`.

Interpretation:

- The only strong controller-like signal is Sjogren salivary epithelial
  `SPNS1` versus lysosomal/APC score; it is not a myeloid/APC disease pass.
- RA blood myeloid has a weak lipid-loader trend but fails effect and FDR
  thresholds.
- This supports SPNS1 as a tissue/lysosomal biology readout, not an upstream
  cross-autoimmune myeloid controller.

Decision:

- Close SPNS1 locally for V3 therapeutic discovery.
- Re-rank remaining route classes instead of continuing target-by-target along
  the already-demoted accessible shortlist.

## 2026-05-28 07:02 CEST

Ran Wave116 closure-aware route rerank.

Output:

- `scripts/v3_wave116_closure_aware_route_rerank.py`
- `results_v3/wave116_closure_aware_route_rerank/REPORT.md`
- `results_v3/wave116_closure_aware_route_rerank/summary.json`
- `results_v3/wave116_closure_aware_route_rerank/closure_aware_route_universe.tsv`

Result:

- Branch call:
  `ROUTE_AVAILABLE_FOR_FORCING_TEST`.
- Routes in universe:
  `257`.
- Open routes after local closure penalties:
  `223`.
- Actionable non-`NO_GO` routes:
  `132`.
- Selected next route:
  `PARK7` from Wave110.

Decision:

- Do not select the top raw rerank row, `eicosanoid_receptors`, because it is
  explicitly a `NO_GO` intervention class.
- Force-test `PARK7` as a stress-route candidate; require MS anchor, myeloid
  recurrence, residual evidence beyond generic stress, response or perturbation
  support, and target-resolution genetics.

## 2026-05-28 07:06 CEST

Ran Wave117 PARK7/DJ-1 stress-route forcing test.

Output:

- `scripts/v3_wave117_park7_stress_route_forcing_test.py`
- `results_v3/wave117_park7_stress_route_forcing_test/REPORT.md`
- `results_v3/wave117_park7_stress_route_forcing_test/summary.json`
- `results_v3/wave117_park7_stress_route_forcing_test/park7_gate_evidence.tsv`
- `results_v3/wave117_park7_stress_route_forcing_test/park7_broad_contexts.tsv`
- `results_v3/wave117_park7_stress_route_forcing_test/park7_broad_disease_summary.tsv`

Result:

- Branch call:
  `NO_REOPEN_PARK7_GENERIC_STRESS_ROUTE`.
- MS anchor:
  `false`.
- Broad myeloid-positive diseases:
  `2`.
- Generic-covariate residual diseases:
  `0`.
- Foundation strong support:
  `false`.
- IBD/Wave68 response support:
  `false` / `false`.
- Target-resolution support:
  `false`.
- CRISPR/efferocytosis support:
  `false`.
- Generic-stress-like:
  `true`.

Decision:

- Close PARK7 locally.
- It remains a stress biology/readout comparator, not a V3 intervention route.

## 2026-05-28 07:16 CEST

Ran Wave118 DAB2/CD9 efferocytosis directionality audit.

Output:

- `scripts/v3_wave118_dab2_cd9_efferocytosis_directionality_audit.py`
- `results_v3/wave118_dab2_cd9_efferocytosis_directionality_audit/REPORT.md`
- `results_v3/wave118_dab2_cd9_efferocytosis_directionality_audit/summary.json`
- `results_v3/wave118_dab2_cd9_efferocytosis_directionality_audit/dab2_cd9_directionality_decisions.tsv`
- `results_v3/wave118_dab2_cd9_efferocytosis_directionality_audit/dab2_cd9_evidence_rows.tsv`

Result:

- Branch call:
  `NO_REOPEN_DAB2_CD9_EFFEROCYTOSIS_ROUTE`.
- `DAB2`: MS nominal true but FDR false; broad positive diseases `0`;
  broad negative diseases `3`; CRISPR nominal true but FDR false; no response,
  genetics, or modality; Wave71 blocked.
- `CD9`: MS nominal true but FDR false; broad positive diseases `0`;
  broad negative diseases `2`; CRISPR nominal true but FDR false; no response,
  genetics, or modality; Wave71 blocked.

Decision:

- Close DAB2 and CD9 locally as V3 intervention routes.
- Keep them only as weak efferocytosis assay comparators.

## 2026-05-28 07:24 CEST

Prefiltered BLK after closure-aware rerank selected it.

Evidence inspected:

- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_ms_rows.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_broad_summary.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_ibd_response_summary.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`

Result:

- No MS row in Wave81 MS evidence.
- Wave37 nominal efferocytosis call is not FDR-supported:
  efficient FDR `0.822`, contrast FDR `0.997`.
- Broad support is single-disease only: Sjogren syndrome.
- IBD response support is absent.
- Wave62 target resolution remains `NO_GO_WAVE62_TARGET_RESOLUTION` despite
  RA/SLE genetics; no MS target-resolution support.

Decision:

- Close BLK by prefilter.
- Add BLK to the closure-aware route penalties rather than building another
  target-specific closure script.

## 2026-05-28 07:30 CEST

Prefiltered LRRC61 after closure-aware rerank selected it.

Evidence inspected:

- `results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_ms_rows.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_broad_summary.tsv`
- `results_v3/wave81_perturbation_first_rescue/perturbation_first_ibd_response_summary.tsv`

Result:

- Broad nominal recurrence is present in four diseases.
- MS anchor is absent: p `0.582`, FDR `0.946`.
- Wave37 screen row has only two sgRNAs and no Wilcoxon/FDR values.
- IBD response support is absent after FDR.
- No genetics or target-resolution support.
- No modality channel.

Decision:

- Close LRRC61 by prefilter.
- Broad expression recurrence without MS/genetics/response/modality is not
  enough for V3 therapeutic discovery.

## 2026-05-28 07:36 CEST

Ran Wave119 batch prefilter for remaining Wave110 survivors.

Output:

- `scripts/v3_wave119_wave110_remaining_survivor_prefilter.py`
- `results_v3/wave119_wave110_remaining_survivor_prefilter/REPORT.md`
- `results_v3/wave119_wave110_remaining_survivor_prefilter/summary.json`
- `results_v3/wave119_wave110_remaining_survivor_prefilter/remaining_wave110_prefilter_decisions.tsv`
- `results_v3/wave119_wave110_remaining_survivor_prefilter/remaining_wave110_prefilter_evidence.tsv`

Result:

- Branch call:
  `NO_REMAINING_WAVE110_SURVIVOR_AFTER_PREFILTER`.
- Candidates tested:
  `14`.
- Candidates parked for targeted forcing:
  `0`.
- Tested genes:
  `CLEC7A`, `FAM49B`, `LYN`, `CCDC121`, `CHST11`, `FBXO16`, `RECQL4`,
  `EFR3A`, `IGLON5`, `MAN1A2`, `MREG`, `PLIN4`, `SLC39A3`, `YWHAE`.

Decision:

- Add these genes to closure-aware route penalties.
- This closes the current low-quality Wave110 perturbation-first tail.
## 2026-05-28 08:05 CEST - Wave120 EPHX2/sEH target-PD coherence closure

I formalized the EPHX2/sEH branch because McClintock correctly identified it
as the only obvious small-molecule pharmacology handle left among the nearby
routes. The critical question was not whether sEH biology is interesting, but
whether the local V3 evidence connects target-level EPHX2, paired
epoxy-fatty-acid/diol pharmacodynamics, cross-disease specificity, treatment
response, and prior-art freedom.

Script:

- `scripts/v3_wave120_ephx2_target_pd_coherence_closure.py`

Outputs:

- `results_v3/wave120_ephx2_target_pd_coherence_closure/summary.json`
- `results_v3/wave120_ephx2_target_pd_coherence_closure/ephx2_target_pd_gates.tsv`
- `results_v3/wave120_ephx2_target_pd_coherence_closure/REPORT.md`

Result:

- Branch call: `NO_REOPEN_EPHX2_TARGET_PD_COHERENCE`.
- Gate pass count: 0/6.
- Direct paired epoxide/diol ratio evidence: absent (`direct_epoxide_diol_pairs=0`;
  `direct_ratio_supportive_tests=0`).
- Target-level EPHX2 support: absent.
- Specificity over generic lipid/inflammatory/lysosomal comparators: absent.
- Independent response replication: absent.
- Cross-disease specific biochemistry: insufficient.
- Prior-art freedom: failed because the Wave74c sidecar marked broad sEH
  autoimmune repurposing as `BLOCKED_BY_PRIOR_ART`.

Interpretation:

- EPHX2/sEH remains a plausible biology topic, but not a promotable V3
  therapeutic finding under the current strict target-PD standard.
- I added `EPHX2` to the Wave116 closure-aware rerank terms to prevent route
  recycling.

## 2026-05-28 08:16 CEST - Wave116 rerank selected ABTB2; closed as orchestration artifact

After adding the Wave119 and Wave120 closures, Wave116 selected `ABTB2` from
the Wave110 perturbation-first route map. I inspected the underlying evidence
instead of launching an individual forcing script.

Observed evidence:

- Wave81 call: `PARK_PERTURBATION_FIRST_CANDIDATE`.
- Wave37 signal: `KO_ENHANCES_EFFEROCYTOSIS_NEGATIVE_REGULATOR`, but with
  `efficient_fdr=0.9601`, `contrast_fdr=0.9200`, and only four sgRNAs.
- MS white-matter anchor: absent (`delta_log2=-0.1477`, `p=0.8826`,
  `fdr=0.9840`).
- Genetics or target resolution: absent.
- IBD response support: absent (`raw_p=0.3587`, `fdr=1.0`).
- Modality channel: absent.
- Wave71 global survivor call: `NO_REOPEN_INSUFFICIENT_CONVERGENCE`.
- Wave110 had no concrete next test for ABTB2.

Decision:

- Close ABTB2 without a dedicated wave.
- Patch Wave116 so actionable route selection requires
  `has_concrete_next_test=True`, preventing low-score PARK artifacts from being
  promoted when they lack an executable forcing test.

## 2026-05-28 08:26 CEST - Wave116 selected CD44; parser bug fixed

The stricter Wave116 rerank selected `CD44` from Wave91 with score 0.5. This
was not a biological promotion. It exposed a parser bug: Wave91 uses
`wave91_call`, `route_blocker`, and `module_intervention_score`, but Wave116 was
looking for generic `call`, `decision`, `score`, and `rank_score` fields.

Underlying CD44 evidence from Wave91:

- `wave91_call=NO_GO_ROUTE_BLOCKED`.
- `route_blocker=NO_GO_ADHESION_MATRIX_PRIOR_ART_AND_BROAD_BIOLOGY`.
- MS white matter is nominal only (`delta_log2=1.3447`, `p=0.0332`,
  `fdr=0.8507`).
- Wave62 target resolution: `NO_GO_WAVE62_TARGET_RESOLUTION`.
- Direct h5ad positives are mostly IBD epithelial/myeloid contexts, with no
  FDR10 disease-level recurrence.
- CD44/SPP1 had already been demoted in earlier scouts for broad adhesion,
  matrix, repair, trafficking, oncology, and autoimmune prior art.

Decision:

- Add `CD44` and `SPP1` to closure terms.
- Patch Wave116 to parse Wave91-specific columns correctly.

## 2026-05-28 08:36 CEST - Wave116 selected HLA-DPB1; no-go text filter fixed

After the Wave91 parser fix, Wave116 selected `HLA-DPB1`. Inspection showed
this was another reranker hygiene issue rather than a viable intervention
route.

Evidence:

- Top actionable Wave91 rows were HLA class-II genes with
  `PARK_RESPONSE_DIRECTIONS_WEAK_OR_UNDERPOWERED`.
- `HLA-DPB1` and `HLA-DPA1` had `recommended_next_test=UNSPECIFIED_ROUTE_NOT_AUDITED`.
- `HLA-DRA` had `recommended_next_test=NO_GO_BROAD_MHC_CLASS_II`.
- The HLA-II antigen-presentation axis has repeatedly failed the intervention
  standard because broad MHC-II suppression is not selective and carries
  host-defense and immune-competence liabilities.

Decision:

- Add `HLA-DPA1`, `HLA-DPB1`, and `HLA-DRA` to closure terms.
- Patch Wave116 so `recommended_next_test` text containing `NO_GO`, `BLOCKED`,
  `NOT_V3`, or `UNSPECIFIED` contributes to `no_go_source`.

## 2026-05-28 08:50 CEST - Wave121 final wet-lab-only route closure

After Wave116 cleanup, only two actionable rows remained:

- `FPR2_ANXA1_BIASED_RESOLUTION`
- `CD300_RECEPTOR_SPECIFIC_TUNING`

Both came from Wave95 and were explicitly `PARK_WETLAB_KILL_TEST_ONLY`, so I
created `scripts/v3_wave121_final_wetlab_only_route_closure.py` to decide
whether either route could be computationally deepened.

Outputs:

- `results_v3/wave121_final_wetlab_only_route_closure/summary.json`
- `results_v3/wave121_final_wetlab_only_route_closure/wetlab_only_route_decisions.tsv`
- `results_v3/wave121_final_wetlab_only_route_closure/REPORT.md`

Result:

- Branch call: `NO_OPEN_ROUTE_AFTER_WETLAB_ONLY_AUDIT`.
- `FPR2_ANXA1_BIASED_RESOLUTION`: 2/10 gates passed.
- `CD300_RECEPTOR_SPECIFIC_TUNING`: 2/10 gates passed.
- Both failed MS anchor/trend, cross-disease residual support,
  cell-resolved response/transition support, target-resolved genetics, broad
  genetics, real perturbation or validated model support, prior-art freedom, and
  direction safety.

Decision:

- Close both routes for V3 computational promotion.
- Keep them only as possible future wet-lab assay comparators if new
  receptor-specific perturbation data become available.
- Add `FPR2`, `ANXA1`, `FPR2_ANXA1_BIASED_RESOLUTION`, `CD300`, and
  `CD300_RECEPTOR_SPECIFIC_TUNING` to Wave116 closure terms.

## 2026-05-28 08:59 CEST - Wave116 fallback bug fixed

After Wave121 closures, a manual inspection of Wave116 output showed
`n_actionable_routes=0`, but `summary.json` still reported
`ROUTE_AVAILABLE_FOR_FORCING_TEST` and selected `eicosanoid_receptors`.

Cause:

- Wave116 selected from `top_open` when `actionable_routes` was empty.
- `top_open` can contain `NO_GO` rows, so the fallback contradicted the stricter
  actionable definition.

Decision:

- Remove the fallback. If `actionable_routes` is empty, Wave116 must report
  `NO_OPEN_ROUTE_AFTER_CLOSURE_RERANK`.

## 2026-05-28 09:04 CEST - Wave116 branch closure confirmed

After the fallback fix, Wave116 reported:

- Branch call: `NO_OPEN_ROUTE_AFTER_CLOSURE_RERANK`.
- `n_actionable_routes=0`.
- `selected_candidate=""`.

Interpretation:

- The post-closure survivor-map branch is exhausted under the current strict
  criteria.
- This does not satisfy session exhaustion. It only closes one route-selection
  family.

Next action:

- Pivot away from Wave110/Wave91/Wave95 survivor recycling.
- Start a fresh breadth-first target-class scan using existing cross-disease
  data products and the closure ledger as exclusions.

## 2026-05-28 09:12 CEST - Boyle sidecar returned; Wave122 fresh scan completed

Boyle returned a read-only advisory list of the least-bad fresh routes:

- `NRCAM`
- `CD200` / `CD200R`
- `MERTK` / TAM agonist-restoration
- `CHI3L1`
- `LIPA`

Boyle's top-line call was that no route survives V3 promotion gates from local
artifacts.

I ran `scripts/v3_wave122_fresh_breadth_target_scan.py` as an independent local
scan over 32,096 genes from the local evidence products.

Wave122 result:

- Branch call: `NO_FRESH_ROUTE_FROM_LOCAL_SCAN`.
- `n_testable=0`.
- `n_park=0`.
- Top gene by score: `NCF2`, but with blocker text:
  `NO_REOPEN_BLOCKED_BRANCH NOX2 host-defense/CGD directionality risk
  NO_GO_WAVE62_TARGET_RESOLUTION`.

Boyle's five suggestions in Wave122:

- `CHI3L1`: two support channels, nominal MS and broad state support, but no
  response/genetics/perturbation/modality.
- `NRCAM`: one support channel, no MS nominal support.
- `CD200`: one support channel, no MS nominal support.
- `LIPA`: one support channel plus blocker.
- `MERTK`: one response channel plus blocker, no MS/broad support.

Decision:

- Convert Boyle's advisory suggestions into an explicit kill audit rather than
  reopening them by narrative plausibility.

## 2026-05-28 09:20 CEST - Wave123 sidecar candidate kill audit

Script:

- `scripts/v3_wave123_sidecar_candidate_kill_audit.py`

Outputs:

- `results_v3/wave123_sidecar_candidate_kill_audit/summary.json`
- `results_v3/wave123_sidecar_candidate_kill_audit/sidecar_candidate_kill_decisions.tsv`
- `results_v3/wave123_sidecar_candidate_kill_audit/REPORT.md`

Result:

- Branch call: `NO_REOPEN_ANY_SIDECAR_CANDIDATE`.
- `NRCAM`: 2/9 gates, no MS nominal/FDR support, no controller support.
- `CD200`: 2/9 gates, no MS nominal/FDR support, no controller support.
- `MERTK`: 1/9 gates, blocker present, no MS/broad/perturbation support.
- `CHI3L1`: 2/9 gates, nominal MS plus broad state only; fails controller,
  perturbation, genetics, modality, and blocker gates.
- `LIPA`: 1/9 gates, blocker present, no MS/perturbation support.

Decision:

- Do not reopen any Boyle candidate as a V3 finding route.
- Next audit Wave122 top-ranked `NCF2` because it has four support channels but
  serious NOX2 host-defense/CGD safety and target-resolution blockers.

## 2026-05-28 09:32 CEST - Wave124 NCF2/NOX2 strict closure

Script:

- `scripts/v3_wave124_ncf2_nox2_strict_closure_audit.py`

Outputs:

- `results_v3/wave124_ncf2_nox2_strict_closure_audit/summary.json`
- `results_v3/wave124_ncf2_nox2_strict_closure_audit/ncf2_nox2_strict_gates.tsv`
- `results_v3/wave124_ncf2_nox2_strict_closure_audit/REPORT.md`

Result:

- Branch call: `NO_REOPEN_NCF2_NOX2_ROUTE`.
- Gate pass count: 1/11.
- Passed only `ms_nominal_support`.
- Failed MS FDR support, cross-disease cell-state support, treatment-response
  FDR support, target-resolution, MS target genetics, real perturbation,
  strong foundation support, host-defense/direction safety, selective
  druggability, and previous-closure gate.

Interpretation:

- NCF2 remains a useful ROS-linked myeloid state marker/comparator.
- It is not a V3 therapeutic intervention point because the NOX2 branch is
  directionally unsafe and not selectively druggable in the required sense.

Next action:

- Build a mechanism-class failure map from Wave122 top candidates to identify a
  pivot that is not just another marker-only gene.

## 2026-05-28 09:42 CEST - Wave125 mechanism-class failure map

Script:

- `scripts/v3_wave125_mechanism_class_failure_map.py`

Outputs:

- `results_v3/wave125_mechanism_class_failure_map/summary.json`
- `results_v3/wave125_mechanism_class_failure_map/failure_mode_summary.tsv`
- `results_v3/wave125_mechanism_class_failure_map/mechanism_class_failure_summary.tsv`
- `results_v3/wave125_mechanism_class_failure_map/pivot_recommendations.tsv`

Result:

- Branch call: `MECHANISM_FAILURE_MAP_COMPLETE`.
- Dominant failure mode among top 300 Wave122 candidates:
  `failure_response_absent` in 297/300.
- `failure_no_modality`: 280/300.
- `failure_no_causal_channel`: 274/300.
- `failure_ms_not_fdr`: 139/300.
- Top mechanism class by score: `ros_host_defense`, driven by NCF2 and already
  closed.

Interpretation:

- More expression ranking will mostly recycle marker genes.
- The constructive pivot is upstream druggable regulator search for recurring
  marker classes, especially secreted remodeling and lysosomal/protease-like
  classes.

## 2026-05-28 09:50 CEST - Wave126 L1000 upstream regulator reopener

Script:

- `scripts/v3_wave126_l1000_upstream_regulator_reopener.py`

Outputs:

- `results_v3/wave126_l1000_upstream_regulator_reopener/summary.json`
- `results_v3/wave126_l1000_upstream_regulator_reopener/l1000_upstream_regulator_decisions.tsv`
- `results_v3/wave126_l1000_upstream_regulator_reopener/REPORT.md`

Result:

- Branch call: `NO_L1000_UPSTREAM_REOPENER`.
- Compounds tested: 123.
- Reopened compounds: 0.

Closest rows:

- Several recurrent hits have unknown target/MOA and cannot support target
  nomination without deconvolution.
- `LRRK2`, `MKNK1`, `FAAH`, `MMP13`, and `CNR1` are mechanistically interesting
  but single-query and/or already fail promotion gates.
- Known recurrent hits are dominated by cytotoxic, steroid, HSP, cell-cycle,
  protease, or generic immune/prior-art mechanisms.

Next action:

- Check whether the highest-scoring unknown L1000 hits can be resolved from
  local LINCS metadata. If not, decide whether targeted external lookup is worth
  a bounded network call.

## 2026-05-28 10:00 CEST - Wave127 external spot-check for recurrent unknown L1000 hits

I checked the highest-scoring recurrent unknown L1000 hits rather than leaving
the branch with an unresolved loophole.

Artifact:

- `literature_v3/wave127_external_l1000_unknown_lookup.md`

Queries:

- `"BFOWTYGBWYCXKR"`
- `"GNLIZSFOCYRQDY" "BRD-K35024477"`
- `"BRD-K05197617"`
- `"BRD-K35024477"`

Findings:

- `BRD-K05197617` has external L1000FWD-derived annotations as an EGFR
  inhibitor. That does not reopen the route; it moves the compound into a broad
  oncology/growth-factor target bucket, not a selective autoimmune
  lipid-lysosomal myeloid intervention.
- `BRD-K35024477` appears in an OCTAD compound-cluster PDF, but I found no clear
  target or autoimmune-relevant mechanism.

Decision:

- Close the recurrent unknown L1000 branch for now.

## 2026-05-28 10:12 CEST - Wave128 genetics-first reopener

Script:

- `scripts/v3_wave128_genetics_first_reopener.py`

Outputs:

- `results_v3/wave128_genetics_first_reopener/summary.json`
- `results_v3/wave128_genetics_first_reopener/genetics_first_reopener_decisions.tsv`
- `results_v3/wave128_genetics_first_reopener/REPORT.md`

Result:

- Branch call: `NO_GENETICS_FIRST_REOPENER`.
- Candidates tested: 195.
- Reopened candidates: 0.

Top rows:

- `SP140`: 8/11 gates, but fails local MS nominal support, residual support, and
  druggability/modality. Already closed as genetics-positive,
  direction-conflicted, prior-art/chemistry-limited comparator.
- `IL7R`: 7/11 gates, fails local MS, residual support, perturbation/model, and
  modality.
- `PRDM1`, `CCL20`, `GALC`, `CXCR2`: 7/11 gates but fail critical MS,
  residual, druggability, or target-resolution gates.

Decision:

- Do not reopen genetics-first target nomination.
- Next pivot to response/stratification as a separate translational angle, while
  keeping it distinct from a therapeutic target claim.

## 2026-05-28 10:24 CEST - Wave129 response/stratification salvage

Script:

- `scripts/v3_wave129_response_stratification_salvage.py`

Outputs:

- `results_v3/wave129_response_stratification_salvage/summary.json`
- `results_v3/wave129_response_stratification_salvage/response_stratification_salvage_decisions.tsv`
- `results_v3/wave129_response_stratification_salvage/REPORT.md`

Result:

- Branch call: `BIOMARKER_ONLY_SIGNAL_EXISTS`.
- Biomarker candidates: 2.
- Target nomination candidates: 0.

Biomarker-only rows:

- `IL1B`: anti-TNF nonresponse marker, cross-system IBD/RA replication, AUC
  0.897, |g| 1.69, but closed/prior target and no MS context trend.
- `LAMP3`: anti-TNF nonresponse marker, cross-system IBD/RA replication, AUC
  0.759, |g| 1.10, but closed marker and no MS context trend.

Decision:

- Preserve IL1B/LAMP3 as biomarker-only response-state information.
- Do not convert this into a V3 therapeutic target claim.
- Check whether an MS treatment-response dataset exists locally; otherwise this
  branch cannot meet the MS-centered V3 bar.

## 2026-05-28 07:31 CEST - Resume and Wave130 MS treatment response

Resumed after interruption. User clarified interrupted/waiting time does not
count toward the 12-hour work floor.

Subagent state:

- Spawned Huygens for read-only inspection of local MS treatment-response
  datasets in `data/raw_v3/wave96_ms_treatment`.
- Spawned Gibbs for read-only fresh-route audit after Wave129.
- Both subagents completed and were closed after integration.

Wave130 implemented and completed:

- Script: `scripts/v3_wave130_ms_treatment_response_audit.py`
- Output: `results_v3/wave130_ms_treatment_response_audit/`
- Runner updated: `run_v3_analysis.sh`

Important debugging:

- First run failed at report rendering because pandas `to_markdown` requires
  optional `tabulate`; replaced with an internal Markdown table formatter.
- Initial GSE235357 metadata parser misclassified misspelled `Helathy donor 2`
  as MS. Fixed donor detection.
- Initial GSE250453 parser failed to pair `Res4_treat` with `R_basal_4`.
  Replaced patient parsing with explicit regex normalization.

Corrected branch call:

- `GENERIC_IFN_APC_SIGNAL_ONLY_NO_LIPID_LYSOSOMAL_RESCUE`

Key corrected results:

- GSE235357 DMF PBMC RNA-seq: 5 responders and 5 nonresponders with paired
  baseline/12-month samples.
- GSE250453 fingolimod PBMC RNA-seq: 5 responders and 5 nonresponders with
  paired baseline/treated samples.
- Primary Wave129 genes did not replicate in MS:
  - `IL1B`: `NO_CROSS_MS_REPLICATION`
  - `LAMP3`: `NO_CROSS_MS_REPLICATION`
- Lipid/lysosomal modules did not replicate:
  - `lysosomal_apc`: `NO_CROSS_MS_REPLICATION`
  - `lipid_loader_repair`: `NO_CROSS_MS_REPLICATION`
- Only `ifn_apc` showed a small-n cross-dataset directional signal:
  baseline mean Hedges g responder-minus-nonresponder = -0.9547,
  best baseline p = 0.03875. This is a generic IFN/APC state and not a
  lipid-lysosomal therapeutic target rescue.

Decision:

- Do not promote Wave129 IL1B/LAMP3 or lipid-lysosomal response
  stratification into a V3 finding.
- Treat the generic IFN/APC result as context only because it is broad,
  prior-art-heavy, and not a selective intervention point.
- Next pivot: class-level forcing tests from Gibbs sidecar, prioritizing
  eicosanoid/LTA4H-adjacent and retinoid/VDR/RXR classes because they are
  non-expression-only and potentially druggable, while expecting prior-art and
  directionality blockers.

## 2026-05-28 07:31 CEST - Wave131 class-route forcing

Wave131 implemented and completed:

- Script: `scripts/v3_wave131_class_route_forcing_audit.py`
- Output: `results_v3/wave131_class_route_forcing_audit/`
- Runner updated: `run_v3_analysis.sh`

Branch call:

- `NO_CLASS_ROUTE_REOPENED_AFTER_WAVE130`

Classes tested:

- `eicosanoid_receptors`: 4/8 gates. Fails target-resolution genetics,
  prior-art freedom, direction/safety, and specificity.
- `retinoid_vdr_rxr`: 3/8 gates. Fails target-resolution genetics, direct
  perturbation/response, prior-art freedom, direction/safety, and specificity.
- `MED16_MEDIATOR_MODULE`: 4/8 gates. Real perturbation support remains, but
  lacks cross-disease cell-state support, MS anchor, target-resolution genetics,
  and safe direction.
- `GALC_LYSOSOMAL_SPHINGOLIPID`: 4/8 gates. Has a genetics row but fails MS
  anchor, direct perturbation/response, prior-art freedom, and direction/safety.

Decision:

- Do not reopen Gibbs' least-bad class routes.
- Continue with remaining Wave83 parked route logic, especially GPR183, because
  it was the only intervention class parked rather than outright no-go in
  Wave83, while checking later Wave111/Wave112 closure evidence.

## 2026-05-28 07:31 CEST - Wave132 GPR183 closure

Wave132 implemented and completed:

- Script: `scripts/v3_wave132_gpr183_post_wave130_closure.py`
- Output: `results_v3/wave132_gpr183_post_wave130_closure/`
- Runner updated: `run_v3_analysis.sh`

Branch call:

- `NO_REOPEN_GPR183_AFTER_POST_WAVE130_AUDIT`

Evidence:

- Wave83 parked `GPR183_EBI2_OXYSTEROL_NICHE` for forcing.
- Wave111: `NO_REOPEN_GPR183_SPATIAL_PROXY`; no matched-donor spatial-proxy
  rows.
- Wave112: `NO_REOPEN_GPR183_COMPARTMENT_FALLBACK`; zero coherent compartment
  diseases.
- Wave130: no lipid-lysosomal MS treatment-response rescue.

Decision:

- Close GPR183 as a post-Wave130 route.
- With Wave131 and Wave132, the sidecar and Wave83 parked intervention-class
  branches do not currently produce a V3 therapeutic nomination.

## 2026-05-28 07:51 CEST - Wave133/Wave134 interruption recovery and strict DAP audit

Subagent state:

- No active subagents remain after recovery from interruption.
- Huygens, Gibbs, and Plato are closed.

Hostile critique integration:

- Accepted that Wave122 had two hygiene failures: wrong Wave55 path and
  substring closure matching.
- Accepted that Wave128 substring closure matching also needed correction.
- Accepted that Wave130 is a peripheral small-n treatment-response audit and
  cannot by itself close compartment-specific CNS biology.

Wave133 implemented and completed:

- Script: `scripts/v3_wave133_closure_hygiene_correction.py`
- Output: `results_v3/wave133_closure_hygiene_correction/`
- Branch call: `HYGIENE_CORRECTION_REOPENS_ROUTE`
- Corrected Wave122 testable routes: 1 (`DAP`)
- Corrected Wave122 exact-closure restorations: 22 genes, all remaining
  `NO_GO_FRESH_SCAN`
- Corrected Wave128 reopened routes: 0

Immediate concern:

- `DAP` was reopened mechanically because inherited blocker detection did not
  treat `NO_REOPEN_INSUFFICIENT_CONVERGENCE` as a strict blocker.
- The Wave133 row itself reports no perturbation/model support and no modality.

Wave134 implemented and completed:

- Script: `scripts/v3_wave134_dap_strict_reopen_audit.py`
- Output: `results_v3/wave134_dap_strict_reopen_audit/`
- Branch call: `NO_REOPEN_DAP_HYGIENE_ARTIFACT`

Wave134 critical failures:

- `ms_fdr_expression`
- `ms_genetic_anchor`
- `target_resolved_coloc_or_l2g`
- `direct_real_perturbation_support`
- `foundation_model_not_contradicted`
- `reachable_selective_modality`
- `directionality_defined`
- `no_strict_blocker`

Decision:

- DAP remains closed as a nonspecific death/autophagy/ribosome-stress marker.
- The hygiene correction was necessary, but it does not create a therapeutic
  target claim.
- Continue with critique-mandated sensitivity tests around lipid-metabolite
  flux and GPR183 ligand-axis scoring.

## 2026-05-28 07:51 CEST - Wave135 lipid-flux MS response sensitivity

Wave135 implemented and completed:

- Script: `scripts/v3_wave135_lipid_flux_ms_response_sensitivity.py`
- Output: `results_v3/wave135_lipid_flux_ms_response_sensitivity/`
- Branch call: `LIPID_FLUX_MS_SMALL_N_SIGNAL_NOT_PROMOTABLE`

Tested:

- Genes: `NAAA`, `EPHX2`, `GPR183`, `P2RX7`, `SPNS1`, `SCD`, `FADS1`,
  `ALOX5`, `ALOX5AP`, `PPARA`, `LTA4H`, `CH25H`, `CYP7B1`, `HSD3B7`.
- Modules: `gpr183_ligand_axis`, `leukotriene_axis`,
  `fatty_acid_desaturation_axis`, `lysolipid_egress_axis`,
  `oxylipin_resolution_axis`, `ppara_lipid_sensor_axis`,
  `critic_flux_panel`.

Result:

- Stable small-n features: `oxylipin_resolution_axis`, `leukotriene_axis`,
  `LTA4H`, `ALOX5`, `critic_flux_panel`, `ppara_lipid_sensor_axis`.
- `gpr183_ligand_axis`: `NO_CROSS_MS_REPLICATION`.

Interpretation:

- The broader lipid-flux operationalization is stronger than Wave130's fixed
  modules and does reveal peripheral treatment-response sensitivity.
- The signal remains small-n and not FDR-grade, so it is context rather than
  target evidence.

## 2026-05-28 07:51 CEST - Wave136 leukotriene strict route audit

Wave136 implemented and completed:

- Script: `scripts/v3_wave136_leukotriene_axis_strict_route_audit.py`
- Output: `results_v3/wave136_leukotriene_axis_strict_route_audit/`
- Branch call: `NO_REOPEN_LEUKOTRIENE_AXIS_SMALL_N_ONLY`

Critical failures:

- `fdr_grade_ms_response`
- `target_resolved_genetics`
- `class_route_previously_reopened`
- `direction_and_safety_clear`
- `prior_art_not_blocking`
- `single_selective_intervention_node_defined`

Decision:

- Keep leukotriene/oxylipin biology as a biomarker/context signal only.
- It is not a V3 target route without target-resolved genetics, a clear
  intervention direction, and a selective node distinct from crowded
  eicosanoid immunology.

## 2026-05-28 07:51 CEST - Wave137 GPR183 fair closure

Wave137 implemented and completed:

- Script: `scripts/v3_wave137_gpr183_ligand_axis_fair_closure.py`
- Output: `results_v3/wave137_gpr183_ligand_axis_fair_closure/`
- Branch call: `NO_REOPEN_GPR183_FAIR_CLOSURE`

Evidence classes:

- `matched_spatial_proxy`: `MISSING_NOT_NEGATIVE`
- `weak_compartment_contrast`: `NEGATIVE`
- `external_response_support`: `MIXED_SUPPORTIVE`
- `ms_pbmc_gpr183_gene_response`: `NO_CROSS_MS_REPLICATION`
- `ms_pbmc_ligand_axis_response`: `NO_CROSS_MS_REPLICATION`

Decision:

- GPR183 remains closed, but the interpretation is corrected. Lack of matched
  spatial-proxy rows is missing evidence, not affirmative negative evidence.
- Available fallback evidence still does not support promotion: zero coherent
  compartment diseases and no cross-dataset MS ligand-axis response.

## 2026-05-28 07:51 CEST - Wave138 post-critique residual route map

Wave138 implemented and completed:

- Script: `scripts/v3_wave138_postcritique_residual_fresh_route_map.py`
- Output: `results_v3/wave138_postcritique_residual_fresh_route_map/`
- Branch call: `NO_STRICT_FRESH_ROUTE_AFTER_POSTCRITIQUE_FILTERS`

Result:

- Strict promote candidates: 0
- Residual testable candidates: 0

Interpretation:

- After treating `NO_REOPEN`/`INSUFFICIENT` text as real blocker text and
  excluding post-critique closed lipid-flux/GPR183/DAP/eicosanoid routes, the
  corrected Wave133 fresh scan contains no immediate route to promote or test
  under V3 gates.
- Wait for sidecar disagreement before choosing the next pivot.

## 2026-05-28 08:05 CEST - Sidecar returns and response-audit correction

Sidecar state:

- Maxwell completed and closed.
- Turing completed and closed.
- Poincare completed and closed.

Maxwell result:

- No finding.
- Parked falsification targets: `FABP5`, `CHI3L1`, `APOC1`, `SNX10`, `GPNMB`,
  `SCARB2`, `MSR1`, `LIPA`, `SCD`, `NPC1/NPC2`.

Turing result:

- No clean genetics-first salvage target.
- Only useful comparator/falsification priorities: `IFI30`, `SP140`, `GALC`.

Poincare result:

- Major methodological defect: Wave130/Wave135 cross-dataset replication was
  too loose.
- Additional accepted defects: GSE250453 label inconsistency, module-score
  scaling mismatch, silent missing-input-to-negative behavior, unsafe Wave133
  false reopen summary, ambiguous Wave131 labels, and Wave137 mixed-response /
  substring-promotion parsing.

Corrections performed:

- Patched `scripts/v3_wave130_ms_treatment_response_audit.py`.
- Patched `scripts/v3_wave135_lipid_flux_ms_response_sensitivity.py`.
- Reran Waves 130, 135, 136, and 137.

Corrected Wave135 result:

- Branch call changed to `NO_LIPID_FLUX_MS_RESPONSE_RESCUE`.
- Stable small-n lipid-flux features changed from six to zero.

Decision:

- Treat all previous Wave130/Wave135 response-rescue language as superseded by
  the corrected reruns.
- Do not advance leukotriene/oxylipin, GPR183, or generic lipid-flux response
  routes.
- Next focus: Maxwell/Turing overlap does not contain a promotable target; use
  their suggestions only as falsification tests for residual markers.

## 2026-05-28 08:05 CEST - Wave139 residual marker falsification integration

Wave139 implemented and completed:

- Script: `scripts/v3_wave139_residual_marker_falsification_integrator.py`
- Output: `results_v3/wave139_residual_marker_falsification_integrator/`
- Branch call: `NO_RESIDUAL_MARKER_PROMOTABLE`

Result:

- `CLOSE_AS_MARKER_OR_READOUT`: 10
- `GENETICS_COMPARATOR_NOT_TARGET`: 3

Interpretation:

- Maxwell's residual lipid-lysosomal candidates do not produce a target route
  when existing residual, response, route, and genetics evidence are integrated.
- Turing's genetics candidates (`IFI30`, `SP140`, `GALC`) remain useful
  comparators but not intervention nominations.

Decision:

- Stop trying to rescue the lipid-lysosomal module as the primary target route
  unless new orthogonal perturbation or spatial data appear.
- Pivot to a different cross-autoimmune mechanism rather than continuing to
  re-rank marker-like lipid-lysosomal genes.
## 2026-05-28 08:09 CEST - Wave140 Target-First Pivot Audit

Action:
- Added `scripts/v3_wave140_target_first_pivot_audit.py` to
  `run_v3_analysis.sh`.
- Ran Wave140 after the Wave133 closure-hygiene correction and Wave139
  residual-marker integrator.

Result:
- Output directory:
  `results_v3/wave140_target_first_pivot_audit/`.
- Branch call: `NO_TARGET_FIRST_PIVOT_AVAILABLE`.
- Pivot candidates: `0`.
- Genetics comparators: `37`.
- Top genetics comparators: `IL7R`, `SP140`, `GAL`, `IFI30`,
  `ARHGAP31`, `CD80`, `IL6ST`, `STAT4`, `TAGAP`, `TNRC18`,
  `PTGER4`, `IL2RA`, `IL12A`, `IL10`, `PUS10`.

Interpretation:
- This closes the target-first salvage route under the current strict gates.
- The leading nodes are genetics comparators, not therapeutic hypotheses:
  they fail on reachable modality, prior-art/blocker status, missing local
  breadth, missing residual/perturbation evidence, or unresolved direction.
- Because another genetics-first rerank is now low-information, the next
  pivot should be perturbation-first or modality-first, with explicit
  validation that the operationalization is not simply a weak signature proxy.
## 2026-05-28 08:10 CEST - Wave141 Modality-First Successor Scan

Action:
- Added and ran `scripts/v3_wave141_modality_first_successor_scan.py`.
- Added Wave141 to `run_v3_analysis.sh`.

Rationale:
- Wave140 closed target-first salvage. Wave141 inverted the search to start
  from actionable modality, perturbation route, or L1000 reversal, then
  required biology gates. This directly attacks the proxy-satisficing risk:
  a marker or broad genetics hit is not enough.

Result:
- Output directory:
  `results_v3/wave141_modality_first_successor_scan/`.
- Branch call: `NO_MODALITY_FIRST_SUCCESSOR_AVAILABLE`.
- Promotable candidates: `0`.
- Near misses with at least six of eight gates: `1`.
- The single six-gate near miss is `CXCR2`, failing `ms_anchor` and
  `prior_not_blocked`.

Interpretation:
- Modality-first routing also fails inside the current lipid/APC evidence
  package.
- CXCR2 is not a successor because it is a neutrophil/chemokine prior-art and
  safety-saturated axis without sufficient MS anchor in this package.
- Next pivot: leave the lipid-lysosomal/APC module and interrogate orthogonal
  cross-autoimmune treatment-response or resistance circuits.
## 2026-05-28 08:18 CEST - Sidecar Returns and Wave142 Sender-Bridge Closure

Sidecar returns:
- Ramanujan: anti-TNF response/resistance circuit (`IL1B/CXCL8/TREM1/OSM`
  plus `LAMP3`) is biomarker-like only. Wave88 proxy adjustment and prior art
  block target nomination.
- Chandrasekhar: best orthogonal candidate is `CD58/CD2` adaptive synapse;
  still likely blocked by alefacept/prior-art and direction conflict, but worth
  a strict forcing test because it has MS genetic anchoring.
- Newton: Waves 140-141 were over-scoped in wording; fix branch/report language
  and stale artifacts.

Corrections performed:
- Wave140 rerun with scoped branch call:
  `NO_TARGET_FIRST_PIVOT_IN_CURRENT_LIPID_APC_CLOSURE_STACK`.
- Wave141 rerun with scoped branch call:
  `NO_MODALITY_FIRST_SUCCESSOR_IN_CURATED_PRIOR_INPUTS`.
- Wave136 report regenerated to remove stale small-n positive language.
- Added `SUPERSEDED_BY_WAVE134.json` in the Wave133 output directory.

Wave142 result:
- Script: `scripts/v3_wave142_sender_bridge_strict_pivot_audit.py`.
- Output: `results_v3/wave142_sender_bridge_strict_pivot_audit/`.
- Branch call: `NO_ORTHOGONAL_BRIDGE_PIVOT_AVAILABLE`.
- Bridge-biology-only candidates: `HIF1A`, `CALR`, `ITGAV`; all fail target
  or safety/prior-art gates.

Decision:
- Do not pursue response/resistance as a target route.
- Do not pursue sender-to-myeloid bridge genes as target routes.
- Proceed to CD58/CD2 adaptive-synapse forcing test.
## 2026-05-28 08:24 CEST - Wave143 CD58/CD2 Adaptive-Synapse Forcing

Action:
- Added and ran `scripts/v3_wave143_cd58_cd2_adaptive_synapse_forcing.py`.
- Added Wave143 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave143_cd58_cd2_adaptive_synapse_forcing/`.
- Branch call: `NO_CD58_CD2_ADAPTIVE_SYNAPSE_PROMOTION`.
- Failed critical gates:
  `ra_signal_survives_full_mixture_adjustment`,
  `ibd_replication_after_mixture`, `response_specificity_ra_and_ibd`,
  `direction_resolved_restore_vs_block`, `non_prior_art_intervention_route`.

Key numbers:
- RA baseline after T-cell/effector-memory adjustment: coef `0.8700`,
  p `0.008714`.
- RA baseline after full mixture adjustment: coef `0.5402`, p `0.08459`.
- IBD full-mixture positive rows p < 0.10: `0`.
- Strict residual surviving disease count: `0`.
- Alefacept prior art present: `true`.

Interpretation:
- `CD58/CD2` remains useful adaptive-synapse comparator biology with a real MS
  genetic anchor, but it is not a V3 target nomination.
- Next pivot: inspect B-cell/plasma-autoantibody/complement effector route as
  the remaining orthogonal candidate class from Chandrasekhar's synthesis.
## 2026-05-28 08:29 CEST - Wave144 B-Cell/Plasma/Complement Architecture Audit

Action:
- Added and ran `scripts/v3_wave144_bcell_complement_architecture_audit.py`.
- Added Wave144 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave144_bcell_complement_architecture_audit/`.
- Branch call: `NO_BCELL_COMPLEMENT_SHARED_THERAPEUTIC_TARGET`.
- Shared target candidates: `0`.
- Architecture-only axes: `3`.
- CFB Wave44 failed gates carried forward:
  `no_MS_anchor_or_positive_MS_lesion_direction`,
  `no_target_resolved_coloc_or_mr`,
  `factor_B_inhibition_prior_art_and_trial_crowding`,
  `systemic_complement_host_defense_safety`.

Interpretation:
- MG, AITD, celiac, and PBC support humoral/complement or antigen-entry
  disease architecture, but not a novel shared intervention node.
- Shared classes (`anti-CD20`, BAFF/APRIL/plasma-cell targeting, CD38,
  complement inhibition) are prior-art/safety crowded.
- Disease-specific antigen-entry routes are mechanistically real but not a
  pan-autoimmune V3 target.
## 2026-05-28 08:23 CEST - Wave145 Strict Route Inventory

Action:
- Added and ran `scripts/v3_wave145_strict_route_inventory.py`.
- Added Wave145 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave145_strict_route_inventory/`.
- Branch call: `NO_PROMOTABLE_ROUTE_AFTER_STRICT_INVENTORY`.
- Routes scanned: `59`.
- Promotable routes after strict inventory: `0`.

Top remaining rows after veto penalties:
- `CD58_TARGETABILITY`: score `-6.3`; vetoed by Wave143 CD58/CD2 closure.
- `MED16_MEDIATOR_MODULE`: score `-8.4`; fails cross-disease cell-state,
  MS-anchor, genetic/target-resolution, safety-direction, and support gates.
- `LRRC61_RESIDUAL_ROUTE`: score `-8.4`; no reachable modality, no MS anchor,
  no genetics, no prior-art/safety clearance.

Interpretation:
- This is a route-hygiene result, not biological exhaustion.
- Do not recycle Wave83/Wave116 top rows as target candidates.
- Next pivot should leave the lipid/APC route catalog and run a fresh
  disease-first architecture scan for mechanisms such as tissue entry, stromal
  retention, and barrier-interface control.
## 2026-05-28 08:23 CEST - Post-Wave145 Sidecars and Wave146 Architecture Scan

Sidecar returns:
- Planck: recommended a structured architecture-first barrier/retention scan.
- Gauss: found no promotable outside-catalog genetics-first route; recommended
  `TAGAP` as a strict adaptive-immune genetics benchmark.
- Faraday: accepted Wave145 as qualitative hygiene but rejected its numerical
  scores as calibrated because of double penalties and brittle string vetoes.

Action:
- Added and ran
  `scripts/v3_wave146_architecture_first_barrier_retention_scan.py`.
- Added Wave146 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave146_architecture_first_barrier_retention_scan/`.
- Branch call: `NO_ARCHITECTURE_FIRST_BARRIER_RETENTION_TARGET`.
- Donor score rows: `2968`.
- Source disease tests: `35`.
- Sender-receiver tests: `80`.
- Passing modules: `0`.

Key decision table:
- `stromal_retention_fibrosis`: source-positive disease count `3`,
  paired-receiver positive disease count `0`, MS anchor pass `true`.
- `epithelial_chemokine_entry`: source-positive disease count `3`,
  paired-receiver positive disease count `0`, MS anchor pass `false`, direct
  prior/comparator block `true`.
- `endothelial_entry`: source-positive disease count `2`,
  paired-receiver positive disease count `0`, MS anchor pass `false`.
- `tls_lymphoid_niche`: source-positive disease count `1`,
  paired-receiver positive disease count `1`, MS anchor pass `false`.
- `tl1a_comparator`: source-positive disease count `1`,
  paired-receiver positive disease count `0`, direct prior/comparator block
  `true`.

Interpretation:
- The architecture pivot did not collapse into a stromal-marker claim.
- Barrier/retention biology recurs in local tissue compartments, especially
  gut epithelial and T1D ductal compartments, but the matched receiver and MS
  anchor gates do not support a V3 therapeutic target.
- Next pivot: Gauss's `TAGAP` adaptive-immune genetics benchmark.
## 2026-05-28 08:23 CEST - Wave147 TAGAP Adaptive-Immune Genetics Benchmark

Action:
- Added and ran `scripts/v3_wave147_tagap_adaptive_genetics_benchmark.py`.
- Added Wave147 to `run_v3_analysis.sh`.
- Corrected a gate bug where an empty direction-proxy field was read as `nan`
  text and incorrectly counted as resolved.

Result:
- Output: `results_v3/wave147_tagap_adaptive_genetics_benchmark/`.
- Branch call: `NO_TAGAP_ADAPTIVE_GENETICS_PROMOTION`.
- T-cell tests: `10`.

Passed gates:
- `cross_autoimmune_genetics_ms_plus_two`.
- `target_resolved_qtl_or_l2g_ms`.

Failed gates:
- `direction_proxy_resolved`.
- `local_tagap_tcell_state_two_diseases`.
- `local_tcr_rhogtpase_module_two_diseases`.
- `ms_white_matter_expression_anchor`.
- `direct_perturbation_support`.
- `reachable_non_broad_suppression_modality`.

Key local expression results:
- No disease had nominal positive `TAGAP_single` T-cell support at p < 0.05.
- No disease had nominal positive `tcr_rhogtpase_activation` module support at
  p < 0.05.

Interpretation:
- Broad cross-autoimmune genetics alone does not yield a target.
- `TAGAP` remains a genetics benchmark/control, not a V3 therapeutic route.
- Next pivot: inspect the TNFSF14/LIGHT-LTBR lymphoid-niche axis surfaced by
  MS genetics and Wave146 TLS module behavior.
## 2026-05-28 08:23 CEST - Wave148 TNFSF14/LIGHT-HVEM/LTBR Audit

Action:
- Added and ran `scripts/v3_wave148_tnfsf14_light_lymphoid_niche_audit.py`.
- Added Wave148 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave148_tnfsf14_light_lymphoid_niche_audit/`.
- Branch call: `NO_TNFSF14_LIGHT_LYMPHOID_NICHE_PROMOTION`.

Passed gate:
- `ms_target_resolved_genetics`.

Failed gates:
- `cross_disease_target_genetics`.
- `local_tls_architecture_pass`.
- `ms_expression_anchor_fdr`.
- `directionality_clean`.
- `prior_art_not_blocking`.
- `direct_perturbation_or_response`.
- `reachable_selective_modality`.

Interpretation:
- `TNFSF14` has strong MS-specific L2G/QTL evidence but not cross-disease
  target-resolved genetics.
- `TNFRSF14` has broader autoimmune genetics but is blocked by HVEM/LIGHT
  directionality and prior-art ambiguity.
- The TLS/lymphoid niche module from Wave146 does not rescue the route.
- Next pivot: revisit only the weaker broad metabolite/barrier closures with a
  focused route audit, not a target claim.
## 2026-05-28 08:23 CEST - Wave149 Metabolite/Barrier Strict Re-Audit

Action:
- Added and ran `scripts/v3_wave149_metabolite_barrier_strict_reaudit.py`.
- Added Wave149 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave149_metabolite_barrier_strict_reaudit/`.
- Branch call: `NO_METABOLITE_BARRIER_ROUTE_REOPENED`.
- Routes scanned: `7`.
- Passing routes: `0`.

Focused weaker closures:
- `ahr_tryptophan`: no local genetics, no strict residual support, no
  disease-signature L1000 support, prior-art/crowding.
- `scfa_ffar_hcar`: no local genetics, no strict residual support, no
  disease-signature L1000 support, expression-only and crowded.
- `bile_acid_fxr_tgr5`: least crowded but unsupported locally; no genetics,
  no strict residual support, no disease-signature L1000 support.
- `retinoid_vdr_rxr`: no local genetics, no strict residual support, no
  disease-signature L1000 support, crowded/pleiotropic.

Interpretation:
- Faraday was right that these closures were weaker than P2RX7/GPR183, but
  stricter re-audit still does not reopen them.
- Next pivot: inspect perturbation/drug-response evidence directly as a
  repurposing-first route.
## 2026-05-28 08:23 CEST - Wave150 Repurposing-First Strict Audit

Action:
- Added and ran `scripts/v3_wave150_repurposing_first_strict_audit.py`.
- Corrected a scope bug so the MS L1000 q-value count only includes
  `gse111972_ms_wm_full_top150`.
- Added Wave150 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave150_repurposing_first_strict_audit/`.
- Branch call: `NO_REPURPOSING_FIRST_CANDIDATE`.
- Recurrent compounds audited: `123`.
- Repurposing gate pass: `0`.
- MS white-matter L1000 q <= 0.05 hits for the MS query: `0`.
- Promotion gate counts: `NO_GO=62`, `PARK_UNKNOWN_ONLY=61`.

Top blockers:
- Top recurrent compound `NVP-AUY922`: HSP90 oncology/stress target.
- Multiple high-ranked compounds: unresolved target/MOA.
- `thapsigargin`, `radicicol`, `vincristine`: cytotoxic/stress mechanisms.
- `SB-225002`: CXCR2 prior-art inflammatory target.

Interpretation:
- Perturbation-first repurposing does not produce a V3 candidate under current
  evidence.

## 2026-05-28 08:48 CEST - Wave151 Interface-Cell Perturbation-First Audit

Action:
- Ran `scripts/v3_wave151_interface_cell_perturbation_first_audit.py`.
- Added Wave151 to `run_v3_analysis.sh`.

Result:
- Output:
  `results_v3/wave151_interface_cell_perturbation_first_audit/`.
- Branch call: `NO_INTERFACE_CELL_PERTURBATION_ROUTE`.
- Routes audited: `8`.
- Passing routes: `0`.

Interpretation:
- This is not a global negative on barrier biology, metabolite receptors, or
  lymphoid-niche control.
- It is a stricter operationalization of the previous proxy-weak route: the
  route must have perturbation evidence in disease-relevant human interface
  cells, not just generic cell-line compound presence or a disease expression
  association.
- The local evidence stack lacks that context. Existing local LINCS/L1000
  outputs are mostly generic cell-line compound signatures, and the available
  Perturb-seq outputs do not label human epithelial/endothelial/fibroblast/TLS
  autoimmune interface contexts for these routes.

Self-critique:
- The wave's `real_interface_perturbation_context` gate is intentionally
  conservative and partly knowledge-engineered from local data limitations.
- Therefore it cannot falsify AHR, bile-acid, SCFA, retinoid, endothelial,
  stromal, or TLS biology. It only shows that the current local evidence stack
  cannot support a translational claim through an interface-cell perturbation
  path.

Next action:
- Search externally for public perturbation datasets in human epithelial,
  endothelial, fibroblast, or stromal/TLS-like cells under autoimmune-relevant
  inflammatory stimulation. If a usable dataset exists, build a new wave around
  direct perturbation-rescue evidence; if not, document the blocker and pivot to
  another independent modality.

## 2026-05-28 09:08 CEST - Wave152 External Interface Perturbation Module Test

Action:
- Dispatched and closed three read-only scout agents:
  epithelial/barrier, stromal/endothelial, and TLS/LTBR.
- Downloaded verified public processed matrices for `GSE190634`, `GSE217552`,
  `GSE200309`, and `GSE237845`.
- Downloaded HGNC complete set for Ensembl-to-symbol harmonization.
- Added and ran
  `scripts/v3_wave152_external_interface_perturbation_module_test.py`.
- Added Wave152 to `run_v3_analysis.sh`.

Result:
- Output:
  `results_v3/wave152_external_interface_perturbation_module_test/`.
- Branch call: `NO_EXTERNAL_INTERFACE_MODULE_ROUTE_REOPENED`.
- Datasets analyzed: `GSE190634`, `GSE200309`, `GSE217552`, `GSE237845`.
- Module contrasts tested: `96`.
- Route-gate passing modules: `0`.

Important signal:
- `epithelial_chemokine_entry` is induced in all four analyzed human
  interface datasets.
- `endothelial_entry` is induced in three datasets.
- In `GSE217552`, global keratinocyte treatment-vs-activated cosines are
  negative for fisetin, rapamycin, fisetin+rapamycin, and methotrexate, but the
  strict module gate does not show a nominal downshift for the inflammatory
  chemokine-entry module.

Self-critique:
- The negative branch call is gate-specific. It says no module currently has
  both broad induction and a direct nominal module-level rescue in the analyzed
  matrices.
- It does not eliminate epithelial chemokine or endothelial-entry biology. In
  fact, induction breadth is strong, but intervention specificity is still
  missing.
- `GSE129488` is probably the most valuable rescue dataset because it includes
  human synovial fibroblast cytokine induction plus siRNA perturbations, but the
  superseries matrix URL did not resolve to a usable processed matrix. This is
  a data-resolution task, not a biological negative.

Next action:
- Resolve `GSE129488` subseries/supplementary files and run a fibroblast
  genetic-perturbation rescue wave if processed expression matrices are
  accessible.

## 2026-05-28 09:21 CEST - Wave153 GSE129487 Synovial Fibroblast siRNA Rescue

Action:
- Resolved `GSE129488` into subseries.
- Identified `GSE129487` as RNA-seq Data 2: human synovial fibroblasts,
  cytokine stimulation, and siRNA perturbations against `CUX1`, `LIFR`,
  `STAT3`, `STAT4`, and `ELF3`.
- Downloaded processed `GSE129487` gene TPM, gene counts, and metadata.
- Added and ran
  `scripts/v3_wave153_gse129487_synovial_fibroblast_sirna_rescue.py`.
- Fixed two parsing bugs before interpretation:
  `s_mod.time` was using a DataFrame method rather than the `time` column, and
  pandas parsed the literal stimulation label `None` as missing.

Result:
- Output:
  `results_v3/wave153_gse129487_synovial_fibroblast_sirna_rescue/`.
- Branch call: `SYNOVIAL_FIBROBLAST_CONTROLLER_RESCUE_SIGNAL`.
- Samples: `192`.
- Rescue tests: `120`.
- Nominal rescue tests: `26`.
- FDR q<0.10 rescue tests: `0`.

Key signals:
- Control-siRNA cytokine induction is strong for epithelial-chemokine,
  endothelial-entry, stromal-retention, and TLS/niche modules.
- Top nominal rescue: `CUX1` siRNA reduces the `epithelial_chemokine_entry`
  module at TNF 6h: control induction `3.0536`, induction p=`6.44e-05`,
  siRNA effect `-0.5306`, siRNA p=`0.00223`, n donors=`4`.
- Multiple nominal CUX1 rescue effects recur across epithelial-chemokine and
  endothelial-entry modules under TNF or TNF+IL17.

Self-critique:
- This is not yet a therapeutic claim. No siRNA effect survives FDR across all
  120 tests, n donors is only `4`, and the tested perturbations are chosen by
  the original study rather than our unbiased screen.
- The current evidence supports a follow-up controller-consistency test, not
  target nomination.

Next action:
- Test whether `CUX1` has a consistent negative effect across induced
  interface modules and time/stimulation contexts, compared with the other
  siRNAs, using an aggregate sign/effect-size analysis that does not depend on
  cherry-picking individual nominal p-values.

## 2026-05-28 09:27 CEST - Wave154 CUX1 Consistency Guardrail

Action:
- Added and ran `scripts/v3_wave154_cux1_consistency_guardrail.py`.
- Aggregated siRNA effects only in module/time/stimulation contexts where
  control-siRNA cytokine induction was positive and BH q<0.05.

Result:
- Output: `results_v3/wave154_cux1_consistency_guardrail/`.
- Branch call: `CUX1_CONSISTENT_DIRECTIONAL_CONTROLLER_SIGNAL`.
- Induced-context siRNA tests: `105`.
- `CUX1`: `21` contexts, `18` negative, fraction negative `0.8571`, mean
  effect `-0.3069`, Wilcoxon one-sided p=`6.53e-05`, BH q=`0.00163`,
  binomial negative p=`0.000745`, q=`0.00621`.

Critical comparator result:
- `STAT4`: `21` contexts, `19` negative, mean effect `-0.2746`, Wilcoxon
  q=`0.00123`, binomial q=`0.00138`.
- `STAT3`: `21` contexts, `19` negative, mean effect `-0.2396`, Wilcoxon
  q=`0.00490`, binomial q=`0.00277`.
- Therefore CUX1 is directionally robust but not unique.

Interpretation:
- The guardrail rescues the CUX1 signal from single-test cherry-picking, but it
  also prevents overclaiming. CUX1 sits alongside STAT3/STAT4 as a controller
  of induced interface modules in human synovial fibroblasts.
- Because STAT3/STAT4 are expected cytokine-signaling nodes with crowded prior
  art and broad immunosuppression risk, the next value question is whether CUX1
  marks a more selective stromal/interface controller that generalizes across
  diseases without simply recapitulating JAK/STAT blockade.

Next action:
- Compare CUX1 specificity against STAT3/STAT4 at gene and module level:
  which induced genes are CUX1-sensitive but not STAT3/STAT4-sensitive, and do
  those genes overlap the cross-autoimmune interface modules from Wave152?

## 2026-05-28 09:34 CEST - Wave155 CUX1 Gene Specificity Versus STAT

Action:
- Added and ran `scripts/v3_wave155_cux1_gene_specificity_vs_stat.py`.
- Restricted analysis to genes in the recurrent interface modules.
- For each induced gene/time/stimulation context, tested whether CUX1 siRNA
  suppresses the gene while STAT3 and STAT4 siRNA do not suppress it nominally
  in the same context.

Result:
- Output: `results_v3/wave155_cux1_gene_specificity_vs_stat/`.
- Branch call: `CUX1_HAS_NOMINAL_NONSTAT_INTERFACE_GENE_SUBSET`.
- Induced gene-contexts: `72`.
- CUX1 nominally suppressed gene-contexts: `37`.
- CUX1-selective nominal gene-contexts: `20`.

Top gene pattern:
- `CXCL1`: `5/5` induced contexts CUX1-suppressed and `5/5` CUX1-selective
  by the nominal rule; mean CUX1 effect `-1.5045`, mean STAT3 effect
  `-0.0555`, mean STAT4 effect `-0.3786`.
- `CXCL8`: `4/5` CUX1-suppressed and `3/5` CUX1-selective; mean CUX1 effect
  `-1.3559`.
- `CXCL2`: `4/6` CUX1-suppressed and `3/6` CUX1-selective; mean CUX1 effect
  `-1.0350`.
- `ICAM1`: `5/5` CUX1-suppressed but only `2/5` CUX1-selective because STAT3
  or STAT4 also suppresses some contexts.

Interpretation:
- The non-obvious part of the CUX1 signal is not broad module suppression. It
  is selective suppression of ELR+ chemokines (`CXCL1`, `CXCL2`, `CXCL8`) in
  human inflammatory synovial fibroblasts, compared with STAT3/STAT4 siRNA.
- This potentially connects the cross-disease interface module to a
  fibroblast/epithelial neutrophil-chemokine circuit, but intervention on
  CXCR1/2 or IL-8 biology is crowded and may carry prior-art or safety issues.

Next action:
- Audit whether the CUX1 -> ELR+ chemokine subset gives a tractable
  intervention point distinct from known broad CXCR1/2 blockade, and whether it
  maps back to MS or remains RA/skin/gut interface biology only.

## 2026-05-28 09:41 CEST - CUX1 Prior-Art Demotion

Action:
- Searched literature for CUX1 and ELR+ chemokine regulation.
- Wrote `CONVERGENCE_CHECK_102.md`.

Verified closest prior work:
- Slowikowski et al., PNAS 2020, DOI `10.1073/pnas.1912702117`, PubMed
  `32079724`.
- The published mechanism already links CUX1/NFKBIZ to TNF+IL17 synergistic
  chemokine output in human synovial fibroblasts using the same study family as
  `GSE129487`.

Decision:
- Wave155 is valuable as an independent reproduction inside the V3
  cross-autoimmune interface-module frame, but it is not a novel target finding.
- CUX1 is demoted from candidate target to prior-art mechanistic anchor.

Next action:
- Test whether the CUX1/NFKBIZ ELR+ chemokine program generalizes across
  non-RA autoimmune interface datasets strongly enough to support either a
  stratification biomarker or a more selective intervention point.

## 2026-05-28 09:49 CEST - Wave156 ELR+ Chemokine Intervention Audit

Action:
- Added and ran `scripts/v3_wave156_elr_chemokine_intervention_audit.py`.
- First run contained a blocker-parser bug: genes with explicit
  `no_target_resolved_coloc_or_mr` text were promoted. Fixed the parser and
  reran before interpretation.
- Added Wave156 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave156_elr_chemokine_intervention_audit/`.
- Branch call: `NO_ELR_CHEMOKINE_INTERVENTION_PROMOTION`.
- Genes audited: `CXCL1`, `CXCL2`, `CXCL3`, `CXCL5`, `CXCL8`.
- Promoted interventions: `0`.

Reason:
- `CXCL1`, `CXCL2`, `CXCL3`, and `CXCL8` have CUX1-linked suppression signal
  in Wave155, but local prior audits block them as direct intervention targets
  because target-resolved causality/MS anchoring is absent or insufficient.
- `CXCL5` lacks a CUX1 signal in the current GSE129487 gene-level test.

Decision:
- Close direct ELR+ chemokine intervention promotion.
- Remaining value is a possible disease-state or treatment-response biomarker,
  not a standalone target.

## 2026-05-28 09:56 CEST - Epicurus Critique And Wave157 ELR State Biomarker Test

Action:
- Spawned Epicurus as hostile reviewer of the CUX1/ELR biomarker salvage route.
- Added and ran `scripts/v3_wave157_elr_state_biomarker_responsiveness.py`.
- Added Wave157 to `run_v3_analysis.sh`.

Epicurus return:
- Do not promote CUX1/ELR as target biology or MS biomarker.
- Only plausible salvage is a low-priority state marker, and only if it shows
  residual specificity, MS anchoring, and predictive value for a named therapy.

Wave157 result:
- Output: `results_v3/wave157_elr_state_biomarker_responsiveness/`.
- Branch call: `ELR_STATE_INDUCED_AND_TREATMENT_RESPONSIVE`.
- ELR genes: `CXCL1`, `CXCL2`, `CXCL3`, `CXCL5`, `CXCL8`.
- Upregulated induction datasets p<0.05: `3`
  (`GSE190634`, `GSE217552`, `GSE237845`).
- Treatment-down contrasts p<0.05: `1`, `GSE217552`
  fisetin+rapamycin vs activated, delta `-0.2171`, p=`0.0288`.

Interpretation:
- The ELR state is reproducibly inducible in human interface systems and is
  weakly treatment-responsive in keratinocytes.
- This still fails Epicurus's actionability bar: no named clinical endpoint,
  no MS anchor in a source-resolved lesion/barrier compartment, and no residual
  specificity versus generic inflammation.

Decision:
- Park CUX1/ELR as a comparator state, not a V3 finding.
- Next pivot should leave ELR chemokines unless a named treatment-response
  dataset appears.

## 2026-05-28 09:14 CEST - Wave158 TNF/IL17-CUX1/NFKBIZ Synergy Closure

Action:
- Verified the active agent state after interruption. Direct close on Epicurus
  returned `not found`, consistent with the written status that Darwin, Parfit,
  Lovelace, and Epicurus had already returned and closed.
- Added and ran
  `scripts/v3_wave158_tnfil17_synergy_controller_closure.py`.
- Added Wave158 to `run_v3_analysis.sh`.

Result:
- Output:
  `results_v3/wave158_tnfil17_synergy_controller_closure/`.
- Branch call: `NO_TNF_IL17_SYNERGY_CONTROLLER_PROMOTION`.
- Genes audited: `CUX1`, `NFKBIZ`, `STAT3`, `STAT4`.
- Promoted gene count: `0`.
- The strongest local mechanistic signal remains Wave155: `CXCL1` was induced
  in `5/5` contexts and CUX1-selective nominally suppressed in `5/5` contexts.
- Wave157 confirms an ELR interface state, but only one treatment-down contrast
  was found and the state lacks the required MS/source-compartment/actionability
  anchors.

Interpretation:
- The TNF/IL17-CUX1/NFKBIZ-ELR circuit is real biology, not a statistical
  artifact.
- It is also not a V3 claim: verified prior art already reports CUX1/NFKBIZ as
  TNF+IL17A synergy mediators in stromal fibroblasts, and local V3 artifacts do
  not supply enough MS anchoring, target-resolved genetics, or a selective
  reachable modality.

Decision:
- Close the CUX1/NFKBIZ/ELR route for therapeutic and biomarker promotion.
- Retain ELR chemokine state only as a comparator inflammatory-interface state.
- Next pivot must not re-promote TNF/IL17 synergy unless a genuinely new
  treatment-response endpoint or MS compartment-resolved dataset appears.

## 2026-05-28 09:18 CEST - Wave159 TWEAK/Fn14 Interface Audit

Action:
- Spawned two read-only sidecars:
  - Feynman: TWEAK/Fn14 prior-art and translational saturation audit.
  - Aquinas: non-ELR interface intervention candidate scout.
- Added and ran `scripts/v3_wave159_tweak_fn14_interface_audit.py`.
- Added Wave159 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave159_tweak_fn14_interface_audit/`.
- Branch call: `NO_TWEAK_FN14_ROUTE_PROMOTION`.
- Dataset: `GSE237845`.
- Genes tested: `18711`.
- FDR10 upregulated genes: `725`.
- Nominal non-ELR upregulated genes: `2096`.
- Promoted candidates: `0`.
- Top module was the closed ELR comparator: mean delta `2.2505`, `3` genes up
  at p<0.05.

Sidecar integration:
- Feynman recommended closing `TNFSF12/TNFRSF12A` because TWEAK/Fn14 is
  prior-art saturated across MS/EAE, IBD, RA, psoriasis, and lupus nephritis,
  with BIIB023 clinical precedent and broad patents.
- Aquinas recommended `LIFR/LIF` as the best next test because it has direct
  GSE129487 siRNA rescue signal outside the closed ELR/CUX1/NFKBIZ route.

Decision:
- Close TWEAK/Fn14 as a discovery branch.
- Retain TWEAK as a positive-control fibroblast/interface inflammatory
  perturbation.
- Pivot to a targeted LIFR audit.

## 2026-05-28 09:18 CEST - Wave160 LIFR Interface Rescue Guardrail

Action:
- Added and ran `scripts/v3_wave160_lifr_interface_rescue_guardrail.py`.
- Added Wave160 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave160_lifr_interface_rescue_guardrail/`.
- Branch call: `NO_LIFR_ROUTE_PROMOTION`.
- Axis genes audited: `LIFR`, `LIF`, `IL6ST`, `OSMR`.
- LIFR induced contexts tested: `21`.
- LIFR nominal negative rescue contexts: `6`.
- LIFR FDR10 negative rescue contexts: `0`.
- LIFR mean siRNA effect: `-0.1443`.
- LIFR MS white-matter delta: `-0.7968`, FDR `0.9203`.

Interpretation:
- LIFR is not noise: the siRNA direction is often negative in induced human
  synovial-fibroblast contexts.
- It is also not a V3 claim: no FDR-stable rescue, no local MS anchor, weak
  cross-disease support, and prior local target scans call the axis `NO_GO`.

Decision:
- Park LIFR/LIF as a wet-lab perturbation follow-up.
- Do not spend the next branch on more weak single-source interface markers.

## 2026-05-28 09:20 CEST - Wave161 Post-Interface Route Reprioritization

Action:
- Added and ran
  `scripts/v3_wave161_post_interface_route_reprioritization.py`.
- First run selected `PARK7` despite no concrete next test. This was a scoring
  bug and would have recycled a weak closed perturbation-first leftover.
- Fixed the guardrail to require a concrete next test for branch selection and
  to hard-penalize recent and older closed routes.
- Added Wave161 to `run_v3_analysis.sh`.

Corrected result:
- Output: `results_v3/wave161_post_interface_route_reprioritization/`.
- Branch call: `POST_INTERFACE_NEXT_BRANCH_SELECTED`.
- Routes ranked: `138`.
- Selected candidate: `FPR2_ANXA1_BIASED_RESOLUTION`.
- Selected next test: cross-disease ANXA1/FPR2 response-state support with MS
  lesion anchor; kill if no MS/resolution-state support.
- Top eligible candidates:
  `FPR2_ANXA1_BIASED_RESOLUTION`, `PSAP`, `GPR183_EBI2_OXYSTEROL_NICHE`,
  `PARK7_RESIDUAL_ROUTE`, `P2RX7_PURINERGIC_STRATIFICATION`.

Decision:
- Proceed to a focused FPR2/ANXA1 test.
- Treat it as a high-risk route because prior art is known and the previous
  blocker was weak MS anchor/target resolution.

## 2026-05-28 09:22 CEST - Wave162 FPR2/ANXA1 Response-State Kill Test

Action:
- Added and ran `scripts/v3_wave162_fpr2_anxa1_response_state_killtest.py`.
- Added Wave162 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave162_fpr2_anxa1_response_state_killtest/`.
- Branch call: `NO_REOPEN_FPR2_ANXA1_NO_MS_OR_PERTURBATION_ANCHOR`.
- FPR2 broad positive diseases: `Crohn disease;ulcerative colitis`.
- FPR2 MS white-matter delta: `-0.9326`, FDR `0.9141`.
- ANXA1 Wave36 up datasets: `4`.
- Promoted candidates: `0`.

Interpretation:
- The pro-resolution biology and druggability are real enough for a wet-lab
  assay branch.
- The V3 computational finding bar is not met: no positive MS lesion anchor,
  no real disease-relevant perturbation anchor, and the route remains crowded
  prior-art biology.

Decision:
- Keep FPR2/ANXA1 closed for V3 promotion.
- Continue down the eligible route list only when the next route has a concrete
  test that can add information beyond prior closures.

## 2026-05-28 09:24 CEST - Wave163 CD300 Receptor-Specific Closure

Action:
- Checked P2RX7 before opening a new branch. Existing Wave114 already closed
  it with `NO_REOPEN_P2RX7_TARGET_LEVEL_STRATIFICATION`; no new script was
  needed.
- Added and ran `scripts/v3_wave163_cd300_receptor_specific_closure.py`.
- Added Wave163 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave163_cd300_receptor_specific_closure/`.
- Branch call: `NO_REOPEN_CD300_DIRECTION_AND_MS_ANCHOR_FAIL`.
- Genes audited: `CD300A`, `CD300E`, `CD300LF`, `CD300C`, `CD300LG`.
- Best cross-signal gene: `CD300E`, positive in `3` diseases.
- Best CRISPR trend gene: `CD300A`, LFC `1.3382`, FDR `0.9200`.
- Promoted candidates: `0`.

Interpretation:
- The route fails by non-convergence: the family member with disease-state
  recurrence is not the member with the perturbation trend.
- No member has positive MS anchoring, FDR perturbation support, or a selective
  safe modality/direction.

Decision:
- Close CD300 receptor-specific tuning for V3 promotion.
- Resolution/efferocytosis reopeners are now closed again after fresh tests.

## 2026-05-28 09:30 CEST - Wave164 Genetics-First Survivor Audit Rerun

Action:
- Reran `scripts/v3_wave164_genetics_first_survivor_audit.py` after fixing the
  missing-ChEMBL handling bug: `NaN` target IDs are now treated as missing, not
  as the literal string `"nan"`.
- Added Wave164 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave164_genetics_first_survivor_audit/`.
- Branch call: `GENETICS_FIRST_MECHANISM_BUT_NO_DIRECT_TARGET`.
- Candidates ranked: `2014`.
- Corrected top gene: `TYK2`, score `23.5`.
- Corrected top-gene blockers:
  `insufficient_cross_disease_ms_genetic_anchor;prior_or_local_no_go_blocker`.
- Promoted candidates: `0`.

Interpretation:
- The bug mattered for ranking details but not for the decision.
- The strongest genetics-first survivors are credible autoimmune mechanisms
  (`TYK2`, `IL12A`, `PTPN2`, `IRF5`, `CLEC16A`, `IL10`, `TAGAP`, `INAVA`), but
  they fail the V3 target bar by one or more of: no MS-specific anchor, weak
  cell-state support, no direct modality, or saturated prior/local no-go status.

Decision:
- Do not claim a genetics-first direct target.
- Use Wave164 to choose a mechanistic-neighbor audit. `INAVA` is the next
  useful branch because it has a strong cross-autoimmune/MS genetic anchor but
  no direct modality, forcing a test of whether a druggable NOD/RIPK/autophagy
  neighbor can carry the mechanism without losing MS/cross-disease support.

## 2026-05-28 09:32 CEST - Wave165 INAVA/NOD/RIPK Neighbor Audit

Action:
- Added and ran `scripts/v3_wave165_inava_nod_ripk_neighbor_audit.py`.
- First run exposed a data-wiring issue: the script pointed at a non-existent
  Wave62 directory and used broad-summary column names that did not match
  `wave96_c15orf48_controller_search/pre_donor_controller_rank.tsv`.
- Fixed the Wave62 path and mapped the Wave96 columns to
  `c15_trend_positive_disease_count`, `c15_strict_positive_context_count`,
  `ms_delta_log2`, `ms_p`, `ms_fdr`, `w37_contrast_lfc`, and
  `w37_contrast_fdr`; reran before integration.
- Added Wave165 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave165_inava_nod_ripk_neighbor_audit/`.
- Branch call: `NO_INAVA_NOD_RIPK_NEIGHBOR_PROMOTION`.
- Genes tested: `INAVA`, `RIPK2`, `NOD2`, `NOD1`, `ATG16L1`, `IRGM`, `CARD9`.
- Best scored gene: `INAVA`, neighbor score `0`.
- Promoted candidates: `0`.

Key evidence:
- `INAVA` preserves the genetics gate:
  `strong_l2g_disease_count=4` (`AS;Crohn;MS;UC`),
  `strong_qtl_coloc_disease_count=5` (`AS;Crohn;MS;PBC;UC`),
  `ms_max_l2g_score=0.6894`, `ms_max_qtl_h4=0.9828`.
- `INAVA` fails cell-state, perturbation, and modality gates:
  only `1` positive C15 context (`t1d_stellate_cell`), MS white matter delta
  `0.0`, p `1.0`, FDR `1.0`, no ChEMBL target/activity rows.
- `RIPK2` and `NOD2` show IBD-local myeloid recurrence
  (`ibd_crohn_myeloid;ibd_uc_myeloid`) but do not preserve the INAVA
  MS/cross-autoimmune genetic anchor. `RIPK2` MS delta is `0.3783`, p
  `0.1975`, FDR `0.8994`; perturbation LFC `0.2823`, FDR `0.9200`.
  `NOD2` is reachable (`CHEMBL1293266`, `840` activity rows) but has no MS
  genetic anchor and negative/non-significant MS expression (delta `-0.1974`,
  p `0.6126`, FDR `0.9476`).

Interpretation:
- `INAVA` remains a credible mechanism clue for barrier/innate genetics, but
  the tractable NOD/RIPK/autophagy neighbor route collapses into IBD-local
  prior biology and loses the MS/cross-autoimmune target-resolution evidence.

Decision:
- Do not promote `INAVA`, `RIPK2`, `NOD2`, `NOD1`, `ATG16L1`, `IRGM`, or
  `CARD9` for V3.
- The genetics-first and interface/resolution reopeners have now failed direct
  therapeutic conversion. The next search should prioritize a fresh central
  node that already has both cross-disease genetics and local cell-state
  recurrence, rather than trying to borrow druggability from a neighbor.

## 2026-05-28 09:38 CEST - Wave166 Same-Gene Genetics/Cell-State Overlap

Action:
- Added and ran `scripts/v3_wave166_same_gene_genetics_cellstate_overlap.py`.
- First run returned apparent eligible routes (`SP140`, `SIRPB1`, `CD83`,
  `IFI30`, `ARHGAP31`), but inspection showed the blocker parser was too weak:
  it did not catch generic `no_go`, `prior_or_local`, or local known-closed
  genes such as `SP140`.
- Tightened the closure filter with generic no-go/prior tokens and a small
  explicit known-closed list (`SP140`, `STAT4`, `STAT3`, `IL7R`, `IFI30`,
  `GPR183`, `P2RX7`, `FPR2`, `ANXA1`, `CD300*`, `TYK2`, `IL12*`, `PTPN2`,
  `IRF5`, `NOD2`, `RIPK2`, `INAVA`), then reran before integration.
- Added Wave166 to `run_v3_analysis.sh`.

Corrected result:
- Output: `results_v3/wave166_same_gene_genetics_cellstate_overlap/`.
- Branch call: `NO_UNBLOCKED_SAME_GENE_GENETICS_CELLSTATE_ROUTE`.
- Genes ranked: `25255`.
- Eligible same-gene routes after guardrails: `0`.
- Top row remains `SP140`, but it is correctly blocked as known closed/prior
  blocked.

Interpretation:
- The same-gene overlap principle is correct, but current local evidence does
  not expose an unblocked route after enforcing prior/local closures.
- Apparent positives are mainly known-crowded transcriptional/immune nodes or
  rows where Wave164 already identified insufficient MS/cell-state/druggability
  support.

Decision:
- Do not select a same-gene genetics/cell-state route from Wave166.
- Next pivot should be a different modality: foundation/perturbation signature
  reversal or external drug-response evidence, because target-first and
  state-first local ranking are now over-depleted.

## 2026-05-28 09:46 CEST - Sidecar Returns And Wave167 No-Label Shadow Rank

Sidecar returns:
- Linnaeus critiqued Waves 164-166 as potentially circular because inherited
  no-go labels and a manual closed-gene list can create false depletion.
  Accepted critique.
- Boole recommended two non-redundant pivots:
  phenotype-first efferocytosis controllers from Wave37/Wave81/Wave166, and
  L1000 repurposing deconvolution from Wave150 joined to target/state evidence.
- Both agents were closed after return.

Action:
- Added and ran `scripts/v3_wave167_shadow_no_label_overlap.py`.
- This recomputes same-gene genetics/cell-state overlap with inherited labels
  removed from eligibility and retained only as annotations.
- Added Wave167 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave167_shadow_no_label_overlap/`.
- Branch call:
  `SHADOW_RANK_READY_FOR_TARGET_QUALITY_AND_INDEPENDENT_STATE_VALIDATION`.
- Genes ranked: `25255`.
- Same-gene genetics + C15 cell-state shadow-pass genes: `7`.
- Top gene without no-go labels: `STAT4`, evidence score `15.9`.
- Top-25 label classes: `20` prior-art/local-prior, `3` local no-go label,
  `2` unlabeled/data-blocked.

Interpretation:
- Linnaeus was correct that route space is not literally empty when labels are
  removed.
- The top no-label candidates are still mostly not actionable. Examples:
  `STAT4` is genetically broad but a nonselective TF route; `SP140` has
  genetics/cell-state and a perturbation trend but prior-art/direction blockers;
  `IL7R` is crowded CD127 biology; `SIRPB1`, `CD83`, `IFI30`, and `ARHGAP31`
  require independent state and target-quality validation before any route can
  be reopened.

Decision:
- Do not reinstate Wave166 depletion as final.
- Use Wave167 as the candidate pool for two follow-up audits:
  target-quality for apparent ChEMBL reachability and C15-independent state
  validation.
- In parallel, run Boole's phenotype-first efferocytosis pivot because it is
  independent of same-gene genetics and may identify an intervention handle for
  myeloid repair rather than a genetics-first target.

## 2026-05-28 09:50 CEST - Wave168 Efferocytosis State-Controller Pivot

Action:
- Added and ran `scripts/v3_wave168_efferocytosis_state_controller_pivot.py`.
- This implements Boole's phenotype-first branch: start from Wave37 CRISPR hits
  where KO enhances efferocytosis, then require autoimmune state recurrence,
  MS anchor, intervention handle, and no hard modality/prior blocker.
- Added Wave168 to `run_v3_analysis.sh`.

Result:
- Output: `results_v3/wave168_efferocytosis_state_controller_pivot/`.
- Branch call: `NO_EFFEROCYTOSIS_STATE_CONTROLLER_PROMOTION`.
- Screen hits tested: `128`.
- Promoted candidates: `0`.
- Best gene: `YWHAE`, pivot score `6.0038`.
- Best-gene blockers:
  `no_ms_anchor;no_intervention_handle;no_genetic_anchor_annotation`.

Key evidence:
- Top phenotype/state genes (`YWHAE`, `RYK`, `ABTB2`, `FAM49B`, `RECQL4`,
  `CHST11`, `TPX2`, `LRRC61`) have functional efferocytosis signal and some
  state recurrence, but no acceptable direct intervention handle and generally
  no MS anchor.
- `FAM49B` has broad state recurrence in `3` diseases and efferocytosis LFC
  `0.7903`, but lacks MS anchor, intervention handle, and genetic annotation.
- `LRRC61` has broad state recurrence in `4` diseases and efferocytosis LFC
  `0.6800`, but lacks MS anchor, intervention handle, and genetic annotation.

Interpretation:
- Phenotype-first repair biology is real enough to keep as a wet-lab discovery
  direction, but it does not currently produce a translational V3 target.
- The limiting issue is not absence of functional signal; it is absence of a
  selective, disease-anchored intervention point.

Decision:
- Do not promote the efferocytosis-state controller branch.
- Continue to Boole's second modality pivot: L1000 repurposing deconvolution,
  because it starts with compounds and may solve intervention-handle limitations
  directly.

## 2026-05-28 09:47 CEST - Waves169-170 L1000 Repurposing Deconvolution

Wave169 action:
- Added and ran `scripts/v3_wave169_l1000_repurposing_deconvolution_pivot.py`.
- This reinterprets Wave150 `PARK_REVIEW` compounds as unresolved
  target-deconvolution candidates rather than failed gene-first targets.

Wave169 result:
- Output: `results_v3/wave169_l1000_repurposing_deconvolution_pivot/`.
- Branch call: `NO_L1000_REPURPOSING_PROMOTION`.
- Review rows tested: `33`.
- Promoted candidates: `0`.
- Best candidate: `XMD-1150/LRRK2`, score `12.0198`.
- Initial blocker: `weak_target_quality_proxy`.

Problem found:
- The local target-quality proxy was incomplete for this modality. It missed
  obvious druggable targets including `LRRK2`, `PIK3CG`, `PTGIR`, and `SLC1A2`.
- Python network access is sandbox-blocked, but `curl` is approved and worked.

External artifacts:
- Downloaded ChEMBL target-search JSON with `curl` into
  `results_v3/wave170_external_chembl_target_quality/raw/` for:
  `LRRK2`, `PIK3CG`, `PTGIR`, `SLC1A2`.
- Downloaded ChEMBL activity JSON for:
  `LRRK2` (`CHEMBL1075104`), `PTGIR` (`CHEMBL1995`), and provisional
  `SLC1A2` (`CHEMBL4398`; no exact search match in the downloaded target file).

Wave170 action:
- Added and ran `scripts/v3_wave170_external_chembl_target_quality.py`.
- This parses only saved raw JSON, so it is reproducible offline once the raw
  artifacts are present.
- Added Waves169-170 to `run_v3_analysis.sh`.

Wave170 result:
- Output: `results_v3/wave170_external_chembl_target_quality/`.
- Branch call: `PROMOTE_AFTER_EXTERNAL_TARGET_QUALITY`.
- Quality-supported genes: `LRRK2`, `PTGIR`.
- Corrected promoted candidate: `XMD-1150/LRRK2`.
- LRRK2 ChEMBL support: `CHEMBL1075104`, single protein, `1000` downloaded
  activity rows, `312` unique molecules, best downloaded nM `0.39`.
- PTGIR ChEMBL support: `CHEMBL1995`, single protein, `1000` downloaded
  activity rows, `785` unique molecules, best downloaded nM `0.0001`.

Interpretation:
- The repurposing branch is the first post-Wave160 route to satisfy the
  mechanical computational gates after fixing target-quality evidence.
- This is not yet a finding. `LRRK2` is likely crowded in neuroinflammation,
  Parkinson's, microglia, and possibly MS/EAE, so novelty and prior-art checks
  become the immediate kill test.

## 2026-05-28 09:55 CEST - Wave171 LRRK2 Prior-Art Kill Test

Action:
- Wrote `results_v3/wave171_lrrk2_prior_art_killtest/REPORT.md`.
- Ran web/PubMed/ClinicalTrials/patent searches for `LRRK2`, MS/EAE,
  neuroinflammation, autoimmune disease, and inhibitors.

Result:
- Branch call: `NO_LRRK2_NOVELTY_OR_SPECIFICITY_PROMOTION`.
- Closest prior work includes:
  - URMC-099 in EAE, a broad MLK inhibitor with additional LRRK2 activity,
    improving microglial inflammatory phenotype and behavioral/synaptic
    outcomes after EAE symptom onset (PubMed `30627663`).
  - BIIB122 as CNS-penetrant LRRK2 inhibitor in Parkinson's disease
    (`NCT05348785`).
  - LRRK2 inhibitor patent prior art explicitly naming MS/neuroinflammation and
    autoimmune indications, including Google Patents `WO2024182689A1` and
    `WO2023224894A9`.

Interpretation:
- `XMD-1150/LRRK2` is not a novel MS/autoimmune therapeutic claim.
- The L1000 branch remains valuable methodologically because it recovered
  known CNS-penetrant neuroimmune kinase biology, but it fails the V3 novelty
  bar and lacks target-resolved MS genetics.

Decision:
- Demote `XMD-1150/LRRK2` to prior-art-blocked comparator.
- Continue L1000 or external-target-quality pivots only for candidates without
  direct MS/autoimmune patent and literature saturation.
