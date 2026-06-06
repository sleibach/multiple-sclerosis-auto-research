# Wave34-A Genetics-First Target Rescue

Date: 2026-05-27

## Scope

Scan broad autoimmune genetic evidence already present in the workspace plus lightweight public lookup surfaces for druggable genes that expression-first screens may have missed. This report is a subagent routing artifact, not a therapeutic finding.

Controlling rule applied here: GWAS Catalog mapped-gene/top-association overlap is weak evidence unless backed by local OpenTargets credible-set breadth, public cis-eQTL availability, or a future coloc/pQTL/MR analysis. No coloc/MR is claimed.

## Executive Call

- Promoted to deeper validation branch: none.
- Parked: IRF5, IL10, PTPN22, FAP, GPR65, CCR6, TNFRSF14.
- Demoted: SH2B3, PTPN2, TYK2, CLEC16A, TNFAIP3, ATG16L1, CARD9, IL6R, STAT4, CTLA4, IL2RA, IL23R, CXCR5, CD226, CD6, PTGER4.

## Strongest Candidate Table

|gene|wave34a_call|genetics_first_score|ot_n_diseases_score_ge_0_5|gwas_catalog_trait_count|gwas_catalog_min_p|gtex_eqtl_tissue_count|manual_druggability|prior_risk|broad_positive_disease_count|broad_negative_disease_count|route_reason|
|---|---|---|---|---|---|---|---|---|---|---|---|
|SH2B3|DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION|22.1|10|22|1.00e-142|3|0.25|medium|1|0|Genetics may be broad, but current modality is absent or wrong-direction restoration.|
|IRF5|PARK_PRIOR_ART_OR_CROWDING|21.9|9|21|2.00e-143|4|2|high|0|0|Target is plausible but prior-art/crowding risk is high.|
|PTPN2|DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION|20.6|8|27|8.00e-28|1|0.75|high|4|0|Genetics may be broad, but current modality is absent or wrong-direction restoration.|
|TYK2|DEMOTE_PRIOR_ART_BLOCKED|19.6|7|36|9.00e-35|3|3|blocking|2|0|Direct clinical or therapeutic-class prior art blocks novelty.|
|CLEC16A|DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION|19.3|7|16|4.00e-95|3|0.75|medium|1|0|Genetics may be broad, but current modality is absent or wrong-direction restoration.|
|TNFAIP3|DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION|16.9|7|26|3.00e-84|0|0.5|high|3|1|Genetics may be broad, but current modality is absent or wrong-direction restoration.|
|ATG16L1|DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION|15.8|8|7|4.00e-78|4|0.5|medium_high|0|0|Genetics may be broad, but current modality is absent or wrong-direction restoration.|
|IL10|PARK_PRIOR_ART_OR_CROWDING|15.8|7|14|5.00e-55|1|2.5|high|0|0|Target is plausible but prior-art/crowding risk is high.|
|CARD9|DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION|12|4|9|4.00e-56|3|0.25|medium|2|0|Genetics may be broad, but current modality is absent or wrong-direction restoration.|
|IL6R|DEMOTE_PRIOR_ART_BLOCKED|11|5|9|3.00e-45|5|3|blocking|0|2|Direct clinical or therapeutic-class prior art blocks novelty.|
|PTPN22|PARK_DIRECTION_OR_MODALITY_UNRESOLVED|10.9|0|28|5.00e-174|3|1.5|medium_high|1|0|Genetic signal survives triage but direction/modality is not clean enough for promotion.|
|FAP|PARK_DIRECTION_OR_MODALITY_UNRESOLVED|10.2|0|15|6.00e-25|2|2.75|medium|2|0|Genetic signal survives triage but direction/modality is not clean enough for promotion.|
|STAT4|DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION|9.96|0|31|1.00e-160|3|0.75|high|2|0|Genetics may be broad, but current modality is absent or wrong-direction restoration.|
|GPR65|PARK_GENETIC_SIGNAL_LOCAL_CELLSTATE_MISMATCH|9.53|5|5|4.00e-18|3|2.5|high|1|2|Genetic signal is plausible but local expression/state support is contradictory.|
|CCR6|PARK_MAPPED_GENE_NEEDS_COLOC|8.45|0|15|4.00e-47|4|2|high|0|0|Broad GWAS Catalog support is mapped-gene/top-association only; needs credible-set/eQTL coloc.|
|CTLA4|DEMOTE_PRIOR_ART_BLOCKED|8.05|0|25|2.00e-90|2|3|blocking|0|0|Direct clinical or therapeutic-class prior art blocks novelty.|
|IL2RA|DEMOTE_PRIOR_ART_BLOCKED|7.25|0|35|3.00e-65|1|3|blocking|0|0|Direct clinical or therapeutic-class prior art blocks novelty.|
|IL23R|DEMOTE_PRIOR_ART_BLOCKED|7.25|0|25|2.00e-170|1|3|blocking|0|0|Direct clinical or therapeutic-class prior art blocks novelty.|

