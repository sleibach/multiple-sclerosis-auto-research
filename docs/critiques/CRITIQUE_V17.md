# CRITIQUE_V17

Date: 2026-06-06

Scope: local hostile critique after subagent spawning failed because the agent
thread limit was reached.

## 1. GPR25 Overclaim Risk

The main overclaim risk is treating `GPR25` as the causal gene because it is
the strongest eQTL signal in the disease-shared block. V17 weakens, rather than
strengthens, an intervention-grade GPR25 claim because:

- `GPR25` is absent from the two local MS CNS/lesion feature spaces checked.
- Cross-atlas h5ad scans show `GPR25` absent or trace in major immune and tissue
  compartments.
- The CXCL17-GPR25 functional literature supports a plausible lymphocyte
  homing/residency mechanism, but it does not place that mechanism in the
  MS-UC chr1 risk locus, MS lesions, or the project's IFN/APC response axis.

Conclusion: the current `GPR25` classification as alive Tier 1, not
intervention-grade, is appropriately conservative. Any stronger claim would be
unsupported.

## 2. KIF21B Weighting Risk

V17 may still under-weight `KIF21B` mechanistically because:

- It has high bounded eQTL-coloc support in both MS/eQTL and UC/eQTL.
- It is much more visible than `GPR25` across the available single-cell atlases.
- It is prior art as an MS/IBD susceptibility locus, which reduces novelty but
  does not invalidate it as the causal gene.

The counterweight is translational: `KIF21B` has poor direct druggability and no
clear autoimmune intervention modality. If it wins causal-gene resolution, the
project should treat the locus as mechanism/biomarker evidence rather than as a
direct drug-repositioning target.

## 3. eQTL SuSiE-Coloc Interpretation Risk

The bounded eQTL coloc results are vulnerable to over-interpretation because
the locus has multiple component pairings with high `PP.H3` and high `PP.H4`.
The correct interpretation is:

- shared disease/eQTL components exist for `GPR25` and `KIF21B`;
- distinct eQTL components also exist;
- the analysis does not prove one exclusive causal gene;
- reference-LD/eQTLGen-blood RSS coloc is weaker than tissue-specific raw-beta
  QTL coloc.

The reports currently state this limitation. Future synthesis must preserve it.

## 4. Next-Action Quality

The updated `meta/NEXT_ACTIONS.md` is concrete enough to avoid repetition:

- it tells future sessions not to repeat generic public GEO CITE-seq searches;
- it directs work toward controlled-access/protein-level immune or CSF data;
- it specifies genotype-linked expression and CXCL17 migration/RhoA/integrin
  assays as the decisive path.

Remaining weakness: the computational route for resolving `GPR25` versus
`KIF21B` is now thin. If no controlled-access or protein-level dataset exists,
the next session should pivot quickly to experimental design or to a formal
statement that chr1 is a shared genetic locus with unresolved causal gene, not
continue mining weak transcript proxies.
