# V53 Prospective Microglia Source-Balance Addendum

Status: prospective acquisition and replication-design addendum. It does not
change V22, V42, or the already-frozen V53 score/test, and it is not a
retroactive rule for rescuing or killing an observed cohort.

## Why This Is Required

The Macnair discovery partition has strong disease/brain-bank association
(Cramer's V `0.773`): one bank supplies 27 MS and no controls, while another
supplies 18 controls and one MS. The frozen score is positive before source
adjustment but attenuates after source fixed effects (wild `p=0.245`). A future
cohort must therefore make disease separable from acquisition source by design,
not rely on post-hoc correction.

## Frozen Prospective Acquisition Target

- At least 32 MS and 32 control donors after all exclusions.
- At least two source families or acquisition sites.
- Every included source contributes at least five MS and five control donors.
- No source contributes more than 60% of either disease group.
- The same source definition is fixed before expression values are read.
- All 16 frozen score/control genes and donor-level age, sex, source, diagnosis,
  and microglial yield are required.

The primary future report must show the existing frozen model and a model adding
source fixed effects. It must also report leave-one-source-out direction and
intervals. A source-adjusted failure is reported as source-sensitive; it cannot
be rescued by a favorable unadjusted result.

## Mechanical Preflight

Run:

```bash
.venv/bin/python scripts/v53_microglia_source_balance_preflight.py
```

The committed preflight verifies a balanced synthetic cohort passes, while
source-confounded, underpowered, sparse-source-cell, and source-concentrated
boundary fixtures fail. Synthetic fixtures are method tests only and are never
biological evidence. Current Macnair partitions
are included only to demonstrate the diagnosed design limitation; this addendum
governs the next donor-balanced acquisition.