## Public Lookup Snapshot

|gene|europepmc_hit_count|clinicaltrials_count|chembl_target_id|chembl_activity_count_nM|
|---|---|---|---|---|
|TNFAIP3|4850|0|CHEMBL4523200|0|
|PTGER4|1630|0|CHEMBL1836|2168|
|SH2B3|1173|0||0|
|TNFRSF14|1021|0||0|
|CLEC16A|756|0||0|
|GPR65|432|0|CHEMBL3714081|99|
|IRF5|4201|1||0|
|PTPN2|1441|1|CHEMBL3807|1279|
|CARD9|1918|2||0|
|CD226|1822|2||0|
|ATG16L1|2959|4||0|
|STAT4|7092|5|CHEMBL4523296|0|
|CD6|1413|6|CHEMBL3712853|0|
|CXCR5|8220|9|CHEMBL1075315|0|
|PTPN22|4800|9|CHEMBL2889|1114|
|IL23R|10506|14|CHEMBL4296013|1106|
|CCR6|8922|14|CHEMBL4423|0|
|TYK2|6839|17|CHEMBL3553|17132|

## Candidate Notes

### `SH2B3` - DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION

- Axis: LNK hematopoietic cytokine brake.
- Intended direction/modality: restore LNK negative regulation / no direct restoration modality.
- Genetics: local OT credible-set diseases >=0.5 = 10 (AITD;AS;Celiac;Crohn;MS;PBC;Psoriasis;RA;T1D;UC); GWAS Catalog autoimmune trait count = 22; min p = 1e-142.
- Expression-first miss/check: broad positive diseases = 1; broad negative diseases = 0; MS white-matter delta = -0.150958184932211.
- Druggability/prior: manual druggability = 0.25; ChEMBL target = none; ChEMBL nM activity records = 0; prior risk = medium.
- Routing reason: Genetics may be broad, but current modality is absent or wrong-direction restoration.
- Manual note: Broadest local OT locus but no direct modality and 12q24 pleiotropy.

### `IRF5` - PARK_PRIOR_ART_OR_CROWDING

- Axis: TLR/IRF5 inflammatory switch.
- Intended direction/modality: inhibit IRF5 activation / allosteric inhibitor or degrader.
- Genetics: local OT credible-set diseases >=0.5 = 9 (AS;Crohn;MS;PBC;Psoriasis;RA;SLE;Sjogren;UC); GWAS Catalog autoimmune trait count = 21; min p = 2e-143.
- Expression-first miss/check: broad positive diseases = 0; broad negative diseases = 0; MS white-matter delta = -0.160335979633075.
- Druggability/prior: manual druggability = 2.0; ChEMBL target = none; ChEMBL nM activity records = 0; prior risk = high.
- Routing reason: Target is plausible but prior-art/crowding risk is high.
- Manual note: Broad locus and drug-discovery feasibility, but lupus/IRF5 prior art is direct.

