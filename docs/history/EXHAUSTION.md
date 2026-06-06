# Exhaustion Report V2: No Therapeutic Finding Survived

**Date:** 2026-05-26

## Decision

I did not produce `FINDING_V2.md`. The strict V2 Definition of Done is not satisfied.

The strongest starting candidate, `ACSL1`, failed under heavier scrutiny. The strongest successor candidate, `NAMPT`, showed better cross-autoimmune recurrence and druggability, but failed novelty/therapeutic-direction requirements because NAMPT/NAD biology is already heavily studied in MS/EAE and autoimmune inflammation, and the direction of intervention is not defensible from these data.

## What Was Attempted

### Subagents

Reports are preserved in `subagents/`.

- γ1 hostile review argued ACSL1 should be treated as an overfit marker until it proves incremental value, therapeutic window, selectivity, and cross-autoimmune recurrence.
- β1 cross-autoimmune review concluded direct ACSL1 recurrence is weak; the stronger pattern is a broader lipid-handling inflammatory myeloid module.
- α1 ACSL1 deepening corrected an important feasibility point: selective ACSL1 chemistry appears possible, but CNS clinical feasibility and biological direction remain unresolved.

### ACSL1 Deepening

Executed:

- ACSL-family AlphaFold/UniProt/ChEMBL inventory: `results_v2/acsl_family_structure_pharmacology.tsv`.
- ODE therapeutic-window simulation: `results_v2/acsl1_ode_sensitivity.tsv`.
- Agent-based lesion-rim simulation: `results_v2/acsl1_abm_runs.tsv`.
- Trial-feasibility simulation: `results_v2/acsl1_trial_feasibility_simulation.tsv`.
- Incremental-value test beyond lipid/lysosomal module: `results_v2/acsl1_incremental_value_models.tsv`.
- Cross-autoimmune expression screen: `results_v2/cross_autoimmune_target_gene_contrasts.tsv`.

Key results:

- ACSL1 has high sequence identity to ACSL6 (`0.675`) and ACSL5 (`0.611`), creating CNS/family selectivity risk, although reported selective benzimidazole chemistry means selectivity is not impossible.
- ODE simulation found `0.0` fraction of parameter draws with a safe therapeutic window defined as `>=20%` injury reduction while keeping free-lipid increase and debris-clearance drop each `<=20%`.
- ABM simulation worsened active lesion area as ACSL1 activity was reduced under the explicit model assumptions.
- ACSL1 failed incremental value in MS foamy proteomics: foamy coefficient fell from `0.366`, p `2.76e-05`, to `0.124`, p `0.136`, after adjustment for the broader lipid/lysosomal module.
- Cross-autoimmune ACSL1 was inconsistent: positive in IBD, negative in psoriasis, null in lupus nephritis, nonsignificant in confounded RA macrophages, positive in SLE myeloid blood but not enough to overcome safety/direction concerns.

Conclusion: ACSL1 remains a marker and perturbation hypothesis, not a V2 therapeutic target nomination.

### Cross-Autoimmune Module And Successor Search

Accessible public datasets analyzed:

- RA macrophages: `GSE97779`.
- IBD mucosa: `GSE75214`.
- Psoriasis skin: `GSE13355`.
- Lupus nephritis kidney: `GSE32591`.
- SLE sorted blood subsets: `GSE10325`.
- Sjogren salivary gland: `GSE23117`.

The lipid/lysosomal inflammatory myeloid module recurred more consistently than ACSL1, but bulk tissue composition and disease-specific polarity prevented a clean therapeutic claim.

Successor ranking nominated `NAMPT` first:

- MS foamy proteome/snRNA convergence: `NAMPT` passed the prior convergence gate.
- Non-MS recurrence: positive in RA macrophages, psoriasis, IBD, and SLE myeloid/B-cell contrasts in accessible public matrices.
- ChEMBL targetability: `73` activity records, `37` sub-micromolar records, best recorded value `1.3 nM`.
- AlphaFold global pLDDT: `94.25`.

Why NAMPT was not promoted:

- PubMed search found substantial prior art: `(NAMPT OR visfatin OR FK866 OR APO866) AND ("multiple sclerosis" OR EAE)` returned `15` records; `FK866 experimental autoimmune encephalomyelitis` returned the 2009 paper titled "Catastrophic NAD+ depletion in activated T lymphocytes through Nampt inhibition reduces demyelination and disability in EAE."
- Broad autoimmune search returned `242` PubMed records for NAMPT/visfatin/FK866/APO866 with autoimmune terms.
- NAMPT biology has conflicting therapeutic direction: intracellular NAMPT inhibition can suppress activated immune cells but may impair NAD-dependent survival, phagocytosis, and repair; extracellular NAMPT neutralization is a different modality and was not established here as a novel MS-lesion mechanism.
- No direct clinical autoimmune NAMPT-inhibitor trial was identified in the simple ClinicalTrials.gov query; that does not create novelty because preclinical prior art is extensive.

