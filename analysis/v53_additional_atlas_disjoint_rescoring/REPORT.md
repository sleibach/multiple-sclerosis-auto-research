# V53 Additional-Atlas Disjoint Rescoring

Verdict: **BROAD_APC_RECURRENCE_SURVIVES_DISJOINT_PHYSICAL_DATASET_GATE**.

Canonical original scores were source-rebuilt before sensitivity analysis. Exact
checks cover the unchanged GSE111972 receptor module and all four canonical modules
in GSE248205 and GSE315138. Effects were then recomputed with genes globally unique
to each of the four APC modules.

For recurrence, compartments and disease contrasts were averaged within each physical
dataset before a directional sign test. This yields eight physical datasets: five
held direct-h5ad sources plus GSE111972, GSE248205, and GSE315138. The gate requires
at least 7/8 positive dataset means, BH q<=0.10 across four modules, and leave-one-
dataset-out positive fraction >=0.75.

Modules passing: `ifn_apc;mif_cd74_receptor_state`.
This result concerns broad cross-disease recurrence only. It is not MS-specific and
does not identify causal direction, treatment benefit, or a therapeutic target.
