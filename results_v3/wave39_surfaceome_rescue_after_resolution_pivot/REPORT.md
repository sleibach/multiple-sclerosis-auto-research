# Wave39 Surfaceome Rescue After Resolution Pivot

## Question

After the resolution/efferocytosis branch failed, can any broad cross-autoimmune surface, secreted, extracellular, or enzyme-accessible candidate survive therapeutic gates?

## Scale

- Candidate pool from broad h5ad recurrence: 224 genes.
- UniProt accessibility queried: 224 genes.
- ChEMBL target/activity queried: 90 genes.
- Europe PMC and ClinicalTrials.gov prior-art counts queried: 60 genes.
- Calls: {"NO_GO_SURFACEOME_RESCUE": 218, "PARK_REVIEW": 6}.

## Result

- `GO_REVIEW`: none.
- `PARK_REVIEW`: MMP7, CD82, FXYD5, SCD, CCL20, IL23A.

Top-ranked rows are in `surfaceome_rescue_rank.tsv`. This scan is a no-go
unless a row survives breadth, MS-anchor, accessibility, modality, direction,
and non-crowded prior-art gates together.

## Top Rows

- `P4HB`: NO_GO_SURFACEOME_RESCUE, score=16.50; breadth=4, MS_anchor=False, accessible=True; insufficient_breadth; no_ms_anchor; reachable protein class by UniProt location/features; ChEMBL exact target found; ChEMBL activity records: 702
- `PIK3R2`: NO_GO_SURFACEOME_RESCUE, score=14.50; breadth=4, MS_anchor=False, accessible=False; insufficient_breadth; no_ms_anchor; not_surface_secreted_extracellular_by_uniprot; ChEMBL exact target found; ChEMBL activity records: 1781
- `PPIA`: NO_GO_SURFACEOME_RESCUE, score=14.00; breadth=5, MS_anchor=False, accessible=True; no_ms_anchor; prior_demoted_or_class_blocked; core_machinery_or_hla_marker; reachable protein class by UniProt location/features; ChEMBL exact target found; ChEMBL activity records: 646
- `HLA-DMA`: NO_GO_SURFACEOME_RESCUE, score=13.75; breadth=4, MS_anchor=False, accessible=True; insufficient_breadth; no_ms_anchor; core_machinery_or_hla_marker; reachable protein class by UniProt location/features; Wave15 residual state support in 7 diseases
- `HLA-DRA`: NO_GO_SURFACEOME_RESCUE, score=13.75; breadth=3, MS_anchor=True, accessible=True; insufficient_breadth; core_machinery_or_hla_marker; reachable protein class by UniProt location/features; Wave15 residual state support in 7 diseases
- `APOL1`: NO_GO_SURFACEOME_RESCUE, score=13.50; breadth=4, MS_anchor=False, accessible=True; insufficient_breadth; no_ms_anchor; reachable protein class by UniProt location/features; ChEMBL exact target found; ChEMBL activity records: 593
- `METAP1`: NO_GO_SURFACEOME_RESCUE, score=13.42; breadth=4, MS_anchor=False, accessible=False; insufficient_breadth; no_ms_anchor; not_surface_secreted_extracellular_by_uniprot; ChEMBL exact target found; ChEMBL activity records: 392
- `HLA-DMB`: NO_GO_SURFACEOME_RESCUE, score=13.25; breadth=4, MS_anchor=False, accessible=True; insufficient_breadth; no_ms_anchor; core_machinery_or_hla_marker; reachable protein class by UniProt location/features; Wave15 residual state support in 7 diseases
- `PKM`: NO_GO_SURFACEOME_RESCUE, score=13.00; breadth=4, MS_anchor=False, accessible=False; insufficient_breadth; no_ms_anchor; not_surface_secreted_extracellular_by_uniprot; ChEMBL exact target found; ChEMBL activity records: 14174
- `CTSC`: NO_GO_SURFACEOME_RESCUE, score=13.00; breadth=4, MS_anchor=False, accessible=False; insufficient_breadth; no_ms_anchor; not_surface_secreted_extracellular_by_uniprot; directional_negative_disease_signal; ChEMBL exact target found; ChEMBL activity records: 2383
- `RAB11A`: NO_GO_SURFACEOME_RESCUE, score=12.75; breadth=4, MS_anchor=False, accessible=True; insufficient_breadth; no_ms_anchor; surface_state_confounder_dominant; reachable protein class by UniProt location/features; ChEMBL exact target found; Wave15 residual state support in 5 diseases
- `LAPTM5`: NO_GO_SURFACEOME_RESCUE, score=12.25; breadth=3, MS_anchor=True, accessible=True; insufficient_breadth; reachable protein class by UniProt location/features; Wave15 residual state support in 6 diseases
