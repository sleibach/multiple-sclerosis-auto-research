# Wave99 Sidecar Audit: CASP4 as C15ORF48/MOCCI Upstream Danger Stress-Generator

Timestamp: 2026-05-27 CEST

Scope: sidecar audit only. I do not claim a finding. I audited `CASP4` as a
possible upstream danger/pyroptosis stress-generator for the C15ORF48/MOCCI
state, with focus on prior art, trials, patents, druggability/selectivity,
cross-autoimmune translational feasibility, and the decisive wet-lab test.

## Bottom Line

`CASP4` should remain a **PARK/NO-GO therapeutic nomination** in the V3 session.
It is biologically plausible as an upstream inflammatory stress node that could
induce a compensatory `C15ORF48`/MOCCI state, but it is not cleanly promotable:
the local MS anchor is weak, the local C15 co-state is not causality, no real
perturbation edge was found locally, CASP4-only selectivity is difficult against
CASP5/CASP1 biology, and 2025-2026 public prior art now directly frames
CASP4/5 as druggable inflammatory targets in IBD and related inflammatory
diseases.

The only novelty-open fragment is **C15ORF48-high stratification of CASP4/5
biology**, not CASP4/5 inhibition itself. That should be treated as a wet-lab
ordering/biomarker hypothesis, not a target claim.

## Local Evidence Checked

Local files read or queried:

