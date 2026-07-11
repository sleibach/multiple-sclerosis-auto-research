# V53 Cross-Disease Summary Lineage Audit

Verdict: **CROSS_DISEASE_SUMMARY_IS_DESCRIPTIVE_DERIVED_ATLAS_NOT_FIFTH_INDEPENDENT_MODALITY**.

The V26 matrix rebuilds exactly (maximum error `2.22e-16`). It is
derived from `170` source rows across `15` dataset
labels and `10` diseases. `108` rows
(`63.5%`) reuse the direct-h5ad cell-state analyses already
represented in V26's cell-state matrix; the remaining rows come from GSE111972,
GSE248205, and GSE315138.

The matrix's six rows are support counts and positive-effect summaries computed
from those source rows. They are not independent observations, and correlating
module columns across those six derived metrics does not create a new modality.
The cross-disease matrix remains useful as a descriptive atlas but is retired as
independent corroboration of the coupled two-arm architecture.

A full disjoint rebuild cannot be obtained from the aggregate matrix. The reused
direct-h5ad component is already de-overlapped in V53; the three additional atlases
would require source-level rescoring. That work may test broad recurrence, but it
cannot make this derived summary an independent fifth modality.
