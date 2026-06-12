#!/usr/bin/env python3
"""Lint V45 operator docs for no-score-before-gates guard language.

This is validation-readiness governance only. It does not inspect data, compute
scores, or run a validation harness.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_no_score_before_gates_linter/live"


BASE_TARGETS = [
    {
        "path": "docs/validation/FIRST_24H_RECEIVED_DATA_OPERATOR_CHECKLIST_V45.md",
        "required": [
            r"may_score_now=no",
            r"Do not open expression matrices",
            r"Stop before scoring",
            r"no validation has occurred until",
        ],
    },
    {
        "path": "docs/validation/HARNESS_READY_DECISION_TEMPLATE_V45.md",
        "required": [
            r"The harness may run only if every required gate",
            r"harness_ready=no",
            r"no validation has occurred",
        ],
    },
    {
        "path": "docs/validation/VALIDATION_COMMAND_RUNNER_V45.md",
        "required": [
            r"does not open quarantined data",
            r"before any frozen harness can run",
            r"A cohort remains blocked if any generated command fails",
        ],
    },
    {
        "path": "docs/validation/COLLABORATOR_VALIDATION_PACKAGE_README_V45.md",
        "required": [
            r"Do not score anything",
            r"harness-ready only after",
            r"Do not score outcomes until",
        ],
    },
    {
        "path": "docs/validation/EXTERNAL_BLOCKER_BOARD_V45.md",
        "required": [
            r"0` cohorts are harness-ready",
            r"not received,\s+quarantined,\s+preflighted,\s+scored,\s+or validated",
        ],
    },
]

ROUTE_PACKET_REQUIRED = [
    r"No scoring is authorized until",
    r"Do not run module scoring",
    r"gates pass",
]

FORBIDDEN = [
    r"\bscore immediately\b",
    r"\brun (?:the )?harness immediately\b",
    r"\bskip (?:the )?(?:preflight|checksum|subject-map|subject map|terms|gate|gates)\b",
    r"\bbypass (?:the )?(?:preflight|checksum|subject-map|subject map|terms|gate|gates)\b",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--synthetic-case", choices=["none", "bad"], default="none")
    parser.add_argument("--expect-status", choices=["PASS", "FAIL"], default=None)
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def default_targets() -> list[dict[str, object]]:
    targets = [dict(item) for item in BASE_TARGETS]
    for path in sorted((ROOT / "analysis/v45_route_arrival_packets").glob("*_arrival_packet.md")):
        targets.append({"path": rel(path), "required": list(ROUTE_PACKET_REQUIRED)})
    return targets


def synthetic_bad_target(outdir: Path) -> list[dict[str, object]]:
    fixture = outdir / "synthetic_bad_no_gate_doc.md"
    fixture.write_text(
        "# Synthetic Bad No-Gate Doc\n\n"
        "synthetic: true\n\n"
        "Score immediately and skip preflight. Run the harness immediately.\n"
    )
    return [{"path": rel(fixture), "required": list(ROUTE_PACKET_REQUIRED)}]


def check_target(target: dict[str, object]) -> list[dict[str, str]]:
    path = ROOT / str(target["path"])
    rows: list[dict[str, str]] = []
    if not path.exists():
        rows.append(
            {
                "path": str(target["path"]),
                "check_type": "exists",
                "pattern": "",
                "status": "FAIL",
                "detail": "missing target",
            }
        )
        return rows
    text = path.read_text(errors="ignore")
    for pattern in target["required"]:
        found = bool(re.search(str(pattern), text, flags=re.IGNORECASE | re.MULTILINE))
        rows.append(
            {
                "path": str(target["path"]),
                "check_type": "required_guard",
                "pattern": str(pattern),
                "status": "PASS" if found else "FAIL",
                "detail": "found" if found else "missing required guard language",
            }
        )
    for pattern in FORBIDDEN:
        found = bool(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE))
        rows.append(
            {
                "path": str(target["path"]),
                "check_type": "forbidden_shortcut",
                "pattern": pattern,
                "status": "FAIL" if found else "PASS",
                "detail": "forbidden shortcut present" if found else "absent",
            }
        )
    return rows


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    targets = synthetic_bad_target(outdir) if args.synthetic_case == "bad" else default_targets()
    rows: list[dict[str, str]] = []
    for target in targets:
        rows.extend(check_target(target))

    table_path = outdir / "no_score_before_gates_lint.tsv"
    with table_path.open("w", newline="") as handle:
        fieldnames = ["path", "check_type", "pattern", "status", "detail"]
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    n_fail = sum(1 for row in rows if row["status"] == "FAIL")
    observed = "PASS" if n_fail == 0 else "FAIL"
    summary = {
        "synthetic": args.synthetic_case != "none",
        "synthetic_case": args.synthetic_case,
        "purpose": "V45 no-score-before-gates documentation linter; no biological claim",
        "n_targets": len(targets),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "observed_status": observed,
        "expected_status": args.expect_status,
        "expectation_met": args.expect_status is None or observed == args.expect_status,
        "table": rel(table_path),
    }
    (outdir / "no_score_before_gates_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.expect_status is not None and observed != args.expect_status:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
