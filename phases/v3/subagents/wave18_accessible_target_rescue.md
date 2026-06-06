# Wave18-B Accessible / Druggable State-Component Rescue

Returned: 2026-05-27

## Executive Call

**No candidate is promoted to GO.**

After removing the already blocked or parked lanes (`CTSH`, `CTSS`, `CD74/MIF`,
`LGALS9`, `LAPTM5`, `CDK8/CDK19`), the accessible target space still does not
contain a credible cross-autoimmune intervention point that clears all four
promotion gates:

1. cross-disease recurrence,
2. druggability/accessibility,
3. non-saturated novelty angle,
4. credible intervention direction.

The best remaining uses are **parked comparator/readout routes**, not promoted
therapeutic targets. `CD44`, `CD274/PD-L1`, `ITGAM`, `CHI3L1`, and `GPNMB`
are the most useful next assay/stratification comparators, but each fails at
least one hard gate.

## Reproducible Outputs

Script:

- `scripts/v3_wave18_accessible_target_rescue.py`

Output directory:

- `results_v3/wave18_accessible_target_rescue/`

Key outputs:

- `accessible_target_rescue_candidates.tsv`
- `accessible_target_rescue_source_log.tsv`
- `summary.json`

Run summary:

- candidates screened: `24`
- `GO`: `0`
- `PARK`: `11`
- `NO_GO`: `13`

## Inputs Used

Local:

- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
- `results_v3/cross_disease_gene_summary.tsv`
- `results_v3/disease_axis_candidate_gene_rank.tsv`
- `results_v3/wave15_surface_trafficking_dependency/candidate_ranked.tsv`
- `results_v3/wave15_orchestrator_dependency_scan/candidate_dependency_priority_summary.tsv`
- `results_v3/existing_evidence_candidate_matrix.tsv`
- `results_v3/opentargets_candidate_disease_hits.tsv`
- `results_v3/intervention_prior_art_audit.tsv`
- prior reports in `subagents_v3/`, especially Waves 5, 7, 8, 15, 16, and 17.

External API/source snapshot:

- Europe PMC query counts.
- ClinicalTrials.gov v2 keyword counts.
- ChEMBL target search/activity counts.
- Local OpenTargets candidate-disease rows plus live target search URLs.
- Google Patents query URLs only; no unauthenticated count API was used.

ClinicalTrials counts are keyword `totalCount` values and include biomarker or
adjacent records. They are used as saturation flags, not proof of direct target
intervention.

## Decision Matrix

