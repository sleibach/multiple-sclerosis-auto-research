# Wave16-A CTSH Chemistry, Structure, Selectivity Feasibility

**Scope:** CTSH/cathepsin H chemistry and structure only. This is a tractability verdict for the V3 cross-autoimmune HLA-II/lysosomal APC-state intervention claim, not a finding claim.

## Verdict

**NO-GO for selective CTSH modulation as a therapeutic intervention point.**

CTSH remains a plausible local APC-state biology marker from Wave15, but the chemistry/selectivity package is not strong enough to support a selective therapeutic claim. Public chemistry is dominated by covalent or reactive cathepsin chemotypes, many CTSH actives are equipotent or stronger against CTSB/CTSL/CTSC/CTSS, curated IUPHAR pharmacology lists only two CTSH inhibitor interactions with selectivity explicitly not determined, and the safety/delivery liabilities are not peripheral-only.

Best disposition: keep CTSH as a lysosomal/APC-state biology comparator and assay readout. Do not nominate CTSH inhibition as the intervention without a new selective probe showing clean CTSH > CTSS/CTSB/CTSL/CTSC/CTSZ margins in primary APC lysosomes and a lung/CNS safety window.

## Reproducible Outputs

Script:
- `scripts/v3_wave16_ctsh_chemistry_selectivity.py`

Output directory:
- `results_v3/wave16_ctsh_chemistry_selectivity/`

Key outputs:
- `chembl_target_summary.tsv`
- `chembl_cathepsin_activities.tsv`
- `chembl_activity_summary.tsv`
- `chembl_ctsh_compound_selectivity.tsv`
- `iuphar_ctsh_interactions.tsv`
- `structure_summary.tsv`
- `uniprot_ctsh_summary.json`
- `summary.json`
- raw API payloads under `raw/`

## Local Context

Wave15 nominated `CTSH` as a local `GO_SCOUT` candidate with residual CD74/HLA state coupling across 8 diseases and disease-control trend support across 5 diseases (`subagents_v3/wave15_surface_trafficking_dependency.md`). That establishes local expression/state recurrence, not chemical intervention feasibility.

## Chemistry And Selectivity

From `summary.json` and `chembl_activity_summary.tsv`:

| Metric | Result |
|---|---:|
| Human CTSH ChEMBL target | `CHEMBL2225` |
| CTSH nM activity records retained | 122 |
| CTSH unique potency molecules | 47 |
| Best CTSH potency | 0.46 nM |
| Median CTSH potency | 5795.5 nM |
| CTSH molecules with any requested comparator assay | 41 |
| CTSH molecules with 10x margin over all assayed comparators | 1 |
| CTSH molecules with 100x margin over all assayed comparators | 0 |
| IUPHAR curated CTSH inhibitor interactions | 2 |

The apparent best CTSH potency is not selective. `CHEMBL371420` has CTSH Ki 0.46 nM, but CTSB 1.3 nM and CTSL 0.79 nM, giving only 2.8x and 1.7x margins. `CHEMBL190121`/leupeptin is much more potent on CTSB/CTSL than CTSH. E-64 (`CHEMBL374508`) is also nonselective, with stronger CTSB/CTSL activity than CTSH in the retained records.

The only row passing a 10x margin over all *assayed* comparators is `CHEMBL114161`: CTSH 40 nM, CTSB 460 nM, CTSL 740 nM. That is not sufficient for a therapeutic selectivity claim because CTSS, CTSC, and CTSZ were not assayed for that molecule in the retained ChEMBL overlap, and the structure is a peptidyl aldehyde-like chemotype rather than an obvious developable selective series.

IUPHAR/GtoPdb is thin: target 2349 lists compound 1b with Ki 40 nM and compound 1e with IC50 440 nM, both marked `Not Determined` for selectivity in the API output (`iuphar_ctsh_interactions.tsv`).

## Structure Tractability

Structure availability is adequate for assay design but not enough to rescue selectivity:

| Source | Evidence |
|---|---|
| AlphaFold | P09668 full-length model, mean pLDDT 93.9 |
| PDB | `6CZK`, wild-type human pro-cathepsin H, 2.001 A |
| PDB | `6CZS`, human pro-cathepsin H C26S mutant, 1.66 A |

The PDB structures are proenzyme structures, not mature human CTSH inhibitor-bound structures. They explain CTSH prodomain/minichain biology, but the catalytic Cys-His-Asn papain fold remains highly conserved across CTSB/CTSL/CTSS. The human procathepsin H paper also reports that procathepsin H is trans-activated by cathepsin L, which complicates a clean CTSH-only intervention model.

