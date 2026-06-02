# V9 Sidecar: Genetics-Axis Robustness Requirements

Timestamp: 2026-06-02  
Scope: report-only reassignment for the MS-centered genetics axis. I did not tune placements and did not run a new LDSC/coloc analysis. No new genetic-correlation, shared-locus, or causal-gene result is claimed here.

## Files Reviewed

- `MS_MECHANISM_MAP_V8.md`
- `MAP_METHODOLOGY_V8.md`
- `MAP_METHODOLOGY_V9.md`
- `ROADMAP_V9.md`
- `scripts/v8_build_genetics_axis.py`
- `analysis/v8_map/AXIS_02_GENETICS_REPORT.md`
- `analysis/v8_map/axis_02_genetics_placements.tsv`
- `analysis/v8_map/axis_02_genetics_evidence.tsv`

## Current State Of The Genetics Axis

V8 genetics is checkpoint-grade, not robust-grade.

The implemented V8 script uses two evidence layers:

1. A first-pass OpenTargets genetic-association target-overlap proxy from `results_v3/wave55_external_genetics_druggability_sweep/opentargets_associated_targets_raw.tsv`.
2. A literature override for UC and Crohn from Yang et al. 2021, `doi:10.1038/s41467-021-25768-0`.

Current V8 placements for the diseases requested here:

| Disease | V8 placement | V8 grade | Current evidence | Main limitation |
|---|---|---:|---|---|
| UC | near | supported | Published LDSC source reports MS-UC `rg=0.33`; OpenTargets target overlap also present | No repo-local LDSC rerun; no locus-level coloc/fine-mapping layer in the map |
| Crohn disease | intermediate | supported | Published LDSC source reports MS-CD `rg=0.16`; OpenTargets target overlap also present | Same as UC; weaker global correlation |
| RA | intermediate | provisional | OpenTargets target-overlap proxy only: 22 shared MS targets, Jaccard `0.070` | No genome-wide rg; no shared-locus/coloc adjudication |
| SLE | intermediate | provisional | OpenTargets proxy only: 19 shared MS targets, Jaccard `0.098` | No genome-wide rg; HLA/IRF/STAT overlap not resolved into MS-specific architecture |
| T1D | intermediate | provisional | OpenTargets proxy only: 11 shared MS targets, Jaccard `0.065` | No genome-wide rg; HLA-only/broad-autoimmunity contribution unresolved |
| Psoriasis | intermediate | provisional | OpenTargets proxy only: 15 shared MS targets, Jaccard `0.071` | No genome-wide rg; IL23/IL12/T-cell loci not resolved against MS |

Under `MAP_METHODOLOGY_V9.md`, target-overlap remains provisional. Therefore RA/SLE/T1D/psoriasis cannot be upgraded without LDSC/HDL, coloc/fine-mapping, MR with validated instruments, or a verified published genetic-correlation matrix including MS.

## What Would Upgrade To Robust-Grade

For MS versus UC/CD/RA/SLE/T1D/psoriasis, robust-grade should require all three layers below. One layer alone is not enough.

### Layer 1: Genome-Wide Genetic Correlation

Minimum supported-grade:

- Pairwise LDSC or HDL genetic correlation between MS and each comparator disease.
- Same ancestry wherever possible, preferably European first because the strongest public MS and comparator summary statistics are European.
- Intercept and attenuation reported to assess sample overlap and population stratification.
- Benjamini-Hochberg FDR across the six MS-vs-disease tests.

Robust-grade:

- LDSC and a second method agree directionally, e.g. HDL or LAVA/SUPERGNOVA local genetic correlation.
- Sensitivity excluding the extended MHC region, because HLA can dominate autoimmune correlation.
- UC/CD/RA/SLE/T1D/psoriasis are analyzed in one harmonized pipeline with identical munging, SNP filters, LD reference, and correction rules.

Interpretation rule:

- Positive genome-wide `rg` after FDR and stable after MHC exclusion supports `near` or `intermediate`.
- No meaningful `rg` with adequate SNP coverage supports `far/supported`.
- Positive HLA-only signal with weak non-HLA signal is capped at `intermediate/supported`.

### Layer 2: Shared Loci Beyond Mapped-Gene Overlap

Minimum supported-grade:

- Independent shared risk loci identified using one of: conjunctional FDR, cross-trait meta-analysis, coloc at known loci, or credible-set intersection.
- HLA and non-HLA loci reported separately.
- Shared variants must have same genomic coordinate/build and allele harmonization.

Robust-grade:

- At least two non-HLA shared loci with consistent direction and credible-set overlap or high coloc posterior.
- Disease-specific and shared-locus categories separated, as in the Yang et al. MS-IBD analysis.
- Local genetic correlation or cross-trait meta-analysis confirms that the global rg is not driven only by broad polygenic background.

### Layer 3: Causal-Gene Evidence

Minimum supported-grade:

- Shared loci are assigned to genes using credible sets plus eQTL/pQTL/sQTL colocalization, not OpenTargets mapped-gene labels alone.
- Use immune-relevant QTL resources first: eQTLGen blood, eQTL Catalogue immune/stimulated contexts, GTEx immune-adjacent tissues, BLUEPRINT, DICE, and available pQTL datasets.

Robust-grade:

- Multi-signal coloc or SuSiE-coloc at priority shared loci with posterior support, e.g. PP4/H4 `>0.8` or a pre-specified equivalent.
- Direction of effect is recorded where possible: disease-risk allele increases or decreases gene expression/protein abundance.
- Causal-gene calls converge with at least one non-genetic axis in V8/V9, such as IFN/APC, lipid-lysosomal, treatment-response, or microbiome.

## Exact Public Summary-Statistic Sources To Use First

The table below lists feasible first-pass public sources. OpenGWAS pages state that VCF downloads are available but automated API/file access generally requires a JWT/token workflow, so the next step should treat token provisioning as an explicit setup task rather than hiding it.

| Trait | Primary source for first-pass LDSC | Why this source | Backup / replication source |
|---|---|---|---|
| MS | OpenGWAS `ieu-b-18`, IMSGC/Patsopoulos 2019, 47,429 cases + 68,374 controls, 6,304,359 SNPs; OpenGWAS listing: `https://gwas.mrcieu.ac.uk/datasets/?gwas_id__icontains=ieu-b&page=7&sort=consortium` | Best public-scale MS source identified; dense enough for LDSC/HDL; matches current post-2019 MS architecture better than older Beecham data | `ebi-a-GCST005531`, Beecham 2013, 14,498 cases + 24,091 controls, 132,089 SNPs; lower-density checkpoint/sensitivity source |
| UC | OpenGWAS `ieu-a-32`, Liu/IIBDGC 2015, 6,968 cases + 20,464 controls, 12,255,197 SNPs; `https://opengwas.io/datasets/ieu-a-32` | Dense European IIBDGC summary stats; already aligned with V8 Yang 2021 source family | Larger but lower-density `ieu-a-970` was cited in MR tables; use only if exact file access and density are adequate |
| Crohn disease | OpenGWAS `ieu-a-30`, Liu/IIBDGC 2015, 5,956 cases + 14,927 controls, 12,276,506 SNPs; `https://opengwas.io/datasets/ieu-a-30` | Dense European IIBDGC summary stats and direct UC/CD comparability | East Asian `ieu-a-11` for ancestry sensitivity, not primary European MS comparison |
| RA | OpenGWAS `ieu-a-832`, Okada 2014, 14,361 cases + 43,923 controls, 8,747,963 SNPs; `https://opengwas.io/datasets/ieu-a-832` | Large curated European RA source with dense SNP coverage | `ebi-a-GCST000679` Stahl 2010 is smaller; `ebi-a-GCST90013534` appears in MR tables but should be verified before use |
| SLE | OpenGWAS `ebi-a-GCST003156`, Bentham 2015, 5,201 cases + 9,066 controls, 7,071,163 SNPs; `https://opengwas.io/datasets/ebi-a-GCST003156` | Best exact public SLE source found with dense coverage and European ancestry | `ieu-a-815` is smaller and can serve as sensitivity only |
| T1D | OpenGWAS `ebi-a-GCST90014023`, Chiou 2021, 18,942 cases, sample size 520,580, 59,999,551 SNPs; `https://opengwas.io/datasets/ebi-a-GCST90014023` | Largest T1D source found; high-density and modern | `ebi-a-GCST005536`, Onengut-Gumuscu 2015, 6,683 cases and 12,173 controls, 101,101 SNPs; lower-density sensitivity |
| Psoriasis | OpenGWAS `finn-b-L12_PSORIASIS`, FinnGen, 4,510 cases + 212,242 controls, 16,380,464 SNPs; `https://opengwas.io/datasets/finn-b-L12_PSORIASIS` | Dense public psoriasis source suitable for LDSC if case/control and liability metadata are handled carefully | `ebi-a-GCST005527`, Tsoi 2012, 10,588 cases + 22,806 controls, 138,661 SNPs; useful independent replication but lower-density |

Important source caveat: `ebi-a-GCST005531` and `ebi-a-GCST005527` are lower-density GWAS Catalog/OpenGWAS imports. They are useful for MR/instrument sensitivity but are weak primary choices for LDSC relative to denser sources.

## Published Evidence Already Strong Enough To Preserve

Yang et al. 2021 is valid support for the V8 UC/CD upgrade. PubMed reports that the study used large-scale GWAS summary data, found significantly greater genetic correlation between MS and UC than MS and CD, and identified shared SNPs in cross-trait meta-analysis. It also reports MR and tissue/cell-type heritability enrichment analyses. This remains a strong checkpoint/supported source for UC and Crohn, but it is not enough for V9 robust-grade because:

- it only covers IBD, not RA/SLE/T1D/psoriasis;
- the repo has not rerun the analysis in one harmonized pipeline;
- the current map does not carry locus-level coloc/fine-mapped causal-gene evidence for the same axis.

