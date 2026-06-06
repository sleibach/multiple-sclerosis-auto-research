# Wave16-B Hostile CTSH Critique

Role: hostile translational immunology critique for the V3 autonomous autoimmune research session.

Ownership: critique report only. I did not edit synthesis or finding files.

## Executive Verdict

Reject CTSH as a V3 central node or intervention claim on the current evidence.

`CTSH` is a useful fail-fast scout around the recurrent `CD74`/HLA-II antigen-presentation state, but the present package would not survive a skeptical translational review. The positive evidence is mostly state proximity, not disease causality. The genetic story is heavily prior-arted and directionally conflicted. The Geneformer result is weak enough to be a hypothesis generator only. The intervention concept is not yet a credible drug program because no selective CTSH-modulating autoimmune pharmacology, target engagement, or disease-specific direction has been shown.

Recommendation: pivot away from promoting CTSH. Continue only as a comparator/readout in a narrower HLA-II-loading falsification experiment. Do not advance a pan-autoimmune CTSH inhibitor strategy.

## Evidence Reviewed

Local artifacts:

- `LAB_NOTEBOOK_V3.md`, especially 2026-05-27 CTSH entries.
- `subagents_v3/wave15_surface_trafficking_dependency.md`.
- `results_v3/wave15_surface_trafficking_dependency/candidate_ranked.tsv`.
- `results_v3/wave15_geneformer_loader_dependency_delete/wave15_geneformer_loader_dependency_gene_summary.tsv`.
- `results_v3/wave15_loader_external_gate/summary.json`.
- `results_v3/wave15_loader_external_gate/open_targets_gwas_credible_sets.tsv`.
- `subagents_v3/wave15_prior_art_feasibility.md`.
- `PLAN_V3.md`, `CRITIQUE_V3.md`, and `CONVERGENCE_CHECK_3.md`.

Public literature / prior art checked:

- Wu et al. 2024, *Medicine*, "Cysteine cathepsins and autoimmune diseases: A bidirectional Mendelian randomization", DOI `10.1097/MD.0000000000040268`, PMID `39470488`: https://journals.lww.com/md-journal/fulltext/2024/10250/cysteine_cathepsins_and_autoimmune_diseases__a.16.aspx
- Lin et al. 2024 medRxiv, "The causal relationship between cathepsins and multiple sclerosis: a mendelian randomization study", DOI `10.1101/2024.09.05.24313125`: https://www.medrxiv.org/content/10.1101/2024.09.05.24313125v1.full.pdf
- Faraco et al. 2013, *PLOS Genetics*, "ImmunoChip Study Implicates Antigen Presentation to T Cells in Narcolepsy", DOI `10.1371/journal.pgen.1003270`: https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1003270
- Hao et al. 2018, *PLOS ONE*, "Crystal structures of human procathepsin H", DOI `10.1371/journal.pone.0200374`: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0200374
- Cathepsin S inhibitor celiac disease trial, PMID `39739628`: https://pubmed.ncbi.nlm.nih.gov/39739628/
- Cathepsin S inhibitor primary Sjogren trial, PMID `36864622`: https://pmc.ncbi.nlm.nih.gov/articles/PMC10629789/
- Cathepsin S inhibitor RA trial `NCT00425321`: https://clinicaltrials.gov/study/NCT00425321
- Cathepsin-S/MHC-II autoimmune patent prior art `EP0912601B2`: https://patents.google.com/patent/EP0912601B2/en

## Main Objections

### 1. CTSH Is Prior-Arted Cathepsin Genetics, Not a Novel Discovery

The current genetics story is not "we discovered CTSH"; it is "we rediscovered a cathepsin/MHC-II-adjacent genetic literature."

Local Open Targets rows are only an external triage gate: 7 `CTSH` `gwas_credible_sets` rows, limited to T1D and MS, with the guardrail "No target-level coloc/MR is claimed." That is not V3-grade target genetics.

The public literature is already worse for novelty:

