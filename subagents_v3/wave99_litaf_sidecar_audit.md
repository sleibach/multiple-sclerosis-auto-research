# Wave99 Sidecar Audit: LITAF

Timestamp: 2026-05-27 Europe/Berlin

Scope: LITAF as a possible upstream inflammatory stress-generator for the
C15ORF48/MOCCI state. This is an audit only. It does not claim a finding.

## Verdict

`LITAF` should remain a perturbation-ordering hypothesis and biomarker-adjacent
stress-generator, not a therapeutic target nomination.

Reason: the local V3 data support residual C15ORF48 co-state and anti-TNF
remission-direction compatibility, but do not provide an MS-strict anchor,
validated LITAF -> C15ORF48 perturbation direction, cross-disease genetic
causality, or a selective modality. External evidence reinforces this: LITAF is
published as a TNF/LPS/endosomal inflammatory regulator, with direct IBD and
murine inflammatory-arthritis evidence, but existing chemical matter is broad
TNF/PDE4/kava-axis anti-inflammatory chemistry rather than selective LITAF
pharmacology.

## Local V3 Evidence Trace

Source files:

- `results_v3/wave97_c15_residual_costate_falsification/REPORT.md`
- `results_v3/wave98_c15_successor_perturbation_first_audit/REPORT.md`
- `results_v3/wave98_c15_successor_perturbation_first_audit/c15_successor_perturbation_first_rank.tsv`

Key local values:

| Metric | LITAF value |
| --- | ---: |
| Wave97 residual C15 co-state positive diseases | 3 |
| Wave97 median residual case correlation | 0.4155 |
| MS white-matter delta | 0.3084 |
| MS p value | 0.1716 |
| Anti-TNF remission adjusted delta, mono/macrophage | -0.4507 |
| Anti-TNF remission adjusted FDR | 0.03313 |
| Wave37 perturbation screen call | UNRESOLVED |
| Wave37 contrast FDR | 0.9971 |
| ChEMBL activity count in local Wave98 table | 0 |
| Wave98 call | PARK_PERTURBATION_ORDERING_REQUIRED |

Interpretation: LITAF is coherent as an upstream inflammatory-stress marker, but
fails the required target gates: no strict MS effect, no direct perturbation
ordering, no selective modality, no model perturbation direction, and no
cross-disease genetic support.

## Search Log

Databases queried:

- PubMed via NCBI E-utilities.
- Europe PMC REST search.
- ClinicalTrials.gov API v2.
- Google Patents and Justia Patents; Google Patents pages include Espacenet
  outbound records for the patent families checked.
- ChEMBL REST API.
- UniProt REST API.
- Open Targets Platform GraphQL API.
- AlphaFold DB API.
- Web full-text/preprint search for `site:biorxiv.org` and `site:medrxiv.org`
  LITAF queries.

Disease query terms:

- `LITAF multiple sclerosis`
- `LITAF rheumatoid arthritis`
- `LITAF lupus OR LITAF SLE`
- `LITAF inflammatory bowel disease OR LITAF Crohn OR LITAF ulcerative colitis`
- `LITAF psoriasis`
- `LITAF type 1 diabetes`
- `LITAF Sjogren`
- `LITAF ankylosing spondylitis`
- `LITAF myasthenia gravis`
- `LITAF autoimmune thyroid OR LITAF Hashimoto OR LITAF Graves`
- `LITAF celiac`
- `LITAF primary biliary cholangitis OR LITAF primary biliary cirrhosis`
- `LITAF inhibitor OR LITAF small molecule OR LITAF antibody`
- `Kava-241 LITAF arthritis`
- `kavain LITAF arthritis`

## Direct Prior Art and IDs

### Core LITAF Biology

