# Wave93 GPR183/EBI2 Druggability Sidecar

Timestamp: 2026-05-27

Scope: independent targetability and druggability assessment for
`GPR183`/EBI2 oxysterol-niche modulation. Inputs inspected: local
`results_v3/wave74_gpr183_oxysterol_niche/`, Wave83 intervention-class
meta-rank, live ClinicalTrials.gov API, ChEMBL API, IUPHAR/GtoPdb,
PubMed/PMC/web literature, Google Patents, and attempted BindingDB access.

This is not a finding claim.

## Bottom Line

`GPR183` is **druggable but not V3-promotable**.

Final call: **BLOCKED_BY_PRIOR_ART_AND_LOCAL_UNDERANCHORING**.

The route has real GPCR pharmacology, selective antagonist chemistry, structural
biology, and active clinical development in autoimmune disease. That is exactly
why it should not be promoted as a novel V3 route. Local evidence also remains
insufficient: Wave74 parks the oxysterol-niche model because ligand production,
direct receptor expression, response biology, MS support, metabolite support,
and target-resolution genetics do not cohere across diseases.

The only defensible remaining use is comparator/stratification:

- use `GPR183`/`CH25H`/`CYP7B1`/`HSD3B7` as an oxysterol-trafficking tissue-state
  marker;
- test whether a GPR183-high UC/LN/RA-like immune-niche state predicts response
  to existing or emerging GPR183 antagonists;
- do not claim a novel autoimmune/MS therapeutic target.

## Local Evidence

Primary local file: `results_v3/wave74_gpr183_oxysterol_niche/REPORT.md`.

Wave74 integrated decision:

- Candidate: `GPR183_EBI2_oxysterol_niche`.
- Call: `PARK_GPR183_OXYSTEROL_NICHE`.
- Gate count: `5`.
- Direct `GPR183` receptor anchor: pass.
- Response module cross-disease: pass.
- Specificity versus IFN/APC generic: pass.
- MS support: fail.
- Ligand module cross-disease: fail.
- Local coherent ligand-plus-receptor-plus-response program: fail.
- Oxysterol-like metabolite support: fail.
- Target-resolved genetics or druggability anchor in local Wave62 capture: fail.
- Decision blocker: no cross-disease coherent ligand-plus-`GPR183`-plus-response
  context; no local target-resolved genetics or direct intervention/druggability
  anchor; sparse Wave66 oxysterol-like metabolite support.

Important detail: broad local modules find response-like trafficking programs
in IBD/Sjogren/T1D, but coherent contexts fail because ligand production and
`GPR183` receptor anchor do not line up in the same disease/compartment.

MS white-matter row:

- `GPR183` receptor anchor in GSE111972 MS white-matter microglia:
  mean effect `-0.136`, p `0.664`, FDR `0.744`.
- IFN/APC and APC/lysosome comparators are positive in the same MS dataset,
  so the MS failure is not due to a globally insensitive assay.

Wave83 meta-rank:

- `GPR183_EBI2_OXYSTEROL_NICHE` is top-ranked only as
  `PARK_INTERVENTION_CLASS_NEEDS_FORCING_TEST`, interestingness score `8.0`.
- Missing gates: `ms_anchor`, `genetic_or_target_resolution`,
  `source_audit_not_promotional`.
- Wave83 lists reachable modality and safety/direction as provisional passes,
  but those are not enough to overcome the local and prior-art blockers.

Interpretation: the local package supports "there is a trafficking/niche axis
worth using as a comparator," not "GPR183 is a V3-promotable target."

## Druggability Databases And Ligands

### ChEMBL

Live ChEMBL API target search for `GPR183` returned:

- Human target `CHEMBL3259470`, G-protein coupled receptor 183.
- Mouse target `CHEMBL3259471`.
- Rat target `CHEMBL4802001`.

Live ChEMBL activity query for human `CHEMBL3259470` returned `616` activity
records. Examples include:

- `CHEMBL3262896`, antagonist activity at recombinant human EBI2/GPR183 in
  CHO cells: IC50 `8.5`, `7.0`, `8.511`, and `7.079 nM` in GTPgammaS assays.
