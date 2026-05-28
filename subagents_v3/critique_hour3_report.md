# Hour 3 Hostile Peer Review Critique

Returned: 2026-05-26

Read-only critique of the V3 direction except for this report. This document does
not claim a discovery. It identifies why the current direction is not yet
defensible as a target, mechanism, or translational product.

## Bottom Line

The current V3 direction has converged on a biologically unsurprising
inflammation/APC axis:

`IFNG -> IFNGR/JAK/STAT1 -> CIITA/NLRC5/RFX5 -> HLA-II/CD74 + IFI30/CTSS/TAP/B2M`

That is not yet a discovery. It is the expected transcriptional consequence of
IFN-gamma exposure and antigen-presentation activation in inflamed tissue. The
data currently show recurrence of a canonical IFN/APC program, but they do not
separate disease mechanism from inflammation severity, immune infiltration, APC
abundance, treatment-response prior art, or known HLA/IFN biology.

The project should not advance a target claim. At most it has a hypothesis for a
combined IFN-gamma/HLA-II/CD74/IFI30/TAP cell-state biomarker, and even that
requires a treatment-by-biomarker interaction in cell-type-resolved clinical
data before it is more than relabeling an IFN signature.

## 1. The IFNG/HLA-II/CD74/GILT/TAP Transition Is Too Generic

The claimed transition is built from genes that are almost diagnostic of generic
IFN-gamma/APC activation: `STAT1`, `IRF1`, `CXCL10`, `GBP1`, `HLA-DRA`,
`HLA-DRB1`, `HLA-DPA1`, `HLA-DPB1`, `B2M`, `TAP1`, `TAP2`, `CD74`, `CTSS`, and
`IFI30`. A reviewer will read this as a canonical antigen-presentation response,
not as a new disease mechanism.

The strongest perturbation evidence, Mixscale, makes the genericness worse. It
shows that knocking down `IFNGR1`, `IFNGR2`, `JAK1`, `JAK2`, or `STAT1` suppresses
IFN/APC readouts under IFN-gamma stimulation. That is exactly what the pathway
diagram predicts. It validates reagent wiring in stimulated cancer/immortalized
cell lines; it does not elevate the downstream state into a novel autoimmune
discovery.

The cross-disease table also points toward a state label rather than a target.
The strongest modules are `mif_cd74_receptor_state`, `ifn_apc`, and
`mixscale_validated_ifng_readout`. The individual-gene table is dominated by HLA
genes, `NLRC5`, `STAT1`, `B2M`, `TAP`, and `IRF1`; `IFI30` is trend-or-better in
only two diseases. That pattern argues against a named effector target and for a
broad immune activation program.

## 2. Inflammation Severity And Infiltration Are Not Excluded

The current analyses do not show that the transition is independent of tissue
inflammation burden. A high IFN/APC score can arise from:

- more immune cells in diseased tissue;
- more APCs among immune cells;
- higher lesion/inflammation severity;
- more epithelial stress and acquired HLA-II expression;
- treatment history or sampling site differences;
- generic IFN exposure shared by many inflammatory diseases.

The direct h5ad analyses improve over bulk tissue, but they still do not fully
answer this. Donor-level compartment scoring is not the same as proving the
program is independent of cell composition, disease severity, and inflamed-site
sampling. Sjogren support being strongest in epithelium, not APCs, further
weakens a clean myeloid/APC mechanism and raises the simpler interpretation:
many inflamed tissues turn on IFN/HLA-II programs in whatever compartment is
most exposed.

The MS evidence is also not decisive. GSE111972 supports a `CD74/CD44/CXCR4/HLA`
microglial receptor/APC state in MS white matter, but the same notebook records
that `IFI30` and `NAMPT` are not strong individual MS microglial hits in that
dataset. The direction already had to retreat from a specific effector claim to
a broad state claim.

## 3. Hashimoto Spatial And GSE253006 Are Weak Proxies

The Hashimoto spatial evidence should be treated as a warning, not a rescue.
The analysis compares two controls with three Hashimoto samples. The reported
standardized effects are implausibly huge, including Hedges g values around 17
to 30 for several module readouts. That is a small-n, low-variance artifact risk,
not a population-scale effect estimate.

