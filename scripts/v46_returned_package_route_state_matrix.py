#!/usr/bin/env python3
"""Build the V46 returned-package route-state matrix.

This is validation-readiness infrastructure only. It enumerates synthetic
returned aggregate package states across terms class, scoreability, and metric
format state, then summarizes the allowed route and hard-stop boundary. It does
not read data, score values, expression matrices, labels, or quarantined
cohorts.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path

import v46_returned_package_command_order_planner as command_order


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_returned_package_route_state_matrix"

TERMS_CLASSES = [
    "LOCAL_PREFLIGHT_ALLOWED",
    "AGGREGATE_ONLY_LOCAL_PREFLIGHT",
    "AUTHOR_RUN_ONLY",
    "NO_PROCESSING_ALLOWED",
    "AMBIGUOUS_TERMS_BLOCK",
    "UNKNOWN",
]
PACKAGE_STATES = ["scored", "unscoreable"]
METRIC_FORMAT_STATES = ["canonical", "noncanonical", "unknown"]
ALLOWED_TERMS = {"LOCAL_PREFLIGHT_ALLOWED", "AGGREGATE_ONLY_LOCAL_PREFLIGHT", "AUTHOR_RUN_ONLY"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


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


def route_class(terms_class: str, package_state: str, metric_format_state: str, plan_status: str) -> str:
    if plan_status == "BLOCKED":
        return "BLOCKED_BEFORE_PACKAGE_HANDLING"
    if package_state == "unscoreable":
        return "UNSCOREABLE_AGGREGATE_PREFLIGHT_ONLY"
    if metric_format_state == "noncanonical":
        return "SCORED_AGGREGATE_ADAPTER_REQUIRED"
    if metric_format_state == "unknown":
        return "SCORED_AGGREGATE_ALIAS_BRANCH_REQUIRED"
    if terms_class == "AUTHOR_RUN_ONLY":
        return "SCORED_AUTHOR_RUN_AGGREGATE_ONLY"
    return "SCORED_AGGREGATE_CANONICAL_PATH"


def allowed_wording(route: str) -> str:
    if route == "BLOCKED_BEFORE_PACKAGE_HANDLING":
        return "Report only the terms/route blocker; do not run package gates or discuss returned results."
    if route == "UNSCOREABLE_AGGREGATE_PREFLIGHT_ONLY":
        return "Use only for receipt, redaction, completeness, schema, and repair logistics; no score or validation wording is allowed."
    if route == "SCORED_AGGREGATE_ADAPTER_REQUIRED":
        return "Normalize accepted aliases first, then continue to gates and safe interpretation if all checks pass."
    if route == "SCORED_AGGREGATE_ALIAS_BRANCH_REQUIRED":
        return "Run the alias adapter branch if initial completeness suggests aliases; request canonical outputs if normalization fails."
    if route == "SCORED_AUTHOR_RUN_AGGREGATE_ONLY":
        return "Handle only the returned aggregate author-run outputs; do not process individual-level data locally."
    return "Proceed through gates to V46 safe interpretation; result wording remains bounded by the returned safe class."


def expected_status(terms_class: str) -> str:
    return "PASS" if terms_class in ALLOWED_TERMS else "BLOCKED"


def build_row(terms_class: str, package_state: str, metric_format_state: str) -> tuple[dict[str, object], list[dict[str, object]]]:
    cohort = f"synthetic_{terms_class.lower()}_{package_state}_{metric_format_state}"
    rows, plan_status, reason = command_order.build_plan(
        cohort=cohort,
        package_root="analysis/v45_author_run_output_check/synthetic_complete_author_run_package",
        terms_capture=f"analysis/v46_terms_governance_matrix/synthetic/{terms_class.lower()}_terms.tsv",
        terms_class=terms_class,
        package_kind="author_run_aggregate",
        package_state=package_state,
        metric_format_state=metric_format_state,
    )
    observed_order = [str(row["step_id"]) for row in rows]
    score_clean = all(str(row["score_values_read"]) == "false" for row in rows)
    route = route_class(terms_class, package_state, metric_format_state, plan_status)
    safe_step_present = "safe_interpretation_classifier" in observed_order
    adapter_step_present = any("metric_format_adapter" in step for step in observed_order)
    stop_step_present = any(step.startswith("stop_") for step in observed_order)
    matrix_row = {
        "terms_class": terms_class,
        "package_kind": "author_run_aggregate",
        "package_state": package_state,
        "metric_format_state": metric_format_state,
        "expected_plan_status": expected_status(terms_class),
        "observed_plan_status": plan_status,
        "route_class": route,
        "n_steps": len(rows),
        "stop_step_present": str(stop_step_present).lower(),
        "adapter_step_present": str(adapter_step_present).lower(),
        "safe_interpretation_step_present": str(safe_step_present).lower(),
        "score_values_read_false": str(score_clean).lower(),
        "allowed_wording": allowed_wording(route),
        "status_reason": reason,
        "observed_order": ";".join(observed_order),
    }
    checks = [
        {
            "terms_class": terms_class,
            "package_state": package_state,
            "metric_format_state": metric_format_state,
            "check": "expected_status",
            "status": "PASS" if matrix_row["expected_plan_status"] == plan_status else "FAIL",
            "detail": f"expected={matrix_row['expected_plan_status']};observed={plan_status}",
        },
        {
            "terms_class": terms_class,
            "package_state": package_state,
            "metric_format_state": metric_format_state,
            "check": "score_values_read_false",
            "status": "PASS" if score_clean else "FAIL",
            "detail": "all plan rows score_values_read=false" if score_clean else "score read flag detected",
        },
        {
            "terms_class": terms_class,
            "package_state": package_state,
            "metric_format_state": metric_format_state,
            "check": "blocked_routes_stop_before_package_gates",
            "status": "PASS" if plan_status == "PASS" or observed_order == ["terms_governance", "stop_terms_block"] else "FAIL",
            "detail": ";".join(observed_order),
        },
        {
            "terms_class": terms_class,
            "package_state": package_state,
            "metric_format_state": metric_format_state,
            "check": "unscoreable_never_allows_score_interpretation_wording",
            "status": "PASS" if package_state == "scored" or route in {"UNSCOREABLE_AGGREGATE_PREFLIGHT_ONLY", "BLOCKED_BEFORE_PACKAGE_HANDLING"} else "FAIL",
            "detail": route,
        },
    ]
    return matrix_row, checks


def main() -> int:
    args = parse_args()
    outdir = resolve(args.outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    matrix: list[dict[str, object]] = []
    checks: list[dict[str, object]] = []
    for terms_class in TERMS_CLASSES:
        for package_state in PACKAGE_STATES:
            for metric_format_state in METRIC_FORMAT_STATES:
                row, row_checks = build_row(terms_class, package_state, metric_format_state)
                matrix.append(row)
                checks.extend(row_checks)

    matrix_path = outdir / "returned_package_route_state_matrix.tsv"
    checks_path = outdir / "returned_package_route_state_checks.tsv"
    write_tsv(
        matrix_path,
        matrix,
        [
            "terms_class",
            "package_kind",
            "package_state",
            "metric_format_state",
            "expected_plan_status",
            "observed_plan_status",
            "route_class",
            "n_steps",
            "stop_step_present",
            "adapter_step_present",
            "safe_interpretation_step_present",
            "score_values_read_false",
            "allowed_wording",
            "status_reason",
            "observed_order",
        ],
    )
    write_tsv(checks_path, checks, ["terms_class", "package_state", "metric_format_state", "check", "status", "detail"])
    n_fail = sum(1 for row in checks if row["status"] != "PASS")
    summary = {
        "synthetic": True,
        "purpose": "V46 returned-package route-state matrix; no biological claim",
        "n_matrix_rows": len(matrix),
        "n_check_rows": len(checks),
        "n_fail": n_fail,
        "n_blocked_routes": sum(1 for row in matrix if row["observed_plan_status"] == "BLOCKED"),
        "n_unscoreable_prefight_only_routes": sum(1 for row in matrix if row["route_class"] == "UNSCOREABLE_AGGREGATE_PREFLIGHT_ONLY"),
        "n_score_values_read": sum(1 for row in matrix if row["score_values_read_false"] != "true"),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "matrix": rel(matrix_path),
        "checks": rel(checks_path),
    }
    (outdir / "returned_package_route_state_matrix_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if args.fail_on_error and n_fail else (0 if n_fail == 0 else 2)


if __name__ == "__main__":
    raise SystemExit(main())
