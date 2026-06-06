# Wave66-A metabolomics access scout

Scout role only. I do not claim a therapeutic finding here. I checked programmatic access paths for the Metabolomics Workbench studies prioritized by Wave64-B on 2026-05-27.

## Common access pattern

Metabolomics Workbench REST documentation page: `https://www.metabolomicsworkbench.org/tools/mw_rest.php`

For most named-metabolite studies, the useful no-auth endpoints are:

- Study summary: `https://www.metabolomicsworkbench.org/rest/study/study_id/<STUDY_ID>/summary`
- Sample factors: `https://www.metabolomicsworkbench.org/rest/study/study_id/<STUDY_ID>/factors`
- Analysis metadata: `https://www.metabolomicsworkbench.org/rest/study/study_id/<STUDY_ID>/analysis`
- Metabolite/sample counts: `https://www.metabolomicsworkbench.org/rest/study/study_id/<STUDY_ID>/number_of_metabolites`
- Sample-level matrix: `https://www.metabolomicsworkbench.org/rest/study/analysis_id/<ANALYSIS_ID>/datatable/`
- Download version of same matrix: `https://www.metabolomicsworkbench.org/rest/study/analysis_id/<ANALYSIS_ID>/datatable/file`
- mwTab metadata: `https://www.metabolomicsworkbench.org/rest/study/analysis_id/<ANALYSIS_ID>/mwtab/txt`

Important exception: TEDDY studies `ST001636` and `ST001386` do not expose the actual feature matrix through `datatable`; that endpoint returns only `Samples` and `Class`. Use:

- Untargeted matrix: `https://www.metabolomicsworkbench.org/rest/study/analysis_id/<ANALYSIS_ID>/untarg_data/`
- Untargeted factor counts: `https://www.metabolomicsworkbench.org/rest/study/analysis_id/<ANALYSIS_ID>/untarg_factors/`

For `datatable/file`, the HTTP `Content-Disposition` filename is generically `download.txt`. For `untarg_data`, it is `untarg_data.txt`.

## Promotion criterion

Promotion criterion is met for access scouting: at least three autoimmune diseases have downloadable individual-level feature matrices, sample metadata, and interpretable disease/control or tissue-state contrasts.

Best immediately usable contrasts:

- RA: `ST001949`, `Condition:Control`, `Condition:RA`, `Condition:RA+MTX`
- IBD: `ST000899`, `Type:Control`, `Type:Crohn disease`, `Type:Ulcerative Colitis`
- Ankylosing spondylitis: `ST002949`, `Treatment:Ankylosing Spondylitis`, `Treatment:healthy control`
- Type 1 diabetes: `ST000422`, `treatment:ND`, `treatment:T1D good glycemic control`
- Psoriasis: `ST000298`, `Psoriasis Status:Normal`, `Psoriasis involved`, `Psoriasis uninvolved`, but n=3/group only
- MS model: `ST003328`, `Disease status:AMC/PMS` and `Treatment:SV/untreated`, but in induced neural stem cells, not patient biofluid or immune tissue

## Study-level audit

### ST001949 - rheumatoid arthritis / methotrexate plasma metabolomics

- Study page: `https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST001949`
- Summary endpoint: `https://www.metabolomicsworkbench.org/rest/study/study_id/ST001949/summary`
- Factors endpoint: `https://www.metabolomicsworkbench.org/rest/study/study_id/ST001949/factors`
- Analysis endpoint: `https://www.metabolomicsworkbench.org/rest/study/study_id/ST001949/analysis`
- Analysis ID: `AN003173`, GC positive ion mode
- Matrix endpoint: `https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN003173/datatable/`
- Download endpoint: `https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN003173/datatable/file`
- mwTab: `https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN003173/mwtab/txt`
- Access status: no-auth sample-level processed matrix and metadata available.
- Visible sample labels: `Condition:Control` n=20, `Condition:RA` n=20, `Condition:RA+MTX` n=20.
- Sample source: blood plasma, n=60.
- Observed matrix features from header: 648.
- Harmonization traps: GC-MS primary-metabolite style data, not lipidomics; `RA+MTX` is a group label and the factors endpoint did not expose subject pairing, so do not treat this as paired pre/post without additional metadata. `number_of_metabolites` had blank `num_metabolites`; header count must be used.
- Scout call: promote for RA disease/control/treatment-group contrast, not as a paired MTX response dataset.

### ST000899 - Crohn disease / ulcerative colitis / control serum