## Feasible Next Computational Step In This Repo

Recommended next step: build a V9 genetics preparation and LDSC runner scaffold without changing placements until outputs are complete.

Proposed files:

- `scripts/v9_genetics_source_manifest.py`
- `scripts/v9_run_ldsc_axis.py`
- `analysis/v9_genetics/source_manifest.tsv`
- `analysis/v9_genetics/ldsc_pairwise_results.tsv`
- `analysis/v9_genetics/ldsc_qc_report.md`

Minimal implementation:

1. Create `analysis/v9_genetics/source_manifest.tsv` with the seven primary OpenGWAS IDs above, source URLs, case/control counts, SNP count, ancestry, build, and whether file access is available.
2. Require `OPENGWAS_JWT` or manually downloaded VCF/sumstats paths. If no token/files exist, stop with an access-status report, not a failed biology result.
3. Munge all summary statistics with the same LDSC settings:
   - build GRCh37/HG19;
   - HapMap3 SNP restriction;
   - allele harmonization;
   - MHC exclusion sensitivity: chr6:25-34 Mb;
   - effective sample size for case-control traits;
   - record SNP retention per disease.
4. Run pairwise LDSC:
   - MS vs UC;
   - MS vs Crohn;
   - MS vs RA;
   - MS vs SLE;
   - MS vs T1D;
   - MS vs psoriasis.
5. Apply BH-FDR across the six pairwise `rg` p values.
6. Emit a placement recommendation table, but do not update `analysis/v8_map` until reviewed.

A first robust-grade decision can be made from this LDSC layer only if:

- at least five of six comparator datasets pass LDSC QC;
- MS-UC and MS-CD reproduce the Yang 2021 direction qualitatively;
- at least one non-IBD comparator gains corrected genetic-correlation support or is cleanly negative with adequate coverage;
- MHC-excluded sensitivity does not invert the main interpretation.

## Locus And Causal-Gene Follow-Up

After LDSC, prioritize loci where V8 non-genetic axes already have biological hypotheses:

- IFN/APC / antigen-presentation: `IL2RA`, `IL7R`, `STAT3`, `TYK2`, `IRF5`, `CD40`, HLA class II.
- Barrier/IBD-transfer loci: `IL23R`, `IL12B`, `PTPN2`, `GPR65`, `INAVA`.
- Lipid-lysosomal/myeloid candidates: `CLEC16A`, `CTSH`, `SP140`, `TNFRSF1A`, `FADS1/FADS2` region.

For each locus:

1. Define a +/-500 kb window around lead variants from the primary GWAS.
2. Fine-map per disease using SuSiE or FINEMAP if sufficient summary-stat/LD inputs are available.
3. Run coloc/SuSiE-coloc with eQTLGen whole blood and immune-cell eQTL Catalogue contexts.
4. Require multi-signal awareness in dense autoimmune loci; single-causal-variant coloc is too weak at HLA, 1p13, 6q23, 12q13, and 16p13.
5. Record direction and whether the same gene is implicated in MS and the comparator disease.

## Decision Rules For V9 Placement Updates

Suggested mapping from new evidence to V9 placement:

- `near/supported`: positive genome-wide rg after FDR plus at least one non-HLA shared locus or pathway.
- `near/robust`: positive rg by LDSC and HDL/local-rg, stable after MHC exclusion, plus multiple shared non-HLA causal genes or loci.
- `intermediate/supported`: positive rg mostly HLA-driven, or broad autoimmunity overlap without MS-specific non-HLA convergence.
- `far/supported`: adequate powered rg near zero, no meaningful non-HLA shared loci, and target-overlap proxy shown to be misleading.
- `contradictory/supported`: global rg positive but coloc/fine-mapping shows distinct causal genes, or MHC-excluded sensitivity reverses the conclusion.

## Risks And Guardrails

- OpenGWAS automated download may require JWT; lack of token is an access blocker, not a genetics null.
- Sample overlap between large autoimmune consortia can bias rg; LDSC intercept and constrained/unconstrained intercept sensitivity are mandatory.
- HLA can dominate apparent autoimmune proximity; report whole-genome and MHC-excluded results separately.
- FinnGen psoriasis is dense but registry-defined and has different ascertainment from consortium case-control GWAS; use as primary density source but replicate with `GCST005527` if possible.
- Target-overlap and OpenTargets L2G can prioritize loci but cannot upgrade map placements alone.
- MR is not a substitute for genetic correlation unless instruments are validated, pleiotropy is assessed, and bidirectional tests are run.

## Bottom Line

To upgrade the V8 genetics axis, the repo needs a harmonized LDSC/HDL run across MS, UC, Crohn, RA, SLE, T1D, and psoriasis, followed by MHC-excluded sensitivity and locus-level causal-gene adjudication. The fastest meaningful next computation is not another OpenTargets overlap; it is a reproducible `analysis/v9_genetics` LDSC source-manifest plus pairwise-rg pipeline using `ieu-b-18` as the MS anchor and dense OpenGWAS comparator summary statistics.
