# Wave58-O Hostile Review: CXCR2 And IL7R Reopeners

Timestamp: 2026-05-27

Scope: hostile review of whether Wave57 reopeners `CXCR2` or `IL7R` can satisfy the V3 cross-autoimmune lipid-lysosomal myeloid-module DoD. Inputs reviewed: `results_v3/wave57_intervention_first_geneformer_screen/`, `CONVERGENCE_CHECK_18.md`, Wave56 `SP140`/`IL12A` reports, local prior-art/druggability artifacts, live Europe PMC/ClinicalTrials.gov/Google Patents searches.

## Verdict

Recommendation: **close both `CXCR2` and `IL7R` for V3 therapeutic promotion**. Keep `IL7R` only as a genetics/prior-art positive comparator or possible downstream stratification axis, and keep `CXCR2` only as a neutrophil-chemotaxis comparator. Neither branch currently has a defensible route to the V3 DoD because the Geneformer evidence is a weak single-context triage signal, both fail strict MS local support, neither sits in the lipid-lysosomal myeloid neighborhood, neither has efferocytosis support, and both are heavily prior-arted.

If the orchestrator needs a one-line decision: **pivot away from both; do not spend integration cycles trying to turn either into `FINDING_V3` unless Wave58-M/N return new target-resolved, cell-specific evidence that is stronger than the current local package.**

## Local Evidence Snapshot

| Gate | `CXCR2` | `IL7R` |
| --- | --- | --- |
| Wave57 call | `REOPEN_MODEL_SUPPORTED_INTERVENTION_FIRST` | `REOPEN_MODEL_SUPPORTED_INTERVENTION_FIRST` |
| Critical gates passed | 3/5 | 3/5 |
| Geneformer support | 1/11 contexts; `IBD_myeloid`; only 3 disease cells with token | 1/11 contexts; `ra_myeloid_dendritic`; 12 disease cells with token |
| Best Geneformer z / projection-minus-random | 1.197 / 0.0288 | 0.529 / 0.0318 |
| Cross-disease Open Targets genetics | AS, Crohn, psoriasis, RA, UC; MS genetic score 0 | AITD, Crohn, MS, PBC, psoriasis, SLE, T1D; MS genetic score 0.789 |
| Local broad positives | Crohn, psoriasis, UC | Crohn, T1D, UC |
| Strict MS white-matter anchor | Failed: delta 0.830, p 0.378, FDR 0.914 | Failed: delta -0.654, p 0.572, FDR 0.943 |
| Lipid-lysosomal myeloid neighborhood | False | False |
| Residual/covariate support | No `CXCR2` retained residual row in reviewed summary | Retained positives in 2 diseases, but only 1 strict core-covariate disease: UC stromal |
| Efferocytosis screen | UNRESOLVED; median efficient-minus-noneater 0.192, FDR 0.997 | UNRESOLVED/wrong direction; median efficient-minus-noneater -0.155, FDR 1.0 |

## Criticism 1: Geneformer Is A Weak Operationalization Here

Wave57 is explicitly a triage screen, not a causal perturbation. In this specific case it is weaker than usual.

- The intervention being tested is not the intervention proposed. Token deletion from a rank-encoded transcriptome is not receptor antagonism, ligand blockade, receptor occupancy, internalization, Fc biology, or chronic pathway modulation.
- Support is single-context only for both candidates. `CXCR2` is supported only in `IBD_myeloid`; `IL7R` only in `ra_myeloid_dendritic`.
- `CXCR2` support rests on only 3 disease cells containing the token. That is too few to distinguish a real state from rare-cell composition, donor idiosyncrasy, neutrophil carryover, or doublets.
- `IL7R` has 12 token-positive disease cells in the supported RA myeloid dendritic context, but it is token-not-detected in most other contexts and has no MS-context support.
- The effect sizes are tiny embedding shifts. `CXCR2` moved mean shift-to-control cosine by 0.000738 versus random -0.000213; `IL7R` by 0.000209 versus random -0.000112. These are not interpretable as biological rescue magnitudes.
- The random baseline used only 3 random repetitions and no donor-blocked bootstrap. This does not protect against the main failure mode: rare cells from one donor or one subcluster driving apparent control-centroid movement.
- The Wave57 support threshold is permissive: one strong context is enough for `model_support_pass`. A hostile reviewer would call that hypothesis generation, not foundation-model perturbation evidence.

