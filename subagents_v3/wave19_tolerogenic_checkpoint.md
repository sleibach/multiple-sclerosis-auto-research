# Wave19-A Tolerogenic / Inhibitory Myeloid Checkpoint Gate

Date: 2026-05-27

## Executive Verdict

**No candidate is promoted to GO.**

The checkpoint idea is pharmacologically plausible, but it does not rescue the
V3 cross-autoimmune lipid-lysosomal/APC/HLA-II state after Wave18. The best
axis is `CD274`/PD-L1 because it has four local disease recurrences and three
state-coupled diseases, but it fails the novelty/saturation gate and lacks a
selective perturbation package. `CD24`, `BTLA`, `CD200`, and `CD47` are parked
as comparator axes only. The other named myeloid inhibitory receptors fail on
local recurrence, state coupling, direction, or prior-art crowding.

Promotion criteria applied:

- at least three disease/tissue supports,
- credible intervention direction,
- plausible drug modality,
- non-saturated prior art for the specific autoimmune use,
- feasible lead indication.

No axis met all five.

## Reproducible Outputs

Script:

- `scripts/v3_wave19_tolerogenic_checkpoint.py`

Output directory:

- `results_v3/wave19_tolerogenic_checkpoint/`

Tables:

- `checkpoint_candidate_synthesis.tsv`
- `local_checkpoint_evidence.tsv`
- `local_checkpoint_evidence_detail.tsv`
- `perturbation_foundation_checkpoint_evidence.tsv`
- `external_prior_art_query_log.tsv`
- `chembl_checkpoint_target_snapshot.tsv`
- `summary.json`
- `raw_api/*.json` cached API responses

Run summary:

- candidates screened: `29`
- `PROMOTE`: `0`
- `PARK`: `5` (`CD274`, `CD24`, `BTLA`, `CD200`, `CD47`)
- `PARK_LOW`: `6`
- `NO_GO`: `18`

## Inputs Used

Local V3 tables:

- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/broad_residual_gate/broad_residual_residual_tests.tsv`
- `results_v3/wave15_orchestrator_dependency_scan/candidate_dependency_priority_summary.tsv`
- `results_v3/wave15_perturbation_drug_response/gse162463_mouse_crispr_screen_gene_summary.tsv`
- `results_v3/geneformer_*/*gene_summary.tsv`
- `results_v3/wave18_accessible_target_rescue/accessible_target_rescue_candidates.tsv`
- `results_v3/wave18_foundation_rescue/foundation_rescue_candidate_rank.tsv`
- `results_v3/gse111972_full_ms_wm_signature.tsv`
- `results_v3/existing_evidence_candidate_matrix.tsv`

External sources queried and logged:

- Europe PMC REST/search URLs.
- PubMed ESearch URLs.
- Europe PMC preprint-filter queries using `SRC:PPR`.
- ClinicalTrials.gov v2 keyword queries.
- ChEMBL target/activity APIs.
- Google Patents query URLs only; no unauthenticated patent count API was used.

All query terms, links, counts, and returned examples are in
`external_prior_art_query_log.tsv` and `chembl_checkpoint_target_snapshot.tsv`.
I am not claiming novelty for any candidate.

The literature and trial counts are saturation flags, not proof that every hit
is a direct autoimmune interventional precedent. The query log preserves the
exact terms so false positives can be audited.

## Decision Matrix

| gene | call | local recurrence | local state coupling | perturbation/foundation | external prior-art snapshot | interpretation |
|---|---:|---:|---:|---|---|---|
| `CD274` | PARK | 4: Crohn, Sjogren, psoriasis, UC | 3: Crohn, psoriasis, T1D | GSE162463 KO not supportive for lowering MHC-II: median `-0.060`, rank `6946`; no Geneformer support | EuropePMC `33145`, PubMed `1495`, preprint `135`, CT.gov `5`, ChEMBL `CHEMBL3580522` with `1875` nM activity rows; patent query `PD-L1 agonist autoimmune disease CD274` | Closest tractable checkpoint, but PD-1/PD-L1 tolerance is crowded and not a specific lipid-lysosomal/APC-state intervention. |
| `CD24` / `SIGLEC10` | PARK / NO_GO | `CD24` recurrence 4; `SIGLEC10` only 1 local support and 1 negative disease | `CD24` state coupling 0; `SIGLEC10` state coupling 1 | no useful Geneformer support; no direct agonism perturbation | `CD24` EuropePMC `5154`, PubMed `225`, preprint `72`, CT.gov `1`; patent query `CD24Fc autoimmune disease Siglec-10` | CD24Fc/Siglec-10 is a plausible DAMP checkpoint modality, but local state coupling is missing and prior art is not clean. |
| `BTLA` | PARK | 3: Crohn, Sjogren, UC | 0 | no useful perturbation/foundation evidence | EuropePMC `2105`, PubMed `117`, CT.gov `2`; patent query `BTLA agonist autoimmune disease` | Broad checkpoint/tolerance biology, but T-cell weighted rather than myeloid APC-state selective. |
| `CD200` / `CD200R1` | PARK / NO_GO | `CD200` recurrence 3; `CD200R1` recurrence 0 with 3 broad negative diseases | 0 | `CD200R1` KO screen weak/negative for desired direction: MHC-II median `-0.248`, rank `7953` | `CD200` EuropePMC `2492`, PubMed `111`; `CD200R1` EuropePMC `1250`, PubMed `64`; patent queries logged | Ligand recurrence does not translate to receptor/state coupling. Receptor direction is locally contradicted. |
| `CD47` / `SIRPA` | PARK / PARK_LOW | `CD47` recurrence 3; `SIRPA` recurrence 2 | 0 | `CD47` KO enriched MHC-II-low in mouse screen, median `1.222`, rank `1189`, but this is knockout evidence and the common drug route is blockade | `CD47` EuropePMC `5095`, PubMed `105`, CT.gov `0`, ChEMBL `25`; patent query `CD47 SIRPA autoimmune disease` | Useful comparator. Oncology-style blockade would increase phagocytosis and is probably the wrong autoimmune direction. |
| `VSIR` / VISTA | NO_GO | 2: Sjogren, T1D; Crohn negative | 0 | mouse KO signal negative for desired screen direction: median `-0.628`, rank `9671`; no Geneformer support | EuropePMC `641`, PubMed `55`, CT.gov `0`, ChEMBL `CHEMBL4523457` with `159` nM rows; patent query logged | Less saturated than PD-L1/TIM-3, but local recurrence and state coupling fail. |
| `LILRB1/2/3/4/5` | PARK_LOW/NO_GO | `LILRB1/2/3` are IBD-only two-disease signals; `LILRB4` only T1D; `LILRB5` no support and UC negative | 0 | no useful foundation evidence; no direct agonism perturbation | LILRB4 EuropePMC `780`, PubMed `43`, CT.gov `0`; LILRB2 EuropePMC `911`, PubMed `42`, CT.gov `0`; patent queries logged | Druggable myeloid checkpoint class, but local support is too thin and oncology antagonist/depletion precedent is directionally opposite. |
| `LAIR1` | NO_GO | 1: T1D; Crohn and UC negative | 0 | mouse KO MHC-II-low median `1.319`, rank `997`, but disease recurrence is contradicted | EuropePMC `402`, PubMed `35`, CT.gov `0`; patent query logged | Mechanistically plausible inhibitory receptor, but local cross-autoimmune evidence fails. |
| `HAVCR2` / TIM-3 | NO_GO | 0; UC negative | 0 | KO screen weak, median `0.438`, rank `4007` | EuropePMC `9050`, PubMed `315`, CT.gov `5`, ChEMBL `81`; patent query logged | Gal-9/TIM-3 tolerance prior art is crowded and directionally complex. |
| `CD300LF` / CD300F | NO_GO | 1: psoriasis | 0 by state-coupling sources | weak Geneformer support only; GSE162463 median `0.631`, rank `3122` | EuropePMC `223`, PubMed `7`, CT.gov `0`; patent query logged | Most non-saturated specific receptor, but local breadth is only one disease/tissue. |
| `CD300A`, `SIGLEC5/7/9`, `CLEC12A`, `FCGR2B`, `PVR`, `NECTIN2`, `PILRA`, `VSIG4`, `TIGIT` | NO_GO/PARK_LOW | mostly 0-2 disease support, several directional negatives | mostly 0 | no promotion-grade perturbation/foundation support | queries logged for all | Either not myeloid/APC-state selective, contradicted locally, or too crowded. |

## Perturbation And Foundation Evidence

The real perturbation evidence does not rescue the checkpoint route.

- State Parse CD14 still has no named-gene transition target rows, consistent
  with Wave18.
- GSE162463 mouse macrophage CRISPR/FACS rows are knockout evidence, not
  agonist checkpoint evidence. `LAIR1`, `CD47`, `CLEC12A`, `SIRPA`, and
  `CD300LF` have positive MHC-II-low enrichment, but that does not establish
  that agonizing the checkpoint will selectively collapse the human
  lipid-lysosomal/APC/HLA-II disease state.
- Geneformer support is essentially absent. `CD300LF` has weak token-deletion
  support in a narrow pivot panel, but it has only one local disease support
  and no independent direct perturbation validation.

## Lead-Indication Assessment

No feasible lead indication is promoted.

- `CD274` could be imagined as an IBD/psoriasis/T1D tolerogenic comparator, but
  the prior-art and broad immunosuppression issues are too large for a specific
  V3 claim.
- `CD24`/`SIGLEC10` has a biologic modality (`CD24Fc`-like checkpoint
  engagement), but the local state-coupling gate fails.
- `CD300LF` is the least saturated named receptor in this pass, but one
  psoriasis-local signal is not enough for a cross-autoimmune lead indication.

## Source / Query Examples

Representative links from the query log:

- `CD274`: Europe PMC <https://europepmc.org/search?query=%28CD274+OR+%22PD-L1%22+OR+B7-H1%29+autoimmune>; PubMed <https://pubmed.ncbi.nlm.nih.gov/?term=%28CD274+OR+%22PD-L1%22+OR+B7-H1%29+autoimmune>; ClinicalTrials <https://clinicaltrials.gov/search?term=PD-L1+autoimmune>; ChEMBL <https://www.ebi.ac.uk/chembl/g/#browse/activities/filter/target_chembl_id%3ACHEMBL3580522>; patents <https://patents.google.com/?q=PD-L1+agonist+autoimmune+disease+CD274>.
- `CD24`/`SIGLEC10`: Europe PMC <https://europepmc.org/search?query=%28CD24+OR+CD24Fc%29+autoimmune>; PubMed <https://pubmed.ncbi.nlm.nih.gov/?term=%28CD24+OR+CD24Fc%29+autoimmune>; ClinicalTrials <https://clinicaltrials.gov/search?term=CD24Fc+autoimmune>; patents <https://patents.google.com/?q=CD24Fc+autoimmune+disease+Siglec-10>.
- `VSIR`: Europe PMC <https://europepmc.org/search?query=%28VSIR+OR+%22VISTA+checkpoint%22+OR+%22V-domain+Ig+suppressor%22%29+autoimmune>; PubMed <https://pubmed.ncbi.nlm.nih.gov/?term=%28VSIR+OR+%22VISTA+checkpoint%22+OR+%22V-domain+Ig+suppressor%22%29+autoimmune>; ClinicalTrials <https://clinicaltrials.gov/search?term=VSIR+VISTA+autoimmune>; patents <https://patents.google.com/?q=VSIR+VISTA+agonist+autoimmune+disease>.
- `CD300LF`: Europe PMC <https://europepmc.org/search?query=%28CD300LF+OR+CD300F+OR+IREM1%29+autoimmune>; PubMed <https://pubmed.ncbi.nlm.nih.gov/?term=%28CD300LF+OR+CD300F+OR+IREM1%29+autoimmune>; ClinicalTrials <https://clinicaltrials.gov/search?term=CD300F+autoimmune>; patents <https://patents.google.com/?q=CD300F+CD300LF+autoimmune+antibody>.

Full query coverage for all 29 candidates, including preprint queries, is in
`external_prior_art_query_log.tsv`.

## Files Changed

- `scripts/v3_wave19_tolerogenic_checkpoint.py`
- `results_v3/wave19_tolerogenic_checkpoint/`
- `subagents_v3/wave19_tolerogenic_checkpoint.md`
