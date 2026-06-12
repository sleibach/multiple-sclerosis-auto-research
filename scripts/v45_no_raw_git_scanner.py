#!/usr/bin/env python3
"""Scan git-tracked/pending paths for forbidden raw/quarantine data commits."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v45_no_raw_git_scanner"

HARD_FORBIDDEN_PREFIXES = [
    "data/quarantine/",
    "data/raw_v3/gafson_dmf_2018/",
    "data/raw_v3/karolinska_dmf_ros_2019/",
    "data/raw_v3/gse228330_ocrelizumab_outcomes/",
]
RAW_PREFIXES = ["data/raw/", "data/raw_v2/", "data/raw_v3/", "data/raw_v35/"]
RESTRICTED_NAME_TOKENS = [
    "signed",
    "agreement",
    "contract",
    "credential",
    "credentials",
    "secret",
    "token",
    "private",
    "data_use_terms.txt",
]
INDIVIDUAL_LEVEL_EXTENSIONS = [
    ".cel",
    ".fastq",
    ".fq",
    ".bam",
    ".cram",
    ".vcf",
    ".idat",
]


def git_lines(args: list[str]) -> list[str]:
    result = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=True)
    return [line for line in result.stdout.splitlines() if line.strip()]


def tracked_and_pending_paths() -> list[dict[str, str]]:
    rows = [{"path": path, "source": "tracked"} for path in git_lines(["ls-files"])]
    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True)
    for line in status.stdout.splitlines():
        if not line.strip():
            continue
        status_code = line[:2].strip() or "pending"
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        rows.append({"path": path, "source": f"pending:{status_code}"})
    dedup = {}
    for row in rows:
        dedup[(row["path"], row["source"])] = row
    return sorted(dedup.values(), key=lambda r: (r["path"], r["source"]))


def classify(path: str, source: str) -> tuple[str, str]:
    lower = path.lower()
    if any(path.startswith(prefix) for prefix in HARD_FORBIDDEN_PREFIXES):
        return "FAIL", "live/quarantine cohort raw path must not be committed"
    if any(token in lower for token in RESTRICTED_NAME_TOKENS) and path.startswith("data/"):
        return "FAIL", "restricted/agreement/credential-like file under data path"
    if any(lower.endswith(ext) or f"{ext}." in lower for ext in INDIVIDUAL_LEVEL_EXTENSIONS) and (
        path.startswith("data/quarantine/") or "gafson" in lower or "karolinska" in lower or "gse228330" in lower
    ):
        return "FAIL", "individual-level assay file in live validation path"
    if any(path.startswith(prefix) for prefix in RAW_PREFIXES):
        return "WARN", "historical/public raw-data path; do not add new restricted validation data here"
    if source.startswith("pending") and path.startswith("data/"):
        return "WARN", "pending data-path change requires manual review"
    return "PASS", "no raw/quarantine/restricted-path pattern detected"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for row in tracked_and_pending_paths():
        level, reason = classify(row["path"], row["source"])
        if level != "PASS":
            rows.append({"level": level, "path": row["path"], "source": row["source"], "reason": reason})
    audit = pd.DataFrame(rows, columns=["level", "path", "source", "reason"])
    audit.to_csv(OUT / "no_raw_git_audit.tsv", sep="\t", index=False)
    n_fail = int((audit["level"] == "FAIL").sum()) if not audit.empty else 0
    n_warn = int((audit["level"] == "WARN").sum()) if not audit.empty else 0
    summary = {
        "status": "scanner_only",
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "n_fail": n_fail,
        "n_warn": n_warn,
        "hard_forbidden_prefixes": HARD_FORBIDDEN_PREFIXES,
        "note": "WARN rows include historical public raw-data paths; FAIL rows block commit until resolved.",
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
