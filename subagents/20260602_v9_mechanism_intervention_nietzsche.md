# V9 Mechanism / Intervention Convergence Sidecar

Date: 2026-06-02  
Role: mechanism/intervention convergence sidecar  
Scope: MS-centered hypothesis emerging from V8 robust placements plus V9 microbiome/genetics gaps.  
Constraint: report only; no central docs edited.

## Executive Position

The strongest MS-centered mechanism/intervention hypothesis is:

> A subset of MS progression or inflammatory-activity biology is driven by a gut-barrier/microbial-metabolite lesion in which loss or instability of mucosal microbial-immune homeostasis reduces APC plasticity, making IFN/APC antigen-presentation states harder to downshift during tissue repair. The intervention hypothesis is to restore gut-derived barrier/metabolite signaling, especially SCFA/bile-acid/mucin-barrier-linked tone, and use early CSF/lesion-edge or gut-proxy IFN/APC downshift as the pharmacodynamic readout.

This is **not a cure claim**. It is an intervention-program hypothesis: it proposes a modifiable upstream physiology and a falsifiable response-monitoring architecture. It does not claim that microbiome modulation alone reverses MS, prevents EBV-driven initiation, remyelinates lesions, or replaces approved DMTs.

## Why This Is Strongest, Not Just Most Attractive

The V8 map argues against a single pan-autoimmune blood IFN/APC rule. RA is far from MS on blood IFN/APC and treatment-response architecture. That negative result is useful: it says MS should not be treated as generic systemic autoimmunity for this mechanism.

The most stable positive convergence is narrower:

- **IBD proximity to MS is dynamic and tissue-centered.** Crohn and UC are near MS on mucosal IFN/APC and repair/response-monitoring axes.
- **HYP_V7_001 gives a working response architecture.** In IBD mucosa, responders to infliximab show larger early IFN/APC downshift: `GSE16879` AUC `0.754`, Hedges g `0.985`; `GSE73661_IFX` AUC `0.825`, Hedges g `1.390`. Vedolizumab exploratory data in the same UC ecosystem also passes directionally, suggesting mucosal healing/plasticity rather than anti-TNF specificity.
- **UC has supported genetic proximity to MS in V8.** This is the only gut-disease genetics upgrade currently strong enough to use as convergent support. Crohn is intermediate/supported, not near/supported.
- **Microbiome remains a gap, not a support.** V9 has not upgraded microbiome placements. The IBDMDB small subset did not pass FDR for pre-specified families, and MS processed microbiome data are blocked by phyloseq/R export. This prevents a strong microbiome finding, but it identifies the forcing test.

The mechanism should therefore be framed as **gut-barrier/metabolite regulation of APC plasticity**, not as "MS is IBD" and not as "dysbiosis causes MS."

## Proposed Mechanistic Chain

### Step 1 - Gut ecology / barrier input

Claim status: **assumed, not yet supported by V9 primary data**.

Candidate inputs:

- short-chain fatty-acid-producing taxa or pathways;
- bile-acid transformation capacity;
- mucin/barrier stability, including Akkermansia/mucin-linked signals;
- microbial translocation or LPS/endotoxin pressure;
- tryptophan/aryl-hydrocarbon receptor tone.

Current V9 status:

- MS processed microbiome files are downloaded but not yet exported/analyzed due R package/tooling limitations.
- IBDMDB subset analysis is too small and did not meet FDR `<0.10`; examples include CD `prevotella` Hedges g `-0.679`, p `0.147`, FDR `0.728`, and CD `faecalibacterium_butyrate` Hedges g `-0.500`, p `0.259`, FDR `0.728`. These are hypothesis-generating only.

### Step 2 - APC plasticity and IFN/APC downshift capacity

Claim status: **supported in IBD mucosal treatment-response data; unproven in MS**.

The relevant state is the locked IFN/APC module:

`STAT1`, `IRF1`, `CXCL10`, `GBP1`, `ISG15`, `CD74`, `HLA-DRA`.

HYP_V7_001 shows that in inflamed intestinal mucosa, early reduction of this module after treatment tracks response better than baseline height. The vedolizumab specificity check suggests this is not anti-TNF-specific; it may measure tissue healing or APC plasticity.

MS analogue:

- lesion-edge, CSF myeloid, or gut-proxy APC compartments should show measurable IFN/APC plasticity under effective therapy or natural recovery;
- PBMC baseline alone is not a valid surrogate, given RA blood failures and prior MS pregnancy/PBMC confounding.

### Step 3 - Tissue repair / resolution transition

Claim status: **supported as response-monitoring architecture in IBD; speculative in MS lesion repair**.

In IBD, early mucosal IFN/APC downshift plausibly marks transition from inflammatory mucosal injury toward healing. In MS, the analogous transition would be from active/chronic-active lesion edge toward resolution, lower compartmental inflammatory antigen presentation, and permissive remyelination environment.

