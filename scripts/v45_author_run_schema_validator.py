#!/usr/bin/env python3
"""Validate value-level schema of author-run aggregate result packages.

This is validation-readiness infrastructure only. It checks aggregate files for
internally consistent fields, numeric ranges, allowed statuses, and unscoreable
failure-code behavior. It does not inspect raw data, private labels, or make any
biological claim.
"""

from __future__ import annotations

import argparse
import json
import math
import shutil
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_author_run_schema_validator"
COMPLETE_ROOT = ROOT / "analysis/v45_author_run_output_check/synthetic_complete_author_run_package"

VERDICT_VALUES = {
    "PASS_CLEAN",
    "PASS_ATTENUATED",
    "FAIL",
    "INCONCLUSIVE",
    "UNSCOREABLE",
    "NOT_SCOREABLE",
    "BLOCKED",
}
ADJUSTMENT_VERDICTS = {
    "SURVIVES",
    "ATTENUATES",
    "EXPLAINED_AWAY",
    "NOT_SCOREABLE",
    "NO_BATCH_METADATA",
    "NO_CONFOUNDER_METADATA",
    "MISSING",
    "BLOCKED",
    "PASS",
    "FAIL",
    "WARN",
}
BOOL_VALUES = {"true", "false", "yes", "no", "1", "0"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run")
    run.add_argument("--root", type=Path, required=True)
    run.add_argument("--package-state", choices=["scored", "unscoreable"], default="scored")
    run.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    run.add_argument("--fail-on-error", action="store_true")

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


def read_json(path: Path) -> dict[str, object]:
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def add(rows: list[dict[str, object]], file: str, check: str, status: str, detail: str) -> None:
    rows.append({"file": file, "check": check, "status": status, "detail": detail})


def as_float(value: object) -> float | None:
    try:
        number = float(value)
    except Exception:
        return None
    return number if math.isfinite(number) else None


def as_int(value: object) -> int | None:
    try:
        return int(value)
    except Exception:
        return None


def check_range(rows: list[dict[str, object]], file: str, check: str, value: object, low: float, high: float) -> None:
    number = as_float(value)
    if number is None or number < low or number > high:
        add(rows, file, check, "FAIL", f"value {value!r} outside [{low}, {high}]")
    else:
        add(rows, file, check, "PASS", f"value={number}")


def check_ci(rows: list[dict[str, object]], file: str, prefix: str, low: object, mid: object, high: object) -> None:
    lo = as_float(low)
    val = as_float(mid)
    hi = as_float(high)
    if lo is None or val is None or hi is None or not (0 <= lo <= val <= hi <= 1):
        add(rows, file, f"{prefix}_ci_order", "FAIL", f"expected 0 <= low <= value <= high <= 1, got {low}, {mid}, {high}")
    else:
        add(rows, file, f"{prefix}_ci_order", "PASS", f"{lo} <= {val} <= {hi}")


def check_summary(root: Path, package_state: str, rows: list[dict[str, object]]) -> dict[str, object]:
    file = "validation_summary.json"
    data = read_json(root / file)
    if not data:
        add(rows, file, "json_readable", "FAIL", "missing or unreadable JSON")
        return {}
    add(rows, file, "json_readable", "PASS", "readable")

    verdict = str(data.get("final_verdict") or data.get("result_class") or data.get("primary_status") or "")
    if not verdict:
        add(rows, file, "verdict_present", "FAIL", "no final_verdict/result_class/primary_status")
    else:
        status = "PASS" if verdict in VERDICT_VALUES or package_state == "scored" else "WARN"
        add(rows, file, "verdict_present", status, verdict)

    n = as_int(data.get("n", data.get("n_labeled")))
    n_labeled = as_int(data.get("n_labeled", data.get("n")))
    n_resp = as_int(data.get("n_responders"))
    n_non = as_int(data.get("n_nonresponders"))
    if None in {n, n_labeled, n_resp, n_non} or min(n or 0, n_labeled or 0, n_resp or 0, n_non or 0) < 0:
        add(rows, file, "counts_parse", "FAIL", "n/n_labeled/n_responders/n_nonresponders must be non-negative integers")
    elif n_resp + n_non != n_labeled:
        add(rows, file, "counts_sum", "FAIL", f"responders+nonresponders={n_resp+n_non}, n_labeled={n_labeled}")
    else:
        add(rows, file, "counts_sum", "PASS", f"n_labeled={n_labeled}")

    for key in ["primary_auc", "primary_auc_ci_low", "primary_auc_ci_high", "receptor_auc"]:
        if key in data:
            check_range(rows, file, key, data[key], 0, 1)
    if {"primary_auc", "primary_auc_ci_low", "primary_auc_ci_high"}.issubset(data):
        check_ci(rows, file, "primary_auc", data["primary_auc_ci_low"], data["primary_auc"], data["primary_auc_ci_high"])
    return data


def read_table(root: Path, file: str, rows: list[dict[str, object]]) -> pd.DataFrame:
    path = root / file
    if not path.exists():
        add(rows, file, "file_present", "FAIL", "missing")
        return pd.DataFrame()
    try:
        table = pd.read_csv(path, sep="\t").fillna("")
    except Exception as exc:
        add(rows, file, "tsv_readable", "FAIL", f"parse failed: {exc}")
        return pd.DataFrame()
    if table.empty:
        add(rows, file, "nonempty", "FAIL", "no rows")
    else:
        add(rows, file, "nonempty", "PASS", f"rows={len(table)}")
    return table


def check_metrics_table(root: Path, summary: dict[str, object], rows: list[dict[str, object]]) -> None:
    file = "locked_rule_metrics.tsv"
    table = read_table(root, file, rows)
    required = {"feature", "n", "n_responders", "n_nonresponders", "auc", "auc_ci_low", "auc_ci_high", "permutation_p"}
    missing = sorted(required - set(table.columns))
    if missing:
        add(rows, file, "required_columns", "FAIL", ",".join(missing))
        return
    add(rows, file, "required_columns", "PASS", "all required columns present")
    if "v22_locked_signed_score" not in set(table["feature"].astype(str)):
        add(rows, file, "primary_feature_present", "FAIL", "missing v22_locked_signed_score row")
    else:
        add(rows, file, "primary_feature_present", "PASS", "present")
    for idx, record in table.iterrows():
        label = f"row_{idx}_{record['feature']}"
        check_range(rows, file, f"{label}_auc", record["auc"], 0, 1)
        check_range(rows, file, f"{label}_p", record["permutation_p"], 0, 1)
        check_ci(rows, file, f"{label}_auc", record["auc_ci_low"], record["auc"], record["auc_ci_high"])
        n = as_int(record["n"])
        n_resp = as_int(record["n_responders"])
        n_non = as_int(record["n_nonresponders"])
        if None in {n, n_resp, n_non} or n_resp + n_non != n:
            add(rows, file, f"{label}_counts", "FAIL", "n must equal n_responders+n_nonresponders")
        else:
            add(rows, file, f"{label}_counts", "PASS", f"n={n}")
    primary = table.loc[table["feature"].astype(str) == "v22_locked_signed_score"]
    if not primary.empty and summary:
        row = primary.iloc[0]
        for metric, source_key in [("n", "n"), ("n_responders", "n_responders"), ("n_nonresponders", "n_nonresponders")]:
            lhs = as_int(row[metric])
            rhs = as_int(summary.get(source_key))
            if lhs is not None and rhs is not None and lhs != rhs:
                add(rows, file, f"primary_{metric}_matches_summary", "FAIL", f"{lhs} != {rhs}")
            else:
                add(rows, file, f"primary_{metric}_matches_summary", "PASS", str(lhs))


def check_gene_mapping(root: Path, rows: list[dict[str, object]]) -> None:
    file = "gene_mapping_coverage.tsv"
    table = read_table(root, file, rows)
    required = {"module", "n_genes", "n_present", "scoreable", "threshold"}
    missing = sorted(required - set(table.columns))
    if missing:
        add(rows, file, "required_columns", "FAIL", ",".join(missing))
        return
    add(rows, file, "required_columns", "PASS", "all required columns present")
    for idx, record in table.iterrows():
        n_genes = as_int(record["n_genes"])
        n_present = as_int(record["n_present"])
        threshold = as_float(record["threshold"])
        scoreable = str(record["scoreable"]).strip().lower()
        label = f"row_{idx}_{record['module']}"
        if n_genes is None or n_present is None or n_genes <= 0 or not (0 <= n_present <= n_genes):
            add(rows, file, f"{label}_counts", "FAIL", "expected 0 <= n_present <= n_genes and n_genes > 0")
        else:
            add(rows, file, f"{label}_counts", "PASS", f"{n_present}/{n_genes}")
        if threshold is None or threshold < 0 or threshold > 1:
            add(rows, file, f"{label}_threshold", "FAIL", f"bad threshold {record['threshold']!r}")
        else:
            add(rows, file, f"{label}_threshold", "PASS", str(threshold))
        if scoreable not in BOOL_VALUES:
            add(rows, file, f"{label}_scoreable_bool", "FAIL", f"bad scoreable {record['scoreable']!r}")
        else:
            add(rows, file, f"{label}_scoreable_bool", "PASS", scoreable)


def check_adjustment_table(root: Path, file: str, verdict_col: str, rows: list[dict[str, object]]) -> None:
    table = read_table(root, file, rows)
    if verdict_col not in table.columns:
        add(rows, file, "verdict_column", "FAIL", f"missing {verdict_col}")
        return
    for idx, record in table.iterrows():
        label = f"row_{idx}"
        verdict = str(record[verdict_col]).strip()
        if verdict and verdict not in ADJUSTMENT_VERDICTS:
            add(rows, file, f"{label}_verdict_allowed", "WARN", verdict)
        else:
            add(rows, file, f"{label}_verdict_allowed", "PASS", verdict or "blank")
        for col in [c for c in table.columns if "auc" in c.lower() or c.endswith("_p") or c == "permutation_p"]:
            value = record[col]
            if str(value).strip() == "":
                continue
            check_range(rows, file, f"{label}_{col}", value, 0, 1)


def check_attrition(root: Path, summary: dict[str, object], rows: list[dict[str, object]]) -> None:
    file = "sample_attrition.tsv"
    table = read_table(root, file, rows)
    if table.empty:
        return
    if "included" not in table.columns:
        add(rows, file, "included_column", "FAIL", "missing included")
        return
    included = table["included"].astype(str).str.lower()
    bad = sorted(set(included) - {"true", "false", "yes", "no", "1", "0"})
    if bad:
        add(rows, file, "included_bool_values", "FAIL", ",".join(bad))
    else:
        add(rows, file, "included_bool_values", "PASS", "parseable")
    n_summary = as_int(summary.get("n", summary.get("n_labeled"))) if summary else None
    n_included = int(included.isin({"true", "yes", "1"}).sum())
    if n_summary is not None and n_included != n_summary:
        add(rows, file, "included_count_matches_summary", "WARN", f"included={n_included}, summary_n={n_summary}")
    elif n_summary is not None:
        add(rows, file, "included_count_matches_summary", "PASS", str(n_included))


def check_unscoreable(root: Path, package_state: str, rows: list[dict[str, object]]) -> None:
    file = "failure_taxonomy_code.txt"
    path = root / file
    if package_state == "unscoreable":
        if not path.exists() or not path.read_text(errors="ignore").strip():
            add(rows, file, "unscoreable_failure_code", "FAIL", "required for unscoreable package")
        else:
            add(rows, file, "unscoreable_failure_code", "PASS", path.read_text(errors="ignore").strip().splitlines()[0])
    elif path.exists() and path.read_text(errors="ignore").strip():
        add(rows, file, "scored_failure_code_absent", "WARN", "failure code present in scored package")
    else:
        add(rows, file, "scored_failure_code_absent", "PASS", "absent")


def validate(root: Path, package_state: str, outdir: Path, fail_on_error: bool) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    root = resolve(root)
    rows: list[dict[str, object]] = []
    summary = check_summary(root, package_state, rows)
    check_metrics_table(root, summary, rows)
    check_gene_mapping(root, rows)
    check_adjustment_table(root, "confounder_adjustment_metrics.tsv", "verdict", rows)
    check_adjustment_table(root, "joint_confounder_metrics.tsv", "verdict", rows)
    check_adjustment_table(root, "batch_diagnostic_metrics.tsv", "verdict", rows)
    check_attrition(root, summary, rows)
    check_unscoreable(root, package_state, rows)

    table = pd.DataFrame(rows)
    table.to_csv(outdir / "author_run_schema_validation.tsv", sep="\t", index=False)
    counts = table["status"].value_counts().sort_index().to_dict()
    n_fail = int((table["status"] == "FAIL").sum())
    overall = "PASS" if n_fail == 0 else "FAIL"
    root_lower = str(root).lower()
    result = {
        "synthetic": "synthetic" in root_lower or "v42_harness_validation" in root_lower,
        "purpose": "author-run aggregate schema validation; no biological claim",
        "root": rel(root),
        "package_state": package_state,
        "n_checks": int(len(table)),
        "n_fail": n_fail,
        "status_counts": counts,
        "overall_status": overall,
        "table": rel(outdir / "author_run_schema_validation.tsv"),
    }
    (outdir / "author_run_schema_validation_summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if fail_on_error and n_fail else 0


def synthetic_check(outdir: Path) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    good = outdir / "synthetic_good_package"
    bad = outdir / "synthetic_bad_metrics_package"
    unscoreable = outdir / "synthetic_unscoreable_missing_code_package"
    for path in [good, bad, unscoreable]:
        if path.exists():
            shutil.rmtree(path)
        shutil.copytree(COMPLETE_ROOT, path)

    locked = pd.read_csv(bad / "locked_rule_metrics.tsv", sep="\t")
    locked.loc[0, "auc"] = 1.3
    locked.loc[0, "auc_ci_low"] = 0.9
    locked.loc[0, "auc_ci_high"] = 0.7
    locked.to_csv(bad / "locked_rule_metrics.tsv", sep="\t", index=False)
    summary = read_json(bad / "validation_summary.json")
    summary["n_responders"] = 99
    (bad / "validation_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    results = [
        ("good", good, "scored", "PASS"),
        ("bad_metrics", bad, "scored", "FAIL"),
        ("unscoreable_missing_code", unscoreable, "unscoreable", "FAIL"),
    ]
    rows = []
    for name, root, state, expected in results:
        rc = validate(root, state, outdir / name, False)
        summary_path = outdir / name / "author_run_schema_validation_summary.json"
        observed = read_json(summary_path).get("overall_status", "MISSING")
        rows.append(
            {
                "case": name,
                "root": rel(root),
                "package_state": state,
                "expected_status": expected,
                "observed_status": observed,
                "expectation_met": observed == expected,
                "returncode": rc,
                "summary": rel(summary_path),
            }
        )
    table = pd.DataFrame(rows)
    table.to_csv(outdir / "synthetic_author_run_schema_cases.tsv", sep="\t", index=False)
    n_mismatch = int((~table["expectation_met"]).sum())
    summary = {
        "synthetic": True,
        "purpose": "synthetic author-run schema validator cases; no biological claim",
        "n_cases": int(len(table)),
        "n_mismatch": n_mismatch,
        "overall_status": "PASS" if n_mismatch == 0 else "FAIL",
        "cases": rel(outdir / "synthetic_author_run_schema_cases.tsv"),
    }
    (outdir / "synthetic_author_run_schema_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_mismatch == 0 else 2


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(resolve(args.outdir))
    return validate(resolve(args.root), args.package_state, resolve(args.outdir), args.fail_on_error)


if __name__ == "__main__":
    raise SystemExit(main())
