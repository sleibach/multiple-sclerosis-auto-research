# Incoming Package Communication Templates V52

Date: 2026-07-10

Status: operational communication templates. This document adds no evidence,
changes no locked rule, and does not interpret any real incoming package. Use
these templates only after package receipt has been classified by the existing
acceptance criteria and command manifest.

## Purpose

When an author, collaborator, or repository package arrives, the project should
respond mechanically and safely. These templates prevent accidental biological
interpretation before package eligibility, access terms, checksums, and required
fields are settled.

## Template 1: Monitoring Package Accepted For Frozen Validation

Subject: MS treatment-response package accepted for frozen validation

Thank you for the package. Based on the provided files and metadata, it appears
eligible for the frozen treatment-response validation workflow:

- paired baseline and early on-treatment PBMC expression are present;
- subject-level response labels are present;
- feature annotation supports V22 module scoring;
- batch/QC metadata are available for the V44 diagnostics.

Next we will record checksums, quarantine the package, and run only the
pre-registered V42/V44 validation harness. We will not tune endpoints,
timepoints, features, thresholds, or signs after receipt. The output will be one
of the pre-specified classes: clean pass, immune-tone/batch-bounded pass,
inconclusive, adequate-powered fail, or unscoreable if a mechanical issue is
found during preflight.

## Template 2: Monitoring Package Partial Context Only

Subject: MS treatment-response package classified as partial context

Thank you for the package. The files contain useful context, but the package is
not currently sufficient for a clean frozen validation because:

`[insert missing field: labels / pairing / feature annotation / batch metadata /
module coverage / timing / access terms]`

We can use the package only for the subset of analyses allowed by the existing
criteria, and we will label any output as partial context. We will not treat an
unscoreable or incomplete package as evidence for or against the monitoring
rule.

To make the package validation-eligible, please provide:

`[insert exact missing fields from TARGET_PACKAGE_ACCEPTANCE_CRITERIA_V52.tsv]`

## Template 3: Monitoring Package Rejected / Unscoreable

Subject: MS treatment-response package is unscoreable under the frozen plan

Thank you for the package. Under the pre-registered validation plan, the package
cannot test the monitoring rule because:

`[insert reason: missing baseline sample / missing early on-treatment sample /
missing response label / failed module coverage / unmappable subject pairing /
terms block analysis]`

This is not a biological null. It means the package cannot mechanically answer
the pre-specified question. We will not tune the rule or substitute a different
endpoint to make the package usable.

## Template 4: chr1 Target-Development Package Accepted

Subject: chr1 KIF21B/GPR25 package accepted for direction-matched review

Thank you for the package. Based on the provided files and metadata, it appears
eligible for the chr1 direction-matched review:

- chr1 credible-set genotype dosage or high-quality imputation is present;
- ancestry/genotype PCs and batch/QC metadata are present;
- candidate gene RNA/protein readouts include GPR25, KIF21B, local alternatives,
  and cell-state labels;
- treatment, steroid, relapse, infection, and disease-context metadata are
  available.

Next we will run the staged chr1 blueprint. The package can support causal-gene,
cell-state, and direction classification. It does not by itself reopen chr1 as a
target unless the full direction-matched chain is satisfied, including
perturbation and modality evidence.

## Template 5: chr1 Package Partial Context Only

Subject: chr1 KIF21B/GPR25 package classified as partial context

Thank you for the package. The data are potentially useful, but they do not
support a full chr1 target-development decision because:

`[insert missing field: credible-set genotype / ancestry PCs / candidate gene
readout / cell-state labels / perturbation / direction harmonization / metadata]`

We can use the package only for the allowed partial-context question. We will
not infer missing causal gene, cell state, direction, or modality from prior
preference.

To make the package decision-useful, please provide:

`[insert exact missing fields from the chr1 collaborator appendix]`

## Template 6: chr1 Package Rejected For Target Reopening

Subject: chr1 package cannot reopen target workup under current criteria

Thank you for the package. Under the V52 chr1 criteria, the package cannot
reopen GPR25 or KIF21B for target workup because:

`[insert reason: no genotype dosage / no candidate readout / no relevant cell
state / direction unharmonizable / perturbation wrong-direction / only
structure or class context]`

This does not erase the chr1 biology. It means the package does not satisfy the
direction-matched target-development chain required before wet-lab target work.

## Template 7: Access Terms Or Use Restrictions Block Analysis

Subject: Package access terms require clarification before analysis

Thank you for the package. Before opening or analyzing the files, we need
clarification of access and use terms:

`[insert issue: no license / no data-use terms / controlled-access restriction /
publication embargo / no derivative analysis permission / unclear sharing
terms]`

Until terms are clarified, the package remains quarantined and unread for
analysis. We will not inspect protected data or infer any result from the
existence of the package.

## Template 8: Additional Fields Request

Subject: Additional fields needed for MS package interpretation

Thank you for the materials. To classify and analyze the package under the
pre-specified plan, please provide the following fields:

- `[field 1]`
- `[field 2]`
- `[field 3]`

Without these fields, the package will remain partial or unscoreable according
to the V52 acceptance criteria. We will not replace missing fields with inferred
or post-hoc alternatives.

## Required Attachments To Any Response

When sending any template, attach or cite:

1. the package classification;
2. the missing-field list, if any;
3. the relevant acceptance criteria row;
4. the statement that frozen rules and pre-registrations will not be changed;
5. the checksum/quarantine status if files were received.

## Source Artifacts

- `docs/validation/TARGET_PACKAGE_ACCEPTANCE_CRITERIA_V52.tsv`
- `docs/validation/MONITORING_VALIDATION_COMMAND_MANIFEST_V52.md`
- `docs/validation/MONITORING_VALIDATION_DECISION_TREE_V52.md`
- `docs/validation/MEDICAL_TEAM_THERAPEUTIC_DATA_REQUEST_V52.md`
- `docs/workups/genetics/CHR1_COLLABORATOR_ASSAY_REQUEST_APPENDIX_V52.md`
- `docs/workups/genetics/CHR1_DIRECTION_MATCHED_EXPERIMENT_BLUEPRINT_V52.md`
