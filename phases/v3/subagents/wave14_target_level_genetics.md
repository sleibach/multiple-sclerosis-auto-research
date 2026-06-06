# Wave 14 Target-Level Genetics Audit

Returned: 2026-05-27

Role: `wave14_target_level_genetics_worker`

Scope: determine whether narrowed V3 candidates have target-level genetic
anchoring strong enough for the V3 DoD, beyond Open Targets credible-set
triage.

Candidates: `SLC15A4`, `TASL`, `IRF5`, `PTPN2`, `TNFAIP3`, `CLEC16A`,
`SH2B3`, `GPR65`, `CIITA`, `RFX5`, `GSK3B`, `CD74`.

## Deliverables

- Script: `scripts/v3_wave14_target_level_genetics.py`
- Output directory: `results_v3/wave14_target_level_genetics/`
- Main truth table:
  `results_v3/wave14_target_level_genetics/target_level_genetics_truth_table.tsv`
- Summary JSON:
  `results_v3/wave14_target_level_genetics/target_level_genetics_summary.json`
- Supporting outputs:
  - `opentargets_locus_summary.tsv`
  - `gtex_gene_lookup.tsv`
  - `gtex_eqtl_availability.tsv`
  - `gwas_catalog_mapped_gene_autoimmune_top_associations.tsv`
  - `gwas_catalog_access.tsv`
  - `resource_accessibility.tsv`

## Bottom Line

**Conservative call: no-go for V3 target-level genetics.**

No narrowed candidate currently has disease GWAS evidence plus validated
cis-eQTL/pQTL instruments plus proper multi-signal coloc/MR across four
autoimmune diseases. The strongest candidates remain **locus-level** genetics
or pathway-state biology, not target-level causal genetics.

Do not use this audit to claim causal genetics from locus co-occurrence. Open
Targets `gwas_credible_sets` rows and GWAS Catalog mapped-gene rows are useful
triage only.

## Method

The audit script:

1. Read the supplied Open Targets file:
   `tmp_v3/wave13_opentargets_gwas_credible_sets.tsv`.
2. Summarized locus-level disease breadth at score thresholds `>=0.5` and
   `>=0.8`.
3. Queried GTEx v8 API for significant single-tissue cis-eQTL counts in a
   compact relevance panel: blood, EBV lymphocytes, spleen, colon, ileum, skin,
   thyroid, brain cortex/frontal cortex, and fibroblasts.
4. Queried GWAS Catalog REST v2 mapped-gene associations and filtered
   autoimmune trait labels. This is top-association evidence, not summary-stat
   colocalization.
5. Checked resource accessibility and blockers for OpenGWAS, FinnGen, eQTLGen,
   eQTL Catalogue, and the local GWAS Catalog parquet.

## Source/Access Notes

- GTEx API was accessible and identifies itself as the service powering the
  GTEx Portal: <https://gtexportal.org/api/v2/>.
- GWAS Catalog REST v2 is documented as providing literature-curated top
  associations and metadata: <https://www.ebi.ac.uk/gwas/rest/api/v2/docs>.
- OpenGWAS documents that most endpoints, including `gwasinfo`, require JWT
  authentication; this run got `401` for the unauthenticated endpoint:
  <https://api.opengwas.io/api/>.
- FinnGen reports that summary statistics are downloadable after filling an
  access form and receiving download instructions by email:
  <https://www.finngen.fi/en/access_results>.
- eQTLGen full cis-eQTL summary statistics are available as a 3.6 GB file:
  <https://kghub.org/kg-registry/resource/eqtlgen/eqtlgen.cis_eqtl_full.html>.

Mechanistic/literature links used only as context, not as causal genetics:
GPR65 pH sensing and endolysosomal immune function
<https://pmc.ncbi.nlm.nih.gov/articles/PMC9720675/>; SLC15A4 inhibitor
chemoproteomics <https://www.nature.com/articles/s41589-023-01527-8>; TASL
autoimmune/TLR biology <https://www.nature.com/articles/s41467-024-55690-0>;
TNFAIP3/A20 immune regulation <https://pmc.ncbi.nlm.nih.gov/articles/PMC6584049/>;
PTPN2 Crohn/UC genetics <https://pmc.ncbi.nlm.nih.gov/articles/PMC3310077/>;
CLEC16A autoimmunity/autophagy review
<https://pmc.ncbi.nlm.nih.gov/articles/PMC10179542/>; SH2B3/LNK JAK-STAT
regulation <https://pmc.ncbi.nlm.nih.gov/articles/PMC8781068/>.

## Truth Table Summary

