# Wave60-P C15ORF48/MOCCI Circuit Audit

Date: 2026-05-27

Scope: audit whether `C15ORF48`/MOCCI and the `C15ORF48`/`NDUFA4` complex-IV switch can anchor the cross-autoimmune lipid-lysosomal myeloid module as a circuit-level mechanism with a tractable intervention point.

## Verdict

**Assay-only.**

`C15ORF48` is a strong recurrent inflammatory-state marker with a real external mechanism: the `C15ORF48` locus can produce MOCCI and miR-147b, and both connect to `NDUFA4`/complex-IV remodeling and inflammatory restraint. That is enough to build a falsifiable circuit assay.

It is **not promotable** as a therapeutic anchor now. Locally, `C15ORF48` recurrence is stronger than the actual `C15ORF48`-up/`NDUFA4`-down switch. The canonical switch appears in only 1 of 17 tested compartments, and the positive `C15ORF48` signal often lacks reciprocal `NDUFA4` suppression. Direct modulation is also directionally ambiguous and poorly druggable. The honest use is as a mechanistic readout and perturbation gate for mitochondrial inflammatory adaptation, not as a target claim.

## Local Evidence Summary

### Expression Recurrence

- Broad h5ad ranking places `C15ORF48` at rank-line 13 with 17 tested compartments, 4 positive compartments, 0 negative compartments, 2 FDR10 positives, 3 positive diseases (`Crohn disease`, `type 1 diabetes mellitus`, `ulcerative colitis`), best p `2.948e-05`, best FDR `0.0287`, max delta `4.446`, median positive Hedges g `2.192`, and MS white-matter delta `1.223`, p `0.00375`, FDR `0.834` in `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv:13`.
- The unranked gene summary gives the same `C15ORF48` support and explicitly flags it **not** in the predefined lipid-lysosomal myeloid neighborhood in `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv:5576`.
- `NDUFA4` is much weaker locally: 17 tested compartments, 2 positives, 0 FDR10 positives, 1 positive disease (`Sjogren syndrome`), best p `0.00648`, FDR `0.841`, MS white-matter delta `0.126`, p `0.226`, FDR `0.899` in `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv:3417` and `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv:15471`.

### Switch-Specific Test

- The dedicated switch audit tested 17 compartments and called: 7 `no_switch_signal`, 5 `c15_up_no_ndufa4_up`, 3 `ndufa4_up_without_c15`, 1 `both_up_not_switch`, and only 1 `canonical_switch_c15_up_ndufa4_down` in `results_v3/wave20_c15orf48_ndufa4_switch/summary.json:2-10`.
- The only canonical switch was Crohn colon myeloid: `C15ORF48` delta `3.882`, p `0.000614`, FDR `0.0848`; `NDUFA4` delta `-0.292`, p `0.0794`, FDR `0.4565`; switch delta `4.174` in `results_v3/wave20_c15orf48_ndufa4_switch/summary.json:13-35` and table line `results_v3/wave20_c15orf48_ndufa4_switch/c15orf48_ndufa4_switch_by_compartment.tsv:8`.
- UC colon myeloid has the strongest `C15ORF48` induction but not a statistically meaningful `NDUFA4` decrease: `C15ORF48` delta `4.446`, FDR `0.0287`; `NDUFA4` delta `-0.088`, FDR `0.862`; switch call `c15_up_no_ndufa4_up` in `results_v3/wave20_c15orf48_ndufa4_switch/summary.json:40-62` and table line `results_v3/wave20_c15orf48_ndufa4_switch/c15orf48_ndufa4_switch_by_compartment.tsv:3`.
- T1D endothelial and stellate signals are also `C15ORF48`-up without reciprocal `NDUFA4` suppression in `results_v3/wave20_c15orf48_ndufa4_switch/summary.json:65-112`.

### Residual Specificity

- Residual gate summary keeps `C15ORF48` as `ms_positive_three_disease;top_rank`, with broad positive disease count `3`, raw positive analysis count `3`, retained positive analysis count `3`, but strict core-covariate surviving analysis count `0`; top retained tests are mostly against HLA-II/APC, C1q/phagocytic, lipid-loader, lysosomal, MIF/CD74, and complement covariates in `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv:40`.
- The JSON guardrail is explicit: this residual screen does not provide genetics, causal perturbation, druggability, novelty, or safety evidence in `results_v3/broad_residual_gate/broad_residual_gate_summary.json:1081`.

### MS Anchor

