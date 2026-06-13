#!/usr/bin/env python3
"""Normalize common author-run aggregate metric format variants.

This is validation-readiness infrastructure only. It adapts collaborator-facing
aggregate table names and column aliases into the exact V45 minimum-output file
names and schemas, then leaves the existing V45 validators to decide whether the
normalized package is acceptable. It does not interpret scores or change values.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v46_author_run_metric_format_adapter"
CANONICAL_PACKAGE = ROOT / "analysis/v45_author_run_output_check/synthetic_complete_author_run_package"

FILE_ALIASES: dict[str, list[str]] = {
    "RUN_METADATA.txt": ["RUN_METADATA.txt", "run_metadata.txt", "run_info.txt", "execution_metadata.txt"],
    "validation_summary.json": ["validation_summary.json", "summary.json", "result_summary.json", "validation_result_summary.json"],
    "sample_attrition.tsv": ["sample_attrition.tsv", "attrition.tsv", "sample_exclusions.tsv", "sample_retention.tsv"],
    "gene_mapping_coverage.tsv": ["gene_mapping_coverage.tsv", "module_gene_coverage.tsv", "gene_coverage.tsv", "module_coverage.tsv"],
    "locked_rule_metrics.tsv": ["locked_rule_metrics.tsv", "metrics.tsv", "primary_metrics.tsv", "locked_rule_results.tsv", "v22_metrics.tsv"],
    "confounder_adjustment_metrics.tsv": ["confounder_adjustment_metrics.tsv", "confounder_metrics.tsv", "confounder_adjusted_metrics.tsv"],
    "joint_confounder_metrics.tsv": ["joint_confounder_metrics.tsv", "joint_adjustment_metrics.tsv", "multi_confounder_metrics.tsv"],
    "batch_diagnostic_metrics.tsv": ["batch_diagnostic_metrics.tsv", "batch_qc.tsv", "batch_diagnostics.tsv", "batch_metrics.tsv"],
    "validation_result_report.md": ["validation_result_report.md", "report.md", "validation_report.md", "result_report.md"],
    "failure_taxonomy_code.txt": ["failure_taxonomy_code.txt", "failure_code.txt", "unscoreable_code.txt"],
}

COLUMN_ALIASES: dict[str, dict[str, str]] = {
    "sample_attrition.tsv": {
        "subject": "patient",
        "sample": "patient",
        "status": "included",
        "exclusion_reason": "reason",
    },
    "gene_mapping_coverage.tsv": {
        "gene_set": "module",
        "module_name": "module",
        "genes_total": "n_genes",
        "total_genes": "n_genes",
        "genes_present": "n_present",
        "present": "n_present",
        "coverage": "fraction_present",
        "can_score": "scoreable",
        "coverage_threshold": "threshold",
    },
    "locked_rule_metrics.tsv": {
        "metric": "feature",
        "score": "feature",
        "score_name": "feature",
        "subjects": "n",
        "n_labeled": "n",
        "responders": "n_responders",
        "non_responders": "n_nonresponders",
        "nonresponders": "n_nonresponders",
        "effect_size": "hedges_g",
        "hedges": "hedges_g",
        "ci_low": "auc_ci_low",
        "auc_lower": "auc_ci_low",
        "ci_high": "auc_ci_high",
        "auc_upper": "auc_ci_high",
        "perm_p": "permutation_p",
        "p_perm": "permutation_p",
    },
    "confounder_adjustment_metrics.tsv": {
        "panel": "confounder",
        "covariate": "confounder",
        "adj_auc": "adjusted_auc",
        "adj_hedges_g": "adjusted_hedges_g",
        "adj_ci_low": "adjusted_auc_ci_low",
        "adj_ci_high": "adjusted_auc_ci_high",
        "perm_p": "adjusted_permutation_p",
        "p_perm": "adjusted_permutation_p",
        "attenuation": "auc_attenuation",
        "status": "verdict",
    },
    "joint_confounder_metrics.tsv": {
        "panel": "risk_set",
        "covariates": "features",
        "feature_set": "features",
        "adj_auc": "adjusted_auc",
        "adj_hedges_g": "adjusted_hedges_g",
        "adj_ci_low": "adjusted_auc_ci_low",
        "adj_ci_high": "adjusted_auc_ci_high",
        "perm_p": "adjusted_permutation_p",
        "p_perm": "adjusted_permutation_p",
        "attenuation": "auc_attenuation",
        "status": "verdict",
    },
    "batch_diagnostic_metrics.tsv": {
        "check": "metadata_feature",
        "field": "metadata_feature",
        "status": "verdict",
        "batch_status": "verdict",
    },
}

SUMMARY_KEY_ALIASES = {
    "result": "final_verdict",
    "verdict": "final_verdict",
    "labeled_n": "n",
    "n_labeled": "n",
    "responders": "n_responders",
    "nonresponders": "n_nonresponders",
    "non_responders": "n_nonresponders",
    "auc": "primary_auc",
    "auc_low": "primary_auc_ci_low",
    "auc_high": "primary_auc_ci_high",
    "ci_low": "primary_auc_ci_low",
    "ci_high": "primary_auc_ci_high",
    "hedges_g": "primary_hedges_g",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    adapt_cmd = sub.add_parser("adapt")
    adapt_cmd.add_argument("--root", type=Path, required=True)
    adapt_cmd.add_argument("--outdir", type=Path, required=True)
    adapt_cmd.add_argument("--fail-on-error", action="store_true")

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


def find_source(root: Path, canonical: str) -> Path | None:
    lower_to_path = {path.name.lower(): path for path in root.iterdir() if path.is_file()}
    for alias in FILE_ALIASES[canonical]:
        path = lower_to_path.get(alias.lower())
        if path:
            return path
    return None


def rename_columns(canonical: str, table: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, str]]:
    aliases = COLUMN_ALIASES.get(canonical, {})
    mapping: dict[str, str] = {}
    used_targets = set(table.columns)
    for column in list(table.columns):
        target = aliases.get(column.strip())
        if target and target not in used_targets:
            mapping[column] = target
            used_targets.add(target)
    if mapping:
        table = table.rename(columns=mapping)
    return table, mapping


def normalize_summary(source: Path, dest: Path) -> dict[str, str]:
    data = json.loads(source.read_text())
    mapping: dict[str, str] = {}
    for key, target in SUMMARY_KEY_ALIASES.items():
        if key in data and target not in data:
            data[target] = data[key]
            mapping[key] = target
    dest.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    return mapping


def adapt(root: Path, outdir: Path, fail_on_error: bool) -> int:
    root = resolve(root)
    outdir = resolve(outdir)
    normalized = outdir / "normalized_package"
    if normalized.exists():
        shutil.rmtree(normalized)
    normalized.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    missing = 0

    for canonical in FILE_ALIASES:
        source = find_source(root, canonical)
        if source is None:
            if canonical == "failure_taxonomy_code.txt":
                continue
            missing += 1
            rows.append(
                {
                    "canonical_file": canonical,
                    "source_file": "",
                    "action": "MISSING",
                    "column_mappings": "",
                    "detail": "no canonical file or accepted alias found",
                }
            )
            continue
        dest = normalized / canonical
        column_mappings: dict[str, str] = {}
        if canonical.endswith(".tsv"):
            table = pd.read_csv(source, sep="\t")
            table, column_mappings = rename_columns(canonical, table)
            table.to_csv(dest, sep="\t", index=False)
            action = "TSV_NORMALIZED" if source.name != canonical or column_mappings else "TSV_COPIED"
        elif canonical == "validation_summary.json":
            column_mappings = normalize_summary(source, dest)
            action = "JSON_NORMALIZED" if source.name != canonical or column_mappings else "JSON_COPIED"
        else:
            shutil.copy2(source, dest)
            action = "COPIED_ALIAS" if source.name != canonical else "COPIED"
        rows.append(
            {
                "canonical_file": canonical,
                "source_file": rel(source),
                "action": action,
                "column_mappings": ";".join(f"{k}->{v}" for k, v in sorted(column_mappings.items())),
                "detail": f"wrote {rel(dest)}",
            }
        )

    manifest = outdir / "metric_format_adapter_manifest.tsv"
    write_tsv(manifest, rows, ["canonical_file", "source_file", "action", "column_mappings", "detail"])
    summary = {
        "synthetic": "synthetic" in str(root).lower(),
        "purpose": "V46 author-run metric format adapter; no biological claim and no score interpretation",
        "source_root": rel(root),
        "normalized_package": rel(normalized),
        "manifest": rel(manifest),
        "n_files": len(rows),
        "n_missing_required": missing,
        "overall_status": "PASS" if missing == 0 else "FAIL",
    }
    (outdir / "metric_format_adapter_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if fail_on_error and missing else 0


def write_variant_table(source: Path, dest: Path, reverse_mapping: dict[str, str]) -> None:
    table = pd.read_csv(source, sep="\t")
    table = table.rename(columns=reverse_mapping)
    dest.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(dest, sep="\t", index=False)


def build_synthetic_variant(root: Path) -> Path:
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CANONICAL_PACKAGE / "RUN_METADATA.txt", root / "run_info.txt")
    shutil.copy2(CANONICAL_PACKAGE / "validation_result_report.md", root / "report.md")

    summary = json.loads((CANONICAL_PACKAGE / "validation_summary.json").read_text())
    variant_summary = {
        "result": summary["final_verdict"],
        "labeled_n": summary["n"],
        "responders": summary["n_responders"],
        "non_responders": summary["n_nonresponders"],
        "auc": summary["primary_auc"],
        "auc_low": summary["primary_auc_ci_low"],
        "auc_high": summary["primary_auc_ci_high"],
        "hedges_g": summary["primary_hedges_g"],
        "batch_guard_flag": summary["batch_guard_flag"],
        "seed": summary["seed"],
    }
    (root / "result_summary.json").write_text(json.dumps(variant_summary, indent=2, sort_keys=True) + "\n")

    write_variant_table(
        CANONICAL_PACKAGE / "sample_attrition.tsv",
        root / "sample_exclusions.tsv",
        {"patient": "subject", "included": "status", "reason": "exclusion_reason"},
    )
    write_variant_table(
        CANONICAL_PACKAGE / "gene_mapping_coverage.tsv",
        root / "module_gene_coverage.tsv",
        {
            "module": "module_name",
            "n_genes": "genes_total",
            "n_present": "genes_present",
            "fraction_present": "coverage",
            "scoreable": "can_score",
        },
    )
    write_variant_table(
        CANONICAL_PACKAGE / "locked_rule_metrics.tsv",
        root / "primary_metrics.tsv",
        {
            "feature": "score_name",
            "n": "subjects",
            "n_responders": "responders",
            "n_nonresponders": "non_responders",
            "hedges_g": "effect_size",
            "auc_ci_low": "auc_lower",
            "auc_ci_high": "auc_upper",
            "permutation_p": "perm_p",
        },
    )
    write_variant_table(
        CANONICAL_PACKAGE / "confounder_adjustment_metrics.tsv",
        root / "confounder_adjusted_metrics.tsv",
        {
            "confounder": "panel",
            "adjusted_auc": "adj_auc",
            "adjusted_hedges_g": "adj_hedges_g",
            "adjusted_auc_ci_low": "adj_ci_low",
            "adjusted_auc_ci_high": "adj_ci_high",
            "adjusted_permutation_p": "perm_p",
            "auc_attenuation": "attenuation",
            "verdict": "status",
        },
    )
    write_variant_table(
        CANONICAL_PACKAGE / "joint_confounder_metrics.tsv",
        root / "multi_confounder_metrics.tsv",
        {
            "risk_set": "panel",
            "features": "covariates",
            "adjusted_auc": "adj_auc",
            "adjusted_hedges_g": "adj_hedges_g",
            "adjusted_auc_ci_low": "adj_ci_low",
            "adjusted_auc_ci_high": "adj_ci_high",
            "adjusted_permutation_p": "perm_p",
            "auc_attenuation": "attenuation",
            "verdict": "status",
        },
    )
    write_variant_table(
        CANONICAL_PACKAGE / "batch_diagnostic_metrics.tsv",
        root / "batch_qc.tsv",
        {"metadata_feature": "check", "verdict": "status"},
    )
    return root


def run_command(command: list[str]) -> dict[str, object]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return {
        "command": " ".join(command),
        "returncode": result.returncode,
        "stdout_tail": result.stdout[-2000:],
        "stderr_tail": result.stderr[-2000:],
    }


def synthetic_check(outdir: Path) -> int:
    outdir = resolve(outdir)
    if outdir.exists():
        shutil.rmtree(outdir)
    variant_root = build_synthetic_variant(outdir / "synthetic_variant_package")
    missing_root = outdir / "synthetic_missing_required_package"
    shutil.copytree(variant_root, missing_root)
    (missing_root / "primary_metrics.tsv").unlink()
    adapter_out = outdir / "adapter"
    adapter_rc = adapt(variant_root, adapter_out, True)
    missing_adapter_out = outdir / "missing_required_adapter"
    missing_adapter_rc = adapt(missing_root, missing_adapter_out, True)
    normalized = adapter_out / "normalized_package"

    completeness = run_command(
        [
            sys.executable,
            "scripts/v45_author_run_output_check.py",
            "check",
            "--root",
            rel(normalized),
            "--package-state",
            "scored",
            "--outdir",
            rel(outdir / "normalized_completeness"),
            "--fail-on-error",
        ]
    )
    schema = run_command(
        [
            sys.executable,
            "scripts/v45_author_run_schema_validator.py",
            "run",
            "--root",
            rel(normalized),
            "--package-state",
            "scored",
            "--outdir",
            rel(outdir / "normalized_schema"),
            "--fail-on-error",
        ]
    )
    checks = [
        {"check": "adapter", "expected": 0, "observed": adapter_rc, "passed": adapter_rc == 0},
        {"check": "missing_required_adapter_blocks", "expected": 1, "observed": missing_adapter_rc, "passed": missing_adapter_rc == 1},
        {"check": "v45_completeness_validator", "expected": 0, "observed": completeness["returncode"], "passed": completeness["returncode"] == 0},
        {"check": "v45_schema_validator", "expected": 0, "observed": schema["returncode"], "passed": schema["returncode"] == 0},
    ]
    write_tsv(outdir / "metric_format_adapter_synthetic_checks.tsv", checks, ["check", "expected", "observed", "passed"])
    (outdir / "validator_command_outputs.json").write_text(json.dumps({"completeness": completeness, "schema": schema}, indent=2, sort_keys=True) + "\n")
    n_fail = sum(1 for row in checks if not row["passed"])
    summary = {
        "synthetic": True,
        "purpose": "V46 author-run metric format adapter synthetic verification; no biological claim",
        "variant_package": rel(variant_root),
        "missing_required_package": rel(missing_root),
        "normalized_package": rel(normalized),
        "adapter_summary": rel(adapter_out / "metric_format_adapter_summary.json"),
        "missing_required_adapter_summary": rel(missing_adapter_out / "metric_format_adapter_summary.json"),
        "check_table": rel(outdir / "metric_format_adapter_synthetic_checks.tsv"),
        "n_checks": len(checks),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "metric_format_adapter_synthetic_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_fail == 0 else 2


def main() -> int:
    args = parse_args()
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir)
    return adapt(args.root, args.outdir, args.fail_on_error)


if __name__ == "__main__":
    raise SystemExit(main())
