# Wave20 Unrestricted Survivor Stress Test

Date: 2026-05-27

Scope: `SNX10`, `DAP`, `FMNL2`, `TNFAIP8L1`, `PPIL3`, `NCK1`,
`PLEK2`, `SEL1L3`, `AQR`, `C15ORF48`, plus adjacent rows from
`results_v3/unrestricted_survivor_scan/unrestricted_survivor_candidates.tsv`.

## Executive Call

No unrestricted survivor passes the hostile Wave19 gates. The focused set is
mostly intracellular trafficking, mitochondrial/stress, cytoskeletal,
spliceosome, or undercharacterized marker biology. The few candidates with
some modality are either wrong-context (`NCK1`) or already prior-arted generic
immune pathways (`LTA4H`, `PPP3CA`, `CHI3L1`, `CXCL9`).

Least-bad comparator: **`SNX10` only as a fail-fast comparator**, not a target.
It has Crohn/UC myeloid recurrence, weak Geneformer support, and public mouse
macrophage/colitis perturbation literature, but fails strict residual
specificity, has no mature selective modality, and carries host-defense/repair
risk.

## Local Gate Evidence

Reproducible outputs are under
`results_v3/wave20_unrestricted_survivor/`.

Key local result: strict residual specificity is essentially absent. In
`wave20_gate_matrix.tsv`, the only candidate with any strict core-covariate
survival is adjacent `CBX3`, and only in one UC stromal analysis. That is a
chromatin/proliferation marker, not a promotable intervention point.

| Candidate | Local recurrence/residual | Perturbation/model | Direction/modality | Wave20 call |
|---|---:|---|---|---|
| `SNX10` | 3 positive diseases, retained residual in 2 IBD diseases, strict core residual 0 | Geneformer 4 support / 1 strong; public mouse colitis/phagosome biology, not V3 module | No safe direction; intracellular, no selective drug | least-bad comparator only |
| `C15ORF48` | 3 positive diseases, retained residual 3, strict core residual 0 | absent from Geneformer token route | MOCCI feedback direction ambiguous; mitochondrial microprotein/miRNA modality poor | state marker only |
| `NCK1` | 3 positive diseases, retained residual 0 | public TCR-Nck inhibitor prior art, wrong local context | inhibit TCR-Nck is broad T-cell suppression | modality comparator only |
| `FMNL2` | 4 positive diseases, retained residual 2, strict core residual 0 | weak Geneformer only | formin/actin inhibition would risk migration and repair | no-go |
| `DAP` | 3 positive diseases, retained residual 2, strict core residual 0 | weak Geneformer only | IFN/death/autophagy direction ambiguous | no-go |
| `PPIL3` | expression recurrence only | weak Geneformer only | nuclear cyclophilin/spliceosome, no direction | no-go |
| `PLEK2` | expression recurrence only | no model/real perturbation | cytoskeletal/PI3K-adjacent, no safe direction | no-go |
| `TNFAIP8L1` | 4-disease expression recurrence, retained residual 0 | no model/real perturbation | TIPE-family biology too ambiguous | no-go |
| `SEL1L3` | expression recurrence only | no model/real perturbation | undercharacterized membrane/ER-adjacent marker | no-go |
| `AQR` | expression recurrence only | no model/real perturbation | core spliceosome helicase | no-go |

Adjacent candidate calls:

- `CBX3`: one strict residual disease, but generic chromatin/proliferation and
  no safe autoimmune modality.
- `CHI3L1`: accessible secreted YKL-40, but crowded autoimmune/inflammatory
  biomarker and repair/remodeling prior art.
- `LTA4H`: enzyme-druggable, but leukotriene/LTB4 inflammatory disease prior
  art is close.
- `PPP3CA`: calcineurin is drugged already; toxicity and prior art dominate.
- `CXCL9`: IFN/CXCR3 trafficking marker; recurrence is not specificity.
- `APOC1`: previous model-demote remains.

## Public Checks

Queries and API outputs are recorded in:

- `wave20_public_search_queries.tsv`: EuropePMC query terms, hit counts, top
  results, and API URLs.
- `wave20_source_links.tsv`: curated source links used for gate judgments.
- `wave20_uniprot_druggability.tsv`: reviewed human UniProt localization and
  function summary.
- `wave20_chembl_target_search.tsv`: ChEMBL human target matches and activity
  counts.

Representative query terms recorded: `SNX10 macrophage colitis`,
`SNX10 phagosome macrophage infection`, `C15ORF48 MOCCI inflammation
macrophage`, `DAP1 interferon gamma cell death`, `FMNL2 Crohn disease L136P`,
`TNFAIP8L1 TIPE1 inflammation immune`, `PPIL3 cyclophilin spliceosome`,
`NCK1 TCR inhibitor autoimmune`, `PLEK2 actin cytoskeleton cell spreading`,
`SEL1L3 immune inflammation`, `AQR Aquarius spliceosome`, `CHI3L1 YKL-40
autoimmune disease`, `LTA4H inhibitor colitis`, and `calcineurin inhibitors
autoimmune tacrolimus cyclosporine`.

Key source links:

- `SNX10` mouse colitis: https://pubmed.ncbi.nlm.nih.gov/26856241/
- `SNX10` phagosome maturation/host defense:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC5589552/
- `C15ORF48`/MOCCI inflammatory macrophage biology:
  https://pubmed.ncbi.nlm.nih.gov/34878835/
- MOCCI coding/non-coding host inflammation:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC8035321/
- `DAP1` IFN-gamma death/autophagy:
  https://pubmed.ncbi.nlm.nih.gov/7828849/
- `FMNL2` Crohn L136P report:
  https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0252428
- `NCK1` TCR-Nck autoimmune inhibitor prior art:
  https://pubmed.ncbi.nlm.nih.gov/28003549/
- `AQR` spliceosome helicase:
  https://pubmed.ncbi.nlm.nih.gov/25599396/
- `CHI3L1` autoimmune YKL-40 review:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC9254466/
- `LTA4H` inhibitor colitis prior art:
  https://pmc.ncbi.nlm.nih.gov/articles/PMC2267273/

## Bottom Line

Do not promote expression recurrence from this unrestricted survivor list. The
honest Wave20 output is negative: **recurrent autoimmune tissue-state markers
without a promotable intervention point**. `SNX10` is the comparator to beat,
not a nominee.
