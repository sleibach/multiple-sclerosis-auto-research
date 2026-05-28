# Wave99 Sidecar: Endogenous Inflammasome/Caspase Brake Prior-Art and Druggability Audit

Scope: prior-art, patent/trial, and translational feasibility audit only. I do not claim a finding.

Web status: web search was available. Some direct PubMed/PMC opens hit browser checks, so I relied on accessible PubMed pages/snippets, ClinicalTrials.gov records, Google Patents, PMC/Nature pages where accessible, and local V3 artifacts.

Local artifacts checked:

- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank_full.tsv`
- `results_v3/wave55_external_genetics_druggability_sweep/external_genetics_rank.tsv`
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`
- `results_v3/wave68_gse282122_unrestricted_gene_screen/adjusted_top_gene_ols.tsv`
- `results_v3/wave96_c15orf48_controller_search/c15orf48_controller_candidate_rank.tsv`
- `results_v3/wave97_c15_residual_costate_falsification/residual_costate_candidate_summary.tsv`
- `results_v3/wave98_c15_successor_perturbation_first_audit/c15_successor_perturbation_first_rank.tsv`

## Executive Call

No candidate is a GO for a V3 therapeutic claim.

`CARD16` is the only candidate I would promote locally, and only as a computationally testable endogenous-brake/state-ordering hypothesis. It has the broadest local signal among the brake candidates, but lacks MS compartment support, strict residual support, genetics, ChEMBL tractability, and any ready modality.

`CARD17` and `CARD18` are mechanistically attractive protein-interface comparators because CARD17/INCA has structural evidence for caspase-1 CARD filament capping and CARD18/ICEBERG binds caspase-1 CARD, but they have almost no local cross-disease evidence and are intracellular protein-interface targets. Treat them as structural controls, not targets.

`SERPINB1` and `IL18BP` are strongly prior-arted. `SERPINB1` is additionally direction-conflicted: boosting it could restrain inflammatory caspases in myeloid cells but may preserve pathogenic Th17 cells in EAE biology. `IL18BP` is clinically tractable but not novel for autoimmunity/MS-adjacent use.

Core pyroptosis comparators (`CASP1`, `CASP4`, `CASP5`, `GSDMD`, `NLRP3`, `IL1B`, `IL18`) are saturated prior-art or safety-blocked. `GBP1/GBP2/GBP5` are generic interferon/host-defense comparators, not selective intervention points.

## Candidate Calls

