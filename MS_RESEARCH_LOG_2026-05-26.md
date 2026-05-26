# Autonomous Research Log: Multiple Sclerosis

**Date:** 2026-05-26  
**Scope:** Basic-research exploration, not clinical guidance.  
**Focused question:** Can EBV-primed, CNS-homing B-cell/T-cell immunity be a mechanistic upstream driver of the chronic active lesion microglial niche that contributes to progressive MS?

## Epistemic Labels

- **Settled science:** supported by multiple converging human datasets or reproduced disease biology; it does not mean every mechanism is settled.
- **Active debate:** supported by credible data but contradicted, incomplete, or not yet causally resolved in humans.
- **Speculation:** a reasoned, falsifiable proposal that is not yet demonstrated.

This log records decision rationale, rejected directions, uncertainty, and self-critique. It does not claim to reproduce an exhaustive internal reasoning trace.

# Phase 1: Orientation

## Prior beliefs before investigation

1. **Settled science:** MS involves immune-mediated CNS demyelination and neuroaxonal injury; progression is not adequately explained by acute relapses alone.
2. **Settled science:** B cells are functionally important in MS, given CSF oligoclonal responses and efficacy of B-cell-depleting therapies.
3. **Prior belief, initially classified active debate:** EBV is probably necessary or near-necessary for most MS, but I did not assume which EBV mechanism matters: molecular mimicry, infected autoreactive B cells, impaired immune control, or an ongoing CNS reservoir.
4. **Prior belief, active debate:** progressive MS is driven substantially by compartmentalized inflammation, including chronic active lesions and possibly meningeal immune aggregates.
5. **Initial uncertainty:** I did not know whether the literature now connects EBV-specific immunity directly to the lesion-rim microglial states implicated in progression.

## Candidate directions considered

| Direction | Reason to investigate | Reason not selected as primary focus |
|---|---|---|
| Remyelination failure and oligodendrocyte precursor arrest | Directly relevant to irreversible disability; therapeutically important. | It starts downstream of the unresolved inflammatory trigger. It would likely produce a repair proposal without explaining why chronic active lesions persist. |
| Gut-brain axis and microbial metabolites | Non-obvious environmental mechanism; tractable through metabolomics and gnotobiotic models. | Human causal inference is less anchored than the EBV-MS association, and there is high risk of generating correlation-driven hypotheses. |
| EBV to compartmentalized progressive pathology | Very strong upstream human epidemiology; emerging mechanistic studies; clear contradiction concerning CNS EBV persistence; progressive MS remains poorly controlled. | It risks overfitting all MS biology to EBV and requires careful separation of initiation from progression. |

## Focus decision

I selected the **EBV-to-chronic-active-lesion bridge**. The reason is not that EBV explains all MS, but that this question has three useful properties:

1. An unusually strong upstream anchor: prospective seroconversion data.
2. A concrete downstream pathology: paramagnetic rim/chronic active lesions with inflammatory microglia and T cells.
3. A missing link that can be falsified: whether EBV-conditioned adaptive immunity initiates or sustains the lesion-rim state, with or without persisting EBV-infected cells inside the CNS.

## Self-critique after orientation

- **Risk of confirmation bias:** Selecting EBV because it has striking epidemiology could bias the investigation toward connecting unrelated downstream findings.
- **Potential category error:** A factor that initiates MS need not sustain late progression. An EBV-triggered autoimmune program could persist after EBV-specific intervention becomes irrelevant.
- **Correction adopted:** I will distinguish three models rather than treat "EBV mechanism" as one theory:
  - **Trigger-only model:** EBV breaks tolerance; later progression is autonomous.
  - **Peripheral replenishment model:** EBV-conditioned cells repeatedly seed CNS inflammation without a stable CNS viral reservoir.
  - **CNS-reservoir model:** persisting EBV-infected cells in meninges/CNS maintain local inflammation.

# Phase 2: Investigation

## Round 1: Establish the upstream EBV anchor

### Evidence collected

