# Wave132 GPR183 Post-Wave130 Closure

## Bottom Line

Branch call: `NO_REOPEN_GPR183_AFTER_POST_WAVE130_AUDIT`.

Wave83 parked GPR183/EBI2 as a forcing route, but later forcing tests do not
promote it. Wave111 had no matched-donor spatial-proxy rows, Wave112 found zero
coherent compartment signals across diseases, and Wave130 did not rescue the
lipid-lysosomal MS treatment-response context.

## Decision Row

| route | branch_call | wave83_call | wave93_call | wave111_branch_call | wave112_branch_call | wave112_coherent_compartment_diseases | wave130_lipid_lysosomal_ms_response_rescue | critical_failures |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPR183_EBI2_OXYSTEROL_NICHE | NO_REOPEN_GPR183_AFTER_POST_WAVE130_AUDIT | PARK_INTERVENTION_CLASS_NEEDS_FORCING_TEST | ROW_PRESENT_NO_PROMOTIONAL_CALL | NO_REOPEN_GPR183_SPATIAL_PROXY | NO_REOPEN_GPR183_COMPARTMENT_FALLBACK | 0 | False | wave93_target_forcing_promoted;wave111_spatial_proxy_reopened;wave112_coherent_compartment_diseases_ge2;wave130_lipid_lysosomal_ms_response_rescue |

## Reproducibility

- Script: `scripts/v3_wave132_gpr183_post_wave130_closure.py`
- Output: `results_v3/wave132_gpr183_post_wave130_closure/`
- Seed: `20260527`
