# V53 MS Microglia Component Specificity

Verdict: **CD44_CXCR4_ASSOCIATION_NOT_COMPONENT_SPECIFIC_AFTER_STRICT_GATE**.

CD44 and CXCR4 were tested separately in patient-equal quadratic-age models with
100,000 wild-null replicates and BH correction across the two genes. The receptor
module was then jointly adjusted for CIITA/RFX5, MIF/DDT, unique IFN/APC, and unique
lysosomal scores.

Base receptor beta is `0.796` (p `0.0029`); joint-adjusted beta is
`0.342` (p `0.1051`), attenuation `57.0%`,
condition number `5.55`, and minimum leave-one-patient-out joint
beta `0.199`.

Passing this gate would support component coherence and separation from measured broad
state scores in one cohort only. It would not establish causality, intervention
direction, target selectivity, or independent replication.
