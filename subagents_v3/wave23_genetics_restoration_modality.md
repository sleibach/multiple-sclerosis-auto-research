# Wave23-B Genetics-First Restoration Modality Scout

Date: 2026-05-27

Scope: revisit genetically anchored negative regulators and
autophagy/endolysosomal loci as restoration targets, not inhibitor targets.
This is a routing artifact for the V3 autoimmune research session, not a final
therapeutic finding.

Owned outputs:

- Script: `scripts/v3_wave23_genetics_restoration_modality.py`
- Results: `results_v3/wave23_genetics_restoration_modality/`

Run:

```bash
.venv_v3_py312/bin/python scripts/v3_wave23_genetics_restoration_modality.py
```

## Inputs Used

Local first:

- `tmp_v3/wave13_opentargets_gwas_credible_sets.tsv`
- `results_v3/wave20_genetic_druggable_altaxis/`
- `results_v3/wave14_target_level_genetics/target_level_genetics_truth_table.tsv`
- `results_v3/broad_h5ad_gene_discovery/broad_h5ad_gene_rank.tsv`
- `results_v3/wave15_perturbation_drug_response/candidate_level_synthesis.tsv`
- `results_v3/druggability/chembl_target_activity_summary.tsv`
- `results_v3/druggability/uniprot_target_summary.tsv`

Public/current source interpretation was limited to modality/prior-art context
already present in Wave20 or checked against public pages. The main public
source table is written to
`results_v3/wave23_genetics_restoration_modality/public_source_interpretation.tsv`.

## Bottom Line

No candidate is promoted.

`GPR65` and `IL10` are `PARK`, not `GO`: each has a plausible current modality
class that can increase pathway activity, but both remain blocked by prior art,
local evidence gaps, and missing target-level disease-cell rescue.

All other candidates are `NO_GO` for a restoration-first program. The common
failure mode is not absence of autoimmune genetics. It is that the correct
direction is either not restoration, or restoration is the correct direction
but no current modality can deliver target-selective restoration in the
relevant immune/tissue compartments.

## Ranked GO/PARK/NO_GO Table

| Rank | Gene | Call | Restoration direction check | Current feasible modality | Kill/park reason |
|---:|---|---|---|---|---|
| 1 | `GPR65` | `PARK` | Agonize/PAM if risk alleles reduce anti-inflammatory pH/cAMP response. | GPCR agonist/PAM chemistry is feasible; ChEMBL/API and patent signals exist. | Local support is weak/contradictory and IBD/GPR65 modulator prior art is already direct. Needs non-IBD coloc and human disease-cell rescue. |
| 2 | `IL10` | `PARK` | Increase regulatory IL-10 signaling. | Recombinant/engineered IL-10 or IL10R agonism is feasible. | Direct IL-10 autoimmune/IBD therapy prior art and no local biomarker delta. Targeted/localized IL-10 remains speculative here. |
| 3 | `PTPN2` | `NO_GO` | Restore TCPTP; inhibition is wrong direction. | No target-selective TCPTP activator/restorer found locally; inhibitor chemistry is abundant but wrong direction. | Correct direction is restoration, but no current modality can restore TCPTP selectively in T-cell/myeloid/epithelial compartments. |
| 4 | `SH2B3` | `NO_GO` | Restore LNK adaptor brake. | No direct adaptor-function restoration modality. | Very broad locus evidence, but 12q24 pleiotropy and no LNK-restoring modality. |
| 5 | `CLEC16A` | `NO_GO` | Restore CLEC16A-linked mitophagy/autophagy if hypofunction is causal. | No selective direct CLEC16A drug; only broad indirect autophagy/mitophagy modulation. | Locus ambiguity with `CIITA`/`DEXI`/`SOCS1` plus no target-selective restoration. |
| 6 | `ATG16L1` | `NO_GO` | Restore autophagy/xenophagy in hypomorphic-risk context. | No selective ATG16L1 restoration drug. | Broad autophagy modulation is not target-selective and carries infection/epithelial/cancer liabilities. |
| 7 | `TNFAIP3` | `NO_GO` | Restore A20/NF-kappaB brake. | No direct A20-restoring small molecule or biologic in local evidence. | Strong biology but no current target-selective restoration modality. |
| 8 | `OSMR` | `NO_GO` | Not restoration; current concept is OSM/OSMR blockade. | Anti-OSM/anti-OSMR biologic concept is inhibitory. | Local Wave20 comparator only; prior-demoted tissue-remodeling/IBD-heavy route. |
| 9 | `TASL` | `NO_GO` | Not restoration; pathway concept is dampening endolysosomal TLR/IRF signaling. | No TASL restoration modality; inhibition would be the comparator. | Local endolysosomal addition, but limited RA/SLE genetics and no restoration rationale. |
| 10 | `CARD9` | `NO_GO` | Direction is not clean restoration; pathway normalization would need preserve antifungal immunity. | No CARD9-restoring target-selective modality. | Infectious-risk biology and no direct modality. |
| 11 | `SLC15A4` | `NO_GO` | Not restoration; pharmacology concept is inhibition. | SLC15A4 inhibitor chemistry exists publicly, but that is not restoration. | SLE-heavy/limited genetics and prior-demoted TLR/IRF branch. |
| 12 | `TYK2` | `NO_GO` | Not restoration; protective genetics/drugs support inhibition. | Approved/clinical TYK2 inhibitors. | Generic JAK/IFN comparator with direct autoimmune prior art. |
| 13 | `IRF5` | `NO_GO` | Not restoration; risk biology supports reducing IRF5 activation. | Current inhibitor/degrader programs exist. | Feasible inhibitor route, but not restoration and heavily crowded in lupus/TLR/IFN biology. |
| 14 | `IL6R` | `NO_GO` | Not restoration; genetics/drugs support IL-6R blockade. | Approved anti-IL6R biologics. | Fully prior-arted inhibitor/antagonist class; not restoration. |

