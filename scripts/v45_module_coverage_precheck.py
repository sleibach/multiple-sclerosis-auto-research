#!/usr/bin/env python3
"""Precheck frozen module gene coverage before full harness execution."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from v42_gafson_validation_harness import ALL_MODULES, IFN_APC, HLAII, RECEPTOR, normalize_gene_id


PRIMARY_REQUIRED = {"IFN_APC": IFN_APC, "HLAII": HLAII, "RECEPTOR": RECEPTOR}


def load_gene_ids(expression: Path) -> set[str]:
    genes = pd.read_csv(expression, sep="\t", usecols=[0]).iloc[:, 0].tolist()
    return {normalize_gene_id(gene) for gene in genes}


def coverage_table(gene_ids: set[str], modules: dict[str, list[str]]) -> pd.DataFrame:
    rows = []
    for module, genes in modules.items():
        normalized = [normalize_gene_id(g) for g in genes]
        present = [gene for gene in normalized if gene in gene_ids]
        missing = [gene for gene in normalized if gene not in gene_ids]
        frac = len(present) / len(normalized) if normalized else 0.0
        rows.append(
            {
                "module": module,
                "n_genes": len(normalized),
                "n_present": len(present),
                "coverage_fraction": frac,
                "scoreable_ge_0p50": frac >= 0.50,
                "complete": len(missing) == 0,
                "present_genes": ";".join(present),
                "missing_genes": ";".join(missing),
            }
        )
    return pd.DataFrame(rows)


def run_precheck(expression: Path, outdir: Path) -> dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    gene_ids = load_gene_ids(expression)
    primary = coverage_table(gene_ids, PRIMARY_REQUIRED)
    all_modules = coverage_table(gene_ids, ALL_MODULES)
    primary.to_csv(outdir / "primary_module_coverage.tsv", sep="\t", index=False)
    all_modules.to_csv(outdir / "all_module_coverage.tsv", sep="\t", index=False)
    primary_pass = bool(primary["scoreable_ge_0p50"].all())
    confounder_scoreable = int(all_modules["scoreable_ge_0p50"].sum())
    summary = {
        "expression": str(expression),
        "n_unique_gene_ids": int(len(gene_ids)),
        "primary_modules_scoreable": primary_pass,
        "n_primary_modules": int(len(primary)),
        "n_all_modules": int(len(all_modules)),
        "n_all_modules_scoreable_ge_0p50": confounder_scoreable,
        "overall_status": "PASS" if primary_pass else "FAIL_PRIMARY_MODULE_COVERAGE",
        "scores_computed": False,
        "outcomes_read": False,
    }
    (outdir / "module_coverage_precheck_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def write_synthetic_expression(path: Path, missing_hlaii: bool) -> None:
    genes = sorted({gene for genes in ALL_MODULES.values() for gene in genes} | {f"CONTROL{i}" for i in range(10)})
    if missing_hlaii:
        genes = [gene for gene in genes if gene not in {"HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"}]
    frame = pd.DataFrame({"S1": [1.0] * len(genes), "S2": [2.0] * len(genes)}, index=genes)
    frame.to_csv(path, sep="\t")


def synthetic_check(outdir: Path) -> dict[str, object]:
    outdir.mkdir(parents=True, exist_ok=True)
    synth = outdir / "synthetic"
    synth.mkdir(exist_ok=True)
    full_expr = synth / "full_module_expression.tsv"
    missing_expr = synth / "missing_hlaii_expression.tsv"
    write_synthetic_expression(full_expr, missing_hlaii=False)
    write_synthetic_expression(missing_expr, missing_hlaii=True)
    full = run_precheck(full_expr, outdir / "full_module_expression")
    missing = run_precheck(missing_expr, outdir / "missing_hlaii_expression")
    assertions = {
        "synthetic": True,
        "full_expression_pass": full["overall_status"] == "PASS",
        "missing_hlaii_fails": missing["overall_status"] == "FAIL_PRIMARY_MODULE_COVERAGE",
        "scores_computed": False,
        "outcomes_read": False,
        "full_summary": full,
        "missing_summary": missing,
    }
    assertions["overall_status"] = "PASS" if assertions["full_expression_pass"] and assertions["missing_hlaii_fails"] else "FAIL"
    (outdir / "synthetic_check_assertions.json").write_text(json.dumps(assertions, indent=2, sort_keys=True) + "\n")
    return assertions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Check module gene coverage for one expression matrix.")
    check.add_argument("--expression", required=True, type=Path)
    check.add_argument("--outdir", required=True, type=Path)
    check.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run passing and failing synthetic coverage checks.")
    synth.add_argument("--outdir", required=True, type=Path)
    args = parser.parse_args()
    if args.command == "check":
        summary = run_precheck(args.expression, args.outdir)
        print(json.dumps(summary, indent=2, sort_keys=True))
        if args.fail_on_error and summary["overall_status"] != "PASS":
            return 2
        return 0
    assertions = synthetic_check(args.outdir)
    print(json.dumps(assertions, indent=2, sort_keys=True))
    return 0 if assertions["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
