#!/usr/bin/env python3
"""Verify OpenGWAS JWT access without printing the token.

The project keeps OPENGWAS_JWT in `.env`; non-interactive shells do not load it
automatically. This script loads `.env` explicitly, then checks a small set of
OpenGWAS API v4 endpoints using POST where required.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOTENV = ROOT / ".env"
API = "https://api.opengwas.io/api"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def request_json(path: str, jwt: str, payload: dict[str, Any] | None = None) -> tuple[int, Any]:
    data = None
    headers = {"Authorization": f"Bearer {jwt}"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(f"{API}{path}", data=data, headers=headers, method="POST" if payload is not None else "GET")
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read()
        parsed = json.loads(body.decode("utf-8"))
        return resp.status, parsed


def main() -> int:
    load_dotenv(DOTENV)
    jwt = os.environ.get("OPENGWAS_JWT")
    if not jwt:
        print("OPENGWAS_JWT missing after loading .env")
        return 2

    print(f"OPENGWAS_JWT loaded: true; length={len(jwt)}")

    checks: list[tuple[str, str, dict[str, Any] | None]] = [
        ("user", "/user", None),
        ("gwasinfo_ieu_b_18", "/gwasinfo", {"id": ["ieu-b-18"]}),
        ("tophits_ieu_b_18", "/tophits", {"id": ["ieu-b-18"], "pval": 5e-8, "clump": 1}),
    ]

    for name, path, payload in checks:
        try:
            status, parsed = request_json(path, jwt, payload)
        except urllib.error.HTTPError as exc:
            print(f"{name}: HTTP {exc.code}")
            return 1
        except Exception as exc:
            print(f"{name}: {type(exc).__name__}: {exc}")
            return 1

        if name == "user":
            user = parsed.get("user", {}) if isinstance(parsed, dict) else {}
            valid_until = user.get("jwt_valid_until", "unknown")
            print(f"{name}: HTTP {status}; jwt_valid_until={valid_until}")
        elif name == "gwasinfo_ieu_b_18":
            row = parsed[0] if isinstance(parsed, list) and parsed else {}
            print(
                f"{name}: HTTP {status}; id={row.get('id')}; trait={row.get('trait')}; "
                f"sample_size={row.get('sample_size')}"
            )
        else:
            n_rows = len(parsed) if isinstance(parsed, list) else "unknown"
            first = parsed[0].get("rsid") if isinstance(parsed, list) and parsed and isinstance(parsed[0], dict) else "none"
            print(f"{name}: HTTP {status}; rows={n_rows}; first_rsid={first}")

    print("OpenGWAS access check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