- `results_v3/wave97_c15_residual_costate_falsification/residual_costate_candidate_summary.tsv`
- `results_v3/wave98_c15_successor_perturbation_first_audit/c15_successor_perturbation_first_rank.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/integrated_gene_target_rank.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/adjusted_top_gene_ols.tsv`
- `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
- `subagents_v3/wave97_c15_prior_art_sidecar.md`
- `subagents_v3/wave97_c15_directionality_sidecar.md`

Local quantitative facts:

| Evidence layer | CASP4 result | Audit interpretation |
| --- | --- | --- |
| MS white matter, `GSE111972` | delta log2 `+0.2067`, p `0.4927`, FDR `0.9272` | No MS expression anchor. |
| Broad cross-disease gate | raw positive in Crohn myeloid, UC myeloid, psoriasis APC, T1D acinar, T1D ductal; retained positive disease count `4`; strict core-covariate residual disease count `0` | Broad inflammation signal, not covariate-resistant central node. |
| C15 residual co-state, Wave97 | residual case-positive contexts `3`, disease count `2`, median residual case r `0.3084`; best context T1D stellate r `0.8867`; Wave97 call `PARK_RESIDUAL_COSTATE_WITH_MODALITY` | Survives as C15-adjacent state marker, but only two diseases and not causal. |
| Anti-TNF response, `GSE282122` Wave68 | Mono/macro remission-adjusted delta `-0.7246`, p `0.0105`, FDR `0.0281` | CASP4 falls with remission after adjustment; supportive for inflammatory burden reduction, not target causality. |
| Foundation/perturbation rescue, Wave18 | `do_not_promote`; total support contexts `2`, strong support contexts `0` | No model support strong enough for promotion. |
| Wave98 integrated call | `NO_GO_CLOSE_PRIOR_OR_SAFETY_BLOCKED` | Consistent with this audit. |

Raw query traces saved:

- `subagents_v3/raw_casp4_sidecar_pubmed_queries.json`
- `subagents_v3/raw_casp4_sidecar_clinicaltrials_queries.json`
- `subagents_v3/raw_casp4_sidecar_chembl_targets.json`
- `subagents_v3/raw_casp4_sidecar_chembl_activity_summary.json`

## External Search Methods

Databases and sources queried:

- PubMed via NCBI E-utilities
- Web/PubMed/PMC/Nature/ClinicalTrials.gov/ChEMBL
- ClinicalTrials.gov API v2
- Google-indexed patent sources: WIPO Patentscope, Justia Patents, Google
  Patents search results, Ventus public pipeline pages

Queries run:

- PubMed: `("CASP4" OR "caspase-4") AND ("C15ORF48" OR "MOCCI")`
- PubMed: `("CASP4" OR "caspase-4" OR "caspase 4") AND ("multiple sclerosis" OR "experimental autoimmune encephalomyelitis" OR EAE)`
- PubMed: `("CASP4" OR "caspase-4") AND autoimmune`
- PubMed: `("CASP4" OR "caspase-4") AND ("inflammatory bowel disease" OR Crohn OR colitis)`
- Web: `CASP4 C15ORF48 MOCCI`, `caspase-4 C15ORF48`, `CASP4 autoimmune disease inflammatory caspase inhibitor patent`
- Patents: `WO2026055444 caspase-4 inhibitors uses thereof`, `caspase-4 inhibitors and uses thereof patent`, `CASP4 Google Patents inhibitor`
- Trials: `CASP4`, `caspase-4`, `caspase 4`, `caspase inhibitor autoimmune`, `caspase inhibitor multiple sclerosis`
- ChEMBL: target searches for `CASP4`, `CASP1`, `CASP5`, then activity overlap by molecule.

## 1. Direct Prior Art and IDs

### CASP4/CASP11 in MS/EAE and Neuroinflammation

- PMID `11136825`, PMCID `PMC2195881`, DOI `10.1084/jem.193.1.111`:
  `Caspase-11 mediates oligodendrocyte cell death and pathogenesis of
  autoimmune-mediated demyelination`. This is mouse caspase-11/EAE, not human
  CASP4 in MS, but it is close mechanistic prior art because mouse caspase-11
  is the noncanonical inflammatory-caspase axis related to human CASP4/5.
- PMID `34044393`, DOI `10.1159/000516064`: `Caspase-11 Noncanonical
  Inflammasome: A Novel Key Player in Murine Models of Neuroinflammation and
  Multiple Sclerosis`. This review explicitly connects mouse caspase-11 and
  human CASP4/5 noncanonical inflammasomes, while noting that human CASP4/5 MS
  evidence remained underdeveloped at that time.
- PubMed ESearch for CASP4/caspase-4 plus MS/EAE returned 8 records. The
  relevant direct records are mostly mouse CASP11 or bioinformatic/pyroptosis
  work rather than human CASP4 causal experiments.

Audit consequence: the broad idea "noncanonical inflammatory caspase inhibition
for MS/EAE" is not novel. A human-CASP4-specific MS stratification might still
be less explored, but the translational anchor is weak.

### CASP4/5 as Druggable Inflammatory Targets

- PMID `40044809`, DOI `10.1038/s41577-025-01142-9`: `New insights into the
  noncanonical inflammasome point to caspase-4 as a druggable target` (Nature
  Reviews Immunology, 2025). This review frames CASP4 as druggable, discusses
  IL-18/GSDMD biology, structural exosite/allosteric opportunity, and lists MS
  as one human-disease relevance path by mouse EAE evidence.
- Ventus VENT-04 public pipeline page: `VENT-04` is described as an oral,
  small-molecule, allosteric inhibitor of caspase-4 and caspase-5, developed
  for IBD and other barrier/inflammatory diseases. The page states preclinical
  protection from gut barrier disruption and inhibition of IL-18 plus downstream
  inflammatory effectors including TNF-alpha, LCN2, and OSM.
- Ventus 2025 press release on the Nature Reviews Immunology review states that
  Ventus identified potent selective small molecules inhibiting caspase-4/5 via
  an allosteric mechanism and frames CASP4/5 as targets across IBD,
  hidradenitis suppurativa, sepsis, and other inflammatory diseases.

Audit consequence: CASP4/5 inhibition in autoimmune/barrier inflammatory
disease is already an active translational program. Any V3 claim must avoid
presenting CASP4/5 inhibition as novel.

### Patents

- `WO2026055444`, `CASPASE-4 INHIBITORS AND USES THEREOF`, WIPO Patentscope:
  publication date `2026-03-12`, international application
  `PCT/US2025/045061`. Search-result text states compounds of Formula I,
  methods of preparation, treatment/prevention of CASP4-mediated diseases, and
  pharmaceutical compositions.
- Justia `US20230250067A1`, `Caspase inhibitors and methods of use thereof`:
  broad methods around caspase-1, caspase-4 and/or caspase-5. The patent text
  explicitly lists autoimmune/inflammatory/CNS categories and examples
  including IBD/UC/Crohn's disease, MS, T1D, lupus nephritis, psoriasis, RA,
  gout, and other conditions.
- Histogen/Conatus-style inflammatory caspase patent family: `US11579703`
  reported as `Caspase Inhibitors and Methods of Use Thereof`, including
  CTS-2090 and oral activity in a UC model. This is not CASP4-only but blocks
  broad novelty around inflammatory caspase inhibitors for IBD/autoimmunity.

Audit consequence: there is broad blocking prior art for inflammatory caspase
inhibition in autoimmune, CNS, IBD, dermatologic, rheumatologic, kidney, and
metabolic inflammatory indications. C15-high stratification is the only narrow
delta found.

### Clinical Trials

ClinicalTrials.gov API results:

- `CASP4`: 3 records returned; none autoimmune/MS CASP4-inhibitor trials.
  Records included sepsis/liver injury, COPD inflammatory response, and an
  observational severe-sepsis inflammasome-monocyte study.
- `caspase-4`: 2 records returned; same sepsis-related space.
- `caspase inhibitor autoimmune`: 1 record, `NCT01653899`, `Caspase Inhibition
  in Islet Transplantation`, intervention `IDN-6556`.
- `caspase inhibitor multiple sclerosis`: 0 records returned.

Audit consequence: clinical CASP4-specific autoimmune/MS intervention is not
yet established in trial registries, but preclinical/patent/company prior art is
sufficiently strong to block novelty of a generic CASP4/5 therapeutic claim.

## 2. Druggability and Selectivity Feasibility

### Target Biology

CASP4 is an intracellular inflammatory cysteine protease. It directly senses
cytosolic LPS via its CARD, activates the noncanonical inflammasome, cleaves
GSDMD, can activate IL-18 directly, and can secondarily engage NLRP3/CASP1
outputs. This makes it enzymatically druggable but safety-sensitive.

### ChEMBL Evidence

ChEMBL target IDs:

- Human CASP4: `CHEMBL2226`
- Human CASP1: `CHEMBL4801`
- Human CASP5: `CHEMBL3131`

ChEMBL activity counts queried locally:

- CASP4: 89 activity rows, 60 potency rows
- CASP1: 6,459 activity rows total; first 1,000 fetched, 701 potency rows in
  fetched page
- CASP5: 177 activity rows, 104 potency rows

Cross-target activity examples from local ChEMBL API:

| Molecule | CASP4 potency | Comparator potency | Interpretation |
| --- | --- | --- | --- |
| `CHEMBL3949842` | CASP4 Ki `8 nM`; IC50 `21 nM` | CASP5 Ki `16 nM`; IC50 `71 nM` | Potent inflammatory-caspase inhibitor, but not CASP4-only. |
| `CHEMBL366927` | CASP4 IC50 `300 nM` | CASP1 IC50 `50 nM`; CASP5 IC50 `200 nM` | More potent on CASP1/CASP5 than CASP4. |
| `CHEMBL2323966` | CASP4 IC50 `90 nM` | CASP5 IC50 `560 nM` | Some CASP4-over-CASP5 window, but no CASP1 row in fetched overlap. |
| `CHEMBL3898379` | CASP4 Ki `248 nM`; IC50 `670 nM` | CASP5 Ki `81 nM`; IC50 `350 nM` | CASP5 stronger than CASP4. |

### Selectivity Call

- CASP4/5 dual inhibition is feasible and now externally validated as a
  development direction by Ventus.
- CASP4-only inhibition is **not** currently a strong translational assumption.
  CASP4 and CASP5 are closely related, share noncanonical inflammasome
  substrates, and ChEMBL overlap shows many compounds are dual or even stronger
  on CASP5/CASP1.
- CASP1 sparing is critical if the claim is specific noncanonical inflammasome
  biology rather than pan-inflammatory caspase suppression. Active-site peptide
  inhibitors are unlikely to supply enough selectivity; allosteric/exosite
  approaches are more plausible.
- Selectivity against apoptotic caspases may be feasible; selectivity within
  inflammatory caspases is the hard part.

## 3. Could C15-High Stratified Autoimmune Use Be Novel?

### Search Result

Searches for `CASP4 C15ORF48`, `caspase-4 C15ORF48`, `CASP4 MOCCI`, and
`caspase-4 MOCCI` found no direct CASP4-C15ORF48/MOCCI therapeutic framing.
PubMed ESearch for `("CASP4" OR "caspase-4") AND ("C15ORF48" OR "MOCCI")`
returned `0` records.

### Novelty Assessment

Potentially novel:

- Using `C15ORF48`/MOCCI-high cell state as a **biomarker to order or stratify
  CASP4/5 noncanonical inflammasome activity**.
- Testing whether CASP4 activation is upstream of C15ORF48/MOCCI induction in
  human autoimmune myeloid, epithelial, endothelial, or glia-like cells.
- In MS specifically, a `C15ORF48`-high chronic active lesion-rim stratum with
  CASP4/5 activation could be novel if validated spatially in human lesions.

Not novel or likely blocked:

- CASP4/5 inhibition as a treatment for IBD or barrier-inflammation.
- Broad CASP1/4/5 inhibition for autoimmune, CNS, MS, IBD, T1D, psoriasis, RA,
  lupus-nephritis-like kidney inflammation, or similar conditions.
- General pyroptosis/inflammasome inhibition in autoimmune disease.

Practical call: C15-high stratification is a **possible biomarker delta**, not a
freedom-to-operate claim and not a target nomination. It could strengthen a
trial-enrichment rationale only after wet-lab ordering and spatial validation.

## 4. Translational Feasibility Across MS and Autoimmune Disease

| Disease context | Feasibility | Reason |
| --- | --- | --- |
| IBD, especially UC/Crohn's nonresponders with barrier dysfunction | Highest external feasibility but novelty crowded | Ventus explicitly targets CASP4/5 in IBD and links to barrier dysfunction, IL-18, TNF, LCN2, OSM. |
| Hidradenitis suppurativa/severe asthma/COPD | Plausible but prior-art crowded | Ventus frames these as CASP4/5-relevant inflammatory/barrier diseases. |
| MS | Low current feasibility | Mouse CASP11/EAE prior is close, but local human MS expression anchor is null and CNS penetration/selective CNS target engagement is unresolved. |
| T1D | Mechanistically possible in pancreatic tissue contexts | Local C15/CASP4 co-state appears in T1D tissue-resident contexts, but genetics/perturbation and trial route are absent. |
| SLE/RA/psoriasis | Generic inflammasome/pyroptosis plausibility | Broad autoimmune prior art and weak CASP4-specific causal anchoring make these poor lead indications. |

Lead indication if forced: IBD has the best biological and delivery logic, but
it is already externally occupied. For novelty, MS C15-high lesion-rim biology
is less crowded but currently too weak for development.

Known failure modes:

- Infection/barrier defense liability from blocking cytosolic LPS sensing and
  pyroptosis.
- CASP5/CASP1 overlap confounding efficacy and toxicity.
- Human/mouse translation mismatch: mouse CASP11 is not a one-to-one surrogate
  for human CASP4/5.
- High `CASP4` may be a marker of IFN/TLR/generic inflammation, not a driver.
- `C15ORF48` may be a compensatory brake; reducing CASP4 might reduce the
  trigger and the readout, but that does not prove therapeutic benefit.
- MS requires CNS exposure or peripheral effect strong enough to affect CNS
  lesions; neither is established for the CASP4/5 route here.

## 5. Decisive Wet-Lab Perturbation Test

### Question

Does CASP4 activation causally induce the C15ORF48/MOCCI state, and does
CASP4/5 inhibition reduce pathogenic inflammatory output in C15-high autoimmune
cells without collapsing protective host-defense biology?

### System

Primary human donor cells plus disease-relevant validation:

1. CD14+ monocyte-derived macrophages from `n = 8` healthy donors and `n = 8`
   autoimmune donors if available, paired within donor.
2. Optional tissue validation in colon organoid-immune co-culture for IBD and
   iPSC microglia or human postmortem MS lesion-derived myeloid cultures if
   available.

Stimuli:

- IFN-gamma priming plus cytosolic LPS transfection or Gram-negative outer
  membrane vesicles to activate CASP4.
- Matched TNF/IL-1beta stimulation controls to induce inflammatory C15ORF48
  without direct cytosolic-LPS CASP4 activation.

Perturbations:

- CRISPRi or siRNA: `CASP4`, `CASP5`, `CASP1`, dual `CASP4/CASP5`, non-targeting
  control.
- Pharmacology: tool CASP4/5 inhibitor if available; active-site peptide tool
  only as assay control; allosteric CASP4/5 compound if accessible through
  collaboration.
- Rescue: wild-type CASP4 and catalytically inactive CASP4 rescue; if feasible,
  inhibitor-resistant CASP4 rescue.

Readouts at 2, 6, 12, and 24 hours:

- `C15ORF48` mRNA and MOCCI protein.
- `NDUFA4` protein displacement or expression change.
- CASP4/CASP5/CASP1 cleavage/activation.
- GSDMD cleavage, LDH/PI uptake pyroptosis, mature IL-18, IL-1beta, HMGB1.
- OSM, TNF, LCN2, CXCL8, CCL20, IL23A.
- Mitochondrial respiration/ECAR, mtROS, and cell viability.
- Optional scRNA-seq/CITE-seq to test whether the C15-high state is specifically
  suppressed or merely shifts cell composition.

### Expected Positive Result

A CASP4-upstream model survives only if, under cytosolic-LPS/OMV conditions:

- `CASP4` knockdown/inhibition reduces C15ORF48/MOCCI induction by at least
  `30-40%` versus paired control while preserving viability above `80%`.
- It reduces CASP4 pathway output by at least `50%` for GSDMD cleavage and
  mature IL-18.
- The effect is stronger for `CASP4` or `CASP4/CASP5` perturbation than for
  `CASP1` perturbation.
- TNF/IL-1beta-only induction of C15ORF48 is not equivalently blocked, showing
  the effect is CASP4-pathway-specific rather than generic transcriptional
  suppression.
- Genetic perturbation and pharmacologic inhibition agree in direction.

### Falsification Criteria

The CASP4-C15 upstream hypothesis should be rejected if any of the following
occur in a paired mixed-effects analysis:

- `CASP4` knockdown/inhibition changes C15ORF48/MOCCI by less than `15%` while
  strongly reducing GSDMD/IL-18. Interpretation: CASP4 drives pyroptosis but not
  the C15 state.
- C15ORF48 induction persists after dual `CASP4/CASP5` perturbation and is
  instead explained by TNF/IL-1beta/IFN generic inflammatory signaling.
- CASP1 perturbation explains the C15 or cytokine phenotype as well as or
  better than CASP4/CASP5.
- Pharmacologic effects persist in CASP4-null cells. Interpretation: off-target
  or pan-caspase artifact.
- In C15-high disease-derived cultures, CASP4/5 inhibition reduces viability or
  barrier function more than it improves inflammatory output.

Stop-loss: after `n = 8` paired donors, if median C15ORF48 reduction under
genetic CASP4 perturbation is below `15%` and the 95% bootstrap CI excludes a
`30%` reduction, stop the C15-CASP4 branch. Do not rescue with broader
transcriptomic associations.

## Audit Verdict

`CASP4` is a useful mechanistic comparator and wet-lab ordering target for the
C15ORF48/MOCCI branch, especially because anti-TNF remission data and residual
C15 co-state point in the expected direction. It is not a V3 therapeutic target
nomination. If the orchestrator continues this branch, the defensible next step
is not more association mining; it is the perturbation test above, with CASP4,
CASP5, and CASP1 explicitly separated.

## Source Links Used

- PubMed PMID `11136825`: https://pubmed.ncbi.nlm.nih.gov/11136825/
- Karger review PMID `34044393`: https://karger.com/nim/article/28/4/195/825442/Caspase-11-Noncanonical-Inflammasome-A-Novel-Key
- Nature Reviews Immunology CASP4 druggable target review: https://www.nature.com/articles/s41577-025-01142-9
- PMC mirror of the CASP4 druggable target review: https://pmc.ncbi.nlm.nih.gov/articles/PMC12704549/
- Ventus VENT-04 pipeline page: https://www.ventustx.com/pipeline/vent-04/
- Ventus 2025 CASP4/5 announcement: https://www.ventustx.com/ventus-therapeutics-announces-nature-reviews-immunology-publication-demonstrating-the-promise-of-caspase-4-5-as-therapeutic-targets/
- WIPO Patentscope `WO2026055444`: https://patentscope.wipo.int/search/pt/detail.jsf?_gid=202611&docId=WO2026055444
- Justia `US20230250067A1`: https://patents.justia.com/patent/20230250067
- ClinicalTrials.gov API: https://clinicaltrials.gov/api/v2/studies
- ChEMBL API: https://www.ebi.ac.uk/chembl/api/data/
