# Wave93 Hostile Review: GPR183/EBI2 Oxysterol-Niche Pivot

Returned: 2026-05-27

Role: hostile peer review of a possible `GPR183`/`EBI2` oxysterol-niche pivot
after `FABP5` was blocked by direct MS/EAE prior art. This is not a finding and
not a target promotion.

## Bottom Line

Do **not** promote `GPR183` as the next V3 translational claim. The pivot is
tempting because GPCR druggability and anti-TNF response signals look better
than many lipid-neighborhood nodes, but the hard gates fail:

- MS anchor is not reproduced in local MS white-matter microglia.
- The ligand/receptor/program coherence is broken across diseases.
- Target-resolution genetics are weak and not MS-centered.
- Disease breadth is mainly response/trafficking biology, not a coherent
  `CH25H/CYP7B1/HSD3B7/GPR183` niche.
- Foundation-model support is absent in the local GPR183 audit.
- Novelty is blocked by active GPR183 antagonist clinical and patent prior art
  in UC/lupus nephritis/RA/IBD.

The correct status is **PARK_AS_PRIOR_ART_BLOCKED_FORCING_TEST_ONLY**. Continue
only if the next package is explicitly an MS-spatial, ligand-measured,
target-engaged niche claim that is narrower than "GPR183 antagonism for
autoimmune inflammation."

## Local Evidence That Should Not Be Overvalued

Primary local source: `results_v3/wave74_gpr183_oxysterol_niche/REPORT.md`.

Wave74-B call was already `PARK_GPR183_OXYSTEROL_NICHE`, not promotion. The
integrated decision row had gate count `5`, but failed the decisive gates:

- `local_coherent_program_cross_disease = 0`
- `ligand_module_cross_disease = 0`
- `ms_support = 0`
- `oxysterol_like_metabolite_support = 0`
- `target_resolved_genetics_or_druggability = 0`
- `coherent_program_disease_count = 0`
- Wave62 `GPR183` call: `NO_GO_WAVE62_TARGET_RESOLUTION`, score `1.2409`

Wave83 then ranked `GPR183_EBI2_OXYSTEROL_NICHE` as the least-bad
intervention-class forcing route, but with missing gates:

- `ms_anchor`
- `genetic_or_target_resolution`
- `source_audit_not_promotional`

That is not a rescue. It is a warning that the route is druggable-looking but
still missing the evidence needed for a V3 claim.

## Failure Mode 1: MS Anchor Is Weak Locally

Local MS data do not support the pivot. In Wave74-B GSE111972 MS white-matter
microglia:

| Module | Mean effect | p | FDR | Interpretation |
|---|---:|---:|---:|---|
| `ligand_production_core` | `0.0711` | `0.247` | `0.495` | no MS ligand-program support |
| `gpr183_receptor_anchor` | `-0.136` | `0.664` | `0.744` | receptor not up; direction is slightly negative |
| `lymphoid_trafficking_response` | `-0.222` | `0.625` | `0.744` | no trafficking support |
| `myeloid_apc_migration_response` | `0.0857` | `0.491` | `0.744` | no myeloid migration support |
| `ifn_apc_comparator` | `0.337` | `0.00322` | `0.0129` | generic IFN/APC signal is present |
| `apc_lysosome_comparator` | `0.317` | `3.81e-06` | `3.05e-05` | APC/lysosome signal is present |

Concrete failure mode: the actual V3 MS tissue signal is IFN/APC and
APC/lysosome, not `GPR183`. If the orchestrator promotes GPR183 anyway, it is
implicitly substituting external EAE/MS lesion literature for local MS
replication.

External MS literature does show relevance, but it is not enough. `EBI2` is
reported as highly expressed in MS lesions and able to promote early CNS
migration of encephalitogenic CD4 T cells:

- Cell Reports article page:
  <https://www.sciencedirect.com/science/article/pii/S2211124717300578>
- Journal of Neuroinflammation review/experimental paper notes EBI2 is
  activated by `7alpha,25-dihydroxycholesterol` and references high MS-lesion
  expression: <https://jneuroinflammation.biomedcentral.com/articles/10.1186/s12974-017-1025-0>

