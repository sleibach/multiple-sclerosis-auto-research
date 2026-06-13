#!/usr/bin/env python3
"""Map report-header metadata failures to safe repair requests.

This is returned-package report governance only. It proves that every required
result-report provenance field has a safe repair path before any result text is
allowed. It does not read score tables, expression matrices, labels, or
quarantined cohort data.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis" / "v46_report_header_repair_template_coverage"

REQUIRED_FIELDS = [
    "cohort_token",
    "route_class",
    "terms_class",
    "safe_class",
    "locked_rule_path",
    "locked_rule_sha256",
]

HEADER_REPAIR_SPECS = [
    {
        "issue_id": "missing_cohort_token",
        "field": "cohort_token",
        "failure_trigger": "required_field:cohort_token fails or token format is invalid",
        "safe_class": "BLOCKED_METADATA_CONTRADICTION",
        "request": "Provide the cohort token used in the receipt manifest and status board, without changing any returned metrics.",
        "required_return": "corrected report header only; receipt manifest if the cohort token is ambiguous",
        "forbidden_action": "Do not infer cohort identity from score values, labels, or expression data.",
    },
    {
        "issue_id": "missing_route_class",
        "field": "route_class",
        "failure_trigger": "required_field:route_class fails or route_class_known fails",
        "safe_class": "BLOCKED_METADATA_CONTRADICTION",
        "request": "Provide the route class emitted by the returned-package command plan or preflight dry run.",
        "required_return": "corrected report header plus the command-plan summary that produced the route",
        "forbidden_action": "Do not choose a route based on whether returned metrics look favorable.",
    },
    {
        "issue_id": "missing_terms_class",
        "field": "terms_class",
        "failure_trigger": "required_field:terms_class fails or terms_class_known fails",
        "safe_class": "BLOCKED_TERMS_OR_RECEIPT_GATES",
        "request": "Provide the terms-governance class from the receipt/terms preflight before any report interpretation proceeds.",
        "required_return": "corrected report header plus terms-governance preflight output",
        "forbidden_action": "Do not inspect or summarize score-bearing outputs until terms handling is cleared.",
    },
    {
        "issue_id": "missing_safe_class",
        "field": "safe_class",
        "failure_trigger": "required_field:safe_class fails or safe_class_known fails",
        "safe_class": "BLOCKED_METADATA_CONTRADICTION",
        "request": "Provide the V46 safe-interpretation class emitted by the safe-interpretation classifier.",
        "required_return": "corrected report header plus safe-interpretation summary",
        "forbidden_action": "Do not invent a safe class manually from the result text.",
    },
    {
        "issue_id": "missing_locked_rule_path",
        "field": "locked_rule_path",
        "failure_trigger": "required_field:locked_rule_path fails or locked_rule_path_exact fails",
        "safe_class": "BLOCKED_METADATA_CONTRADICTION",
        "request": "Use the exact locked rule path `docs/locked_rules/LOCKED_RULE_V22.md` in the report header.",
        "required_return": "corrected report header only",
        "forbidden_action": "Do not substitute a successor, sensitivity, or local copy of the locked rule.",
    },
    {
        "issue_id": "missing_or_wrong_locked_rule_sha256",
        "field": "locked_rule_sha256",
        "failure_trigger": "required_field:locked_rule_sha256 fails or locked_rule_hash_matches_v45_baseline fails",
        "safe_class": "BLOCKED_METADATA_CONTRADICTION",
        "request": "Use the V45 locked-artifact hash baseline for `docs/locked_rules/LOCKED_RULE_V22.md`.",
        "required_return": "corrected report header plus locked-artifact hash audit output if mismatch persists",
        "forbidden_action": "Do not recompute or accept a different hash after seeing returned results.",
    },
    {
        "issue_id": "metadata_after_result_text",
        "field": "all_required_fields",
        "failure_trigger": "metadata_before_result_text fails",
        "safe_class": "BLOCKED_METADATA_CONTRADICTION",
        "request": "Move all required provenance fields before any result heading or score-bearing language.",
        "required_return": "corrected report header ordering only",
        "forbidden_action": "Do not leave score-bearing language above missing or late provenance metadata.",
    },
]

FORBIDDEN_PATTERNS = [
    re.compile(r"\bAUC\s*[=:]", re.I),
    re.compile(r"\bp\s*[=:]", re.I),
    re.compile(r"\beffect[- ]size\s*[=:]", re.I),
    re.compile(r"\bvalidation (?:passed|failed|succeeded)\b", re.I),
    re.compile(r"\bthe rule (?:passed|failed)\b", re.I),
    re.compile(r"\bconfirmed\b", re.I),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def render_template(spec: dict[str, str]) -> str:
    return f"""# Report-Header Repair Request: {spec['issue_id']}

Status: report-header repair template. No validation result and no biological
claim.

Blocked header field: `{spec['field']}`

Failure trigger: {spec['failure_trigger']}

Temporary safe class: `{spec['safe_class']}`

Requested repair:

- {spec['request']}

