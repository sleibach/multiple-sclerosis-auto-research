# Wave102 SEL1L3 / FXYD5 Mechanism, Topology, and Modality Sidecar

Date: 2026-05-27 21:37 CEST

Role: sidecar audit after Wave101 ranked `SEL1L3` and `FXYD5` as parked
accessible survivors. This note asks whether either candidate has a plausible
intervention route. It does not claim promotion.

## Bottom Line

No candidate receives a therapeutic `GO`.

`SEL1L3` remains `PARK_TOPOLOGY_VALIDATION_ONLY`. It has the cleaner local
cross-disease expression profile and nominal MS white-matter signal, but public
annotation still supports only an undercharacterized single-pass membrane
protein with no ligand, pathway, catalytic function, ChEMBL target, clinical
candidate, or validated perturbation direction. The first useful experiment is
surface/topology and function discovery, not intervention development.

`FXYD5` remains `PARK_WETLAB_KILL_TEST_ONLY`. It has a much clearer surface
topology and a mechanistic route through Na,K-ATPase, adhesion, and epithelial
barrier biology, but that same route is the safety liability. Only a
non-depleting, barrier-preserving perturbation could reopen it. Cytotoxic or
Na,K-ATPase-disruptive FXYD5 targeting is a no-go for autoimmune disease.

## Targetability Matrix

| Axis | `SEL1L3` | `FXYD5` |
|---|---|---|
| Sidecar call | `PARK_TOPOLOGY_VALIDATION_ONLY` | `PARK_WETLAB_KILL_TEST_ONLY` |
| Local Wave101 status | `PARK_NEEDS_PERTURBATION_AND_GENETIC_ANCHOR`; score `22.78`; MS delta `0.9225`, p `0.01814`, FDR `0.8373`; positive diseases `3`; missing perturbation/model and genetics | `PARK_NEEDS_PERTURBATION_AND_GENETIC_ANCHOR`; score `17.23`; MS delta `0.3525`, p `0.05871`, FDR `0.8989`; positive diseases `4`, negative disease `1`; missing perturbation/model, genetics, and clean direction |
| Likely disease cell source from local data | Tissue-resident compartments, mainly UC/Crohn colon stromal and T1D endothelial. Not a myeloid/APC-centered signal in Wave79. | Epithelial/barrier and tissue-resident compartments, especially UC colon epithelial, psoriasis keratinocyte, T1D endothelial/stellate/acinar contexts; Crohn contradiction remains. |
| HPA expression readout | Evidence at protein level; tissue enhanced in lymphoid tissue; single-cell RNA enriched in B cells, pDCs, and plasma cells; detected broadly. | Evidence at protein level; low tissue specificity; single-cell RNA enriched in apical squamous epithelial cells and trophoblast cells, with cDC/monocyte signal also listed; detected broadly. |
| UniProt topology | Q68CR1, 1132 aa, single-pass membrane protein, predicted TM helix 1057-1077. UniProt does not provide an explicit extracellular/cytoplasmic domain assignment in the retrieved fields. | Q96DB9, precursor/type I single-pass membrane protein; signal peptide 1-21, extracellular domain 22-145, TM helix 146-164, cytoplasmic tail 165-178. This is the stronger extracellular-accessibility case. |
| OpenTargets tractability | Antibody tractability has only the weak `UniProt SigP or TMHMM` flag true; small-molecule tractability false across queried categories; no drug/clinical candidates. | Antibody tractability has UniProt and GO high-confidence membrane flags true plus SigP/TMHMM true; small-molecule tractability false across queried categories; no drug/clinical candidates. |
| ChEMBL | Exact target search returned 0 targets. | Exact target search returned 0 targets. |
| Pharos | API access returned HTTP 403, so no Pharos data were used. | API access returned HTTP 403, so no Pharos data were used. |
| Mechanistic interpretability | Weak. SEL1-repeat membrane protein, but no actionable receptor/ligand/catalytic axis found. Disease-direction hypothesis is therefore speculative. | Moderate. FXYD5/dysadherin regulates Na,K-ATPase activity and cell adhesion/E-cadherin biology; disease-direction hypothesis is testable but safety-sensitive. |
| Selectivity feasibility | Antibody selectivity may be possible if a disease-exposed ectodomain is confirmed, but current topology is too uncertain. Small molecules are not credible from current data. | Antibody/Fab selectivity against the long extracellular ectodomain is plausible in principle. Functional selectivity is harder because FXYD5 couples to Na,K-ATPase and junctional biology. |
| Safety liabilities | Unknown-biology liability. Broad immune/lymphoid and brain RNA detection means depletion or systemic engagement is not justifiable without function. Absence of OpenTargets safety liabilities is not reassuring. | Known-biology liability. Perturbing FXYD5 can affect epithelial adhesion, barrier state, Na,K-ATPase activity, and cancer/metastasis-associated programs. Barrier impairment is an immediate kill criterion. |
| Most defensible modality | None yet. Discovery reagents only: surface antibody validation, CRISPRi/siRNA, tagged topology constructs. | Non-depleting anti-ectodomain Fab/antibody or RNA knockdown as an ex vivo perturbation. ADC/cytotoxic payloads and Na,K-ATPase-toxic payloads are not acceptable autoimmune modalities. |
| Lead wet-lab context if tested | UC/Crohn colon stromal/endothelial cultures, T1D islet endothelial cells, or MS lesion perivascular/stromal validation tissue. | UC epithelial organoid/monolayer or inflamed epithelial-stromal co-culture first; psoriasis keratinocyte model as a secondary accessible-tissue check. |

