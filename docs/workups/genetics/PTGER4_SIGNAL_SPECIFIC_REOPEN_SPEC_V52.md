# PTGER4 Signal-Specific Reopen Specification V52

Date: 2026-07-10

Status: future evidence gate. PTGER4 remains closed as a naive MS/IBD transfer
target; this document defines what would be required before revisiting that
status.

## Current Closed-State Rationale

PTGER4 is not closed because it is structurally or pharmacologically
uninteresting. It is closed because the project evidence is not direction-clean:

- V14/V15/V16 found a chr5 PTGER4-neighborhood locus with both shared and
  distinct components.
- V16 showed the shared and distinct components have opposite
  disease-direction implications.
- V50 source-specific records strengthened transfer caution: external same-rsid
  rows preserve an MS/Crohn allele contrast, and Crohn-side expression
  modulation does not establish MS-safe direction.
- V52 AlphaFold context confirms receptor-core interpretability, but structure
  does not solve signal decomposition or disease direction.

## What Would Count As Reopen Evidence

All four evidence classes are required before PTGER4 can move from "closed
transfer warning" to "worth dedicated target workup":

| gate | required evidence | minimum acceptable form |
|---|---|---|
| Signal decomposition | Separate the shared and distinct PTGER4-region components. | Fine-mapping or SuSiE/coloc with credible sets and posterior support for each component, matched to MS and comparator trait definitions. |
| Cell-type direction | Define the MS-protective PTGER4 expression or activity direction in the relevant cell state. | Cell-type QTL or genotype-linked expression/protein data with allele, effect direction, ancestry/LD, and metadata. |
| Disease-layer match | Show the direction is relevant to MS, not just Crohn/UC or generic EP4 biology. | MS immune, CSF, lesion-adjacent, or treatment-response data where PTGER4 direction maps to the project disease layer. |
| Modality fit | Identify an intervention direction that matches the protective biology. | Agonism, antagonism, biased agonism, or pathway modulation justified by the resolved signal direction and safety context. |

## What Does Not Count

Do not reopen PTGER4 based on:

- AlphaFold or GPCR structure alone;
- generic EP4 druggability;
- Crohn or UC association without MS direction;
- broad MS/IBD shared-genetics literature;
- external target-database presence;
- an rsid row without strand/effect-convention harmonization;
- pathway plausibility without perturbation or genotype-linked direction.

## Minimum Future Analysis Plan

If the required data arrive, the future analysis must be pre-specified:

1. Freeze the variants/components to be tested before inspecting PTGER4
   target-readout direction.
2. Harmonize allele, strand, phenotype, and effect conventions across MS,
   comparator disease, and QTL/protein data.
3. Score shared and distinct components separately.
4. Test PTGER4 expression/protein direction by cell type and disease layer.
5. Report whether a single intervention direction exists. If the shared and
   distinct components imply conflicting directions, keep PTGER4 closed.
6. Treat any positive result as "worth dedicated target workup," not as a
   therapeutic finding.

## Decision Rule

PTGER4 can be reopened only if the future evidence shows:

`one disease-relevant signal` + `one causal direction` + `one relevant cell
state` + `one plausible modality`.

Anything less preserves the V52 no-go status.
