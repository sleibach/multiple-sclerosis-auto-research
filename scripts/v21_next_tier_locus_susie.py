#!/usr/bin/env python3
"""Run bounded SuSiE-coloc for V21 next-tier loci.

Uses cached V13 OpenGWAS regional summary statistics and POST /ld/matrix for
EUR LD. This is locus-level vetting, not genome-wide LDSC.
"""

from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "analysis" / "v13_genetics_coloc" / "raw"
OUT = ROOT / "analysis" / "v21_next_tier_loci"
LD_RAW = OUT / "raw_ld"
API = "https://api.opengwas.io/api"
MAX_SNPS_ATTEMPTS = [500, 300, 200, 100]

LOCUS_SPECS = [
    {
        "name": "MS_Crohn_chr14_68710199_69753364",
        "comparator": "Crohn",
        "path1": RAW / "assoc_MS_ieu-b-18_14_68710199_69753364.json",
        "path2": RAW / "assoc_Crohn_ieu-a-30_14_68710199_69753364.json",
    },
    {
        "name": "MS_UC_chr2_60689469_61742410",
        "comparator": "UC",
        "path1": RAW / "assoc_MS_ieu-b-18_2_60689469_61742410.json",
        "path2": RAW / "assoc_UC_ieu-a-32_2_60689469_61742410.json",
    },
]


def load_dotenv() -> None:
    env = ROOT / ".env"
    if not env.exists():
        return
    for raw in env.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_assoc(path: Path) -> dict[str, dict[str, Any]]:
    rows = json.loads(path.read_text())
    out: dict[str, dict[str, Any]] = {}
    for r in rows:
        try:
            beta = float(r["beta"])
            se = float(r["se"])
            p = float(r["p"])
            n = int(r["n"])
        except Exception:
            continue
        rsid = str(r.get("rsid") or "")
        ea = str(r.get("ea") or "").upper()
        nea = str(r.get("nea") or "").upper()
        if not rsid or not ea or not nea or se <= 0 or p <= 0:
            continue
        out[rsid] = {
            "beta": beta,
            "se": se,
            "p": max(p, 1e-300),
            "ea": ea,
            "nea": nea,
            "n": n,
            "position": r.get("position"),
        }
    return out


def ld_matrix(rsids: list[str], name: str, max_snps: int, jwt: str) -> dict[str, Any]:
    LD_RAW.mkdir(parents=True, exist_ok=True)
    cache = LD_RAW / f"{name}_EUR_ld_{max_snps}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    payload = {"rsid": rsids[:max_snps], "pop": "EUR"}
    req = urllib.request.Request(
        f"{API}/ld/matrix",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {jwt}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=240) as resp:
        body = resp.read().decode()
    cache.write_text(body)
    time.sleep(0.1)
    return json.loads(body)


def parse_ld_snp(label: str) -> tuple[str, str, str]:
    parts = label.split("_")
    return parts[0], parts[-2].upper(), parts[-1].upper()


def aligned_beta(row: dict[str, Any], ld_a1: str, ld_a2: str) -> float | None:
    if row["ea"] == ld_a1 and row["nea"] == ld_a2:
        return row["beta"]
    if row["ea"] == ld_a2 and row["nea"] == ld_a1:
        return -row["beta"]
    return None


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def run_locus(spec: dict[str, Any], jwt: str) -> dict[str, Any]:
    a = load_assoc(spec["path1"])
    b = load_assoc(spec["path2"])
    shared = sorted(set(a) & set(b), key=lambda rs: min(a[rs]["p"], b[rs]["p"]))
    last_error = ""
    for max_snps in MAX_SNPS_ATTEMPTS:
        try:
            ld = ld_matrix(shared, spec["name"], max_snps, jwt)
            snplist = ld.get("snplist") or []
            matrix = ld.get("matrix") or []
            keep_idx: list[int] = []
            records: list[dict[str, Any]] = []
            for i, label in enumerate(snplist):
                rsid, ld_a1, ld_a2 = parse_ld_snp(label)
                if rsid not in a or rsid not in b:
                    continue
                beta1 = aligned_beta(a[rsid], ld_a1, ld_a2)
                beta2 = aligned_beta(b[rsid], ld_a1, ld_a2)
                if beta1 is None or beta2 is None:
                    continue
                keep_idx.append(i)
                records.append(
                    {
                        "snp": rsid,
                        "ld_label": label,
                        "ld_a1": ld_a1,
                        "ld_a2": ld_a2,
                        "beta1": beta1,
                        "se1": a[rsid]["se"],
                        "varbeta1": a[rsid]["se"] ** 2,
                        "z1": beta1 / a[rsid]["se"],
                        "p1": a[rsid]["p"],
                        "n1": a[rsid]["n"],
                        "beta2": beta2,
                        "se2": b[rsid]["se"],
                        "varbeta2": b[rsid]["se"] ** 2,
                        "z2": beta2 / b[rsid]["se"],
                        "p2": b[rsid]["p"],
                        "n2": b[rsid]["n"],
                    }
                )
            if len(records) < 50:
                raise RuntimeError(f"only {len(records)} allele-aligned SNPs")
            sub = [[float(matrix[i][j]) for j in keep_idx] for i in keep_idx]
            for i in range(len(sub)):
                sub[i][i] = 1.0
            locus_dir = OUT / spec["name"]
            locus_dir.mkdir(parents=True, exist_ok=True)
            fields = [
                "snp",
                "ld_label",
                "ld_a1",
                "ld_a2",
                "beta1",
                "se1",
                "varbeta1",
                "z1",
                "p1",
                "n1",
                "beta2",
                "se2",
                "varbeta2",
                "z2",
                "p2",
                "n2",
            ]
            write_tsv(locus_dir / "aligned_sumstats.tsv", records, fields)
            with (locus_dir / "ld_matrix.tsv").open("w", newline="") as fh:
                writer = csv.writer(fh, delimiter="\t")
                writer.writerow(["snp", *[r["snp"] for r in records]])
                for r, vals in zip(records, sub, strict=True):
                    writer.writerow([r["snp"], *vals])
            return {
                "name": spec["name"],
                "status": "prepared",
                "shared_snps_available": len(shared),
                "max_snps_attempt": max_snps,
                "ld_snps_returned": len(snplist),
                "allele_aligned_snps": len(records),
                "n1": records[0]["n1"],
                "n2": records[0]["n2"],
                "error": "",
            }
        except Exception as exc:
            last_error = repr(exc)
    return {
        "name": spec["name"],
        "status": "failed_prepare",
        "shared_snps_available": len(shared),
        "max_snps_attempt": "",
        "ld_snps_returned": "",
        "allele_aligned_snps": "",
        "n1": "",
        "n2": "",
        "error": last_error,
    }


