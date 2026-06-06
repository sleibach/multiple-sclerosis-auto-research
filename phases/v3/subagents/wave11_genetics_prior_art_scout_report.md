# Wave 11 Genetics / Prior-Art Scout Report

Returned: 2026-05-27 01:23 CEST

Scope: independent genetics and prior-art review of current V3 candidate nodes:
`SNX10`, `C15ORF48`, `LIPA`, `IFI30`/GILT, `CTSS`/`CTSB`/`CTSL`,
`SDC4`, `FMNL2`, `ABHD2`, TYK2/JAK/IFN comparators, and adjacent
lipid-lysosomal myeloid candidates.

Conclusion discipline: this is a scout report, not a finding. I treated local
artifacts as prior work to critique, then verified genetics and prior art using
Open Targets Platform, GWAS Catalog gene pages, PubMed/PMC, ClinicalTrials.gov,
and patent-search links where feasible.

## Bottom Line

No current candidate satisfies both requirements:

1. cross-autoimmune genetic anchoring across the requested disease panel; and
2. sufficient novelty / prior-art clearance for a new intervention point.

Hard call: **no-go for promoting any current candidate node as a V3 autonomous
autoimmune genetics-backed novel intervention finding.**

The split is sharp:

- `TYK2`/JAK/IFN has the cross-autoimmune genetics and clinical tractability,
  but is already a saturated therapeutic lane.
- `IFI30`/GILT has the best candidate-specific MS genetics among the
  lysosomal/APC genes, but the genetic anchor is not cross-autoimmune and the
  intervention direction is not safe to infer.
- `CTSS` is the cleanest druggable lysosomal APC enzyme, but direct
  cathepsin-S autoimmune clinical prior art is blocking.
- `SNX10`, `C15ORF48`, `SDC4`, `FMNL2`, and `ABHD2` are expression/state
  scouts. They do not have enough target genetics across autoimmune disease.
- `LIPA` is biologically attractive for lysosomal lipid repair, but current
  local expression is compartment-conflicted, genetics are weak, and the CNS
  repair lane is already prior-arted.

## Local Artifacts Critiqued

Read first, per instruction:

- `MS_RESEARCH_LOG_2026-05-26.md`
- `FINDING_EXECUTION_PHASE.md`
- `FINDING.md`
- `EXHAUSTION.md`
- `ORCHESTRATION_LOG_V3.md`
- `LAB_NOTEBOOK_V3.md`
- `results_v3/unrestricted_survivor_scan/unrestricted_survivor_candidates.tsv`
- `results_v3/geneformer_unrestricted_survivor_delete/geneformer_unrestricted_survivor_gene_summary.tsv`

Additional V3 reports read because they directly bear on this scout:

- `subagents_v3/genetics_james_report.md`
- `subagents_v3/wave4_lipa_scout_report.md`
- `subagents_v3/wave7_lipid_myeloid_target_scout_report.md`
- `subagents_v3/wave8_target_prior_art_druggability_report.md`
- `subagents_v3/wave10_survivor_cell_state_biology_report.md`
- `subagents_v3/intervention_ohm_report.md`
- `subagents_v3/cd74_mif_novelty_galileo_report.md`

Critique:

- The unrestricted survivor scan is useful for expression triage, not genetics.
  Its own rows show weak MS FDR values for the survivor genes and sparse
  Open Targets evidence. It should not be read as genetic support.
- The Geneformer survivor-deletion screen does not rescue the survivor set:
  `SNX10` is mixed/weak, `ABHD2` has no support contexts, and `C15ORF48` was
  absent from the token dictionary in the relevant route.
- The V3 genetics report's promotion of `IFI30 + IRF1/HLA-II` is reasonable as
  an axis-level interpretation, but `IFI30` itself remains mostly MS anchored,
  not cross-autoimmune anchored.
- The V3 intervention report correctly demotes `IFI30` as a direct intervention
  because it is an intracellular lysosomal reductase with unclear modality and
  direction.
- The `LIPA` scout already reaches the right local conclusion: retain as a
  repair marker/biology clue, not a central cross-autoimmune node.