Hostile interpretation: this is prior biological plausibility, not a V3 MS
anchor. It is also T-cell trafficking-heavy, whereas the V3 claim has been
myeloid/lipid-lysosomal/APC-centered.

## Failure Mode 2: Ligand/Receptor Coherence Is Broken

The pivot requires more than finding `GPR183` or oxysterol enzymes somewhere.
It requires a spatially coherent circuit:

`CH25H/CYP7B1` produce `7alpha,25-OHC` or related ligand, `HSD3B7` shapes the
gradient, and `GPR183`-positive immune cells respond in the same disease niche.

Verified ligand biology:

- `7alpha,25-OHC` is a ligand for EBI2/GPR183, synthesized through `CH25H` and
  `CYP7B1`, and metabolized by `HSD3B7`:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3465460/>
- Primary human macrophages can express EBI2 and ligand-production enzymes
  including `CH25H`, `CYP27A1`, and `CYP7B1`: PMID `24480442`,
  <https://pubmed.ncbi.nlm.nih.gov/24480442/>
- Brain vascular-cell paper summarizes the same ligand synthesis/degradation
  chain and EAE relevance:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC11856462/>

Local coherence failed anyway. Wave74-B coherent cell-state table showed zero
contexts where ligand production, direct `GPR183`, and response module all pass:

- T1D endothelial/stellate/ductal/acinar contexts had ligand signal but failed
  direct `GPR183` receptor anchor.
- IBD Crohn/UC myeloid contexts had `GPR183`/response support but failed ligand
  production.
- Sjogren stromal had response support but failed direct receptor anchor.
- Psoriasis APC had negative/weak receptor direction.

Concrete failure mode: the current evidence can be explained as generic
lymphoid/DC trafficking in inflamed tissue plus independent sterol-enzyme
signals, not as a measured oxysterol gradient acting through `GPR183`.

Minimum continuation requirement:

- Spatial transcriptomics or single-cell multiome in MS lesion edge and at least
  one non-MS autoimmune tissue showing same-neighborhood co-localization of
  ligand enzymes and `GPR183`-positive responder cells.
- Orthogonal LC-MS/MS or imaging-MS quantification of `7alpha,25-OHC` or
  agreed oxysterol feature in the same lesions.
- Do not count `EBI3` as EBI2/GPR183 support; Wave74 already treated it as a
  nomenclature control.

## Failure Mode 3: Genetics Are Too Weak

Wave74-B target-level evidence:

- `GPR183`: Wave62 score `1.2409`, `NO_GO_WAVE62_TARGET_RESOLUTION`.
- Strong L2G disease count `1`, disease `Psoriasis`.
- Relevant QTL colocalization disease count `0`.
- `wave72_broad_positive_disease_count = 2`, diseases `Crohn disease; Sjogren
  syndrome`.
- No Wave57 or Wave69d Geneformer presence.

Ligand enzymes did not rescue the target-resolution problem:

- `CH25H`: Wave62 score `1.3179`, `NO_GO_WAVE62_TARGET_RESOLUTION`, strong L2G
  disease only `UC`, no relevant QTL colocalization.
- `HSD3B7`: Wave62 score `1.3169`, `NO_GO_WAVE62_TARGET_RESOLUTION`, one
  relevant QTL coloc disease `Psoriasis`.
- `CYP7B1` and `CYP27A1`: no usable Wave62 support row in the Wave74 summary.

Concrete failure mode: this is not an MS genetic target. If the target is
promoted, it is being promoted as a pharmacologically accessible pathway with
expression/response suggestiveness, not as a target-resolved autoimmune locus.

Minimum continuation requirement:

- MS target-resolution evidence for `GPR183` or a ligand-enzyme node: high L2G,
  credible colocalized eQTL/sQTL/protein-QTL in relevant immune/CNS cell type,
  or an MR-like ligand/enzyme causal argument.
