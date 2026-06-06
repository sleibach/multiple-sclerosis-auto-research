# Wave48 Resolution-Reopener Audit

Random seed: `20260527`.

## Verdict

- `FPR2_ANXA1_BIASED_RESOLUTION`: `REOPEN_WITH_WETLAB_TEST_ONLY_NOT_V3_PROMOTION`.
  - Signal: FPR2 GWAS trait count=1, min_p=2e-06; FPR2 local positives=2.0 (Crohn disease;ulcerative colitis); ANXA1 rescue-context up=6.0 contexts/4.0 datasets; Wave37 FPR2 call=UNRESOLVED, ANXA1 call=UNRESOLVED; ChEMBL FPR2 activities=10101.
  - Blocker: dynamic resolution biology and chemical tractability exist, but strict MS expression anchor is negative/non-significant, the GWAS hit is not target-resolved, Wave37 efferocytosis perturbation is unresolved, and prior literature already covers SPM/FPR2 activity in autoimmune/EAE/colitis contexts.
  - Decisive reopen assay: human intestinal or synovial macrophage efferocytosis under lipid/IFN stress with biased FPR2 agonist plus antagonist rescue.
- `CD300_RECEPTOR_SPECIFIC_TUNING`: `REOPEN_ONLY_IF_RECEPTOR_SPECIFIC_PERTURBATION_NOT_V3_PROMOTION`.
  - Signal: CD300E direct positives=3.0 (Crohn disease;psoriasis;ulcerative colitis); CD300E Geneformer strong contexts=1.0; CD300A Wave37 median efficient-minus-noneater=1.3382347566762522, contrast_fdr=0.920009505703422; CD300LF Wave37 call=UNRESOLVED; strict MS positive anchors absent.
  - Blocker: family-level CD300 direction remains biologically unsafe: CD300A/F/LF/E have different inhibitory/activating roles, local MS anchoring is absent or negative, and the only strong-looking CRISPR contrast is not significant after FDR.
  - Decisive reopen assay: paired CD300A/CD300F/CD300E perturbation in human RA/IBD/MS myeloid cells with apoptotic-cell/myelin-debris uptake and cytokine readouts.

No branch satisfies V3 promotion gates. Both remain assay-reopeners only.

## Gate Matrix

- `FPR2_ANXA1_BIASED_RESOLUTION` / `specific_directionality`: PASS (`True`) - requires biased ligand or receptor-specific direction.
- `FPR2_ANXA1_BIASED_RESOLUTION` / `cross_autoimmune_local_signal`: PASS (`4.0`) - requires at least three disease/tissue signals.
- `FPR2_ANXA1_BIASED_RESOLUTION` / `strict_ms_anchor`: FAIL (`False`) - requires positive MS expression/state or target-resolved MS genetics.
- `FPR2_ANXA1_BIASED_RESOLUTION` / `real_perturbation_anchor`: FAIL (`False`) - requires real disease-relevant perturbation rather than expression recurrence.
- `FPR2_ANXA1_BIASED_RESOLUTION` / `foundation_model_support`: FAIL (`False`) - requires disease-context support beyond a single token/small context.
- `FPR2_ANXA1_BIASED_RESOLUTION` / `druggability_selectivity`: PASS (`True`) - requires targetable chemical/biologic matter and plausible selectivity.
- `FPR2_ANXA1_BIASED_RESOLUTION` / `prior_art_not_blocking`: PASS (`NOT_BLOCKED_BUT_IMMATURE`) - requires no blocking patent/clinical/prior-art status in route audit.
- `FPR2_ANXA1_BIASED_RESOLUTION` / `novelty_delta_sufficient`: FAIL (`1064`) - requires a direct delta beyond known autoimmune/efferocytosis literature.
- `CD300_RECEPTOR_SPECIFIC_TUNING` / `specific_directionality`: FAIL (`False`) - requires biased ligand or receptor-specific direction.
- `CD300_RECEPTOR_SPECIFIC_TUNING` / `cross_autoimmune_local_signal`: PASS (`3.0`) - requires at least three disease/tissue signals.
- `CD300_RECEPTOR_SPECIFIC_TUNING` / `strict_ms_anchor`: FAIL (`False`) - requires positive MS expression/state or target-resolved MS genetics.
- `CD300_RECEPTOR_SPECIFIC_TUNING` / `real_perturbation_anchor`: FAIL (`False`) - requires real disease-relevant perturbation rather than expression recurrence.
- `CD300_RECEPTOR_SPECIFIC_TUNING` / `foundation_model_support`: PASS (`True`) - requires disease-context support beyond a single token/small context.
- `CD300_RECEPTOR_SPECIFIC_TUNING` / `druggability_selectivity`: FAIL (`False`) - requires targetable chemical/biologic matter and plausible selectivity.
- `CD300_RECEPTOR_SPECIFIC_TUNING` / `prior_art_not_blocking`: PASS (`NOT_BLOCKED_BUT_DIRECTION_AMBIGUOUS`) - requires no blocking patent/clinical/prior-art status in route audit.
- `CD300_RECEPTOR_SPECIFIC_TUNING` / `novelty_delta_sufficient`: FAIL (`145`) - requires a direct delta beyond known autoimmune/efferocytosis literature.

## Traceable Outputs

- `route_reopener_audit.tsv`: route-level verdicts.
- `decision_matrix.tsv`: strict promotion gates.
- `candidate_gene_evidence.tsv`: gene-level local, perturbation, foundation-model, and ChEMBL evidence.
- `public_api_counts.tsv`: cached prior and live Europe PMC / ClinicalTrials.gov counts.
- `patent_search_urls.tsv`: patent search URLs retained for manual verification.