## Verification Methods

Primary database checks:

- Open Targets Platform GraphQL target-disease associations, queried locally on
  2026-05-27. Raw qualitative score output is preserved at
  `tmp_v3/wave11_opentargets_target_disease_scores.tsv`.
- Open Targets target pages, for example:
  - `IFI30`: <https://platform.opentargets.org/target/ENSG00000216490/associations>
  - `CTSS`: <https://platform.opentargets.org/target/ENSG00000163131/associations>
  - `CTSB`: <https://platform.opentargets.org/target/ENSG00000164733/associations>
  - `TYK2`: <https://platform.opentargets.org/target/ENSG00000105397/associations>
  - `IRF1`: <https://platform.opentargets.org/target/ENSG00000125347/associations>
  - `MERTK`: <https://platform.opentargets.org/target/ENSG00000153208/associations>
- GWAS Catalog gene pages, for example:
  - `SNX10`: <https://www.ebi.ac.uk/gwas/genes/SNX10>
  - `C15orf48`: <https://www.ebi.ac.uk/gwas/genes/C15orf48>
  - `LIPA`: <https://www.ebi.ac.uk/gwas/genes/LIPA>
  - `IFI30`: <https://www.ebi.ac.uk/gwas/genes/IFI30>
  - `CTSS`: <https://www.ebi.ac.uk/gwas/genes/CTSS>
  - `CTSB`: <https://www.ebi.ac.uk/gwas/genes/CTSB>
  - `FMNL2`: <https://www.ebi.ac.uk/gwas/genes/FMNL2>
  - `ABHD2`: <https://www.ebi.ac.uk/gwas/genes/ABHD2>
  - `TYK2`: <https://www.ebi.ac.uk/gwas/genes/TYK2>
- PubMed/PMC and ClinicalTrials.gov targeted searches, linked in candidate
  sections below.

Disease panel requested:

`MS`, `RA`, `SLE`, `Crohn`, `UC`, `psoriasis`, `T1D`, `Sjogren`, `AS`,
`autoimmune thyroid disease`, `celiac`, `PBC`.

## Genetics Evidence Matrix

Legend:

- `G`: credible target-level or strong locus-level genetics for the named gene
  in that disease.
- `g?`: weak / non-decisive locus or database signal; not enough for target
  promotion.
- `-`: no convincing target genetics identified in this scout.
- `blocked`: genetics may exist, but prior art already blocks novelty.