| Finding | Source |
| --- | --- |
| LITAF was cloned as an LPS-induced transcription factor regulating TNF-alpha expression. | PMID: 10200294, DOI: 10.1073/pnas.96.8.4518 |
| Macrophage-specific LITAF-deficient mice have reduced LPS-induced cytokines and increased resistance to LPS lethality. | PMID: 16954198, DOI: 10.1073/pnas.0605988103 |
| Whole-body inducible LITAF deletion improves experimental endotoxic shock and inflammatory arthritis. | PMID: 22160695, DOI: 10.1073/pnas.1111492108 |
| LITAF/SIMPLE functions with ESCRT machinery in endosomal trafficking. | PMID: 23166352, DOI: 10.1128/MCB.05770-11 |

### Disease-Specific Prior Art

| Disease | Direct LITAF evidence found | Interpretation |
| --- | --- | --- |
| Multiple sclerosis | PMID: 23319192 reports CMT1C due LITAF coexisting with progressive MS in a family. No evidence that LITAF is an MS therapeutic target. | Not target prior art; safety/context only. |
| Rheumatoid arthritis | PMID: 22160695: LITAF deletion improves murine inflammatory arthritis. PMID: 29914930: Kava-241 reduces articular/systemic inflammation in a P. gingivalis-induced arthritis model. Google Patent `US11767283B2` claims kava analog anti-inflammatory compounds for infective/rheumatoid arthritis and states Kava-241 reduced LITAF in macrophages. | Direct RA/inflammatory-arthritis prior art; blocks novelty for a simple "inhibit LITAF/TNF in RA" claim. |
| Systemic lupus erythematosus | PubMed/Europe PMC exact LITAF lupus/SLE searches returned no direct target paper. | No support. |
| Crohn's disease / ulcerative colitis | PMID: 16804395 reports increased LITAF in CD/UC intestinal tissues. PMID: 21984950 reports LITAF mediation of increased TNF-alpha secretion from inflamed colonic lamina propria macrophages. Open Targets associates LITAF with IBD, Crohn's disease, and ulcerative colitis, driven mainly by genetic/literature channels. | Real IBD biology, but as TNF/LPS macrophage mechanism; not selective therapeutic proof. |
| Psoriasis | PMID: 26634547 reports LITAF/HHEX/DUSP1 expression in mesenchymal stem cells from psoriasis patients. | Expression/biomarker-level only. |
| Type 1 diabetes | PubMed hits were diabetes-retina transcriptomic context, not autoimmune-islet LITAF target biology. | No target support. |
| Sjogren's syndrome | No direct PubMed/Europe PMC hits. | No support. |
| Ankylosing spondylitis | No direct PubMed/Europe PMC hits. | No support. |
| Myasthenia gravis | No direct PubMed/Europe PMC hits. | No support. |
| Autoimmune thyroid disease | No direct autoimmune-thyroid LITAF hits; broad thyroid text hits were not disease-target evidence. | No support. |
| Celiac disease | No direct PubMed/Europe PMC hits. | No support. |
| Primary biliary cholangitis | No direct PubMed/Europe PMC hits. | No support. |

### Patent and Trial Prior Art

| ID | What it covers | Relevance |
| --- | --- | --- |
| `US11767283B2`, Google Patents / Justia Patents | Synthetic kava analog anti-inflammatory compounds, including Kava-241 and Kava-205Me, for periodontitis and infective/rheumatoid arthritis; patent text states macrophage Kava-241 exposure reduced TLR2/4, MAPK elements, LITAF, and TNF-alpha. | Direct prior art for LITAF-adjacent kava analog suppression in RA-like inflammatory arthritis. |
| `US20200010396A1` / `US20230382840A1` | Related kava analog applications. | Same family/continuation space. |
| `US10085990B2` | Tricyclic compounds as TNF-alpha synthesis modulators and PDE4 inhibitors; claims include inflammatory diseases such as psoriasis, RA, UC, Crohn's, and MS. | Adjacent broad TNF/PDE4 prior art; not direct LITAF-targeted prior art. |
| ClinicalTrials.gov exact `LITAF`, `Kava-241`, `I-BC-241`, `Kava-205Me`, `kavain autoimmune`, `LITAF Kava` | No LITAF-directed autoimmune interventional trial found. A loose `LITAF` query returned `NCT05490862`, an obesity/monocyte activation study whose outcome text includes "lipopolysaccharide-induced tumor necrosis factor-alpha"; it is not a LITAF-targeted autoimmune trial. | No clinical target validation. |

