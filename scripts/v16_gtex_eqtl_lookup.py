#!/usr/bin/env python3
"""GTEx API eQTL lookup for V16 live loci.

This script uses the reachable GTEx Portal API. It does not claim to be a full
raw summary-statistics colocalization layer: `/association/singleTissueEqtl`
returns significant eQTL records. Positive records are useful for allele-level
direction checks; missing records are endpoint-level negatives, not proof of no
eQTL effect.
"""

from __future__ import annotations

import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v16_eqtl_workup"
RAW = OUT / "raw_api"
API = "https://gtexportal.org/api/v2"

GENES = {
    "GPR25": "GPR25",
    "C1orf106": "C1orf106",
    "KIF21B": "KIF21B",
    "CACNA1S": "CACNA1S",
    "ZMIZ1": "ZMIZ1",
    "PPIF": "PPIF",
    "PTGER4": "PTGER4",
}

LEADS = {
    "GPR25_chr1_MS_UC": {
        "genes": ["GPR25", "C1orf106", "KIF21B", "CACNA1S"],
        "snps": [
            "rs12132349",
            "rs59655222",
            "rs35730213",
            "rs12132298",
            "rs41299637",
            "rs12131796",
            "rs7554511",
            "rs55838263",
            "rs296520",
            "rs10800746",
            "rs7522462",
        ],
    },
    "ZMIZ1_chr10_MS_Crohn": {
        "genes": ["ZMIZ1", "PPIF"],
        "snps": ["rs1250563", "rs1250566", "rs1250573", "rs1892497"],
    },
    "PTGER4_chr5_MS_UC": {
        "genes": ["PTGER4"],
        "snps": ["rs350054", "rs62356511", "rs1445002"],
    },
}

TISSUES = [
    "Whole_Blood",
    "Colon_Sigmoid",
    "Colon_Transverse",
    "Small_Intestine_Terminal_Ileum",
    "Brain_Cortex",
    "Brain_Frontal_Cortex_BA9",
    "Brain_Cerebellum",
    "Spleen",
]

TARGETED_QUERIES = {
    # chr1: prioritize the two variants with existing OpenTargets QTL-coloc
    # evidence plus the top shared H4 SNP.
    "GPR25_chr1_MS_UC": {
        "genes": ["GPR25", "C1orf106", "KIF21B", "CACNA1S"],
        "snps": ["rs12132349", "rs55838263", "rs7554511"],
        "tissues": ["Whole_Blood", "Colon_Transverse", "Brain_Cortex", "Spleen"],
    },
    # chr10: the four-SNP shared credible-set intersection.
    "ZMIZ1_chr10_MS_Crohn": {
        "genes": ["ZMIZ1", "PPIF"],
        "snps": ["rs1250563", "rs1250566", "rs1250573", "rs1892497"],
        "tissues": ["Whole_Blood", "Colon_Transverse", "Brain_Cortex", "Spleen"],
    },
    # chr5: one shared-signal SNP and the two distinct-signal SNPs from V15.
    "PTGER4_chr5_MS_UC": {
        "genes": ["PTGER4"],
        "snps": ["rs350054", "rs62356511", "rs1445002"],
        "tissues": ["Whole_Blood", "Colon_Transverse", "Brain_Cortex", "Spleen"],
    },
}


def fetch_json(path: str, params: dict[str, Any], cache_name: str) -> dict[str, Any]:
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / cache_name
    if cache.exists():
        return json.loads(cache.read_text())
    url = f"{API}{path}?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={"User-Agent": "ms-auto-research-v16/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        body = response.read().decode("utf-8")
    cache.write_text(body)
    time.sleep(0.05)
    return json.loads(body)


def first_data(payload: dict[str, Any]) -> dict[str, Any] | None:
    data = payload.get("data")
    if isinstance(data, list) and data:
        return data[0]
    return None


def gene_record(symbol: str) -> dict[str, Any] | None:
    payload = fetch_json(
        "/reference/gene",
        {"geneId": symbol, "datasetId": "gtex_v8"},
        f"gtex_gene_{symbol}.json",
    )
    return first_data(payload)


def variant_record(rsid: str) -> dict[str, Any] | None:
    payload = fetch_json(
        "/dataset/variant",
        {"snpId": rsid, "datasetId": "gtex_v8"},
        f"gtex_variant_snpId_{rsid}.json",
    )
    return first_data(payload)


