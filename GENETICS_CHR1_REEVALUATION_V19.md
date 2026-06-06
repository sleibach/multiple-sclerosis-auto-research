# GENETICS_CHR1_REEVALUATION_V19

Date: 2026-06-06

## Scope

V19 re-evaluated the MS-UC chr1 shared locus under the domain-reviewer's
objection that prior druggability calls were too class-precedent-driven:
`GPR25` was favored partly because GPCRs are familiar drug targets, while
`KIF21B` was down-weighted partly because kinesins are difficult. V19 therefore
tested the data-favored `KIF21B` candidate directly and separated
first-principles target features from existing chemical precedent.

Reproducible entry point:

```bash
.venv/bin/python scripts/v19_chr1_reanalysis.py
```

Primary outputs:

- `analysis/v19_chr1_druggability/v18_checksum_verification.tsv`
- `analysis/v19_chr1_druggability/kif21b_qtd000021_aligned_to_ms_uc.tsv`
- `analysis/v19_chr1_druggability/kif21b_qtd_coloc_abf_summary.tsv`
- `analysis/v19_chr1_druggability/v19_chr1_reanalysis_summary.json`
- `analysis/v19_chr1_druggability/alphafold_domain_confidence.tsv`

## First-Action Checks

- OpenGWAS token: verified with `scripts/check_opengwas_access.py`.
- `/user`: HTTP 200.
- JWT valid until `2026-06-19 12:28 UTC`.
- POST `gwasinfo` and `tophits` for `ieu-b-18`: HTTP 200.
- No OpenGWAS GET-style calls were used.
- RAG query for `V19 KIF21B GPR25 first-principles druggability chr1 credible
  set eQTL colocalization V18` returned `knowledge/candidates/KIF21B.md`,
  `knowledge/candidates/GPR25.md`, `meta/NEXT_ACTIONS.md`, and
  `meta/DATA_ACQUISITION_PLAN_V18.md` as the top project-memory hits.

## V18 Input Verification

`scripts/v19_chr1_reanalysis.py` rechecked all V18-acquired source checksums.

- Files checked: `19`.
- All expected SHA-256 values matched: `true`.

V18 smoke-test result reproduced:

- Public target eQTL hits: `15`.
- Hits by gene: `KIF21B = 15`; `GPR25 = 0`; `CXCL17 = 0`.
- Hits by source: `OneK1K_top_eqtl = 14`; `DICE_significant_eqtl = 1`.
- Exact overlap with V17 shared credible-set positions: `0`.
- Minimum distance from a OneK1K/DICE top/significant hit to a V17 shared
  credible-set variant: `17,230 bp`.

Interpretation: public top/significant immune eQTL hits support `KIF21B`
context but do not by themselves prove the V17 shared causal variant acts
through `KIF21B`.

## Investigation 1: KIF21B

### Dense Immune-QTL Colocalization

V18 acquired a dense eQTL Catalogue extract:

- Source file:
  `data/raw/v18_source_triage/eqtl_catalogue/QTD000021_chr1_200000000_202000000_targets.tsv`.
- `KIF21B` rows in the extract: `8,416`.
- Rows intersecting the saved V14 MS/UC chr1 disease SNP set after allele
  alignment: `472`.

V19 ran `coloc.abf` using allele-aligned KIF21B QTD000021 betas against the
V14 disease sumstats:

| Comparison | SNPs | PP.H3 | PP.H4 |
|---|---:|---:|---:|
| MS vs QTD000021 KIF21B eQTL | 472 | 0.0658560991820944 | 0.874879034973956 |
| UC vs QTD000021 KIF21B eQTL | 472 | 0.0691528812741881 | 0.868660082128031 |

Caveats:

- This is single-causal-variant `coloc.abf`, not SuSiE-coloc.
- The eQTL Catalogue REST metadata layer remains unusable for this run:
  - `GET https://www.ebi.ac.uk/eqtl/api/studies/QTD000021` returned HTTP 404
    with body `{"message":"Study QTD000021 does not exist!"}`.
  - `GET https://www.ebi.ac.uk/eqtl/api/studies?size=100&study_accession=QTS000002`
    returned HTTP 500.
  - FTP listings confirm the files exist at
    `https://ftp.ebi.ac.uk/pub/databases/spot/eQTL/sumstats/QTS000002/QTD000021/`,
    including `QTD000021.all.tsv.gz` (`2.8G`), `.tbi` (`1.8M`),
    `QTD000021.cc.tsv.gz` (`1.0G`), and `QTD000021.permuted.tsv.gz` (`572K`).
  - Therefore the exact QTD000021 cell/tissue metadata remains to be verified
    before publication-grade use.
- `coloc` estimated quantitative-trait `sdY` from MAF and N; the run emitted
  that warning. This is acceptable for triage but not the final publication
  layer.

Interpretation: independent dense immune-QTL evidence supports `KIF21B` as a
real chr1 candidate. The support is strong enough to prevent dismissing
`KIF21B`, but below the V17 eQTLGen bounded SuSiE-coloc values for both
`GPR25` and `KIF21B`.

### Effect Direction

In the exact V17 shared credible-set SNPs that intersect QTD000021:

- Exact shared credible-set SNPs present in QTD000021: `11`.
- MS risk allele lowers KIF21B expression: `11 / 11`.
- UC risk allele lowers KIF21B expression: `11 / 11`.

Across all 472 intersecting SNPs:

- MS risk allele lowers KIF21B expression: `304 / 472`.
- UC risk allele lowers KIF21B expression: `386 / 472`.

Direction verdict: if `KIF21B` is the causal gene, the shared MS-UC risk
mechanism is lower `KIF21B` expression, and the therapeutic direction would be
restoration or increased function/expression, not inhibition.

### Cell-State and Mechanism

Evidence carried forward from V17/V18:

- V17 local MS CNS atlas `GSE301908_sn_all.rds` contained measurable `KIF21B`
  in lymphocytes, microglia, astrocytes, and neurons.
- V17 h5ad scans found `KIF21B` materially more detectable than `GPR25` across
  available immune/tissue atlases, including psoriasis T-cell subsets and IBD
  T cells.
- V18 DICE mean expression showed high `KIF21B` expression across immune
  subsets, with max mean TPM `180.946938037` in memory Treg.
- V18 OneK1K top eQTL hits for `KIF21B` appeared across monocyte, NK, CD8,
  plasma, DC, B, and CD4 subsets, but these top hits did not exactly match the
  V17 shared credible set.

Mechanistic interpretation: the available data favor a cytoskeletal/transport
or lymphocyte-state mechanism over a lesion-myeloid IFN/APC mechanism. The data
do not yet connect `KIF21B` to the V6/V7 mucosal IFN/APC treatment-response
architecture.

### Prior Art, Recalibrated

`KIF21B` is not a novel autoimmune locus; it has MS/IBD susceptibility prior
art in the project record. V19's possible contribution is narrower:

- MS-UC shared-locus causal-gene re-evaluation after multi-signal disease coloc.
- Independent dense immune-QTL support for `KIF21B`.
- Direction: disease risk appears to lower `KIF21B` expression at exact shared
  credible-set SNPs.

This is not an intervention claim.

## Investigation 2: GPR25

V19 did not find new V18 public immune-QTL support for `GPR25`.

Evidence still supporting `GPR25`:

- V17 full eQTLGen candidate-gene extraction: `GPR25` is strongest in the
  disease-shared credible-set block.
- V17 bounded disease-vs-eQTL SuSiE-coloc:
  - MS/eQTL max PP.H4 `0.969296`.
  - UC/eQTL max PP.H4 `0.981623`.
- V17/V16 direction: expression-increasing alleles are protective for both MS
  and UC.
- UniProt/IUPHAR support a CXCL17-GPR25 receptor axis with lymphocyte homing
  biology.

Evidence weakening `GPR25`:

- V18 OneK1K, DICE, and QTD000021 acquired public immune-QTL sources produced
  no `GPR25` target hit.
- V17 local MS CNS atlases did not contain measurable `GPR25`.
- V17 h5ad scans found `GPR25` absent or trace across available gut, blood,
  salivary, skin, and IBD myeloid atlases.
