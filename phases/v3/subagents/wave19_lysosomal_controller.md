# Wave19-B lysosomal/lipid-controller audit

Date: 2026-05-27

## Bottom line

No upstream lysosomal stress or lipid-handling controller met promotion criteria for the shared cross-autoimmune lipid-lysosomal/APC/HLA-II module.

The closest tractable route is **LIPA/LAL enhancement**, but it is a **PARK**, not a GO: the direction is explicit and modality precedent exists, yet V3 local support is confounder-heavy/myeloid-contradictory, CNS delivery is unresolved, and MS white-matter repair prior art is already active. **NPC1/NPC2 rescue** is a useful cholesterol-egress readout route, and **LRRK2 inhibition** is an IBD-skewed disease-specific route. TFEB/TFE3, MCOLN1/TRPML1, PIKFYVE, GBA/GBA2, PPAR/LXR/ABCA1/ABCG1, and generic mTOR/autophagy modulation are not promoted.

## Reproducible outputs

Script: `scripts/v3_wave19_lysosomal_controller.py`

Command:

```bash
./.venv_v3_py312/bin/python scripts/v3_wave19_lysosomal_controller.py
```

Output directory: `results_v3/wave19_lysosomal_controller/`

Generated tables:

- `candidate_local_evidence.tsv`: 35 candidates merged across broad h5ad recurrence, cross-disease summary, Wave15 surface/orchestrator dependency tables, and Geneformer/foundation summaries.
- `route_summary.tsv`: route-level local maxima plus external gate calls.
- `decision_matrix.tsv`: promotion criteria by route.
- `external_evidence_matrix.tsv`: direction, modality, delivery, prior-art, and blocker notes.
- `source_log.tsv`: real source URLs and query terms used for external evidence.
- `summary.json`: counts and call lists.

## Decision matrix

| Route | Direction | Local state/recurrence read | External tractability / prior art | Call |
|---|---|---:|---|---|
| LIPA/LAL | Enhance or replace LAL; do not inhibit | Max recurrence 4, state 5, negative 2; `state_supported_confounded_mixed_negative` | Approved ERT precedent, macrophage biology, but tissue/CNS delivery unresolved and MS repair prior art active | PARK |
| NPC1/NPC2 | Rescue lysosomal cholesterol egress | Max recurrence 3, state 7, negative 1; NPC2 confounded | Strong NPC disease biology, weak selective autoimmune modality | PARK_READOUT |
| LRRK2 | Inhibit kinase | Crohn/UC-skewed recurrence 2; no state support | Clinical kinase-inhibitor matter, but Crohn/Parkinson prior art crowded and not shared-autoimmune | PARK_DISEASE_SPECIFIC |
| MCOLN1/TRPML1 | Activate TRPML1/CLEAR flux | MCOLN1 local negative/absent | ML-SA1/tool agonist biology, no autoimmune-grade package | NO_GO_TOOL_ONLY |
| TFEB/TFE3 | Activate CLEAR/lysosomal biogenesis | TFEB/TFE3 local negative/absent | Master regulator biology, but indirect broad activation and no selective APC modality | NO_GO |
| PIKFYVE | Inhibit for IL-12/23/TLR suppression | Recurrence 2; no state support | Apilimod reached Crohn/RA/psoriasis-adjacent prior art; direction disrupts lysosomal homeostasis | NO_GO |
| PPAR/LXR/ABCA1/ABCG1 | Activate efflux programs | Mixed/negative: PPARG/NR1H3 negative in 2, ABCG1 negative in 3 | Saturated autoimmune/metabolic claims, LXR lipogenesis and PPAR-gamma systemic liabilities | NO_GO |
| mTOR/autophagy | mTOR inhibition/autophagy induction | Sparse/mixed; ATG7 recurrence without state | Rapalog prior art, broad immunosuppression/autophagy liability | NO_GO |
| GBA/GBA2 | Enhance/rebalance sphingolipid handling | No recurrence; GBA2 negative in UC | Gaucher/Parkinson modality precedent only; no autoimmune module support | NO_GO |

Cathepsin/IFI30, lysosomal membrane, and endolysosomal trafficking rows are retained as local comparators only. They confirm that V3 can recover lysosomal APC/HLA-II biology (`CTSH`, `CTSS`, `IFI30`) but they are not upstream controller interventions for this task.

