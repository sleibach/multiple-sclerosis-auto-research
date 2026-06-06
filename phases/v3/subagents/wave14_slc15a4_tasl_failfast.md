# Wave 14 SLC15A4/TASL/IRF5 Fail-Fast

**Recommendation: NO-GO as a cross-autoimmune central/intervention candidate.**

The branch is real biology and is highly relevant to lupus biology, but the V3 fail-fast gate does not support a broad cross-autoimmune intervention claim. Local recurrence is trend-level and uneven, genetics are dominated by IRF5 plus SLE-heavy SLC15A4/TASL signals, and the available perturbation/LINCS artifacts do not directly test branch inhibition against IFN/HLA-II/CD74 downshift.

## Artifacts

- Script: `scripts/v3_wave14_slc15a4_tasl_failfast.py`
- Output directory: `results_v3/wave14_slc15a4_tasl_failfast/`
- Key tables:
  - `branch_gene_summary.tsv`
  - `branch_module_summary.tsv`
  - `branch_genetics_summary.tsv`
  - `perturbation_evidence_summary.tsv`
  - `mixscale_top_downstream_controls.tsv`
  - `l1000_generic_inflammatory_reversal_hits.tsv`
  - `summary.json`

## Method

I tested `SLC15A4`, `TASL/CXorf21`, `IRF5`, `TLR7`, `TLR8`, `TLR9`, and `UNC93B1` across the existing V3 direct h5ad disease compartments using donor-level pseudobulk expression and control-standardized z scores. `TASL` and `CXorf21` were collapsed to `TASL_CXorf21`. I added MS white-matter microglia gene-level rows from `results_v3/gse111972_full_ms_wm_signature.tsv`.

Support levels are deliberately weak/transparent: FDR <= 0.10 is `fdr10_positive`; nominal p <= 0.10 with positive delta is only `trend_positive`. All local branch gene and module summaries below have **0 FDR10-positive diseases**.

All 18 direct h5ad compartment runs completed. TLR9 was absent from the RA and T1D matrices, so its gene summary has fewer local tests.

## Local Expression

From `branch_gene_summary.tsv`:

| gene | diseases tested | FDR10+ | trend-or-better diseases | median positive Hedges g | supporting diseases |
|---|---:|---:|---:|---:|---|
| SLC15A4 | 7 | 0 | 4 | 1.39 | Crohn, MS, psoriasis, UC |
| TASL_CXorf21 | 7 | 0 | 3 | 1.57 | Sjogren, psoriasis, UC |
| TLR8 | 7 | 0 | 3 | 1.21 | Crohn, psoriasis, UC |
| UNC93B1 | 7 | 0 | 2 | 1.88 | Crohn, psoriasis |
| IRF5 | 7 | 0 | 0 | NA | none |
| TLR7 | 7 | 0 | 0 | NA | none |
| TLR9 | 5 | 0 | 0 | NA | none |

Best local examples are still nominal only after multiple testing. SLC15A4 had Crohn myeloid p=0.0073 but FDR=0.599; TASL/CXorf21 had psoriasis APC p=0.026 and UC myeloid p=0.029 but FDR=0.599. IRF5, despite strong genetics, did not recur transcriptionally in the local disease/control contrasts.

## Branch Modules

From `branch_module_summary.tsv`:

| module | diseases tested | FDR10+ | trend-or-better diseases | supporting diseases |
|---|---:|---:|---:|---|
| full_slc15a4_tasl_tlr_irf5_branch | 6 | 0 | 2 | Crohn, psoriasis |
| endosomal_tlr_sensor_chaperone | 6 | 0 | 2 | Crohn, psoriasis |
| slc15a4_tasl_irf5_core | 6 | 0 | 2 | Crohn, psoriasis |

This is weaker than the broad IFN/HLA/CD74 state already present in V3: `cross_disease_module_summary.tsv` has `ifn_apc` trend-or-better in 7/10 diseases, `mif_cd74_receptor_state` in 7/10, and `hla_ii_apc` in 6/9. The state recurs more broadly than the branch genes/modules.

## Genetics

From `tmp_v3/wave13_opentargets_gwas_credible_sets.tsv`, summarized in `branch_genetics_summary.tsv`:

| gene | diseases queried | diseases with evidence | max score | total evidence count | evidence diseases |
|---|---:|---:|---:|---:|---|
| IRF5 | 12 | 9 | 0.919 | 76 | UC, SLE, RA, Sjogren, Crohn, psoriasis, MS, AS, PBC |
| TASL_CXorf21 | 12 | 2 | 0.885 | 2 | RA, SLE |
| SLC15A4 | 12 | 1 | 0.892 | 8 | SLE |
| TLR7 | 12 | 1 | 0.081 | 1 | SLE |
| TLR8 | 12 | 0 | 0 | 0 | none |
| TLR9 | 0 | 0 | 0 | 0 | not queried in this file |
| UNC93B1 | 12 | 0 | 0 | 0 | none |

Interpretation: genetics support is not branch-balanced. IRF5 is broad, but SLC15A4/TASL/TLR7 support is SLE/RA-heavy, with SLC15A4 itself only positive for SLE in this local OpenTargets extract.

## Perturbation/LINCS

From `perturbation_evidence_summary.tsv`:

| source | direct branch perturbation rows | generic downstream rows | interpretation |
|---|---:|---:|---|
| MixScale transition controller rank | 0 | 12 | no direct branch perturbation; IFN/JAK/STAT controls suppress IFN/HLA/CD74 modules |
| L1000FWD/CMap reversal hits | 0 | 3 | no branch-targeted reversal hit; generic JAK/IKK/NFKB hits are not branch-specific |
| Geneformer phagolysosomal delete | 0 | 0 | branch genes absent from available delete summary |

The strongest local perturbation evidence is downstream, not branch-specific: MixScale IFNG `IFNGR1` perturbation suppresses all 4 tracked modules with `transition_suppression_score=2.49`, `ifn_apc_mean_log2fc=-1.49`, `hla_ii_apc_mean_log2fc=-1.60`, and `mif_cd74_receptor_state_mean_log2fc=-0.53`. That proves IFN/HLA/CD74 state controllability, not SLC15A4/TASL branch intervention.

The L1000FWD filter found no direct branch/TLR hit. The only strong generic inflammatory reversal was tozasertib/JAK inhibitor against `ifn_lysosomal_apc_state` (`q=6.1e-5`), again downstream and non-specific.

## Public Prior Art Check

Verified public sources make the branch mechanistically and therapeutically crowded, especially in lupus:

- Nature 2020 identified TASL/CXorf21 as the SLC15A4-associated adaptor that links endolysosomal TLR7/8/9 to IRF5 and explains SLE genetic involvement: https://www.nature.com/articles/s41586-020-2282-0
- Cell Reports 2023 reported SLC15A4 controls endolysosomal TLR7-9 responses by recruiting TASL; the abstract explicitly frames the SLC15A4-TASL complex as a therapeutic strategy for SLE and related diseases: https://pubmed.ncbi.nlm.nih.gov/37527038/
- Nature Chemical Biology 2024 reported first-in-class functional SLC15A4 inhibitors, including AJ2-30, suppressing SLC15A4-mediated TLR/NOD inflammatory functions and lupus patient PBMC cytokines: https://www.nature.com/articles/s41589-023-01527-8
- TLR7/8 is clinically prior-arted in lupus. Enpatoran has phase 2 SLE/CLE data and WILLOW registration; afimetoran/BMS-986256 has an active SLE trial record. Public records searched May 27, 2026: https://pubmed.ncbi.nlm.nih.gov/42107374/ and https://clinicaltrials.gov/study/NCT04895696
- IRF5 is also an explicit lupus therapeutic target in preclinical literature: https://pubmed.ncbi.nlm.nih.gov/34282144/

## Call

**No-go for V3 cross-autoimmune central/intervention nomination.**

Rationale:

1. Local recurrence does not clear a robust cross-disease bar: no branch gene or branch module has FDR10-positive recurrence.
2. The broad IFN/HLA-II/CD74 APC state is more recurrent than this upstream branch.
3. Genetics are branch-imbalanced: IRF5 is broad, but SLC15A4/TASL/TLR7 are mostly SLE/RA, not cross-autoimmune.
4. Available perturbation artifacts do not connect direct SLC15A4/TASL/TLR/IRF5 inhibition to IFN/HLA-II/CD74 downshift.
5. Prior art is strong: TLR7/8 inhibitors are in lupus clinical development and SLC15A4 inhibitors/TASL biology are already published.

Best disposition: keep as a lupus-biased mechanistic comparator or upstream explanation for IFN/HLA/CD74 biology, but do not advance as a novel cross-autoimmune intervention candidate without direct branch perturbation data across non-lupus APC contexts.