This must not be overstated. IBD mucosal healing is not remyelination. The transferable object is a **response-monitoring architecture**, not the tissue repair process itself.

### Step 4 - Clinical phenotype

Claim status: **assumed for MS; observed indirectly in IBD response cohorts**.

MS clinical targets where this mechanism is plausible:

- early relapsing MS with gut-barrier/metabolite dysfunction and active inflammatory lesions;
- postpartum or hormonal-transition periods if gut/barrier and APC kinetics are shown to shift;
- progressive or smoldering lesion patients only if CSF/lesion-edge APC plasticity can be measured and linked to progression.

The most defensible lead population is **MS patients with active inflammatory MRI/CSF biology plus gut-barrier/metabolite abnormality**, not unselected progressive MS.

## Intervention Hypothesis

### Intervention class

Not a single drug target yet. The strongest intervention point is:

> Restore microbial-metabolite/barrier signaling that increases APC downshift capacity under standard anti-inflammatory or DMT pressure.

Possible modalities, in descending defensibility:

1. **Biomarker-guided adjunctive microbiome/metabolite intervention.**
   - Examples: diet/prebiotic/resistant-starch strategy, defined microbial consortium, butyrate/SCFA-pathway augmentation, bile-acid-pathway modulation.
   - Advantage: directly targets the V9 gap without claiming a novel immune drug.
   - Risk: weak CNS delivery assumptions and noisy microbiome readouts.

2. **Trialable pharmacodynamic biomarker strategy.**
   - Use gut microbiome/metabolite state plus early CSF/PBMC/gut IFN/APC downshift as enrichment/readout for existing DMT response.
   - Advantage: lower mechanistic burden than claiming microbiome therapy is disease-modifying.
   - Risk: needs paired longitudinal MS samples.

3. **Barrier-immune modulator combination.**
   - Pair a gut/metabolite intervention with an approved MS DMT to test whether the adjunct improves IFN/APC plasticity or repair biomarkers.
   - Advantage: biologically aligned with "plasticity under therapeutic pressure."
   - Risk: high clinical noise; causal attribution difficult.

### What this is not

- Not a cure.
- Not a claim that IBD drugs should be repurposed directly into MS.
- Not a claim that anti-TNF is appropriate in MS.
- Not a generic dysbiosis claim.
- Not a baseline PBMC biomarker claim.
- Not a pan-autoimmune rule including RA blood.

## Evidence Dimensions Needed

### Dimension 1 - Primary MS microbiome/metabolite quantification

Need:

- process the downloaded MS phyloseq RDS files or equivalent MS gut microbiome abundance tables;
- quantify pre-specified families: SCFA/butyrate, bile acid, tryptophan/AHR, LPS/Enterobacteriaceae, mucin/barrier, Akkermansia/Faecalibacterium/Prevotella/Bacteroides;
- compare MS versus matched controls and, if available, before/after B-cell depletion or other therapy.

Pass signal:

- MS shows a reproducible functional-family abnormality that overlaps IBD/T1D more than RA, after medication, age, sex, geography, and stool-processing caveats are addressed.

Stop-loss:

- no stable MS abnormality in these families across two MS microbiome cohorts, or effect-size direction stability below 50%.

### Dimension 2 - IBD full-scale microbiome and mucosal-response linkage

Need:

- replace the 30-sample IBDMDB subset with full or statistically adequate IBDMDB analysis, or use verified machine-readable published feature/effect tables;
- test whether microbial feature families associate with mucosal IFN/APC state or treatment-response dynamics.

Pass signal:

- microbial feature families predict or covary with IFN/APC downshift or mucosal healing in UC/Crohn.

Stop-loss:

- IBD microbial feature families do not associate with IFN/APC downshift in adequate sample size, making the gut-to-APC chain unsupported even in the proxy disease.

### Dimension 3 - MS APC plasticity in relevant compartment

Need:

- paired MS CSF, lesion-edge, or gut biopsy data before/after DMT or during relapse/remission;
- score locked IFN/APC module dynamically;
- avoid PBMC baseline-only inference.

Pass signal:

- effective therapy or recovery produces early IFN/APC downshift in CSF/lesion-edge/gut-proxy APC compartments, preceding MRI/NfL/clinical improvement.

Stop-loss:

- no dynamic IFN/APC downshift in relevant MS compartments under effective therapy, or direction opposite in two independent cohorts.

### Dimension 4 - Genetics / causal anchoring

Need:

- genome-wide genetic correlation for MS with UC/Crohn/RA/SLE/T1D under a consistent source;
- coloc or fine-mapping at gut-barrier/APC/microbial-immune loci;
- avoid target-overlap-only upgrades.

Pass signal:

- UC/MS genetic proximity remains supported and maps to non-HLA loci plausibly connected to barrier/APC/metabolite immune regulation.

Stop-loss:

- UC/MS proximity disappears under proper genome-wide analysis, or shared signals are HLA-only with no barrier/APC/metabolite loci.

### Dimension 5 - Perturbation / intervention model

Need:

- human monocyte/macrophage/DC or gut organoid-immune co-culture perturbation with SCFA/bile-acid/tryptophan/barrier signals;
- measure IFN/APC downshift capacity under inflammatory stimulation.

Pass signal:

- metabolite/barrier intervention reduces IFN/APC module or increases downshift capacity without global cytotoxicity or antiviral IFN collapse.

Stop-loss:

- intervention fails to change IFN/APC dynamics, or only works by nonspecific toxicity/global IFN collapse.

## Specific Falsification Path

### Stage 1 - Computational falsification

Build a harmonized dataset matrix:

1. MS microbiome/metabolite cohort: process `PRJEB44538` GitHub phyloseq RDS files or equivalent accessible abundance table.
2. IBD microbiome cohort: full IBDMDB or sufficiently powered subset.
3. RA/T1D comparator: at least one machine-readable RA or TEDDY/T1D feature table.
4. MS dynamic immune compartment cohort: CSF/lesion/gut-proxy paired DMT or relapse-remission transcriptomes if accessible.

Decision rule:

- Continue only if MS and IBD/T1D share at least two pre-specified microbial functional-family directions and MS has a relevant-compartment IFN/APC dynamic readout.
- Kill as intervention hypothesis if microbiome proximity fails and no MS compartmental APC plasticity dataset supports the dynamic response axis.

### Stage 2 - Ex vivo falsification

Experiment:

- primary human monocyte-derived macrophages/DCs or iPSC microglia;
- inflammatory stimulus: IFN-gamma plus microbial/barrier-relevant co-stimulus;
- interventions: butyrate/SCFA-pathway augmentation, bile-acid receptor modulation, tryptophan/AHR ligand, and negative-control metabolite;
- readouts: locked IFN/APC module, HLA-II/CD74, antiviral IFN core, viability/stress, phagocytosis/efferocytosis optional.

Sample size:

- at least 12 donors per arm for discovery, balanced by sex;
- replication in 12 additional donors or independent cell system before any clinical translation.

Expected effect:

- at least 25-30% reduction in IFN/APC module induction or at least Hedges g `0.70` in downshift capacity versus vehicle, while antiviral IFN/stress/viability controls do not show nonspecific collapse.

Stop-loss:

- effect size below Hedges g `0.30`, or IFN/APC reduction explained by cytotoxicity/global transcriptional suppression, in both discovery and replication.

### Stage 3 - Clinical pilot falsification

Design:

- biomarker-enriched MS observational or adjunctive pilot;
- population: active inflammatory MS or early relapsing MS on standard DMT, enriched for gut-barrier/metabolite abnormality;
- intervention: defined diet/prebiotic/metabolite or microbial-consortium adjunct, not DMT replacement;
- endpoints: gut microbial/metabolite target engagement, CSF/PBMC/gut IFN/APC dynamic change, serum/CSF NfL, MRI inflammatory activity.

Sample size:

- pilot: 40-60 participants for biomarker effect, not clinical efficacy;
- randomized feasibility trial: 80-120 participants if biomarker effect survives.

Expected effect:

- target-engagement shift in microbial/metabolite family;
- early IFN/APC downshift in relevant immune compartment with Hedges g `>=0.50`;
- exploratory reduction in NfL/MRI inflammatory activity, not powered as cure endpoint.

Stop-loss:

- no target-engagement shift, or no immune readout change despite target engagement, or worsening inflammatory/MRI activity signal.

## Most Important Negative Controls

- RA blood anti-TNF cohorts remain negative comparators; do not expect the same rule there.
- Baseline-only UC data failed; require dynamic measurement.
- PBMC-only MS measures are weak proxies unless paired with compartment or clinical kinetics.
- Receptor-only `CD74/CD44/CXCR4` should not outperform the IFN/APC dynamic architecture.
- Microbiome taxa without functional-family mapping should not drive claims.

## Recommended Next Action

Do not write a V9 therapeutic finding yet. The next orchestrator action should be a forcing analysis:

1. finish MS phyloseq export and score pre-specified microbial families;
2. expand IBDMDB beyond the 30-sample subset or use verified machine-readable effect tables;
3. search specifically for paired MS CSF/lesion/gut immune transcriptomics under DMT or relapse/recovery;
4. only then decide whether the gut-barrier/metabolite-to-APC-plasticity intervention hypothesis can advance.

The candidate survives as the strongest **intervention hypothesis** because it integrates the V8 robust placements and the V9 gaps without pretending the gaps are evidence.
