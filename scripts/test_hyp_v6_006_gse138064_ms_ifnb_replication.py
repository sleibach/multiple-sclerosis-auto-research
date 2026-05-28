#!/usr/bin/env python3
"""Independent MS IFN-beta response check for HYP_V6_006 using GSE138064."""

from __future__ import annotations

import gzip
import json
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as st


ROOT = Path(__file__).resolve().parents[1]
SOFT = ROOT / "data" / "raw" / "GSE138064" / "GSE138064_family.soft.gz"
OUT = ROOT / "analysis" / "tier_0_triage" / "hyp_v6_006_gse138064_ms_ifnb_replication"

MODULES = {
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"],
    "hla_ii_without_cd74": ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"],
    "receptor_only_cd74_cd44_cxcr4": ["CD74", "CD44", "CXCR4"],
    "cd74_alone": ["CD74"],
}
TARGET_GENES = {g for genes in MODULES.values() for g in genes}


def parse_platform() -> tuple[dict[str, set[str]], set[str]]:
    id_to_genes: dict[str, set[str]] = {}
    keep_ids: set[str] = set()
    in_platform = False
    header: list[str] | None = None
    with gzip.open(SOFT, "rt", errors="replace") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line == "!platform_table_begin":
                in_platform = True
                continue
            if line == "!platform_table_end" and in_platform:
                break
            if not in_platform:
                continue
            if header is None:
                header = line.split("\t")
                continue
            parts = line.split("\t")
            if len(parts) != len(header):
                continue
            row = dict(zip(header, parts))
            assignment = row.get("gene_assignment", "")
            genes = {g for g in TARGET_GENES if re.search(rf"(^| // ){re.escape(g)}( // |$)", assignment)}
            if genes:
                probe_id = row["ID"]
                id_to_genes[probe_id] = genes
                keep_ids.add(probe_id)
    return id_to_genes, keep_ids


def parse_title(title: str) -> dict[str, object]:
    # Example: SM1.Complete_Responder.A1, Clinically stable MS, 8MU IFN-beta
    # (250 ug), 0 h after IFN-beta injection
    m = re.search(r"SM\d+\.([A-Za-z_]+)\.([AB]\d+)", title)
    responder = m.group(1) if m else "unknown"
    subject = m.group(2) if m else "unknown"
    status = "active" if "Clinically active" in title else ("stable" if "Clinically stable" in title else "other")
    dose = "16MU" if "16MU" in title or "500 ug" in title else ("8MU" if "8MU" in title or "250 ug" in title else "none")
    hm = re.search(r",\s*(0|4|24)\s+h after", title)
    hour = int(hm.group(1)) if hm else np.nan
    return {"responder": responder, "subject": subject, "clinical_status": status, "dose": dose, "hour": hour}


