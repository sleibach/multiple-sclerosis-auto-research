#!/usr/bin/env python3
"""Download small Arc State released outputs used in V3.

Large companion AnnData files are deliberately not downloaded here because
they are ~9.1 GB each. Their absence is recorded as a blocker for gene-level
module scoring of the released DE outputs.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "state_parse_split4"
TMP = ROOT / "phases/v3/tmp"
DERIVED = ROOT / "data" / "derived_v3"

BASE = "https://huggingface.co/arcinstitute/ST-HVG-Parse/resolve/main/fewshot/split_4"
FILES = [
    (
        f"{BASE}/eval_best.ckpt/CD14_Mono_pred_de.csv",
        RAW / "CD14_Mono_pred_de.csv",
        "State predicted DE for CD14 monocyte cytokine perturbations",
    ),
    (
        f"{BASE}/eval_best.ckpt/CD14_Mono_real_de.csv",
        RAW / "CD14_Mono_real_de.csv",
        "Matched real DE for CD14 monocyte cytokine perturbations",
    ),
    (
        f"{BASE}/eval_best.ckpt/CD14_Mono_agg_results.csv",
        RAW / "CD14_Mono_agg_results.csv",
        "Aggregate State prediction metrics for CD14 monocytes",
    ),
    (
        f"{BASE}/var_dims.pkl",
        TMP / "var_dims_split4.pkl",
        "Released dimensions/gene-name metadata; exact 2,000-HVG order not recoverable from this alone",
    ),
    (
        f"{BASE}/data_module.torch",
        TMP / "data_module_split4.torch",
        "Released data-module configuration",
    ),
]

BLOCKED_LARGE = [
    {
        "url": f"{BASE}/eval_best.ckpt/adata_real.h5ad",
        "size_bytes": 9_112_404_896,
        "reason_not_downloaded": "Needed to recover exact HVG feature order, but too large for first-pass run without a stronger need.",
    },
    {
        "url": f"{BASE}/eval_best.ckpt/adata_pred.h5ad",
        "size_bytes": 9_112_404_896,
        "reason_not_downloaded": "Needed to recover exact HVG feature order, but too large for first-pass run without a stronger need.",
    },
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        return
    with urlopen(url, timeout=120) as resp, path.open("wb") as out:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    DERIVED.mkdir(parents=True, exist_ok=True)
    rows = []
    for url, path, description in FILES:
        download(url, path)
        rows.append(
            {
                "source": "arcinstitute/ST-HVG-Parse",
                "source_sha": "a69af46d5b8c6f8c036c489a8f71354f321d968b",
                "url": url,
                "local_path": str(path.relative_to(ROOT)),
                "description": description,
                "size_bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    manifest = DERIVED / "state_parse_split4_manifest.tsv"
    with manifest.open("w", encoding="utf-8") as fh:
        fields = ["source", "source_sha", "url", "local_path", "description", "size_bytes", "sha256"]
        fh.write("\t".join(fields) + "\n")
        for row in rows:
            fh.write("\t".join(str(row[f]) for f in fields) + "\n")
    (DERIVED / "state_parse_split4_blocked_large_files.json").write_text(json.dumps(BLOCKED_LARGE, indent=2) + "\n")
    print(f"Wrote {manifest}")


if __name__ == "__main__":
    main()
