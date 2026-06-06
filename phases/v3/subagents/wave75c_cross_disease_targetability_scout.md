# Wave75-C cross-disease targetability scout

Date: 2026-05-27. Scope: existing local artifacts only. This is a
falsification-first targetability scout for recurrent IFN/APC plus
lysosomal/APC-adjacent biology. It is not a therapeutic finding.

## Bottom line

No node is promotable from the current local evidence. After excluding the
explicitly demoted branches and the locally closed checkpoint/complement/Fc/
lipid-mediator/cathepsin routes, only a small set remains worth a strict local
follow-up test. The best scout is `CD58`; the best mechanistic lysosomal
transporter scout is `SPNS1`. `P4HB` and `SEL1L3` are weaker accessibility
checks. `IFI30` is retained only as a target-resolution benchmark, not as a
targetability nomination.

## Files inspected

- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_lipid_lysosomal_neighborhood_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_ms_positive_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
- `results_v3/wave21_residual_druggability_scan/wave21_residual_druggability_ranked_full.tsv`
- `subagents_v3/wave21_residual_druggability_scan.md`
- `results_v3/wave23_orchestrator_nonexpression_axis_triage/chembl_api_target_snapshot.tsv`
- `subagents_v3/wave23_metabolite_barrier_circuit.md`
- `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
- `subagents_v3/wave34a_genetics_first_target_rescue.md`
- `subagents_v3/wave34c_checkpoint_prior_art_sanity.md`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank.tsv`
- `subagents_v3/wave39b_accessibility_prior_art_critique.md`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_gate_matrix.tsv`
- `subagents_v3/wave62v_opentargets_target_resolution.md`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave69_parked_controller_rank/REPORT.md`
- `results_v3/wave71_global_survivor_meta_rank/global_survivor_meta_rank.tsv`
- `subagents_v3/wave71a_global_survivor_meta_rank.md`
- `subagents_v3/wave71b_prior_branch_status_synthesis.md`
- `subagents_v3/wave74c_prior_art_druggability_scout.md`
- `DATA_V3.md`, `ORCHESTRATION_LOG_V3.md`

## Exclusion rule applied

I excluded the named no-go/demoted branches: `ACSL1`, `NAMPT`, `GALC`/`ASAH1`,
cathepsins, complement/`CFB`, `GPR65`, `MFGE8`, `PTPN2`/`PTPN22`, `CXCR2`,
`IL7R`, `SP140`, `SLAMF7`, Fc/ROS/`LILRB`/`INPP5D`, `P2RX7`, `EPHX2`,
`GPR183`, and `NAAA`. I also did not rank direct HLA/CD74/MIF/JAK/STAT,
checkpoint/costimulation, `CD44`/`SPP1`, `LTA4H`/leukotriene, S1P, AHR/IDO,
PPAR/LXR/RXR, SCFA, bile-acid, and broad eicosanoid routes because local
checkpoint or circuit reports already mark them as prior-arted, generic,
directionally conflicted, or expression-only.

## Ranked targetability table