### `PTPN2` - DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION

- Axis: TCPTP cytokine/barrier negative regulator.
- Intended direction/modality: restore/increase TCPTP function / would require restoration/activation; inhibitors point wrong way.
- Genetics: local OT credible-set diseases >=0.5 = 8 (AS;Celiac;Crohn;Psoriasis;RA;SLE;T1D;UC); GWAS Catalog autoimmune trait count = 27; min p = 8e-28.
- Expression-first miss/check: broad positive diseases = 4; broad negative diseases = 0; MS white-matter delta = -0.0059418057306839.
- Druggability/prior: manual druggability = 0.75; ChEMBL target = CHEMBL3807; ChEMBL nM activity records = 1279; prior risk = high.
- Routing reason: Genetics may be broad, but current modality is absent or wrong-direction restoration.
- Manual note: Strong genetics benchmark, but no correct-direction restoration modality.

### `TYK2` - DEMOTE_PRIOR_ART_BLOCKED

- Axis: TYK2 cytokine kinase.
- Intended direction/modality: inhibit TYK2 / approved/clinical allosteric inhibitors.
- Genetics: local OT credible-set diseases >=0.5 = 7 (AITD;Crohn;PBC;Psoriasis;RA;SLE;T1D); GWAS Catalog autoimmune trait count = 36; min p = 9e-35.
- Expression-first miss/check: broad positive diseases = 2; broad negative diseases = 0; MS white-matter delta = -0.0976695299908261.
- Druggability/prior: manual druggability = 3.0; ChEMBL target = CHEMBL3553; ChEMBL nM activity records = 17132; prior risk = blocking.
- Routing reason: Direct clinical or therapeutic-class prior art blocks novelty.
- Manual note: Positive control for genetics plus druggability; excluded by direct autoimmune prior art.

### `CLEC16A` - DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION

- Axis: mitophagy/autophagy quality control.
- Intended direction/modality: restore CLEC16A-linked mitophagy / indirect mitophagy restoration.
- Genetics: local OT credible-set diseases >=0.5 = 7 (Crohn;MS;PBC;Psoriasis;RA;SLE;T1D); GWAS Catalog autoimmune trait count = 16; min p = 4e-95.
- Expression-first miss/check: broad positive diseases = 1; broad negative diseases = 0; MS white-matter delta = 0.1097171053941039.
- Druggability/prior: manual druggability = 0.75; ChEMBL target = none; ChEMBL nM activity records = 0; prior risk = medium.
- Routing reason: Genetics may be broad, but current modality is absent or wrong-direction restoration.
- Manual note: 16p13 locus ambiguity and no direct modality.

### `TNFAIP3` - DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION

- Axis: A20 NF-kappaB/TNF/TLR brake.
- Intended direction/modality: increase/restore A20 function / restore A20 function or mimic negative-feedback complex.
- Genetics: local OT credible-set diseases >=0.5 = 7 (AS;Crohn;Psoriasis;RA;SLE;Sjogren;UC); GWAS Catalog autoimmune trait count = 26; min p = 3e-84.
- Expression-first miss/check: broad positive diseases = 3; broad negative diseases = 1; MS white-matter delta = 0.328353196360478.
- Druggability/prior: manual druggability = 0.5; ChEMBL target = CHEMBL4523200; ChEMBL nM activity records = 0; prior risk = high.
- Routing reason: Genetics may be broad, but current modality is absent or wrong-direction restoration.
- Manual note: Strong locus biology but not currently target-selectively druggable.

### `ATG16L1` - DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION

- Axis: autophagy/xenophagy.
- Intended direction/modality: restore autophagy in risk-variant context / indirect autophagy modulation.
- Genetics: local OT credible-set diseases >=0.5 = 8 (AITD;AS;Celiac;Crohn;Psoriasis;SLE;T1D;UC); GWAS Catalog autoimmune trait count = 7; min p = 4e-78.
- Expression-first miss/check: broad positive diseases = 0; broad negative diseases = 0; MS white-matter delta = -0.0960188702877271.
- Druggability/prior: manual druggability = 0.5; ChEMBL target = none; ChEMBL nM activity records = 0; prior risk = medium_high.
- Routing reason: Genetics may be broad, but current modality is absent or wrong-direction restoration.
- Manual note: Broad autophagy modulation is nonspecific.

### `IL10` - PARK_PRIOR_ART_OR_CROWDING

- Axis: IL-10 regulatory cytokine.
- Intended direction/modality: increase regulatory IL-10 signaling / engineered IL-10 or IL10R agonism.
- Genetics: local OT credible-set diseases >=0.5 = 7 (AS;Crohn;Psoriasis;RA;SLE;T1D;UC); GWAS Catalog autoimmune trait count = 14; min p = 5e-55.
- Expression-first miss/check: broad positive diseases = 0; broad negative diseases = 0; MS white-matter delta = 0.5386340709389863.
- Druggability/prior: manual druggability = 2.5; ChEMBL target = CHEMBL3712920; ChEMBL nM activity records = 0; prior risk = high.
- Routing reason: Target is plausible but prior-art/crowding risk is high.
- Manual note: Direct IL-10 autoimmune/IBD therapy prior art and no local subgroup delta.

### `CARD9` - DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION

- Axis: CARD9 innate adaptor.
- Intended direction/modality: context-dependent inhibition while preserving antifungal immunity / none selective.
- Genetics: local OT credible-set diseases >=0.5 = 4 (AS;Crohn;Psoriasis;UC); GWAS Catalog autoimmune trait count = 9; min p = 4e-56.
- Expression-first miss/check: broad positive diseases = 2; broad negative diseases = 0; MS white-matter delta = -0.4691972101237329.
- Druggability/prior: manual druggability = 0.25; ChEMBL target = none; ChEMBL nM activity records = 0; prior risk = medium.
- Routing reason: Genetics may be broad, but current modality is absent or wrong-direction restoration.
- Manual note: Genetic breadth but poor druggability and infection-risk problem.

### `IL6R` - DEMOTE_PRIOR_ART_BLOCKED

- Axis: IL-6 receptor signaling.
- Intended direction/modality: block IL-6R / approved anti-IL6R biologics.
- Genetics: local OT credible-set diseases >=0.5 = 5 (AS;Crohn;Psoriasis;RA;UC); GWAS Catalog autoimmune trait count = 9; min p = 3e-45.
- Expression-first miss/check: broad positive diseases = 0; broad negative diseases = 2; MS white-matter delta = 0.3662122714747209.
- Druggability/prior: manual druggability = 3.0; ChEMBL target = CHEMBL2364155; ChEMBL nM activity records = 0; prior risk = blocking.
- Routing reason: Direct clinical or therapeutic-class prior art blocks novelty.
- Manual note: Approved autoimmune mechanism; comparator only.

### `PTPN22` - PARK_DIRECTION_OR_MODALITY_UNRESOLVED

- Axis: Lyp lymphocyte-receptor signaling phosphatase.
- Intended direction/modality: unclear across R620W-like risk biology; inhibition is plausible in some models but not directionally settled / small-molecule inhibitor/allosteric modulator concept.
- Genetics: local OT credible-set diseases >=0.5 = 0 (none); GWAS Catalog autoimmune trait count = 28; min p = 5e-174.
- Expression-first miss/check: broad positive diseases = 1; broad negative diseases = 0; MS white-matter delta = 0.81950776939291.
- Druggability/prior: manual druggability = 1.5; ChEMBL target = CHEMBL2889; ChEMBL nM activity records = 1114; prior risk = medium_high.
- Routing reason: Genetic signal survives triage but direction/modality is not clean enough for promotion.
- Manual note: Very broad autoimmune genetics, but disease-safe direction and selectivity over other PTPs remain unresolved.