| Candidate | MS | RA | SLE | Crohn | UC | Psoriasis | T1D | Sjogren | AS | AITD | Celiac | PBC | Genetics read |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SNX10` | - | - | - | - | - | - | - | - | - | - | - | - | No target genetics found across the panel. Local Crohn/UC myeloid expression is not genetic anchoring. |
| `C15ORF48` / MOCCI | - | - | - | - | - | - | - | - | - | - | - | - | No target genetics found. Treat as inflammation/immunometabolic marker. |
| `LIPA` / LAL | - | - | - | - | - | - | - | - | - | - | - | - | No useful autoimmune target genetics found despite clear lipid biology. |
| `IFI30` / GILT | G | - | - | - | - | - | - | - | - | - | - | - | MS genetics are real enough to keep as an axis marker; cross-autoimmune genetics are absent. |
| `CTSS` | - | - | - | g? | - | - | - | - | - | - | - | - | Little target genetics; druggability comes from enzyme biology, not genetics. |
| `CTSB` | - | - | g? | - | - | - | G | - | - | g? | - | - | T1D is the clearest database signal; SLE/AITD are weak or locus-confounded. Not cross-autoimmune. |
| `CTSL` | - | - | - | - | - | - | - | - | - | - | - | - | No autoimmune genetics sufficient for promotion. |
| `SDC4` | - | - | - | - | - | - | - | - | - | - | - | - | RA/EAE biology exists, but no target genetics. |
| `FMNL2` | - | - | - | G/g? | - | - | - | - | - | - | - | - | Crohn/IBD evidence exists, including a rare pediatric CD variant report, but no broad autoimmune anchor. |
| `ABHD2` | - | - | - | - | - | - | - | - | - | - | - | - | No autoimmune genetic anchor identified. |
| `TYK2` | g?/blocked | G/blocked | G/blocked | G/blocked | g?/blocked | G/blocked | G/blocked | -/blocked | g?/blocked | G/blocked | -/blocked | G/blocked | Strongest cross-autoimmune genetic comparator, but already heavily drugged and prior-arted. |
| `JAK1` | G/blocked | G/blocked | -/blocked | -/blocked | -/blocked | -/blocked | -/blocked | -/blocked | -/blocked | G/blocked | -/blocked | -/blocked | Broad clinical/JAK prior art; genetic signals are not specific enough for a novel node. |
| `JAK2` | -/blocked | -/blocked | G/blocked | G/blocked | G/blocked | g?/blocked | -/blocked | -/blocked | G/blocked | -/blocked | -/blocked | -/blocked | Broad JAK prior art and safety baggage block novelty. |
| `STAT1` | - | g? | g? | g? | - | - | g? | g? | - | g? | g? | g? | Low-level genetics across several diseases; too upstream/broad and not a clean drug target. |
| `IRF1` | - | - | G | G | g? | G | g? | - | g? | g? | g? | - | Best non-MHC regulatory genetics after TYK2/JAK comparators, but not a selective intervention point. |
| `MERTK` | G | - | - | g? | - | - | - | - | - | - | - | - | Closest lipid/efferocytosis myeloid genetics comparator; mostly MS-only. |
| `LGALS3` | - | - | - | - | - | - | - | - | - | - | - | - | Literature-rich, genetics-poor; no-go for genetics-backed novelty. |
| `FABP5` | - | - | - | - | - | - | - | - | - | - | - | - | Literature/prior-art rich in EAE/psoriasis; genetics absent. |
| `LTA4H` | - | - | - | g? | - | - | - | - | - | - | - | - | Weak Crohn signal only; leukotriene prior art blocks novelty. |

## Candidate Calls

### `SNX10`

Genetics:

- I found no convincing target-level autoimmune genetic anchoring for `SNX10`
  across MS, RA, SLE, Crohn, UC, psoriasis, T1D, Sjogren, AS, AITD, celiac, or
  PBC in Open Targets/GWAS Catalog checks.
- The local survivor signal is expression-based: Crohn/UC myeloid and T1D
  endothelial/stellate positives. That is not a genetics anchor.

Prior art:

- `SNX10` has direct macrophage/colitis biology. A PubMed-indexed study reports
  SNX10 as a regulator of macrophage polarization in experimental mouse colitis:
  <https://pubmed.ncbi.nlm.nih.gov/26856241/>.
- A more recent IBD/barrier paper links SNX10 expression to barrier dysfunction
  and inflammatory responses: <https://pubmed.ncbi.nlm.nih.gov/39412576/>.
- SNX10 is also tied to endolysosomal/osteoclast trafficking biology, which
  supports plausibility but not autoimmune novelty:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6570537/>.

Hard call: **no-go**. `SNX10` is a plausible IBD macrophage/endosomal marker,
not a cross-autoimmune genetically anchored intervention point.

### `C15ORF48` / MOCCI

Genetics:

- No convincing autoimmune target genetics found across the requested disease
  panel.
- The local `C15ORF48` signal is strong expression biology, especially Crohn/UC
  myeloid, but Geneformer was token-blocked and genetics are absent.

Prior art:

- C15ORF48/MOCCI is already published as an inflammation-induced mitochondrial
  cytochrome-c oxidase remodeling gene:
  <https://pubmed.ncbi.nlm.nih.gov/34878835/> and
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC8654286/>.
- Another full-text paper frames MOCCI/C15ORF48 as coordinating host
  inflammation and immunity:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC8035321/>.
- This biology is not a mature drug target. It is also directionally risky:
  several reports suggest immune-dampening or cytoprotective roles rather than
  a simple inhibit-to-treat strategy.

Hard call: **no-go**. Good inflammatory myeloid marker; no genetics, no
actionable modality, no cross-autoimmune target claim.

### `LIPA` / Lysosomal Acid Lipase

Genetics:

- No useful autoimmune genetic anchor found for `LIPA` across the requested
  panel.
- This agrees with the local `wave4_lipa_scout_report.md`: `LIPA` is not
  genetically anchored as a central cross-autoimmune node.

Prior art:

- `LIPA` encodes lysosomal acid lipase, with well-established biology in
  lysosomal cholesteryl ester and triglyceride hydrolysis. UniProt:
  <https://www.uniprot.org/uniprotkb/P38571/entry>. GeneReviews:
  <https://www.ncbi.nlm.nih.gov/books/NBK305870/>.
- Sebelipase alfa is approved enzyme replacement for LAL deficiency, not
  autoimmune disease. FDA label:
  <https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/125561s020lbl.pdf>.
  Clinical trial example: ARISE / NCT01757184:
  <https://clinicaltrials.gov/study/NCT01757184>.
- The CNS repair angle is already prior-arted by recent white-matter injury
  work reporting LAL/Lipa regulation of a GPNMB+ reparative microglial state,
  myelin-debris digestion, and remyelination:
  <https://link.springer.com/article/10.1186/s12974-026-03782-7>.
- Patent space around LAL enzyme/gene therapy is crowded enough to require
  counsel review before any modality claim. Examples:
  <https://patents.google.com/patent/WO2024254319A1/en> and
  <https://patents.google.com/patent/WO2022122883A1/en>.

Hard call: **no-go as cross-autoimmune intervention**. Keep only as a
repair-competence / lysosomal lipid-handling biomarker or safety comparator.

### `IFI30` / GILT

Genetics:

- `IFI30` is the best candidate-specific genetics-compatible lysosomal/APC node
  in the current V3 set, but the support is mostly **MS-specific**.
- GWAS Catalog lists `IFI30` under MS-associated literature/traits:
  <https://www.ebi.ac.uk/gwas/genes/IFI30>.
- The autoimmune fine-mapping literature explicitly discusses the MS `IFI30`
  locus and LD complexity around the lead coding variant region:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4336207/>.
- Open Targets shows genetic-association evidence for `IFI30` with MS, but I
  did not find comparable target-level evidence across RA, SLE, Crohn, UC,
  psoriasis, T1D, Sjogren, AS, AITD, celiac, or PBC.

Prior art:

- GILT/IFI30 antigen-processing biology is well established. Review:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3125571/>.
- GILT shapes MHC-II-restricted peptidomes and includes known autoantigen
  processing relevance for MOG:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3885806/>.
- EAE prior art is directionally complicated: GILT-free mice can alter MOG
  peptide processing and switch pathogenic mechanisms rather than simply
  eliminating disease:
  <https://pubmed.ncbi.nlm.nih.gov/22586035/>.
- A translational EAE review summarizes IFI30/GILT as antigen-processing
  relevant and notes GILT knockout effects in MOG EAE:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4654535/>.
- I found no mature, selective clinical `IFI30` inhibitor/activator program for
  autoimmune disease in targeted ClinicalTrials.gov searches:
  <https://clinicaltrials.gov/search?term=IFI30> and
  <https://clinicaltrials.gov/search?term=GILT%20autoimmune>.

Hard call: **no-go as direct intervention; keep as axis biomarker**. `IFI30`
can support an IFN/HLA-II/GILT antigen-processing state hypothesis in MS, but
not a cross-autoimmune genetically anchored target claim.

### `CTSS`, `CTSB`, `CTSL`

Genetics:

- `CTSS`: weak/non-decisive Crohn signal in Open Targets; no broad genetic
  anchor across the panel.
- `CTSB`: strongest database signal is T1D; SLE/AITD are weak or
  locus-confounded. Not cross-autoimmune.
- `CTSL`: no convincing autoimmune genetics in this scout.

Prior art:

- Cathepsin activity in MS and EAE is old biology. MS cathepsin expression
  review: <https://pmc.ncbi.nlm.nih.gov/articles/PMC3822953/>.
- Cathepsin B activity in MS brain was already reported decades ago:
  <https://pubmed.ncbi.nlm.nih.gov/7561950/>.
- Cathepsin redundancy in EAE is a major mechanistic blocker for selective
  single-gene claims:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4468166/>.
- `CTSS` is druggable, but direct autoimmune clinical prior art is blocking:
  - RO5459072/petesicatib in primary Sjogren did not produce clinically
    meaningful benefit despite target engagement:
    <https://pmc.ncbi.nlm.nih.gov/articles/PMC10629789/> and
    <https://clinicaltrials.gov/study/NCT02701985>.
  - RO5459072 in celiac gluten challenge showed no clear treatment effect:
    <https://pubmed.ncbi.nlm.nih.gov/39739628/> and
    <https://clinicaltrials.gov/study/NCT02679014>.
  - RWJ-445380 was trialed in active RA:
    <https://clinicaltrials.gov/study/NCT00425321>.
  - A cathepsin-S review notes clinical studies in psoriasis, RA, celiac, and
    Sjogren:
    <https://link.springer.com/article/10.1186/s12931-020-01381-5>.

Hard call: **no-go for novelty; use `CTSS` only as mechanistic comparator**.
The druggability is real, but the intervention lane is crowded and clinically
haircutted.

### `SDC4`

Genetics:

- I found no convincing target genetics for `SDC4` across the requested
  autoimmune disease panel.

Prior art:

- Syndecan-4 is already connected to autoimmune-response regulation through the
  DC-HIL/syndecan-4 pathway in EAE:
  <https://pubmed.ncbi.nlm.nih.gov/24516197/>.
- RA tissue/serology biology is already published:
  <https://pubmed.ncbi.nlm.nih.gov/35725524/>.
- Antibody-mediated SDC4 modulation has been explored in inflammatory
  signaling contexts:
  <https://pubmed.ncbi.nlm.nih.gov/32094158/>.

Hard call: **no-go**. Matrix/endothelial/barrier biology is plausible, but it
is broad repair/inflammation biology without cross-autoimmune genetics.

### `FMNL2`

Genetics:

- Open Targets shows a Crohn disease genetic-association signal for `FMNL2`,
  but I did not find support across the rest of the autoimmune panel.
- The clearest literature is not a common-variant cross-disease anchor; it is a
  rare/de novo variant report in pediatric Crohn disease.

Prior art:

- A PLOS One study characterized an `FMNL2` L136P mutation identified in a
  pediatric Crohn disease case and connected it to actin-dependent cell
  functions:
  <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0252428>.
- `FMNL2` is actin/migration biology, not lipid-lysosomal myeloid biology.
- No mature, selective autoimmune intervention modality was identified.

Hard call: **no-go**. Potential IBD genetics/rare-disease clue, not a
cross-autoimmune intervention point.

### `ABHD2`

Genetics:

- I found no useful autoimmune target genetics for `ABHD2` across the requested
  panel.
- The local signal is IBD epithelial/lipid-hydrolase adjacency, not genetics.

Prior art:

- UniProt annotates ABHD2 as a monoacylglycerol lipase / hydrolase:
  <https://www.uniprot.org/uniprotkb/P08910/entry>.
- NCBI Gene lists ABHD2 literature mainly around sperm activation, COPD,
  atherosclerosis/macrophage-rich plaques, and cancer rather than autoimmune
  disease: <https://www.ncbi.nlm.nih.gov/gene/11057>.
- I did not find direct ABHD2 autoimmune interventional prior art in targeted
  searches, but the lack of genetics and lack of disease-specific perturbation
  evidence are decisive blockers.

Hard call: **no-go**. Too thin for autoimmune genetics or intervention.

### TYK2 / JAK / IFN Pathway Comparators

Genetics:

- This is the strongest genetic comparator in the entire scout.
- TYK2 common and coding variants have been associated with multiple autoimmune
  diseases. A systematic review/meta-analysis covers MS, SLE, Crohn, UC,
  psoriasis, RA, T1D, and IBD:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC8097517/>.
- TYK2 protein-coding protective variants have been linked to RA and broader
  autoimmunity:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC4388675/>.
- TYK2 P1104A has functional autoimmune-protective literature spanning SLE,
  T1D, MS, RA, psoriasis, Crohn, IBD, and UC:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC6355696/>.
- Open Targets shows broad genetic/clinical evidence for `TYK2`, `JAK1`,
  `JAK2`, `STAT1`, and `IRF1`, but `TYK2` and `IRF1` are the most relevant to
  cross-autoimmune susceptibility.

Prior art:

- Deucravacitinib is an approved oral allosteric TYK2 inhibitor for psoriasis
  in multiple jurisdictions; FDA label:
  <https://www.accessdata.fda.gov/drugsatfda_docs/label/2022/214958s000lbl.pdf>.
- BMS announced U.S. FDA approval for active psoriatic arthritis in 2026:
  <https://news.bms.com/news/details/2026/U-S--FDA-Approves-Bristol-Myers-Squibbs-Sotyktu-deucravacitinib-for-the-Treatment-of-Adults-with-Active-Psoriatic-Arthritis/default.aspx>.
- Deucravacitinib has been tested in SLE:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC10100399/> and
  <https://clinicaltrials.gov/study/NCT03252587>.
- Deucravacitinib has also been tested in Crohn/UC phase 2 programs:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC12137900/>.
- Review-level TYK2 therapeutic prior art is extensive:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC9959504/>.

Hard call: **blocked positive control**. TYK2/JAK/IFN proves that the genetics
standard is achievable, but it is not a novel V3 intervention point. Use as
benchmark and ex vivo perturbation control.

### Adjacent Lipid-Lysosomal Myeloid Nodes

#### `MERTK`

Genetics:

- `MERTK` is the closest genetics-backed lipid/efferocytosis myeloid comparator
  I found, but it is mostly MS-specific.
- MS GWAS/eQTL/MR literature prioritizes `MERTK` as a potential MS target:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC7519728/>.
- Earlier MERTK-MS susceptibility work:
  <https://pubmed.ncbi.nlm.nih.gov/21347448/>.
- A recent microglial target paper also names MERTK among MS susceptibility
  genes:
  <https://pubmed.ncbi.nlm.nih.gov/41239018/>.

Prior art / blocker:

- MERTK is a repair/efferocytosis receptor with directionality risk. Inhibiting
  MERTK can plausibly worsen debris clearance, while agonism/delivery is not a
  mature autoimmune modality.
- SLE literature already ties MerTK to apoptotic-cell clearance and tolerance:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3987794/>.

Hard call: **hold/no-go**. Best adjacent genetics clue after `IFI30`, but not
cross-autoimmune and not a clean intervention.

#### `LGALS3`

Genetics:

- No target genetics sufficient for the requested panel.

Prior art / blocker:

- Galectin-3 has direct MS/EAE, macrophage, inflammasome, fibrosis, and
  remyelination literature. Representative PubMed search:
  <https://pubmed.ncbi.nlm.nih.gov/?term=galectin-3+multiple+sclerosis+experimental+autoimmune+encephalomyelitis>.
- Galectin-3 inhibitors are clinically developed mostly outside autoimmunity;
  ClinicalTrials.gov search:
  <https://clinicaltrials.gov/search?term=galectin-3%20inhibitor>.

Hard call: **no-go for genetics-backed novelty**. Could be a fail-fast biology
test only.

#### `FABP5`

Genetics:

- No convincing autoimmune target genetics.

Prior art / blocker:

- Direct EAE/MS and psoriasis prior art exist for FABP5/lipid inflammatory
  biology. PubMed query:
  <https://pubmed.ncbi.nlm.nih.gov/?term=FABP5+inhibitor+experimental+autoimmune+encephalomyelitis+multiple+sclerosis>.

Hard call: **no-go / comparator only**.

#### `LTA4H`

Genetics:

- Weak Crohn database signal only; no cross-autoimmune anchor.

Prior art / blocker:

- Leukotriene B4 / BLT / LTA4H inflammatory disease biology is crowded.
  PubMed query:
  <https://pubmed.ncbi.nlm.nih.gov/?term=LTA4H+Crohn+disease+genetic+association>.
- LTA4H inhibitor clinical development exists outside autoimmune disease,
  e.g. acebilustat:
  <https://pubmed.ncbi.nlm.nih.gov/?term=acebilustat+LTA4H+inhibitor> and
  <https://clinicaltrials.gov/search?term=acebilustat>.

Hard call: **no-go**. Not enough genetics and too much lipid-mediator prior
art.

## Disease-by-Disease Genetics Read

This section answers the requested disease panel explicitly.

| Disease | Verified genetics-bearing nodes from this scout | What fails |
|---|---|---|
| MS | `IFI30`, `MERTK`; TYK2 literature support but Open Targets MS genetics was not the strongest in the current target query. | `SNX10`, `C15ORF48`, `LIPA`, `CTSS/B/L`, `SDC4`, `FMNL2`, `ABHD2` lack sufficient MS target genetics. |
| RA | `TYK2` is strong and blocked; broad JAK clinical precedent. | Survivor and lysosomal-lipid genes lack target genetics; `SDC4` has RA biology but not genetics. |
| SLE | `TYK2`, `IRF1`, and `JAK2` comparators have genetics; `CTSB` is weak/locus-confounded. | `IFI30`, `LIPA`, `SNX10`, `C15ORF48`, `SDC4`, `FMNL2`, `ABHD2` do not anchor. |
| Crohn | `TYK2`, `JAK2`, `IRF1`; `FMNL2` is Crohn-specific/rare-variant plausible; `CTSS`/`LTA4H` weak. | Crohn expression positives for `SNX10`/`C15ORF48` do not convert to genetics. |
| UC | `JAK2`, `TYK2` weak/clinical, `IRF1` weak; broad JAK/TYK prior art. | `ABHD2` local epithelial signal lacks genetics; `SNX10`/`C15ORF48` expression only. |
| Psoriasis | `TYK2` and `IRF1` are strong; deucravacitinib/TYK2 prior art blocks novelty. | `FABP5` has prior art but not genetics; `LIPA` keratinocyte expression is not genetic. |
| T1D | `TYK2`; `CTSB` appears as the clearest cathepsin genetic signal. | `SNX10`, `C15ORF48`, `SDC4`, `ABHD2`, `LIPA` expression signals are not target genetics. |
| Sjogren | No clean candidate genetics among the survivor/lipid-lysosomal set; TYK2 has clinical/literature interest but not strong target genetics in this query. | `CTSS` has direct failed/underwhelming trial precedent despite target engagement. |
| AS | `JAK2` and `TYK2` weak-to-moderate comparator genetics/clinical pathway. | No survivor/lipid-lysosomal genetic anchor. |
| AITD | `TYK2` and `JAK1`; `STAT1/IRF1` weak. | No current survivor/lipid-lysosomal candidate qualifies. |
| Celiac | Mostly HLA biology outside this target list; `STAT1/IRF1` weak database signals only. | `CTSS` celiac trial prior art is negative/underwhelming; no novel genetics. |
| PBC | `TYK2` comparator genetics; `STAT1` weak. | `CTSS`/`CD74`/CXCL10 pathway biology is expression/literature/prior art, not novel target genetics. |

## Patent / Trial Blockers

Representative search links:

- `TYK2 inhibitor autoimmune`: <https://patents.google.com/?q=%22TYK2+inhibitor%22+autoimmune>
- Deucravacitinib trials: <https://clinicaltrials.gov/search?term=deucravacitinib>
- `cathepsin S inhibitor autoimmune`: <https://patents.google.com/?q=%22cathepsin+S+inhibitor%22+autoimmune>
- RO5459072/petesicatib trials: <https://clinicaltrials.gov/search?term=RO5459072>
- `IFI30` / GILT clinical trials: <https://clinicaltrials.gov/search?term=IFI30>
- `LIPA` / sebelipase trials: <https://clinicaltrials.gov/search?term=sebelipase%20alfa>
- `LIPA` patents: <https://patents.google.com/?q=%22lysosomal+acid+lipase%22+autoimmune>
- `SNX10` patents: <https://patents.google.com/?q=SNX10+autoimmune+colitis>
- `C15ORF48` patents: <https://patents.google.com/?q=C15ORF48+autoimmune+inflammation>
- `FMNL2` patents: <https://patents.google.com/?q=FMNL2+inflammatory+bowel+disease>
- `ABHD2` patents: <https://patents.google.com/?q=ABHD2+autoimmune+inflammatory+disease>

Main blockers:

- TYK2/JAK: approved drugs, active clinical programs, extensive patents/trials.
- CTSS: direct autoimmune clinical tests in Sjogren, celiac, RA, psoriasis-like
  contexts; mixed/negative efficacy despite mechanism.
- LIPA: approved replacement therapy for LAL-D and new CNS repair prior art.
- CD74/MIF, while not a main requested target here, is already blocked for a
  broad progressive-MS target claim by SPRINT-MS/ibudilast and MIF/CD74 patents
  per `cd74_mif_novelty_galileo_report.md`.
- Survivor genes: not blocked by strong trials; they fail earlier on genetics,
  causality, and modality.

## Final Go / No-Go Table

| Candidate / axis | Genetics grade | Novelty / prior-art grade | Intervention tractability | Final call |
|---|---|---|---|---|
| `SNX10` | Fail | Some colitis prior art | Poor/unclear | **No-go** |
| `C15ORF48` | Fail | Inflammation/MOCCI prior art | Poor/unclear | **No-go** |
| `LIPA` | Fail | CNS repair + LAL-D therapy prior art | Enhancement delivery hard | **No-go** |
| `IFI30` | MS-only partial pass | EAE/GILT antigen-processing prior art | Poor/unclear direction | **No-go as target; keep biomarker** |
| `CTSS` | Fail/weak | Direct autoimmune trial prior art | Good enzyme tractability | **No-go for novelty; comparator only** |
| `CTSB` | T1D-only partial | Broad cathepsin prior art | Poor selectivity/safety | **No-go** |
| `CTSL` | Fail | Broad cathepsin prior art | Poor selectivity/safety | **No-go** |
| `SDC4` | Fail | RA/EAE biology prior art | Broad repair liability | **No-go** |
| `FMNL2` | Crohn-only partial | Rare Crohn variant prior art | Poor | **No-go** |
| `ABHD2` | Fail | Thin autoimmune prior art | Immature | **No-go** |
| `TYK2` | Strong pass | Saturated/approved drug class | Good | **Blocked positive control** |
| `JAK1/JAK2/STAT1/IRF1` | Mixed, pathway-level | Saturated pathway | Broad safety/selectivity issues | **Comparator only** |
| `MERTK` | MS-only partial | Efferocytosis/SLE/MS prior art | Direction unclear | **Hold/no-go** |
| `LGALS3` | Fail | Crowded MS/EAE/macrophage prior art | Some inhibitors | **No-go for genetics-backed novelty** |
| `FABP5` | Fail | EAE/psoriasis prior art | Some chemistry | **No-go** |
| `LTA4H` | Weak Crohn only | Leukotriene prior art | Druggable enzyme | **No-go** |

## Recommended Use Of These Candidates Going Forward

- Use `TYK2/JAK/STAT/IFN` as the positive-control genetics/perturbation axis,
  not as a discovery claim.
- Use `IFI30`, `CTSS`, `CD74`, HLA-II, `CXCL9/10`, and `IRF1/STAT1` as markers
  of the IFN-licensed antigen-processing state.
- Use `MERTK`, `LIPA`, `GPNMB`, `LGALS3`, and cathepsins as repair/debris
  clearance safety comparators.
- Do not advance `SNX10`, `C15ORF48`, `FMNL2`, `SDC4`, or `ABHD2` without
  independent genetics, cell-type localization, and perturbation evidence.

Hard final answer for Wave 11: **no claim; no-go for all current candidates as
genetics-anchored, novel cross-autoimmune intervention points.**