Required return:

- {spec['required_return']}

Forbidden action:

- {spec['forbidden_action']}

Boundary:

- This request concerns provenance/header metadata only.
- It does not ask for rerunning the locked rule, changing the locked rule,
  changing thresholds, changing labels, changing timepoints, or interpreting
  returned scores.
- No score-bearing text may appear before the corrected header passes the V46
  report-header metadata linter.
"""


def lint_template(spec: dict[str, str], text: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for pattern in FORBIDDEN_PATTERNS:
        rows.append(
            {
                "issue_id": spec["issue_id"],
                "field": spec["field"],
                "check": f"forbidden_pattern:{pattern.pattern}",
                "status": "FAIL" if pattern.search(text) else "PASS",
                "detail": "present" if pattern.search(text) else "absent",
                "score_values_read": "false",
            }
        )
    required_phrases = [
        ("names_field", f"`{spec['field']}`" if spec["field"] != "all_required_fields" else "all required provenance fields"),
        ("contains_no_score_boundary", "No score-bearing text may appear before the corrected header passes"),
        ("contains_no_rule_change_boundary", "changing the locked rule"),
    ]
    for check, phrase in required_phrases:
        rows.append(
            {
                "issue_id": spec["issue_id"],
                "field": spec["field"],
                "check": check,
                "status": "PASS" if phrase in text else "FAIL",
                "detail": phrase,
                "score_values_read": "false",
            }
        )
    return rows


def write_markdown(path: Path, specs: list[dict[str, str]], templates: dict[str, str]) -> None:
    lines = [
        "# Report-Header Repair Template Coverage V46",
        "",
        "Status: report-governance infrastructure. No validation result and no biological claim.",
        "",
        "This map links every report-header metadata failure to a safe repair request",
        "before any result or score-bearing text may proceed.",
        "",
        "| Issue | Field | Safe class | Trigger |",
        "|---|---|---|---|",
    ]
    for spec in specs:
        lines.append(
            f"| `{spec['issue_id']}` | `{spec['field']}` | `{spec['safe_class']}` | {spec['failure_trigger']} |"
        )
    lines.extend(["", "## Templates", ""])
    for spec in specs:
        lines.append(templates[spec["issue_id"]])
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    templates = {spec["issue_id"]: render_template(spec) for spec in HEADER_REPAIR_SPECS}
    rows = []
    for spec in HEADER_REPAIR_SPECS:
        rows.append(
            {
                **spec,
                "template_path": rel(outdir / f"{spec['issue_id']}.md"),
                "score_values_read": "false",
            }
        )
        (outdir / f"{spec['issue_id']}.md").write_text(templates[spec["issue_id"]])

    lint_rows = [
        row
        for spec in HEADER_REPAIR_SPECS
        for row in lint_template(spec, templates[spec["issue_id"]])
    ]
    field_coverage = {field: False for field in REQUIRED_FIELDS}
    for spec in HEADER_REPAIR_SPECS:
        if spec["field"] in field_coverage:
            field_coverage[spec["field"]] = True
    coverage_rows = [
        {
            "field": field,
            "covered": "true" if covered else "false",
            "score_values_read": "false",
        }
        for field, covered in field_coverage.items()
    ]

    write_tsv(
        outdir / "report_header_repair_template_coverage.tsv",
        rows,
        [
            "issue_id",
            "field",
            "failure_trigger",
            "safe_class",
            "request",
            "required_return",
            "forbidden_action",
            "template_path",
            "score_values_read",
        ],
    )
    write_tsv(outdir / "report_header_required_field_coverage.tsv", coverage_rows, ["field", "covered", "score_values_read"])
    write_tsv(outdir / "report_header_repair_template_lint.tsv", lint_rows, ["issue_id", "field", "check", "status", "detail", "score_values_read"])
    write_markdown(outdir / "REPORT_HEADER_REPAIR_TEMPLATE_COVERAGE.md", HEADER_REPAIR_SPECS, templates)

    n_lint_fail = sum(1 for row in lint_rows if row["status"] != "PASS")
    n_uncovered = sum(1 for row in coverage_rows if row["covered"] != "true")
    summary = {
        "purpose": "V46 report-header repair-template coverage; no biological claim",
        "issues": len(HEADER_REPAIR_SPECS),
        "required_fields": len(REQUIRED_FIELDS),
        "uncovered_required_fields": n_uncovered,
        "lint_failures": n_lint_fail,
        "score_values_read": False,
        "overall_status": "PASS" if n_lint_fail == 0 and n_uncovered == 0 else "FAIL",
        "outputs": [
            rel(outdir / "report_header_repair_template_coverage.tsv"),
            rel(outdir / "report_header_required_field_coverage.tsv"),
            rel(outdir / "report_header_repair_template_lint.tsv"),
            rel(outdir / "REPORT_HEADER_REPAIR_TEMPLATE_COVERAGE.md"),
        ],
    }
    (outdir / "report_header_repair_template_coverage_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if args.fail_on_error and summary["overall_status"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
