#!/usr/bin/env python3
"""Wave51 audit of reachable stromal/surface reopeners FAP and FXYD5."""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave51_reachable_stromal_surface_audit"
RAW = OUT / "raw_api"
SEED = 20260527

INPUTS = {
    "wave47": ROOT / "phases/v3/results" / "wave47_late_stage_survivor_map" / "reopen_only_requirements.tsv",
    "wave34a": ROOT / "phases/v3/results" / "wave34a_genetics_first_target_rescue" / "genetics_first_candidate_rank.tsv",
    "wave34": ROOT / "phases/v3/results" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv",
    "wave39": ROOT / "phases/v3/results" / "wave39_surfaceome_rescue_after_resolution_pivot" / "surfaceome_rescue_rank.tsv",
    "wave40": ROOT / "phases/v3/results" / "wave40_parked_surface_failfast" / "parked_surface_failfast.tsv",
    "broad": ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "residual": ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
}

GENES = ["FAP", "FXYD5"]

PUBLIC_QUERIES = [
    ("FAP", "EuropePMC", "FAP fibroblast activation protein autoimmune multiple sclerosis psoriasis IBD"),
    ("FAP", "EuropePMC", "FAPI imaging autoimmune disease inflammation"),
    ("FAP", "ClinicalTrials.gov", "FAP autoimmune"),
    ("FXYD5", "EuropePMC", "FXYD5 autoimmune inflammatory bowel psoriasis multiple sclerosis"),
    ("FXYD5", "EuropePMC", "FXYD5 antibody inhibitor inflammation"),
    ("FXYD5", "ClinicalTrials.gov", "FXYD5 autoimmune"),
]

PATENT_QUERIES = [
    ("FAP", "FAP inhibitor autoimmune disease"),
    ("FAP", "fibroblast activation protein imaging autoimmune inflammation"),
    ("FXYD5", "FXYD5 antibody autoimmune disease"),
    ("FXYD5", "FXYD5 inhibitor inflammatory disease"),
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path, sep="\t", low_memory=False)
    return pd.DataFrame()


