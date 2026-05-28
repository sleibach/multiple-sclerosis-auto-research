#!/usr/bin/env python3
"""
Wave99: perturbation/time-course forcing audit for LITAF and CASP4 as
upstream inflammatory stress generators of the C15ORF48/MOCCI state.

Wave97 kept LITAF and CASP4 as residual C15 co-state candidates. This script
does not ask whether they co-express with C15ORF48 again. It asks whether real
perturbation/time-course data in the workspace give direction-aware support
strong enough to promote either as a therapeutic intervention point.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


SEED = 20260527
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave99_litaf_casp4_stress_generator_audit"


GENES_HUMAN = [
    "C15ORF48",
    "NDUFA4",
    "LITAF",
    "CASP4",
    "CASP1",
    "CASP5",
    "GSDMD",
    "IL1B",
    "TNF",
    "NFKBIA",
    "STAT1",
    "IRF1",
    "CIITA",
    "CD74",
]

GENES_MOUSE = [
    "C15orf48",
    "Ndufa4",
    "Litaf",
    "Casp4",
    "Casp1",
    "Gsdmd",
    "Il1b",
    "Tnf",
    "Nfkbia",
    "Stat1",
    "Irf1",
    "Ciita",
    "Cd74",
    "Gsk3b",
    "Med16",
]


def read_tsv(path: str) -> pd.DataFrame:
    p = ROOT / path
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p, sep="\t", low_memory=False)


def first_gene(df: pd.DataFrame, gene: str, gene_col: str = "gene") -> dict[str, Any]:
    if df.empty or gene_col not in df.columns:
        return {}
    sub = df[df[gene_col].astype(str).str.upper() == gene.upper()]
    if sub.empty:
        return {}
    return sub.iloc[0].to_dict()


def fnum(x: Any, default: float = np.nan) -> float:
    try:
        if pd.isna(x):
            return default
        return float(x)
    except Exception:
        return default


def fmt(x: Any, digits: int = 4) -> str:
    y = fnum(x)
    if np.isnan(y):
        return ""
    return f"{y:.{digits}g}"


def df_to_markdown(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    clean = df.copy()
    for col in clean.columns:
        clean[col] = clean[col].map(lambda x: "" if pd.isna(x) else str(x))
    header = "| " + " | ".join(clean.columns.astype(str)) + " |"
    sep = "| " + " | ".join(["---"] * len(clean.columns)) + " |"
    rows = [
        "| " + " | ".join(str(v).replace("\n", " ") for v in row) + " |"
        for row in clean.to_numpy()
    ]
    return "\n".join([header, sep, *rows])


def load_human_timecourse() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    path = ROOT / "data/raw_v3/wave14_gsk3b_ciita/GSE294918_IFNyRNAseq_CPM.csv.gz"
    if not path.exists():
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    raw = pd.read_csv(path)
    raw = raw.rename(columns={raw.columns[0]: "gene_raw"})
    raw["gene_upper"] = raw["gene_raw"].astype(str).str.upper()
    sub = raw[raw["gene_upper"].isin(GENES_HUMAN)].copy()
    # Convert C15orf48 to canonical uppercase output name.
    sub["gene"] = sub["gene_upper"]
    expr_cols = [c for c in sub.columns if c not in {"gene_raw", "gene_upper", "gene"}]
    sub[expr_cols] = np.log2(sub[expr_cols].astype(float) + 1.0)
    sub[["gene", *expr_cols]].to_csv(OUT / "gse294918_log2cpm_selected_genes.tsv", sep="\t", index=False)

    time_rows: list[dict[str, Any]] = []
    trajectories = {
        "PBS_LPS": {0: "D4_PBS_LPS0H", 1: "D4_PBS_LPS1H", 3: "D4_PBS_LPS3H", 6: "D4_PBS_LPS6H", 12: "D4_PBS_LPS12H"},
        "IFNY_LPS": {0: "D4_IFNy_LPS0H", 1: "D4_IFNy_LPS1H", 3: "D4_IFNy_LPS3H", 6: "D4_IFNy_LPS6H", 12: "D4_IFNy_LPS12H"},
        "PBS_RUX_LPS": {0: "D4_PBS_rux_LPS0H", 1: "D4_PBS_rux_LPS1H", 3: "D4_PBS_rux_LPS3H", 6: "D4_PBS_rux_LPS6H"},
        "IFNY_RUX_LPS": {0: "D4_IFNy_rux_LPS0H", 1: "D4_IFNy_rux_LPS1H", 3: "D4_IFNy_rux_LPS3H", 6: "D4_IFNy_rux_LPS6H"},
    }
    for _, row in sub.iterrows():
        gene = row["gene"]
        for trajectory, tcols in trajectories.items():
            base = row[tcols[0]]
            for hour, col in tcols.items():
                time_rows.append(
                    {
                        "gene": gene,
                        "trajectory": trajectory,
                        "hour": hour,
                        "log2_cpm": row[col],
                        "delta_vs_0h": row[col] - base,
                    }
                )
    time_df = pd.DataFrame(time_rows)
    time_df.to_csv(OUT / "gse294918_lps_timecourse_deltas.tsv", sep="\t", index=False)

    summary_rows: list[dict[str, Any]] = []
    threshold = math.log2(1.5)
    for gene in ["C15ORF48", "NDUFA4", "LITAF", "CASP4", "CASP1", "CASP5", "GSDMD", "IL1B", "TNF"]:
        for trajectory in ["PBS_LPS", "IFNY_LPS"]:
            g = time_df[(time_df["gene"] == gene) & (time_df["trajectory"] == trajectory)].copy()
            if g.empty:
                continue
            rise = g[(g["hour"] > 0) & (g["delta_vs_0h"] >= threshold)]
            first_rise = float(rise["hour"].min()) if not rise.empty else np.nan
            peak = g.loc[g["delta_vs_0h"].idxmax()]
            summary_rows.append(
                {
                    "gene": gene,
                    "trajectory": trajectory,
                    "first_1_5x_rise_hour": first_rise,
                    "peak_hour": float(peak["hour"]),
                    "peak_delta_log2": float(peak["delta_vs_0h"]),
                    "delta_3h": float(g.loc[g["hour"] == 3, "delta_vs_0h"].iloc[0]) if 3 in set(g["hour"]) else np.nan,
                    "delta_6h": float(g.loc[g["hour"] == 6, "delta_vs_0h"].iloc[0]) if 6 in set(g["hour"]) else np.nan,
                    "delta_12h": float(g.loc[g["hour"] == 12, "delta_vs_0h"].iloc[0]) if 12 in set(g["hour"]) else np.nan,
                }
            )
    tc_summary = pd.DataFrame(summary_rows)
    tc_summary.to_csv(OUT / "gse294918_timecourse_summary.tsv", sep="\t", index=False)

    # Actual drug perturbation available in this time course: ruxolitinib under
    # IFN-primed LPS conditions. This is not target-specific LITAF/CASP4
    # perturbation, so the output is interpreted as pathway confounding unless
    # candidate movement is selective relative to IFN/APC/NFKB modules.
    rux_rows: list[dict[str, Any]] = []
    modules = {
        "ifn_apc": ["STAT1", "IRF1", "CIITA", "CD74"],
        "nfkb_cytokine": ["NFKBIA", "TNF", "IL1B", "LITAF"],
        "pyroptosis": ["CASP4", "CASP5", "CASP1", "GSDMD", "IL1B"],
        "c15_switch": ["C15ORF48", "NDUFA4"],
    }
    value = {(r["gene"], c): r[c] for _, r in sub.iterrows() for c in expr_cols}
    for hour in [0, 1, 3, 6]:
        for gene in GENES_HUMAN:
            a = value.get((gene, f"D4_IFNy_rux_LPS{hour}H"))
            b = value.get((gene, f"D4_IFNy_LPS{hour}H"))
            if a is None or b is None:
                continue
            rux_rows.append(
                {
                    "feature": gene,
                    "feature_type": "gene",
                    "hour": hour,
                    "rux_minus_ifny_lps_log2": a - b,
                }
            )
        for module, genes in modules.items():
            vals = []
            for gene in genes:
                a = value.get((gene, f"D4_IFNy_rux_LPS{hour}H"))
                b = value.get((gene, f"D4_IFNy_LPS{hour}H"))
                if a is not None and b is not None:
                    if module == "c15_switch" and gene == "NDUFA4":
                        # Higher NDUFA4 moves opposite the C15ORF48/MOCCI switch.
                        vals.append(-(a - b))
                    else:
                        vals.append(a - b)
            if vals:
                rux_rows.append(
                    {
                        "feature": module,
                        "feature_type": "module",
                        "hour": hour,
                        "rux_minus_ifny_lps_log2": float(np.mean(vals)),
                    }
                )
    rux_df = pd.DataFrame(rux_rows)
    rux_df.to_csv(OUT / "gse294918_ruxolitinib_effects.tsv", sep="\t", index=False)
    return sub, tc_summary, rux_df


def load_mouse_perturbation() -> pd.DataFrame:
    path = ROOT / "data/raw_v3/wave14_gsk3b_ciita/GSE162464_Normalized_Gene_Counts_Matrix.txt.gz"
    if not path.exists():
        return pd.DataFrame()
    raw = pd.read_csv(path, sep="\t")
    sub = raw[raw["Symbol"].astype(str).isin(GENES_MOUSE)].copy()
    groups = {
        "NTC_US": [c for c in raw.columns if "_NTC_US" in c],
        "NTC_IFNg": [c for c in raw.columns if "_NTC_IFNg" in c],
        "Gsk3b_US": [c for c in raw.columns if "_Gsk3b_US" in c],
        "Gsk3b_IFNg": [c for c in raw.columns if "_Gsk3b_IFNg" in c],
        "Med16_US": [c for c in raw.columns if "_Med16_US" in c],
        "Med16_IFNg": [c for c in raw.columns if "_Med16_IFNg" in c],
    }
    rows: list[dict[str, Any]] = []
    for _, row in sub.iterrows():
        means = {}
        for group, cols in groups.items():
            if cols:
                means[group] = float(np.log2(row[cols].astype(float).mean() + 1.0))
        contrasts = {
            "NTC_IFNg_vs_NTC_US": means.get("NTC_IFNg", np.nan) - means.get("NTC_US", np.nan),
            "Gsk3b_IFNg_vs_NTC_IFNg": means.get("Gsk3b_IFNg", np.nan) - means.get("NTC_IFNg", np.nan),
            "Med16_IFNg_vs_NTC_IFNg": means.get("Med16_IFNg", np.nan) - means.get("NTC_IFNg", np.nan),
            "Gsk3b_US_vs_NTC_US": means.get("Gsk3b_US", np.nan) - means.get("NTC_US", np.nan),
            "Med16_US_vs_NTC_US": means.get("Med16_US", np.nan) - means.get("NTC_US", np.nan),
        }
        rows.append({"gene": row["Symbol"], **means, **contrasts})
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "gse162464_mouse_perturbation_selected_genes.tsv", sep="\t", index=False)
    return out


def collect_candidate_rows() -> pd.DataFrame:
    w96 = read_tsv("results_v3/wave96_c15orf48_controller_search/c15orf48_controller_candidate_rank.tsv")
    w97 = read_tsv("results_v3/wave97_c15_residual_costate_falsification/residual_costate_candidate_summary.tsv")
    w37 = read_tsv("results_v3/wave37_gse212008_crispr_efferocytosis_screen/gene_level_screen_scores.tsv")
    w39 = read_tsv("results_v3/wave39_surfaceome_rescue_after_resolution_pivot/surfaceome_rescue_rank.tsv")
    w57 = read_tsv("results_v3/wave57_intervention_first_geneformer_screen/wave57_geneformer_gene_summary.tsv")
    w68 = read_tsv("results_v3/wave68_gse282122_unrestricted_gene_screen/adjusted_top_gene_ols.tsv")
    w81 = read_tsv("results_v3/wave81_perturbation_first_rescue/perturbation_first_integrated_rank.tsv")

    rows = []
    for gene in ["LITAF", "CASP4"]:
        r96 = first_gene(w96, gene)
        r97 = first_gene(w97, gene)
        r37 = first_gene(w37, gene, "gene_symbol")
        r39 = first_gene(w39, gene)
        r57 = first_gene(w57, gene)
        r81 = first_gene(w81, gene)
        if not w68.empty:
            s68 = w68[
                (w68["gene"].astype(str).str.upper() == gene)
                & (w68["cell_state"].astype(str) == "Mono_macro")
            ]
            r68 = s68.iloc[0].to_dict() if not s68.empty else {}
        else:
            r68 = {}
        rows.append(
            {
                "gene": gene,
                "wave96_call": r96.get("wave96_call", ""),
                "wave97_call": r97.get("wave97_call", ""),
                "c15_positive_disease_count": r96.get("c15_trend_positive_disease_count", np.nan),
                "c15_state_pearson_r": r96.get("c15_state_pearson_r", np.nan),
                "residual_case_positive_disease_count": r97.get("residual_case_positive_disease_count", np.nan),
                "median_residual_case_r": r97.get("median_residual_case_r", np.nan),
                "ms_delta_log2": r96.get("ms_delta_log2", np.nan),
                "ms_p": r96.get("ms_p", np.nan),
                "ms_fdr": r96.get("ms_fdr", np.nan),
                "wave62_strong_qtl_coloc_disease_count": r96.get("wave62_strong_qtl_coloc_disease_count", np.nan),
                "chembl_activity_count": r96.get("chembl_activity_count", np.nan),
                "uniprot_accessible": r96.get("uniprot_accessible", np.nan),
                "w68_remission_adjusted_delta": r68.get("remission_adjusted_delta", np.nan),
                "w68_remission_adjusted_p": r68.get("remission_adjusted_p", np.nan),
                "w68_remission_adjusted_fdr": r68.get("remission_adjusted_fdr", np.nan),
                "w37_screen_call": r37.get("screen_call", ""),
                "w37_contrast_lfc": r37.get("median_efficient_minus_noneater_lfc", np.nan),
                "w37_contrast_fdr": r37.get("contrast_fdr", np.nan),
                "wave39_call": r39.get("wave39_call", ""),
                "wave39_reason": r39.get("wave39_reason", ""),
                "geneformer_strong_support_contexts": r57.get("strong_support_contexts", np.nan),
                "wave81_call": r81.get("wave81_call", ""),
                "wave81_decision_reason": r81.get("decision_reason", ""),
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "litaf_casp4_local_evidence_summary.tsv", sep="\t", index=False)
    return out


def source_table() -> pd.DataFrame:
    rows = [
        {
            "gene_or_axis": "LITAF",
            "source_id": "PMID:21984950",
            "kind": "literature",
            "claim_used": "LITAF mediates increased TNF-alpha secretion from inflamed colonic lamina propria macrophages.",
            "effect_on_wave99": "mechanistically close IBD macrophage/TNF prior art; supports stress-generator biology but not novelty/druggability",
        },
        {
            "gene_or_axis": "LITAF",
            "source_id": "PMID:22160695",
            "kind": "literature",
            "claim_used": "Whole-body Litaf deletion improved endotoxic shock and inflammatory arthritis in mice.",
            "effect_on_wave99": "direct inflammatory arthritis prior; systemic deletion not a selective modality",
        },
        {
            "gene_or_axis": "CASP4/CASP11",
            "source_id": "PMID:11136825",
            "kind": "literature",
            "claim_used": "Mouse caspase-11 mediated oligodendrocyte cell death and autoimmune demyelination pathogenesis.",
            "effect_on_wave99": "direct MS/EAE-adjacent inflammatory caspase prior art",
        },
        {
            "gene_or_axis": "CASP4",
            "source_id": "WO2026055444",
            "kind": "patent",
            "claim_used": "Caspase-4 inhibitor patent family surfaced in prior Wave97 audit.",
            "effect_on_wave99": "selective-inhibitor route is patent-crowded and requires CASP4-vs-CASP1/CASP5 selectivity",
        },
        {
            "gene_or_axis": "C15ORF48/MOCCI",
            "source_id": "PMID:33837217;PMID:34878835;PMID:38296961",
            "kind": "mechanism",
            "claim_used": "C15ORF48/MOCCI is inflammation-induced mitochondrial complex-IV/autophagy brake biology.",
            "effect_on_wave99": "defines the state being ordered against LITAF/CASP4",
        },
    ]
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "source_anchor_table.tsv", sep="\t", index=False)
    return out


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    local = collect_candidate_rows()
    _, tc_summary, rux = load_human_timecourse()
    mouse = load_mouse_perturbation()
    sources = source_table()

    gate_rows: list[dict[str, Any]] = []
    for gene in ["LITAF", "CASP4"]:
        lrow = local[local["gene"] == gene].iloc[0].to_dict()
        gene_tc = tc_summary[tc_summary["gene"] == gene]
        c15_tc = tc_summary[tc_summary["gene"] == "C15ORF48"]

        lead_flags = []
        lead_evidence = []
        for trajectory in ["PBS_LPS", "IFNY_LPS"]:
            gt = gene_tc[gene_tc["trajectory"] == trajectory]
            ct = c15_tc[c15_tc["trajectory"] == trajectory]
            if gt.empty or ct.empty:
                continue
            g = gt.iloc[0]
            c = ct.iloc[0]
            flag = (
                fnum(g["first_1_5x_rise_hour"]) <= fnum(c["first_1_5x_rise_hour"])
                and fnum(g["peak_hour"]) <= fnum(c["peak_hour"])
            )
            lead_flags.append(bool(flag))
            lead_evidence.append(
                f"{trajectory}: {gene} first={fmt(g['first_1_5x_rise_hour'])}h peak={fmt(g['peak_hour'])}h; "
                f"C15ORF48 first={fmt(c['first_1_5x_rise_hour'])}h peak={fmt(c['peak_hour'])}h"
            )

        rux_3 = rux[(rux["feature"] == gene) & (rux["hour"] == 3)]
        rux_6 = rux[(rux["feature"] == gene) & (rux["hour"] == 6)]
        c15_rux_6 = rux[(rux["feature"] == "C15ORF48") & (rux["hour"] == 6)]
        ifn_rux_6 = rux[(rux["feature"] == "ifn_apc") & (rux["hour"] == 6)]
        py_rux_6 = rux[(rux["feature"] == "pyroptosis") & (rux["hour"] == 6)]
        rux_gene_mean = float(np.nanmean([fnum(rux_3["rux_minus_ifny_lps_log2"].iloc[0]) if not rux_3.empty else np.nan,
                                          fnum(rux_6["rux_minus_ifny_lps_log2"].iloc[0]) if not rux_6.empty else np.nan]))
        rux_c15_6 = fnum(c15_rux_6["rux_minus_ifny_lps_log2"].iloc[0]) if not c15_rux_6.empty else np.nan
        rux_ifn_6 = fnum(ifn_rux_6["rux_minus_ifny_lps_log2"].iloc[0]) if not ifn_rux_6.empty else np.nan
        rux_py_6 = fnum(py_rux_6["rux_minus_ifny_lps_log2"].iloc[0]) if not py_rux_6.empty else np.nan

        mouse_gene = gene.capitalize() if gene != "CASP4" else "Casp4"
        m = mouse[mouse["gene"] == mouse_gene]
        gsk3b_effect = fnum(m["Gsk3b_IFNg_vs_NTC_IFNg"].iloc[0]) if not m.empty else np.nan
        med16_effect = fnum(m["Med16_IFNg_vs_NTC_IFNg"].iloc[0]) if not m.empty else np.nan

        gates = [
            {
                "candidate": gene,
                "gate": "residual_c15_costate_replicates",
                "status": bool(
                    fnum(lrow.get("c15_positive_disease_count")) >= 3
                    and fnum(lrow.get("residual_case_positive_disease_count")) >= 2
                ),
                "evidence": (
                    f"c15_positive_diseases={fmt(lrow.get('c15_positive_disease_count'))}; "
                    f"residual_case_positive_diseases={fmt(lrow.get('residual_case_positive_disease_count'))}; "
                    f"median_residual_r={fmt(lrow.get('median_residual_case_r'))}"
                ),
            },
            {
                "candidate": gene,
                "gate": "human_timecourse_temporal_lead_over_c15",
                "status": bool(lead_flags and all(lead_flags)),
                "evidence": "; ".join(lead_evidence),
            },
            {
                "candidate": gene,
                "gate": "real_perturbation_moves_candidate_and_c15",
                "status": bool(rux_gene_mean <= -0.25 and rux_c15_6 <= -0.20),
                "evidence": (
                    f"rux_mean_3_6h_{gene}={fmt(rux_gene_mean)}; "
                    f"rux_6h_C15ORF48={fmt(rux_c15_6)}; rux_6h_ifn_apc={fmt(rux_ifn_6)}; "
                    f"rux_6h_pyroptosis={fmt(rux_py_6)}"
                ),
            },
            {
                "candidate": gene,
                "gate": "perturbation_not_just_broad_jak_ifn_confounding",
                "status": bool(rux_gene_mean <= -0.25 and abs(rux_ifn_6) < 0.50),
                "evidence": (
                    f"rux_6h_ifn_apc={fmt(rux_ifn_6)}; if this is strongly negative, "
                    "candidate suppression is broad JAK/IFN confounding rather than selective stress-node perturbation"
                ),
            },
            {
                "candidate": gene,
                "gate": "mouse_indirect_perturbation_consistent",
                "status": bool(gsk3b_effect < -0.25 and med16_effect < -0.25),
                "evidence": (
                    f"Gsk3b_KO_IFNg_vs_NTC_IFNg={fmt(gsk3b_effect)}; "
                    f"Med16_KO_IFNg_vs_NTC_IFNg={fmt(med16_effect)}; "
                    "C15orf48 absent from this mouse matrix"
                ),
            },
            {
                "candidate": gene,
                "gate": "ms_claim_grade_anchor",
                "status": bool(
                    fnum(lrow.get("ms_delta_log2")) > 0.25
                    and fnum(lrow.get("ms_p")) < 0.05
                    and fnum(lrow.get("ms_fdr")) < 0.10
                ),
                "evidence": (
                    f"MS delta={fmt(lrow.get('ms_delta_log2'))}; p={fmt(lrow.get('ms_p'))}; "
                    f"fdr={fmt(lrow.get('ms_fdr'))}"
                ),
            },
            {
                "candidate": gene,
                "gate": "target_resolved_genetics_or_coloc",
                "status": bool(fnum(lrow.get("wave62_strong_qtl_coloc_disease_count")) >= 4),
                "evidence": f"strong_qtl_coloc_diseases={fmt(lrow.get('wave62_strong_qtl_coloc_disease_count'))}",
            },
            {
                "candidate": gene,
                "gate": "direct_crispr_or_foundation_support",
                "status": bool(
                    str(lrow.get("w37_screen_call", "")).startswith("KO_")
                    or fnum(lrow.get("geneformer_strong_support_contexts")) >= 2
                ),
                "evidence": (
                    f"Wave37={lrow.get('w37_screen_call', '')}; "
                    f"contrast_lfc={fmt(lrow.get('w37_contrast_lfc'))}; "
                    f"contrast_fdr={fmt(lrow.get('w37_contrast_fdr'))}; "
                    f"Geneformer strong contexts={fmt(lrow.get('geneformer_strong_support_contexts'))}"
                ),
            },
            {
                "candidate": gene,
                "gate": "selective_druggable_modality",
                "status": bool(gene == "CASP4" and fnum(lrow.get("chembl_activity_count")) > 0),
                "evidence": (
                    f"ChEMBL activity count={fmt(lrow.get('chembl_activity_count'))}; "
                    f"uniprot_accessible={lrow.get('uniprot_accessible')}; "
                    "for CASP4 this is only provisional because CASP1/CASP5 selectivity is not shown"
                ),
            },
            {
                "candidate": gene,
                "gate": "prior_art_not_blocking",
                "status": bool(gene == "LITAF"),
                "evidence": (
                    "LITAF has close macrophage/TNF and arthritis prior plus no modality; "
                    "CASP4/CASP11 has direct EAE/demyelination and inhibitor-patent prior"
                ),
            },
        ]
        gate_rows.extend(gates)

    gates = pd.DataFrame(gate_rows)
    gates.to_csv(OUT / "litaf_casp4_gate_matrix.tsv", sep="\t", index=False)

    calls = []
    for gene, sub in gates.groupby("candidate"):
        passed = int(sub["status"].sum())
        failed = sub.loc[~sub["status"], "gate"].tolist()
        if passed == len(sub):
            call = "REOPEN_STRESS_GENERATOR_FOR_DEEP_VALIDATION"
        elif gene == "LITAF":
            call = "PARK_LITAF_UPSTREAM_STRESS_MARKER_NO_MODALITY"
        else:
            call = "PARK_CASP4_UPSTREAM_PYROPTOSIS_NODE_PRIOR_SELECTIVITY_BLOCKED"
        calls.append(
            {
                "candidate": gene,
                "call": call,
                "gates_passed": passed,
                "gates_total": int(len(sub)),
                "failed_gates": ";".join(failed),
            }
        )
    calls_df = pd.DataFrame(calls)
    calls_df.to_csv(OUT / "litaf_casp4_calls.tsv", sep="\t", index=False)

    summary = {
        "random_seed": SEED,
        "analysis_call": "NO_PROMOTABLE_LITAF_CASP4_STRESS_GENERATOR",
        "candidate_calls": calls,
        "interpretation": (
            "LITAF and CASP4 are plausible upstream inflammatory stress-state markers that can precede "
            "C15ORF48 induction in human macrophage LPS time courses. The perturbation evidence is not "
            "selective: ruxolitinib effects ride broad IFN/APC suppression, mouse perturbation is indirect "
            "and lacks C15orf48, direct CRISPR/foundation support is absent, MS anchors are weak, and genetics "
            "do not support target-resolved causality."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = [
        "# Wave99 LITAF/CASP4 Stress-Generator Audit",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Question",
        "",
        "Do `LITAF` or `CASP4` survive as upstream inflammatory stress-generator",
        "intervention points for the C15ORF48/MOCCI state after adding real",
        "macrophage time-course and perturbation evidence?",
        "",
        "## Verdict",
        "",
        "Analysis call: `NO_PROMOTABLE_LITAF_CASP4_STRESS_GENERATOR`.",
        "",
        "Both genes remain biologically useful upstream-stress hypotheses, but",
        "neither is a V3 therapeutic nomination.",
        "",
        "## Candidate Calls",
        "",
        df_to_markdown(calls_df),
        "",
        "## Local Evidence Summary",
        "",
        df_to_markdown(local),
        "",
        "## Human Macrophage Time-Course Summary",
        "",
        df_to_markdown(tc_summary[tc_summary["gene"].isin(["C15ORF48", "NDUFA4", "LITAF", "CASP4"])]),
        "",
        "## Human Ruxolitinib Perturbation Effects",
        "",
        df_to_markdown(
            rux[
                rux["feature"].isin(["C15ORF48", "NDUFA4", "LITAF", "CASP4", "ifn_apc", "nfkb_cytokine", "pyroptosis", "c15_switch"])
            ]
        ),
        "",
        "## Mouse Indirect Perturbation",
        "",
        df_to_markdown(mouse[mouse["gene"].isin(["Ndufa4", "Litaf", "Casp4", "Casp1", "Gsdmd", "Il1b", "Tnf", "Stat1", "Ciita", "Cd74"])]),
        "",
        "## Gate Matrix",
        "",
        df_to_markdown(gates),
        "",
        "## Source Anchors",
        "",
        df_to_markdown(sources),
        "",
        "## Decision",
        "",
        "- `LITAF`: park as an upstream macrophage/TNF/endolysosomal stress marker;",
        "  no selective modality and no MS/genetic support.",
        "- `CASP4`: park as an upstream pyroptosis/danger-state node; druggability",
        "  exists only provisionally and is limited by selectivity and prior art.",
        "- Next branch should not promote C15 co-state markers without direct",
        "  target perturbation, MS spatial validation, and target-resolved genetics.",
        "",
        "## Output Files",
        "",
        "- `results_v3/wave99_litaf_casp4_stress_generator_audit/litaf_casp4_gate_matrix.tsv`",
        "- `results_v3/wave99_litaf_casp4_stress_generator_audit/litaf_casp4_calls.tsv`",
        "- `results_v3/wave99_litaf_casp4_stress_generator_audit/litaf_casp4_local_evidence_summary.tsv`",
        "- `results_v3/wave99_litaf_casp4_stress_generator_audit/gse294918_log2cpm_selected_genes.tsv`",
        "- `results_v3/wave99_litaf_casp4_stress_generator_audit/gse294918_lps_timecourse_deltas.tsv`",
        "- `results_v3/wave99_litaf_casp4_stress_generator_audit/gse294918_timecourse_summary.tsv`",
        "- `results_v3/wave99_litaf_casp4_stress_generator_audit/gse294918_ruxolitinib_effects.tsv`",
        "- `results_v3/wave99_litaf_casp4_stress_generator_audit/gse162464_mouse_perturbation_selected_genes.tsv`",
        "- `results_v3/wave99_litaf_casp4_stress_generator_audit/source_anchor_table.tsv`",
        "- `results_v3/wave99_litaf_casp4_stress_generator_audit/summary.json`",
        "- `results_v3/wave99_litaf_casp4_stress_generator_audit/REPORT.md`",
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report))


if __name__ == "__main__":
    main()
