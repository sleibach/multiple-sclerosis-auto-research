# Wave 14 GSK3B / CIITA Perturbation Scout

Returned: 2026-05-27

Worker: `wave14_gsk3b_ciita_perturbation_worker`

## Scope

Test whether public macrophage IFN-gamma perturbation data support `GSK3B` as
an intervention controller upstream of the `CIITA/RFX5/HLA-II/CD74` state,
without collapsing generic IFN signaling. This is a perturbation scout, not a
final therapeutic finding.

## Data Used

All raw downloads were kept under `data/raw_v3/wave14_gsk3b_ciita/`; raw FASTQ
was not downloaded.

| Accession | Source URL | Processed file used | Local file |
|---|---|---|---|
| `GSE162463` | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE162463 | normalized sgRNA counts for mouse macrophage MHCII/CD40/PD-L1 CRISPR screen | `data/raw_v3/wave14_gsk3b_ciita/GSE162463_sgRNA_CountsNormalized.txt.gz` |
| `GSE162464` | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE162464 | normalized RNA-seq gene counts for NTC, `Gsk3b` KO, and `Med16` KO +/- IFN-gamma, triplicates | `data/raw_v3/wave14_gsk3b_ciita/GSE162464_Normalized_Gene_Counts_Matrix.txt.gz` |
| `GSE294918` | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE294918 | human macrophage IFN-gamma memory/ruxolitinib RNA-seq CPM table | `data/raw_v3/wave14_gsk3b_ciita/GSE294918_IFNyRNAseq_CPM.csv.gz` |

Relevant paper/source context:

- eLife/PMC macrophage screen/RNA-seq study: https://pmc.ncbi.nlm.nih.gov/articles/PMC8598162/
- Human IFN-gamma memory/ruxolitinib study record: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE294918

## Methods

Script: `scripts/v3_wave14_gsk3b_ciita_perturbation.py`

Command:

```bash
./.venv_v3_py312/bin/python scripts/v3_wave14_gsk3b_ciita_perturbation.py
```

Analyses:

- `GSE162463`: computed sgRNA-level `log2((low gate + 1) / (high gate + 1))`
  for MHCII, CD40, and PD-L1 gates. Gene-level summaries use median across
  sgRNAs, ranked among genes with at least three sgRNAs. Direction: positive
  MHCII low/high means knockout is enriched in the MHCII-low gate.
- `GSE162464`: computed log2 normalized-count contrasts with pseudocount 1.
  Direct IFN-gamma contrasts use Welch tests across triplicates; module scores
  are mean gene log2FC across predefined CIITA/MHC-II/CD74, generic IFN, and
  lysosomal antigen-processing readouts.
- `GSE294918`: computed descriptive log2 CPM contrasts only, because the
  processed table exposes one column per condition/timepoint, not replicate
  columns. Used as human macrophage broad-JAK positive-control context.

Traceable outputs:

- `results_v3/wave14_gsk3b_ciita_perturbation/download_manifest.tsv`
- `results_v3/wave14_gsk3b_ciita_perturbation/gse162463_screen_gene_summary.tsv`
- `results_v3/wave14_gsk3b_ciita_perturbation/gse162463_target_gene_summary.tsv`
- `results_v3/wave14_gsk3b_ciita_perturbation/gse162464_mouse_rna_gene_contrasts.tsv`
- `results_v3/wave14_gsk3b_ciita_perturbation/gse162464_mouse_rna_module_summary.tsv`
- `results_v3/wave14_gsk3b_ciita_perturbation/gse294918_human_rux_gene_contrasts.tsv`
- `results_v3/wave14_gsk3b_ciita_perturbation/gse294918_human_rux_module_summary.tsv`
- `results_v3/wave14_gsk3b_ciita_perturbation/wave14_verdict.json`
- `results_v3/wave14_gsk3b_ciita_perturbation/wave14_summary.json`

## Results

### `GSE162463` CRISPR Screen

`Gsk3b` knockout sgRNAs were enriched in the MHCII-low gate:

- `Gsk3b`: median MHCII low/high log2 = `3.386`, rank `39 / 11701` genes with
  at least three sgRNAs; 3/4 sgRNAs positive.
- Positive controls behaved as expected: `Ifngr2` rank `1`, `Ifngr1` rank `8`,
  `Jak1` rank `37`, `Stat1` rank `44`.
- CIITA-gate controls also ranked high: `Med16` rank `42`, `Ciita` rank `53`,
  `Rfx5` rank `153`.

Caveat: this script used normalized sgRNA count ranks, not a full MAGeCK-style
screen reanalysis. The crude `Gsk3b` sgRNA one-sample p-value was `0.108` and
not FDR-significant after genome-wide correction, so the robust claim here is
direction/rank consistency with the published screen, not independent
screen-level statistical discovery.

Specificity was mixed: `Gsk3b` had CD40 low/high median `-0.963` but PD-L1
low/high median `1.106`, so it is not a pure MHCII-only screen hit.

