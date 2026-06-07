#!/usr/bin/env python3
"""Minimal OpenAI API key checker for optional V28 sub-model lens."""

from __future__ import annotations

import json
import os
import sys
import urllib.request


def main() -> int:
    key = os.environ.get("OPENAI_API_KEY")
    print(f"OPENAI_API_KEY loaded: {bool(key)}; length={len(key or '')}")
    if not key:
        return 2
    req = urllib.request.Request(
        "https://api.openai.com/v1/models",
        headers={"Authorization": f"Bearer {key}"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            models = body.get("data", [])
            first = models[0].get("id") if models else "none"
            print(f"models: HTTP {resp.status}; count={len(models)}; first={first}")
            return 0 if resp.status == 200 else 1
    except Exception as exc:  # pragma: no cover - diagnostic script
        print(f"models: error={type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
