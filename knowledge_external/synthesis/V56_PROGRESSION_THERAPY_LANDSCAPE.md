# V56 Progression-Therapy Landscape

Date accessed: 2026-08-05

Purpose: current external context around the grounded V56 progression-route
audit. Every external statement is explicitly classed and sourced. The project
results remain in `docs/reports/PROGRESSION_THERAPY_OPPORTUNITY_V56.md`.

## What Changed Clinically

- [`external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: https://pubmed.ncbi.nlm.nih.gov/40202696/] HERCULES randomized 1,131 participants with non-relapsing SPMS and reported 6-month confirmed disability progression in 22.6% with tolebrutinib versus 30.7% with placebo (hazard ratio 0.69, 95% CI 0.55 to 0.88); serious adverse events and alanine-aminotransferase elevations were more frequent with tolebrutinib.
- [`external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: https://www.ema.europa.eu/en/medicines/human/EPAR/cenrifki] The European Union authorized tolebrutinib in June 2026 for adults with SPMS without relapses in the preceding two years, with additional monitoring and explicit liver-testing requirements.
- [`external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: https://download.open.fda.gov/crl/CRL_NDA219624_20251223.pdf] The FDA did not approve the same program in December 2025 because severe, potentially fatal drug-induced liver injury could not be adequately mitigated and no clinically identifiable subgroup had sufficiently certain benefit to outweigh that risk.
- [`external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: https://www.sanofi.com/en/media-room/press-releases/2025/2025-12-15-06-05-00-3205094] Sanofi reported that the PERSEUS phase 3 trial did not meet its primary PPMS disability-progression endpoint; this is sponsor-reported topline information pending complete peer-reviewed analysis.
- [`external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: https://medically.gene.com/content/dam/pdmahub/restricted/neurology/actrims-forum-2026/ACTRIMS-Forum-2026-presentation-bar-or-efficacy-and-safety-of-fenebrutinib-vs-ocrelizumab-in-primary-progressive-multiple-sclerosis.pdf] A sponsor presentation reported that fenebrutinib met its prespecified non-inferiority criterion versus ocrelizumab in PPMS (composite disability-progression hazard ratio 0.88, 95% CI 0.75 to 1.03); non-inferiority to an active comparator is not superiority and the complete peer-reviewed report was pending.
- [`external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: https://eprints.whiterose.ac.uk/id/eprint/233048/1/Effect%20of%20repurposed%20simvastatin%20on%20disability%20progression%20in%20secondary%20progressive%20multiple%20sclerosis.pdf] MS-STAT2 reported no SPMS disability-progression benefit from simvastatin versus placebo (hazard ratio 1.13, 95% CI 0.91 to 1.39), closing the simple simvastatin progression route despite the earlier phase 2 rationale.

These external results are not mutually reducible to a single “BTK works” or
“BTK fails” statement. They show compound-, phenotype-, comparator-, and
jurisdiction-specific benefit-risk decisions. None validates a project module.

## The Most Important Tension

- [`external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: https://download.open.fda.gov/crl/CRL_NDA219624_20251223.pdf] In FDA-reported subgroup analyses, the HERCULES treatment-effect estimate was larger with baseline gadolinium-enhancing lesions (hazard ratio 0.346, 95% CI 0.183 to 0.656) than without them (0.777, 0.601 to 1.006), and diminished as the number of prior MS therapies increased; the FDA explicitly treated those results as uncertain rather than a validated selection rule.
- [`external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/SAP_001.pdf] Baseline gadolinium activity and prior-therapy count were prespecified subgroup factors in the final public statistical analysis plan, but subgroup interaction tests were not in the primary multiplicity hierarchy and the FDA's broader active-versus-non-active interpretation was limited by absent historical MRI.
- [`external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: https://www.ema.europa.eu/en/medicines/human/EPAR/cenrifki] The EMA nevertheless concluded that the overall benefit-risk balance supported authorization for adults with SPMS without relapses in the previous two years, with intensive liver-risk management.

This regulatory divergence is the decision-relevant frontier. The defensible
question is not whether to invent a molecular story for the average effect. It
is whether activity history, prior treatment, safety susceptibility, and any
prospectively collected molecular measurements can identify a reproducible
favorable-benefit subgroup without post hoc overfitting.

## Direct Data-Access Opportunity

- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://clinicaltrials.gov/study/NCT04411641] The HERCULES registry states that qualified researchers may request anonymized participant-level data, data specifications, protocol, statistical analysis plan, case-report form, and clinical study report through Vivli, subject to sponsor and independent-review approval.
- [`external-unverifiable`; `NOT_PROJECT_GROUNDED`; source: https://www.sanofi.com/en/our-science/clinical-trials-and-results/our-data-sharing-commitments] Sanofi states that it accepts researcher proposals for participant-level trial data through Vivli; access remains controlled and approval is not guaranteed.

This route is more actionable than another public cross-sectional expression
scan. The registry does not establish that transcriptomics, proteomics, or CSF
biomarkers are shareable; that must be asked explicitly and verified against the
approved data dictionary.

### ToleDYNAMIC intervention-omics route

- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf] The public HERCULES protocol separately describes ToleDYNAMIC, an approximately 80-participant HERCULES/PERSEUS substudy with baseline, month-3, and month-12 samples, detailed immune phenotyping, CD14-monocyte functional assays, and B-cell/monocyte RNA sequencing in a subset.
- [`external-verifiable`; `NOT_PROJECT_GROUNDED`; source: https://cdn.clinicaltrials.gov/large-docs/41/NCT04411641/Prot_000.pdf] The appendix repeatedly specifies tolebrutinib-treated participants and sampling after treatment initiation; it does not describe placebo-arm sampling.

ToleDYNAMIC is the highest-priority molecular access question because it links
an intervention, two progressive-MS phenotypes, repeated immune measurements,
functional myeloid assays, and parent clinical/MRI outcomes. The protocol does
not prove completion, availability, or assay quality. Its public design supports
paired pharmacodynamic description and a cross-trial sufficiency check, not a
randomized treatment effect. Both-arm inference is allowed only if sponsor
metadata explicitly document a different design. It must be requested
explicitly; standard clinical IPD access cannot be assumed to include it.

## Relationship To Project Results

### Corroborated Methodological Constraints

The external context independently aligns with three project-grounded decision
rules without turning the external claims into project findings:

1. **Context dependence matters.** A route cannot be generalized across SPMS,
   PPMS, inflammatory activity, and prior-treatment strata.
2. **CNS exposure is necessary but insufficient.** Brain penetrance does not
   remove compound-level safety, subgroup uncertainty, or phenotype failure.
3. **Collateral safety can dominate pathway plausibility.** A biologically
   credible mechanism is not a favorable therapeutic route when severe toxicity
   cannot be acceptably mitigated.

Project sources: `docs/history/FAILURE_STRUCTURE_AND_EXCLUSION_V39.md` and
`docs/reports/THERAPEUTIC_PATH_V52.md`.

### What Is Not Corroborated

No external trial result corroborates the locked V22 DMF-response scalar, the
CD44/CXCR4 state, the lysosomal proxy, the MIF/CD74 coupling, or the broad-rim
module associations as a progression-treatment biomarker. The V56 rapid-versus-
slow SPMS PBMC analysis is null, and the lesion result remains acquisition- and
reconstruction-bounded.

## Ranked External-Context Opportunities

| rank | opportunity | why it matters | critical boundary |
|---:|---|---|---|
| 1 | Controlled HERCULES participant-level reanalysis | Direct randomized progression-treatment and safety outcomes; can test stability of clinical effect modifiers | Controlled access; subgroup multiplicity; standard IPD may omit molecular data |
| 2 | ToleDYNAMIC controlled intervention-omics request | Direct baseline/month-3/month-12 B-cell/monocyte transcript and function opportunity across HERCULES/PERSEUS | Public design appears active-treatment-only; completion/access and RNA-subset size unverified; likely small |
| 3 | Prospective CNS-penetrant-BTK treatment biomarker cohort | Could test whether early blood/CSF change improves prediction beyond activity, MRI, and prior treatment | Requires pre-registration, adequate sample size, and independent validation |
| 4 | Author-complete broad-rim lesion reconstruction | Could determine whether lesion modules are source-balanced and lesion-specific | Postmortem association; no treatment or longitudinal disability |
| 5 | Fenebrutinib participant-level analysis after full reporting | Independent compound and PPMS setting may test class versus compound specificity | Active comparator, data-access timing, no asserted molecular package |
| 6 | Simvastatin route | Decision-useful phase 3 null | No-go for repurposed simvastatin as SPMS progression therapy; not a blanket lipid-biology exclusion |

## Honest Bottom Line

There is now external clinical evidence that disability progression can be
modified in at least one defined SPMS trial setting, but the effect is not a
cure, is not phenotype-invariant, and is paired with a serious compound-level
safety problem. The project did not discover that treatment and cannot claim to
explain it.

The tractable contribution available to this project is narrower and concrete:
obtain controlled participant-level data, reproduce the primary analysis,
pre-register effect-modification and benefit-risk questions, and test any
molecular measurement only after clinical/MRI baselines and multiplicity are
locked. That is a credible path toward better treatment selection. No held-data
result currently supports a new drug target.