### `FAP` - PARK_DIRECTION_OR_MODALITY_UNRESOLVED

- Axis: fibroblast activation / tissue remodeling.
- Intended direction/modality: unclear in autoimmunity; inhibit pathogenic fibroblast activation if causal / enzyme inhibitor, antibody, or targeted delivery handle.
- Genetics: local OT credible-set diseases >=0.5 = 0 (none); GWAS Catalog autoimmune trait count = 15; min p = 6e-25.
- Expression-first miss/check: broad positive diseases = 2; broad negative diseases = 0; MS white-matter delta = nan.
- Druggability/prior: manual druggability = 2.75; ChEMBL target = CHEMBL4683; ChEMBL nM activity records = 0; prior risk = medium.
- Routing reason: Genetic signal survives triage but direction/modality is not clean enough for promotion.
- Manual note: Druggable stromal gene with GWAS Catalog breadth, but likely locus-proxy/tissue-remodeling rather than target-level immune causality.

### `STAT4` - DEMOTE_NOT_DRUGGABLE_IN_CORRECT_DIRECTION

- Axis: IL-12/23 transcriptional polarization.
- Intended direction/modality: reduce STAT4-driven Th1/Th17 polarization / indirect cytokine/JAK pathway blockade.
- Genetics: local OT credible-set diseases >=0.5 = 0 (none); GWAS Catalog autoimmune trait count = 31; min p = 1e-160.
- Expression-first miss/check: broad positive diseases = 2; broad negative diseases = 0; MS white-matter delta = 0.8684079555977076.
- Druggability/prior: manual druggability = 0.75; ChEMBL target = CHEMBL4523296; ChEMBL nM activity records = 0; prior risk = high.
- Routing reason: Genetics may be broad, but current modality is absent or wrong-direction restoration.
- Manual note: Broad genetics but poor direct druggability; upstream pathways are already crowded.

### `GPR65` - PARK_GENETIC_SIGNAL_LOCAL_CELLSTATE_MISMATCH

- Axis: acidic tissue pH-sensing GPCR.
- Intended direction/modality: agonize/PAM if risk alleles reduce anti-inflammatory cAMP response / agonist/PAM.
- Genetics: local OT credible-set diseases >=0.5 = 5 (AS;Crohn;MS;Psoriasis;UC); GWAS Catalog autoimmune trait count = 5; min p = 4e-18.
- Expression-first miss/check: broad positive diseases = 1; broad negative diseases = 2; MS white-matter delta = 0.09040507812532.
- Druggability/prior: manual druggability = 2.5; ChEMBL target = CHEMBL3714081; ChEMBL nM activity records = 99; prior risk = high.
- Routing reason: Genetic signal is plausible but local expression/state support is contradictory.
- Manual note: Previously parked; GPCR tractable but IBD/GPR65 prior art and weak local support remain.

## Exact Local Files Used

- `tmp_v3/wave13_opentargets_gwas_credible_sets.tsv`: exists=True, rows=468, columns=9
- `tmp_v3/wave11_opentargets_target_disease_scores.tsv`: exists=True, rows=228, columns=8
- `tmp_v3/gwascatalog_associations_20260317_convert.parquet`: exists=True, rows=parquet, columns=
- `results_v3/wave14_target_level_genetics/target_level_genetics_truth_table.tsv`: exists=True, rows=12, columns=20
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`: exists=True, rows=25176, columns=40
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`: exists=True, rows=271, columns=22
- `results_v3/wave20_genetic_druggable_altaxis/local_opentargets_genetics_summary.tsv`: exists=True, rows=44, columns=10
- `results_v3/wave20_genetic_druggable_altaxis/negative_ranked_shortlist.tsv`: exists=True, rows=12, columns=28
- `results_v3/wave23_genetics_restoration_modality/ranked_go_park_no_go.tsv`: exists=True, rows=14, columns=17
- `results_v3/wave25_causal_genetics_module_proxy/causal_proxy_candidate_matrix.tsv`: exists=True, rows=206, columns=38
- `results_v3/wave28_target_first_rescue/target_first_rescue_matrix.tsv`: exists=True, rows=26, columns=53
- `results_v3/wave33_tolerance_costimulation_audit/tolerance_costimulation_axis_audit.tsv`: exists=True, rows=13, columns=29

