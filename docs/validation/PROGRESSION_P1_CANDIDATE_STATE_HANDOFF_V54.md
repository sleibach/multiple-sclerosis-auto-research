# V54 P1 Candidate-State Identity Handoff

Status: **verified pointer to the existing V53 score; no new score and no
progression finding**.

## Exact Identity

The only currently named P1 candidate state is the pre-existing V53
`CD44/CXCR4 receptor state`. Its controlling specification is
`docs/validation/MS_MICROGLIA_CD44_CXCR4_REPLICATION_SPEC_V53.md`.

- Genes: exactly `CD44` and `CXCR4`; no substitution.
- Input: provided normalized log expression or `log2(CPM + 1)` for counts.
- Formula: z-score each gene across all eligible cohort samples, then take the
  unweighted mean of the two gene z-scores.
- Repeated eligible samples: create the score at the specified sample level and
  apply the frozen donor/timepoint aggregation; do not select a sample after
  viewing disability outcomes.
- Missingness: unscoreable if fewer than half of the frozen genes are present;
  for this two-gene primary, both genes are therefore required.

The V53 disease-association model and replication thresholds do **not** transfer
to progression. A future P1 package uses the V54 frozen event-time endpoint,
covariate, control, information, and interpretation contracts. Only score
identity transfers.

## Compartment Boundary

The state was established in human microglia and the V53 specification requires
purified/sorted microglia or donor-level microglial pseudobulk with frozen
annotation. It is not licensed for PBMC, whole blood, CSF bulk, or another
compartment merely because `CD44` and `CXCR4` are measured. An incompatible
package fails closed rather than extrapolating the score.

The score has a replicated, quality-qualified MS disease-state association, but
V54 did not establish that it predicts disability progression, is component-
specific, is causal, has a favorable intervention direction, or is a target.

## Frozen Source Hashes

| artifact | SHA-256 |
|---|---|
| `docs/validation/MS_MICROGLIA_CD44_CXCR4_REPLICATION_SPEC_V53.md` | `160c7b855ce52a6d01b96f0fdb97ae9bf0a2ffb09ff20665b9d457d76df126e3` |
| `scripts/v53_analyze_macnair_microglia_replication.py` | `df923fbbb0dff4f7863e59e7a8dc5aa4d62a3900008976c3dc7ac19dcb2252ea` |
| `analysis/v53_ms_microglia_independent_cohort_scout/summary.json` | `4b40ea71bd3deee1c14fb0c705ad881e85d3e068be8399aac9b04c7faef65bae` |

Verify without reading any quarantined cohort:

```bash
.venv/bin/python scripts/v54_progression_candidate_state_reference.py
```