- Directional genetics: risk allele must predict increased GPR183/ligand-axis
  activity if antagonism is the proposed direction.

## Failure Mode 4: Disease Breadth Is a Trafficking/Response Artifact

Broad h5ad signals look better for response modules than for the actual
ligand-plus-receptor circuit:

- `ligand_production_core`: positive disease count `1` only, T1D.
- `gpr183_receptor_anchor`: positive disease count `3`, Crohn/Sjogren/UC, with
  a negative psoriasis APC trend.
- `lymphoid_trafficking_response`: positive disease count `4`.
- `myeloid_apc_migration_response`: positive disease count `4`.
- IFN/APC comparator: positive disease count `5`.
- APC/lysosome comparator: positive disease count `5`.

Concrete failure mode: the broadest signals are generic inflammatory/APC and
migration modules. The GPR183 receptor and ligand modules do not have matching
cross-disease breadth.

IBD/RA treatment response is also easy to overread:

- IBD GSE282122: strongest FDR row was mono/macrophage ligand-production
  remission-minus-nonremission (`FDR 0.000304`), but direct DC `GPR183`
  receptor response was only nominal (`p 0.0823`, `FDR 0.196`).
- RA GSE198520: lymphoid-trafficking module had paired and response support, but
  `GPR183` receptor anchor had paired p `0.923`, and good-vs-other FDR
  `0.180`.

Concrete failure mode: response signals may be measuring successful collapse of
inflammatory lymphoid/DC organization after anti-TNF, not target-specific
GPR183 pharmacology.

Minimum continuation requirement:

- Receptor-level response replication for `GPR183` itself after covariate
  adjustment, not only a module containing `CCR7`, `CCL19`, `CXCL13`, `LAMP3`,
  or other generic immune-trafficking genes.
- Demonstrate that GPR183 score adds predictive/biological information beyond
  IFN/APC, APC/lysosome, lymphoid aggregate, and generic inflammation scores.

## Failure Mode 5: Foundation-Model Evidence Is Absent

Wave74-B external target evidence says:

- `wave57_geneformer_present = False` for `GPR183`, `CH25H`, `CYP7B1`,
  `HSD3B7`, and `CYP27A1`.
- `wave69d_geneformer_present = False` for the same nodes.

Concrete failure mode: a pivot may be framed as "niche biology not captured by
single-gene deletion models." That may be true, but then foundation-model support
cannot be counted as a positive gate. It is missing, not unfavorable-but-irrelevant.

Minimum continuation requirement:

- A targeted in silico perturbation that models receptor antagonism or ligand
  gradient collapse in a relevant single-cell context, with adequate token
  support and a pre-specified remission/MS-lesion direction.
- Or drop the foundation-model gate explicitly and replace it with real
  target-engagement perturbation data.

## Failure Mode 6: Prior-Art Novelty Is Already Blocked

This is the hardest blocker. The broad autoimmune GPR183 antagonist story is no
longer novel.

Verified current public sources:

- ClinicalTrials.gov `NCT07535489`: Phase 2 IPG11406 in moderately to severely
  active ulcerative colitis, listed as an investigational oral drug targeting
  `GPR183`; last update posted 2026-04-17:
  <https://clinicaltrials.gov/study/NCT07535489>
- ClinicalTrials.gov `NCT06717815`: Phase Ib/IIa IPG11406 in lupus nephritis;
  record identifies IPG11406 as a `GPR183` antagonist:
  <https://clinicaltrials.gov/study/NCT06717815>
- ClinicalTrials.gov `NCT06255834`: IPG11406 Phase 1 healthy-volunteer record:
  <https://clinicaltrials.gov/study/NCT06255834>
- RA medicinal chemistry: "Discovery of a First-in-Class GPR183 Antagonist for
  the Potential Treatment of Rheumatoid Arthritis", PMID `38047891`:
  <https://pubmed.ncbi.nlm.nih.gov/38047891/> and ACS page
  <https://pubs.acs.org/doi/abs/10.1021/acs.jmedchem.3c01364>