| Candidate | Call | Closest prior art | Druggability and safety | Local computational promotion |
|---|---:|---|---|---|
| `CARD16` | PARK | CARD-only proteins (`CARD16`, `CARD17`, `CARD18`) reported to prevent inflammasome assembly and ameliorate gout in vivo; older literature describes COP/Pseudo-ICE as a caspase-1-related decoy family member. | Intracellular CARD-only protein; no enzymatic pocket, no ChEMBL tractability locally, delivery would require gene/RNA/protein-mimetic strategy. Safety unknown; could blunt host-defense inflammasome function. | Yes, but only for local ordering: broad local positive disease count `5`, Wave39 positive diseases Crohn/UC/psoriasis/Sjogren/T1D, anti-TNF remission-adjusted mono/macro delta `-0.767`, FDR `0.0339`; however MS p `0.495` and strict residual disease count `0`. |
| `CARD17` / INCA | PARK | Structural PubMed record shows INCA/CARD17 caps caspase-1 CARD filaments with low-nanomolar inhibition of polymerization and inflammasome activation in cells: https://pubmed.ncbi.nlm.nih.gov/27043298/. | Intracellular protein-interface target; no local small-molecule modality. Protein mimetic might be possible but nontrivial and currently speculative. | No primary promotion. Use as a structural comparator if CARD16 survives local ordering. |
| `CARD18` / ICEBERG | PARK | CARD18/ICEBERG is part of the CARD-only inflammasome-regulator literature; keratinocyte/lichen-planus prior art exists: https://pubmed.ncbi.nlm.nih.gov/28506683/. Local Wave62 had psoriasis genetics support but no local positive disease expression. | Same intracellular protein-interface/delivery issue. Potential skin relevance, weak MS relevance. | No primary promotion. Use as CARD17/CARD16 comparator. |
| `SERPINB1` | NO-GO | SERPINB1-mediated inflammatory-caspase checkpoint is published: https://pubmed.ncbi.nlm.nih.gov/30692621/. Separate EAE prior art reports SerpinB1 controlling encephalitogenic T helper cells; MouseMine links PNAS 2019, PMID `31548399`, DOI `10.1073/pnas.1905762116`: https://www.mousemine.org/mousemine/report.do?id=74099282. | Intracellular serpin. Direction conflict: inhibiting it may kill pathogenic Th17-like cells, while augmenting it may restrain myeloid caspases/neutrophil proteases. Safety risk includes neutrophil survival/protease balance and infection handling. | No. Local broad signal is weaker than CARD16, MS p `0.869`, strict residual disease count `0`; use as a directionality warning. |
| `IL18BP` | NO-GO | Recombinant IL-18BP/r-hIL-18BP has Phase I RA/psoriasis safety/PK prior art: https://pubmed.ncbi.nlm.nih.gov/16898079/. Tadekinig alfa Phase II AOSD trial: ClinicalTrials.gov `NCT02398435`, https://clinicaltrials.gov/study/NCT02398435. Phase III monogenic IL-18-driven autoinflammation: `NCT03113760`, https://clinicaltrials.gov/study/NCT03113760. MS/neurological inflammatory patents exist: US8128920B2 and IL-18R antagonist MS/demyelination patent WO2007096396A2. | Strong biologic modality and biomarker (`free IL-18`) feasibility. Novelty blocked for IL-18 neutralization in autoimmune/inflammatory disease; CNS penetration uncertain for biologic. | No as central node. Use as positive-control modality for IL-18-output blockade. |
| `CARD8` | PARK/NO-GO | CARD8 has prior art as NLRP3/NLRP1/CARD8 inflammasome regulator and Crohn kindred variant biology: https://pubmed.ncbi.nlm.nih.gov/29408806/. DPP8/9 inhibitors activate CARD8 inflammasome in immune cells, including resting T cells: https://pmc.ncbi.nlm.nih.gov/articles/PMC7428001/. | Current chemical biology mostly activates CARD8 via DPP8/9, opposite of a brake strategy and likely unsafe in autoimmunity. Direct CARD8 inhibition/augmentation is not a mature modality. | No. Local MS nominal p `0.029` but FDR `0.851`; no broad or residual support. |
| `CASP1` | NO-GO | Caspase-1 inhibitors are old and clinically explored. VX-765 inhibits IL-1β/IL-18 release and reduced disease severity in RA/skin-inflammation models: https://pubmed.ncbi.nlm.nih.gov/17289835/. Broad caspase inhibitor patents cover RA, IBD, Crohn, psoriasis, MS: https://patents.google.com/patent/WO2011094426A1/en. | Catalytic target, but selectivity, host defense, and inflammasome-wide safety are major liabilities. CNS/MS prior art blocks novelty. | No. Local MS p `0.811`; CRISPR efferocytosis screen unresolved. |
| `CASP4` | NO-GO | Noncanonical inflammasome comparator; Wave98 already classified `NO_GO_CLOSE_PRIOR_OR_SAFETY_BLOCKED`. Emerging CASP4 inhibitor patents exist, including WO2026055444 from WIPO search. | Catalytic target with family selectivity challenges; host-defense and infection risk. Local ChEMBL count exists (`61`) but no MS anchor. | No. Local residual C15 co-state survives in two diseases, but MS p `0.493` and Wave98 rejected promotion. |
| `CASP5` | NO-GO | Same noncanonical pyroptosis family as CASP4; no distinctive autoimmune novelty in this branch. | Catalytic but selectivity over CASP1/4 and host-defense liability remain unresolved. | No. Strong IBD remission-direction local signal in mono/macro (`-2.299`, FDR `0.0145`) but no MS/breadth/residual package. |
| `GSDMD` | NO-GO | GSDMD in EAE/MS and fumarate/succination are directly prior-arted. Google Patents WO2021252915A1 claims GSDMD succination/fumarate approaches including MS and notes DMF is frontline MS therapy: https://patents.google.com/patent/WO2021252915A1/en. | Druggable by covalent/electrophilic chemistry in principle; selectivity and broad pyroptosis suppression are safety issues. Already connected to DMF/MS. | No. Local MS nominal p `0.0496` but FDR `0.877`; C15 gate failed. |
| `NLRP3` | NO-GO | NLRP3 inhibitors are saturated: dapansutrile EAE paper https://pubmed.ncbi.nlm.nih.gov/31736980/, selnoflast UC trial https://pubmed.ncbi.nlm.nih.gov/37962000/, and broad patents claiming MS/RA/autoimmune uses such as WO2023204967A1 and US20250034114A1. | Strongest small-molecule modality among comparators, but novelty blocked and UC selnoflast signal was limited. Host defense and patient selection remain key risks. | No. Local broad positive disease count `1`, MS p `0.477`, strict residual disease count `0`. |
| `IL1B` | NO-GO | IL-1β blockade is established across autoinflammatory/autoimmune indications; canakinumab RA Phase II prior art exists (`NCT00784628` in https://pmc.ncbi.nlm.nih.gov/articles/PMC3152943/). | Biologic modality mature; infection risk and limited novelty. CNS penetration limited. | No. Local Wave86/87 treated IL1B as prior-arted inflammatory nonresponse marker; MS p `0.271`. |
| `IL18` | NO-GO | IL-18/IL-18BP axis has RA/psoriasis, AOSD, IBD, and neurological inflammatory/MS patent prior art; IL-18R antagonism in demyelinating disease is explicitly patented in WO2007096396A2. | Biologic blockade feasible through IL18BP or antibodies, but novelty is blocked and biology is context-dependent. | No. Local DC remission-adjusted delta was positive (`+0.836`, FDR `0.0312`), direction opposite to simple inhibition; MS p `0.206`. |
| `GBP1` | NO-GO | Prior local Wave86/87 flagged GBP1 as an interferon/nonresponse marker, not a selective controller. | GTPase/host-defense target; inhibition risks antimicrobial/antiviral defense. No clean selective autoimmune modality. | No. Local anti-TNF remission delta is strong (`-1.976`, FDR `0.0171`) but generic IFN confounding dominates; MS only trend p `0.068`. |
| `GBP2` | NO-GO | Same interferon/host-defense comparator class as GBP1. | Poor selectivity and infection risk; not a tractable autoimmune target. | No. Local remission delta `-1.179`, FDR `0.0224`, but no MS/broad/residual package. |
| `GBP5` | NO-GO | Same interferon/host-defense comparator class; known inflammasome/IFN adjacency but not a selective therapeutic node here. | Poor selectivity and infection risk. | No. Local CRISPR unresolved; C15 gate failed; MS p `0.0838`, FDR `0.899`. |

## Closest Prior Art and Blocking Deltas

1. CARD-only brakes (`CARD16`, `CARD17`, `CARD18`) are not a blank space. The 2023 COP paper reports endogenous COP knockout increases IL-1β/IL-18 release and that COPs prevent inflammasome assembly/ameliorate gout: https://pmc.ncbi.nlm.nih.gov/articles/PMC10151391/. Structural work shows CARD17/INCA can cap caspase-1 CARD filaments: https://pubmed.ncbi.nlm.nih.gov/27043298/.

   Delta: I did not find direct MS or pan-autoimmune therapeutic development of CARD16/CARD17/CARD18 augmentation, but the missing part is not novelty alone; it is modality and disease anchoring.

2. SERPINB1 has strong mechanistic prior art as an inflammatory-caspase checkpoint and as an EAE/Th17 regulator. This blocks a simple "SERPINB1 as novel MS target" claim and creates a directionality trap.

   Delta: A myeloid-specific SERPINB1 brake hypothesis could be distinct from the Th17 survival prior art, but local data do not support promoting it.

3. IL18BP/IL-18 axis is clinically and patent saturated. RA/psoriasis Phase I, AOSD Phase II, monogenic IL-18-driven autoinflammation Phase III, Crohn expression literature, and MS/neurological inflammatory patents all exist.

   Delta: A biomarker-stratified autoimmune subgroup might still be possible, but this sidecar found no local support tying IL18BP to the V3 lipid-lysosomal myeloid module.

4. NLRP3/CASP1/GSDMD are saturated therapeutic axes. Dapansutrile, selnoflast, VX-765/pralnacasan-like caspase inhibitors, DMF/fumarate-GSDMD succination, and broad patents already claim MS/RA/IBD/psoriasis territory.

   Delta: These are useful comparators and positive controls, not novelty-open V3 nodes.

## Recommendation to Orchestrator

Run Wave99 as a forcing audit, not a rescue attempt:

- Promote `CARD16` only to local computation: test whether it is residualized from generic inflammation and whether its ordering fits brake induction after `CASP4`/`LITAF` stress rather than passive inflammatory state.
- Include `CARD17` and `CARD18` as structural/protein-interface comparators, not expression-led targets.
- Use `SERPINB1` and `IL18BP` as directionality and modality controls.
- Treat `CASP1`, `CASP4`, `CASP5`, `GSDMD`, `NLRP3`, `IL1B`, `IL18`, `GBP1`, `GBP2`, and `GBP5` as no-go comparators unless a new cell-type-specific, genetic, and perturbation-backed result overturns the prior-art and safety gates.

Practical stop rule: if `CARD16` fails residualized MS/IBD/psoriasis/Sjogren/T1D co-state or has no perturbation ordering signal, close the endogenous inflammasome-brake branch. A therapeutic claim should not be made from CARD-only-protein plausibility alone.
