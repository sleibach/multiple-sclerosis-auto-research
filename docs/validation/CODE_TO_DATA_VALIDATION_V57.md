# Privacy-Preserving Code-to-Data Validation V57

Status: verified validation infrastructure. No external cohort was run and no
biological claim is made.

## Why This Method Exists

The existing author-run fallback allowed a data owner to run the frozen V42
harness locally, but the raw harness output directory contains
`paired_module_deltas.tsv` and participant-level attrition. A written request
not to return those files is weaker than preventing their export.

`scripts/v57_code_to_data_validation.py` makes the privacy boundary executable:

1. verifies SHA-256 hashes of itself and the frozen V42 harness against the
   committed collaborator-packet manifest;
2. installs a Python audit hook that denies socket and subprocess events while
   scoring;
3. runs the unchanged harness in an ephemeral private directory;
4. copies only a fixed aggregate allowlist;
5. converts participant-level attrition into counts and suppresses cells below
   five;
6. never exports `paired_module_deltas.tsv`;
7. writes `EXPORT_ATTESTATION.json` with pinned-code and exported-file hashes;
8. verifies the export before returning success.

This reduces dependence on transfer of politically or legally restricted data.
It does not make an aggregate-only result independently rerunnable. Until raw or
auditable execution access exists, a returned result has status
`AUTHOR_RUN_AGGREGATE_UNVERIFIED` and does not qualify as a project-grounded
finding.

## Data-Owner Command

Run the module-coverage precheck first. Then, from the checksum-verified packet:

```bash
.venv/bin/python scripts/v57_code_to_data_validation.py run \
  --expression <local_expression.tsv> \
  --metadata <local_sample_metadata.tsv> \
  --outdir <new_empty_aggregate_export_dir> \
  --expression-type auto
```

The output directory must be new or empty. Input paths and identifiers are not
written to the export; only input hashes are recorded.

For the strongest operating-system boundary, execute the verified packet in an
institution-controlled disconnected environment or a container launched with
network disabled. The Python audit hook is a second, fail-closed application
control; it is not represented as a substitute for host isolation.

## Receiver Verification

```bash
.venv/bin/python scripts/v57_code_to_data_validation.py verify-export \
  --outdir <returned_aggregate_export_dir> \
  --fail-on-error

.venv/bin/python scripts/v45_author_run_return_gate_runner.py run \
  --root <returned_aggregate_export_dir> \
  --package-state scored \
  --outdir <receipt_gate_dir> \
  --fail-on-error
```

Passing verifies code/output integrity and the aggregate boundary. It does not
determine the scientific interpretation, which remains frozen by
`docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md`.

## Synthetic Verification

```bash
.venv/bin/python scripts/v57_code_to_data_validation.py synthetic-check \
  --outdir analysis/v57_code_to_data_validation
```

The committed test uses only V42 synthetic planted-signal input. It requires:

- a valid aggregate export to pass;
- an altered metric file to fail its hash check;
- a deliberately leaked participant table to fail;
- no participant-level score table in the valid export;
- the existing redaction, completeness, and aggregate-schema gates to pass on
  the valid export.

Synthetic behavior characterizes the method only. It is not evidence about MS,
the V22 signal, or any treatment.