Visium spots are mixed tissue units. In Hashimoto thyroiditis, lymphocytic
infiltration and IFN/HLA activation are core disease features. A spot-level or
sample-level IFN/HLA signal can therefore reflect infiltrate density, follicular
destruction, tertiary lymphoid structure, or local APC abundance. It does not
establish a conserved, therapeutically relevant transition. Graves being weak in
the same dataset also argues against using autoimmune thyroid disease as broad
support.

GSE253006 is even weaker as translational evidence. The current analysis is an
all-cell sample-level baseline comparison with 5 responders and 6
non-responders, no GEO cell-type annotations, and no tested feature surviving
FDR. The top nominal signal, `NLRC5`, has p=0.0655 and FDR=0.978. `ifn_apc`,
`CD74`, `IRF1`, `CTSS`, `B2M`, and related features do not provide a defensible
biomarker validation. The published dataset already points to baseline
JAK-STAT activity in responders, so a broad JAK/IFN response-biomarker angle is
also prior art.

## 4. Foundation-Model Evidence Is Insufficient

The foundation-model requirement is not met. State released CD14 outputs were
only analyzed feature-agnostically because the feature-to-gene mapping was
missing. The notebook explicitly blocks gene-module conclusions from those files
until the 9.1 GB AnnData mapping is recovered. That means there is no
gene-specific State evidence for `IFI30`, `CD74`, `CTSS`, `TAP`, or the module.

Stack and Evo 2 are not contributing usable biological evidence here. Evo 2
local inference is blocked by macOS CPU/no CUDA/no hosted credentials. Stack was
installed but no reported result supports the target or mechanism. Mixscale is
real perturb-seq evidence, but it is not foundation-model evidence. L1000FWD
does not nominate a clean therapeutic reversal; curated module reversals are
dominated by broad stress, oncology, tubulin, PLK, HSP90, or toxicity probes.

Therefore the model channel currently says: availability was partially tested,
but no foundation model has provided target-specific, gene-mapped, disease-state
support.

## 5. Genetics Fails The DoD

The genetics report explicitly blocks the target-level genetics claim. It says
there is pathway-compatible anchoring, not clean single-gene cross-autoimmune
anchoring.

The broad HLA-II/MHC signal supports antigen-presentation biology but is too
LD-complex and non-specific to nominate `CD74`, `IFI30`, `CTSS`, `STAT1`, or any
specific HLA-II component. `IRF1/CARINH` is the best non-MHC regulatory anchor,
but it is not proven isolated `IRF1`, and it is not an intervention target
validated by the rest of the package. `IFI30` has coloc-grade MS-specific
support, but not pan-autoimmune support. The report specifically says not to
claim supported MR/coloc for `CD74`, `CTSS`, `STAT1`, `CIITA`, `RFX5`,
`IFNGR1`, `JAK1`, or pan-disease `IFI30`.

If the DoD requires genetic support for a target across multiple scoped
autoimmune diseases, V3 fails. If the DoD only requires pathway compatibility,
that standard is too weak to distinguish this project from any IFN/HLA
autoimmunity review.

## 6. No Intervention Point Survives Novelty And Feasibility

Every plausible intervention point is either obvious, blocked, broad, weakly
druggable, or unsupported.

- `IFNGR/JAK/STAT1`: strongest controller, but therapeutically obvious,
  heavily prior-arted, and broad immunosuppression.
- `CD74/MIF`: prior-arted by ibudilast and CD74/MIF autoimmune literature; at
  best a state/stratification marker, not a new therapeutic direction.
- `CIITA/RFX5/NLRC5`: mechanistically narrower, but transcription-factor
  druggability is poor, structural confidence is weak, and genetics is not
  robust.
- `CTSS`: druggable, but crowded with autoimmune prior art and underwhelming
  clinical history.
- `IFI30/GILT`: attractive mainly because it is less crowded, not because it is
  validated. It lacks chemical matter, has only MS-specific genetics, is not a
  clean pan-disease expression hit, has EAE mechanism cautions, and the
  explicit ODE model says suppressing it does not reproduce broad IFN/APC or
  HLA-II/CD74 suppression.

