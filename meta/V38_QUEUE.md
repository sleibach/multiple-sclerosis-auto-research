# V38 Queue - Four-Hour Autonomous Block

## Timing

- Block start UTC: 2026-06-08T20:30:23Z
- Target end UTC: 2026-06-09T00:30:23Z
- Timing source: real `date -u` system-clock reads.

## Integrity Rules

- Mode: unconventional question generation with unchanged evidence gate.
- No model/RPT output is evidence; it only prioritizes grounded tests.
- No locked-rule edits.
- OpenGWAS POST only; token expires 2026-06-19 and is near enough to flag.
- Commit each clean iteration.

## Backlog

| Priority | Workstream | Item | Status | Resume Note |
|---:|---|---|---|---|
| 1 | B | Adversarial inversion of bounded V22/V23 monitoring signal | in-progress | Construct strongest artifact/inversion cases and ground on held V22/V23/V28/V32 data. |
| 2 | A | Failure-structure meta-analysis across killed/closed leads | done | V37 closed/negative frame analyzed: dominant families are evidence-resolution failure (7/20), context/axis dependence (5/20), direction/modality constraint (5/20), and specificity/control failure (4/20). |
| 3 | E | RPT-led structured mining over V37 score table and lead matrices | done | RPT matched 5/6 masked V37 action classes; only contradiction was bounded scalar predicted as data-gated follow-up, sharpening operational-priority wording without evidence demotion. |
| 4 | C | Unpublishable-but-true exclusion/non-replication list | done | Ledger written with 16 exclusions/non-replications: 13 negative-established, 2 supported exclusions, 1 data-gated not-established. |
| 5 | D | Cross-scale/control-systems reframing | todo | Test whether held module data support set-point/feedback interpretations beyond scalar scores. |

## Iteration Log

### Iteration 1

- Start UTC: 2026-06-08T20:30:23Z
- Resume UTC after interruption: 2026-06-09T04:16:56Z
- End UTC: 2026-06-09T04:21:54Z
- Status: completed
- Item selected: Workstream B, adversarial inversion of the bounded monitoring
  signal.
- Planned grounding: verify environment/tooling, read V37/V28/V32/V22/V23
  artifacts, build artifact/inversion tests from existing summary tables, and
  write the first V38 report section.
- Result: OpenGWAS verified HTTP 200; token expires `2026-06-19 12:28 UTC`.
  Gemini, Claude, and RPT smoke-passed. Claude/Gemini generated proposal-only
  inversion candidates. Grounding in `scripts/v38_adversarial_monitoring_inversion.py`
  showed adversarial inversion narrows but does not kill the V37 scalar claim:
  bounded AUC `0.811` vs primary-all AUC `0.547`; DMF-only AUC `0.720`, exact
  p `0.155`; exact tofacitinib-only AUC `0.950`, exact p `0.0159`; V32
  immune-tone adjustment AUC `0.656`, p `0.163`; threshold transfer weak
  (`0.667` and `0.600` accuracy). Report updated in
  `docs/history/UNCONVENTIONAL_FINDINGS_V38.md`.

### Iteration 2

- Start UTC: 2026-06-09T04:22:36Z
- End UTC: 2026-06-09T04:24:43Z
- Status: completed
- Item selected: Workstream A, failure-structure meta-analysis across
  killed/closed leads.
- Planned grounding: use `docs/reports/FINDINGS_SCORES_V37.tsv` as the
  closed/negative item frame, annotate failure modes from committed artifact
  summaries, count recurrent structures, and update the V38 report.
- Result: `scripts/v38_failure_structure_meta.py` analyzed 20 V37
  closed/negative/decoupling items. There is no single universal failure law.
  Dominant families: evidence-resolution failure `7/20`, context/axis
  dependence `5/20`, direction/modality constraint `5/20`, specificity/control
  failure `4/20`. V38 report updated.

### Iteration 3

- Start UTC: 2026-06-09T04:25:16Z
- End UTC: 2026-06-09T04:27:45Z
- Status: completed
- Item selected: Workstream E, RPT-led structured mining over V37 score table
  and V38 failure-mode annotations.
- Planned grounding: construct a compact tabular payload from V37/V38 tables,
  let RPT classify masked rows, then compare RPT-surfaced patterns against
  actual scored-table/failure-family counts.
- Result: `scripts/v38_rpt_structural_mining.py` built a V37/V38 feature table
  and masked six edge items. RPT matched the artifact-derived action class for
  `5/6` rows. The single contradiction was the bounded scalar, predicted as
  `data_gated_followup` rather than `external_validation_priority`, reinforcing
  that its priority is operational/clinical and not evidence-grade inflation.

### Iteration 4

- Start UTC: 2026-06-09T04:28:25Z
- End UTC: 2026-06-09T04:29:59Z
- Status: completed
- Item selected: Workstream C, unpublishable-but-true exclusion and
  non-replication ledger.
- Planned grounding: extract negative-established and supported exclusion
  statements from V37/V38 tables and source artifacts; distinguish rigorous
  exclusions from merely data-gated unknowns.
- Result: `scripts/v38_exclusion_ledger.py` wrote 16 decision-useful
  exclusions/non-replications. Counts: 13 negative-established, 2 supported
  exclusions, 1 data-gated not-established. V38 report updated.
