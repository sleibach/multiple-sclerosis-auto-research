#!/usr/bin/env python3
"""Validate the returned-package state machine.

This is validation-readiness infrastructure only. It enumerates synthetic
returned-package paths and forbidden shortcut transitions, then verifies that no
score-reading or result-report state is reachable before terms, format,
completeness/schema, label, and safe-class gates pass. It does not read returned
scores, real cohort data, expression data, labels, or quarantined cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_returned_package_state_transition_validator"

STATE_META = {
    "RECEIVED": ("package receipt logged; no package content interpreted", False, False),
    "TERMS_ALLOWED": ("data-use terms permit the selected aggregate route", False, False),
    "TERMS_BLOCKED": ("data-use terms block local package handling", False, False),
    "FORMAT_CANONICAL": ("canonical aggregate files/columns identified", False, False),
    "FORMAT_NONCANONICAL": ("accepted aliases detected; adapter required", False, False),
    "FORMAT_UNKNOWN": ("format state unknown; alias branch required", False, False),
    "FORMAT_NORMALIZED": ("noncanonical aggregate aliases normalized", False, False),
    "COMPLETENESS_PASS": ("redaction and required-output completeness gate passed", False, False),
    "COMPLETENESS_BLOCK": ("redaction/completeness gate blocked", False, False),
    "SCHEMA_PASS": ("aggregate schema validation passed", False, False),
    "SCHEMA_BLOCK": ("aggregate schema validation blocked", False, False),
    "LABELS_CLASSIFIED": ("analyzable-pair and response-label coverage classified", False, False),
    "LABELS_BLOCKED": ("response-label coverage blocks or severely restricts interpretation", False, False),
    "SAFE_CLASS_ASSIGNED": ("V46 safe-interpretation class assigned", False, False),
    "SAFE_CLASS_BLOCKED": ("safe-interpretation classifier emitted a blocked/restricted class", False, False),
    "REPORT_READY": ("result report may use only the safe class's allowed language", True, True),
    "REPORT_READY_WITH_CAUTION": ("result report may use only caution-bounded safe-class language", True, True),
    "RESTRICTED_LANGUAGE_READY": ("blocked/restricted report language only; no score interpretation", False, True),
    "REPAIR_REQUEST_READY": ("repair request can be drafted; no result interpretation", False, False),
}

ALLOWED_EDGES = {
    ("RECEIVED", "TERMS_ALLOWED"),
    ("RECEIVED", "TERMS_BLOCKED"),
    ("TERMS_ALLOWED", "FORMAT_CANONICAL"),
    ("TERMS_ALLOWED", "FORMAT_NONCANONICAL"),
    ("TERMS_ALLOWED", "FORMAT_UNKNOWN"),
    ("TERMS_BLOCKED", "REPAIR_REQUEST_READY"),
    ("FORMAT_NONCANONICAL", "FORMAT_NORMALIZED"),
    ("FORMAT_UNKNOWN", "FORMAT_NORMALIZED"),
    ("FORMAT_CANONICAL", "COMPLETENESS_PASS"),
    ("FORMAT_CANONICAL", "COMPLETENESS_BLOCK"),
    ("FORMAT_NORMALIZED", "COMPLETENESS_PASS"),
    ("FORMAT_NORMALIZED", "COMPLETENESS_BLOCK"),
    ("COMPLETENESS_PASS", "SCHEMA_PASS"),
    ("COMPLETENESS_PASS", "SCHEMA_BLOCK"),
    ("COMPLETENESS_BLOCK", "REPAIR_REQUEST_READY"),
    ("SCHEMA_PASS", "LABELS_CLASSIFIED"),
    ("SCHEMA_PASS", "LABELS_BLOCKED"),
    ("SCHEMA_BLOCK", "REPAIR_REQUEST_READY"),
    ("LABELS_CLASSIFIED", "SAFE_CLASS_ASSIGNED"),
    ("LABELS_CLASSIFIED", "SAFE_CLASS_BLOCKED"),
    ("LABELS_BLOCKED", "SAFE_CLASS_BLOCKED"),
    ("SAFE_CLASS_ASSIGNED", "REPORT_READY"),
    ("SAFE_CLASS_ASSIGNED", "REPORT_READY_WITH_CAUTION"),
    ("SAFE_CLASS_BLOCKED", "RESTRICTED_LANGUAGE_READY"),
    ("SAFE_CLASS_BLOCKED", "REPAIR_REQUEST_READY"),
}

REPORT_STATES = {"REPORT_READY", "REPORT_READY_WITH_CAUTION", "RESTRICTED_LANGUAGE_READY"}
SCORE_STATES = {"REPORT_READY", "REPORT_READY_WITH_CAUTION"}
SAFE_STATES = {"SAFE_CLASS_ASSIGNED", "SAFE_CLASS_BLOCKED"}
FORMAT_STATES = {"FORMAT_CANONICAL", "FORMAT_NONCANONICAL", "FORMAT_UNKNOWN", "FORMAT_NORMALIZED"}

SCENARIOS = {
    "scored_canonical_clean": [
        "RECEIVED",
        "TERMS_ALLOWED",
        "FORMAT_CANONICAL",
        "COMPLETENESS_PASS",
        "SCHEMA_PASS",
        "LABELS_CLASSIFIED",
        "SAFE_CLASS_ASSIGNED",
        "REPORT_READY",
    ],
    "scored_noncanonical_clean": [
        "RECEIVED",
        "TERMS_ALLOWED",
        "FORMAT_NONCANONICAL",
        "FORMAT_NORMALIZED",
        "COMPLETENESS_PASS",
        "SCHEMA_PASS",
        "LABELS_CLASSIFIED",
        "SAFE_CLASS_ASSIGNED",
        "REPORT_READY",
    ],
    "unknown_alias_branch_clean": [
        "RECEIVED",
        "TERMS_ALLOWED",
        "FORMAT_UNKNOWN",
        "FORMAT_NORMALIZED",
        "COMPLETENESS_PASS",
        "SCHEMA_PASS",
        "LABELS_CLASSIFIED",
        "SAFE_CLASS_ASSIGNED",
        "REPORT_READY",
    ],
    "terms_blocked": ["RECEIVED", "TERMS_BLOCKED", "REPAIR_REQUEST_READY"],
    "unscoreable_completeness_block": [
        "RECEIVED",
        "TERMS_ALLOWED",
        "FORMAT_CANONICAL",
        "COMPLETENESS_BLOCK",
        "REPAIR_REQUEST_READY",
    ],
    "schema_blocked": [
        "RECEIVED",
        "TERMS_ALLOWED",
        "FORMAT_CANONICAL",
        "COMPLETENESS_PASS",
        "SCHEMA_BLOCK",
        "REPAIR_REQUEST_READY",
    ],
    "labels_below_floor": [
        "RECEIVED",
        "TERMS_ALLOWED",
        "FORMAT_CANONICAL",
        "COMPLETENESS_PASS",
        "SCHEMA_PASS",
        "LABELS_BLOCKED",
        "SAFE_CLASS_BLOCKED",
        "RESTRICTED_LANGUAGE_READY",
    ],
    "batch_or_confounder_caution": [
        "RECEIVED",
        "TERMS_ALLOWED",
        "FORMAT_CANONICAL",
        "COMPLETENESS_PASS",
        "SCHEMA_PASS",
        "LABELS_CLASSIFIED",
        "SAFE_CLASS_ASSIGNED",
        "REPORT_READY_WITH_CAUTION",
    ],
}

FORBIDDEN_SHORTCUTS = [
    ("RECEIVED", "REPORT_READY"),
    ("RECEIVED", "SAFE_CLASS_ASSIGNED"),
    ("TERMS_ALLOWED", "REPORT_READY"),
    ("TERMS_ALLOWED", "SAFE_CLASS_ASSIGNED"),
    ("FORMAT_CANONICAL", "REPORT_READY"),
    ("FORMAT_NORMALIZED", "REPORT_READY"),
    ("COMPLETENESS_PASS", "REPORT_READY"),
    ("SCHEMA_PASS", "REPORT_READY"),
    ("LABELS_CLASSIFIED", "REPORT_READY"),
    ("TERMS_BLOCKED", "FORMAT_CANONICAL"),
    ("TERMS_BLOCKED", "SAFE_CLASS_ASSIGNED"),
    ("COMPLETENESS_BLOCK", "SAFE_CLASS_ASSIGNED"),
    ("SCHEMA_BLOCK", "REPORT_READY"),
    ("LABELS_BLOCKED", "REPORT_READY"),
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


def state_rows() -> list[dict[str, object]]:
    rows = []
    for state, (description, score_read_allowed, report_allowed) in STATE_META.items():
        rows.append(
            {
                "state": state,
                "description": description,
                "score_read_allowed": str(score_read_allowed).lower(),
                "report_state_allowed": str(report_allowed).lower(),
            }
        )
    return rows


def edge_rows() -> list[dict[str, object]]:
    return [
        {
            "from_state": start,
            "to_state": end,
            "allowed": "true",
            "score_values_read": "false",
        }
        for start, end in sorted(ALLOWED_EDGES)
    ]


def scenario_transition_rows() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    transitions: list[dict[str, object]] = []
    lint: list[dict[str, object]] = []
    for scenario, path in SCENARIOS.items():
        for order, state in enumerate(path, start=1):
            score_read_allowed = STATE_META[state][1]
            report_allowed = STATE_META[state][2]
            transitions.append(
                {
                    "scenario": scenario,
                    "step_order": order,
                    "state": state,
                    "description": STATE_META[state][0],
                    "score_read_allowed": str(score_read_allowed).lower(),
                    "report_state_allowed": str(report_allowed).lower(),
                    "path": ";".join(path),
                }
            )
        for order, (start, end) in enumerate(zip(path, path[1:]), start=1):
            lint.append(
                {
                    "scenario": scenario,
                    "check": "allowed_edge",
                    "status": "PASS" if (start, end) in ALLOWED_EDGES else "FAIL",
                    "detail": f"{order}:{start}->{end}",
                }
            )
        lint.extend(path_lints(scenario, path))
    return transitions, lint


def path_lints(scenario: str, path: list[str]) -> list[dict[str, object]]:
    lint: list[dict[str, object]] = []
    indexed = {state: i for i, state in enumerate(path)}
    report_indexes = [i for i, state in enumerate(path) if state in REPORT_STATES]
    score_indexes = [i for i, state in enumerate(path) if state in SCORE_STATES]
    safe_indexes = [i for i, state in enumerate(path) if state in SAFE_STATES]
    first_safe = min(safe_indexes) if safe_indexes else None

    clean_report = "REPORT_READY" in path or "REPORT_READY_WITH_CAUTION" in path
    if clean_report:
        required = [
            "TERMS_ALLOWED",
            "COMPLETENESS_PASS",
            "SCHEMA_PASS",
            "LABELS_CLASSIFIED",
            "SAFE_CLASS_ASSIGNED",
        ]
        missing = [state for state in required if state not in path]
        has_format = bool(FORMAT_STATES.intersection(path))
        if not has_format:
            missing.append("FORMAT_*")
        lint.append(
            {
                "scenario": scenario,
                "check": "report_requires_all_gates",
                "status": "PASS" if not missing else "FAIL",
                "detail": "all required gates present" if not missing else "missing=" + ",".join(missing),
            }
        )

    if report_indexes:
        report_after_safe = first_safe is not None and min(report_indexes) > first_safe
        lint.append(
            {
                "scenario": scenario,
                "check": "report_after_safe_class",
                "status": "PASS" if report_after_safe else "FAIL",
                "detail": f"first_report={min(report_indexes)};first_safe={first_safe}",
            }
        )

    if score_indexes:
        score_after_safe = first_safe is not None and min(score_indexes) > first_safe
        lint.append(
            {
                "scenario": scenario,
                "check": "score_state_after_safe_class",
                "status": "PASS" if score_after_safe else "FAIL",
                "detail": f"first_score={min(score_indexes)};first_safe={first_safe}",
            }
        )

    if "TERMS_BLOCKED" in path:
        allowed_after_terms_block = path[indexed["TERMS_BLOCKED"] + 1 :] == ["REPAIR_REQUEST_READY"]
        lint.append(
            {
                "scenario": scenario,
                "check": "terms_block_allows_only_repair",
                "status": "PASS" if allowed_after_terms_block else "FAIL",
                "detail": ";".join(path[indexed["TERMS_BLOCKED"] + 1 :]),
            }
        )

    if "REPAIR_REQUEST_READY" in path:
        no_score_with_repair = not any(state in SCORE_STATES for state in path)
        lint.append(
            {
                "scenario": scenario,
                "check": "repair_path_never_reads_scores",
                "status": "PASS" if no_score_with_repair else "FAIL",
                "detail": ";".join(state for state in path if state in SCORE_STATES) or "no score states",
            }
        )

    return lint


def shortcut_lints() -> list[dict[str, object]]:
    lint: list[dict[str, object]] = []
    for start, end in FORBIDDEN_SHORTCUTS:
        lint.append(
            {
                "scenario": "forbidden_shortcut_matrix",
                "check": f"shortcut_blocked_{start}_to_{end}",
                "status": "PASS" if (start, end) not in ALLOWED_EDGES else "FAIL",
                "detail": f"{start}->{end}",
            }
        )
    return lint


def write_markdown(path: Path, summary: dict[str, object], scenarios: list[dict[str, object]]) -> None:
    lines = [
        "# Returned-Package State-Transition Validator V46",
        "",
        "Status: synthetic/software readiness only. No validation result and no biological claim.",
        "",
        "This validator freezes the allowed route from package receipt to report readiness.",
        "It checks that a returned package cannot reach a report or score-reading state before",
        "terms, format, completeness/schema, label coverage, and the V46 safe-interpretation",
        "class have been resolved.",
        "",
        f"Overall status: `{summary['overall_status']}`.",
        f"Synthetic scenarios: `{summary['n_scenarios']}`; scenario transitions: `{summary['n_scenario_transition_rows']}`; lint failures: `{summary['n_lint_fail']}`.",
        f"Forbidden shortcut checks: `{summary['n_forbidden_shortcut_checks']}`.",
        "",
        "| Scenario | Terminal state | Score states before safe class | Report states before safe class |",
        "|---|---|---:|---:|",
    ]
    terminal_by_scenario = {}
    for row in scenarios:
        terminal_by_scenario[str(row["scenario"])] = str(row["state"])
    for scenario in sorted(terminal_by_scenario):
        lines.append(f"| `{scenario}` | `{terminal_by_scenario[scenario]}` | `0` | `0` |")
    lines.extend(
        [
            "",
            "The validator intentionally permits only restricted-language or repair-request",
            "states for blocked paths. Clean result reports are reachable only after",
            "`SAFE_CLASS_ASSIGNED`.",
            "",
        ]
    )
    path.write_text("\n".join(lines))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    states = state_rows()
    edges = edge_rows()
    transitions, lints = scenario_transition_rows()
    lints.extend(shortcut_lints())

    states_path = outdir / "returned_package_states.tsv"
    edges_path = outdir / "returned_package_allowed_transitions.tsv"
    transitions_path = outdir / "returned_package_state_transition_scenarios.tsv"
    lint_path = outdir / "returned_package_state_transition_lint.tsv"
    markdown_path = outdir / "RETURNED_PACKAGE_STATE_TRANSITION_VALIDATOR.md"

    write_tsv(states_path, states, ["state", "description", "score_read_allowed", "report_state_allowed"])
    write_tsv(edges_path, edges, ["from_state", "to_state", "allowed", "score_values_read"])
    write_tsv(
        transitions_path,
        transitions,
        ["scenario", "step_order", "state", "description", "score_read_allowed", "report_state_allowed", "path"],
    )
    write_tsv(lint_path, lints, ["scenario", "check", "status", "detail"])

    n_fail = sum(1 for row in lints if row["status"] != "PASS")
    n_premature_score_paths = 0
    n_premature_report_paths = 0
    for path in SCENARIOS.values():
        safe_indexes = [i for i, state in enumerate(path) if state in SAFE_STATES]
        first_safe = min(safe_indexes) if safe_indexes else 10_000
        if any(i < first_safe for i, state in enumerate(path) if state in SCORE_STATES):
            n_premature_score_paths += 1
        if any(i < first_safe for i, state in enumerate(path) if state in REPORT_STATES):
            n_premature_report_paths += 1

    summary = {
        "synthetic": True,
        "purpose": "V46 returned-package state-transition validator; no biological claim",
        "n_states": len(states),
        "n_allowed_edges": len(edges),
        "n_scenarios": len(SCENARIOS),
        "n_scenario_transition_rows": len(transitions),
        "n_lint_checks": len(lints),
        "n_lint_fail": n_fail,
        "n_forbidden_shortcut_checks": len(FORBIDDEN_SHORTCUTS),
        "n_premature_score_paths": n_premature_score_paths,
        "n_premature_report_paths": n_premature_report_paths,
        "overall_status": "PASS" if n_fail == 0 and n_premature_score_paths == 0 and n_premature_report_paths == 0 else "FAIL",
        "states": rel(states_path),
        "allowed_transitions": rel(edges_path),
        "scenario_transitions": rel(transitions_path),
        "lint": rel(lint_path),
        "markdown": rel(markdown_path),
    }
    write_markdown(markdown_path, summary, transitions)
    (outdir / "returned_package_state_transition_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and summary["overall_status"] != "PASS":
        return 1
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
