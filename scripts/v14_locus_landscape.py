#!/usr/bin/env python3
"""V14 landscape and sensitivity workup for V13 shared loci.

This script does not claim robust genetics grade. It adds the next feasible
robustness layer in the current environment:
- prior/effect-size sensitivity for V13 approximate coloc;
- candidate-region landscape ranking;
- joins to existing local target-resolution, QTL-coloc, cell-state, and
  druggability evidence.

Blocked layers are recorded in the report: LDSC/HDL binaries and R susieR/coloc
are not installed in this environment.
"""

from __future__ import annotations

import csv
import json
import math
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
IN = ROOT / "analysis" / "v13_genetics_coloc"
OUT = ROOT / "analysis" / "v14_locus_landscape"
OUT.mkdir(parents=True, exist_ok=True)

P1 = 1e-4
P2 = 1e-4
P12_VALUES = [1e-6, 1e-5, 1e-4]
W_VALUES = [0.01, 0.04, 0.09]

TARGET_SUMMARY = ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
CELLSTATE = ROOT / "phases/v3/results" / "wave166_same_gene_genetics_cellstate_overlap" / "same_gene_genetics_cellstate_rank.tsv"
EXTERNAL = ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv"


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open() as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def fnum(v: Any, default: float = 0.0) -> float:
    try:
        if v in ("", None):
            return default
        x = float(v)
        if math.isnan(x):
            return default
        return x
    except Exception:
        return default


def logsumexp(vals: list[float]) -> float:
    if not vals:
        return float("-inf")
    m = max(vals)
    if not math.isfinite(m):
        return m
    return m + math.log(sum(math.exp(v - m) for v in vals))


def logdiffexp(a: float, b: float) -> float:
    if b >= a:
        return float("-inf")
    return a + math.log1p(-math.exp(b - a))


def log_abf(beta: float, se: float, w: float) -> float:
    v = se * se
    if v <= 0:
        return float("-inf")
    z2 = (beta / se) ** 2
    r = w / (v + w)
    return 0.5 * (math.log1p(-r) + r * z2)


def coloc_for_records(records: list[dict[str, str]], p12: float, w: float) -> dict[str, float]:
    l1s, l2s, l12s = [], [], []
    for r in records:
        b1, se1, b2, se2 = fnum(r["beta1"]), fnum(r["se1"]), fnum(r["beta2"]), fnum(r["se2"])
        l1 = log_abf(b1, se1, w)
        l2 = log_abf(b2, se2, w)
        if not math.isfinite(l1) or not math.isfinite(l2):
            continue
        l1s.append(l1)
        l2s.append(l2)
        l12s.append(l1 + l2)
    lsum1 = logsumexp(l1s)
    lsum2 = logsumexp(l2s)
    lsum12 = logsumexp(l12s)
    lh0 = 0.0
    lh1 = math.log(P1) + lsum1
    lh2 = math.log(P2) + lsum2
    lh3 = math.log(P1) + math.log(P2) + logdiffexp(lsum1 + lsum2, lsum12)
    lh4 = math.log(p12) + lsum12
    denom = logsumexp([lh0, lh1, lh2, lh3, lh4])
    return {
        "PP.H3": math.exp(lh3 - denom) if math.isfinite(lh3) else 0.0,
        "PP.H4": math.exp(lh4 - denom),
    }