| gene | call | recurrence diseases | state-coupled diseases | broad pos/neg | surface delta/resid/confounder | orchestrator expr/resid | EuropePMC | CT.gov | ChEMBL nM records | reason |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `ITGAM` | PARK | 3 | 7 | 1/0 | 2/6/4 | 0/2 | 29214 | 1 | 0 | SLE/genetics comparator; recurrence below threshold and prior art crowded. |
| `CD44` | PARK | 5 | 4 | 2/1 | 0/0/0 | 4/4 | 20529 | 6 | 21 | Best accessible state-adjacent route, but CD44/hyaluronan/SPP1 biology is saturated and one broad negative disease exists. |
| `CD274` | PARK | 4 | 3 | 4/0 | 0/0/0 | 3/3 | 32490 | 10 | 1875 | Druggable checkpoint, but state support misses threshold and agonist/tolerance lane is heavily crowded. |
| `ITGAX` | PARK | 4 | 4 | 0/1 | 4/4/6 | 2/2 | 19941 | 1 | NA | APC marker/targeting handle; confounder dominance and prior art block promotion. |
| `TYROBP` | PARK | 4 | 4 | 1/1 | 3/3/5 | 2/2 | 2193 | 0 | NA | TREM/DAP12 biology present but intracellular adaptor and confounded myeloid signal. |
| `CD24` | PARK | 4 | 0 | 4/0 | 0/0/0 | 0/0 | 5154 | 1 | NA | Accessible CD24-Siglec checkpoint, but no local state-coupling support. |
| `MSR1` | PARK | 3 | 4 | 0/0 | 2/4/9 | 2/2 | 6103 | 0 | 2 | Scavenger receptor biology, but direct h5ad breadth is weak and confounder dominance is severe. |
| `LILRB2` | PARK | 2 | 0 | 2/0 | 0/0/0 | 0/0 | 898 | 0 | NA | Druggable myeloid checkpoint idea, but insufficient local recurrence/state support. |
| `SIRPA` | PARK | 2 | 0 | 2/0 | 0/0/0 | 0/0 | 872 | 0 | NA | CD47/SIRPA checkpoint is accessible but not locally state-coupled. |
| `GPNMB` | PARK | 3 | 3 | 1/2 | 2/3/7 | 0/0 | 782 | 1 | 0 | Strong MS/repair marker; intervention direction and cross-disease consistency fail. |
| `CHI3L1` | PARK | 3 | 0 | 3/0 | 0/0/0 | 0/0 | 1833 | 9 | 39 | Secreted benchmark/biomarker; no local state-coupling or causal drug route. |
| `LGALS9` | NO_GO | 4 | 7 | 2/0 | 4/7/3 | 3/2 | 2649 | 3 | 191 | Already blocked: crowded and directionally complex Gal-9/TIM-3 tolerance biology. |
| `C1QB` | NO_GO | 2 | 6 | 1/0 | 2/5/5 | 1/3 | 11628 | 10 | NA | Complement/C1q is prior-arted, double-edged, and locally not direction-stable. |
| `FCGR3A` | NO_GO | 2 | 5 | 1/0 | 2/4/6 | 2/3 | 2606 | 6 | 0 | Fc receptor class is crowded and confounded by myeloid abundance. |
| `TREM2` | NO_GO | 1 | 5 | 0/0 | 1/4/6 | 0/2 | 3393 | 2 | 6 | Repair/efferocytosis direction is plausible, but local recurrence is too weak. |
| `FCGR2A` | NO_GO | 3 | 5 | 1/1 | 3/5/9 | 2/0 | 1323 | 1 | 1 | Fc/complement uptake is saturated and highly confounded. |
| `C1QA` | NO_GO | 2 | 6 | 1/1 | 2/6/7 | 1/3 | 11787 | 10 | NA | Same C1q blocker as `C1QB`; lupus/MS-specific biology does not rescue cross-disease target. |
| `TREM1` | NO_GO | 2 | 0 | 2/0 | 0/0/0 | 0/0 | 1613 | 2 | 0 | Tractable inflammatory-myeloid receptor, but IBD-heavy and not state-coupled locally. |
| `LILRB1` | NO_GO | 2 | 0 | 2/0 | 0/0/0 | 0/0 | 1026 | 1 | NA | Too little recurrence/state evidence. |
| `SPP1` | NO_GO | 3 | 4 | 2/0 | 2/4/8 | 0/0 | 7405 | 10 | 0 | SPP1/CD44 axis is crowded and confounder-dominant; repair direction is context-dependent. |
| `AXL` | NO_GO | 1 | 7 | 0/3 | 1/7/8 | 1/2 | 3006 | 3 | 4937 | Druggable TAM kinase, but local disease direction is negative/contradictory and inhibition likely wrong. |
| `LGALS3` | NO_GO | 2 | 5 | 0/2 | 2/3/8 | 1/4 | 4459 | 0 | 1282 | Galectin-3 remains mechanistically interesting, but direct local breadth is contradicted and prior art is heavy. |
| `CD47` | NO_GO | 3 | 0 | 3/0 | 0/0/0 | 0/0 | 5542 | 0 | 25 | Accessible but not state-coupled; blockade would likely increase phagocytosis rather than rescue repair. |
| `MERTK` | NO_GO | 1 | 3 | 0/2 | 1/3/8 | 0/1 | 2713 | 2 | 4425 | Druggable kinase, but local recurrence is weak/negative and autoimmune direction would require agonism, not available inhibition. |

## Candidate Notes

### `CD44`: best parked accessible route, not promotion

Local upside:

- Recurrence union: `5` diseases.
- State-coupled union: `4` diseases.
- Orchestrator: expression support `4` diseases and residual state support `4`
  diseases; priority score `12.0`.
- Broad h5ad: positive in Crohn and UC, MS white-matter microglia delta
  `1.345`, p `0.0332`; one broad negative disease also appears.

Why it is parked:

- Prior-art saturation is high: Europe PMC count `20529` for `"CD44"
  autoimmune`; ClinicalTrials keyword count `6`; ChEMBL target `CHEMBL3232692`
  has `21` nM activity records.
- The intervention direction is not clean. Blocking CD44/hyaluronan/SPP1 could
  reduce inflammatory retention but may also impair repair, trafficking, and
  tissue remodeling.
- Local signal is state-adjacent, not causal. No perturbation evidence shows
  CD44 modulation selectively rescues the lipid-lysosomal/HLA-II APC state.

Call: **PARK as surface stratifier / assay comparator.**

### `CD274` / PD-L1: accessible checkpoint, crowded