- Patent `WO2024208303A1`, GPR183 inhibitors and autoimmune/IBD use:
  <https://patents.google.com/patent/WO2024208303A1/en>
- Patent `US11919895B2`, GPR183 antagonist IP space:
  <https://patents.google.com/patent/US11919895B2/en>

Concrete failure mode: saying "GPR183 antagonist for autoimmune/IBD/RA
inflammation" directly overlaps active clinical and patent estates. Druggability
is a liability here because it proves someone else has already moved the obvious
route into humans.

Minimum continuation requirement:

- A novelty delta narrower than active IPG11406/IBD/LN/RA prior art. Examples:
  MS lesion-edge biomarker stratification, CNS-specific exposure/PD, a biased
  modulator rather than antagonist, or a ligand-enzyme/spatial-gradient
  intervention not covered by GPR183 antagonist claims.
- Patent/literature clearance for that exact delta, not for the broad receptor.

## Failure Mode 7: Direction And Safety Are Under-Specified

The presumed direction is antagonism, because active clinical prior art uses an
oral GPR183 antagonist. But the V3 biology has not proven whether blocking
GPR183 is desirable in the relevant tissue state.

Possible contradictions:

- In MS/EAE literature, GPR183 can promote encephalitogenic CD4 T-cell CNS
  migration, supporting antagonism.
- In tissue repair and immune organization, disrupting cell positioning can have
  mixed consequences: impaired follicular/lymphoid organization, altered
  macrophage/DC localization, and unpredictable infection/vaccine-response
  effects.
- The V3 local signal is APC/lysosome and IFN-heavy; GPR183 antagonism may only
  change trafficking, not lipid-lysosomal repair.

Concrete failure mode: the route could reduce inflammatory cell positioning in
UC/LN while doing little for the MS myeloid lipid module, or could disrupt a
protective resolution niche.

Minimum continuation requirement:

- Ex vivo antagonism or genetic knockdown in human MS-relevant cells/tissue must
  show the intended direction: reduced pathogenic migration/APC activation
  without worsening myelin uptake, efferocytosis, lysosomal handling, or
  resolution markers.
- Include positive and negative controls: IPG11406 or a validated antagonist,
  inactive analog, ligand rescue with `7alpha,25-OHC`, and comparator IFN/APC
  blockade.

## Concrete Stop/Go Criteria

Stop now unless all of the following are obtained:

1. **MS spatial anchor:** active MS lesion or lesion-edge data show
   `GPR183`-positive immune cells adjacent to `CH25H/CYP7B1` ligand-producing
   cells, with quantifiable oxysterol enrichment.
2. **Receptor-level signal:** `GPR183` itself, not only a migration module,
   replicates in MS or a clearly analogous treatment-resistant autoimmune niche.
3. **Target engagement:** GPR183 antagonism or knockdown reverses the specific
   niche signature in primary human cells or tissue explants; ligand rescue
   restores the phenotype.
4. **Specificity:** effects remain after adjusting for IFN/APC, APC/lysosome,
   lymphoid aggregate, and generic inflammation scores.
5. **Genetic/causal support:** target-resolution or directional genetics support
   increased GPR183/ligand-axis activity as pathogenic in the intended disease.
6. **Prior-art delta:** the claim is not broad autoimmune GPR183 antagonism and
   is demonstrably distinct from IPG11406 UC/LN/RA/IBD patent and clinical
   programs.
7. **Safety/direction:** antagonism does not impair beneficial resolution,
   efferocytosis, myelin clearance, host defense, or vaccine-relevant immune
   positioning in the proposed treatment context.

## Final Peer-Review Call

`GPR183` is not a clean FABP5 replacement. It is druggable, but druggability is
the trap: the broad autoimmune receptor route is already clinically occupied,
while the local V3 data do not establish an MS-anchored, ligand-coherent,
genetically supported oxysterol niche.

Recommendation: **do not advance to target claim**. Keep only as a forcing-test
branch if the next work package is a narrowly defined MS spatial-lipid niche
experiment with target engagement and explicit prior-art differentiation.
