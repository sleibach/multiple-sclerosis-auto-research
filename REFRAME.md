# Therapeutic Discovery Reframe

**Date:** 2026-05-26  
**Starting artifacts reviewed:** `MS_RESEARCH_LOG_2026-05-26.md`, prior `FINDING.md`, and both persistent memory notes.

## Reviewer Correction Accepted

The execution-phase test asked whether a bulk transcript score for `TNFRSF9`/`TNFSF9` tracked a bulk lipid/complement score. That was a valid test of a narrow surrogate, but it was a weak operationalization of the biological mechanism: interaction between adaptive immune cells and lipid-stressed microglia at a spatially localized chronic-active lesion rim. The result must not be extended to rule out spatial cell-cell interactions or therapeutic targets within that niche.

I will not continue by mining additional bulk signature correlations. I will treat spatial neighborhood evidence and targetable perturbation evidence as mandatory.

## Chosen Direction

I will pursue a **target-agnostic therapeutic discovery/repurposing screen for progressive MS with chronic-active/paramagnetic-rim lesion biology**, centered on dysfunctional lipid/lysosome-handling microglia and their immune neighbors.

The initial candidate class is deliberately broad:

- targets and agents that restore lipid/lysosomal processing in `GPNMB+`/foamy microglia;
- targets that interrupt a spatially demonstrated immune-to-microglia injury signal;
- agents already capable of reaching the CNS at target-engaging concentrations.

Known intervention paths, **MAGL inhibition** and **DHCR24 inhibition/desmosterol elevation**, are controls and exclusion boundaries because they are already proposed or in clinical translation for progressive MS. A final claim must identify an intervention point or stratification delta not already disclosed by those programs.

## Why This Direction Is Appropriate

1. **It repairs the operationalization error.** `GSE284005` provides human MERFISH spatial data for chronic-active MS lesions; `GSE301908` provides its paired human snRNA-seq atlas. These data can test neighborhoods and cellular states rather than tissue-level co-abundance.
2. **It connects to translational assets.** `GSE279972` and its deposited workbook provide independent human lesion transcriptomic, proteomic, lipidomic, chemical-proteomic, morphology, and clinical-progression information. This can determine whether a spatially nominated target also participates in a clinically adverse lesion state.
3. **It permits cross-domain transfer.** Lipid/lysosomal microglial failure is studied in lysosomal storage disease, Parkinson disease, Alzheimer disease, atherosclerosis, and oncology. Compounds developed in those fields may already solve CNS exposure or target-engagement problems.
4. **It has hard rejection criteria.** A target will be rejected if it is not spatially present in the implicated niche, does not reproduce in independent human lesion data, lacks plausible CNS-active chemical matter, or is already directly claimed for the same MS population/mechanism.

## Alternatives Rejected Or Held In Reserve

### Alternative 1: Continue The EBV-Specific Bridge Directly

**Why attractive:** EBV is the strongest upstream causal anchor; an EBV-imprinted adaptive cell mechanism would be distinctive.

**Why not primary now:** Public spatial chronic-active lesion data do not encode EBV infection, EBV-specific clonotypes, or paired EBNA1/GlialCAM reactivity. Any EBV-specific conclusion from these datasets would again rely on a weak proxy. EBV may re-enter only if a target is independently supported and has a plausible EBV-conditioned upstream context.

### Alternative 2: Pursue The 4-1BB/CD137 Axis From The Prior Run

**Why attractive:** It generated an exploratory foamy-lesion signal and is pharmacologically addressable.

**Why rejected:** CD137-positive B cells in chronic-active MS lesions were previously published, while the prior result did not connect `TNFRSF9`/`TNFSF9` to the lipid/complement lesion program. It does not currently clear the translational or novelty bar.

### Alternative 3: Claim MAGL Or DHCR24/LXR-Lipid Efflux Directly

**Why attractive:** These are now strongly supported by human lesion multi-omics/spatial data and EAE intervention.

**Why rejected as a discovery claim:** Van der Vliet et al. already identify MAGL and disclose an ongoing progressive-MS trial of `RO7268489`; Feng et al. already test DHCR24 inhibitor `SH42` in EAE and disclose a DHCR24-inhibitor patent conflict. These are important benchmarks, not new output.

### Alternative 4: Remyelination-Only Drug Screen

**Why attractive:** Direct restoration is essential to cure.

**Why held in reserve:** A remyelination-only screen may ignore the ongoing lesion-rim injury that prevents successful repair in progression. It becomes a pivot only if no targetable inflammatory/metabolic niche survives.

## Required Evidence Before A Candidate Can Be Claimed

A proposed candidate must pass all gates:

1. **Spatial gate:** target or its actionable pathway is enriched within or immediately adjacent to pathological microglial/immune lesion-rim neighborhoods in human spatial data, not merely in bulk tissue.
2. **Independent human validation gate:** the target state or pathway reproduces in an independent human lesion dataset or independent modality tied to adverse lesion/progression biology.
3. **Intervention gate:** an agent or modality has verified target engagement, a credible CNS-exposure path, and no obvious mechanistic contradiction.
4. **Novelty gate:** PubMed, Europe PMC, bioRxiv, medRxiv, trial registries, Google Patents, and Espacenet searches do not disclose the same intervention/population/mechanism claim.
5. **Falsifiability gate:** the claim can be killed in a defined spatial/functional experiment before a clinical efficacy trial.

## Output Decision Rule

- If a candidate passes all gates, produce a therapeutic `FINDING.md`, archiving the prior negative report.
- If known targets dominate and no new candidate passes the gates, write `EXHAUSTION.md` documenting each candidate’s failure rather than manufacturing a therapeutic claim.

