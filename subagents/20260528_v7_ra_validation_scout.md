# V7 RA Validation Cohort Scout

Timestamp: 2026-05-28 23:02 CEST

Scope: public RA anti-TNF/JAK/biologic transcriptomic response cohorts excluding
the locked derivation/refinement cohorts `GSE282122`, `GSE138064`, and
`GSE24427`. I did not tune `LOCKED_RULE_V7.md` and did not edit shared indexes.

## Locked-Rule Class Key

- **Class A:** inflammatory input blockade. For this scout, anti-TNF,
  tocilizumab/IL-6R blockade, and JAK inhibition map here.
- **Class B:** exogenous IFN/APC-reprogramming. No RA cohort below clearly maps
  to Class B.
- **Class C:** non-APC-primary therapy, cell depletion, trafficking, or
  costimulation/depletion-style mechanisms. Abatacept is treated as Class C for
  V7 primary validation unless an APC-relevant hypothesis is pre-registered
  before analysis.

## High-Priority Validation Candidates

| Accession | Therapy | Platform / tissue | Sample counts available from source | Baseline and/or post-treatment | Response label source | Data accessibility | Locked class | Scout verdict |
|---|---|---|---:|---|---|---|---|---|
| `GSE198520` | anti-TNF: etanercept (`n=19`) or certolizumab pegol (`n=27`) | RNA-seq, RA synovial biopsy, Illumina HiSeq 3000 / `GPL21290` | 92 samples from 46 RA patients | paired baseline and 12-week post-treatment synovial biopsies | GEO summary states EULAR good/moderate/nonresponse; samples named `r_###_pre` and `r_###_post`; source paper/metadata needed to map patient IDs to response labels | GEO public; processed/supplementary availability must be checked before analysis | Class A | Best held-out RA anti-TNF longitudinal validation candidate. Not “early” by locked rule, but has paired on-treatment delta and responder labels. |
| `GSE8350` | infliximab | custom low-density cDNA microarray, peripheral whole blood/PAXgene / `GPL5460` | 72 samples from 18 RA patients | baseline, 2 weeks, 14 weeks, 22 weeks after first infliximab infusion | GEO summary: responders/nonresponders by ACR50 at 22 weeks; sample titles encode patient/time and apparent response group via suffix values, but response decoding should be verified from SOFT/publication | GEO public; processed data included in Sample table and RAW tar is small | Class A | Very strong V7 target because it has true early delta at 2 weeks. Small `n=18`, but directly tests locked Class A early-delta rule. |
| `GSE42296` | infliximab | Affymetrix Human Gene 1.0 ST Array / `GPL6244`, peripheral blood | 78 total samples: 20 IBD week0/week2 pairs and 19 RA week0/week2 pairs | week 0 and week 2 | GEO title/summary says markers predicting responder status; response labels likely require SOFT/sample characteristics or publication table because visible sample titles encode disease/time/patient, not responder status | GEO public; processed data included plus supplementary processed file | Class A | Strong candidate if response labels are extractable. Early week-2 delta exactly matches locked Class A primary feature. |
| `GSE78068` | infliximab, tocilizumab, abatacept | Agilent Whole Human Genome 4x44K / `GPL6480`, whole blood | 209 baseline samples: IFX `n=140` (`98` non-remission, `42` remission), TCZ `n=38` (`30` non-remission, `8` remission), ABT `n=31` (`24` non-remission, `7` remission) | baseline only | sample titles explicitly encode therapy and remission/non-remission; remission defined by CDAI at 6 months in GEO summary | GEO public; processed data included, RAW tar large | IFX Class A; TCZ Class A; ABT Class C | Highest-throughput baseline-only RA biologic validation set. IFX is the cleanest Class A baseline test; TCZ is useful Class A comparator; ABT should be exploratory/Class C. |
| `GSE58795` | infliximab | Rosetta/Merck Human RSTA Custom Affymetrix / `GPL10379`, whole blood | 59 baseline samples | baseline only | GEO summary: baseline samples from placebo-controlled infliximab trial; response assessed by 12-week dynamic contrast-enhanced MRI and DAS28; sample-level responder labels likely in SOFT/sample metadata or publication | GEO public; processed data included; RAW CEL tar 280 MB | Class A | Good baseline-only Class A validation candidate if binary response labels can be parsed. Larger than most older RA cohorts. |
| `GSE21537` | infliximab | KTH Human 30k spotted oligo array / `GPL7768`, synovial biopsy | 62 baseline synovial biopsy samples | baseline only | GEO summary gives EULAR response counts: 18 good, 30 moderate, 14 nonresponding; sample-level mapping likely in SOFT/publication | GEO public; processed data included; RAW GPR tar available | Class A | Valuable synovial baseline-only validation cohort. Confounded by lymphoid aggregates per GEO summary, so mark as tissue-pathotype-sensitive. |
| `GSE12051` | infliximab | Sentrix Human-6 Expression BeadChip / `GPL2507`, blood | 44 samples from 44 week-14 evaluable patients | baseline only | sample titles explicitly encode `blood_responder` or `blood_nonresponder`; GEO summary says response determined at week 14 | GEO public; processed data included and Series Matrix available | Class A | Easy baseline-only Class A validation cohort with labels in sample names. |
| `GSE33377` | anti-TNF, monoclonal antibodies likely infliximab/adalimumab per publication context | Affymetrix Human Exon 1.0 ST / `GPL5175`, white blood cells | 42 samples: 18 responders, 24 nonresponders | baseline only | sample titles explicitly encode `anti-TNF responder` and `anti-TNF non-responder` | GEO public; processed data included; RAW CEL tar large | Class A | Easy baseline-only Class A validation cohort with clear labels. Therapy granularity may be mixed anti-TNF, but still in-scope. |
| `GSE3592` | infliximab + methotrexate | INSERM Homo sapiens 14K array / `GPL3064`, PBMC | 44 array samples; GEO design says 13 RA patients in responder/nonresponder comparison plus controls/technical repeats | likely baseline/predictor samples; sample names encode `R` and `NR` patient/sample replicate IDs | sample names encode responder/nonresponder (`R#S#`, `NR#S#`); publication says good vs poor response to infliximab/MTX | GEO public; Series Matrix available, no supplementary raw files | Class A | Usable only with careful replicate handling. Lower priority than cleaner one-sample-per-patient cohorts. |
| `GSE20690` | infliximab | Agilent Whole Human Genome 4x44K / `GPL4133`, PAXgene/white blood cells | 68 baseline samples: 42 training + 26 verification | baseline only | sample titles encode `No Inflammation (NI)` or `Residual Inflammation (RI)` at 14 weeks; this is CRP-defined residual inflammation, not standard EULAR/ACR response | GEO public; processed data included, supplementary normalized matrix available | Class A | In-scope mechanistically but endpoint differs from locked binary clinical response. Use as secondary/context validation unless V7 accepts NI/RI as response label before analysis. |

