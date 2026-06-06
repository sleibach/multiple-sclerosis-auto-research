# Wave137 GPR183 Ligand-Axis Fair Closure

## Bottom Line

Branch call: `NO_REOPEN_GPR183_FAIR_CLOSURE`.

This wave corrects the interpretation of Wave111: zero matched spatial-proxy
pairs is missing evidence, not negative evidence. Even with that correction,
GPR183 does not reopen because the weak compartment fallback has zero coherent
compartment diseases and Wave135 shows no cross-dataset MS PBMC ligand-axis
replication.

## Evidence Classes

```json
{
  "external_response_support": "MIXED_SUPPORTIVE",
  "matched_spatial_proxy": "MISSING_NOT_NEGATIVE",
  "ms_pbmc_gpr183_gene_response": "NO_CROSS_MS_REPLICATION",
  "ms_pbmc_ligand_axis_response": "NO_CROSS_MS_REPLICATION",
  "weak_compartment_contrast": "NEGATIVE"
}
```

## Gate Matrix

| Gate | Passed |
| --- | --- |
| do_not_count_missing_spatial_as_negative | True |
| coherent_compartment_signal_ge2_diseases | False |
| external_response_support_ge2_systems | True |
| ms_ligand_axis_cross_dataset_signal | False |
| ms_gpr183_gene_cross_dataset_signal | False |
| wave83_route_not_blocked | False |
| wave93_promoted | False |

## Interpretation

The fair statement is narrow: matched spatial evidence is unavailable here; the
available fallback and MS treatment-response tests do not support promotion.
This keeps GPR183 closed without converting missing spatial data into a stronger
negative claim than the data justify.
