# Subagent α1 ACSL1 Deepening Report

**Returned:** 2026-05-26

No finding claimed by subagent.

## Structure And Selectivity

Human ACSL1 is structurally tractable in principle but not structure-enabled for confident CNS drug design. UniProt confirms ACSL1/3/4/5/6 are long-chain acyl-CoA ligases with overlapping catalytic chemistry.

Local UniProt-sequence alignment versus ACSL1:

- ACSL3: ~36% identity
- ACSL4: ~35%
- ACSL5: ~61%
- ACSL6: ~68%

Interpretation: ACSL1-vs-ACSL3/4 selectivity looks chemically plausible; ACSL1-vs-ACSL5/6 is harder. ACSL6 is a CNS off-target red flag because it has brain lipid-metabolism relevance.

RCSB/AlphaFold show computed full-length models, not experimental human ligand-bound structures. Docking against AlphaFold ACSL1 alone should not be treated as strong evidence because ligand pocket, membrane context, transition-state chemistry, and isoform selectivity need enzymology.

## Ligands And Inhibitors

Strongest positive: Shionogi's benzimidazole series. Compound 13 is reported as a potent ACSL1 inhibitor with human ACSL1 IC50 `0.042 uM` and `>200 uM` IC50 against ACSL3/4/5/6 in recombinant assays, with mouse in vivo long-chain acyl-CoA suppression. This establishes that ACSL1 selectivity is feasible in principle.

Current translational status remains weak:

- ChEMBL target ACSL1: `CHEMBL4295746`; local ChEMBL API returned multiple nM ACSL1 activity records, but no named clinical ACSL1 drug.
- OpenTargets for `ENSG00000151726`: no clinical candidates found by subagent; tractability says high-quality small-molecule ligand exists but ligand-bound structure is false.
- DrugBank has an ACSL1 polypeptide entry but not a clinical ACSL1-directed therapy.

Other ACSL-family compounds:

- Triacsin C inhibits ACSL1/3/4 and is not ACSL1-selective.
- Thiazolidinediones inhibit ACSL4, not ACSL1 tools.
- No verified ACSL1-selective, brain-engaged, clinically tested inhibitor was found.

## Recommended Computations

The orchestrator already ran the core recommendations:

- ODE model of myelin debris, ACSL1 activity, lipid droplets, inflammatory output, and repair safety.
- Lesion ABM simulation.
- Monte Carlo trial simulation.
- Incremental association test of ACSL1 beyond broader lipid/lysosomal module.

## Failure Reasons

- ACSL1 may be a marker of lipid-loaded phagocytes, not a driver.
- Lipid droplets may be protective lipid buffering; blocking ACSL1 could worsen lipotoxicity.
- Myelin-debris clearance and remyelination could be impaired.
- ACSL5/6 similarity creates selectivity risk; ACSL6 off-target CNS inhibition is especially concerning.
- Systemic ACSL1 liability includes cardiac fatty-acid oxidation concerns.
- No human MS ACSL1 perturbation, no clinical ACSL1 drug, no demonstrated CNS target engagement.

## Bottom Line

ACSL1 remains a plausible perturbation hypothesis only if selective CNS/microglia engagement and repair-safety windows survive wet-lab perturbation. Current chemical matter supports selectivity feasibility, not clinical feasibility.
