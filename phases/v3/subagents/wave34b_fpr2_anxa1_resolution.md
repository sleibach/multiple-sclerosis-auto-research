# Wave34-B: FPR2/ALX + ANXA1 Efferocytosis / Resolution Branch

Date: 2026-05-27  
Role: scoped branch report for V3 autoimmune/MS research.  
Instruction honored: do not claim a finding.

## Verdict

**PARK, do not promote.** Biased `FPR2/ALX` pro-resolution agonism plus `ANXA1` remains a plausible IBD/lupus-nephritis follow-up branch, but it does **not** currently have enough MS lesion-local support or MS-relevant perturbation evidence to move beyond the Crohn/UC/LN follow-up tier. The branch is stronger than a generic SPM story because real FPR2 pharmacology exists, but the available MS evidence is mostly ANXA1 presence/SPM-context/EAE rather than a demonstrated `FPR2`-dependent repair mechanism in MS lesions or myelin-laden microglia.

## Decision Rule Used

Promote required all of:

- Real perturbation/pharmacology evidence for biased pro-resolution/efferocytosis signaling.
- MS lesion-local or MS-relevant myeloid/microglial support, not just peripheral or EAE-only evidence.
- Cross-autoimmune evidence beyond colitis.
- No sign conflict severe enough to make agonism direction ambiguous.

The first and third criteria are partially met. The second and fourth are not.

## Local V3 Evidence

### Local expression / cell-state signal

Source tables:

- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/wave23_metabolite_barrier_circuit/candidate_gene_local_evidence.tsv`
- `results_v3/wave23_metabolite_barrier_circuit/chembl_target_snapshot.tsv`
- `results_v3/wave32c_resolution_prior_art_audit/route_feasibility_ranked.tsv`
- `results_v3/wave32c_resolution_prior_art_audit/api_hit_summary.tsv`

`FPR2` is locally positive in IBD myeloid compartments:

| Gene | Dataset | Disease / compartment | Case donors | Control donors | delta log2 CPM | Hedges g | p | FDR | Call |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| `FPR2` | `data/raw_v3/cell_state/ibd_human_10x.h5ad` | Crohn colon myeloid | 6 | 6 | `4.638177` | `2.933260` | `0.000260` | `0.068672` | positive FDR10 |
| `FPR2` | `data/raw_v3/cell_state/ibd_human_10x.h5ad` | UC colon myeloid | 6 | 6 | `4.123173` | `2.632765` | `0.000587` | `0.082977` | positive FDR10 |

The MS white-matter summary is negative:

| Gene | MS white-matter delta log2 | Hedges g | p | FDR | Interpretation |
|---|---:|---:|---:|---:|---|
| `FPR2` | `-0.932638` | `-0.387238` | `0.372217` | `0.914127` | no local MS support |
| `ANXA1` | `-0.069322` | `-0.066777` | `0.880061` | `0.982923` | no local MS support |

`ANXA1` local positives are not a clean myeloid/MS pattern. In broad h5ad ranking it has positives in type 1 diabetes beta/acinar cells and UC epithelium, while IBD myeloid/stromal trends are negative or mixed. The broad table reports `ANXA1` positive disease count `2`, negative disease count `2`, and MS white-matter p `0.880061`.

`results_v3/gse111972_target_contrasts.tsv` did not include `FPR2` or `ANXA1`; that is absence of targeted analysis rather than positive or negative evidence. The broad V3 rank already imports the MS white-matter summary above, so I treat that as the operative local MS result.

### Local druggability / perturbation

`FPR2` is a real druggable GPCR target:

- ChEMBL target: `CHEMBL4227`, "N-formyl peptide receptor 2", Homo sapiens, UniProt `P25090`.
- `results_v3/wave23_metabolite_barrier_circuit/chembl_target_snapshot.tsv` reports `3374` ChEMBL nM activity records for `FPR2`.
- `results_v3/wave23_metabolite_barrier_circuit/lincs_compound_presence.tsv` had no FPR2 branch LINCS compound match in the V3 route.

Wave32-C route feasibility ranked `specialized_pro_resolving_mediator_FPR2_axis` as the least-blocked resolution route, but explicitly as "not yet a finding":

- Direction: `agonism_not_inhibition`.
- Blocking status: `NOT_BLOCKED_BUT_IMMATURE`.
- Lead indication if any: "IBD first; MS only after CNS/peripheral PK-PD proof."
- Biomarker readouts proposed: tissue efferocytosis index, SPM lipidomics, FPR2 response, S100A8/A9/neutrophil program down, resolution macrophage markers.

## External Perturbation / Pharmacology Evidence

### Strongest positive pharmacology: IBD / colitis

1. **Columbamine biased FPR2 agonism enhances efferocytosis in colitis.**  
   PMID `37994307`; Wu MY et al.; *EMBO Molecular Medicine*; 2023; DOI `10.15252/emmm.202317815`.  
   Query: `(FPR2 OR "formyl peptide receptor 2") AND (colitis OR "inflammatory bowel") AND (efferocytosis OR macrophage OR agonist)`; PubMed count `13`.  
   Characterization: identifies columbamine as a biased `FPR2` agonist, enhances macrophage LC3-associated efferocytosis, attenuates DSS colitis, and reports dependence on FPR2 blockade/ablation in the abstract. This is the best real perturbation support for the branch.

2. **Oral FPR2/ALX modulators ameliorate mucosal inflammation in IBD models.**  
   PMID `40069490`; "Oral FPR2/ALX modulators tune myeloid cell activity to ameliorate mucosal inflammation in inflammatory bowel disease"; *Acta Pharmacologica Sinica*; 2025; DOI `10.1038/s41401-025-01525-7`.  
   Characterization: oral Quin-C1 / Quin-C7 FPR2/ALX modulators in DSS colitis with structural activation analysis. Useful for druggability and gut disease, not sufficient for MS.

### Cross-autoimmune support: lupus nephritis and articular inflammation

3. **ANXA1-FPR2/ALX macrophage reprogramming in lupus nephritis.**  
   PMID `41800263`; Tao J et al.; *International Journal of Biological Sciences*; 2026; DOI `10.7150/ijbs.118613`.  
   Query: `(FPR2 OR "FPR2/ALX" OR "formyl peptide receptor 2" OR ANXA1 OR "annexin A1") AND (lupus OR "lupus nephritis") AND macrophage`; PubMed count `4`.  
   Characterization: reports renal `ANXA1`, an `Anxa1+Spp1+` macrophage subset, and ANXA1/FPR2/ALX signaling through mTOR/FABP4/FAO in macrophages; Ac2-26 ameliorated kidney injury in lupus-prone mice. This is meaningful cross-autoimmune support, but it is LN-fibrosis biology, not MS lesion biology.

4. **FPR2/ALX agonist AT-01-KG in articular inflammation.**  
   PMID `33493655`; Galvao I et al.; *Pharmacological Research*; 2021; DOI `10.1016/j.phrs.2021.105445`.  
   Characterization: synthetic lipoxin A4 mimetic / FPR2/ALX agonist reduced neutrophil and inflammatory readouts in articular inflammation models. Supports tractability of FPR2/ALX resolution pharmacology, not MS.

### MS / CNS evidence: supportive but insufficient

5. **ANXA1 in EAE lesions with exogenous fragment benefit.**  
   PMID `9472682`; Huitinga I et al.; *Clinical and Experimental Immunology*; 1998; DOI `10.1046/j.1365-2249.1998.00490.x`.  
   Characterization: annexin-1 expressed in ED1+ macrophages and astrocytes in EAE CNS lesions; intracerebroventricular annexin-1 fragment reduced mild EAE severity. This supports CNS inflammatory-lesion relevance of ANXA1 but predates FPR2-biased agonism and is not human MS lesion perturbation.

6. **Human MS plaque ANXA1 expression.**  
   PMID `12175341`; Probst-Cousin S et al.; *Neuropathology and Applied Neurobiology*; 2002; DOI `10.1046/j.1365-2990.2002.00396.x`.  
   Query: `("annexin A1" OR ANXA1 OR annexin-1) AND ("multiple sclerosis" OR EAE OR "experimental autoimmune encephalomyelitis")`; PubMed count `22`.  
   Characterization: stage-dependent ANXA1 expression in MS plaques, including macrophages, perivascular lymphocytes, and activated astrocytes. This is lesion-local ANXA1 evidence. It is not FPR2 expression, ligand-receptor interaction, or agonist response evidence.

7. **Reduced peripheral ANXA1 associates with RRMS severity.**  
   PMID `31462505`; "Reduced Annexin A1 Expression Associates with Disease Severity and Inflammation in Multiple Sclerosis Patients"; *Journal of Immunology*; 2019; DOI `10.4049/jimmunol.1801683`.  
   Characterization: circulating ANXA1 expression inversely correlated with disease score/progression and impaired ANXA1 production in T-cell subsets. Useful peripheral immune support; not lesion-local myeloid repair.

8. **SPMs altered in MS blood and attenuate monocyte/BBB dysfunction.**  
   PMID `31780628`; "Specialized pro-resolving lipid mediators are differentially altered in peripheral blood of patients with multiple sclerosis and attenuate monocyte and blood-brain barrier dysfunction"; *Haematologica*; 2020; DOI `10.3324/haematol.2019.219519`.  
   Characterization: supports an MS resolution-lipid deficit frame, but not specifically `FPR2`/`ANXA1` as a lesion target.

9. **Lipoxin A4 and RvD1 analogs improve EAE.**  
   - PMID `34077725`; "Pro-resolving lipid mediator lipoxin A4 attenuates neuro-inflammation by modulating T cell responses and modifies the spinal cord lipidome"; *Cell Reports*; 2021; DOI `10.1016/j.celrep.2021.109201`.  
   - PMID `39116500`; "The chemically stable analogue of resolvin D1 ameliorates experimental autoimmune encephalomyelitis by mediating the resolution of inflammation"; *International Immunopharmacology*; 2024; DOI `10.1016/j.intimp.2024.112740`.  
   Characterization: supports pro-resolution lipid mediator biology in EAE. These are not enough to promote `FPR2/ANXA1` because EAE/SPM benefit does not establish human MS lesion-local FPR2 target engagement.

10. **FPR2/ALX in NMOSD / autoimmune astrocytopathy, with sign ambiguity.**  
   - PMID `40225578`; "Targeting formyl peptide receptor 2 to suppress neuroinflammation in neuromyelitis optica spectrum disorder"; *Theranostics*; 2025; DOI `10.7150/thno.107303`. This reports FPR2 targeting in NMOSD and uses antagonist `Quin-C7` in the abstract.  
   - PMID `41807546`; "FPR2/ALX stimulation modulates microglia and natural killer cells to restrict autoimmune astrocytopathy"; *Acta Pharmacologica Sinica*; 2026; DOI `10.1038/s41401-026-01778-w`. This reports agonist `Quin-C1` reducing brain lesion volume, astrocyte loss, and demyelination in an AQP4-IgG/complement astrocytopathy model.  
   Interpretation: valuable CNS-autoimmune pharmacology, but not MS. The agonist-versus-antagonist split reinforces that FPR2 ligand bias and cellular context are central liabilities.

### Contradictory / cautionary MS evidence

11. **Endogenous ANXA1 can promote EAE depending on immune context.**  
   PMID `19912648`; Paschalidis N et al.; *Journal of Neuroinflammation*; 2009; DOI `10.1186/1742-2094-6-33`.  
   Characterization: `AnxA1` null mice had decreased EAE signs, linked to T-cell activation effects. This directly blocks a simplistic "more ANXA1 is always protective in MS" interpretation.

12. **FPR2 pharmacology is ligand-biased and can be inflammatory.**  
   PMID `35797341`; Qin CX et al.; *British Journal of Pharmacology*; 2022; DOI `10.1111/bph.15919`.  
   Characterization: IUPHAR review covering FPR2 nomenclature, structure, signaling, ligand diversity, and translational issues. This is the pharmacology reason to require biased pro-resolution agonism rather than generic FPR2 agonism.

13. **Clinical small-molecule FPR2 agonism has translational caution.**  
   PMID `31085160`; Lind S et al.; *Biochemical Pharmacology*; 2019; DOI `10.1016/j.bcp.2019.04.030`.  
   Characterization: ACT-389949 was tested in Phase I healthy subjects and then characterized functionally in human neutrophils. Useful chemical precedent, but generic neutrophil agonism is not equivalent to lesion-myeloid repair.

## Trial Surface

ClinicalTrials.gov API v2 queries run on 2026-05-27:

| Query | Returned studies | Interpretation |
|---|---:|---|
| `FPR2 agonist` | `0` | no direct FPR2 agonist trial found |
| `formyl peptide receptor 2 agonist` | `0` | no direct FPR2 agonist trial found |
| `annexin A1 autoimmune` | `0` | no autoimmune ANXA1 interventional trial found |
| `FPR2 multiple sclerosis` | `0` | no MS FPR2 trial found |
| `lipoxin A4 multiple sclerosis` | `0` | no MS LXA4 trial found |
| `resolvin autoimmune` | `1` | unrelated keyword noise: `NCT05834855`, rituximab vs ocrelizumab in relapsing MS |

Conclusion: no clinical MS or autoimmune trial evidence currently promotes the branch.

## Patent / Prior-Art Surface

Local Wave32-C patent URLs:

- Google Patents query: `FPR2 agonist autoimmune disease`  
  URL: `https://patents.google.com/?q=FPR2+agonist+autoimmune+disease`