## Druggability and Selective Modality

Conclusion: no selective LITAF modality is ready.

Evidence:

- UniProt `Q99732` describes LITAF as a small lysosome/late-endosome protein
  with nuclear/cytokine-regulatory and endosomal-trafficking functions, plus
  CMT1C variants.
- Open Targets target `ENSG00000189067` has no approved, advanced clinical, or
  phase 1 modality flags for small molecules, antibodies, protein degraders, or
  oligonucleotides. It reports no high-quality ligand, no high-quality pocket,
  and no druggable-family flag.
- AlphaFold DB `AF-Q99732-F1` model v6: 161 residues; mean pLDDT from downloaded
  PDB B-factors was 69.58. The N-terminal 1-70 region was low-confidence
  (mean pLDDT 47.8), while residues 71-161 were higher confidence. This
  supports structural caution, not a pocketable target nomination.
- ChEMBL target search returns `CHEMBL6066581` for LITAF. ChEMBL currently lists
  62 IC50 activity rows from patent document `CHEMBL5725733` / `US10085990B2`,
  but the assay description is TNF ELISA and the patent title is TNF synthesis
  modulation plus PDE4 inhibition. This is not adequate evidence of selective
  direct LITAF binding or LITAF-family selectivity.
- Kava/kava-analog literature and patent matter are functional anti-inflammatory
  modulators. They affect LITAF/TNF/MAPK/TLR readouts but are not validated as
  selective LITAF ligands.

Modality audit:

| Modality | Status |
| --- | --- |
| Small molecule inhibitor | Not ready. Existing compounds are broad TNF/PDE4/kava-axis modulators, not selective LITAF ligands. |
| Antibody | Poor fit. LITAF is primarily intracellular/endosomal/lysosomal with no clean extracellular target epitope for standard antibodies. |
| PROTAC / molecular glue | Theoretically possible only after discovering a selective binder. No such binder verified. |
| ASO / siRNA | Technically possible, but delivery to lesion/synovial/gut macrophages and peripheral-nerve safety are unresolved. |
| CRISPR/editing | Research perturbation only. Not translationally plausible for broad autoimmune indications at present. |

## Target Versus Biomarker

LITAF is biomarker/ordering-hypothesis only in this program.

Why not a target:

1. Local evidence lacks strict MS anchoring and perturbation causality.
2. External evidence is strongest for generic LPS/TNF biology and IBD/RA
   inflammatory contexts, not for a disease-selective causal autoimmune node.
3. Direct systemic LITAF modulation has peripheral-nerve liability concern
   because pathogenic LITAF/SIMPLE variants cause CMT1C.
4. No selective chemical matter or biologic modality is available.
5. Prior art already covers the obvious RA/TNF/kava/LITAF-adjacent route.

What LITAF can still be used for:

- A readout of LPS/TLR/TNF inflammatory stress.
- A stratification or mechanistic-ordering marker in C15ORF48/MOCCI experiments.
- A positive-control upstream inflammatory-stress perturbation in macrophage
  systems.

## Decisive Wet-Lab Perturbation Test

Question: does LITAF sit upstream of the C15ORF48/MOCCI state, or is it merely a
co-induced inflammatory-stress marker?

Design:

- Cells: primary human CD14+ monocyte-derived macrophages from healthy donors
  plus disease donors where tissue access is feasible: RA synovial macrophages,
  IBD lamina propria macrophages, and MS monocyte-derived macrophages as a
  practical peripheral proxy. Use sorted tissue macrophages where available for
  confirmatory work.