## Local evidence highlights

- `LIPA`: broad positive in Crohn disease, psoriasis, and T1D; negative in UC. Wave15 surface dependency had 4 delta-trend diseases, 5 residual non-IFN state-support diseases, and 6 confounder-dominant diseases. Orchestrator support was 3 expression-trend and 3 residual-state diseases. Foundation support was present but weak/inconsistent.
- `NPC1/NPC2`: NPC1 had Crohn/psoriasis broad positives and strong Wave15 state coupling, but confounder dominance remained high; NPC2 was T1D-positive and confounded.
- `TFEB`, `TFE3`, `MCOLN1`: no recurrent positive local signal; each had a negative broad h5ad disease call.
- `PIKFYVE`: Crohn/psoriasis recurrence without state coupling.
- `PPARG/NR1H3/ABCG1`: mixed or negative local direction; `ABCG1` was negative across Crohn, psoriasis, and T1D.
- `ATG7`: recurrence in psoriasis, T1D, and UC, but no state coupling; this supports the decision to demote generic autophagy routes.
- Positive local controls were recovered: `CTSH` max recurrence 5/state 8, `CTSS` recurrence 4/state 6, and `IFI30` recurrence 5/state 5, confirming the module is detectable but favoring downstream APC/HLA-II handling over upstream lysosome-wide controllers.

## External evidence anchors

The full source/query list is in `results_v3/wave19_lysosomal_controller/source_log.tsv`. Key anchors:

- TFEB/CLEAR: PubMed `19556463`, `21617040`, and mTOR-TFEB PubMed `22576015`.
- MCOLN1/TRPML1: TRPML1-calcium/calcineurin/TFEB biology via PubMed/PMC `25720963`, and ML-SA1 tool agonist PubMed `25266962`.
- LIPA/LAL: GeneReviews LAL deficiency (`https://www.ncbi.nlm.nih.gov/books/NBK305870/`), FDA Kanuma label, macrophage LAL perturbation (`https://pmc.ncbi.nlm.nih.gov/articles/PMC3178672/`), and 2026 LAL/GPNMB microglial white-matter repair prior art (`https://link.springer.com/article/10.1186/s12974-026-03782-7`).
- PIKFYVE/apilimod: IL-12/23 inhibition PubMed `17053051`, Crohn phase 2 PubMed `19918967`, macrophage lysosomal homeostasis liability (`https://pmc.ncbi.nlm.nih.gov/articles/PMC6791654/`).
- NPC1/NPC2: GeneReviews NPC (`https://www.ncbi.nlm.nih.gov/books/NBK1296/`) and HPBCD/NPC ClinicalTrials query.
- LRRK2: Crohn/Parkinson functional variants DOI `10.1126/scitranslmed.aai7795` and LRRK2 inhibitor ClinicalTrials query.
- LXR/PPAR/mTOR: LXR EAE PubMed `16955483`, LXR lipogenesis PubMed `11090131`, rosiglitazone UC PubMed `18325386`, and sirolimus SLE PubMed `29551338`.

## Interpretation

The shared autoimmune module is real locally, but the upstream lysosomal/lipid-controller layer is not the best intervention point right now. The robust V3 signal sits closer to antigen processing/loading and lysosomal APC machinery than to global CLEAR, autophagy, cholesterol-efflux, or lipid-storage rescue programs.

If this axis is carried forward experimentally, use the parked routes as perturbation/readout controls rather than target nominations: LIPA/LAL enhancement as the main rescue hypothesis, NPC1/NPC2 as cholesterol-egress readouts, MCOLN1/TFEB as positive lysosomal-flux tools, and CTSS/CTSH/IFI30 as APC/HLA-II module readouts.

## Files changed

- `scripts/v3_wave19_lysosomal_controller.py`
- `subagents_v3/wave19_lysosomal_controller.md`
- `results_v3/wave19_lysosomal_controller/candidate_local_evidence.tsv`
- `results_v3/wave19_lysosomal_controller/decision_matrix.tsv`
- `results_v3/wave19_lysosomal_controller/external_evidence_matrix.tsv`
- `results_v3/wave19_lysosomal_controller/route_summary.tsv`
- `results_v3/wave19_lysosomal_controller/source_log.tsv`
- `results_v3/wave19_lysosomal_controller/summary.json`