Generated table:
`results_v3/wave23_genetics_restoration_modality/ranked_go_park_no_go.tsv`.

## Genetics and Direction Checks

OpenTargets credible-set breadth is strong for several genes:

- `SH2B3`: 10 diseases at score `>=0.5`
- `IRF5`: 9
- `PTPN2`: 8
- `ATG16L1`: 8
- `IL10`, `TNFAIP3`, `TYK2`, `CLEC16A`: 7 each
- `GPR65` and `IL6R`: 5 each
- `CARD9` and `OSMR`: 4 each

But Wave14 remains the controlling genetics caveat: these are locus-level
signals unless formal disease GWAS/cis-eQTL or pQTL coloc/MR is available. For
this scout, locus breadth supports prioritization only. It does not prove
target-level causality or direction.

Direction calls:

- Restoration-compatible: `PTPN2`, `TNFAIP3`, `SH2B3`, `CLEC16A`, `ATG16L1`,
  `GPR65`, `IL10`.
- Not clean restoration or context-dependent: `CARD9`.
- Inhibitor/blockade comparator, not restoration: `IRF5`, `IL6R`, `TYK2`,
  `OSMR`, `SLC15A4`, `TASL`.

## Perturbation Evidence

Local perturbation evidence does not rescue any restoration candidate.

- `TYK2` has Mixscale evidence, but it is broad IFN/JAK-like collapse and
  supports inhibitor-comparator biology, not restoration.
- `IRF5` Mixscale is null/wrong-direction locally.
- `PTPN2`, `TNFAIP3`, `SH2B3`, `CLEC16A`, `ATG16L1`, `GPR65`, `CARD9`, and
  `IL10` rely on Wave20 manual perturbation/context scores or literature
  biology, not a direct local restoration rescue assay.

The evidence matrix is written to
`results_v3/wave23_genetics_restoration_modality/local_restoration_evidence_matrix.tsv`.

## Candidate Notes

### `GPR65` PARK

This is the cleanest restoration-style modality class: a GPCR agonist or PAM can
in principle restore protective acidic-tissue sensing. Local genetics show 5
OpenTargets diseases at score `>=0.5` (`AS`, Crohn, MS, psoriasis, UC), but
local broad h5ad support is weak and contradictory: one positive disease and
two negative diseases in Wave20-derived metrics.

The route is also crowded. Public sources include a GPR65 experimental-colitis
target paper and a GPR65 modulator patent with autoimmune-disease language.
This remains `PARK`, not `GO`.

### `IL10` PARK

