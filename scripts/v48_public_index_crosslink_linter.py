#!/usr/bin/env python3
"""Lint local links in knowledge_external/INDEX.md.

This checks navigation integrity only. It does not validate external sources or
make biological claims.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = ROOT / "knowledge_external/INDEX.md"
DEFAULT_OUTDIR = ROOT / "analysis/v48_public_index_crosslink_linter"
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    lint = sub.add_parser("lint", help="Lint public external index local links")
    lint.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    lint.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    lint.add_argument("--fail-on-error", action="store_true")
    synth = sub.add_parser("synthetic-check", help="Run synthetic crosslink fixtures")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def extract_links(text: str) -> list[str]:
    return [match.group(1).strip() for match in LINK_RE.finditer(text)]


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def lint_index(index: Path, outdir: Path, fail_on_error: bool) -> int:
    outdir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    if not index.exists():
        rows.append({"link": "", "target": str(index), "check": "index_exists", "status": "FAIL", "detail": "missing index"})
    else:
        base = index.parent
        for link in extract_links(index.read_text(errors="ignore")):
            if link.startswith(("http://", "https://", "mailto:", "#")):
                rows.append({"link": link, "target": link, "check": "external_or_anchor_skipped", "status": "PASS", "detail": ""})
                continue
            target = (base / link.split("#", 1)[0]).resolve()
            rows.append({"link": link, "target": str(target), "check": "local_target_exists", "status": "PASS" if target.exists() else "FAIL", "detail": ""})
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    write_tsv(outdir / "public_index_crosslink_lint.tsv", rows, ["link", "target", "check", "status", "detail"])
    summary = {
        "synthetic": False,
        "purpose": "V48 public external index crosslink lint; navigation only",
        "index": str(index),
        "n_links": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "lint": str(outdir / "public_index_crosslink_lint.tsv"),
    }
    (outdir / "public_index_crosslink_lint_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    if outdir.exists():
        shutil.rmtree(outdir)
    root = outdir / "synthetic_root"
    ext = root / "knowledge_external"
    ext.mkdir(parents=True)
    (ext / "ok.md").write_text("ok\n")
    (ext / "INDEX.md").write_text("[ok](ok.md)\n[bad](missing.md)\n[remote](https://example.invalid)\n")
    lint_out = outdir / "synthetic_lint"
    lint_index(ext / "INDEX.md", lint_out, fail_on_error=False)
    rows = list(csv.DictReader((lint_out / "public_index_crosslink_lint.tsv").open(), delimiter="\t"))
    checks = {
        "ok_link_passes": any(row["link"] == "ok.md" and row["status"] == "PASS" for row in rows),
        "missing_link_fails": any(row["link"] == "missing.md" and row["status"] == "FAIL" for row in rows),
        "remote_link_skipped": any(row["link"] == "https://example.invalid" and row["status"] == "PASS" for row in rows),
    }
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_public_index_crosslink_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V48 public external index crosslink synthetic fixture; navigation only",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_public_index_crosslink_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "lint":
        return lint_index(args.index, args.outdir, args.fail_on_error)
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
