# Wave 7 Lipid-Myeloid Target Scout

Role: target-scout worker, wave 7.

Scope: successor intervention nodes in the cross-autoimmune lipid-lysosomal /
inflammatory myeloid module after demotion of `ACSL1`, `NAMPT`, `LIPA`,
`CD74/HLA`, complement/C1q, and `OSM/OSMR`.

Conclusion discipline: this is not a final finding. It is a hostile scout
report for the orchestrator. "Go" below means "worth the next computational
test", not therapeutic promotion.

## 1. Candidate Shortlist With Mechanism And Intervention Point

| Rank | Candidate axis | Mechanism hypothesis | Plausible intervention point | Scout disposition |
|---:|---|---|---|---|
| 1 | `LGALS3` / galectin-3 | Glycan-binding macrophage/microglial checkpoint coupled to phagocytosis, lysosomal stress, myelin debris handling, inflammasome/fibrosis-like tissue injury. | Galectin-3 inhibitor or context-specific modulation; test whether inhibition reduces inflammatory state without blocking debris clearance. | **Best next computational test.** Not promoted; cross-disease local breadth is still weak. |
| 2 | `GPNMB` surface/reparative lipid-loader state | Foamy/lipid-loaded phagocyte marker with tissue-remodeling and immunoregulatory biology. | Do not deplete chronically. Possible use as state marker, delivery handle, or agonistic/reparative biology only after direction tests. | **Hold / no-go as direct target.** Strong MS marker, weak intervention hypothesis. |
| 3 | `CTSS` / `CTSB` / `CTSD` / `CTSL` cathepsins | Lysosomal proteolysis, antigen processing, matrix/myelin debris turnover. | Selective cathepsin inhibition, most tractable for `CTSS`; avoid broad cathepsin blockade. | **Hold / no-go.** Druggable but prior-arted and repair/specificity risks are unresolved. |
| 4 | `SPP1` / `CD44` / integrins | Osteopontin-driven injury macrophage survival, migration, retention, and tissue remodeling. | Anti-osteopontin, CD44 blockade, or integrin pathway intervention. | **No-go as a novel successor.** Broad biology but crowded, broad-liability, and weak MS single-gene SPP1 support locally. |
| 5 | TAM / TREM2 module: `AXL`, `MERTK`, `TYRO3`, `TREM2`, `TYROBP` | Efferocytosis, apoptotic/debris clearance, lipid-loaded microglial repair states. | Prefer agonism / repair-preserving activation, not blockade. | **Hold.** Attractive biology, but local disease direction is mixed and drug direction is immature. |
| 6 | `LRP1` / `CALR` clearance/DAMP axis | "Eat-me" / DAMP clearance, efferocytosis, antigen handling, tissue stress. | Cargo- or context-specific efferocytosis modulation; direct systemic targeting is too broad. | **No-go as direct target.** Useful safety/repair control. |
| 7 | `LTA4H` / leukotriene B4 / `LTB4R1` | Lipid-mediator amplification in inflammatory myeloid cells adjacent to foamy microglia and IBD myeloid activation. | Inhibit `LTA4H` enzymatic activity, or block downstream BLT1/BLT2 signaling. | **No-go after orchestrator update.** Attractive expression screen, but Geneformer support is zero and prior art blocks. |
| 8 | `PLA2G7`, `TBXAS1`, `MGLL/MAGL` and other oxylipin enzymes | Lipid mediator production in foamy lesions. | Enzyme inhibition. | **No-go as successor claim.** `MGLL/MAGL` is an explicit benchmark/exclusion; `TBXAS1` and `PLA2G7` are blocked locally. |

Best next candidate for orchestrator computational testing: **`LGALS3`**.

Rationale: after the 22:34 UTC orchestrator demotion of `LTA4H`, `LGALS3` is
the remaining node with the best combination of MS foamy/MIMS2 evidence,
druggability, and an intervention hypothesis that is not simply an already
demoted enzyme lane. It still fails the final V3 standard today: local
cross-disease breadth is not established, no clean genetics/coloc/MR support
was found, and the intervention direction could damage repair/remyelination.

## 2. Candidate Evidence Details

### `LTA4H` / LTB4 / BLT1

Mechanism and intervention point:

