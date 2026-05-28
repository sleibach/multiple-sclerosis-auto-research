# Wave 8 Candidate Breadth Scout

Role: focused data-breadth sidecar for `FABP5`, `MSR1`, `SCARB2`, `LGALS1`,
`LGALS3`, and adjacent lipid-lysosomal / glycan-checkpoint genes.

Returned: 2026-05-27.

Conclusion discipline: this is not a final finding. This report is a breadth
and contradiction scout for orchestrator vetting.

## Bottom Line

The five named candidates are weak as cross-autoimmune central nodes in the
current local evidence. The common pattern is MS white-matter support plus thin,
null, or contradictory non-MS h5ad breadth.

Current triage:

| Candidate | Scout call | Reason |
|---|---|---|
| `FABP5` | Best of the five, still weak | Strong MS and psoriasis keratinocyte signal, plus UC myeloid positive, but UC epithelial/stromal are negative in the same disease. |
| `MSR1` | Do not promote | MS-positive and older matrix-positive, but the direct broad h5ad pass has zero positive compartments and negative-leaning APC/skin trends. |
| `SCARB2` | Do not promote | MS-positive, but no direct non-MS positive breadth and a T1D ductal negative. |
| `LGALS1` | Do not promote yet | MS-positive with several non-MS positive-looking but non-nominal effects; no direct h5ad positive compartment. |
| `LGALS3` | Contradicted locally | Prior wave MS/MIMS2 rationale remains plausible, but broad h5ad shows Crohn and psoriasis negatives and only MS trend in this table. |

Pivot criterion is met. The named set should not be rescued by relaxing the
standard. If the orchestrator wants a next test, prioritize a small validation
panel rather than a promoted target claim: `ACSL3`, `APOC1`, `CD44`, `LAMP3`,
and `CTSL`, with `CHI3L1` as a positive-control benchmark rather than a novel
candidate.

## Evidence Sources Used

Local files read:

- `MILESTONE_2.md`
- `DATA_V3.md`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_lipid_lysosomal_neighborhood_rank.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_discovery_summary.json`
- `results_v3/geneformer_candidate_delete/geneformer_candidate_delete_gene_summary.tsv`
- `results_v3/geneformer_candidate_delete/geneformer_candidate_delete_metrics.tsv`
- `results_v3/geneformer_candidate_delete/summary.json`
- `subagents_v3/wave7_lipid_myeloid_target_scout_report.md`
- `subagents_v3/wave4_lipa_scout_report.md`

Supporting extract written:

- `subagents_v3/wave8_candidate_breadth_contrast_extract.tsv`

No heavy downloads were run. Web checks were limited to public validation dataset
triage links.

## Direct Local Breadth For Named Candidates

All broad h5ad non-MS effects below are donor-level log2-CPM contrasts from
`results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`. MS rows
are the imported local `GSE111972` white-matter microglia/macrophage statistics
in `broad_h5ad_lipid_lysosomal_neighborhood_rank.tsv`. The named candidates do
not have local Geneformer deletion support because they were not included in
`results_v3/geneformer_candidate_delete/summary.json` candidate genes.

| Gene | MS local anchor | Crohn | UC | Psoriasis | Sjogren | T1D | Main contradiction |
|---|---|---|---|---|---|---|---|
| `FABP5` | Positive: delta 1.265, g 1.355, p=0.00414, FDR=0.834 | No nominal; myeloid +0.970 p=0.140, stromal -1.24 p=0.240 | Mixed: myeloid +1.64 p=0.0281, epithelial -1.30 p=0.00533, stromal -1.70 p=0.0198 | Keratinocyte +3.86, g 5.2, p=0.00146 | Null; strongest stromal/endothelial -0.147 p=0.516 | Positive-looking but not nominal except endothelial trend: beta +1.68 p=0.345, endothelial +0.687 p=0.0593 | UC has opposite-sign compartments; psoriasis signal is keratinocyte, not APC. |
| `MSR1` | Positive: delta 0.566, g 1.025, p=0.0313, FDR=0.851 | No nominal; myeloid -0.783 p=0.360 | No nominal; myeloid -1.17 p=0.183 | No nominal; APC -1.07 p=0.0512, stromal -0.944 p=0.177 | APC negative trend: -0.457 p=0.0535 | Null; beta +0.564 p=0.538 | Older matrix says Crohn/Sjogren/UC/lupus nephritis/psoriasis positive, but direct h5ad pass finds zero positives. |
| `SCARB2` | Positive: delta 0.526, g 1.437, p=0.00484, FDR=0.834 | Null | Null; myeloid -0.358 p=0.417 | Null | APC +0.573 p=0.349, not nominal | Ductal negative: -0.274 p=0.0236 | MS-only signal with a T1D contradiction and no positive non-MS disease. |
| `LGALS1` | Positive: delta 1.013, g 1.540, p=0.00202, FDR=0.834 | Null; myeloid -0.411 p=0.228 | Null | Positive-looking but not nominal: APC +1.05 p=0.223, stromal +0.935 p=0.101 | Null | Positive-looking but not nominal: acinar +0.829 p=0.107, beta +1.96 p=0.268, endothelial +0.533 p=0.078 | MS-positive but no direct h5ad positive compartments. |
| `LGALS3` | Trend only in this broad table: delta 0.778, g 0.925, p=0.0509, FDR=0.879 | Negative in all tested compartments: epithelial -0.646 p=0.0302, myeloid -1.13 p=0.00497, stromal -0.585 p=0.00451 | Null to negative | Keratinocyte negative trend -1.12 p=0.058; stromal -0.540 p=0.0402 | Null | Beta positive trend +1.07 p=0.0554 | Strongest glycan-checkpoint candidate mechanistically, but directly contradicted in Crohn and psoriasis. |

Direct FDR note: none of the five named candidates had a non-MS positive FDR10
compartment in the broad h5ad pass. `FABP5` has the strongest nominal non-MS
signals, but the same UC dataset contains both positive myeloid and negative
epithelial/stromal effects.

## Adjacent Geneformer Context

The Geneformer deletion screen does not directly test `FABP5`, `MSR1`,
`SCARB2`, `LGALS1`, or `LGALS3`. Relevant adjacent genes in
`geneformer_candidate_delete_gene_summary.tsv`:

| Gene | Contexts with token | Disease cells with token | Mean cosine shift | Mean projection shift | Support contexts | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| `LIPA` | 2 | 6 | 0.000763 | -0.00452 | 2 | Weak/limited support; already demoted as compartment-restricted and myeloid-conflicted. |
| `SNX10` | 3 | 10 | -0.000312 | -0.0502 | 2 | Context support flags exist, but aggregate direction is negative. |
| `CHI3L1` | 4 | 18 | -0.000146 | 0.0441 | 1 | Mixed/weak despite strong expression breadth. |
| `LTA4H` | 4 | 6 | -0.000289 | -0.00278 | 0 | Negative by the posthoc rule; keep demoted. |

## Pivot Shortlist From Lipid-Lysosomal Rank

This is a next-validation shortlist, not promotion. Ranking favors better local
breadth than the named five, some intervention plausibility, and a path to
falsification in RA/SLE/MS. `CHI3L1` is included as a benchmark despite prior-art
burden because it is the strongest local lipid-neighborhood row.

| Rank | Gene | Local breadth signal | Why test next | Key caveat |
|---:|---|---|---|---|
| 1 | `ACSL3` | Positive in 3 diseases / 5 compartments, no negatives; Crohn epithelial +1.07 p=5.86e-05 FDR=0.0365, Crohn stromal +0.806 p=0.00859, UC epithelial +0.896 p=0.0295, UC stromal +0.388 p=0.0182, T1D endothelial +0.965 p=0.0318. | Underexplored lipid-handling enzyme relative to demoted `ACSL1`; test whether it is a recurrent epithelial/stromal lipid-stress node. | MS anchor is weak/null: delta 0.221, p=0.275. Needs RA/SLE/MS replication before elevation. |
| 2 | `APOC1` | Positive in 3 diseases with MS nominal positive: MS delta 0.806 p=0.0333; Sjogren epithelial +1.18 p=0.00967; T1D acinar +1.51 p=0.00775; UC epithelial +1.28 p=0.0473. | Secreted/lipoprotein biology gives intervention and biomarker tractability; adjacent to lipid-loaded phagocyte biology. | UC stromal negative -1.57 p=0.0468 and psoriasis keratinocyte negative trend; compartment direction may be disease-specific. |
| 3 | `CD44` | MS positive delta 1.345 p=0.0332; Crohn epithelial +1.24 p=0.00208 and myeloid +0.805 p=0.0119; UC epithelial +1.97 p=0.00158 FDR=0.0852. | Surface receptor with intervention precedent; useful to test macrophage retention / tissue-injury interface. | Broad prior art and UC stromal negative -0.482 p=0.0162; not an undercrowded target. |
| 4 | `LAMP3` | Strong Crohn/UC myeloid positives: Crohn myeloid +4.27 p=9.16e-06 FDR=0.0376; UC myeloid +3.65 p=1.48e-04 FDR=0.044; MS trend +1.113 p=0.159. | Lysosomal/DC activation marker could separate antigen-presenting lysosomal states from generic IFN. | UC epithelial negative -0.594 p=0.0398; intervention as direct target is poor, likely state marker first. |
| 5 | `CTSL` | MS nominal positive delta 0.406 p=0.0338; psoriasis keratinocyte +2.27 p=0.0048; UC myeloid +1.86 p=0.0229. | Enzyme tractability and lysosomal biology are real; useful comparator against `LGALS3` and `FABP5`. | UC epithelial negative -1.79 p=0.039; cathepsin repair/specificity and prior-art risks are serious. |
| Benchmark | `CHI3L1` | Strongest local row: MS delta 2.007 p=0.00461; positive in Crohn, UC, T1D; UC stromal +5.94 p=5.62e-04 FDR=0.0627. | Positive-control for breadth and MS anchoring; useful to calibrate validation datasets. | Heavy biomarker/prior-art burden and weak Geneformer support; do not call novel. |

Genes not prioritized despite high rank:

- `CALR`: broad Crohn/UC/psoriasis signal, but MS direction is negative
  (delta -0.363, p=0.0596).
- `CTSB`: psoriasis/UC positives, but MS is null/negative (delta -0.060,
  p=0.814).
- `SPP1`: local T1D/UC positives but weak MS single-gene support and crowded
  prior art.
- `MARCO`: strong IBD myeloid signal but MS is negative-trending.
- `TBXAS1`: psoriasis/UC epithelial positives but MS is null/negative and
  lipid-mediator prior-art risk remains high.

## Public Datasets To Validate Next

At least two independent public datasets can test whether the named candidates
or pivot shortlist replicate outside the current local h5ads.

1. AMP RA Phase II synovium single-cell / CITE-seq.
   - Link: `https://immunogenomics.io/ampra2/`
   - Use: validate RA synovial macrophage, fibroblast, endothelial, and T cell
     compartments for `FABP5`, `MSR1`, `LGALS3`, `CD44`, `ACSL3`, `APOC1`,
     `LAMP3`, and `CTSL`.
   - Access note: more tractable than the currently blocked local
     `E-MTAB-8322.project.h5ad` route because the AMP page points to public
     Synapse resources and processed analysis artifacts.

