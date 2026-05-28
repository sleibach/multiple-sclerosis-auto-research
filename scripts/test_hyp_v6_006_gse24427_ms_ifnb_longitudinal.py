#!/usr/bin/env python3
"""GSE24427 MS IFN-beta longitudinal module check for HYP_V6_006."""

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
SOFT = ROOT / "data" / "raw" / "GSE24427" / "GSE24427_family.soft.gz"
OUT = ROOT / "analysis" / "tier_0_triage" / "hyp_v6_006_gse24427_ms_ifnb_longitudinal"

MODULES = {
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "ISG15", "CD74", "HLA-DRA"],
    "hla_ii_without_cd74": ["HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DQA1", "HLA-DQB1"],
    "receptor_only_cd74_cd44_cxcr4": ["CD74", "CD44", "CXCR4"],
    "cd74_alone": ["CD74"],
}
TARGET_GENES = {g for genes in MODULES.values() for g in genes}


def parse_platforms() -> tuple[dict[str, set[str]], set[str]]:
    id_to_genes = {}
    in_platform = False
    header = None
    with gzip.open(SOFT, "rt", errors="replace") as handle:
        for line in handle:
            line = line.rstrip("\n")
            if line == "!platform_table_begin":
                in_platform = True
                header = None
                continue
            if line == "!platform_table_end" and in_platform:
                in_platform = False
                continue
            if not in_platform:
                continue
            if header is None:
                header = line.split("\t")
                continue
            parts = line.split("\t")
            if len(parts) != len(header):
                continue
            row = dict(zip(header, parts))
            symbol_field = row.get("Gene Symbol", "")
            genes = set()
            for item in re.split(r"\s*///\s*", symbol_field):
                item = item.strip()
                if item in TARGET_GENES:
                    genes.add(item)
            if genes:
                id_to_genes[row["ID"]] = genes
    return id_to_genes, set(id_to_genes)


def parse_title(title: str) -> dict[str, object]:
    m = re.search(r"Patient\s+(\d+),\s+(.+?)_chip([AB])", title)
    patient = m.group(1) if m else "unknown"
    time_label = m.group(2) if m else "unknown"
    chip = m.group(3) if m else "unknown"
    if "before first" in time_label:
        timepoint = "baseline"
        month = 0.0
    elif "before second" in time_label:
        timepoint = "second_injection"
        month = 0.07
    elif "month1" in time_label or "month 1" in time_label:
        timepoint = "month_1"
        month = 1.0
    elif "month12" in time_label or "month 12" in time_label:
        timepoint = "month_12"
        month = 12.0
    elif "month24" in time_label or "month 24" in time_label:
        timepoint = "month_24"
        month = 24.0
    else:
        timepoint = "unknown"
        month = np.nan
    return {"patient": patient, "timepoint": timepoint, "month": month, "chip": chip}


def numeric_value(text: str) -> float:
    try:
        return float(text)
    except Exception:
        return np.nan


