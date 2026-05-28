# Foundation/Perturbation Route Report: Hubble

Returned: 2026-05-26 19:20 UTC

## Verdict

The defensible route is not de novo State in this workspace. It is:

1. Primary: LINCS/CMap signature reversal against real local disease/module
   signatures.
2. Validation: real Perturb-seq/Mixscale IFN/TNF pathway data.
3. Secondary model support: State/Stack only for cytokine/drug-response
   hypotheses with strict labels.

## State/Stack Constraints

State CD14 released outputs are feature-agnostic unless the exact 2,000 HVG
order is recovered. De novo State needs compatible AnnData/control cells and
pseudo-AnnData would be invalid. Evo2 is locally blocked. Stack/Perturb-Sapiens
is model-side/synthetic support and large; it cannot count as real validation.

## LINCS/CMap Route

Use local signed signatures from `GSE111972`, V3 rankings, and broader local
disease contrasts. CLUE/LINCS L1000 data are in `GSE92742` and `GSE70138`.

Required large downloads:

- `GSE92742` Level 5: 21,328,033,748 bytes
- `GSE70138` Level 5: 5,365,179,698 bytes
- metadata: roughly 13 MB total plus small gene/perturbagen metadata

Candidate coverage:

- Direct perturbation coverage: `STAT1`, `IRF1`, `IFI30`, `NAMPT`, `OSMR`
- Drug coverage: `ruxolitinib` has many phase signatures
- Ligand signatures: `OSM`, `CXCL10`, `CTSS`
- No exact direct perturbagen: `CD74`, `CXCR3`, `TREM1`
- Query-gene caveat: `STAT1` is Landmark; many others are BING; `IFI30` and
  `OSM` are not BING and should not anchor CMap scoring.

## Perturb-seq Route

Best targeted dataset: Mixscale pathway Perturb-seq. Zenodo
`DE_results_all_pathway.zip` is about 324 MB, with full IFNG/IFNB/TNFA Seurat
objects at multi-GB scale. Use it to test whether regulator perturbations reduce
IFN/TNF pathway programs and downstream genes like `STAT1`, `IRF1`, `CXCL10`,
`CD74`, `IFI30`, and `CTSS`.

scPerturb `DixitRegev2016.h5ad` is about 309 MB and can be used as orthogonal
mechanistic support, not direct human MS proof.

## Integration Decision

For this session, the honest claim is that foundation-model and perturbation
execution is only partially satisfied by State feature-agnostic cytokine
validation. A full perturbation claim requires a LINCS/Perturb-seq branch.
Invalid shortcuts include pseudo-AnnData State inference, guessed State feature
mapping, undirected CMap candidate-list queries, or treating embeddings as
perturbation evidence.
