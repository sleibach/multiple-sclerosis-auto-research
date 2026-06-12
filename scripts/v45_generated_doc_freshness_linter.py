#!/usr/bin/env python3
"""Lint selected human-facing V45 docs against machine-readable summaries.

This is documentation governance only. It does not inspect data or run
validation. The linter checks that key count/timing strings in docs match the
current generated JSON/TSV outputs.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_generated_doc_freshness_linter"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_json(rel_path: str) -> dict[str, object]:
    return json.loads((ROOT / rel_path).read_text())


def stale_detector_artifact_count() -> int:
    module_path = ROOT / "scripts/v45_readiness_stale_output_detector.py"
    spec = importlib.util.spec_from_file_location("v45_readiness_stale_output_detector", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return len(module.CHECKS)


def doc_contains(doc: str, expected: str) -> bool:
    return expected in (ROOT / doc).read_text()


def add(rows: list[dict[str, str]], doc: str, source: str, label: str, expected: str) -> None:
    rows.append(
        {
            "doc": doc,
            "source": source,
            "label": label,
            "expected_text": expected,
            "status": "PASS" if doc_contains(doc, expected) else "FAIL",
        }
    )


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    artifact = read_json("analysis/v45_artifact_index/summary.json")
    storage = read_json("analysis/v45_compute_storage_summary/summary.json")
    synthetic = read_json("analysis/v45_synthetic_artifact_index/summary.json")
    precommit = read_json("analysis/v45_precommit_readiness/precommit_readiness_summary.json")
    regression = read_json("analysis/v45_regression_aggregator/regression_aggregator_summary.json")
    stale_count = stale_detector_artifact_count()

    rows: list[dict[str, str]] = []

    add(rows, "docs/validation/V45_GOVERNANCE_REFRESH.md", "analysis/v45_artifact_index/summary.json", "artifact_paths", f"| artifact-index paths | `{artifact['n_paths_indexed']}` |")
    add(rows, "docs/validation/V45_GOVERNANCE_REFRESH.md", "analysis/v45_synthetic_artifact_index/summary.json", "synthetic_dirs", f"| V43-V45 method/governance directories | `{synthetic['n_dirs_indexed']}` |")
    add(rows, "docs/validation/V45_GOVERNANCE_REFRESH.md", "analysis/v45_compute_storage_summary/summary.json", "storage_dirs", f"| V45 analysis directories in storage summary | `{storage['n_v45_analysis_dirs']}` |")
    add(rows, "docs/validation/V45_GOVERNANCE_REFRESH.md", "analysis/v45_compute_storage_summary/summary.json", "storage_files", f"| V45 analysis files in storage summary | `{storage['n_files']}` |")
    add(rows, "docs/validation/V45_GOVERNANCE_REFRESH.md", "analysis/v45_compute_storage_summary/summary.json", "storage_mib", f"| V45 analysis footprint | `{storage['total_mib']:.3f} MiB` |")

    add(rows, "docs/validation/V45_ARTIFACT_INDEX.md", "analysis/v45_artifact_index/summary.json", "artifact_paths_sentence", f"The current run indexes `{artifact['n_paths_indexed']}` paths")
    front_label = {
        "cohort_dependence": "cohort dependence",
        "data_free_validation": "data-free validation",
        "external_account": "external account",
        "infrastructure": "infrastructure",
        "infrastructure_rpt": "infrastructure/RPT",
        "power_design": "power/design",
        "resume_backbone": "resume backbone",
        "robustness": "robustness",
    }
    for front, count in artifact["front_counts"].items():
        add(rows, "docs/validation/V45_ARTIFACT_INDEX.md", "analysis/v45_artifact_index/summary.json", f"front_{front}", f"| {front_label[front]} | {count} |")
    evidence_label = {
        "documentation_or_governance": "documentation/governance",
        "internal_convergence_null": "internal convergence null",
        "proposal_lens_grounding": "proposal-lens grounding",
        "public_or_external_acquisition_operations": "public/external acquisition operations",
        "resume_state": "resume state",
        "software": "software",
        "synthesis_documentation": "synthesis documentation",
        "synthetic_method_behavior": "synthetic method behavior",
        "validation_infrastructure": "validation infrastructure",
    }
    for evidence, count in artifact["evidence_class_counts"].items():
        add(rows, "docs/validation/V45_ARTIFACT_INDEX.md", "analysis/v45_artifact_index/summary.json", f"evidence_{evidence}", f"| {evidence_label[evidence]} | {count} |")

    add(rows, "docs/validation/V45_COMPUTE_STORAGE_SUMMARY.md", "analysis/v45_compute_storage_summary/summary.json", "storage_dirs", f"| V45 analysis directories | {storage['n_v45_analysis_dirs']} |")
    add(rows, "docs/validation/V45_COMPUTE_STORAGE_SUMMARY.md", "analysis/v45_compute_storage_summary/summary.json", "storage_files", f"| files | {storage['n_files']} |")
    add(rows, "docs/validation/V45_COMPUTE_STORAGE_SUMMARY.md", "analysis/v45_compute_storage_summary/summary.json", "storage_total", f"| total size | {storage['total_mib']:.3f} MiB |")

    add(rows, "docs/validation/PRECOMMIT_READINESS_CHECKLIST_V45.md", "analysis/v45_precommit_readiness/precommit_readiness_summary.json", "precommit_total", f"| total | `PASS` | `{precommit['total_elapsed_seconds']:.3f}` |")
    add(rows, "docs/validation/V45_READINESS_CHANGELOG.md", "analysis/v45_precommit_readiness/precommit_readiness_summary.json", "changelog_precommit", f"precommit readiness: `5/5` pass in `{precommit['total_elapsed_seconds']:.3f}` seconds")

    add(rows, "docs/validation/SYNTHETIC_ARTIFACT_RETENTION_INDEX_V45.md", "analysis/v45_synthetic_artifact_index/summary.json", "synthetic_dirs", f"The refreshed index covers `{synthetic['n_dirs_indexed']}` V43-V45 analysis directories")
    add(rows, "docs/validation/SYNTHETIC_ARTIFACT_RETENTION_INDEX_V45.md", "analysis/v45_synthetic_artifact_index/summary.json", "synthetic_marked_dirs", f"with `{synthetic['n_dirs_containing_synthetic']}`")
    add(rows, "docs/validation/SYNTHETIC_OUTPUT_RETENTION_POLICY_V45.md", "analysis/v45_synthetic_artifact_index/summary.json", "policy_dirs", f"- `{synthetic['n_dirs_indexed']}` V43-V45 analysis directories;")
    add(rows, "docs/validation/SYNTHETIC_OUTPUT_RETENTION_POLICY_V45.md", "analysis/v45_synthetic_artifact_index/summary.json", "policy_marked_dirs", f"- `{synthetic['n_dirs_containing_synthetic']}` directories with synthetic path/content markers;")

    add(rows, "docs/validation/V45_REGRESSION_AGGREGATOR.md", "analysis/v45_regression_aggregator/regression_aggregator_summary.json", "regression_total", f"Total runtime: `{regression['total_elapsed_seconds']:.3f}` seconds.")
    add(rows, "docs/validation/READINESS_STALE_OUTPUT_DETECTOR_V45.md", "scripts/v45_readiness_stale_output_detector.py", "stale_artifacts_checked", f"- artifacts checked: `{stale_count}`")

    table = pd.DataFrame(rows)
    table.to_csv(outdir / "generated_doc_freshness_lint.tsv", sep="\t", index=False)
    n_fail = int((table["status"] == "FAIL").sum())
    summary = {
        "synthetic": False,
        "purpose": "V45 generated-doc freshness linter; no biological claim",
        "n_checks": int(len(table)),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "table": rel(outdir / "generated_doc_freshness_lint.tsv"),
    }
    (outdir / "generated_doc_freshness_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