- Pilot sample size: 8 donors per disease context plus 8 healthy donors, paired
  within donor across perturbations. Confirmatory stage: 20 donors in the best
  disease context only.
- Perturbations:
  - non-targeting CRISPRi or siRNA control;
  - LITAF knockdown with at least two independent guides/siRNAs;
  - LITAF knockdown plus guide-resistant LITAF rescue;
  - optional LITAF overexpression;
  - positive controls: TLR4/LPS and TNF/IL1B stimulation;
  - orthogonal comparator: Kava-241 or Kava-205Me only as broad pathway tools,
    not as proof of LITAF selectivity.
- Required knockdown: at least 70% LITAF mRNA and protein reduction without
  more than 15% viability loss.
- Readouts at 6, 24, and 48 hours:
  - C15ORF48/MOCCI mRNA and protein;
  - NDUFA4, mitochondrial membrane potential, mitochondrial ROS, oxygen
    consumption if feasible;
  - TNF, IL1B, IL6, CXCL8, CCL20 secretion;
  - caspase-4/caspase-1 activation and GSDMD cleavage if pyroptosis branch is
    included;
  - single-cell RNA-seq in the confirmatory stage to test whether the whole
    C15ORF48/MOCCI state shifts, not just one transcript.

Advance criterion:

- LITAF perturbation changes the C15ORF48/MOCCI module by at least 0.5 log2 in
  the predicted direction, FDR < 0.05, in at least 70% of donors, and rescue
  restores at least 50% of the effect. The effect must remain after matching
  TNF/IL1B exposure or cytokine-neutralization conditions.

Falsification:

- If LITAF knockdown changes TNF-related cytokines but C15ORF48/MOCCI changes by
  less than 0.25 log2 or fails FDR < 0.05, LITAF is not an upstream controller
  of the C15 state.
- If exogenous TNF/IL1B restores C15ORF48/MOCCI after LITAF knockdown, LITAF is
  upstream only through generic cytokine load, not a selective therapeutic node.
- If knockdown/rescue effects are donor-idiosyncratic or coupled to viability or
  endosomal-trafficking toxicity, stop direct LITAF targeting.

## Sidecar Recommendation

Do not promote LITAF as the V3 central node or intervention point.

Use LITAF as a wet-lab ordering probe for the C15ORF48/MOCCI branch. If the
ordering test is positive, the therapeutic search should move downstream or
parallel to a selective, safer node in the LITAF-induced stress program rather
than attempting direct LITAF inhibition.

## Source URLs

- PubMed 10200294: https://pubmed.ncbi.nlm.nih.gov/10200294/
- PubMed 16954198: https://pubmed.ncbi.nlm.nih.gov/16954198/
- PubMed 16804395: https://pubmed.ncbi.nlm.nih.gov/16804395/
- PubMed 21984950: https://pubmed.ncbi.nlm.nih.gov/21984950/
- PubMed 22160695: https://pubmed.ncbi.nlm.nih.gov/22160695/
- PubMed 26634547: https://pubmed.ncbi.nlm.nih.gov/26634547/
- PubMed 29914930: https://pubmed.ncbi.nlm.nih.gov/29914930/
- PubMed 23319192: https://pubmed.ncbi.nlm.nih.gov/23319192/
- UniProt Q99732: https://rest.uniprot.org/uniprotkb/Q99732
- AlphaFold AF-Q99732-F1: https://alphafold.ebi.ac.uk/entry/Q99732
- ChEMBL target CHEMBL6066581: https://www.ebi.ac.uk/chembl/g/#browse/targets/filter/target_chembl_id%3ACHEMBL6066581
- Google Patents US11767283B2: https://patents.google.com/patent/US11767283B2/en
- Google Patents US10085990B2: https://patents.google.com/patent/US10085990B2/en
- ClinicalTrials.gov API query: https://clinicaltrials.gov/api/v2/studies?query.term=LITAF
- Open Targets target ENSG00000189067: https://platform.opentargets.org/target/ENSG00000189067
