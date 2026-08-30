#!/usr/bin/env python3
"""Create and combine privacy-preserving V22 validation site records."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
KAPPAS = np.array([0.25, 0.50, 0.75], dtype=float)
THRESHOLD = 20.0
ESTIMAND_ID = "V22_LOCKED_EARLY_DELTA_NEDA4"


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text())


def site_record(export_dir: Path, cohort_token: str, independence_group: str, arrival_index: int, out: Path) -> int:
    attestation_path = export_dir / "EXPORT_ATTESTATION.json"
    attestation = load_json(attestation_path)
    if attestation.get("overall_status") != "PASS":
        raise ValueError("export attestation is not PASS")
    expected = attestation.get("export_file_sha256", {})
    if not isinstance(expected, dict):
        raise ValueError("export attestation hash map is invalid")
    for name, digest in expected.items():
        path = export_dir / str(name)
        if not path.exists() or sha256(path) != digest:
            raise ValueError(f"export hash mismatch: {name}")
    metrics = pd.read_csv(export_dir / "locked_rule_metrics.tsv", sep="\t")
    primary = metrics.loc[metrics["feature"].astype(str).eq("v22_locked_signed_score")]
    if len(primary) != 1:
        raise ValueError("expected exactly one v22_locked_signed_score row")
    row = primary.iloc[0]
    auc = float(row["auc"])
    auc_ci_low = float(row["auc_ci_low"])
    auc_ci_high = float(row["auc_ci_high"])
    hedges_g = float(row["hedges_g"])
    p_value = float(row["permutation_p"])
    if not (0.0 < p_value <= 1.0):
        raise ValueError("primary permutation p-value is outside (0,1]")
    if not (0.5 <= auc <= 1.0):
        raise ValueError("locked-direction AUC is below 0.5; do not convert a reversed effect into positive evidence")
    if not (0.0 <= auc_ci_low <= auc <= auc_ci_high <= 1.0):
        raise ValueError("primary AUC confidence interval is missing or inconsistent")
    if not math.isfinite(hedges_g):
        raise ValueError("primary Hedges g is not finite")
    pinned = attestation.get("pinned_code_sha256", {})
    if not isinstance(pinned, dict) or "scripts/v42_gafson_validation_harness.py" not in pinned:
        raise ValueError("attestation lacks frozen harness hash")
    record = {
        "synthetic": bool(attestation.get("synthetic", False)),
        "purpose": "privacy-preserving same-estimand validation contribution; no standalone biological claim",
        "cohort_token": cohort_token,
        "independence_group": independence_group,
        "arrival_index": arrival_index,
        "estimand_id": ESTIMAND_ID,
        "harness_sha256": str(pinned["scripts/v42_gafson_validation_harness.py"]),
        "export_attestation_sha256": sha256(attestation_path),
        "n": int(row["n"]),
        "n_responders": int(row["n_responders"]),
        "n_nonresponders": int(row["n_nonresponders"]),
        "auc": auc,
        "auc_ci_low": auc_ci_low,
        "auc_ci_high": auc_ci_high,
        "hedges_g": hedges_g,
        "one_sided_permutation_p": p_value,
        "direction": "locked_positive",
        "valid_p_requirement": "frozen one-sided label permutation with plus-one correction",
        "project_grounding_status": "unavailable_without_rerunnable_data",
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0


def mixture_path(p_values: np.ndarray) -> np.ndarray:
    clipped = np.clip(p_values, np.finfo(float).tiny, 1.0)
    log_factors = np.log(KAPPAS)[None, :] + (KAPPAS[None, :] - 1.0) * np.log(clipped)[:, None]
    log_products = np.cumsum(log_factors, axis=0)
    maximum = np.max(log_products, axis=1, keepdims=True)
    return np.exp(maximum[:, 0]) * np.mean(np.exp(log_products - maximum), axis=1)


def combine(record_paths: list[Path], outdir: Path, expect_status: str | None) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    records = [load_json(path) for path in record_paths]
    problems: list[str] = []
    required = {
        "cohort_token",
        "independence_group",
        "arrival_index",
        "estimand_id",
        "harness_sha256",
        "n",
        "auc",
        "auc_ci_low",
        "auc_ci_high",
        "hedges_g",
        "one_sided_permutation_p",
        "direction",
    }
    for index, record in enumerate(records):
        missing = sorted(required - set(record))
        if missing:
            problems.append(f"record_{index}_missing:{','.join(missing)}")
    if not problems:
        cohort_tokens = [str(record["cohort_token"]) for record in records]
        groups = [str(record["independence_group"]) for record in records]
        estimands = {str(record["estimand_id"]) for record in records}
        hashes = {str(record["harness_sha256"]) for record in records}
        arrivals = [int(record["arrival_index"]) for record in records]
        if len(cohort_tokens) != len(set(cohort_tokens)):
            problems.append("duplicate_cohort_token")
        if len(groups) != len(set(groups)):
            problems.append("duplicate_independence_group")
        if estimands != {ESTIMAND_ID}:
            problems.append("estimand_mismatch")
        if len(hashes) != 1:
            problems.append("harness_hash_mismatch")
        if sorted(arrivals) != list(range(1, len(records) + 1)):
            problems.append("arrival_indices_not_consecutive_from_one")
        for index, record in enumerate(records):
            p_value = float(record["one_sided_permutation_p"])
            auc = float(record["auc"])
            auc_ci_low = float(record["auc_ci_low"])
            auc_ci_high = float(record["auc_ci_high"])
            hedges_g = float(record["hedges_g"])
            if not (0.0 < p_value <= 1.0):
                problems.append(f"record_{index}_invalid_p")
            if str(record["direction"]) != "locked_positive" or auc < 0.5:
                problems.append(f"record_{index}_wrong_direction")
            if not (0.0 <= auc_ci_low <= auc <= auc_ci_high <= 1.0):
                problems.append(f"record_{index}_invalid_auc_ci")
            if not math.isfinite(hedges_g):
                problems.append(f"record_{index}_invalid_hedges_g")

    rows: list[dict[str, object]] = []
    if not problems:
        ordered = sorted(records, key=lambda record: int(record["arrival_index"]))
        p_values = np.asarray([float(record["one_sided_permutation_p"]) for record in ordered])
        e_values = mixture_path(p_values)
        for record, e_value in zip(ordered, e_values):
            rows.append(
                {
                    "arrival_index": int(record["arrival_index"]),
                    "cohort_token": record["cohort_token"],
                    "independence_group": record["independence_group"],
                    "n": int(record["n"]),
                    "auc": float(record["auc"]),
                    "auc_ci_low": float(record["auc_ci_low"]),
                    "auc_ci_high": float(record["auc_ci_high"]),
                    "hedges_g": float(record["hedges_g"]),
                    "one_sided_permutation_p": float(record["one_sided_permutation_p"]),
                    "mixture_e_value": float(e_value),
                    "crossed_20": bool(e_value >= THRESHOLD),
                }
            )
    pd.DataFrame(rows).to_csv(outdir / "federated_evidence_path.tsv", sep="\t", index=False)
    status = "PASS" if not problems else "FAIL"
    summary = {
        "synthetic": bool(records) and all(bool(record.get("synthetic", False)) for record in records),
        "purpose": "same-estimand federated evidence accumulation; no standalone biological claim",
        "n_records": len(records),
        "n_problems": len(set(problems)),
        "problems": sorted(set(problems)),
        "final_mixture_e_value": rows[-1]["mixture_e_value"] if rows else None,
        "crossed_20": bool(rows and any(bool(row["crossed_20"]) for row in rows)),
        "overall_status": status,
        "interpretation_boundary": "combine only independent cohorts testing the identical frozen estimand; retain site effect sizes and V42 result classes",
    }
    (outdir / "federated_evidence_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    if expect_status is not None:
        return 0 if status == expect_status else 2
    return 0 if status == "PASS" else 1


def synthetic_check(outdir: Path) -> int:
    if outdir.exists():
        import shutil

        shutil.rmtree(outdir)
    records_dir = outdir / "synthetic_records"
    records_dir.mkdir(parents=True)
    base = {
        "synthetic": True,
        "purpose": "synthetic federated evidence schema fixture; no biological claim",
        "estimand_id": ESTIMAND_ID,
        "harness_sha256": "a" * 64,
        "n": 20,
        "n_responders": 10,
        "n_nonresponders": 10,
        "auc": 0.70,
        "auc_ci_low": 0.55,
        "auc_ci_high": 0.85,
        "hedges_g": 0.60,
        "direction": "locked_positive",
    }
    valid_paths = []
    for index, p_value in enumerate([0.02, 0.08, 0.40], start=1):
        record = {
            **base,
            "cohort_token": f"SYN_SITE_{index}",
            "independence_group": f"SYN_INDEPENDENT_{index}",
            "arrival_index": index,
            "one_sided_permutation_p": p_value,
        }
        path = records_dir / f"site_{index}.json"
        path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        valid_paths.append(path)
    valid_rc = combine(valid_paths, outdir / "valid_combination", "PASS")

    duplicate = load_json(valid_paths[1])
    duplicate["independence_group"] = "SYN_INDEPENDENT_1"
    duplicate_path = records_dir / "site_2_duplicate_group.json"
    duplicate_path.write_text(json.dumps(duplicate, indent=2, sort_keys=True) + "\n")
    duplicate_rc = combine([valid_paths[0], duplicate_path], outdir / "duplicate_group_rejected", "FAIL")

    mismatch = load_json(valid_paths[1])
    mismatch["harness_sha256"] = "b" * 64
    mismatch_path = records_dir / "site_2_hash_mismatch.json"
    mismatch_path.write_text(json.dumps(mismatch, indent=2, sort_keys=True) + "\n")
    mismatch_rc = combine([valid_paths[0], mismatch_path], outdir / "hash_mismatch_rejected", "FAIL")

    missing_uncertainty = load_json(valid_paths[1])
    del missing_uncertainty["auc_ci_low"]
    missing_uncertainty_path = records_dir / "site_2_missing_uncertainty.json"
    missing_uncertainty_path.write_text(json.dumps(missing_uncertainty, indent=2, sort_keys=True) + "\n")
    missing_uncertainty_rc = combine(
        [valid_paths[0], missing_uncertainty_path],
        outdir / "missing_uncertainty_rejected",
        "FAIL",
    )

    summary = {
        "synthetic": True,
        "purpose": "federated evidence operational regression; no biological claim",
        "valid_combination_passed": valid_rc == 0,
        "duplicate_independence_group_rejected": duplicate_rc == 0,
        "harness_hash_mismatch_rejected": mismatch_rc == 0,
        "missing_uncertainty_rejected": missing_uncertainty_rc == 0,
        "overall_status": "PASS"
        if valid_rc == duplicate_rc == mismatch_rc == missing_uncertainty_rc == 0
        else "FAIL",
    }
    (outdir / "synthetic_check_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    site = sub.add_parser("site-record")
    site.add_argument("--export-dir", type=Path, required=True)
    site.add_argument("--cohort-token", required=True)
    site.add_argument("--independence-group", required=True)
    site.add_argument("--arrival-index", type=int, required=True)
    site.add_argument("--out", type=Path, required=True)
    comb = sub.add_parser("combine")
    comb.add_argument("--record", type=Path, action="append", required=True)
    comb.add_argument("--outdir", type=Path, required=True)
    comb.add_argument("--expect-status", choices=["PASS", "FAIL"])
    syn = sub.add_parser("synthetic-check")
    syn.add_argument("--outdir", type=Path, default=ROOT / "analysis/v57_federated_evidence")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "site-record":
        return site_record(resolve(args.export_dir), args.cohort_token, args.independence_group, args.arrival_index, resolve(args.out))
    if args.command == "combine":
        return combine([resolve(path) for path in args.record], resolve(args.outdir), args.expect_status)
    return synthetic_check(resolve(args.outdir))


if __name__ == "__main__":
    raise SystemExit(main())