Falsification criterion: rerun with donor-blocked resampling, leave-one-donor-out centroids, higher random repetitions, and minimum token-positive cell count >=25 per context. If either candidate loses support or remains single-context only, the Geneformer branch is falsified for V3 use.

## Criticism 2: Cell-Composition Artifacts Are More Plausible Than Mechanism

### `CXCR2`

`CXCR2` is primarily a neutrophil/chemokine-trafficking receptor in this disease framing. The local positives are exactly the compartments where neutrophil infiltration, epithelial chemokine response, or inflamed-tissue composition could dominate: Crohn myeloid, UC myeloid, and psoriasis keratinocyte/skin contexts. A 3-cell Geneformer signal in IBD myeloid is especially compatible with rare CXCR2+ neutrophil-like cells rather than macrophage-state control of lipid-lysosomal pathology.

This matters because the V3 mechanism is not "fewer neutrophils enter inflamed tissue." It is supposed to resolve a shared lipid-lysosomal inflammatory myeloid state. A neutrophil migration receptor can be upstream of inflammation, but the local package does not show that it controls lysosomal lipid handling, efferocytosis, myelin/debris processing, or lesion-rim macrophage behavior.

Falsification criterion: reannotate CXCR2+ cells with neutrophil markers (`S100A8`, `S100A9`, `CXCR1`, `FCGR3B`, `MPO`, `ELANE`) and doublet scores; rerun donor-level pseudobulk after excluding neutrophil-like cells. If the CXCR2 disease signal disappears or becomes a neutrophil fraction covariate, close the branch.

### `IL7R`

`IL7R` is canonical lymphocyte biology. The RA myeloid dendritic Geneformer signal could reflect lymphoid contamination, T-cell/APC doublets, shared inflammatory context, or a migratory DC subset carrying lymphocyte-associated transcripts. The local residual support is mostly IBD, and the one strict covariate-surviving disease is UC stromal, not a myeloid lipid-lysosomal state. The broad local positives do not establish per-cell myeloid mechanism.

The strongest biological case for `IL7R` in MS is genetic and T-cell/splicing biology, not lesion-rim lipid processing. That is a legitimate autoimmune axis, but it is not the V3 lipid-lysosomal myeloid module unless new spatial or perturbation data connects IL7R signaling to myeloid lipid/debris handling.

Falsification criterion: use CITE-seq/spatial or strict scRNA reannotation to verify CD127 protein/transcript in the disease-associated APC/myeloid cells. If `IL7R` signal maps to T cells, stromal cells, doublets, or composition rather than APC-intrinsic expression, close the branch for V3 mechanism.

## Criticism 3: Target-Resolved Genetics Do Not Save Either Branch

### `CXCR2`

`CXCR2` has Open Targets genetic breadth in AS/Crohn/psoriasis/RA/UC but **no MS genetic anchor** in Wave55 (`ms_genetic_association = 0.0`). It also lacks coloc/MR-grade target resolution in the artifacts reviewed. Because the locus is embedded in chemokine-receptor/chemokine inflammatory biology, disease association cannot be assumed to mean `CXCR2` antagonism is the causal intervention.

Minimum genetics needed to reopen: at least four disease coloc/MR results linking `CXCR2` expression/protein to disease with consistent direction, plus MS or MS-endophenotype support. Current evidence is far below that.

### `IL7R`