def eqtl_records(gencode_id: str, variant_id: str, tissue: str) -> list[dict[str, Any]]:
    payload = fetch_json(
        "/association/singleTissueEqtl",
        {
            "gencodeId": gencode_id,
            "variantId": variant_id,
            "tissueSiteDetailId": tissue,
            "datasetId": "gtex_v8",
            "itemsPerPage": 100000,
        },
        f"gtex_eqtl_{gencode_id}_{variant_id}_{tissue}.json".replace("/", "_"),
    )
    data = payload.get("data")
    return data if isinstance(data, list) else []


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    gene_rows = []
    variant_rows = []
    eqtl_rows = []

    gene_map: dict[str, dict[str, Any]] = {}
    variant_map: dict[str, dict[str, Any]] = {}

    for gene in GENES:
        rec = gene_record(gene)
        if rec:
            gene_map[gene] = rec
            gene_rows.append(
                {
                    "gene": gene,
                    "gencodeId": rec.get("gencodeId", ""),
                    "chromosome": rec.get("chromosome", ""),
                    "start": rec.get("start", ""),
                    "end": rec.get("end", ""),
                    "strand": rec.get("strand", ""),
                    "description": rec.get("description", ""),
                }
            )

    for spec in LEADS.values():
        for rsid in spec["snps"]:
            if rsid in variant_map:
                continue
            rec = variant_record(rsid)
            if rec:
                variant_map[rsid] = rec
                variant_rows.append(
                    {
                        "rsid": rsid,
                        "variantId": rec.get("variantId", ""),
                        "b37VariantId": rec.get("b37VariantId", ""),
                        "chromosome": rec.get("chromosome", ""),
                        "pos_b38": rec.get("pos", ""),
                        "ref": rec.get("ref", ""),
                        "alt": rec.get("alt", ""),
                    }
                )

    for lead, spec in LEADS.items():
        for gene in spec["genes"]:
            grec = gene_map.get(gene)
            if not grec:
                continue
            gid = str(grec["gencodeId"])
            for rsid in spec["snps"]:
                vrec = variant_map.get(rsid)
                if not vrec:
                    continue
                vid = str(vrec["variantId"])
                for tissue in TISSUES:
                    records = eqtl_records(gid, vid, tissue)
                    if not records:
                        eqtl_rows.append(
                            {
                                "lead": lead,
                                "gene": gene,
                                "gencodeId": gid,
                                "rsid": rsid,
                                "variantId": vid,
                                "b37VariantId": vrec.get("b37VariantId", ""),
                                "tissue": tissue,
                                "has_significant_eqtl": "False",
                            }
                        )
                        continue
                    for rec in records:
                        row = {
                            "lead": lead,
                            "gene": gene,
                            "gencodeId": gid,
                            "rsid": rsid,
                            "variantId": vid,
                            "b37VariantId": vrec.get("b37VariantId", ""),
                            "tissue": tissue,
                            "has_significant_eqtl": "True",
                        }
                        for key, value in rec.items():
                            if key not in row:
                                row[key] = value
                        eqtl_rows.append(row)

    write_rows(OUT / "gtex_gene_map.tsv", gene_rows)
    write_rows(OUT / "gtex_variant_map.tsv", variant_rows)
    write_rows(OUT / "gtex_significant_eqtl_lookup.tsv", eqtl_rows)
    print(f"genes={len(gene_rows)} variants={len(variant_rows)} eqtl_rows={len(eqtl_rows)}")


def targeted() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    gene_map = {gene: gene_record(gene) for gene in GENES}
    variant_map: dict[str, dict[str, Any] | None] = {}
    rows = []
    for lead, spec in TARGETED_QUERIES.items():
        for rsid in spec["snps"]:
            if rsid not in variant_map:
                variant_map[rsid] = variant_record(rsid)
        for gene in spec["genes"]:
            grec = gene_map.get(gene)
            if not grec:
                continue
            gid = str(grec["gencodeId"])
            for rsid in spec["snps"]:
                vrec = variant_map.get(rsid)
                if not vrec:
                    continue
                vid = str(vrec["variantId"])
                for tissue in spec["tissues"]:
                    records = eqtl_records(gid, vid, tissue)
                    if not records:
                        rows.append(
                            {
                                "lead": lead,
                                "gene": gene,
                                "gencodeId": gid,
                                "rsid": rsid,
                                "variantId": vid,
                                "b37VariantId": vrec.get("b37VariantId", ""),
                                "tissue": tissue,
                                "has_significant_eqtl": "False",
                            }
                        )
                        continue
                    for rec in records:
                        row = {
                            "lead": lead,
                            "gene": gene,
                            "gencodeId": gid,
                            "rsid": rsid,
                            "variantId": vid,
                            "b37VariantId": vrec.get("b37VariantId", ""),
                            "tissue": tissue,
                            "has_significant_eqtl": "True",
                        }
                        for key, value in rec.items():
                            if key not in row:
                                row[key] = value
                        rows.append(row)
    write_rows(OUT / "gtex_targeted_significant_eqtl_lookup.tsv", rows)
    print(f"targeted_eqtl_rows={len(rows)}")


def write_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--targeted":
        targeted()
    else:
        main()
