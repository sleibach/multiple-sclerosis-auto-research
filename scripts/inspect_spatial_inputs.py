#!/usr/bin/env python3
"""Inspect deposited MERFISH files before selecting an analysis representation."""

from __future__ import annotations

import gzip
import io
import tarfile
from pathlib import Path


RAW = Path("data/raw")


def decode_head(handle: io.BufferedReader, n: int = 5) -> list[str]:
    lines = []
    for _ in range(n):
        line = handle.readline()
        if not line:
            break
        lines.append(line.decode(errors="replace").rstrip()[:1000])
    return lines


def main() -> int:
    soft_path = RAW / "GSE284005_family.soft.gz"
    print(f"## {soft_path}")
    with gzip.open(soft_path, "rt", errors="replace") as handle:
        for _ in range(60):
            line = handle.readline()
            if not line:
                break
            print(line.rstrip()[:1000])

    tar_path = RAW / "GSE284005_RAW.tar"
    print(f"\n## {tar_path}")
    with tarfile.open(tar_path) as tar:
        members = tar.getmembers()
        print(f"members={len(members)}")
        for member in members:
            print(f"{member.name}\t{member.size}")
        for member in members[:3]:
            extracted = tar.extractfile(member)
            if extracted is None:
                continue
            print(f"\n### head {member.name}")
            if member.name.endswith(".gz"):
                with gzip.GzipFile(fileobj=extracted) as nested:
                    for line in decode_head(nested):
                        print(line)
            else:
                for line in decode_head(extracted):
                    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
