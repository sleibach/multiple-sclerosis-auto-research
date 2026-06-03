# MATRIX_STATUS

Last updated: 2026-06-04 00:22 

Canonical machine-readable state: `analysis/v11_matrix/disagreement_matrix.tsv`.

## Summary

- Total qualifying supported disagreement cells: `10`.
- Non-unresolved cells: `6`.
- Completion: `60.0%`.
- `unresolved`: `4`.
- `biological`: `3`.
- `artifact`: `2`.
- `explained`: `0`.
- `intervention_derived`: `1`.

## Cells

### 005_rheumatoid_arthritis_axis_08_tissue_repair_resolution_vs_axis_09_sex_hormonal_pregnancy

- Disease: `rheumatoid arthritis`.
- Axis A: `tissue repair and resolution biology` = `far/supported`.
- Axis B: `sex, hormonal, and pregnancy modulation` = `near/supported`.
- Rank score: `3.75`.
- Status: `artifact`.
- Resolution grade: `V11 axis-scope correction`.
- Last action: V11 audit found the RA axis-08 far placement is supported mainly by blood anti-TNF response-monitoring failures, while synovial tissue repair remains under-tested. The pregnancy contrast remains valid only against blood response-monitoring, not global RA tissue repair.
- Next action: Rebuild RA tissue-repair axis with paired synovial tissue or validated synovial repair endpoints. See RA_TISSUE_REPAIR_PREGNANCY_SCOPE_AUDIT_V11.md.

### 010_ulcerative_colitis_axis_07_treatment_response_vs_axis_08_tissue_repair_resolution

- Disease: `ulcerative colitis`.
- Axis A: `treatment-response architecture` = `contradictory/supported`.
- Axis B: `tissue repair and resolution biology` = `near/supported`.
- Rank score: `0.78125`.
- Status: `artifact`.
- Resolution grade: `downgraded axis-design issue`.
- Last action: V10 hostile critique found high evidence overlap between treatment-response and tissue-repair axes; row downgraded by independence penalty.
- Next action: Rebuild tissue-repair axis with independent repair endpoints.

### 002_Sjogren_syndrome_axis_01_ifn_apc_vs_axis_04_lipid_lysosomal

- Disease: `Sjogren syndrome`.
- Axis A: `IFN/APC antigen-presentation state` = `near/supported`.
- Axis B: `lipid-lysosomal / foamy myeloid state` = `far/supported`.
- Rank score: `3.75`.
- Status: `biological`.
- Resolution grade: `Tier 1 candidate`.
- Last action: V10 matched salivary epithelial/APC audit plus GSE23117 bulk replication; sharpened to IFN/APC-positive versus lysosomal/APC-null, lipid-loader-negative component remains weaker.
- Next action: Find independent salivary single-cell/spatial APC replication for lipid-loader/foamy-myeloid component.

### 003_rheumatoid_arthritis_axis_01_ifn_apc_vs_axis_09_sex_hormonal_pregnancy

- Disease: `rheumatoid arthritis`.
- Axis A: `IFN/APC antigen-presentation state` = `far/supported`.
- Axis B: `sex, hormonal, and pregnancy modulation` = `near/supported`.
- Rank score: `3.75`.
- Status: `biological`.
- Resolution grade: `Tier 1 perturbation-class candidate`.
- Last action: V10 RA audit: blood IFN/APC negative/null while seropositive RA pregnancy shows late-pregnancy trough and postpartum rebound.
- Next action: Seek composition-adjusted RA/MS pregnancy data with monocyte/APC resolution.

### 004_rheumatoid_arthritis_axis_07_treatment_response_vs_axis_09_sex_hormonal_pregnancy

- Disease: `rheumatoid arthritis`.
- Axis A: `treatment-response architecture` = `far/supported`.
- Axis B: `sex, hormonal, and pregnancy modulation` = `near/supported`.
- Rank score: `3.75`.
- Status: `biological`.
- Resolution grade: `Tier 1 perturbation-class candidate`.
- Last action: V10 RA audit: RA anti-TNF blood APC response rules fail, but pregnancy immune-kinetic axis is near MS.
- Next action: Test whether pregnancy modules fail to rescue RA anti-TNF APC response in independent cohorts.

### 001_ulcerative_colitis_axis_01_ifn_apc_vs_axis_07_treatment_response

- Disease: `ulcerative colitis`.
- Axis A: `IFN/APC antigen-presentation state` = `near/robust`.
- Axis B: `treatment-response architecture` = `contradictory/supported`.
- Rank score: `3.955078125`.
- Status: `intervention_derived`.
- Resolution grade: `V11 transfer-validity finding`.
- Last action: V11 UC audit resolved cell as static-state versus dynamic-downshift decoupling. Cross-sectional colon myeloid IFN/APC is high, but baseline mucosal IFN/APC fails as a response predictor while early -delta IFN/APC passes in paired mucosal treatment cohorts.
- Next action: Use as MS transfer warning: test early compartment-relevant IFN/APC delta, not baseline IFN/APC height. See UC_STATIC_DYNAMIC_APC_DECOUPLING_V11.md.

### 006_ulcerative_colitis_axis_02_genetics_vs_axis_07_treatment_response

- Disease: `ulcerative colitis`.
- Axis A: `genetic risk architecture` = `near/supported`.
- Axis B: `treatment-response architecture` = `contradictory/supported`.
- Rank score: `3.75`.
- Status: `unresolved`.
- Resolution grade: ``.
- Last action: Imported from frozen V10 supported-only disagreement matrix.
- Next action: Run V11 artifact audit: compartment, cohort, measurement grade.

### 007_Crohn_disease_axis_01_ifn_apc_vs_axis_02_genetics

- Disease: `Crohn disease`.
- Axis A: `IFN/APC antigen-presentation state` = `near/supported`.
- Axis B: `genetic risk architecture` = `intermediate/supported`.
- Rank score: `1.5`.
- Status: `unresolved`.
- Resolution grade: ``.
- Last action: Imported from frozen V10 supported-only disagreement matrix.
- Next action: Run V11 artifact audit: compartment, cohort, measurement grade.

### 008_Crohn_disease_axis_02_genetics_vs_axis_07_treatment_response

- Disease: `Crohn disease`.
- Axis A: `genetic risk architecture` = `intermediate/supported`.
- Axis B: `treatment-response architecture` = `near/supported`.
- Rank score: `1.5`.
- Status: `unresolved`.
- Resolution grade: ``.
- Last action: Imported from frozen V10 supported-only disagreement matrix.
- Next action: Run V11 artifact audit: compartment, cohort, measurement grade.

### 009_Crohn_disease_axis_02_genetics_vs_axis_08_tissue_repair_resolution

- Disease: `Crohn disease`.
- Axis A: `genetic risk architecture` = `intermediate/supported`.
- Axis B: `tissue repair and resolution biology` = `near/supported`.
- Rank score: `1.5`.
- Status: `unresolved`.
- Resolution grade: ``.
- Last action: Imported from frozen V10 supported-only disagreement matrix.
- Next action: Run V11 artifact audit: compartment, cohort, measurement grade.
