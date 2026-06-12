# GSE228330 Pharmacodynamic-Only Runbook V45

## Status

`GSE228330` is an open anti-CD20/ocrelizumab MS PBMC transcriptomic cohort, but
it is **not response-validation ready** from public data. It remains
pharmacodynamic context only unless sample-mapped outcomes and a confirmed
subject/timepoint map are obtained and a cohort-specific blinded addendum is
committed before analysis.

This runbook prepares acquisition and context-only handling. It does not apply
the V22 rule and does not create any response-prediction result.

## Verified Public Structure

Prior scout:

- `docs/validation/GSE228330_OUTCOME_SCOUT_V45.md`
- `analysis/v45_gse228330_outcome_scout/summary.json`

V45 runbook artifacts:

- `analysis/v45_gse228330_pharmacodynamic_runbook/gse228330_download_manifest.tsv`
- `analysis/v45_gse228330_pharmacodynamic_runbook/gse228330_draft_pharmacodynamic_metadata_unverified.tsv`
- `analysis/v45_gse228330_pharmacodynamic_runbook/gse228330_timepoint_counts.tsv`
- `analysis/v45_gse228330_pharmacodynamic_runbook/gse228330_subtype_timepoint_counts.tsv`

Public metadata support:

| Field | Verified value |
|---|---|
| Samples | 44 |
| Timepoints | baseline `n=15`, week 2 / 0.5 months `n=14`, month 6 `n=15` |
| Therapy | ocrelizumab |
| Therapy class | anti-CD20 |
| Tissue | PBMC |
| Platform | Clariom S Human array, `GPL24539` |
| Public response labels | absent |
| Public subject-pairing map | not confirmed |

The absence of public response labels means the cohort cannot validate or
falsify the locked V22 treatment-response rule. The unconfirmed subject map also
means formal paired-delta context should wait until pairing is verified from an
author response, paper supplement, or an independently auditable file.

## Public Files

The two series-level public files resolve by HTTP HEAD as of this V45 run:

| File | Size / role |
|---|---|
| `GSE228330_Clariom_S_Human.hg38.main.probes.tab.gz` | about 5.1 MB; Clariom annotation/probe table, not expression matrix |
| `GSE228330_RAW.tar` | about 1.8 GB; raw sample archive containing CEL/CHP files |

The generated download manifest also lists per-sample CEL and CHP URLs derived
from GEO metadata.

## Acquisition Commands

Create a quarantined package:

```bash
mkdir -p data/quarantine/gse228330_pharmacodynamic/raw
mkdir -p data/quarantine/gse228330_pharmacodynamic/metadata
mkdir -p data/quarantine/gse228330_pharmacodynamic/processed
```

Download the public files:

```bash
curl -L -o data/quarantine/gse228330_pharmacodynamic/raw/GSE228330_Clariom_S_Human.hg38.main.probes.tab.gz \
  https://ftp.ncbi.nlm.nih.gov/geo/series/GSE228nnn/GSE228330/suppl/GSE228330_Clariom_S_Human.hg38.main.probes.tab.gz

curl -L -o data/quarantine/gse228330_pharmacodynamic/raw/GSE228330_RAW.tar \
  https://ftp.ncbi.nlm.nih.gov/geo/series/GSE228nnn/GSE228330/suppl/GSE228330_RAW.tar
```

Record checksums:

```bash
find data/quarantine/gse228330_pharmacodynamic -type f -print0 \
  | sort -z \
  | xargs -0 shasum -a 256 \
  > data/quarantine/gse228330_pharmacodynamic/SHA256SUMS
```

The 1.8 GB raw archive was not downloaded in this V45 checkpoint. The runbook
only verifies that it resolves and records the exact acquisition path.

## Metadata Preparation

Generate the draft acquisition artifacts from already-audited GEO metadata:

```bash
.venv/bin/python scripts/v45_prepare_gse228330_pharmacodynamic_runbook.py
```

The draft metadata file is intentionally marked:

- `pairing_status = inferred_unverified`
- `use_status = context_only_subject_map_required_before_paired_delta`

Do not feed the draft table into a formal paired-delta context run until the
subject map is confirmed. It is a preparation artifact, not a validated sample
map.

## Processing Requirement

The public 5.1 MB series-level file is an annotation/probe table, not an
expression matrix. A context run therefore needs one of:

1. CEL reprocessing from `GSE228330_RAW.tar`; or
2. author-provided processed expression/module scores; or
3. an independently verified processed matrix from another public source.

Local reprocessing preflight in this V45 checkpoint:

| Tool | Status |
|---|---|
| `Rscript` | available |
| `Biobase` | available |
| `oligo` | not installed |
| `pd.clariom.s.human` | not installed |

The immediately missing software path is the Bioconductor Clariom/Affymetrix
processing stack. A future reprocessing checkpoint should install or otherwise
provide `oligo` plus the appropriate Clariom S platform package, then produce a
gene-by-sample normalized expression matrix under:

```text
data/quarantine/gse228330_pharmacodynamic/processed/expression.tsv
```

## Intake Preflight

After acquisition and before any context harness:

```bash
.venv/bin/python scripts/v45_validation_intake_preflight.py check \
  --root data/quarantine/gse228330_pharmacodynamic \
  --mode pharmacodynamic \
  --metadata data/quarantine/gse228330_pharmacodynamic/metadata/pharmacodynamic_metadata.tsv \
  --expression data/quarantine/gse228330_pharmacodynamic/processed/expression.tsv \
  --outdir analysis/intake_preflight/gse228330_pharmacodynamic
```

The preflight must pass. If response-like columns appear in the metadata, the
preflight fails by default because this cohort is context-only.

## Context-Only Harness Command

Only after expression and confirmed subject mapping are available:

```bash
.venv/bin/python scripts/v45_pharmacodynamic_only_harness.py run \
  --metadata data/quarantine/gse228330_pharmacodynamic/metadata/pharmacodynamic_metadata.tsv \
  --expression data/quarantine/gse228330_pharmacodynamic/processed/expression.tsv \
  --outdir analysis/pharmacodynamic_context/gse228330 \
  --expression-type normalized_log
```

If the future processing step produces precomputed frozen module scores instead:

```bash
.venv/bin/python scripts/v45_pharmacodynamic_only_harness.py run \
  --metadata data/quarantine/gse228330_pharmacodynamic/metadata/pharmacodynamic_metadata.tsv \
  --module-scores data/quarantine/gse228330_pharmacodynamic/processed/module_scores.tsv \
  --outdir analysis/pharmacodynamic_context/gse228330
```

Required interpretation:

> GSE228330 is pharmacodynamic context only. It does not validate or falsify the
> locked V22 treatment-response rule, and it cannot support response, NEDA,
> relapse, remission, or patient-stratification claims without author-provided
> sample-mapped outcomes and a blinded preregistration addendum.

## Upgrade Path

To upgrade from context-only to response-validation candidate, obtain:

1. confirmed GSM-to-subject/timepoint map;
2. sample-mapped responder, NEDA, relapse, EDSS-change, or other clinical
   outcome labels;
3. outcome definition and assessment window;
4. steroid, batch, processing, and cell-composition metadata sufficient for
   V42/V44/V45 diagnostics.

Then write and commit a cohort-specific preregistration addendum before any
outcome-labeled expression or module-score analysis.