- Same molecule in human U937 cell migration: IC50 `0.3 nM` and `0.2239 nM`
  for inhibition of 7alpha,25-OHC-induced migration.
- `CHEMBL3262876`, U937 migration IC50 about `5.3 nM` / `4.898 nM`.

ChEMBL target page:
<https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3259470/>

### IUPHAR / Guide to Pharmacology

IUPHAR/GtoPdb lists `GPR183` as a class-A orphan/emerging pharmacology GPCR
with ChEMBL target `CHEMBL3259470`, UniProt `P32249`, endogenous oxysterol
ligands including `7alpha,25-dihydroxycholesterol`, and antagonist entries
including `NIBR189`.

Source:
<https://www.guidetopharmacology.org/GRAC/ObjectDisplayForward?objectId=81>

For compound 32/IPG11406-related pharmacology, GtoPdb ligand activity page
reports human GPR183 antagonism of beta-arrestin recruitment with IC50 `8.6 nM`
for PMID `38047891`:
<https://www.guidetopharmacology.org/GRAC/LigandActivityRangeVisForward?ligandId=13050>

### BindingDB

BindingDB was checked but not relied on:

- The direct SDF target download endpoint returned HTTP 500 for `GPR183`, `EBI2`,
  `IPG11406`, `NIBR189`, and `GSK682753A`.
- Web search found only generic BindingDB search pages, not a stable GPR183
  target result page.

Conclusion: lack of a usable BindingDB extraction is not evidence of absence;
ChEMBL and IUPHAR already establish ligandability.

### DrugBank / Approved-Drug Status

No approved `GPR183`/EBI2 drug was identified in this pass. The actionable
clinical drug signal is investigational IPG11406, not an approved medicine.

## Clinical Development

Live ClinicalTrials.gov API query for `GPR183`/`IPG11406` returned three
target-relevant IPG11406 records:

| NCT | title | status on 2026-05-27 | phase | condition | enrollment | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `NCT06255834` | Phase 1 Study for IPG11406 in Healthy Volunteer | Completed | Phase 1 | IBD listed in record | 66 | establishes human clinical entry |
| `NCT06717815` | Phase IIa Study for IPG11406 in Patients With Lupus Nephritis | Recruiting | Phase 1/2 | Lupus nephritis | 36 | oral IPG11406, dose cohorts |
| `NCT07535489` | Efficacy and Safety of IPG11406 in Moderately to Severely Active Ulcerative Colitis | Not yet recruiting | Phase 2 | UC | 144 | placebo-controlled UC efficacy study |

ClinicalTrials.gov links:

- <https://clinicaltrials.gov/study/NCT06255834>
- <https://clinicaltrials.gov/study/NCT06717815>
- <https://clinicaltrials.gov/study/NCT07535489>

Interpretation: the translational route is already in humans for autoimmune/
inflammatory disease. This validates druggability but blocks novelty for a V3
promotion claim.

## Medicinal Chemistry And Selectivity

Key medicinal chemistry source:

- "Discovery of a First-in-Class GPR183 Antagonist for the Potential Treatment
  of Rheumatoid Arthritis", Journal of Medicinal Chemistry, PMID `38047891`.
  <https://pubmed.ncbi.nlm.nih.gov/38047891/>
  ACS page:
  <https://pubs.acs.org/doi/abs/10.1021/acs.jmedchem.3c01364>

Hostile read:

- Chemistry is good enough: compound 32/IPG11406 is described as potent/selective,
  with improved solubility, mitigated hERG liability, good PK, and efficacy in
  collagen-induced arthritis mice.
- The paper itself frames the indication as RA/autoimmune disease. That is direct
  prior art against a broad autoimmune GPR183 antagonist claim.
- GPCR selectivity is not solved just because GPR183 potency is good. The axis is
  embedded in a class-A lipid/chemotaxis receptor landscape, and early optimization
  explicitly had to address hERG/ADMET liabilities. A V3 claim would need
  orthogonal selectivity and in-tissue pharmacodynamic evidence, not only nanomolar
  in vitro antagonism.

Additional ligand literature:

- NIBR189 and related agonist/antagonist scaffold work show that both antagonism
  and agonism are pharmacologically feasible:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC8518411/>
