#!/usr/bin/env python3
"""Wave70 Fc/ROS-resolution candidate matrix.

Wave69 left a coherent but blocked neighborhood: FCGR2A/FCGR2B/NCF1 plus
checkpoint/costimulation/JAK comparators. This matrix asks whether inhibitory
Fc downstream regulators, myeloid inhibitory receptors, TAM/efferocytosis
nodes, or kinase mediators show enough cross-modal local evidence to justify a
deeper intervention audit.

It is a triage matrix, not a finding.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave70_fc_ros_resolution_matrix"
SEED = 20260527

WAVE68 = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
WAVE62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
RESIDUAL = ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
MS = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
WAVE37 = ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
WAVE57 = ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_intervention_first_candidate_calls.tsv"
WAVE61 = ROOT / "results_v3" / "wave61_perturbation_first_guardrail" / "intervention_evidence_tiers.tsv"
WAVE69D = ROOT / "results_v3" / "wave69d_gse282122_geneformer_remission_centroid" / "geneformer_remission_candidate_calls.tsv"
RA_COUNTS = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_counts_used.tsv"
RA_META = ROOT / "results_v3" / "wave65_gse198520_ra_synovium_antitnf_audit" / "gse198520_sample_metadata.tsv"

CANDIDATES = {
    "INPP5D": "SHIP1 inhibitory Fc/PI3K lipid phosphatase",
    "PTPN6": "SHP1 inhibitory receptor phosphatase",
    "PTPN11": "SHP2 checkpoint/inhibitory receptor phosphatase",
    "LILRB1": "myeloid inhibitory receptor",
    "LILRB2": "myeloid inhibitory receptor",
    "LILRB3": "myeloid inhibitory receptor",
    "LILRB4": "myeloid inhibitory receptor",
    "LAIR1": "collagen-binding inhibitory receptor",
    "SIGLEC10": "sialic-acid inhibitory receptor",
    "CD300A": "lipid-sensing inhibitory receptor",
    "CD300LF": "CD300 inhibitory/immune receptor",
    "BTK": "B-cell/myeloid Fc receptor kinase",
    "PIK3CD": "PI3K-delta leukocyte signaling kinase",
    "PIK3CG": "PI3K-gamma myeloid signaling kinase",
    "MERTK": "TAM efferocytosis receptor",
    "AXL": "TAM inflammatory-resolution receptor",
    "TYRO3": "TAM receptor",
    "GAS6": "TAM ligand",
    "PROS1": "TAM ligand",
    "SH2D1B": "Fc receptor signaling adaptor",
    "FCGR2A": "activating Fc-gamma receptor comparator",
    "FCGR2B": "inhibitory Fc-gamma receptor comparator",
    "NCF1": "NOX2 cytosolic subunit comparator",
    "NCF2": "NOX2 cytosolic subunit",
    "CYBB": "NOX2 catalytic subunit",
    "CYBA": "NOX2 p22phox subunit",
    "SYK": "Fc receptor kinase comparator",
    "LYN": "SRC-family Fc receptor kinase comparator",
    "BLK": "B-cell/SRC-family kinase Wave69 scout",
}

MANUAL_BLOCKERS = {
    "BTK": "BTK_MS_and_autoimmune_prior_art_clinical_saturation",
    "PIK3CD": "PI3Kdelta_immunodeficiency_infection_oncology_safety",
    "PIK3CG": "PI3Kgamma_broad_myeloid_host_defense_prior_art",
    "SYK": "SYK_prior_art_broad_immunosuppression",
    "LYN": "SRC_family_broad_selectivity_safety",
    "BLK": "myeloid_expression_missing_in_Wave69D",
    "FCGR2A": "Fc_receptor_directionality_and_safety",
    "FCGR2B": "Fc_receptor_directionality_and_safety",
    "NCF1": "NADPH_oxidase_host_defense_CGD_directionality_risk",
    "NCF2": "NADPH_oxidase_host_defense_CGD_directionality_risk",
    "CYBB": "NADPH_oxidase_host_defense_CGD_directionality_risk",
    "CYBA": "NADPH_oxidase_host_defense_CGD_directionality_risk",
    "PTPN11": "SHP2_oncology_development_and_broad_signaling",
    "AXL": "TAM_oncology_fibrosis_thrombosis_context_risk",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def f(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def s(value: Any) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return str(value)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def row_for(df: pd.DataFrame, gene: str, col: str = "gene") -> dict[str, Any]:
    if df.empty or col not in df.columns:
        return {}
    sub = df[df[col].astype(str).str.upper().eq(gene.upper())]
    if sub.empty:
        return {}
    return sub.iloc[0].to_dict()


def wave68_summary(df: pd.DataFrame, gene: str) -> dict[str, Any]:
    if df.empty:
        return {}
    sub = df[df["gene"].astype(str).str.upper().eq(gene.upper())].copy()
    if sub.empty:
        return {}
    for col in ["raw_p", "raw_fdr", "paired_p", "paired_fdr", "remission_adjusted_p", "remission_adjusted_fdr", "integrated_score"]:
        if col in sub.columns:
            sub[col] = pd.to_numeric(sub[col], errors="coerce")
    best = sub.sort_values(
        ["wave68_call_priority", "remission_adjusted_fdr", "paired_fdr", "raw_fdr", "integrated_score"],
        ascending=[True, True, True, True, False],
    ).iloc[0]
    return best.to_dict()


def ra_candidate_tests(candidates: list[str]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if not RA_COUNTS.exists() or not RA_META.exists():
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    counts = pd.read_csv(RA_COUNTS, sep="\t")
    meta = pd.read_csv(RA_META, sep="\t")
    counts["GeneSymbol"] = counts["GeneSymbol"].astype(str).str.upper()
    sub = counts[counts["GeneSymbol"].isin(candidates)].copy()
    if sub.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    sub = sub.groupby("GeneSymbol", as_index=False).sum(numeric_only=True)
    sample_cols = [c for c in sub.columns if c != "GeneSymbol"]
    libs = counts[sample_cols].sum(axis=0).replace(0, np.nan)
    expr = sub.set_index("GeneSymbol")[sample_cols].div(libs, axis=1).mul(1e6)
    expr = np.log2(expr + 1.0)
    meta = meta[meta["count_column"].isin(sample_cols)].copy()
    rows = []
    for patient, pm in meta.groupby("patient", dropna=False):
        if set(pm["timepoint"].astype(str).str.lower()) < {"pre", "post"}:
            continue
        pre_col = pm[pm["timepoint"].astype(str).str.lower().eq("pre")]["count_column"].iloc[0]
        post_col = pm[pm["timepoint"].astype(str).str.lower().eq("post")]["count_column"].iloc[0]
        info = pm.iloc[0].to_dict()
        for gene in expr.index:
            rows.append(
                {
                    "patient": patient,
                    "gene": gene,
                    "response_class": info.get("response_class"),
                    "responder_good_only": bool(info.get("responder_good_only")),
                    "responder_moderate_or_good": bool(info.get("responder_moderate_or_good")),
                    "pathotype": info.get("pathotype"),
                    "pre_log2cpm": float(expr.loc[gene, pre_col]),
                    "post_log2cpm": float(expr.loc[gene, post_col]),
                    "post_minus_pre": float(expr.loc[gene, post_col] - expr.loc[gene, pre_col]),
                }
            )
    deltas = pd.DataFrame(rows)
    paired_rows = []
    for gene, gd in deltas.groupby("gene", dropna=False):
        vals = gd["post_minus_pre"].dropna().to_numpy(float)
        if len(vals) >= 3:
            t, p = stats.ttest_1samp(vals, 0.0)
        else:
            t, p = np.nan, np.nan
        paired_rows.append(
            {
                "gene": gene,
                "n_patients": int(len(vals)),
                "mean_post_minus_pre": float(np.mean(vals)) if len(vals) else np.nan,
                "sd_post_minus_pre": float(np.std(vals, ddof=1)) if len(vals) > 1 else np.nan,
                "t": float(t) if np.isfinite(t) else np.nan,
                "p": float(p) if np.isfinite(p) else np.nan,
            }
        )
    paired = pd.DataFrame(paired_rows)
    paired["fdr"] = multipletests(paired["p"].fillna(1.0), method="fdr_bh")[1] if not paired.empty else []
    response_rows = []
    for gene, gd in deltas.groupby("gene", dropna=False):
        for label, col in [("good_vs_other", "responder_good_only"), ("modgood_vs_none", "responder_moderate_or_good")]:
            a = gd[gd[col].astype(bool)]["post_minus_pre"].dropna().to_numpy(float)
            b = gd[~gd[col].astype(bool)]["post_minus_pre"].dropna().to_numpy(float)
            if len(a) >= 3 and len(b) >= 3:
                t, p = stats.ttest_ind(a, b, equal_var=False)
            else:
                t, p = np.nan, np.nan
            response_rows.append(
                {
                    "gene": gene,
                    "contrast": label,
                    "n_true": int(len(a)),
                    "n_false": int(len(b)),
                    "mean_true": float(np.mean(a)) if len(a) else np.nan,
                    "mean_false": float(np.mean(b)) if len(b) else np.nan,
                    "delta_true_minus_false": float(np.mean(a) - np.mean(b)) if len(a) and len(b) else np.nan,
                    "p": float(p) if np.isfinite(p) else np.nan,
                }
            )
    response = pd.DataFrame(response_rows)
    response["fdr"] = multipletests(response["p"].fillna(1.0), method="fdr_bh")[1] if not response.empty else []
    return deltas, paired, response


def build_matrix() -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    candidates = sorted(CANDIDATES)
    wave68 = read_tsv(WAVE68)
    wave62 = read_tsv(WAVE62)
    broad = read_tsv(BROAD)
    residual = read_tsv(RESIDUAL)
    ms = read_tsv(MS)
    wave37 = read_tsv(WAVE37)
    wave57 = read_tsv(WAVE57)
    wave61 = read_tsv(WAVE61)
    wave69d = read_tsv(WAVE69D)
    ra_deltas, ra_paired, ra_response = ra_candidate_tests(candidates)

    rows = []
    for gene in candidates:
        w68 = wave68_summary(wave68, gene)
        w62 = row_for(wave62, gene)
        br = row_for(broad, gene)
        res = row_for(residual, gene)
        msr = row_for(ms, gene)
        eff = row_for(wave37, gene, "gene_symbol")
        gf = row_for(wave57, gene)
        pert = row_for(wave61, gene)
        gf69 = row_for(wave69d, gene)
        ra = row_for(ra_paired, gene)
        ra_resp = row_for(ra_response.sort_values("fdr") if not ra_response.empty else ra_response, gene)

        gse282122_support = min(
            f(w68.get("raw_fdr"), 1.0),
            f(w68.get("paired_fdr"), 1.0),
            f(w68.get("remission_adjusted_fdr"), 1.0),
        ) <= 0.10
        broad_support = f(br.get("positive_disease_count")) >= 3 or f(br.get("positive_fdr10_compartment_count")) >= 1
        residual_support = f(res.get("retained_positive_disease_count")) >= 2 or f(res.get("strict_core_covariate_surviving_disease_count")) >= 1
        ms_support = f(msr.get("p"), 1.0) < 0.05 and f(msr.get("delta_log2")) > 0
        ra_support = f(ra.get("fdr"), 1.0) <= 0.10
        ra_response_support = f(ra_resp.get("fdr"), 1.0) <= 0.20
        genetics_support = (
            f(w62.get("strong_l2g_disease_count")) >= 3
            or f(w62.get("strong_qtl_coloc_disease_count")) >= 3
            or f(w62.get("wave62_score")) >= 4
        )
        eff_support = "KO_ENHANCES_EFFEROCYTOSIS" in s(eff.get("screen_call"))
        model_support = (
            "REOPEN" in s(gf.get("wave57_call"))
            or "PROMOTE" in s(gf.get("wave57_call"))
            or "MODEL_SUPPORT" in s(gf69.get("wave69d_call"))
        )
        real_pert_support = "REOPEN" in s(pert.get("wave61_call")) or "PROMOTE" in s(pert.get("wave61_call"))
        blocker = MANUAL_BLOCKERS.get(gene, "")
        evidence_count = sum(
            [
                gse282122_support,
                broad_support,
                residual_support,
                ms_support,
                ra_support,
                ra_response_support,
                genetics_support,
                eff_support,
                model_support,
                real_pert_support,
            ]
        )
        score = (
            evidence_count
            + 0.5 * min(f(w62.get("wave62_score")), 8) / 2
            + 0.5 * min(f(br.get("positive_disease_count")), 5)
            + 1.0 * eff_support
            + 1.0 * model_support
            - 2.5 * bool(blocker)
        )
        if blocker:
            call = "NO_GO_BLOCKED_OR_BROAD_CLASS"
        elif evidence_count >= 4 and (eff_support or model_support or ra_support):
            call = "PARK_FC_ROS_RESOLUTION_SCOUT"
        elif evidence_count >= 3:
            call = "PARK_BIOLOGY_ONLY_NEEDS_INTERVENTION_HANDLE"
        else:
            call = "NO_GO_INSUFFICIENT_CONVERGENCE"
        rows.append(
            {
                "gene": gene,
                "route": CANDIDATES[gene],
                "wave70_call": call,
                "wave70_score": score,
                "manual_blocker": blocker,
                "evidence_count": evidence_count,
                "gse282122_support": gse282122_support,
                "gse282122_best_call": w68.get("wave68_call", ""),
                "gse282122_min_raw_fdr": f(w68.get("raw_fdr"), np.nan),
                "gse282122_min_paired_fdr": f(w68.get("paired_fdr"), np.nan),
                "gse282122_min_adjusted_fdr": f(w68.get("remission_adjusted_fdr"), np.nan),
                "broad_support": broad_support,
                "broad_positive_disease_count": f(br.get("positive_disease_count")),
                "broad_positive_fdr10_compartment_count": f(br.get("positive_fdr10_compartment_count")),
                "broad_positive_diseases": br.get("positive_diseases", ""),
                "residual_support": residual_support,
                "residual_retained_positive_disease_count": f(res.get("retained_positive_disease_count")),
                "ms_support": ms_support,
                "ms_delta_log2": f(msr.get("delta_log2"), np.nan),
                "ms_p": f(msr.get("p"), np.nan),
                "ms_fdr": f(msr.get("fdr"), np.nan),
                "ra_support": ra_support,
                "ra_mean_post_minus_pre": f(ra.get("mean_post_minus_pre"), np.nan),
                "ra_paired_fdr": f(ra.get("fdr"), np.nan),
                "ra_response_support": ra_response_support,
                "ra_best_response_contrast": ra_resp.get("contrast", ""),
                "ra_best_response_delta": f(ra_resp.get("delta_true_minus_false"), np.nan),
                "ra_best_response_fdr": f(ra_resp.get("fdr"), np.nan),
                "genetics_support": genetics_support,
                "wave62_score": f(w62.get("wave62_score")),
                "wave62_call": w62.get("wave62_call", ""),
                "strong_l2g_diseases": w62.get("strong_l2g_diseases", ""),
                "strong_qtl_coloc_diseases": w62.get("strong_qtl_coloc_diseases", ""),
                "eff_support": eff_support,
                "efferocytosis_screen_call": eff.get("screen_call", ""),
                "efferocytosis_delta": f(eff.get("median_efficient_minus_noneater_lfc"), np.nan),
                "efferocytosis_fdr": f(eff.get("contrast_fdr"), np.nan),
                "model_support": model_support,
                "wave57_call": gf.get("wave57_call", ""),
                "wave69d_call": gf69.get("wave69d_call", ""),
                "real_pert_support": real_pert_support,
                "wave61_call": pert.get("wave61_call", ""),
                "wave61_manual_blocker": pert.get("manual_blocker", ""),
            }
        )
    matrix = pd.DataFrame(rows).sort_values(["wave70_call", "wave70_score"], ascending=[True, False])
    extras = {"ra_deltas": ra_deltas, "ra_paired": ra_paired, "ra_response": ra_response}
    return matrix, extras


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        vals = []
        for col in cols:
            value = "" if pd.isna(row[col]) else str(row[col])
            vals.append(value.replace("\n", " ").replace("|", "\\|")[:500])
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    matrix, extras = build_matrix()
    matrix.to_csv(OUT / "fc_ros_resolution_candidate_matrix.tsv", sep="\t", index=False)
    for name, df in extras.items():
        df.to_csv(OUT / f"{name}.tsv", sep="\t", index=False)
    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "candidate_count": len(matrix),
        "call_counts": matrix["wave70_call"].value_counts().to_dict(),
        "top_rows": matrix.head(20)[
            ["gene", "wave70_call", "wave70_score", "evidence_count", "manual_blocker"]
        ].to_dict("records"),
        "interpretation": "Wave70 matrix is a triage gate for Fc/ROS-resolution routes; PARK rows require hostile prior-art and direct perturbation follow-up.",
        "inputs": {
            "wave68": rel(WAVE68),
            "wave62": rel(WAVE62),
            "broad": rel(BROAD),
            "residual": rel(RESIDUAL),
            "ms": rel(MS),
            "wave37": rel(WAVE37),
            "wave57": rel(WAVE57),
            "wave61": rel(WAVE61),
            "wave69d": rel(WAVE69D),
            "ra_counts": rel(RA_COUNTS),
            "ra_meta": rel(RA_META),
        },
    }
    write_json(OUT / "summary.json", summary)
    cols = [
        "gene",
        "route",
        "wave70_call",
        "wave70_score",
        "evidence_count",
        "manual_blocker",
        "gse282122_support",
        "broad_support",
        "residual_support",
        "ms_support",
        "ra_support",
        "ra_response_support",
        "genetics_support",
        "eff_support",
        "model_support",
        "real_pert_support",
    ]
    report = [
        "# Wave70 Fc/ROS Resolution Candidate Matrix",
        "",
        "## Verdict",
        "",
        f"Calls: `{summary['call_counts']}`.",
        "",
        "This is a triage matrix. A parked row is not a therapeutic claim.",
        "",
        "## Candidate Matrix",
        "",
        markdown_table(matrix[[c for c in cols if c in matrix.columns]].head(40)),
        "",
        "## Guardrails",
        "",
        "- RA anti-TNF bulk pharmacodynamics are not cell-resolved controller evidence.",
        "- Efferocytosis CRISPR support is mouse macrophage phagocytosis biology, not autoimmune disease efficacy.",
        "- Prior-art and safety blockers are conservative; sidecar prior-art review must vet any parked route before promotion.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