2. AMP Phase I RA and lupus nephritis single-cell portal / ImmPort resources.
   - Link: `https://singlecell.broadinstitute.org/single_cell/study/SCP279/amp-phase-1`
   - Use: independent RA synovium and lupus nephritis immune/kidney validation,
     especially for the contradiction pattern: `MSR1`/`LGALS3` macrophage
     direction, `CD44` tissue injury, and `APOC1` epithelial/myeloid split.
   - Access note: public portal plus ImmPort-backed datasets; may require
     account or controlled-access steps for full matrices, but cell browser
     triage is fast.

3. MS white-matter single-nucleus datasets on CELLxGENE / primary MS snRNA
   studies.
   - CELLxGENE entry point:
     `https://cellxgene.cziscience.com/collections`
   - Literature example for human MS white matter single-nucleus work:
     `https://www.nature.com/articles/s41586-019-1404-z`
   - Use: replicate the `GSE111972` sorted-microglia MS anchor in independent
     lesion, normal-appearing white matter, oligodendrocyte, astrocyte, and
     microglial compartments; especially important for `LGALS3`, `FABP5`,
     `LGALS1`, `SCARB2`, and `APOC1`.

4. SLE/lupus nephritis kidney single-cell datasets in public kidney/immune
   portals.
   - Starting point: search ImmPort and Single Cell Portal for lupus nephritis
     AMP datasets linked from the AMP Phase I study above.
   - Use: test whether lipid/lysosomal/glycan signals are kidney-infiltrating
     immune, tubular epithelial, endothelial, or stromal, and whether `FABP5`
     older matrix SLE positives reproduce.