| Rank | Node | Modality class | Local positive evidence | Why not already closed | Missing evidence and blocker | Exact next falsifying test |
|---:|---|---|---|---|---|---|
| 1 | `CD58` | surface ligand; biologic or CD2/CD58 interface modulation | Wave71 top non-reopener; Wave62 MS L2G `0.951`, same-target QTL in `Crohn;MS`, module-link gate true, local positives in Crohn/T1D/UC. | Not in the explicit no-go list or Wave34-C checkpoint axes. Wave62 had no manual/prior blocker; Wave71 blocks only for insufficient convergence and missing perturbation/modality. | Needs proof the signal is APC/myeloid-state relevant rather than T-cell admixture or generic immune synapse biology. No local perturbation. | Run donor-level residual models for `CD58` in broad h5ad APC/myeloid compartments plus MS white-matter, adjusting for IFN/APC, HLA-II/CD74, lysosome_APC, cell-count, and generic inflammation. Close if `CD58` is not positive after residualization in MS plus at least two non-MS APC/myeloid diseases, or if GSE282122 DC/mono-macro remission deltas do not move in the same direction at remission-adjusted FDR <= 0.10. |
| 2 | `SPNS1` | lysosomal membrane transporter; genetic/chemical tool or transporter biology | Wave39: positive in 4 diseases (`Crohn`, `Sjogren`, `psoriasis`, `T1D`), transmembrane lysosomal protein, phospholipid salvage function; Wave62 local positives also 4 diseases. | Not one of the closed lysosomal enzymes, sphingolipid nodes, or lipid mediators. Current no-go is missing MS anchor and missing druggability, not a target-specific prior-art or wrong-direction closure. | No MS support, no ChEMBL activity, no target genetics, and no perturbation. Risk: generic lysosomal-stress marker. | In existing broad h5ad contrasts plus MS white-matter, residualize `SPNS1` against IFN/APC, HLA-II/CD74, lysosome_APC, `LIPA`, `IFI30`, and tissue injury/stromal markers. Close if MS is not positive nominally and fewer than three APC/myeloid disease contexts retain positive residual effect, or if the retained signal localizes mainly to epithelial/stromal compartments. |
| 3 | `P4HB` | accessible redox/isomerase enzyme; small-molecule or biologic tool | Wave39: accessible/catalytic, exact ChEMBL target `CHEMBL5422`, 702 activity rows, best returned value 3 nM; positive in 4 diseases (`Crohn`, `Sjogren`, `psoriasis`, `UC`). | Not a prior V3 named no-go branch. It was rejected by the surfaceome pass for no MS anchor/insufficient breadth, not because a target-specific autoimmune blocker was established. | No MS anchor; likely generic ER/protein-folding and viability biology; not clearly lysosomal/APC causal. | Test `P4HB` only if it has an MS white-matter or treatment-response anchor independent of generic ER stress. Close if broad h5ad residualization against IFN/APC, HLA-II/CD74, unfolded-protein/stress, and epithelial/stromal injury leaves fewer than three positive diseases or MS remains null/negative. |
| 4 | `SEL1L3` | membrane protein; possible antibody/surface handle only | Broad MS-positive rank: Crohn/T1D/UC positives, MS white-matter delta `0.923`, p `0.018`; Wave39 accessible single-pass membrane row. | Earlier Wave10/Wave39 demoted it as undercharacterized/expression-marker biology, but no target-specific prior-art or directionality closure exists. | Biology and modality are too thin; no ChEMBL, no genetics, no perturbation, no known ligand/pathway connection to APC lysosomes. | Perform cell-compartment localization and residualization. Close if `SEL1L3` is not APC/myeloid-enriched after excluding stromal/endothelial contamination, or if MS positivity disappears after injury/stromal and IFN/APC adjustment. |

## Benchmark, not nomination

`IFI30` is the closest mechanistic APC/lysosomal benchmark: broad h5ad positive
in psoriasis/T1D/UC, Wave62 MS target-resolution with L2G around `0.65` and
same-target QTL support in `Celiac;Crohn;MS`, and direct lysosomal antigen
processing relevance. It is not ranked as a clean target because Wave62 already
flags direct antigen-processing/host-defense/druggability, Wave39 excludes
`IFI30`-like lysosomal loading nodes on expression alone, and no modality is
available locally. The useful falsifier is simple: if `IFI30` does not retain
MS plus at least two non-MS APC/myeloid residual signals after HLA-II/CD74,
cathepsin, IFN/APC, and lysosome_APC adjustment, close it permanently as a
state readout.

## Near misses explicitly not ranked

- `PTGER4`: targetable GPCR with strong ChEMBL matter and Wave62 target
  resolution in Crohn/MS/UC, but Wave34A and Wave62 already mark EP4 direction
  and prior-art context as conflicted; also not module-specific.
- `RGS1`/`RGS14`/`INAVA`/`MMEL1`: target-resolution or response intersections
  exist, but reports mark weak module linkage, poor modality, or independent
  validation failure. They are genetics benchmarks, not targetability leads.
- `LTA4H`/`ALOX5`/`ALOX5AP`/LTB receptors: druggable and superficially
  myeloid-lipid relevant, but local reports already demote leukotriene biology
  for prior art, zero/weak model support, and generic inflammatory direction.
- `PPIA`, `CHI3L1`, `SLPI`, `LTF`, `CCL20`, `CXCL9`: reachable proteins but
  marker/secreted-injury/chemokine biology; insufficient specificity for the
  IFN/APC plus lysosomal/APC state.

## Recommendation

Run one local falsification pass, not a broad re-rank. Test `CD58`, `SPNS1`,
`P4HB`, and `SEL1L3` with the same residual model and response-direction gate.
If none retains APC/myeloid, MS, and treatment-response support after IFN/APC,
HLA-II/CD74, lysosomal, injury, and cell-mixture adjustment, do not spend more
V3 effort on targetability from expression recurrence.
