# Arrival Command Packet: any_author_run_fallback

Status: route-specific operational packet. No scoring is authorized until
all required gates pass.

Role: `frozen_harness_local_author_run`
Access tier: `Tier2_low_barrier_author_execution`
Current blocker: `local_run_of_frozen_harness_plus_non_sensitive_aggregate_outputs`

## Hard Stop

Do not run module scoring, response metrics, or interpretation before the
route-specific receipt, checksum, terms, preflight, subject-map, label, and
addendum gates pass.

## First Actions

1. Save the returned aggregate package path.
2. Confirm the return contains aggregate outputs only.
3. Run:

```bash
.venv/bin/python scripts/v45_author_run_return_gate_runner.py run \
  --root <returned_aggregate_package_dir> \
  --package-state scored \
  --outdir analysis/v45_author_run_return_gate_runner/<cohort>_<date> \
  --fail-on-error
```

4. Fill the result report only if redaction and completeness both pass.