- Early small-molecule antagonism of oxysterol-induced EBI2 activation:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC3668520/>
- Structural biology of active 7alpha,25-OHC-bound EBI2 and inactive inverse
  agonist-bound EBI2: PMID `35537452`.
  <https://pubmed.ncbi.nlm.nih.gov/35537452/>

## Patent / Prior-Art Estate

Clean blocker:

- `WO2024208303A1`, "Compounds and their uses as GPR183 inhibitors", assigned to
  Nanjing Immunophage Biotech. Google Patents lists priority `2023-04-04`,
  publication `2024-10-10`, and explicitly states GPR183 inhibitor use in
  GPR183-mediated diseases including autoimmune diseases.
  <https://patents.google.com/patent/WO2024208303A1/en>

Additional active IP signal:

- `US11919895B2`, GPR183 antagonist family for pain, includes autoimmune-neuropathy
  language and demonstrates broader active GPR183 antagonist IP.
  <https://patents.google.com/patent/US11919895B2/en>

Interpretation: even if some legal status fields are jurisdiction-specific and
should not be overread, the published patent estate is enough to block a broad
V3 novelty claim around GPR183 antagonism for autoimmune inflammation.

## Disease Biology And Directionality

Supportive biology:

- GPR183/EBI2 senses oxysterols such as `7alpha,25-OHC` and guides immune-cell
  migration/positioning. Review:
  <https://pubmed.ncbi.nlm.nih.gov/24810762/>
- Oxysterols in intestinal immunity and inflammation describe GPR183 as an
  immune-cell oxysterol receptor controlling migration and tissue remodeling:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC7379495/>
- MS/EAE prior art: "EBI2 Is Highly Expressed in Multiple Sclerosis Lesions and
  Promotes Early CNS Migration of Encephalitogenic CD4 T Cells."
  <https://www.sciencedirect.com/science/article/pii/S2211124717300578>
- Countervailing CNS biology: EBI2 receptor regulates myelin development and
  inhibits LPC-induced demyelination, suggesting that indiscriminate antagonism
  could remove protective CNS/myelin biology:
  <https://jneuroinflammation.biomedcentral.com/articles/10.1186/s12974-017-1025-0>

Directionality conclusion:

Antagonism is the clinical and RA/UC/LN route. It is plausible for inflammatory
immune trafficking, but not clean for MS or tissue repair. In MS, GPR183 may
promote encephalitogenic T-cell migration yet also participate in myelin biology.
This creates a compartment-specific directionality problem: peripheral immune
trafficking blockade could help, while CNS/local receptor blockade could be
harmful or neutral.

## Tissue Delivery And PD Feasibility

Peripheral autoimmune tissue:

- Oral IPG11406 makes gut, blood, lymphoid, and kidney immune-cell targeting
  plausible. UC and lupus nephritis trials are the best current translational
  contexts.

CNS/MS:

- Current public IPG11406 literature does not establish a CNS-penetrant MS drug.
- The ACS abstract/search snippet notes compound 32 was not highly BBB penetrable
  in a brain-target context. Even if peripheral immune trafficking is sufficient
  for relapsing inflammation, a V3 MS/white-matter claim needs lesion/CNS PD or
  immune-trafficking pharmacodynamics.
- Local MS evidence fails: `GPR183` is not positive in the MS white-matter
  microglia dataset, whereas IFN/APC and APC/lysosome comparators are.

Practical PD markers if used only as comparator:

- blood and tissue B/T/DC positioning markers;
- `CH25H`/`CYP7B1`/`HSD3B7` ligand-production module;
- `CCR7`/`CCL19`/`CCL21`/`CXCL13` trafficking module;
- tissue oxysterol measurements, especially `7alpha,25-OHC`/related species.

## Safety Liabilities

Primary safety concern: immune trafficking is normal host defense, not just
pathology.

Known biology implies risks in:

- B-cell positioning, germinal-center dynamics, antibody responses, and vaccine
  quality;
- T-cell and DC migration in inflamed tissue;
- mucosal immune organization and IgA/plasma-cell biology;
- infection surveillance and viral-response contexts, including EBV-linked
  nomenclature/history;
- possible CNS/myelin biology if antagonist exposure reaches relevant compartments.

