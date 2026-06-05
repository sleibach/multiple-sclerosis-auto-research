# V7 Validation Ledger

Locked rule: `LOCKED_RULE_V7.md`  
Validation exclusion: `GSE282122`, `GSE138064`, `GSE24427`

| Cohort | Disease | Therapy | Class | Data status | N labeled | Locked feature | AUC | AUC 95% CI | Hedges g | p | Pass/fail | Notes |
| --- | --- | --- | --- | --- | ---: | --- | ---: | --- | ---: | ---: | --- | --- |
| `GSE12051` | RA | infliximab | Class A baseline-only | analyzed | 44 | `baseline_IFN_APC` | 0.382 | 0.181-0.595 | -0.339 | 0.385 | fail | Whole-blood baseline RA infliximab response; locked Class A fallback because no early on-treatment sample is present. |
| `GSE16879` | IBD | infliximab | Class A early delta | analyzed | 60 | `-delta_IFN_APC` | 0.754 | 0.613-0.871 | 0.985 | 0.0003647 | pass | Mucosal IBD before/4-6 week post first infliximab; all paired IBD samples pooled per locked rule, no UC/CD subgroup tuning. |
| `GSE12251` | UC | infliximab | Class A baseline-only | analyzed | 22 | `baseline_IFN_APC` | 0.250 | 0.060-0.500 | -1.043 | 0.01947 | fail | UC colonic biopsy baseline before infliximab; week-8 endoscopic/histologic healing. Duplicate P13 arrays averaged before statistics. |
| `GSE138746_CD14` | RA | adalimumab/etanercept | Class A baseline-only | analyzed | 78 | `baseline_IFN_APC` | 0.485 | 0.358-0.613 | -0.099 | 0.6547 | fail | RA sorted CD14 monocyte baseline RNA-seq before anti-TNF; EULAR moderate/good versus none pooled across adalimumab and etanercept per anti-TNF class. |
| `GSE73661_IFX` | UC | infliximab | Class A early delta | analyzed | 23 | `-delta_IFN_APC` | 0.825 | 0.559-1.000 | 1.390 | 0.01265 | pass | UC colonic mucosa before and W4-6 after first infliximab; response from W4-6 sample title R/NR and study individual pairing. |
| `GSE8350` | RA | infliximab | Class A early delta | analyzed | 18 | `-delta_IFN_APC` | 0.450 | 0.163-0.769 | -0.356 | 0.443 | fail | RA whole-blood baseline and 2-week post-infliximab custom array; response encoded by ACR score in sample titles, responder defined as ACR >=50. |
