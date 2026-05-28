# Wave94 Hostile Critique After Waves 88-93

Timestamp: 2026-05-27 20:09 CEST

Scope: hostile sidecar review of the V3 trajectory after Wave88-Wave93. Assumption for this critique: the lipid-loader/lysosomal myeloid module is a real disease-state signature. The question is whether the current operationalizations can convert that signature into a therapeutic-relevant target or intervention point.

## Bottom-Line Verdict

The current trajectory is scientifically disciplined but still target-discovery weak. Waves 88-93 repeatedly show that the module exists, then fail when asked to identify a causal, druggable, MS-anchored controller. The failure mode is not just "wrong target"; it is a repeated operationalization error: treating expression, response association, or route membership as if it were evidence of controllability.

Do not run another marker-to-target scan unless it explicitly tests causal direction, residualizes away generic inflammatory/composition axes, and validates perturbation direction against a real perturbation dataset. The next computation should either identify a transition controller or demote the module to a stratification phenotype.

## Attack on Operationalizations

### 1. State Marker Is Still Being Confused With State Controller

Wave90 correctly parks `LPL` after showing it is MS white-matter-up and anti-TNF nonresponse-high across IBD/RA/psoriasis, but the branch still treated lipid-loader neighborhood genes as plausible controllers in Wave91. That is too permissive. A gene being high in a lipid-loaded macrophage does not imply that inhibiting or activating it will move the cell out of the pathogenic state.

Examples:

- `LPL`: strong psoriasis adalimumab signal, but targetability and disease-vs-control contradictions make it a marker.
- `FABP5`: stronger local controller-looking signal, but prior-art blocked and still directionally inconsistent.
- `GPR183`: druggable receptor route, but Wave93 fails the core biology gates: no MS receptor anchor, no ligand-production anchor, no coherent ligand/receptor/response context.

The current route scoring has too much "co-membership in a plausible biological neighborhood" and too little perturbational proof.

### 2. Bulk/Tissue Response Is a Weak Proxy for a Spatial Cell-State Mechanism

Wave88 improved rigor by showing the inflammatory anti-TNF circuit adds almost no value beyond tissue-composition and generic inflammation proxies. That should have forced a stronger redesign. Instead, subsequent waves still lean heavily on pretreatment bulk tissue response associations:

- IBD mucosa anti-TNF response.
- RA synovium anti-TNF response.
- Psoriasis lesional skin adalimumab response.

These are not independent tests of a lipid-lysosomal myeloid transition. They are inflamed tissue readouts with different disease biology, different clinical endpoints, different cell mixtures, and different treatment contexts.

The core mechanistic question is spatial and cell-resolved: which controller drives persistence of lipid-loaded inflammatory myeloid cells in damaged tissue? Bulk response does not answer that.

### 3. MS Anchoring Is Still Too Thin

The MS anchor is dominated by `GSE111972` bulk white matter contrasts and derived module scores. That is useful but insufficient for a V3 therapeutic claim.

Specific weaknesses:

- `LPL` is MS white-matter-up, but its gene-level FDR in Wave90 is `0.7144`; the module is significant, the gene is not.
- `FABP5` has a nominal MS anchor and prior-art support, but that makes it not novel.
- `GPR183` fails the MS receptor anchor directly in Wave93.
- Controller routes in Wave92 mostly fail because the strongest response-associated routes do not have MS white-matter support.

The trajectory needs an MS lesion-compartment or MS myeloid-cell anchor, not only bulk white matter. If `data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad` cannot provide that, the branch should admit the MS evidence is mostly bulk-tissue disease-state evidence.

### 4. Evidence Channels Are Less Independent Than They Look

The current convergence map overcounts independence.

Not fully independent:

- Broad h5ad disease-vs-control contrasts and bulk response signatures both reflect inflammatory tissue composition.
- Module gene scans, lipid-neighborhood scans, and route scans reuse overlapping gene sets and biological priors.
- IBD response datasets share treatment class and mucosal inflammation structure.
- Geneformer deletion rows, where available, are not independent biological evidence unless validated against real perturbation data.

Actual independent evidence would be: cell-resolved residual state association, genetic colocalization or validated causal instrument, real perturbation effect, treatment-response specificity after proxy adjustment, and target-level druggability/prior-art audit.

The current work often has three views of the same tissue-state axis, not three independent modalities.

### 5. Foundation-Model Usage Is Not Claim-Grade

Geneformer embedding movement has been used as a weak directional screen. That is not enough for the V3 foundation-model requirement.

Problems:

- Token coverage is incomplete, so missing genes silently bias candidate selection.
- Embedding movement toward a control or remission centroid is not equivalent to a perturbation prediction with calibrated effect size.
- There is limited validation against real perturbation outputs.
- State/Stack/Evo-style perturbation or sequence-regulatory predictions are not yet integrated into the current Waves 88-93 logic.