## Candidate-Specific Assessment

### SEL1L3

`PARK_TOPOLOGY_VALIDATION_ONLY`.

The local signal is interesting because `SEL1L3` has a nominal MS
white-matter increase and recurrent tissue-resident disease signals without a
negative-disease call in Wave101. However, the signal is not yet a mechanism.
Wave79 already classified it as `NO_GO_TARGETABILITY_SHORTLIST_NODE`, with no
APC/myeloid-positive disease count, no genetics/target-resolution support, no
residual survival, and no promotable model or perturbation evidence.

Public target annotation does not rescue the case. UniProt supports a
single-pass membrane protein with a C-terminal transmembrane helix, but the
retrieved annotation does not assign a clear extracellular targetable domain.
OpenTargets gives only a low-level antibody tractability flag from predicted
signal/TM features and no clinical candidates. ChEMBL returns no exact target.
HPA indicates broad detection with lymphoid/B-cell/pDC/plasma-cell enrichment,
which cuts against a clean stromal/endothelial-only therapeutic window.

Disease-direction hypothesis: if causal, `SEL1L3-high` stromal/endothelial
cells may license leukocyte retention or inflammatory remodeling in UC/Crohn,
T1D, and perhaps perivascular MS tissue. That is an unvalidated hypothesis.
The current evidence cannot distinguish causal licensing from a surface marker
of diseased tissue architecture.

Kill-test design:

1. Validate surface exposure in disease-positive cells by flow/CITE-seq or
   immunofluorescence using at least two independent antibodies plus an
   epitope-tagged topology construct. Primary contexts: UC/Crohn colon stromal
   and endothelial cells, T1D islet endothelial cells, and MS lesion
   perivascular/stromal tissue if available.
2. Perturb `SEL1L3` by CRISPRi/siRNA in primary stromal/endothelial cultures
   stimulated with TNF, IL-1 beta, and IFN-gamma; rescue with an
   RNAi-resistant cDNA if feasible.
3. Readouts: target protein loss, cell viability, leukocyte adhesion or
   transmigration, `ICAM1`/`VCAM1`/`CCL2`/`CCL20`/`CXCL10`, matrix-remodeling
   genes, and the local lipid-lysosomal/stress modules used in V3.
4. Pass condition: at least two independent donors show a reproducible
   `>=30%` reduction in inflammatory licensing or leukocyte adhesion with
   `<10%` viability loss and rescue in the same direction.
5. Stop-loss: no disease-enriched surface protein, no perturbation effect,
   non-rescuable effect, broad toxicity, or a response explained entirely by
   generic inflammatory suppression.

This is a discovery assay. A failed topology experiment closes `SEL1L3` as an
intervention candidate while preserving it as a possible localization marker.

### FXYD5

`PARK_WETLAB_KILL_TEST_ONLY`.

`FXYD5` has the better modality surface: UniProt gives an extracellular domain
and OpenTargets antibody-tractability evidence is stronger than for `SEL1L3`.
It also has a concrete mechanism. UniProt and the linked literature describe
FXYD5/dysadherin as a Na,K-ATPase regulator that can affect Na/K transport,
E-cadherin, adhesion, polarity, and metastasis-associated behavior. That makes
the biology testable, but not automatically therapeutic.

The core blocker is direction and safety. Local evidence contains a Crohn
negative-disease context and response-direction conflict. A molecule that
modulates epithelial adhesion and Na,K-ATPase could either reduce inflammatory
barrier pathology or worsen barrier integrity and tissue repair. Oncology
antibody-drug-conjugate precedent against dysadherin also does not translate:
depleting or poisoning FXYD5-positive epithelial/stromal cells is inappropriate
for autoimmune repair-preserving therapy.

