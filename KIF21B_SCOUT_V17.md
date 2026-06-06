# KIF21B_SCOUT_V17

Date: 2026-06-06

## Why This Scout Was Run

V17 bounded eQTL SuSiE-coloc showed that `KIF21B` competes with `GPR25` at the
MS-UC chr1 shared locus:

- `KIF21B` MS/eQTL max PP.H4 `0.956099`.
- `KIF21B` UC/eQTL max PP.H4 `0.963951`.

This prevents an exclusive `GPR25` causal-gene claim.

## Expression Support

V17 h5ad scans found `KIF21B` more consistently detectable than `GPR25`.

Highest cell-type detections:

- Psoriasis helper T cells: `10.17%`.
- Psoriasis regulatory T cells: `8.79%`.
- Psoriasis cytotoxic T cells: `7.38%`.
- IBD T cells: `4.09%`.
- Sjogren effector CD8 T cells: `3.55%`.
- Sjogren CD4 T cells: `2.05%`.

In the local MS CNS atlas `GSE301908`, `KIF21B` was measurable in multiple
major clusters, including lymphocytes, microglia, astrocytes, neurons, and OPCs.

## Mechanism / Druggability Scout

Verified source checks:

- UniProt `O75037` / `KI21B_HUMAN`: reviewed protein, kinesin-like protein
  KIF21B.
- AlphaFold `AF-O75037-F1`, version 6, global metric value `69.62`.
- ChEMBL target search for `KIF21B`: `0` targets.
- ChEMBL mechanism query: `0` mechanisms.
- ClinicalTrials.gov query for `KIF21B`: `0` studies.
- Google Patents exact `KIF21B`: `492` results; inspected top hits were broad
  biomarker/platform or unrelated disease-context patents, not a KIF21B
  autoimmune intervention program.

Europe PMC:

- `KIF21B AND "multiple sclerosis"`: hit count `105`; top results include
  bioinformatic/genetic and neurological-disease reviews.
- `KIF21B AND (ulcerative colitis OR Crohn OR inflammatory bowel disease)`:
  hit count `92`, mostly broad shared-genetics or pathway literature.
- `KIF21B AND autoimmune`: hit count `125`, again mostly broad genetic or
  review context.
- `KIF21B AND (multiple sclerosis OR T cell OR lymphocyte OR microglia) AND
  (function OR perturbation OR knockout OR knockdown)`: hit count `456`; top
  results were broad bioinformatic/neurological or oncology-context studies,
  not direct MS immune-cell perturbation evidence.
- Literature search confirms that KIF21B is established prior art as an
  autoimmune susceptibility locus rather than a novel locus:
  - "Comprehensive follow-up of the first genome-wide association study of
    multiple sclerosis identifies KIF21B and TMEM39A as susceptibility loci",
    Human Molecular Genetics 2010, DOI `10.1093/hmg/ddp542`.
  - "Replication of KIF21B as a susceptibility locus for multiple sclerosis",
    Journal of Medical Genetics 2010, DOI `10.1136/jmg.2009.075911`.

GEO:

- `KIF21B CITE-seq multiple sclerosis`: count `0`.
- `KIF21B T cell multiple sclerosis`: count `0`.

## Verdict

`KIF21B` is a serious causal-gene competitor but a weak direct therapeutic
target.

Supported:

- Bounded eQTL-coloc support at the same MS-UC chr1 locus.
- Better transcript-level cell-state support than `GPR25` in available h5ad
  atlases.

Not supported:

- Direct druggability.
- Existing chemical matter.
- Clinical intervention precedent.
- A specific MS mechanism beyond broad microtubule/kinesin biology.
- A public MS CITE-seq/protein or direct immune-cell perturbation dataset that
  resolves the locus in favor of KIF21B.
- Novelty as a susceptibility locus; the possible new contribution would be
  fine-mapped causal-gene resolution and cell-state mechanism, not discovery of
  KIF21B as an MS/IBD locus.

Classification:

- Keep `KIF21B` alive for causal-gene resolution.
- Do not treat `KIF21B` as a direct target without a modality concept.
- If `KIF21B` wins causal-gene resolution, likely contribution is mechanism or
  biomarker biology rather than immediate drug repositioning.
