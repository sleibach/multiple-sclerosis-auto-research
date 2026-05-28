# Wave50-G GPR65 Acid-Sensing GPCR Critique

Status: completed and closed.

## Verdict

`NO_GO`.

GPR65 agonism/PAM should not be promoted to a V3 therapeutic candidate. It has
real biology and chemical matter, but the V3 package fails the promotion bar:
no target-resolved MS/non-IBD directionality, weak contradictory local
cell-state evidence, no MS expression anchor, and direct GPR65 autoimmune/IBD
prior art.

## Strongest Evidence

- Genetics: local V3 genetics shows GPR65 across AS/Crohn/MS/Psoriasis/UC,
  minimum GWAS p = `4e-18`.
- Directional IBD biology is plausible: I231L/rs3742704 and linked rs8005161
  reduce GPR65/cAMP signaling; acid-pH GPR65 signaling is generally
  anti-inflammatory in myeloid/DC contexts.
- PAM tool biology exists: BRD5075/BRD5080 potentiate GPR65/I231L and alter
  dendritic-cell cytokine programs.
- Colitis prior biology supports activation as anti-inflammatory, mainly in
  IBD/CAC models.

## Strongest Blockers

- Local gate fails target-resolved genetics:
  `target_resolved_coloc_or_mr=False` and no fine-mapped causal direction in
  `results_v3/wave50_gpr65_acid_sensing_gpcr_audit/decision_matrix.tsv`.
- Local cell-state evidence is not aligned: only 1 positive disease versus 2
  negative, no FDR10 positives, and not lipid/lysosomal myeloid-neighborhood
  positive in the broad H5AD table.
- MS anchor is absent locally: MS white-matter delta `0.09`, p = `0.624`,
  FDR = `0.949`.
- MS biology is directionally unsafe: a PLOS 2024 paper reports TDAG8/GPR65 up
  in MS plaques but does not establish a robust oligodendrocyte/myelination
  role and notes conflicting EAE literature.
- Prior art is blocking: Pathios GPR65 modulator patent families claim immune
  and autoimmune uses including MS, Crohn's, psoriasis, ankylosing spondylitis,
  and ulcerative colitis.
- Clinical prior art exists for GPR65, but with opposite modality:
  `PTT-4256` is in Phase 1/2 solid tumors, not autoimmune agonism/PAM.

## Closest Prior Art Flagged By Subagent

- Neale et al. 2024 Science Advances: BRD5075/BRD5080 GPR65 PAMs for IBD-risk
  I231L cytokine modulation.
- Pathios `WO2023067322A1` and `WO2024224064A1`: GPR65 modulators with
  autoimmune/MS claims.
- `PTT-4256`: clinical GPR65 inhibitor in oncology.

## Reopen-Only Experiment

Run a genotype-stratified acidic-pH human primary-cell perturbation:
rs3742704/rs8005161 carriers versus noncarriers, MS/IBD-relevant
monocyte-derived DC/myeloid plus Th17 co-culture, pH 6.6-6.8, selective GPR65
PAM versus inactive analog and GPR65 loss/block control. Require on-target
cAMP/CREB rescue, reduced IL-12/23/TNF/GM-CSF or antigen-presentation state,
and no Th17/EAE-like worsening. Failure keeps `NO_GO`; success would only
justify reopening, not immediate promotion.

