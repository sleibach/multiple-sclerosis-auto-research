#!/usr/bin/env python3
"""Smoke-check V50 non-OpenGWAS public routes.

The checks are transport/schema probes only. They do not import datasets, do
not call OpenGWAS, and do not create biological evidence.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis" / "v50_non_opengwas_route_checks"


@dataclass(frozen=True)
class Route:
    route_id: str
    service: str
    method: str
    url: str
    params: dict[str, str] | None
    body: dict[str, Any] | None
    timeout_seconds: int
    expected_status: int = 200


ROUTES = [
    Route(
        "gwas_catalog_association_by_rsid",
        "NHGRI-EBI GWAS Catalog REST",
        "GET",
        "https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId",
        {"rsId": "rs1250550", "projection": "associationBySnp"},
        None,
        20,
    ),
    Route(
        "europe_pmc_search",
        "Europe PMC REST",
        "GET",
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search",
        {"query": "multiple sclerosis", "format": "json", "pageSize": "1"},
        None,
        20,
    ),
    Route(
        "ncbi_eutils_geo_search",
        "NCBI E-utilities GDS",
        "GET",
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
        {"db": "gds", "term": "multiple sclerosis", "retmode": "json", "retmax": "1"},
        None,
        20,
    ),
    Route(
        "biostudies_search",
        "EBI BioStudies API",
        "GET",
        "https://www.ebi.ac.uk/biostudies/api/v1/search",
        {"query": "multiple sclerosis", "pageSize": "1"},
        None,
        20,
    ),
    Route(
        "clinicaltrials_v2_search",
        "ClinicalTrials.gov API v2",
        "GET",
        "https://clinicaltrials.gov/api/v2/studies",
        {"query.term": "multiple sclerosis", "pageSize": "1"},
        None,
        20,
    ),
    Route(
        "crossref_works_search",
        "Crossref REST",
        "GET",
        "https://api.crossref.org/works",
        {"query": "multiple sclerosis", "rows": "1"},
        None,
        20,
    ),
    Route(
        "opentargets_graphql_search",
        "Open Targets Platform GraphQL",
        "POST",
        "https://api.platform.opentargets.org/api/v4/graphql",
        None,
        {"query": '{ search(queryString: "multiple sclerosis") { hits { id name entity } } }'},
        20,
    ),
    Route(
        "ena_portal_study_search",
        "ENA Portal API",
        "GET",
        "https://www.ebi.ac.uk/ena/portal/api/search",
        {
            "result": "study",
            "query": 'study_title="multiple sclerosis"',
            "fields": "study_accession,study_title",
            "limit": "1",
            "format": "json",
        },
        None,
        20,
    ),
]


def build_request(route: Route) -> urllib.request.Request:
    url = route.url
    data: bytes | None = None
    headers = {
        "User-Agent": "ms-auto-research-v50-route-checker/1.0",
        "Accept": "application/json,text/plain,*/*",
    }
    if route.params:
        url = f"{url}?{urllib.parse.urlencode(route.params)}"
    if route.method == "POST":
        data = json.dumps(route.body or {}).encode("utf-8")
        headers["Content-Type"] = "application/json"
    return urllib.request.Request(url, data=data, headers=headers, method=route.method)


def check_route(route: Route) -> dict[str, Any]:
    started = time.time()
    request = build_request(route)
    try:
        with urllib.request.urlopen(request, timeout=route.timeout_seconds) as response:
            payload = response.read(2048)
            status = int(response.status)
            elapsed_ms = int((time.time() - started) * 1000)
            return {
                "route_id": route.route_id,
                "service": route.service,
                "method": route.method,
                "url": request.full_url,
                "http_status": status,
                "elapsed_ms": elapsed_ms,
                "bytes_sampled": len(payload),
                "status": "PASS" if status == route.expected_status else "FAIL",
                "error": "",
                "open_gwas_used": False,
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(512).decode("utf-8", errors="replace")
        elapsed_ms = int((time.time() - started) * 1000)
        return {
            "route_id": route.route_id,
            "service": route.service,
            "method": route.method,
            "url": request.full_url,
            "http_status": int(exc.code),
            "elapsed_ms": elapsed_ms,
            "bytes_sampled": len(body),
            "status": "PASS" if int(exc.code) == route.expected_status else "FAIL",
            "error": body.replace("\n", " ")[:300],
            "open_gwas_used": False,
        }
    except Exception as exc:  # noqa: BLE001 - CLI checker should report all failures.
        elapsed_ms = int((time.time() - started) * 1000)
        return {
            "route_id": route.route_id,
            "service": route.service,
            "method": route.method,
            "url": request.full_url,
            "http_status": 0,
            "elapsed_ms": elapsed_ms,
            "bytes_sampled": 0,
            "status": "FAIL",
            "error": repr(exc)[:300],
            "open_gwas_used": False,
        }


def write_outputs(rows: list[dict[str, Any]], outdir: Path) -> dict[str, Any]:
    outdir.mkdir(parents=True, exist_ok=True)
    tsv = outdir / "route_check_results.tsv"
    summary_path = outdir / "summary.json"
    fields = [
        "route_id",
        "service",
        "method",
        "http_status",
        "elapsed_ms",
        "bytes_sampled",
        "status",
        "open_gwas_used",
        "url",
        "error",
    ]
    with tsv.open("w", encoding="utf-8") as handle:
        handle.write("\t".join(fields) + "\n")
        for row in rows:
            handle.write(
                "\t".join(str(row.get(field, "")).replace("\t", " ").replace("\n", " ") for field in fields)
                + "\n"
            )
    n_fail = sum(1 for row in rows if row["status"] != "PASS")
    summary = {
        "purpose": "V50 non-OpenGWAS public route checker; transport/schema only; no biological claim",
        "synthetic": False,
        "checked_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "n_routes": len(rows),
        "n_fail": n_fail,
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "open_gwas_used": False,
        "results": str(tsv.relative_to(ROOT)),
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check"])
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    rows = [check_route(route) for route in ROUTES]
    summary = write_outputs(rows, args.outdir)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and summary["n_fail"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