Local upside:

- Broad h5ad positives in `4` diseases: Crohn, Sjogren, psoriasis, UC.
- Orchestrator expression support in `3` diseases and residual state support in
  `3` diseases.
- ChEMBL target `CHEMBL3580522` has `1875` nM activity records, reflecting a
  highly tractable checkpoint target class.

Why it is parked:

- State-coupled support is below threshold (`3`, not `4` diseases).
- Europe PMC count is extremely high: `32490` for `("PD-L1" OR CD274)
  autoimmune`.
- The desired autoimmune direction would be checkpoint agonism/tolerization,
  not oncology-style blockade; this is not a new or CD74/HLA-II-specific angle.

Call: **PARK as tolerogenic checkpoint comparator only.**

### `ITGAM`: genetics-rich comparator, not cross-disease rescue

Local upside:

- Wave15 surface screen watchlist: residual state support `6` diseases and raw
  state support `6` diseases.
- State-coupled union in this Wave18 merge: `7` diseases.
- Strong external SLE genetics/prior biology remains relevant from Wave16.

Why it is parked:

- Local recurrence union is only `3` diseases.
- Orchestrator has negative expression support in MS and priority only `3.25`.
- Europe PMC query count is `29214`; integrin/complement modulation is crowded.
- Direction is disease-specific: SLE CD11b functional restoration is not the
  same as cross-autoimmune HLA-II/APC-state rescue.

Call: **PARK as SLE/complement-genetics comparator, not a promoted target.**

### `CHI3L1`: secreted recurrence benchmark, not state target

Local upside:

- Broad h5ad positives in `3` diseases: Crohn, T1D, UC.
- MS white-matter microglia delta `2.007`, p `0.00461`.
- Secreted/accessibility profile is attractive for biomarkers and antibody
  concepts.

Why it is parked:

- No local state-coupling support in Wave15 surface/orchestrator dependency
  tables.
- Europe PMC count `1833` and ClinicalTrials keyword count `9`, mostly
  biomarker/adjacent records.
- ChEMBL target `CHEMBL5724768` has only `39` nM activity records; this is not
  a strong selective intervention package.

Call: **PARK as positive-control biomarker / secreted benchmark.**

### `GPNMB`: repair-marker/delivery handle only

Local upside:

- Strong MS repair/lipid-loader evidence from prior local tables:
  foamy lesion proteomics effect `2.164`, p `3.50e-10`; MIMS2-like microglia
  effect `2.097`, p `0.00592`; spatial MERFISH pathological-vs-homeostatic
  effect `1.743`, p `0.03125`.
- Surface/secreted biology gives a plausible delivery or stratification handle.

Why it is parked:

- Broad h5ad is contradictory: positive disease count `1`, negative disease
  count `2`.
- Wave15 surface screen: delta trend `2`, residual state support `3`,
  confounder-dominant diseases `7`.
- ChEMBL target `CHEMBL3712919` has `0` nM activity records in the API pass.
- A cytotoxic/depleting antibody route is likely the wrong autoimmune modality.

Call: **PARK as PD marker / possible delivery handle; no direct antagonist or
depletion target.**

## Hard No-Go Classes

### Galectins

`LGALS9` remains a no-go despite strong local Wave15 state coupling because the
prior-art and direction problems are unchanged. Wave18 external snapshot:
Europe PMC `2649`, ClinicalTrials `3`, ChEMBL `191` records.

`LGALS3` is even weaker locally for this task: recurrence union `2`, broad
negative diseases `2`, surface confounder-dominant diseases `8`, despite
ChEMBL `1282` records. Its MS/MIMS2 biology is useful, but the direct broad
h5ad evidence and repair/remyelination risk block promotion.

### Complement / Fc Uptake

`C1QA/C1QB`, `FCGR2A`, and `FCGR3A` are no-go. The local Wave5 complement
report already found complement/C1q unsuitable as a shared cross-autoimmune
state. Wave18 recapitulates the issue: C1q has state-coupled correlations but
poor disease recurrence, heavy prior art, negative/contradictory local signals,
and clearance-protection liabilities. Fc receptors are even more confounded by
myeloid abundance and immune-complex disease context.

### TAM / TREM-like Repair Routes

`TREM2`, `MERTK`, and `AXL` are not rescued. They have biologically plausible
repair/efferocytosis direction, but Wave18 recurrence is weak or negative and
the druggable chemistry usually points to inhibition, which is probably the
wrong direction for chronic autoimmune repair.

`TREM1` is tractable as an inflammatory-myeloid receptor but is IBD-heavy and
not state-coupled locally.

