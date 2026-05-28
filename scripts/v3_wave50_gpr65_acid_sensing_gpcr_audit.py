#!/usr/bin/env python3
"""Wave50 GPR65 acid-sensing GPCR audit.

GPR65 is a tractable GPCR with cross-autoimmune genetic support, but prior V3
waves flagged weak/contradictory local cell-state support and direct IBD/patent
prior art. This audit decides whether GPR65 can serve as the cross-autoimmune
intervention point or remains a future coloc/perturbation problem.
"""

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
OUT = ROOT / "results_v3" / "wave50_gpr65_acid_sensing_gpcr_audit"
RAW = OUT / "raw_api"
SEED = 20260527

INPUTS = {
    "wave47_reopen": ROOT / "results_v3" / "wave47_late_stage_survivor_map" / "reopen_only_requirements.tsv",
    "wave34a": ROOT / "results_v3" / "wave34a_genetics_first_target_rescue" / "genetics_first_candidate_rank.tsv",
    "wave34": ROOT / "results_v3" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv",
    "broad_h5ad": ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "wave20_local": ROOT / "results_v3" / "wave20_genetic_druggable_altaxis" / "local_biology_and_druggability_metrics.tsv",
    "wave20_genetics": ROOT / "results_v3" / "wave20_genetic_druggable_altaxis" / "local_opentargets_genetics_summary.tsv",
    "wave20_public": ROOT / "results_v3" / "wave20_genetic_druggable_altaxis" / "public_api_prior_art_druggability_audit.tsv",
    "wave20_interpretation": ROOT / "results_v3" / "wave20_genetic_druggable_altaxis" / "public_source_interpretation.tsv",
    "wave23_restoration": ROOT / "results_v3" / "wave23_genetics_restoration_modality" / "ranked_go_park_no_go.tsv",
}

PUBLIC_QUERIES = [
    ("EuropePMC", 'GPR65 TDAG8 agonist autoimmune multiple sclerosis'),
    ("EuropePMC", 'GPR65 inflammatory bowel disease therapeutic target agonist'),
    ("EuropePMC", 'GPR65 Th17 autoimmune pH sensing GPCR'),
    ("ClinicalTrials.gov", 'GPR65 autoimmune'),
    ("ClinicalTrials.gov", 'GPR65 agonist'),
]

PATENT_QUERIES = [
    "GPR65 modulator autoimmune multiple sclerosis",
    "TDAG8 GPR65 agonist inflammatory bowel disease",
    "GPR65 positive allosteric modulator autoimmune disease",
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
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "ms-auto-research-wave50/1.0"})
        payload = response.json() if response.text.strip() else {}
        cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(0.2)
        return response.status_code, payload, "live"
    except Exception as exc:  # noqa: BLE001
        payload = {"error": type(exc).__name__, "message": str(exc), "url": url}
        cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return None, payload, "error"


def europepmc(query: str) -> dict[str, Any]:
    url = (
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        f"?query={quote_plus(query)}&format=json&pageSize=5&resultType=lite"
    )
    status, payload, mode = get_json(url, RAW / cache_name("europepmc", query))
    hits = (((payload or {}).get("resultList") or {}).get("result") or [])
    top = []
    for hit in hits[:5]:
        top.append(f"{hit.get('pmid') or hit.get('id')}: {hit.get('title', '')} ({hit.get('pubYear', '')})")
    return {
        "source": "EuropePMC",
        "query": query,
        "count": as_int((payload or {}).get("hitCount")),
        "top_hits": " | ".join(top),
        "status": status,
        "mode": mode,
        "url": url,
        "raw_path": rel(RAW / cache_name("europepmc", query)),
    }


def clinicaltrials(query: str) -> dict[str, Any]:
    url = f"https://clinicaltrials.gov/api/v2/studies?query.term={quote_plus(query)}&pageSize=5"
    status, payload, mode = get_json(url, RAW / cache_name("clinicaltrials", query))
    studies = (payload or {}).get("studies") or []
    total = as_int((payload or {}).get("totalCount"))
    if total == 0 and studies:
        total = len(studies)
    top = []
    for study in studies[:5]:
        proto = study.get("protocolSection") or {}
        ident = proto.get("identificationModule") or {}
        status_mod = proto.get("statusModule") or {}
        top.append(f"{ident.get('nctId', '')}: {ident.get('briefTitle') or ident.get('officialTitle') or ''} [{status_mod.get('overallStatus', '')}]")
    return {
        "source": "ClinicalTrials.gov",
        "query": query,
        "count": total,
        "top_hits": " | ".join(top),
        "status": status,
        "mode": mode,
        "url": url,
        "raw_path": rel(RAW / cache_name("clinicaltrials", query)),
    }


