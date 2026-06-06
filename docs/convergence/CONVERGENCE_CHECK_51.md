# Convergence Check 51: Accessible-State Rerank

Timestamp: 2026-05-27 20:05 CEST

## Forcing Question

After closing direct lipid enzymes, FABP5, and GPR183, what route remains that
is not just a lipid marker and not a generic cytokine/HLA axis?

## New Evidence

Wave94 reranked `46` accessible or manually retained state candidates using:

- MS white-matter expression;
- broad h5ad cross-disease recurrence;
- myeloid versus tissue-resident localization;
- IBD, RA, and psoriasis treatment-response direction;
- target-resolution/genetics summaries;
- existing Geneformer outputs;
- surface/secreted/transmembrane targetability;
- hard penalties for already closed and generic immune routes.

## Agreement Across Tracks

The lipid-lysosomal module is still real as a disease-associated state, but it
is not yielding a clean direct target. The strongest remaining signals split
into three different classes:

- `SEL1L3`: best statistical rerank, membrane protein, low prior saturation,
  but nearly no mechanism.
- `NRCAM`: consistent response-marker behavior across IBD/RA/psoriasis and MS
  tissue signal, but neural adhesion/safety concerns.
- `C15ORF48`: strongest mechanistic immunometabolic story and myeloid/tolerance
  plausibility, but not a conventional druggable surface target and absent from
  the current Geneformer token dictionary.

## Disagreement

The rerank does not point back to the original lipid-lysosomal myeloid module
as a direct intervention axis. `APOC1`, `LPL`, `GPNMB`, `APOE`, and `FABP5`
all fail by direction conflict, prior art, or weak targetability.

## Decision

Proceed to a Wave95 mechanistic triage comparing `SEL1L3`, `NRCAM`,
`C15ORF48`, and `CD200`.

The ranking alone is insufficient. The next branch must answer:

- Is the candidate a causal controller or a tissue-damage marker?
- Is there a plausible intervention modality?
- Is prior art already blocking the exact autoimmune use?
- Does the mechanism connect back to demyelination/progression or to a
  transferable cross-autoimmune treatment strategy?
