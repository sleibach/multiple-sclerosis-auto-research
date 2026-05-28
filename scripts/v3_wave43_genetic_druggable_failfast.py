#!/usr/bin/env python3
"""Wave43 strict fail-fast for genetics-plus-druggability parked candidates.

Wave34 left four `PARK_GENETIC_DRUGGABLE_NEEDS_CELL_STATE` rows. FADS1 was
audited in Wave42. This script closes the full parked class by checking whether
any row can be reframed as a stratified or pathway intervention despite weak
cell-state evidence.

No row can be promoted without:
- target-level genetic direction or coloc/MR-ready evidence,
- disease-relevant local or perturbation support,
- a correct-direction modality,
- non-blocking novelty/prior art.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave43_genetic_druggable_failfast"
SEED = 20260527

WAVE34 = ROOT / "results_v3" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv"
BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
RESIDUAL = ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
WAVE42 = ROOT / "results_v3" / "wave42_fads_lipid_desaturation_axis" / "summary.json"

MANUAL_RULES = {
    "FADS1": {
        "correct_direction_modality": "unresolved; FADS1 inhibition exists but autoimmune direction is not target-resolved",
        "branch_specific_blocker": "Wave42: 11q12 locus ambiguity, weak/non-MS state evidence, no LINCS FADS perturbagen, and no target-level direction",
        "prior_art_class": "close_lipid_inhibitor_and_patient_selection_prior_art",
        "wave43_call": "NO_GO_ALREADY_DEMOTED_WAVE42",
    },
    "TYK2": {
        "correct_direction_modality": "inhibit TYK2/JAK-STAT signaling",
        "branch_specific_blocker": "TYK2 inhibitors are an established/crowded autoimmune class; local V3 signal lacks a new lipid-lysosomal or MS-lesion responder delta",
        "prior_art_class": "blocking_autoimmune_prior_art",
        "wave43_call": "NO_GO_PRIOR_ART_AND_GENERIC_IMMUNOSUPPRESSION",
    },
    "JAK2": {
        "correct_direction_modality": "inhibit JAK2/JAK-STAT signaling",
        "branch_specific_blocker": "JAK2 inhibition is broad immunosuppression/hematologic pharmacology, not selective control of the cross-autoimmune lipid-lysosomal module",
        "prior_art_class": "blocking_jak_prior_art_and_safety",
        "wave43_call": "NO_GO_PRIOR_ART_AND_GENERIC_IMMUNOSUPPRESSION",
    },
    "NOD2": {
        "correct_direction_modality": "unclear; Crohn-like loss-of-function biology suggests restoration/agonism, whereas inhibitors would be directionally suspect",
        "branch_specific_blocker": "NOD2 is genetically real but IBD-heavy, lacks local residual/MS support, lacks a validated correct-direction drug package, and host-defense safety is central",
        "prior_art_class": "crowded_ibd_host_defense_prior_art",
        "wave43_call": "NO_GO_DIRECTION_AND_CONTEXT_MISMATCH",
    },
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        values = []
        for col in cols:
            value = "" if pd.isna(row[col]) else str(row[col])
            value = value.replace("\n", " ").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    wave34 = read_tsv(WAVE34)
    broad = read_tsv(BROAD)
    residual = read_tsv(RESIDUAL)
    if wave34.empty:
        raise FileNotFoundError(WAVE34)

    parked = wave34[wave34["wave34_call"].eq("PARK_GENETIC_DRUGGABLE_NEEDS_CELL_STATE")].copy()
    broad_sub = broad[broad.get("gene", pd.Series(dtype=str)).isin(parked["gene"].astype(str))].copy()
    residual_sub = residual[residual.get("gene", pd.Series(dtype=str)).isin(parked["gene"].astype(str))].copy()

    rows = []
    for _, row in parked.iterrows():
        gene = str(row["gene"])
        rule = MANUAL_RULES.get(gene, {})
        local = broad_sub[broad_sub["gene"].astype(str).eq(gene)]
        residual_gene = residual_sub[residual_sub["gene"].astype(str).eq(gene)]
        local_record = local.iloc[0].to_dict() if not local.empty else {}
        row_out = {
            "gene": gene,
            "wave34_score": row.get("wave34_score"),
            "gwas_catalog_trait_count": row.get("gwas_catalog_trait_count"),
            "local_positive_disease_count": row.get("local_positive_disease_count"),
            "residual_retained_disease_count": row.get("residual_retained_disease_count"),
            "ms_anchor": row.get("ms_anchor"),
            "druggable_activity_count": row.get("druggable_activity_count"),
            "chembl_target_id": row.get("chembl_target_id"),
            "chembl_pref_name": row.get("chembl_pref_name"),
            "chembl_best_nM": row.get("chembl_best_nM"),
            "clinicaltrials_autoimmune_count": row.get("clinicaltrials_autoimmune_count"),
            "europepmc_autoimmune_hit_count": row.get("europepmc_autoimmune_hit_count"),
            "wave34_failed_gates": row.get("failed_gates"),
            "broad_positive_diseases": local_record.get("positive_diseases"),
            "broad_ms_delta": local_record.get("ms_wm_delta_log2"),
            "broad_ms_p": local_record.get("ms_wm_p"),
            "residual_summary_rows": int(len(residual_gene)),
            "correct_direction_modality": rule.get("correct_direction_modality", ""),
            "prior_art_class": rule.get("prior_art_class", ""),
            "branch_specific_blocker": rule.get("branch_specific_blocker", ""),
            "wave43_call": rule.get("wave43_call", "NO_GO_UNSPECIFIED"),
            "promotion_allowed": False,
        }
        rows.append(row_out)

    out = pd.DataFrame(rows).sort_values(["wave34_score"], ascending=False)
    out.to_csv(OUT / "genetic_druggable_failfast.tsv", sep="\t", index=False)
    parked.to_csv(OUT / "wave34_parked_input_rows.tsv", sep="\t", index=False)
    broad_sub.to_csv(OUT / "broad_cellstate_rows.tsv", sep="\t", index=False)
    residual_sub.to_csv(OUT / "residual_rows.tsv", sep="\t", index=False)

    wave42_summary = {}
    if WAVE42.exists():
        wave42_summary = json.loads(WAVE42.read_text(encoding="utf-8"))

    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "n_parked_genetic_druggable_rows": int(len(out)),
        "promoted_count": int(out["promotion_allowed"].sum()),
        "wave43_call_counts": out["wave43_call"].value_counts().to_dict(),
        "inputs": {
            "wave34": rel(WAVE34),
            "broad": rel(BROAD),
            "residual": rel(RESIDUAL),
            "wave42_summary": rel(WAVE42) if WAVE42.exists() else None,
        },
        "interpretation": (
            "The full Wave34 genetics-plus-druggability parked class is closed for V3 promotion. "
            "FADS1 is parked only for future coloc/perturbation work; TYK2 and JAK2 are prior-art/generic "
            "JAK-STAT immunosuppression; NOD2 is genetically real but directionally and contextually IBD-heavy "
            "without MS/residual or correct-direction perturbation support."
        ),
        "wave42_fads_context": {
            "wave42_call": wave42_summary.get("wave42_call"),
            "promotion_status": wave42_summary.get("promotion_status"),
            "lincs_fads_perturbagen_rows": wave42_summary.get("lincs_fads_perturbagen_rows"),
        },
        "output_paths": {
            "failfast": rel(OUT / "genetic_druggable_failfast.tsv"),
            "wave34_input_rows": rel(OUT / "wave34_parked_input_rows.tsv"),
            "broad_rows": rel(OUT / "broad_cellstate_rows.tsv"),
            "residual_rows": rel(OUT / "residual_rows.tsv"),
        },
    }
    write_json(OUT / "summary.json", summary)

    report = [
        "# Wave43 Genetic-Druggable Fail-Fast",
        "",
        "## Result",
        "",
        summary["interpretation"],
        "",
        "## Calls",
        "",
        markdown_table(out),
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
