# Wave49-G PTPN22 Directionality Critique

Status: completed. Advisory only; no files were edited by the subagent.

## Verdict

`NO_GO`.

`PTPN22` should not be promoted to a V3 therapeutic candidate. The best
interpretation is: genetically interesting, chemically probeable, but not
MS-anchored, not direction-resolved, not selectively druggable enough, and not
novel enough.

## Strongest Evidence

- Local V3: Wave47 keeps `PTPN22` as `REOPEN_WITH_NEW_TEST_ONLY`, explicitly
  missing `correct_direction_modality`, `direction_resolution`, and
  `target_resolved_coloc_or_mr`.
- Local Wave34A: broad autoimmune GWAS Catalog signal across 28 traits, minimum
  p about `5e-174`, plus ChEMBL target `CHEMBL2889`.
- Mechanistic literature supports plausibility of inhibitor biology: LTV-1/LYP
  inhibition modulates TCR signaling, and PTPN22 blockade restored defective
  central B-cell tolerance in a humanized model. Advisory sources: Vang 2012
  PubMed; Schickel 2016 PubMed.
- Newer RA/neutrophil work supports inhibitor-side biology in inflammatory
  arthritis models, but not MS or cross-autoimmune translation. Advisory
  source: Gardette 2025 PubMed.

## Strongest Blockers

- MS anchor is weak: local MS white-matter signal is nominal only
  (`delta=0.82`, `p=0.031`, `FDR=0.85`) and residual cross-disease support is
  absent. Published meta-analysis reportedly finds negligible association of
  `PTPN22 C1858T` with MS. Advisory source: Zheng 2012 PubMed.
- R620W-like direction is not clean enough for therapy. Inhibition can look
  corrective in B/T-cell tolerance models, but PTPN22 biology is
  cell-context-dependent, including myeloid/neutrophil effects.
- Selectivity remains a core medicinal-chemistry liability. Local ChEMBL pulls
  confirm many PTPN22 rows, but the off-target scan found top molecules with
  stronger `PTPN1` activity than `PTPN22` in some cases.
- Clinical translation is absent: current ClinicalTrials.gov search finds
  PTPN22 observational/genetic studies, but `PTPN22 inhibitor` returns zero
  interventional trials.
- Novelty is poor: advisory patent scan identified Yale claims on PTPN22
  inhibition for autoimmune disease including MS (`WO2017205765A1` /
  `US11311543B2`), Purdue LYP inhibitor IP (`US11629130B2`), and
  Indiana/Purdue benzofuran/LYP inhibitor chemistry (`WO2012149048A1`).

## Closest Prior Art

- Yale/Schickel-Meffre: PTPN22 inhibition to restore central B-cell tolerance
  and treat autoimmune disease, including MS claims: Google Patents
  `WO2017205765A1`.
- Purdue: LYP/PTPN22 small-molecule inhibitor matter and autoimmune /
  cancer-immunotherapy uses: Google Patents `US11629130B2`.
- Indiana/Purdue benzofuran/LYP inhibitor chemistry: Google Patents
  `WO2012149048A1`.
- LTV-1 and follow-on PTPN22 probes, including 2025 improved isozyme-selective
  compound 8b-19. Advisory source: Jassim 2025 PubMed.

## Decisive Experiment

Run an allele-stratified primary human assay package across MS, RA/T1D/SLE, and
healthy donors: R620W carriers vs noncarriers; T cells, transitional B cells,
monocytes/neutrophils; selective PTPN22 inhibition vs CRISPR/base-edit rescue
vs inactive analog; plus PTPN22 rescue to prove on-target action.

Revive only if one direction reverses R620W-like autoimmune phenotypes and
MS-relevant inflammatory modules without broad immune activation and with clean
selectivity over `PTPN1`, `PTPN2`, and `PTPN11`. Otherwise, close permanently.