Suggested validation design:

- Use donor-level pseudobulk by disease, compartment, and dataset.
- Keep MS, RA, and SLE/lupus nephritis as independent validation diseases, not
  just more IBD/skin/islet evidence.
- Require same-direction replication in at least two independent validation
  datasets before any target moves beyond scout status.
- For `LGALS3` and `FABP5`, pre-register contradiction checks: myeloid/APC vs
  epithelial/stromal effects must not flip within the same disease unless the
  mechanism explicitly explains the flip.

## Commands Used

```bash
pwd && rg --files | rg '(^MILESTONE_2\.md$|results_v3/(broad_h5ad_gene_discovery|geneformer_candidate_delete)|subagents_v3)'
git status --short
sed -n '1,220p' MILESTONE_2.md
head -5 results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_summary.tsv
wc -l results_v3/broad_h5ad_gene_discovery/*.tsv
head -5 results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv
head -5 results_v3/broad_h5ad_gene_discovery/broad_h5ad_lipid_lysosomal_neighborhood_rank.tsv
head -5 results_v3/geneformer_candidate_delete/geneformer_candidate_delete_gene_summary.tsv
head -5 results_v3/geneformer_candidate_delete/geneformer_candidate_delete_metrics.tsv
rg -n "FABP5|MSR1|SCARB2|LGALS1|LGALS3|GPNMB|SNX10|C15ORF48|LIPA|LTA4H|CHI3L1" subagents_v3 results_v3/geneformer_candidate_delete results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_discovery_summary.json scripts/v3_broad_h5ad_gene_discovery.py
cat results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_discovery_summary.json
cat results_v3/geneformer_candidate_delete/summary.json
cat results_v3/geneformer_candidate_delete/geneformer_candidate_delete_summary.json
awk -F'\t' 'NR==1 || $1 ~ /^(FABP5|MSR1|SCARB2|LGALS1|LGALS3|GPNMB|SNX10|C15ORF48|LIPA|LTA4H|CHI3L1|CALR|ACSL3|IFI30)$/' results_v3/broad_h5ad_gene_discovery/broad_h5ad_lipid_lysosomal_neighborhood_rank.tsv
awk -F'\t' 'NR==1 || $1 ~ /^(FABP5|MSR1|SCARB2|LGALS1|LGALS3|GPNMB|SNX10|C15ORF48|LIPA|LTA4H|CHI3L1|CALR|ACSL3|IFI30)$/' results_v3/geneformer_candidate_delete/geneformer_candidate_delete_gene_summary.tsv
sed -n '1,220p' DATA_V3.md
sed -n '1,230p' subagents_v3/wave7_lipid_myeloid_target_scout_report.md
sed -n '230,470p' subagents_v3/wave7_lipid_myeloid_target_scout_report.md
sed -n '1,170p' subagents_v3/wave4_lipa_scout_report.md
python3 - <<'PY'
# standard-library TSV extraction and disease-by-disease summaries for target
# and adjacent genes; wrote subagents_v3/wave8_candidate_breadth_contrast_extract.tsv
PY
```

Web checks used for public validation dataset triage:

```text
site:cellxgene.cziscience.com rheumatoid arthritis synovium h5ad single cell
site:cellxgene.cziscience.com lupus nephritis single cell h5ad
site:cellxgene.cziscience.com multiple sclerosis lesion h5ad single nucleus
rheumatoid arthritis synovium single cell RNA seq dataset h5ad public
single cell lupus nephritis h5ad public dataset
multiple sclerosis single nucleus RNA seq lesions h5ad public dataset
```
