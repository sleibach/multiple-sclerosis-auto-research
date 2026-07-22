# V54 Progression Reference-Design Manifest

Status: machine-readable operational contract. It consolidates existing V54
decisions and changes no locked rule, pre-registration, endpoint, or threshold.

## Purpose

`analysis/v54_progression_reference_manifest/manifest.json` is the canonical
machine description of the prospective progression route. It binds:

- the stress-tested reference counts and assumptions;
- eight executable blind gates and their permitted decisions;
- package lifecycle transitions from quarantine through frozen-analysis
  handoff;
- explicit forbidden fields and interpretation boundaries;
- SHA-256 digests of every source document and script.

The manifest is deliberately drift-detecting. The consolidated regression
suite runs verification mode; changing a bound source causes failure until the
manifest is intentionally regenerated and reviewed.

## Commands

Create or intentionally refresh the committed manifest:

```bash
.venv/bin/python scripts/v54_progression_reference_manifest.py --write
```

Verify it without changing it:

```bash
.venv/bin/python scripts/v54_progression_reference_manifest.py --verify
```

The two-case synthetic regression verifies that the current document passes
and a threshold-tampered copy fails. Synthetic behavior is method validation,
not biological evidence.

## Boundary

Reference alignment is not eligibility, validation, association, treatment
effect, target evidence, or proof that an intervention halts MS. A package can
advance only through the separately frozen gates; the manifest cannot waive a
failure or infer a missing field.
