# Contribute A Dataset Or Cohort Lead

A paper title, repository accession, or statement that “the data are public” is
the start of a data lead, not proof that the project can use it. This guide
turns a source lead into a verifiable eligibility package.

Do not upload participant data, personal health information, credentials, or
material whose use terms do not authorize the proposed analysis. Metadata and
public links are enough for first review.

No cohort is counted usable until pairing, labels, time, required measurements,
source/provenance, independent units, and permitted use are verified. Missing
fields are a data boundary, not evidence that the biology is absent. `[A01-
A04, P01-P05, E01-E02]`

## Step 1: Name The Exact Decision

Choose one data role:

| role | decision it could change | closest project boundary |
|---|---|---|
| Monitoring validation | Run the frozen early-change score on an independent paired response cohort. | One provisional monitoring lead; outside validation pending. `[M01-M05, A01]` |
| Monitoring replication | Estimate transport after the primary frozen test without redefining it. | Mixed therapy/cohort results; no broad rule. `[M02]` |
| Progression prediction | Test a fixed compatible molecular state against later repeated confirmed disability. | Required longitudinal design absent. `[P01-P03, A02]` |
| Microglia state replication | Recheck exact state identity in source-balanced independent donors. | Bounded identity support; one partition source-sensitive. `[C01-C02]` |
| Functional direction | Test whether increasing or decreasing a causally supported entity produces the required outcome in the relevant cell state. | Genetics routes closed on causal assignment or direction. `[G02-G05]` |
| Confound or negative control | Challenge source, batch, broad immune state, composition, timing, or observation-process explanations. | Specificity is bounded by known confound lessons. `[M04, C02]` |

If the source does not change a named decision, record it as context rather
than describing it as validation-ready.

## Step 2: Record Source And Access

Provide:

```markdown
Dataset/study title:
Repository and accession:
Primary paper and permanent identifier:
Data-availability statement URL:
Metadata URL:
Access tier: open / registration / application / controlled / author-held
Exact access steps:
License or data-use terms:
Date checked:
Contact or application route, if public:
```

Do not include a token, service key, private email, application password, or
signed agreement in a public issue.

## Step 3: Prove The Study Unit

State what is independent:

```markdown
People or donors:
Samples:
Sites or source collections:
Repeated samples per person/donor:
Any overlap with a cohort already used here:
How overlap was checked:
```

Two assays, tissues, or papers from the same people do not create two
independent cohorts. Multiple cells from one donor do not create independent
people. If independence cannot be checked, mark it unverified.

## Step 4: Verify The Required Fields

### For monitoring validation

All of these are required for primary eligibility:

- stable person ID and sample ID;
- paired pre-treatment baseline and allowed early on-treatment sample;
- exact collection dates or treatment-relative times;
- verified person-level response label;
- outcome definition and assessment window;
- treatment identity and timing;
- genes needed by the locked modules under a mappable identifier system;
- normalization and platform provenance;
- source, site, processing batch, and quality fields;
- inclusion/exclusion provenance; and
- permitted use for the frozen analysis.
  `[A01, A04]`

Paired samples without response labels are not validation-ready. A response
label reconstructed from molecular data is not independent. A different
treatment or outcome may support a separate transport question but cannot
silently replace the primary frozen test. `[M02, A01]`

### For progression prediction

All of these are required for the primary progression role:

- stable person/donor and sample IDs;
- an eligible microglia-compatible molecular compartment if testing the fixed
  candidate;
- repeated molecular timing or a pre-outcome molecular measurement under the
  fixed role specification;
- repeated disability measurements with dates;
- the exact confirmation and progression definition;
- relapse timing kept separate from progression adjudication;
- treatment and treatment-change timing;
- attendance, dropout, censoring, and follow-up provenance;
- source, site, processing batch, and quality fields; and
- permitted longitudinal linkage and analysis.
  `[B02, P01-P06, A02]`

A static disease-stage label, one disability score, relapse activity, lesion
morphology, pharmacodynamic blood response, or a substitute gene score does not
fill this role. `[P01-P06]`

### For source-balanced state replication

Verify:

- independent donors;
- diagnosis and source represented within overlapping strata;
- exact compatible cell compartment;
- fixed score genes without substitution;
- donor-aware units and repeated-cell handling;
- source, bank, site, processing, and quality metadata; and
- a plan that can return “not identifiable” when overlap is inadequate.
  `[C01-C02, P06]`