## Public Queries Run

All public lookups were cached under `results_v3/wave34a_genetics_first_target_rescue/raw_api/`. The query log is `results_v3/wave34a_genetics_first_target_rescue/public_query_log.tsv`.

- Local GWAS Catalog autoimmune subset rows scanned: 15875.
- Surfaces queried per candidate where available: ChEMBL target/activity API, GTEx Portal reference/single-tissue eQTL API, Europe PMC search API, ClinicalTrials.gov API v2.

|gene|surface|url|
|---|---|---|
|CD226|ChEMBL target|https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=CD226|
|CD226|GTEx lookup|https://gtexportal.org/api/v2/reference/gene?geneId=CD226&gencodeVersion=v26&genomeBuild=GRCh38%2Fhg38&itemsPerPage=3|
|CD226|Europe PMC|https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%28CD226%29+AND+%28%22autoimmune%22+OR+%22multiple+sclerosis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+Crohn+OR+pso|
|CD226|ClinicalTrials.gov|https://clinicaltrials.gov/api/v2/studies?query.term=CD226&query.cond=autoimmune+OR+multiple+sclerosis+OR+rheumatoid+arthritis+OR+lupus+OR+Crohn+OR+psoriasis&format=json&pageSize=1|
|PTGER4|ChEMBL target|https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=PTGER4|
|PTGER4|ChEMBL activity|https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id=CHEMBL1836&standard_units=nM&limit=1|
|PTGER4|GTEx lookup|https://gtexportal.org/api/v2/reference/gene?geneId=PTGER4&gencodeVersion=v26&genomeBuild=GRCh38%2Fhg38&itemsPerPage=3|
|PTGER4|Europe PMC|https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%28PTGER4%29+AND+%28%22autoimmune%22+OR+%22multiple+sclerosis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+Crohn+OR+ps|
|PTGER4|ClinicalTrials.gov|https://clinicaltrials.gov/api/v2/studies?query.term=PTGER4&query.cond=autoimmune+OR+multiple+sclerosis+OR+rheumatoid+arthritis+OR+lupus+OR+Crohn+OR+psoriasis&format=json&pageSize=|
|CXCR5|ChEMBL target|https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=CXCR5|
|CXCR5|ChEMBL activity|https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id=CHEMBL1075315&standard_units=nM&limit=1|
|CXCR5|GTEx lookup|https://gtexportal.org/api/v2/reference/gene?geneId=CXCR5&gencodeVersion=v26&genomeBuild=GRCh38%2Fhg38&itemsPerPage=3|
|CXCR5|Europe PMC|https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%28CXCR5%29+AND+%28%22autoimmune%22+OR+%22multiple+sclerosis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+Crohn+OR+pso|
|CXCR5|ClinicalTrials.gov|https://clinicaltrials.gov/api/v2/studies?query.term=CXCR5&query.cond=autoimmune+OR+multiple+sclerosis+OR+rheumatoid+arthritis+OR+lupus+OR+Crohn+OR+psoriasis&format=json&pageSize=1|
|CCR6|ChEMBL target|https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=CCR6|
|CCR6|ChEMBL activity|https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id=CHEMBL4423&standard_units=nM&limit=1|
|CCR6|GTEx lookup|https://gtexportal.org/api/v2/reference/gene?geneId=CCR6&gencodeVersion=v26&genomeBuild=GRCh38%2Fhg38&itemsPerPage=3|
|CCR6|Europe PMC|https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%28CCR6%29+AND+%28%22autoimmune%22+OR+%22multiple+sclerosis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+Crohn+OR+psor|
|CCR6|ClinicalTrials.gov|https://clinicaltrials.gov/api/v2/studies?query.term=CCR6&query.cond=autoimmune+OR+multiple+sclerosis+OR+rheumatoid+arthritis+OR+lupus+OR+Crohn+OR+psoriasis&format=json&pageSize=1&|
|TNFRSF14|ChEMBL target|https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=TNFRSF14|
|TNFRSF14|GTEx lookup|https://gtexportal.org/api/v2/reference/gene?geneId=TNFRSF14&gencodeVersion=v26&genomeBuild=GRCh38%2Fhg38&itemsPerPage=3|
|TNFRSF14|Europe PMC|https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%28TNFRSF14%29+AND+%28%22autoimmune%22+OR+%22multiple+sclerosis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+Crohn+OR+|
|TNFRSF14|ClinicalTrials.gov|https://clinicaltrials.gov/api/v2/studies?query.term=TNFRSF14&query.cond=autoimmune+OR+multiple+sclerosis+OR+rheumatoid+arthritis+OR+lupus+OR+Crohn+OR+psoriasis&format=json&pageSiz|
|FAP|ChEMBL target|https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=FAP|
|FAP|ChEMBL activity|https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id=CHEMBL4683&standard_units=nM&limit=1|
|FAP|GTEx lookup|https://gtexportal.org/api/v2/reference/gene?geneId=FAP&gencodeVersion=v26&genomeBuild=GRCh38%2Fhg38&itemsPerPage=3|
|FAP|Europe PMC|https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=%28FAP%29+AND+%28%22autoimmune%22+OR+%22multiple+sclerosis%22+OR+%22rheumatoid+arthritis%22+OR+lupus+OR+Crohn+OR+psori|
|FAP|ClinicalTrials.gov|https://clinicaltrials.gov/api/v2/studies?query.term=FAP&query.cond=autoimmune+OR+multiple+sclerosis+OR+rheumatoid+arthritis+OR+lupus+OR+Crohn+OR+psoriasis&format=json&pageSize=1&c|
|CD6|ChEMBL target|https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=CD6|
|CD6|ChEMBL activity|https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id=CHEMBL3712853&standard_units=nM&limit=1|

