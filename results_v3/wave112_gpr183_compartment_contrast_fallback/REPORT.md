# Wave112 GPR183 Compartment-Contrast Fallback

## Bottom Line

Branch call: `NO_REOPEN_GPR183_COMPARTMENT_FALLBACK`.

Wave111 could not run matched-donor spatial proxies. This fallback is weaker:
it asks whether broad compartment contrasts show myeloid/APC `GPR183` up in
the same disease where non-myeloid oxysterol-axis genes are up, with no strong
directional contradiction.

## Disease Summary

| disease_name | receptor_myeloid_positive_contexts | receptor_myeloid_negative_contexts | ligand_nonmyeloid_positive_contexts | ligand_nonmyeloid_negative_contexts | coherent_compartment_signal | best_receptor_context | best_ligand_context |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Crohn disease | 0 | 0 | 2 | 1 | False | {'analysis': 'ibd_crohn_myeloid', 'delta_log2_cpm': 0.975302839797214, 'p': 0.1413388691761818} | {'analysis': 'ibd_crohn_epithelial', 'gene': 'CYP27A1', 'delta_log2_cpm': -1.8185872484310737, 'p': 0.0020256693223881} |
| Sjogren syndrome | 0 | 0 | 0 | 0 | False | {'analysis': 'sjogren_gland_apc', 'delta_log2_cpm': 0.2633994006448397, 'p': 0.2974534480328355} | {'analysis': 'sjogren_gland_stromal', 'gene': 'CH25H', 'delta_log2_cpm': 0.9847826299219392, 'p': 0.1413820547793303} |
| psoriasis | 0 | 1 | 1 | 2 | False | {'analysis': 'psoriasis_skin_apc', 'delta_log2_cpm': -1.2498901037911736, 'p': 0.0496082040015271} | {'analysis': 'psoriasis_skin_stromal', 'gene': 'HSD3B7', 'delta_log2_cpm': -0.7120219991008807, 'p': 0.0012863968859704} |
| type 1 diabetes mellitus | 0 | 0 | 6 | 1 | False | {} | {'analysis': 't1d_endothelial_cell', 'gene': 'CYP27A1', 'delta_log2_cpm': 1.84442933113559, 'p': 0.0198807926844594} |
| ulcerative colitis | 1 | 0 | 0 | 2 | False | {'analysis': 'ibd_uc_myeloid', 'delta_log2_cpm': 1.0385480940916807, 'p': 0.0969321031619274} | {'analysis': 'ibd_uc_epithelial', 'gene': 'CYP27A1', 'delta_log2_cpm': -3.9939633258528295, 'p': 0.0001359160277507} |

## Response Support Rows

| system | gene | nonresponse_high_contexts | responder_high_contexts | min_p | weighted_mean_hedges_g_responder_minus_non |
| --- | --- | --- | --- | --- | --- |
| IBD | CH25H | 4 | 0 | 0.05744 | -0.368 |
| IBD | CYP27A1 | 1 | 3 | 0.2079 | 0.2645 |
| IBD | CYP7B1 | 4 | 0 | 0.002531 | -1.254 |
| IBD | GPR183 | 4 | 0 | 0.0008986 | -1.108 |
| IBD | HSD3B7 | 1 | 3 | 0.4756 | 0.1259 |
| RA | CH25H | 1 | 0 | 0.06356 | -0.6067 |
| RA | CYP27A1 | 1 | 0 | 0.02538 | -0.6525 |
| RA | CYP7B1 | 1 | 0 | 0.3173 | -0.3853 |
| RA | GPR183 | 0 | 1 | 0.02785 | 0.7061 |
| RA | HSD3B7 | 0 | 1 | 0.1234 | 0.5705 |
| psoriasis | CH25H | 0 | 1 | 0.9543 | 0.02937 |
| psoriasis | CYP27A1 | 1 | 0 | 0.687 | -0.2014 |
| psoriasis | CYP7B1 | 0 | 1 | 0.09351 | 0.8119 |
| psoriasis | GPR183 | 1 | 0 | 0.8967 | -0.06372 |
| psoriasis | HSD3B7 | 0 | 1 | 0.2473 | 0.5902 |

## Interpretation

This cannot promote GPR183. At best it can justify rebuilding donor-level
GPR183/ligand scores from h5ad. If coherent disease count is below two, the
route remains closed locally.

## Reproducibility

- Script: `scripts/v3_wave112_gpr183_compartment_contrast_fallback.py`
- Broad h5ad rows: `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_contrasts.tsv`
- Output summary: `results_v3/wave112_gpr183_compartment_contrast_fallback/gpr183_compartment_contrast_summary.tsv`
- Seed: `20260527`
