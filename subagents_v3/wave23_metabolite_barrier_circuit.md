# Wave23-A Metabolite / Barrier-Repair Circuit Scout

Date: 2026-05-27

Scope:

- Script: `scripts/v3_wave23_metabolite_barrier_circuit.py`
- Results: `results_v3/wave23_metabolite_barrier_circuit/`

This is gate evidence only. It does not nominate a final therapeutic finding.

## Question

Test whether the cross-autoimmune lipid-lysosomal/APC state is better explained
by a druggable metabolite-sensing or barrier-repair circuit than by a single
residual gene.

Candidate classes audited:

- AHR / tryptophan-kynurenine
- bile-acid receptors `NR1H4`/FXR and `GPBAR1`/TGR5
- lipid nuclear receptors `PPARA`, `PPARD`, `PPARG`, `NR1H3`, `NR1H2`, RXRs
- SCFA receptors `FFAR2`, `FFAR3`, `HCAR2`
- retinoid/RAR/RXR/VDR
- S1P receptors
- eicosanoid/leukotriene/prostaglandin sensors

## Run

```bash
.venv_v3_py312/bin/python scripts/v3_wave23_metabolite_barrier_circuit.py
```

Inputs were local-first:

- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
- `results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`
- `results_v3/broad_residual_gate/broad_residual_residual_tests.tsv`
- `tmp_v3/wave13_opentargets_gwas_credible_sets.tsv`
- `tmp_v3/wave13_opentargets_reopen_scores.tsv`
- `results_v3/l1000fwd_compound_summary.tsv`
- `results_v3/wave15_perturbation_drug_response/l1000fwd_selectivity_compound_rank.tsv`
- Wave19 PPAR/LXR demotion tables
- LINCS compound metadata

Public API snapshots were used only for druggability/prior-art gaps:
ChEMBL, EuropePMC, and ClinicalTrials.gov.

## Ranked Gate Table

| Rank | Route | Call | Local recurrence | Genetics | Perturbation/L1000 | Druggability | Prior-art / blocker | Whitespace |
|---:|---|---|---|---|---|---|---|---|
| 1 | Eicosanoid / leukotriene / prostaglandin sensors | `NO_GO` | route union positive in 5 diseases but also negative in 5; `LTA4H` retained only Crohn/UC; no strict-core residual survivor | none local | module L1000 hits exist (`PTGIR`, `ALOX5AP`, `zileuton`), but they are generic lipid-inflammatory perturbations | very druggable: top ChEMBL records include `PTGS2:8608`, `PTGS1:5444`, `PTGDR2:4828`, `TBXA2R:4613` | crowded, directionally contradictory, wound/host-defense risk | no |
| 2 | AHR / tryptophan-kynurenine | `NO_GO` | `IDO1` and `KYNU` recur in 4 diseases and retain direction in Crohn/UC/Sjogren, but strict-core survival is 0 | none local | no matching L1000 reversal hit in existing disease/module outputs | druggable: `IDO1:7278`, `TDO2:1640`, `AHR:845` ChEMBL nM records | broad AHR/IDO immunoregulation; EuropePMC query count 17159 | no |
| 3 | PPAR/LXR/RXR lipid nuclear receptors | `NO_GO` | weak/mixed: max gene positive disease count 1; negative union 5 | only weak `NR1H3` MS score 0.099, no disease at >=0.5 | `PPARA` antagonist `GW-6471` reverses local modules in L1000, but does not rescue local/prior gates | very druggable: `PPARG:9307`, `PPARA:5658`, `PPARD:4164` | already demoted in Wave19 for mixed/negative local signal and saturated PPAR/LXR claims | no |
| 4 | SCFA receptors `FFAR2`/`FFAR3`/`HCAR2` | `NO_GO` | `FFAR2`/`HCAR3` expression reaches 3 diseases; no residual support | none local | no disease-signature L1000 support after removing acetate-salt false matches | druggable enough: `FFAR2:1764`, `HCAR2:1210` | microbiome/SCFA/niacin route is crowded and hard to make target-selective | no |
| 5 | Bile-acid receptors FXR/TGR5 | `NO_GO` | max gene positive disease count 1; negative Crohn/UC signal; no residual support | none local | no L1000 support | druggable: `NR1H4:5718`, `GPBAR1:1583` | least crowded in cross-autoimmune terms, but still broad bile-acid/IBD/PBC/metabolic prior art and no V3 state support | least crowded, unsupported |
| 6 | Retinoid/RAR/RXR/VDR | `NO_GO` | expression mixed; positive union 4 and negative union 4; no residual support | none local | retinoid hits are mostly similar/generic, not disease reversal | very druggable: `VDR:24841`, `RXRA:2968`, RARs/RXRs active | vitamin D/retinoic acid/RXR immunomodulation is crowded and pleiotropic | no |
| 7 | S1P receptors | `NO_GO` | expression-only; positive union 4 and negative union 3; no residual support | none local | no L1000 reversal support | druggable: `S1PR1:5512`, `S1PR3:3619`, others active | approved/clinical MS and UC S1P modulators; broad lymphocyte trafficking immunosuppression | no |