- Study page: `https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST000899`
- Summary/factors/analysis endpoints follow the common pattern.
- Analysis IDs:
  - `AN001462`, reversed-phase positive, matrix `.../AN001462/datatable/`, 160 features
  - `AN001463`, HILIC positive, matrix `.../AN001463/datatable/`, 131 features
  - `AN001464`, reversed-phase negative, matrix `.../AN001464/datatable/`, 311 features
  - `AN001465`, HILIC negative, matrix `.../AN001465/datatable/`, 69 features
- Access status: no-auth sample-level processed matrices and metadata available.
- Visible sample labels: `Type:Control` n=20, `Type:Crohn disease` n=20, `Type:Ulcerative Colitis` n=20.
- Sample source: blood, n=60.
- Harmonization traps: four ion/chromatography modes should be treated as separate assays until duplicate metabolites/adducts are reconciled; lipid names mix shorthand and named metabolites; some GPC/GPE ether/plasmalogen nomenclature will need RefMet/LipidMaps normalization.
- Scout call: promote strongly for IBD case/control cross-disease lipid/metabolite analysis.

### ST002470 - IBD pediatric plasma longitudinal/severity profiling

- Study page: `https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST002470`
- Summary/factors/analysis endpoints follow the common pattern.
- Analysis IDs:
  - `AN004029`, HILIC positive, matrix `.../AN004029/datatable/`, 290 features
  - `AN004030`, reversed-phase positive, matrix `.../AN004030/datatable/`, 224 features
  - `AN004031`, HILIC negative, matrix `.../AN004031/datatable/`, 111 features
  - `AN004032`, reversed-phase negative, matrix `.../AN004032/datatable/`, 103 features
- Access status: no-auth sample-level processed matrices and metadata available.
- Visible sample labels from factors: `collectionWeek:0` n=34, `collectionWeek:4` n=27, `collectionWeek:12` n=24, `collectionWeek:52` n=4; `PUCAI_C3_WKall:inactive` n=34, `mild` n=25, `moderate/severe` n=30.
- Sample source: blood plasma, n=89. Raw file names are present in the factors endpoint for all 89 samples.
- Harmonization traps: no healthy-control factor was visible; disease activity and collection week are crossed, but subject IDs/pairing are not explicit in the factors endpoint. Use as severity/timepoint dataset only after resolving repeated-measure structure from local sample IDs or raw metadata. Some features are diet/drug/exposure metabolites and internal standards.
- Scout call: conditional; useful for IBD severity/longitudinal validation, not a clean case/control contrast.

### ST002732 - systemic lupus erythematosus plasma lipids and coronary artery calcification

- Study page: `https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST002732`
- Summary/factors/analysis endpoints follow the common pattern.
- Analysis IDs:
  - `AN004429`, HILIC positive, matrix `.../AN004429/datatable/`, 105 features, ceramide-heavy
  - `AN004430`, HILIC positive, matrix `.../AN004430/datatable/`, 39 features, PC/SM-heavy
- Access status: no-auth sample-level processed matrices and metadata available.
- Visible sample labels: `Group:Null` n=140, `Group:Med` n=47, `Group:High` n=20.
- Sample source: blood plasma, n=207. Raw file names present in factors endpoint.
- Harmonization traps: labels are severity/risk strata, not SLE-vs-control. The title indicates coronary artery calcification in women with SLE, so `Null/Med/High` should not be reinterpreted as autoimmune disease status. Excellent lipid-class relevance, weak for cross-autoimmune case/control unless the analysis question is lipid association with vascular/severity phenotype inside SLE.
- Scout call: promote for within-SLE lipid severity axis; demote for disease/control promotion criterion.

### ST002949 - ankylosing spondylitis serum metabolomics

- Study page: `https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST002949`
- Summary/factors/analysis endpoints follow the common pattern.
- Analysis IDs:
  - `AN004836`, reversed-phase positive, matrix `.../AN004836/datatable/`, 20 features
  - `AN004837`, reversed-phase negative, matrix `.../AN004837/datatable/`, 6 features
- Access status: no-auth sample-level processed matrices and metadata available.
- Visible sample labels: `Treatment:Ankylosing Spondylitis` n=134, `Treatment:healthy control` n=134.
- Sample source: blood serum, n=268. Raw mzML names present in factors endpoint.
- Harmonization traps: only 26 named features total across the two matrices, so class-level lipid analysis will be low-dimensional. Some text encoding is messy in feature names, for example `(plus/minus)-Tryptophan`; clean names before RefMet matching.
- Scout call: promote for AS disease/control, but expect limited lipid-class breadth.