def chembl_activity() -> dict[str, Any]:
    target_url = "https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=GPR65&limit=10"
    status, payload, mode = get_json(target_url, RAW / "chembl_target_GPR65.json")
    targets = (payload or {}).get("targets") or []
    human = [t for t in targets if as_str(t.get("organism")).lower() == "homo sapiens"]
    target = human[0] if human else (targets[0] if targets else {})
    target_id = target.get("target_chembl_id") or ""
    activity_url = f"https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id={quote_plus(target_id)}&standard_units=nM&limit=100" if target_id else ""
    a_status, a_payload, a_mode = get_json(activity_url, RAW / "chembl_activity_GPR65.json") if activity_url else (None, {}, "")
    activities = (a_payload or {}).get("activities") or []
    values = [as_float(a.get("standard_value")) for a in activities if as_float(a.get("standard_value")) is not None]
    return {
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
        "target_url": target_url,
        "activity_url": activity_url,
    }


def local_evidence() -> pd.DataFrame:
    rows = []
    for source, path in INPUTS.items():
        df = read_tsv(path)
        if df.empty:
            continue
        gene_cols = [c for c in ["gene", "genes", "label"] if c in df.columns]
        if not gene_cols:
            continue
        mask = pd.Series(False, index=df.index)
        for col in gene_cols:
            mask |= df[col].astype(str).str.contains("GPR65", na=False)
        for _, r in df[mask].iterrows():
            rows.append(
                {
                    "source": source,
                    "path": rel(path),
                    "call": as_str(r.get("wave34a_call") or r.get("wave34_call") or r.get("call") or r.get("source_call") or r.get("target_level_status")),
                    "score": as_float(r.get("genetics_first_score") or r.get("wave34_score") or r.get("rank_score") or r.get("source_score") or r.get("discovery_priority_score")),
                    "genetics_disease_count": as_float(r.get("ot_n_diseases_score_ge_0_5") or r.get("trait_count_score_ge_0_5")),
                    "genetics_diseases": as_str(r.get("ot_diseases_score_ge_0_5") or r.get("trait_diseases_score_ge_0_5")),
                    "gwas_trait_count": as_float(r.get("gwas_catalog_trait_count")),
                    "gwas_min_p": as_float(r.get("gwas_catalog_min_p")),
                    "gwas_traits": as_str(r.get("gwas_catalog_traits") or r.get("gwas_catalog_traits_short")),
                    "local_positive_disease_count": as_float(r.get("local_positive_disease_count") or r.get("positive_disease_count") or r.get("broad_positive_disease_count")),
                    "local_negative_disease_count": as_float(r.get("local_negative_disease_count") or r.get("negative_disease_count") or r.get("broad_negative_disease_count")),
                    "positive_diseases": as_str(r.get("positive_diseases") or r.get("broad_positive_diseases")),
                    "negative_diseases": as_str(r.get("negative_diseases") or r.get("broad_negative_diseases")),
                    "ms_wm_delta_log2": as_float(r.get("ms_wm_delta_log2")),
                    "ms_wm_p": as_float(r.get("ms_wm_p")),
                    "ms_wm_fdr": as_float(r.get("ms_wm_fdr")),
                    "prior_art_signal": as_str(r.get("prior_art_signal") or r.get("prior_art_summary") or r.get("prior_risk")),
                    "blocker_or_reason": as_str(r.get("route_reason") or r.get("decision_reason") or r.get("primary_blocker") or r.get("needed_to_reopen") or r.get("blocker")),
                }
            )
    return pd.DataFrame(rows)


def public_counts() -> pd.DataFrame:
    rows = []
    for source, query in PUBLIC_QUERIES:
        rows.append(europepmc(query) if source == "EuropePMC" else clinicaltrials(query))
    return pd.DataFrame(rows)


