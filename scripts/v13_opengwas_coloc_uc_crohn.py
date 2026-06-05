#!/usr/bin/env python3
"""V13 OpenGWAS-backed MS/UC/Crohn locus overlap and coloc pass.

Scope:
- Load OPENGWAS_JWT from `.env`.
- Use OpenGWAS API v4 POST endpoints only.
- Fetch top hits and regional association statistics.
- Run a first-pass single-causal-variant approximate coloc ABF analysis.

This is not a replacement for full LDSC/HDL or SuSiE-coloc. It is the first
executable colocalization layer needed to upgrade V12 genetics cells beyond
target-overlap and published rg summaries.
"""

from __future__ import annotations

import csv
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "v13_genetics_coloc"
RAW = OUT / "raw"
API = "https://api.opengwas.io/api"

STUDIES = {
    "MS": "ieu-b-18",
    "UC": "ieu-a-32",
    "Crohn": "ieu-a-30",
}

COMPARATORS = ["UC", "Crohn"]
WINDOW_BP = 500_000
P_TOP = 5e-8
P_SHARED = 1e-5
P1 = 1e-4
P2 = 1e-4
P12 = 1e-5
# coloc.abf uses trait-type-dependent priors. This fixed W is a conservative
# first pass for log-OR binary traits; later V13 work should sensitivity-test W.
W = 0.04


