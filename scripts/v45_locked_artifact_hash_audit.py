#!/usr/bin/env python3
"""Hash-audit locked rules and frozen preregistration artifacts."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASELINE = ROOT / "docs/validation/LOCKED_ARTIFACT_HASH_BASELINE_V45.tsv"


DEFAULT_ARTIFACTS = [
    (
        "docs/locked_rules/LOCKED_RULE_V22.md",
        "locked_rule",
        "Immutable V22 scalar treatment-response rule.",
    ),
    (
        "docs/validation/PREREGISTRATION_V42.md",
        "primary_preregistration",
        "Frozen Gafson/DMF/NEDA-4 validation plan.",
    ),
    (
        "docs/validation/OUTCOME_INTERPRETATION_GRID_V42.md",
        "primary_interpretation_grid",
        "Pre-committed Gafson outcome interpretation grid.",
    ),
    (
        "docs/validation/BATCH_GUARD_V44.md",
        "primary_batch_guard",
        "Blind additive V44 batch-diagnostic guard.",
    ),
    (
        "docs/validation/POSTPARTUM_APC_ARM_PREREGISTRATION_V44.md",
        "secondary_preregistration",
        "Frozen postpartum APC-arm secondary lead plan.",
    ),
    (
        "docs/validation/TB_COMPARTMENT_PREREGISTRATION_V44.md",
        "secondary_preregistration",
        "Frozen T/B compartment secondary lead plan.",
    ),
    (
        "docs/validation/PHARMACODYNAMIC_ONLY_PREREGISTRATION_V45.md",
        "context_preregistration",
        "Frozen pharmacodynamic-only context plan.",
    ),
    (
        "docs/validation/KAROLINSKA_PREREGISTRATION_TEMPLATE_V45.md",
        "future_addendum_template",
        "Blind template for future Karolinska addendum if labels arrive.",
    ),
    (
        "docs/validation/GSE228330_OUTCOME_LABEL_ADDENDUM_TEMPLATE_V45.md",
        "future_addendum_template",
        "Blind template for future GSE228330 outcome-label addendum.",
    ),
]


FIELDNAMES = ["path", "category", "sha256", "bytes", "role"]


def repo_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def artifact_row(path_text: str, category: str, role: str) -> dict[str, str]:
    path = ROOT / path_text
    if not path.exists():
        raise FileNotFoundError(path)
    return {
        "path": path_text,
        "category": category,
        "sha256": sha256(path),
        "bytes": str(path.stat().st_size),
        "role": role,
    }


def write_tsv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_baseline(out: Path) -> dict[str, object]:
    out = repo_path(out)
    rows = [artifact_row(*artifact) for artifact in DEFAULT_ARTIFACTS]
    write_tsv(out, rows, FIELDNAMES)
    return {
        "baseline": str(out),
        "n_artifacts": len(rows),
        "overall_status": "BASELINE_WRITTEN",
    }


def audit(baseline: Path, outdir: Path) -> dict[str, object]:
    baseline = repo_path(baseline)
    outdir = repo_path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    baseline_rows = read_tsv(baseline)
    rows = []
    for expected in baseline_rows:
        path = ROOT / expected["path"]
        exists = path.exists()
        observed_sha = sha256(path) if exists else ""
        observed_bytes = str(path.stat().st_size) if exists else ""
        if not exists:
            status = "MISSING"
        elif observed_sha != expected["sha256"] or observed_bytes != expected["bytes"]:
            status = "DRIFT"
        else:
            status = "MATCH"
        rows.append(
            {
                **expected,
                "observed_sha256": observed_sha,
                "observed_bytes": observed_bytes,
                "status": status,
            }
        )
    write_tsv(
        outdir / "locked_artifact_hash_audit.tsv",
        rows,
        FIELDNAMES + ["observed_sha256", "observed_bytes", "status"],
    )
    status_counts = {status: sum(row["status"] == status for row in rows) for status in ["MATCH", "DRIFT", "MISSING"]}
    overall = "PASS" if status_counts["DRIFT"] == 0 and status_counts["MISSING"] == 0 else "FAIL"
    summary = {
        "baseline": str(baseline),
        "n_artifacts": len(rows),
        "status_counts": status_counts,
        "overall_status": overall,
    }
    (outdir / "locked_artifact_hash_audit_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    return summary


def synthetic_check(outdir: Path) -> dict[str, object]:
    outdir = repo_path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    synth_root = outdir / "synthetic"
    synth_root.mkdir(exist_ok=True)
    target = synth_root / "locked.txt"
    target.write_text("frozen\n")
    rel_target = target.relative_to(ROOT)
    rows = [
        {
            "path": str(rel_target),
            "category": "synthetic_locked_file",
            "sha256": sha256(target),
            "bytes": str(target.stat().st_size),
            "role": "Synthetic hash-audit pass/fail fixture.",
        }
    ]
    baseline = synth_root / "baseline.tsv"
    write_tsv(baseline, rows, FIELDNAMES)
    pass_summary = audit(baseline, outdir / "synthetic_pass")
    target.write_text("changed\n")
    fail_summary = audit(baseline, outdir / "synthetic_fail")
    assertions = {
        "synthetic": True,
        "pass_audit_passed": pass_summary["overall_status"] == "PASS",
        "changed_file_failed": fail_summary["overall_status"] == "FAIL",
        "overall_status": "PASS"
        if pass_summary["overall_status"] == "PASS" and fail_summary["overall_status"] == "FAIL"
        else "FAIL",
    }
    (outdir / "synthetic_check_assertions.json").write_text(json.dumps(assertions, indent=2, sort_keys=True) + "\n")
    return assertions


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    write = sub.add_parser("write-baseline", help="Write the current locked-artifact hash baseline.")
    write.add_argument("--out", type=Path, default=DEFAULT_BASELINE)
    check = sub.add_parser("audit", help="Compare locked artifacts to a committed baseline.")
    check.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    check.add_argument("--outdir", type=Path, required=True)
    check.add_argument("--fail-on-drift", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Verify pass/fail mechanics on synthetic files.")
    synth.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "write-baseline":
        summary = write_baseline(args.out)
    elif args.command == "audit":
        summary = audit(args.baseline, args.outdir)
    else:
        summary = synthetic_check(args.outdir)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if getattr(args, "fail_on_drift", False) and summary["overall_status"] != "PASS":
        return 2
    return 0 if summary["overall_status"] in {"PASS", "BASELINE_WRITTEN"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