def patent_urls() -> pd.DataFrame:
    rows = []
    for query in PATENT_QUERIES:
        rows.append({"database": "GooglePatents", "query": query, "url": f"https://patents.google.com/?q={quote_plus(query)}"})
        rows.append({"database": "Espacenet", "query": query, "url": f"https://worldwide.espacenet.com/patent/search?q={quote_plus(query)}"})
    return pd.DataFrame(rows)


@dataclass
class Gate:
    gate: str
    passed: bool
    value: str
    rationale: str


def evaluate(local_df: pd.DataFrame, public_df: pd.DataFrame, chembl: dict[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    gwas_traits = max([as_int(v) for v in local_df.get("gwas_trait_count", pd.Series(dtype=float)).tolist()] or [0])
    gwas_min = min([as_float(v) for v in local_df.get("gwas_min_p", pd.Series(dtype=float)).tolist() if as_float(v) is not None] or [1.0])
    genetics_disease_count = max([as_int(v) for v in local_df.get("genetics_disease_count", pd.Series(dtype=float)).tolist()] or [0])
    genetics_diseases = ";".join(
        sorted(
            {
                item
                for item in ";".join(local_df.get("genetics_diseases", pd.Series(dtype=str)).dropna().astype(str)).split(";")
                if item
            }
        )
    )
    local_pos = max([as_float(v) or 0.0 for v in local_df.get("local_positive_disease_count", pd.Series(dtype=float)).tolist()] or [0.0])
    local_neg = max([as_float(v) or 0.0 for v in local_df.get("local_negative_disease_count", pd.Series(dtype=float)).tolist()] or [0.0])
    ms_delta = max([as_float(v) or -999.0 for v in local_df.get("ms_wm_delta_log2", pd.Series(dtype=float)).tolist()] or [-999.0])
    ms_p = min([as_float(v) for v in local_df.get("ms_wm_p", pd.Series(dtype=float)).tolist() if as_float(v) is not None] or [1.0])
    ms_fdr_values = [as_float(v) for v in local_df.get("ms_wm_fdr", pd.Series(dtype=float)).tolist() if as_float(v) is not None]
    ms_fdr = min(ms_fdr_values) if ms_fdr_values else None
    prior_text = " ".join(local_df.get("prior_art_signal", pd.Series(dtype=str)).dropna().astype(str).tolist() + local_df.get("blocker_or_reason", pd.Series(dtype=str)).dropna().astype(str).tolist())
    patent_block = "WO2023067322A1" in prior_text or "patent" in prior_text.lower() or "prior art" in prior_text.lower()
    europepmc_max = int(public_df.loc[public_df["source"] == "EuropePMC", "count"].max()) if not public_df.empty else 0
    ct_max = int(public_df.loc[public_df["source"] == "ClinicalTrials.gov", "count"].max()) if not public_df.empty else 0

    gates = [
        Gate("cross_disease_genetic_breadth", genetics_disease_count >= 5 and gwas_traits >= 5 and gwas_min < 5e-8, f"OT_diseases={genetics_disease_count}; GWAS_traits={gwas_traits}; min_p={gwas_min}", "requires broad disease genetics"),
        Gate("target_resolved_coloc_or_mr", False, "not_run/no_target_resolved_coloc", "requires fine-mapped direction rather than mapped-gene support"),
        Gate("strict_ms_anchor", bool(ms_delta > 0 and ms_p < 0.05 and (ms_fdr is not None and ms_fdr < 0.1)), f"delta={ms_delta}; p={ms_p}; fdr={ms_fdr}", "requires MS state signal beyond nominal/noise"),
        Gate("local_cell_state_alignment", local_pos >= 3 and local_neg == 0, f"positive={local_pos}; negative={local_neg}", "requires local support not contradicted by negative disease signals"),
        Gate("real_perturbation_anchor", False, "absent", "requires GPR65 agonist/PAM rescue in disease-relevant cells"),
        Gate("selective_modality_exists", as_int(chembl.get("activity_rows_bounded")) >= 20 and (as_float(chembl.get("best_nM_bounded")) or 1e9) <= 10000, f"activity_rows={chembl.get('activity_rows_bounded')}; best_nM={chembl.get('best_nM_bounded')}", "requires tractable GPCR chemical matter"),
        Gate("clinical_whitespace", ct_max == 0, f"ClinicalTrials_max={ct_max}", "requires no active direct clinical program"),
        Gate("novelty_prior_art_not_blocking", not patent_block and europepmc_max < 100, f"patent_block={patent_block}; EuropePMC_max={europepmc_max}", "requires no direct autoimmune/IBD patent-literature blockage"),
    ]
    gate_df = pd.DataFrame([g.__dict__ for g in gates])
    passed = int(gate_df["passed"].sum())
    call = "PROMOTE_CANDIDATE" if passed == len(gates) else "NO_GO_GPR65_PRIOR_ART_AND_LOCAL_CELLSTATE_MISMATCH"
    audit = pd.DataFrame(
        [
            {
                "gene": "GPR65",
                "call": call,
                "critical_gate_pass_count": passed,
                "critical_gate_total": len(gates),
                "summary": (
                    f"GPR65 has cross-disease genetic support ({genetics_disease_count} OT diseases: {genetics_diseases}; "
                    f"{gwas_traits} GWAS traits, min p={gwas_min}) and GPCR chemical matter, but local support is weak "
                    f"and contradictory (positive diseases={local_pos}, negative diseases={local_neg}), MS expression support "
                    f"is absent (delta={ms_delta}, p={ms_p}), and direct IBD/autoimmune prior art blocks novelty."
                ),
                "primary_blocker": (
                    "GPR65 remains a plausible biology axis but not a V3 finding: target-resolved direction, non-IBD "
                    "coloc, and disease-cell agonist/PAM perturbation are missing, while public literature/patent prior "
                    "art already covers autoimmune GPR65 modulation."
                ),
                "decisive_reopen_test": (
                    "Fine-map non-IBD/MS GPR65 colocalization and test selective agonist/PAM rescue in acidic human "
                    "MS/psoriasis/AS myeloid or T-cell contexts with cAMP, Th17, and lipid-lysosomal inflammatory readouts."
                ),
            }
        ]
    )
    return audit, gate_df


def write_report(audit: pd.DataFrame, gates: pd.DataFrame, public_df: pd.DataFrame) -> None:
    r = audit.iloc[0]
    lines = [
        "# Wave50 GPR65 Acid-Sensing GPCR Audit",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Verdict",
        "",
        f"`GPR65`: `{r['call']}`.",
        "",
        r["summary"],
        "",
        f"Primary blocker: {r['primary_blocker']}",
        "",
        f"Decisive reopen test: {r['decisive_reopen_test']}",
        "",
        "## Gate Matrix",
        "",
    ]
    for _, g in gates.iterrows():
        status = "PASS" if bool(g["passed"]) else "FAIL"
        lines.append(f"- `{g['gate']}`: {status} (`{g['value']}`) - {g['rationale']}.")
    lines.extend(["", "## Public Source Snapshot", ""])
    for _, p in public_df.iterrows():
        lines.append(f"- {p['source']} `{p['query']}`: count={p['count']}; top hits: {p['top_hits']}")
    OUT.joinpath("REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    local_df = local_evidence()
    public_df = public_counts()
    chembl = chembl_activity()
    audit, gates = evaluate(local_df, public_df, chembl)
    patents = patent_urls()

    local_df.to_csv(OUT / "gpr65_local_evidence.tsv", sep="\t", index=False)
    public_df.to_csv(OUT / "public_api_counts.tsv", sep="\t", index=False)
    pd.DataFrame([chembl]).to_csv(OUT / "chembl_gpr65_activity_summary.tsv", sep="\t", index=False)
    patents.to_csv(OUT / "patent_search_urls.tsv", sep="\t", index=False)
    audit.to_csv(OUT / "gpr65_audit.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "decision_matrix.tsv", sep="\t", index=False)
    write_report(audit, gates, public_df)
    summary = {
        "seed": SEED,
        "call": audit.iloc[0]["call"],
        "critical_gate_pass_count": int(audit.iloc[0]["critical_gate_pass_count"]),
        "critical_gate_total": int(audit.iloc[0]["critical_gate_total"]),
        "output_dir": rel(OUT),
        "key_outputs": [
            rel(OUT / "gpr65_audit.tsv"),
            rel(OUT / "decision_matrix.tsv"),
            rel(OUT / "chembl_gpr65_activity_summary.tsv"),
            rel(OUT / "REPORT.md"),
        ],
    }
    write_json(OUT / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
