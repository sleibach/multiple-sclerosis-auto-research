# V53 MS Microglia Receptor-State Decoupling

Verdict: **MS_MICROGLIA_CD44_CXCR4_DECOUPLING_NOT_ESTABLISHED**.

GSE111972 contains `31` sorted-microglia samples from `21`
patients. The primary model adjusts for region, standardized age, and sex, uses
patient-clustered standard errors, and applies 100,000 patient-cluster wild-null
replicates per outcome with BH correction across five modules/controls and two
pre-specified module-difference tests.

CD44/CXCR4 adjusted disease beta is `0.714`
(wild-cluster q `0.0790`). Its difference
from CIITA/RFX5 is `0.849`
(q `0.1994`), and its difference
from MIF/DDT ligand is `0.168`
(q `0.6476`).

The receptor-state association passes its component gate, but the full decoupling
gate does not. This single-cohort sorted-bulk result does not establish cell-intrinsic
causality, beneficial intervention
direction, target selectivity, or replication in an independent MS cohort.