- ChEMBL has only `2` screening activity records for GPR25 and `0` mechanism
  records.

Verdict: `GPR25` remains a live causal candidate only because the eQTLGen
shared-block and bounded colocalization signals are strong. It is not currently
supported by the public genotype-linked immune-cell QTL sources acquired in
V18, nor by available scRNA expression data. It should no longer be treated as
the protected favorite.

## Investigation 3: First-Principles Druggability

### GPR25

Structural features:

- UniProt reviewed protein `O00155`, length `361`.
- Seven transmembrane helices annotated by UniProt:
  - TM1 `40-60`;
  - TM2 `76-96`;
  - TM3 `127-147`;
  - TM4 `156-176`;
  - TM5 `201-220`;
  - TM6 `243-263`;
  - TM7 `290-310`.
- AlphaFold model `AF-O00155-F1`, global metric value `82.44`.
- GPCRdb entry `gpr25_human`, accession `O00155`.
- V19 per-domain AlphaFold confidence:
  - all seven transmembrane helices have mean pLDDT `>= 90.899`;
  - TM1, TM2, and TM4 have 100% residues with pLDDT `>= 90`;
  - cytoplasmic tail `311-361` is low-confidence/flexible, mean pLDDT
    `55.069`.

First-principles tractability:

- The seven-transmembrane GPCR fold gives a plausible orthosteric/allosteric
  pocket architecture.
- The therapeutic direction inferred from genetics is higher expression or
  higher signaling, i.e. restoration/agonism.
- Agonism of a sparsely tooled receptor is harder than antagonism because it
  must stabilize productive signaling rather than just block a pocket.
- The endogenous ligand axis is not absent: UniProt annotates CXCL17 as the
  receptor ligand. However, chemical matter remains immature.

Prior-chemical-matter view:

- ChEMBL target activity records: `2`.
- ChEMBL mechanism records: `0`.
- ClinicalTrials.gov GPR25 studies in V17: `0`.

Druggability verdict:

- First-principles structural tractability is real.
- Intervention tractability is still limited because the required direction is
  agonism/restoration and existing tool chemistry is minimal.
- Earlier "GPR25 is druggable because GPCR" was over-credited. The correct V19
  status is "structurally plausible but chemically immature and causally
  unresolved."

### KIF21B

Structural features:

- UniProt reviewed protein `O75037`, length `1,637`.
- Kinesin motor domain: residues `8-370`.
- Binding-site annotation: residues `87-94`.
- Multiple coiled-coil regions:
  - `376-604`;
  - `631-824`;
  - `928-1016`.
- Large disordered regions, including `509-538`, `552-628`, `830-865`,
  `880-906`, and `1194-1251`.
- AlphaFold model `AF-O75037-F1`, global metric value `69.62`, consistent with
  a structured motor plus large flexible regions.
- V19 per-domain AlphaFold confidence:
  - kinesin motor domain `8-370`: mean pLDDT `83.95`, median `90.06`,
    `87.1%` residues pLDDT `>= 70`;
  - binding-site annotation `87-94`: mean pLDDT `90.71`, all residues pLDDT
    `>= 70`;
  - coiled-coil and disordered regions are more variable, explaining the lower
    full-length AlphaFold metric without invalidating the motor-domain
    tractability assessment.

First-principles tractability:

- The kinesin motor domain and binding-site annotation mean `KIF21B` is not
  "undruggable" by first principles.
- The ATPase/microtubule motor machinery is a real ligandable architecture in
  principle.
- The main first-principles obstacle is not the existence of a pocket; it is
  selectivity among kinesins, cell-state-specific functional modulation, and
  the required therapeutic direction.
- V19 direction analysis indicates disease risk lowers `KIF21B` expression.
  Therefore, a conventional inhibitor would be directionally wrong unless the
  disease mechanism is gain-of-toxic-function despite lower expression, which
  current data do not support.

Prior-chemical-matter view:

