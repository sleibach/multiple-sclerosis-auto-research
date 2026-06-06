# Wave69-B Independent Validation Scout

Timestamp: 2026-05-27 16:04 CEST

Scope: independent validation scout for Wave68 parked gene/controller signals in public single-cell/spatial autoimmune datasets already present or lightweight-feasible. Candidate anchors were `RGS14`, `CD274`, `TNFSF15`, `CD80`, `FCGR2B`, `NCF1`, `IL7R`, `STAT4`, and `SP140` as a blocked comparator.

## Verdict

No Wave68 parked candidate should be promoted from this scout. The best cross-dataset expression recurrence is `IL7R`, `CD274`, and `SP140`; that is not intervention-grade evidence. `IL7R` and `SP140` are already blocked by prior-art/directionality audits, `CD274` is checkpoint/safety territory, and none has a strong independent MS white-matter anchor. `FCGR2B` and `NCF1` move in paired RA synovium after anti-TNF, but that is bulk pharmacodynamic recurrence, not a clean myeloid controller mechanism. `RGS14`, the top Wave68 DC parked row, is not independently supported strongly enough to reopen.

## New Scout Outputs

Script:

- `scripts/v3_wave69b_independent_validation_scout.py`

Outputs:

- `results_v3/wave69b_independent_validation_scout/wave68_origin_candidate_rows.tsv`
- `results_v3/wave69b_independent_validation_scout/ms_gse111972_candidate_rows.tsv`
- `results_v3/wave69b_independent_validation_scout/broad_h5ad_priority_candidate_rows.tsv`
- `results_v3/wave69b_independent_validation_scout/broad_h5ad_candidate_summary.tsv`
- `results_v3/wave69b_independent_validation_scout/ra_gse198520_candidate_patient_deltas.tsv`
- `results_v3/wave69b_independent_validation_scout/ra_gse198520_candidate_paired_tests.tsv`
- `results_v3/wave69b_independent_validation_scout/ra_gse198520_candidate_response_tests.tsv`
- `results_v3/wave69b_independent_validation_scout/summary.json`

Random seed: `20260527`.

## Datasets And Feasibility Checks

| Dataset | Disease/system | Status in this scout | Exact use |
| --- | --- | --- | --- |
| `GSE282122`, Zenodo `14007626` | Crohn/UC lamina propria myeloid anti-TNF, `Mono_macro` and `DC` | Origin only, not independent validation | Extracted Wave68 candidate rows so independent checks could be interpreted against the discovery context. |
| `GSE111972` | sorted human microglia, MS white matter vs control white matter | Analyzed from existing full signature table | Candidate gene-level MS-local contrast from `results_v3/gse111972_full_ms_wm_signature.tsv`. This is sorted microglia, not lesion-rim spatial data. |
| CELLxGENE IBD h5ad, publication DOI `10.1038/s41467-023-40156-6` | Crohn/UC colon myeloid, epithelial, stromal compartments | Analyzed through existing broad h5ad donor-level contrasts | Independent disease-vs-control recurrence for candidate genes. |
| CELLxGENE psoriasis h5ad, publication DOI `10.1038/s41419-021-03724-6` | psoriasis skin APC, keratinocyte, stromal compartments | Analyzed through existing broad h5ad donor-level contrasts | Independent skin recurrence for candidate genes. |
| `GSE198520` | RA paired synovium bulk RNA-seq pre/post anti-TNF | Newly analyzed at candidate-gene level | Computed log2 CPM, paired post-minus-pre tests across 46 patients, and response-delta tests with pathotype adjustment. |
| `GSE183047` | psoriasis scRNA pre/post secukinumab | Local raw feasible only | Raw 10x matrices and metadata are present, but no ready candidate-level annotated table with response labels exists. Rebuilding it would test pharmacodynamics only, not intervention-grade validation. |
| RA blood h5ad, DOI `10.1172/jci.insight.178499` | RA blood immune cells | Feasibility-only | Not synovium and not present in the existing broad contrast output; not used as a priority validation system. |

## Exact Analyses

1. `GSE111972` MS-local check: extracted candidate genes from the full MS white-matter microglia signature. Status labels: FDR <= 0.10 positive/negative, nominal p < 0.05 positive/negative, otherwise null/weak.

2. Broad h5ad recurrence: extracted candidate rows from `broad_h5ad_gene_contrasts.tsv` and `broad_h5ad_gene_summary.tsv`, restricted to IBD and psoriasis priority compartments. The table is donor-level disease-vs-control log2 CPM with Welch tests and BH FDR already computed upstream.

3. RA synovium candidate audit: using `GSE198520` counts and sample metadata already produced by Wave65, summed duplicate gene symbols, computed log2 CPM with all genes as library-size denominator, calculated paired post-minus-pre deltas for 46 patients, tested one-sample deltas against zero, and tested good-vs-other / moderate-or-good-vs-none response differences with and without pathotype adjustment.

## Candidate Status

