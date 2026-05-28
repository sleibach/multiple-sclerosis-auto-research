# Wave21-B Residual Candidate Prior-Art Gate

Timestamp: 2026-05-27

## Scope

Hostile novelty/modality review for residual candidates named in
`CONVERGENCE_CHECK_5.md` plus strict-residual accessible extras from
`results_v3/broad_residual_gate/broad_residual_gate_summary.tsv`.

Reviewed named candidates: `ATOX1`, `SQLE`, `LDLRAD3`, `IL15`, `CD82`,
`PSME1`, `PSME2`, `POMP`, `IFITM2`, `IFITM3`.

Reviewed local extras because they had strict residual support plus an obvious
surface/secreted/enzyme/stress-modality route: `CFB`, `IL7R`, `CXCL8`,
`TIMP1`, `PDPN`, `HIF1A`, `PTPRE`, `C1QTNF1`.

## Output Files

- `results_v3/wave21_residual_candidate_prior_art/local_candidate_context.tsv`
- `results_v3/wave21_residual_candidate_prior_art/external_query_log.tsv`
- `results_v3/wave21_residual_candidate_prior_art/api_hit_summary.tsv`
- `results_v3/wave21_residual_candidate_prior_art/candidate_prior_art_gate.tsv`
- `results_v3/wave21_residual_candidate_prior_art/raw_api/`

`external_query_log.tsv` has 126 source rows, with exact query strings, search
URLs, API URLs, raw-file paths, counts/signals, and top hits for PubMed, Europe
PMC, Europe PMC preprints, ClinicalTrials.gov, Google Patents, ChEMBL, and
UniProt.

## Gate Summary

No candidate should be promoted from this review. This is a gate-evidence
return only, not a final therapeutic finding.

The hard blockers are:

- `IL15`, `CFB`, `IL7R`, `CXCL8`, and `HIF1A` have real modality, but the route
  is already clinically/patent saturated or generic.
- `PSME1/2`, `POMP`, and `IFITM2/3` are generic IFN/proteasome/antiviral or
  core-machinery biology.
- `ATOX1`, `LDLRAD3`, `CD82`, `TIMP1`, `PDPN`, `PTPRE`, and `C1QTNF1` lack a
  clean intervention direction or mature autoimmune-ready modality.
- `SQLE` is the closest small-molecule residual enzyme, but current support is
  IBD/stromal-skewed, MS-negative, sterol-repair-confounded, and heavily
  prior-arted outside this V3 biology.

## Local Gate Readout

The named candidates split into two groups:

- Strict residual but IBD/stromal-skewed: `ATOX1`, `SQLE`, `LDLRAD3`.
- Broad expression but no strict-core residual survival: `IL15`, `CD82`,
  `PSME1`, `PSME2`, `POMP`, `IFITM2`, `IFITM3`.

The local extras with at least one strict-core residual disease were mostly
single-disease strict survivors. `CFB`, `IL7R`, `CXCL8`, `TIMP1`, `PDPN`,
`PTPRE` are UC or Crohn skewed; `HIF1A` and `C1QTNF1` survive only in Crohn/UC
stromal contexts. None adds a convincing MS anchor.

## External Evidence Highlights

- `IL15`: PubMed query returned 2335 hits and Europe PMC 38993 hits. Clinical
  precedent includes AMG 714/PRV-015 in celiac disease
  (`NCT02637141`, PubMed `31494096`). The direct intervention direction is
  blockade, but novelty and systemic NK/T-cell safety are blocking.
- `CFB`: ChEMBL target `CHEMBL5731` returned 873 activity records. Iptacopan
  / LNP023 is in `NCT04578834` for IgA nephropathy, and Google Patents has
  factor B inhibitor method claims such as `WO2024176169A1`. This is a
  druggable comparator, not a novel residual target.
- `IL7R`: anti-IL-7R alpha/CD127 blockade is already in UC clinical prior art
  via lusvertikimab/OSE-127 (`NCT04882007`). Local strict residual support is
  only UC stromal.
- `CXCL8`: ChEMBL target `CHEMBL2157` returned 726 activity records. IL-8 /
  CXCR1/2 blockade is generic neutrophil inflammatory biology with wound-healing
  and host-defense risk.
- `SQLE`: ChEMBL target `CHEMBL3592` returned 100 activity records. Google
  Patents contains long-standing SQLE inhibitor art, including `EP0448934A3`,
  and newer oncology SQLE inhibitor applications. Direction is confounded by
  sterol synthesis and epithelial/stromal repair.
- `PSME1/2` and `POMP`: UniProt places these in immunoproteasome/proteasome
  assembly biology. POMP-related immune dysregulation/PRAID (`PMID 29805043`)
  is a safety warning. Immunoproteasome inhibitor autoimmunity prior art
  (`PMID 29034459`) blocks novelty for the whole route.
- `LDLRAD3`: literature is sparse for autoimmunity and points instead to APP
  processing and Venezuelan equine encephalitis virus receptor biology
  (`PMID 34646021`), creating CNS/viral-entry liabilities.
- `IFITM2/3`: UniProt calls these IFN-induced antiviral restriction factors.
  No ChEMBL target hit was found. Inhibition would directly trade against viral
  host defense.

## Recommendations

No immediate orchestrator follow-up is justified for a target-promotion track.

Comparator-only uses:

- `CFB`, `IL15`, `IL7R`, `CXCL8`, and `HIF1A` are useful as positive controls
  for "druggable but prior-art/generic" failures.
- `SQLE` can be parked as a conditional stress test only if Wave21-A finds
  independent non-IBD residual support and perturbation evidence for local,
  safe suppression.
- `PSME1/2`, `POMP`, and `IFITM2/3` should be treated as demotion controls for
  proteasome/IFN machinery.

## Source Links

- Full exact query log: `results_v3/wave21_residual_candidate_prior_art/external_query_log.tsv`
- UniProt examples: `ATOX1` https://www.uniprot.org/uniprotkb/O00244/entry,
  `IL15` https://www.uniprot.org/uniprotkb/P40933/entry,
  `CFB` https://www.uniprot.org/uniprotkb/P00751/entry,
  `IFITM3` https://www.uniprot.org/uniprotkb/Q01628/entry
- ChEMBL examples: `SQLE` https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3592/,
  `IL15` https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3712954/,
  `CFB` https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL5731/,
  `CXCL8` https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL2157/
- ClinicalTrials.gov examples: AMG 714 celiac disease
  https://clinicaltrials.gov/study/NCT02637141, iptacopan IgA nephropathy
  https://clinicaltrials.gov/study/NCT04578834, lusvertikimab UC
  https://clinicaltrials.gov/study/NCT04882007, EZN-2968 HIF1A
  https://clinicaltrials.gov/study/NCT01120288
- Google Patents examples: SQLE inhibitor
  https://patents.google.com/patent/EP0448934A3/en, factor B inhibitor
  https://patents.google.com/patent/WO2024176169A1/en