- Wu et al. 2024 explicitly reports cathepsin H associations across autoimmune diseases, including cathepsin H protective for celiac disease and risk-increasing for T1D and PBC.
- Lin et al. 2024 preprint reports cathepsin H/MS MR association (`IVW P=0.036`, `OR=1.095`, `95% CI=1.006-1.192`) according to the V3 notebook extraction.
- Faraco et al. 2013 already placed `CTSH` in an antigen-presentation/autoimmune-like narcolepsy context.
- T1D biology already treats `CTSH` as a candidate gene, including beta-cell and APC relevance.

Reviewer reaction: "This is known cathepsin immunogenetics with a new spreadsheet around it." The only potentially novel claim would be a very specific cross-disease HLA-II loading-state dependency that is not reducible to prior cathepsin genetics. The current evidence does not establish that.

Falsifying evidence required:

- Fine-mapped `CTSH` cis-eQTL or cis-pQTL colocalization, independent of neighboring locus artifacts, in at least MS and T1D, with disease-relevant cell-type direction.
- Formal MR using validated cis instruments, not broad protein-level cathepsin panels alone.
- Conditioning against HLA/MHC and antigen-presentation state covariates where relevant.
- A clear statement of what is new beyond "cathepsin H genetically associates with autoimmune disease."

### 2. The Cross-Disease Signal Is Still Confounded by APC/Myeloid Abundance and IFN/HLA State

The local CTSH signal is not strong disease-control recurrence. It is mostly coupling to a pre-existing `CD74`/HLA-II state.

From `candidate_ranked.tsv`:

- `CTSH` has 1 FDR10-positive disease-control signal out of 10 tested diseases.
- It has 5 trend-or-better disease-control diseases, but several are weak or small-n: thyroid Visium with 2 controls, celiac marker-derived compartments, and non-significant MS.
- RA blood myeloid is not supportive by disease-control delta (`delta=-0.055`, Hedges g `-0.517`, p `0.123`, FDR `0.995`).
- Sjogren APC disease-control delta is essentially null/slightly negative (`delta=-0.0149`, p `0.898`).
- Celiac myeloid/APC-like disease-control support is positive but null (`delta=0.132`, p `0.251`, FDR `0.616`).
- The top score is rescued by state coupling: 8 residual non-IFN state-coupling diseases and 8 raw state-coupling diseases.
- There are still 9 diseases with raw confounder correlation and 3 confounder-dominant diseases.

This is not a clean central-node pattern. It is the expected behavior of a lysosomal protease expressed in antigen-presenting or inflamed tissue compartments. Residualizing out `myeloid_abundance`, `generic_nfkb`, and `lipid_loader_phagocytic` helps, but it does not eliminate the main concern: CTSH can be a passenger of HLA-II/IFN/APC activation. The broader V3 critique already found the antigen-processing state collapses after IFN control in many settings. CTSH has not escaped that prior failure.

Reviewer reaction: "You nominated a marker of cells doing antigen presentation, then called it a controller of antigen presentation."

Falsifying evidence required:

- Donor-level models showing CTSH predicts disease/control or tissue damage after controlling for cell-type abundance, HLA-II module, `CD74`, `CIITA`, `RFX5`, IFN score, tissue injury, treatment, and sampling site.
- Single-cell or spatial colocalization showing CTSH-high cells are not merely APC-rich regions or infiltrate-rich tissue.
- Independent RA synovium, SLE myeloid/pDC, and MS lesion-edge validation under the same covariate model.
- A negative-control inflammation cohort showing CTSH is not just a generic inflammation/APC activation marker.

### 3. Geneformer Support Is Too Weak to Count as Support

The Geneformer evidence should be treated as nearly null.

Local summary:

- `CTSH` has 9 contexts with token and 43 disease cells with token.
- Mean cosine shift is tiny and negative (`-8.09e-05`).
- Mean projection shift is tiny (`0.00713`).
- Mean cosine z versus random is essentially zero (`0.0112`).
- It has 3 support contexts but 0 strong support contexts.
- Positive projection contexts are 4; negative projection contexts are 5.

