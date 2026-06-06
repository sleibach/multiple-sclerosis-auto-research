# Wave62-W Hostile Genetics-First Review

Status: completed.

Date: 2026-05-27.

## Verdict

Recommendation: **do not promote any V3 therapeutic claim from current Open
Targets target-resolution outputs. Continue only as a tightly bounded
falsification and triage branch.**

The current genetics-first pivot is useful for preventing expression-only
overclaiming, but it has its own failure mode: an API returns a target-disease
genetic score, a plausible gene name, and a colocalisation or L2G row, then the
analysis silently upgrades that into causal proof, therapeutic direction, and
module relevance. That upgrade is not valid.

For V3, Open Targets credible sets, L2G predictions, and colocalisation rows are
allowed to nominate a candidate only if they are connected to a complete chain:

1. disease-relevant GWAS signal;
2. high-quality credible set outside unresolved HLA/MHC ambiguity;
3. target resolution robust enough to beat neighbouring genes and pleiotropic
   explanations;
4. disease-cell or disease-tissue molecular trait colocalisation in the claimed
   direction;
5. intervention direction mapped to target function, not only variant beta sign;
6. local lipid-lysosomal/APC myeloid module evidence independent of the genetics
   lookup;
7. tractable, correct-direction druggability;
8. prior-art clearance.

If any of those links is missing, the result is **target-prioritisation
evidence**, not a V3 therapeutic claim.

## Inputs Reviewed

Local files:

