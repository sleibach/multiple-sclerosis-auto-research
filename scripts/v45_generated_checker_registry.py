#!/usr/bin/env python3
"""Create a registry linking V45/V46 scripts to docs, outputs, and summaries.

This is reviewer/navigation infrastructure. It does not run any checker and
does not make biological claims.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v45_generated_checker_registry"

OUTPUT_EXCEPTIONS = {
    "v45_author_run_packet_checksum_manifest": ["analysis/v45_author_run_packet_checksums"],
    "v45_collaborator_package_path_resolver": ["analysis/v45_collaborator_path_resolver"],
    "v45_followup_due_board": ["analysis/v45_followup_due_board"],
    "v45_followup_escalation_packet_generator": ["analysis/v45_followup_escalation_packets"],
    "v45_followup_message_template_generator": ["analysis/v45_followup_message_templates"],
    "v45_external_blocker_board": ["analysis/v45_external_blocker_board"],
    "v45_readiness_status_dashboard": ["analysis/v45_readiness_status_dashboard"],
    "v45_request_sent_updater": ["analysis/v45_request_sent_updater"],
    "v45_received_status_updater": ["analysis/v45_received_status_updater"],
    "v45_route_arrival_packet_generator": ["analysis/v45_route_arrival_packets"],
    "v45_author_run_return_gate_runner": ["analysis/v45_author_run_return_gate_runner"],
    "v45_author_run_redaction_precheck": ["analysis/v45_author_run_redaction_precheck"],
    "v45_author_run_output_check": [
        "analysis/v45_author_run_output_check",
        "analysis/v45_author_run_output_check_incomplete",
    ],
    "v45_leave_one_family_convergence": ["analysis/v45_convergence_family_jackknife"],
    "v45_prepare_gse228330_pharmacodynamic_runbook": ["analysis/v45_gse228330_pharmacodynamic_runbook"],
    "v45_postpartum_harness_pathology_simulation": ["analysis/v45_postpartum_pathology"],
    "v45_refresh_governance_summaries": ["analysis/v45_governance_refresh"],
    "v45_secondary_real_cohort_harness": ["analysis/v45_secondary_real_ingest"],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def docs_for_script(script_name: str) -> list[str]:
    refs = []
    for path in sorted((ROOT / "docs").rglob("*.md")):
        text = path.read_text(errors="ignore")
        if script_name in text:
            refs.append(rel(path))
    for path in sorted((ROOT / "meta").glob("*.md")):
        text = path.read_text(errors="ignore")
        if script_name in text:
            refs.append(rel(path))
    return refs


def likely_output_dirs(stem: str) -> list[str]:
    dirs = set(OUTPUT_EXCEPTIONS.get(stem, []))
    version = stem.split("_", 1)[0]
    suffix = stem.removeprefix(f"{version}_")
    for path in sorted((ROOT / "analysis").iterdir()):
        if not path.is_dir() or not (path.name.startswith("v45") or path.name.startswith("v46")):
            continue
        if path.name == stem or path.name == f"{version}_{suffix}":
            dirs.add(rel(path))
        elif suffix in path.name or path.name.removeprefix(f"{version}_") in suffix:
            dirs.add(rel(path))
    return sorted(dirs)


def summary_statuses(output_dirs: list[str]) -> tuple[list[str], list[str]]:
    summary_paths: list[str] = []
    statuses: list[str] = []
    for directory in output_dirs:
        path = ROOT / directory
        if not path.exists():
            continue
        for json_path in sorted(path.rglob("*.json")):
            if "summary" not in json_path.name:
                continue
            summary_paths.append(rel(json_path))
            try:
                data = json.loads(json_path.read_text())
            except json.JSONDecodeError:
                statuses.append("UNREADABLE_JSON")
                continue
            status = data.get("overall_status") or data.get("headline_status") or data.get("status")
            if status:
                statuses.append(str(status))
    return summary_paths, sorted(set(statuses))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)

    rows = []
    scripts = sorted((ROOT / "scripts").glob("v45_*.py")) + sorted((ROOT / "scripts").glob("v46_*.py"))
    for script in scripts:
        stem = script.stem
        doc_refs = docs_for_script(script.name)
        outputs = likely_output_dirs(stem)
        summary_paths, statuses = summary_statuses(outputs)
        rows.append(
            {
                "script": rel(script),
                "doc_status": "DOCUMENTED" if doc_refs else "NO_DOC_REFERENCE_FOUND",
                "n_doc_refs": len(doc_refs),
                "doc_refs": ";".join(doc_refs[:20]),
                "n_output_dirs": len(outputs),
                "output_dirs": ";".join(outputs),
                "n_summary_json": len(summary_paths),
                "summary_json": ";".join(summary_paths[:40]),
                "observed_statuses": ";".join(statuses) if statuses else "none",
            }
        )

    registry = outdir / "generated_checker_registry.tsv"
    fieldnames = [
        "script",
        "doc_status",
        "n_doc_refs",
        "doc_refs",
        "n_output_dirs",
        "output_dirs",
        "n_summary_json",
        "summary_json",
        "observed_statuses",
    ]
    with registry.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    n_undocumented = sum(1 for row in rows if row["doc_status"] != "DOCUMENTED")
    n_without_outputs = sum(1 for row in rows if row["n_output_dirs"] == 0)
    summary = {
        "synthetic": False,
        "purpose": "V45/V46 generated-checker registry; no biological claim",
        "registry": rel(registry),
        "n_scripts": len(rows),
        "n_undocumented": n_undocumented,
        "n_without_output_dirs": n_without_outputs,
        "overall_status": "PASS" if n_undocumented == 0 else "REVIEW_NEEDED",
    }
    (outdir / "generated_checker_registry_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
