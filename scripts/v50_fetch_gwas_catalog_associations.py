#!/usr/bin/env python3
"""Fetch GWAS Catalog association rows by rsid without using OpenGWAS.

This script is a V50 routing utility. It reads the public NHGRI-EBI GWAS
Catalog REST API and writes flattened metadata rows suitable for later
allele-harmonization checks. The output is external API metadata only; it is
not project-grounded evidence and it does not perform strand harmonization,
LD-aware fine mapping, or target promotion.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


API = "https://www.ebi.ac.uk/gwas/rest/api/associations/search/findByRsId"
DEFAULT_RSIDS = ["rs1250550", "rs4613763", "rs7522462"]
FIELDNAMES = [
    "rsid",
    "traits",
    "risk_alleles",
    "or_per_copy",
    "beta",
    "beta_direction",
    "pvalue",
    "risk_frequency",
    "author_reported_genes",
    "chromosome_locations",
    "source_url",
]


def api_url(rsid: str) -> str:
    query = urllib.parse.urlencode({"rsId": rsid, "projection": "associationBySnp"})
    return f"{API}?{query}"


def request_json(url: str, timeout: int) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"Accept": "application/json"}, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def compact(values: list[str]) -> str:
    clean = [v.strip() for v in values if v and v.strip() and v.strip() != "None"]
    return ";".join(dict.fromkeys(clean))


def association_rows(rsid: str, payload: dict[str, Any], source_url: str) -> list[dict[str, str]]:
    associations = payload.get("_embedded", {}).get("associations", [])
    rows: list[dict[str, str]] = []
    for assoc in associations:
        traits = compact([str(t.get("trait", "")) for t in assoc.get("efoTraits", [])])

        risk_alleles: list[str] = []
        risk_frequencies: list[str] = []
        author_genes: list[str] = []
        for locus in assoc.get("loci", []):
            for allele in locus.get("strongestRiskAlleles", []):
                risk_alleles.append(str(allele.get("riskAlleleName") or f"{rsid}-?"))
                risk_frequencies.append(str(allele.get("riskFrequency") or ""))
            for gene in locus.get("authorReportedGenes", []):
                author_genes.append(str(gene.get("geneName") or ""))

        if not risk_frequencies and assoc.get("riskFrequency") is not None:
            risk_frequencies.append(str(assoc.get("riskFrequency")))
        elif assoc.get("riskFrequency") is not None:
            risk_frequencies.append(str(assoc.get("riskFrequency")))

        locations: list[str] = []
        for snp in assoc.get("snps", []):
            for loc in snp.get("locations", []):
                chrom = loc.get("chromosomeName")
                pos = loc.get("chromosomePosition")
                region = (loc.get("region") or {}).get("name")
                bits = [str(x) for x in [chrom, pos, region] if x not in [None, ""]]
                if bits:
                    locations.append(":".join(bits))

        rows.append(
            {
                "rsid": rsid,
                "traits": traits or "NR",
                "risk_alleles": compact(risk_alleles) or f"{rsid}-?",
                "or_per_copy": "" if assoc.get("orPerCopyNum") is None else str(assoc.get("orPerCopyNum")),
                "beta": "" if assoc.get("betaNum") is None else str(assoc.get("betaNum")),
                "beta_direction": "" if assoc.get("betaDirection") is None else str(assoc.get("betaDirection")),
                "pvalue": "" if assoc.get("pvalue") is None else str(assoc.get("pvalue")),
                "risk_frequency": compact(risk_frequencies) or "NR",
                "author_reported_genes": compact(author_genes) or "NR",
                "chromosome_locations": compact(locations) or "NR",
                "source_url": source_url,
            }
        )
    return rows


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_summary(path: Path, rows: list[dict[str, str]], rsids: list[str], errors: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "purpose": "V50 GWAS Catalog rsid routing table; external API extraction only; no OpenGWAS use",
        "opengwas_used": False,
        "rsids": rsids,
        "n_rows": len(rows),
        "rows_by_rsid": {rsid: sum(1 for row in rows if row["rsid"] == rsid) for rsid in rsids},
        "errors": errors,
        "synthetic": False,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rsid", action="append", dest="rsids", help="rsid to fetch; repeatable")
    parser.add_argument(
        "--output",
        default="analysis/v50_gwas_catalog_fetcher/gwas_catalog_associations.tsv",
        help="Output TSV path",
    )
    parser.add_argument(
        "--summary",
        default="analysis/v50_gwas_catalog_fetcher/gwas_catalog_associations_summary.json",
        help="Output JSON summary path",
    )
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout in seconds")
    parser.add_argument("--sleep", type=float, default=0.0, help="Delay between rsid calls")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    rsids = args.rsids or DEFAULT_RSIDS
    rows: list[dict[str, str]] = []
    errors: dict[str, str] = {}

    for i, rsid in enumerate(rsids):
        url = api_url(rsid)
        try:
            payload = request_json(url, args.timeout)
            rows.extend(association_rows(rsid, payload, url))
        except urllib.error.HTTPError as exc:
            errors[rsid] = f"HTTP {exc.code}"
        except Exception as exc:
            errors[rsid] = f"{type(exc).__name__}: {exc}"
        if args.sleep and i < len(rsids) - 1:
            time.sleep(args.sleep)

    write_tsv(Path(args.output), rows)
    write_summary(Path(args.summary), rows, rsids, errors)

    print(
        json.dumps(
            {
                "output": args.output,
                "summary": args.summary,
                "n_rsids": len(rsids),
                "n_rows": len(rows),
                "n_errors": len(errors),
                "opengwas_used": False,
            },
            sort_keys=True,
        )
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
