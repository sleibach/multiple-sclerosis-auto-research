#!/usr/bin/env python3
"""Smoke-test V18 acquired data sources for GPR25/KIF21B/CXCL17 queryability."""

from __future__ import annotations

import csv
import json
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "raw" / "v18_source_triage"
OUT = ROOT / "analysis" / "v18_source_triage"
TARGETS = {
    "GPR25": "ENSG00000170128",
    "KIF21B": "ENSG00000116852",
    "CXCL17": "ENSG00000189377",
}


def smoke_onek1k() -> list[dict[str, str]]:
    rows = []
    zip_path = BASE / "onek1k" / "OneK1K_TensorQTL_top_eQTL_summary.zip"
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if not name.endswith(".csv") or "/._" in name:
                continue
            cell = name.split("/")[-1].replace("OneK1K_", "").split(
                ".sig_cis_qtl_pairs"
            )[0]
            chrom = name.rsplit("chr", 1)[-1].replace(".csv", "")
            with zf.open(name) as fh:
                header = fh.readline().decode("utf-8", "replace").strip().split("\t")
                for line in fh:
                    parts = line.decode("utf-8", "replace").rstrip("\n").split("\t")
                    if not parts or parts[0] not in TARGETS:
                        continue
                    rows.append(
                        {
                            "source": "OneK1K_top_eqtl",
                            "cell": cell,
                            "chrom": chrom,
                            "gene_symbol": parts[0],
                            "fields": json.dumps(dict(zip(header, parts))),
                        }
                    )
    return rows


def smoke_dice_vcf() -> list[dict[str, str]]:
    rows = []
    for path in sorted((BASE / "dice").glob("*.significant.vcf")):
        cell = path.name.replace(".significant.vcf", "")
        with path.open(errors="replace") as fh:
            for line in fh:
                if line.startswith("#") or not any(g in line for g in TARGETS):
                    continue
                fields = line.rstrip("\n").split("\t")
                info = {}
                for item in fields[7].split(";"):
                    if "=" in item:
                        key, value = item.split("=", 1)
                        info[key] = value
                rows.append(
                    {
                        "source": "DICE_significant_eqtl",
                        "cell": cell,
                        "chrom": fields[0],
                        "gene_symbol": info.get("GeneSymbol", ""),
                        "fields": json.dumps(
                            {
                                "variant": f"{fields[0]}:{fields[1]}:{fields[3]}:{fields[4]}",
                                **info,
                            }
                        ),
                    }
                )
    return rows


def dice_mean_expression() -> list[dict[str, str]]:
    rows = []
    id_to_symbol = {ensembl: symbol for symbol, ensembl in TARGETS.items()}
    with (BASE / "dice" / "mean_tpm_merged.csv").open(newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            symbol = id_to_symbol.get(row["gene"])
            if not symbol:
                continue
            rows.append({"gene_symbol": symbol, "ensembl_id": row["gene"], **row})
    return rows


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    eqtl_rows = smoke_onek1k() + smoke_dice_vcf()
    write_tsv(OUT / "target_gene_eqtl_hits.tsv", eqtl_rows)
    write_tsv(OUT / "dice_mean_expression_target_genes.tsv", dice_mean_expression())
    print("target_gene_eqtl_hits", len(eqtl_rows), Counter((r["source"], r["gene_symbol"]) for r in eqtl_rows))


if __name__ == "__main__":
    main()