### `GSE162464` Mouse RNA-Seq

IFN-gamma strongly induced both the target state and generic IFN genes in NTC
macrophages:

- NTC IFN-gamma vs untreated: CIITA/MHC-II/CD74 module `+5.757`;
  generic IFN module `+5.117`.

Under IFN-gamma, `Gsk3b` KO reduced the CIITA/MHC-II/CD74 state more than the
generic IFN module:

- `Gsk3b_IFNg_vs_NTC_IFNg`: CIITA/MHC-II/CD74 module `-1.856`.
- MHC-II surface core module: `-1.985`.
- Generic IFN core module: `-0.483`.
- Absolute MHC/IFN effect ratio: `3.84`.

Key gene-level `Gsk3b_IFNg_vs_NTC_IFNg` effects:

| Gene | log2FC | FDR |
|---|---:|---:|
| `Ciita` | `-1.791` | `0.044` |
| `Rfx5` | `-1.023` | `0.105` |
| `Cd74` | `-0.920` | `0.110` |
| `H2-Aa` | `-3.497` | `0.014` |
| `H2-Ab1` | `-2.143` | `0.027` |
| `H2-Eb1` | `-2.471` | `0.020` |
| `Stat1` | `-0.239` | `0.560` |
| `Irf1` | `-0.379` | `0.411` |
| `Gbp2` | `-0.030` | `0.929` |
| `Tap1` | `-0.201` | `0.605` |
| `Tap2` | `+0.131` | `0.730` |
| `B2m` | `+0.209` | `0.592` |
| `Cxcl10` | `-1.452` | `0.039` |

Interpretation: this supports a preferential CIITA/MHC-II/CD74 reduction, but
not a perfectly IFN-neutral intervention. `Cxcl10` drops strongly, while
`Stat1`, `Irf1`, `Gbp2`, `Tap1`, `Tap2`, and `B2m` are comparatively spared.

`Med16` behaved as a stronger CIITA/MHC-II gate control:

- `Med16_IFNg_vs_NTC_IFNg`: CIITA/MHC-II/CD74 module `-3.741`;
  generic IFN module `-0.465`.

This is useful as a non-druggable gate comparator, not as a GSK3B-specific
therapeutic argument.

### `GSE294918` Human Ruxolitinib Positive Control

The processed CPM table supports ruxolitinib as a broad IFN/JAK shutdown
comparator in human macrophages.

At D4/LPS0, IFN-gamma memory vs PBS:

- CIITA/HLA-II/CD74 module `+0.878`.
- Generic IFN core module `+3.403`.

At D4/LPS0, ruxolitinib in IFN-gamma-pretreated macrophages:

- CIITA/HLA-II/CD74 module `-1.079`.
- Generic IFN core module `-3.184`.

Key ruxolitinib gene effects at D4/LPS0:

| Gene | log2FC |
|---|---:|
| `CIITA` | `-1.954` |
| `CD74` | `-1.007` |
| `HLA-DRA` | `-0.898` |
| `HLA-DRB1` | `-0.941` |
| `STAT1` | `-3.353` |
| `IRF1` | `-3.926` |
| `CXCL10` | `-4.200` |
| `GBP1` | `-5.053` |
| `TAP1` | `-2.778` |
| `B2M` | `-0.923` |

Interpretation: ruxolitinib reduces HLA-II/CD74 but collapses generic IFN
readouts much more strongly. This is a useful positive control and a contrast
against the more selective `Gsk3b` KO pattern in `GSE162464`.

## Blockers / Nulls

- No raw FASTQ was needed; processed GEO files were accessible.
- `GSE294918` processed CPM has one column per condition/timepoint, so no
  replicate-level inference was attempted for the ruxolitinib analysis.
- The `GSE294918` processed RNA-seq table used here contains the ruxolitinib
  arm; I did not find an anti-IFN-gamma RNA-seq replicate table in the GEO
  processed CPM file.
- `GSK3B` is not MHC-II-only: the CRISPR screen suggests PD-L1 involvement,
  and the RNA-seq contrast includes a significant `Cxcl10` decrease.
- Lysosomal antigen-processing transcripts were not a clean positive result
  for `Gsk3b` KO. The `GSE162464` lysosomal module mean was `+0.137` under
  IFN-gamma despite `Ifi30` and `Ctss` modest negative trends.

## Verdict

The public macrophage perturbation data support `GSK3B` as a testable upstream
controller of the IFN-gamma-induced `CIITA/RFX5/MHC-II/CD74` state.

They do not support a final therapeutic finding. The strongest result is
selective-ish, not selective: `Gsk3b` KO preferentially reduces CIITA/MHC-II/CD74
relative to averaged generic IFN signaling, but it also affects selected IFN
outputs such as `Cxcl10` and has PD-L1 screen signal. Compared with
ruxolitinib, `Gsk3b` KO is much less pan-IFN-collapsing, which keeps it in the
intervention-controller lane for follow-up.