def index_by_gene(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {r.get("gene", ""): r for r in rows if r.get("gene")}


def main() -> int:
    summary = read_tsv(IN / "coloc_region_summary_annotated.tsv")
    snps = read_tsv(IN / "coloc_snp_abf.tsv")
    by_region: dict[tuple[str, str], list[dict[str, str]]] = {}
    for r in snps:
        by_region.setdefault((r["comparator"], r["region"]), []).append(r)

    sens_rows: list[dict[str, Any]] = []
    for row in summary:
        records = by_region.get((row["comparator"], row["region"]), [])
        vals_h4, vals_h3 = [], []
        for p12 in P12_VALUES:
            for w in W_VALUES:
                res = coloc_for_records(records, p12, w)
                vals_h4.append(res["PP.H4"])
                vals_h3.append(res["PP.H3"])
                sens_rows.append(
                    {
                        "comparator": row["comparator"],
                        "region": row["region"],
                        "p12": p12,
                        "W": w,
                        "PP.H3": res["PP.H3"],
                        "PP.H4": res["PP.H4"],
                        "n_shared_snps": row["n_shared_snps"],
                    }
                )

    write_tsv(
        OUT / "coloc_prior_sensitivity.tsv",
        sens_rows,
        ["comparator", "region", "p12", "W", "PP.H3", "PP.H4", "n_shared_snps"],
    )

    target = index_by_gene(read_tsv(TARGET_SUMMARY))
    cell = index_by_gene(read_tsv(CELLSTATE))
    ext = index_by_gene(read_tsv(EXTERNAL))

    landscape: list[dict[str, Any]] = []
    for row in summary:
        genes = [g for g in row.get("protein_coding_genes", "").split(";") if g]
        records = by_region.get((row["comparator"], row["region"]), [])
        vals = [coloc_for_records(records, p12, w)["PP.H4"] for p12 in P12_VALUES for w in W_VALUES]
        min_h4 = min(vals) if vals else 0.0
        median_h4 = sorted(vals)[len(vals) // 2] if vals else 0.0
        max_h4 = max(vals) if vals else 0.0
        h4_stable = min_h4 >= 0.8
        h4_nominal = fnum(row["PP.H4"])
        h3_nominal = fnum(row["PP.H3"])
        region_class = (
            "stable_H4_first_pass" if h4_stable else
            "nominal_H4_only" if h4_nominal >= 0.8 else
            "stable_H3_or_distinct" if h3_nominal >= 0.8 else
            "unresolved_or_suggestive"
        )
        for gene in genes:
            t = target.get(gene, {})
            c = cell.get(gene, {})
            e = ext.get(gene, {})
            qtl_h4 = max(fnum(t.get("ms_max_qtl_h4")), fnum(t.get("max_qtl_h4")))
            l2g_count = fnum(t.get("strong_l2g_disease_count"))
            qtl_count = fnum(t.get("strong_qtl_coloc_disease_count"))
            drug_activity = fnum(t.get("druggable_activity_count"), fnum(e.get("druggable_activity_count")))
            chembl = t.get("chembl_target_id") or e.get("chembl_target_id") or ""
            cell_score = fnum(c.get("score"))
            same_gene_cellstate = str(c.get("same_gene_cellstate_gate", "")).lower() == "true"
            prior_block = t.get("manual_blocker") or c.get("wave164_blockers") or ""
            score = (
                4.0 * h4_nominal
                + 1.5 * median_h4
                + 1.0 * min(l2g_count, 5) / 5
                + 1.0 * min(qtl_count, 5) / 5
                + 1.0 * min(qtl_h4, 1)
                + (0.8 if chembl else 0)
                + (0.5 if drug_activity > 0 else 0)
                + (0.5 if same_gene_cellstate else 0)
                + min(max(cell_score, -2), 8) / 16
            )
            landscape.append(
                {
                    "gene": gene,
                    "comparator": row["comparator"],
                    "region": row["region"],
                    "region_class": region_class,
                    "nominal_PP.H4": h4_nominal,
                    "nominal_PP.H3": h3_nominal,
                    "min_sensitivity_PP.H4": min_h4,
                    "median_sensitivity_PP.H4": median_h4,
                    "max_sensitivity_PP.H4": max_h4,
                    "top_shared_snp": row["top_shared_snp"],
                    "strong_l2g_disease_count": l2g_count,
                    "strong_l2g_diseases": t.get("strong_l2g_diseases", ""),
                    "strong_qtl_coloc_disease_count": qtl_count,
                    "strong_qtl_coloc_diseases": t.get("strong_qtl_coloc_diseases", ""),
                    "ms_max_qtl_h4": t.get("ms_max_qtl_h4", ""),
                    "max_qtl_h4": t.get("max_qtl_h4", ""),
                    "qtl_direction_proxy_values": t.get("direction_proxy_values", "")[:500],
                    "same_gene_cellstate_score": cell_score,
                    "same_gene_cellstate_gate": c.get("same_gene_cellstate_gate", ""),
                    "positive_c15_contexts": c.get("positive_c15_contexts", ""),
                    "best_c15_context": c.get("best_c15_context", ""),
                    "chembl_target_id": chembl,
                    "druggable_activity_count": drug_activity,
                    "manual_blocker": prior_block,
                    "landscape_score": score,
                }
            )

    landscape.sort(key=lambda r: (r["region_class"] == "stable_H4_first_pass", r["landscape_score"]), reverse=True)
    write_tsv(
        OUT / "shared_locus_gene_landscape.tsv",
        landscape,
        [
            "gene", "comparator", "region", "region_class", "nominal_PP.H4", "nominal_PP.H3",
            "min_sensitivity_PP.H4", "median_sensitivity_PP.H4", "max_sensitivity_PP.H4",
            "top_shared_snp", "strong_l2g_disease_count", "strong_l2g_diseases",
            "strong_qtl_coloc_disease_count", "strong_qtl_coloc_diseases", "ms_max_qtl_h4",
            "max_qtl_h4", "qtl_direction_proxy_values", "same_gene_cellstate_score",
            "same_gene_cellstate_gate", "positive_c15_contexts", "best_c15_context",
            "chembl_target_id", "druggable_activity_count", "manual_blocker", "landscape_score",
        ],
    )

    # Region-level rollup for resume readability.
    region_rollup: list[dict[str, Any]] = []
    for row in summary:
        genes = [r for r in landscape if r["comparator"] == row["comparator"] and r["region"] == row["region"]]
        top = genes[:5]
        records = by_region.get((row["comparator"], row["region"]), [])
        vals = [coloc_for_records(records, p12, w)["PP.H4"] for p12 in P12_VALUES for w in W_VALUES]
        region_rollup.append(
            {
                "comparator": row["comparator"],
                "region": row["region"],
                "nominal_PP.H4": row["PP.H4"],
                "nominal_PP.H3": row["PP.H3"],
                "min_sensitivity_PP.H4": min(vals) if vals else "",
                "median_sensitivity_PP.H4": sorted(vals)[len(vals)//2] if vals else "",
                "n_shared_snps": row["n_shared_snps"],
                "top_genes_by_landscape_score": ";".join(g["gene"] for g in sorted(genes, key=lambda x: x["landscape_score"], reverse=True)[:8]),
            }
        )
    region_rollup.sort(key=lambda r: fnum(r["nominal_PP.H4"]), reverse=True)
    write_tsv(
        OUT / "region_landscape_rollup.tsv",
        region_rollup,
        ["comparator", "region", "nominal_PP.H4", "nominal_PP.H3", "min_sensitivity_PP.H4", "median_sensitivity_PP.H4", "n_shared_snps", "top_genes_by_landscape_score"],
    )

    top_rows = [r for r in landscape if r["region_class"] in {"stable_H4_first_pass", "nominal_H4_only"}][:20]
    lines = [
        "# V14 Shared-Locus Landscape",
        "",
        "Status: landscape and prior-sensitivity layer over V13 OpenGWAS coloc outputs.",
        "",
        "## Tool Availability",
        "",
        f"- `ldsc.py`: `{bool(shutil.which('ldsc.py'))}`.",
        f"- `munge_sumstats.py`: `{bool(shutil.which('munge_sumstats.py'))}`.",
        "- R package `susieR`: not installed in this run.",
        "- R package `coloc`: not installed in this run.",
        "",
        "Therefore this checkpoint does not claim robust genetics grade. It ranks",
        "candidate loci and tests sensitivity of the V13 single-causal-variant coloc",
        "posteriors to priors/effect-size assumptions.",
        "",
        "## Top Landscape Rows",
        "",
        "| rank | gene | comparator | region | class | H4 | min H4 sensitivity | L2G diseases | QTL diseases | blocker |",
        "| ---: | --- | --- | --- | --- | ---: | ---: | --- | --- | --- |",
    ]
    for i, r in enumerate(top_rows, 1):
        lines.append(
            f"| {i} | {r['gene']} | {r['comparator']} | {r['region']} | {r['region_class']} | "
            f"{float(r['nominal_PP.H4']):.4g} | {float(r['min_sensitivity_PP.H4']):.4g} | "
            f"{r['strong_l2g_diseases']} | {r['strong_qtl_coloc_diseases']} | {str(r['manual_blocker'])[:80]} |"
        )
    lines += [
        "",
        "## PTGER4 Interim Read",
        "",
        "PTGER4 remains the strongest druggable candidate in the first-pass landscape",
        "because it sits in a high-H4 MS-UC region and has existing target-resolution",
        "support across Crohn/MS/Psoriasis/T1D/UC plus QTL-coloc in Crohn/MS/UC.",
        "However, the V3/V14 blocker is unchanged: EP4 therapeutic direction is",
        "unresolved and prior-art/conflicted. No MS intervention direction is claimed.",
        "",
        "## Next Required Work",
        "",
        "1. Install or otherwise provision LDSC/HDL and run genome-wide MS-UC/MS-Crohn",
        "   genetic correlation with MHC sensitivity.",
        "2. Install `susieR`/`coloc` or run an equivalent external SuSiE-coloc pipeline.",
        "3. For PTGER4, resolve effect-allele-aligned QTL direction in CD4 T cells and",
        "   monocytes before any agonist/antagonist hypothesis.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"landscape_rows": len(landscape), "region_rows": len(region_rollup), "out": str(OUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
