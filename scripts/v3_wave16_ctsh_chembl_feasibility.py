#!/usr/bin/env python3
"""Wave16 CTSH ChEMBL feasibility audit.

This script is intentionally modest: it does not claim medicinal-chemistry
selectivity. It checks whether public ChEMBL bioactivity records make CTSH look
like a tractable, selective autoimmune intervention point relative to nearby
cysteine cathepsins.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pandas as pd
import requests


OUT = Path("phases/v3/results/wave16_ctsh_chembl_feasibility")
OUT.mkdir(parents=True, exist_ok=True)

SEED = 20260526

TARGETS = {
    "CTSH": "CHEMBL2225",
    "CTSS": "CHEMBL2954",
    "CTSB": "CHEMBL4072",
    "CTSL": "CHEMBL3837",
    "CTSK": "CHEMBL268",
    "CTSZ": "CHEMBL4160",
}

ACTIVITY_URL = "https://www.ebi.ac.uk/chembl/api/data/activity.json"
MAX_RECORDS_PER_TARGET = 1500


def fetch_target_activities(gene: str, target_id: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    url = ACTIVITY_URL
    params: dict[str, Any] | None = {
        "target_chembl_id": target_id,
        "limit": 1000,
        "standard_type__in": "IC50,Ki,EC50,Potency",
        "standard_units": "nM",
    }
    total_count = None
    while url and len(rows) < MAX_RECORDS_PER_TARGET:
        try:
            resp = requests.get(url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:  # noqa: BLE001 - preserve remote API blocker
            errors.append(str(exc))
            break

        page_meta = data.get("page_meta", {})
        total_count = page_meta.get("total_count", total_count)
        for act in data.get("activities", []):
            value = act.get("standard_value")
            try:
                value_f = float(value)
            except (TypeError, ValueError):
                continue
            if value_f <= 0 or math.isnan(value_f):
                continue
            rows.append(
                {
                    "gene": gene,
                    "target_chembl_id": target_id,
                    "molecule_chembl_id": act.get("molecule_chembl_id"),
                    "standard_type": act.get("standard_type"),
                    "standard_relation": act.get("standard_relation"),
                    "standard_value_nM": value_f,
                    "pchembl_value": act.get("pchembl_value"),
                    "assay_chembl_id": act.get("assay_chembl_id"),
                    "document_chembl_id": act.get("document_chembl_id"),
                    "bao_endpoint": act.get("bao_endpoint"),
                    "source": "ChEMBL activity API",
                }
            )
            if len(rows) >= MAX_RECORDS_PER_TARGET:
                break

        next_path = page_meta.get("next")
        url = f"https://www.ebi.ac.uk{next_path}" if next_path and len(rows) < MAX_RECORDS_PER_TARGET else None
        params = None

    meta = {
        "gene": gene,
        "target_chembl_id": target_id,
        "total_count_reported": total_count,
        "records_retained": len(rows),
        "cap": MAX_RECORDS_PER_TARGET,
        "errors": errors,
    }
    return rows, meta


def summarize(df: pd.DataFrame, meta: list[dict[str, Any]]) -> pd.DataFrame:
    meta_df = pd.DataFrame(meta)
    if df.empty:
        return meta_df
    stats = (
        df.groupby("gene")
        .agg(
            n_activity_rows=("molecule_chembl_id", "size"),
            unique_molecules=("molecule_chembl_id", "nunique"),
            median_nM=("standard_value_nM", "median"),
            min_nM=("standard_value_nM", "min"),
            n_sub_100nM=("standard_value_nM", lambda s: int((s <= 100).sum())),
            n_sub_1000nM=("standard_value_nM", lambda s: int((s <= 1000).sum())),
        )
        .reset_index()
    )
    return meta_df.merge(stats, on="gene", how="left")


def overlap_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    ctsh = set(df.loc[df["gene"] == "CTSH", "molecule_chembl_id"].dropna())
    for gene in sorted(set(TARGETS) - {"CTSH"}):
        other = set(df.loc[df["gene"] == gene, "molecule_chembl_id"].dropna())
        rows.append(
            {
                "gene": gene,
                "ctsh_molecule_count": len(ctsh),
                "other_molecule_count": len(other),
                "overlap_with_ctsh": len(ctsh & other),
                "fraction_ctsh_with_other_record": len(ctsh & other) / len(ctsh) if ctsh else 0.0,
            }
        )
    return pd.DataFrame(rows)


def selectivity_probe(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    best = (
        df.groupby(["gene", "molecule_chembl_id"])["standard_value_nM"]
        .min()
        .reset_index()
        .pivot(index="molecule_chembl_id", columns="gene", values="standard_value_nM")
    )
    if "CTSH" not in best:
        return pd.DataFrame()
    best = best.loc[best["CTSH"].notna()].copy()
    comparator_cols = [c for c in best.columns if c != "CTSH"]
    best["best_non_ctsh_nM"] = best[comparator_cols].min(axis=1, skipna=True)
    best["has_any_non_ctsh_record"] = best[comparator_cols].notna().any(axis=1)
    best["best_selectivity_ratio_non_ctsh_over_ctsh"] = best["best_non_ctsh_nM"] / best["CTSH"]
    best["ctsh_sub_1000nM"] = best["CTSH"] <= 1000
    best["ctsh_sub_100nM"] = best["CTSH"] <= 100
    best["selectivity_10x_by_observed_records"] = (
        best["has_any_non_ctsh_record"]
        & best["ctsh_sub_1000nM"]
        & (best["best_selectivity_ratio_non_ctsh_over_ctsh"] >= 10)
    )
    best = best.reset_index()
    return best.sort_values(["selectivity_10x_by_observed_records", "CTSH"], ascending=[False, True])


def main() -> None:
    all_rows: list[dict[str, Any]] = []
    meta: list[dict[str, Any]] = []
    for gene, target_id in TARGETS.items():
        rows, target_meta = fetch_target_activities(gene, target_id)
        all_rows.extend(rows)
        meta.append(target_meta)

    df = pd.DataFrame(all_rows)
    if not df.empty:
        df.to_csv(OUT / "cathepsin_activity_records.tsv", sep="\t", index=False)
    summary = summarize(df, meta)
    summary.to_csv(OUT / "cathepsin_activity_summary.tsv", sep="\t", index=False)

    overlaps = overlap_table(df) if not df.empty else pd.DataFrame()
    overlaps.to_csv(OUT / "ctsh_cross_cathepsin_molecule_overlap.tsv", sep="\t", index=False)

    selectivity = selectivity_probe(df)
    selectivity.to_csv(OUT / "ctsh_observed_selectivity_probe.tsv", sep="\t", index=False)

    no_go_reasons = []
    ctsh_summary = summary.loc[summary["gene"] == "CTSH"]
    if not ctsh_summary.empty:
        unique_ctsh = int(ctsh_summary["unique_molecules"].fillna(0).iloc[0])
        median_ctsh = float(ctsh_summary["median_nM"].fillna(float("nan")).iloc[0])
        if unique_ctsh < 200:
            no_go_reasons.append("CTSH has far fewer public ChEMBL molecules than CTSS/CTSB/CTSL comparator targets.")
        if median_ctsh >= 1000:
            no_go_reasons.append("Median retained CTSH potency is micromolar-to-weak, not a strong selective-tool landscape.")
    if not overlaps.empty:
        max_overlap = int(overlaps["overlap_with_ctsh"].max())
        if max_overlap >= 25:
            no_go_reasons.append("A substantial fraction of CTSH molecules also have records against other cysteine cathepsins.")
    if not selectivity.empty:
        n_observed_10x = int(selectivity["selectivity_10x_by_observed_records"].sum())
        if n_observed_10x == 0:
            no_go_reasons.append("No pulled record shows a sub-micromolar CTSH molecule with observed >=10x selectivity over comparator cathepsins.")
        else:
            no_go_reasons.append(
                f"Only {n_observed_10x} pulled molecules meet an observed >=10x CTSH selectivity heuristic; absence of comparator data is not proof of selectivity."
            )

    summary_json = {
        "seed": SEED,
        "targets": TARGETS,
        "activity_url": ACTIVITY_URL,
        "max_records_per_target": MAX_RECORDS_PER_TARGET,
        "interpretation": "CTSH remains druggable-in-principle but not feasibility-positive for V3 without selective cellular target-engagement data.",
        "no_go_reasons": no_go_reasons,
        "outputs": [
            str(OUT / "cathepsin_activity_records.tsv"),
            str(OUT / "cathepsin_activity_summary.tsv"),
            str(OUT / "ctsh_cross_cathepsin_molecule_overlap.tsv"),
            str(OUT / "ctsh_observed_selectivity_probe.tsv"),
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary_json, indent=2), encoding="utf-8")

    print(json.dumps(summary_json, indent=2))


if __name__ == "__main__":
    main()
