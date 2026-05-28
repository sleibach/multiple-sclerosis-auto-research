# Wave41 L1000 External Unknown Deconvolution

## Result

The only Wave27 external-lookup survivor, BRD-A72180425/K784-3188, resolves to PubChem CID 3689416 and ChEMBL CHEMBL1472126, an ML162 analog/RAS-selective-lethal probe-family compound. Public target and mechanism resources do not provide a selective autoimmune target; the compound has a single L1000 opposite query and cytotoxic electrophile-probe context. The perturbation-first repurposing branch therefore remains closed.

## Candidate Calls

| pert_id | lincs_cmap_name | compound_aliases | pubchem_cid | chembl_id | n_opposite_queries | wave41_call | promotion_allowed | resolved_identity | no_go_reasons |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BRD-A72180425 | K784-3188 | K-784-3188 | 3689416 | CHEMBL1472126 | 1 | NO_GO_CYTOTOXIC_PROBE_ANALOG | False | CHEMBL1472126 / PubChem CID 3689416 / ML162 analog-like Broad probe SAR member | single L1000 opposite-query hit, no recurrence across module signatures \| no approved or clinical-phase ChEMBL development status \| ChEMBL mechanism endpoint has zero target-mechanism records \| L1000FWD DMOA report lists known MOA and target(s) as Unknown \| NCBI Bookshelf places BRD-A72180425 in ML162/RAS-selective-lethal probe SAR, not autoimmune therapeutics \| contains chloroacetamide-like electrophile motif consistent with reactive/cytotoxic probe chemistry |

## External Evidence

- PubChem, ChEMBL, Europe PMC, ClinicalTrials.gov, L1000FWD DMOA, and NCBI Bookshelf calls are cached in `raw_api/` and enumerated in `api_call_log.tsv`.
- ChEMBL target activities are summarized in `chembl_target_activity_summary.tsv`; ChEMBL mechanism records were required for target promotion and were absent for this molecule.
- NCBI Bookshelf Table 2 places BRD-A72180425 in the ML162 SAR table for RAS-selective lethal probe development.