- ChEMBL target search for `KIF21B`: `0` targets.
- ChEMBL mechanism records for `KIF21B`: `0`.
- ClinicalTrials.gov studies for `KIF21B` in V17: `0`.
- Comparator precedent kept separate from KIF21B itself:
  - ChEMBL target search for `KIF11` returned `4` target records.
  - ChEMBL mechanism query for KIF11 target `CHEMBL4581` returned `4`
    inhibitor mechanisms, all with max phase `2`.
  - This supports the first-principles claim that kinesin motor domains can be
    engaged pharmacologically, but it does not solve KIF21B selectivity or the
    wrong-direction problem.

Modality fit:

- Inhibition: structurally plausible in the motor domain, but likely wrong
  direction for this locus.
- Degradation/ASO/siRNA: also likely wrong direction if low expression is risk.
- Expression restoration, CRISPRa-like upregulation, or functional rescue:
  directionally aligned but currently much less tractable as a systemic MS/UC
  therapy.
- Biomarker or mechanism target: more realistic near-term use than direct
  therapeutic target.

Druggability verdict:

- Earlier "KIF21B weakly druggable because kinesin" was too prior-art-driven.
- First-principles analysis upgrades it from "dismissed" to "structurally
  ligandable but directionally difficult."
- The honest conclusion is not that `KIF21B` is a good drug target; it is that
  it may be real causal biology whose most plausible therapeutic direction is
  currently hard.

## Integrated Verdict

The chr1 MS-UC locus is real shared biology, but it is not an
intervention-grade target yet.

Causal-gene balance after V19:

- `GPR25` remains strongest in eQTLGen shared-block evidence and V17 bounded
  eQTL SuSiE-coloc.
- `KIF21B` now has independent dense immune-QTL colocalization:
  - MS vs QTD000021 KIF21B eQTL PP.H4 `0.874879034973956`;
  - UC vs QTD000021 KIF21B eQTL PP.H4 `0.868660082128031`;
  - V17 bounded eQTL SuSiE-coloc also supports KIF21B with MS/eQTL PP.H4
    `0.956099` and UC/eQTL PP.H4 `0.963951`.
- V18 public immune QTL and expression sources favor `KIF21B` context.
- Available scRNA expression data favor `KIF21B` over `GPR25`.

Therapeutic-direction balance:

- If `GPR25` is causal, higher expression/signaling is protective, so the
  direction is agonism/restoration. That is structurally plausible but
  chemically immature.
- If `KIF21B` is causal, higher expression appears protective at exact shared
  credible-set SNPs, so the direction is restoration/up-function. That is
  biologically plausible but therapeutically hard because simple inhibition is
  likely wrong-direction.

V19 significance verdict:

- `KIF21B` can no longer be down-weighted on a class-precedent heuristic.
- `GPR25` can no longer be up-weighted on GPCR class precedent alone.
- The chr1 locus is currently a tractable genetics/mechanism lead, not a
  tractable intervention lead.

Single most informative next dataset/experiment:

- Genotype-stratified immune-cell or CSF single-cell/CITE-seq data for carriers
  of the exact chr1 shared credible-set haplotype, measuring both `GPR25`
  surface protein/transcript and `KIF21B` transcript/protein in T/NK/B-cell
  subsets. The decisive readout is whether the protective haplotype raises
  `GPR25`, `KIF21B`, or both in the same disease-relevant cell subset, followed
  by perturbation of the winning gene in migration/cytoskeletal assays.

## Hostile Critique

- The QTD000021 KIF21B coloc is not publication-grade because study metadata
  remains incompletely verified and `sdY` was estimated.
- `coloc.abf` is single-causal-variant and can overstate shared signal in a
  multi-signal locus. V17 bounded SuSiE-coloc partly mitigates this but used
  eQTLGen blood/reference LD, not cell-type QTL.
- Direction is robust at the exact shared credible-set SNPs in QTD000021, but
  expression restoration is a therapeutic modality gap for both candidates.
- Neither `GPR25` nor `KIF21B` currently has perturbation data showing movement
  of an MS-relevant cell state.
- Therefore no matrix upgrade to intervention-grade is justified in V19.