- `results_v3/wave55_external_genetics_druggability_sweep/REPORT.md`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_candidate_audit.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/opentargets_associated_targets_raw.tsv`
- `results_v3/wave34_genetics_expression_druggability_scan/wave34_genetics_expression_druggability_rank.tsv`
- `results_v3/wave14_target_level_genetics/opentargets_locus_summary.tsv`
- `tmp_v3/wave13_opentargets_gwas_credible_sets.tsv`
- `tmp_v3/wave11_opentargets_target_disease_scores.tsv`
- `subagents_v3/wave34a_genetics_first_target_rescue.md`
- `subagents_v3/wave58o_hostile_review_cxcr2_il7r.md`
- `subagents_v3/wave61u_hostile_review_perturbation_first.md`

External documentation checked on 2026-05-27:

- Open Targets Platform: credible sets, target-disease evidence, fine-mapping,
  colocalisation, L2G, study metadata, GraphQL API, and release notes.

## Current Failure Mode

The local record already shows the problem. Wave55 explicitly marks
`coloc_or_mr_grade_target_resolution` as failed because paired disease/eQTL/pQTL
summary-statistic analysis was not run. The top genetics-sweep candidates still
fail strict MS local anchors, real perturbation support, druggability, or module
relevance. Several top rows have `in_lipid_lysosomal_myeloid_neighborhood =
False`. Wave14 calls the Open Targets locus summaries "locus-level triage only;
not target-level coloc/MR."

That is the correct hostile read. The branch becomes unsafe only if those
warnings are ignored and the associated-target output is treated as if it
answered the causal, directional, cell-state, and therapeutic questions.

## Evidence Hierarchy

### Allowed Uses

**Open Targets target-disease genetic association score:** triage only. It says a
credible set has been linked to a protein-coding gene with L2G above the
Platform inclusion threshold. It does not prove the gene is causal, directionally
therapeutic, or active in the claimed disease cell.

**Credible set row:** admissible as locus evidence only after the underlying
study, ancestry, fine-mapping confidence, lead variant, PIP distribution, and
neighbouring genes are inspected.

**L2G prediction:** admissible as target-resolution evidence only if high,
margin-separated, stable across releases or independent datasets, and explained
by biological features more specific than distance or generic enhancer overlap.
The Platform displays predictions above 0.05; that threshold is far too low for
V3 promotion.

**Colocalisation row:** admissible as molecular mechanism evidence only if the
GWAS credible set and the molecular QTL credible set plausibly share one causal
variant, the QTL is in the relevant cell/tissue/context, and the effect allele
direction is manually harmonised.

### Disallowed Uses

- Do not use `overall_score` or target rank as genetics. It can be driven by
  clinical, literature, RNA expression, or other sources.
- Do not use "many autoimmune diseases have Open Targets evidence" as proof of a
  shared target mechanism. That often measures pleiotropy, HLA-dominated immune
  genetics, or prior-art density.
- Do not use L2G score alone as causality. L2G is a release-dependent machine
  learning prioritisation, not an experiment.
- Do not use any colocalisation row as therapeutic direction without allele
  harmonisation and trait coding.
- Do not use blood, LCL, whole-tissue, plasma, or unrelated QTL colocalisation to
  claim lipid-lysosomal/APC myeloid control unless there is an explicit bridge.

## Minimum Bar For V3 Use

### 1. Disease And Study Identity

Every promoted genetics row must expose the exact study, trait, phenotype
mapping, sample size, case definition, ancestry composition, and publication.
The disease must match the V3 claim. Broad or meta-trait labels such as
"inflammatory bowel disease", "chronic inflammatory diseases", "rheumatoid
arthritis or type 1 diabetes", or MTAG/pleiotropy composites do not support a
specific disease claim without sensitivity analysis.

Go rule:

- MS claim requires an MS or lesion-relevant MS endophenotype anchor, not only
  psoriasis/IBD/T1D/SLE breadth.
- Pan-autoimmune claim requires consistent evidence in at least three
  independently ascertained diseases plus a defensible shared mechanism.
- Composite traits can be used only as discovery evidence, not as decisive
  V3 support.

No-go rule: if the only positive row is a composite, MTAG, PheCode, cross-disease
meta-analysis, or top-hit-mapped trait, classify it as hypothesis generation.

### 2. HLA/MHC Ambiguity

Autoimmune genetics is dominated by HLA/MHC. Open Targets excludes credible sets
whose lead variant falls in the MHC region, so absence of a displayed MHC
credible set is not evidence that HLA biology has been ruled out. Conversely,
GWAS Catalog mapped-gene rows in or near MHC genes are almost never
target-resolved therapeutic evidence.

Special rule:

- Any locus within chr6 MHC, adjacent long-range LD, antigen-presentation
  machinery, HLA-processing genes, TAP/PSMB/ERAP-like rows, or HLA-tagged disease
  signal must be presumed ambiguous until HLA-conditioned analysis proves an
  independent non-HLA signal.
- HLA/MHC evidence can support "immune genetics is relevant"; it cannot promote
  a specific target unless fine-mapping, conditional analysis, and functional
  data resolve the target away from classical HLA alleles.

No-go rule: if the locus explanation is compatible with classical HLA allele
effects, antigen presentation haplotypes, or population-specific HLA LD, do not
use it for V3 target promotion.

### 3. Credible Set Quality

A 95% credible set is probabilistic, not deterministic. The minimum promotion
bar is:

- fine-mapping confidence recorded and high;
- in-sample LD preferred; out-of-sample LD downgraded;
- SuSiE/FINEMAP-like credible set preferred over PICS/top-hit-derived rows;
- lead variant and all high-PIP variants visible;
- credible set not a single proxy because the lead variant was missing from the
  LD reference;
- total PIP valid and not spread across dozens of plausible variants;
- at least one high-PIP variant with interpretable regulatory, coding, splice,
  or molQTL support;
- independent replication or a second credible set for the same target-disease
  mechanism.

No-go rule: broad target-disease evidence without the underlying credible set,
PIP distribution, and fine-mapping confidence is not acceptable. This is exactly
the weakness in several current local Open Targets summaries.

### 4. Winner's Curse And Fine-Mapping Limitations

The highest scoring variant, the largest GWAS beta, and the top L2G gene are
not immune to winner's curse, ascertainment, imputation, and LD reference bias.
Fine-mapping can fail when there are multiple causal variants, weak sample size,
poor imputation, mismatched ancestry, local structural variation, or an
unmodelled HLA-like haplotype.

Minimum safeguards:

- report whether the association comes from discovery-only or replicated GWAS;
- avoid using unconditioned p-values as independent support when the locus has
  multiple signals;
- require conditional or multi-signal fine-mapping in crowded immune loci;
- rerun or cross-check with an independent fine-mapping/colocalisation method
  before promotion;
- do not score each disease, study, or variant in the same locus as an
  independent replicate.

No-go rule: if the apparent target depends on the top SNP from a broad,
multi-gene immune locus and there is no conditional independence, demote.

### 5. Ancestry

Fine-mapping is LD-dependent. An L2G/credible-set result generated with
out-of-sample LD or a major-ancestry proxy does not automatically transfer to a
different disease population. European/NFE-rich autoimmune GWAS signals are not
pan-human evidence.

Minimum bar:

- report ancestry composition and LD reference ancestry for each promoted row;
- require effect direction and target resolution to hold in the ancestry groups
  relevant to the proposed patient population, or explicitly narrow the claim;
- downgrade multi-ancestry studies if fine-mapping uses a single major ancestry
  or if sample-size imbalance makes one ancestry dominate;
- require trans-ancestry replication for broad claims when available.

No-go rule: no broad V3 claim from a single-ancestry target-resolution result
unless the indication and patient framing are explicitly restricted.

### 6. L2G Target Resolution

The V3 bar must be much higher than "L2G > 0.05." That threshold only determines
whether a GWAS association can enter the Platform evidence set.

Minimum V3 L2G standard:

- top target L2G preferably >=0.50, and never promoted below 0.30 without strong
  orthogonal evidence;
- margin over the second-best nearby protein-coding gene >=0.20 or at least
  2-fold score ratio;
- SHAP/feature explanation not dominated by distance alone;
- coloc, functional-impact, enhancer-gene, or coding/splice evidence points to
  the same gene;
- same target nominated in independent credible sets or diseases with compatible
  biology;
- neighbouring known immune genes manually inspected.

No-go rule: if L2G is low, distance-driven, unstable by release, or tied among
neighbouring immune genes, it is a prioritisation hint only.

### 7. Colocalisation And QTL Tissue Match

Colocalisation is the main chance for target resolution to become mechanistic.
It also has the highest overclaim risk. Open Targets colocalisation is based on
overlapping credible sets, not a full-locus causal proof. A shared variant
hypothesis is only useful if the molecular trait is relevant to the disease cell.

Minimum V3 colocalisation bar:

- GWAS and molecular QTL credible sets overlap on high-PIP variants;
- COLOC-PIP/H4 or eCAVIAR/CLPP supports one shared signal rather than two
  independent signals;
- H3 or independent-signal evidence is low;
- alleles are harmonised and trait coding is documented;
- QTL is cis unless a trans mechanism is independently proven;
- QTL biosample is relevant to the claim: monocyte, macrophage, dendritic cell,
  microglia-like cell, lesion myeloid, inflamed gut/skin APC, or a stimulated
  context matching IFN/TNF/myelin/lipid stress;
- bulk tissue or blood QTL is not used as a substitute for disease APC biology.

No-go rule: a GTEx whole-blood, LCL, whole-colon, whole-skin, or plasma-only
colocalisation row cannot bridge to the lipid-lysosomal/APC myeloid module by
itself.

### 8. Beta Sign And Direction

Neither L2G nor target-disease genetic association score gives therapeutic
direction. Even colocalisation direction is not enough unless the alleles,
units, trait coding, and molecular readout are aligned.

Minimum direction bar:

- define the disease-increasing allele and effect allele explicitly;
- confirm whether GWAS beta means risk, protection, case status, quantitative
  trait increase, or inverse-coded phenotype;
- confirm whether QTL beta means increased expression, splicing isoform usage,
  protein abundance, or assay signal;
- decide whether the proposed intervention should inhibit, agonise, restore,
  degrade, replace, or modulate the target;
- check whether the genetic mechanism is gain-of-function, loss-of-function,
  altered splicing, altered cell composition, or altered ligand/protein level;
- require functional perturbation to match the predicted direction.

No-go rule: do not infer "inhibit target" from a risk association unless the
risk allele increases target activity or expression in the relevant disease cell
and inhibition phenocopies the protective allele without safety collapse.

### 9. Trans-QTL And pQTL Caveats

Trans-QTL and plasma pQTL evidence is especially vulnerable to biomarker
overclaiming.

Rules:

- cis-eQTL, cis-sQTL, cis-pQTL near the target gene can support target
  resolution if tissue/cell context and direction are right.
- trans-QTL is mechanistic clue only. It may reflect an upstream immune pathway,
  cell composition, inflammation, clearance, assay cross-reactivity, or a shared
  haplotype.
- plasma pQTL for cytokines, receptors, complement, or enzymes can represent
  secretion, shedding, binding proteins, degradation, glycosylation, renal or
  hepatic clearance, or immune-cell abundance rather than target activity.
- pQTL assay validity must be checked for protein isoform, antibody/aptamer
  specificity, cis/trans status, and disease-state relevance.

No-go rule: trans-pQTL or plasma-pQTL colocalisation alone cannot establish a
drug target. It can rank a wet-lab assay.

### 10. Pleiotropy

Pleiotropy is not automatically good. The current genetics-first rows are rich
in classic immune genes: `IL7R`, `IL12A/B`, `STAT4`, `CD40`, `BACH2`, `TAGAP`,
`TNFAIP3`, `PTPN2`, `TYK2`, `SH2B3`, and related pathways. Broad autoimmune
association can mean a target is fundamental, but it can also mean the target is
generic, unsafe, old, and mechanistically unrelated to the V3 module.

Minimum pleiotropy review:

- run PheWAS for protective and risk directions separately;
- flag opposite-effect diseases;
- check infection, malignancy, neurodevelopmental, lipid/metabolic, and
  hematopoietic liabilities;
- separate adaptive immune, barrier, stromal, neutrophil, and myeloid/APC
  mechanisms;
- avoid counting correlated diseases or shared meta-analyses as independent
  support.

No-go rule: if the target's strongest biology is generic immune activation,
lymphocyte survival, cytokine blockade, complement, HLA, or broad transcriptional
control, do not claim a lipid-lysosomal/APC myeloid therapeutic mechanism without
direct module perturbation.

### 11. Prior-Art Leakage

Open Targets is built for target identification and therapeutic hypothesis
generation. That means clinical, literature, and known-drug information can be
near the same surface as genetic evidence. This creates prior-art leakage:
targets rise in rank because they are already studied or clinically exploited,
then the branch calls them novel because the route began with genetics.

Minimum prior-art gate:

- separate genetic score from overall score, clinical score, literature score,
  and known-drug evidence;
- perform external Europe PMC, PubMed, ClinicalTrials.gov, ChEMBL, drug label,
  company pipeline, and Google Patents checks before promotion;
- treat high clinical or literature scores as novelty risk, not as support for a
  new V3 claim;
- identify whether the proposed direction, modality, indication, patient
  subgroup, and biomarker are already disclosed.

No-go rule: if the claim is "block/activate known autoimmune target X" and X has
approved, clinical, patent, or direct preclinical autoimmune prior art, it is a
comparator, not a V3 finding.

### 12. Druggability And Directional Modality

Genetic causality does not create a drug. Many genetically strong immune genes
are intracellular scaffolds, transcription factors, adaptors, phosphatases,
HLA-processing proteins, or loss-of-function restoration targets. The V3 claim
needs a feasible intervention in the right direction.

Minimum druggability bar:

- modality exists or is credible: antibody, ligand trap, small molecule,
  degrader, RNA, gene editing, enzyme replacement, or targeted delivery;
- modality can reach the relevant tissue and cell state;
- intervention direction matches genetic direction;
- safety window preserves host defense, repair, and debris clearance;
- target is not essential or broadly toxic in the required cell context;
- selectivity over close homologs and pathway paralogs is plausible;
- biomarker and pharmacodynamic readout exist.

No-go rule: "genetically strong but not druggable in the needed direction" stays
parked, even if the target is broad across autoimmune diseases.

## Can Target Resolution Bridge To The Lipid-Lysosomal/APC Myeloid Module?

Not by itself.

Credible sets, L2G, and colocalisation can say "this inherited disease-risk
locus may act through this gene." They do not say that the gene controls the
late disease tissue module, that the module is causal, that the therapeutic
direction is known, or that an intervention will selectively repair the module
without suppressing host defense.

To bridge into the V3 lipid-lysosomal/APC myeloid claim, the candidate must pass
all of the following:

1. **Cell-state presence:** target mRNA/protein is present in disease-associated
   myeloid/APC cells, not explained by lymphocyte, neutrophil, stromal,
   epithelial, doublet, or abundance artifacts.
2. **Genetic-to-cell bridge:** risk allele, eQTL/sQTL/pQTL, or genotype-stratified
   data changes the target or module in relevant APC/myeloid cells.
3. **Module specificity:** target perturbation changes lipid handling,
   lysosomal stress, antigen-presentation burden, and APC state more strongly
   than generic IFN, TNF/NF-kB, JAK/STAT, stress, viability, or cell-abundance
   programs.
4. **Functional guardrails:** perturbation preserves or improves myelin-debris
   clearance, efferocytosis, lysosomal function, cholesterol efflux, repair
   macrophage/microglial programs, and antimicrobial/antiviral competence.
5. **Disease replication:** at least MS plus two other disease-relevant
   contexts, or explicitly narrow the claim to the disease where the evidence
   exists.
6. **Orthogonal validation:** genetics, local disease expression, perturbation,
   and prior-art/druggability all point to the same target and direction.

No-go rule: target-resolution evidence cannot be used as a narrative bridge
after expression and perturbation branches failed. It must add an independent,
directional, disease-cell-specific mechanism.

## Gate Table

| Risk | Minimum V3 gate | Kill condition |
| --- | --- | --- |
| HLA/MHC ambiguity | HLA-conditioned non-MHC signal, independent target evidence | classical HLA or MHC LD can explain the association |
| Pleiotropy | direction-consistent PheWAS and disease-specific mechanism | broad generic immune target with opposite effects or unrelated biology |
| Ancestry | ancestry-matched LD and replication or claim restriction | single ancestry used for broad patient claim |
| QTL tissue mismatch | disease-cell cis-QTL or stimulated myeloid/APC QTL | blood/LCL/plasma/whole-tissue QTL only |
| Beta sign ambiguity | manual allele harmonisation and trait coding | intervention direction inferred from score alone |
| Winner's curse/fine-mapping | high-confidence credible set plus replication/conditioning | top SNP or low-confidence PICS/top-hit proxy only |
| Trans-QTL/pQTL caveat | validated cis-pQTL or orthogonal protein mechanism | trans/plasma biomarker treated as target causality |
| Prior-art leakage | source-separated novelty review | known clinical/patent autoimmune mechanism |
| Druggability | correct-direction modality with tissue exposure | target requires restoration, broad transcriptional control, or unsafe immune suppression |
| Module bridge | genotype or perturbation changes lipid-lysosomal/APC myeloid state | genetics points to adaptive, stromal, neutrophil, or generic cytokine biology only |

## Continue Criteria

The genetics-first branch may continue only as a **candidate filter and
falsification pass**. It should not be the primary rescue route for V3 until the
pipeline can emit per-candidate evidence packets with:

- exact credible set IDs, study IDs, disease labels, ancestry, fine-mapping
  method, confidence, lead variant, PIP distribution, and neighbouring genes;
- L2G score, rank, margin, release version, and feature contribution summary;
- colocalisation details for disease GWAS versus cis-eQTL/sQTL/pQTL in relevant
  cell/tissue contexts, including H4/CLPP, H3 or independent-signal flags, and
  allele direction;
- HLA/MHC and ancestry flags;
- PheWAS/opposite-effect review;
- prior-art and druggability review separated from genetics;
- local module bridge: disease-cell expression, residual support, strict MS
  anchor, perturbation direction, and functional guardrails.

Promotion rule: a candidate can enter V3 only if it passes **all** of these
strict criteria:

1. MS genetic anchor plus at least two additional independent autoimmune disease
   anchors, or a deliberately narrower disease claim.
2. Non-MHC, high-confidence credible set with robust target resolution.
3. L2G top gene with strong score margin and orthogonal coloc or coding/splice
   support.
4. Relevant cis-QTL/protein/splicing direction in myeloid/APC or disease tissue,
   not only blood/plasma.
5. Clear intervention direction with a feasible modality.
6. Direct perturbation evidence in human disease-relevant myeloid/APC cells that
   shifts the lipid-lysosomal/APC module while preserving repair and clearance.
7. Prior-art space not already occupied by known autoimmune programs.

If those criteria cannot be met, stop calling the branch genetics-first target
rescue. Call it what it is: **Open Targets triage for wet-lab hypotheses and
comparators**.

## Final Recommendation

Continue for one narrow pass only if the next work product extracts the full
credible-set/L2G/colocalisation packets and applies the kill rules above. Do not
use associated-target scores, L2G threshold hits, or unmatched colocalisation
rows to patch the failed expression and perturbation branches.

Current V3 status: **NO_GO for therapeutic promotion from Open Targets genetics
outputs alone. CONDITIONAL_CONTINUE for target-resolution triage under strict
causal, directional, module, prior-art, and druggability gates.**

