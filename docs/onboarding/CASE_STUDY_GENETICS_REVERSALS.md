# Case Study: When Attractive Genetics Leads Reversed

A disease-associated region can be real while its most familiar gene is not
the causal gene. A protein can have a plausible binding pocket while the useful
therapeutic direction is still unknown or technically difficult. These are not
minor caveats; they are separate links in the target argument.

This page retells the project's GPR25/KIF21B and PTGER4 trajectories. It adds
no new scientific claim. `[G03-G05]`

## The Short Version

Two apparently attractive routes became less actionable under harder tests:

- **GPR25:** a receptor at a shared MS-ulcerative-colitis region looked like a
  familiar target class. Allele alignment then showed that the potentially
  protective direction was higher expression or signaling, not simple
  inhibition. Later immune-QTL and cell-state checks supported nearby KIF21B
  more strongly than GPR25 in several contexts. GPR25 became a conditional
  causal candidate, not a protected favorite. `[G03, G05]`
- **PTGER4:** a known receptor near an MS-ulcerative-colitis region looked
  tractable. Signal decomposition showed shared and distinct genetic
  components with conflicting disease-direction implications. Receptor
  tractability could not turn that conflict into one safe intervention
  direction. The naive transfer-target route closed. `[G04]`

Neither correction says the regions are biologically imaginary. Both say the
chain from region to intervention is incomplete.

## The Four Links A Target Needs

```text
disease region
    -> causal gene
        -> protective biological direction
            -> modality that can safely create that direction
```

A strong first link does not automatically supply the other three.

| link | question | common shortcut |
|---|---|---|
| Region | Is a genetic signal credibly associated with disease? | “The nearest or most familiar gene is the target.” |
| Gene | Which gene and cell state carry the relevant signal? | “The receptor-shaped candidate wins because receptors are druggable.” |
| Direction | Would benefit require more function, less function, or a context-specific change? | “Any modulation should help.” |
| Modality | Can an intervention create that direction with acceptable selectivity and safety? | “A pocket means an actionable medicine.” |

## Reversal 1: GPR25 Was The Attractive Favorite

### Why It Looked Good

The chr1 region showed shared MS and ulcerative-colitis genetics. GPR25 sat in
the credible block, had strong blood expression-QTL support in the earlier
analysis, and belonged to a receptor class familiar to drug developers.

That combination made a coherent first story:

> Shared region + receptor-like protein = plausible shared target.

The story was useful enough to test. It was not enough to nominate a target.

### First Correction: The Direction Reversed

Allele-aligned GTEx and eQTLGen work showed that alleles associated with higher
GPR25 expression were protective for both MS and ulcerative colitis. The
earlier proxy direction was wrong. `[G03, G05]`

If GPR25 is causal, a direction-matched intervention would therefore need to
raise or restore GPR25 expression/signaling. A conventional blocker would not
follow the genetic direction.

This made the hypothesis more precise and harder:

```text
not: block GPR25
but: establish that GPR25 is causal, then restore or increase its useful state
```

### Second Correction: The Gene Was Not Resolved

Denser public immune-QTL and expression checks did not produce new GPR25 target
support. GPR25 was absent or trace in the available cell-state scans, while
nearby KIF21B gained independent dense immune-QTL and expression support.
`[G03, G05]`

This did not prove that KIF21B alone carries the region. It removed the reason
to protect GPR25 from local alternatives merely because it looked easier to
drug.

### Third Correction: Shape Did Not Repair Direction

Predicted-structure context supports a plausible receptor-like GPR25 core. That
is useful context about physical tractability, not project-grounded evidence
that GPR25 causes MS or that increasing its activity is safe and beneficial.
`[G03]`

The lead stayed demoted because the structure did not provide:

- signal-specific causal-gene resolution;
- strong presence in an MS-relevant cell state;
- functional evidence that restoration creates a protective phenotype; or
- mature agonist/restoration chemistry.

### What Would Reopen GPR25

All of the following are needed before dedicated target work is justified:

1. Genotype-linked expression or surface-protein data showing that the
   protective chr1 haplotype raises GPR25 in an MS-relevant immune or CSF cell
   state.
2. Evidence that GPR25 fits the disease signal better than KIF21B and other
   local genes.
3. A restoration, agonist, positive-allosteric, or equivalent perturbation
   that moves an MS-relevant phenotype in the protective direction.
4. A plausible modality that can create that direction, rather than merely
   occupy a receptor pocket. `[G03, G05]`

Until then, GPR25 remains a controlled-data handoff, not an MS therapeutic
candidate.

## The KIF21B Contrast

