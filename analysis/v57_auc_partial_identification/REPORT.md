# V57 Missing-Label AUC Partial Identification

## Result

Every missing-label subset of size 1-5 was enumerated around the fixed
19-subject score distribution; participant-level patterns were not persisted.
The complete-data reference AUC is 0.811.

| Information mode | Missing labels | Worst lower | Median lower | Median upper | Median width | Patterns lower >=0.60 |
|---|---:|---:|---:|---:|---:|---:|
| `known_total_responder_count` | 1 | 0.811 | 0.811 | 0.811 | 0.000 | 100.0% |
| `known_total_responder_count` | 2 | 0.611 | 0.811 | 0.811 | 0.011 | 100.0% |
| `known_total_responder_count` | 3 | 0.611 | 0.722 | 0.811 | 0.100 | 100.0% |
| `known_total_responder_count` | 4 | 0.433 | 0.689 | 0.811 | 0.144 | 91.6% |
| `known_total_responder_count` | 5 | 0.433 | 0.644 | 0.822 | 0.200 | 74.7% |
| `no_prevalence_information` | 1 | 0.711 | 0.773 | 0.811 | 0.050 | 100.0% |
| `no_prevalence_information` | 2 | 0.611 | 0.727 | 0.811 | 0.102 | 100.0% |
| `no_prevalence_information` | 3 | 0.522 | 0.689 | 0.822 | 0.156 | 93.4% |
| `no_prevalence_information` | 4 | 0.433 | 0.644 | 0.852 | 0.211 | 76.1% |
| `no_prevalence_information` | 5 | 0.352 | 0.600 | 0.856 | 0.265 | 52.9% |

Without response-prevalence information, the largest universally tolerable
missing-label count is
2.
When an independently audited total responder count is available, it is
3.

## Operational implication

Partial labels do not justify complete-case or point-imputed validation by
default. A returned package should report sharp AUC bounds first. A point AUC
is interpretable only after labels are resolved or a missingness assumption is
separately justified. Knowing only the cohort-wide class total can narrow the
bounds, but it cannot be assumed from the expression rows.

These are empirical identification regions conditional on the held score
ordering. They characterize method behavior and package requirements; they do
not validate V22 or estimate any future cohort's missingness process.
