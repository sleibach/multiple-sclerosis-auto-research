#!/usr/bin/env python3
"""Wave72 lipid-mediator intervention fail-fast.

Wave71-C suggested that the next non-Fc/ROS route should be biochemical rather
than expression-first: NAAA substrates, soluble epoxide hydrolase oxylipin
ratios, GPR183 oxysterol gradients, and P2RX7 purinergic/inflammasome tone.

This script tests those ideas against existing real Wave66 public
metabolomics/lipidomics contrasts, then joins the result to local gene-state,
genetics, foundation-model, treatment-response, and MS foamy proteome evidence.
It is deliberately a gate: no branch is promoted without replicated biochemical
support plus gene-level convergence.
"""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave72_lipid_mediator_intervention_scout"
SEED = 20260527

WAVE66 = ROOT / "results_v3" / "wave66_metabolomics_class_convergence"
FEATURE_EFFECTS = WAVE66 / "feature_contrast_effects.tsv"
CLASS_EFFECTS = WAVE66 / "class_contrast_effects.tsv"
BROAD_H5AD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_summary.tsv"
WAVE62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
WAVE57 = ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_intervention_first_candidate_calls.tsv"
WAVE68 = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "integrated_gene_target_rank.tsv"
FOAMY_PROTEOME = ROOT / "results" / "mims2_proteome_convergent_targets.tsv"


BRANCHES: dict[str, dict[str, Any]] = {
    "NAAA_lipid_amide_preservation": {
        "gene": "NAAA",
        "intervention": "NAAA inhibition to preserve PEA/OEA-like N-acylethanolamide tone",
        "feature_pattern": r"palmitoylethanolamide|oleoylethanolamide|anandamide|ethanolamide|N-acylethanolamine|\bPEA\b|\bOEA\b|\bAEA\b",
        "expected_disease_sign": -1.0,
        "support_logic": "substrates lower in disease/worse state and higher after improvement",
        "manual_blocker": "requires direct PEA/OEA depletion or NAAA activity evidence; transcript recurrence alone is weak",
    },
    "EPHX2_sEH_oxylipin_diol": {
        "gene": "EPHX2",
        "intervention": "soluble epoxide hydrolase inhibition to reduce inflammatory diols and preserve epoxy-fatty acids",
        "feature_pattern": r"DiHOME|DHET|DiHETE|DiHDPA|EpOME|EpETrE|EpDPE|\bEET\b|eicosatrienoic acid",
        "expected_disease_sign": 1.0,
        "support_logic": "diol/oxylipin branch higher in disease/worse state and lower after improvement",
        "manual_blocker": "requires real EpFA:diol ratios; transcript/protein EPHX2 is not sufficient",
    },
    "GPR183_oxysterol_gradient": {
        "gene": "GPR183",
        "intervention": "GPR183/EBI2 antagonism or spatial modulation of oxysterol-driven inflammatory niches",
        "feature_pattern": r"oxysterol|hydroxycholesterol|cholestenoic acid|7alpha|7-alpha|7α|25-hydroxy|25HC|25-HC",
        "expected_disease_sign": 1.0,
        "support_logic": "oxysterol-gradient metabolites higher in disease/worse state and lower after improvement",
        "manual_blocker": "direction is niche-dependent and needs spatial cell-state support",
    },
    "P2RX7_purinergic_inflammasome": {
        "gene": "P2RX7",
        "intervention": "P2RX7 antagonism in purine/inflammasome-high myeloid disease states",
        "feature_pattern": r"\bATP\b|\bADP\b|\bAMP\b|adenosine|inosine|hypoxanthine|xanthine|uric acid|urate|8-oxo-2'?[- ]deoxyadenosine|methyladenosine|methylthioadenosine",
        "expected_disease_sign": 1.0,
        "support_logic": "purine danger/turnover metabolites higher in disease/worse state and lower after improvement",
        "manual_blocker": "purine metabolomics is nonspecific unless linked to P2RX7/IL1B/NLRP3 cell state",
    },
}

COMPARATOR_GENES = ["MFGE8", "GPR65", "SLC15A4"]
GENES = [branch["gene"] for branch in BRANCHES.values()] + COMPARATOR_GENES


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def num(value: Any) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return math.nan
    return out