KIF21B was initially easier to discount because kinesins are often treated as
difficult targets. Harder review corrected that class bias too. Dense
immune-QTL evidence and exact shared-variant direction made KIF21B a serious
causal candidate, and its motor region is not structurally featureless.
`[G03]`

But its likely protective direction is also restoration or increased
function. Inhibition, degradation, knockdown, or other loss-of-function
approaches would probably move opposite to the locus-implied direction.

The balanced conclusion is therefore:

- do not ignore KIF21B because it is a kinesin;
- do not promote it because a modeled domain could bind something;
- resolve the causal gene and cell state; and
- require a credible up-function modality before target work.

The region remains real biology and a hard-target handoff. It is not an
intervention-grade lead. `[G03]`

## Reversal 2: PTGER4 Was Druggable But Direction-Conflicted

### Why It Looked Good

PTGER4 offered a familiar receptor and a shared autoimmune-disease region. It
was easy to imagine transferring receptor pharmacology across diseases.

### The Harder Test

Signal decomposition found both a strongly shared component and a strongly
distinct component at the region. Allele-aligned expression-QTL work then
showed opposite disease-direction implications across those components.
`[G04]`

The problem was no longer “can PTGER4 be modulated?” It was:

> Which signal, in which cell state, for which disease, requires which PTGER4
> direction?

A generic agonist or antagonist answer would combine effects that the genetics
had separated.

### Why Tractability Could Not Rescue It

A structurally interpretable receptor and existing pharmacology can answer
whether modulation is physically conceivable. They cannot determine which
genetic component is causal for MS, whether comparator-disease direction
transfers, or which intervention direction is protective in the relevant MS
cell state. `[G04]`

PTGER4 therefore closed as a **naive shared-disease transfer target**. That is
narrower and more accurate than saying PTGER4 has no biology.

### What Would Reopen PTGER4

A future package must supply all four links:

1. **Signal decomposition:** credible sets and posterior support that separate
   the shared and distinct components.
2. **Cell-state direction:** allele-aligned expression, protein, or activity
   data showing the MS-protective PTGER4 direction in a relevant cell state.
3. **Disease-layer match:** direct MS evidence rather than transfer from Crohn
   disease, ulcerative colitis, or generic receptor biology.
4. **Modality fit:** agonism, antagonism, biased signaling, or another approach
   matched to the resolved protective direction and safety context. `[G04]`

If the components still imply conflicting intervention directions, the route
stays closed.

## What The Project Learned

### Druggability Is Directional

“Can bind a molecule” and “can create the genetically protective state” are
different questions. The second is the therapeutic question.

### Familiar Protein Classes Can Bias Prioritization

GPR25 and PTGER4 initially benefited from receptor familiarity. KIF21B was
penalized by kinesin-class difficulty. Direct evidence corrected both biases.
`[G03-G05]`

### A Real Locus Is Not A Drug Nomination

Regional association can survive while target status closes. That is not a
contradiction. It means the project knows something about disease biology but
not yet how to intervene safely.

### Reopening Requires New Information

Repeating that a receptor has a pocket, that a region associates with disease,
or that another disease uses the same pathway does not reopen these routes.
The new evidence must resolve the missing link that caused closure.

## A Checklist For New Target Ideas

Before proposing a target from genetics, answer:

1. Which exact signal is being interpreted?
2. Is there more than one causal component?
3. Which gene wins over local alternatives?
4. In which cell state is that gene linked to the signal?
5. Which allele is protective, and what does it do to expression or function?
6. Does the proposed modality increase, decrease, restore, relocate, or bias
   signaling in that same direction?
7. What experiment could show the direction is wrong?
8. What evidence would keep the region biologically interesting while closing
   the intervention route?

That last question matters. It lets data close a target without forcing the
project to deny real regional biology.

## Trace The Evidence

- [chr1 KIF21B/GPR25 re-evaluation](../workups/genetics/GENETICS_CHR1_REEVALUATION_V19.md)
- [Allele-aligned GPR25 and PTGER4 workup](../workups/genetics/GENETICS_EQTL_WORKUP_V16.md)
- [Therapeutic-path synthesis](../reports/THERAPEUTIC_PATH_V52.md)
- [GPR25 direction-matched reopen specification](../workups/genetics/GPR25_DIRECTION_MATCHED_MODALITY_SPEC_V52.md)
- [PTGER4 signal-specific reopen specification](../workups/genetics/PTGER4_SIGNAL_SPECIFIC_REOPEN_SPEC_V52.md)
- [Claim-source contract](CLAIM_SOURCE_MATRIX_V55.md), rows `G03-G05`