Disease-direction hypothesis: in selected epithelial/barrier-dominant
autoimmune contexts, excess FXYD5 may promote an adhesion-low, inflammatory,
barrier-unstable state. A non-depleting antagonist or normalizing perturbation
could be beneficial only if it restores junctional integrity while reducing
the disease module. The hypothesis is not safe to test first in CNS/MS; UC or
psoriasis ex vivo systems are the tractable kill-test entry point.

Kill-test design:

1. Use human UC epithelial organoids/monolayers or inflamed epithelial-stromal
   co-cultures as the primary system. Include psoriasis keratinocytes only as
   a secondary accessible-tissue replication model.
2. Perturb with two orthogonal, non-depleting strategies: CRISPRi/siRNA and a
   non-depleting anti-FXYD5 extracellular-domain Fab or blocking antibody.
   Explicitly exclude ADC, cytotoxic payload, and cardiac-glycoside/Na,K-ATPase
   toxic payload approaches.
3. Readouts: target engagement, TEER, FITC-dextran permeability, E-cadherin,
   ZO-1/occludin/claudin localization, Na,K-ATPase activity, viability,
   inflammatory cytokines, and the V3 disease-state modules.
4. Pass condition: orthogonal perturbations reduce the FXYD5-positive disease
   module by `>=30%`, preserve or improve TEER/permeability, maintain
   Na,K-ATPase activity within `+/-20%`, preserve viability, and reproduce in
   at least two independent donors/organoid lines.
5. Stop-loss: TEER decreases by `>10%`, permeability worsens, E-cadherin or
   tight-junction localization worsens, Na,K-ATPase activity shifts by `>20%`,
   cytotoxicity appears, effects are not target-engagement dependent, or the
   Crohn direction conflict reproduces.

This is a falsification assay, not a promotion package. Passing it would only
justify a target-specific perturbation branch; failing any barrier or
Na,K-ATPase criterion closes `FXYD5`.

## Integration Decision

`FXYD5` is the better mechanistic and topological candidate, but its safety
liabilities are exactly colocated with the proposed mechanism. `SEL1L3` is the
cleaner underexplored expression survivor, but it lacks the minimum target
biology needed for intervention design.

Therefore:

- Do not promote either candidate to FINDING_V3.
- If wet-lab access exists, prioritize one bounded `FXYD5` barrier-preserving
  kill test.
- Run `SEL1L3` only as a cheap topology/function-discovery assay bundled with
  broader tissue-resident-cell validation.
- If no new target-specific perturbation appears, close the accessible-survivor
  route and pivot away from surface-marker discovery.

## Traceability

Local inputs:

- `CONVERGENCE_CHECK_57.md`
- `results_v3/wave101_accessible_survivor_forcing_triage/REPORT.md`
- `results_v3/wave101_accessible_survivor_forcing_triage/accessible_survivor_forcing_rank.tsv`
- `subagents_v3/wave94_cd82_fxyd5_sidecar.md`
- `subagents_v3/wave94_accessible_state_sidecar.md`
- `subagents_v3/wave79_targetability_prior_art_directionality.md`
- `results_v3/wave79_targetability_shortlist_audit/REPORT.md`
- `results_v3/wave79_targetability_shortlist_audit/targetability_integrated_decision.tsv`

External annotation checks:

- UniProt `SEL1L3` Q68CR1: https://www.uniprot.org/uniprotkb/Q68CR1/entry
- UniProt `FXYD5` Q96DB9: https://www.uniprot.org/uniprotkb/Q96DB9/entry
- HPA `SEL1L3`: https://www.proteinatlas.org/ENSG00000091490-SEL1L3
- HPA `FXYD5`: https://www.proteinatlas.org/ENSG00000089327-FXYD5
- ChEMBL target search `SEL1L3`: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=SEL1L3&limit=10
- ChEMBL target search `FXYD5`: https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=FXYD5&limit=10
- OpenTargets `SEL1L3`: https://platform.opentargets.org/target/ENSG00000091490
- OpenTargets `FXYD5`: https://platform.opentargets.org/target/ENSG00000089327
- OpenTargets tractability documentation: https://platform-docs.opentargets.org/target/tractability
- FXYD5 Na,K-ATPase activity PMID 18263667: https://pubmed.ncbi.nlm.nih.gov/18263667/
- FXYD5/dysadherin review PMID 27066483: https://pubmed.ncbi.nlm.nih.gov/27066483/
- FXYD5 ectodomain/adhesion paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC4920254/
- Dysadherin/E-cadherin/metastasis paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC117566/
- FXYD5 ADC/EDC patent EP2475391B1: https://patentimages.storage.googleapis.com/44/7b/ba/41285c567683cf/EP2475391B1.pdf

Pharos note: direct API calls to `https://pharos.nih.gov/idg/api/v1/targets`
returned HTTP 403 for both genes in this environment, so Pharos values were not
used as evidence.
