#!/usr/bin/env python3
"""Index V45 committed outputs by front and evidence/usage class."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v45_artifact_index"
FIRST_V45_COMMIT = "fb9bf15"


def git_lines(args: list[str]) -> list[str]:
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, text=True, capture_output=True)
    return [line for line in result.stdout.splitlines() if line.strip()]


def latest_commit(path: str) -> str:
    lines = git_lines(["log", "-1", "--format=%h", "--", path])
    return lines[0] if lines else "pending_this_checkpoint"


def changed_paths() -> list[str]:
    commits = git_lines(["rev-list", "--reverse", f"{FIRST_V45_COMMIT}^..HEAD"])
    paths: set[str] = set()
    for commit in commits:
        for line in git_lines(["show", "--name-only", "--format=", commit]):
            if not line:
                continue
            paths.add(line)
    # Include the current checkpoint before it has been committed, so the index
    # can describe its own generator and outputs in the commit that adds them.
    for line in git_lines(["ls-files", "--others", "--exclude-standard"]):
        lower = line.lower()
        if "v45" in lower or "v46" in lower:
            paths.add(line)
    return sorted(paths)


def classify_front(path: str) -> str:
    lower = path.lower()
    if "karolinska" in lower or "gse228330" in lower or "outbound" in lower or "cohort_acquisition" in lower:
        return "cohort_dependence"
    if "batch" in lower or "pathology" in lower or "seed_variation" in lower or "regression" in lower:
        return "robustness"
    if "power" in lower or "cohort_spec" in lower or "dropout" in lower or "crf" in lower:
        return "power_design"
    if "convergence" in lower or "apc_hla" in lower:
        return "data_free_validation"
    if "preflight" in lower or "harness" in lower or "handoff" in lower or "schema" in lower or "subject_map" in lower or "pharmacodynamic_only" in lower:
        return "infrastructure"
    if "external" in lower or "rebuttal" in lower:
        return "external_account"
    if "rpt" in lower:
        return "infrastructure_rpt"
    if "queue" in lower:
        return "resume_backbone"
    return "infrastructure"


def classify_evidence(path: str) -> tuple[str, str]:
    lower = path.lower()
    if lower.endswith(".py"):
        return "software", "executable infrastructure; no biological claim by itself"
    if "synthetic" in lower or any(token in lower for token in ["simulation", "pathology", "calibration", "seed_variation", "regression", "power", "dropout"]):
        return "synthetic_method_behavior", "method behavior/planning only; never biological evidence"
    if any(token in lower for token in ["gse228330", "karolinska", "outbound", "cohort_acquisition", "request"]):
        return "public_or_external_acquisition_operations", "cohort availability/request readiness; no validation claim"
    if any(token in lower for token in ["convergence", "apc_hla_no", "family_jackknife"]):
        return "internal_convergence_null", "data-free internal support; not clinical validation"
    if "rpt" in lower:
        return "proposal_lens_grounding", "proposal prioritization only; no model output as evidence"
    if any(token in lower for token in ["preflight", "harness", "handoff", "schema", "subject_map", "intake"]):
        return "validation_infrastructure", "mechanical guardrail/readiness; no biological claim"
    if any(token in lower for token in ["external", "rebuttal", "account"]):
        return "synthesis_documentation", "external framing/checklist; no new analysis"
    if "queue" in lower:
        return "resume_state", "resume state and running backlog"
    return "documentation_or_governance", "governance/readiness documentation"


def status_for_path(path: str) -> str:
    if not (ROOT / path).exists():
        return "deleted_or_moved"
    if path.startswith("analysis/"):
        return "generated_output"
    if path.startswith("scripts/"):
        return "executable"
    if path.startswith("docs/"):
        return "documentation"
    if path.startswith("meta/"):
        return "resume_or_meta"
    return "tracked"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = changed_paths()
    rows = []
    for path in paths:
        evidence_class, allowed = classify_evidence(path)
        rows.append(
            {
                "path": path,
                "front": classify_front(path),
                "status": status_for_path(path),
                "evidence_class": evidence_class,
                "allowed_interpretation": allowed,
                "latest_commit": latest_commit(path),
                "contains_synthetic_marker": "synthetic" in path.lower(),
                "exists": (ROOT / path).exists(),
            }
        )
    table = pd.DataFrame(rows).sort_values(["front", "evidence_class", "path"])
    table.to_csv(OUT / "v45_artifact_index.tsv", sep="\t", index=False)
    summary_table = (
        table.groupby(["front", "evidence_class", "allowed_interpretation"], as_index=False)
        .agg(n_paths=("path", "nunique"))
        .sort_values(["front", "evidence_class"])
    )
    summary_table.to_csv(OUT / "front_class_summary.tsv", sep="\t", index=False)
    summary = {
        "purpose": "V45 artifact governance index; no biological claim",
        "first_v45_commit": FIRST_V45_COMMIT,
        "n_paths_indexed": int(len(table)),
        "n_fronts": int(table["front"].nunique()),
        "n_evidence_classes": int(table["evidence_class"].nunique()),
        "front_counts": table["front"].value_counts().sort_index().to_dict(),
        "evidence_class_counts": table["evidence_class"].value_counts().sort_index().to_dict(),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