def parse_samples(keep_ids: set[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    meta_rows = []
    expr_rows = []
    current = None
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
            if line.startswith("!Sample_characteristics_ch1 = "):
                item = line.split(" = ", 1)[1]
                if ": " in item:
                    key, value = item.split(": ", 1)
                    key = key.strip().lower()
                    if key.startswith("number of relapses during 2-year"):
                        current["relapses_2y"] = numeric_value(value)
                    elif key.startswith("time from start of therapy to the first relapse"):
                        current["first_relapse_month"] = numeric_value(value)
                    elif key.startswith("edss at baseline"):
                        current["edss_baseline"] = numeric_value(value)
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
                parts = line.split("\t")
                if len(parts) >= 2 and parts[0] in keep_ids:
                    try:
                        value = float(parts[1])
                    except Exception:
                        continue
                    expr_rows.append({"geo_accession": current["geo_accession"], "probe_id": parts[0], "value": value})
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
    id_to_genes, keep_ids = parse_platforms()
    meta, expr = parse_samples(keep_ids)
    meta["relapse_free_2y"] = (meta["relapses_2y"] == 0).astype(int)
    meta.to_csv(OUT / "sample_metadata.tsv", sep="\t", index=False)

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
        coverage.append({"module": module, "present": ";".join(present), "missing": ";".join(sorted(set(genes) - set(present))), "n_present": len(present)})
        vals = z[present].mean(axis=1)
        for geo, score in vals.items():
            score_rows.append({"geo_accession": geo, "module": module, "score": float(score)})
    scores = pd.DataFrame(score_rows).merge(meta, on="geo_accession", how="left")
    scores.to_csv(OUT / "sample_module_scores.tsv", sep="\t", index=False)
    pd.DataFrame(coverage).to_csv(OUT / "module_gene_coverage.tsv", sep="\t", index=False)

    wide = scores.pivot_table(index=["patient", "timepoint", "month"], columns="module", values="score").reset_index()
    clinical = meta[["patient", "relapse_free_2y", "relapses_2y", "first_relapse_month"]].drop_duplicates("patient")
    wide = wide.merge(clinical, on="patient", how="left")
    delta_rows = []
    for patient, sub in wide.groupby("patient", observed=True):
        base = sub[sub["timepoint"] == "baseline"]
        if base.empty:
            continue
        for _, post in sub[sub["timepoint"] != "baseline"].iterrows():
            row = {
                "patient": patient,
                "timepoint": post["timepoint"],
                "month": post["month"],
                "relapse_free_2y": int(post["relapse_free_2y"]),
                "relapses_2y": post["relapses_2y"],
                "first_relapse_month": post["first_relapse_month"],
            }
            for module in MODULES:
                row[f"baseline__{module}"] = float(base.iloc[0][module])
                row[f"delta__{module}"] = float(post[module] - base.iloc[0][module])
            delta_rows.append(row)
    deltas = pd.DataFrame(delta_rows)
    deltas.to_csv(OUT / "paired_module_deltas.tsv", sep="\t", index=False)

    tests = []
    baseline = wide[wide["timepoint"] == "baseline"].copy()
    for module in MODULES:
        a = baseline[baseline["relapse_free_2y"] == 1][module]
        b = baseline[baseline["relapse_free_2y"] == 0][module]
        t = st.ttest_ind(a, b, equal_var=False, nan_policy="omit")
        tests.append(
            {
                "analysis": "baseline_relapse_free_2y",
                "timepoint": "baseline",
                "module": module,
                "n_relapse_free": len(a),
                "n_not_relapse_free": len(b),
                "delta_relapse_free_minus_not": float(a.mean() - b.mean()),
                "hedges_g": hedges_g(a, b),
                "welch_p": float(t.pvalue),
            }
        )
    for tp in sorted(deltas["timepoint"].dropna().unique()):
        sub = deltas[deltas["timepoint"] == tp]
        for module in MODULES:
            col = f"delta__{module}"
            a = sub[sub["relapse_free_2y"] == 1][col]
            b = sub[sub["relapse_free_2y"] == 0][col]
            if len(a) >= 2 and len(b) >= 2:
                t = st.ttest_ind(a, b, equal_var=False, nan_policy="omit")
                tests.append(
                    {
                        "analysis": "delta_relapse_free_2y",
                        "timepoint": tp,
                        "module": module,
                        "n_relapse_free": len(a),
                        "n_not_relapse_free": len(b),
                        "delta_relapse_free_minus_not": float(a.mean() - b.mean()),
                        "hedges_g": hedges_g(a, b),
                        "welch_p": float(t.pvalue),
                    }
                )
    tests_df = pd.DataFrame(tests)
    tests_df.to_csv(OUT / "relapse_free_contrasts.tsv", sep="\t", index=False)

    summary = {
        "dataset": "GSE24427",
        "n_samples": int(len(meta)),
        "n_patients": int(meta["patient"].nunique()),
        "target_probe_count": int(len(keep_ids)),
        "relapse_free_counts_baseline": baseline["relapse_free_2y"].value_counts(dropna=False).to_dict(),
        "key_contrasts": tests_df[tests_df["module"].isin(["ifn_apc", "hla_ii_without_cd74", "receptor_only_cd74_cd44_cxcr4"])].to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    key = tests_df[tests_df["module"].isin(["ifn_apc", "hla_ii_without_cd74", "receptor_only_cd74_cd44_cxcr4"])].copy()
    lines = [
        "# HYP_V6_006 Independent Check: GSE24427 MS IFN-Beta Longitudinal",
        "",
        "## Scope",
        "",
        "Tests whether baseline or longitudinal changes in IFN/APC, HLA-II, or",
        "receptor-only CD74/CD44/CXCR4 modules associate with two-year relapse-free",
        "status during IFN-beta-1b therapy.",
        "",
        "Caveat: GSE24427 uses Affymetrix U133 A/B chips. This parser combines",
        "target-gene probes across chip samples and averages to patient/timepoint;",
        "it is a Tier -1/Tier 0 screen, not a full reprocessing pipeline.",
        "",
        "## Key Contrasts",
        "",
        "```tsv",
        key.sort_values(["analysis", "timepoint", "module"]).to_csv(sep="\t", index=False).strip(),
        "```",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