## Step 5: Show The Sample Map, Not The Outcome

For first review, a safe aggregate table is enough:

| field | value to report |
|---|---|
| People/donors | count, without identifiers |
| Samples | count by required time and compartment |
| Pairing | complete pairs, partial pairs, duplicate/ambiguous maps |
| Outcomes | counts by label and missingness, if disclosure is permitted |
| Follow-up | range and missingness, without person-level dates |
| Sources/sites | counts and overlap with outcomes |
| Platform/genes | identifier system and required-gene coverage |
| Access | exact tier, application, and use restrictions |

Do not expose small-cell combinations if they create a re-identification risk.
The holder may instead run a pre-specified eligibility checker and return only
safe flags.

## Step 6: Classify The Lead Honestly

| status | meaning | allowed statement |
|---|---|---|
| Unverified lead | A title, accession, or claim exists; required fields have not been checked. | “Candidate source to verify.” |
| Metadata near-match | Some required design is visible, but a decisive field is missing or incompatible. | “Potentially useful for a different question; not ready for this role.” |
| Holder clarification needed | The field may exist but is absent from public metadata. | “Eligibility pending a named answer.” |
| Access blocked | Structure appears compatible, but permission or terms are unresolved. | “Potential package; analysis not authorized.” |
| Eligible in principle | Every required field and use term is documented, but no files have been ingested. | “Ready for blind ingestion checks.” |
| Ingested and mechanically eligible | The pre-specified checker passed without reading outcomes beyond allowed eligibility summaries. | “Ready for the frozen run.” |
| Incompatible | A non-substitutable requirement fails. | “Does not answer this bounded question.” |

None of these is a scientific evidence grade. “Eligible” does not mean the
result will support the claim. `[E01, A01]`

## Common False Positives In Dataset Scouting

- Longitudinal samples but no response or disability outcome.
- Response labels in prose but no sample-person mapping.
- A baseline and a later sample, but the later time is outside the frozen
  window.
- Disease-stage labels described as progression.
- Relapse or lesion activity used as confirmed disability.
- Blood measurements proposed for a microglia-specific score.
- The right molecular assay but repeated cells from only a few donors.
- Required genes absent or available only through an outcome-informed proxy.
- “Available on request” with no confirmed holder response or use terms.
- Controlled data described as open.
- A processed matrix with no source, batch, normalization, or quality
  provenance.
- A cohort already used by the project presented as independent replication.

## Copy-Ready Data-Lead Submission

Replace every angle-bracket prompt. Submit metadata and lawful access details,
not participant rows, health records, credentials, controlled links, or private
files.

```markdown
### Decision role
<monitoring validation / replication / progression / state replication /
functional direction / confound control>

### Source and access
<title, accession, paper, permanent links, date checked, access tier, terms>

### Independent unit
<people/donors/sites; repeated samples; overlap with held cohorts>

### Required-field verification
| required field | present / absent / unclear | source proving it |
|---|---|---|
| ... | ... | ... |

### Aggregate structure
<safe counts for people, samples, pairing, times, outcomes, sources, platform>

### Main eligibility risk
<one strongest missing or potentially confounded field>

### Safe next action
<public metadata check / holder question / access application / blind
eligibility check / no further action>

### What this source cannot establish
<nearest tempting overread>

### Safety and evidence boundary
No personal/row-level data, credentials, or restricted material are attached.
This is a source candidate, not a usable cohort, validation, or finding until
blind eligibility and a separate frozen analysis pass.
```

## What Happens Next

The reviewer should verify permanent links and metadata, identify the one
strongest blocker, and return a workflow status using the
[review-response templates](REVIEW_RESPONSE_TEMPLATES.md). No raw data should
be requested publicly. Access and use terms are checked before ingestion.

If the package becomes mechanically eligible, it still runs under the existing
frozen plan or a separately pre-specified new test. The data lead itself never
changes a finding.

Continue with the [data-needed map](DATA_THAT_WOULD_CHANGE_THE_ANSWER.md),
[open problem 2](OPEN_PROBLEMS_FOR_COLLABORATORS.md#problem-2-remove-dependence-on-one-hard-to-access-cohort),
or the general [contribution guide](HOW_TO_CONTRIBUTE_IDEAS.md).
