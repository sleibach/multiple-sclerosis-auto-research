#!/usr/bin/env python3
"""Wave163: CD300 receptor-specific tuning closure.

CD300 was the other resolution/efferocytosis reopener. This wave asks whether
any receptor-specific member now satisfies direction, MS anchor, perturbation,
and modality gates after the post-interface reprioritization.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave163_cd300_receptor_specific_closure"
OUT.mkdir(parents=True, exist_ok=True)

GENES = ["CD300A", "CD300E", "CD300LF", "CD300C", "CD300LG"]


def read(path: Path) -> pd.DataFrame:
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
    broad = read(ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_summary.tsv")
    ms = read(ROOT / "phases/v3/results" / "gse111972_full_ms_wm_signature.tsv")
    wave37 = read(ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv")
    wave48_route = read(ROOT / "phases/v3/results" / "wave48_resolution_reopener_audit" / "route_reopener_audit.tsv")
    wave103 = read(ROOT / "phases/v3/results" / "wave103_intervention_first_successor_triage" / "intervention_first_successor_rank.tsv")

    rows = []
    for gene in GENES:
        b = pick(broad, gene)
        m = pick(ms, gene)
        w37 = pick(wave37.rename(columns={"gene_symbol": "gene"}), gene)
        w103 = pick(wave103, gene)

        positive_diseases = int(float(b.get("positive_disease_count", 0))) if b else 0
        positive_fdr10 = int(float(b.get("positive_fdr10_compartment_count", 0))) if b else 0
        disease_names = str(b.get("positive_diseases", "")) if b else ""
        ms_delta = float(m.get("delta_log2", 0.0)) if m else 0.0
        ms_fdr = float(m.get("fdr", 1.0)) if m else 1.0
        contrast_lfc = float(w37.get("median_efficient_minus_noneater_lfc", 0.0)) if w37 else 0.0
        contrast_fdr = float(w37.get("contrast_fdr", 1.0)) if w37 else 1.0
        screen_call = str(w37.get("screen_call", "")) if w37 else ""
        wave103_call = str(w103.get("wave103_call", "")) if w103 else "not_in_wave103"

        cross_signal = positive_diseases >= 3 or positive_fdr10 >= 2
        ms_anchor = ms_fdr < 0.10 and ms_delta > 0.25
        perturbation_anchor = contrast_fdr < 0.10 and abs(contrast_lfc) >= 0.5
        receptor_specific_direction = gene in {"CD300A", "CD300LF"} and perturbation_anchor
        modality = False  # no local ChEMBL/antibody route with clear agonist/inhibitor direction

        blockers = []
        if not cross_signal:
            blockers.append("insufficient_cross_disease_signal")
        if not ms_anchor:
            blockers.append("no_positive_ms_anchor")
        if not perturbation_anchor:
            blockers.append("no_fdr_perturbation_anchor")
        if not receptor_specific_direction:
            blockers.append("no_receptor_specific_safe_direction")
        if not modality:
            blockers.append("no_selective_modality")
        if "NO_GO" in wave103_call:
            blockers.append("prior_local_no_go")

        rows.append(
            {
                "gene": gene,
                "broad_positive_disease_count": positive_diseases,
                "broad_positive_fdr10_compartment_count": positive_fdr10,
                "broad_positive_diseases": disease_names,
                "ms_delta_log2": ms_delta,
                "ms_fdr": ms_fdr,
                "wave37_contrast_lfc": contrast_lfc,
                "wave37_contrast_fdr": contrast_fdr,
                "wave37_screen_call": screen_call,
                "wave103_call": wave103_call,
                "promote": False,
                "blockers": ";".join(blockers),
            }
        )

    audit = pd.DataFrame(rows)
    audit.to_csv(OUT / "cd300_receptor_member_audit.tsv", sep="\t", index=False)
    if not wave48_route.empty:
        wave48_route[wave48_route["route"].astype(str).str.contains("CD300", na=False)].to_csv(
            OUT / "copied_wave48_cd300_route.tsv", sep="\t", index=False
        )

    branch = "NO_REOPEN_CD300_DIRECTION_AND_MS_ANCHOR_FAIL"
    summary = {
        "branch_call": branch,
        "genes_audited": GENES,
        "promoted_candidates": [],
        "best_cross_signal_gene": audit.sort_values("broad_positive_disease_count", ascending=False).iloc[0]["gene"],
        "best_cross_signal_disease_count": int(audit["broad_positive_disease_count"].max()),
        "best_crispr_trend_gene": audit.sort_values("wave37_contrast_lfc", ascending=False).iloc[0]["gene"],
        "best_crispr_trend_lfc": float(audit["wave37_contrast_lfc"].max()),
        "best_crispr_trend_fdr": float(audit.sort_values("wave37_contrast_lfc", ascending=False).iloc[0]["wave37_contrast_fdr"]),
        "interpretation": (
            "CD300 receptor-specific tuning remains wet-lab-only. CD300E has "
            "some cross-disease myeloid signal and CD300A has a CRISPR trend, "
            "but no member has a positive MS anchor, FDR perturbation support, "
            "or a selective safe modality/direction."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = [
        "# Wave163 CD300 Receptor-Specific Closure",
        "",
        f"Branch call: `{branch}`.",
        "",
        "## Result",
        "",
        "Do not reopen CD300 receptor-specific tuning as a V3 finding.",
        "",
        "## Key Facts",
        "",
        f"- Best cross-signal gene: `{summary['best_cross_signal_gene']}` in `{summary['best_cross_signal_disease_count']}` diseases.",
        f"- Best CRISPR trend gene: `{summary['best_crispr_trend_gene']}`, LFC `{summary['best_crispr_trend_lfc']:.4f}`, FDR `{summary['best_crispr_trend_fdr']:.4f}`.",
        "",
        "## Interpretation",
        "",
        summary["interpretation"],
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
