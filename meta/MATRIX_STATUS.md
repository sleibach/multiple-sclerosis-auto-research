# MATRIX_STATUS

Last updated: 2026-06-06 00:05 CEST

Canonical machine-readable state: `analysis/v11_matrix/disagreement_matrix.tsv`.

## Summary

- Total qualifying supported disagreement cells: `10`.
- Non-unresolved cells: `10`.
- Completion: `100.0%`.
- `unresolved`: `0`.
- `biological`: `4`.
- `artifact`: `2`.
- `explained`: `0`.
- `intervention_derived`: `4`.

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

### 007_Crohn_disease_axis_01_ifn_apc_vs_axis_02_genetics

- Disease: `Crohn disease`.
- Axis A: `IFN/APC antigen-presentation state` = `near/supported`.
- Axis B: `genetic risk architecture` = `intermediate/supported`.
- Rank score: `1.5`.
- Status: `biological`.
- Resolution grade: `V12 supported downstream-convergence finding`.
- Last action: V15 worked up the V14 MS-Crohn chr10 shared SuSiE-coloc locus (`10:80542475-81559335`, max PP.H4 `0.958107919239886`). Credible-set intersection is four variants inside/near `ZMIZ1`; Crohn eQTL-coloc supports ZMIZ1 in blood, but no stored MS eQTL-coloc row was available and MS/Crohn aligned disease effects are opposite. This supports a genetics decoupling locus, not a transfer-ready shared treatment mechanism.
- Next action: Retrieve raw eQTLGen/GTEx summary statistics for the chr10 four-SNP credible set and run allele-aligned ZMIZ1 eQTL colocalization; then test ZMIZ1 perturbation in APC/myeloid models. See GENETICS_LOCI_WORKUP_V15.md.

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
- Status: `intervention_derived`.
- Resolution grade: `V12 supported genetics layer-decoupling finding`.
- Last action: V15 worked up the V14 MS-UC chr1 shared SuSiE-coloc locus (`1:200375242-201375897`, max PP.H4 `0.959324545654259`). Credible-set intersection is 11 variants near/overlapping `C1orf106/INAVA`, but stored QTL colocalization points most strongly to blood eQTLs for `GPR25` in both MS and UC. Direction proxies suggest concordant MS/UC risk-increasing GPR25 expression, but raw allele-aligned eQTL summary statistics were not rerun and cell-state/druggability support is weak.
- Next action: Retrieve raw eQTLGen/GTEx summary statistics for `GPR25`, `C1orf106/INAVA`, `KIF21B`, and `CACNA1S` around the chr1 credible set; run allele-aligned eQTL coloc before any therapeutic-direction claim. See GENETICS_LOCI_WORKUP_V15.md.

### 008_Crohn_disease_axis_02_genetics_vs_axis_07_treatment_response

- Disease: `Crohn disease`.
- Axis A: `genetic risk architecture` = `intermediate/supported`.
- Axis B: `treatment-response architecture` = `near/supported`.
- Rank score: `1.5`.
- Status: `intervention_derived`.
- Resolution grade: `V12 supported downstream-response convergence finding`.
- Last action: V15 added the chr10 `ZMIZ1` shared-locus workup. The locus supports a real MS-Crohn inherited-risk connection, but opposite MS/Crohn disease-effect signs and weak MS cell-state support mean it should not be interpreted as a Crohn-to-MS response-biomarker transfer locus.
- Next action: Add Crohn-only paired mucosal response cohorts and raw ZMIZ1 eQTL direction; preserve the downstream response-convergence claim as separate from the chr10 inherited-risk decoupling. See CROHN_GENETICS_RESPONSE_REPAIR_DECOUPLING_V12.md and GENETICS_LOCI_WORKUP_V15.md.

### 009_Crohn_disease_axis_02_genetics_vs_axis_08_tissue_repair_resolution

- Disease: `Crohn disease`.
- Axis A: `genetic risk architecture` = `intermediate/supported`.
- Axis B: `tissue repair and resolution biology` = `near/supported`.
- Rank score: `1.5`.
- Status: `intervention_derived`.
- Resolution grade: `V12 supported downstream-repair convergence finding`.
- Last action: V15 added the chr10 `ZMIZ1` shared-locus workup. The genetic locus is not a repair-transfer mechanism on current evidence; it is a decoupling locus with opposite MS/Crohn disease-effect signs.
- Next action: Upgrade repair axis using repair endpoints independent of IFN/APC delta; do not use chr10 ZMIZ1 as repair-transfer evidence unless perturbation or longitudinal repair data appears. See CROHN_GENETICS_RESPONSE_REPAIR_DECOUPLING_V12.md and GENETICS_LOCI_WORKUP_V15.md.