def parse_samples(keep_ids: set[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    meta_rows = []
    expr_rows = []
    current: dict[str, object] | None = None
    in_table = False
    with gzip.open(SOFT, "rt", errors="replace") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line.startswith("^SAMPLE = "):
                current = {"geo_accession": line.split(" = ", 1)[1]}
                in_table = False
                continue
            if current is None:
                continue
            if line.startswith("!Sample_title = "):
                title = line.split(" = ", 1)[1]
                current["title"] = title
                current.update(parse_title(title))
                continue
            if line == "!sample_table_begin":
                in_table = True
                continue
            if line == "!sample_table_end":
                meta_rows.append(current)
                current = None
                in_table = False
                continue
            if in_table and not line.startswith("ID_REF"):
                probe, value = line.split("\t")[:2]
                if probe in keep_ids:
                    expr_rows.append(
                        {
                            "geo_accession": current["geo_accession"],
                            "probe_id": probe,
                            "value": float(value),
                        }
                    )
    return pd.DataFrame(meta_rows), pd.DataFrame(expr_rows)


def hedges_g(a: pd.Series, b: pd.Series) -> float:
    a = a.dropna().astype(float)
    b = b.dropna().astype(float)
    if len(a) < 2 or len(b) < 2:
        return math.nan
    pooled = math.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    if pooled == 0:
        return math.nan
    return float(((a.mean() - b.mean()) / pooled) * (1 - 3 / (4 * (len(a) + len(b)) - 9)))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    id_to_genes, keep_ids = parse_platform()
    meta, expr = parse_samples(keep_ids)

    gene_rows = []
    for row in expr.itertuples(index=False):
        for gene in id_to_genes[row.probe_id]:
            gene_rows.append({"geo_accession": row.geo_accession, "gene": gene, "value": row.value})
    gene_expr = pd.DataFrame(gene_rows).groupby(["geo_accession", "gene"], observed=True)["value"].mean().reset_index()
    wide_gene = gene_expr.pivot(index="geo_accession", columns="gene", values="value")

    z = (wide_gene - wide_gene.mean()) / wide_gene.std(ddof=0).replace(0, np.nan)
    score_rows = []
    coverage = []
    for module, genes in MODULES.items():
        present = [g for g in genes if g in z.columns]
        missing = sorted(set(genes) - set(present))
        coverage.append({"module": module, "present": ";".join(present), "missing": ";".join(missing), "n_present": len(present)})
        scores = z[present].mean(axis=1)
        for geo, score in scores.items():
            score_rows.append({"geo_accession": geo, "module": module, "score": float(score)})
    scores = pd.DataFrame(score_rows).merge(meta, on="geo_accession", how="left")
    scores.to_csv(OUT / "sample_module_scores.tsv", sep="\t", index=False)
    pd.DataFrame(coverage).to_csv(OUT / "module_gene_coverage.tsv", sep="\t", index=False)
    meta.to_csv(OUT / "sample_metadata.tsv", sep="\t", index=False)

    piv = scores.pivot_table(
        index=["subject", "responder", "clinical_status", "dose", "hour"],
        columns="module",
        values="score",
    ).reset_index()
    delta_rows = []
    for (subject, responder, status, dose), sub in piv.groupby(["subject", "responder", "clinical_status", "dose"], observed=True):
        base = sub[sub["hour"] == 0]
        if base.empty:
            continue
        for hour in [4, 24]:
            post = sub[sub["hour"] == hour]
            if post.empty:
                continue
            row = {"subject": subject, "responder": responder, "clinical_status": status, "dose": dose, "hour": hour}
            for module in MODULES:
                row[f"delta__{module}"] = float(post.iloc[0][module] - base.iloc[0][module])
                row[f"baseline__{module}"] = float(base.iloc[0][module])
            delta_rows.append(row)
    deltas = pd.DataFrame(delta_rows)
    deltas.to_csv(OUT / "paired_module_deltas.tsv", sep="\t", index=False)

    tests = []
    comp = deltas[deltas["responder"].isin(["Complete_Responder", "Partial_Responder"])].copy()
    for status in ["stable", "active", "all"]:
        for dose in ["8MU", "16MU", "all"]:
            for hour in [4, 24]:
                sub = comp[comp["hour"] == hour].copy()
                if status != "all":
                    sub = sub[sub["clinical_status"] == status]
                if dose != "all":
                    sub = sub[sub["dose"] == dose]
                if sub["responder"].nunique() < 2 or len(sub) < 8:
                    continue
                for module in MODULES:
                    for timing, prefix in [("baseline", "baseline__"), ("delta", "delta__")]:
                        col = prefix + module
                        cr = sub[sub["responder"] == "Complete_Responder"][col]
                        pr = sub[sub["responder"] == "Partial_Responder"][col]
                        t = st.ttest_ind(cr, pr, equal_var=False, nan_policy="omit")
                        tests.append(
                            {
                                "clinical_status": status,
                                "dose": dose,
                                "hour": hour,
                                "module": module,
                                "timing": timing,
                                "n_complete": len(cr),
                                "n_partial": len(pr),
                                "delta_complete_minus_partial": float(cr.mean() - pr.mean()),
                                "hedges_g": hedges_g(cr, pr),
                                "welch_p": float(t.pvalue),
                            }
                        )
    tests_df = pd.DataFrame(tests)
    tests_df.to_csv(OUT / "responder_contrasts.tsv", sep="\t", index=False)

    key = tests_df[
        (tests_df["clinical_status"].isin(["stable", "all"]))
        & (tests_df["dose"].isin(["16MU", "all"]))
        & (tests_df["module"].isin(["ifn_apc", "hla_ii_without_cd74", "receptor_only_cd74_cd44_cxcr4"]))
    ].copy()
    key.to_csv(OUT / "key_responder_contrasts.tsv", sep="\t", index=False)

    summary = {
        "dataset": "GSE138064",
        "n_samples": int(len(meta)),
        "n_target_probes": int(len(keep_ids)),
        "responder_counts": meta["responder"].value_counts(dropna=False).to_dict(),
        "key_contrasts": key.to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = [
        "# HYP_V6_006 Independent Check: GSE138064 MS IFN-Beta",
        "",
        "## Scope",
        "",
        "Tests whether MS complete versus partial IFN-beta responders differ in",
        "baseline or acute inducibility of IFN/APC, HLA-II, or receptor-only",
        "CD74/CD44/CXCR4 modules. This is an independent treatment-response",
        "replication attempt for the GSE282122 IFN/APC-HLA-II remodeling branch.",
        "",
        "## Key Contrasts",
        "",
        "```tsv",
        key.sort_values(["clinical_status", "dose", "hour", "timing", "module"]).to_csv(sep="\t", index=False).strip(),
        "```",
        "",
        "## Outputs",
        "",
        "- `sample_metadata.tsv`",
        "- `sample_module_scores.tsv`",
        "- `paired_module_deltas.tsv`",
        "- `responder_contrasts.tsv`",
        "- `key_responder_contrasts.tsv`",
        "- `summary.json`",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
