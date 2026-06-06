# AXIS_DISAGREEMENT_FINDINGS_V12

Status: completed supported-cell disagreement matrix synthesis.

## Executive Finding

The completed V12 matrix supports a specific MS transfer-validity rule:

> MS-adjacent autoimmune mechanisms transfer by biological layer, not by disease
> label. UC is closest to MS on inherited risk among the gut diseases, while
> Crohn and UC both converge downstream on mucosal IFN/APC response-monitoring;
> RA transfers as a pregnancy/postpartum timing comparator but not as a blood
> APC treatment-response comparator; Sjogren transfers antigen-presentation
> biology but not matched lysosomal/APC lesion-rim biology.

This is not a cure-class intervention claim. It is a completed, evidence-graded
axis-disagreement map that constrains which adjacent-disease mechanisms should
and should not be transferred to MS.

## Matrix Completion

Canonical state:

- `analysis/v11_matrix/disagreement_matrix.tsv`
- `meta/MATRIX_STATUS.md`

Completion:

- Total supported disagreement cells: `10`.
- Resolved/classified cells: `10`.
- Completion: `100%`.

Status counts:

- `intervention_derived`: `4`.
- `biological`: `4`.
- `artifact`: `2`.
- `unresolved`: `0`.

## V12 Genetics Credential Limitation

The V12 prompt stated that `OPENGWAS_JWT` was available, but the environment
visible to this process returned `OPENGWAS_JWT_MISSING`. Therefore:

- no new OpenGWAS/LDSC/HDL runs were performed;
- no new MS-UC or MS-Crohn cross-trait colocalization was performed;
- V12 genetics cells are resolved at **supported** grade by triangulating
  existing project evidence and published genetics, not at robust coloc-grade.

This limitation is preserved in every genetics-cell report.

## Resolved Biological / Intervention-Derived Findings

### 1. UC Genetics Versus Treatment Response

File:

- `UC_GENETICS_TREATMENT_DECOUPLING_V12.md`

Resolved statement:

> MS and UC share upstream immune genetic liability, but UC treatment-response
> transfer depends on downstream mucosal inflammatory-state dynamics; shared
> genetic risk does not imply baseline IFN/APC response-stratifier transfer.

Tool ecosystems combined:

- published LDSC genetics from Yang et al. 2021;
- OpenTargets shared genetic target overlap;
- QTL/L2G target-resolution evidence;
- UC colon myeloid cell-state transcriptomics;
- V7 UC/IBD treatment-response cohorts.

MS consequence:

- UC genetics supports immune-risk hypothesis generation for MS.
- UC baseline mucosal IFN/APC response prediction does not transfer.
- The transferable readout is early compartment-relevant IFN/APC delta.

### 2. Crohn IFN/APC Versus Genetics

File:

- `CROHN_IFN_APC_GENETICS_DECOUPLING_V12.md`

Resolved statement:

> Crohn shares downstream colon myeloid IFN/APC inflammatory state with the
> MS-adjacent APC axis more strongly than it shares MS germline risk; this is
> downstream inflammatory convergence exceeding inherited-risk proximity.

Tool ecosystems combined:

- published LDSC genetics;
- OpenTargets shared target overlap;
- QTL/L2G and same-gene cell-state evidence;
- Crohn colon myeloid cell-state transcriptomics;
- IBD treatment/repair-response context.

MS consequence:

- Crohn can inform dynamic inflammatory-state monitoring hypotheses even though
  Crohn genetic target transfer to MS remains weaker than UC.

### 3. Crohn Genetics Versus Treatment/Repair Response

File:

- `CROHN_GENETICS_RESPONSE_REPAIR_DECOUPLING_V12.md`

Resolved statements:

> Crohn's intermediate MS genetic proximity does not prevent downstream mucosal
> treatment-response convergence; early IFN/APC downshift can converge
> downstream of different inherited causes.

> Crohn's intermediate MS genetic proximity does not prevent downstream
> tissue-repair / resolution-monitoring convergence, but the transferable
> concept is inflammatory-state downshift, not remyelination biology or shared
> causal genetics.

MS consequence:

- Crohn supports response-monitoring analogies, not direct genetic target
  transfer.

### 4. UC Static/Dynamic APC Decoupling

File:

- `UC_STATIC_DYNAMIC_APC_DECOUPLING_V11.md`

Resolved statement:

> UC is near MS on inflammatory IFN/APC state, but treatment-response transfer
> depends on dynamic IFN/APC downshift rather than baseline IFN/APC height.

MS consequence:

- In MS trials, test early compartmental IFN/APC delta as a pharmacodynamic
  readout; do not use baseline IFN/APC height as a transferred stratifier
  without direct MS validation.

### 5. RA Pregnancy/Treatment Decoupling

File:

- `RA_PREGNANCY_TREATMENT_DECOUPLING_V10.md`