The mechanistic model is especially damaging to the IFI30 intervention story.
Even 95% IFI30 suppression mainly reduces the GILT/lysosomal readout and has
minimal effect on upstream IFN/APC or HLA-II/CD74 readouts across the tested
feedback range. That means an IFI30 inhibitor cannot be pitched as arresting the
whole transition without direct contrary perturbation data.

The only novelty lane left is a precise companion biomarker:
combined `IFN-gamma/HLA-II/CD74/IFI30-GILT/TAP` cell-state enrichment to predict
response to an existing JAK/IFN/antigen-processing intervention. That lane is
not proven by the current data and is easy to lose to prior art unless the
claim is treatment-response interaction, not diagnosis or generic IFN signature.

## 7. Analyses That Would Falsify Or Rescue The Direction

### Falsification Tests

1. Cell composition control: reanalyze every disease atlas with donor-level
   models that include APC fraction, immune-cell fraction, epithelial fraction,
   lesion/inflammation severity proxies, batch, tissue site, and treatment where
   available. If the transition loses effect after these covariates, it is
   infiltration/severity, not a disease mechanism.

2. Generic inflammation control: compare against non-autoimmune inflamed tissue,
   infection, rejection, wound, and cytokine-treated control datasets. If the
   score is equally high there, it is generic IFN/APC activation.

3. IFN orthogonalization: regress out canonical IFN-gamma and type-I IFN module
   scores, then ask whether `CD74/IFI30/CTSS/TAP/HLA-II` residuals still
   replicate across diseases. If not, the project is an IFN signature with extra
   antigen-presentation genes.

4. Effector perturbation: directly perturb `IFI30` and `CTSS` in primary
   disease-relevant cells under IFN-gamma and measure HLA-II/CD74/TAP/B2M,
   peptidome, cytokines, antigen presentation, and T-cell activation. If
   IFI30/CTSS perturbation only changes lysosomal processing and not disease
   phenotypes, the therapeutic target claim fails.

5. Genetics gate: require target-level colocalization or credible regulatory
   genetics for the proposed intervention point in more than one disease. If
   only MHC and `IRF1/CARINH` remain, genetics supports background biology only.

6. Biomarker interaction: in a treatment dataset, test whether the combined
   cell-state score predicts differential benefit from a specific therapy beyond
   baseline IFN score, baseline severity, and cell composition. If not, the
   biomarker lane fails.

### Rescue Tests

1. Build a residual disease-state signature that is orthogonal to generic IFN,
   HLA-II abundance, APC proportion, and tissue inflammation severity. Replicate
   the residual signature in at least four independent diseases with donor-level
   statistics.

2. Recover gene-mapped State results or run a relevant perturbation foundation
   model end to end. The required output is gene-specific prediction for
   IFN-gamma/JAK/STAT and downstream `IFI30`, `CTSS`, `CD74`, `TAP`, and HLA-II
   genes in relevant primary cell states, benchmarked against held-out real
   perturbation data.

3. Reprocess GSE253006 from raw 10x matrices with cell typing, donor-level
   pseudo-bulk, and a preregistered baseline-response model. Abandon it if the
   effect remains all-cell, non-significant, or reducible to published JAK-STAT
   response biology.

4. Redo the Hashimoto spatial analysis with deconvolution, immune-density
   covariates, spatial neighborhood features, and additional thyroid cohorts. It
   only helps if the state persists within matched compartments after accounting
   for infiltrate density.

5. Define the intervention product before more scoring. If it is a target, it
   needs direct perturbation, genetics, druggability, and novelty. If it is a
   biomarker, it needs clinical treatment interaction and a prior-art-safe claim.
   The current hybrid wording lets weak target evidence borrow strength from
   weak biomarker evidence.

## Recommendation

Do not claim an intervention target or discovery from the current V3 package.
Demote the direction to a stress-tested hypothesis: a recurrent but generic
IFN-gamma/APC antigen-processing state that may or may not become useful as a
cell-state response biomarker. The next work should be adversarial covariate
control and direct perturbation, not more cross-disease scoring of the same
canonical IFN/HLA genes.