### ST001636 - TEDDY lipidomics study

- Study page: `https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST001636`
- Summary endpoint: `https://www.metabolomicsworkbench.org/rest/study/study_id/ST001636/summary`
- Analysis endpoint: `https://www.metabolomicsworkbench.org/rest/study/study_id/ST001636/analysis`
- Metadata page shows factor columns `Sex` and `cc`; page reports 11,560 samples.
- Analysis IDs:
  - `AN002673`, reversed-phase positive
  - `AN002674`, reversed-phase negative
- Correct matrix endpoints:
  - `https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN002673/untarg_data/`, 540 features
  - `https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN002674/untarg_data/`, 444 features
- Factor-count endpoints:
  - `https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN002673/untarg_factors/`
  - `https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN002674/untarg_factors/`
- Do not use for matrix:
  - `https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN002673/datatable/`
  - `https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN002674/datatable/`
  These returned only `Samples` and `Class`, no feature columns.
- Access status: no-auth untargeted sample-level matrices available; sample-level labels are embedded as `Samples` and `group`.
- Visible group counts from `untarg_factors`:
  - `AN002673`: Female cc1=818, cc2=405, cc3=338, cc4=1742, cc5=353, cc6=1776; Male cc1=741, cc2=319, cc3=663, cc4=1730, cc5=421, cc6=2241.
  - `AN002674`: Female cc1=820, cc2=405, cc3=338, cc4=1742, cc5=355, cc6=1775; Male cc1=741, cc2=318, cc3=663, cc4=1734, cc5=420, cc6=2243.
- Harmonization traps: `cc` values 1-6 are not self-describing in the accessible matrix/factor endpoints. The study page says this is a 1:3 matched TEDDY case-control design and says the study-design variables are explained in a data dictionary in the raw-data download section, but I did not resolve a direct raw-data/data-dictionary file URL in this scout. Internal standards are included as features in `untarg_data`; remove `iSTD` columns before biological class analysis. Analysis-specific sample counts from `untarg_factors` do not exactly equal 11,560, consistent with QC removal.
- Scout call: conditional. Promote as high-value T1D lipidomics only after mapping `cc` values to clinical case/control/autoantibody states from the data dictionary.

### ST001386 - TEDDY primary metabolomics study

- Study page: `https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST001386`
- Summary endpoint: `https://www.metabolomicsworkbench.org/rest/study/study_id/ST001386/summary`
- Analysis endpoint: `https://www.metabolomicsworkbench.org/rest/study/study_id/ST001386/analysis`
- Analysis ID: `AN002314`, GC-MS data.
- Correct matrix endpoint: `https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN002314/untarg_data/`, 144 features.
- Factor-count endpoint: `https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN002314/untarg_factors/`
- Do not use for matrix: `https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN002314/datatable/`, which returned only `Samples` and `Class`.
- Access status: no-auth untargeted sample-level matrix available.
- Visible group counts from `untarg_factors`: Female cc1=820, cc2=404, cc3=339, cc4=1742, cc5=355, cc6=1777; Male cc1=741, cc2=319, cc3=664, cc4=1735, cc5=421, cc6=2243.
- Sample source: plasma, n=11,560 from summary.
- Harmonization traps: same `cc` ambiguity as `ST001636`; metabolite matrix is primary metabolites, not lipidomics; study page notes 144 named metabolites and 221 unidentified compounds in BinBase, but `untarg_data` header exposes 144 features. Do not use as interpretable disease/control without the data dictionary.
- Scout call: conditional/demote for immediate cross-disease disease-control analysis; keep as TEDDY covariate/replication source after resolving `cc`.

### ST000422 - type 1 diabetes good glycemic control and controls

- Study page: `https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST000422`
- Summary/factors/analysis endpoints follow the common pattern.
- Analysis IDs:
  - `AN000667`, HILIC positive, matrix `.../AN000667/datatable/`, observed header 552 features
  - `AN000668`, HILIC negative, matrix `.../AN000668/datatable/`, observed header 397 features
  - `AN000669`, reversed-phase positive, matrix `.../AN000669/datatable/`, observed header 916 features
  - `AN000670`, reversed-phase negative, matrix `.../AN000670/datatable/`, observed header 259 features
