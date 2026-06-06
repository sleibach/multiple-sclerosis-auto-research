# Wave146 Architecture-First Barrier/Retention Scan

Branch call: `NO_ARCHITECTURE_FIRST_BARRIER_RETENTION_TARGET`.

Decision table:

| module | source_disease_positive_count | paired_receiver_positive_count | ms_anchor_pass | direct_prior_or_comparator_block | passes_architecture_gate |
| --- | --- | --- | --- | --- | --- |
| endothelial_entry | 2 | 0 | False | False | False |
| stromal_retention_fibrosis | 3 | 0 | True | False | False |
| epithelial_chemokine_entry | 3 | 0 | False | True | False |
| tls_lymphoid_niche | 1 | 1 | False | False | False |
| tl1a_comparator | 1 | 0 | False | True | False |

Interpretation:
- This scan is architecture-first: predefined tissue-interface modules, not lipid/APC target rows.
- A module must be disease-up in at least three source compartments, predict paired myeloid/APC receiver state in at least two diseases, and have an MS white-matter anchor.
- Comparator modules with direct crowded prior art are not promotable even if biologically recurrent.
