#!/usr/bin/env python3
"""Enforce V51 structural-prediction provenance and confidence fields.

AlphaFold records are external-unverifiable predictions. This gate verifies
that predicted structures stay in the external structural tree, carry source
and model version metadata, and expose confidence provenance before they are
used as druggability context.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis/v51_structural_prediction_gate"
STRUCTURAL_ROOT = "knowledge_external/structures"
RECORD_TYPE = "structural_prediction"
EXTERNAL_CLASS = "external-unverifiable"
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"
PREDICTION_MARKER = "PREDICTED_STRUCTURE_NOT_EXPERIMENTAL"
GROUND_TREE_PREFIXES = [
    "docs/findings/",
    "docs/history/",
    "docs/locked_rules/",
    "docs/reports/",
    "docs/validation/",
    "docs/workups/",
    "knowledge/",
    "results/",
]
ALLOWED_NON_STRUCTURAL_PREFIXES = [
    "docs/knowledge/",
    "analysis/v51_structural_prediction_gate/",
    "scripts/v51_structural_prediction_gate.py",
    "meta/V51_QUEUE.md",
]


@dataclass
class GateIssue:
    path: str
    check: str
    status: str
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit", help="Audit structural-prediction records")
    audit.add_argument("--root", type=Path, default=ROOT)
    audit.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    audit.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic structural gate fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_json(path: Path) -> tuple[dict[str, Any] | None, str]:
    try:
        data = json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001 - gate reports parser failures.
        return None, str(exc)
    if not isinstance(data, dict):
        return None, "JSON root is not an object"
    return data, ""


def nested_get(data: dict[str, Any], dotted: str) -> Any:
    value: Any = data
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def has_text(data: dict[str, Any], dotted: str) -> bool:
    return bool(str(nested_get(data, dotted) or "").strip())


def has_source(source: Any) -> bool:
    if not isinstance(source, dict):
        return False
    if not str(source.get("label", "")).strip():
        return False
    return any(str(source.get(field, "")).strip() for field in ["url", "doi", "citation", "label"])


def local_path_exists(root: Path, maybe_path: str) -> bool:
    if not maybe_path:
        return False
    path = Path(maybe_path)
    if path.is_absolute():
        return path.exists()
    return (root / path).exists()


def structural_json_files(root: Path) -> list[Path]:
    base = root / STRUCTURAL_ROOT
    if not base.exists():
        return []
    files: list[Path] = []
    for path in sorted(base.rglob("*.json")):
        if not path.is_file():
            continue
        if path.name == "record.json":
            files.append(path)
            continue
        data, _ = load_json(path)
        if isinstance(data, dict) and data.get("record_type") == RECORD_TYPE:
            files.append(path)
    return files


def is_allowed_non_structural(rel_path: str) -> bool:
    return any(rel_path == prefix or rel_path.startswith(prefix) for prefix in ALLOWED_NON_STRUCTURAL_PREFIXES)


def is_grounded_prefix(rel_path: str) -> bool:
    return any(rel_path.startswith(prefix) for prefix in GROUND_TREE_PREFIXES)


def audit_structural_record(root: Path, path: Path) -> list[GateIssue]:
    rel_path = rel(root, path)
    issues: list[GateIssue] = []
    data, error = load_json(path)
    if data is None:
        return [GateIssue(rel_path, "json_parse", "FAIL", error)]

    checks = {
        "record_type_valid": data.get("record_type") == RECORD_TYPE,
        "epistemic_class_external_unverifiable": data.get("epistemic_class") == EXTERNAL_CLASS,
        "not_project_grounded_marker": data.get("not_project_grounded_marker") == NOT_GROUNDED,
        "prediction_marker": data.get("predicted_structure_not_experimental_marker") == PREDICTION_MARKER,
        "record_id_present": has_text(data, "record_id"),
        "claim_present": has_text(data, "claim"),
        "source_present": has_source(data.get("source")),
        "date_accessed_present": has_text(data, "date_accessed"),
        "why_unverifiable_present": has_text(data, "why_unverifiable"),
        "relationship_to_project_present": has_text(data, "relationship_to_project_findings"),
        "protein_uniprot_id_present": has_text(data, "protein.uniprot_id"),
        "protein_gene_symbol_present": has_text(data, "protein.gene_symbol"),
        "protein_sequence_present": has_text(data, "protein.sequence"),
        "protein_sequence_source_present": has_text(data, "protein.sequence_source"),
        "model_source_present": has_text(data, "model.source"),
        "model_entity_id_present": has_text(data, "model.model_entity_id"),
        "model_version_present": has_text(data, "model.model_version"),
        "model_source_url_present": has_text(data, "model.source_url"),
        "model_retrieval_date_present": has_text(data, "model.retrieval_date"),
        "plddt_mean_present": nested_get(data, "confidence.plddt.mean") is not None,
        "plddt_per_residue_path_present": has_text(data, "confidence.plddt.per_residue_path"),
        "pae_mean_present": nested_get(data, "confidence.pae.mean") is not None,
        "pae_matrix_or_source_present": has_text(data, "confidence.pae.matrix_path") or has_text(data, "confidence.pae.source_url"),
    }

    plddt_path = str(nested_get(data, "confidence.plddt.per_residue_path") or "")
    if plddt_path:
        checks["plddt_per_residue_path_exists"] = local_path_exists(root, plddt_path)
    pae_matrix_path = str(nested_get(data, "confidence.pae.matrix_path") or "")
    if pae_matrix_path:
        checks["pae_matrix_path_exists"] = local_path_exists(root, pae_matrix_path)
    structure_path = str(nested_get(data, "structure_files.pdb_path") or "")
    if structure_path:
        checks["pdb_path_exists"] = local_path_exists(root, structure_path)

    plddt_mean = nested_get(data, "confidence.plddt.mean")
    if plddt_mean is not None:
        checks["plddt_mean_range"] = isinstance(plddt_mean, (int, float)) and 0 <= float(plddt_mean) <= 100
    pae_mean = nested_get(data, "confidence.pae.mean")
    if pae_mean is not None:
        checks["pae_mean_nonnegative"] = isinstance(pae_mean, (int, float)) and float(pae_mean) >= 0

    for check, ok in checks.items():
        issues.append(GateIssue(rel_path, check, "PASS" if ok else "FAIL", str(data.get("record_id", ""))))
    return issues


def audit_structural_markers_outside_tree(root: Path) -> list[GateIssue]:
    issues: list[GateIssue] = []
    markers = [RECORD_TYPE, PREDICTION_MARKER]
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel_path = rel(root, path)
        if rel_path.startswith(f"{STRUCTURAL_ROOT}/") or is_allowed_non_structural(rel_path):
            continue
        if path.suffix.lower() not in {".json", ".md", ".txt", ".tsv"}:
            continue
        try:
            if path.stat().st_size > 1_500_000:
                continue
            text = path.read_text(errors="ignore")
        except OSError:
            continue
        if any(marker in text for marker in markers) and is_grounded_prefix(rel_path):
            issues.append(GateIssue(rel_path, "structural_prediction_marker_outside_external_structures", "FAIL", "structural marker in grounded tree"))
    return issues


def audit_root(root: Path, outdir: Path) -> tuple[dict[str, object], list[GateIssue]]:
    outdir.mkdir(parents=True, exist_ok=True)
    issues: list[GateIssue] = []
    structural_root = root / STRUCTURAL_ROOT
    issues.append(GateIssue(STRUCTURAL_ROOT, "structural_root_exists", "PASS" if structural_root.exists() else "FAIL", rel(root, structural_root)))
    files = structural_json_files(root)
    issues.append(GateIssue(STRUCTURAL_ROOT, "structural_json_record_present", "PASS" if files else "FAIL", str(len(files))))
    for path in files:
        issues.extend(audit_structural_record(root, path))
    issues.extend(audit_structural_markers_outside_tree(root))
    n_fail = sum(1 for issue in issues if issue.status != "PASS")
    rows = [issue.__dict__ for issue in issues]
    write_tsv(outdir / "structural_prediction_gate_issues.tsv", rows, ["path", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V51 structural prediction gate; no biological claim",
        "root": str(root),
        "n_checks": len(issues),
        "n_fail": n_fail,
        "n_structural_json_records": len(files),
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "issues": rel(root, outdir / "structural_prediction_gate_issues.tsv") if root == ROOT else str(outdir / "structural_prediction_gate_issues.tsv"),
    }
    (outdir / "structural_prediction_gate_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary, issues


def write_json(path: Path, **kwargs: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(kwargs, indent=2, sort_keys=True) + "\n")


def write_good_synthetic_record(root: Path) -> None:
    base = root / STRUCTURAL_ROOT / "alphafold" / "SYNTH"
    base.mkdir(parents=True, exist_ok=True)
    (base / "synthetic.pdb").write_text("HEADER SYNTHETIC STRUCTURE\n")
    (base / "synthetic_plddt.tsv").write_text("residue_index\taa\tplddt\n1\tM\t90.0\n2\tA\t80.0\n")
    write_json(base / "synthetic_pae.json", predicted_aligned_error=[[0.0, 1.0], [1.0, 0.0]], max_predicted_aligned_error=31.75)
    write_json(
        base / "record.json",
        record_id="V51_SYNTH_STRUCTURAL_GOOD",
        record_type=RECORD_TYPE,
        claim="Synthetic AlphaFold-style structural-prediction record used only to test the V51 gate.",
        epistemic_class=EXTERNAL_CLASS,
        source={"label": "Synthetic AlphaFold fixture", "url": "https://example.invalid/alphafold/synthetic"},
        date_accessed="2026-07-09",
        relationship_to_project_findings="orthogonal",
        not_project_grounded_marker=NOT_GROUNDED,
        predicted_structure_not_experimental_marker=PREDICTION_MARKER,
        why_unverifiable="Synthetic fixture and predicted-structure class are not project-grounded experimental evidence.",
        protein={
            "uniprot_id": "SYNTH",
            "gene_symbol": "SYNTH",
            "organism": "Synthetic organism",
            "sequence": "MA",
            "sequence_source": "synthetic fixture",
        },
        model={
            "source": "Synthetic AlphaFold-like fixture",
            "model_entity_id": "AF-SYNTH-F1",
            "model_version": "synthetic-v1",
            "source_url": "https://example.invalid/alphafold/synthetic",
            "retrieval_date": "2026-07-09",
        },
        structure_files={"pdb_path": f"{STRUCTURAL_ROOT}/alphafold/SYNTH/synthetic.pdb"},
        confidence={
            "plddt": {"mean": 85.0, "per_residue_path": f"{STRUCTURAL_ROOT}/alphafold/SYNTH/synthetic_plddt.tsv"},
            "pae": {"mean": 0.5, "matrix_path": f"{STRUCTURAL_ROOT}/alphafold/SYNTH/synthetic_pae.json"},
        },
    )


def build_synthetic_root(base: Path) -> Path:
    root = base / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    (root / "docs/history").mkdir(parents=True)
    write_good_synthetic_record(root)
    return root


def run_synthetic(outdir: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    outdir.mkdir(parents=True, exist_ok=True)
    root = build_synthetic_root(outdir)
    cases: list[dict[str, object]] = []

    def run_case(case_id: str, mutate: Any, expected_status: str) -> None:
        case_root = outdir / f"case_{case_id}"
        if case_root.exists():
            shutil.rmtree(case_root)
        shutil.copytree(root, case_root)
        mutate(case_root)
        summary, _ = audit_root(case_root, outdir / f"case_{case_id}_audit")
        observed = str(summary["overall_status"])
        cases.append(
            {
                "case_id": case_id,
                "expected_status": expected_status,
                "observed_status": observed,
                "expectation_met": str(observed == expected_status).lower(),
                "n_fail": summary["n_fail"],
                "audit_dir": str(outdir / f"case_{case_id}_audit"),
            }
        )

    run_case("proper_structural_prediction_passes", lambda _: None, "PASS")

    def missing_confidence(case_root: Path) -> None:
        path = case_root / STRUCTURAL_ROOT / "alphafold/SYNTH/record.json"
        data = json.loads(path.read_text())
        data.pop("confidence")
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

    run_case("missing_confidence_fails", missing_confidence, "FAIL")

    def missing_prediction_marker(case_root: Path) -> None:
        path = case_root / STRUCTURAL_ROOT / "alphafold/SYNTH/record.json"
        data = json.loads(path.read_text())
        data.pop("predicted_structure_not_experimental_marker")
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

    run_case("missing_prediction_marker_fails", missing_prediction_marker, "FAIL")

    def missing_model_version(case_root: Path) -> None:
        path = case_root / STRUCTURAL_ROOT / "alphafold/SYNTH/record.json"
        data = json.loads(path.read_text())
        data["model"].pop("model_version")
        path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

    run_case("missing_model_version_fails", missing_model_version, "FAIL")

    def structural_in_grounded_tree(case_root: Path) -> None:
        source = case_root / STRUCTURAL_ROOT / "alphafold/SYNTH/record.json"
        target = case_root / "docs/history/structural_prediction_bad.json"
        target.write_text(source.read_text())

    run_case("structural_prediction_in_grounded_tree_fails", structural_in_grounded_tree, "FAIL")

    n_fail = sum(1 for case in cases if case["expectation_met"] != "true")
    write_tsv(outdir / "synthetic_structural_prediction_gate_cases.tsv", cases, ["case_id", "expected_status", "observed_status", "expectation_met", "n_fail", "audit_dir"])
    summary = {
        "synthetic": True,
        "purpose": "V51 structural prediction gate synthetic pass/fail fixtures; no biological claim",
        "n_cases": len(cases),
        "n_expected_fail_cases": sum(1 for case in cases if case["expected_status"] == "FAIL"),
        "n_expectation_failures": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "cases": str(outdir / "synthetic_structural_prediction_gate_cases.tsv"),
    }
    (outdir / "synthetic_structural_prediction_gate_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary, cases


def main() -> int:
    args = parse_args()
    if args.command == "audit":
        root = args.root if args.root.is_absolute() else ROOT / args.root
        outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
        summary, _ = audit_root(root, outdir)
        if args.fail_on_error and summary["overall_status"] != "PASS":
            return 1
        return 0 if summary["overall_status"] == "PASS" else 2
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    summary, _ = run_synthetic(outdir)
    if args.fail_on_error and summary["overall_status"] != "PASS":
        return 1
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