## Safety And Delivery Liabilities

CTSH is not a clean APC-restricted target.

Lung: PubMed literature implicates cathepsin H in processing hydrophobic surfactant-associated protein C in type II pneumocytes. That makes systemic CTSH inhibition a pulmonary surfactant risk, especially for chronic autoimmune dosing.

CNS: Cathepsin H contributes to enkephalin and galanin neuropeptide production in secretory vesicles, with knockout reducing brain peptide levels in mice. CNS penetration would be needed for an MS microglia/APC claim, but CNS exposure is exactly where this liability becomes hardest to ignore.

Skin/gut: Local delivery could reduce systemic exposure, but it narrows the claim. A topical or gut-restricted CTSH modulator would not support a cross-autoimmune HLA-II/APC-state intervention without disease-specific delivery and tissue proof. Skin is also not clearly an inhibition-safe compartment: recent AD work reports reduced cathepsin H expression in atopic dermatitis, making blanket skin inhibition directionally risky.

Lysosomal homeostasis: CTSH is annotated as important for overall lysosomal protein degradation. Chronic partial inhibition may be tolerated if exquisitely selective and compartment-limited, but the current chemistry does not show that.

## Patent / Prior-Art Saturation

Targeted Google Patents searches did not reveal a dense CTSH-specific autoimmune/HLA-II inhibitor estate comparable to CTSS. That does not make CTSH attractive; it mostly reflects weaker therapeutic prosecution around CTSH.

The neighboring CTSS/MHC-II space is crowded:
- `US20050080010A1` claims suppression of class II MHC-restricted immune responses via cathepsin S inhibition, including autoimmune use.
- `US8227468B2` covers cathepsin S inhibitor compounds.
- A 2011 patent review reports more than 40 cathepsin S patent applications from 2004 to 2010.
- `US20240352070A1` shows modern broad cathepsin inhibitor claims that include CTSS and CTSH assay language and immunological-disorder use.

Interpretation: patent saturation is moderate for broad cathepsin inhibitors and high for CTSS/MHC-II immunology. CTSH-specific whitespace may exist, but the chemical and safety barriers are the gating problem, not IP whitespace.

## Decision Logic

Go criteria for CTSH would require all of the following:
- A selective CTSH probe with at least 100x biochemical margin against CTSS, CTSB, CTSL, CTSC, and CTSZ.
- Demonstrated HLA-II/CD74/APC-state modulation in disease-relevant human APCs at exposures below comparator cathepsin inhibition.
- Lung type II pneumocyte/SP-C and neuropeptide safety counterscreens.
- A delivery strategy matched to disease tissue: CNS for MS, local gut for IBD/celiac, topical/skin-local for psoriasis/AD.

Current public evidence fails the first criterion and raises concerns on the third. Therefore CTSH is **not tractable enough** for the V3 therapeutic intervention point.

## Public Sources Checked

- ChEMBL target/activity API: CTSH `CHEMBL2225`; comparators `CHEMBL2954`, `CHEMBL4072`, `CHEMBL3837`, `CHEMBL2252`, `CHEMBL4160`: https://www.ebi.ac.uk/chembl/
- IUPHAR/GtoPdb cathepsin H target 2349: https://www.guidetopharmacology.org/GRAC/ObjectDisplayForward?objectId=2349
- UniProt P09668: https://www.uniprot.org/uniprotkb/P09668/entry
- AlphaFold P09668: https://alphafold.ebi.ac.uk/entry/P09668
- RCSB PDB 6CZK: https://www.rcsb.org/structure/6CZK
- RCSB PDB 6CZS: https://www.rcsb.org/structure/6CZS
- Crystal structures of human procathepsin H: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0200374
- CTSH neuropeptide processing: https://pubmed.ncbi.nlm.nih.gov/22582844/
- CTSH surfactant protein C processing: https://pubmed.ncbi.nlm.nih.gov/12034564/
- CTSS selective inhibitor autoimmunity model: https://pubmed.ncbi.nlm.nih.gov/21439785/
- CTSS inhibitor patent review: https://pubmed.ncbi.nlm.nih.gov/21342054/
- ASP1617 cathepsin-S first-in-human safety/PD paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC12830235/
- Google Patents, CTSS MHC-II autoimmune claim: https://patents.google.com/patent/US20050080010A1/en
- Google Patents, CTSS inhibitor compounds: https://patents.google.com/patent/US8227468
- Google Patents, broad cathepsin inhibitors including CTSS/CTSH assay language: https://patents.google.com/patent/US20240352070A1/en
