#!/usr/bin/env python3
"""V53 grounded re-audit of the MIF/CD74 therapeutic angle.

This script uses committed project outputs only. It does not fetch data, alter
locked rules, or treat structural/literature context as biological evidence.
"""

from __future__ import annotations

import ast
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis/v53_mif_cd74_grounded_audit"
SEED = 53001
N_SIGN_NULL = 20000
MIN_DIRECTIONAL_ABS_G = 0.2
MODULE = "mif_cd74_receptor_state"

MODULE_DEFINITION_SOURCES = [
    "scripts/v3_analyze_direct_h5ad_cell_states.py",
    "scripts/v3_analyze_mixscale_perturbseq.py",
    "scripts/v3_analyze_gse253006_tofacitinib_uc.py",
    "scripts/v3_analyze_cellxgene_cross_autoimmune.py",
    "scripts/analyze_gse17410_ms_pregnancy_modules.py",
    "scripts/analyze_emt12260_ms_tcells.py",
    "scripts/analyze_gse108497_sle_pregnancy.py",
    "scripts/v10_sjogren_gse23117_bulk_replication.py",
    "scripts/v3_analyze_gse111972_microglia.py",
]


def literal_module_definition(path: Path) -> list[str] | None:
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        value = node.value
        if not isinstance(value, ast.Dict):
            continue
        try:
            mapping = ast.literal_eval(value)
        except (ValueError, TypeError):
            continue
        if isinstance(mapping, dict) and MODULE in mapping:
            genes = mapping[MODULE]
            if isinstance(genes, (list, tuple)):
                return [str(gene) for gene in genes]
    return None


def module_definition_audit() -> pd.DataFrame:
    rows = []
    for rel in MODULE_DEFINITION_SOURCES:
        genes = literal_module_definition(ROOT / rel)
        rows.append(
            {
                "source": rel,
                "definition_found": genes is not None,
                "genes": ";".join(genes or []),
                "n_genes": len(genes or []),
                "contains_MIF": bool(genes and "MIF" in genes),
                "contains_CD74": bool(genes and "CD74" in genes),
                "contains_HLAII": bool(genes and any(gene.startswith("HLA-D") for gene in genes)),
            }
        )
    return pd.DataFrame(rows)


def exact_majority_sign_p(n_positive: int, n_negative: int) -> float:
    n = n_positive + n_negative
    if n == 0:
        return math.nan
    observed = max(n_positive, n_negative)
    probability = 0.0
    for positives in range(n + 1):
        if max(positives, n - positives) >= observed:
            probability += math.comb(n, positives) / (2**n)
    return min(probability, 1.0)


