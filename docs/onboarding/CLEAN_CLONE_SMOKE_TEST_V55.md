# Clean-Clone Newcomer Smoke Test V55

This is a point-in-time public-delivery and reproducibility check. It tests the
committed onboarding package as received from GitHub. It does not test human
comprehension, scientific validity, or clinical use. `[E01]`

## Test Boundary

- Source: public `origin/main`
- Commit tested: `5fca1cf800e7340b95a3acd7af7aaba433ba5307`
- Clone mode: shallow (`--depth 1`)
- Local project `.env`: not copied
- Test location: an untracked temporary directory outside the repository
- Date: 2026-07-26

No test read a quarantined cohort, called OpenGWAS, or changed a scientific
artifact.

## Results

| check | clean-clone result |
|---|---|
| Onboarding traceability/accessibility | PASS, 2,487/2,487 checks |
| Synthetic onboarding fault detector | PASS, all 11 fixtures behaved as expected |
| Plain-language load | PASS, 43 documents, 0 undefined acronyms |
| Claim-source coverage | PASS, 33/33 bounded claims, 33/33 controlling artifacts, 44 reader documents |
| Core route and public graph | PASS, 17/17 routes and 73/73 connected public documents |
| Heading and table semantics | PASS, 2,291/2,291 checks |
| Lightweight public package | PASS, 84 files and 731,734 bytes; no file over 512 KiB |
| Authored-artifact manifest | PASS, 100/100 artifact identities |
| Provenance segregation gate | PASS, 841/841 checks; four synthetic cases behaved as expected |
| Structural-prediction gate | PASS, 142/142 checks; five synthetic cases behaved as expected |
| Browser rendering | PASS, 49/49 checks across eight SVGs; no raster retained |
| Constrained-width delivery | PASS, 74/74 checks; all 24 small-label scenarios have required text equivalents |
| One-page print brief | PASS, 26/26 checks and one page; no PDF retained |
| Working tree after every check reran | Clean (`DIRTY_COUNT=0`) |

Two earlier fresh-clone runs were also useful failures. They exposed absolute
checkout paths in generated reports and a nondeterministic exact temporary-PDF
byte count. Both generators were repaired before this final run. A same-machine
pass without the clean-tree criterion would not have found those defects. No
smoke-test file or temporary render was added from the clone.

## Commands Exercised

```bash
python3 scripts/v55_onboarding_audit.py --fail-on-error
python3 scripts/v55_onboarding_audit.py --synthetic-check --fail-on-error
python3 scripts/v55_plain_language_audit.py --fail-on-error
python3 scripts/v55_source_coverage.py --fail-on-error
python3 scripts/v55_route_depth_audit.py --fail-on-error
python3 scripts/v55_semantic_structure_audit.py --fail-on-error
python3 scripts/v55_public_package_footprint.py --fail-on-error
python3 scripts/v47_provenance_gate.py synthetic-check \
  --outdir analysis/v47_provenance_gate --fail-on-error
python3 scripts/v47_provenance_gate.py audit --fail-on-error
python3 scripts/v51_structural_prediction_gate.py synthetic-check \
  --outdir analysis/v51_structural_prediction_gate --fail-on-error
python3 scripts/v51_structural_prediction_gate.py audit --fail-on-error
python3 scripts/v55_visual_render_regression.py --fail-on-error
python3 scripts/v55_responsive_visual_audit.py --fail-on-error
python3 scripts/v55_print_brief_audit.py --fail-on-error
python3 scripts/v55_onboarding_manifest.py --check --fail-on-error
git status --porcelain
```

The test used the public remote, no local `.env`, and the system browser. All
generated output was compared with the committed tree through the final status
check.

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
