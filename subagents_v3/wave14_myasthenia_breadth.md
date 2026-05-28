# Wave14 Myasthenia Breadth Report

Returned: 2026-05-27

Worker: `wave14_myasthenia_breadth_worker`

## Verdict

GSE227835 is tractable and adds a real independent myasthenia gravis PBMC breadth
test for V3.

Result: **partial support, not clean pan-autoimmune support**. The dataset
supports recurrence of a lysosomal/APC program in marker-derived B/APC-like
PBMCs and a lipid-loader signal in seronegative MG marker-derived myeloid/APC
cells. It also shows AChR-positive MG IFNG/HLA-II/CD74 recurrence in
marker-derived T-cell-like cells. It **contradicts** a simple universal
HLA-II/CD74 claim because seronegative pre-treatment marker-derived B/APC-like
and plasmablast-like compartments show negative HLA-II/CD74 and IFNG/HLA-II/CD74
module trends.

Interpretation for the V3 cross-autoimmune mechanism: MG PBMC extends the
mechanism as a **compartment-specific systemic immune recurrence** centered on
lysosomal APC and lipid-loader biology. It should not be used as evidence that
all MG compartments, or the neuromuscular-junction lesion, share the same
IFNG/HLA-II/CD74 state.

## Dataset And Accessions

Source: GEO `GSE227835`, "Single-cell RNA-seq data of human PBMC from
Myasthenia Gravis patients"; public on 2024-04-03; last GEO update 2024-05-15;
PubMed `38711503`.

Public URLs:

- GEO: <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE227835>
- Series matrix: <https://ftp.ncbi.nlm.nih.gov/geo/series/GSE227nnn/GSE227835/matrix/GSE227835_series_matrix.txt.gz>
- Family SOFT: <https://ftp.ncbi.nlm.nih.gov/geo/series/GSE227nnn/GSE227835/soft/GSE227835_family.soft.gz>
- Supplement file list: <https://ftp.ncbi.nlm.nih.gov/geo/series/GSE227nnn/GSE227835/suppl/filelist.txt>

Samples: 40 PBMC processed count matrices.

- AChR-positive MG: 10 samples, `GSM7266236`-`GSM7266245`
- Healthy controls: 10 samples, `GSM7266246`-`GSM7266255`
- Seronegative MG pre-treatment: 10 samples, `GSM7266256`, `GSM7266258`,
  `GSM7266260`, `GSM7266262`, `GSM7266264`, `GSM7266266`, `GSM7266268`,
  `GSM7266270`, `GSM7266272`, `GSM7266274`
- Seronegative MG post-treatment: 10 samples, paired by N donor index,
  `GSM7266257`, `GSM7266259`, `GSM7266261`, `GSM7266263`, `GSM7266265`,
  `GSM7266267`, `GSM7266269`, `GSM7266271`, `GSM7266273`, `GSM7266275`

## Files And Checksums

Script:

- `scripts/v3_wave14_gse227835_myasthenia_marker.py`
- SHA256: `85fe4226163bf512467598bb543b28f0ee709902a38191f85750a30ff047e573`

Downloaded raw/metadata files are under `data/raw_v3/gse227835/`.
Full raw file checksums are in:

- `results_v3/wave14_gse227835_myasthenia/gse227835_file_manifest.tsv`

Key raw checksum examples:

| file | size bytes | sha256 |
|---|---:|---|
| `GSE227835_series_matrix.txt.gz` | 3749 | `fc97307925af1eef4b4db7a58daa252f0eba34c86014e465d2c07ae899cd48dc` |
| `GSE227835_family.soft.gz` | 4219 | `c2f90da3663f815a248328e6f044d53e681ce53b5537a172ccc0ca6731fde905` |
| `filelist.txt` | 2478 | `611427c47132b8f28393ebaccb32ba6ae922597ed7d5410abfe931226ebb8ea7` |
| `GSM7266236_A1.txt.gz` | 14169551 | `bb0a25c5912ad78faa82d4a80a21e3048bf38639d77b7550b3da988b6191e2a7` |
| `GSM7266275_N9b.txt.gz` | 22898023 | `c160402537da0631d237e93a630c2de177b016eafc6dc8794bbc43fbdb8a9eb1` |

Generated output checksums are in:

- `results_v3/wave14_gse227835_myasthenia/output_checksums.tsv`

Key generated output checksums:

| file | sha256 |
|---|---|
| `gse227835_summary.json` | `ead4055d517aacc02a8f999f49bc308fa8fefe7acdb235e8b3e0a6bda1461ac4` |
| `gse227835_module_comparisons.tsv` | `e0a86c4972bc182faef87c73ad3e4e4f30133d8b7abb216cfa90eff1cf26cf34` |
| `gse227835_candidate_gene_comparisons.tsv` | `a4f36fa41c83f45fed4b8ff6a9cdf78fc9b053ae051191dcb6fe78513bc53b21` |
| `gse227835_donor_module_scores.tsv` | `caa5565f43ff130cf833f6ec6eaf064204076325fa85b399c1182321b35e5713` |

## Code Outputs

Output directory: `results_v3/wave14_gse227835_myasthenia/`

Primary outputs:

- `gse227835_sample_metadata.tsv`: 40 sample metadata rows plus header.
- `gse227835_file_manifest.tsv`: 43 files plus header; includes raw checksums.
- `gse227835_run_log.tsv`: all 40 samples completed; each matrix had 36,601 gene rows and 105 selected genes present.
- `gse227835_marker_compartment_counts.tsv`: marker-derived cell counts.
- `gse227835_module_genes_present.tsv`: all requested module genes present in all 40 samples.
- `gse227835_donor_module_scores.tsv`: 1,400 donor/sample module rows plus header.
- `gse227835_module_comparisons.tsv`: 280 donor-level module tests plus header.
- `gse227835_candidate_gene_donor_scores.tsv`: 9,800 donor/sample candidate gene rows plus header.
- `gse227835_candidate_gene_comparisons.tsv`: 1,960 donor-level candidate gene tests plus header.
- `gse227835_seronegative_prepost_module_comparisons.tsv`: secondary paired treatment-state module tests.
- `gse227835_summary.json`: run summary and top statistics.

Total parsed cells: 444,357.

Marker-derived compartments:

| group | ambiguous | B/APC-like | myeloid/APC-like | NK-like | plasmablast-like | T-cell-like |
|---|---:|---:|---:|---:|---:|---:|
| AChR-positive MG | 5141 | 16537 | 19631 | 25484 | 949 | 41685 |
| healthy control | 4757 | 13420 | 15461 | 22199 | 724 | 45477 |
| seronegative MG post | 5592 | 9494 | 25314 | 30515 | 1173 | 45474 |
| seronegative MG pre | 7199 | 9830 | 22827 | 32192 | 1651 | 41631 |

Important guardrail: GEO gives curated **sample** labels only. Cell compartments
above are marker-derived from the count matrices; there are no curated GEO cell
labels in the supplement.

## Donor-Level Statistics

Primary disease-control contrasts:

- `untreated_mg_vs_healthy_control`: AChR-positive MG plus seronegative
  pre-treatment MG, n=20 case donors vs n=10 controls.
- `achr_positive_mg_vs_healthy_control`: n=10 vs n=10.
- `seronegative_mg_pre_vs_healthy_control`: n=10 vs n=10.

All tests are donor/sample-level Welch tests after cell-level scores were
aggregated to donor/sample by marker-derived compartment. Hedges g is
case-minus-control.

Module summary:

| module | FDR10 positive tests | trend-or-better tests | negative trend tests | key interpretation |
|---|---:|---:|---:|---|
| `lysosomal_apc` | 3 | 4 | 1 | strongest MG support; especially B/APC-like cells |
| `mixscale_validated_ifng_readout` | 2 | 3 | 2 | AChR-positive support; seronegative negative in NK/plasmablast-like |
| `lipid_loader_repair` | 1 | 7 | 1 | myeloid/APC seronegative and combined support |
| `ifng_hlaii_cd74` | 1 | 1 | 2 | AChR T-cell-like support but seronegative B/plasmablast-like contradiction |
| `hla_ii_cd74` | 1 | 1 | 4 | AChR T-cell-like support but broader negative B/plasmablast-like evidence |
| `slc15a4_tasl_branch` | 0 | 2 | 0 | nominal B/APC-like support only |
| `complement_phagocytosis` | 0 | 0 | 3 | negative in plasmablast-like compartment |

Selected module results:

| contrast | compartment | module | delta | Hedges g | p | FDR |
|---|---|---|---:|---:|---:|---:|
| AChR-positive MG vs HC | B/APC-like | `lysosomal_apc` | 0.0865 | 2.252 | 8.18e-05 | 0.0111 |
| untreated MG vs HC | B/APC-like | `lysosomal_apc` | 0.0780 | 1.729 | 1.96e-04 | 0.0111 |
| seronegative MG pre vs HC | plasmablast-like | `complement_phagocytosis` | -0.0533 | -1.955 | 2.42e-04 | 0.0113 |
| seronegative MG pre vs HC | B/APC-like | `hla_ii_cd74` | -0.2633 | -1.757 | 6.98e-04 | 0.0163 |
| AChR-positive MG vs HC | T-cell-like | `ifng_hlaii_cd74` | 0.0878 | 1.644 | 0.00121 | 0.0245 |
| seronegative MG pre vs HC | B/APC-like | `ifng_hlaii_cd74` | -0.1379 | -1.618 | 0.00140 | 0.0245 |
| seronegative MG pre vs HC | myeloid/APC-like | `lipid_loader_repair` | 0.1032 | 1.647 | 0.00152 | 0.0251 |
| AChR-positive MG vs HC | T-cell-like | `mixscale_validated_ifng_readout` | 0.1051 | 1.535 | 0.00216 | 0.0303 |
| AChR-positive MG vs HC | T-cell-like | `hla_ii_cd74` | 0.0936 | 1.387 | 0.00492 | 0.0574 |
| seronegative MG pre vs HC | B/APC-like | `lysosomal_apc` | 0.0695 | 1.332 | 0.00639 | 0.0643 |
| AChR-positive MG vs HC | B/APC-like | `slc15a4_tasl_branch` | 0.0541 | 1.067 | 0.0228 | 0.1208 |

Selected candidate-gene results:

| contrast | compartment | gene | delta | Hedges g | p | FDR |
|---|---|---|---:|---:|---:|---:|
| untreated MG vs HC | myeloid/APC-like | `PLIN2` | 0.1600 | 1.527 | 1.67e-05 | 0.00879 |
| untreated MG vs HC | B/APC-like | `IFI30` | 0.1194 | 1.510 | 2.63e-05 | 0.00879 |
| untreated MG vs HC | B/APC-like | `CTSB` | 0.0245 | 1.521 | 5.42e-05 | 0.0152 |
| seronegative MG pre vs HC | myeloid/APC-like | `PLIN2` | 0.2398 | 2.492 | 8.90e-05 | 0.0179 |
| AChR-positive MG vs HC | T-cell-like | `PLIN2` | 0.0391 | 2.140 | 1.01e-04 | 0.0179 |
| AChR-positive MG vs HC | B/APC-like | `IFI30` | 0.1180 | 1.892 | 5.75e-04 | 0.0440 |
| AChR-positive MG vs HC | B/APC-like | `TASL`/`CXorf21` | 0.0249 | 1.584 | 0.00165 | 0.0839 |
| AChR-positive MG vs HC | T-cell-like | `CTSS` | 0.0810 | 1.588 | 0.00183 | 0.0876 |
| untreated MG vs HC | B/APC-like | `SLC15A4` | 0.0221 | 1.247 | 0.00905 | 0.1739 |
| AChR-positive MG vs HC | T-cell-like | `CD74` | 0.0920 | 1.128 | 0.0173 | 0.2390 |
| seronegative MG pre vs HC | B/APC-like | `HLA-DRA` | -0.2798 | -1.228 | 0.0103 | 0.1835 |

`TASL` is represented by the current gene symbol `CXorf21` in the matrix. The
script exposes both labels for candidate-gene traceability, but the
`slc15a4_tasl_branch` module counts the TASL/CXorf21 biology once.

## Mechanism Call

Supports:

- `lysosomal_apc`: strong positive donor-level recurrence in B/APC-like PBMCs,
  including combined untreated MG and AChR-positive MG after FDR correction.
- `IFI30`, `CTSB`, `CTSS`: candidate-gene support is concentrated in B/APC-like
  and T-cell-like marker compartments.
- `lipid_loader_repair`: strongest in seronegative pre-treatment
  myeloid/APC-like cells; `PLIN2` is the clearest candidate-gene contributor.
- `SLC15A4/TASL`: weak-to-moderate B/APC-like expression support, but module
  support does not reach FDR10.

Contradicts or limits:

- HLA-II/CD74 is not uniformly increased. Seronegative pre-treatment B/APC-like
  cells are negative for `hla_ii_cd74` and `ifng_hlaii_cd74` at FDR10.
- Plasmablast-like compartments show multiple negative module trends, including
  complement/phagocytosis and HLA-II related modules.
- PBMC evidence should not be over-read as neuromuscular-junction tissue
  causality in MG.

Bottom line: GSE227835 supports a **compartment-specific autoimmune PBMC
recurrence** of the V3 lysosomal/APC and lipid-loader axes, with subtype- and
compartment-dependent IFNG/HLA-II/CD74 behavior. It strengthens MG as a
supporting breadth disease, but it does not rescue a simple pan-autoimmune,
pan-compartment IFNG/HLA-II/CD74 mechanism.
