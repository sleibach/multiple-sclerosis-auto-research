#!/usr/bin/env python3
"""Generate a compact V48 preflight handoff card."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "knowledge_external/catalogs/indexes"
INPUTS = {
    "governance_preflight": ROOT / "analysis/v48_governance_preflight/v48_governance_preflight_summary.json",
    "provenance_gate": ROOT / "analysis/v47_provenance_gate/provenance_gate_summary.json",
    "governance_navigation": ROOT / "knowledge_external/catalogs/indexes/v48_governance_navigation_summary.json",
    "convergence_matrix": ROOT / "knowledge_external/catalogs/indexes/convergence_contradiction_v48_summary.json",
    "source_terms_packet": ROOT / "knowledge_external/catalogs/indexes/high_priority_source_terms_packet_v48_summary.json",
}
COMMANDS = [
    ("full_preflight", "python3 scripts/v48_governance_preflight.py"),
    ("provenance_gate", "python3 scripts/v47_provenance_gate.py audit"),
    ("governance_navigation", "python3 scripts/v48_governance_navigation.py"),
    ("external_markdown_lint", "python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error"),
    ("public_index_freshness", "python3 scripts/v48_public_index_freshness_linter.py lint --fail-on-error"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=OUTDIR)
    return parser.parse_args()


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return data if isinstance(data, dict) else {}


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build(outdir: Path) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for name, path in INPUTS.items():
        data = read_json(path)
        rows.append(
            {
                "component": name,
                "summary_path": str(path.relative_to(ROOT)),
                "summary_exists": "yes" if path.exists() else "no",
                "overall_status": data.get("overall_status", "MISSING"),
                "n_checks": data.get("n_checks", data.get("n_artifacts", data.get("n_high_priority_records", ""))),
                "n_fail": data.get("n_fail", data.get("n_missing_artifacts", "")),
            }
        )
    command_rows = [{"check": name, "command": command} for name, command in COMMANDS]
    n_missing = sum(1 for row in rows if row["summary_exists"] != "yes")
    n_failed = sum(1 for row in rows if str(row["overall_status"]).upper() not in {"PASS", "MISSING"} and str(row["overall_status"]).upper() != "NOT_APPLICABLE")
    summary = {
        "purpose": "V48 preflight summary card; handoff/navigation only; no biological claim",
        "n_components": len(rows),
        "n_missing_summaries": n_missing,
        "n_components_with_failure_status": n_failed,
        "overall_status": "PASS" if n_missing == 0 and n_failed == 0 else "FAIL",
        "markdown": "knowledge_external/catalogs/indexes/V48_PREFLIGHT_SUMMARY_CARD.md",
        "tsv": "knowledge_external/catalogs/indexes/v48_preflight_summary_card.tsv",
    }
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "v48_preflight_summary_card.tsv", rows, ["component", "summary_path", "summary_exists", "overall_status", "n_checks", "n_fail"])
    write_tsv(outdir / "v48_preflight_summary_card_commands.tsv", command_rows, ["check", "command"])
    (outdir / "v48_preflight_summary_card_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 Preflight Summary Card",
        "",
        "Status: handoff/navigation only. This card summarizes governance controls; it does not validate external claims or provide biological evidence.",
        "",
        f"- overall status: `{summary['overall_status']}`",
        f"- components summarized: `{summary['n_components']}`",
        f"- missing summaries: `{summary['n_missing_summaries']}`",
        f"- components with failure status: `{summary['n_components_with_failure_status']}`",
        "",
        "## Current Status",
        "",
        "| component | status | checks/artifacts | failures/missing | summary |",
        "|---|---|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"`{row['component']}` | "
            f"`{row['overall_status']}` | "
            f"{row['n_checks']} | "
            f"{row['n_fail']} | "
            f"`{row['summary_path']}` |"
        )
    lines.extend(
        [
            "",
            "## Commands",
            "",
            "| check | command |",
            "|---|---|",
        ]
    )
    for row in command_rows:
        lines.append(f"| `{row['check']}` | `{row['command']}` |")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Passing checks mean segregation/provenance/navigation controls passed.",
            "- External knowledge remains external-classed and is not project-grounded evidence.",
            "- Grounded findings, locked rules, and validation pre-registrations remain outside this external layer.",
            "",
        ]
    )
    (outdir / "V48_PREFLIGHT_SUMMARY_CARD.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    summary = build(args.outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
