# Author-Run Redaction Precheck V45

Status: governance and handoff-readiness check. No validation is run by this
script, and no biological claim is made.

Script:

`scripts/v45_author_run_redaction_precheck.py`

Purpose: scan collaborator-returned author-run aggregate packages for obvious
redaction risks before the package is treated as handoff-complete. This is the
gate that catches files or columns that look like raw expression matrices,
sample-level clinical labels, private correspondence, signed agreements, or
credentials.

## Why This Exists

The author-run fallback is designed for cases where individual-level data cannot
leave the source institution. A returned package should contain only
non-sensitive aggregate harness outputs. If raw expression, patient labels,
private correspondence, or credentials appear in a package, stop and repair the
package before any completeness or interpretation step.

## Command

For a returned package:

```bash
.venv/bin/python scripts/v45_author_run_redaction_precheck.py check \
  --root <returned_aggregate_package_dir> \
  --outdir analysis/v45_author_run_redaction_precheck/<cohort>_<date> \
  --fail-on-error
```

Synthetic regression:

```bash
.venv/bin/python scripts/v45_author_run_redaction_precheck.py synthetic-check \
  --outdir analysis/v45_author_run_redaction_precheck
```

Current synthetic verification:

- complete synthetic aggregate package: `PASS`, `0` block findings across `9` files;
- deliberate risky synthetic package: `FAIL`, `3` block findings across `12` files.

The risky synthetic package contains only synthetic test files, but it is shaped
to resemble the leak classes the project must block: raw expression matrix,
clinical labels, and private email text.

## Block Classes

The precheck blocks on:

- raw expression/count/matrix-looking filenames;
- sample/subject/patient map, metadata, label, or ID filenames;
- clinical/NEDA/EDSS/relapse/response label filenames;
- private correspondence, agreement, or email-looking filenames/text;
- credential, token, secret, password, `.env`, or private-URL markers;
- columns that look like individual identifiers or individual clinical labels.

Unexpected files that do not match a block pattern are marked `WARN` and require
manual review.

## Required Order

For author-run aggregate returns:

1. Run this redaction precheck.
2. Only if it passes, run `scripts/v45_author_run_output_check.py`.
3. Only if completeness passes, fill the V45 result report template.
4. Interpret under the pre-registered outcome grid.

If this precheck fails, do not commit or interpret the package. Request a
redacted aggregate-only return.