- Access status: no-auth sample-level processed matrices and metadata available.
- Visible sample labels: `treatment:ND` n=90, `treatment:T1D good glycemic control` n=90.
- Sample source: blood plasma, n=180.
- Harmonization traps: Workbench `number_of_metabolites` reports larger counts than observed matrix headers for these analyses, so use actual downloaded header columns for analysis. Many feature identifiers include retention-time/adduct-like suffixes such as `compound + 0.81928736`, duplicate features, xenobiotics, and poorly classifiable names; class-level lipid aggregation needs aggressive ID filtering and cannot be treated as fully named lipidomics.
- Scout call: promote for T1D-vs-control, but with strict feature-quality filtering.

### ST003328 - progressive MS induced neural stem cell lipidomics

- Study page: `https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST003328`
- Summary/factors/analysis endpoints follow the common pattern.
- Analysis IDs:
  - `AN005452`, reversed-phase negative, matrix `.../AN005452/datatable/`, 217 features
  - `AN005453`, reversed-phase positive, matrix `.../AN005453/datatable/`, 425 features
- Access status: no-auth sample-level processed matrices and metadata available.
- Visible sample labels: `Disease status:PMS` n=24, `Disease status:AMC` n=18; `Treatment:SV` n=21, `Treatment:untreated` n=21.
- Sample source: induced neural stem cell, n=42. Raw names present in factors endpoint.
- Harmonization traps: this is a cellular MS model, not patient plasma/CSF/lesion tissue and not myeloid. `Disease status` and `Treatment` are crossed; analysis must model both. Feature naming is lipidomics-friendly but uses shorthand such as `Cer(d18:1_16:0)`, `CL(...)`, `ChE(...)`, `FA(...)`; normalize separately from RefMet-style named metabolites.
- Scout call: promote as MS lipid-metabolism model validation, not as systemic autoimmune-metabolomics evidence.

### ST000298 - psoriasis biopsy steroid metabolites

- Study page: `https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST000298`
- Summary/factors/analysis endpoints follow the common pattern.
- Analysis ID: `AN000476`, MS of steroids.
- Matrix endpoint: `https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN000476/datatable/`
- Download endpoint: `https://www.metabolomicsworkbench.org/rest/study/analysis_id/AN000476/datatable/file`
- Access status: no-auth sample-level processed matrix and metadata available.
- Visible sample labels: `Psoriasis Status:Normal` n=3, `Psoriasis Status:Psoriasis involved` n=3, `Psoriasis Status:Psoriasis uninvolved` n=3.
- Sample source: biopsy, n=9.
- Observed matrix features: 9 steroid metabolites.
- Harmonization traps: tiny n=3/group; targeted steroid panel, not lipid-lysosomal or broad lipidomics; lesion/nonlesion/normal labels may be paired by donor, but donor pairing was not exposed in the factor labels I checked.
- Scout call: demote for discovery, keep only as a weak psoriasis tissue-state sanity check.

## Cross-study harmonization traps

- Matrix endpoint choice is study-specific. Use `datatable` for named-metabolite matrices, but use `untarg_data` for TEDDY `ST001636` and `ST001386`.
- Class labels are stored as a single `Class` or `group` string and may contain multiple factors separated by `|`; parse into separate columns before modeling.
- Ion-mode/platform split is real. Do not concatenate positive/negative/HILIC/reversed-phase assays before duplicate/adduct resolution.
- Internal standards and QC-like features are present in `untarg_data` and in some named matrices; remove `iSTD`, obvious standards, and non-biological features before class-level analysis.
- RefMet matching will be uneven. Lipid shorthand (`PC(34:1)`, `Cer(d18:1_16:0)`), older GPC/GPE notation, exact chain notation, and adduct/retention suffixes need separate normalization rules.
- Some studies are not clean disease/control: `ST002732` is within-SLE calcification strata; `ST002470` is IBD activity/timepoint; TEDDY `cc` codes require data-dictionary resolution.
- Study designs span plasma, serum, biopsy, and induced neural stem cells. A cross-autoimmune metabolomics meta-analysis should use within-study standardized class scores, not raw intensity comparison across studies.

## Recommended next use

For an immediate cross-autoimmune class-level test, start with:

1. `ST000899` IBD: strongest clean case/control and mixed lipid/metabolite breadth.
2. `ST000422` T1D: clean ND-vs-T1D labels, but strict feature QC required.
3. `ST001949` RA: clean RA/control/RA+MTX labels, primary-metabolite biased.
4. `ST002949` AS: clean disease/control but low feature count.
5. `ST003328` MS model: lipid-rich MS mechanistic anchor, but cellular model rather than patient systemic disease.

Use `ST002732` as SLE lipid severity validation and `ST002470` as IBD activity/longitudinal validation after resolving repeated-measure structure. Use TEDDY only after mapping `cc` values from the raw-data dictionary.
