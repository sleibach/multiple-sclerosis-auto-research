#!/usr/bin/env python3
"""Gate blinded ToleDYNAMIC functional-endpoint mapping before values."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v56_toledynamic_functional_mapping_gate"
REQUIRED_COLUMNS = {
    "family",
    "endpoint_role",
    "source_variable",
    "source_document",
    "source_locator",
    "units",
    "expected_direction",
    "available",
    "mapping_basis",
    "values_read_before_mapping",
}
EXPECTED_ROLES = {
    "myelin_phagocytosis": {"primary"},
    "cd64": {"primary"},
    "ros": {"primary"},
    "metabolic": {"basal_respiration", "spare_respiration"},
    "inflammatory_cytokine_summary": {"primary"},
}
DIRECTIONS = {"increase", "decrease", "two_sided"}
MAPPING_BASES = {"sap_designated", "protocol_unique"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("mapping", type=Path)
    run.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    run.add_argument("--fail-on-block", action="store_true")
    check = sub.add_parser("synthetic-check")
    check.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    check.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def truth(value: str) -> bool:
    folded = value.strip().casefold()
    if folded not in {"true", "false"}:
        raise ValueError(f"expected true/false, observed {value!r}")
    return folded == "true"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        missing = sorted(REQUIRED_COLUMNS - set(reader.fieldnames or []))
        if missing:
            raise ValueError(f"mapping missing columns: {', '.join(missing)}")
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if not rows:
        raise ValueError("mapping contains no rows")
    return rows


def analyze(rows: list[dict[str, str]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    blockers: list[str] = []
    seen: set[tuple[str, str]] = set()
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    any_values_read = False

    for index, row in enumerate(rows, start=2):
        family = row["family"]
        role = row["endpoint_role"]
        if family not in EXPECTED_ROLES:
            blockers.append(f"row_{index}_unknown_family")
            continue
        key = (family, role)
        if key in seen:
            blockers.append(f"duplicate_family_role:{family}:{role}")
        seen.add(key)
        grouped[family].append(row)
        try:
            any_values_read |= truth(row["values_read_before_mapping"])
            truth(row["available"])
        except ValueError as exc:
            blockers.append(f"row_{index}_{exc}")

    if any_values_read:
        blockers.append("mapping_not_blinded_values_were_read")

    family_rows: list[dict[str, Any]] = []
    n_test_eligible = 0
    for family, expected_roles in EXPECTED_ROLES.items():
        mapped = grouped.get(family, [])
        roles = {row["endpoint_role"] for row in mapped}
        reasons: list[str] = []
        available_rows = []
        for row in mapped:
            try:
                if truth(row["available"]):
                    available_rows.append(row)
            except ValueError:
                continue
        if not mapped or not available_rows:
            status = "DESCRIPTIVE_UNAVAILABLE"
            reasons.append("family_or_endpoint_unavailable")
        else:
            if roles != expected_roles:
                reasons.append("endpoint_roles_do_not_exactly_match_frozen_family")
            for row in available_rows:
                if not all(row[field] for field in ("source_variable", "source_document", "source_locator", "units")):
                    reasons.append("source_mapping_incomplete")
                if row["expected_direction"] not in DIRECTIONS:
                    reasons.append("expected_direction_not_frozen")
                if row["mapping_basis"] not in MAPPING_BASES:
                    reasons.append("mapping_basis_not_allowed")
                if family == "inflammatory_cytokine_summary" and row["mapping_basis"] != "sap_designated":
                    reasons.append("cytokine_summary_not_sap_designated")
            if any_values_read:
                reasons.append("mapping_not_blinded")
            reasons = sorted(set(reasons))
            status = "TEST_ELIGIBLE" if not reasons else "DESCRIPTIVE_ONLY"
        n_test_eligible += int(status == "TEST_ELIGIBLE")
        family_rows.append(
            {
                "family": family,
                "expected_roles": ";".join(sorted(expected_roles)),
                "mapped_roles": ";".join(sorted(roles)) or "none",
                "n_mapping_rows": len(mapped),
                "status": status,
                "reasons": ";".join(reasons) or "none",
            }
        )

    blockers = sorted(set(blockers))
    summary = {
        "purpose": "blinded functional-endpoint mapping gate; no assay or outcome values read",
        "n_families": len(EXPECTED_ROLES),
        "n_test_eligible": n_test_eligible,
        "n_blockers": len(blockers),
        "blockers": blockers,
        "overall_status": "BLOCKED" if blockers else "MAPPING_COMPLETE",
        "values_read_before_mapping": any_values_read,
        "treatment_effect_established": False,
        "mechanism_established": False,
        "boundary": "TEST_ELIGIBLE fixes an endpoint for later testing; it is not evidence that the endpoint changes.",
    }
    return summary, family_rows


def write_outputs(outdir: Path, summary: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    with (outdir / "family_status.tsv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def complete_rows() -> list[dict[str, str]]:
    rows = []
    for family, roles in EXPECTED_ROLES.items():
        for role in sorted(roles):
            rows.append(
                {
                    "family": family,
                    "endpoint_role": role,
                    "source_variable": f"SYNTHETIC_{family}_{role}",
                    "source_document": "SYNTHETIC_SAP",
                    "source_locator": f"SYNTHETIC_SECTION_{family}_{role}",
                    "units": "SYNTHETIC_UNIT",
                    "expected_direction": "two_sided",
                    "available": "true",
                    "mapping_basis": "sap_designated",
                    "values_read_before_mapping": "false",
                }
            )
    return rows


def write_mapping(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=sorted(REQUIRED_COLUMNS))
        writer.writeheader()
        writer.writerows(rows)


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    fixtures: dict[str, tuple[list[dict[str, str]], str, int]] = {}
    fixtures["complete"] = (complete_rows(), "MAPPING_COMPLETE", 5)
    unavailable = complete_rows()
    for row in unavailable:
        if row["family"] == "inflammatory_cytokine_summary":
            row["available"] = "false"
    fixtures["cytokine_unavailable"] = (unavailable, "MAPPING_COMPLETE", 4)
    unblinded = complete_rows()
    unblinded[0]["values_read_before_mapping"] = "true"
    fixtures["values_read"] = (unblinded, "BLOCKED", 0)
    duplicate = complete_rows()
    duplicate.append(dict(duplicate[0]))
    fixtures["duplicate"] = (duplicate, "BLOCKED", 0)

    results = []
    fixture_dir = outdir / "synthetic"
    for name, (rows, expected_status, expected_eligible) in fixtures.items():
        path = fixture_dir / f"{name}.tsv"
        write_mapping(path, rows)
        summary, _ = analyze(load_rows(path))
        observed_eligible = summary["n_test_eligible"] if summary["overall_status"] != "BLOCKED" else 0
        passed = summary["overall_status"] == expected_status and observed_eligible == expected_eligible
        results.append(
            {
                "fixture": name,
                "expected_status": expected_status,
                "observed_status": summary["overall_status"],
                "expected_effective_test_eligible": expected_eligible,
                "observed_effective_test_eligible": observed_eligible,
                "status": "PASS" if passed else "FAIL",
            }
        )
    n_fail = sum(row["status"] == "FAIL" for row in results)
    summary = {
        "purpose": "deterministic synthetic functional-mapping behavior check; no biological evidence",
        "synthetic": True,
        "n_fixtures": len(results),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "fixtures": results,
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if fail_on_error and n_fail else 0


def main() -> int:
    args = parse_args()
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    try:
        summary, family_rows = analyze(load_rows(args.mapping))
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    write_outputs(args.outdir, summary, family_rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if args.fail_on_block and summary["overall_status"] == "BLOCKED" else 0


if __name__ == "__main__":
    sys.exit(main())
