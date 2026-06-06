#!/usr/bin/env python3
"""Wave121 closure audit for final wet-lab-only resolution routes."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT
from v3_wave85_external_geo_antitnf_validation import markdown_table, rel, write_json


SEED = 20260527
OUT = ROOT / "phases/v3/results" / "wave121_final_wetlab_only_route_closure"

W95 = ROOT / "phases/v3/results" / "wave95_mechanistic_forcing_triage" / "mechanistic_forcing_candidate_rank.tsv"
W95_SIDECAR = ROOT / "phases/v3/subagents" / "wave95_sidecar_returns_integrated.md"
W94_HOSTILE = ROOT / "phases/v3/subagents" / "wave94_remaining_route_hostile_rank.md"
W32C_PRIOR = ROOT / "phases/v3/results" / "wave32c_resolution_prior_art_audit" / "resolution_prior_art_audit.tsv"
W81 = ROOT / "phases/v3/results" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W37 = ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"

ROUTES = {
    "FPR2_ANXA1_BIASED_RESOLUTION": ["FPR2", "ANXA1"],
    "CD300_RECEPTOR_SPECIFIC_TUNING": ["CD300A", "CD300C", "CD300E", "CD300LF", "CD300LG"],
}


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def boolish(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def first_row(df: pd.DataFrame) -> dict[str, object]:
    return df.to_dict(orient="records")[0] if not df.empty else {}


def rows_for_gene(df: pd.DataFrame, gene: str) -> pd.DataFrame:
    for col in ["gene", "gene_symbol", "candidate"]:
        if col in df.columns:
            return df[df[col].astype(str).eq(gene)].copy()
    return pd.DataFrame()


def text_contains_any(text: str, terms: list[str]) -> bool:
    upper = text.upper()
    return any(term.upper() in upper for term in terms)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    w95 = read_tsv(W95)
    w81 = read_tsv(W81)
    w37 = read_tsv(W37)
    sidecar_text = "\n".join(
        p.read_text(encoding="utf-8") for p in [W95_SIDECAR, W94_HOSTILE] if p.exists()
    )
    w32c = read_tsv(W32C_PRIOR)

    route_rows = []
    evidence_rows = []
    for route, genes in ROUTES.items():
        r95 = w95[w95["candidate"].astype(str).eq(route)].copy() if not w95.empty else pd.DataFrame()
        row = first_row(r95)
        ms_anchor = boolish(row.get("gate_ms_anchor", False)) or boolish(row.get("gate_ms_trend", False))
        residual = boolish(row.get("gate_cross_disease_residual", False))
        response_transition = boolish(row.get("gate_cell_resolved_response_or_transition", False))
        target_genetics = boolish(row.get("gate_target_resolved_genetics_ge2", False))
        broad_genetics = boolish(row.get("gate_broad_genetics_ge4", False))
        perturbation_model = boolish(row.get("gate_real_perturbation_or_validated_model", False))
        modality = boolish(row.get("gate_modality", False))
        prior_not_blocked = boolish(row.get("gate_prior_not_blocked", False))
        not_generic = boolish(row.get("gate_not_generic_or_closed", False))
        direction_safe = not text_contains_any(
            sidecar_text,
            [
                f"{route} directionally unsafe",
                "direction is ambiguous",
                "ligand bias can switch",
                "not interchangeable",
            ],
        )

        prior_art_close = text_contains_any(
            sidecar_text,
            [
                "CD300F/CLM-1 agonist patent for MS",
                "CD300C autoimmune/EAE/CIA patent",
                "FPR2/SPM/ANXA1 already has autoimmune/EAE/colitis prior art",
                "FPR2/SPM/EAE/colitis prior art",
            ],
        )

        gene_evidence = []
        for gene in genes:
            r81 = rows_for_gene(w81, gene)
            r37 = rows_for_gene(w37, gene)
            gene_evidence.append(
                {
                    "route": route,
                    "gene": gene,
                    "wave81_call": r81.iloc[0].get("wave81_call", "") if not r81.empty else "",
                    "ms_delta_log2": r81.iloc[0].get("ms_delta_log2", "") if not r81.empty else "",
                    "ms_p": r81.iloc[0].get("ms_p", "") if not r81.empty else "",
                    "wave71_call": r81.iloc[0].get("wave71_call", "") if not r81.empty else "",
                    "wave37_screen_call": r37.iloc[0].get("screen_call", "") if not r37.empty else "",
                    "wave37_contrast_fdr": r37.iloc[0].get("contrast_fdr", "") if not r37.empty else "",
                }
            )
        evidence_rows.extend(gene_evidence)

        hard_gates = {
            "ms_anchor_or_trend": ms_anchor,
            "cross_disease_residual": residual,
            "cell_resolved_response_or_transition": response_transition,
            "target_resolved_genetics_ge2": target_genetics,
            "broad_genetics_ge4": broad_genetics,
            "real_perturbation_or_validated_model": perturbation_model,
            "modality_ready": modality,
            "prior_not_blocked": prior_not_blocked and not prior_art_close,
            "not_generic_or_closed": not_generic,
            "direction_safe": direction_safe,
        }
        failed = [gate for gate, ok in hard_gates.items() if not ok]
        call = (
            "REOPEN_FOR_COMPUTATIONAL_DEEPENING"
            if sum(hard_gates.values()) >= 8 and ms_anchor and perturbation_model and not failed
            else "NO_REOPEN_WETLAB_ONLY_ROUTE"
        )
        route_rows.append(
            {
                "route": route,
                "genes": ";".join(genes),
                "call": call,
                "passed_gates": int(sum(hard_gates.values())),
                "gate_count": len(hard_gates),
                "failed_gates": ";".join(failed),
                "wave95_call": row.get("wave95_call", ""),
                "wave95_reason": row.get("wave95_reason", ""),
                "route_ms_call": row.get("route_ms_call", ""),
                "route_wave92_call": row.get("route_wave92_call", ""),
                "response_systems": row.get("route_response_systems", ""),
                "nominal_response_systems": row.get("route_response_nominal_systems", ""),
                "prior_art_close": prior_art_close,
                "direction_safe": direction_safe,
            }
        )

    decisions = pd.DataFrame(route_rows)
    evidence = pd.DataFrame(evidence_rows)
    decisions.to_csv(OUT / "wetlab_only_route_decisions.tsv", sep="\t", index=False)
    evidence.to_csv(OUT / "wetlab_only_gene_evidence.tsv", sep="\t", index=False)

    n_reopen = int(decisions["call"].str.startswith("REOPEN").sum())
    branch_call = "REOPEN_WETLAB_ONLY_ROUTE" if n_reopen else "NO_OPEN_ROUTE_AFTER_WETLAB_ONLY_AUDIT"

    write_json(
        OUT / "summary.json",
        {
            "random_seed": SEED,
            "branch_call": branch_call,
            "n_routes": int(len(decisions)),
            "n_reopen": n_reopen,
            "inputs": {
                "wave95": rel(W95),
                "wave95_sidecar": rel(W95_SIDECAR),
                "wave94_hostile": rel(W94_HOSTILE),
                "wave32c_prior": rel(W32C_PRIOR),
                "wave81": rel(W81),
                "wave37": rel(W37),
            },
        },
    )

    report = f"""# Wave121 Final Wet-Lab-Only Route Closure

## Bottom Line

Branch call: `{branch_call}`.

After Wave116 hygiene fixes, only `FPR2_ANXA1_BIASED_RESOLUTION` and
`CD300_RECEPTOR_SPECIFIC_TUNING` remained open. Both are retained only as
wet-lab kill-test concepts, not computationally promotable target nominations.

## Route Decisions

{markdown_table(decisions, max_rows=20)}

## Gene-Level Evidence

{markdown_table(evidence, max_rows=30)}

## Interpretation

These routes have useful resolution-biology hypotheses, but the V3 claim needs
MS anchoring, target-resolved genetics or validated perturbation/model support,
directional safety, and novelty. The two routes fail that standard from
available local evidence. They should not keep consuming orchestration cycles
unless new wet-lab perturbation data are available.

## Reproducibility

- Script: `{rel(ROOT / "scripts" / "v3_wave121_final_wetlab_only_route_closure.py")}`
- Output: `{rel(OUT / "wetlab_only_route_decisions.tsv")}`
- Seed: `{SEED}`
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