The key distinction from a generic anti-inflammatory is that GPR183 controls
cell positioning. Chronic blockade could alter where immune cells go, not merely
how activated they are. That can be useful in UC/LN trials, but it is not a
low-risk V3 repair mechanism.

## Blockers

Hard blockers:

- **Clinical prior art:** IPG11406 is already in Phase 1/2 lupus nephritis and
  Phase 2 UC, with Phase 1 completed.
- **Patent prior art:** published GPR183 inhibitor patent estate covers autoimmune
  disease.
- **Disease-literature prior art:** RA antagonist optimization, IBD antagonist
  discovery, and MS/EAE immune-trafficking literature are public.
- **Local MS failure:** no MS white-matter support for the receptor/niche module.
- **No coherent local niche:** ligand enzymes, receptor anchor, and response module
  do not align cross-disease in the same cell-state contexts.
- **No local target-resolution genetics:** Wave74/Wave62 report no relevant QTL
  colocalization and only weak/limited L2G disease support.

Soft but important blockers:

- CNS delivery/PD unresolved for an MS claim.
- Antagonism direction may conflict with protective myelin/CNS biology.
- Immune-trafficking safety risk is mechanism-intrinsic.
- GPCR/hERG/selectivity liabilities are improved for IPG11406 but remain a class
  issue for new chemotypes.

## Remaining Route

No V3-promotable therapeutic route remains from the current package.

Allowed residual uses:

- **Comparator:** use IPG11406/GPR183 as a positive control for "druggable but
  prior-arted immune-trafficking GPCR."
- **Stratification hypothesis:** test whether a `GPR183` oxysterol-niche score
  identifies UC/LN/RA tissue subsets likely to respond to existing GPR183 antagonism.
- **MS falsification only:** require CNS/lesion PD, direct immune-trafficking
  evidence, and a direction-safe compartment model before reopening.

Rejected V3 claim:

- "GPR183 antagonism is a novel cross-autoimmune/MS lipid-lysosomal myeloid target."

That claim is blocked by prior art and not supported by local target-level evidence.

## Source Pointers

Local:

- `results_v3/wave74_gpr183_oxysterol_niche/REPORT.md`
- `results_v3/wave74_gpr183_oxysterol_niche/integrated_decision.tsv`
- `results_v3/wave74_gpr183_oxysterol_niche/external_target_evidence.tsv`
- `results_v3/wave83_intervention_class_meta_rank/REPORT.md`
- `results_v3/wave83_intervention_class_meta_rank/intervention_class_meta_rank.tsv`
- `subagents_v3/wave74c_prior_art_druggability_scout.md`

External:

- ChEMBL GPR183: <https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3259470/>
- IUPHAR/GtoPdb GPR183: <https://www.guidetopharmacology.org/GRAC/ObjectDisplayForward?objectId=81>
- IPG11406 Phase 1: <https://clinicaltrials.gov/study/NCT06255834>
- IPG11406 lupus nephritis: <https://clinicaltrials.gov/study/NCT06717815>
- IPG11406 UC: <https://clinicaltrials.gov/study/NCT07535489>
- RA antagonist medicinal chemistry: <https://pubmed.ncbi.nlm.nih.gov/38047891/>
- GPR183 inhibitor patent: <https://patents.google.com/patent/WO2024208303A1/en>
- GPR183 pain/antagonist patent: <https://patents.google.com/patent/US11919895B2/en>
- EBI2/GPR183 structure: <https://pubmed.ncbi.nlm.nih.gov/35537452/>
- Oxysterol/EBI2 immune regulation review: <https://pubmed.ncbi.nlm.nih.gov/24810762/>
- Oxysterols in intestinal immunity: <https://pmc.ncbi.nlm.nih.gov/articles/PMC7379495/>
- MS lesion/T-cell migration paper: <https://www.sciencedirect.com/science/article/pii/S2211124717300578>
- Myelin/demyelination counterpoint: <https://jneuroinflammation.biomedcentral.com/articles/10.1186/s12974-017-1025-0>
- Small-molecule EBI2 antagonism: <https://pmc.ncbi.nlm.nih.gov/articles/PMC3668520/>
- GPR183 agonist/antagonist scaffold work: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8518411/>

