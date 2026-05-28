# Wave 12 Broad Residual-Gate Genetics / Prior-Art Triage

Returned: 2026-05-27

Scope: triage the new broad residual-gate leaders from
`results_v3/broad_residual_gate/`, especially `ATOX1`, `SQLE`, `TPM4`,
`LDLRAD3`, `C1QTNF1`, `HIF1A`, `CBX3`, `CFB`, and `TIMP1`, plus top broad
candidate-panel rows that looked more druggable or biologically plausible.

Status: **triage only; no finding is claimed.**

## Files Read

- `ORCHESTRATION_LOG_V3.md`
- `LAB_NOTEBOOK_V3.md`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/broad_residual_gate/broad_residual_candidate_panel.tsv`

## Bottom Line

No new broad residual-gate leader satisfies the three required gates together:

1. cross-autoimmune target-level genetics;
2. plausible intervention modality; and
3. non-blocking prior art for a therapeutic claim.

The top residual rows are mostly residual expression/state correlates in
stromal, epithelial, myeloid, or keratinocyte compartments. The best actual
drug/modality rows (`CFB`, `HIF1A`, `IL15`, `JAK3`, `TIMP1`/MMP axis, `SQLE`)
are either heavily prior-arted, too broad/safety-limited, or lack
cross-autoimmune target genetics. The cleaner residual-rank rows (`ATOX1`,
`TPM4`, `LDLRAD3`, `C1QTNF1`, `CBX3`) do not currently have enough genetics or
intervention tractability to support a therapeutic target claim.

## Local Signal Interpretation

The residual-gate summary is ranked differently from the broad candidate panel.

- Residual-gate leaders: `ATOX1`, `SQLE`, `TPM4`, `LDLRAD3`, `C1QTNF1`,
  `HIF1A`, `CBX3`, `CFB`, `TIMP1`, `REG1A`, `COL4A1`, `RPL17`, `MPHOSPH6`,
  `PDPN`, `CXCL8`, `ACSL3`, `PDLIM7`, `PTPRE`, `IL7R`, `HLA-B`.
- Candidate-panel leaders by broad expression priority include `IFITM3`,
  `IFITM2`, `PSME2`, `EEF1E1`, `POMP`, `PSME1`, `NME1`, `TMEM167A`, `CARD16`,
  `IL15`, `NLRC5`, `JAK3`, `CBX3`, `TIMP1`, `CFB`, `PTPRE`, `MMP7`.

The residual-gate top rows are often driven by IBD stromal residuals against
complement/IFN/HLA/lysosomal modules, not by disease-causal target genetics.
This should be treated as a discovery-prioritization layer, not as target
validation.

## Database / Literature Checks

Primary database links checked or used as source anchors:

- Open Targets target pages: `ATOX1`
  <https://platform.opentargets.org/target/ENSG00000177556/associations>,
  `SQLE` <https://platform.opentargets.org/target/ENSG00000104549/associations>,
  `HIF1A` <https://platform.opentargets.org/target/ENSG00000100644/associations>,
  `CBX3` <https://platform.opentargets.org/target/ENSG00000122565/associations>,
  `CFB` <https://platform.opentargets.org/target/ENSG00000243649/associations>,
  `TIMP1` <https://platform.opentargets.org/target/ENSG00000102265/associations>,
  `IL15` <https://platform.opentargets.org/target/ENSG00000164136/associations>,
  `JAK3` <https://platform.opentargets.org/target/ENSG00000105639/associations>,
  `PTPRE` <https://platform.opentargets.org/target/ENSG00000132334/associations>.
- GWAS Catalog gene pages: <https://www.ebi.ac.uk/gwas/genes/ATOX1>,
  <https://www.ebi.ac.uk/gwas/genes/SQLE>,
  <https://www.ebi.ac.uk/gwas/genes/HIF1A>,
  <https://www.ebi.ac.uk/gwas/genes/CBX3>,
  <https://www.ebi.ac.uk/gwas/genes/CFB>,
  <https://www.ebi.ac.uk/gwas/genes/TIMP1>,
  <https://www.ebi.ac.uk/gwas/genes/IL15>,
  <https://www.ebi.ac.uk/gwas/genes/JAK3>,
  <https://www.ebi.ac.uk/gwas/genes/PTPRE>.
- Functional/druggability anchors: UniProt `SQLE`
  <https://www.uniprot.org/uniprotkb/Q14534/entry>, UniProt `CFB`
  <https://www.uniprot.org/uniprotkb/P00751/entry>, UniProt `TIMP1`
  <https://www.uniprot.org/uniprotkb/P01033/entry>.
- Prior-art and translational anchors: human SQLE structural/inhibitor work
  <https://pubmed.ncbi.nlm.nih.gov/34288071/>, ATOX1 and intestinal
  inflammation <https://pubmed.ncbi.nlm.nih.gov/37605010/>, CFB coding variant
  in perianal Crohn disease <https://pubmed.ncbi.nlm.nih.gov/39307822/>,
  iptacopan/factor-B clinical trial record example
  <https://clinicaltrials.gov/study/NCT04154787>, iptacopan label
  <https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/218276s000lbl.pdf>,
  IL-15 celiac trial example <https://clinicaltrials.gov/study/NCT02633020>,
  AMG 714 / IL-15 in celiac disease
  <https://pubmed.ncbi.nlm.nih.gov/34111489/>, anti-IL-15 in rheumatoid
  arthritis <https://pubmed.ncbi.nlm.nih.gov/17265473/>.

## Candidate Calls

| Candidate | Local residual signal | Genetics call | Modality call | Prior-art call | Triage |
|---|---:|---|---|---|---|
| `ATOX1` | Top residual row; IBD stromal plus psoriasis stromal; no MS support | No cross-autoimmune target genetics found | Intracellular copper chaperone/transcriptional cofactor; difficult direct modality | Already linked to intestinal inflammation; not clean enough for broad autoimmune novelty | **No-go therapeutic; possible fail-fast biology scout** |
| `SQLE` | Top residual row; IBD stromal plus psoriasis stromal; negative MS trend | No useful cross-autoimmune genetics | Enzyme and chemically targetable | Sterol pathway/SQLE inhibitors and statin-adjacent prior art crowd mechanism; systemic lipid/skin toxicity risk | **No-go unless a narrow immune-cell sterol assay emerges** |
| `TPM4` | Broad epithelial/stromal/myeloid residual correlations | No target genetics | Structural cytoskeletal protein; poor direct target | Likely state/contractility marker, not intervention node | **No-go** |
| `LDLRAD3` | IBD stromal/myeloid and psoriasis APC/stromal | No target genetics found | Receptor-like but poorly characterized; no obvious therapeutic package | Biology too underdefined for claim | **No-go for now** |
| `C1QTNF1` | IBD stromal residual signal | No cross-autoimmune target genetics | Secreted adipokine-like protein, but direction unclear | Inflammation/metabolic literature likely makes broad modulation obvious; target biology weak | **No-go** |
| `HIF1A` | Strong residual IBD stromal signal | Pathway-level autoimmune genetics exist around hypoxia/inflammation, not selective target genetics | Drug-modulatable transcriptional pathway, but broad | Massive HIF/inflammation/IBD/autoimmunity prior art and safety issues | **Hard blocker** |
| `CBX3` | Four-disease, nominal MS-positive local expression | No cross-autoimmune target genetics | Chromatin protein; possible oncology-style epigenetic tooling, not selective autoimmune modality | Broad chromatin target, likely toxicity/non-specificity | **No-go; expression/state marker only** |
| `CFB` | Four-disease local expression; complement-linked compartments | Best genetics/modality among named rows; complement factor B has direct druggability and complement genetics | Existing factor-B inhibitors/antisense/biologics make modality real | Heavily prior-arted by iptacopan and complement programs; broad autoimmune complement blockade is not novel | **Comparator / blocker-heavy follow-up only** |
| `TIMP1` | Strong UC stromal/myeloid residuals plus T1D/psoriasis expression | No convincing cross-autoimmune target genetics | Secreted protein, antibody/biologic conceivable | MMP/TIMP biology is disease- and repair-risk heavy; inhibition could worsen tissue damage | **No-go therapeutic** |

## Hard Prior-Art / Genetics Blockers

- **Complement factor B / `CFB`:** this is the strongest modality-positive
  row, but factor-B inhibition is already a clinical therapeutic class. A broad
  autoimmune or complement-inflammatory therapeutic claim would collide with
  existing iptacopan/factor-B programs and complement-disease patents/trials.
  The recent Crohn coding-variant paper is useful biology, but it does not
  create an open broad therapeutic lane.
- **`HIF1A`:** too upstream and too crowded. It is a central inflammatory and
  metabolic transcriptional regulator, so intervention is biologically
  plausible but not selective or novel.
- **`IL15` / `JAK3`:** both appear in the top candidate panel and are real
  autoimmune intervention biology, but the therapeutic space is saturated:
  anti-IL-15 has celiac and RA clinical prior art, and JAK3/JAK-family
  inhibition is an established autoimmune drug class.
- **`SQLE`:** druggable enzyme, but no cross-autoimmune genetics and likely
  sterol-pathway prior art. Its current signal looks more like tissue metabolic
  state than a causally anchored autoimmune target.
- **`TIMP1` / MMP axis and `MMP7`:** secreted/enzyme-adjacent and measurable,
  but target direction is not safe. Matrix remodeling can be pathogenic,
  reparative, or fibrosis-linked depending on tissue and phase.
- **`ATOX1`, `TPM4`, `LDLRAD3`, `C1QTNF1`, `CBX3`:** no sufficient
  cross-autoimmune genetics and no mature, selective modality. These cannot
  support a therapeutic claim from the current evidence.

## Other Top-20 Rows Worth Explicitly Noting

- `IFITM3` / `IFITM2`: strong broad expression rows and plausible IFN-state
  biology, but they are interferon/antiviral restriction genes with unclear
  intervention direction and no clean autoimmune target genetics. Treat as IFN
  residual-state markers, not drug targets.
- `PSME1` / `PSME2` / `POMP`: immunoproteasome/proteasome-adjacent biology is
  plausible, but targeting these specific regulators is not currently a clean
  autoimmune modality. Immunoproteasome inhibition is itself prior-arted.
- `NLRC5`: mechanistically coherent for antigen-presentation state, but it is
  a transcriptional regulator and not a tractable selective intervention point.
- `PTPRE`: more interesting than many generic structural rows because it is a
  phosphatase and recurrent in IBD myeloid/stromal compartments, but I did not
  identify cross-autoimmune genetics or a credible selective therapeutic
  package. It remains a low-priority scout.
- `CARD16`: inflammasome-adjacent and biologically plausible, but modality and
  genetics are not strong enough for promotion.
- `PDPN`, `COL4A1`, `MMP7`, `REG1A`, `CXCL8`, `CCL20`, `LCN2`, `S100A8`:
  biologically plausible tissue-injury, epithelial, stromal, neutrophil, or
  chemokine markers, but they are either prior-arted, non-specific, or unsafe
  as target claims.

## Candidate Calls By Claim Type

No candidate supports: **new cross-autoimmune, genetics-backed therapeutic
claim.**

Potential comparator only:

- `CFB`: best druggability and complement biology; blocked by clinical/prior
  art burden.
- `IL15` / `JAK3`: strong autoimmune modality comparators; blocked by clinical
  prior art.
- `HIF1A`: biology comparator for metabolic/hypoxic licensing; blocked by
  breadth and prior art.

Potential fail-fast biology scouts:

- `ATOX1`: test only if the next local analysis can show immune-cell-specific,
  IFN/NF-kB/stress-residual activity outside IBD stromal contexts.
- `SQLE`: test only if immune-cell cholesterol-biosynthesis state survives
  residualization and does not collapse into keratinocyte/epithelial metabolic
  stress.
- `PTPRE`: test only if phosphatase-centered myeloid residuals recur in a new
  primary autoimmune tissue and can be linked to a perturbable signaling edge.

## Top 3 For Foundation-Model Follow-Up

Strict answer: **none deserve foundation-model follow-up as therapeutic leads
yet.** The genetics/prior-art gates are not met.

If the orchestrator wants a limited fail-fast foundation-model queue, use:

1. `CFB` as a positive-control comparator, not a novelty lead. Ask whether
   factor-B/complement residual expression is upstream of the local module or
   merely tissue-injury complement load.
2. `ATOX1` as a low-prior-art biology scout. Ask whether perturbation changes
   inflammatory/lysosomal/APC readouts in immune contexts, and require effects
   after generic stress and NF-kB controls.
3. `SQLE` as a druggable-enzyme scout. Ask whether partial suppression moves
   macrophage/stromal inflammatory residuals without simply inducing sterol
   stress or broad cytotoxicity.

Do not prioritize `HIF1A`, `IL15`, `JAK3`, `TIMP1`, or `MMP7` for
foundation-model novelty follow-up unless the purpose is explicitly comparator
or blocker characterization.

## Decision

The broad residual-gate run is useful as a source of new biology questions, but
it does not rescue a V3 therapeutic target. The only defensible next step is
fail-fast modeling/perturbation on `CFB`, `ATOX1`, and `SQLE` as comparator or
scout nodes, while preserving the negative call that no candidate currently
passes cross-autoimmune genetics plus non-blocking prior art.
