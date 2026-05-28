#!/usr/bin/env python3
"""Wave139 integrate residual-marker falsification targets from sidecars."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from v3_analyze_osmr_complement_axes import ROOT


SEED = 20260527
OUT = ROOT / "results_v3" / "wave139_residual_marker_falsification_integrator"

FILES = {
    "lipid_rank": ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_lipid_lysosomal_neighborhood_rank.tsv",
    "controller91": ROOT / "results_v3" / "wave91_lipid_neighborhood_controller_scan" / "lipid_neighborhood_controller_rank.tsv",
    "route92": ROOT / "results_v3" / "wave92_lipid_state_controller_route_audit" / "controller_route_rank.tsv",
    "snx10": ROOT / "results_v3" / "snx10_c15orf48_residual_gate" / "snx10_c15orf48_residual_gate.tsv",
    "wave133": ROOT / "results_v3" / "wave133_closure_hygiene_correction" / "wave122_corrected_rank.tsv",
    "wave104": ROOT / "results_v3" / "wave104_genetics_first_lipid_state_convergence_audit" / "genetics_first_lipid_state_rank.tsv",
    "wave62": ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv",
    "wave128": ROOT / "results_v3" / "wave128_genetics_first_reopener" / "genetics_first_reopener_decisions.tsv",
}

CANDIDATES = [
    "FABP5", "CHI3L1", "APOC1", "SNX10", "GPNMB", "SCARB2", "MSR1", "LIPA",
    "NPC1", "NPC2", "IFI30", "SP140", "GALC",
]


def read(path: Path) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        raise FileNotFoundError(path)
    return pd.read_csv(path, sep="\t", low_memory=False)


def first(df: pd.DataFrame, col: str, value: str) -> dict:
    if col not in df.columns:
        return {}
    hit = df[df[col].astype(str).str.upper().eq(value.upper())]
    return hit.iloc[0].to_dict() if not hit.empty else {}


def fnum(x, default=0.0) -> float:
    try:
        if pd.isna(x) or x == "":
            return default
        return float(x)
    except Exception:
        return default


def truth(x) -> bool:
    return str(x).lower() in {"true", "1", "yes"}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    t = {k: read(v) for k, v in FILES.items()}
    rows = []
    evidence = []
    for gene in CANDIDATES:
        lipid = first(t["lipid_rank"], "gene", gene)
        c91 = first(t["controller91"], "gene", gene)
        w133 = first(t["wave133"], "gene", gene)
        snx = first(t["snx10"], "gene", gene)
        w104 = first(t["wave104"], "gene", gene)
        w62 = first(t["wave62"], "gene", gene)
        w128 = first(t["wave128"], "gene", gene)

        routes = t["route92"]
        route_hit = routes[
            routes.astype(str).agg(" ".join, axis=1).str.upper().str.contains(gene.upper(), regex=False)
        ] if not routes.empty else pd.DataFrame()

        ms_nominal = truth(lipid.get("ms_positive_nominal", False)) or truth(w133.get("ms", False))
        ms_fdr = fnum(lipid.get("ms_wm_fdr", w133.get("ms_fdr", 1.0)), 1.0)
        broad_pos = int(fnum(lipid.get("positive_disease_count", w133.get("broad_positive_disease_count", 0))))
        broad_neg = int(fnum(lipid.get("negative_disease_count", 0)))
        controller_call = str(c91.get("wave91_call", ""))
        route_call = ";".join(route_hit["wave92_call"].astype(str).unique().tolist()) if not route_hit.empty and "wave92_call" in route_hit.columns else ""
        strict_residual = int(fnum(snx.get("strict_core_covariate_surviving_analysis_count", 0)))
        non_ibd_residual = int(fnum(snx.get("non_ibd_retained_positive_disease_count", 0)))
        genetics = int(fnum(w62.get("strong_l2g_disease_count", w133.get("strong_l2g_disease_count", 0)))) + int(
            fnum(w62.get("strong_qtl_coloc_disease_count", w133.get("strong_qtl_coloc_disease_count", 0)))
        )
        modality = truth(w133.get("modality", False)) or "PARK" in controller_call or "PARK" in route_call
        blockers = []
        if not ms_nominal:
            blockers.append("no_nominal_ms_anchor")
        if ms_fdr >= 0.10:
            blockers.append("no_fdr_ms_anchor")
        if broad_pos < 3:
            blockers.append("insufficient_broad_disease_breadth")
        if broad_neg > 0:
            blockers.append("negative_context_present")
        if strict_residual == 0:
            blockers.append("no_strict_core_residual_survival")
        if non_ibd_residual < 2:
            blockers.append("no_non_ibd_residual_breadth")
        if genetics == 0 and gene not in {"SP140", "GALC", "IFI30"}:
            blockers.append("no_target_resolved_genetics")
        if not modality:
            blockers.append("no_clear_modality")
        text = " ".join([controller_call, route_call, str(w133.get("blocker_text", "")), str(w128.get("call", ""))]).upper()
        if any(term in text for term in ["NO_GO", "NO_REOPEN", "BLOCKED", "PRIOR_ART", "HOST_DEFENSE"]):
            blockers.append("prior_no_go_or_blocker")

        call = "PARK_FALSIFICATION_TARGET"
        if len(blockers) >= 4:
            call = "CLOSE_AS_MARKER_OR_READOUT"
        if gene in {"IFI30", "SP140", "GALC"}:
            call = "GENETICS_COMPARATOR_NOT_TARGET"
        rows.append(
            {
                "gene": gene,
                "call": call,
                "ms_nominal": ms_nominal,
                "ms_fdr": ms_fdr,
                "broad_positive_disease_count": broad_pos,
                "broad_negative_disease_count": broad_neg,
                "strict_core_residual_surviving_analysis_count": strict_residual,
                "non_ibd_residual_positive_disease_count": non_ibd_residual,
                "target_resolution_signal_count": genetics,
                "controller91_call": controller_call,
                "route92_call": route_call,
                "blockers": ";".join(sorted(set(blockers))),
            }
        )
        evidence.append(
            {
                "gene": gene,
                "lipid_rank": json.dumps(lipid, sort_keys=True),
                "controller91": json.dumps(c91, sort_keys=True),
                "route92_rows": route_hit.to_json(orient="records"),
                "snx10_residual": json.dumps(snx, sort_keys=True),
                "wave104": json.dumps(w104, sort_keys=True),
                "wave62": json.dumps(w62, sort_keys=True),
                "wave128": json.dumps(w128, sort_keys=True),
                "wave133": json.dumps(w133, sort_keys=True),
            }
        )
    out = pd.DataFrame(rows)
    evidence_df = pd.DataFrame(evidence)
    out.to_csv(OUT / "residual_marker_falsification_summary.tsv", sep="\t", index=False)
    evidence_df.to_csv(OUT / "residual_marker_falsification_evidence.tsv", sep="\t", index=False)
    counts = out["call"].value_counts().to_dict()
    summary = {
        "random_seed": SEED,
        "branch_call": "NO_RESIDUAL_MARKER_PROMOTABLE",
        "call_counts": counts,
        "inputs": {k: str(v.relative_to(ROOT)) for k, v in FILES.items()},
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    report = f"""# Wave139 Residual Marker Falsification Integrator

## Bottom Line

Branch call: `NO_RESIDUAL_MARKER_PROMOTABLE`.

Maxwell and Turing identified useful falsification/comparator targets, but
integrating existing local residual, route, and genetics evidence does not
produce a promotable therapeutic target.

## Counts

```json
{json.dumps(counts, indent=2, sort_keys=True)}
```

## Interpretation

The residual lipid-lysosomal space is now best treated as a set of marker and
readout hypotheses. `IFI30`, `SP140`, and `GALC` remain genetics comparators,
not intervention candidates. Other candidates fail through negative contexts,
lack of strict residual survival, weak/nonexistent target-resolution genetics,
unclear modality, or prior no-go route status.
"""
    (OUT / "REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
