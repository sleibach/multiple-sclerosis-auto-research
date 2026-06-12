#!/usr/bin/env python3
"""Check completeness of collaborator author-run aggregate outputs.

The checker verifies package completeness against the V45 minimum-output
specification. It does not read raw expression, does not inspect private labels,
and does not interpret biology.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = ROOT / "docs/validation/input_schemas/V45_author_run_minimum_output_spec.tsv"
DEFAULT_OUTDIR = ROOT / "analysis/v45_author_run_output_check"
SYNTHETIC_SOURCE = ROOT / "analysis/v45_primary_harness_regression_tests/v42_primary_synthetic/planted_result"

REQUIRED_COLUMNS = {
    "gene_mapping_coverage.tsv": {"module", "n_genes", "n_present", "scoreable"},
    "locked_rule_metrics.tsv": {"auc", "hedges_g", "auc_ci_low", "auc_ci_high", "permutation_p"},
    "confounder_adjustment_metrics.tsv": {"confounder", "adjusted_auc", "verdict"},
    "joint_confounder_metrics.tsv": {"risk_set", "adjusted_auc", "verdict"},
    "batch_diagnostic_metrics.tsv": {"verdict"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    check = sub.add_parser("check")
    check.add_argument("--root", type=Path, required=True, help="Directory containing returned aggregate outputs.")
    check.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    check.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    check.add_argument("--package-state", choices=["scored", "unscoreable"], default="scored")
    check.add_argument("--fail-on-error", action="store_true")

    syn = sub.add_parser("synthetic-check")
    syn.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def required_now(required_value: str, package_state: str) -> bool:
    value = str(required_value).strip().lower()
    if value == "yes":
        return True
    if value == "yes_if_unscoreable":
        return package_state == "unscoreable"
    return False


def check_file(path: Path) -> tuple[str, str]:
    if not path.exists():
        return "MISSING", "file is absent"
    if path.stat().st_size == 0:
        return "EMPTY", "file is empty"
    name = path.name
    if name.endswith(".json"):
        try:
            data = json.loads(path.read_text())
        except Exception as exc:
            return "UNREADABLE", f"json parse failed: {exc}"
        if name == "validation_summary.json":
            keys = set(data)
            verdict_ok = bool(keys & {"final_verdict", "result_class", "primary_status"})
            n_ok = bool(keys & {"n", "n_labeled"}) and {"n_responders", "n_nonresponders"}.issubset(keys)
            if not verdict_ok or not n_ok:
                return "CONTENT_WARN", "summary lacks expected verdict/count keys"
        return "PRESENT", "json readable"
    if name.endswith(".tsv"):
        try:
            table = pd.read_csv(path, sep="\t")
        except Exception as exc:
            return "UNREADABLE", f"tsv parse failed: {exc}"
        if table.empty:
            return "EMPTY", "tsv has no rows"
        needed = REQUIRED_COLUMNS.get(name, set())
        missing = sorted(needed - set(table.columns))
        if missing:
            return "CONTENT_WARN", f"missing expected columns: {','.join(missing)}"
        return "PRESENT", "tsv readable"
    text = path.read_text(errors="ignore")
    if name == "RUN_METADATA.txt":
        lowered = text.lower()
        if "command" not in lowered or "software" not in lowered:
            return "CONTENT_WARN", "run metadata should include command and software/version notes"
    return "PRESENT", "text readable"


def run_check(root: Path, spec_path: Path, outdir: Path, package_state: str, fail_on_error: bool) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    spec = pd.read_csv(spec_path, sep="\t").fillna("")
    rows = []
    for record in spec.to_dict(orient="records"):
        output_file = str(record["output_file"])
        path = root / output_file
        is_required = required_now(str(record["required"]), package_state)
        status, detail = check_file(path)
        hard_fail = is_required and status in {"MISSING", "EMPTY", "UNREADABLE"}
        rows.append(
            {
                **record,
                "package_state": package_state,
                "root": str(root.relative_to(ROOT)) if root.is_relative_to(ROOT) else str(root),
                "path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
                "required_now": is_required,
                "check_status": status,
                "detail": detail,
                "hard_fail": hard_fail,
            }
        )

    result = pd.DataFrame(rows)
    result.to_csv(outdir / "author_run_output_check.tsv", sep="\t", index=False)
    status_counts = result["check_status"].value_counts().sort_index().to_dict()
    n_hard_fail = int(result["hard_fail"].sum())
    root_lower = str(root).lower()
    summary = {
        "synthetic": "synthetic" in root_lower or "v42_harness_validation" in root_lower,
        "purpose": "author-run returned-output completeness check; no biological claim",
        "root": str(root.relative_to(ROOT)) if root.is_relative_to(ROOT) else str(root),
        "package_state": package_state,
        "n_rows": int(len(result)),
        "n_required_now": int(result["required_now"].sum()),
        "n_hard_fail": n_hard_fail,
        "status_counts": status_counts,
        "overall_status": "PASS" if n_hard_fail == 0 else "FAIL",
    }
    (outdir / "author_run_output_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if fail_on_error and n_hard_fail else 0


def synthetic_check(outdir: Path) -> int:
    package = outdir / "synthetic_complete_author_run_package"
    package.mkdir(parents=True, exist_ok=True)
    for name in [
        "validation_summary.json",
        "sample_attrition.tsv",
        "gene_mapping_coverage.tsv",
        "locked_rule_metrics.tsv",
        "confounder_adjustment_metrics.tsv",
        "joint_confounder_metrics.tsv",
        "batch_diagnostic_metrics.tsv",
    ]:
        shutil.copy2(SYNTHETIC_SOURCE / name, package / name)
    (package / "RUN_METADATA.txt").write_text(
        "synthetic: true\n"
        "command: .venv/bin/python scripts/v42_gafson_validation_harness.py run --expression <local_expression.tsv> --metadata <local_sample_metadata.tsv> --outdir <local_output_dir> --expression-type auto\n"
        "software: synthetic fixture generated by scripts/v45_author_run_output_check.py\n"
    )
    (package / "validation_result_report.md").write_text(
        "# Synthetic Author-Run Validation Result Report\n\n"
        "synthetic: true\n\n"
        "This is a synthetic completeness fixture only and is not biological evidence.\n"
    )
    return run_check(package, DEFAULT_SPEC, outdir, "scored", True)


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir if args.outdir.is_absolute() else ROOT / args.outdir)
    return run_check(
        args.root if args.root.is_absolute() else ROOT / args.root,
        args.spec if args.spec.is_absolute() else ROOT / args.spec,
        args.outdir if args.outdir.is_absolute() else ROOT / args.outdir,
        args.package_state,
        args.fail_on_error,
    )


if __name__ == "__main__":
    raise SystemExit(main())
