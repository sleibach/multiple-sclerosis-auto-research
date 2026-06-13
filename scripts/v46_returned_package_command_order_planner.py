#!/usr/bin/env python3
"""Generate the safe command order for returned validation packages.

This is validation-readiness infrastructure only. It writes the ordered command
plan for returned aggregate packages and the hard-stop conditions between
gates. It does not execute validation, read score values, inspect expression
data, or make biological claims.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_returned_package_command_order_planner"

TERMS_CLASSES = {
    "LOCAL_PREFLIGHT_ALLOWED",
    "AGGREGATE_ONLY_LOCAL_PREFLIGHT",
    "AUTHOR_RUN_ONLY",
    "NO_PROCESSING_ALLOWED",
    "AMBIGUOUS_TERMS_BLOCK",
    "UNKNOWN",
}
PROCEED_TERMS = {"LOCAL_PREFLIGHT_ALLOWED", "AGGREGATE_ONLY_LOCAL_PREFLIGHT"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    plan = sub.add_parser("plan")
    plan.add_argument("--cohort-token", default="<cohort>_<date>", help="Non-sensitive token used in output paths.")
    plan.add_argument("--package-root", default="<returned_aggregate_package_dir>")
    plan.add_argument("--terms-capture", default="<terms_capture_tsv>")
    plan.add_argument("--terms-class", choices=sorted(TERMS_CLASSES), default="UNKNOWN")
    plan.add_argument("--package-kind", choices=["author_run_aggregate", "individual_level_transfer"], default="author_run_aggregate")
    plan.add_argument("--package-state", choices=["scored", "unscoreable"], default="scored")
    plan.add_argument("--metric-format-state", choices=["canonical", "noncanonical", "unknown"], default="unknown")
    plan.add_argument("--outdir", type=Path, required=True)
    plan.add_argument("--expect-status", choices=["PASS", "BLOCKED"], default=None)

    syn = sub.add_parser("synthetic-check")
    syn.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
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


def cmd(*parts: str) -> str:
    return " ".join(parts)


def step(
    order: int,
    step_id: str,
    branch: str,
    command: str,
    required_input: str,
    expected_output: str,
    proceed_if: str,
    stop_if: str,
    rationale: str,
) -> dict[str, object]:
    return {
        "step_order": order,
        "step_id": step_id,
        "branch": branch,
        "command": command,
        "required_input": required_input,
        "expected_output": expected_output,
        "proceed_if": proceed_if,
        "stop_if": stop_if,
        "score_values_read": "false",
        "rationale": rationale,
    }


def paths(cohort: str) -> dict[str, str]:
    return {
        "terms_out": f"analysis/v46_terms_governance_matrix/{cohort}",
        "adapter_out": f"analysis/v46_author_run_metric_format_adapter/{cohort}",
        "gate_out": f"analysis/v45_author_run_return_gate_runner/{cohort}",
        "gate_out_norm": f"analysis/v45_author_run_return_gate_runner/{cohort}_normalized",
        "schema_out": f"analysis/v45_author_run_schema_validator/{cohort}",
        "partial_out": f"analysis/v46_partial_label_return_classifier/{cohort}",
        "safe_out": f"analysis/v46_returned_package_safe_interpretation/{cohort}",
        "pair_summary": f"analysis/v45_route_analyzable_pair_calculator/{cohort}/analyzable_pair_summary.json",
        "metadata_summary": f"analysis/v45_metadata_contradiction_stress/{cohort}/metadata_contradiction_summary.json",
        "batch_summary": f"analysis/v45_batch_confounder_guard/{cohort}/pre_score_batch_or_confounder_warning_summary.json",
    }


def terms_allows_returned_package(terms_class: str, package_kind: str) -> tuple[bool, str]:
    if terms_class == "UNKNOWN":
        return False, "terms class must be resolved before package handling proceeds"
    if terms_class in PROCEED_TERMS:
        return True, "terms allow local handling of aggregate preflight outputs"
    if terms_class == "AUTHOR_RUN_ONLY" and package_kind == "author_run_aggregate":
        return True, "terms block local individual-level processing but allow aggregate author-run return handling"
    return False, f"terms class {terms_class} blocks this package route"


def build_plan(
    cohort: str,
    package_root: str,
    terms_capture: str,
    terms_class: str,
    package_kind: str,
    package_state: str,
    metric_format_state: str,
) -> tuple[list[dict[str, object]], str, str]:
    p = paths(cohort)
    rows: list[dict[str, object]] = []
    rows.append(
        step(
            1,
            "terms_governance",
            "mandatory",
            cmd(
                ".venv/bin/python",
                "scripts/v46_terms_governance_matrix.py",
                "classify",
                "--terms",
                terms_capture,
                "--outdir",
                p["terms_out"],
            ),
            terms_capture,
            f"{p['terms_out']}/terms_governance_summary.json",
            "result_class permits this route",
            "UNKNOWN, AMBIGUOUS_TERMS_BLOCK, or NO_PROCESSING_ALLOWED; AUTHOR_RUN_ONLY blocks individual-level local transfer",
            "data-use terms are the first gate and can block all downstream handling",
        )
    )

    allowed, reason = terms_allows_returned_package(terms_class, package_kind)
    if not allowed:
        rows.append(
            step(
                2,
                "stop_terms_block",
                "mandatory_stop",
                "STOP",
                f"{p['terms_out']}/terms_governance_summary.json",
                "",
                "",
                reason,
                "no package gate, schema check, score reading, or interpretation is permitted",
            )
        )
        return rows, "BLOCKED", reason

    package_for_gate = package_root
    gate_out = p["gate_out"]
    next_order = 2
    if metric_format_state == "noncanonical":
        rows.append(
            step(
                next_order,
                "metric_format_adapter",
                "mandatory_for_declared_noncanonical_package",
                cmd(
                    ".venv/bin/python",
                    "scripts/v46_author_run_metric_format_adapter.py",
                    "adapt",
                    "--root",
                    package_root,
                    "--outdir",
                    p["adapter_out"],
                    "--fail-on-error",
                ),
                package_root,
                f"{p['adapter_out']}/normalized_package",
                "adapter overall_status PASS",
                "missing required canonical output after alias normalization",
                "normalize accepted aggregate file and column aliases before gate/schema checks",
            )
        )
        package_for_gate = f"{p['adapter_out']}/normalized_package"
        next_order += 1
    elif metric_format_state == "unknown":
        rows.append(
            step(
                next_order,
                "metric_format_adapter_branch",
                "conditional_if_initial_completeness_fails_with_recognizable_aliases",
                cmd(
                    ".venv/bin/python",
                    "scripts/v46_author_run_metric_format_adapter.py",
                    "adapt",
                    "--root",
                    package_root,
                    "--outdir",
                    p["adapter_out"],
                    "--fail-on-error",
                ),
                package_root,
                f"{p['adapter_out']}/normalized_package",
                "rerun return gate on normalized package if adapter PASS",
                "adapter FAIL; request missing canonical aggregate outputs",
                "repair naming/column variants only; never infer missing values",
            )
        )
        next_order += 1

    rows.append(
        step(
            next_order,
            "author_run_return_gate",
            "mandatory",
            cmd(
                ".venv/bin/python",
                "scripts/v45_author_run_return_gate_runner.py",
                "run",
                "--root",
                package_for_gate,
                "--package-state",
                package_state,
                "--outdir",
                gate_out,
                "--fail-on-error",
            ),
            package_for_gate,
            f"{gate_out}/author_run_return_gate_summary.json",
            "redaction_status PASS and completeness_status PASS",
            "redaction FAIL, completeness FAIL, or overall_status FAIL",
            "reject raw/private leakage before completeness and before any schema or score interpretation",
        )
    )
    next_order += 1

    if metric_format_state == "unknown":
        rows.append(
            step(
                next_order,
                "author_run_return_gate_after_adapter",
                "conditional_after_metric_adapter",
                cmd(
                    ".venv/bin/python",
                    "scripts/v45_author_run_return_gate_runner.py",
                    "run",
                    "--root",
                    f"{p['adapter_out']}/normalized_package",
                    "--package-state",
                    package_state,
                    "--outdir",
                    p["gate_out_norm"],
                    "--fail-on-error",
                ),
                f"{p['adapter_out']}/normalized_package",
                f"{p['gate_out_norm']}/author_run_return_gate_summary.json",
                "redaction_status PASS and completeness_status PASS",
                "redaction FAIL, completeness FAIL, or overall_status FAIL",
                "only run this branch when the initial gate failed due to alias-like completeness issues",
            )
        )
        next_order += 1

    rows.append(
        step(
            next_order,
            "aggregate_schema_validator",
            "mandatory_after_return_gate_pass",
            cmd(
                ".venv/bin/python",
                "scripts/v45_author_run_schema_validator.py",
                "run",
                "--root",
                package_for_gate,
                "--package-state",
                package_state,
                "--outdir",
                p["schema_out"],
                "--fail-on-error",
            ),
            f"{gate_out}/author_run_return_gate_summary.json and {package_for_gate}",
            f"{p['schema_out']}/author_run_schema_validation_summary.json",
            "overall_status PASS",
            "schema validation FAIL",
            "aggregate values must be internally consistent before any interpretation class is assigned",
        )
    )
    next_order += 1

    rows.append(
        step(
            next_order,
            "partial_label_classifier",
            "mandatory_before_safe_interpretation",
            cmd(
                ".venv/bin/python",
                "scripts/v46_partial_label_return_classifier.py",
                "classify",
                "--analyzable-summary",
                p["pair_summary"],
                "--outdir",
                p["partial_out"],
            ),
            p["pair_summary"],
            f"{p['partial_out']}/partial_label_classification_summary.json",
            "classifier writes response-label coverage class",
            "BLOCKED_PAIR_PARSE, response labels absent, single-class labels, or below-floor classes limit wording",
            "label coverage must be classified before returned results are discussed",
        )
    )
    next_order += 1

    rows.append(
        step(
            next_order,
            "safe_interpretation_classifier",
            "mandatory_final_pre_score_gate",
            cmd(
                ".venv/bin/python",
                "scripts/v46_returned_package_safe_interpretation.py",
                "classify",
                "--gate-summary",
                f"{gate_out}/author_run_return_gate_summary.json",
                "--schema-summary",
                f"{p['schema_out']}/author_run_schema_validation_summary.json",
                "--analyzable-summary",
                p["pair_summary"],
                "--metadata-summary",
                p["metadata_summary"],
                "--batch-confounder-summary",
                p["batch_summary"],
                "--terms-status",
                "PASS",
                "--outdir",
                p["safe_out"],
            ),
            "terms, return gate, schema, analyzable-pair, metadata, and batch/confounder summaries",
            f"{p['safe_out']}/safe_interpretation_summary.json",
            "result_class permits the exact pre-registered wording",
            "any blocked/caution class restricts wording; no score interpretation outside classifier class",
            "this is the final no-score-before-gates boundary",
        )
    )
    return rows, "PASS", reason


def plan(args: argparse.Namespace) -> int:
    outdir = resolve(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rows, status, reason = build_plan(
        args.cohort_token,
        args.package_root,
        args.terms_capture,
        args.terms_class,
        args.package_kind,
        args.package_state,
        args.metric_format_state,
    )
    table = outdir / "returned_package_command_plan.tsv"
    write_tsv(
        table,
        rows,
        [
            "step_order",
            "step_id",
            "branch",
            "command",
            "required_input",
            "expected_output",
            "proceed_if",
            "stop_if",
            "score_values_read",
            "rationale",
        ],
    )
    summary = {
        "synthetic": "synthetic" in str(outdir).lower() or "synthetic" in args.cohort_token.lower(),
        "purpose": "V46 returned-package command-order planner; no biological claim and no score values read",
        "score_values_read": False,
        "cohort_token": args.cohort_token,
        "terms_class": args.terms_class,
        "package_kind": args.package_kind,
        "package_state": args.package_state,
        "metric_format_state": args.metric_format_state,
        "plan_status": status,
        "status_reason": reason,
        "n_steps": len(rows),
        "n_stop_steps": sum(1 for row in rows if str(row["step_id"]).startswith("stop_")),
        "n_conditional_steps": sum(1 for row in rows if str(row["branch"]).startswith("conditional")),
        "hard_stop_before_scores": True,
        "command_plan": rel(table),
        "expect_status": args.expect_status or "",
        "expectation_met": (not args.expect_status) or status == args.expect_status,
    }
    (outdir / "returned_package_command_plan_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["expectation_met"] else 2


def check_case(name: str, outdir: Path, kwargs: dict[str, str], expected_status: str, expected_order: list[str]) -> dict[str, object]:
    case_out = outdir / name
    args = argparse.Namespace(outdir=case_out, expect_status=expected_status, **kwargs)
    rc = plan(args)
    summary = json.loads((case_out / "returned_package_command_plan_summary.json").read_text())
    rows = list(csv.DictReader((case_out / "returned_package_command_plan.tsv").open(), delimiter="\t"))
    observed_order = [row["step_id"] for row in rows]
    score_clean = all(row["score_values_read"] == "false" for row in rows)
    order_ok = observed_order == expected_order
    return {
        "case": name,
        "expected_status": expected_status,
        "observed_status": summary["plan_status"],
        "expected_order": ";".join(expected_order),
        "observed_order": ";".join(observed_order),
        "order_ok": str(order_ok).lower(),
        "score_values_read_false": str(score_clean).lower(),
        "returncode": rc,
        "summary": rel(case_out / "returned_package_command_plan_summary.json"),
    }


def synthetic_check(outdir: Path) -> int:
    outdir = resolve(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    base = {
        "cohort_token": "synthetic_return",
        "package_root": "analysis/v45_author_run_output_check/synthetic_complete_author_run_package",
        "terms_capture": "analysis/v46_terms_governance_matrix/synthetic/aggregate_only_local_preflight_terms.tsv",
        "package_kind": "author_run_aggregate",
        "package_state": "scored",
    }
    cases = [
        (
            "canonical_aggregate",
            {**base, "terms_class": "AGGREGATE_ONLY_LOCAL_PREFLIGHT", "metric_format_state": "canonical"},
            "PASS",
            [
                "terms_governance",
                "author_run_return_gate",
                "aggregate_schema_validator",
                "partial_label_classifier",
                "safe_interpretation_classifier",
            ],
        ),
        (
            "noncanonical_declared",
            {**base, "terms_class": "AGGREGATE_ONLY_LOCAL_PREFLIGHT", "metric_format_state": "noncanonical"},
            "PASS",
            [
                "terms_governance",
                "metric_format_adapter",
                "author_run_return_gate",
                "aggregate_schema_validator",
                "partial_label_classifier",
                "safe_interpretation_classifier",
            ],
        ),
        (
            "unknown_alias_branch",
            {**base, "terms_class": "LOCAL_PREFLIGHT_ALLOWED", "metric_format_state": "unknown"},
            "PASS",
            [
                "terms_governance",
                "metric_format_adapter_branch",
                "author_run_return_gate",
                "author_run_return_gate_after_adapter",
                "aggregate_schema_validator",
                "partial_label_classifier",
                "safe_interpretation_classifier",
            ],
        ),
        (
            "author_run_only_aggregate_return",
            {**base, "terms_class": "AUTHOR_RUN_ONLY", "metric_format_state": "canonical"},
            "PASS",
            [
                "terms_governance",
                "author_run_return_gate",
                "aggregate_schema_validator",
                "partial_label_classifier",
                "safe_interpretation_classifier",
            ],
        ),
        (
            "ambiguous_terms_block",
            {**base, "terms_class": "AMBIGUOUS_TERMS_BLOCK", "metric_format_state": "canonical"},
            "BLOCKED",
            ["terms_governance", "stop_terms_block"],
        ),
        (
            "no_processing_block",
            {**base, "terms_class": "NO_PROCESSING_ALLOWED", "metric_format_state": "canonical"},
            "BLOCKED",
            ["terms_governance", "stop_terms_block"],
        ),
    ]
    rows = [check_case(name, outdir, kwargs, expected_status, expected_order) for name, kwargs, expected_status, expected_order in cases]
    write_tsv(
        outdir / "returned_package_command_order_synthetic_cases.tsv",
        rows,
        [
            "case",
            "expected_status",
            "observed_status",
            "expected_order",
            "observed_order",
            "order_ok",
            "score_values_read_false",
            "returncode",
            "summary",
        ],
    )
    n_fail = sum(
        1
        for row in rows
        if row["expected_status"] != row["observed_status"]
        or row["order_ok"] != "true"
        or row["score_values_read_false"] != "true"
        or row["returncode"] != 0
    )
    summary = {
        "synthetic": True,
        "purpose": "V46 returned-package command-order planner synthetic check; no biological claim",
        "n_cases": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "cases": rel(outdir / "returned_package_command_order_synthetic_cases.tsv"),
    }
    (outdir / "returned_package_command_order_synthetic_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_fail == 0 else 2


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir)
    return plan(args)


if __name__ == "__main__":
    raise SystemExit(main())