| gene | Wave68 status | MS `GSE111972` | Broad h5ad recurrence | RA synovium anti-TNF |
| --- | --- | --- | --- | --- |
| `RGS14` | DC parked genetic/perturbation intersection | negative nominal, delta `-0.504`, p `0.0463`, FDR `0.874` | 1 positive nominal compartment, Crohn epithelial only | null, delta `-0.0747`, p `0.650`, FDR `0.731` |
| `CD274` | DC parked genetic/perturbation intersection | null, delta `0.354`, p `0.328`, FDR `0.914` | 5 positive nominal compartments across Crohn, UC, psoriasis, Sjogren; no FDR10 | null, delta `0.0281`, p `0.807`, FDR `0.807` |
| `TNFSF15` | DC parked genetic/perturbation intersection | null, delta `0.394`, p `0.756`, FDR `0.971` | 3 positive nominal compartments in UC and psoriasis; no FDR10 | null, delta `-0.0461`, p `0.598`, FDR `0.731` |
| `CD80` | DC parked genetic/perturbation intersection | null, delta `-0.221`, p `0.862`, FDR `0.980` | 1 positive nominal compartment, UC myeloid | null, delta `-0.146`, p `0.290`, FDR `0.522` |
| `FCGR2B` | DC parked genetic/perturbation intersection | null, delta `0.374`, p `0.600`, FDR `0.947` | no positive compartments; one negative nominal UC stromal compartment | anti-TNF paired decrease, delta `-0.308`, p `0.00107`, FDR `0.00963` |
| `NCF1` | Mono/mac parked genetic/perturbation intersection | null, delta `0.664`, p `0.480`, FDR `0.926` | 1 positive nominal compartment, Crohn epithelial | anti-TNF paired decrease, delta `-0.665`, p `0.00777`, FDR `0.0349`; good-responder response raw p `0.0120`, adjusted FDR `0.151` |
| `IL7R` | DC parked genetic/perturbation intersection | null/negative trend, delta `-0.654`, p `0.572`, FDR `0.943` | strongest recurrence: 4 positive compartments, 3 FDR10, Crohn/UC/T1D | weak anti-TNF decrease, delta `-0.209`, p `0.0512`, FDR `0.153`; good-responder response raw p `0.0489`, adjusted FDR `0.336` |
| `STAT4` | Mono/mac parked genetic/perturbation intersection | null, delta `0.868`, p `0.461`, FDR `0.924` | 2 positive nominal IBD myeloid compartments; no FDR10 | null, delta `-0.0691`, p `0.536`, FDR `0.731` |
| `SP140` | blocked comparator, not reopened | null, delta `-0.0868`, p `0.726`, FDR `0.968` | 4 positive nominal compartments across Crohn, UC, psoriasis, Sjogren; no FDR10 | weak paired decrease only, delta `-0.166`, p `0.0789`, FDR `0.177` |

## Interpretation By Candidate

`RGS14`: The Wave68 DC signal does not replicate in an intervention-grade way. Independent recurrence is only Crohn epithelial nominal expression, and MS white-matter microglia are nominally lower. This is a no-go for current promotion.

`CD274`: Recurrent expression across inflamed tissues is real but generic checkpoint biology. It is likely a marker of inflamed tissue and immune-tissue crosstalk, not a novel tractable autoimmune target. The report treats it as a checkpoint comparator only.

`TNFSF15`: The UC/psoriasis expression pattern is plausible for mucosal/skin inflammation, but the scout does not establish MS support, RA pharmacodynamics, or a clean myeloid lipid-lysosomal mechanism. It stays parked.

`CD80`: Too weak. One UC myeloid nominal recurrence and no MS/RA support.

`FCGR2B`: The RA synovium paired anti-TNF decrease is statistically real in bulk tissue, but the broader h5ad recurrence is weak/negative and the result may reflect Fc receptor-bearing cell abundance or anti-TNF-complex biology. It is a pharmacodynamic readout, not a controller claim.

`NCF1`: RA synovium decrease after anti-TNF is also real, and the good-responder contrast is nominal before multiplicity. That suggests oxidative-burst/myeloid inflammatory load tracks anti-TNF response, but no cross-disease or MS-local evidence is strong enough for a target claim.

`IL7R`: This is the strongest expression recurrence by this scout: Crohn and UC myeloid FDR10 plus UC stromal FDR10, with T1D stellate nominal support. But it is already blocked by Wave58-N and Wave34-C: canonical CD127/sIL7R biology, existing clinical/patent programs, and null local MS tissue support. Use as a positive-control recurrent autoimmune axis, not a new target.

`STAT4`: Broad target-resolved genetics exist from Wave62, but this scout adds only IBD myeloid nominal expression. STAT4 remains an indirect/crowded IL-12/JAK/TYK2 transcription-factor comparator, not a selective drug target.

`SP140`: Expression recurrence in IBD/psoriasis/Sjogren reproduces the prior comparator signal. It remains blocked by Wave56-J/Wave56-K/Wave63-X: local MS signal is null, direct SP140 autoimmune modulation is prior art, and disease-risk direction conflicts with simple inhibition.

## Blockers And Limitations

- Independent MS evidence is weak because the local MS dataset is sorted white/grey matter microglia, not spatial chronic-active lesion rim. This is a useful contradiction screen but not definitive lesion-compartment validation.
- RA synovium evidence is bulk tissue. It cannot separate target expression change from shifts in macrophage, DC, plasma-cell, lymphoid, or stromal abundance.
- The broad h5ad recurrence tests are expression recurrence, not perturbation. A recurrent inflamed-state marker can be a bad therapeutic target.
- No foundation-model, CRISPR, CMap, or spatial validation was run in this subagent scope.
- `GSE183047` is feasible for future psoriasis pharmacodynamic candidate-gene reconstruction, but it lacks response labels and would not by itself convert expression recurrence into intervention-grade evidence.

## Recommendation To Orchestrator

Do not reopen any direct Wave68 candidate. If the main session continues this branch, the most useful next forcing tests are:

1. Treat `IL7R` and `SP140` as positive-control recurrent axes and explicitly exclude them from novelty promotion.
2. Use `NCF1`/`FCGR2B` only as RA anti-TNF pharmacodynamic readouts unless cell-type-resolved synovium validates them in myeloid cells.
3. For `RGS14`, require an independent DC/myeloid dataset with disease-vs-control and treatment-response support before spending effort on druggability.
4. Prioritize fetching or locating true MS chronic-active-lesion single-nucleus/spatial data. Current MS-local evidence does not rescue any parked gene.
