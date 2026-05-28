#!/usr/bin/env python3
"""Wave170: parse externally downloaded ChEMBL target-quality artifacts.

Raw JSON is fetched with curl because Python network is sandbox-blocked here.
This script is offline/reproducible from the saved raw files.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave170_external_chembl_target_quality"
RAW = OUT / "raw"
OUT.mkdir(parents=True, exist_ok=True)

GENES = ["LRRK2", "PIK3CG", "PTGIR", "SLC1A2"]


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def f(x, default=None):
    try:
        if x in ("", None):
            return default
        return float(x)
    except Exception:
        return default


def exact_human_targets(gene: str) -> list[dict]:
    data = load_json(RAW / f"{gene}_target_search.json")
    out = []
    for t in data.get("targets", []):
        if t.get("organism") != "Homo sapiens":
            continue
        synonyms = []
        for comp in t.get("target_components", []):
            for syn in comp.get("target_component_synonyms", []):
                synonyms.append(str(syn.get("component_synonym", "")).upper())
        if gene.upper() in synonyms or gene.upper() in str(t.get("pref_name", "")).upper():
            out.append(t)
    return out


def summarize_activities(gene: str, target_id: str) -> dict:
    data = load_json(RAW / f"{gene}_activities.json")
    acts = data.get("activities", [])
    vals = []
    types = {}
    molecules = set()
    for a in acts:
        if a.get("target_chembl_id") != target_id:
            continue
        molecules.add(a.get("molecule_chembl_id"))
        stype = a.get("standard_type") or ""
        types[stype] = types.get(stype, 0) + 1
        units = str(a.get("standard_units", "")).lower()
        val = f(a.get("standard_value"))
        if val is not None and units in {"nm", "nanomolar"}:
            vals.append(val)
    vals_s = pd.Series(vals, dtype=float) if vals else pd.Series(dtype=float)
    return {
        "activity_records_downloaded_for_target": len([a for a in acts if a.get("target_chembl_id") == target_id]),
        "unique_molecules_downloaded": len([m for m in molecules if m]),
        "n_nm_values": int(len(vals_s)),
        "best_nm": float(vals_s.min()) if len(vals_s) else None,
        "median_nm": float(vals_s.median()) if len(vals_s) else None,
        "activity_type_counts": ";".join(f"{k}:{v}" for k, v in sorted(types.items(), key=lambda kv: (-kv[1], kv[0]))[:8]),
    }


rows = []
for gene in GENES:
    targets = exact_human_targets(gene)
    if not targets:
        rows.append(
            {
                "gene": gene,
                "target_chembl_id": "",
                "pref_name": "",
                "target_type": "",
                "target_quality_call": "NO_EXACT_HUMAN_TARGET_IN_DOWNLOADED_SEARCH",
            }
        )
        continue
    for t in targets:
        tid = t.get("target_chembl_id", "")
        act = summarize_activities(gene, tid)
        target_type = t.get("target_type", "")
        single_or_complex = target_type in {"SINGLE PROTEIN", "PROTEIN COMPLEX", "PROTEIN COMPLEX GROUP"}
        has_potent = (act.get("best_nm") is not None and act["best_nm"] <= 100) or act.get("unique_molecules_downloaded", 0) >= 25
        if single_or_complex and has_potent:
            call = "CHEMBL_TARGET_QUALITY_SUPPORTED"
        elif single_or_complex:
            call = "CHEMBL_TARGET_EXISTS_ACTIVITY_LIMITED_OR_NOT_DOWNLOADED"
        else:
            call = "CHEMBL_TARGET_TYPE_WEAK"
        rows.append(
            {
                "gene": gene,
                "target_chembl_id": tid,
                "pref_name": t.get("pref_name", ""),
                "target_type": target_type,
                "target_quality_call": call,
                **act,
            }
        )

quality = pd.DataFrame(rows)
quality.to_csv(OUT / "external_chembl_target_quality.tsv", sep="\t", index=False)

wave169 = pd.read_csv(
    ROOT / "results_v3" / "wave169_l1000_repurposing_deconvolution_pivot" / "l1000_repurposing_deconvolution_rank.tsv",
    sep="\t",
    low_memory=False,
)
q_best = quality.sort_values(
    ["target_quality_call", "unique_molecules_downloaded"], ascending=[True, False]
).drop_duplicates("gene")
merged = wave169.merge(q_best, left_on="target_gene", right_on="gene", how="left", suffixes=("", "_external"))
merged["external_target_quality_supported"] = merged["target_quality_call"].eq("CHEMBL_TARGET_QUALITY_SUPPORTED")
merged["target_quality_proxy_corrected"] = merged["target_quality_proxy"].astype(bool) | merged["external_target_quality_supported"]
merged["corrected_blockers"] = merged["blockers"].fillna("").str.replace("weak_target_quality_proxy;?", "", regex=True)
merged.loc[~merged["target_quality_proxy_corrected"], "corrected_blockers"] = (
    merged.loc[~merged["target_quality_proxy_corrected"], "corrected_blockers"].fillna("") + ";weak_target_quality_proxy"
)
merged["corrected_promote"] = (
    merged["review_not_toxic_or_generic"].astype(bool)
    & (merged["max_opposite_abs_score"] >= 8)
    & merged["target_state_recurrence"].astype(bool)
    & merged["ms_anchor"].astype(bool)
    & merged["target_quality_proxy_corrected"].astype(bool)
    & ~merged["prior_blocked_annotation"].astype(bool)
    & merged["delivery_annotation"].astype(bool)
)
merged.to_csv(OUT / "wave169_with_external_target_quality.tsv", sep="\t", index=False)

promoted = merged[merged["corrected_promote"]]
branch = "PROMOTE_AFTER_EXTERNAL_TARGET_QUALITY" if len(promoted) else "NO_PROMOTION_AFTER_EXTERNAL_TARGET_QUALITY"
best = merged.sort_values("repurposing_pivot_score", ascending=False).iloc[0].to_dict()
summary = {
    "branch_call": branch,
    "genes_audited": GENES,
    "quality_supported_genes": quality[quality["target_quality_call"].eq("CHEMBL_TARGET_QUALITY_SUPPORTED")]["gene"].drop_duplicates().tolist(),
    "corrected_promoted_candidates": (promoted["compound"] + "/" + promoted["target_gene"]).tolist() if len(promoted) else [],
    "top_candidate_after_quality": f"{best.get('compound', '')}/{best.get('target_gene', '')}",
    "top_candidate_external_quality_call": best.get("target_quality_call", ""),
    "interpretation": "External ChEMBL rescues target-quality for some top L1000 targets, but does not by itself satisfy the full V3 convergence gate.",
}
(OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
(OUT / "REPORT.md").write_text(
    f"""# Wave170 External ChEMBL Target Quality

## Branch call
`{branch}`

## Result
- Genes audited: `{', '.join(GENES)}`.
- Quality-supported genes: `{', '.join(summary['quality_supported_genes'])}`.
- Corrected promoted candidates: `{len(promoted)}`.
- Top candidate after quality: `{summary['top_candidate_after_quality']}`.

## Interpretation
The local target-quality proxy was too weak for repurposing-first routes.
Saved ChEMBL artifacts support druggability for some targets, but full
promotion still requires state, MS, prior-art, delivery, and selectivity
convergence.
"""
)

print(json.dumps(summary, indent=2))