| Gene | Disease genetics | cis-eQTL availability | Tissue relevance | Proper coloc/MR feasible now? | Conservative call |
|---|---|---|---|---|---|
| `SLC15A4` | Limited locus: SLE only in OT score `>=0.5`; GWAS Catalog autoimmune hits are SLE-heavy. | Yes in GTEx panel. | Local trend in 4/7 tested diseases, but not genetics. | No. Disease breadth and full paired summary stats missing. | No-go; lupus-focused follow-up only. |
| `TASL` / `CXorf21` | Limited locus: RA and SLE in OT. | Yes via GTEx `CXorf21`, but sparse. | Local trend in 3/7 tested diseases. | No. X-linked/SLE-heavy and full paired summary stats missing. | No-go; branch support only. |
| `IRF5` | Broad locus: 9 OT diseases at score `>=0.5`/`>=0.8`. | Yes in 9 queried GTEx tissues. | No local gene-level recurrence trend in 7 tested diseases. | No. Needs target-level colocalization, not mapped-gene/locus breadth. | Future coloc priority, not DoD. |
| `PTPN2` | Broad locus: 8 OT diseases at score `>=0.5`; 4 at `>=0.8`. | Yes in spleen, thyroid, fibroblasts. | Local trend in 4/7 tested diseases. | No. Direction likely restoration, not inhibition; full summary stats missing. | Future coloc priority, not DoD. |
| `TNFAIP3` | Broad locus: 7 OT diseases at score `>=0.5`/`>=0.8`. | Not detected in queried GTEx panel. | Local trend in 2/7 tested diseases. | No. No usable cis-eQTL instrument in this panel and restoration direction is hard. | No-go as target-level genetics. |
| `CLEC16A` | Broad locus: 7 OT diseases at score `>=0.5`. | Yes in 7 queried GTEx tissues. | Local trend in 1/7 tested diseases. | No. 16p13 locus ambiguity with nearby `CIITA`/`DEXI`/`SOCS1`; full summary stats missing. | Future coloc priority, not DoD. |
| `SH2B3` | Broad locus: 10 OT diseases at score `>=0.5`; 9 at `>=0.8`. | Yes in blood/immune GTEx tissues. | Local trend in 2/7 tested diseases. | No. 12q24 pleiotropy and no target-level coloc/MR. | Future coloc/control only. |
| `GPR65` | Broad-ish locus: 5 OT diseases at score `>=0.5`; only Crohn/UC at `>=0.8`. | Yes in 5 queried GTEx tissues. | Local trend in 1/7 tested diseases. | No. Directionality unresolved; full paired summary stats missing. | Best fail-fast genetics scout, not DoD. |
| `CIITA` | GWAS Catalog top-association-only; no supplied OT credible-set support. | Yes in 5 queried GTEx tissues. | Local trend in 3/7 tested diseases. | No. HLA-II state proximity is not target-level disease genetics. | No-go. |
| `RFX5` | No disease genetic locus evidence in supplied OT rows or GWAS Catalog sample. | Yes in 5 queried GTEx tissues. | Local trend in 3/7 tested diseases. | No. | No-go. |
| `GSK3B` | No disease genetic locus evidence in supplied OT rows or GWAS Catalog sample. | Yes in 9 queried GTEx tissues. | No wave13 expression row. | No. | No-go. |
| `CD74` | No disease genetic locus evidence in supplied OT rows or GWAS Catalog sample. | Yes only in colon sigmoid in queried GTEx panel. | Local trend in 5/7 tested diseases. | No. Expression/state marker, not genetic target. | No-go. |

## Interpretation

`IRF5`, `PTPN2`, `CLEC16A`, `SH2B3`, and `GPR65` are the only candidates worth
future formal coloc/MR work. That statement is a prioritization, not evidence
that any is causal. `TNFAIP3` has strong autoimmune locus breadth but did not
show a significant GTEx cis-eQTL in the queried relevance panel, and the
therapeutic direction would likely be restoration of A20 function.

`SLC15A4`/`TASL` are mechanistically attractive but genetically narrow in this
audit. `SLC15A4` is SLE-heavy; `TASL` has RA/SLE locus evidence and sparse
eQTL availability. They do not meet a cross-autoimmune target-level genetics
bar.

`CIITA`, `RFX5`, `GSK3B`, and `CD74` do not have enough disease genetic support
to anchor a V3 target claim. Their relevance is pathway/state/perturbation
biology, not genetics.

## Why Full Coloc/MR Was Not Run

Full target-level coloc/MR requires disease GWAS summary statistics and
matching cis-eQTL/pQTL summary statistics at the relevant loci, plus LD-aware
multi-signal handling. This run did not have those inputs locally.

Concrete blockers:

- Open Targets rows are already reduced locus-level evidence and do not expose
  enough per-variant summary-stat detail for independent coloc.
- GWAS Catalog API returned top associations and metadata, not the full
  disease summary-stat matrices needed for coloc.
- The local GWAS Catalog parquet exists, but no `pyarrow`, `fastparquet`, or
  `duckdb` reader is installed in the active Python environment.
- OpenGWAS required JWT authentication for the needed endpoints in this run.
- FinnGen summary stats are public but require an access form/email workflow;
  no files were available locally during this run.
- GTEx API could confirm significant cis-eQTL availability, but the full
  SNP-level tissue QTL files were not downloaded.
- eQTLGen full cis-eQTL summary statistics are a 3.6 GB file; not downloaded.
- No target-specific public pQTL instruments were established for these mostly
  intracellular/adaptor/transcriptional candidates.

## Go/No-Go Call

**No-go for target-level genetics supporting V3 DoD.**

The cleanest statement the project can make is: several candidates have strong
autoimmune locus-level evidence and some have cis-eQTL availability, but none
currently has validated, directionally interpretable, disease-colocalized
target-level genetics across the required disease breadth. The genetics channel
should be marked missing/insufficient for V3 DoD unless a future run obtains
and analyzes the necessary disease GWAS and eQTL/pQTL summary statistics.
