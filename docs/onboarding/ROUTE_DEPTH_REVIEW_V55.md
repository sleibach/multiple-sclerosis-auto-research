# Newcomer Route-Depth Review V55

This maintenance review asks whether a newcomer can reach the essential pages
without hunting through the repository, and whether contribution endpoints
offer a clear next or return step. It tests links and path length, not human
comprehension or scientific validity. The linked pages still preserve the one
provisional monitoring lead and the no-target/no-progression boundary. `[M01,
M05, P02]`

## Measured Result

Run:

```bash
python3 scripts/v55_route_depth_audit.py --fail-on-error
```

Current result: `PASS`.

| measure | result |
|---|---:|
| Public Markdown documents in the route graph | 66 |
| Configured high-value routes | 17 |
| Routes within their hop limit | 17 |
| Failed or unreachable routes | 0 |
| Maximum permitted depth | 2 links |

The full shortest paths are in
`analysis/v55_route_depth_audit/route_depth.tsv`.

## What Is One Link From The Root

The public root page links directly to:

- the onboarding route chooser;
- the two-minute and layered explanation;
- the visual guide;
- all open problems;
- the submission guide;
- the repository tour; and
- the glossary.

Lead status cards and the post-submission lifecycle remain within two links.
This allows the root page to stay short while keeping both destinations
measurably near.

## The Contribution Loop

The shortest contribution route is:

```text
explanation -> open problem -> submission guide -> response lifecycle
```

Each step links directly to the next. The response lifecycle links back to the
problem board and submission guide, so a repair request does not strand the
contributor. Lead status cards link back to the route chooser and forward to
the problem board.

## Repairs Made

- Added the route chooser directly to the root README.
- Added submission, lifecycle, and landing-page links at the end of the open
  problem board.
- Added landing, problem-board, and explanation links after the lead inventory.
- Added the route-depth check to the secret-free onboarding workflow.

## What This Does Not Prove

A short path does not prove that labels are obvious, prose is understood, a
screen reader interaction is efficient, or a newcomer will choose the intended
route. Those questions require human testing with the
[comprehension kit](COMPREHENSION_TEST_KIT.md). This audit only prevents a
known navigation failure from silently returning.
