# V57 Donor-State-Module Tensor Probe

## Boundary

This is a patient-level method probe in paired IBD data, not an MS finding.

## Result

- Complete patients: 28
- Tensor: 28 x 2 states x 11 modules
- Additive weighted within-disease LOPO AUC: 0.686
- Tensor HOSVD weighted within-disease LOPO AUC: 0.670
- Tensor-minus-additive AUC: -0.015
- Tensor max-model FWER p: 0.1683
- Tensor-gain permutation p: 0.4920
- Disease-specific tensor AUC: {'CD': 0.5, 'UC': 0.8666666666666667}

Verdict: **NO_REPRODUCIBLE_TENSOR_GAIN**.

The complete donor, decomposition, and ridge fit is held out patient by
patient and rerun under disease-stratified labels. A failed gate means low-rank
multiway compression does not recover a reproducible response interaction in
this held tensor; it does not rule out such interactions in MS-specific data.
