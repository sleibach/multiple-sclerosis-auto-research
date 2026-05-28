#!/usr/bin/env python3
"""Mine V5 outputs for V6 Tier -1 hypothesis-generating patterns.

Tier -1 deliberately uses loose criteria. This script does not make therapeutic
claims; it creates a traceable table of patterns worth independent checks.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "tier_minus_1_exploration" / "v6_initial_pattern_mining"


def tier_minus_1_flag(p: float | None, g: float | None) -> bool:
    p_ok = p is not None and pd.notna(p) and p < 0.10
    g_ok = g is not None and pd.notna(g) and abs(g) > 0.50
    return bool(p_ok or g_ok)


def add_row(rows: list[dict], source: str, pattern: str, effect: float | None,
            hedges_g: float | None, p_value: float | None,
            interpretation: str, next_check: str) -> None:
    rows.append(
        {
            "source": source,
            "pattern": pattern,
            "effect": effect,
            "hedges_g": hedges_g,
            "p_value": p_value,
            "tier_minus_1_flag": tier_minus_1_flag(p_value, hedges_g),
            "interpretation": interpretation,
            "next_check": next_check,
        }
    )


def mine_gse17410(rows: list[dict]) -> None:
    source = "results/pregnancy_dimension/gse17410_ms_sensitivity"
    comp = pd.read_csv(ROOT / source / "component_contrasts.tsv", sep="\t")
    for _, r in comp.iterrows():
        add_row(
            rows,
            source,
            f"GSE17410 month9_vs_pre {r['component']}",
            r["delta_month9_minus_pre"],
            r["hedges_g"],
            r["welch_p"],
            "MS late-pregnancy component shift; Tier -1 if loose p or effect-size criteria pass.",
            "validate in independent pregnancy/postpartum blood data or deconvolve cell source",
        )

    resid = pd.read_csv(ROOT / source / "composition_residual_contrasts.tsv", sep="\t")
    for _, r in resid.iterrows():
        add_row(
            rows,
            source,
            f"GSE17410 residual {r['component']} adjusted_for_{r['covariates']}",
            r["delta_month9_minus_pre"],
            r["hedges_g"],
            r["welch_p"],
            "Adjustment behavior identifies whether composition absorbs or preserves the pregnancy signal.",
            "treat absorbed covariate set as candidate mechanism if biologically plausible",
        )


def mine_emt12260(rows: list[dict]) -> None:
    path = ROOT / "results/pregnancy_dimension/emt12260_ms_tcells/timepoint_contrasts.tsv"
    if not path.exists():
        return
    source = str(path.relative_to(ROOT).parent)
    df = pd.read_csv(path, sep="\t")
    for _, r in df.iterrows():
        p_col = "welch_p" if "welch_p" in df.columns else "p_value"
        effect_col = "delta" if "delta" in df.columns else [c for c in df.columns if c.startswith("delta")][0]
        add_row(
            rows,
            source,
            "E-MTAB-12260 " + " ".join(str(r.get(c, "")) for c in ["module", "contrast"] if c in df.columns),
            r[effect_col],
            r.get("hedges_g"),
            r.get(p_col),
            "Sorted MS T-cell pregnancy/postpartum pattern.",
            "compare against relapse timing and cross-disease pregnancy T-cell trafficking",
        )


def mine_gse108497(rows: list[dict]) -> None:
    path = ROOT / "results/pregnancy_dimension/gse108497_sle/timepoint_contrasts.tsv"
    if not path.exists():
        return
    source = str(path.relative_to(ROOT).parent)
    df = pd.read_csv(path, sep="\t")
    for _, r in df.iterrows():
        p_col = "welch_p" if "welch_p" in df.columns else "p_value"
        delta_cols = [c for c in df.columns if c.startswith("delta")]
        effect_col = delta_cols[0] if delta_cols else "effect"
        label_cols = [c for c in ["outcome_group", "module", "contrast"] if c in df.columns]
        add_row(
            rows,
            source,
            "GSE108497 " + " ".join(str(r.get(c, "")) for c in label_cols),
            r.get(effect_col),
            r.get("hedges_g"),
            r.get(p_col),
            "Outcome-stratified SLE pregnancy/postpartum immune kinetics.",
            "test decoupling in independent pregnancy and disease-outcome datasets",
        )


def mine_mif_cd74_ms(rows: list[dict]) -> None:
    source = "analysis/tier_1_mechanism/mif_cd74_component_ms_pseudobulk"
    df = pd.read_csv(ROOT / source / "component_residual_tests.tsv", sep="\t")
    for _, r in df.iterrows():
        add_row(
            rows,
            source,
            f"MS pseudobulk {r['cell_type']} {r['component']} {r['contrast']} residual",
            r["residual_delta"],
            r["residual_hedges_g"],
            r["residual_p"],
            "Residualized lesion-compartment pattern after broad APC/size adjustment.",
            "prioritize cell types where residual survives Tier -1 despite failing FDR",
        )


def mine_gse282122(rows: list[dict]) -> None:
    source = "analysis/tier_1_mechanism/mif_cd74_gse282122_component_response"
    df = pd.read_csv(ROOT / source / "component_remission_interaction.tsv", sep="\t")
    for _, r in df.iterrows():
        add_row(
            rows,
            source,
            f"GSE282122 {r['state_level']} {r['cell_state']} {r['component']} raw remission",
            r["raw_delta_remission_minus_non"],
            r["raw_hedges_g"],
            r["raw_p"],
            "Raw treatment-response remodeling pattern before IFN/APC adjustment.",
            "if adjusted away, inspect IFN/APC as mechanism rather than discard",
        )
        add_row(
            rows,
            source,
            f"GSE282122 {r['state_level']} {r['cell_state']} {r['component']} IFN-adjusted remission",
            r["ifn_adjusted_delta"],
            None,
            r["ifn_adjusted_p"],
            "Residual treatment-response pattern after IFN/APC adjustment.",
            "promote only if an independent dataset preserves direction or mechanism",
        )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    mine_gse17410(rows)
    mine_emt12260(rows)
    mine_gse108497(rows)
    mine_mif_cd74_ms(rows)
    mine_gse282122(rows)

    df = pd.DataFrame(rows)
    df["abs_hedges_g"] = df["hedges_g"].abs()
    flagged = df[df["tier_minus_1_flag"]].copy()
    flagged = flagged.sort_values(
        ["p_value", "abs_hedges_g"], ascending=[True, False], na_position="last"
    )

    df.to_csv(OUT / "all_patterns.tsv", sep="\t", index=False)
    flagged.to_csv(OUT / "tier_minus_1_flagged_patterns.tsv", sep="\t", index=False)

    summary = {
        "n_patterns_total": int(len(df)),
        "n_tier_minus_1_flagged": int(len(flagged)),
        "sources": sorted(df["source"].unique().tolist()),
        "criteria": "p < 0.10 uncorrected or abs(Hedges g) > 0.50",
        "top_patterns": flagged.head(20)[
            ["source", "pattern", "effect", "hedges_g", "p_value", "interpretation"]
        ].to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report_lines = [
        "# V6 Initial Tier -1 Pattern Mining",
        "",
        "This report uses loose V6 exploration criteria only: uncorrected p `< 0.10`",
        "or absolute Hedges g `> 0.50`. It does not make validation-tier claims.",
        "",
        f"Total patterns scanned: `{summary['n_patterns_total']}`.",
        f"Tier -1 flagged patterns: `{summary['n_tier_minus_1_flagged']}`.",
        "",
        "## Top Flagged Patterns",
        "",
    ]
    for item in summary["top_patterns"]:
        report_lines.append(
            f"- `{item['pattern']}` from `{item['source']}`: effect "
            f"`{item['effect']}`, Hedges g `{item['hedges_g']}`, p `{item['p_value']}`."
        )
    report_lines.extend(
        [
            "",
            "## Outputs",
            "",
            "- `all_patterns.tsv`",
            "- `tier_minus_1_flagged_patterns.tsv`",
            "- `summary.json`",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(report_lines) + "\n")


if __name__ == "__main__":
    main()
