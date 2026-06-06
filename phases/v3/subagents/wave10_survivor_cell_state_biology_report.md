# Wave 10 Survivor Cell-State Biology Scout

Returned: 2026-05-27.

Scope: biology scout for the unrestricted broad-screen survivors after `APOC1`
failed Geneformer support:

`SNX10`, `C15ORF48`, `TNFAIP8L1`, `FMNL2`, `SEL1L3`, `PLEK2`, `DAP`,
`PPP3CA`, `CXCL9`, `IL2RG`, `ABHD2`, `BIRC3`, `SDC4`, `STARD10`.

Conclusion discipline: this is not a final finding and not a target promotion.
The goal is to identify which survivors look like recurrent disease cell-state
biology rather than generic proliferation/stress, which are myeloid,
lysosomal, or lipid adjacent, and which have a tissue pattern that could justify
a lead-indication validation test.

## Bottom Line

The survivor set does not collapse into one clean cross-autoimmune mechanism.
It splits into two plausible cell-state branches plus a generic stress/survival
tail:

1. **Inflammatory myeloid / immunometabolic branch:** strongest for
   `C15ORF48` and `SNX10`, with `IL2RG` and `CXCL9` as broader immune/IFN
   context markers. This is the most coherent branch, but it is still marker
   biology, not intervention evidence.
2. **Barrier/stromal/endothelial remodeling branch:** strongest for `FMNL2`,
   `SDC4`, `ABHD2`, `SEL1L3`, `PLEK2`, and partly `STARD10`. This branch is
   tissue-state biology, not a myeloid-lysosomal successor claim.
3. **Generic stress/survival/signaling tail:** `DAP`, `BIRC3`, and `PPP3CA`
   are locally positive but biologically too broad to treat as specific
   cross-disease transitions without stronger cell-state validation.

Important local guardrail: in
`results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`, **none** of
the 14 requested survivors is flagged by the pipeline as
`in_lipid_lysosomal_myeloid_neighborhood=True`. Any myeloid, lysosomal, or
lipid adjacency below comes from the compartment pattern plus literature, not
from the local predefined neighborhood flag.

## Local Evidence Used First

Local files read:

- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_ms_positive_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_discovery_summary.json`
- `results_v3/existing_evidence_candidate_matrix.tsv`
- `results_v3/geneformer_candidate_delete/geneformer_candidate_delete_gene_summary.tsv`
- `results_v3/geneformer_candidate_delete/geneformer_candidate_delete_metrics.tsv`
- `results_v3/geneformer_pivot_panel_delete/geneformer_pivot_panel_gene_summary.tsv`
- `results_v3/pivot_panel_triage/pivot_panel_summary.tsv`
- `ORCHESTRATION_LOG_V3.md`
- `LAB_NOTEBOOK_V3.md`
- `subagents_v3/wave8_candidate_breadth_report.md`
- `subagents_v3/wave7_lipid_myeloid_target_scout_report.md`

Broad-screen context:

- The broad discovery run covered 17 local disease/compartment h5ad analyses
  and 282,630 donor-level gene contrasts.
- All 14 requested survivors are nominally MS-positive in the imported
  `GSE111972` white-matter microglia/macrophage anchor, but all have weak MS FDR
  values around 0.83-0.85. Treat this as an MS trend, not independent MS proof.
- None of the 14 has a negative nominal local broad-h5ad disease compartment in
  the extracted rows.
- Positive FDR10 support outside the imported MS anchor is limited to:
  `C15ORF48` in Crohn/UC myeloid, `SNX10` in Crohn myeloid, `SEL1L3` in UC
  stromal, `IL2RG` in UC myeloid, `ABHD2` in UC epithelial, and `SDC4` in T1D
  endothelial.
- Existing evidence matrix support is sparse for this set: `FMNL2` has a
  positive MS MIMS2-like microglia row; `PPP3CA` and `STARD10` are locally
  mostly null in the existing MS rows; most other survivors do not appear in the
  prior candidate matrix.
- Geneformer does not rescue this set. `APOC1` failed the pivot panel screen
  with 0 support contexts. In the older candidate screen, `SNX10` had support
  flags in some contexts but aggregate mean cosine/projection shifts were
  negative; `FMNL2` was weak/mixed; `TNFAIP8L1` was weak/mixed; `C15ORF48` was
  not in the Geneformer token dictionary in that run.

## Conservative Ranking

Ranks prioritize coherent cell-state biology and lead-indication plausibility,
not raw broad-screen score alone.

| Rank | Gene | Scout call | Local pattern | Biology read | Main caveat |
|---:|---|---|---|---|---|
| 1 | `C15ORF48` | Best coherent inflammatory-myeloid survivor | Positive in Crohn, UC, and T1D; strongest rows are UC myeloid +4.45 log2-CPM, FDR 0.0287, and Crohn myeloid +3.88, FDR 0.0848; MS trend +1.22, p=0.00375 | Macrophage stimulation / inflammatory immunometabolic marker; literature links it to inflammation-induced mitochondrial cytochrome c oxidase remodeling and inflammatory macrophage states | Target biology is unclear; can still be an inflammation-response marker rather than a causal node |
| 2 | `SNX10` | Best lysosomal/endosomal-myeloid survivor | Crohn and UC myeloid positive, plus T1D endothelial/stellate positives; Crohn myeloid is FDR10; MS trend +0.71, p=0.0127 | Sorting nexin/endosomal trafficking; literature supports macrophage polarization/colitis and osteoclast lysosomal trafficking biology | Geneformer aggregate direction was negative; intervention tractability and cell specificity are unresolved |
| 3 | `FMNL2` | Best barrier/migration remodeling survivor | Positive in 4 diseases and 5 compartments: IBD epithelium, psoriasis keratinocyte, T1D endothelial/ductal; existing matrix has positive MS MIMS2-like microglia row | Formin/actin protrusion and migration biology; fits tissue remodeling and inflammatory motility more than proliferation | Not lipid/lysosomal; local signal is mostly tissue-resident rather than myeloid |
| 4 | `SDC4` | Strongest tissue-specific endothelial/matrix clue | T1D endothelial +2.09, FDR 0.0396; T1D beta, UC epithelial, and UC myeloid nominal positives; MS trend +0.96, p=0.0250 | Syndecan-4 / heparan sulfate proteoglycan; matrix, endothelial, epithelial barrier, and inflammation literature | Broad matrix/repair biology; direct modulation could harm tissue repair |
| 5 | `ABHD2` | IBD epithelial lipid-hydrolase scout | UC epithelial +0.95, FDR 0.0295; Crohn epithelial nominal positive; MS trend +0.71, p=0.00324 | Alpha/beta hydrolase, TAG/ester hydrolase; literature links ABHD2 to lipid biology and macrophage-rich vascular plaques | Non-MS local breadth is IBD-only and epithelial, not myeloid |
| 6 | `IL2RG` | Gut myeloid immune-activation marker | UC myeloid +1.24, FDR 0.0290; Crohn myeloid +1.34; UC stromal +1.95; MS trend +0.77, p=0.0170 | Common gamma-chain cytokine receptor component; supports immune-cell activation/residency context | High immune-composition and broad cytokine-receptor confounding; unsafe as a direct target axis |
| 7 | `SEL1L3` | Undercharacterized stromal/endothelial scout | UC stromal +2.09, FDR 0.0852; Crohn stromal +1.46; T1D endothelial +1.55; MS trend +0.92, p=0.0181 | Sparse mechanistic literature; expression resources suggest gastrointestinal/lymphoid tissue signal | Biology too thin for promotion; useful only as a validation marker now |
| 8 | `PLEK2` | Cytoskeletal tissue-remodeling scout | Positive in IBD epithelium, Crohn myeloid, and T1D stellate; strong MS trend +3.05, p=0.00738 | Pleckstrin-2 / PI3K phosphoinositide binding, actin rearrangement, cell spreading | Cytoskeletal and hematopoietic confounding; not specific to myeloid/lysosomal/lipid biology |
| 9 | `CXCL9` | IFN chemokine state marker, not target lead | T1D stellate, Sjogren APC, and UC myeloid nominal positives; MS trend +2.55, p=0.0310 | Canonical IFN-gamma-inducible CXCR3 ligand; strong autoimmune-tissue inflammation plausibility | Too generic and heavily prior-arted; best used as a PD/state marker |
| 10 | `STARD10` | Lipid-transfer tissue scout | Crohn stromal/epithelial and Sjogren stromal positives; MS trend +1.34, p=0.00279 | START-domain phospholipid transfer protein; external expression/literature points to liver and pancreatic beta-cell lipid biology | Local positives are not T1D beta/islet; cross-disease state coherence is weak |
| 11 | `TNFAIP8L1` | Weak immune-metabolic family scout | Positive in 4 diseases but no FDR10 rows; strongest local rows are Crohn stromal, UC epithelial, T1D beta, psoriasis stromal; MS trend +0.46, p=0.00856 | TNFAIP8/TIPE family is immunometabolic/inflammatory, but gene-specific evidence for `TNFAIP8L1` is thin | Low local statistical strength and weak mechanistic specificity |
| 12 | `BIRC3` | Generic NF-kB/survival tail | T1D endothelial/stellate and UC epithelial/stromal positives; MS trend +0.77, p=0.0182 | cIAP2/NF-kB/TNF survival and inflammatory cell-death control | Broad stress/survival response; target biology crowded and non-specific |
| 13 | `PPP3CA` | Generic calcineurin signaling tail | IBD epithelial and T1D acinar positives; MS trend +0.37, p=0.0343 | Calcineurin catalytic subunit; immune and calcium/NFAT biology is real | Broad immunosuppression pathway, not a specific survivor state |
| 14 | `DAP` | Generic IFN/cell-death/autophagy tail | IBD epithelial plus psoriasis stromal/APC positives; MS trend +0.39, p=0.00807 | Death-associated protein 1; IFN-gamma cell-death/autophagy literature | Most likely generic IFN/stress/death response among the survivors |

## Coherent Transition vs Generic Stress

Most coherent as cross-disease cell-state biology:

- `C15ORF48`: coherent inflammatory macrophage/immunometabolic signal. The
  local signal is centered on Crohn/UC myeloid and extends into T1D
  endothelial/stellate compartments. Literature supports induction in
  stimulated macrophages and inflammatory tissues. This is not a classic
  proliferation marker.
- `SNX10`: coherent myeloid/endosomal-lysosomal state. Local Crohn/UC myeloid
  support is strong enough to justify an IBD macrophage validation test.
  Literature connects SNX10 to endosomal/lysosomal trafficking and macrophage
  polarization in colitis.
- `FMNL2` and `PLEK2`: coherent if framed as tissue remodeling/cell migration,
  not if framed as lipid-lysosomal myeloid biology. The local signal is mainly
  epithelial, keratinocyte, endothelial, and stellate.
- `SDC4` and `ABHD2`: coherent tissue-state leads, especially endothelial/
  matrix and IBD epithelial lipid/barrier biology respectively. They do not
  define a pan-myeloid transition.

Likely state markers but too generic for target claims:

- `CXCL9`: IFN-gamma chemokine state. Useful to annotate an inflamed tissue
  axis but not a distinctive mechanism.
- `IL2RG`: immune cytokine-receptor composition/activation marker. The local
  gut myeloid pattern is real, but the biology is too broad.

Generic stress/survival/signaling tail:

- `DAP`: IFN/cell-death/autophagy response.
- `BIRC3`: NF-kB/cIAP survival and inflammatory cell-death control.
- `PPP3CA`: calcineurin/NFAT signaling. It is biologically important, but broad
  calcineurin biology is not a specific cell-state transition.

Underpowered/undercharacterized:

- `TNFAIP8L1`, `SEL1L3`, and `STARD10` should not be interpreted beyond scout
  status without independent replication and cell-type localization.

## Myeloid, Lysosomal, and Lipid Adjacency

| Gene | Myeloid/APC adjacency | Lysosomal/endosomal adjacency | Lipid/metabolic adjacency | Read |
|---|---|---|---|---|
| `C15ORF48` | High: Crohn/UC myeloid FDR10, macrophage-stimulation literature | Low/directly not lysosomal | Moderate: mitochondrial/immunometabolic remodeling | Best inflammatory-myeloid marker, not lipid-lysosomal target |
| `SNX10` | High: Crohn/UC myeloid, macrophage colitis literature | High: sorting nexin/endolysosomal trafficking, osteoclast lysosomal biology | Indirect: IBD/cholesterol barrier literature | Best lysosomal/endosomal survivor |
| `IL2RG` | High but broad immune | Low | Low | Immune-cell activation/composition marker |
| `CXCL9` | Moderate/high in APC contexts, but IFN-driven | Low | Low | Inflamed APC/tissue chemokine marker |
| `ABHD2` | Literature macrophage-plaque adjacency; local myeloid is absent | Low | High: hydrolase/lipid metabolism | Best lipid-adjacent IBD epithelial survivor |
| `STARD10` | Low | Low | High: phospholipid transfer, beta-cell/liver literature | Lipid-transfer tissue scout, weak local disease fit |
| `SDC4` | Low/moderate: UC myeloid nominal; DC-HIL/MDSC autoimmune literature | Low | Matrix/glycosaminoglycan rather than lipid | Endothelial/matrix injury state |
| `FMNL2` | Low/moderate: existing MS MIMS2-like row, but local direct signal tissue-resident | Low | Low | Migration/remodeling state |
| `PLEK2` | Weak/moderate: Crohn myeloid nominal | Low | PI3K phosphoinositide/cytoskeleton, not lipid-handling | Cytoskeletal remodeling, possible confound |
| `TNFAIP8L1` | Weak | Low | Possible TNFAIP8/TIPE family immunometabolic adjacency, gene-specific thin | Hold |
| `SEL1L3` | Weak/unknown | Unknown | Unknown | Hold; expression marker only |
| `BIRC3` | Broad immune/inflammatory | Low | Low | Generic NF-kB/cell survival |
| `PPP3CA` | Broad immune signaling | Low | Low | Generic calcineurin |
| `DAP` | IFN/stress adjacent | Autophagy adjacent, not lysosomal-specific | Low | Generic cell-death/stress |

## Lead-Indication Clues

These are validation hypotheses only.

### IBD / Colon

Most supportable lead-indication frame: **IBD macrophage plus epithelial barrier
state**, not broad autoimmunity.

Best local genes:

- Myeloid: `C15ORF48`, `SNX10`, `IL2RG`; `PLEK2` and `SDC4` weaker.
- Epithelial/barrier: `ABHD2`, `FMNL2`, `PLEK2`, `DAP`, `PPP3CA`, `BIRC3`.
- Stromal: `SEL1L3`, `STARD10`, `TNFAIP8L1`.

Validation need: donor-level replication in independent Crohn/UC single-cell
datasets with macrophage, epithelial, and stromal compartments analyzed
separately. Do not pool compartments; the biology differs.

### T1D / Islet-Vascular-Stromal

Most supportable lead-indication frame: **islet endothelial/stellate injury or
vascular inflammation**, not beta-cell intrinsic autoimmunity.

Best local genes:

- Endothelial/stellate: `C15ORF48`, `SNX10`, `SEL1L3`, `BIRC3`, `SDC4`,
  `CXCL9`, `PLEK2`.
- Beta cell: only `SDC4` and `TNFAIP8L1` have local beta-cell nominal positives.
- Literature-only beta/lipid clue: `STARD10` has pancreatic beta-cell lipid
  biology literature, but the local broad-h5ad result here did not show a T1D
  beta positive for `STARD10`.

Validation need: independent human T1D islet sc/snRNA with endothelial,
stellate/pericyte, acinar/ductal, and beta compartments separated.

### Psoriasis / Skin

Most supportable lead-indication frame: **keratinocyte/stromal remodeling**.

Best local genes:

- `FMNL2`: psoriasis keratinocyte positive.
- `DAP`: skin stromal and APC positives.
- `TNFAIP8L1`: skin stromal positive.

This is not a lipid-lysosomal myeloid indication from the local evidence.

### Sjogren / Salivary Gland

Most supportable lead-indication frame: **inflamed gland APC/stromal marker**,
but current support is weak.

Best local genes:

- `CXCL9`: salivary gland APC positive.
- `STARD10`: salivary gland stromal/endothelial positive.

This is too thin for promotion, but useful for validation panel design.

### MS

All 14 survivors have nominal imported MS white-matter positive trends, but none
has strong MS FDR support in the broad-rank table. `FMNL2` is the only one with
a positive existing MS MIMS2-like microglia row in
`existing_evidence_candidate_matrix.tsv`. `PPP3CA` and `STARD10` are mostly null
in existing MS rows. Treat MS as an anchor to replicate, not as a solved lead
indication.

## Source Links and Literature Queries

Representative literature and expression-resource links checked:

- `C15ORF48`: inflammation and macrophage mitochondrial remodeling:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8654286/ ;
  HPA expression page:
  https://www.proteinatlas.org/ENSG00000166920-C15orf48 ;
  PubMed query:
  https://pubmed.ncbi.nlm.nih.gov/?term=C15ORF48+macrophage+inflammation
- `SNX10`: macrophage polarization/experimental colitis:
  https://pubmed.ncbi.nlm.nih.gov/26856241/ ;
  IBD/barrier/cholesterol paper:
  https://pubmed.ncbi.nlm.nih.gov/39412576/ ;
  osteoclast/endolysosomal trafficking:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC6570537/ ;
  PubMed query:
  https://pubmed.ncbi.nlm.nih.gov/?term=SNX10+macrophage+colitis
- `FMNL2`: actin protrusion/migration:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC3765947/ ;
  tissue characterization:
  https://bmcmolcellbiol.biomedcentral.com/articles/10.1186/1471-2121-11-55 ;
  HPA:
  https://www.proteinatlas.org/ENSG00000157827-FMNL2/tissue
- `TNFAIP8L1`: NCBI gene and related articles:
  https://www.ncbi.nlm.nih.gov/gene/126282 ;
  TNFAIP8/TIPE family review query:
  https://pubmed.ncbi.nlm.nih.gov/?term=TNFAIP8L1+TIPE1+inflammation+immune
- `SEL1L3`: HPA tissue page:
  https://www.proteinatlas.org/ENSG00000091490-SEL1L3/tissue ;
  NCBI gene:
  https://www.ncbi.nlm.nih.gov/gene/23231 ;
  PubMed query:
  https://pubmed.ncbi.nlm.nih.gov/?term=SEL1L3+immune+inflammation
- `PLEK2`: pleckstrin-2/cytoskeleton review:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8637889/ ;
  UniProt:
  https://www.uniprot.org/uniprotkb/Q9NYT0/entry ;
  HPA:
  https://www.proteinatlas.org/ENSG00000100558-PLEK2
- `DAP`: IFN-gamma-induced death-associated protein discovery:
  https://pubmed.ncbi.nlm.nih.gov/7828849/ ;
  DAP1 autophagy regulator:
  https://pubmed.ncbi.nlm.nih.gov/20537536/ ;
  UniProt:
  https://www.uniprot.org/uniprotkb/P51397/entry
- `PPP3CA`: calcineurin/NFAT/T-cell activation:
  https://pubmed.ncbi.nlm.nih.gov/8668213/ ;
  calcineurin inhibitor mechanism:
  https://pubmed.ncbi.nlm.nih.gov/7509138/ ;
  PubMed query:
  https://pubmed.ncbi.nlm.nih.gov/?term=PPP3CA+calcineurin+NFAT+autoimmune
- `CXCL9`: T1D chemokine expression:
  https://pubmed.ncbi.nlm.nih.gov/22210319/ ;
  PubMed query:
  https://pubmed.ncbi.nlm.nih.gov/?term=CXCL9+autoimmune+disease+Sjogren+ulcerative+colitis+type+1+diabetes
- `IL2RG`: HPA:
  https://v22.proteinatlas.org/ENSG00000147168-IL2RG ;
  IL-2 receptor/common gamma-chain review:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC9633542/ ;
  myeloid IL2R expression:
  https://pubmed.ncbi.nlm.nih.gov/8630406/
- `ABHD2`: TAG lipase/ester hydrolase and macrophage plaque context:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4945992/ ;
  ABHD inhibitor/lipid-disease review:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8389839/ ;
  HPA:
  https://v22.proteinatlas.org/ENSG00000140526-ABHD2/tissue
- `BIRC3`: cIAP2 macrophage survival/NF-kB:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC1346893/ ;
  cIAP1/2 cell-death/inflammation query:
  https://pubmed.ncbi.nlm.nih.gov/?term=BIRC3+cIAP2+inflammation+cell+death
- `SDC4`: DC-HIL/syndecan-4 autoimmune response:
  https://pubmed.ncbi.nlm.nih.gov/24516197/ ;
  pulmonary inflammation:
  https://pubmed.ncbi.nlm.nih.gov/22427536/ ;
  fibrosis/inflammation:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2877927/ ;
  HPA:
  https://www.proteinatlas.org/ENSG00000124145-SDC4/tissue
- `STARD10`: phospholipid transfer:
  https://www.sciencedirect.com/science/article/pii/S0021925820567707 ;
  pancreatic beta-cell differentiation/triglyceride metabolism:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC12985384/ ;
  HPA:
  https://www.proteinatlas.org/ENSG00000214530-STARD10/tissue

Search queries used during scouting:

```text
SNX10 macrophage lysosome inflammatory bowel disease monocytes
SNX10 lysosome osteoclast macrophage
C15ORF48 macrophage inflammation single cell colitis
C15orf48 macrophage lysosome inflammation gene
FMNL2 macrophage inflammation actin cytoskeleton immune cell migration
TNFAIP8L1 TIPE1 inflammation macrophage PubMed
SEL1L3 Human Protein Atlas tissue expression immune endothelial
PLEK2 regulates actin cytoskeleton cell spreading migration PubMed
DAP death-associated protein 1 interferon gamma induced cell death autophagy PubMed
PPP3CA calcineurin NFAT T cell activation PubMed review
CXCL9 interferon gamma chemokine autoimmune tissue expression Sjogren ulcerative colitis type 1 diabetes
IL2RG common gamma chain autoimmune disease tissue resident myeloid expression
ABHD2 lipid hydrolase inflammation macrophage tissue expression
BIRC3 cIAP2 NF-kB inflammation autoimmune tissue expression
SDC4 syndecan-4 inflammation fibrosis endothelial autoimmune disease
STARD10 lipid transfer tissue expression pancreas inflammation autoimmune
```

## Recommended Next Validation

Do not promote any survivor now. The cleanest next step is a compact validation
panel with cell-type-stratified tests:

- IBD myeloid/endolysosomal panel: `C15ORF48`, `SNX10`, `IL2RG`, `CXCL9`,
  plus local comparators `LAMP3`, `CTSL`, `CTSB`, and `CHI3L1`.
- IBD epithelial/barrier panel: `ABHD2`, `FMNL2`, `PLEK2`, `DAP`, `PPP3CA`,
  `BIRC3`.
- T1D vascular/stromal panel: `SDC4`, `C15ORF48`, `SNX10`, `SEL1L3`, `BIRC3`,
  `CXCL9`.
- Lipid tissue panel: `ABHD2`, `STARD10`, and `SNX10`; keep `APOC1` as a failed
  Geneformer comparator, not a promoted candidate.

Minimum promotion gate for any survivor: replicate same-direction donor-level
signal in at least one independent dataset for the intended lead indication,
with compartment separation and a negative check against generic IFN/stress,
cell-cycle, and tissue-damage modules.
