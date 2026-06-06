# DATA_TIER3_DOWNLOAD_INSTRUCTIONS

Date: 2026-06-06

These sources cannot be self-acquired by the agent. They require a human
researcher, institutional account, signing official, controlled-access portal,
or manual download. Controlled individual-level genetic, CSF, or clinical data
may carry legal and ethics restrictions; consult institutional data-protection
and IRB/ethics processes before placing files in this sandbox.

## Highest-Leverage Tier 3 Sources

### 1. OneK1K Individual-Level Genotype/Single-Cell Data

Purpose:

- Resolve whether the chr1 protective haplotype affects `GPR25` or `KIF21B` in
  specific immune-cell subsets beyond public top-eQTL summaries.

Current open status:

- Public OneK1K top eQTL summaries were acquired in V18 from Zenodo.
- GEO `GSE196830` exposes `GSE196830_RAW.tar`, but it is `13,459,619,840`
  bytes and was not downloaded in V18 because public top-eQTL summaries already
  covered the immediate smoke test. It may contain raw scRNA material, but the
  genotype-level access needed for new eQTL mapping should be verified before a
  13.46 GB download.

Human action:

1. Inspect the OneK1K publication/data-availability statement and GEO
   `GSE196830` supplementary tar contents.
2. Confirm whether genotype dosage files or individual-level genotype metadata
   are public or controlled.
3. If controlled, follow the cited repository/portal instructions from the
   publication or GEO record.

Place files here:

- `data/raw/onek1k_individual_level/`
- Suggested naming:
  - `genotypes/`
  - `cell_metadata/`
  - `expression/`
  - `README_ACCESS_TERMS.txt`

After placement, the agent will run:

```bash
find data/raw/onek1k_individual_level -type f -print0 | xargs -0 sha256sum > data/raw/onek1k_individual_level/SHA256SUMS
```

Priority: highest if individual-level genotypes are available. This is the most
direct route to genotype-linked immune-cell expression for `GPR25` versus
`KIF21B`.

### 2. DICE Controlled Individual-Level Data

Portal:

- dbGaP, linked from the DICE download page as `phs001703.v3.p1`.

Purpose:

- DICE public significant eQTLs and mean expression were acquired in V18.
- Controlled individual-level expression/genotype could allow custom chr1
  locus tests, genotype-linked expression, and subset-specific checks not
  limited to significant public VCF entries.

Human action:

1. Log in to dbGaP with an authorized NIH/eRA Commons account.
2. Navigate to study `phs001703.v3.p1`.
3. Submit a data-access request for immune-cell genotype/expression data.
4. Expect institutional signing official approval and data-use certification.
5. Confirm whether reanalysis for autoimmune/MS genetic mechanism work is
   compatible with the study's data-use limitations.

Place files here:

- `data/raw/dice_controlled_phs001703/`
- Include:
  - genotype dosage/VCF files;
  - sample metadata;
  - cell-type expression matrices;
  - dbGaP data-use terms as `README_ACCESS_TERMS.txt`.

Priority: high. Public DICE already shows `KIF21B` expression and one NK-cell
significant eQTL; controlled individual-level data would test whether `GPR25`
has non-significant but genotype-linked effects in the relevant subsets.

### 3. MS CSF/PBMC Single-Cell Plus Genotype Cohorts

Purpose:

- Directly test the V17 decisive question in disease-relevant material:
  genotype-linked `GPR25`/`KIF21B` expression or GPR25 surface protein in MS
  PBMC/CSF immune cells.

Candidate access routes:

- Search dbGaP/EGA for multiple sclerosis PBMC/CSF single-cell cohorts with
  genotype or donor-level variant data.
- V18 web/source scout found references to MS ocrelizumab PBMC/CSF controlled
  resources in dbGaP searches, but no dataset was self-acquired. Treat specific
  accessions as to-verify before application.
- EGA records such as MS CSF/scRNA studies may require institutional EGA DAC
  approval; verify the accession and DAC before applying.

Human action:

1. Search dbGaP for `multiple sclerosis single cell CSF PBMC genotype`.
2. Search EGA for `multiple sclerosis CSF single cell genotype`.
3. Prioritize cohorts with:
   - donor genotype or imputed genotype;
   - PBMC and CSF immune cells;
   - raw or normalized gene expression;
   - CITE-seq or surface-protein measurements if available.
4. Submit access requests through the listed DAC/dbGaP process.
5. Confirm data-use terms allow local computational genetics/eQTL analysis.

Place files here:

- `data/raw/ms_csf_pbmc_genotype_sc/`
- Suggested structure:
  - `genotypes/`
  - `expression/`
  - `protein_or_citeseq/`
  - `metadata/`
  - `README_ACCESS_TERMS.txt`

Priority: highest biologically. This is the only class that directly resolves
the MS-specific immune/CSF question rather than using healthy-donor immune
QTLs.

### 4. UK Biobank / Large Biobank Individual-Level Immune Phenotype Data

Purpose:

- Secondary route for genotype-to-immune-cell-state or comorbidity analyses if
  single-cell sources fail.

Human action:

1. Apply through UK Biobank Access Management System with an approved research
   purpose.
2. Request relevant genotypes, immune-cell counts/biomarkers, MS diagnosis, IBD
   diagnosis, and any available transcriptomic/proteomic fields.
3. Budget for fees and institutional approvals; timelines are usually weeks to
   months.

Place files here:

- `data/raw/ukbb_controlled/`

Priority: medium. Useful for phenotype-scale genetics, less direct for
GPR25-versus-KIF21B cellular causality.

## Governance Reminder

Do not place controlled-access data into the repository unless:

- the data-use agreement permits this local environment;
- the files remain outside version control;
- access terms are stored locally for audit;
- no identifiable or restricted individual-level data is committed.
