# Wave87 Cross-Disease Circuit Evidence Sidecar

Timestamp: 2026-05-27

Scope: sidecar review only. I do not claim a therapeutic finding. I interrogated local V3/V2 outputs around the Wave86 anti-TNF nonresponse circuit genes `IL1B`, `CXCL8`, `TREM1`, `OSM`, `SPP1`, `ACSL1`, `IFI30`, and `LAMP3`, with limited verified literature context where local files already pointed to PubMed records.

Final call: **PARK**

Reason: the eight-gene circuit is a strong IBD anti-TNF nonresponse signal, and `IL1B`/`LAMP3` partially replicate in RA baseline anti-TNF nonresponse. However, no single gene from this set has verified local breadth across five autoimmune diseases with multiple independent evidence channels. MS gene-level support is weak in the checked local microglia/white-matter dataset, and target-resolved genetics is insufficient except for a narrow `IFI30` MS/Crohn/celiac signal that has poor druggability and no response breadth.

## Local Row Ledger

Primary inspected TSVs and rows:

- `results_v3/wave86_external_geo_antitnf_gene_driver/external_geo_gene_meta_rank.tsv`, rows 2-4 and 9-13: all eight genes are IBD anti-TNF nonresponse anchors across four baseline IBD contexts.
- `results_v3/wave87_cross_system_antitnf_resistance_gene_check/cross_system_antitnf_gene_integration.tsv`, rows 7, 14-17, 20, 25-26: cross-system IBD-to-RA anti-TNF replication check.
- `results_v3/wave87_cross_system_antitnf_resistance_gene_check/ra_synovium_baseline_gene_response_tests.tsv`, rows 2, 3, 5, 6, 13, 19, 20, 23: RA synovium baseline gene-response test.
- `results_v3/cross_disease_gene_summary.tsv`, rows 13, 25, 27, 31, 32, 35, 36, 39: direct H5AD cross-disease gene breadth summary for the eight genes.
- `data/derived_v3/disease_axis_evidence_v3.tsv`, rows 2-7, 9, 11: disease-level lipid/lysosomal/myeloid axis evidence summary.
- `results_v3/gse111972_full_ms_wm_signature.tsv`, rows 3028, 5144, 7144, 13722, 14276, 15102, 16589, 17150: MS white-matter microglia gene-level checks for all eight genes.
- `results_v3/direct_h5ad_gene_replication/direct_h5ad_gene_donor_comparisons.tsv`, rows 112-219 and 332-439: Crohn and UC myeloid direct H5AD gene checks; rows 442-619: psoriasis skin compartments; rows 732-949: Sjogren gland compartments; rows 952-1279: T1D pancreatic compartments.
- `results_v2/cross_autoimmune_target_gene_contrasts.tsv`, rows 28-100: psoriasis bulk/paired skin; rows 106-207: IBD bulk mucosa; rows 214-256: lupus nephritis kidney compartments.
- `results_v2/extended_autoimmune_target_gene_contrasts.tsv`, rows 2, 7, 17, 21, 27, 32, 42, 46, 52, 57, 67, 71: SLE sorted blood subset checks.
- `results_v3/wave62_opentargets_target_resolution/target_resolution_summary.tsv`, row 32; `opentargets_l2g_rows.tsv`, rows 29 and 164; `opentargets_qtl_coloc_rows.tsv`, rows 146, 154, 1068, 1077, 5119, 14716, 15175, 15479: `IFI30` genetics and QTL colocalization checks.

## Circuit-Level Summary

### IBD Anti-TNF Response

Wave86 is the strongest local evidence channel. In `external_geo_gene_meta_rank.tsv`, all eight requested genes are called `GENE_LEVEL_ANTITNF_NONRESPONSE_ANCHOR` across four IBD baseline contexts:

| Gene | nonresponse-high contexts | nominal contexts | FDR10 contexts | weighted mean Hedges g, responder-minus-non | median AUC high-score nonresponse |
| --- | ---: | ---: | ---: | ---: | ---: |
| `IL1B` | 4/4 | 3 | 3 | -1.695 | 0.897 |
| `CXCL8` | 4/4 | 3 | 3 | -1.702 | 0.885 |
| `TREM1` | 4/4 | 3 | 3 | -1.629 | 0.883 |
| `ACSL1` | 4/4 | 3 | 2 | -1.328 | 0.822 |
| `IFI30` | 4/4 | 3 | 2 | -0.975 | 0.795 |
| `OSM` | 4/4 | 2 | 2 | -1.431 | 0.815 |
| `SPP1` | 4/4 | 2 | 2 | -1.234 | 0.785 |
| `LAMP3` | 4/4 | 2 | 2 | -1.097 | 0.759 |

