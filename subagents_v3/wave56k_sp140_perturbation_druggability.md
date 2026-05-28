# Wave56-K SP140 Perturbation And Druggability Audit

Timestamp: 2026-05-27

## Verdict

`SP140` should **not** be promoted as the V3 cross-autoimmune/MS therapeutic target. The earlier local statement "no direct perturbation support" was too narrow: published public data do contain target-specific SP140 perturbation evidence, including `SP140` siRNA and the SP140 PHD/bromodomain inhibitor `GSK761`. However, that evidence supports a Crohn/IBD macrophage anti-inflammatory tool-compound route more than a novel cross-autoimmune lipid-lysosomal myeloid target. The strongest GSK761 effect is suppression of IFN/NF-kB inflammatory genes under M1/LPS conditions, not consistent shutdown of the lipid-lysosomal repair module; local V3 MS white-matter signal is null; and SP140 inhibition is already direct prior art for Crohn/inflammatory disease.

Final call: `DEMOTE_FOR_V3_PROMOTION; PARK_AS_SP140_HIGH_IBD_TOOL_COMPOUND_AND_STRATIFICATION_ROUTE`.

## Sources Checked

Local artifacts:

- `CONVERGENCE_CHECK_18.md`
- `results_v3/wave55_external_genetics_druggability_sweep/`
- `results_v3/wave56_sp140_targeted_reopener_audit/`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/wave15_perturbation_drug_response/`

New support script and outputs:

- `scripts/v3_wave56k_sp140_perturbation_druggability_audit.py`
- `results_v3/wave56k_sp140_perturbation_druggability/gsk761_sp140_supplement_module_summary.tsv`
- `results_v3/wave56k_sp140_perturbation_druggability/gsk761_sp140_interest_gene_effects.tsv`
- `results_v3/wave56k_sp140_perturbation_druggability/sp140_domain_structure_summary.tsv`
- `results_v3/wave56k_sp140_perturbation_druggability/sp140_public_endpoint_summary.tsv`

Verified external sources:

- Ghiboub et al., BMC Biology 2022, "Modulation of macrophage inflammatory function through selective inhibition of the epigenetic reader protein SP140", DOI `10.1186/s12915-022-01380-6`: https://link.springer.com/article/10.1186/s12915-022-01380-6
- Amatullah et al., Cell 2022, "Epigenetic reader SP140 loss of function drives Crohn's disease due to uncontrolled macrophage topoisomerases", DOI `10.1016/j.cell.2022.06.048`: https://doi.org/10.1016/j.cell.2022.06.048
- UniProt `Q13342` / `SP140_HUMAN`: https://www.uniprot.org/uniprotkb/Q13342/entry
- AlphaFold `AF-Q13342-F1`: https://alphafold.ebi.ac.uk/entry/Q13342
- RCSB `6G8R`, SP140 PHD-bromodomain complex: https://www.rcsb.org/structure/6G8R
- RCSB `8J71`, SP140 SAND domain with DNA: https://www.rcsb.org/structure/8J71
- ChEMBL target `CHEMBL3108643`: https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3108643/
- PubChem GSK761 `CID 168007146`: https://pubchem.ncbi.nlm.nih.gov/compound/168007146
- Google Patents `EP2643462B1`, SP140 bromodomain inhibitors: https://patents.google.com/patent/EP2643462B1/en

## Local V3 Context

Wave55 made `SP140` the strongest non-closed reopener because it combined external genetics breadth with local cross-disease cell-state recurrence:

| Evidence | Local result |
| --- | --- |
| Open Targets genetic breadth | 6 diseases with genetic association >= 0.25: AS, Crohn, MS, psoriasis, RA, UC |
| MS Open Targets genetic score | 0.759 |
| Local cross-disease expression/cell-state positives | 4 diseases: Crohn, UC, psoriasis, Sjogren |
| Local MS white matter | delta `-0.087`, p `0.726`, FDR `0.968` |
| Wave55 perturbation gate | failed |
| Wave55 ChEMBL bounded nM activity | 0 rows |

`SP140` is therefore a cross-disease marker/reopener, not an MS-anchored target. The local residual gate also demoted it: only one retained positive residual disease count and no strict core covariate-surviving analyses in `results_v3/wave56_sp140_targeted_reopener_audit/sp140_comparator_local_evidence.tsv`.

## Perturbation Evidence

### Published SP140/GSK761 Evidence

Ghiboub et al. report a direct SP140 inhibitor, `GSK761`, and use it in human M1 macrophages and Crohn colon macrophages. The paper states that GSK761 inhibits SP140 binding to inflammatory genes and supports SP140 as a Crohn inflammation target. The same paper provides public supplemental summary statistics:

- Table S1: `SP140` siRNA M1 macrophage vs scrambled siRNA.
- Table S2: `SP140` siRNA M1 macrophage + 4 h LPS vs scrambled.
- Table S5: GSK761 M1 macrophage vs DMSO.
- Table S6: GSK761 M1 macrophage + 4 h LPS vs DMSO.
- Table S7: GSK761 M1 macrophage + 8 h LPS vs DMSO.

I re-parsed those XLSX tables and tested the V3 readout modules with BH-adjusted p-values from the provided per-gene p-values.

Key module results:

| Contrast | IFN/APC | HLA-II/APC | lysosomal APC | lipid-loader repair | inflammatory NF-kB |
| --- | --- | --- | --- | --- | --- |
| `SP140` siRNA M1 | median `-0.148`, no FDR<0.05 module genes | median `-0.026`, no FDR genes | median `0.012`, no FDR genes | median `0.023`, no FDR genes | median `0.284`, no FDR genes |
| `SP140` siRNA + 4 h LPS | median `0.030`, no FDR genes | `HLA-DPB1` down | no FDR genes | `MSR1` down only | no FDR genes |
| GSK761 M1 | IFN/APC down: `CXCL10`, `IRF1`; enrichment p `0.0219` | no FDR genes | no FDR genes | no FDR genes | `CCL2`, `IL1B`, `IL6` down; enrichment p `0.00191` |
| GSK761 + 4 h LPS | IFN/APC down: `GBP1`, `IRF1`; enrichment p `0.00891` | no FDR genes | no FDR genes | `ACSL1` down only | `IL1B`, `IL6`, `TNFAIP3` down; enrichment p `0.000489` |
| GSK761 + 8 h LPS | mixed: `CXCL10`, `GBP1` down but `STAT1` up | `HLA-DMB` up | `CTSB` down, `LAMP1` up | `ACSL1`, `LIPA` down but `MERTK`, `PLIN2` up | `IL6` down but `CCL2`, `CXCL8`, `NFKBIA`, `NFKBIZ` up |

Interpretation: GSK761 is a real SP140 perturbation with anti-inflammatory signal at early M1/LPS timepoints, but it does **not** cleanly suppress the lipid-lysosomal module. At 8 h LPS, lipid-loader genes move in opposing directions (`ACSL1`, `LIPA` down; `MERTK`, `PLIN2` up), which is not a coherent demyelination-relevant lipid-lysosomal rescue signature.

### Local LINCS/CMap/Perturb-seq Check

Local perturbation files do not contain a SP140 perturbation. The closest family-neighbor perturbation is `SP110` CRISPRi in Mixscale, but this is not a valid SP140 phenocopy:

- IFNB `SP110` CRISPRi selectivity score `-0.0255`, call `null_or_wrong_direction`.
- IFNG `SP110` CRISPRi selectivity score `-0.0399`, call `null_or_wrong_direction`.
- System: stimulated human cancer-cell pathway Perturb-seq, not primary macrophage, microglia, or autoimmune tissue.

Local L1000FWD outputs do not show `GSK761`, `SP140`, or a target-specific SP140 perturbation profile. The topoisomerase-inhibitor signals in L1000 are not acceptable SP140 phenocopies: they are broad cytotoxic mechanisms, and the Cell 2022 topoisomerase result is a rescue hypothesis for SP140 loss-of-function Crohn biology, not a general way to suppress the V3 module.

## Druggability And Structure

SP140 is not undruggable in principle. It has structured reader domains:

| Domain | UniProt coordinates | AlphaFold mean pLDDT |
| --- | --- | --- |
| HSR | 22-138 | 81.3 |
| SAND | 580-661 | 85.3 |
| PHD-type zinc finger | 690-736 | 89.2 |
| Bromodomain | 754-857 | 85.9 |
| PHD-bromodomain construct | 687-867 | 84.2 |

Experimental structures also exist: `6G8R` is the SP140 PHD-bromodomain complex at 2.74 A, and `8J71` is the SP140 SAND domain with DNA at 1.85 A. That is enough for tool-compound optimization and structure-guided selectivity work.

The practical druggability problem is different:

- ChEMBL has `CHEMBL3108643` for SP140 and 61 activity rows, but these are thermal-shift `Delta Tm` records, not potency/pChEMBL or nM functional activity records.
- ChEMBL molecule search did not find `GSK761`.
- PubChem lists GSK761 as `CID 168007146`, MW `646.8`, XLogP `7`, TPSA `94.5`, and 13 rotatable bonds. This is compatible with a biochemical/cellular probe, but it is not a credible CNS lead without major medicinal chemistry and exposure data.
- The Ghiboub paper reports BROMOscan selectivity against other human bromodomain-containing proteins, which supports SP140 selectivity relative to generic BET inhibition. That also means generic bromodomain/BET inhibitors should **not** be assumed to phenocopy SP140.

## Prior Art And Novelty

The SP140 inhibition concept is not novel for autoimmune/inflammatory disease:

- Ghiboub et al. explicitly present SP140 inhibition with GSK761 as a way to regulate Crohn inflammation and possibly support anti-TNF non-responder therapy.
- Google Patents `EP2643462B1` covers SP140 bromodomain inhibitors and includes inflammatory/autoimmune framing.
- Europe PMC query counts from the support script: `SP140 inhibitor` 388 hits, `SP140 autoimmune therapeutic target` 130 hits, `SP140 degrader` 8 hits. Counts are broad and not all relevant, but they make this a crowded prior-art lane.
- ClinicalTrials.gov query `SP140 autoimmune` returned 0 trials, so there is no obvious clinical-stage SP140 autoimmune program surfaced by that query.

Novelty remaining, if any, would need to be very narrow: an SP140-high, genotype-aware macrophage/APC stratification biomarker or a non-CNS IBD/skin/salivary-gland ex vivo validation package. It is not a novel V3 cross-autoimmune target nomination.

## Adjacent Intervention Points

| Route | Verdict | Reason |
| --- | --- | --- |
| Direct SP140 PHD/bromodomain inhibition | `PARK_AS_TOOL` | Real perturbation and selectivity evidence exist, but prior art is direct and local MS support is null. |
| Generic BET/bromodomain inhibition | `NO_GO` | Mechanistically unsupported as SP140 phenocopy; broader chromatin toxicity and different targets. |
| SP140 restoration | `PARK_THEORETICAL` | May be directionally relevant for SP140 loss-of-function Crohn genotypes, but no tractable restoration modality identified. |
| TOP1/TOP2 inhibition | `NO_GO_FOR_V3` | Cell 2022 supports topoisomerase involvement in SP140-loss Crohn macrophages, but broad topoisomerase inhibitors are cytotoxic and not module-selective. |
| Downstream IL1B/IL6/CCL2 suppression | `NO_GO_AS_SP140_ADJACENT` | These are generic inflammatory effectors; they do not preserve the SP140-specific genetic/cell-state rationale. |

## Explicit Blockers

1. No strict local MS anchor: white-matter delta `-0.087`, p `0.726`, FDR `0.968`.
2. No target-resolved MS coloc/MR evidence in current artifacts.
3. No public LINCS/CMap or local Perturb-seq SP140 perturbation profile beyond the Ghiboub supplemental macrophage data.
4. GSK761 raw sequencing is not directly available as simple GEO count matrices; article metadata points to `EGAS00001004460` and `GSE134809`, while public supplemental tables were sufficient only for summary-statistic overlap testing.
5. GSK761 has poor lead-like/CNS properties from PubChem descriptors; no CNS exposure or unbound brain concentration evidence found.
6. Directionality is unstable: SP140 inhibition suppresses inflammatory readouts in SP140-high macrophages, but SP140 loss of function is itself implicated in Crohn macrophage pathology through topoisomerase dysregulation.
7. Prior art is direct for SP140 inhibition in Crohn/inflammatory disease.

## Decisive Next Experiments

1. **Genotype-stratified macrophage perturbation.** Use primary human monocyte-derived macrophages from `SP140` risk/low-expression carriers and non-carriers, plus CRISPRi/CRISPRa/rescue controls. Treat with GSK761 and inactive matched analogs under LPS, IFNG, TNF, immune-complex, and myelin-debris conditions. Falsify the route if GSK761 does not reduce the V3 IFN/APC and inflammatory NF-kB readouts by at least 30% without worsening lipid-handling/efferocytosis genes, or if low-SP140 genotypes are harmed.
2. **MS-relevant cell test.** Run iPSC microglia or primary human microglia-like cultures with myelin debris plus IFNG/TNF. Read out RNA-seq, lipid droplet burden, lysosomal pH, myelin phagocytosis, antigen presentation, and viability. Falsify MS relevance if SP140 expression is low/uncoupled or GSK761 fails to shift module scores by at least 0.5 SD versus vehicle at non-toxic concentrations.
3. **Target engagement and selectivity.** In primary macrophages, measure SP140 engagement by CETSA/NanoBRET and SP140 CUT&RUN/ChIP at TNF, CXCL10, HLA, and lipid-handling loci. Include BET inhibitor and topoisomerase inhibitor controls. Falsify SP140 specificity if the transcriptomic effect is reproduced by BET/topoisomerase controls without SP140 occupancy loss.
4. **Tissue ex vivo validation.** Test Crohn, UC, psoriasis, and Sjogren inflamed tissue explants sorted or spatially assayed for SP140-high APC/myeloid states. Falsify cross-autoimmune breadth if only Crohn macrophages respond.
5. **Medicinal chemistry feasibility.** Before any CNS/MS claim, measure GSK761 solubility, microsomal stability, plasma protein binding, permeability, efflux, and brain unbound fraction. Falsify CNS feasibility if unbound CNS exposure cannot exceed cellular EC50 with a safety margin of at least 10x.

## Integration Recommendation

Do not spend the next V3 integration cycle trying to make SP140 the central cross-autoimmune node. The valid update from Wave56-K is narrower: SP140 is a real, druggable-ish epigenetic reader with published anti-inflammatory macrophage perturbation evidence, but the therapeutic route is already Crohn-focused, directionally genotype-sensitive, and weak for MS/lipid-lysosomal biology. If the orchestrator keeps SP140 alive, it should be as a comparator for "published SP140-high inflammatory macrophage inhibition" or as a stratification marker, not as the V3 lead target.