| Finding | Epistemic status | Interpretation |
|---|---|---|
| In more than 10 million US military personnel, 955 incident MS cases were identified; among the evaluable cases, EBV infection preceded nearly all cases, and EBV seroconversion was associated with a 32-fold increase in MS risk. [Bjornevik et al., 2022](https://doi.org/10.1126/science.abj8222) | **Settled science** for a very strong association and temporal ordering; **active debate** for strict causal necessity. | EBV is a high-priority causal upstream exposure, not merely an accompaniment of diagnosed MS. |
| CSF-derived clonally expanded B-cell antibodies can bind EBNA1 and cross-react with the CNS protein GlialCAM; functional relevance was tested in an MS mouse model. [Lanz et al., 2022](https://doi.org/10.1038/s41586-022-04432-7) | **Active debate:** demonstrated mechanism in a subset, not a universal explanation. | Molecular mimicry supplies one route from EBV immunity to CNS autoimmunity. |
| In 650 MS cases and 661 matched controls, elevated anti-EBNA1 and anti-GlialCAM reactivity associated with MS; blocking supported cross-reactivity and suggested epitope spreading. [Sattarnezhad et al., 2025](https://doi.org/10.1073/pnas.2424986122) | **Active debate**, with a stronger replication basis than in 2022. | EBNA1/GlialCAM is not just an isolated monoclonal-antibody observation, but effect sizes and predictive utility are still insufficient to declare it the central mechanism. |

### Decision and pivot

The EBV association is sufficiently strong to continue, but molecular mimicry alone does not explain:

- why disease becomes compartmentalized in the CNS;
- why chronic active lesion rims are associated with progression; or
- whether EBV remains an actionable driver after disease is established.

I therefore pivoted from "Does EBV trigger MS?" to "What EBV-conditioned cell program could connect initial immune dysregulation to progression-associated CNS niches?"

### Specific gap

**Gap G1:** It is uncharacterized in humans whether the EBV-associated immune repertoire that precedes or accompanies MS is enriched in patients who later develop persistent paramagnetic rim lesions or more aggressive chronic active lesion biology.

### Self-critique after Round 1

- A 32-fold risk ratio does not identify the causal molecular mediator. EBV could alter immune development broadly rather than operate through GlialCAM.
- The antibody work emphasizes a subset of patients. Treating it as universal would discard heterogeneity.
- This round says little about progressive MS specifically; it justifies looking for a bridge.

## Round 2: Is there an ongoing EBV-directed intrathecal response, and does it require CNS infection?

### Evidence collected

| Finding | Epistemic status | Interpretation |
|---|---|---|
| CSF B-cell clonal expansions and somatic hypermutation were found in MS, consistent with compartmentalized humoral immunity. [Colombo et al., 2000](https://pubmed.ncbi.nlm.nih.gov/10679121/) | **Settled science** at the level of intrathecal B-cell clonal responses. | The CNS/CSF is an active immune compartment, but this does not identify antigen. |
| Persistent clonally related CSF B cells, including memory B cells and plasmablasts, were found longitudinally despite treatment contexts. [Greenfield et al., 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6482992/) | **Settled science** for persistence of clones; **active debate** for their pathogenic antigen targets. | A durable intrathecal reservoir of immune cells exists, but it need not be EBV infected. |
| In eight newly diagnosed relapsing-remitting MS participants, lymphoblastoid-cell-line-reactive TCR sequences comprised `13.0 +/- 4.3%` of CSF reads; LCL specificity overlapped with `47%` of the most expanded CSF clones on average. [Gottlieb et al., 2024](https://doi.org/10.1073/pnas.2315857121) | **Active debate:** compelling but small and based on response to autologous EBV-infected lymphoblastoid cell lines, not proof of in situ viral antigen. | EBV-infected-B-cell-reactive T cells are enriched early in the intrathecal immune repertoire and could be recruited by infected cells or cross-reactive human antigens. |
| A pathology study reported EBV latent infection and BAFF expression in B cells in MS brain and ectopic follicles. [Serafini et al., 2010](https://pubmed.ncbi.nlm.nih.gov/20535037/) | **Active debate.** | Supports the CNS-reservoir model. |
| An independent pathology investigation reported that EBV infection is not a characteristic feature of MS brain tissue. [Willis et al., 2009](https://doi.org/10.1093/brain/awp200) | **Active debate.** | Directly contradicts a general CNS-reservoir model; detection methods, tissue selection, and low abundance may matter. |

### Dead end retained in the log

My initial inclination was to make a meningeal EBV reservoir the central bridge. That is not defensible as a starting assumption: positive and negative tissue studies conflict. Designing only reservoir-depletion experiments would bake a disputed premise into the program.

### Revised model

The working model now separates **antigenic imprinting** from **ongoing viral presence**:

- EBV can generate CNS-homing or autoreactive B/T populations.
- Those populations may establish or renew an intrathecal inflammatory circuit.
- Once established, microglial/glial pathology could persist even when EBV-infected cells are absent or too rare to detect.

### Specific gaps

- **Gap G2:** The antigen(s) recognized by the abundant LCL-reactive CSF T-cell clones are unresolved: latent/lytic EBV peptides, EBV-induced host proteins, or cross-reactive CNS proteins.
- **Gap G3:** No adequately powered, harmonized spatial study has resolved whether EBV-positive B cells are enriched specifically in meninges adjacent to chronic active lesions or severe cortical pathology.
- **Gap G4:** It is unknown whether EBV-negative but EBV-imprinted immune clones can maintain lesion-rim inflammation.

### Self-critique after Round 2

- "LCL-reactive" is not equivalent to "EBV-specific"; transformed B cells change host gene expression.
- Pathology non-detection is not proof of absence for rare cells, while positive detection is vulnerable to specificity and sampling concerns. A decisive study needs orthogonal viral detection and blinded pathology.
- My revised model is harder to falsify unless experiments explicitly distinguish reservoir-dependent from reservoir-independent routes.

## Round 3: What biology actually characterizes progressive lesion niches?

### Evidence collected

| Finding | Epistemic status | Interpretation |
|---|---|---|
| In secondary progressive MS autopsies, meningeal B-cell follicle-like structures occurred in 20 of 37 cases and associated with greater subpial cortical demyelination and cortical atrophy. [Magliozzi et al., 2010](https://pubmed.ncbi.nlm.nih.gov/20976767/) | **Settled science** for association in this pathology series; **active debate** for causality and general frequency. | Meningeal immune organization plausibly contributes to progressive cortical injury. |
| Paramagnetic rim/chronic active lesions identified by susceptibility MRI were associated with greater disability and worse tissue injury. [Absinta et al., 2019](https://pubmed.ncbi.nlm.nih.gov/31403674/) | **Settled science** for clinical association; biomarkers do not prove mechanism. | Chronic active lesions are an observable human outcome for mechanistic studies. |
| MRI-informed single-nucleus profiling of chronic active lesions identified inflammatory microglia (`MIMS`), inflammatory astrocytes, complement activation, and CD8 T cells at lesion edges; C1q perturbation reduced pathology in EAE. [Absinta et al., 2021](https://doi.org/10.1038/s41586-021-03892-7) | **Active debate** for causal translation from model to human; robust evidence for the human lesion niche. | A T-cell/glial/complement circuit is a plausible effector layer of chronic injury. |
| Spatial single-cell profiling of 14 human chronic active lesions reported lesion-rim CD8 T-cell niches adjacent to interferon-responsive, lipid-metabolism-altered microglia; disrupting microglial `ABCA1/G1` worsened lipid-storing phagocytes and inflammation in EAE, while sterol targeting mitigated disease in the model. [Feng et al., 2025](https://doi.org/10.1016/j.immuni.2025.10.003) | **Active debate** for human causality; strong mechanistic lead. | Failure of lipid handling may translate adaptive immune pressure into persistent microglial injury. |

### Pivot

The relevant downstream endpoint is no longer broadly "progression." It is more specific:

> **A CNS inflammatory niche in which recruited or retained CD8 T cells interact with interferon-responsive, lipid-storing microglia at chronic active lesion rims, possibly linked to adjacent meningeal immune organization.**

This allows a bridge hypothesis to be tested through cell states and spatial relationships rather than requiring clinical disability changes in an initial experiment.

### Specific gaps

- **Gap G5:** The antigen specificity of CD8 T cells spatially adjacent to lesion-rim dysfunctional microglia is uncharacterized; EBV/LCL reactivity has been measured in CSF, not paired to lesions.
- **Gap G6:** The signals causing microglial lipid-handling failure in human lesions are unresolved: `IFNG`, complement, myelin-debris overload, aging programs, or a combination.
- **Gap G7:** It is unknown whether meningeal B-cell inflammation and white-matter chronic active lesions belong to one causal circuit or are parallel outcomes of broader compartmentalized immunity.

### Self-critique after Round 3

- The lesion-rim studies are postmortem or model-supported; temporal direction cannot be read from spatial co-location.
- CD8 T cells at lesion rims could be consequences of tissue injury, not initiators.
- Focusing on rim lesions risks underrepresenting spinal cord, diffuse grey-matter, and non-rim mechanisms of progression.

## Round 4: Non-obvious connections and intervention reality check

### Connection A: Lupus provides a cellular EBV mechanism worth testing in MS

In SLE, an EBV-specific single-cell platform identified increased `EBV+ CD27+CD21low` memory B cells with `ZEB2`, `TBX21`/T-bet, and antigen-presentation programs; EBNA2 occupied relevant regulatory regions, and recombinant antibodies from EBV-positive SLE B cells bound autoantigens. [Younis et al., 2025](https://doi.org/10.1126/scitranslmed.ady0210)

- **Settled science:** this mechanism was demonstrated in the reported SLE cohort and assays.
- **Speculation for MS:** EBV may similarly convert a rare autoreactive MS B-cell subset into an antigen-presenting, CNS-homing cell state.
- **Why this is useful:** it suggests an assay strategy: detect viral transcripts and autoreactivity within the same B cells, rather than measuring bulk EBV serology.

### Connection B: EBV-driven B-cell homing can connect to lesion-rim T cells without proving human CNS persistence

In humanized mice, EBV expanded oligoclonal `T-bet+CXCR3+` B cells that entered submeningeal brain regions and attracted effector memory CD8, Th1, and Th17 cells; rituximab or CXCR3 blockade reduced CNS infiltration. [Laderach et al., 2025](https://doi.org/10.1038/s41586-025-09378-0)

- **Settled science:** this occurred in the reported humanized-mouse system.
- **Active debate:** applicability to human MS initiation and, especially, progressive disease.
- **Mechanistic connection:** `T-bet+CXCR3+` B cells could be an upstream recruiter of the CD8-rich niches observed at chronic active lesion rims.

### Connection C: A failed EBV-targeting clinical result constrains enthusiasm

The registered Phase 1/2 `ATA188` study targeted EBV-infected cells with allogeneic EBV-specific T cells in progressive MS (`NCT03283826`). Its sponsor reported on 2023-11-08 that the Phase 2 EMBOLD primary endpoint of confirmed disability improvement at 12 months was not achieved. [ClinicalTrials.gov](https://clinicaltrials.gov/study/NCT03283826); [Atara announcement](https://d1io3yog0oux5.cloudfront.net/_088e2a13b1234d81caa03c8e6a1d48fb/atarabio/news/2023-11-08_Atara_Biotherapeutics_Announces_Primary_Analysis_330.pdf)

- **Settled science:** the reported primary endpoint was not achieved.
- **Active debate:** whether this falsifies ongoing EBV involvement, because target engagement in the CNS, relevant disease stage, cellular product potency, and endpoint sensitivity are not resolved by the announcement alone.
- **Constraint:** a simple claim that eliminating EBV-infected cells should reverse established progressive MS is not supported.

### Current causal diagram

```text
Primary EBV infection / EBV immune control defect
        |
        |  [settled upstream association; mechanisms debated]
        v
EBNA1 cross-reactivity and/or EBV-reprogrammed T-bet+CXCR3+ B cells
        |
        |  [human mimicry evidence; mouse homing evidence]
        v
CNS/meningeal recruitment or retention of B cells and EBV/LCL-reactive T cells
        |
        |  [CSF support; tissue EBV reservoir disputed]
        v
CD8-rich lesion-rim niche -> IFN/complement/lipid-handling-stressed microglia
        |
        |  [human spatial evidence; bridge untested]
        v
Chronic active lesion expansion, axonal loss, progressive disability
```

### Self-critique after Round 4

- The SLE analogy can mislead: SLE is systemic and autoantigen context differs from CNS disease.
- A mouse CNS-homing mechanism is a bridge candidate, not human proof.
- The ATA188 failure could mean the EBV-reservoir model is wrong, or merely that established lesions become self-sustaining; both interpretations remain possible without target-engagement data.
- The focus has shifted from an infectious reservoir to a cell-state circuit because it fits more evidence, but that shift makes intervention targets less obvious and demands paired human data.

# Phase 3: Synthesis

## Working synthesis

**Primary synthesis, active debate/speculation:** EBV may contribute to MS progression indirectly by generating or expanding CNS-homing, antigen-presenting B-cell states and EBV/LCL-reactive T-cell clones. These cells may promote a CD8-rich inflammatory microenvironment that pushes lesion-rim microglia into interferon/complement-activated and lipid-clearance-impaired states. A persistent CNS EBV reservoir is one possible amplifier, but it is not required by the current evidence.

This synthesis is deliberately weaker than "EBV drives progressive MS": it specifies the cell states and spatial readouts needed to reject or support the bridge.

## Hypothesis 1: EBV-imprinted CSF immunity predicts chronic active lesion biology

**Hypothesis (speculation):** In early untreated MS, high CSF abundance of `T-bet+CXCR3+` B cells and EBV/LCL-reactive expanded TCR clones predicts development or persistence of paramagnetic rim lesions (PRLs) over 24 months.

**Design**

- Enrol `n=150` untreated participants with clinically isolated syndrome or early relapsing MS before disease-modifying therapy where ethically and practically feasible; longitudinal analysis must account for subsequently initiated therapy.
- Add `n=50` non-inflammatory neurological controls for baseline CSF immune-state comparison; they are not used for PRL prediction.
- At baseline: paired CSF/blood single-cell RNA-seq plus V(D)J/TCR sequencing, spectral flow cytometry for `CD19/CD27/CD21/T-bet/CXCR3`, EBV-targeted RNA/DNA assay in B cells, EBNA1/GlialCAM antibody assays, and EBV/LCL-reactive TCR mapping.
- At baseline, 12, and 24 months: standardized 3T susceptibility/QSM MRI for PRLs, new lesions, and slowly expanding lesion measures; serum neurofilament light as secondary readout.
- Primary endpoint: new or persistent PRL at 24 months.

**Expected result if true**

- Participants in the upper tertile of the joint CSF signature have a PRL endpoint rate of at least `45%`, versus at most `20%` in the lowest tertile, corresponding to an approximate risk ratio of `>=2.25`.
- This magnitude is intentionally set above a weak biomarker association; roughly 50 participants per tertile is adequate for an initial detection of this difference, subject to adjustment for therapy and baseline lesion burden.

**Falsification criterion**

- Falsified for practical purposes if the pre-registered joint CSF signature has adjusted risk ratio `<1.3` for PRL outcome with a 95% confidence interval excluding `2.0`, or if a signature is present only in blood and not enriched in CSF.

**Main confounders**

- Treatment initiation after sampling; disease activity at baseline; HLA genotype; MRI acquisition variability; LCL reactivity not uniquely proving EBV antigen recognition.

## Hypothesis 2: EBV programs a CNS-homing antigen-presenting B-cell state through EBNA2/T-bet/CXCR3

**Hypothesis (speculation grounded by the SLE and humanized-mouse analogy):** EBV infection of susceptible MS-derived memory B cells induces an `EBNA2 -> TBX21/CXCR3` antigen-presenting program that enhances migration across a blood-brain-barrier model and recruits inflammatory T cells.

**Design**

- Obtain B cells and autologous T cells from `n=24` untreated MS donors enriched for `HLA-DRB1*15:01` and `n=24` age/sex/EBV-serostatus-matched controls. This supports paired within-donor perturbation and provides about 80% power for a paired standardized effect around `0.6`.
- Generate low-passage EBV-infected B cells using a characterized virus stock; compare with mock-exposed and CMV-antigen-stimulated controls.
- Perturbations: CRISPR interference or degron-based suppression of `EBNA2`; CRISPR knockout or antibody blockade of `CXCR3`; `TBX21` knockdown.
- Readouts: scRNA-seq/ATAC-seq for B-cell state, EBV transcript quantification, antigen presentation markers, transendothelial migration through iPSC-derived BBB chips, and recruitment/activation of autologous CD8/Th1 cells.

**Expected result if true**

- EBV exposure produces at least a `2-fold` increase in `T-bet+CXCR3+` B-cell frequency and at least a `50%` increase in BBB-chip migration in MS donors relative to mock.
- `EBNA2`, `TBX21`, or `CXCR3` disruption reduces migration and T-cell recruitment by at least `50%` relative to EBV-infected unperturbed cells.

**Falsification criterion**

- Falsified if EBV does not induce the cell state or migration above mock/virus-control levels, or if the nominated pathway perturbations leave migration and T-cell recruitment unchanged within a pre-specified equivalence margin of `+/-15%`.

**Interpretive limitation**

- Even a positive result demonstrates a route to CNS entry, not chronic lesion persistence in people.

## Hypothesis 3: EBV-conditioned adaptive cells drive lesion-rim lipid-stressed microglia through IFN/complement signalling

**Hypothesis (speculation):** EBV-conditioned B/T-cell interactions induce a lesion-rim-like microglial state characterized by interferon response, complement activation, and impaired cholesterol efflux; this state does not require ongoing infection of microglia or oligodendrocytes.

**Design**

- Use autologous immune cells from `n=20` MS donors and `n=20` matched controls, with repeated conditions per donor.
- Co-culture EBV-conditioned `T-bet+CXCR3+` B cells plus recruited CD8 T cells with iPSC-derived human microglia exposed to standardized myelin debris in a tri-culture including oligodendrocytes/astrocytes.
- Perturbations: B-cell removal; `IFNG` neutralization; C1q blockade; combined intervention; `ABCA1/G1` rescue via CRISPR activation or cholesterol-efflux-enhancing perturbation.
- Readouts: scRNA-seq similarity score to the human Feng/Absinta lesion-rim microglial states, lipid-droplet imaging, cholesterol efflux, C1q/C3 deposition, myelin/axon injury measures, and cytokines.

**Expected result if true**

- MS EBV-conditioned adaptive cells raise the human lesion-rim microglial signature score by `>=1` standardized unit and lipid-droplet burden by `>=50%` versus mock-conditioned immune cells.
- Blocking `IFNG` and/or complement reduces signature score and lipid accumulation by `>=40%`; restoring cholesterol efflux reduces injury despite continued adaptive-cell presence.

**Falsification criterion**

- Falsified if adaptive-cell conditioning does not alter microglial state compared with controls, or if the lesion-rim signature is driven entirely by myelin debris and is unaffected by removal or blockade of adaptive-cell signals.

**Why this hypothesis matters**

- A negative result would detach EBV-linked immunity from the strongest current progression-associated cellular niche, forcing a pivot toward autonomous microglial aging/metabolic failure or other upstream drivers.

## Hypothesis 4: CNS EBV reservoir and EBV-imprinted-but-virus-negative inflammation are distinguishable human pathologies

**Hypothesis (two-sided discriminating hypothesis, active debate):** Only a subset of progressive MS tissue contains detectable EBV-infected meningeal B cells; however, EBV/LCL-reactive T-cell clonotypes and `T-bet+CXCR3+` B-cell states may associate with adjacent chronic pathology even in EBV-negative tissue.

**Design**

- Multicentre rapid-autopsy collection: `n=30` secondary progressive MS cases with high meningeal inflammation, `n=20` progressive MS cases with low meningeal inflammation, and `n=20` non-neurological controls. Sampling must include meninges, adjacent cortex, PRL-corresponding white matter where ante-mortem MRI is available, and cervical lymph nodes where obtainable.
- Blind pathology teams to disease/tissue inflammation strata during viral detection.
- Orthogonal viral assays: EBER in situ hybridization, EBV DNA digital droplet PCR, latent/lytic protein multiplex immunostaining with rigorously verified controls, and targeted spatial transcript detection.
- Immune-state assays: spatial transcriptomics/CODEX or equivalent protein imaging, BCR/TCR repertoire linkage, ex vivo reconstructed antibodies/TCR testing against EBV-infected autologous B cells and candidate CNS antigens.

**Expected result if the proposed bridge is correct**

- If reservoir-dependent: EBV-positive B cells are at least `3-fold` enriched in high-inflammation progressive MS meninges versus controls and spatially co-localize with EBV/LCL-reactive T cells and adjacent glial injury.
- If reservoir-independent: EBV-positive cells are absent or rare without enrichment, but EBV/LCL-reactive clonotypes or EBV-imprinted B-cell states remain enriched near chronic pathology.

**Falsification criterion**

- The overall EBV-imprinted bridge is weakened substantially if neither orthogonally verified EBV-positive cells nor EBV/LCL-reactive or EBNA1/CNS-cross-reactive immune clonotypes/states are enriched in inflamed progressive MS compartments relative to controls.
- The **CNS-reservoir model alone** is falsified if sensitive blinded orthogonal assays show no enrichment of EBV-positive cells despite adequate positive controls and tissue sampling.

**Reason this is included**

- This experiment prevents the program from treating a controversial tissue finding as fact. It can redirect effort to reservoir-dependent intervention, reservoir-independent autoimmunity, or away from EBV in progression.

## Hypothesis priority

| Priority | Hypothesis | Reason |
|---|---|---|
| 1 | Hypothesis 1 | Least assumption-heavy human bridge test; can justify or terminate deeper mechanistic work. |
| 2 | Hypothesis 4 | Resolves the major contradiction concerning tissue EBV and progression compartments. |
| 3 | Hypothesis 2 | Provides intervention-ready cellular mechanism if the human association is present. |
| 4 | Hypothesis 3 | Mechanistically most ambitious; best undertaken after confirming that EBV-imprinted immunity tracks PRL biology. |

## Stopping and pivot rules

1. If Hypothesis 1 fails, deprioritize EBV as a progression driver even if it remains an MS trigger; pivot to intrinsic glial/metabolic drivers of chronic lesions.
2. If Hypothesis 1 succeeds but Hypothesis 4 finds no CNS EBV enrichment, discontinue reservoir-depletion-first thinking and focus on persistent autoreactive/imprinted immune circuits.
3. If Hypothesis 4 strongly supports a reservoir but EBV-targeted interventions show no target engagement or immune-niche change, distinguish delivery failure from wrong causality before any efficacy trial.

## Self-critique after synthesis

- The program is enriched for mechanisms connecting published results; it may miss independent drivers such as mitochondrial injury, iron biology, aging, meningeal fibrosis, or spinal pathology.
- Hypothesis 1 remains correlational. Even a successful predictor does not show that EBV-imprinted cells cause PRLs.
- Hypotheses 2 and 3 use reductionist models; CNS trafficking and lesion evolution in humans are more complex.
- The expected effect sizes are intentionally chosen as biologically meaningful pilot thresholds, not claimed from prior data.

# Phase 4: Meta-Reflection

## Confidence assessment

| Output | Confidence | Basis and boundary |
|---|---|---|
| EBV is a major upstream MS risk factor that precedes disease onset. | High | Prospective longitudinal human data with unusually large risk increase; this does not specify mechanism. |
| EBNA1/CNS molecular mimicry contributes in at least a subset of MS. | Moderate-high | Initial mechanistic Nature study and larger 2025 antibody replication; not universal or proven to drive progression. |
| Intrathecal B-cell and EBV/LCL-reactive T-cell responses are relevant in MS. | Moderate | Multiple CSF studies; key EBV/LCL TCR study has only eight early MS participants and antigen specificity remains ambiguous. |
| Persistent EBV-infected CNS/meningeal cells sustain progressive MS. | Low-moderate | Directly conflicting pathology literature; requires a harmonized orthogonal study. |
| CD8/microglial lipid-stress lesion niches are linked to chronic active lesions. | Moderate-high | Human spatial/transcriptomic studies with model perturbation support; causal order in humans not proven. |
| EBV-imprinted B/T cells drive the chronic active lesion niche. | Low | This is the central proposed bridge and has not been tested in paired human compartments. |

## What was difficult

1. **Separating initiation from progression.** The best EBV evidence concerns risk and early immune responses; the selected unmet problem concerns chronic progression.
2. **Interpreting tissue EBV claims.** The positive and negative pathology studies cannot be responsibly collapsed into a single conclusion.
3. **Avoiding an unfalsifiable model.** A theory in which EBV first triggers disease, sometimes persists, and later becomes unnecessary can explain any result unless the program sets stopping rules.
4. **Using new evidence conservatively.** The 2025 studies make a bridge biologically plausible, but joining two separate papers is inference, not a result.

## What I would do with more time or tools

1. Build a systematic evidence table with formal inclusion criteria for all human tissue studies of EBV in MS, extracting tissue preservation, viral assays, controls, disease subtype, and blinding.
2. Reanalyse public single-cell/spatial datasets from chronic active lesions for `CXCR3`, `TBX21`, interferon, complement, and antigen-presentation modules, while acknowledging that EBV transcripts may be too rare for discovery datasets.
3. Obtain the supplementary datasets from the 2025 Nature and Immunity papers and check whether their cellular signatures can be made comparable without inappropriate batch integration.
4. Seek paired ante-mortem MRI, CSF, and postmortem tissue resources, because the hardest gap is connecting immune specificity to the actual PRL tissue niche.
5. With wet-lab access, begin with the blinded orthogonal pathology design and the lower-risk prospective CSF/PRL cohort rather than launching an intervention.

## Final assessment

The most defensible research direction is not "eradicate EBV to cure progressive MS." It is to determine whether an **EBV-imprinted adaptive immune state** identifies and mechanistically feeds the **CD8/microglial chronic active lesion niche**. The proposal survives the major contradiction in the literature because it explicitly tests both reservoir-dependent and reservoir-independent versions. It also has clear failure modes: if EBV-imprinted cells do not associate with PRLs or inflamed progressive compartments, EBV should be deprioritized as a driver of progression even if it remains central to disease initiation.

# Verified Source Ledger

Primary sources and registry/report used in this log:

1. Bjornevik K, et al. *Science*. 2022. Longitudinal analysis reveals high prevalence of Epstein-Barr virus associated with multiple sclerosis. [DOI](https://doi.org/10.1126/science.abj8222)
2. Lanz TV, et al. *Nature*. 2022. Clonally expanded B cells in multiple sclerosis bind EBV EBNA1 and GlialCAM. [DOI](https://doi.org/10.1038/s41586-022-04432-7)
3. Sattarnezhad N, et al. *PNAS*. 2025. Antibody reactivity against EBNA1 and GlialCAM differentiates multiple sclerosis patients from healthy controls. [DOI](https://doi.org/10.1073/pnas.2424986122)
4. Colombo M, et al. *J Immunol*. 2000. Accumulation of clonally related B lymphocytes in the cerebrospinal fluid of multiple sclerosis patients. [PubMed](https://pubmed.ncbi.nlm.nih.gov/10679121/)
5. Greenfield AL, et al. 2019. Longitudinally persistent cerebrospinal fluid B cells can resist treatment in multiple sclerosis. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6482992/)
6. Gottlieb A, et al. *PNAS*. 2024. Expanded T lymphocytes in the cerebrospinal fluid of multiple sclerosis patients are specific for Epstein-Barr-virus-infected B cells. [DOI](https://doi.org/10.1073/pnas.2315857121)
7. Serafini B, et al. 2010. Epstein-Barr virus latent infection and BAFF expression in B cells in the multiple sclerosis brain. [PubMed](https://pubmed.ncbi.nlm.nih.gov/20535037/)
8. Willis SN, et al. *Brain*. 2009. Epstein-Barr virus infection is not a characteristic feature of multiple sclerosis brain. [DOI](https://doi.org/10.1093/brain/awp200)
9. Magliozzi R, et al. 2010. A gradient of neuronal loss and meningeal inflammation in multiple sclerosis. [PubMed](https://pubmed.ncbi.nlm.nih.gov/20976767/)
10. Absinta M, et al. *JAMA Neurol*. 2019. Association of chronic active multiple sclerosis lesions with disability in vivo. [PubMed](https://pubmed.ncbi.nlm.nih.gov/31403674/)
11. Absinta M, et al. *Nature*. 2021. A lymphocyte-microglia-astrocyte axis in chronic active multiple sclerosis. [DOI](https://doi.org/10.1038/s41586-021-03892-7)
12. Feng R, et al. *Immunity*. 2025. Single-cell spatial transcriptomic profiling defines a pathogenic inflammatory niche in chronic active multiple sclerosis lesions. [DOI](https://doi.org/10.1016/j.immuni.2025.10.003)
13. Younis S, et al. *Science Translational Medicine*. 2025. Epstein-Barr virus reprograms autoreactive B cells as antigen-presenting cells in systemic lupus erythematosus. [DOI](https://doi.org/10.1126/scitranslmed.ady0210)
14. Laderach F, et al. *Nature*. 2025. EBV induces CNS homing of B cells attracting inflammatory T cells. [DOI](https://doi.org/10.1038/s41586-025-09378-0)
15. ClinicalTrials.gov. Phase 1/2 study of ATA188 in progressive MS, `NCT03283826`. [Registry record](https://clinicaltrials.gov/study/NCT03283826)
16. Atara Biotherapeutics. 2023-11-08. Primary analysis data announcement for Phase 2 EMBOLD. [PDF](https://d1io3yog0oux5.cloudfront.net/_088e2a13b1234d81caa03c8e6a1d48fb/atarabio/news/2023-11-08_Atara_Biotherapeutics_Announces_Primary_Analysis_330.pdf)