`LTA4H` converts leukotriene A4 to leukotriene B4, a potent myeloid
chemoattractant/activation lipid mediator. This is adjacent to, but distinct
from, the demoted `PLA2G7` and `TBXAS1` lipid-mediator lanes. Intervention is
straightforward in principle: inhibit `LTA4H` enzymatic activity or block
downstream leukotriene B4 receptors (`LTB4R1`/BLT1, `LTB4R2`/BLT2). The
claim would have to be tested as an inflammatory-myeloid lipid-mediator node,
not as a generic anti-inflammatory. However, this axis has now been demoted by
the orchestrator after the Geneformer candidate-deletion screen.

MS relevance:

- Local V3 broad screen: MS white-matter microglia `LTA4H` delta 0.809,
  Hedges g 1.357, p=0.00636 in `results_v3/gse111972_full_ms_wm_signature.tsv`
  and `results_v3/broad_h5ad_gene_discovery/broad_h5ad_ms_positive_rank.tsv`.
- Local MIMS2/foamy support: `GSE301908` MIMS2-like microglia effect 1.483,
  p=0.0108; foamy lesion proteomics effect 0.169, p=0.0321 in
  `results_v3/existing_evidence_candidate_matrix.tsv`.
- External MS lipid-mediator context: Van der Vliet et al. report foamy
  microglia/oxylipin biology in MS and nominate MAGL/MGLL as a direct
  intervention benchmark. That source strengthens the local oxylipin module,
  but `MGLL` itself is not available as a novel claim here.
  Source: https://www.nature.com/articles/s41593-026-02302-3

Cross-autoimmune breadth:

- Local positives are three diseases, not five: Crohn myeloid delta 1.229,
  p=0.00719; ulcerative colitis myeloid delta 1.177, p=0.0196; T1D acinar
  delta 0.427, p=0.00872. No local negative disease at the broad-screen
  threshold, but psoriasis trends negative and Sjogren is neutral.
