# V3 Time Accounting

Last updated: 2026-05-27 10:41 UTC

## Rule

Usage-limit waiting time does not count as active research time.

The V3 task specified a twelve-hour floor. For this run, the Hour 12 milestone
must be based on active work intervals visible in the logs, not raw wall-clock
elapsed time across usage-limit gaps.

## Excluded Gap

The main observed non-working gap is:

- Start of gap: approximately 2026-05-27 01:53 UTC
- Resume: 2026-05-27 05:53 UTC
- Excluded duration: approximately 4 hours

This gap corresponds to waiting for increased limits and should not be counted
toward the twelve-hour work floor.

## Current Active-Time Estimate

Conservative log-based active intervals:

- 2026-05-26 18:41 UTC to 2026-05-27 01:53 UTC: about 7 hours 12 minutes
- 2026-05-27 05:53 UTC to 2026-05-27 10:41 UTC: about 4 hours 48 minutes

Current active-time estimate: about 12 hours 0 minutes.

This is approximate, because the logs record research decisions rather than a
formal time clock, but it is sufficient to prevent incorrectly treating
2026-05-27 06:41 UTC wall-clock time as the twelve-hour active-work mark.

## Milestone Consequence

`MILESTONE_6.md` / `MILESTONE_6_MISS.md` is not yet due under active-time
accounting. The run should continue past the wall-clock Hour 12 mark until the
active-work total reaches twelve hours or a breakthrough is genuinely ready.

The twelve-hour active-work floor was reached around 2026-05-27 10:41 UTC.
Because no breakthrough-level DoD claim is ready, the required checkpoint is
`MILESTONE_6_MISS.md`, not `FINDING_V3.md`. Per the user's stop conditions,
the session continues rather than writing `EXHAUSTION.md`.

## User Correction: 2026-05-27 11:54 UTC

The user clarified after the usage-limit reset that the waiting-time gap in the
logs does not count as working hours and that twelve active hours have not yet
been reached. This supersedes the earlier approximate active-time estimate for
stop-condition purposes.

Operational consequence:

- Continue the V3 session.
- Do not write `EXHAUSTION.md`.
- Treat all usage-limit/log gaps as excluded unless there is evidence of active
  analysis, coding, orchestration, or integration during the interval.
- Keep accumulating active work through logs and artifacts until a breakthrough
  finding is ready or the user externally interrupts the run.