The implementation itself is explicitly limited:

- Custom lightweight deletion screen, not official Geneformer `InSilicoPerturberStats`.
- Maximum 24 disease and 24 control cells per context.
- Only 3 random deletion reps.
- Candidate-expressing disease cells were enriched, so effect sizes are not population estimates.
- Embedding shifts are not expression changes, target engagement, antigen-presentation assays, or causal perturbation.

This is not "foundation model support"; it is at most a weak non-veto. A reviewer would not let this satisfy the V3 foundation-model/perturbation criterion, especially when the shift magnitude is basically numerical dust and the direction is mixed.

Falsifying evidence required:

- Official or independently benchmarked Geneformer/State/Perturb-seq-style perturbation with enough cells per context and predeclared statistics.
- Demonstrated CTSH deletion or inhibition moves disease APCs toward controls in multiple disease contexts with effect sizes exceeding random-token and cathepsin-family controls.
- Agreement with real perturbation data: CTSH CRISPRi/KO or selective inhibition should reduce HLA-II peptide loading or pathogenic T-cell activation without generic IFN collapse.

### 4. Celiac Protective MR Contradicts a Pan-Autoimmune Inhibitor Strategy

Wu et al. 2024 is a direct problem for the therapeutic story. The V3 notebook records cathepsin H as:

- protective for celiac disease (`WR OR=0.881`, `95% CI=0.838-0.926`, `P=6.5e-7`);
- risk-increasing for T1D (`IVW OR=1.121`, `95% CI=1.053-1.194`, `P=.0003`);
- risk-increasing for PBC (`WR OR=1.792`, `95% CI=1.062-3.024`, `P=.0288`).

If higher cathepsin H is protective in celiac disease, systemic CTSH inhibition is directionally suspect for celiac. You cannot call this pan-autoimmune unless you explain why inhibition is beneficial in T1D/MS/PBC but not harmful in celiac, or why the proposed modality is not a simple inhibitor.

The celiac issue is not a small footnote. Celiac is one of the V3 breadth diseases and one of the cleanest antigen-presentation diseases. A protective MR signal for the same protease undercuts the idea that "less CTSH equals less autoimmune antigen presentation equals good."

Reviewer reaction: "Your own genetics says the same target may be protective in an autoimmune disease. Why are you proposing a pan-autoimmune inhibitor?"

Falsifying evidence required:

- Disease-by-disease directionality map separating expression, protein activity, antigenic peptide repertoire, and clinical risk.
- Celiac-specific data proving CTSH inhibition does not worsen gluten peptide presentation, epithelial injury, or T-cell activation.
- If the proposal is not inhibition, define the modality precisely: inhibitor, activator, compartmental modulator, substrate-biased inhibitor, delivery-restricted agent, or biomarker only.
- Explicit exclusion of celiac from any inhibitor claim unless protective-direction data are overturned.

### 5. Druggability and Selectivity Are Not Credible Yet

The claim "CTSH is an enzyme, therefore druggable" is too shallow for chronic autoimmune translation.

CTSH is an intracellular lysosomal cysteine protease with distinctive aminopeptidase biology, broad tissue expression, and physiological functions outside APCs. Structural work shows special activation/mini-chain biology and dependence on other proteases such as cathepsin L for proenzyme activation. This is not automatically a clean oral target.

The class history warns against overconfidence:

- Cathepsin S is the most obvious MHC-II cathepsin precedent, and it is already clinically and patent saturated in autoimmune disease.
- CTSS has direct Sjogren, celiac, and RA trial prior art and patent claims around suppressing class-II MHC immune responses.
- Cathepsin-family active sites are conserved enough that selectivity and lysosomal/off-target liabilities require direct proof, not assertion.
- Broad cathepsin inhibition risks lysosomal proteostasis, tissue repair, host defense, surfactant biology, beta-cell stress, and non-immune tissue effects.

There is no local evidence of:

- selective CTSH chemical matter;
- human APC target engagement;
- antigen-presentation selectivity over CTSS/CTSB/CTSL/CTSD;
- disease-relevant exposure in lysosomal compartments;
- acceptable chronic safety margins;
- any CTSH clinical trial.

ClinicalTrials.gov returning zero CTSH/cathepsin-H hits is not a novelty win. It is also a tractability warning.

Falsifying evidence required:

- A selective CTSH inhibitor or modulator with biochemical selectivity across cysteine cathepsins and cellular lysosomal target engagement.
- Activity-based probe evidence in primary human APCs showing CTSH can be modulated without hitting CTSS/CTSB/CTSL enough to explain the phenotype.
- Human antigen-presentation assays showing disease-relevant peptide/HLA-II changes, not generic lysosomal shutdown.
- Safety package covering lung surfactant biology, pancreatic beta-cell survival/stress, macrophage lysosomal function, infection risk, and tissue repair.
- A delivery strategy if systemic CTSH modulation is unsafe.

### 6. CTSH Does Not Meet the V3 Central Node / Intervention DoD

V3 promotion requires convergence across independent workstreams, perturbation/foundation support, interpretable genetics, tractability, non-blocking prior art, and a feasible falsification path.

CTSH fails or is incomplete on each:

- Breadth: only 1 FDR10-positive disease-control signal; broader support is state coupling.
- MS anchor: MS microglia disease-control signal is positive but non-significant (`p=0.320`, FDR `0.648` in the surface screen details).
- Genetics: locus-level Open Targets and prior-art MR, not target-level coloc/MR with a clean intervention direction.
- Perturbation: no real CTSH perturbation. Geneformer is weak and non-causal.
- Prior art: cathepsin genetics and MHC-II cathepsin intervention are crowded.
- Druggability: enzyme class is tractable in principle, but CTSH-specific selectivity, modality, and chronic autoimmune safety are unproven.
- Direction: celiac protective MR contradicts a pan-autoimmune inhibitor.

Reviewer reaction: "At best, CTSH is a measurable member of a known APC/cathepsin/HLA-II axis. It is not yet the axis controller, and it is not a defensible intervention."

## Required Falsification Package Before Any Resurrection

Minimum package to continue CTSH as more than a scout:

1. **Causality:** CTSH perturbation in primary human disease-relevant APCs, epithelial cells where relevant, or organoids must selectively alter HLA-II peptide loading/pathogenic T-cell activation. Knockdown/inhibition must outperform `CTSS`, `CTSB`, `CTSL`, and generic lysosome controls.
2. **Specificity:** Effects must remain after IFN, HLA-II abundance, APC abundance, and lysosomal-stress controls. Readouts should include peptide repertoire, HLA-II surface complex quality, T-cell activation, and cell viability.
3. **Genetics:** Coloc/MR must be target-level and directionally consistent for the proposed indication set. Celiac must be excluded or rescued with contrary evidence.
4. **Pharmacology:** A selective CTSH chemical or genetic modulation tool must show cellular target engagement and cathepsin-family selectivity.
5. **Translation:** Safety must address lung, beta-cell, macrophage/host-defense, and tissue-repair liabilities.
6. **Novelty:** The claim must be stated as something narrower than cathepsin-autoimmune genetics or cathepsin/MHC-II inhibition, because those lanes are already occupied.

## Continue / Pivot Recommendation

Pivot.

Do not spend V3 synthesis capital trying to make CTSH the central node. Keep it as:

- a local HLA-II-loading/APC-state scout;
- a cathepsin-family comparator against `CTSS`;
- a possible peptide-repertoire readout in future wet-lab designs.

The next productive route is not "CTSH inhibitor for pan-autoimmunity." It is either:

- a narrow, disease-specific antigen-presentation dependency experiment where celiac is excluded upfront; or
- a pivot to a controller with stronger perturbation support, cleaner disease direction, and less prior-art saturation.

Explicit V3 call: `CTSH` is **NO-GO for central node/intervention promotion** under the current DoD. Continue only as a falsification target or comparator; otherwise pivot.