- The independent sorted microglia dataset `GSE111972` has 31 samples, including 10 MS white-matter and 11 control white-matter samples, with primary contrast `MS_WM_vs_CON_WM` in `results_v3/gse111972_summary.json:1-31`.
- In `GSE111972`, the MS microglia module support is for the broader state, not `C15ORF48` itself: `lipid_loader_repair` delta `0.478`, Hedges g `1.379`, p `0.00528`, FDR `0.0192`; `lysosome_antigen_processing` delta `0.513`, p `0.0413`, FDR `0.0965`; interpretation guardrail says this is normal-appearing WM/GM sorted microglia, not lesion-rim spatial data in `results_v3/gse111972_summary.json:151-223`.

### Geneformer / Foundation-Model Channel

- `C15ORF48` was included among broad-residual candidate genes, but the Geneformer route cannot test it because the token is absent or not usable. The broad-residual Geneformer summary lists `C15ORF48` among candidates in `results_v3/geneformer_broad_residual_delete/geneformer_broad_residual_summary.json:139-146`, while limitations say embedding shifts are hypotheses, not expression or causal perturbation evidence in `results_v3/geneformer_broad_residual_delete/geneformer_broad_residual_summary.json:186-191`.
- The unrestricted-survivor metrics explicitly show `C15ORF48` as `not_in_geneformer_token_dictionary` in IBD epithelial and myeloid contexts in `results_v3/geneformer_unrestricted_survivor_delete/geneformer_unrestricted_survivor_delete_metrics.tsv:4` and `:48`.

### Prior Local Critique

- Wave20 already called `C15ORF48` “state marker only”: 3 positive diseases, retained residual 3, strict core residual 0, absent from Geneformer token route, ambiguous MOCCI feedback direction, and poor microprotein/miRNA modality in `subagents_v3/wave20_unrestricted_survivor.md:33-44`.
- Wave10 called `C15ORF48` strong for inflammatory mitochondrial/stress biology but weak for intervention, high in autoimmune/gut prior art, and `uncertain-to-no-go` in `subagents_v3/wave10_unrestricted_survivor_target_scout.md:67-84` and `:136-170`.
- Wave11 framed the right direction as preserving or mimicking an adaptive `C15ORF48` program, not inhibiting the gene, and required a neighbor score/residual test before any intervention direction in `subagents_v3/wave11_cross_domain_intervention_scout_report.md:110-164`.
- The genetics/prior-art scout says `C15ORF48` lacks sufficient MS target genetics and does not convert Crohn/UC expression positives into genetics in `subagents_v3/wave11_genetics_prior_art_scout_report.md:486-494`; final call there was genetics fail, prior-art risk, poor/unclear tractability, **no-go** in `subagents_v3/wave11_genetics_prior_art_scout_report.md:529-535`.
- The current global gate is strict: promotable nodes need residual support beyond IFN/APC, HLA-II/CD74, NF-kB/TNF, lysosomal stress, lipid repair, myeloid abundance, tissue injury, and treatment covariates plus real perturbation, effect size, safety guardrails, explicit direction, plausible modality, and no close prior art in `CRITIQUE_V3.md:184-200`.
- Convergence Check 20 says a promotable intervention probably needs to sit at a state-transition, niche-signal, or stratification layer rather than generic organelle housekeeping in `CONVERGENCE_CHECK_20.md:36-45`.

## External Mechanism And Prior-Art Search Log

Verified mechanism and prior-art records:

