# V55 Onboarding Maintainer Release Checklist

This checklist maintains a communication layer derived from existing evidence.
It does not authorize a scientific status change. Hashes, passing checks, and
clear prose cannot turn a provisional or outside-source statement into a
grounded result. `[E01-E03]`

## 1. Classify The Change Before Editing

| change type | first action | evidence consequence |
|---|---|---|
| Wording, layout, or navigation only | Keep existing claim IDs and source rows. | None. Meaning and status must remain unchanged. |
| New onboarding page or visual | Map every scientific statement to existing claim IDs before drafting. | None unless the source contract itself is legitimately updated. |
| Controlling scientific artifact changed | Review its row in `ONBOARDING_CLAIM_SOURCES_V55.tsv`, then inspect every dependent page via `artifact_coverage.tsv`. | May require narrower or different wording; never infer an upgrade from file recency. |
| New project-grounded result | Complete the scientific workflow outside V55 first; update authoritative findings/status before onboarding. | Onboarding follows the new source state; it does not create it. |
| Outside-source context added | Keep it in `knowledge_external/` with source/class provenance. | Context only; cannot support a project conclusion. |
| Locked rule or preregistration implicated | Stop and verify immutability. | No retroactive tuning or threshold change is permitted. |

## 2. Preserve These Release Invariants

- One live clinical route is still described as a **provisional monitoring
  signal**, never a target, selector, clinical tool, cure, or progression
  measure. `[M01, M05]`
- No intervention-grade target or established progression marker, mechanism,
  treatment effect, or halt strategy is implied. `[P01-P02]`
- Negative, demoted, closed, inconclusive, unscoreable, and data-blocked states
  remain visible and distinct.
- Missing compatible data are not translated into absent biology.
- Outside-source and model material cannot be cited as project evidence.
- Predicted structure remains prediction context with confidence attached.
- Synthetic results describe method behavior only.
- Locked rules and preregistrations are not edited to improve a result.
- No secret, raw returned package, patient-identifiable material, model weight,
  tracked `tmp/` path, or tracked file over 50 MB enters the release.

## 3. Update In The Right Order

For an evidence-affecting source change:

1. Update the authoritative finding/report/status through the scientific
   process, not through onboarding.
2. Update the corresponding row in
   `docs/onboarding/ONBOARDING_CLAIM_SOURCES_V55.tsv`.
3. Run `scripts/v55_source_coverage.py` and inspect
   `analysis/v55_source_coverage/artifact_coverage.tsv` for all affected pages.
4. Update every affected page, visual text equivalent, brief, glossary entry,
   and forbidden-overread warning.
5. Re-run human and machine checks below.

For wording/layout only, begin at step 4 and keep claim rows unchanged.

## 4. Human Review

Read, do not only lint:

- [ ] The two-minute route still yields the candid bottom line.
- [ ] The root and onboarding first screen state one provisional monitor, no
      target/progression result, and the research-only/no-private-data boundary
      before long navigation or history.
- [ ] The one-page brief still leads with one provisional monitor, no target,
      no progression result, and the exact data moves.
- [ ] Closed and negative routes remain as prominent as positive context.
- [ ] Every simplification retains its material caveat.
- [ ] Each visual's text equivalent carries the complete meaning.
- [ ] Dense visuals are not claimed to be directly readable when shrunk.
- [ ] The print brief has no clipping, overlap, tiny body text, or lost status
      color labels.
- [ ] A newcomer can reach source artifacts without treating onboarding as the
      authority.
- [ ] An idea contributor can find prediction, data, null/holdout, confound,
      correction, and drop-rule fields.
- [ ] The direct research-direction form still opens the pushed 10-element
      contract, and no authenticated visual render is claimed unless checked.
- [ ] No patient-specific guidance or medical advice was introduced.

## 5. Required Machine Checks

Run from the repository root:

```bash
python3 scripts/v55_onboarding_audit.py --fail-on-error
python3 scripts/v55_onboarding_audit.py --synthetic-check --fail-on-error
python3 scripts/v55_plain_language_audit.py --fail-on-error
python3 scripts/v55_source_coverage.py --fail-on-error
python3 scripts/v55_route_depth_audit.py --fail-on-error
python3 scripts/v55_semantic_structure_audit.py --fail-on-error
python3 scripts/v55_visual_render_regression.py --fail-on-error
python3 scripts/v55_responsive_visual_audit.py --fail-on-error
python3 scripts/v55_print_brief_audit.py --fail-on-error
python3 scripts/v47_provenance_gate.py audit --fail-on-error
python3 scripts/v51_structural_prediction_gate.py audit --fail-on-error
python3 scripts/v55_onboarding_manifest.py --write --fail-on-error
python3 scripts/v55_onboarding_manifest.py --check --fail-on-error
```

