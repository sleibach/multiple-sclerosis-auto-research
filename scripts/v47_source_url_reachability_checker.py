#!/usr/bin/env python3
"""Check source URL reachability for V47 external records.

This checker records transport-level URL status only. HTTP success, redirect,
or failure is not evidence for or against any external claim. The output exists
to flag stale/dead source locators and to help maintain provenance.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import socket
import ssl
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_ROOT = "knowledge_external"
DEFAULT_OUTDIR = ROOT / EXTERNAL_ROOT / "catalogs/indexes"
DEFAULT_SYNTHETIC_OUTDIR = ROOT / "analysis/v47_source_url_reachability_checker"
NOT_GROUNDED = "NOT_PROJECT_GROUNDED"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Check real external source URLs")
    check.add_argument("--root", type=Path, default=ROOT)
    check.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    check.add_argument("--timeout", type=float, default=8.0)
    check.add_argument("--max-records", type=int, default=0, help="Optional cap for debugging; 0 means all")
    synth = sub.add_parser("synthetic-check", help="Run synthetic status-classification fixtures without network")
    synth.add_argument("--outdir", type=Path, default=DEFAULT_SYNTHETIC_OUTDIR)
    synth.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def candidate_json_paths(root: Path) -> list[Path]:
    base = root / EXTERNAL_ROOT
    if not base.exists():
        return []
    return sorted(
        path
        for path in base.rglob("*.json")
        if not path.name.endswith(".schema.json")
        and "indexes" not in path.parts
        and "synthesis" not in path.parts
    )


def load_record(path: Path) -> dict[str, Any] | None:
    data = json.loads(path.read_text())
    if not isinstance(data, dict) or "epistemic_class" not in data:
        return None
    return data


def source_field(source: Any, field: str) -> str:
    if not isinstance(source, dict):
        return ""
    return str(source.get(field, "")).strip()


def source_url(data: dict[str, Any]) -> str:
    return source_field(data.get("source"), "url")


def classify_http_status(code: int, final_url: str, original_url: str) -> str:
    if 200 <= code <= 299:
        if final_url and final_url != original_url:
            return "reachable_redirected_2xx"
        return "reachable_2xx"
    if 300 <= code <= 399:
        return "redirect_status"
    if 400 <= code <= 499:
        return "client_error"
    if 500 <= code <= 599:
        return "server_error"
    return "unexpected_http_status"


def check_url(url: str, timeout: float) -> tuple[str, str, str, int | str]:
    if not url:
        return "missing_url", "", "No HTTP URL present in record source.", ""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return "non_http_locator", url, "Non-HTTP locator; reachability not checked.", ""
    headers = {
        "User-Agent": "curl/8.7.1 ms-auto-research-v47-source-checker/1.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    for method in ["HEAD", "GET"]:
        try:
            req = Request(url, method=method, headers=headers)
            with urlopen(req, timeout=timeout) as response:  # noqa: S310 - source reachability only.
                final_url = response.geturl()
                code = int(response.getcode())
                return classify_http_status(code, final_url, url), final_url, f"{method} completed; transport status only.", code
        except HTTPError as exc:
            code = int(exc.code)
            if method == "HEAD":
                continue
            return classify_http_status(code, url, url), url, f"{method} returned HTTPError; transport status only.", code
        except (URLError, TimeoutError, socket.timeout, ssl.SSLError, OSError) as exc:
            if method == "HEAD":
                continue
            return "network_error", "", f"{type(exc).__name__}: {exc}", ""
    return "network_error", "", "No transport response.", ""


def row_for_record(root: Path, path: Path, data: dict[str, Any], timeout: float) -> dict[str, object]:
    url = source_url(data)
    status, final_url, detail, http_code = check_url(url, timeout)
    return {
        "record_id": str(data.get("record_id", "")),
        "record_type": str(data.get("record_type", "")),
        "resource_name": str(data.get("resource_name", "")),
        "epistemic_class": str(data.get("epistemic_class", "")),
        "relationship_to_project_findings": str(data.get("relationship_to_project_findings", "")),
        "not_project_grounded_marker": str(data.get("not_project_grounded_marker", "")),
        "source_label": source_field(data.get("source"), "label"),
        "source_url": url,
        "final_url": final_url,
        "http_code": http_code,
        "reachability_status": status,
        "detail": detail,
        "interpretation_boundary": "transport_status_only_not_claim_validation",
        "path": rel(root, path),
    }


def write_markdown(path: Path, rows: list[dict[str, object]], counts: list[dict[str, object]], summary: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# External Source URL Reachability",
        "",
        "Status: transport metadata only. HTTP reachability does not validate any external claim.",
        "",
        f"- records checked: `{summary['n_records']}`",
        f"- reachable 2xx or redirected 2xx: `{summary['n_reachable_or_redirected_2xx']}`",
        f"- non-2xx/network/missing statuses: `{summary['n_non_success_status']}`",
        f"- overall status: `{summary['overall_status']}`",
        "",
        "## Status Counts",
        "",
        "| reachability status | count |",
        "|---|---:|",
    ]
    for row in counts:
        lines.append(f"| `{row['reachability_status']}` | {row['count']} |")
    lines.extend(
        [
            "",
            "## Records",
            "",
            "| record | class | source | status | marker | boundary |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in rows:
        record_label = row["resource_name"] or row["record_id"]
        lines.append(
            f"| {record_label} | `{row['epistemic_class']}` | {row['source_url']} | "
            f"`{row['reachability_status']}` | `{row['not_project_grounded_marker']}` | "
            f"`{row['interpretation_boundary']}` |"
        )
    path.write_text("\n".join(lines) + "\n")


def check_real(root: Path, outdir: Path, timeout: float, max_records: int) -> dict[str, object]:
    outdir = outdir if outdir.is_absolute() else root / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    paths = [path for path in candidate_json_paths(root) if load_record(path) is not None]
    if max_records:
        paths = paths[:max_records]
    rows = [row_for_record(root, path, load_record(path) or {}, timeout) for path in paths]
    counter = Counter(str(row["reachability_status"]) for row in rows)
    counts = [{"reachability_status": status, "count": count} for status, count in sorted(counter.items())]
    n_success = sum(counter.get(status, 0) for status in ["reachable_2xx", "reachable_redirected_2xx"])
    n_missing_marker = sum(1 for row in rows if row["not_project_grounded_marker"] != NOT_GROUNDED)
    n_non_success = len(rows) - n_success
    summary = {
        "synthetic": False,
        "purpose": "V47 source URL reachability check; transport metadata only, no claim validation",
        "n_records": len(rows),
        "n_reachable_or_redirected_2xx": n_success,
        "n_non_success_status": n_non_success,
        "n_missing_not_grounded_marker": n_missing_marker,
        "overall_status": "PASS" if n_missing_marker == 0 else "FAIL",
        "warning": "Non-success statuses are maintenance warnings, not evidence about external claims.",
        "table": rel(root, outdir / "external_source_url_reachability.tsv") if root == ROOT else str(outdir / "external_source_url_reachability.tsv"),
    }
    fields = [
        "record_id",
        "record_type",
        "resource_name",
        "epistemic_class",
        "relationship_to_project_findings",
        "not_project_grounded_marker",
        "source_label",
        "source_url",
        "final_url",
        "http_code",
        "reachability_status",
        "detail",
        "interpretation_boundary",
        "path",
    ]
    write_tsv(outdir / "external_source_url_reachability.tsv", rows, fields)
    write_tsv(outdir / "external_source_url_reachability_counts.tsv", counts, ["reachability_status", "count"])
    write_markdown(outdir / "EXTERNAL_SOURCE_URL_REACHABILITY.md", rows, counts, summary)
    (outdir / "external_source_url_reachability_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def build_synthetic_root(outdir: Path) -> Path:
    root = outdir / "synthetic_root"
    if root.exists():
        shutil.rmtree(root)
    records = root / EXTERNAL_ROOT / "catalogs/resources"
    records.mkdir(parents=True, exist_ok=True)
    base = {
        "record_type": "external_resource_catalog",
        "claim": "Synthetic reachability resource.",
        "epistemic_class": "external-unverifiable",
        "date_accessed": "2026-06-13",
        "relationship_to_project_findings": "orthogonal",
        "not_project_grounded_marker": NOT_GROUNDED,
        "why_unverifiable": "Synthetic fixture.",
        "future_grounding_route": "Synthetic route.",
        "project_use": "Synthetic reachability test.",
        "access_tier": "open",
    }
    (records / "synthetic.json").write_text(
        json.dumps(
            {
                **base,
                "record_id": "SYNTH_REACHABLE",
                "resource_name": "Synthetic Reachable",
                "source": {"label": "Synthetic", "url": "https://example.invalid/reachable"},
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    return root


def synthetic_check(outdir: Path, fail_on_error: bool) -> int:
    outdir = outdir if outdir.is_absolute() else ROOT / outdir
    outdir.mkdir(parents=True, exist_ok=True)
    checks = {
        "classify_200": classify_http_status(200, "https://example.invalid/a", "https://example.invalid/a") == "reachable_2xx",
        "classify_redirected_200": classify_http_status(200, "https://example.invalid/b", "https://example.invalid/a") == "reachable_redirected_2xx",
        "classify_404": classify_http_status(404, "https://example.invalid/a", "https://example.invalid/a") == "client_error",
        "classify_503": classify_http_status(503, "https://example.invalid/a", "https://example.invalid/a") == "server_error",
        "missing_url_is_boundary_status": check_url("", timeout=0.1)[0] == "missing_url",
    }
    root = build_synthetic_root(outdir)
    rows = []
    for path in candidate_json_paths(root):
        data = load_record(path)
        if data:
            source = data.get("source")
            rows.append(
                {
                    "record_id": str(data.get("record_id", "")),
                    "record_type": str(data.get("record_type", "")),
                    "resource_name": str(data.get("resource_name", "")),
                    "epistemic_class": str(data.get("epistemic_class", "")),
                    "relationship_to_project_findings": str(data.get("relationship_to_project_findings", "")),
                    "not_project_grounded_marker": str(data.get("not_project_grounded_marker", "")),
                    "source_label": source_field(source, "label"),
                    "source_url": source_field(source, "url"),
                    "final_url": "",
                    "http_code": "",
                    "reachability_status": "synthetic_not_contacted",
                    "detail": "Synthetic fixture; network not contacted.",
                    "interpretation_boundary": "transport_status_only_not_claim_validation",
                    "path": rel(root, path),
                }
            )
    write_tsv(outdir / "synthetic_reachability_rows.tsv", rows, [
        "record_id",
        "record_type",
        "resource_name",
        "epistemic_class",
        "relationship_to_project_findings",
        "not_project_grounded_marker",
        "source_label",
        "source_url",
        "final_url",
        "http_code",
        "reachability_status",
        "detail",
        "interpretation_boundary",
        "path",
    ])
    check_rows = [{"check": key, "status": "PASS" if value else "FAIL"} for key, value in checks.items()]
    write_tsv(outdir / "synthetic_source_url_reachability_checks.tsv", check_rows, ["check", "status"])
    summary = {
        "synthetic": True,
        "purpose": "V47 source URL reachability synthetic fixture; no network claim validation",
        "n_checks": len(check_rows),
        "n_fail": sum(1 for row in check_rows if row["status"] != "PASS"),
        "overall_status": "PASS" if all(checks.values()) else "FAIL",
    }
    (outdir / "synthetic_source_url_reachability_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["overall_status"] == "PASS" or not fail_on_error else 2


def main() -> int:
    args = parse_args()
    if args.command == "check":
        summary = check_real(args.root.resolve(), args.outdir, args.timeout, args.max_records)
        return 0 if summary["overall_status"] == "PASS" else 2
    if args.command == "synthetic-check":
        return synthetic_check(args.outdir, args.fail_on_error)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