### Scavenger / Myeloid Checkpoints

`MSR1`, `LILRB1/2`, `SIRPA`, and `CD47` do not pass. Some are accessible and
less saturated than CD44/PD-L1, but they lack the required cross-disease
state-component recurrence. `CD47/SIRPA` also has an intervention-direction
problem: blockade increases phagocytosis and is not a repair-preserving
HLA-II/APC-state rescue.

## Blocked Comparator Carry-Forward

The Wave18 screen did not reopen these lanes:

- `CTSH`: Wave16 chemistry/selectivity no-go. Public CTSH ChEMBL package had
  `122` retained nM records, `47` unique potency molecules, only `1` molecule
  with 10x margin over assayed comparators, and `0` with 100x margin.
- `CTSS`: direct autoimmune clinical prior art, including RA `NCT00425321`,
  primary Sjogren `NCT02701985`, and celiac `NCT02679014`; use only as assay
  comparator.
- `CD74/MIF`: crowded and directional; anti-CD74/MIF lane remains prior-art
  blocked.
- `LGALS9`: included in Wave18 only to show it still fails promotion despite
  local state coupling.
- `LAPTM5`: Wave17 park as biomarker/readout due poor modality and ambiguous
  cell-type direction.
- `CDK8/CDK19`: mediator kinase route remains parked.

## Source Links

Generated source log:

- `results_v3/wave18_accessible_target_rescue/accessible_target_rescue_source_log.tsv`

Representative public source URLs from the generated log:

- CD44 Europe PMC: <https://europepmc.org/search?query=%22CD44%22+autoimmune>
- CD44 ChEMBL: <https://www.ebi.ac.uk/chembl/g/#browse/activities/filter/target_chembl_id%3ACHEMBL3232692>
- CD44 ClinicalTrials: <https://clinicaltrials.gov/search?term=CD44+autoimmune>
- CD274 Europe PMC: <https://europepmc.org/search?query=%28%22PD-L1%22+OR+CD274%29+autoimmune>
- CD274 ChEMBL: <https://www.ebi.ac.uk/chembl/g/#browse/activities/filter/target_chembl_id%3ACHEMBL3580522>
- CD24 ClinicalTrials: <https://clinicaltrials.gov/search?term=CD24Fc+autoimmune>
- ITGAM ClinicalTrials: <https://clinicaltrials.gov/search?term=ITGAM+autoimmune>
- CHI3L1 Europe PMC: <https://europepmc.org/search?query=%28%22CHI3L1%22+OR+%22YKL-40%22%29+autoimmune>
- GPNMB Europe PMC: <https://europepmc.org/search?query=%28%22GPNMB%22+OR+osteoactivin%29+autoimmune>
- LGALS3 ChEMBL: <https://www.ebi.ac.uk/chembl/g/#browse/activities/filter/target_chembl_id%3ACHEMBL4531>
- LGALS9 ChEMBL: <https://www.ebi.ac.uk/chembl/g/#browse/activities/filter/target_chembl_id%3ACHEMBL5474>
- C1q ClinicalTrials: <https://clinicaltrials.gov/search?term=C1q+autoimmune>
- Google Patents CD44 query: <https://patents.google.com/?q=CD44+antibody+autoimmune+disease+hyaluronan>
- Google Patents PD-L1 query: <https://patents.google.com/?q=PD-L1+agonist+autoimmune+disease+CD274>
- Google Patents anti-C1q query: <https://patents.google.com/?q=anti-C1q+autoimmune+lupus+nephritis>
- CTSS RA trial `NCT00425321`: <https://clinicaltrials.gov/study/NCT00425321>
- CTSS Sjogren trial `NCT02701985`: <https://clinicaltrials.gov/study/NCT02701985>
- CTSS celiac trial `NCT02679014`: <https://clinicaltrials.gov/study/NCT02679014>
- CTSS celiac PubMed `39739628`: <https://pubmed.ncbi.nlm.nih.gov/39739628/>

## Bottom Line

Wave18 did not rescue a promotable accessible target. The strongest practical
next use is to keep a **parked assay panel**:

`CD44`, `CD274`, `ITGAM`, `CHI3L1`, `GPNMB`, plus blocked comparators
`CTSS`, `CTSH`, `LGALS9`, and `LAPTM5`.

Promotion should require new perturbation evidence showing selective reduction
of the `CD74/HLA-II/lysosomal APC` state without collapsing generic IFN/APC
biology or damaging repair/efferocytosis programs. No current accessible node
meets that standard.
