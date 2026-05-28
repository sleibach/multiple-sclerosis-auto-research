# Wave98 Hostile Review: C15ORF48 -> CCL20 Branch

Timestamp: 2026-05-27 CEST

Scope: hostile review only. Assumption: the `C15ORF48 -> CCL20` branch is wrong until proven otherwise. No final finding is proposed here.

## Local Inputs Read

- `results_v3/wave96_c15orf48_controller_search/REPORT.md`
- `results_v3/wave96_c15orf48_controller_search/c15orf48_controller_candidate_rank.tsv`
- `results_v3/wave97_c15_residual_costate_falsification/REPORT.md`
- `results_v3/wave97_c15_residual_costate_falsification/residual_costate_candidate_summary.tsv`
- `results_v3/wave97_c15_residual_costate_falsification/residual_costate_context_tests.tsv`
- `subagents_v3/wave97_c15_directionality_sidecar.md`
- `subagents_v3/wave97_c15_prior_art_sidecar.md`
- `CONVERGENCE_CHECK_53.md`

## Verified Source Anchors

- Reboldi et al., `C-C chemokine receptor 6-regulated entry of TH-17 cells into the CNS through the choroid plexus is required for the initiation of EAE`, PMID 19305396.
- Sachi et al., `CCL20/CCR6 chemokine signaling is not essential for pathogenesis in an experimental autoimmune encephalomyelitis mouse model of multiple sclerosis`, PMID 36527746, DOI 10.1016/j.bbrc.2022.11.088.
- ClinicalTrials.gov `NCT02671188`, GSK3050002 anti-CCL20 in psoriatic arthritis, withdrawn before treatment.
- Google Patents `US8491901B2`, neutralizing anti-CCL20 antibodies; claims include autoimmune/inflammatory uses and chemotaxis inhibition.
- Meitei et al., `CCR6-CCL20 axis as a therapeutic target for autoimmune diseases`, PMID 33971346.
- `Cerebrospinal Fluid and Blood Cytokines as Biomarkers for Multiple Sclerosis: A Systematic Review and Meta-Analysis of 226 Studies With 13,526 Multiple Sclerosis Patients`, noting high heterogeneity for blood CCL20 in MS cytokine studies.
- `CC Chemokine Ligand 20 and Its Cognate Receptor CCR6 in Mucosal T Cell Immunology and Inflammatory Bowel Disease`, PMC3711275.

## Verdict

Do not promote `CCL20` from the current C15ORF48 branch. The branch has one residualized associative survival signal, no demonstrated C15-to-CCL20 directionality, no MS lesion-compartment validation, weak receptor-side support, obvious inflammatory confounding, and severe prior-art saturation around `CCL20/CCR6` autoimmune biology.

## Criticisms

1. The C15 anchor is not an MS anchor.

Wave96 strict C15ORF48-positive anchors are Crohn myeloid, UC myeloid, T1D stellate, and T1D endothelial. Two of four fail FDR 0.10. No strict MS lesion or MS single-cell compartment anchors the branch. A C15-positive IBD/T1D tissue-state cannot be used as an MS therapeutic mechanism without independent MS lesion validation.

2. The residualized CCL20 survival is fragile and in the wrong system.

Wave97 reopens `CCL20`, but only with `residual_case_positive_context_count=1` and `residual_case_positive_disease_count=1`. The best residual case context is T1D acinar cells, not MS, not CNS, and not myeloid. The median residual case correlation is only `0.1878`. Crohn myeloid residual case correlation is negative (`-0.025`), UC myeloid is positive but non-significant (`0.465`, p `0.353`), and the strong residual p-value comes from T1D acinar case donors (`n=5`). That is not a cross-disease controller signal.

3. This still looks like inflammatory-load confounding.

CCL20 is a canonical inflammatory chemokine induced by IL-17, TNF, IL-1, TLR/LPS, IFN-linked contexts, epithelial stress, and tissue damage. C15ORF48/MOCCI is itself inflammation-induced and plausibly compensatory. Co-movement can be explained by shared upstream inflammatory load without any C15-to-CCL20 edge.

4. State-marker/controller confusion has not been resolved.

The local evidence says `CCL20` is near a C15-high state, not that it controls that state or is controlled by C15. Wave97 explicitly states it is a confounding check, not a causal model. The directionality sidecar already classifies `CCL20` as a downstream inflammatory output or parallel chemokine rather than a protective brake.

5. Receptor-side biology does not match the ligand-side claim.

`CCR6` itself was not a Wave96 parked candidate: zero C15-positive contexts and no donor co-state. The claimed therapeutic axis therefore depends on a ligand expressed in one compartment and receptor-positive cells in another. That might be true biologically, but it requires spatial ligand-receptor evidence. It cannot be inferred from CCL20 expression alone.

6. MS-specific evidence is too weak.

Local MS white-matter evidence for `CCL20` is only a trend: delta `1.147`, p `0.061`, FDR about `0.899`. The wave does not show localization to chronic active lesion rims, choroid plexus, meninges, perivascular cuffs, microglia/macrophage subsets, or CCR6+ infiltrates. This is not an MS progression mechanism yet.

7. Genetics is not target-resolved for MS.

