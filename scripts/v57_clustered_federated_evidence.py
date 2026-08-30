#!/usr/bin/env python3
"""Combine declared dependent site records as independent cluster e-values."""

from __future__ import annotations

import argparse
import json
import math
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

from v57_federated_evidence_accumulator import ESTIMAND_ID, KAPPAS, ROOT, THRESHOLD


DEFAULT_OUT = ROOT / "analysis/v57_clustered_federated_evidence"
REQUIRED_OVERLAP_DIMENSIONS = {
    "participant",
    "center",
    "biobank",
    "source_study",
    "preprocessing_lineage",
}
MIN_CLUSTERS = 4
MAX_CLUSTER_SIZE = 4


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text())


def combine(
    record_paths: list[Path],
    manifest_path: Path,
    outdir: Path,
    expect_status: str | None = None,
) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    records = [load(path) for path in record_paths]
    manifest = load(manifest_path)
    problems: list[str] = []
    required_record = {
        "cohort_token",
        "independence_group",
        "estimand_id",
        "harness_sha256",
        "auc",
        "auc_ci_low",
        "auc_ci_high",
        "hedges_g",
        "one_sided_permutation_p",
        "direction",
    }
    for index, record in enumerate(records):
        missing = required_record - set(record)
        if missing:
            problems.append(f"record_{index}_missing:{','.join(sorted(missing))}")

    clusters = manifest.get("clusters", [])
    if not isinstance(clusters, list):
        clusters = []
        problems.append("manifest_clusters_not_list")
    if manifest.get("cluster_membership_frozen_before_results") is not True:
        problems.append("cluster_membership_not_frozen")
    if manifest.get("cross_cluster_independence_attested") is not True:
        problems.append("cross_cluster_independence_not_attested")
    reviewed = set(manifest.get("overlap_dimensions_reviewed", []))
    if reviewed != REQUIRED_OVERLAP_DIMENSIONS:
        problems.append("overlap_dimensions_incomplete")
    if len(clusters) < MIN_CLUSTERS:
        problems.append("fewer_than_four_independent_clusters")

    cohort_tokens = [str(record.get("cohort_token", "")) for record in records]
    if len(cohort_tokens) != len(set(cohort_tokens)):
        problems.append("duplicate_cohort_token")
    by_token = {str(record.get("cohort_token", "")): record for record in records}
    cluster_ids: list[str] = []
    cluster_arrivals: list[int] = []
    assigned: list[str] = []
    group_to_clusters: dict[str, set[str]] = {}
    for index, cluster in enumerate(clusters):
        if not isinstance(cluster, dict):
            problems.append(f"cluster_{index}_not_object")
            continue
        cluster_id = str(cluster.get("cluster_id", ""))
        members = [str(value) for value in cluster.get("cohort_tokens", [])]
        try:
            arrival = int(cluster.get("cluster_arrival_index"))
        except (TypeError, ValueError):
            arrival = -1
        cluster_ids.append(cluster_id)
        cluster_arrivals.append(arrival)
        assigned.extend(members)
        if not (2 <= len(members) <= MAX_CLUSTER_SIZE):
            problems.append(f"cluster_{cluster_id}_size_outside_2_to_4")
        if len(members) != len(set(members)):
            problems.append(f"cluster_{cluster_id}_duplicate_member")
        for token in members:
            record = by_token.get(token)
            if record is not None:
                group = str(record.get("independence_group", ""))
                group_to_clusters.setdefault(group, set()).add(cluster_id)
    if len(cluster_ids) != len(set(cluster_ids)) or "" in cluster_ids:
        problems.append("cluster_ids_not_unique_nonempty")
    if sorted(cluster_arrivals) != list(range(1, len(clusters) + 1)):
        problems.append("cluster_arrivals_not_consecutive_from_one")
    if sorted(assigned) != sorted(cohort_tokens) or len(assigned) != len(set(assigned)):
        problems.append("site_assignment_not_exactly_once")
    if any(len(cluster_set) > 1 for cluster_set in group_to_clusters.values()):
        problems.append("independence_group_split_across_clusters")

    if records:
        estimands = {str(record.get("estimand_id", "")) for record in records}
        hashes = {str(record.get("harness_sha256", "")) for record in records}
        if estimands != {ESTIMAND_ID}:
            problems.append("estimand_mismatch")
        if len(hashes) != 1:
            problems.append("harness_hash_mismatch")
        for index, record in enumerate(records):
            try:
                p_value = float(record.get("one_sided_permutation_p"))
                auc = float(record.get("auc"))
                auc_ci_low = float(record.get("auc_ci_low"))
                auc_ci_high = float(record.get("auc_ci_high"))
                hedges_g = float(record.get("hedges_g"))
            except (TypeError, ValueError):
                problems.append(f"record_{index}_invalid_numeric")
                continue
            if not (0.0 < p_value <= 1.0):
                problems.append(f"record_{index}_invalid_p")
            if str(record.get("direction")) != "locked_positive" or auc < 0.5:
                problems.append(f"record_{index}_wrong_direction")
            if not (0.0 <= auc_ci_low <= auc <= auc_ci_high <= 1.0):
                problems.append(f"record_{index}_invalid_auc_ci")
            if not math.isfinite(hedges_g):
                problems.append(f"record_{index}_invalid_hedges_g")

    rows: list[dict[str, object]] = []
    if not problems:
        products = np.ones(len(KAPPAS), dtype=float)
        for cluster in sorted(clusters, key=lambda value: int(value["cluster_arrival_index"])):
            members = [by_token[str(token)] for token in cluster["cohort_tokens"]]
            p_values = np.asarray([float(record["one_sided_permutation_p"]) for record in members])
            factors = KAPPAS[None, :] * p_values[:, None] ** (KAPPAS[None, :] - 1.0)
            cluster_factors = np.mean(factors, axis=0)
            products *= cluster_factors
            mixture = float(np.mean(products))
            rows.append(
                {
                    "cluster_arrival_index": int(cluster["cluster_arrival_index"]),
                    "cluster_id": str(cluster["cluster_id"]),
                    "n_sites": len(members),
                    "cohort_tokens": ";".join(str(record["cohort_token"]) for record in members),
                    "minimum_site_p": float(p_values.min()),
                    "maximum_site_p": float(p_values.max()),
                    "mixture_e_value": mixture,
                    "crossed_20": mixture >= THRESHOLD,
                }
            )
    status = "PASS" if not problems else "FAIL"
    pd.DataFrame(rows).to_csv(outdir / "clustered_evidence_path.tsv", sep="\t", index=False)
    summary = {
        "synthetic": bool(records) and all(bool(record.get("synthetic", False)) for record in records),
        "purpose": "clustered same-estimand federated evidence operation; no standalone biological claim",
        "n_records": len(records),
        "n_clusters": len(clusters),
        "minimum_planning_clusters": MIN_CLUSTERS,
        "n_problems": len(set(problems)),
        "problems": sorted(set(problems)),
        "final_mixture_e_value": rows[-1]["mixture_e_value"] if rows else None,
        "crossed_20": bool(rows and any(bool(row["crossed_20"]) for row in rows)),
        "overall_status": status,
        "interpretation_boundary": "Within-cluster averaging requires valid site e-factors; products require truthful cross-cluster independence.",
    }
    (outdir / "clustered_evidence_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    if expect_status is not None:
        return 0 if status == expect_status else 2
    return 0 if status == "PASS" else 1


def synthetic_record(token: str, group: str, p_value: float) -> dict[str, object]:
    return {
        "synthetic": True,
        "purpose": "synthetic clustered evidence fixture; no biological claim",
        "cohort_token": token,
        "independence_group": group,
        "arrival_index": 1,
        "estimand_id": ESTIMAND_ID,
        "harness_sha256": "a" * 64,
        "n": 20,
        "auc": 0.70,
        "auc_ci_low": 0.55,
        "auc_ci_high": 0.85,
        "hedges_g": 0.60,
        "one_sided_permutation_p": p_value,
        "direction": "locked_positive",
    }


def synthetic_check(outdir: Path) -> int:
    if outdir.exists():
        shutil.rmtree(outdir)
    fixtures = outdir / "synthetic_fixtures"
    fixtures.mkdir(parents=True)
    records: list[Path] = []
    clusters: list[dict[str, object]] = []
    for cluster_index in range(1, 5):
        tokens = []
        for member in range(1, 3):
            token = f"SITE_{cluster_index}_{member}"
            tokens.append(token)
            path = fixtures / f"{token}.json"
            path.write_text(
                json.dumps(synthetic_record(token, f"SOURCE_{cluster_index}", 0.02 * member), indent=2, sort_keys=True) + "\n"
            )
            records.append(path)
        clusters.append(
            {
                "cluster_id": f"CLUSTER_{cluster_index}",
                "cluster_arrival_index": cluster_index,
                "cohort_tokens": tokens,
            }
        )
    base_manifest = {
        "synthetic": True,
        "purpose": "synthetic cluster manifest fixture; no biological claim",
        "cluster_membership_frozen_before_results": True,
        "cross_cluster_independence_attested": True,
        "overlap_dimensions_reviewed": sorted(REQUIRED_OVERLAP_DIMENSIONS),
        "clusters": clusters,
    }

    cases: list[tuple[str, dict[str, object], list[Path], str]] = [
        ("valid_four_clusters", base_manifest, records, "PASS"),
        ("too_few_clusters", {**base_manifest, "clusters": clusters[:3]}, records[:6], "FAIL"),
        ("incomplete_overlap_review", {**base_manifest, "overlap_dimensions_reviewed": ["participant"]}, records, "FAIL"),
        ("independence_not_attested", {**base_manifest, "cross_cluster_independence_attested": False}, records, "FAIL"),
        ("missing_site_assignment", {**base_manifest, "clusters": [{**clusters[0], "cohort_tokens": clusters[0]["cohort_tokens"][:1]}, *clusters[1:]]}, records, "FAIL"),
    ]

    oversized_tokens = ["SITE_1_3", "SITE_1_4", "SITE_1_5"]
    oversized_paths: list[Path] = []
    for offset, oversized_token in enumerate(oversized_tokens, start=3):
        oversized_path = fixtures / f"{oversized_token}.json"
        oversized_path.write_text(
            json.dumps(synthetic_record(oversized_token, "SOURCE_1", 0.01 * offset), indent=2, sort_keys=True) + "\n"
        )
        oversized_paths.append(oversized_path)
    extra_paths = [*records, *oversized_paths]
    oversized_clusters = [{**clusters[0], "cohort_tokens": [*clusters[0]["cohort_tokens"], *oversized_tokens]}, *clusters[1:]]
    cases.append(("oversized_cluster", {**base_manifest, "clusters": oversized_clusters}, extra_paths, "FAIL"))

    split_records = [load(path) for path in records]
    split_records[2]["independence_group"] = "SOURCE_1"
    split_paths: list[Path] = []
    for index, record in enumerate(split_records):
        path = fixtures / f"split_{index}.json"
        path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        split_paths.append(path)
    cases.append(("group_split_across_clusters", base_manifest, split_paths, "FAIL"))

    checks: list[dict[str, object]] = []
    for case_id, manifest, case_records, expected in cases:
        manifest_path = fixtures / f"{case_id}_manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        rc = combine(case_records, manifest_path, outdir / case_id, expected)
        checks.append(
            {
                "case_id": case_id,
                "expected_status": expected,
                "expectation_met": rc == 0,
            }
        )
    pd.DataFrame(checks).to_csv(outdir / "synthetic_clustered_evidence_checks.tsv", sep="\t", index=False)
    passed = all(bool(row["expectation_met"]) for row in checks)
    summary = {
        "synthetic": True,
        "purpose": "clustered federated evidence operational regression; no biological claim",
        "n_cases": len(checks),
        "n_pass": sum(bool(row["expectation_met"]) for row in checks),
        "overall_status": "PASS" if passed else "FAIL",
    }
    (outdir / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if passed else 2


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    combine_parser = sub.add_parser("combine")
    combine_parser.add_argument("--record", action="append", type=Path, required=True)
    combine_parser.add_argument("--manifest", type=Path, required=True)
    combine_parser.add_argument("--outdir", type=Path, required=True)
    combine_parser.add_argument("--expect-status", choices=("PASS", "FAIL"))
    synthetic = sub.add_parser("synthetic-check")
    synthetic.add_argument("--outdir", type=Path, default=DEFAULT_OUT)
    return root


def main() -> int:
    args = parser().parse_args()
    if args.command == "combine":
        return combine(
            [resolve(path) for path in args.record],
            resolve(args.manifest),
            resolve(args.outdir),
            args.expect_status,
        )
    return synthetic_check(resolve(args.outdir))


if __name__ == "__main__":
    raise SystemExit(main())