Interpretation: this is a real IBD baseline anti-TNF nonresponse circuit in local data. It does not by itself prove a causal cell-cell mechanism or cross-autoimmune target status.

### RA Anti-TNF Response

Wave87 RA synovium baseline response is the main cross-system response test. Only two requested genes meet RA directional replication:

| Gene | RA Hedges g responder-minus-non | AUC high-score nonresponse | p | FDR | RA call |
| --- | ---: | ---: | ---: | ---: | --- |
| `LAMP3` | -0.927 | 0.786 | 0.00238 | 0.0261 | directional replication |
| `IL1B` | -0.588 | 0.701 | 0.0407 | 0.0995 | directional replication |
| `CXCL8` | -0.237 | 0.538 | 0.431 | 0.603 | same direction weak |
| `OSM` | -0.288 | 0.560 | 0.439 | 0.603 | same direction weak |
| `TREM1` | +0.704 | 0.330 | 0.0371 | 0.0995 | opposite direction |
| `ACSL1` | +0.180 | 0.451 | 0.527 | 0.682 | no replication |
| `SPP1` | +0.118 | 0.504 | 0.648 | 0.757 | no replication |
| `IFI30` | +0.081 | 0.449 | 0.801 | 0.839 | no replication |

Interpretation: `IL1B` and `LAMP3` are the only cross-response genes I would keep open. `TREM1`, `ACSL1`, `SPP1`, and `IFI30` fail the RA response check; `CXCL8` and `OSM` are directionally compatible but statistically weak.

## Per-Disease Evidence Channels

Evidence-channel labels:

- Cell state: local single-cell/spatial/module or bulk tissue expression evidence.
- Response: local anti-TNF or therapy-response association.
- Genetics: local target-resolved GWAS/QTL/coloc evidence.
- Perturbation: direct perturbation or intervention evidence; local direct evidence preferred, verified literature noted separately.
- Clinical: clinical/prior-art context, not used as proof of mechanism.