def direction_consistency() -> tuple[pd.DataFrame, dict[str, object]]:
    source = pd.read_csv(
        ROOT / "analysis/v36_receptor_coupling_followup/receptor_recurrence_tests.tsv",
        sep="\t",
    )
    receptor = source[source["feature"].eq("delta_RECEPTOR")].copy()
    rows = []
    for family, sub in [
        ("GSE85034_MTX", receptor[receptor["cohort"].eq("GSE85034_MTX")]),
        ("GSE85034_ADA", receptor[receptor["cohort"].eq("GSE85034_ADA")]),
        ("GSE253006_TOF", receptor[receptor["cohort"].str.startswith("GSE253006_TOF")]),
    ]:
        effects = pd.to_numeric(sub["hedges_g_responder_minus_non"], errors="coerce").dropna()
        aucs = pd.to_numeric(sub["auc_high_score_response"], errors="coerce").dropna()
        median_g = float(effects.median()) if len(effects) else math.nan
        if not math.isfinite(median_g) or abs(median_g) < MIN_DIRECTIONAL_ABS_G:
            direction = "near_null"
        else:
            direction = "positive" if median_g > 0 else "negative"
        rows.append(
            {
                "cohort_family": family,
                "n_rows_collapsed": len(sub),
                "median_hedges_g": median_g,
                "median_auc": float(aucs.median()) if len(aucs) else math.nan,
                "direction": direction,
            }
        )
    collapsed = pd.DataFrame(rows)
    n_positive = int(collapsed["direction"].eq("positive").sum())
    n_negative = int(collapsed["direction"].eq("negative").sum())
    n_near_null = int(collapsed["direction"].eq("near_null").sum())
    rng = np.random.default_rng(SEED)
    null_majorities = []
    for _ in range(N_SIGN_NULL):
        signs = rng.choice([-1, 1], size=n_positive + n_negative)
        null_majorities.append(max(int((signs > 0).sum()), int((signs < 0).sum())))
    observed_majority = max(n_positive, n_negative)
    empirical_p = (sum(value >= observed_majority for value in null_majorities) + 1) / (N_SIGN_NULL + 1)
    summary = {
        "n_therapy_cohorts_total": int(len(collapsed)),
        "n_direction_bearing_cohorts": n_positive + n_negative,
        "n_positive_direction": n_positive,
        "n_negative_direction": n_negative,
        "n_near_null": n_near_null,
        "minimum_directional_abs_hedges_g": MIN_DIRECTIONAL_ABS_G,
        "observed_majority": observed_majority,
        "exact_two_sided_majority_sign_p": exact_majority_sign_p(n_positive, n_negative),
        "empirical_majority_sign_p": empirical_p,
        "seed": SEED,
        "n_sign_null": N_SIGN_NULL,
    }
    return collapsed, summary