Resolved statement:

> RA shares with MS a pregnancy/postpartum immune-kinetic axis but not the blood
> APC treatment-response architecture tested in V7.

MS consequence:

- RA is useful as a postpartum flare / hormonal timing comparator.
- RA blood APC response biomarkers should remain negative transfer comparators.

### 6. Sjogren Antigen-Presentation / Lysosomal-APC Decoupling

Files:

- `SJOGREN_SPLIT_AUDIT_V10.md`
- `analysis/v10_sjogren_gse23117/REPORT.md`

Resolved statement:

> Sjogren robustly supports antigen-presentation activation and does not show a
> matched APC lysosomal-repair signal; whole-gland bulk data are insufficient to
> rule out lipid-loader activation because lipid-loader is positive-null in
> bulk.

MS consequence:

- Sjogren can inform antigen-presentation comparison.
- It should not be used as evidence for MS chronic-active lesion-rim
  lysosomal/APC or foamy-myeloid biology without matched APC/spatial
  replication.

## Artifact / Scope Corrections

### UC Treatment Response Versus Tissue Repair

Resolution:

- Artifact / axis non-independence.

Reason:

- Treatment-response and tissue-repair axes reused overlapping dynamic IFN/APC
  evidence. This is not an independent axis disagreement.

### RA Tissue Repair Versus Pregnancy

Resolution:

- Artifact / axis-scope correction.

Reason:

- RA axis-08 far placement was supported mainly by blood anti-TNF
  response-monitoring failures. RA synovial tissue repair remains under-tested.

## Strongest Tool-Combination Finding

The strongest hard-for-humans V12 finding is the gut-disease layer split:

> UC is genetically closer to MS than Crohn, but both UC and Crohn converge
> downstream on mucosal IFN/APC dynamic response-monitoring. Therefore, genetic
> transfer and treatment-response biomarker transfer must be handled as
> different axes: UC is the better genetics comparator, while UC/Crohn both
> support dynamic inflammatory-state downshift as a response-monitoring analogy.

This finding depends on combining:

- published cross-disease genetic correlation;
- OpenTargets genetic target overlap;
- QTL/L2G and same-gene cell-state evidence;
- colon myeloid single-cell/transcriptomic module evidence;
- V7 treatment-response validation cohorts;
- V9 microbiome negative evidence showing the gut proximity is not explained by
  broad shared taxonomic dysbiosis.

No single ecosystem would produce the layer split. Genetics alone would
over-prioritize UC. Treatment-response alone would group UC/Crohn together.
Microbiome alone would not support broad MS/IBD taxonomic convergence.

## MS Transfer-Validity Map

| Comparator | Transfers to MS | Does not transfer |
| --- | --- | --- |
| UC | Genetic-risk hypothesis generation; dynamic IFN/APC pharmacodynamic readout design | Baseline mucosal IFN/APC response stratifier; anti-TNF therapeutic logic |
| Crohn | Dynamic mucosal inflammatory-state downshift analogy; response-monitoring design | UC-level genetic target transfer; Crohn causal architecture as MS architecture |
| RA | Pregnancy/postpartum timing and rebound hypotheses | Blood APC anti-TNF response biomarkers; global RA tissue-repair model |
| Sjogren | Antigen-presentation activation comparison | MS lesion-rim lysosomal/APC or foamy-myeloid repair biology without matched evidence |

## Falsification Path

For the gut-disease layer split:

1. Run in-process OpenGWAS/LDSC/HDL for MS-UC and MS-Crohn with sample-overlap
   and ancestry checks.
2. Run cross-trait colocalization at shared loci.
3. In Crohn-only and UC-only paired mucosal treatment cohorts, test whether
   early `-delta_IFN_APC` beats baseline IFN/APC as a response/readout feature.
4. In MS paired CSF/lesion-edge treatment cohorts, test whether early
   compartment-relevant `-delta_IFN_APC` tracks NfL, MRI activity, or other
   response/repair endpoints.

Stop-loss:

- If MS-Crohn colocalization is as strong as MS-UC and Crohn-only paired
  cohorts fail early `-delta_IFN_APC`, the current layer split is downgraded.
- If MS paired-compartment cohorts show no directionally consistent IFN/APC
  delta association with response or repair, the MS transfer-validity claim is
  downgraded to an IBD-only observation.

## Current Scope

This V12 synthesis completes the supported-cell matrix. It does not claim:

- a cure-class target;
- a validated MS clinical biomarker;
- a cross-trait colocalized causal gene;
- a direct drug-repositioning program.

It does claim:

- a completed axis-disagreement map at supported grade;
- a specific layer-decoupling rule for MS/IBD transfer;
- a resume-clean next state: no unresolved supported cells remain, and the next
  work is robust-grade genetics upgrade plus lower-grade/thin-axis population.
