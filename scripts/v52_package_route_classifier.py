#!/usr/bin/env python3
"""Classify synthetic incoming package manifests against the V52 route table.

This is an intake smoke tool, not a validation harness. It checks whether a
manifest's declared available fields satisfy the minimum_fields column in
docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLASSIFIER = ROOT / "docs/validation/VALIDATION_PACKAGE_ROUTE_CLASSIFIER_V52.tsv"
REQUIRED_MANIFEST_COLUMNS = {"package_id", "provided_fields"}


def split_fields(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def read_manifest_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fieldnames = set(reader.fieldnames or [])
        missing = sorted(REQUIRED_MANIFEST_COLUMNS - fieldnames)
        if missing:
            raise SystemExit({"manifest_missing_required_columns": str(path), "missing": missing})
        rows = list(reader)
    package_ids = [row.get("package_id", "") for row in rows]
    duplicates = sorted({package_id for package_id in package_ids if package_ids.count(package_id) > 1})
    if duplicates:
        raise SystemExit({"manifest_duplicate_package_id": str(path), "duplicates": duplicates})
    return rows


def classify_manifest(manifest: dict[str, str], routes: list[dict[str, str]]) -> dict[str, str]:
    provided = set(split_fields(manifest.get("provided_fields", "")))
    scored: list[tuple[int, int, dict[str, str], list[str], list[str]]] = []

    for route in routes:
        required = split_fields(route["minimum_fields"])
        missing = [field for field in required if field not in provided]
        present = [field for field in required if field in provided]
        scored.append((len(present), len(required), route, present, missing))

    full = [item for item in scored if item[0] == item[1]]
    if full:
        # Classifier TSV order is the pre-specified precedence.
        chosen = full[0]
        candidate_routes = [item[2]["route_class"] for item in full]
        status = "matched"
    else:
        chosen = max(scored, key=lambda item: (item[0], -item[1]))
        candidate_routes = []
        status = "partial_or_unscoreable" if chosen[0] else "unscoreable_no_route"

    matched, required_n, route, present, missing = chosen
    return {
        "package_id": manifest["package_id"],
        "expected_route": manifest.get("expected_route", ""),
        "assigned_route": route["route_class"] if status != "unscoreable_no_route" else "",
        "status": status,
        "matched_required_count": str(matched),
        "required_count": str(required_n),
        "missing_required_fields": ";".join(missing),
        "candidate_full_routes": ";".join(candidate_routes),
        "expected_matches_assigned": str(
            bool(manifest.get("expected_route", "") == (route["route_class"] if status != "unscoreable_no_route" else ""))
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifests", required=True, type=Path)
    parser.add_argument("--classifier", type=Path, default=DEFAULT_CLASSIFIER)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    routes = read_tsv(args.classifier)
    manifests = read_manifest_tsv(args.manifests)
    results = [classify_manifest(manifest, routes) for manifest in manifests]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "package_id",
        "expected_route",
        "assigned_route",
        "status",
        "matched_required_count",
        "required_count",
        "missing_required_fields",
        "candidate_full_routes",
        "expected_matches_assigned",
    ]
    with args.out.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)

    failures = [
        row
        for row in results
        if row["expected_route"] and row["expected_matches_assigned"] != "True"
    ]
    print({"manifests": len(manifests), "output": str(args.out), "expectation_failures": len(failures)})
    if failures:
        raise SystemExit({"expectation_failures": failures})


if __name__ == "__main__":
    main()
