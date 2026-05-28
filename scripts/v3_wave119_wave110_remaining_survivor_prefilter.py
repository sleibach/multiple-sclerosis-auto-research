#!/usr/bin/env python3
"""Wave119 batch prefilter for remaining Wave110 perturbation-first survivors."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "results_v3" / "wave119_wave110_remaining_survivor_prefilter"
CANDIDATES = [
    "CLEC7A",
    "FAM49B",
    "LYN",
    "CCDC121",
    "CHST11",
    "FBXO16",
    "RECQL4",
    "EFR3A",
    "IGLON5",
    "MAN1A2",
    "MREG",
    "PLIN4",
    "SLC39A3",
    "YWHAE",
]

W110 = ROOT / "results_v3" / "wave110_post_closure_intervention_route_map" / "post_closure_route_map.tsv"
W81 = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W37 = ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
MS = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_ms_rows.tsv"
BROAD = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_broad_summary.tsv"
IBD = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_ibd_response_summary.tsv"
W62 = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_wave62_rows.tsv"
W71 = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_wave71_rows.tsv"


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def rows_for(df: pd.DataFrame, gene: str) -> pd.DataFrame:
    for col in ["gene", "gene_symbol", "candidate"]:
        if col in df.columns:
            return df[df[col].astype(str).eq(gene)].copy()
    return pd.DataFrame()


def first(df: pd.DataFrame) -> dict[str, object]:
    return df.to_dict(orient="records")[0] if not df.empty else {}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tables = {
        "w110": read_tsv(W110),
        "w81": read_tsv(W81),
        "w37": read_tsv(W37),
        "ms": read_tsv(MS),
        "broad": read_tsv(BROAD),
        "ibd": read_tsv(IBD),
        "w62": read_tsv(W62),
        "w71": read_tsv(W71),
    }
    rows = []
    evidence = []
    for gene in CANDIDATES:
        r81 = rows_for(tables["w81"], gene)
        r37 = rows_for(tables["w37"], gene)
        rms = rows_for(tables["ms"], gene)
        rbroad = rows_for(tables["broad"], gene)
        ribd = rows_for(tables["ibd"], gene)
        rw62 = rows_for(tables["w62"], gene)
        rw71 = rows_for(tables["w71"], gene)
        rw110 = rows_for(tables["w110"], gene)
        ms_anchor = (not rms.empty) and (float(rms.iloc[0].get("p", 1) or 1) < 0.05) and (float(rms.iloc[0].get("delta_log2", 0) or 0) > 0)
        ms_fdr = (not rms.empty) and (float(rms.iloc[0].get("fdr", 1) or 1) < 0.10)
        broad_pos = int(rbroad.iloc[0].get("positive_disease_count", 0) or 0) if not rbroad.empty else 0
        broad_neg = int(rbroad.iloc[0].get("negative_disease_count", 0) or 0) if not rbroad.empty else 0
        response = (not ribd.empty) and bool(ribd.iloc[0].get("ibd_response_fdr10", 0))
        target_resolution = (not rw62.empty) and not str(rw62.iloc[0].get("wave62_call", "")).startswith("NO_GO")
        modality = (not r81.empty) and bool(r81.iloc[0].get("modality_channel", 0))
        foundation = (not r81.empty) and bool(r81.iloc[0].get("foundation_model_support", 0))
        crispr_call = str(r37.iloc[0].get("screen_call", "")) if not r37.empty else ""
        crispr_nominal = crispr_call.startswith("KO_ENHANCES")
        crispr_fdr = (not r37.empty) and (
            float(r37.iloc[0].get("efficient_fdr", 1) or 1) < 0.10
            or float(r37.iloc[0].get("contrast_fdr", 1) or 1) < 0.10
        )
        n_sgrna = int(r37.iloc[0].get("n_sgrna", 0) or 0) if not r37.empty else 0
        wave71_blocked = (not rw71.empty) and str(rw71.iloc[0].get("wave71_call", "")).startswith("NO_REOPEN")
        hard_passes = sum([ms_anchor, response, target_resolution, crispr_fdr, modality, foundation])
        call = (
            "PARK_FOR_TARGETED_FORCING_TEST"
            if hard_passes >= 3 and not wave71_blocked and broad_pos >= 2
            else "NO_GO_PREFILTER_REMAINING_WAVE110_SURVIVOR"
        )
        rows.append(
            {
                "gene": gene,
                "call": call,
                "hard_passes": hard_passes,
                "ms_anchor": ms_anchor,
                "ms_fdr10": ms_fdr,
                "broad_positive_diseases": broad_pos,
                "broad_negative_diseases": broad_neg,
                "response_fdr10": response,
                "target_resolution": target_resolution,
                "modality": modality,
                "foundation": foundation,
                "crispr_nominal": crispr_nominal,
                "crispr_fdr10": crispr_fdr,
                "n_sgrna": n_sgrna,
                "wave71_blocked": wave71_blocked,
            }
        )
        for source, frame in [
            ("wave110", rw110),
            ("wave81", r81),
            ("wave37", r37),
            ("ms", rms),
            ("broad", rbroad),
            ("ibd", ribd),
            ("wave62", rw62),
            ("wave71", rw71),
        ]:
            evidence.append({"gene": gene, "source": source, "value": first(frame)})

    decisions = pd.DataFrame(rows)
    evidence_df = pd.DataFrame(evidence)
    decisions.to_csv(OUT / "remaining_wave110_prefilter_decisions.tsv", sep="\t", index=False)
    evidence_df.to_csv(OUT / "remaining_wave110_prefilter_evidence.tsv", sep="\t", index=False)
    n_park = int(decisions["call"].str.startswith("PARK").sum())
    branch_call = "PARK_REMAINING_WAVE110_SURVIVOR_EXISTS" if n_park else "NO_REMAINING_WAVE110_SURVIVOR_AFTER_PREFILTER"
    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "branch_call": branch_call,
            "n_candidates": len(CANDIDATES),
            "n_park": n_park,
            "inputs": {
                "wave110": rel(W110),
                "wave81": rel(W81),
                "wave37": rel(W37),
                "ms": rel(MS),
                "broad": rel(BROAD),
                "ibd": rel(IBD),
                "wave62": rel(W62),
                "wave71": rel(W71),
            },
        },
    )
    report = f"""# Wave119 Remaining Wave110 Survivor Prefilter

## Bottom Line

Branch call: `{branch_call}`.

This batch prefilter tests whether the current top Wave110 survivor genes
deserve individual forcing scripts, using hard gates for MS, response,
target-resolution, FDR-supported perturbation, modality, and foundation support.

## Decisions

{markdown_table(decisions, max_rows=30)}

## Evidence Rows

{markdown_table(evidence_df, max_rows=40)}

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave119_wave110_remaining_survivor_prefilter.py")}`
- Output: `{rel(OUT / "remaining_wave110_prefilter_decisions.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