def as_int(value: Any) -> int:
    value_f = num(value)
    return int(value_f) if math.isfinite(value_f) else 0


def s(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value)


def gene_row(df: pd.DataFrame, gene: str, columns: list[str] | None = None) -> dict[str, Any]:
    if df.empty:
        return {}
    columns = columns or ["gene"]
    for col in columns:
        if col in df.columns:
            sub = df[df[col].astype(str).str.upper().eq(gene.upper())]
            if not sub.empty:
                return sub.iloc[0].to_dict()
    return {}


def best_wave68(df: pd.DataFrame, gene: str) -> dict[str, Any]:
    if df.empty or "gene" not in df.columns:
        return {}
    sub = df[df["gene"].astype(str).str.upper().eq(gene.upper())].copy()
    if sub.empty:
        return {}
    sub["score_sort"] = pd.to_numeric(sub.get("integrated_score"), errors="coerce").fillna(-999)
    return sub.sort_values("score_sort", ascending=False).iloc[0].to_dict()


def classify_features(features: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    if features.empty:
        return pd.DataFrame(rows)

    for branch_name, meta in BRANCHES.items():
        pattern = re.compile(meta["feature_pattern"], flags=re.IGNORECASE)
        for _, row in features.iterrows():
            label = " ".join(
                [
                    s(row.get("feature_label")),
                    s(row.get("metabolite_class")),
                    s(row.get("feature_id")),
                ]
            )
            if not pattern.search(label):
                continue
            contrast_type = s(row.get("contrast_type"))
            effect = num(row.get("hedges_g_case_minus_control"))
            p = num(row.get("p"))
            fdr = num(row.get("fdr_within_study_contrast"))
            expected = float(meta["expected_disease_sign"])
            if "treatment" in contrast_type or "improvement" in contrast_type:
                support = math.isfinite(effect) and effect * expected <= -0.35 and (not math.isfinite(p) or p <= 0.10)
                support_kind = "normalizing_treatment_shift"
            else:
                support = math.isfinite(effect) and effect * expected >= 0.35 and (not math.isfinite(p) or p <= 0.10)
                support_kind = "disease_or_severity_shift"
            rows.append(
                {
                    "branch": branch_name,
                    "gene": meta["gene"],
                    "study_id": row.get("study_id"),
                    "disease": row.get("disease"),
                    "contrast": row.get("contrast"),
                    "contrast_type": contrast_type,
                    "feature_id": row.get("feature_id"),
                    "feature_label": row.get("feature_label"),
                    "metabolite_class": row.get("metabolite_class"),
                    "n_case": row.get("n_case"),
                    "n_control": row.get("n_control"),
                    "hedges_g_case_minus_control": effect,
                    "p": p,
                    "fdr_within_study_contrast": fdr,
                    "expected_disease_sign": expected,
                    "support_kind": support_kind,
                    "supports_branch_direction": bool(support),
                    "passes_nominal_effect_gate": bool(math.isfinite(effect) and abs(effect) >= 0.35 and (not math.isfinite(p) or p <= 0.10)),
                    "passes_fdr10": bool(math.isfinite(fdr) and fdr <= 0.10),
                }
            )
    return pd.DataFrame(rows)


def summarize_branch_features(matches: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for branch_name, meta in BRANCHES.items():
        sub = matches[matches["branch"].eq(branch_name)] if not matches.empty else pd.DataFrame()
        disease_like = sub[
            ~sub["contrast_type"].astype(str).str.contains("treatment|improvement", case=False, na=False)
        ] if not sub.empty else pd.DataFrame()
        treatment_like = sub[
            sub["contrast_type"].astype(str).str.contains("treatment|improvement", case=False, na=False)
        ] if not sub.empty else pd.DataFrame()
        supportive_disease = disease_like[disease_like["supports_branch_direction"]] if not disease_like.empty else pd.DataFrame()
        supportive_treatment = treatment_like[treatment_like["supports_branch_direction"]] if not treatment_like.empty else pd.DataFrame()
        fdr10 = sub[sub["passes_fdr10"]] if not sub.empty else pd.DataFrame()
        n_support_diseases = supportive_disease["disease"].nunique() if not supportive_disease.empty else 0
        n_treat_hits = len(supportive_treatment)
        if n_support_diseases >= 3 and n_treat_hits >= 1:
            call = "REOPEN_BIOCHEMICAL_SCOUT_NEEDS_GENE_LEVEL_VALIDATION"
        elif n_support_diseases >= 2:
            call = "PARK_BIOCHEMICAL_PATTERN_INSUFFICIENT_FOR_TARGET"
        else:
            call = "NO_GO_INSUFFICIENT_BIOCHEMICAL_SUPPORT"
        rows.append(
            {
                "branch": branch_name,
                "gene": meta["gene"],
                "intervention": meta["intervention"],
                "feature_match_count": len(sub),
                "disease_like_match_count": len(disease_like),
                "treatment_like_match_count": len(treatment_like),
                "supportive_disease_count": n_support_diseases,
                "supportive_diseases": ";".join(sorted(map(str, supportive_disease["disease"].dropna().unique()))) if n_support_diseases else "",
                "supportive_feature_count": len(supportive_disease),
                "normalizing_treatment_hit_count": n_treat_hits,
                "normalizing_treatment_hits": ";".join(
                    supportive_treatment.apply(lambda r: f"{r['study_id']}:{r['contrast']}:{r['feature_label']}", axis=1).tolist()
                ) if n_treat_hits else "",
                "fdr10_feature_count": len(fdr10),
                "best_nominal_feature": (
                    sub.assign(abs_g=lambda d: d["hedges_g_case_minus_control"].abs())
                    .sort_values(["supports_branch_direction", "passes_fdr10", "abs_g"], ascending=[False, False, False])
                    .head(1)
                    .apply(lambda r: f"{r['study_id']}|{r['disease']}|{r['contrast']}|{r['feature_label']}|g={r['hedges_g_case_minus_control']:.3g}|p={r['p']:.3g}|fdr={r['fdr_within_study_contrast']:.3g}", axis=1)
                    .iloc[0]
                    if not sub.empty
                    else ""
                ),
                "support_logic": meta["support_logic"],
                "manual_blocker": meta["manual_blocker"],
                "biochemical_call": call,
            }
        )
    return pd.DataFrame(rows)


def purine_class_summary(class_effects: pd.DataFrame) -> dict[str, Any]:
    if class_effects.empty or "metabolite_class" not in class_effects.columns:
        return {}
    sub = class_effects[class_effects["metabolite_class"].astype(str).str.lower().eq("purine")].copy()
    if sub.empty:
        return {}
    disease_like = sub[~sub["contrast_type"].astype(str).str.contains("treatment|improvement", case=False, na=False)].copy()
    disease_like["support"] = (
        pd.to_numeric(disease_like["hedges_g_case_minus_control"], errors="coerce").ge(0.35)
        & pd.to_numeric(disease_like["p"], errors="coerce").le(0.10)
    )
    treatment_like = sub[sub["contrast_type"].astype(str).str.contains("treatment|improvement", case=False, na=False)].copy()
    treatment_like["support"] = (
        pd.to_numeric(treatment_like["hedges_g_case_minus_control"], errors="coerce").le(-0.35)
        & pd.to_numeric(treatment_like["p"], errors="coerce").le(0.10)
    )
    return {
        "purine_class_rows": int(len(sub)),
        "purine_supportive_disease_count": int(disease_like.loc[disease_like["support"], "disease"].nunique()),
        "purine_supportive_diseases": ";".join(sorted(map(str, disease_like.loc[disease_like["support"], "disease"].dropna().unique()))),
        "purine_normalizing_treatment_rows": int(treatment_like["support"].sum()) if not treatment_like.empty else 0,
        "purine_best_rows": disease_like.assign(abs_g=lambda d: pd.to_numeric(d["hedges_g_case_minus_control"], errors="coerce").abs())
        .sort_values(["support", "abs_g"], ascending=[False, False])
        .head(5)[["study_id", "disease", "contrast", "hedges_g_case_minus_control", "p", "fdr_within_study_contrast"]]
        .to_dict(orient="records"),
    }


def gene_evidence() -> pd.DataFrame:
    broad = read_tsv(BROAD_H5AD)
    wave62 = read_tsv(WAVE62)
    wave57 = read_tsv(WAVE57)
    wave68 = read_tsv(WAVE68)
    proteome = read_tsv(FOAMY_PROTEOME)
    rows: list[dict[str, Any]] = []
    for gene in GENES:
        br = gene_row(broad, gene)
        w62 = gene_row(wave62, gene)
        w57 = gene_row(wave57, gene)
        w68 = best_wave68(wave68, gene)
        prot = gene_row(proteome, gene)
        rows.append(
            {
                "gene": gene,
                "broad_positive_disease_count": br.get("positive_disease_count"),
                "broad_negative_disease_count": br.get("negative_disease_count"),
                "broad_positive_diseases": br.get("positive_diseases"),
                "broad_negative_diseases": br.get("negative_diseases"),
                "broad_best_positive_fdr": br.get("best_positive_fdr"),
                "broad_in_lipid_lysosomal_neighborhood": br.get("in_lipid_lysosomal_myeloid_neighborhood"),
                "wave62_score": w62.get("wave62_score"),
                "wave62_call": w62.get("wave62_call"),
                "wave62_strong_l2g_disease_count": w62.get("strong_l2g_disease_count"),
                "wave62_strong_qtl_coloc_disease_count": w62.get("strong_qtl_coloc_disease_count"),
                "wave62_ms_max_relevant_qtl_h4": w62.get("ms_max_relevant_qtl_h4"),
                "geneformer_wave57_call": w57.get("wave57_call"),
                "geneformer_support_contexts": w57.get("support_contexts"),
                "geneformer_strong_support_contexts": w57.get("strong_support_contexts"),
                "geneformer_model_priority_score": w57.get("wave57_model_priority_score"),
                "gse282122_best_cell_state": w68.get("cell_state"),
                "gse282122_raw_p": w68.get("raw_p"),
                "gse282122_raw_fdr": w68.get("raw_fdr"),
                "gse282122_paired_fdr": w68.get("paired_fdr"),
                "gse282122_integrated_score": w68.get("integrated_score"),
                "gse282122_wave68_call": w68.get("wave68_call"),
                "ms_foamy_proteome_passes_convergence_gate": prot.get("passes_convergence_gate"),
                "ms_foamy_proteome_mean_delta": prot.get("mean_delta"),
                "ms_foamy_proteome_gee_p": prot.get("gee_p"),
                "ms_foamy_proteome_fdr_bh": prot.get("fdr_bh"),
            }
        )
    return pd.DataFrame(rows)


def final_decisions(branch_summary: pd.DataFrame, gene_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for _, branch in branch_summary.iterrows():
        gene = s(branch["gene"])
        g = gene_df[gene_df["gene"].astype(str).eq(gene)]
        grow = g.iloc[0].to_dict() if not g.empty else {}
        local_pos = as_int(grow.get("broad_positive_disease_count"))
        local_neg = as_int(grow.get("broad_negative_disease_count"))
        genetics = as_int(grow.get("wave62_strong_l2g_disease_count")) + as_int(grow.get("wave62_strong_qtl_coloc_disease_count"))
        model_support = as_int(grow.get("geneformer_support_contexts"))
        proteome_pass = str(grow.get("ms_foamy_proteome_passes_convergence_gate")).lower() == "true"
        biochemical_support = as_int(branch.get("supportive_disease_count"))
        normalizing = as_int(branch.get("normalizing_treatment_hit_count"))
        gate_count = 0
        gate_count += int(biochemical_support >= 3)
        gate_count += int(normalizing >= 1)
        gate_count += int(local_pos >= 3 and local_neg == 0)
        gate_count += int(genetics >= 2)
        gate_count += int(model_support >= 2)
        gate_count += int(proteome_pass)
        if gate_count >= 5:
            call = "REOPEN_FOR_TARGETED_VALIDATION"
        elif biochemical_support >= 2 or proteome_pass:
            call = "PARK_ORTHOGONAL_BIOCHEMICAL_SCOUT"
        else:
            call = "NO_GO_WAVE72"
        rows.append(
            {
                "branch": branch["branch"],
                "gene": gene,
                "wave72_call": call,
                "gate_count": gate_count,
                "biochemical_supportive_disease_count": biochemical_support,
                "normalizing_treatment_hit_count": normalizing,
                "local_positive_disease_count": local_pos,
                "local_negative_disease_count": local_neg,
                "genetic_anchor_count": genetics,
                "geneformer_support_contexts": model_support,
                "ms_foamy_proteome_pass": proteome_pass,
                "decisive_blocker": (
                    "biochemical feature support is absent or underpowered"
                    if biochemical_support < 2
                    else "biochemical pattern lacks target-level gene convergence"
                ),
            }
        )
    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    display = df.fillna("").astype(str)
    headers = list(display.columns)

    def esc(value: str) -> str:
        return value.replace("|", "\\|").replace("\n", " ")[:500]

    lines = [
        "| " + " | ".join(esc(col) for col in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(esc(row[col]) for col in headers) + " |")
    return "\n".join(lines)


def write_report(branch_summary: pd.DataFrame, gene_df: pd.DataFrame, decisions: pd.DataFrame, summary: dict[str, Any]) -> None:
    lines = [
        "# Wave72 Lipid-Mediator Intervention Scout",
        "",
        "## Question",
        "",
        "Do the Wave71-C biochemical intervention routes (`NAAA`, `EPHX2`, `GPR183`, `P2RX7`) survive a real public metabolomics/lipidomics fail-fast when joined to local V3 gene-level evidence?",
        "",
        "## Verdict",
        "",
        "No branch is promoted. The strongest orthogonal signal is biochemical-class level, not target-level. `P2RX7` has broad purine-class disturbance but this is nonspecific; `EPHX2` has scattered DiHOME/eicosanoid rows but no replicated EpFA:diol ratio; `NAAA` substrates are essentially absent from the available feature panels; `GPR183` oxysterol evidence is sparse.",
        "",
        "## Branch Decisions",
        "",
        markdown_table(decisions),
        "",
        "## Biochemical Feature Summary",
        "",
        markdown_table(branch_summary),
        "",
        "## Gene-Level Evidence",
        "",
        markdown_table(gene_df),
        "",
        "## Purine Class Context",
        "",
        "```json",
        json.dumps(summary.get("purine_class_summary", {}), indent=2, sort_keys=True, allow_nan=True),
        "```",
        "",
        "## Interpretation",
        "",
        "- This wave answers Wave71-C's strongest new computational test with existing public data.",
        "- Available metabolomics panels are not rich enough in PEA/OEA, EpFA:diol pairs, or GPR183 oxysterols to support a target claim.",
        "- `P2RX7` remains a possible stratification concept only if future baseline ATP/purine plus `IL1B/NLRP3` cell-state data can identify a responder subset; current data are too nonspecific.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    feature_effects = read_tsv(FEATURE_EFFECTS)
    class_effects = read_tsv(CLASS_EFFECTS)
    matches = classify_features(feature_effects)
    branch_summary = summarize_branch_features(matches)
    gene_df = gene_evidence()
    decisions = final_decisions(branch_summary, gene_df)
    summary = {
        "random_seed": SEED,
        "inputs": {
            "feature_effects": rel(FEATURE_EFFECTS),
            "class_effects": rel(CLASS_EFFECTS),
            "broad_h5ad": rel(BROAD_H5AD),
            "wave62": rel(WAVE62),
            "wave57": rel(WAVE57),
            "wave68": rel(WAVE68),
            "foamy_proteome": rel(FOAMY_PROTEOME),
        },
        "feature_match_count": int(len(matches)),
        "branch_calls": decisions["wave72_call"].value_counts(dropna=False).to_dict() if not decisions.empty else {},
        "purine_class_summary": purine_class_summary(class_effects),
    }
    matches.to_csv(OUT / "lipid_mediator_feature_matches.tsv", sep="\t", index=False)
    branch_summary.to_csv(OUT / "lipid_mediator_branch_summary.tsv", sep="\t", index=False)
    gene_df.to_csv(OUT / "lipid_mediator_gene_evidence.tsv", sep="\t", index=False)
    decisions.to_csv(OUT / "lipid_mediator_decisions.tsv", sep="\t", index=False)
    write_json(OUT / "summary.json", summary)
    write_report(branch_summary, gene_df, decisions, summary)


if __name__ == "__main__":
    main()
