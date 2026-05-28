# Foundation Alternative Report: Bernoulli

Returned: 2026-05-26 19:36 UTC

## Recommendation

Use real Mixscale Perturb-seq CRISPRi data as the primary gene-specific
perturbation route.

Target dataset: `GSE281048` / Zenodo `14035992`, "Systematic reconstruction of
molecular pathway signatures using scalable single-cell perturbation screens."

The core test is whether CRISPRi perturbation of `STAT1`, `IRF1`, `IFNGR1`,
`IFNGR2`, `JAK2`, or TNF/NF-kB regulators collapses the
`CD74/HLA-II/IFI30/CTSS/CD44/CXCR4` antigen-processing state under `IFNG` or
`TNFA` stimulation.

## Verified Sources

- GEO `GSE281048`: human Perturb-seq across six cancer cell lines and cytokine
  contexts including `IFNB`, `IFNG`, `TNFA`, `TGFB`, and `INS`.
- Zenodo `14035992`, DOI `10.5281/zenodo.14035992`.
- Processed file: `DE_results_all_pathway.zip`, 324.1 MB, md5
  `f077cba680a1affc599f5153d99b0e45`.

## Why This Is Stronger

This branch is gene-specific because the causal unit is a named CRISPRi
perturbation with sgRNAs, not a correlation, module score, or broad cell-line
signature reversal. The readout is transcriptomic differential expression, so
candidate readout genes can be checked directly.

## Risks

- Cell lines are not myeloid, microglia, or target autoimmune tissues.
- Some target readouts may be absent in specific cell lines.
- Full Seurat objects are multi-GB; use the 324 MB DE archive first.

## Fallback

If the processed DE archive lacks required readouts, download the full IFNG
Seurat object from Zenodo and run regulator/readout contrasts locally in R.
If that is too heavy, use PerturBase summaries as a curated real-data fallback,
but not as the primary reproducible analysis.
