# Clean-Clone Newcomer Smoke Test V55

This is a point-in-time public-delivery and reproducibility check. It tests the
committed onboarding package as received from GitHub. It does not test human
comprehension, scientific validity, or clinical use. `[E01]`

## Test Boundary

- Source: public `origin/main`
- Commit tested: `96634e309bd4b87ff7a0506340910e167dce8dcb`
- Clone mode: shallow (`--depth 1`)
- Local project `.env`: not copied
- Test location: an untracked temporary directory outside the repository
- Date: 2026-07-26

No test read a quarantined cohort, called OpenGWAS, or changed a scientific
artifact.

## Results

| check | clean-clone result |
|---|---|
| Onboarding traceability/accessibility | PASS, 2,310/2,310 checks |
| Plain-language load | PASS, 43 documents, 0 undefined acronyms |
| Claim-source coverage | PASS, 33/33 bounded claims and 33/33 controlling artifacts |
| Core route depth | PASS, 17/17 routes |
| Heading and table semantics | PASS, 2,102/2,102 checks |
| Authored-artifact manifest | PASS, 90/90 artifact identities |
| Provenance segregation gate | PASS, 841/841 checks |
| Structural-prediction gate | PASS, 142/142 checks |
| Research-direction issue form | PASS, 10 elements, 9 unique inputs, all inputs required |
| Lightweight visuals | PASS, 8 SVG files present |
| Standalone collaborator brief | HTTP 200, `text/html` |
| Research-map visual | HTTP 200, `image/svg+xml` |
| Working tree after checks | Clean |

The local server was stopped after the two delivery checks. No smoke-test file
was added from the temporary clone.

## Commands Exercised

```bash
python3 scripts/v55_onboarding_audit.py --fail-on-error
python3 scripts/v55_plain_language_audit.py --fail-on-error
python3 scripts/v55_source_coverage.py --fail-on-error
python3 scripts/v55_route_depth_audit.py --fail-on-error
python3 scripts/v55_semantic_structure_audit.py --fail-on-error
python3 scripts/v55_onboarding_manifest.py --check --fail-on-error
python3 scripts/v47_provenance_gate.py audit --fail-on-error
python3 scripts/v51_structural_prediction_gate.py audit --fail-on-error
```

The issue-form schema and SVG count used read-only local checks. A temporary
local HTTP server delivered the HTML brief and research-map SVG, then exited.

## What This Establishes

At the tested commit, a new clone contains the expected onboarding artifacts,
their traceability contract, lightweight visuals, contributor form, and
maintenance checks without relying on the author's uncommitted workspace or
environment secrets.

## What This Does Not Establish

- It does not show that a newcomer chose the right route or understood it.
- It does not emulate every GitHub, browser, phone, or screen-reader rendering.
- It does not turn machine checks, model review, or clean delivery into
  scientific evidence.
- It does not replace the unrun
  [human comprehension pilot](COMPREHENSION_TEST_KIT.md).

Return to the [onboarding landing page](README.md) or the
[maintainer release checklist](MAINTAINER_RELEASE_CHECKLIST_V55.md).
