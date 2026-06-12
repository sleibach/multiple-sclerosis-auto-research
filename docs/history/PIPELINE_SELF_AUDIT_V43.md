# PIPELINE SELF-AUDIT V43

Status: synthetic-null method audit only. This does not create or refute a biological MS finding.

## Synthetic Null Design

- Loaded the V41 entity-by-modality evidence matrix and held-out split.
- Generated synthetic null corpora by shuffling support z-scores within each training modality, preserving modality coverage and score distribution.
- Generated recurrence nulls by randomizing positive source-unit entity assignments while preserving the number of source units and entity vocabulary.
- Null replicates: `5000`.

## Joint-Inference Calibration

- Real V41 `apc_hla_ifn_monitoring` train joint z: `8.0548`.
- Synthetic-null max joint z 95th percentile: `8.1547`.
- Synthetic-null max joint z 99th percentile: `8.5299`.
- Empirical FWER p for the real joint z against V43 null: `0.0706`.
- Entity-specific empirical p for the real joint z against the shuffled APC-entity null: `0.0018`.

Interpretation: the real central joint score is strong for the named APC entity, but it sits near the family-wise maximum tail expected when many entities/modalities are searched. That supports the V41 conclusion: the signal is repeatable and known-context, not a license for unconstrained new discovery.

## Recurrence Calibration

- Real V41 top recurrence: `78` positive source units.
- Synthetic-null max recurrence 95th percentile: `12.0`.
- Synthetic-null max recurrence 99th percentile: `13.0`.
- Empirical FWER p for real recurrence against V43 null: `0.0002`.

Interpretation: the recurrence result is far outside this synthetic-null structure and is the stronger methodological corroboration of the central APC-axis recurrence. It still remains prior-known/validation-gated biological context, not a new intervention claim.

## Machine-Readable Outputs

- `analysis/v43_method_validation/synthetic/pipeline_null_replicates.tsv.gz`
- `analysis/v43_method_validation/pipeline_self_audit_summary.json`