| Area | Verified source | ID / link | Audit take |
|---|---|---|---|
| MOCCI dual coding/noncoding inflammation program | Lee et al., *Nature Communications* 2021 | PMID `33837217`, PMCID `PMC8035321`, DOI `10.1038/s41467-021-22397-5`, https://www.nature.com/articles/s41467-021-22397-5 | `C15ORF48` encodes MOCCI and miR-147b; MOCCI can replace `NDUFA4` in complex IV and dampen membrane potential/ROS/inflammation. Strong mechanism, but mainly endothelial/epithelial plus macrophage-context nuance. |
| Inflammatory macrophage complex-IV remodeling | Timblin et al., *Science Advances* 2021 | PMID `34878835`, PMCID `PMC8654286`, DOI `10.1126/sciadv.abl5182`, https://pmc.ncbi.nlm.nih.gov/articles/PMC8654286/ | LPS-stimulated primary macrophages induce `C15orf48`/miR-147b and reduce `NDUFA4`; supports an inflammatory myeloid switch. |
| NDUFA4 is complex IV subunit | Balsa et al., *Cell Metabolism* 2012 | PMID `22902835`, DOI `10.1016/j.cmet.2012.07.015`, https://pubmed.ncbi.nlm.nih.gov/22902835/ | Validates `NDUFA4` as complex-IV biology, not just historical complex-I annotation. |
| Gut epithelial C15ORF48/miR-147-NDUFA4 axis | Xiong et al., *PNAS* 2024 | PMID `38917002`, PMCID `PMC11228508`, DOI `10.1073/pnas.2315944121`, https://pmc.ncbi.nlm.nih.gov/articles/PMC11228508/ | Strong disease-adjacent prior art: epithelial `C15ORF48`/miR-147 protects against DSS colitis through `NDUFA4`/metabolism/inflammation. This crowds IBD novelty and shows cell-type-dependent direction. |
| miR147 mucosal integrity | *JCI Insight* 2025 | PMID `40956617`, PMCID `PMC12581662`, DOI `10.1172/jci.insight.190466`, https://insight.jci.org/articles/view/190466 | Reinforces mucosal-healing/gut-inflammation prior art and reciprocal `C15ORF48`/`NDUFA4` epithelial pattern. |
| Autophagy/autoimmunity | *Nature Communications* 2024 | PMID `38296961`, PMCID `PMC10831050`, DOI `10.1038/s41467-024-45206-1`, https://pubmed.ncbi.nlm.nih.gov/38296961/ | `C15ORF48` connects to AMPK-ULK1 autophagy and autoimmune phenotypes; supports assay biology but adds safety/direction complexity. |
| RA miR-147 prior art | *European Journal of Immunology* 2021 | PMID `33864383`, DOI `10.1002/eji.202048850`, https://pubmed.ncbi.nlm.nih.gov/33864383/ | miR-147 function intersects RA synovial inflammation; not `C15ORF48` target validation, but prior-art crowding for autoimmune miR-147 modulation. |
| MS chronic-active lesion context | Absinta et al., *Nature* 2021 | PMID `34497421`, DOI `10.1038/s41586-021-03892-7`, https://pubmed.ncbi.nlm.nih.gov/34497421/ | Supports chronic-active lesion lymphocyte-microglia-astrocyte niche. No direct `C15ORF48`/MOCCI claim. |
| MS PRL clinical relevance | Absinta et al., *JAMA Neurology* 2019 | PMID `31403674`, PMCID `PMC6692692`, DOI `10.1001/jamaneurol.2019.2399`, https://pubmed.ncbi.nlm.nih.gov/31403674/ | PRLs/chronic active lesions associate with disability and tissue injury; justifies MS relevance for a circuit assay. |
| MS lipid-storing microglia niche | Feng et al., *Immunity* 2025 | PMID `41167189`, DOI `10.1016/j.immuni.2025.10.003`, https://pure.mpg.de/view/item_3678140_2 | Spatial chronic-active lesion study with CD8/lipid-storing phagocyte biology and ABCA1/G1 perturbation. Supports lipid-myeloid endpoint, not MOCCI specifically. |

Trials and databases:

- ClinicalTrials.gov API query `C15ORF48` returned one irrelevant exercise study, `NCT06480643`, with OA/sarcopenia/RA conditions and exercise interventions; no C15ORF48-directed interventional trial was found. Query `NDUFA4` returned no studies.
- ChEMBL target search returned `0` targets for `C15ORF48`. For `NDUFA4`, ChEMBL returned `CHEMBL2317` (`Cytochrome c oxidase subunit NDUFA4`) and 8 activities, but these are mitochondrial-complex inhibitor/assay records, not selective autoimmune tools.
- DGIdb returned no `C15ORF48` gene node. For `NDUFA4`, DGIdb listed inhibitor interactions from ChEMBL for `ME-344`, metformin hydrochloride, and `NV-128`; these are nonspecific mitochondrial/metabolic agents and do not define a tractable `NDUFA4` switch therapy.

Patent search log:

- Google Patents query `C15ORF48 miR-147 autoimmune disease` did not surface a direct `C15ORF48`/MOCCI therapeutic-modulation patent in autoimmune disease. It did surface biomarker-style or pathway-adjacent claims.
- `WO2019018440A1` claims a healthy/UC colon cell atlas and includes measuring `C15orf48` in GI macrophages for IBD detection: https://patents.google.com/patent/WO2019018440A1/en.
- `WO2018232288A1` / `CN110740733A` use `C15orf48` as an IRAK4-pathway biomarker among many genes for IRAK4-mediated disorders: https://patents.google.com/patent/WO2018232288A1/en and https://patents.google.com/patent/CN110740733A/zh.
- Other hits include melanoma/immune-related biomarker lists (`WO2019115480A1`, `WO2020254658A1`) and broad nucleotide/gene lists (`WO2022012420A1`), not a clean C15ORF48/MOCCI intervention claim.

## Circuit Interpretation

The mechanism is biologically coherent:

```text
inflammatory stimulus / tissue stress
    -> C15ORF48 locus induction
    -> MOCCI peptide + miR-147b
    -> NDUFA4 suppression / complex-IV composition change
    -> altered complex-IV flux, membrane potential, ROS, autophagy
    -> inflammatory-output tuning, lipid/lysosomal stress tolerance
```

But the local disease evidence supports only the first arrow robustly. The actual reciprocal switch is not recurrent enough. The most likely interpretation is:

- `C15ORF48` marks a high-intensity inflammatory mitochondrial adaptation state in myeloid and stressed tissue-resident compartments.
- The canonical MOCCI/`NDUFA4` switch is one possible downstream implementation, but transcript-only pseudobulk cannot prove MOCCI translation, miR-147b processing, complex-IV incorporation, or functional CIV flux.
- In autoimmune tissue, the biology may be protective/adaptive rather than pathogenic. Directly suppressing `C15ORF48` could be backwards.

## Intervention-Point Options

| Layer | Option | Tractability | Main blocker |
|---|---|---|---|
| Upstream induction | Identify non-inflammatory activators of the `C15ORF48`/miR-147 program, or upstream state controllers that induce the adaptive switch without NF-kB/JAK/TLR activation | Low-medium as screening concept | Current known inducers are inflammatory; broad induction risks worsening the module. |
| Direct locus/product replacement | Deliver MOCCI mRNA/protein, `C15ORF48` ORF, or miR-147b mimic to selected myeloid/microglial states | Low | Mitochondrial microprotein delivery, miRNA off-targets, CNS/tissue targeting, and unclear desired direction. |
| Downstream `NDUFA4` lowering | siRNA/ASO/CRISPRi against `NDUFA4` or chemical CIV tuning | Poor | Core mitochondrial respiration liability; available database “inhibitors” are nonspecific and not switch-selective. |
| Autophagy/AMPK-ULK1 mimicry | Use `C15ORF48` as a readout for controlled autophagy/mitochondrial stress-resolution modulators | Medium as assay, poor as claim | AMPK/autophagy modulators are broad and can affect repair, metabolism, infection response, and cell survival. |
| Screening readout | Screen candidate state-correctors in `C15ORF48`-high cells and require MOCCI/miR-147/`NDUFA4` switch plus lipid-lysosomal rescue | Good | This is an assay strategy, not a named target. |

Best immediate intervention framing: **do not inhibit `C15ORF48`; use the switch as a target-engagement and state-resolution readout for upstream or parallel interventions.**

## Druggability And Safety

Druggability:

- `C15ORF48` has no ChEMBL target record and no DGIdb interactions in the checked APIs.
- `NDUFA4` has database records, but they point to mitochondrial-complex inhibition rather than a selective, safe, cell-state switch.
- MOCCI is a small mitochondrial protein; miR-147b is an RNA regulator. Both are technically perturbable in vitro, but not mature therapeutic handles.

Safety:

- Complex IV and mitochondrial membrane potential are core cell-biology processes. Chronic or systemic manipulation risks broad bioenergetic toxicity.
- In gut models, `C15ORF48`/miR-147 appears protective for epithelial barrier and microbiome homeostasis; suppressing it may worsen barrier inflammation.
- miR-147b has immune and antiviral functions, including RIG-I/MDA5 pathway effects in the MOCCI paper; mimics or inhibitors may alter host defense.
- Autophagy/AMPK/ULK1 effects intersect thymic epithelial tolerance and autoimmunity; this is not a simple anti-inflammatory knob.
- In MS, microglia need to preserve myelin-debris uptake, lysosomal acidification, efferocytosis, oligodendrocyte support, and host defense. Any mitochondrial intervention must pass these guardrails before in vivo claims.

## MS Relevance

MS relevance is plausible but indirect:

- Local broad h5ad ranking gives `C15ORF48` an MS white-matter nominal positive signal: delta `1.223`, Hedges g `1.438`, p `0.00375`, FDR `0.834` in `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv:13`.
- `GSE111972` supports a broader MS microglial lipid/lysosomal state, especially `lipid_loader_repair` and `lysosome_antigen_processing`, but it is sorted normal-appearing WM/GM, not lesion-rim spatial data in `results_v3/gse111972_summary.json:151-223`.
- External MS literature supports chronic-active/PRL lesion microglia, lipid-storing phagocytes, complement, and adaptive-cell niches, but no verified source directly shows a MOCCI/`NDUFA4` switch in MS lesion microglia.

Therefore, the MS claim should be limited to: **a testable mitochondrial adaptation subcircuit that may intersect the lipid-lysosomal lesion-rim myeloid state.**

## Falsification Experiment

### Experiment 1: Human Myeloid/Microglia Switch Causality

Material:

- iPSC-derived microglia/macrophages from `n=18-24` donors, including MS donors where feasible, plus matched control donors.
- Parallel human monocyte-derived macrophages and IBD mucosal macrophage-like culture, because local switch support is strongest in Crohn/UC myeloid.

Stimuli:

- Human myelin debris plus lesion-relevant `IFNG`/`TNF`/IL-1 beta conditions.
- Gut comparator: LPS/IL-1 beta/TNF with lipid/debris challenge.

Perturbations:

- `C15ORF48` CRISPRi/siRNA.
- ORF-only rescue, miR-147b mimic/inhibitor, and `NDUFA4` rescue/knockdown to separate MOCCI peptide, miRNA, and target-subunit effects.

Primary readouts:

- `C15ORF48` RNA, MOCCI peptide by targeted proteomics or validated antibody, mature miR-147b, `NDUFA4` mRNA/protein.
- BN-PAGE or complex-IV immunocapture for MOCCI/`NDUFA4` occupancy.
- CIV flux, oxygen consumption, membrane potential, mitochondrial ROS.
- Lipid droplets, lysosomal acidification, myelin uptake/degradation, cytokines, complement/C1q-associated readouts, cell viability.

Pass condition:

- Disease-relevant stimulation produces a reproducible `C15ORF48`/MOCCI/miR-147 increase with reciprocal `NDUFA4` protein decrease and measurable CIV/ROS/autophagy shift in at least two disease-relevant systems.
- Perturbing the axis changes lipid-lysosomal/inflammatory readouts by at least `30%` or donor-level effect size `>=0.5 SD`, while preserving viability, myelin uptake, lysosomal acidification, and efferocytosis at `>=80%` of control.
- Rescue separates MOCCI and miR-147b effects and restores the phenotype.

Fail condition:

- `C15ORF48` transcript rises without MOCCI peptide, miR-147b maturation, or `NDUFA4` protein/complex-IV change.
- Perturbation only tracks generic NF-kB/IFN intensity or viability.
- `C15ORF48` lowering worsens ROS, lipid burden, myelin clearance, or barrier/repair readouts.

### Experiment 2: MS Lesion Spatial Validation

Material:

- Postmortem PRL/chronic-active lesion rims and matched non-rim white matter from `n=20-30` MS donors where MRI-pathology linkage is available.

Assay:

- Multiplex RNA/protein imaging for `C15ORF48`, MOCCI, `NDUFA4`, CD68/TMEM119, `GPNMB`, `PLIN2`, C1q, HLA-II/CD74, CD8 proximity, lipid stain, and mitochondrial stress markers.

Pass condition:

- The switch is enriched specifically in lipid-laden lesion-rim myeloid cells, not just inflamed tissue, and remains associated after myeloid density and IFN/HLA-II adjustment.

Fail condition:

- `C15ORF48` is only a diffuse inflammation marker, `NDUFA4` is not reciprocally reduced, or the signal is epithelial/vascular/immune-infiltrate dominated rather than microglial/macrophage localized.

## Final Call

Use `C15ORF48`/MOCCI as an **assayable circuit marker** and a falsifiable bridge between inflammatory stimuli, mitochondrial complex-IV remodeling, ROS/autophagy, and lipid-lysosomal myeloid stress.

Do **not** promote it as a therapeutic target or cross-autoimmune mechanism anchor yet. The evidence does not currently satisfy the local strict residual, perturbation, genetics, tractability, or safety gates. The next valuable action is a focused wet-lab perturbation and spatial validation package, not a target nomination.