def load_dotenv() -> None:
    env = ROOT / ".env"
    if not env.exists():
        return
    for raw in env.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def api_post(path: str, payload: dict[str, Any], jwt: str, cache_name: str) -> Any:
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / cache_name
    if cache.exists():
        return json.loads(cache.read_text())

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{API}{path}",
        data=data,
        headers={"Authorization": f"Bearer {jwt}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        body = resp.read()
    cache.write_bytes(body)
    time.sleep(0.1)
    return json.loads(body.decode("utf-8"))


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


@dataclass(frozen=True)
class Region:
    comparator: str
    chr: str
    start: int
    end: int
    ms_lead: str
    comparator_lead: str
    ms_lead_p: float
    comparator_lead_p: float

    @property
    def key(self) -> str:
        return f"{self.comparator}_chr{self.chr}_{self.start}_{self.end}_{self.ms_lead}_{self.comparator_lead}"

    @property
    def query(self) -> str:
        return f"{self.chr}:{self.start}-{self.end}"


def fnum(x: Any) -> float | None:
    try:
        if x in ("", None):
            return None
        v = float(x)
        if math.isnan(v):
            return None
        return v
    except Exception:
        return None


def top_hits(label: str, jwt: str) -> list[dict[str, Any]]:
    rows = api_post(
        "/tophits",
        {"id": [STUDIES[label]], "pval": P_TOP, "clump": 1},
        jwt,
        f"tophits_{label}_{STUDIES[label]}.json",
    )
    return rows if isinstance(rows, list) else []


def make_regions(all_hits: dict[str, list[dict[str, Any]]]) -> list[Region]:
    regions: list[Region] = []
    ms_hits = all_hits["MS"]
    for comp in COMPARATORS:
        for mh in ms_hits:
            mch = str(mh.get("chr"))
            mpos = fnum(mh.get("position"))
            mp = fnum(mh.get("p"))
            if mpos is None or mp is None:
                continue
            for ch in all_hits[comp]:
                cch = str(ch.get("chr"))
                cpos = fnum(ch.get("position"))
                cp = fnum(ch.get("p"))
                if cpos is None or cp is None or cch != mch:
                    continue
                if abs(int(mpos) - int(cpos)) <= WINDOW_BP:
                    start = max(1, min(int(mpos), int(cpos)) - WINDOW_BP)
                    end = max(int(mpos), int(cpos)) + WINDOW_BP
                    regions.append(
                        Region(
                            comparator=comp,
                            chr=mch,
                            start=start,
                            end=end,
                            ms_lead=str(mh.get("rsid")),
                            comparator_lead=str(ch.get("rsid")),
                            ms_lead_p=mp,
                            comparator_lead_p=cp,
                        )
                    )
    # De-duplicate highly overlapping windows by comparator/chr/start/end/leads.
    unique: dict[str, Region] = {r.key: r for r in regions}
    return sorted(unique.values(), key=lambda r: (r.comparator, r.chr, r.start, r.end))[:50]


def region_assoc(region: Region, label: str, jwt: str) -> list[dict[str, Any]]:
    rows = api_post(
        "/associations",
        {"id": [STUDIES[label]], "variant": [region.query], "proxies": 0},
        jwt,
        f"assoc_{label}_{STUDIES[label]}_{region.chr}_{region.start}_{region.end}.json",
    )
    return rows if isinstance(rows, list) else []


def logsumexp(vals: list[float]) -> float:
    if not vals:
        return float("-inf")
    m = max(vals)
    if not math.isfinite(m):
        return m
    return m + math.log(sum(math.exp(v - m) for v in vals))


def logdiffexp(a: float, b: float) -> float:
    if not math.isfinite(a):
        return float("-inf")
    if b >= a:
        return float("-inf")
    return a + math.log1p(-math.exp(b - a))


def log_abf(beta: float, se: float) -> float:
    v = se * se
    if v <= 0:
        return float("-inf")
    z2 = (beta / se) ** 2
    r = W / (v + W)
    return 0.5 * (math.log1p(-r) + r * z2)


def coloc_abf(rows1: list[dict[str, Any]], rows2: list[dict[str, Any]]) -> dict[str, Any]:
    by1 = {str(r.get("rsid")): r for r in rows1 if r.get("rsid")}
    by2 = {str(r.get("rsid")): r for r in rows2 if r.get("rsid")}
    shared = sorted(set(by1) & set(by2))
    records: list[dict[str, Any]] = []
    l1s: list[float] = []
    l2s: list[float] = []
    l12s: list[float] = []
    for rsid in shared:
        r1, r2 = by1[rsid], by2[rsid]
        b1, se1 = fnum(r1.get("beta")), fnum(r1.get("se"))
        b2, se2 = fnum(r2.get("beta")), fnum(r2.get("se"))
        p1, p2 = fnum(r1.get("p")), fnum(r2.get("p"))
        if b1 is None or se1 is None or b2 is None or se2 is None or p1 is None or p2 is None:
            continue
        l1 = log_abf(b1, se1)
        l2 = log_abf(b2, se2)
        if not math.isfinite(l1) or not math.isfinite(l2):
            continue
        l1s.append(l1)
        l2s.append(l2)
        l12s.append(l1 + l2)
        records.append(
            {
                "rsid": rsid,
                "chr": r1.get("chr"),
                "position": r1.get("position"),
                "beta1": b1,
                "se1": se1,
                "p1": p1,
                "ea1": r1.get("ea"),
                "nea1": r1.get("nea"),
                "beta2": b2,
                "se2": se2,
                "p2": p2,
                "ea2": r2.get("ea"),
                "nea2": r2.get("nea"),
                "lABF1": l1,
                "lABF2": l2,
                "lABF12": l1 + l2,
            }
        )

    lsum1 = logsumexp(l1s)
    lsum2 = logsumexp(l2s)
    lsum12 = logsumexp(l12s)
    lh0 = 0.0
    lh1 = math.log(P1) + lsum1
    lh2 = math.log(P2) + lsum2
    # Sum over distinct causal SNP pairs.
    lh3 = math.log(P1) + math.log(P2) + logdiffexp(lsum1 + lsum2, lsum12)
    lh4 = math.log(P12) + lsum12
    denom = logsumexp([lh0, lh1, lh2, lh3, lh4])
    pp = {
        "PP.H0": math.exp(lh0 - denom),
        "PP.H1": math.exp(lh1 - denom),
        "PP.H2": math.exp(lh2 - denom),
        "PP.H3": math.exp(lh3 - denom) if math.isfinite(lh3) else 0.0,
        "PP.H4": math.exp(lh4 - denom),
    }
    top = max(records, key=lambda r: r["lABF12"], default={})
    return {
        "n_shared_snps": len(records),
        "top_shared_snp": top.get("rsid", ""),
        "top_shared_position": top.get("position", ""),
        "top_shared_p1": top.get("p1", ""),
        "top_shared_p2": top.get("p2", ""),
        **pp,
        "records": records,
    }


def main() -> int:
    load_dotenv()
    jwt = os.environ.get("OPENGWAS_JWT")
    if not jwt:
        print("OPENGWAS_JWT missing after loading .env", file=sys.stderr)
        return 2

    OUT.mkdir(parents=True, exist_ok=True)
    all_hits = {label: top_hits(label, jwt) for label in STUDIES}

    hit_rows: list[dict[str, Any]] = []
    for label, rows in all_hits.items():
        for row in rows:
            hit_rows.append({"label": label, **row})
    write_tsv(
        OUT / "opengwas_tophits.tsv",
        hit_rows,
        ["label", "id", "trait", "chr", "position", "rsid", "ea", "nea", "eaf", "beta", "se", "p", "n"],
    )

    regions = make_regions(all_hits)
    region_rows = [
        {
            "comparator": r.comparator,
            "chr": r.chr,
            "start": r.start,
            "end": r.end,
            "query": r.query,
            "ms_lead": r.ms_lead,
            "comparator_lead": r.comparator_lead,
            "ms_lead_p": r.ms_lead_p,
            "comparator_lead_p": r.comparator_lead_p,
        }
        for r in regions
    ]
    write_tsv(
        OUT / "shared_tophit_regions.tsv",
        region_rows,
        ["comparator", "chr", "start", "end", "query", "ms_lead", "comparator_lead", "ms_lead_p", "comparator_lead_p"],
    )

    coloc_rows: list[dict[str, Any]] = []
    snp_rows: list[dict[str, Any]] = []
    for r in regions:
        ms = region_assoc(r, "MS", jwt)
        comp = region_assoc(r, r.comparator, jwt)
        coloc = coloc_abf(ms, comp)
        call = "insufficient_shared_snps"
        if coloc["n_shared_snps"] >= 50:
            if coloc["PP.H4"] >= 0.8:
                call = "shared_causal_variant_supported"
            elif coloc["PP.H3"] >= 0.8:
                call = "distinct_causal_variants_supported"
            elif coloc["PP.H4"] >= 0.5:
                call = "suggestive_shared_causal_variant"
            else:
                call = "unresolved_coloc"
        row = {
            "comparator": r.comparator,
            "region": r.query,
            "chr": r.chr,
            "start": r.start,
            "end": r.end,
            "ms_lead": r.ms_lead,
            "comparator_lead": r.comparator_lead,
            "ms_lead_p": r.ms_lead_p,
            "comparator_lead_p": r.comparator_lead_p,
            "n_ms_region_rows": len(ms),
            "n_comparator_region_rows": len(comp),
            "call": call,
            **{k: v for k, v in coloc.items() if k != "records"},
        }
        coloc_rows.append(row)
        for rec in coloc["records"]:
            snp_rows.append({"comparator": r.comparator, "region": r.query, **rec})

    write_tsv(
        OUT / "coloc_region_summary.tsv",
        coloc_rows,
        [
            "comparator",
            "region",
            "chr",
            "start",
            "end",
            "ms_lead",
            "comparator_lead",
            "ms_lead_p",
            "comparator_lead_p",
            "n_ms_region_rows",
            "n_comparator_region_rows",
            "n_shared_snps",
            "top_shared_snp",
            "top_shared_position",
            "top_shared_p1",
            "top_shared_p2",
            "PP.H0",
            "PP.H1",
            "PP.H2",
            "PP.H3",
            "PP.H4",
            "call",
        ],
    )
    write_tsv(
        OUT / "coloc_snp_abf.tsv",
        snp_rows,
        [
            "comparator",
            "region",
            "rsid",
            "chr",
            "position",
            "beta1",
            "se1",
            "p1",
            "ea1",
            "nea1",
            "beta2",
            "se2",
            "p2",
            "ea2",
            "nea2",
            "lABF1",
            "lABF2",
            "lABF12",
        ],
    )

    report = [
        "# V13 OpenGWAS UC/Crohn Colocalization Pass",
        "",
        "Status: executable first-pass coloc layer using OpenGWAS API v4 POST calls.",
        "",
        "## Inputs",
        "",
        f"- MS: `{STUDIES['MS']}`.",
        f"- UC: `{STUDIES['UC']}`.",
        f"- Crohn: `{STUDIES['Crohn']}`.",
        f"- Top-hit threshold: `{P_TOP}`.",
        f"- Shared-region window: `+/-{WINDOW_BP}` bp around overlapping top hits.",
        "",
        "## Method Caveat",
        "",
        "This is single-causal-variant approximate coloc ABF. Dense autoimmune loci,",
        "especially MHC, require multi-signal SuSiE-coloc before a final robust-grade",
        "claim. PP.H4 and PP.H3 are separated so locus overlap is not mistaken for",
        "shared causality.",
        "",
        "## Region Summary",
        "",
    ]
    if coloc_rows:
        report.append("| comparator | region | shared SNPs | PP.H3 | PP.H4 | call |")
        report.append("| --- | --- | ---: | ---: | ---: | --- |")
        for row in sorted(coloc_rows, key=lambda x: (x["comparator"], -float(x["PP.H4"]))):
            report.append(
                f"| {row['comparator']} | {row['region']} | {row['n_shared_snps']} | "
                f"{float(row['PP.H3']):.4g} | {float(row['PP.H4']):.4g} | {row['call']} |"
            )
    else:
        report.append("No shared top-hit regions were identified.")
    report.extend(
        [
            "",
            "## Files",
            "",
            "- `opengwas_tophits.tsv`",
            "- `shared_tophit_regions.tsv`",
            "- `coloc_region_summary.tsv`",
            "- `coloc_snp_abf.tsv`",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps({"out": str(OUT), "regions": len(regions), "coloc_rows": len(coloc_rows)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
