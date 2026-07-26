#!/usr/bin/env python3
"""Audit the public onboarding package for lightweight, self-contained delivery."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "docs" / "onboarding"
DEFAULT_OUTDIR = ROOT / "analysis" / "v55_public_package_footprint"
ALLOWED_EXTENSIONS = {".html", ".md", ".svg", ".tsv"}
MAX_FILE_BYTES = 512 * 1024
MAX_PACKAGE_BYTES = 5 * 1024 * 1024
HEAVY_EXTENSIONS = {
    ".7z", ".bin", ".gif", ".gz", ".h5ad", ".jpeg", ".jpg", ".mp4",
    ".parquet", ".pdf", ".png", ".safetensors", ".tar", ".webp", ".zip",
}
HTML_ASSET_RE = re.compile(
    r"<(?:script|img)\b[^>]*\bsrc\s*=|<link\b[^>]*\bhref\s*=",
    flags=re.IGNORECASE,
)
SVG_ASSET_RE = re.compile(
    r"<(?:image|script)\b[^>]*(?:href|xlink:href)\s*=|\bdata:",
    flags=re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("path", "bytes", "extension", "status", "detail"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    files = sorted(path for path in PACKAGE.rglob("*") if path.is_file())
    rows: list[dict[str, object]] = []
    extension_counts: Counter[str] = Counter()
    total_bytes = 0
    failures = 0

    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        extension = path.suffix.lower() or "[none]"
        size = path.stat().st_size
        total_bytes += size
        extension_counts[extension] += 1
        problems: list[str] = []

        if extension not in ALLOWED_EXTENSIONS:
            problems.append("extension is not in the public text/vector allowlist")
        if extension in HEAVY_EXTENSIONS:
            problems.append("heavy media/archive/model extension is forbidden")
        if size > MAX_FILE_BYTES:
            problems.append(f"file exceeds {MAX_FILE_BYTES} bytes")
        if "tmp" in path.relative_to(PACKAGE).parts:
            problems.append("tmp path is forbidden")

        raw = path.read_bytes()
        if b"\x00" in raw:
            problems.append("binary NUL byte detected")
        text = raw.decode("utf-8", errors="replace")
        if extension == ".html" and HTML_ASSET_RE.search(text):
            problems.append("HTML references a script, image, or stylesheet asset")
        if extension == ".svg" and SVG_ASSET_RE.search(text):
            problems.append("SVG embeds or references an image/script payload")

        status = "FAIL" if problems else "PASS"
        failures += int(bool(problems))
        rows.append(
            {
                "path": relative,
                "bytes": size,
                "extension": extension,
                "status": status,
                "detail": "; ".join(problems) if problems else "lightweight text/vector asset",
            }
        )

    if total_bytes > MAX_PACKAGE_BYTES:
        failures += 1

    visuals = [row for row in rows if str(row["path"]).startswith("docs/onboarding/visuals/")]
    largest = max(rows, key=lambda row: int(row["bytes"]), default=None)
    summary = {
        "purpose": "V55 public onboarding package footprint audit; no scientific claim",
        "n_files": len(rows),
        "total_bytes": total_bytes,
        "max_package_bytes": MAX_PACKAGE_BYTES,
        "max_file_bytes": MAX_FILE_BYTES,
        "largest_file": largest["path"] if largest else None,
        "largest_file_bytes": largest["bytes"] if largest else 0,
        "extension_counts": dict(sorted(extension_counts.items())),
        "n_visual_files": len(visuals),
        "visual_bytes": sum(int(row["bytes"]) for row in visuals),
        "n_fail": failures,
        "overall_status": "FAIL" if failures else "PASS",
        "files": "analysis/v55_public_package_footprint/package_files.tsv",
        "interpretation": (
            "Delivery footprint only; small files do not prove accessibility, "
            "comprehension, correctness, or scientific validity."
        ),
    }
    write_tsv(outdir / "package_files.tsv", rows)
    (outdir / "package_footprint_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 1 if args.fail_on_error and failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
