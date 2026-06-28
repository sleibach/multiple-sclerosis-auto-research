#!/usr/bin/env python3
"""V50 status freshness linter.

This linter checks that public landing/status files point to the live V50 queue
and do not retain stale "current phase" or OpenGWAS-validity wording.

It is a navigation/status control only. It does not evaluate biological claims.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis" / "v50_status_freshness_linter"


@dataclass(frozen=True)
class Check:
    check_id: str
    file: str
    status: str
    detail: str


def latest_queue_phase(meta_dir: Path) -> str:
    phases: list[int] = []
    for path in meta_dir.glob("V*_QUEUE.md"):
        match = re.fullmatch(r"V(\d+)_QUEUE\.md", path.name)
        if match:
            phases.append(int(match.group(1)))
    if not phases:
        raise RuntimeError("No meta/V*_QUEUE.md files found")
    return f"V{max(phases)}"


def read_rel(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def add_contains(checks: list[Check], rel: str, text: str, needle: str, check_id: str) -> None:
    status = "PASS" if needle in text else "FAIL"
    checks.append(Check(check_id, rel, status, f"expected substring: {needle!r}"))


def add_not_contains(
    checks: list[Check], rel: str, text: str, needle: str, check_id: str
) -> None:
    status = "PASS" if needle not in text else "FAIL"
    checks.append(Check(check_id, rel, status, f"forbidden substring: {needle!r}"))


def run_checks(expected_phase: str) -> list[Check]:
    checks: list[Check] = []
    readme = read_rel("README.md")
    current = read_rel("meta/CURRENT_STATUS.md")
    next_actions = read_rel("meta/NEXT_ACTIONS.md")

    add_contains(
        checks,
        "README.md",
        readme,
        f"The current live operational phase is **{expected_phase}**",
        "readme_current_phase",
    )
    add_contains(
        checks,
        "README.md",
        readme,
        f"meta/{expected_phase}_QUEUE.md",
        "readme_live_queue_pointer",
    )
    add_not_contains(
        checks,
        "README.md",
        readme,
        "The current phase is **V43**",
        "readme_no_v43_current_phrase",
    )

    add_contains(
        checks,
        "meta/CURRENT_STATUS.md",
        current,
        f"{expected_phase} is the current live operational phase",
        "current_status_current_phase",
    )
    add_contains(
        checks,
        "meta/CURRENT_STATUS.md",
        current,
        f"meta/{expected_phase}_QUEUE.md",
        "current_status_live_queue_pointer",
    )
    add_contains(
        checks,
        "meta/CURRENT_STATUS.md",
        current,
        "JWT expired at `2026-06-19T12:28:39Z`",
        "current_status_opengwas_expired",
    )
    for forbidden in (
        "JWT valid until",
        "near-expiry",
        "token valid until",
        "OpenGWAS access works when `.env` is loaded explicitly",
    ):
        add_not_contains(
            checks,
            "meta/CURRENT_STATUS.md",
            current,
            forbidden,
            f"current_status_no_stale_{re.sub(r'[^a-z0-9]+', '_', forbidden.lower()).strip('_')}",
        )

    add_contains(
        checks,
        "meta/NEXT_ACTIONS.md",
        next_actions,
        f"{expected_phase} update:",
        "next_actions_current_block",
    )
    add_contains(
        checks,
        "meta/NEXT_ACTIONS.md",
        next_actions,
        f"meta/{expected_phase}_QUEUE.md",
        "next_actions_live_queue_pointer",
    )
    add_contains(
        checks,
        "meta/NEXT_ACTIONS.md",
        next_actions,
        "OpenGWAS JWT expired at `2026-06-19T12:28:39Z`",
        "next_actions_opengwas_expired",
    )
    for forbidden in ("JWT valid until", "near-expiry", "expires `2026-06-19"):
        add_not_contains(
            checks,
            "meta/NEXT_ACTIONS.md",
            next_actions,
            forbidden,
            f"next_actions_no_stale_{re.sub(r'[^a-z0-9]+', '_', forbidden.lower()).strip('_')}",
        )

    return checks


def write_outputs(checks: list[Check], outdir: Path, expected_phase: str) -> dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    lint_path = outdir / "status_freshness_lint.tsv"
    summary_path = outdir / "summary.json"

    with lint_path.open("w", encoding="utf-8") as handle:
        handle.write("check_id\tfile\tstatus\tdetail\n")
        for check in checks:
            handle.write(
                "\t".join(
                    [
                        check.check_id,
                        check.file,
                        check.status,
                        check.detail.replace("\t", " ").replace("\n", " "),
                    ]
                )
                + "\n"
            )

    n_fail = sum(1 for check in checks if check.status == "FAIL")
    summary = {
        "purpose": "V50 status freshness lint; navigation/status only; no biological claim",
        "synthetic": False,
        "expected_phase": expected_phase,
        "n_checks": len(checks),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": str(lint_path.relative_to(ROOT)),
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["lint"])
    parser.add_argument("--expected-phase", default=None)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    expected_phase = args.expected_phase or latest_queue_phase(ROOT / "meta")
    checks = run_checks(expected_phase)
    summary = write_outputs(checks, args.outdir, expected_phase)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and summary["n_fail"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