- Google Patents query: `resolvin autoimmune multiple sclerosis`  
  URL: `https://patents.google.com/?q=resolvin+autoimmune+multiple+sclerosis`
- Espacenet query: `FPR2 agonist autoimmune disease`  
  URL: `https://worldwide.espacenet.com/patent/search?q=FPR2+agonist+autoimmune+disease`  
  Status in this environment: HTTP 403 / browser challenge.
- Espacenet query: `resolvin autoimmune multiple sclerosis`  
  URL: `https://worldwide.espacenet.com/patent/search?q=resolvin+autoimmune+multiple+sclerosis`  
  Status in this environment: HTTP 403 / browser challenge.

Direct patent pages fetched from Google Patents:

- `US11708327B2`, "Phenylpyrrolidinone formyl peptide 2 receptor agonists"; Google Patents URL `https://patents.google.com/patent/US11708327B2/en`. The disclosure covers FPR2 and/or FPR1 agonists and lists inflammatory/neuroinflammatory indications including multiple sclerosis.
- `EP3981878A1`, "FPR2 receptor agonist aptamers and uses thereof"; Google Patents URL `https://patents.google.com/patent/EP3981878A1/en`. The disclosure covers FPR2 agonist aptamers and broad autoimmune/neurological diseases including multiple sclerosis.

