# Wave50 GPR65 Acid-Sensing GPCR Audit

Random seed: `20260527`.

## Verdict

`GPR65`: `NO_GO_GPR65_PRIOR_ART_AND_LOCAL_CELLSTATE_MISMATCH`.

GPR65 has cross-disease genetic support (5 OT diseases: AS;Crohn;MS;Psoriasis;UC; 5 GWAS traits, min p=4e-18) and GPCR chemical matter, but local support is weak and contradictory (positive diseases=1.0, negative diseases=2.0), MS expression support is absent (delta=0.09040507812532, p=0.6241465917972195), and direct IBD/autoimmune prior art blocks novelty.

Primary blocker: GPR65 remains a plausible biology axis but not a V3 finding: target-resolved direction, non-IBD coloc, and disease-cell agonist/PAM perturbation are missing, while public literature/patent prior art already covers autoimmune GPR65 modulation.

Decisive reopen test: Fine-map non-IBD/MS GPR65 colocalization and test selective agonist/PAM rescue in acidic human MS/psoriasis/AS myeloid or T-cell contexts with cAMP, Th17, and lipid-lysosomal inflammatory readouts.

## Gate Matrix

- `cross_disease_genetic_breadth`: PASS (`OT_diseases=5; GWAS_traits=5; min_p=4e-18`) - requires broad disease genetics.
- `target_resolved_coloc_or_mr`: FAIL (`not_run/no_target_resolved_coloc`) - requires fine-mapped direction rather than mapped-gene support.
- `strict_ms_anchor`: FAIL (`delta=0.09040507812532; p=0.6241465917972195; fdr=0.9490245393797272`) - requires MS state signal beyond nominal/noise.
- `local_cell_state_alignment`: FAIL (`positive=1.0; negative=2.0`) - requires local support not contradicted by negative disease signals.
- `real_perturbation_anchor`: FAIL (`absent`) - requires GPR65 agonist/PAM rescue in disease-relevant cells.
- `selective_modality_exists`: PASS (`activity_rows=99; best_nM=364.84`) - requires tractable GPCR chemical matter.
- `clinical_whitespace`: PASS (`ClinicalTrials_max=0`) - requires no active direct clinical program.
- `novelty_prior_art_not_blocking`: FAIL (`patent_block=True; EuropePMC_max=76`) - requires no direct autoimmune/IBD patent-literature blockage.

## Public Source Snapshot

- EuropePMC `GPR65 TDAG8 agonist autoimmune multiple sclerosis`: count=30; top hits: 40563452: Proton-Sensing G Protein-Coupled Receptors and Their Potential Role in Exercise Regulation of Arterial Function. (2025) | 41775781: Integrative mendelian randomization approaches for therapeutic target prioritisation in immune-mediated diseases. (2026) | 38527054: The proton-sensing receptors TDAG8 and GPR4 are differentially expressed in human and mouse oligodendrocytes: Exploring their role in neuroinflammation and multiple sclerosis. (2024) | 39336742: The Roles of Proton-Sensing G-Protein-Coupled Receptors in Inflammation and Cancer. (2024) | 39028811: Small-molecule probe for IBD risk variant GPR65 I231L alters cytokine signaling networks through positive allosteric modulation. (2024)
- EuropePMC `GPR65 inflammatory bowel disease therapeutic target agonist`: count=76; top hits: 41964562: Unveiling the impact of colonic pH and pH-sensing receptors in blood pressure regulation. (2026) | 40898810: GPR65 Functions as a Key Factor of Bone Aging and a Novel Therapeutic Target for Osteoporosis. (2025) | 41775781: Integrative mendelian randomization approaches for therapeutic target prioritisation in immune-mediated diseases. (2026) | 41595528: Joint Acidosis and GPR68 Signaling in Osteoarthritis: Implications for Cartilage Gene Regulation. (2026) | 41190345: Acid sensing to inflammaging: mechanisms and therapeutic promise of GPR68 (OGR1) in aging-related diseases. (2025)
- EuropePMC `GPR65 Th17 autoimmune pH sensing GPCR`: count=12; top hits: 39336742: The Roles of Proton-Sensing G-Protein-Coupled Receptors in Inflammation and Cancer. (2024) | 39358616: GPCRs: emerging targets for novel T cell immune checkpoint therapy. (2024) | 39028811: Small-molecule probe for IBD risk variant GPR65 I231L alters cytokine signaling networks through positive allosteric modulation. (2024) | 39483470: <i>In silico</i> and pharmacological evaluation of GPR65 as a cancer immunotherapy target regulating T-cell functions. (2024) | 38514581: Role of pH-sensing receptors in colitis. (2024)
- ClinicalTrials.gov `GPR65 autoimmune`: count=0; top hits: 
- ClinicalTrials.gov `GPR65 agonist`: count=0; top hits: 