Conclusion: NAMPT is a plausible known inflammatory-metabolic node, but not a novel V2 finding.

## Why The V2 DoD Is Not Met

| DoD item | Status |
|---|---|
| Therapeutic-relevant claim with mechanism | Not met. ACSL1 failed; NAMPT mechanism is plausible but prior-arted and directionally ambiguous. |
| Heavy theoretical/simulation backing | Partly met for ACSL1, but simulations weakened rather than hardened the claim. |
| Cross-autoimmune convergent evidence | Met only at module level, not for a clean target with therapeutic direction. |
| Multi-dataset replication within MS | ACSL1 and NAMPT have MS convergence, but ACSL1 loses incremental value and NAMPT is not novel. |
| Mechanistic chain with simulation grounding | ACSL1 simulation argues against safe inhibition; no positive chain survived. |
| Translational feasibility audit | ACSL1 lacks CNS clinical modality; NAMPT is tractable but high-liability and prior-arted. |
| Verified novelty | Not met for NAMPT; ACSL1 narrow novelty remains but target claim failed. |
| Falsification path | Exists for ACSL1 from prior phase, but V2 claim is rejected. |
| Reproducibility | Met for analyses executed; entrypoint is `./run_v2_analysis.sh`. |

## What Would Revive Each Path

### ACSL1

Needed:

- Human microglia/macrophage myelin-debris perturbation with ACSL1 knockdown/inhibition plus rescue.
- Demonstration that partial ACSL1 modulation reduces inflammatory lipid-droplet injury while preserving phagocytosis, lysosomal clearance, oligodendrocyte support, and axonal survival.
- Larger spatial/protein MS lesion cohort proving ACSL1 adds information beyond `GPNMB`/`APOE`/`PLIN2`/`CTSD`/`NAMPT` and myeloid density.
- CNS/microglia target-engagement data for a selective ACSL1 tool compound or RNA modality.

### NAMPT / eNAMPT

Needed:

- Separate intracellular NAMPT inhibition from extracellular NAMPT neutralization in MS lesion-relevant human cells.
- Evidence that eNAMPT is elevated specifically in PRL/foamy lesion microglia/macrophage niches or CSF extracellular vesicles.
- Perturbation showing eNAMPT neutralization reduces harmful inflammatory signaling without NAD-depletion toxicity.
- Novelty audit focused on eNAMPT-neutralizing antibodies or extracellular NAMPT blockade in MS, including patents.

### Broader Lipid/Lysosomal Myeloid Module

Needed:

- Cell-resolved cross-autoimmune atlases from RA synovium, IBD gut, psoriasis skin, lupus nephritis kidney, Sjogren gland, and MS lesions in a harmonized pseudobulk workflow.
- Non-autoimmune inflammatory-injury controls to distinguish pan-autoimmune from pan-injury macrophage biology.
- Perturbation datasets or CMap/LINCS signatures connecting a druggable node to module reversal.

## Reproducibility

Entry point:

```bash
./run_v2_analysis.sh
```

Important outputs:

- `results_v2/cross_autoimmune_target_gene_contrasts.tsv`
- `results_v2/cross_autoimmune_module_contrasts.tsv`
- `results_v2/extended_autoimmune_target_gene_contrasts.tsv`
- `results_v2/acsl1_incremental_value_models.tsv`
- `results_v2/acsl1_ode_summary.json`
- `results_v2/acsl1_abm_summary.tsv`
- `results_v2/successor_target_priority_rank.tsv`
- `results_v2/nampt_feasibility_summary.json`
- `results_v2/prior_art_pubmed_counts.tsv`
- `data/derived_v2_manifest.tsv`

Random seed: `20260526`.

Compute: all completed on local CPU with Python/R environment already present, except the deliberately stopped `GPL17692` annotation download.

## Honest Scope

This V2 work contributes a negative/triage result, not a cure candidate:

- ACSL1 is demoted from therapeutic target nomination to marker/perturbation hypothesis.
- A recurrent lipid/lysosomal inflammatory myeloid module appears across autoimmune datasets, but target-level causality is unresolved.
- NAMPT is the strongest successor computationally, but not novel enough and too directionally ambiguous to satisfy the requested DoD.
