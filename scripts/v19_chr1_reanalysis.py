#!/usr/bin/env python3
"""V19 chr1 GPR25/KIF21B re-analysis.

This script intentionally does not fetch new data. It verifies the V18-acquired
files, intersects the dense eQTL Catalogue KIF21B extract with the saved V14
MS/UC chr1 disease sumstats, aligns QTL alleles to the disease LD-effect allele,
and writes coloc-ready inputs. If R coloc is installed, it runs coloc.abf for
MS-vs-KIF21B-eQTL and UC-vs-KIF21B-eQTL.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v19_chr1_druggability"
SHA_FILE = ROOT / "analysis" / "v18_source_triage" / "acquired_sha256.tsv"
DISEASE = ROOT / "analysis" / "v14_susie_coloc" / "MS_UC_chr1_200375242_201375897" / "aligned_sumstats.tsv"
QTD = ROOT / "data" / "raw" / "v18_source_triage" / "eqtl_catalogue" / "QTD000021_chr1_200000000_202000000_targets.tsv"
V18_HITS = ROOT / "analysis" / "v18_source_triage" / "target_gene_eqtl_hits.tsv"
V18_DIST = ROOT / "analysis" / "v18_source_triage" / "v18_hits_vs_v17_credible_set.tsv"
V17_SHARED = ROOT / "analysis" / "v17_gpr25_mechanism" / "eqtlgen_full_chr1_candidate_rows_overlapping_shared_credible_set.tsv"
V17_COLOC = ROOT / "analysis" / "v17_gpr25_mechanism" / "eqtl_coloc_chr1" / "competitor_eqtl_susie_coloc_rollup.tsv"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def f(x: str | None) -> float | None:
    try:
        if x is None or x == "" or x == "NA":
            return None
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return None
        return v
    except Exception:
        return None


def verify_v18() -> list[dict[str, object]]:
    rows = []
    for raw in SHA_FILE.read_text().splitlines():
        if not raw.strip():
            continue
        expected, rel = raw.split(None, 1)
        path = ROOT / rel
        exists = path.exists()
        actual = sha256(path) if exists else ""
        rows.append(
            {
                "path": rel,
                "exists": exists,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "matches": exists and expected == actual,
            }
        )
    return rows


def summarize_v18_hits() -> dict[str, object]:
    hits = read_tsv(V18_HITS)
    dist = read_tsv(V18_DIST)
    by_gene: dict[str, int] = {}
    by_source: dict[str, int] = {}
    distances = []
    exact = 0
    for r in hits:
        by_gene[r["gene_symbol"]] = by_gene.get(r["gene_symbol"], 0) + 1
        by_source[r["source"]] = by_source.get(r["source"], 0) + 1
    for r in dist:
        if r["exact_credible_position"] == "True":
            exact += 1
        d = f(r.get("distance_bp"))
        if d is not None:
            distances.append(d)
    return {
        "target_hits_total": len(hits),
        "target_hits_by_gene": by_gene,
        "target_hits_by_source": by_source,
        "exact_credible_matches": exact,
        "min_distance_to_v17_credible_bp": min(distances) if distances else None,
        "median_distance_to_v17_credible_bp": sorted(distances)[len(distances) // 2] if distances else None,
    }


def load_disease() -> dict[str, dict[str, str]]:
    return {r["snp"]: r for r in read_tsv(DISEASE)}


def align_eqtl_to_disease() -> list[dict[str, object]]:
    disease = load_disease()
    rows = []
    for r in read_tsv(QTD):
        if r.get("gene_symbol") != "KIF21B":
            continue
        rsid = r.get("rsid") or ""
        if rsid not in disease:
            continue
        beta = f(r.get("beta"))
        se = f(r.get("se"))
        p = f(r.get("pvalue"))
        if beta is None or se is None or se <= 0 or p is None:
            continue
        d = disease[rsid]
        ref, alt = r.get("ref"), r.get("alt")
        ld_a1, ld_a2 = d["ld_a1"], d["ld_a2"]
        if alt == ld_a1 and ref == ld_a2:
            aligned_beta = beta
            qtl_effect_allele = alt
            alignment = "alt_to_ld_a1"
        elif ref == ld_a1 and alt == ld_a2:
            aligned_beta = -beta
            qtl_effect_allele = ref
            alignment = "ref_to_ld_a1_beta_flipped"
        else:
            continue
        rows.append(
            {
                "snp": rsid,
                "position": r["position"],
                "ld_a1": ld_a1,
                "ld_a2": ld_a2,
                "qtl_ref": ref,
                "qtl_alt": alt,
                "qtl_effect_allele": qtl_effect_allele,
                "alignment": alignment,
                "qtl_beta_aligned_to_ld_a1": aligned_beta,
                "qtl_se": se,
                "qtl_varbeta": se * se,
                "qtl_p": p,
                "qtl_maf": r.get("maf", ""),
                "qtl_n_approx": int(round((f(r.get("an")) or 0) / 2)) if f(r.get("an")) else "",
                "ms_beta": d["beta1"],
                "ms_varbeta": d["varbeta1"],
                "ms_p": d["p1"],
                "ms_n": d["n1"],
                "uc_beta": d["beta2"],
                "uc_varbeta": d["varbeta2"],
                "uc_p": d["p2"],
                "uc_n": d["n2"],
            }
        )
    return rows


def run_coloc(aligned_path: Path) -> None:
    rscript = OUT / "run_kif21b_qtd_coloc.R"
    rscript.write_text(
        """
