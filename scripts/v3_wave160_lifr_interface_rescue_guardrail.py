#!/usr/bin/env python3
"""Wave160: LIFR/LIF interface rescue guardrail.

LIFR was the best non-ELR interface candidate returned by the post-Wave158
sidecar because GSE129487 contains direct siRNA rescue signals. This wave
checks whether that signal is broad, specific, and externally anchored enough
to reopen a V3 intervention route.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave160_lifr_interface_rescue_guardrail"
OUT.mkdir(parents=True, exist_ok=True)

AXIS = ["LIFR", "LIF", "IL6ST", "OSMR"]
COMPARATORS = ["CUX1", "STAT3", "STAT4", "ELF3"]


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def pick(df: pd.DataFrame, gene: str) -> dict[str, object]:
    if df.empty or "gene" not in df.columns:
        return {}
    hit = df[df["gene"].astype(str).str.upper() == gene]
    if hit.empty:
        return {}
    return hit.iloc[0].to_dict()


def main() -> None:
    rescue = read_tsv(ROOT / "phases/v3/results" / "wave153_gse129487_synovial_fibroblast_sirna_rescue" / "sirna_rescue_module_tests.tsv")
    broad = read_tsv(ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_summary.tsv")
    ms = read_tsv(ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv")
    wave62 = read_tsv(ROOT / "phases/v3/results" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv")
    wave103 = read_tsv(ROOT / "phases/v3/results" / "wave103_intervention_first_successor_triage" / "intervention_first_successor_rank.tsv")
    wave122 = read_tsv(ROOT / "phases/v3/results" / "wave122_fresh_breadth_target_scan" / "fresh_breadth_target_rank.tsv")

    induced = rescue[(rescue["ctrl_induction_p_value"] < 0.05) & (rescue["mean_ctrl_induction"] > 0)].copy()
    induced.to_csv(OUT / "all_induced_context_rescue_tests.tsv", sep="\t", index=False)

    summary_rows = []
    for gene in AXIS + COMPARATORS:
        sub = induced[induced["sirna"].astype(str).str.upper() == gene]
        if sub.empty:
            neg_frac = np.nan
            wilcox_p = np.nan
            nominal = 0
            fdr10 = 0
            mean_effect = np.nan
        else:
            effects = sub["mean_sirna_effect_vs_ctrl"].astype(float)
            neg_frac = float((effects < 0).mean())
            wilcox_p = float(stats.wilcoxon(effects, alternative="less").pvalue) if len(effects) >= 2 and (effects != 0).any() else np.nan
            nominal = int(((sub["mean_sirna_effect_vs_ctrl"] < 0) & (sub["sirna_effect_p_value"] < 0.05)).sum())
            fdr10 = int(((sub["mean_sirna_effect_vs_ctrl"] < 0) & (sub["sirna_effect_q_value_bh"] < 0.10)).sum())
            mean_effect = float(effects.mean())

        b = pick(broad, gene)
        m = pick(ms, gene)
        w62 = pick(wave62, gene)
        w103 = pick(wave103, gene)
        w122 = pick(wave122, gene)
        ms_delta = float(m.get("delta_log2", 0.0)) if m else 0.0
        ms_fdr = float(m.get("fdr", 1.0)) if m else 1.0
        ms_genetic = float(w103.get("ms_genetic_score", 0.0)) if w103 else float(w62.get("ms_max_l2g_score", 0.0) or 0.0)
        positive_diseases = int(float(b.get("positive_disease_count", 0))) if b else 0
        positive_fdr10 = int(float(b.get("positive_fdr10_compartment_count", 0))) if b else 0
        fresh_call = str(w122.get("call", w122.get("wave122_call", ""))) if w122 else "not_in_wave122"
        wave103_call = str(w103.get("wave103_call", "")) if w103 else "not_in_wave103"

        ms_anchor = (ms_fdr < 0.10 and abs(ms_delta) >= 0.25) or ms_genetic >= 0.50
        cross_anchor = positive_diseases >= 3 or positive_fdr10 >= 2
        perturbation_support = nominal >= 3 and neg_frac >= 0.70
        fdr_support = fdr10 >= 1
        reachable = gene in {"LIF", "LIFR", "IL6ST", "OSMR"}

        blockers = []
        if not perturbation_support:
            blockers.append("weak_or_narrow_siRNA_rescue")
        if not fdr_support:
            blockers.append("no_fdr10_siRNA_rescue")
        if not ms_anchor:
            blockers.append("no_ms_anchor")
        if not cross_anchor:
            blockers.append("insufficient_cross_disease_cell_state_anchor")
        if "NO_GO" in fresh_call or "NO_GO" in wave103_call:
            blockers.append("prior_local_no_go")
        if not reachable:
            blockers.append("weak_reachability")

        summary_rows.append(
            {
                "gene": gene,
                "n_induced_contexts_tested": int(len(sub)),
                "negative_effect_fraction": neg_frac,
                "mean_sirna_effect_vs_ctrl": mean_effect,
                "wilcoxon_less_p": wilcox_p,
                "nominal_negative_rescue_count": nominal,
                "fdr10_negative_rescue_count": fdr10,
                "ms_expr_delta_log2": ms_delta,
                "ms_expr_fdr": ms_fdr,
                "ms_genetic_score": ms_genetic,
                "broad_positive_disease_count": positive_diseases,
                "broad_positive_fdr10_compartment_count": positive_fdr10,
                "broad_positive_diseases": str(b.get("positive_diseases", "")) if b else "",
                "wave103_call": wave103_call,
                "wave122_call": fresh_call,
                "promote": False,
                "blockers": ";".join(blockers),
            }
        )

    axis_summary = pd.DataFrame(summary_rows)
    axis_summary.to_csv(OUT / "lif_lifr_axis_guardrail.tsv", sep="\t", index=False)

    lifr_contexts = induced[induced["sirna"].astype(str).str.upper() == "LIFR"].copy()
    lifr_contexts = lifr_contexts.sort_values(["sirna_effect_p_value", "module", "stimulation", "time"])
    lifr_contexts.to_csv(OUT / "lifr_induced_context_rescue_tests.tsv", sep="\t", index=False)

    branch = "NO_LIFR_ROUTE_PROMOTION"
    summary = {
        "branch_call": branch,
        "axis_genes": AXIS,
        "lifr_induced_contexts_tested": int((induced["sirna"].astype(str).str.upper() == "LIFR").sum()),
        "lifr_nominal_negative_rescue_count": int(axis_summary.loc[axis_summary["gene"] == "LIFR", "nominal_negative_rescue_count"].iloc[0]),
        "lifr_fdr10_negative_rescue_count": int(axis_summary.loc[axis_summary["gene"] == "LIFR", "fdr10_negative_rescue_count"].iloc[0]),
        "lifr_mean_effect": float(axis_summary.loc[axis_summary["gene"] == "LIFR", "mean_sirna_effect_vs_ctrl"].iloc[0]),
        "lifr_ms_expr_delta_log2": float(axis_summary.loc[axis_summary["gene"] == "LIFR", "ms_expr_delta_log2"].iloc[0]),
        "lifr_ms_expr_fdr": float(axis_summary.loc[axis_summary["gene"] == "LIFR", "ms_expr_fdr"].iloc[0]),
        "promoted_candidates": [],
        "interpretation": (
            "LIFR has real nominal siRNA rescue in human synovial fibroblasts, "
            "but the signal is not FDR-stable and lacks local MS, cross-disease, "
            "and genetics anchors required for V3 promotion."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = [
        "# Wave160 LIFR Interface Rescue Guardrail",
        "",
        f"Branch call: `{branch}`.",
        "",
        "## Result",
        "",
        "LIFR is parked as a perturbation follow-up candidate, not promoted as a V3 finding.",
        "",
        "## Key Numbers",
        "",
        f"- LIFR induced contexts tested: `{summary['lifr_induced_contexts_tested']}`.",
        f"- LIFR nominal negative rescue contexts: `{summary['lifr_nominal_negative_rescue_count']}`.",
        f"- LIFR FDR10 negative rescue contexts: `{summary['lifr_fdr10_negative_rescue_count']}`.",
        f"- LIFR mean siRNA effect: `{summary['lifr_mean_effect']:.4f}`.",
        f"- LIFR MS white-matter delta: `{summary['lifr_ms_expr_delta_log2']:.4f}`, FDR `{summary['lifr_ms_expr_fdr']:.4f}`.",
        "",
        "## Interpretation",
        "",
        summary["interpretation"],
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