## Blockers

- No disease GWAS summary statistics plus matched immune/tissue eQTL or pQTL summary statistics were available locally for formal coloc/MR.
- GWAS Catalog mapped-gene counts are locus/top-association triage only; they are especially unsafe in dense immune loci and pleiotropic MTAG/pleiotropy traits.
- GTEx cis-eQTL availability is not direction-of-effect and not colocalization. It only tells us whether a future coloc branch is feasible.
- ChEMBL activity or target presence is not autoimmune-correct target engagement. It does not solve direction, selectivity, tissue delivery, or safety.
- Expression-first V3 screens remain useful vetoes for tissue-state support. CD226, CXCR5, CCR6, IL2RA, IL23R, CTLA4, and several other genetics-first candidates were not locally promoted by cell-state data.
- Several genes with excellent genetics and druggability (`TYK2`, `IL23R`, `IL2RA`, `CTLA4`, `IL6R`, `CD6`) are demoted for direct prior-art saturation rather than lack of biology.

## Next Validation Questions

1. For `CD226`, obtain disease GWAS summary stats and immune-cell cis-eQTL/pQTL for formal coloc across MS, RA, SLE, T1D, IBD/PBC/PSC where possible.
2. For `CD226`, test whether risk alleles increase CD226 expression or alter CD226/TIGIT/PVR-NECTIN2 balance in CD8 T, NK, and pathogenic T helper states.
3. For `PTGER4`, resolve direction before any target claim: allele-to-expression/eQTL direction, cell-type specificity, and agonist versus antagonist pharmacology must agree.
4. For `CXCR5`/`CCR6`, require tissue-atlas evidence of disease-enriched pathogenic trafficking states before deeper medicinal-chemistry work.
