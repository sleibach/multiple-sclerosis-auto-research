# Reframe V3: Cross-Autoimmune Lipid-Lysosomal Myeloid Mechanism

**Started:** 2026-05-26 18:41 UTC  
**Working directory:** `/Users/soeren.leibach/Projects/ms-auto-research`

## Starting Point

The V2 session demoted `ACSL1` from therapeutic target to marker/perturbation hypothesis. The useful surviving signal was not a single enzyme but a recurrent inflammatory myeloid program with lipid handling, lysosomal activation, complement/phagocytosis, and tissue-injury features across MS, RA, IBD, psoriasis, lupus, and Sjogren-accessible datasets. `NAMPT` was the top V2 successor target by simple scoring, but broad prior art and direction ambiguity blocked a therapeutic nomination.

## Core Reframe

The V3 question is no longer "can ACSL1 be rescued?" or "is NAMPT the target?" It is:

> Within the cross-autoimmune lipid-lysosomal inflammatory myeloid state, what node or state transition is the broadest mechanistic anchor, and what druggable intervention point can modulate it without collapsing tissue repair?

This is a breadth-first target-resolution problem. The central node may be a gene (`IFI30`, `GPNMB`, `CTSD`, `SPP1`, `NAMPT`, `LIPA`, `C1Q`, `CXCL10`), a regulator (`TFEB`, `PPAR/LXR`, `HIF1A`, `STAT1/IRF`, `NF-kB`, `NRF2`), or a transition (homeostatic/reparative macrophage to lipid-lysosomal inflammatory macrophage). It must be selected by convergence across diseases and modalities, not by narrative appeal.

## Track Allocation

### Primary Track: Cross-Disease Module Resolution

Priority is assigned to breadth across autoimmune diseases, then to mechanistic specificity. The first-pass disease set is:

- multiple sclerosis
- rheumatoid arthritis
- systemic lupus erythematosus and lupus nephritis
- Crohn's disease
- ulcerative colitis
- psoriasis
- type 1 diabetes
- Sjogren's syndrome
- ankylosing spondylitis
- myasthenia gravis
- autoimmune thyroid disease
- celiac disease
- primary biliary cholangitis

Rationale: V2 already found that a single-disease MS-only target ranking overfits. A node that recurs across diverse autoimmune tissues while preserving tissue-specific context is more likely to be a causal inflammatory-state controller or a broadly actionable drug-discovery node.

### Secondary Track: Foundation-Model Perturbation

State/Stack/Evo 2 or comparable models will be used only if they can be installed or accessed with documented versions, inputs, and outputs. If Arc models cannot run locally on this macOS CPU/Python 3.13 environment, the fallback hierarchy is:

1. Use official hosted/API or container route if available and traceable.
2. Use comparable open cell foundation models (`scGPT`, `Geneformer`, `scFoundation`, `UCE`, or `CellPLM`) only if weights can be obtained and actual inference can be run.
3. If no foundation model can run, document blocker and use real perturbation datasets plus transparent linear/network perturbation models as non-foundation substitutes. These substitutes do **not** satisfy the foundation-model DoD by themselves.

Rationale: fabricated model outputs are worse than no model. The value comes from actual perturbation prediction that can be checked against real perturbation data.

### Tertiary Track: Intervention-Point Search

The target does not have to be the central node itself. If the central node is a damaging state marker or high-liability hub, the intervention point can be an upstream regulator, downstream effector, receptor-ligand interaction, enzyme, transporter, or modality that safely pushes the state transition.

## Rejected Alternatives

### Reject: Continue ACSL1 as Lead

Reason: V2 showed `ACSL1` loses incremental value after module adjustment in MS foamy proteomics (`p=0.136`) and partial ACSL1 inhibition worsened model lesion dynamics under explicit assumptions. It remains useful as a state marker and comparator, not a lead.

### Reject: Promote NAMPT Immediately

Reason: V2 NAMPT evidence was broad, but prior art around NAMPT/FK866/visfatin in MS/EAE and autoimmunity is extensive. NAMPT may still be a central node, but a V3 therapeutic claim must find a more specific modality, context, or downstream pathway that avoids old claims and NAD-toxicity ambiguity.

### Reject: Bulk Signature Correlation as Primary Test

Reason: The execution-phase failure showed that bulk-style scores can satisfy a plan while missing cell-cell and compartment mechanisms. V3 will use bulk data only for breadth screening; central claims require cell-type or tissue-state validation, genetics, perturbation, or model-based support.

### Reject: GWAS Overlap Without Colocalization/MR Validation

Reason: autoimmune diseases share immune loci for many reasons. Mere overlap is not genetic anchoring. Genetic claims require locus-level evidence, validated instruments, colocalization where summary statistics allow it, or cautious labeling as "genetic neighborhood only."

## Decision Criteria

Promote a central-node candidate only if it satisfies all of:

- recurrent signal in at least five autoimmune diseases;
- at least three evidence channels in the leading diseases, not three re-analyses of the same expression data;
- MS evidence in at least two modalities;
- mechanistic plausibility that distinguishes state driver from tissue-injury marker;
- perturbation prediction or real perturbation data indicating that modulating the node reverses the harmful state without simply killing myeloid cells;
- tractable intervention point with prior-art room for the specific autoimmune use.

## Initial Candidate Families

The first-pass search will not assume one target. It will rank:

- lysosomal antigen-processing nodes: `IFI30`, `CTSD`, `CTSB`, `TPP1`, `LAMP1`;
- lipid handling and lipid droplet nodes: `ACSL1`, `LIPA`, `PLIN2`, `APOE`, `LPL`, `GPNMB`;
- macrophage activation and tissue remodeling nodes: `SPP1`, `TREM2`, `MERTK`, `MARCO`, `MSR1`, `CD36`;
- inflammatory metabolic nodes: `NAMPT`, `HIF1A`, `SLC2A1`, `LDHA`;
- interferon/chemokine/complement nodes: `CXCL10`, `C1QA/B/C`, `STAT1`, `IRF1/7`, `TNF`, `IL1B`;
- regulatory programs: `TFEB/TFE3`, `LXR/PPARG`, `NRF2`, `NF-kB`, `HIF1A`, `STAT1/IRF`.

## Immediate Forcing Question

By the first convergence checkpoint, the run must answer:

> Is the cross-autoimmune lipid-lysosomal myeloid module best anchored by lysosomal antigen processing, lipid overload/efflux, interferon-chemokine activation, or metabolic inflammatory licensing?

If the evidence does not separate these axes, the next pivot is to cell-state transition modeling rather than single-gene nomination.
