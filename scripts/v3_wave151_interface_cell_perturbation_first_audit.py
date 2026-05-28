#!/usr/bin/env python3
"""Wave151: interface-cell perturbation-first audit.

This wave responds to Euler's critique. It asks whether any available real
perturbation signatures support reversal of interface-cell disease programs for
barrier/metabolite/TLS routes, rather than requiring paired myeloid/APC receiver
effects.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_direct_h5ad_cell_states import ROOT


OUT = ROOT / "results_v3" / "wave151_interface_cell_perturbation_first_audit"
SEED = 20260527

ROUTE_TO_ARCH = {
    "ahr_tryptophan": None,
    "scfa_ffar_hcar": None,
    "bile_acid_fxr_tgr5": None,
    "retinoid_vdr_rxr": None,
    "tnfsf14_light_hvem_ltbr": "tls_lymphoid_niche",
    "endothelial_entry": "endothelial_entry",
    "stromal_retention_fibrosis": "stromal_retention_fibrosis",
    "tls_lymphoid_niche": "tls_lymphoid_niche",
}

FILES = {
    "w23_routes": ROOT / "results_v3" / "wave23_metabolite_barrier_circuit" / "wave23_ranked_routes.tsv",
    "w23_l1000": ROOT / "results_v3" / "wave23_metabolite_barrier_circuit" / "route_l1000_matches.tsv",
    "w23_presence": ROOT / "results_v3" / "wave23_metabolite_barrier_circuit" / "lincs_compound_presence.tsv",
    "w146_source": ROOT / "results_v3" / "wave146_architecture_first_barrier_retention_scan" / "architecture_source_disease_tests.tsv",
    "w146_ms": ROOT / "results_v3" / "wave146_architecture_first_barrier_retention_scan" / "architecture_ms_anchor.tsv",
    "w148": ROOT / "results_v3" / "wave148_tnfsf14_light_lymphoid_niche_audit" / "summary.json",
}


def read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    w23 = read(FILES["w23_routes"])
    l1000 = read(FILES["w23_l1000"])
    presence = read(FILES["w23_presence"])
    source = read(FILES["w146_source"])
    ms = read(FILES["w146_ms"])

    rows = []
    for route, arch in ROUTE_TO_ARCH.items():
        r23 = w23[w23["route"].eq(route)].iloc[0].to_dict() if not w23.empty and route in set(w23["route"]) else {}
        route_l1000 = l1000[l1000["route"].eq(route)].copy() if not l1000.empty and "route" in l1000.columns else pd.DataFrame()
        route_presence = presence[presence["route"].eq(route)].copy() if not presence.empty and "route" in presence.columns else pd.DataFrame()
        arch_source = source[source["module"].eq(arch)].copy() if arch and not source.empty else pd.DataFrame()
        arch_ms = ms[ms["module"].eq(arch)].iloc[0].to_dict() if arch and not ms.empty and arch in set(ms["module"]) else {}

        interface_positive = int(((arch_source["delta_case_minus_control"] > 0) & (arch_source["p"] < 0.05)).sum()) if not arch_source.empty else int(r23.get("route_positive_disease_union_count", 0) or 0)
        interface_diseases = (
            sorted(arch_source.loc[(arch_source["delta_case_minus_control"] > 0) & (arch_source["p"] < 0.05), "disease_name"].unique().tolist())
            if not arch_source.empty
            else str(r23.get("route_positive_disease_union", "")).split(";") if r23 else []
        )
        real_reversal = int(((route_l1000["mode"].eq("opposite")) & (route_l1000["min_qval"] <= 0.05)).sum()) if not route_l1000.empty else 0
        compound_presence = int(len(route_presence))
        ms_anchor = False
        if arch_ms:
            ms_anchor = bool(int(arch_ms.get("n_fdr_positive_genes", 0) or 0) > 0)
        elif r23:
            try:
                ms_anchor = float(r23.get("best_ms_wm_p", 1) or 1) < 0.05 and float(r23.get("best_ms_wm_delta_log2", 0) or 0) > 0
            except Exception:
                ms_anchor = False
        prior_clear = str(r23.get("not_already_crowded_assessment", "")).lower() in {"yes", "least_crowded_but_unsupported"}
        real_interface_context = False
        # Local L1000FWD outputs do not carry epithelial/endothelial/fibroblast
        # perturbation context labels; treat them as non-interface-specific.
        context_note = "no interface-cell perturbation context available in local L1000/Perturb-seq outputs"
        passes = interface_positive >= 2 and real_reversal >= 1 and ms_anchor and prior_clear and real_interface_context
        rows.append(
            {
                "route": route,
                "architecture_module": arch or "",
                "interface_positive_count": interface_positive,
                "interface_positive_diseases": ";".join([d for d in interface_diseases if d]),
                "available_compound_presence_count": compound_presence,
                "real_l1000_reversal_q_le_0_05_count": real_reversal,
                "ms_anchor": ms_anchor,
                "prior_clear_or_least_crowded": prior_clear,
                "real_interface_perturbation_context": real_interface_context,
                "context_note": context_note,
                "passes_wave151": passes,
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "interface_perturbation_route_audit.tsv", sep="\t", index=False)
    passing = out[out["passes_wave151"]]
    branch = "INTERFACE_PERTURBATION_ROUTE_REOPENED" if len(passing) else "NO_INTERFACE_CELL_PERTURBATION_ROUTE"
    missing = (
        "No local real perturbation dataset provides disease-relevant human epithelial/endothelial/fibroblast/TLS-cell "
        "perturbations for these routes with interface-cell context labels. LINCS availability is mostly generic cell-line "
        "compound presence/reversal, not autoimmune interface-cell rescue."
    )
    summary = {
        "branch_call": branch,
        "random_seed": SEED,
        "n_routes": int(len(out)),
        "n_passing_routes": int(len(passing)),
        "missing_external_requirement": missing,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    report = [
        "# Wave151 Interface-Cell Perturbation-First Audit",
        "",
        f"Branch call: `{branch}`.",
        "",
        "Interpretation:",
        "- This wave does not close barrier biology globally.",
        "- It closes the current local evidence branch because available perturbation evidence is not disease-relevant interface-cell perturbation evidence.",
        f"- Missing external requirement: {missing}",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