IL-10 restoration is biologically coherent and technically feasible as a
cytokine/agonist modality. The problem is novelty and selectivity: recombinant
IL-10 has direct Crohn/autoimmune prior art, and the local data do not define a
new responder compartment or cross-autoimmune biomarker delta. Localized or
matrix-targeted IL-10 is a speculative delivery improvement unless connected to
the V3 disease-cell data.

### `PTPN2`, `TNFAIP3`, `SH2B3` NO_GO

These are the strongest negative-regulator genetics anchors but also the most
important restoration kills.

- `PTPN2`: correct direction is TCPTP restoration. PTPN2/PTPN1 inhibitor
  precedent is oncology-directed and wrong for autoimmune restoration.
- `TNFAIP3`: A20 restoration is attractive, but local evidence shows no direct
  A20-restoring modality.
- `SH2B3`: very broad genetics, but LNK is an intracellular adaptor with no
  current restoration route and substantial hematopoietic/vascular pleiotropy.

All three fail the target-selective restoration gate.

### `CLEC16A`, `ATG16L1` NO_GO

These are the relevant autophagy/mitophagy restoration loci. Both fail for the
same practical reason: current autophagy/mitophagy modulation is indirect and
broad. It is not target-selective restoration in the disease compartment.

`CLEC16A` has the additional 16p13 locus ambiguity problem with neighboring
`CIITA`/`DEXI`/`SOCS1`. `ATG16L1` has plausible Crohn hypomorphic biology, but
no selective target-engagement package.

### `IRF5`, `TYK2`, `IL6R` NO_GO

These are not restoration targets in this scope.

- `IRF5`: inhibitor/degrader precedent is current and real, but it is not
  restoration and is crowded in lupus/TLR/IFN biology.
- `TYK2`: inhibitor precedent is approved/clinical and generic JAK/IFN-family.
- `IL6R`: approved antagonist biologics already occupy the autoimmune class.

They are useful positive controls for genetic tractability and modality
precedent, not Wave23 restoration opportunities.

### Local Additions

`OSMR`, `SLC15A4`, and `TASL` were included because local Wave20/Wave14 outputs
make them relevant comparators:

- `OSMR`: local OT support reaches four diseases, but the feasible modality is
  blockade and the route was already demoted as tissue-remodeling/IBD-heavy.
- `SLC15A4`/`TASL`: endolysosomal TLR/IRF branch comparators; the therapeutic
  concept is inhibition, not restoration, and genetics breadth is limited
  (`SLC15A4` SLE-only; `TASL` RA/SLE).

## Public Source Notes

Key public sources used for modality/prior-art interpretation:

- GPR65 experimental colitis/target rationale:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC8629932/>
- GPR65 modulator patent:
  <https://patents.google.com/patent/WO2023067322A1/en>
- PTPN2 autoimmune loss-of-function/restoration context:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC9456094/>
- PTPN2/PTPN1 inhibitor oncology precedent:
  <https://www.nature.com/articles/s41586-023-06575-7>
- A20/TNFAIP3 haploinsufficiency context:
  <https://www.ncbi.nlm.nih.gov/sites/books/NBK610430/>
- CLEC16A autoimmunity/mitophagy review:
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC10179542/>
- IRF5 inhibitor/degrader precedent:
  <https://www.hotspotthera.com/press_release/hotspot-therapeutics-presents-preclinical-data-from-small-molecule-irf5-inhibitor-program-at-15th-european-lupus-meeting/>
  and <https://investors.kymeratx.com/node/11946/pdf>
- Recombinant IL-10 Crohn trial:
  <https://pubmed.ncbi.nlm.nih.gov/11113068/>
- IL6R antagonist precedent:
  <https://www.accessdata.fda.gov/drugsatfda_docs/label/2024/125276s144%2C125472s056lbl.pdf>
- TYK2 inhibitor precedent:
  <https://www.fda.gov/drugs/drug-approvals-and-databases/drug-trials-snapshots-sotyktu>

## Files Written

- `scripts/v3_wave23_genetics_restoration_modality.py`
- `results_v3/wave23_genetics_restoration_modality/local_restoration_evidence_matrix.tsv`
- `results_v3/wave23_genetics_restoration_modality/ranked_go_park_no_go.tsv`
- `results_v3/wave23_genetics_restoration_modality/public_source_interpretation.tsv`
- `results_v3/wave23_genetics_restoration_modality/summary.json`
- `subagents_v3/wave23_genetics_restoration_modality.md`