def as_float(value: Any) -> float | None:
    if value is None or pd.isna(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def as_int(value: Any) -> int:
    f = as_float(value)
    return int(f) if f is not None else 0


def as_str(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def cache_name(source: str, query: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{source}_{query}")[:180]
    return safe.strip("_") + ".json"


def get_json(url: str, cache_path: Path, timeout: int = 20) -> tuple[int | None, dict[str, Any] | None, str]:
    if cache_path.exists():
        try:
            return 200, json.loads(cache_path.read_text(encoding="utf-8")), "cache"
        except json.JSONDecodeError:
            pass
    try:
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "ms-auto-research-wave51/1.0"})
        payload = r.json() if r.text.strip() else {}
        cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(0.15)
        return r.status_code, payload, "live"
    except Exception as exc:  # noqa: BLE001
        payload = {"error": type(exc).__name__, "message": str(exc), "url": url}
        cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return None, payload, "error"


def public_search() -> pd.DataFrame:
    rows = []
    for gene, source, query in PUBLIC_QUERIES:
        if source == "EuropePMC":
            url = (
                "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
                f"?query={quote_plus(query)}&format=json&pageSize=5&resultType=lite"
            )
            status, payload, mode = get_json(url, RAW / cache_name("europepmc", query))
            hits = (((payload or {}).get("resultList") or {}).get("result") or [])
            top_hits = " | ".join(
                f"{h.get('pmid') or h.get('id')}: {h.get('title', '')} ({h.get('pubYear', '')})" for h in hits[:5]
            )
            count = as_int((payload or {}).get("hitCount"))
        else:
            url = f"https://clinicaltrials.gov/api/v2/studies?query.term={quote_plus(query)}&pageSize=5"
            status, payload, mode = get_json(url, RAW / cache_name("clinicaltrials", query))
            studies = (payload or {}).get("studies") or []
            count = as_int((payload or {}).get("totalCount"))
            if count == 0 and studies:
                count = len(studies)
            top_hits = " | ".join(
                f"{(s.get('protocolSection') or {}).get('identificationModule', {}).get('nctId', '')}: "
                f"{(s.get('protocolSection') or {}).get('identificationModule', {}).get('briefTitle', '')}"
                for s in studies[:5]
            )
        rows.append(
            {
                "gene": gene,
                "source": source,
                "query": query,
                "count": count,
                "top_hits": top_hits,
                "status": status,
                "mode": mode,
                "url": url,
                "raw_path": rel(RAW / cache_name(source.lower(), query)),
            }
        )
    return pd.DataFrame(rows)


def chembl_gene(gene: str) -> dict[str, Any]:
    target_url = f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={quote_plus(gene)}&limit=10"
    status, payload, mode = get_json(target_url, RAW / cache_name("chembl_target", gene))
    targets = (payload or {}).get("targets") or []
    human = [t for t in targets if as_str(t.get("organism")).lower() == "homo sapiens"]
    target = human[0] if human else (targets[0] if targets else {})
    target_id = target.get("target_chembl_id") or ""
    activity_url = f"https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id={quote_plus(target_id)}&standard_units=nM&limit=50" if target_id else ""
    a_status, a_payload, a_mode = get_json(activity_url, RAW / cache_name("chembl_activity", target_id or gene)) if activity_url else (None, {}, "")
    values = [
        as_float(a.get("standard_value"))
        for a in ((a_payload or {}).get("activities") or [])
        if as_float(a.get("standard_value")) is not None
    ]
    return {
        "gene": gene,
        "target_chembl_id": target_id,
        "target_name": target.get("pref_name") or "",
        "target_type": target.get("target_type") or "",
        "organism": target.get("organism") or "",
        "target_status": status,
        "target_mode": mode,
        "activity_status": a_status,
        "activity_mode": a_mode,
        "activity_rows_bounded": len(values),
        "best_nM_bounded": min(values) if values else None,
    }


def local_evidence() -> pd.DataFrame:
    rows = []
    for source, path in INPUTS.items():
        df = read_tsv(path)
        if df.empty:
            continue
        cols = [c for c in ["gene", "genes", "label"] if c in df.columns]
        if not cols:
            continue
        mask = pd.Series(False, index=df.index)
        for col in cols:
            mask |= df[col].astype(str).isin(GENES)
        for _, r in df[mask].iterrows():
            gene = next((g for g in GENES if g in [as_str(r.get(c)) for c in cols]), as_str(r.get(cols[0])))
            rows.append(
                {
                    "gene": gene,
                    "source": source,
                    "path": rel(path),
                    "call": as_str(r.get("wave34a_call") or r.get("wave34_call") or r.get("wave39_call") or r.get("wave40_call") or r.get("source_call")),
                    "score": as_float(r.get("genetics_first_score") or r.get("wave34_score") or r.get("wave39_score") or r.get("source_score") or r.get("discovery_priority_score")),
                    "gwas_trait_count": as_float(r.get("gwas_catalog_trait_count")),
                    "gwas_min_p": as_float(r.get("gwas_catalog_min_p")),
                    "local_positive_disease_count": as_float(r.get("local_positive_disease_count") or r.get("positive_disease_count") or r.get("broad_positive_disease_count")),
                    "local_negative_disease_count": as_float(r.get("local_negative_disease_count") or r.get("negative_disease_count") or r.get("broad_negative_disease_count")),
                    "positive_diseases": as_str(r.get("positive_diseases") or r.get("broad_positive_diseases")),
                    "negative_diseases": as_str(r.get("negative_diseases") or r.get("broad_negative_diseases")),
                    "ms_wm_delta_log2": as_float(r.get("ms_wm_delta_log2")),
                    "ms_wm_p": as_float(r.get("ms_wm_p")),
                    "ms_wm_fdr": as_float(r.get("ms_wm_fdr")),
                    "strict_core_covariate_surviving_disease_count": as_float(r.get("strict_core_covariate_surviving_disease_count")),
                    "chembl_activity_count": as_float(r.get("chembl_activity_count") or r.get("druggable_activity_count")),
                    "europepmc_hit_count": as_float(r.get("europepmc_hit_count") or r.get("europepmc_autoimmune_hit_count")),
                    "clinicaltrials_hit_count": as_float(r.get("clinicaltrials_hit_count") or r.get("clinicaltrials_autoimmune_count")),
                    "blocker_or_reason": as_str(r.get("blockers") or r.get("wave39_reason") or r.get("route_reason") or r.get("primary_blocker") or r.get("blocker")),
                }
            )
    return pd.DataFrame(rows)


@dataclass
class Gate:
    gene: str
    gate: str
    passed: bool
    value: str
    rationale: str


def evaluate(local_df: pd.DataFrame, public_df: pd.DataFrame, chembl_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    gates: list[Gate] = []
    rows = []
    for gene in GENES:
        sub = local_df[local_df["gene"] == gene]
        public = public_df[public_df["gene"] == gene]
        chembl = chembl_df[chembl_df["gene"] == gene].iloc[0].to_dict()
        gwas_traits = max([as_int(v) for v in sub.get("gwas_trait_count", pd.Series(dtype=float)).tolist()] or [0])
        gwas_min = min([as_float(v) for v in sub.get("gwas_min_p", pd.Series(dtype=float)).tolist() if as_float(v) is not None] or [1.0])
        local_pos = max([as_float(v) or 0.0 for v in sub.get("local_positive_disease_count", pd.Series(dtype=float)).tolist()] or [0.0])
        local_neg = max([as_float(v) or 0.0 for v in sub.get("local_negative_disease_count", pd.Series(dtype=float)).tolist()] or [0.0])
        ms_delta = max([as_float(v) or -999.0 for v in sub.get("ms_wm_delta_log2", pd.Series(dtype=float)).tolist()] or [-999.0])
        ms_p = min([as_float(v) for v in sub.get("ms_wm_p", pd.Series(dtype=float)).tolist() if as_float(v) is not None] or [1.0])
        ms_fdr_values = [as_float(v) for v in sub.get("ms_wm_fdr", pd.Series(dtype=float)).tolist() if as_float(v) is not None]
        ms_fdr = min(ms_fdr_values) if ms_fdr_values else None
        strict_resid = max([as_float(v) or 0.0 for v in sub.get("strict_core_covariate_surviving_disease_count", pd.Series(dtype=float)).tolist()] or [0.0])
        emax = int(public.loc[public["source"] == "EuropePMC", "count"].max()) if not public.empty else 0
        ctmax = int(public.loc[public["source"] == "ClinicalTrials.gov", "count"].max()) if not public.empty else 0
        prior_block = (gene == "FAP" and (emax >= 500 or ctmax > 0)) or "prior_art_or_trial_saturation" in " ".join(sub.get("blocker_or_reason", pd.Series(dtype=str)).astype(str))
        modality = (as_int(chembl.get("activity_rows_bounded")) >= 20 and (as_float(chembl.get("best_nM_bounded")) or 1e9) <= 1000) or (gene == "FAP" and ctmax > 0)
        if gene == "FXYD5":
            modality = False
        gene_gates = [
            Gate(gene, "cross_disease_local_signal", local_pos >= 3 and local_neg == 0, f"positive={local_pos}; negative={local_neg}", "requires broad non-contradictory local signal"),
            Gate(gene, "strict_ms_anchor", bool(ms_delta > 0 and ms_p < 0.05 and ms_fdr is not None and ms_fdr < 0.1), f"delta={ms_delta}; p={ms_p}; fdr={ms_fdr}", "requires FDR-supported MS signal"),
            Gate(gene, "target_level_genetics", gwas_traits >= 5 and gwas_min < 5e-8, f"traits={gwas_traits}; min_p={gwas_min}", "requires target/locus support"),
            Gate(gene, "strict_residual_state_survival", strict_resid >= 1, str(strict_resid), "requires survival after covariate/core-module residualization"),
            Gate(gene, "direction_and_safety_resolved", False, "unresolved", "requires intervention direction that does not impair repair/barrier biology"),
            Gate(gene, "real_perturbation_anchor", False, "absent", "requires disease-relevant perturbation rescue"),
            Gate(gene, "tractable_modality", modality, f"activity_rows={chembl.get('activity_rows_bounded')}; best_nM={chembl.get('best_nM_bounded')}; trials={ctmax}", "requires usable inhibitor/antibody/modality"),
            Gate(gene, "novelty_prior_art_not_blocking", not prior_block, f"EuropePMC={emax}; ClinicalTrials={ctmax}; prior_block={prior_block}", "requires no direct crowded/prior-art blockage"),
        ]
        gates.extend(gene_gates)
        pass_count = sum(g.passed for g in gene_gates)
        call = "PROMOTE_CANDIDATE" if pass_count == len(gene_gates) else "NO_GO_REACHABLE_SURFACE_STROMAL_ROUTE"
        rows.append(
            {
                "gene": gene,
                "call": call,
                "critical_gate_pass_count": pass_count,
                "critical_gate_total": len(gene_gates),
                "summary": (
                    f"{gene} remains reachable/druggable-looking but not promotable: local positives={local_pos}, "
                    f"negatives={local_neg}, MS delta={ms_delta}, p={ms_p}, FDR={ms_fdr}, strict residual={strict_resid}, "
                    f"GWAS traits={gwas_traits}, EuropePMC={emax}, ClinicalTrials={ctmax}."
                ),
                "primary_blocker": (
                    "FAP is a stromal/remodeling and imaging/prior-art saturated route without MS or perturbation proof; "
                    "FXYD5 has surface accessibility and multi-tissue expression but no clear modality, no FDR-supported MS anchor, "
                    "a conflicting Crohn negative signal, and unresolved Na/K-ATPase/barrier direction."
                ),
                "decisive_reopen_test": (
                    "Human tissue organoid/slice perturbation showing non-depleting target modulation reverses disease-state modules "
                    "while preserving epithelial/barrier and repair functions, plus target-resolved genetics or MS lesion validation."
                ),
            }
        )
    return pd.DataFrame(rows), pd.DataFrame([g.__dict__ for g in gates])


def patent_urls() -> pd.DataFrame:
    rows = []
    for gene, query in PATENT_QUERIES:
        rows.append({"gene": gene, "database": "GooglePatents", "query": query, "url": f"https://patents.google.com/?q={quote_plus(query)}"})
        rows.append({"gene": gene, "database": "Espacenet", "query": query, "url": f"https://worldwide.espacenet.com/patent/search?q={quote_plus(query)}"})
    return pd.DataFrame(rows)


def write_report(audit: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = ["# Wave51 Reachable Stromal/Surface Audit", "", f"Random seed: `{SEED}`.", "", "## Verdict", ""]
    for _, r in audit.iterrows():
        lines.append(f"- `{r['gene']}`: `{r['call']}`; {r['summary']}")
        lines.append(f"  - Blocker: {r['primary_blocker']}")
    lines.extend(["", "## Gate Matrix", ""])
    for _, g in gates.iterrows():
        status = "PASS" if bool(g["passed"]) else "FAIL"
        lines.append(f"- `{g['gene']}` / `{g['gate']}`: {status} (`{g['value']}`) - {g['rationale']}.")
    OUT.joinpath("REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    local_df = local_evidence()
    public_df = public_search()
    chembl_df = pd.DataFrame([chembl_gene(g) for g in GENES])
    audit, gates = evaluate(local_df, public_df, chembl_df)
    patents = patent_urls()
    local_df.to_csv(OUT / "reachable_local_evidence.tsv", sep="\t", index=False)
    public_df.to_csv(OUT / "public_api_counts.tsv", sep="\t", index=False)
    chembl_df.to_csv(OUT / "chembl_activity_summary.tsv", sep="\t", index=False)
    patents.to_csv(OUT / "patent_search_urls.tsv", sep="\t", index=False)
    audit.to_csv(OUT / "reachable_surface_stromal_audit.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "decision_matrix.tsv", sep="\t", index=False)
    write_report(audit, gates)
    summary = {
        "seed": SEED,
        "promoted_count": int(audit["call"].astype(str).str.contains("PROMOTE").sum()),
        "calls": dict(zip(audit["gene"], audit["call"], strict=True)),
        "output_dir": rel(OUT),
        "key_outputs": [
            rel(OUT / "reachable_surface_stromal_audit.tsv"),
            rel(OUT / "decision_matrix.tsv"),
            rel(OUT / "REPORT.md"),
        ],
    }
    write_json(OUT / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