Foundation-model evidence should be treated as hypothesis generation only until it predicts a quantitative perturbation effect that matches a real perturbation dataset.

### 6. Treatment-Response Results Are at High Risk of Overfitting

Wave89 psoriasis is especially fragile:

- Adalimumab evaluable baseline subjects: `14`.
- Nonresponders: `5`.
- `LPL` has a large effect, but FDR across tested genes is `0.4998`.

Wave88 already showed that an apparently strong inflammatory circuit collapses after proxy adjustment. The same hostile adjustment standard must be applied to `LPL`, lipid-loader modules, and later candidates before they are allowed to influence target choice.

The anti-TNF response branch is useful only if it answers: "does this state predict anti-TNF nonresponse beyond generic inflammation, tissue damage, cell composition, and disease severity?" For Wave88, the answer was no for the inflammatory circuit. That failure should be generalized as a warning, not treated as isolated.

### 7. Prior-Art Logic Is Being Applied Too Late

Wave92 appropriately blocks `FABP5`, but only after it became the top local controller. This wastes cycles and invites confirmation bias.

Prior art should be a first-class filter before deepening any target branch, especially for:

- obvious lipid enzymes and binding proteins,
- PPAR/LXR pathways,
- IL1/TNF/TREM/OSM inflammatory routes,
- GPR183/EBI2 and other named immune GPCRs,
- efferocytosis receptors with autoimmune/EAE literature.

Also, API failure must never be interpreted as absence of prior art. Wave93 recorded PubMed/ChEMBL DNS failures in the report; the GPR183 no-go did not rely on those fields, which is correct. But no positive novelty claim can be made from a run with failed literature/druggability APIs.

## What Survives the Attack

The following statements survive:

- A lipid-loader/lysosomal myeloid state is repeatedly visible across MS and several autoimmune tissue contexts.
- The state is associated with anti-TNF nonresponse in some external tissue datasets, but current evidence does not prove treatment specificity.
- Direct module genes are mostly markers, prior-arted, not safely druggable, or directionally unstable.
- Route-level biology points toward lipid handling, lysosomal processing, efferocytosis, and tissue damage response, but no route has yet passed MS anchoring plus perturbational direction plus druggability plus novelty.

The correct next question is not "which module gene is highest?" It is "which perturbable mechanism moves cells out of the residual lipid-lysosomal myeloid state after generic inflammation and composition are removed?"

## Next Pivot 1: Residualized Cell-State Transition Controller

### Hypothesis

The lipid-loader/lysosomal myeloid module is maintained by a smaller transition-controller program that remains associated with disease after removing generic inflammation, HLA/APC, IFN, neutrophil, stromal, epithelial, and cell-composition proxies. A valid controller should be visible across multiple tissues and supported by perturbation evidence.

### Exact Local Artifacts To Consume

Core disease-state inputs:

- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
- `results_v3/direct_h5ad_cell_state/direct_h5ad_donor_module_scores.tsv`
- `results_v3/direct_h5ad_cell_state/direct_h5ad_donor_module_comparisons.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/gse111972_module_contrasts.tsv`

Cell-resolved source data:

- `data/raw_v3/wave67_gse282122_myeloid/myeloid_final.h5ad`
- `data/raw_v3/cell_state/ibd_human_10x.h5ad`
- `data/raw_v3/cell_state/psoriasis_skin.h5ad`
- `data/raw_v3/cell_state/sjogren_salivary.h5ad`
- `data/raw_v3/cell_state/ra_binvignat_blood.h5ad`
- `data/raw_v3/cell_state/t1d_hpap_islet.h5ad`

Perturbation/foundation checks:

- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave57_intervention_first_geneformer_screen/wave57_geneformer_gene_summary.tsv`
- `results_v3/geneformer_pivot_panel_delete/geneformer_pivot_panel_gene_summary.tsv`
- `results_v3/wave79_targetability_shortlist_audit/targetability_qtl_coloc_summary.tsv`

### Computation

Use donor-level pseudobulk within matched cell classes. Build a residual lipid-lysosomal state score after regressing out generic inflammation, IFN/APC, HLA-II, neutrophil, stromal/ulceration, epithelial depletion, and dataset/cell-type effects. Then rank genes/regulons whose expression predicts the residual state across tissues.

Do not rank genes by disease-vs-control expression alone. Rank by cross-disease residual association plus perturbation support.

### Promotion Criteria

Promote a candidate only if all of the following pass:

- Same-direction residual association with the lipid-lysosomal state in at least three autoimmune tissues, including at least one myeloid/APC context.
- MS anchor in either `GSE111972` or `GSE282122` myeloid cells after generic module adjustment.
- Real perturbation evidence or credible foundation-model perturbation predicts movement away from the disease-state centroid with effect size at least `0.3` SD in the intended direction.
- The candidate is not merely a module member, HLA/IFN/inflammatory marker, or cell-abundance proxy.
- Targetability and prior-art screen do not immediately block the route.

### Failure Criteria

Fail the pivot if:

- top candidates disappear after residualization,
- same candidate is not seen in MS and at least two non-MS autoimmune tissues,
- perturbation evidence is absent or directionally opposite,
- candidates are only generic inflammatory markers,
- foundation-model evidence cannot be validated against real perturbation data.

### Why This Is Worth Doing

This directly addresses the main operationalization defect. It treats the lipid-loader module as a state to explain, not a gene list to mine.

## Next Pivot 2: Receptor-Specific Lipid/Efferocytosis Checkpoint Forcing Test

### Hypothesis

The module may reflect failed clearance/resolution rather than lipid metabolism per se. A receptor-specific lipid/efferocytosis checkpoint, especially within the `CD300`/`FPR2`/related resolution axis, could control persistence of the state without directly modulating systemic lipid enzymes. The route-level Wave92 audit is too aggregated; receptor-specific direction must be tested.

### Exact Local Artifacts To Consume

Route-level evidence:

- `results_v3/wave92_lipid_state_controller_route_audit/controller_route_rank.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/external_ibd_controller_route_response_tests.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/ra_controller_route_response_tests.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/psoriasis_controller_route_response_tests.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/broad_h5ad_route_context_tests.tsv`
- `results_v3/wave92_lipid_state_controller_route_audit/ms_white_matter_controller_route_support.tsv`

Prior route scans:

- `results_v3/wave48_resolution_reopener_audit/route_reopener_audit.tsv`
- `results_v3/wave48_resolution_reopener_audit/candidate_gene_evidence.tsv`
- `results_v3/wave48_resolution_reopener_audit/decision_matrix.tsv`
- `results_v3/wave48_resolution_reopener_audit/patent_search_urls.tsv`

Perturbation and targetability:

- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave79_targetability_shortlist_audit/targetability_broad_context_rows.tsv`
- `results_v3/wave79_targetability_shortlist_audit/targetability_ms_white_matter_rows.tsv`
- `results_v3/wave79_targetability_shortlist_audit/targetability_qtl_coloc_summary.tsv`

### Computation

Decompose aggregated routes into individual receptor/ligand candidates. For `CD300`, do not treat the family as one target; test `CD300A`, `CD300C`, `CD300E`, `CD300F`, `CD300LF`, `CD300LB`, and `CD300LG` separately. For resolution biology, test `FPR2`, `ANXA1`, ligand/resolvin-adjacent genes, and efferocytosis comparators.

For each receptor-specific candidate:

- test MS anchor in white matter and available MS myeloid data,
- test cross-disease residual association after generic inflammation adjustment,
- test anti-TNF response direction in IBD/RA/psoriasis,
- test ligand/receptor coherence within the same tissue contexts,
- intersect with real efferocytosis perturbation rows where possible,
- run prior-art and clinical/patent search before promotion.

### Promotion Criteria

Promote only if one specific receptor or ligand satisfies:

- MS anchor is positive after adjustment, not only route-average support.
- Same-direction signal in at least two non-MS autoimmune diseases.
- Ligand/receptor context is coherent in the same tissue and cell class.
- Perturbation data support the intended direction of modulation.
- Druggability is receptor-specific and plausible with antibody, agonist, antagonist, or biased agonist format.
- Prior art does not already claim the same receptor-specific autoimmune/MS intervention.

### Failure Criteria

Fail the pivot if:

- route signal is driven by family aggregation,
- receptor-specific directions conflict,
- MS anchor remains absent,
- the strongest evidence is only IBD anti-TNF response,
- prior art already covers the receptor-specific autoimmune use,
- perturbation data do not support efferocytosis/resolution rescue.

### Why This Is Worth Doing

This is the strongest remaining mechanistic branch that is not just another lipid-enzyme scan. It has plausible biology, druggable receptor formats, and a direct path to falsification. It also has a high chance of failure, which is acceptable; a clean failure would prevent further recycling of "resolution/efferocytosis" language without target-level evidence.

## Explicit No-Go Recommendations

Do not promote any of the following from current evidence:

- `LPL` as a target.
- `FABP5` as a novel MS target.
- `GPR183` as a cross-autoimmune lipid-lysosomal controller.
- `IL1B`, `LAMP3`, `TREM1`, `CXCL8`, or `OSM` as V3 novelty targets.
- broad `PPAR`, `LXR`, or systemic lipid metabolism modulation without tissue-selective mechanism.

Do not count Geneformer centroid movement as foundation-model validation unless it is compared against real perturbation data.

Do not claim cross-autoimmune therapeutic convergence from anti-TNF response associations alone.
