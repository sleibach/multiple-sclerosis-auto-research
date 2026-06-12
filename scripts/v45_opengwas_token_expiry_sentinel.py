#!/usr/bin/env python3
"""Decode and classify the local OpenGWAS JWT expiry without printing it.

This sentinel is an operations guard only. It makes no OpenGWAS requests and
does not produce genetic evidence. The POST-only access check remains
`scripts/check_opengwas_access.py`.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DOTENV = ROOT / ".env"
DEFAULT_OUTDIR = ROOT / "analysis/v45_opengwas_token_expiry_sentinel"
RENEW_SOON_DAYS = 7
URGENT_DAYS = 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def dotenv_value(key: str) -> str:
    if not DOTENV.exists():
        return ""
    for raw in DOTENV.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        lhs, rhs = line.split("=", 1)
        if lhs.strip() == key:
            return rhs.strip().strip('"').strip("'")
    return ""


def decode_expiry(jwt: str) -> tuple[dt.datetime | None, str]:
    try:
        payload = jwt.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        parsed = json.loads(base64.urlsafe_b64decode(payload.encode("utf-8")))
        exp = parsed.get("exp")
        if exp is None:
            return None, "JWT payload lacks exp"
        return dt.datetime.fromtimestamp(int(exp), tz=dt.timezone.utc), "decoded"
    except Exception as exc:
        return None, f"decode_failed:{type(exc).__name__}"


def classify(expiry: dt.datetime | None, now: dt.datetime, jwt: str) -> tuple[str, str, float | None]:
    if not jwt:
        return "MISSING", "OPENGWAS_JWT not found in .env", None
    if expiry is None:
        return "INVALID_FORMAT", "JWT could not be decoded locally; renew before OpenGWAS work", None
    remaining = (expiry - now).total_seconds() / 86400.0
    if remaining <= 0:
        return "EXPIRED", "renew before any OpenGWAS-dependent work", remaining
    if remaining <= URGENT_DAYS:
        return "URGENT_RENEWAL", "renew immediately; expiry is within 48 hours", remaining
    if remaining <= RENEW_SOON_DAYS:
        return "RENEW_SOON", "renew before any multi-day or queued OpenGWAS-dependent work", remaining
    return "VALID", "token is outside the renewal-soon window", remaining


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now(dt.timezone.utc)
    env_jwt = os.environ.get("OPENGWAS_JWT", "")
    dotenv_jwt = dotenv_value("OPENGWAS_JWT")
    jwt = dotenv_jwt or env_jwt
    expiry, decode_status = decode_expiry(jwt) if jwt else (None, "missing")
    status, action, days_remaining = classify(expiry, now, jwt)
    env_shadowed = bool(env_jwt and dotenv_jwt and env_jwt != dotenv_jwt)

    row = {
        "synthetic": False,
        "purpose": "OpenGWAS token-expiry operations sentinel; no biological claim",
        "checked_at_utc": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "source_used": ".env" if dotenv_jwt else "environment",
        "dotenv_present": bool(dotenv_jwt),
        "env_present": bool(env_jwt),
        "env_shadowed_by_dotenv": env_shadowed,
        "jwt_length": len(jwt),
        "jwt_segments": len(jwt.split(".")) if jwt else 0,
        "decode_status": decode_status,
        "expiry_utc": expiry.strftime("%Y-%m-%d %H:%M:%S UTC") if expiry else "unknown",
        "days_remaining": round(days_remaining, 3) if days_remaining is not None else "",
        "renewal_status": status,
        "required_action": action,
        "post_only_checker": "scripts/check_opengwas_access.py",
    }
    table = pd.DataFrame([row])
    table_path = outdir / "opengwas_token_expiry_sentinel.tsv"
    table.to_csv(table_path, sep="\t", index=False)
    summary = {**row, "table": rel(table_path)}
    (outdir / "opengwas_token_expiry_sentinel_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if status in {"VALID", "RENEW_SOON"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