`IL7R` has a much stronger genetics story, including MS. But that is not enough for the V3 claim. The likely causal axis is IL-7 receptor biology in adaptive immune cells and soluble/membrane receptor regulation, not the lipid-lysosomal myeloid state. Cross-disease Open Targets breadth does not prove a shared causal mechanism across MS, IBD, T1D, psoriasis, SLE, PBC, and AITD.

Minimum genetics needed to reopen for V3: disease colocalization of the same IL7R molecular trait with MS and at least three other autoimmune diseases, directionally tied to the proposed intervention, and shown in the cell type being claimed. A T-cell IL7R splicing/eQTL mechanism would support an adaptive-immune stratification claim, not a lipid-lysosomal myeloid central-node claim.

## Criticism 4: Prior Art Is Blocking, Not Incidental

### `CXCR2`

The prior-art lane is crowded and directly overlaps MS/demyelination:

- Literature: `Inhibition of CXCR2 signaling promotes recovery in models of multiple sclerosis` is direct preclinical MS/demyelination prior art.
- Literature: `CXCR2-positive neutrophils are essential for cuprizone-induced demyelination: relevance to multiple sclerosis` is direct neutrophil/CXCR2 demyelination prior art.
- Literature/chemistry: `Discovery of CNS Penetrant CXCR2 Antagonists for the Potential Treatment of CNS Demyelinating Disorders` is direct CNS-penetrant CXCR2 antagonist prior art for demyelinating disorders.
- Patent: `US9809581B2`, "Inhibitors of CXCR2", is active small-molecule CXCR2 inhibitor chemical matter.
- Patent: `WO2019136370A3`, "Methods of treating generalized pustular psoriasis with an antagonist of CCR6 or CXCR2", directly overlaps psoriasis/neutrophil inflammatory disease.
- Local V3 prior runs already treated CXCR2/SB-225002 L1000 reversal as `NO_GO_PRIOR` or `NO_GO_L1000_ONLY_CONTROLLER` because it was generic/prior-art inflammatory targeting rather than a selective transition controller.

Novelty remaining would have to be extremely narrow, e.g. a biomarker-defined CXCR2+ neutrophil-high subgroup in an autoimmune tissue. That is not the V3 central lipid-lysosomal myeloid mechanism.

### `IL7R`

The prior-art lane is even more direct:

- ClinicalTrials.gov: `GSK2618960` anti-IL7R-alpha/CD127 was tested in healthy volunteers and relapsing-remitting MS (`NCT01808482`), healthy volunteers (`NCT02293161`), and planned/withdrawn in primary Sjogren syndrome (`NCT03239600`).
- ClinicalTrials.gov: `OSE-127`/lusvertikimab was evaluated in moderate-to-severe UC (`NCT04882007`) and healthy subjects (`NCT03980080`).
- OSE Immunotherapeutics describes lusvertikimab as a humanized CD127/IL7R-alpha antagonist with Phase 2 UC clinical data.
- Patent: `WO2010017468A1`, "Treatment of autoimmune and inflammatory disease", covers anti-CD127/anti-IL7 or IL7R antagonist treatment of autoimmune/inflammatory disease.
- Patent: `US12371502B2`, "Antibodies directed against CD127", covers anti-human CD127 agents antagonizing IL-7R signaling.
- Recent meeting/pipeline signal: JNJ-67484703 has a phase II proof-of-biology report in RA, UC, and Sjogren disease.
- Local Wave21 prior-art review already demoted `IL7R` because anti-IL7R-alpha/CD127 blockade is UC clinical prior art via lusvertikimab/OSE-127.

Generic "block IL7R/CD127 in autoimmunity" is therefore not novel. A V3 continuation would need a non-obvious stratification or dosing/combination hypothesis with a clear delta over GSK2618960/OSE-127/JNJ-67484703.

## Criticism 5: Poor Connection To The Lipid-Lysosomal Myeloid Mechanism

