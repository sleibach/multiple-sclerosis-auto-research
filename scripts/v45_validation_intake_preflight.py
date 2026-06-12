#!/usr/bin/env python3
"""Preflight validation intake packages before running any frozen harness.

This script checks quarantine/checksum coverage, metadata schema fields, optional
expression-column matching, and response-label guardrails. It does not compute
module scores or biological metrics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "primary": ROOT / "docs/validation/input_schemas/V45_primary_metadata_schema.tsv",
    "postpartum": ROOT / "docs/validation/input_schemas/V45_postpartum_apc_arm_schema.tsv",
    "tb": ROOT / "docs/validation/input_schemas/V45_tb_compartment_schema.tsv",
    "pharmacodynamic": ROOT / "docs/validation/input_schemas/V45_pharmacodynamic_only_schema.tsv",
}
CHECKSUM_NAMES = {"SHA256SUMS", "checksums.sha256", "sha256sums.txt"}
RESPONSE_LIKE_TOKENS = [
    "response",
    "responder",
    "nonresponder",
    "neda",
    "relapse",
    "remission",
    "edss_change",
    "outcome",
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def relative_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and path.name not in CHECKSUM_NAMES
    )


def write_checksums(root: Path, checksum_file: Path) -> None:
    lines = []
    for path in relative_files(root):
        rel = path.relative_to(root)
        lines.append(f"{sha256(path)}  {rel}\n")
    checksum_file.write_text("".join(lines))


def parse_checksums(root: Path) -> dict[str, str]:
    checksum_file = None
    for name in CHECKSUM_NAMES:
        candidate = root / name
        if candidate.exists():
            checksum_file = candidate
            break
    if checksum_file is None:
        return {}
    records = {}
    for line in checksum_file.read_text().splitlines():
        if not line.strip():
            continue
        parts = line.strip().split(maxsplit=1)
        if len(parts) != 2:
            continue
        digest, rel = parts
        rel = rel.lstrip("*")
        records[rel] = digest.lower()
    return records


def checksum_audit(root: Path) -> pd.DataFrame:
    expected = parse_checksums(root)
    rows = []
    for path in relative_files(root):
        rel = str(path.relative_to(root))
        observed = sha256(path)
        exp = expected.get(rel)
        rows.append(
            {
                "relative_path": rel,
                "in_checksum_file": exp is not None,
                "expected_sha256": exp or "",
                "observed_sha256": observed,
                "status": "PASS" if exp == observed else ("MISSING_CHECKSUM" if exp is None else "CHECKSUM_MISMATCH"),
            }
        )
    for rel, digest in expected.items():
        if not (root / rel).exists():
            rows.append(
                {
                    "relative_path": rel,
                    "in_checksum_file": True,
                    "expected_sha256": digest,
                    "observed_sha256": "",
                    "status": "LISTED_FILE_MISSING",
                }
            )
    return pd.DataFrame(rows)


def schema_rows(mode: str) -> pd.DataFrame:
    schema = pd.read_csv(SCHEMAS[mode], sep="\t")
    col_field = "column" if "column" in schema.columns else "field"
    req_field = "required" if "required" in schema.columns else "requirement"
    return schema.rename(columns={col_field: "field", req_field: "required_level"})


def metadata_schema_check(metadata: pd.DataFrame, mode: str) -> pd.DataFrame:
    schema = schema_rows(mode)
    rows = []
    for _, row in schema.iterrows():
        field = row["field"]
        level = str(row["required_level"])
        present = field in metadata.columns
        complete = bool(present and metadata[field].notna().all())
        required = level in {"yes", "required"}
        status = "PASS"
        if required and not present:
            status = "FAIL_MISSING_REQUIRED"
        elif required and not complete:
            status = "FAIL_MISSING_REQUIRED_VALUES"
        elif "strongly_required" in level and not complete:
            status = "WARN_MISSING_STRONGLY_REQUIRED"
        elif not present:
            status = "OPTIONAL_ABSENT"
        rows.append(
            {
                "field": field,
                "required_level": level,
                "present": present,
                "complete": complete,
                "missing_count": int(metadata[field].isna().sum()) if present else len(metadata),
                "status": status,
            }
        )
    return pd.DataFrame(rows)


def response_guard(metadata: pd.DataFrame, mode: str, allow_response_columns_for_pharmacodynamic: bool) -> pd.DataFrame:
    rows = []
    response_like = [col for col in metadata.columns if any(token in col.lower() for token in RESPONSE_LIKE_TOKENS)]
    if mode == "pharmacodynamic":
        for col in response_like:
            rows.append(
                {
                    "field": col,
                    "check": "pharmacodynamic_no_response_labels",
                    "status": "WARN_ALLOWED_BY_FLAG" if allow_response_columns_for_pharmacodynamic else "FAIL_RESPONSE_LIKE_COLUMN_PRESENT",
                    "note": "Response-like columns must not be used by pharmacodynamic-only harness.",
                }
            )
        if not response_like:
            rows.append(
                {
                    "field": "",
                    "check": "pharmacodynamic_no_response_labels",
                    "status": "PASS",
                    "note": "No response-like metadata columns detected.",
                }
            )
    else:
        expected = {"primary": "response", "postpartum": "postpartum_relapse_3m", "tb": "response"}[mode]
        status = "PASS" if expected in metadata.columns else "FAIL_EXPECTED_RESPONSE_FIELD_MISSING"
        rows.append(
            {
                "field": expected,
                "check": "response_label_required_for_validation_mode",
                "status": status,
                "note": "Response/outcome labels are required for this validation mode.",
            }
        )
    return pd.DataFrame(rows)


def expression_header_check(metadata: pd.DataFrame, expression: Path | None) -> pd.DataFrame:
    if expression is None:
        return pd.DataFrame(
            [
                {
                    "check": "expression_header_sample_match",
                    "status": "SKIPPED_NO_EXPRESSION",
                    "n_metadata_samples": int(metadata["sample_id"].nunique()) if "sample_id" in metadata.columns else 0,
                    "n_expression_samples": 0,
                    "missing_metadata_samples_in_expression": "",
                }
            ]
        )
    header = pd.read_csv(expression, sep="\t", nrows=0)
    expr_samples = list(header.columns[1:])
    meta_samples = metadata["sample_id"].astype(str).tolist() if "sample_id" in metadata.columns else []
    missing = sorted(set(meta_samples) - set(expr_samples))
    return pd.DataFrame(
        [
            {
                "check": "expression_header_sample_match",
                "status": "PASS" if not missing else "FAIL_METADATA_SAMPLES_MISSING_FROM_EXPRESSION",
                "n_metadata_samples": len(set(meta_samples)),
                "n_expression_samples": len(set(expr_samples)),
                "missing_metadata_samples_in_expression": ";".join(missing[:20]),
            }
        ]
    )


def run_check(
    root: Path,
    mode: str,
    metadata_path: Path,
    outdir: Path,
    expression_path: Path | None,
    write_checksum_file: bool,
    allow_response_columns_for_pharmacodynamic: bool,
) -> dict[str, object]:
    root = root.resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    if write_checksum_file:
        write_checksums(root, root / "SHA256SUMS")
    metadata = pd.read_csv(metadata_path, sep="\t")
    checksums = checksum_audit(root)
    schema = metadata_schema_check(metadata, mode)
    guard = response_guard(metadata, mode, allow_response_columns_for_pharmacodynamic)
    expr = expression_header_check(metadata, expression_path)
    check_tables = {
        "checksum_audit.tsv": checksums,
        "schema_check.tsv": schema,
        "response_guard.tsv": guard,
        "expression_header_check.tsv": expr,
    }
    for name, table in check_tables.items():
        table.to_csv(outdir / name, sep="\t", index=False)
    status_frames = [
        checksums[["status"]].assign(source="checksum"),
        schema[["status"]].assign(source="schema"),
        guard[["status"]].assign(source="response_guard"),
        expr[["status"]].assign(source="expression"),
    ]
    statuses = pd.concat(status_frames, ignore_index=True)
    fail_count = int(statuses["status"].astype(str).str.startswith("FAIL").sum())
    missing_checksum_count = int((checksums["status"] == "MISSING_CHECKSUM").sum())
    warn_count = int(statuses["status"].astype(str).str.startswith("WARN").sum())
    summary = {
        "mode": mode,
        "root": str(root),
        "metadata": str(metadata_path),
        "expression": str(expression_path) if expression_path else "",
        "files_audited": int(len(checksums)),
        "missing_checksum_count": missing_checksum_count,
        "fail_count": fail_count,
        "warn_count": warn_count,
        "overall_status": "PASS" if fail_count == 0 and missing_checksum_count == 0 else "FAIL",
        "note": "Preflight only; no module score or validation metric computed.",
    }
    (outdir / "preflight_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    pd.concat(
        [
            table.assign(table=name.removesuffix(".tsv"))
            for name, table in check_tables.items()
        ],
        ignore_index=True,
        sort=False,
    ).to_csv(outdir / "preflight_checks.tsv", sep="\t", index=False)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def synthetic_check(outdir: Path) -> int:
    root = outdir / "synthetic_quarantine"
    if root.exists():
        shutil.rmtree(root)
    (root / "metadata").mkdir(parents=True)
    (root / "processed").mkdir(parents=True)
    primary_meta = pd.DataFrame(
        {
            "sample_id": ["S1_BL", "S1_W6", "S2_BL", "S2_W6"],
            "patient": ["S1", "S1", "S2", "S2"],
            "timepoint": ["baseline", "week6", "baseline", "week6"],
            "response": ["Responder", "Responder", "Non-responder", "Non-responder"],
            "days_since_treatment": [0, 42, 0, 42],
            "batch": ["b1", "b1", "b2", "b2"],
            "processing_batch": ["p1", "p1", "p2", "p2"],
            "collection_date": ["2026-01-01", "2026-02-12", "2026-01-02", "2026-02-13"],
            "processing_date": ["2026-01-02", "2026-02-13", "2026-01-03", "2026-02-14"],
            "steroid_exposure": ["none", "none", "none", "none"],
            "prior_dmt": ["none", "none", "none", "none"],
            "concomitant_dmt": ["DMF", "DMF", "DMF", "DMF"],
            "outcome_window": ["15m", "15m", "15m", "15m"],
        }
    )
    pharma_meta = pd.DataFrame(
        {
            "sample_id": ["P1_BL", "P1_W2", "P2_BL", "P2_W2"],
            "subject": ["P1", "P1", "P2", "P2"],
            "timepoint": ["baseline", "week2", "baseline", "week2"],
            "days_since_treatment": [0, 14, 0, 14],
            "therapy": ["ocrelizumab", "ocrelizumab", "ocrelizumab", "ocrelizumab"],
            "therapy_class": ["anti_cd20", "anti_cd20", "anti_cd20", "anti_cd20"],
            "expression_platform": ["array", "array", "array", "array"],
            "disease": ["MS", "MS", "MS", "MS"],
            "batch": ["b1", "b1", "b2", "b2"],
            "processing_batch": ["p1", "p1", "p2", "p2"],
            "collection_date": ["2026-01-01", "2026-01-15", "2026-01-02", "2026-01-16"],
            "steroid_exposure": ["none", "none", "none", "none"],
        }
    )
    expr = pd.DataFrame(
        {
            "gene_id": ["STAT1", "HLA-DRA"],
            "S1_BL": [1, 2],
            "S1_W6": [2, 3],
            "S2_BL": [1, 2],
            "S2_W6": [1, 2],
        }
    )
    primary_meta_path = root / "metadata" / "primary_metadata.tsv"
    pharma_meta_path = root / "metadata" / "pharmacodynamic_metadata.tsv"
    bad_pharma_meta_path = root / "metadata" / "pharmacodynamic_with_response_metadata.tsv"
    expr_path = root / "processed" / "expression.tsv"
    primary_meta.to_csv(primary_meta_path, sep="\t", index=False)
    pharma_meta.to_csv(pharma_meta_path, sep="\t", index=False)
    bad_pharma = pharma_meta.copy()
    bad_pharma["response"] = ["Responder", "Responder", "Non-responder", "Non-responder"]
    bad_pharma.to_csv(bad_pharma_meta_path, sep="\t", index=False)
    expr.to_csv(expr_path, sep="\t", index=False)
    write_checksums(root, root / "SHA256SUMS")
    primary = run_check(
        root=root,
        mode="primary",
        metadata_path=primary_meta_path,
        outdir=outdir / "primary_preflight",
        expression_path=expr_path,
        write_checksum_file=False,
        allow_response_columns_for_pharmacodynamic=False,
    )
    pharma = run_check(
        root=root,
        mode="pharmacodynamic",
        metadata_path=pharma_meta_path,
        outdir=outdir / "pharmacodynamic_preflight",
        expression_path=None,
        write_checksum_file=False,
        allow_response_columns_for_pharmacodynamic=False,
    )
    bad_pharma_result = run_check(
        root=root,
        mode="pharmacodynamic",
        metadata_path=bad_pharma_meta_path,
        outdir=outdir / "pharmacodynamic_response_guard_preflight",
        expression_path=None,
        write_checksum_file=False,
        allow_response_columns_for_pharmacodynamic=False,
    )
    assertions = {
        "synthetic": True,
        "primary_preflight_pass": primary["overall_status"] == "PASS",
        "pharmacodynamic_preflight_pass": pharma["overall_status"] == "PASS",
        "pharmacodynamic_response_label_guard_fails": bad_pharma_result["overall_status"] == "FAIL",
        "no_module_scores_computed": True,
    }
    (outdir / "synthetic_check_assertions.json").write_text(json.dumps(assertions, indent=2, sort_keys=True) + "\n")
    print(json.dumps(assertions, indent=2, sort_keys=True))
    return 0 if all(v for k, v in assertions.items() if k != "synthetic") else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="Run intake preflight checks.")
    p_check.add_argument("--root", required=True, type=Path)
    p_check.add_argument("--mode", required=True, choices=sorted(SCHEMAS))
    p_check.add_argument("--metadata", required=True, type=Path)
    p_check.add_argument("--expression", type=Path)
    p_check.add_argument("--outdir", required=True, type=Path)
    p_check.add_argument("--write-checksums", action="store_true")
    p_check.add_argument("--allow-response-columns-for-pharmacodynamic", action="store_true")

    p_syn = sub.add_parser("synthetic-check", help="Verify preflight mechanics on synthetic files.")
    p_syn.add_argument("--outdir", type=Path, default=Path("analysis/v45_validation_intake_preflight"))

    args = parser.parse_args()
    if args.cmd == "check":
        summary = run_check(
            root=args.root,
            mode=args.mode,
            metadata_path=args.metadata,
            outdir=args.outdir,
            expression_path=args.expression,
            write_checksum_file=args.write_checksums,
            allow_response_columns_for_pharmacodynamic=args.allow_response_columns_for_pharmacodynamic,
        )
        return 0 if summary["overall_status"] == "PASS" else 1
    if args.cmd == "synthetic-check":
        return synthetic_check(args.outdir)
    raise AssertionError(args.cmd)


if __name__ == "__main__":
    raise SystemExit(main())