Then inspect:

```bash
git diff --check
git status --short
git ls-files | rg '(^|/)tmp/'
git ls-files -z | xargs -0 du -k | awk '$1 > 51200 {print}'
```

Expected last two outputs: no tracked temporary paths and no tracked file above
50 MB.

Check the dated [link-and-label review](LINK_AND_LABEL_REVIEW_V55.md) when an
external destination or contribution link changes. HTTP availability is a
point-in-time delivery check, not an evidence check.

## 6. Visual And Print Verification

The browser checks prove rendering, dimensions, fit, and one-page output. They
do not prove visual quality.

For every changed SVG:

1. render at native size;
2. inspect text clipping, overlap, arrow/card alignment, status labels, and
   contrast;
3. confirm the visible text equivalent still matches;
4. inspect at the constrained-width fallback route; and
5. remove all temporary screenshots.

For a changed print brief, create a temporary A4 PDF, confirm exactly one page,
render it to an image, inspect it, and delete both files. Never commit the
rendered PDF or preview.

## 7. Refresh The Artifact Manifest

Run:

```bash
python3 scripts/v55_onboarding_manifest.py --write --fail-on-error
```

The outputs are:

- `analysis/v55_onboarding_manifest/artifact_manifest.tsv`
- `analysis/v55_onboarding_manifest/artifact_manifest_summary.json`

The manifest covers authored onboarding documents, visuals, templates,
contribution surfaces, V55 maintenance scripts, root navigation, and resume
state. It records role, size, and SHA-256 identity. It deliberately excludes
generated audit outputs from its input set so platform-specific browser
fingerprints do not make the authored-artifact manifest unstable.

A matching hash means “this is the reviewed file,” not “the scientific content
is true.”

## 8. Clean-Clone Release Smoke Test

Before a public onboarding release, repeat the
[clean-clone smoke test](CLEAN_CLONE_SMOKE_TEST_V55.md) from pushed
`origin/main`, not the author's workspace:

1. make a shallow clone in an untracked temporary directory;
2. run every required machine check and manifest `--check` without a local
   `.env`;
3. verify the issue-form schema and eight lightweight SVGs;
4. serve the standalone HTML brief and one SVG to confirm delivery/MIME type;
5. confirm the clone remains clean; and
6. remove the temporary clone.

Record the tested commit. A clean clone proves delivery independence, not
human comprehension or scientific validity.

## 9. Human-Pilot Status

- [ ] State whether a real comprehension/idea-production pilot ran.
- [ ] If not run, say so; model and machine audits do not substitute.
- [ ] If recruiting, use the
      [recruitment handoff](HUMAN_PILOT_RECRUITMENT_HANDOFF.md).
- [ ] If run, use private copies of the scorecard and
      [session capture sheet](templates/HUMAN_PILOT_SESSION_CAPTURE_V55.md),
      collect no health/identity data, and report route-comparable aggregate
      documentation outcomes only.
- [ ] Include: “This was a documentation test, not scientific validation.”

## 10. Commit And Push

- [ ] Review `git diff --cached` for accidental scientific status changes.
- [ ] Confirm no `.env` content, token, credential, raw returned package, or
      temporary render is staged.
- [ ] Commit one coherent maintenance iteration.
- [ ] Push with `git push origin main`.
- [ ] Do not force a rejected push; surface repository desynchronization.
- [ ] Confirm `git status -sb` shows local `main` aligned with `origin/main`.

## 11. Release Note Template

```text
Communication change:
Pages/visuals changed:
Scientific status changed: no / yes (controlling artifact and claim rows)
Negatives and boundaries rechecked:
Human visual/print review:
Onboarding/plain/source/route/semantic/render/responsive/print checks:
Provenance/structure gates:
Manifest refreshed:
Clean-clone check and tested commit:
Human-pilot status:
Large-file/tmp guard:
Commit and push:
Residual accessibility/comprehension limits:
```

If “scientific status changed” is `yes` but there is no new authoritative
scientific artifact outside onboarding, the release is not ready.

Continue with the [final drift and safety review](FINAL_DRIFT_AND_SAFETY_REVIEW_V55.md)
or return to the [onboarding landing page](README.md).
