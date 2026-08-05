# ToleDYNAMIC Functional-Endpoint Mapping Gate V56

Purpose: prevent outcome-driven endpoint selection among flow, phagocytosis,
ROS, cytokine, and Seahorse outputs. This gate fixes variable mappings before
assay or clinical values are read; it produces no treatment or biological
evidence.

## Frozen Families

1. myelin phagocytosis: one primary endpoint;
2. monocyte CD64: one primary endpoint;
3. reactive oxygen species: one primary endpoint;
4. metabolism: basal and spare respiration as one two-endpoint family; and
5. inflammatory cytokines: one SAP-designated primary summary.

Unavailable or ambiguously defined families remain `DESCRIPTIVE_UNAVAILABLE` or
`DESCRIPTIVE_ONLY`; they cannot be rescued by selecting the best observed
variable. The cytokine family specifically requires an SAP-designated summary.

## Command

```bash
python3 scripts/v56_toledynamic_functional_mapping_gate.py run \
  <controlled-workspace>/functional_endpoint_mapping.tsv \
  --outdir <controlled-workspace>/functional_mapping_gate \
  --fail-on-block
```

Every available row requires a source variable, source document and locator,
unit, mapping basis, and a pre-value expected direction (`increase`, `decrease`,
or `two_sided`). Any declaration that values were read before mapping blocks the
entire map. `TEST_ELIGIBLE` means only that a later corrected test is defined;
it does not mean the endpoint changed or anchors a transcript effect.

## Synthetic Verification

```bash
python3 scripts/v56_toledynamic_functional_mapping_gate.py synthetic-check \
  --outdir analysis/v56_toledynamic_functional_mapping_gate \
  --fail-on-error
```

The deterministic fixtures cover a complete blinded map, an unavailable
cytokine family, mapping after values were read, and a duplicate endpoint role.
All inputs and results are synthetic method checks, never MS evidence.