## Lower-Priority / Not Cleanly Usable

| Accession / resource | Therapy | Platform / tissue | Sample counts | Baseline and/or post-treatment | Response label source | Data accessibility | Locked class | Scout verdict |
|---|---|---|---:|---|---|---|---|---|
| `GSE19821` | infliximab | expression profiling by array, RA blood/PAXgene | 30 samples listed by external catalogue | before/after infliximab in publication context | response categories are not unambiguously available; one systematic bioinformatics analysis explicitly excluded `GSE19821` for absence of response categories | GEO accession exists; external eTRIKS distribution is deprecated/not accessible | Class A | Do not prioritize for V7 validation unless SOFT inspection recovers sample-level responder labels. |
| `GSE7524` | etanercept / Enbrel | Affymetrix U133A / `GPL96`, LPS-stimulated whole blood | 6 samples: 2 controls, 2 RA pre-treatment, 2 RA post-treatment | pre and 3-month post-treatment | no responder/nonresponder labels; only two RA patients/replicates | GEO public; processed data included and RAW tar available | Class A by therapy, not validation-usable | Too small and unlabeled for locked validation. Could be exploratory pharmacodynamic context only. |
| `E-MTAB-11` | etanercept | Affymetrix U133A/U95A, PBMC | 19 RA patients in publication: 12 responders, 7 nonresponders | baseline and 72 hours after first etanercept application | publication defines response by DAS28/EULAR-like clinical outcome at 3 months; ArrayExpress accession, not GEO | public ArrayExpress per publication, not yet checked locally | Class A | Potentially excellent early-delta Class A cohort, but not GEO. Include only if V7 broadens acquisition beyond GEO. |

## Notes On Other Biologic/JAK Cohorts

- I found literature for tofacitinib/JAK transcriptomic response in RA, including
  synovial qPCR/biopsy and whole-blood RNA-seq studies, but I did not verify a
  GEO accession with sample-level expression and responder/nonresponder labels
  during this sidecar.
- `GSE78068` supplies the cleanest non-TNF biologic comparator within GEO:
  tocilizumab baseline remission/non-remission is Class A under the V7
  inflammatory-input-blockade framing; abatacept is Class C and should not count
  toward primary validation success.

## Recommended Acquisition Order

1. `GSE8350` - Class A, true early delta, small but directly aligned to locked
   primary feature.
2. `GSE42296` - Class A, week-0/week-2 RA infliximab pairs; first check response
   label availability.
3. `GSE198520` - Class A, paired synovial RNA-seq pre/post anti-TNF; stronger
   tissue relevance though post-treatment is 12 weeks, not early.
4. `GSE78068` - large baseline-only Class A IFX and TCZ arms with labels in
   sample titles.
5. `GSE12051`, `GSE33377`, `GSE58795`, `GSE21537` - baseline-only validation
   cohorts; useful for locked fallback baseline feature.
6. `GSE20690` - use cautiously because endpoint is residual inflammation by
   CRP, not standard responder/nonresponder.

## Source Links Checked

- `GSE12051`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE12051
- `GSE33377`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE33377
- `GSE58795`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE58795
- `GSE21537`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE21537
- `GSE8350`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE8350
- `GSE42296`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE42296
- `GSE20690`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE20690
- `GSE78068`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE78068
- `GSE198520`: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE198520
- `GSE19821` external catalogue note:
  https://datacatalogue.elixir-luxembourg.org/e/dataset/924f496a-71e8-11eb-bafe-3e22fbb3883f
- `E-MTAB-11` source publication:
  https://arthritis-research.biomedcentral.com/articles/10.1186/ar2419

