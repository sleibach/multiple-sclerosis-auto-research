# Wave110 Overlooked Intervention-First Route Scout

Bound: local V3 artifacts only. No finding claimed.

## Call

`NO_FINDING_TOP_ROUTE_FORCING_TEST_ONLY`.

The least-bad overlooked route is still `GPR183/EBI2 oxysterol-niche modulation`, not because it is strong, but because it is an intervention-first GPCR axis with local response movement and a plausible spatial/niche mechanism. It still fails V3 promotion.

## Top 3 Routes

### 1. GPR183/EBI2 Oxysterol-Niche Modulation

Why it might escape previous blockers:

- Wave83 ranked `GPR183_EBI2_OXYSTEROL_NICHE` as the only `PARK_INTERVENTION_CLASS_NEEDS_FORCING_TEST` route.
- Wave74 found a direct receptor anchor in Crohn/Sjogren/UC and response-module support in IBD and RA treatment datasets.
- It is not another lysosomal marker target. It is an upstream spatial GPCR/niche hypothesis: oxysterol-guided APC/lymphoid trafficking could move the lipid-lysosomal myeloid state indirectly.
- It avoids the CD82 failure mode because the intervention is not a marker surface protein; it asks whether niche guidance drives the marker state.

Why it likely fails:

- Wave74 found zero coherent cross-disease ligand-plus-`GPR183`-plus-response contexts.
- MS white-matter support is absent: `GPR183` receptor and ligand/response modules were null while IFN/APC and APC/lysosome comparators were positive.
- Wave66 oxysterol-like metabolite support was sparse/negative.
- Wave62 did not give target-resolved genetics or local druggability support.
- Prior Wave93 sidecars already made this route vulnerable to prior-art/druggability/methods objections.

Local forcing test:

- Re-run a stricter spatial-proxy test using only contexts where both ligand-production cells and receptor-response myeloid/APC cells are present in the same disease dataset. Require: ligand module up in tissue/stromal/endothelial compartment, `GPR183` up in myeloid/APC compartment, response module up, response normalizes in GSE282122 or GSE198520, and all margins exceed IFN/APC and generic inflammation comparators. Disease-level collapse first; no per-context rescue.

### 2. P2RX7 Purinergic-Inflammasome Stratification

Why it might escape previous blockers:

- Wave72 had the broadest orthogonal biochemical signal: purine/danger metabolite disturbance across AS, Crohn, RA, T1D, and UC, with treatment-normalizing hits.
- Wave73 found cross-disease cell-state support for a `P2RX7/IL1B/NLRP3/CASP1` module in Crohn, T1D, and UC.
- This is not a claim that `P2RX7` is generally causal. The only defensible version is a stratification route: antagonize only in purine-high, inflammasome-high samples.
- It avoids the MFGE8 safety-window trap because the forcing question is target-linked inflammatory response, not nonspecific debris uptake.

Why it likely fails:

- Wave73 specificity was zero against generic NF-kB/TNF, IFN/APC, and lysosome/APC comparators.
- MS module anchor failed or trended the wrong way.
- GSE282122 and RA response tests did not support expected responder biology.
- `P2RX7` gene-level target evidence was missing; Wave72 explicitly said the biochemical pattern lacks target-level convergence.
- Purine metabolomics is dirty. Without ATP/receptor/protein activity, it can be energy turnover, cell death, sample handling, or generic inflammation.

Local forcing test:

- Build a baseline stratifier from available metabolomics purine score plus local `P2RX7_inflammasome` expression score. Test whether the double-high subgroup shows treatment normalization or responder separation beyond generic NF-kB/TNF, IFN/APC, lysosome/APC, and disease severity covariates. If double-high does not beat all comparators after disease-collapse/permutation, close it.

### 3. SPNS1 Lysosomal Lysophospholipid-Efflux Route

Why it might escape previous blockers:

- Wave79 identified `SPNS1` as a recurrent accessible lysosomal membrane/transporter-like node across Crohn, Sjogren, and psoriasis, with APC/myeloid positives in Crohn and Sjogren.
- It sits closer to lipid-lysosomal handling than CD58/CD2, CD82, or generic inflammatory cytokines.
- Unlike cathepsins, MHC-II, complement, or `LIPA/LPL`, the route is not already exhausted by broad host-defense, antigen-presentation, systemic lipid, or complement prior-art blockers in the local artifacts.
- The intervention-first angle is not "drug SPNS1 tomorrow"; it is "force-test lysosomal lysophospholipid efflux as an upstream controller of the lipid-loader/APC state."

Why it likely fails:

- Wave79 still called it `NO_GO_TARGETABILITY_SHORTLIST_NODE`.
- No MS anchor, no target-resolved genetics, no perturbation/model support, and no chemical matter.
- It is probably another stress/lysosome marker unless a directional lipid-efflux phenotype is shown.
- It may be technically inaccessible: 12-transmembrane lysosomal transporter, no ChEMBL exact target, no obvious agonist/antagonist route.

Local forcing test:

- Use existing broad h5ad contrasts plus treatment-response tables to test whether `SPNS1` behaves as a controller rather than a marker: residualize against IFN/APC, generic inflammation, lysosome/APC, and lipid-loader scores; require retained `SPNS1` association with downstream lipid-loader/APC modules in at least two diseases and normalization in a responder dataset. If residual `SPNS1` vanishes, stop calling it a route.

## Not Selected

- `CD58/CD2`: better genetic/response evidence than most routes, but direction is conflicted and alefacept/CD2 prior art blocks novelty. It is an immune-synapse comparator, not an overlooked lipid-lysosomal route.
- `FABP5`: nominal MS white-matter up and a lipid-chaperone story, but Wave91 has weak response direction, UC negative direct signal, no genetics, no modality resolution, and no perturbation support.
- `MFGE8`: Wave108/109 reduced it to a local assay-design constraint. The model demands extreme debris-over-viable selectivity for even modest benefit.
- `CD82`: closed by Wave107. Marker/readout only.

## Recommended Next Local Move

Run the GPR183 spatial-proxy forcing test first. It is the only route here with a real intervention class, local response movement, and a mechanism that could sit upstream of the measured lipid-lysosomal APC state. Expect failure; the value is killing the last plausible GPCR/niche escape hatch cleanly.