suppressPackageStartupMessages(library(coloc))
args <- commandArgs(trailingOnly=TRUE)
inp <- args[[1]]
out <- args[[2]]
d <- read.delim(inp, stringsAsFactors=FALSE)
run_one <- function(prefix) {
  ds1 <- list(beta=d[[paste0(prefix, "_beta")]],
              varbeta=d[[paste0(prefix, "_varbeta")]],
              snp=d$snp,
              type="cc",
              N=as.numeric(d[[paste0(prefix, "_n")]][1]))
  ds2 <- list(beta=d$qtl_beta_aligned_to_ld_a1,
              varbeta=d$qtl_varbeta,
              MAF=as.numeric(d$qtl_maf),
              snp=d$snp,
              type="quant",
              N=max(as.numeric(d$qtl_n_approx), na.rm=TRUE))
  res <- coloc.abf(ds1, ds2)
  s <- as.data.frame(t(res$summary))
  s$comparison <- paste0(toupper(prefix), "_vs_QTD000021_KIF21B")
  s$nsnps_input <- nrow(d)
  s
}
summary <- rbind(run_one("ms"), run_one("uc"))
write.table(summary, file=out, sep="\\t", quote=FALSE, row.names=FALSE)
""".strip()
        + "\n"
    )
    subprocess.run(["Rscript", str(rscript), str(aligned_path), str(OUT / "kif21b_qtd_coloc_abf_summary.tsv")], check=True)


def summarize_v17_shared() -> list[dict[str, object]]:
    rows = read_tsv(V17_SHARED)
    out: dict[str, dict[str, object]] = {}
    for r in rows:
        g = r["GeneSymbol"]
        o = out.setdefault(g, {"gene": g, "overlap_snps": 0, "min_p": 1.0, "max_abs_z": 0.0})
        o["overlap_snps"] = int(o["overlap_snps"]) + 1
        p = f(r["Pvalue"])
        z = abs(f(r["Zscore"]) or 0)
        if p is not None:
            o["min_p"] = min(float(o["min_p"]), p)
        o["max_abs_z"] = max(float(o["max_abs_z"]), z)
    return list(out.values())


def direction_summary(aligned: list[dict[str, object]]) -> dict[str, object]:
    shared = {r["SNP"] for r in read_tsv(V17_SHARED)}
    out: dict[str, object] = {}
    for label, rows in {
        "all_intersecting_snps": aligned,
        "exact_v17_shared_credible_snps": [r for r in aligned if r["snp"] in shared],
    }.items():
        block: dict[str, object] = {"n": len(rows)}
        for trait in ("ms", "uc"):
            total = 0
            lowers = 0
            raises = 0
            for r in rows:
                disease_beta = float(r[f"{trait}_beta"])
                qtl_beta = float(r["qtl_beta_aligned_to_ld_a1"])
                if disease_beta == 0 or qtl_beta == 0:
                    continue
                total += 1
                if disease_beta * qtl_beta < 0:
                    lowers += 1
                elif disease_beta * qtl_beta > 0:
                    raises += 1
            block[f"{trait}_risk_allele_lowers_kif21b_expression"] = lowers
            block[f"{trait}_risk_allele_raises_kif21b_expression"] = raises
            block[f"{trait}_direction_total"] = total
        block["top_qtl_snps"] = sorted(
            [
                {
                    "snp": r["snp"],
                    "position": r["position"],
                    "qtl_p": r["qtl_p"],
                    "qtl_beta_aligned_to_ld_a1": r["qtl_beta_aligned_to_ld_a1"],
                    "ms_beta": r["ms_beta"],
                    "uc_beta": r["uc_beta"],
                }
                for r in rows
            ],
            key=lambda r: float(r["qtl_p"]),
        )[:10]
        out[label] = block
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    checksum_rows = verify_v18()
    write_tsv(
        OUT / "v18_checksum_verification.tsv",
        checksum_rows,
        ["path", "exists", "expected_sha256", "actual_sha256", "matches"],
    )

    aligned = align_eqtl_to_disease()
    write_tsv(
        OUT / "kif21b_qtd000021_aligned_to_ms_uc.tsv",
        aligned,
        [
            "snp",
            "position",
            "ld_a1",
            "ld_a2",
            "qtl_ref",
            "qtl_alt",
            "qtl_effect_allele",
            "alignment",
            "qtl_beta_aligned_to_ld_a1",
            "qtl_se",
            "qtl_varbeta",
            "qtl_p",
            "qtl_maf",
            "qtl_n_approx",
            "ms_beta",
            "ms_varbeta",
            "ms_p",
            "ms_n",
            "uc_beta",
            "uc_varbeta",
            "uc_p",
            "uc_n",
        ],
    )
    if len(aligned) >= 50:
        run_coloc(OUT / "kif21b_qtd000021_aligned_to_ms_uc.tsv")

    rollup = {
        "v18_checksums_all_match": all(bool(r["matches"]) for r in checksum_rows),
        "v18_checksum_files_checked": len(checksum_rows),
        "qtd_kif21b_rows_total": sum(1 for r in read_tsv(QTD) if r.get("gene_symbol") == "KIF21B"),
        "qtd_kif21b_rows_intersecting_v14_disease_snps": len(aligned),
        "qtd_kif21b_effect_direction": direction_summary(aligned),
        "v18_hits": summarize_v18_hits(),
        "v17_shared_block_by_gene": summarize_v17_shared(),
    }
    coloc_path = OUT / "kif21b_qtd_coloc_abf_summary.tsv"
    if coloc_path.exists():
        rollup["kif21b_qtd_coloc_abf"] = read_tsv(coloc_path)
    rollup["v17_bounded_eqtl_susie_competitor_rollup"] = read_tsv(V17_COLOC)
    (OUT / "v19_chr1_reanalysis_summary.json").write_text(json.dumps(rollup, indent=2, sort_keys=True))
    print(json.dumps(rollup, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
