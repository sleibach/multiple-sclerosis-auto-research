#!/usr/bin/env python3
"""Small PubMed prior-art query record for V2 exhaustion."""

from __future__ import annotations

import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v2/results"

QUERIES = {
    "ACSL1_MS": '(ACSL1 OR "acyl-CoA synthetase 1") AND ("multiple sclerosis" OR EAE)',
    "NAMPT_MS": '(NAMPT OR visfatin OR FK866 OR APO866) AND ("multiple sclerosis" OR EAE)',
    "NAMPT_AUTOIMMUNE": "(NAMPT OR visfatin OR FK866 OR APO866) AND (rheumatoid OR lupus OR psoriasis OR Crohn OR ulcerative OR autoimmune)",
    "FK866_EAE": "FK866 experimental autoimmune encephalomyelitis",
}


def fetch(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": "ms-auto-research/0.1"})
    with urlopen(req, timeout=45) as resp:
        return resp.read()


def main() -> None:
    OUT.mkdir(exist_ok=True)
    rows = []
    summaries = []
    for name, query in QUERIES.items():
        data = json.loads(
            fetch(
                "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
                f"db=pubmed&retmode=json&retmax=10&term={quote(query)}"
            )
        )
        result = data["esearchresult"]
        ids = result.get("idlist", [])
        rows.append(
            {
                "query_name": name,
                "query": query,
                "count": result.get("count"),
                "first_pmids": ",".join(ids),
            }
        )
        if ids:
            root = ET.fromstring(
                fetch(
                    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"
                    f"db=pubmed&retmode=xml&id={','.join(ids)}"
                )
            )
            for doc in root.findall("DocSum"):
                title = ""
                pubdate = ""
                for item in doc.findall("Item"):
                    if item.attrib.get("Name") == "Title":
                        title = item.text or ""
                    if item.attrib.get("Name") == "PubDate":
                        pubdate = item.text or ""
                summaries.append(
                    {
                        "query_name": name,
                        "pmid": doc.findtext("Id"),
                        "pubdate": pubdate,
                        "title": title,
                    }
                )
    with (OUT / "prior_art_pubmed_counts.tsv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["query_name", "query", "count", "first_pmids"], delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    with (OUT / "prior_art_pubmed_summaries.tsv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["query_name", "pmid", "pubdate", "title"], delimiter="\t")
        writer.writeheader()
        writer.writerows(summaries)
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