Prior-art interpretation: FPR2 agonism for inflammatory/neuroinflammatory/autoimmune use is not a blank space. However, I did not find a directly blocking published or clinical claim for **biased FPR2/ANXA1 agonism to repair human MS chronic active lesion macrophage/microglia efferocytosis**. That narrower concept remains unproven rather than clearly novel-and-actionable.

## Blockers

1. **MS local support is negative or missing.** Local V3 `FPR2` and `ANXA1` MS white-matter summaries are negative. Human MS plaque literature supports `ANXA1` presence, not FPR2-dependent repair.

2. **No MS lesion perturbation.** I found no human MS lesion culture, iPSC-microglia myelin-debris, organotypic slice, or postmortem lesion macrophage experiment showing that FPR2-biased agonism plus ANXA1 improves myelin/apoptotic-cell clearance.

3. **Ligand-bias risk is not cosmetic.** FPR2 can signal pro-resolving or inflammatory depending on ligand and context. NMOSD/astrocytopathy papers include both antagonist and agonist benefit models. ANXA1/EAE genetics also show sign conflict.

4. **No target-level genetics.** No V3 local genetics, coloc, MR, or pQTL anchor supports `FPR2` or `ANXA1` as a causal autoimmune node.

5. **Cross-autoimmune evidence is two strong indications plus weak tail.** Crohn/UC and LN are the meaningful branches. RA/articular inflammation is supportive but not a disease-target package. Psoriasis, Sjogren, T1D, and PBC are weak or not locally supportive.

6. **CNS delivery and target engagement are unsettled.** Small molecules exist, but the branch needs evidence that a biased pro-resolution agonist reaches the relevant CNS/perivascular/myeloid compartment at non-inflammatory exposure.

## Promote / Park / Demote Call

**Park as an IBD/LN-first pro-resolution branch. Do not promote for MS V3. Do not demote entirely.**

Rationale:

- Promote fails because MS lesion-local `FPR2` support and MS-relevant perturbation are absent.
- Full demotion is too harsh because columbamine/FPR2 colitis efferocytosis, ANXA1/FPR2 LN macrophage reprogramming, FPR2/ALX CNS-autoimmune pharmacology, and MS SPM/ANXA1 context form a coherent follow-up path.
- The correct next test is not another bulk signature score. It is a cell- and cargo-resolved perturbation assay.

## Exact Next Experiment Needed to Unpark

Use human disease-relevant macrophage/microglia systems:

1. **IBD/LN validation tier:** primary Crohn/UC lamina propria macrophages and LN kidney macrophages treated with columbamine, Quin-C1, AT-01-KG or other biased FPR2 agonists, Ac2-26, inactive analogs, and FPR2 antagonist/knockdown controls.
2. **MS bridge tier:** human iPSC microglia and, if accessible, postmortem MS lesion-derived myeloid cultures loaded with myelin debris and apoptotic oligodendrocyte-lineage cells.
3. Required success criteria:
   - >= `30%` increase in myelin/apoptotic-cell efferocytosis versus vehicle.
   - Effect abolished or strongly reduced by FPR2 blockade/knockdown.
   - No broad suppression of IFN response, HLA-II/CD74 antigen-presentation capacity, or antiviral response.
   - Reduction in lipid-inflammatory readouts such as `S100A8/A9`, `IL1B`, `CXCL8`, or foam-cell stress markers.
   - No increase in profibrotic `TGFB1`/collagen program in LN/IBD macrophage contexts.

Until that experiment or an equivalent public perturbation dataset exists, this branch should remain parked.