| Disease | Cell state | Response | Genetics | Perturbation | Clinical/prior art | Sidecar interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| MS | Disease-axis evidence supports a lesion lipid/lysosomal/AP myeloid state, but not the eight-gene response circuit specifically. In GSE111972 white-matter microglia, all eight genes have FDR 0.899-0.999. `LAMP3` has the largest delta among the eight but p=0.159/FDR=0.899. | No local anti-TNF or analogous response evidence for these genes. | `IFI30` has MS L2G and monocyte eQTL colocalization support: L2G 0.650/0.645 and monocyte eQTL H4 0.961-0.996 in Wave62 rows. Other genes lack comparable target-resolved MS support in local outputs. | No local perturbation evidence for the eight-gene circuit. Verified OSM literature in EAE/remyelination is directionally complex and can be protective, so OSM is not a clean MS inhibition target. | No local clinical response dataset. OSM biology is not straightforwardly pro-inflammatory in CNS context. | Weak for the Wave86 circuit. MS supports the broader lipid/lysosomal lesion module, not a single one of these eight genes as cross-disease anchor. |
| RA | Local disease-axis row supports SPP1/STAT1 macrophage states but notes GSE97779 macrophage contrast is confounded. | Strongest response replication is `LAMP3` and `IL1B` in GSE198520 baseline RA synovium. `CXCL8`/`OSM` weak same-direction; others fail or oppose. | No broad local genetics support for the eight genes as RA anchors. Prior Wave55/Wave62 point more toward receptor/axis-level signals such as OSMR, not `OSM` itself. | Verified anti-OSM monoclonal antibody RA trial exists, but that is prior art and not local perturbation validation for the eight-gene circuit. | Anti-OSM RA trial prior art: GSK315234 was tested in RA. | Partial. RA keeps `IL1B`/`LAMP3` open as response biomarkers, not as proven causal targets. |
| Crohn disease | Direct H5AD Crohn myeloid rows show nominal increases for `ACSL1` delta 1.702 p=0.0145, `IL1B` delta 1.062 p=0.0292, `LAMP3` delta 0.751 p=0.0137, `OSM` delta 0.494 p=0.0382, and `TREM1` delta 2.547 p=0.0471, but FDRs are not strong. Older bulk GSE75214 active CD ileum shows positive disease association for `ACSL1`, `SPP1`, `IFI30`, and `IL1B`. | Strong Wave86 anti-TNF nonresponse signal across all eight genes. | `IFI30` has Crohn pQTL coloc row H4 0.838 but posterior condition flag is not strong enough to treat as broad causal anchor. | No local direct perturbation. | OSM in IBD anti-TNF nonresponse is verified prior art. | Strongest disease for the circuit, but not enough for pan-autoimmune mechanism alone. |
| Ulcerative colitis | Direct H5AD UC myeloid rows show nominal increases for `ACSL1` delta 1.978 p=0.0228, `CXCL8` delta 1.103 p=0.00116, `IFI30` delta 0.765 p=0.0365, `IL1B` delta 1.265 p=0.0116, `OSM` delta 0.826 p=0.0357, and `TREM1` delta 3.542 p=0.0103; FDRs are modest. Older bulk GSE75214 UC active colon supports `ACSL1`, `SPP1`, `IFI30`, and `IL1B` strongly but is cell-composition confounded. | Strong Wave86 anti-TNF nonresponse signal across all eight genes. | No clean target-resolved local genetics for a single requested gene as UC anchor; receptor/axis evidence is stronger for OSMR than `OSM`. | No local direct perturbation. | OSM predicts anti-TNF response in IBD and is prior art. | Strong with Crohn as IBD. Still an IBD-centered anti-TNF nonresponse circuit. |
| Psoriasis | Older paired bulk GSE13355 involved-vs-uninvolved shows `IFI30` delta 0.856 p=3.51e-11, `IL1B` delta 1.012 p=3.51e-11, `SPP1` delta 0.297 p=3.74e-4, and `ACSL1` negative delta -0.480 p=6.10e-8. Direct H5AD skin APC/keratinocyte rows for the eight genes are mostly weak or nonsignificant in the inspected small donor setting. | No local anti-TNF nonresponse replication for the eight-gene circuit. | Local target sweeps previously favored OSMR/axis-level signals more than these eight genes; not enough to count a single-node genetic anchor here. | No local direct perturbation. | OSMR blockade has skin-disease clinical precedent, which is prior art and not psoriasis-specific proof for this circuit. | Partial disease-inflammation support, weak circuit-specific support. |
| SLE / lupus nephritis | Lupus nephritis GSE32591 has strong `IFI30` kidney signal: tubulointerstitium delta 0.603 p=1.37e-6 and glomeruli delta 2.528 p=1.68e-11. `IL1B` is contradictory: tubulointerstitium delta -0.223 p=7.38e-4, glomeruli delta 0.473 p=0.089. Sorted SLE blood myeloid GSE10325 has `ACSL1` delta 1940.5 p=0.0219 but `IFI30`, `SPP1`, and `IL1B` are not significant in myeloid rows. | No local anti-TNF response evidence. | No clean target-resolved genetics for a single requested gene as SLE anchor in inspected local outputs. | No local direct perturbation. | No clinical circuit-specific evidence inspected. | `IFI30` is the strongest SLE/LN cell-state gene among the eight, but lacks response and druggability support. |
| Sjogren syndrome | Disease-axis row supports IFN/APC recurrence and includes `LAMP3`, but direct H5AD salivary APC/epithelial rows mostly fail for the eight genes. Notable opposite/negative rows: APC `SPP1` delta -0.182 p=0.0383 and APC `OSM` detection delta -0.0443 p=0.0434, with FDR not strong. Epithelial `IL1B` detection delta 0.00098 p=0.0416 but FDR 0.280. | No local response evidence. | No target-resolved local genetics for these genes. | No local direct perturbation. | No clinical circuit-specific evidence inspected. | Weak. The broader IFN/APC axis appears, but the Wave86 genes do not carry it cleanly. |
| Type 1 diabetes | Disease-axis row supports islet/cytokine perturbation IFN/AP genes. Direct H5AD rows show strong-looking `CXCL8` increases in acinar and ductal cells: acinar mean delta 1.215 p=0.0191, detection delta 0.415 p=0.0152; ductal mean delta 1.052 p=0.0116, detection delta 0.383 p=0.0108. `SPP1` has large positive deltas but weaker p values. | No local anti-TNF response evidence. | Local genetics not sufficient for a requested single gene. | T1D axis row mentions cytokine perturbation evidence at pathway level, but no direct local perturbation of the eight genes was inspected here. | No clinical circuit-specific evidence inspected. | Partial cell-state support through `CXCL8`/`SPP1`, not enough for pan-autoimmune circuit call. |

## Strongest and Weakest Genes

Strongest by local anti-TNF response breadth:

- `IL1B`: strongest overall response evidence. It is a Wave86 IBD anchor and RA directional replication gene. Weakness: MS gene-level support is absent in GSE111972; SLE direction is inconsistent across kidney compartments; broad genetics is not adequate.
- `LAMP3`: cleanest RA replication among the eight (`AUC high-score nonresponse` 0.786, FDR 0.0261) and also an IBD anchor. Weakness: broader disease cell-state evidence is inconsistent, and it may be a dendritic/APC-state marker rather than a causal node.

Strongest by disease/injury cell-state breadth:

- `IFI30`: best genetics-adjacent support because Wave62 resolves an MS locus to `IFI30` with L2G around 0.65 and monocyte eQTL colocalization H4 above 0.96. It also has lupus nephritis kidney signal and appears in IBD/psoriasis inflammatory tissue contexts. Weakness: it fails RA response replication, direct H5AD breadth summary is modest, and as a lysosomal antigen-processing enzyme it is a difficult and risky drug target.
- `IL1B`: appears across IBD response, RA response, IBD myeloid disease-state rows, psoriasis bulk, and some Sjogren/T1D epithelial/islet trends. Weakness: this breadth is largely generic inflammation, and `IL1B` is not novel or selective.

Weakest as cross-autoimmune anti-TNF nonresponse nodes:

- `SPP1`: broad inflammatory/tissue-remodeling marker, but no RA anti-TNF response replication and weak direct H5AD breadth for this specific circuit. It remains a state marker more than a central node here.
- `ACSL1`: strong IBD response and UC/Crohn myeloid signal, but RA response is opposite/absent and MS GSE111972 is null. Prior ACSL1 target hypothesis remains demoted.
- `TREM1`: very strong IBD response/cell-state gene, but RA baseline direction is opposite despite nominal p=0.0371; that is a serious cross-disease warning.

Special case:

- `OSM`: biologically and clinically important in IBD and probably skin/RA axes, but heavily prior-arted and CNS-directionally ambiguous. Local evidence points more toward OSM/OSMR axis context than `OSM` as a novel single central node. In MS/EAE/remyelination literature, OSM can be protective, which blocks a simple cross-autoimmune inhibition story.

## Does Any Single Node Have Breadth in >=5 Diseases?

No, not under the required standard.

Using the direct local H5AD breadth summary in `results_v3/cross_disease_gene_summary.tsv`:

- `IL1B`: trend-or-better in 3 diseases (`Crohn disease`, `Sjogren syndrome`, `ulcerative colitis`).
- `IFI30`: trend-or-better in 2 diseases (`Hashimoto thyroiditis`, `ulcerative colitis`), despite stronger genetics/lupus evidence outside this summary.
- `CXCL8`: trend-or-better in 2 diseases (`type 1 diabetes mellitus`, `ulcerative colitis`).
- `TREM1`, `LAMP3`, `ACSL1`, `OSM`: trend-or-better in 2 diseases each, mainly Crohn/UC.
- `SPP1`: trend-or-better in 1 disease (`type 1 diabetes mellitus`).

If relaxed to mixed local bulk + direct H5AD + response + genetics + literature context, `IL1B`, `IFI30`, and `LAMP3` become plausible follow-up candidates. But that mixed standard would conflate generic inflammation, cell-state marking, target genetics, and response prediction. I would not count it as a verified >=5-disease central-node result.

## Perturbation and Clinical Context Checked

Local perturbation data for these eight genes is mostly absent in the inspected files. Literature context that is verified and relevant:

- `OSM` in IBD anti-TNF nonresponse: West et al., Nature Medicine 2017, PMID 28368383, DOI 10.1038/nm.4307.
- Anti-OSM antibody in RA: Choy et al., Annals of the Rheumatic Diseases 2013, PMID 24286335, DOI 10.1136/annrheumdis-2013-203523.
- OSM limiting autoimmune neuroinflammation in EAE: PMID 33581044, DOI 10.1016/j.immuni.2021.01.004.
- OSM-induced astrocytic TIMP-1 and remyelination context: PMID 32071226, DOI 10.1073/pnas.1912910117.

These sources make `OSM` a useful comparator and prior-art anchor, not a fresh single-node discovery candidate in this sidecar.

## Sidecar Decision

**PARK**, not `OPEN` and not `BLOCKED`.

Why not `OPEN`: no single requested gene currently satisfies broad cross-autoimmune evidence in >=5 diseases with response, cell-state, genetics, perturbation, and clinical channels. The strongest signal is still IBD-centered.

Why not `BLOCKED`: the local evidence gives concrete next tests. The best follow-up would be a focused `IL1B`/`LAMP3` cross-response analysis in independent RA and IBD anti-TNF datasets, with MS lesion spatial/single-cell validation specifically asking whether `LAMP3+` APC/DC states or `IL1B+` inflammatory myeloid states occur at lesion rims rather than in bulk white matter. `IFI30` should remain a genetics/cell-state comparator, not a drug target, unless a selective and safe antigen-processing modulation strategy appears.

Practical handoff to orchestrator:

- Keep `IL1B` and `LAMP3` as response-biomarker candidates.
- Keep `IFI30` as genetics/cell-state comparator.
- Do not promote `TREM1`, `ACSL1`, `SPP1`, or `OSM` as cross-autoimmune central nodes from this evidence alone.
- Treat the Wave86 circuit as an IBD anti-TNF nonresponse module with partial RA echo, not as a resolved pan-autoimmune therapeutic mechanism.