Both rows explicitly have `in_lipid_lysosomal_myeloid_neighborhood = False` in Wave57.

`CXCR2` can plausibly modulate inflammatory-cell recruitment, especially neutrophils. That is not the same as controlling lysosomal lipid handling, myelin-debris clearance, efferocytosis, antigen-presentation burden, or chronic active lesion-rim macrophage/microglia state. Its efferocytosis screen is unresolved and not FDR-supported.

`IL7R` can plausibly modulate adaptive immune survival/migration and maybe stromal/lymphoid crosstalk. The local `IL7R` top retained tests include UC myeloid `lipid_loader_repair`, `c1q_phagocytic_myeloid`, and `hla_ii_apc`, but this is coexpression/covariate evidence, not pathway control. The efferocytosis screen is unresolved and directionally unfavorable.

Falsification criterion for both: perturb the target in disease-relevant human primary cells or tissue explants and require >=0.5 SD reduction of the V3 lipid-lysosomal inflammatory myeloid module without reducing phagocytosis/efferocytosis or inducing toxicity. If the effect is only decreased neutrophil/T-cell migration, generic STAT5 suppression, or broad inflammatory marker movement, it does not satisfy V3.

## Branch-Specific Falsification Paths

### `CXCR2`

Close if any of the following occur:

- Donor-blocked Geneformer rerun loses the single IBD-myeloid support context.
- CXCR2+ cells are neutrophil-like or doublets rather than macrophage/APC cells after marker reannotation.
- The Crohn/UC/psoriasis signal is explained by neutrophil fraction or epithelial chemokine response after covariate adjustment.
- Fine-mapping/colocalization does not resolve disease signals to `CXCR2` expression/protein, especially with no MS support.
- CXCR2 antagonists reduce neutrophil chemotaxis but fail to shift lipid-lysosomal myeloid module scores by >=0.5 SD in myelin-debris/IFNG/TNF human macrophage, microglia-like, or gut/skin explant assays.
- Prior-art search confirms the proposed use is just CXCR2 blockade for demyelination, psoriasis, IBD, or inflammatory neutrophil recruitment.

Continue only if all of the following are true: target-resolved genetics emerges, spatial data places CXCR2+ cells at the disease-driving compartment, intervention changes lipid-lysosomal myeloid state independently of cell recruitment, and the proposed claim has a novel patient-stratified delta over existing demyelination/CXCR2 literature. Probability from current evidence: low.

### `IL7R`

Close if any of the following occur:

- The RA myeloid dendritic Geneformer support disappears under donor-blocked rerun or stricter token/cell thresholds.
- CD127 protein/transcript is not robustly present in the claimed APC/myeloid cell state.
- Colocalization shows the disease genetics is T-cell IL7R splicing/expression rather than myeloid lipid-lysosomal control.
- Anti-CD127 perturbation changes T-cell STAT5/migration but does not reproducibly shift myeloid lipid-loader/lysosomal/efferocytosis modules.
- OSE-127/GSK2618960/JNJ-67484703 prior art covers the proposed autoimmune use.
- The only viable claim becomes "IL7R blockade in UC/MS/Sjogren/RA", which is already a clinical/patent lane.

Continue only as a non-V3-central comparator or as a stratification hypothesis: IL7R genotype/soluble receptor/protein state predicting response to existing anti-CD127 programs. That could be useful, but it is not a novel lipid-lysosomal myeloid therapeutic mechanism.

## Final Recommendation

`CXCR2`: **close for V3 promotion**. It is intervention-tractable but mechanistically wrong for the module, MS-genetics negative, likely composition-driven, and direct demyelination/CXCR2 prior art exists.

`IL7R`: **close for V3 promotion; retain as comparator/stratification only**. It has real autoimmune genetics and real clinical modality, but it is canonical adaptive immune biology with direct anti-CD127 prior art and no demonstrated control over the V3 lipid-lysosomal myeloid state.

