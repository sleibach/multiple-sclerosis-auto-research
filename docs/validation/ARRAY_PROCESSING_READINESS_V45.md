# V45 Array Processing Readiness Checklist

Status: processing-readiness artifact. No expression data were reprocessed.

## Purpose

Some alternative cohorts are public but not immediately module-scoreable because
they are array/CEL archives rather than ready gene-by-sample expression
matrices. This checklist separates expression-processing blockers from
clinical-label and subject-map blockers for:

- `GSE228330` ocrelizumab PBMC (`GPL24539`, Clariom S/D Human CEL/CHP);
- Karolinska DMF `GSE130478` (`GPL17692`, Affymetrix expression array).

Checker:

`scripts/v45_array_processing_readiness.py`

Outputs:

- `analysis/v45_array_processing_readiness/local_tool_readiness.tsv`
- `analysis/v45_array_processing_readiness/r_package_readiness.tsv`
- `analysis/v45_array_processing_readiness/array_cohort_processing_requirements.tsv`
- `analysis/v45_array_processing_readiness/summary.json`

## Local Readiness Result

| Component | Status |
|---|---:|
| `Rscript` | available |
| `R` | available |
| `tar` | available |
| `gzip` | available |
| `Biobase` | available |
| `BiocManager` | available |
| `oligo` | missing |
| `affy` | missing |
| `pd.clariom.s.human` | missing |
| `hugene20sttranscriptcluster.db` | missing |

Summary:

| Cohort path | Local raw-array processing status |
|---|---|
| GSE228330 Clariom/CEL | not ready locally; requires `oligo` + `pd.clariom.s.human` or an author-provided processed matrix |
| Karolinska GSE130478 Affymetrix | not ready locally without `oligo`/`affy` plus the correct platform annotation, or an author-provided processed matrix |

## GSE228330 Processing Checklist

Already verified:

- public raw archive resolves;
- per-sample CEL/CHP paths are listed in
  `analysis/v45_gse228330_pharmacodynamic_runbook/gse228330_download_manifest.tsv`;
- public annotation/probe table resolves;
- R is available locally.

Still required before expression/module scoring:

1. download `GSE228330_RAW.tar` or per-sample CEL files into quarantine;
2. install/provide Bioconductor Clariom processing stack:
   - `oligo`;
   - `pd.clariom.s.human` or equivalent current platform package;
   - transcript/gene annotation sufficient to map probesets to gene symbols;
3. produce a normalized gene-by-sample expression matrix;
4. verify sample IDs against metadata;
5. pass intake preflight;
6. pass subject-map sanity if paired deltas are needed.

Non-processing blockers still remain:

- public GSM-to-subject/timepoint pairing is unverified;
- public response/NEDA/relapse/EDSS labels are absent.

Therefore GSE228330 remains context-only and not paired-response ready even if
raw array processing is solved.

## Karolinska GSE130478 Processing Checklist

Already verified:

- `GSE130478` has public expression array data for 28 CD4+ T-cell samples from
  14 MS patients at baseline and 6 months;
- raw archive path is listed in public GEO metadata;
- R is available locally.

Still required before expression/module scoring:

1. obtain or download the raw archive;
2. install/provide `oligo`/`affy` and the correct `GPL17692` annotation path;
3. produce a normalized gene-by-sample expression matrix;
4. verify sample IDs against the author-provided GSM-to-patient/timepoint map;
5. finalize the Karolinska preregistration addendum before scoring labels.

Non-processing blockers still remain:

- beneficial-response labels are absent from public GEO;
- GSM-to-patient/timepoint map is absent from public GEO;
- the cohort is a late-timepoint CD4+ T-cell secondary stress test, not a direct
  primary Gafson substitute.

## Preferred Route

For both array cohorts, the cleanest path is author-provided processed expression
plus sample mapping and labels. Local raw-array reprocessing is feasible only
after the missing Bioconductor packages/platform annotations are installed and
documented.

## Guardrail

Solving array processing does not solve validation readiness. A cohort still
must pass:

1. data-use/terms capture;
2. checksum manifest;
3. response-column audit where applicable;
4. intake preflight;
5. subject-map sanity;
6. cohort-specific preregistration/addendum;
7. matching frozen harness.
