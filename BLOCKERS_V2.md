# Blockers And Downscopes V2

## Controlled Or Heavy Single-Cell Data

Several best-in-class cross-autoimmune single-cell datasets identified by β1 are not straightforward public matrix downloads:

- AMP RA synovium resources require Synapse/ImmPort style access paths.
- Lupus nephritis atlas resources were identified as ARK/Synapse-linked.
- Some psoriasis spatial/scRNA resources are available but would require additional large raw/scRNA processing beyond the current local environment.

Impact: cross-autoimmune evidence in this session relied heavily on accessible GEO processed bulk matrices plus one sorted-cell SLE dataset and one RA macrophage array dataset. This is enough to falsify a simple ACSL1 pan-autoimmune claim, but not enough to establish a new cell-resolved pan-autoimmune therapeutic target.

## T1D `GSE154609` Annotation

Downloaded `GSE154609_series_matrix.txt.gz`, a CD14+ monocyte dataset for type 1 diabetes. The platform `GPL17692` GEO annotation did not have a small `annot` file. The available SOFT file advertised as approximately `2.3 GB`; I started the download, recognized the silent compute/network escalation, stopped it, and removed the partial file.

Impact: T1D was not included in quantitative gene-level analysis. Rescuing this path requires a smaller platform annotation source, Bioconductor annotation package, or a preprocessed gene-symbol matrix.

## Docking / Structure-Based Screening

AlphaFold structures and UniProt/ChEMBL inventories were feasible. I did not run docking because:

- ACSL1 failed upstream biological gates before docking would be decisive.
- Docking against an AlphaFold model without ligand-bound ACSL1-family structures, membrane context, and isoform-selectivity validation would be a weak surrogate.

Impact: no docking score is reported or used.

## Genetic Colocalization / MR

Full colocalization/MR was not executed because the candidate direction changed during the session:

- ACSL1 failed incremental, simulation, and cross-disease recurrence gates before genetics could rescue it as a target.
- NAMPT is heavily prior-arted as an inflammatory target, so genetics would not solve novelty or therapeutic-direction problems.

Impact: no MR/colocalization evidence is claimed.
