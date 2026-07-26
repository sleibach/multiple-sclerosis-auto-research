#!/usr/bin/env python3
"""Build or verify a lightweight manifest of authored V55 public artifacts.

The manifest supports release maintenance. Hashes establish file identity only;
they do not validate scientific content or increase an evidence grade.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "analysis" / "v55_onboarding_manifest"
MANIFEST = OUTDIR / "artifact_manifest.tsv"
SUMMARY = OUTDIR / "artifact_manifest_summary.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Write committed outputs")
    mode.add_argument("--check", action="store_true", help="Compare with committed outputs")
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def artifact_paths() -> list[Path]:
    paths = list((ROOT / "docs" / "onboarding").rglob("*"))
    paths.extend((ROOT / "scripts").glob("v55_*.py"))
    paths.extend(
        ROOT / relative
        for relative in (
            ".github/ISSUE_TEMPLATE/research-direction.yml",
            ".github/pull_request_template.md",
            ".github/workflows/onboarding-integrity.yml",
            "CONTRIBUTING.md",
            "README.md",
            "meta/V55_QUEUE.md",
        )
    )
    return sorted({path for path in paths if path.is_file()})


def classify(path: Path) -> tuple[str, str, str]:
    relative = path.relative_to(ROOT)
    value = str(relative)
    if value.startswith("docs/onboarding/visuals/"):
        return "visual", "public orientation", "render+responsive+provenance gates"
    if value.startswith("docs/onboarding/templates/"):
        return "template", "collaboration operations", "onboarding+provenance gates"
    if value.startswith("docs/onboarding/"):
        kind = "print brief" if path.suffix == ".html" else "reader/review document"
        return kind, "public orientation", "onboarding+plain/source+provenance gates"
    if value.startswith("scripts/"):
        return "checker", "maintenance", "syntax+own regression path"
    if value.startswith(".github/workflows/"):
        return "continuous check", "maintenance", "workflow syntax+local command parity"
    if value.startswith(".github/"):
        return "contribution template", "collaboration operations", "onboarding+provenance gates"
    if value.startswith("meta/"):
        return "resume state", "operations", "provenance+time-accounting review"
    return "entry/contribution document", "public navigation", "onboarding+provenance gates"


def build_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in artifact_paths():
        content = path.read_bytes()
        artifact_type, audience_role, required_check = classify(path)
        rows.append(
            {
                "path": str(path.relative_to(ROOT)),
                "artifact_type": artifact_type,
                "audience_role": audience_role,
                "evidence_role": "communication_or_method_only_no_status_upgrade",
                "required_check": required_check,
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    return rows


def manifest_text(rows: list[dict[str, object]]) -> str:
    output = io.StringIO()
    fields = (
        "path",
        "artifact_type",
        "audience_role",
        "evidence_role",
        "required_check",
        "bytes",
        "sha256",
    )
    writer = csv.DictWriter(output, fieldnames=fields, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def summary_text(rows: list[dict[str, object]]) -> str:
    by_type: dict[str, int] = {}
    total_bytes = 0
    for row in rows:
        key = str(row["artifact_type"])
        by_type[key] = by_type.get(key, 0) + 1
        total_bytes += int(row["bytes"])
    payload = {
        "purpose": "V55 authored-artifact identity manifest; no scientific claim",
        "n_artifacts": len(rows),
        "total_bytes": total_bytes,
        "artifact_types": dict(sorted(by_type.items())),
        "n_files_over_50mb": sum(int(row["bytes"]) > 50 * 1024 * 1024 for row in rows),
        "n_tmp_paths": sum("/tmp/" in f"/{row['path']}/" for row in rows),
        "interpretation": (
            "Hashes and sizes support release identity only; they do not validate "
            "scientific truth, evidence class, or comprehension."
        ),
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main() -> int:
    args = parse_args()
    rows = build_rows()
    expected_manifest = manifest_text(rows)
    expected_summary = summary_text(rows)
    check_only = args.check
    failures: list[str] = []

    if check_only:
        if not MANIFEST.is_file() or MANIFEST.read_text(encoding="utf-8") != expected_manifest:
            failures.append("artifact_manifest.tsv is missing or stale")
        if not SUMMARY.is_file() or SUMMARY.read_text(encoding="utf-8") != expected_summary:
            failures.append("artifact_manifest_summary.json is missing or stale")
    else:
        OUTDIR.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(expected_manifest, encoding="utf-8")
        SUMMARY.write_text(expected_summary, encoding="utf-8")

    result = {
        "purpose": "V55 authored-artifact identity manifest; no scientific claim",
        "mode": "check" if check_only else "write",
        "n_artifacts": len(rows),
        "n_fail": len(failures),
        "failures": failures,
        "overall_status": "PASS" if not failures else "FAIL",
        "manifest": str(MANIFEST.relative_to(ROOT)),
        "summary": str(SUMMARY.relative_to(ROOT)),
    }
    print(json.dumps(result, indent=2))
    return 1 if args.fail_on_error and failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