The broad genetics support for `CCL20` in the Wave96 row is not an MS-specific causal anchor. The listed Wave55 diseases are AS, Crohn, psoriasis, RA, and UC; Wave62 target resolution remains `NO_GO_WAVE62_TARGET_RESOLUTION`. This is autoimmune-locus adjacency, not proof that modulating CCL20 changes MS risk or progression.

8. Prior art blocks broad therapeutic novelty.

The `CCL20/CCR6` autoimmune target concept is already explicit in reviews, EAE/MS biology, clinical trial records, and patents. The only possibly novel delta is "C15ORF48-high state stratified CCL20 biology." That delta is a biomarker/state-framing delta, not a new therapeutic target claim.

9. The EAE literature is contradictory, not validating.

PMID 19305396 supports CCR6/CCL20 in early CNS entry through choroid plexus biology. PMID 36527746 reports CCL20/CCR6 signaling is not essential in an EAE model. That is exactly the kind of redundancy/compensation expected for chemokine trafficking. It weakens any simple anti-CCL20 disease-arrest claim.

10. CNS delivery and disease-stage fit are unresolved.

Anti-CCL20 antibodies are plausible for peripheral inflammation, but chronic MS progression involves compartmentalized CNS inflammation behind barriers. If the relevant site is choroid plexus or peripheral recruitment, the target population is likely early inflammatory MS, not progressive lesion-rim biology. If the relevant site is chronic active lesion rim, systemic antibody delivery and local target engagement are unproven.

11. Safety and clinical risk are underweighted.

CCR6/CCL20 recruits not only pathogenic Th17-like cells but also Tregs, B cells, dendritic cells, ILCs, and mucosal immune cells. Blunt blockade risks impairing mucosal homeostasis and antimicrobial defense while failing to suppress redundant trafficking routes. A therapy that reduces both pathogenic Th17 and regulatory recruitment could be biologically neutral or harmful.

12. The clinical precedent is not encouraging.

GSK3050002 reached a psoriatic arthritis trial (`NCT02671188`) but was withdrawn before treatment. That is not an efficacy failure, but it is also not de-risking. There is no demonstrated human autoimmune efficacy for anti-CCL20 in the local evidence stack.

## Minimum Tests Before Any Promotion

1. MS lesion-compartment validation.

Use independent MS single-nucleus or spatial datasets. Required pass: C15ORF48/MOCCI-high cells and CCL20 protein/RNA co-localize in the same lesion-relevant compartment, and CCR6+ target cells are spatially enriched nearby, in at least two independent MS datasets. Require FDR < 0.05 and at least 2x enrichment versus control/nonactive tissue. Stop if the signal is absent from chronic active rims or only appears in bulk inflammatory tissue.

2. Residualized cross-disease replication.

Redo the C15-CCL20 association with covariates for IFN, TNF/IL1/NFKB, IL17/IL23, hypoxia, epithelial damage, mitochondrial stress, cell-cycle, donor detection rate, cell-type fraction, and batch. Required pass: partial correlation rho >= 0.4 at FDR < 0.05 in MS plus at least two non-MS autoimmune tissues, with leave-one-disease-out stability. Stop if rho falls below 0.2 or survives only in T1D acinar/endothelial tissue.

3. Directionality ordering.

In primary human macrophages and iPSC microglia, n >= 8 donors, run time course stimulation with LPS, TNF, IL-1beta, IL-17A/F, IFN-gamma, and Th17-conditioned media. Perturb C15ORF48/MOCCI with CRISPRi/overexpression and measure CCL20 RNA/protein. Required pass: C15 perturbation changes CCL20 by >= 30% after controlling for NF-kB/IFN activation and viability, FDR < 0.10, replicated in both macrophages and iPSC microglia. Stop if CCL20 follows inflammatory stimulus intensity but not C15 perturbation.

4. Ligand-receptor functional test.

Use C15-high myeloid/tissue-cell conditioned media and autologous CCR6+ Th17/Treg migration assays. Required pass: anti-CCL20 reduces pathogenic CCR6+ Th17 migration by >= 50% while preserving or enriching Treg migration, with no compensatory CXCR3/CCR2/CCR5 chemokine recruitment. Stop if regulatory and pathogenic migration are equally blocked.

5. CNS target-engagement test.

For MS, show achievable target engagement in the proposed compartment. If systemic anti-CCL20 is proposed, require CSF/choroid plexus or lesion-adjacent pharmacodynamic suppression of free CCL20 and CCR6+ recruitment in a relevant model. Stop if target engagement is only peripheral blood.

6. Prior-art/FTO narrowing.

Do not claim broad anti-CCL20/CCR6 autoimmune therapy. The only potentially open claim is a C15ORF48/MOCCI-high, spatially defined, biomarker-stratified use. Before any promotion, run a formal patent and trial-registry search around that exact stratified use. Stop if existing anti-CCL20 claims already cover biomarker-selected autoimmune/MS treatment broadly enough to block freedom to operate.

## Bottom Line

The clean hostile interpretation is: `CCL20` is a known inflammatory chemokine passenger that happens to survive one permissive residualized C15 co-state test. The current branch is useful as a positive-control map of C15-high inflammatory tissue, not as a novel therapeutic target.