def run_r_coloc() -> None:
    script = OUT / "run_coloc_susie.R"
    script.write_text(
        r'''
library(coloc)
library(susieR)
out_root <- "analysis/v21_next_tier_loci"
summary_rows <- list()
for (locus in list.dirs(out_root, recursive=FALSE, full.names=FALSE)) {
  if (locus == "raw_ld") next
  ss_path <- file.path(out_root, locus, "aligned_sumstats.tsv")
  ld_path <- file.path(out_root, locus, "ld_matrix.tsv")
  if (!file.exists(ss_path) || !file.exists(ld_path)) next
  ss <- read.delim(ss_path, stringsAsFactors=FALSE)
  ld_raw <- read.delim(ld_path, check.names=FALSE, stringsAsFactors=FALSE)
  snps <- ld_raw[[1]]
  LD <- as.matrix(ld_raw[, -1])
  rownames(LD) <- snps
  colnames(LD) <- colnames(ld_raw)[-1]
  ss <- ss[match(snps, ss$snp), ]
  stopifnot(all(ss$snp == snps))
  d1 <- list(beta=ss$beta1, varbeta=ss$varbeta1, LD=LD, snp=ss$snp, N=ss$n1[1], type="cc")
  d2 <- list(beta=ss$beta2, varbeta=ss$varbeta2, LD=LD, snp=ss$snp, N=ss$n2[1], type="cc")
  set.seed(20260606)
  res <- tryCatch(
    coloc.susie(d1, d2, susie.args=list(L=10, coverage=0.95, min_abs_corr=0.1, max_iter=1000)),
    error=function(e) e
  )
  if (inherits(res, "error")) {
    writeLines(conditionMessage(res), file.path(out_root, locus, "coloc_susie_error.txt"))
    summary_rows[[length(summary_rows)+1]] <- data.frame(
      locus=locus, status="error", nsnps=nrow(ss), n_pairwise=NA,
      max_PP.H3=NA, max_PP.H4=NA, error=conditionMessage(res)
    )
  } else if (is.data.frame(res$summary)) {
    write.table(res$summary, file.path(out_root, locus, "coloc_susie_summary.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
    write.table(res$results, file.path(out_root, locus, "coloc_susie_results.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
    summary_rows[[length(summary_rows)+1]] <- data.frame(
      locus=locus, status="ok", nsnps=nrow(ss), n_pairwise=nrow(res$summary),
      max_PP.H3=max(res$summary$PP.H3.abf, na.rm=TRUE),
      max_PP.H4=max(res$summary$PP.H4.abf, na.rm=TRUE),
      error=""
    )
  } else {
    summary_rows[[length(summary_rows)+1]] <- data.frame(
      locus=locus, status="no_cs", nsnps=nrow(ss), n_pairwise=NA,
      max_PP.H3=NA, max_PP.H4=NA, error="coloc.susie returned no summary"
    )
  }
}
if (length(summary_rows) > 0) {
  rollup <- do.call(rbind, summary_rows)
  write.table(rollup, file.path(out_root, "susie_coloc_rollup.tsv"), sep="\t", quote=FALSE, row.names=FALSE)
}
'''.lstrip()
    )
    subprocess.run(["Rscript", str(script)], cwd=ROOT, check=True)


def main() -> int:
    load_dotenv()
    jwt = os.environ.get("OPENGWAS_JWT")
    if not jwt:
        raise SystemExit("OPENGWAS_JWT missing")
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [run_locus(spec, jwt) for spec in LOCUS_SPECS]
    write_tsv(
        OUT / "preparation_rollup.tsv",
        rows,
        ["name", "status", "shared_snps_available", "max_snps_attempt", "ld_snps_returned", "allele_aligned_snps", "n1", "n2", "error"],
    )
    if any(r["status"] != "prepared" for r in rows):
        print(json.dumps(rows, indent=2))
        return 1
    run_r_coloc()
    print((OUT / "susie_coloc_rollup.tsv").read_text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