- Plausibility beyond local hits exists for MS/EAE, IBD, RA, psoriasis,
  lupus nephritis, and T1D through leukotriene B4 biology, but this is
  pathway-level and must not be counted as validated single-gene breadth.
  Examples to verify/use: EAE BLT1/leukotriene work
  (https://pubmed.ncbi.nlm.nih.gov/?term=leukotriene+B4+BLT1+experimental+autoimmune+encephalomyelitis),
  RA leukotriene B4 work
  (https://pubmed.ncbi.nlm.nih.gov/?term=leukotriene+B4+rheumatoid+arthritis+LTA4H),
  lupus nephritis leukotriene B4 work
  (https://pubmed.ncbi.nlm.nih.gov/?term=leukotriene+B4+lupus+nephritis),
  psoriasis leukotriene B4 work
  (https://pubmed.ncbi.nlm.nih.gov/?term=leukotriene+B4+psoriasis).

Genetics / coloc / MR:

- No local coloc/MR support found.
- Local OpenTargets candidate table did not contain a usable `LTA4H`
  autoimmune hit.
- A small Crohn-disease candidate association for `LTA4H` has been reported
  in a Chinese cohort, but this is not a V3-grade genetics anchor without
  replication/colocalization.
  Source: https://pubmed.ncbi.nlm.nih.gov/?term=LTA4H+Crohn+disease+genetic+association
- GWAS Catalog gene page checked as a to-verify genetics source:
  https://www.ebi.ac.uk/gwas/genes/LTA4H

Perturbation / drug-response evidence:

- Local Geneformer deletion results are negative by the posthoc rule. `LTA4H`
  had 4 contexts with token, 6 disease cells with token, aggregate cosine /
  projection shifts below support threshold, and 0 support contexts
  (`results_v3/geneformer_candidate_delete/geneformer_candidate_delete_metrics.tsv`).
- External pharmacology exists through LTA4H inhibitors and BLT antagonists.
  Acebilustat is a clinical LTA4H inhibitor program in cystic fibrosis, useful
  for druggability rather than autoimmune proof.
  Sources: https://pubmed.ncbi.nlm.nih.gov/?term=acebilustat+LTA4H+inhibitor,
  https://clinicaltrials.gov/search?term=acebilustat

Druggability:

- Enzyme target with existing inhibitor chemistry and clinical precedent.
- Need confirm CNS exposure if the desired indication remains MS/progressive MS.
  Peripheral autoimmune testing may not require CNS-penetrant exposure.

Prior-art blockers:

- Leukotriene biology and BLT antagonism are heavily prior-arted in
  inflammatory disease.
- `MGLL/MAGL` is a direct MS foamy-microglia intervention benchmark and is
  explicitly an exclusion boundary in the local workspace (`REFRAME.md`,
  `THERAPEUTIC_PLAN.md`).
- A valid claim would need to be `LTA4H`-specific, cross-disease, and not just
  "another oxylipin enzyme in foamy MS lesions".

Go/no-go:

**No-go.** Do not force `LTA4H` after the orchestrator's Geneformer/prior-art
demotion. Keep it as a lipid-mediator comparator for `LGALS3` and cathepsin
tests because its expression evidence is useful, but do not hand it back as
the next promoted candidate.

### `LGALS3` / Galectin-3

Mechanism and intervention point:

Galectin-3 sits at a plausible intersection of phagocytosis, glycan sensing,
lysosomal damage, microglial/macrophage activation, inflammasome biology, and
fibrotic tissue remodeling. Intervention could be galectin-3 inhibition, but
the biology may require context-specific modulation rather than simple blockade.

MS relevance:

- Local MS foamy lesion proteomics: effect 0.339, p=0.00420.
- Local `GSE301908` MIMS2-like microglia: effect 0.872, p=0.00592.
- Galectin-3 has direct MS/EAE and remyelination literature; the direction is
  not uniformly "block is good". It can participate in inflammatory activation
  and also in debris handling/remyelination.
  Sources: https://pubmed.ncbi.nlm.nih.gov/?term=galectin-3+multiple+sclerosis+experimental+autoimmune+encephalomyelitis,
  https://pubmed.ncbi.nlm.nih.gov/?term=galectin-3+remyelination+microglia

Cross-autoimmune breadth:

- Local V3 breadth is weak: `LGALS3` is MS-supported in
  `results_v3/existing_evidence_candidate_matrix.tsv`, but it was not a broad
  local cross-disease hit in the core V3 summary tables.
- External plausibility spans RA, SLE/lupus nephritis, IBD, psoriasis,
  Sjogren/fibrotic gland injury, and T1D, but this is literature-level and
  needs local quantification before promotion.
  Source query: https://pubmed.ncbi.nlm.nih.gov/?term=galectin-3+autoimmune+disease+macrophage

Genetics / coloc / MR:

- No local coloc/MR support found.
- No V3-grade genetic anchor identified in the local genetics reports.

Perturbation / drug-response evidence:

- No local LINCS/State named-gene perturbation evidence found.
- External EAE/manipulation literature exists but is directionally complex.
- Galectin-3 inhibitors have clinical development precedent, mostly outside
  autoimmunity.
  Sources: https://pubmed.ncbi.nlm.nih.gov/?term=belapectin+galectin-3+inhibitor,
  https://pubmed.ncbi.nlm.nih.gov/?term=GB0139+TD139+galectin-3+inhibitor,
  https://clinicaltrials.gov/search?term=galectin-3%20inhibitor

Druggability:

- Druggable as an extracellular/intracellular lectin with small molecules and
  carbohydrate-derived inhibitors in clinical development.
- Selectivity, intracellular exposure, and tissue distribution are major
  concerns.

Prior-art blockers:

- Galectin-3 is crowded in MS/EAE, fibrosis, macrophage activation, and
  inflammasome literature.
- Repair risk is a serious blocker: a blunt inhibitor could worsen myelin
  clearance/remyelination.

Go/no-go:

**Go for the next computational test, not therapeutic promotion.** `LGALS3`
is the best remaining scout handoff after `LTA4H` demotion, but the test must
be designed to fail fast. Require disease breadth beyond MS, and require a
repair-vs-inflammation split showing that predicted galectin-3 inhibition
reduces harmful inflammatory myeloid state without suppressing debris
clearance/remyelination programs.

### `GPNMB`

Mechanism and intervention point:

`GPNMB` marks lipid-loaded, phagocytic, tissue-remodeling myeloid states and is
surface-accessible. The intervention problem is that it may be reparative or
damage-limiting. Depletion or antagonism is not justified from the current
evidence.

MS relevance:

- Strongest local MS marker among this wave's examples:
  `GSE111972` sorted microglia: MS white-matter delta 1.434, Hedges g 1.356,
  p=0.00491; all-MS delta 1.617, p=0.00714.
- Local foamy/MIMS2 convergence: foamy lesion proteomics effect 2.164,
  p=3.50e-10; `GSE301908` MIMS2-like effect 2.097, p=0.00592.
- Local spatial support: `GSE284005` pathological-vs-homeostatic effect 1.743,
  p=0.03125.
- External foamy-microglia MS context:
  https://www.nature.com/articles/s41593-026-02302-3

Cross-autoimmune breadth:

- Local bulk/existing evidence: positive in active UC, active Crohn, lupus
  nephritis tubulointerstitium, Sjogren trend, but negative in RA macrophages
  and psoriasis skin.
- Direct donor-level h5ad evidence is not supportive: UC myeloid and psoriasis
  keratinocyte trend negative.
- Cross-disease result is therefore "state marker with mixed direction", not a
  central intervention node.

Genetics / coloc / MR:

- No local coloc/MR or strong OpenTargets genetic support found.

Perturbation / drug-response evidence:

- Surface-targeting precedent exists in oncology through anti-GPNMB antibody
  drug conjugates such as glembatumumab vedotin, but that supports targetability,
  not a chronic autoimmune mechanism.
  Sources: https://pubmed.ncbi.nlm.nih.gov/?term=glembatumumab+vedotin+GPNMB,
  https://clinicaltrials.gov/search?term=glembatumumab%20vedotin

Druggability:

- Surface protein; antibody/ADC precedent.
- For chronic autoimmune disease, cytotoxic depletion is likely the wrong
  modality unless a pathogenic subset is proven.

Prior-art blockers:

- Strong MS foamy-microglia marker prior art.
- Oncology ADC prior art is not therapeutically aligned with autoimmune repair.
- Directionally inconsistent across autoimmune tissues.

Go/no-go:

**No-go as a direct target.** Keep as a pharmacodynamic/state marker and
possible delivery handle. Do not advance as antagonist/depletion target.

### Cathepsin Proteases: `CTSS`, `CTSB`, `CTSD`, `CTSL`

Mechanism and intervention point:

Cathepsins connect lysosomal proteolysis, antigen processing, extracellular
matrix remodeling, and myelin/debris turnover. `CTSS` is the most obvious
inhibitor target; `CTSD`/`CTSL`/`CTSB` are more likely to be state or repair
markers unless a selective path is demonstrated.

MS relevance:

- Local `CTSD`: MS white-matter microglia delta 0.493, Hedges g 0.940,
  p=0.0483; foamy proteomics effect 0.607, p=8.19e-06; MIMS2-like effect
  1.471, p=0.00592.
- Local `CTSL`: foamy proteomics effect 0.610, p=0.000678; MIMS2-like effect
  1.021, p=0.0249.
- Local `CTSS`: weaker MS microglia signal but strong IBD myeloid/T1D/AITD
  support.
- Local `CTSB`: broad inflammatory signal, but weaker MS anchoring.

Cross-autoimmune breadth:

- `CTSS`: trend-or-better in Crohn, Hashimoto thyroiditis, T1D, and UC.
- `CTSB`: Crohn, psoriasis, and T1D.
- `CTSD`: Hashimoto thyroiditis and MS; but negative in Crohn/UC myeloid direct
  h5ad contrasts.
- Older/bulk evidence broadens the cathepsin signal, but direction and
  compartment are not clean.

Genetics / coloc / MR:

- Local OpenTargets table has limited disease-target support for `CTSS`/`CTSB`
  in celiac/psoriasis, but no clean V3 genetic anchor.
- Wave 3 genetics report found no clean cross-autoimmune single-gene anchor
  for `CTSS`.

Perturbation / drug-response evidence:

- `CTSS` inhibition has direct autoimmune prior art, including Sjogren-focused
  work.
  Source: https://pubmed.ncbi.nlm.nih.gov/?term=cathepsin+S+inhibitor+Sjogren+syndrome+RO5459072
- Local ChEMBL extraction shows dense chemical matter:
  `CTSS` human ChEMBL2954, 1000 returned records, best 0.1 nM, median 188 nM;
  `CTSL`, `CTSB`, and `CTSD` also have large inhibitor literature
  (`results_v3/druggability/chembl_target_activity_summary.tsv`).

Druggability:

- High for cathepsins as enzymes.
- Selectivity, lysosomal toxicity, antigen-presentation breadth, and repair
  inhibition are key blockers.

Prior-art blockers:

- `CTSS` is already a known autoimmune intervention lane and was previously
  blocked/demoted as insufficiently novel.
- Broad cathepsin inhibition risks suppressing necessary debris clearance.

Go/no-go:

**Hold / no-go.** Use cathepsins as lysosomal state comparators. Reconsider only
if a selective cathepsin-node residual signal survives after controlling for
lysosomal/APC load and repair markers.

### `SPP1` / `CD44` / Integrins

Mechanism and intervention point:

Osteopontin (`SPP1`) binds CD44 and multiple integrins, supporting macrophage
retention, migration, survival, and tissue remodeling. Intervention is feasible
with antibodies, aptamers, CD44 blockers, or integrin pathway modulation.

MS relevance:

- Local `CD44` has MS signal: `GSE111972` MS white-matter delta 1.345,
  Hedges g 0.954, p=0.0332; `GSE301908` MIMS2-like effect 1.869, p=0.00592.
- Local `SPP1` does not have strong MS single-gene support: sorted MS microglia
  null and MIMS2/proteomics weak/non-significant.
- Osteopontin has extensive MS/EAE literature.
  Source: https://pubmed.ncbi.nlm.nih.gov/?term=osteopontin+SPP1+multiple+sclerosis+experimental+autoimmune+encephalomyelitis

Cross-autoimmune breadth:

- Local bulk/existing evidence for `SPP1` is broad: RA macrophages, psoriasis,
  UC, Crohn, lupus nephritis trend, Sjogren trend.
- Direct h5ad evidence is narrower and inconsistent: T1D acinar/beta trends,
  Sjogren APC negative, weak MS.
- `CD44` has local trend-or-better support in Crohn, Hashimoto thyroiditis, MS,
  and UC.

Genetics / coloc / MR:

- No local V3-grade genetics/coloc/MR support found.

Perturbation / drug-response evidence:

- Extensive EAE and autoimmune literature exists for osteopontin and CD44.
- Integrin blockade is already therapeutic in MS/IBD; natalizumab is the
  obvious prior-art boundary for leukocyte trafficking in MS.
  Source: https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/125104s979lbl.pdf

Druggability:

- High, but broad target biology creates safety and differentiation problems.

Prior-art blockers:

- Very crowded `SPP1`/osteopontin and integrin space.
- `SPP1` can mark macrophage subsets rather than drive a unique lipid-lysosomal
  node.
- Integrin/CD44 targeting risks broad trafficking and repair liabilities.

Go/no-go:

**No-go as a novel successor.** Keep `SPP1`/`CD44` as tissue-injury and
macrophage-retention comparators.

### TAM / TREM2 / TYROBP Module

Mechanism and intervention point:

`AXL`, `MERTK`, `TYRO3`, `TREM2`, and `TYROBP` converge on phagocytosis,
efferocytosis, apoptotic/debris clearance, and lipid-loaded microglial repair.
The more plausible intervention direction is agonism or repair-preserving
activation, not inhibition.

MS relevance:

- Local `TREM2` and `MERTK` single-gene evidence is weak in the V3 direct
  h5ad and sorted MS tables.
- The broader DAM/MIMS2/foamy program is strongly represented through
  `GPNMB`, `APOE`, `CTSD`, and `LGALS3`, but that does not prove
  `TREM2`/TAM as the intervention node.
- External MS/efferocytosis literature supports relevance of MerTK-mediated
  myelin phagocytosis.
  Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC5777663/

Cross-autoimmune breadth:

- Local `MERTK`: RA and psoriasis negative, UC and lupus nephritis positive in
  older/bulk tables, Sjogren weak; direct h5ad includes UC epithelial and
  Sjogren APC negatives.
- Local `TREM2`: psoriasis and lupus nephritis positive in some older/bulk
  rows; RA negative; direct h5ad weak.
- Local `TYROBP`: UC myeloid positive and Sjogren epithelial positive in the
  OSMR/complement extended pass, but not enough for a five-disease claim.

Genetics / coloc / MR:

- No local V3-grade genetic anchor found.
- `TREM2` genetics are much stronger in neurodegeneration than in
  cross-autoimmune disease; do not import that as autoimmune genetics.

Perturbation / drug-response evidence:

- TREM2 agonist antibody programs exist in neurodegeneration, but autoimmune
  translation is not established.
  Source: https://pubmed.ncbi.nlm.nih.gov/?term=TREM2+agonist+antibody+clinical+trial
- TAM inhibitors are common in oncology; TAM agonism or efferocytosis
  enhancement is less mature.

Druggability:

- Biologics possible for TREM2/TAM receptors; small-molecule TAM kinase
  inhibitors exist but likely point in the wrong direction for repair biology.

Prior-art blockers:

- Neurodegeneration/efferocytosis literature is crowded.
- Direction is difficult: inhibiting clearance receptors may worsen debris
  burden, while agonism could have macrophage survival/tolerance liabilities.

Go/no-go:

**Hold.** Test pathway activation signatures only if `LTA4H` and `LGALS3` fail.
Do not prioritize receptor blockade.

### `LRP1` / `CALR`

Mechanism and intervention point:

`CALR` can act as an "eat-me" / stress signal and `LRP1`/CD91 participates in
clearance and antigen handling. The axis is relevant to efferocytosis and
DAMP handling, but direct systemic targeting is too broad.

MS relevance:

- Local `LRP1`: foamy proteomics effect 0.149, p=0.0160; MIMS2-like weak.
- Local OpenTargets candidate table had an MS `LRP1` affected-pathway signal,
  but not a clean genetic signal.
- Local `CALR`: not MS-anchored in the foamy/MIMS2 local tables, but strong
  Crohn/UC/psoriasis/T1D tissue-compartment signal in the OSMR/complement
  extended pass.

Cross-autoimmune breadth:

- `CALR` local signal is broad across Crohn, UC, psoriasis, and T1D, but mostly
  epithelial/stromal/barrier, not a myeloid intervention signal.
- `LRP1` is directionally mixed: Crohn/UC stromal negative, some MS/protein
  and pathway support.
- Literature plausibility exists for apoptotic-cell clearance and autoimmunity,
  but local data do not support direct target promotion.
  Source: https://pubmed.ncbi.nlm.nih.gov/?term=calreticulin+LRP1+efferocytosis+autoimmunity

Genetics / coloc / MR:

- No local coloc/MR support found.
- `LRP1` OpenTargets row is affected-pathway/literature-like, not genetics.

Perturbation / drug-response evidence:

- No local drug-response or named-gene perturbation support found.

Druggability:

- Poor as direct systemic targets. Both proteins participate in many
  housekeeping/stress-clearance processes.

Prior-art blockers:

- High pleiotropy and safety risk.
- Likely better as a repair/efferocytosis covariate than an intervention node.

Go/no-go:

**No-go as direct target.** Use as safety and repair-control axis.

### `PLA2G7`, `TBXAS1`, `MGLL/MAGL`, and Related Oxylipin Enzymes

Mechanism and intervention point:

These enzymes connect lipid mediator metabolism to foamy microglia and
inflammatory myeloid biology. The intervention point is enzyme inhibition, but
local prior work has already blocked the obvious claims.

MS relevance:

- `PLA2G7`: local foamy lesion activity elevated, but LPC product coupling
  failed (`CANDIDATE_REGISTER.md`; `results/pla2g7_lpc_coupling.tsv`).
- `TBXAS1`: foamy lesion protein and thromboxane coupling were strong, but
  independent source localization was inconsistent and the direct prior-art
  boundary is severe.
- `MGLL/MAGL`: local ABPP recovers `MGLL` as a positive benchmark, and the
  external MS foamy-microglia paper directly nominates MAGL inhibition.
  Local `GSE301908` MIMS2-like single-gene `MGLL` is weak/negative
  (`results/egln1_gse301908_paired_statistics.tsv`), and broad V3 h5ad has
  weak/negative peripheral breadth.
  Source: https://www.nature.com/articles/s41593-026-02302-3

Cross-autoimmune breadth:

- `PLA2G7` and `TBXAS1` do not have enough local cross-autoimmune breadth after
  the product-coupling and independent-localization failures.
- `MGLL/MAGL` is not a successor claim in this workspace because it is already
  an explicit benchmark/exclusion.

Genetics / coloc / MR:

- No local V3-grade genetics/coloc/MR support for these as successor nodes.

Perturbation / drug-response evidence:

- MAGL inhibition has direct MS-model support in the external foamy-microglia
  source, but that makes it prior art for this project rather than a new claim.
- `TBXAS1` prior-art blocker: patent `WO2004028339A2` includes thromboxane
  synthase among increased MS CNS gene products.
  Source: https://patents.google.com/patent/WO2004028339A2/en

Druggability:

- Enzyme tractability is generally good, but novelty and specificity fail for
  the obvious members.

Prior-art blockers:

- Direct MAGL/MS prior art and progressive-MS clinical translation boundary in
  the workspace.
- Direct `TBXAS1` MS patent boundary.
- `PLA2G7` local biochemical coupling failure.

Go/no-go:

**No-go as successor claims.** Keep `MGLL/MAGL` as positive control and
exclusion benchmark; use `TBXAS1`/`PLA2G7` only as oxylipin comparators.

## 3. Explicit Go / No-Go Summary

| Candidate | Go/no-go | Reason |
|---|---|---|
| `LGALS3` | **Go for next computational test** | Best remaining non-demoted handoff: MS foamy/MIMS2 evidence and tractable inhibitors, but cross-disease local breadth is weak and repair-risk is serious. |
| `GPNMB` | **No-go as direct target** | Strong MS state marker, mixed autoimmune direction, wrong default intervention modality. |
| Cathepsins | **Hold / no-go** | Druggable and biologically relevant, but crowded, broad lysosomal/APC confounding, and repair liability. |
| `SPP1`/`CD44`/integrins | **No-go** | Broad injury biology but prior-arted and not cleanly lipid-lysosomal; `SPP1` weak in local MS single-gene data. |
| TAM/TREM2/TYROBP | **Hold** | Repair/efferocytosis biology is real, but local signal and intervention direction are not crisp. |
| `LRP1`/`CALR` | **No-go as direct target** | Clearance/DAMP covariate, too broad and not locally myeloid-central. |
| `LTA4H` / LTB4 | **No-go after update** | Expression screen was attractive, but 22:34 UTC orchestrator integration demoted it: Geneformer deletion support is zero and inhibitor prior art is blocking. |
| `PLA2G7`/`TBXAS1`/`MGLL` | **No-go** | Local biochemical/prior-art blocks; `MGLL` is a benchmark/exclusion, not a successor claim. |

Best next candidate for orchestrator:

**`LGALS3`**.

Recommended computational test:

1. Build two non-identical galectin-3 tests: `LGALS3` single-gene donor-level
   contrasts, and a galectin-3 lysosomal/phagocyte module using `LGALS3`,
   `GPNMB`, `CTSD`, `CTSL`, `CTSB`, `LAMP1`, `LAMP2`, `APOE`, `TREM2`,
   `TYROBP`, `MERTK`, and `LRP1`.
2. Re-score existing local h5ad disease/compartment pseudobulks and MS
   microglia datasets with donor-level tests.
3. Residualize against generic myeloid abundance, IFN/APC, lysosomal/APC,
   OSM/C1q, tissue-injury, and lipid-loader programs so `LGALS3` is not just
   a `GPNMB`/cathepsin state surrogate.
4. Check whether `LGALS3` is positive in MS plus at least five autoimmune
   diseases; if not, keep it as MS/foamy-state biology only.
5. Query perturbation signatures for galectin-3 inhibition/knockdown and
   require predicted reversal of harmful inflammatory myeloid state without
   suppressing repair/debris-clearance modules (`GPNMB`, `TREM2`, `MERTK`,
   `LRP1`, `CTSD`, `CTSL` controls).
6. Include `LTA4H`, `MGLL`, `TBXAS1`, `PLA2G7`, `CTSS`, and `SPP1/CD44` as
   demoted/prior-art comparators, not alternative promotions.
7. Falsify immediately if the signal is just generic macrophage abundance,
   lysosomal load, fibrosis/tissue injury, or a marker of foamy microglia with
   no repair-preserving intervention direction.

## 4. Verified Sources And To-Verify Items

Local evidence sources used:

- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_ms_positive_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/existing_evidence_candidate_matrix.tsv`
- `results_v3/cross_disease_gene_summary.tsv`
- `results_v3/gse111972_target_contrasts.tsv`
- `results_v3/osmr_complement_axes/osmr_complement_gene_comparisons.tsv`
- `results/mims2_proteome_convergent_targets.tsv`
- `results/foamy_screen_abpp.tsv`
- `results/foamy_screen_proteomics.tsv`
- `results/pla2g7_lpc_coupling.tsv`
- `results/tbxas1_thromboxane_coupling.tsv`
- `results_v3/druggability/chembl_target_activity_summary.tsv`
- `subagents_v3/wave3_genetics_kierkegaard_report.md`
- `subagents_v3/wave4_residual_cd74_scout_report.md`
- `subagents_v3/wave5_osmr_scout_report.md`
- `subagents_v3/wave5_complement_scout_report.md`
- `LAB_NOTEBOOK_V3.md`
- `CANDIDATE_REGISTER.md`
- `REFRAME.md`
- `THERAPEUTIC_PLAN.md`

External sources checked:

- Foamy microglia / oxylipins / MAGL benchmark in MS:
  https://www.nature.com/articles/s41593-026-02302-3
- FDA natalizumab label as integrin prior-art boundary:
  https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/125104s979lbl.pdf
- `TBXAS1` MS patent prior-art boundary:
  https://patents.google.com/patent/WO2004028339A2/en
- MerTK/myelin phagocytosis in MS macrophages:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5777663/
- PubMed query links used for literature verification:
  https://pubmed.ncbi.nlm.nih.gov/?term=leukotriene+B4+BLT1+experimental+autoimmune+encephalomyelitis
  https://pubmed.ncbi.nlm.nih.gov/?term=leukotriene+B4+rheumatoid+arthritis+LTA4H
  https://pubmed.ncbi.nlm.nih.gov/?term=leukotriene+B4+lupus+nephritis
  https://pubmed.ncbi.nlm.nih.gov/?term=leukotriene+B4+psoriasis
  https://pubmed.ncbi.nlm.nih.gov/?term=LTA4H+Crohn+disease+genetic+association
  https://pubmed.ncbi.nlm.nih.gov/?term=acebilustat+LTA4H+inhibitor
  https://clinicaltrials.gov/search?term=acebilustat
  https://pubmed.ncbi.nlm.nih.gov/?term=galectin-3+multiple+sclerosis+experimental+autoimmune+encephalomyelitis
  https://pubmed.ncbi.nlm.nih.gov/?term=galectin-3+remyelination+microglia
  https://pubmed.ncbi.nlm.nih.gov/?term=galectin-3+autoimmune+disease+macrophage
  https://pubmed.ncbi.nlm.nih.gov/?term=belapectin+galectin-3+inhibitor
  https://pubmed.ncbi.nlm.nih.gov/?term=GB0139+TD139+galectin-3+inhibitor
  https://clinicaltrials.gov/search?term=galectin-3%20inhibitor
  https://pubmed.ncbi.nlm.nih.gov/?term=glembatumumab+vedotin+GPNMB
  https://clinicaltrials.gov/search?term=glembatumumab%20vedotin
  https://pubmed.ncbi.nlm.nih.gov/?term=cathepsin+S+inhibitor+Sjogren+syndrome+RO5459072
  https://pubmed.ncbi.nlm.nih.gov/?term=osteopontin+SPP1+multiple+sclerosis+experimental+autoimmune+encephalomyelitis
  https://pubmed.ncbi.nlm.nih.gov/?term=TREM2+agonist+antibody+clinical+trial
  https://pubmed.ncbi.nlm.nih.gov/?term=calreticulin+LRP1+efferocytosis+autoimmunity
- GWAS Catalog gene page checked for `LTA4H`:
  https://www.ebi.ac.uk/gwas/genes/LTA4H

To-verify / uncertain:

- Exact disease-by-disease `LGALS3` genetics/coloc/MR remains to verify.
  Current evidence is not V3-grade genetics.
- `LTA4H` should remain demoted unless a new test overcomes the zero-support
  Geneformer result and the inhibitor/prior-art boundary.
- Literature-level leukotriene breadth across psoriasis, lupus nephritis, RA,
  T1D, and IBD is pathway plausibility, not validated `LTA4H` single-gene
  causality.
- Galectin-3 intervention direction must be resolved experimentally because
  both inflammatory and repair/remyelination roles are reported.
