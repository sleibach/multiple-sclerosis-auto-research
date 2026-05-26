#!/usr/bin/env python3
"""Emit structural diagnostics for downloaded GEO files before analysis coding."""

from __future__ import annotations

import gzip
import tarfile
from pathlib import Path


RAW = Path("data/raw")


def print_text_head(path: Path, n: int = 6) -> None:
    opener = gzip.open if path.suffix == ".gz" else path.open
    mode = "rt"
    print(f"\n## {path}")
    with opener(path, mode, errors="replace") as handle:
        for _ in range(n):
            line = handle.readline()
            if not line:
                break
            print(line.rstrip()[:500])


def main() -> int:
    print_text_head(RAW / "GSE180759_annotation.txt.gz", n=8)
    print_text_head(RAW / "GSE180759_expression_matrix.csv.gz", n=3)
    print_text_head(RAW / "GSE279972_family.soft.gz", n=30)
    tar_path = RAW / "GSE279972_RAW.tar"
    print(f"\n## {tar_path}")
    with tarfile.open(tar_path) as tar:
        members = tar.getmembers()
        print(f"members={len(members)}")
        for member in members[:12]:
            print(f"{member.name}\t{member.size}")
        if members:
            extracted = tar.extractfile(members[0])
            if extracted is not None:
                if members[0].name.endswith(".gz"):
                    with gzip.GzipFile(fileobj=extracted) as nested:
                        for _ in range(5):
                            print(nested.readline().decode(errors="replace").rstrip()[:500])
                else:
                    for _ in range(5):
                        print(extracted.readline().decode(errors="replace").rstrip()[:500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