Summary counts from `summary.json`: 7 routes audited, 7 `NO_GO`, 0 `PARK`,
0 `GO`.

## Interpretation

The metabolite/barrier circuit hypothesis does not currently explain the V3
cross-autoimmune state better than the residual-gene framing. The route-level
sensor genes are mostly weaker than the residual candidates under the strict
gate: none has strict-core residual survival, none has local multi-disease
genetics, and the apparent local recurrence is mostly expression-only or
IBD-skewed.

The most biologically tempting signal is AHR/tryptophan because `IDO1` and
`KYNU` recur locally. It still fails: the signal collapses to retained but not
strict residual evidence, has no genetics/L1000 support, and looks like
IFN/APC-state readout or broad immunoregulatory prior art rather than a clean
barrier-repair circuit.

The least crowded route is FXR/TGR5 bile-acid sensing, mainly because a
gut-restricted intervention direction is imaginable. It is not actionable from
V3: local recurrence is weak/negative, no residual support appears, and no
perturbation/genetic channel offsets the gap.

## Output Files

- `candidate_gene_local_evidence.tsv`
- `route_local_summary.tsv`
- `route_l1000_matches.tsv`
- `route_l1000_summary.tsv`
- `lincs_compound_presence.tsv`
- `chembl_target_snapshot.tsv`
- `route_chembl_summary.tsv`
- `route_public_api_audit.tsv`
- `source_links.tsv`
- `wave23_ranked_routes.tsv`
- `summary.json`
- `raw_api/` cached ChEMBL, EuropePMC, and ClinicalTrials.gov JSON

## Source Pointers

Exact query URLs and ChEMBL target links are in
`results_v3/wave23_metabolite_barrier_circuit/source_links.tsv`.
Representative API query links:

- AHR/IDO prior art:
  https://europepmc.org/search?query=%28%22aryl+hydrocarbon+receptor%22+OR+AHR+OR+IDO1+OR+kynurenine%29+autoimmune
- FXR/TGR5 prior art:
  https://europepmc.org/search?query=%28%22FXR+agonist%22+OR+NR1H4+OR+GPBAR1+OR+TGR5+OR+%22bile+acid+receptor%22%29+autoimmune+OR+%22inflammatory+bowel+disease%22
- S1P clinical snapshot:
  https://clinicaltrials.gov/search?term=S1P+receptor+modulator+autoimmune
- ChEMBL examples:
  https://www.ebi.ac.uk/chembl/g/#browse/activities/filter/target_chembl_id%3ACHEMBL4685
  and
  https://www.ebi.ac.uk/chembl/g/#browse/activities/filter/target_chembl_id%3ACHEMBL2047

## Changed Files

- `scripts/v3_wave23_metabolite_barrier_circuit.py`
- `results_v3/wave23_metabolite_barrier_circuit/`
- `subagents_v3/wave23_metabolite_barrier_circuit.md`
