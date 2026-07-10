#!/usr/bin/env python3
"""Validate V52 received-package IDs before creating intake paths."""

from __future__ import annotations

import argparse
import re


PACKAGE_ID_RE = re.compile(r"^\d{8}_[a-z0-9]+(?:_[a-z0-9]+)*$")


def validate(package_id: str) -> tuple[bool, str]:
    if not PACKAGE_ID_RE.match(package_id):
        return False, "must match YYYYMMDD_lowercase_alnum_underscore_segments"
    if "__" in package_id or package_id.endswith("_"):
        return False, "must not contain empty underscore segments"
    return True, "PASS"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("package_id")
    args = parser.parse_args()

    ok, detail = validate(args.package_id)
    print({"package_id": args.package_id, "status": "PASS" if ok else "FAIL", "detail": detail})
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