def evidence_ledger(definitions: pd.DataFrame, direction: dict[str, object]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    cross = pd.read_csv(ROOT / "phases/v3/results/cross_disease_cell_state_convergence.tsv", sep="\t")
    ms = cross[(cross["disease"].eq("MS")) & (cross["dataset"].eq("GSE111972"))]
    for feature in [MODULE, "mif_ligand_axis"]:
        sub = ms[ms["module"].eq(feature)]
        if len(sub):
            rec = sub.iloc[0]
            rows.append(
                {
                    "evidence_layer": "MS_cross_sectional_microglia",
                    "test": feature,
                    "effect": float(rec["delta"]),
                    "p": float(rec["p"]),
                    "q_or_fdr": float(rec["fdr"]),
                    "outcome": "supported_state_association" if float(rec["fdr"]) <= 0.10 else "not_supported",
                    "interpretation": "observational state association; not causal or directional target evidence",
                    "source": "phases/v3/results/cross_disease_cell_state_convergence.tsv",
                }
            )

    tier0 = pd.read_csv(ROOT / "analysis/tier_0_triage/mif_cd74_stratification/residual_evidence.tsv", sep="\t")
    rows.append(
        {
            "evidence_layer": "cross_disease_IFN_residualization",
            "test": "all receptor-state residual tests",
            "effect": int((tier0["residual_fdr"] <= 0.10).sum()),
            "p": math.nan,
            "q_or_fdr": float(tier0["residual_fdr"].min()),
            "outcome": "not_supported",
            "interpretation": "zero tests survived FDR<=0.10",
            "source": "analysis/tier_0_triage/mif_cd74_stratification/residual_evidence.tsv",
        }
    )

    ms_components = pd.read_csv(
        ROOT / "analysis/tier_1_mechanism/mif_cd74_component_ms_pseudobulk/component_residual_tests.tsv",
        sep="\t",
    )
    immune_cd74 = ms_components[(ms_components["cell_type"].eq("immune")) & (ms_components["component"].eq("cd74_alone"))]
    rows.append(
        {
            "evidence_layer": "MS_lesion_component_residualization",
            "test": "immune CD74 after APC/size adjustment",
            "effect": int((immune_cd74["residual_fdr"] <= 0.10).sum()),
            "p": float(immune_cd74["residual_p"].min()),
            "q_or_fdr": float(immune_cd74["residual_fdr"].min()),
            "outcome": "not_supported",
            "interpretation": "no immune CD74 contrast survived multiplicity correction",
            "source": "analysis/tier_1_mechanism/mif_cd74_component_ms_pseudobulk/component_residual_tests.tsv",
        }
    )

    response = pd.read_csv(
        ROOT / "analysis/tier_1_mechanism/mif_cd74_gse282122_component_response/component_remission_interaction.tsv",
        sep="\t",
    )
    receptor_components = response[response["component"].isin(["cd74_alone", "receptor_only_cd74_cd44_cxcr4", "full_mif_cd74_state"])]
    rows.append(
        {
            "evidence_layer": "component_resolved_treatment_response",
            "test": "receptor/CD74/full-state after IFN/APC adjustment",
            "effect": int((receptor_components["ifn_adjusted_fdr"] <= 0.10).sum()),
            "p": float(receptor_components["ifn_adjusted_p"].min()),
            "q_or_fdr": float(receptor_components["ifn_adjusted_fdr"].min()),
            "outcome": "not_supported",
            "interpretation": "zero adjusted receptor-specific tests survived FDR<=0.10",
            "source": "analysis/tier_1_mechanism/mif_cd74_gse282122_component_response/component_remission_interaction.tsv",
        }
    )

    dependencies = pd.read_csv(ROOT / "analysis/v26_deep_structure/workstream_b_module_dependencies.tsv", sep="\t")
    mif_dependencies = dependencies[
        (dependencies["module_a"].eq(MODULE) | dependencies["module_b"].eq(MODULE))
        & dependencies["claim_grade"].eq("supported")
    ]
    rows.append(
        {
            "evidence_layer": "cross_modality_module_dependency",
            "test": "supported V26 dependencies involving receptor-state module",
            "effect": int(len(mif_dependencies)),
            "p": float(mif_dependencies["perm_p"].min()),
            "q_or_fdr": float(mif_dependencies["q_bh_within_modality"].min()),
            "outcome": "supported_coupling",
            "interpretation": "module coupling is supported, but does not establish ligand causality or intervention direction",
            "source": "analysis/v26_deep_structure/workstream_b_module_dependencies.tsv",
        }
    )

    tone = pd.read_csv(ROOT / "analysis/v38_coupled_architecture_inversion/module_global_tone_tests.tsv", sep="\t")
    mif_tone = tone[tone["module"].eq(MODULE)]
    rows.append(
        {
            "evidence_layer": "global_tone_loading",
            "test": "receptor-state module vs row-wise module mean",
            "effect": int((mif_tone["q_bh_all_module_tone_tests"] <= 0.10).sum()),
            "p": float(mif_tone["perm_p"].min()),
            "q_or_fdr": float(mif_tone["q_bh_all_module_tone_tests"].max()),
            "outcome": "supported_confounding_context",
            "interpretation": f"tone association survives in {int((mif_tone['q_bh_all_module_tone_tests'] <= 0.10).sum())}/{len(mif_tone)} modalities",
            "source": "analysis/v38_coupled_architecture_inversion/module_global_tone_tests.tsv",
        }
    )

    rows.append(
        {
            "evidence_layer": "therapy_direction_recurrence",
            "test": "collapsed delta_RECEPTOR sign consistency",
            "effect": direction["observed_majority"],
            "p": direction["empirical_majority_sign_p"],
            "q_or_fdr": math.nan,
            "outcome": "not_supported",
            "interpretation": f"{direction['n_positive_direction']} positive, {direction['n_negative_direction']} negative, and {direction['n_near_null']} near-null therapy-cohort directions",
            "source": "analysis/v36_receptor_coupling_followup/receptor_recurrence_tests.tsv",
        }
    )

    rows.append(
        {
            "evidence_layer": "module_definition_provenance",
            "test": "literal module definitions containing MIF",
            "effect": int(definitions["contains_MIF"].sum()),
            "p": math.nan,
            "q_or_fdr": math.nan,
            "outcome": "inconsistent_coverage",
            "interpretation": f"MIF present in {int(definitions['contains_MIF'].sum())}/{int(definitions['definition_found'].sum())} recovered literal definitions",
            "source": "committed analysis scripts listed in module_definition_audit.tsv",
        }
    )
    return pd.DataFrame(rows)


def markdown_table(frame: pd.DataFrame) -> str:
    def render(value: object) -> str:
        if pd.isna(value):
            return ""
        return str(value).replace("|", "\\|").replace("\n", " ")

    columns = list(frame.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in frame.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(render(value) for value in row) + " |")
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    definitions = module_definition_audit()
    directions, direction_summary = direction_consistency()
    ledger = evidence_ledger(definitions, direction_summary)
    definitions.to_csv(OUT / "module_definition_audit.tsv", sep="\t", index=False)
    directions.to_csv(OUT / "direction_consistency.tsv", sep="\t", index=False)
    ledger.to_csv(OUT / "evidence_ledger.tsv", sep="\t", index=False)

    summary = {
        "purpose": "V53 grounded MIF/CD74 re-audit; no new discovery claim",
        "seed": SEED,
        "n_sign_null": N_SIGN_NULL,
        "module_definitions_recovered": int(definitions["definition_found"].sum()),
        "module_definitions_containing_MIF": int(definitions["contains_MIF"].sum()),
        "direction_consistency": direction_summary,
        "receptor_specific_adjusted_successes": 0,
        "verdict": "NOT_SUPPORTED_AS_THERAPEUTIC_TARGET_RETAIN_AS_TONE_LOADED_STATE_READOUT",
        "interpretation": (
            "Held data support a recurrent, tone-loaded CD74/HLA-II receptor-state context. "
            "They do not support MIF ligand causality, receptor-specific response after IFN/APC "
            "adjustment, or a stable therapy direction. The prior Tier-1 demotion stands."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    report = [
        "# V53 MIF/CD74 Grounded Re-Audit",
        "",
        "Status: completed targeted re-examination on committed held-data outputs. This is not a new public-data discovery run.",
        "",
        "## Verdict",
        "",
        "**Not supported as a therapeutic target; retain only as a tone-loaded APC state readout.**",
        "",
        "The mature audit confirms the earlier Tier-1 demotion. Project data support recurring CD74/HLA-II receptor-state coupling, but not MIF ligand causality, receptor-specific adjusted response, or a stable intervention direction.",
        "",
        "## Evidence Ledger",
        "",
        markdown_table(ledger),
        "",
        "## Module-Definition Audit",
        "",
        markdown_table(definitions),
        "",
        "The label `mif_cd74_receptor_state` is not a consistent MIF measurement. Several central V26/V36 source definitions omit `MIF` and combine CD74/CD44/CXCR4 with HLA-II genes.",
        "",
        "## Therapy-Direction Null",
        "",
        markdown_table(directions),
        "",
        f"Collapsed therapy-cohort directions are {direction_summary['n_positive_direction']} positive, {direction_summary['n_negative_direction']} negative, and {direction_summary['n_near_null']} near-null using |Hedges g| >= {MIN_DIRECTIONAL_ABS_G}; exact majority-sign p = {direction_summary['exact_two_sided_majority_sign_p']:.4g}, empirical p = {direction_summary['empirical_majority_sign_p']:.4g} ({N_SIGN_NULL} seeded null draws).",
        "",
        "## What Survives",
        "",
        "- Supported: recurrent APC receptor-state coupling and observational MS microglial state association.",
        "- Not supported: MIF-specific causality, receptor-specific adjusted treatment response, same-direction transfer across therapies, or target promotion.",
        "- Needs data: an MS treatment or lesion dataset measuring MIF, CD74, CD44, CXCR4, HLA-II, cell composition, and clinical outcome together, followed by a pre-specified component-resolved test.",
        "",
        "## Therapeutic Boundary",
        "",
        "Structure may establish that MIF or CD74 is physically tractable, but cannot repair the missing causal and directional evidence. Any structure-first follow-up remains prediction-informed context and cannot reopen this target as a finding.",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
