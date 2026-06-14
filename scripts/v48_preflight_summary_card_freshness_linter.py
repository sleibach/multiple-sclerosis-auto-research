#!/usr/bin/env python3
"""Check that the V48 preflight summary card matches current summaries."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CARD = ROOT / "knowledge_external/catalogs/indexes/v48_preflight_summary_card.tsv"
DEFAULT_COMMANDS = ROOT / "knowledge_external/catalogs/indexes/v48_preflight_summary_card_commands.tsv"
DEFAULT_SUMMARY = ROOT / "knowledge_external/catalogs/indexes/v48_preflight_summary_card_summary.json"
DEFAULT_OUTDIR = ROOT / "analysis/v48_preflight_summary_card_freshness_linter"
INPUTS = {
    "governance_preflight": ROOT / "analysis/v48_governance_preflight/v48_governance_preflight_summary.json",
    "provenance_gate": ROOT / "analysis/v47_provenance_gate/provenance_gate_summary.json",
    "governance_navigation": ROOT / "knowledge_external/catalogs/indexes/v48_governance_navigation_summary.json",
    "convergence_matrix": ROOT / "knowledge_external/catalogs/indexes/convergence_contradiction_v48_summary.json",
    "source_terms_packet": ROOT / "knowledge_external/catalogs/indexes/high_priority_source_terms_packet_v48_summary.json",
}
COMMANDS = {
    "full_preflight": "python3 scripts/v48_governance_preflight.py",
    "provenance_gate": "python3 scripts/v47_provenance_gate.py audit",
    "governance_navigation": "python3 scripts/v48_governance_navigation.py",
    "external_markdown_lint": "python3 scripts/v47_external_markdown_index_linter.py lint --fail-on-error",
    "public_index_freshness": "python3 scripts/v48_public_index_freshness_linter.py lint --fail-on-error",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint preflight summary card freshness")
    lint.add_argument("--card", type=Path, default=DEFAULT_CARD)
    lint.add_argument("--commands", type=Path, default=DEFAULT_COMMANDS)
    lint.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic freshness fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


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


def summary_metrics(data: dict[str, object]) -> tuple[str, str, str]:
    status = str(data.get("overall_status", "MISSING"))
    checks = data.get("n_checks", data.get("n_artifacts", data.get("n_high_priority_records", "")))
    failures = data.get("n_fail", data.get("n_missing_artifacts", ""))
    return status, str(checks), str(failures)


def add(rows: list[dict[str, object]], component: str, check: str, status: str, detail: str) -> None:
    rows.append({"component": component, "check": check, "status": status, "detail": detail})


def lint_card(
    card_path: Path,
    commands_path: Path,
    summary_path: Path,
    input_summaries: dict[str, Path],
    expected_commands: dict[str, str],
    outdir: Path,
    fail_on_error: bool,
) -> int:
    card_rows = {row.get("component", ""): row for row in read_tsv(card_path)}
    command_rows = {row.get("check", ""): row.get("command", "") for row in read_tsv(commands_path)}
    card_summary = read_json(summary_path)
    rows: list[dict[str, object]] = []
    for component, path in sorted(input_summaries.items()):
        row = card_rows.get(component)
        add(rows, component, "component_present", "PASS" if row else "FAIL", str(card_path))
        if not row:
            continue
        data = read_json(path)
        expected_status, expected_checks, expected_failures = summary_metrics(data)
        add(rows, component, "summary_path_matches", "PASS" if row.get("summary_path") == str(path.relative_to(ROOT)) else "FAIL", f"expected={path.relative_to(ROOT)} observed={row.get('summary_path', '')}")
        add(rows, component, "overall_status_matches", "PASS" if row.get("overall_status") == expected_status else "FAIL", f"expected={expected_status} observed={row.get('overall_status', '')}")
        add(rows, component, "n_checks_matches", "PASS" if row.get("n_checks") == expected_checks else "FAIL", f"expected={expected_checks} observed={row.get('n_checks', '')}")
        add(rows, component, "n_fail_matches", "PASS" if row.get("n_fail") == expected_failures else "FAIL", f"expected={expected_failures} observed={row.get('n_fail', '')}")
    for component in sorted(set(card_rows) - set(input_summaries)):
        add(rows, component, "no_extra_component", "FAIL", "card contains component not in expected input summaries")
    for check, command in sorted(expected_commands.items()):
        observed = command_rows.get(check)
        add(rows, check, "command_present", "PASS" if observed else "FAIL", str(commands_path))
        add(rows, check, "command_matches", "PASS" if observed == command else "FAIL", f"expected={command} observed={observed or ''}")
    for check in sorted(set(command_rows) - set(expected_commands)):
        add(rows, check, "no_extra_command", "FAIL", "card contains command not in expected command list")
    add(
        rows,
        "summary",
        "summary_component_count_matches_rows",
        "PASS" if int(card_summary.get("n_components", -1)) == len(card_rows) else "FAIL",
        f"summary={card_summary.get('n_components', '')} rows={len(card_rows)}",
    )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "preflight_summary_card_freshness_lint.tsv", rows, ["component", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 preflight summary card freshness lint; handoff/navigation only; no biological claim",
        "n_expected_components": len(input_summaries),
        "n_card_components": len(card_rows),
        "n_expected_commands": len(expected_commands),
        "n_card_commands": len(command_rows),
        "n_checks": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
    }
    (outdir / "preflight_summary_card_freshness_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_fail == 0 or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    root = outdir / "synthetic_root"
    summaries = {
        "A": root / "a_summary.json",
        "B": root / "b_summary.json",
    }
    for path, status, checks, failures in [
        (summaries["A"], "PASS", 2, 0),
        (summaries["B"], "PASS", 3, 0),
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"overall_status": status, "n_checks": checks, "n_fail": failures}) + "\n")
    card = root / "card.tsv"
    commands = root / "commands.tsv"
    summary = root / "card_summary.json"
    write_tsv(
        card,
        [
            {"component": "A", "summary_path": str(summaries["A"].relative_to(ROOT)), "summary_exists": "yes", "overall_status": "STALE", "n_checks": "2", "n_fail": "0"},
            {"component": "EXTRA", "summary_path": "extra.json", "summary_exists": "yes", "overall_status": "PASS", "n_checks": "1", "n_fail": "0"},
        ],
        ["component", "summary_path", "summary_exists", "overall_status", "n_checks", "n_fail"],
    )
    write_tsv(commands, [{"check": "run", "command": "wrong command"}, {"check": "extra", "command": "extra command"}], ["check", "command"])
    summary.write_text(json.dumps({"n_components": 99}) + "\n")
    lint_out = outdir / "synthetic_lint"
    lint_card(card, commands, summary, summaries, {"run": "right command"}, lint_out, fail_on_error=False)
    rows = read_tsv(lint_out / "preflight_summary_card_freshness_lint.tsv")
    checks = {
        "missing_component_fails": any(row["component"] == "B" and row["check"] == "component_present" and row["status"] == "FAIL" for row in rows),
        "stale_status_fails": any(row["component"] == "A" and row["check"] == "overall_status_matches" and row["status"] == "FAIL" for row in rows),
        "extra_component_fails": any(row["component"] == "EXTRA" and row["check"] == "no_extra_component" and row["status"] == "FAIL" for row in rows),
        "wrong_command_fails": any(row["component"] == "run" and row["check"] == "command_matches" and row["status"] == "FAIL" for row in rows),
        "extra_command_fails": any(row["component"] == "extra" and row["check"] == "no_extra_command" and row["status"] == "FAIL" for row in rows),
        "bad_summary_count_fails": any(row["component"] == "summary" and row["check"] == "summary_component_count_matches_rows" and row["status"] == "FAIL" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_preflight_summary_card_freshness_checks.tsv", check_rows, ["check", "status"])
    synth_summary = {
        "synthetic": True,
        "purpose": "V48 preflight summary card freshness synthetic fixture; no biological claim",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_preflight_summary_card_freshness_summary.json").write_text(json.dumps(synth_summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(synth_summary, indent=2, sort_keys=True))
    return 0 if synth_summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_card(args.card, args.commands, args.summary, INPUTS, COMMANDS, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