Next orchestration move: pivot to a candidate with target-specific evidence inside the lipid-lysosomal/efferocytosis/debris-handling program, or reformulate the V3 claim away from this module. Do not let a one-context Geneformer hit resurrect generic inflammatory targets.

## Search Log And Source Pointers

Local trace files reviewed:

- `results_v3/wave57_intervention_first_geneformer_screen/wave57_intervention_first_candidate_calls.tsv`
- `results_v3/wave57_intervention_first_geneformer_screen/wave57_geneformer_metrics.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv`
- `results_v3/wave31_dynamic_transition_controller_audit/dynamic_transition_controller_audit.tsv`
- `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
- `subagents_v3/wave21_residual_candidate_prior_art.md`
- `subagents_v3/wave56j_sp140_genetics_prior_art.md`
- `subagents_v3/wave56k_sp140_perturbation_druggability.md`
- `subagents_v3/wave56l_il12a_comparator_prior_art.md`

Live external searches run:

- Europe PMC: `(CXCR2 OR "C-X-C motif chemokine receptor 2" OR "IL-8 receptor B") AND (autoimmune OR autoimmunity OR inflammation OR "multiple sclerosis" OR Crohn OR "ulcerative colitis" OR psoriasis OR rheumatoid)`, hitCount `17541`.
- Europe PMC: `(IL7R OR "IL-7 receptor alpha" OR CD127) AND (autoimmune OR autoimmunity OR inflammation OR "multiple sclerosis" OR Crohn OR "ulcerative colitis" OR psoriasis OR Sjogren OR "type 1 diabetes" OR rheumatoid)`, hitCount `19446`.
- ClinicalTrials.gov API: `OSE-127` -> `NCT04882007`, `NCT03980080`.
- ClinicalTrials.gov API: `GSK2618960` -> `NCT01808482`, `NCT02293161`, `NCT03239600`.
- ClinicalTrials.gov API: `CXCR2 OR navarixin OR danirixin OR AZD5069 OR reparixin` -> examples included reparixin COVID/T1D and GSK1325756 first-in-human records, confirming mature CXCR1/2/CXCR2 clinical chemical matter even if not the V3 autoimmune indication.
- Google Patents queries: `CXCR2 antagonist autoimmune multiple sclerosis patent`, `CXCR2 antagonist psoriasis patent`, `anti CD127 IL7R antibody autoimmune patent`, `OSE-127 patent IL7R antagonist`.

Key external pointers:

- CXCR2/MS prior art: https://pmc.ncbi.nlm.nih.gov/articles/PMC2761527/
- CXCR2/cuprizone demyelination prior art: https://pmc.ncbi.nlm.nih.gov/articles/PMC2827651/
- CNS-penetrant CXCR2 antagonists for demyelinating disorders: https://pubmed.ncbi.nlm.nih.gov/27096048/
- CXCR2 inhibitor patent: https://patents.google.com/patent/US9809581B2/en
- CXCR2/CCR6 antagonist generalized pustular psoriasis patent: https://patents.google.com/patent/WO2019136370A3/en
- GSK2618960 anti-IL7R-alpha clinical paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC6339973/
- GSK2618960 RRMS/healthy-volunteer trial: https://clinicaltrials.gov/study/NCT01808482
- OSE-127/lusvertikimab UC trial: https://clinicaltrials.gov/study/NCT04882007
- OSE lusvertikimab product/clinical-data page: https://www.ose-immuno.com/nos-produits/ose-127/
- Anti-CD127 autoimmune/inflammatory patent: https://patents.google.com/patent/WO2010017468A1/en
- CD127 antibody patent: https://patents.google.com/patent/US12371502B2/en
- JNJ-67484703 RA/UC/Sjogren proof-of-biology abstract: https://academic.oup.com/rheumatology/article/doi/10.1093/rheumatology/keag121.151/8663558
