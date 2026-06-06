#!/usr/bin/env python3
"""Wave44 audit of CFB / alternative complement as a stratified repurposing route."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave44_cfb_complement_stratification_audit"
RAW = OUT / "raw_api"
SEED = 20260527

WAVE34 = ROOT / "phases/v3/results" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv"
BROAD = ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
RESIDUAL = ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
WAVE21_PRIOR = ROOT / "phases/v3/results" / "wave21_residual_candidate_prior_art" / "candidate_prior_art_gate.tsv"
WAVE25 = ROOT / "phases/v3/results" / "wave25_causal_genetics_module_proxy" / "causal_proxy_candidate_matrix.tsv"
OSMR_COMPLEMENT = ROOT / "phases/v3/results" / "osmr_complement_axes" / "osmr_complement_summary.json"


@dataclass
class ApiCall:
    source: str
    query: str
    url: str
    status: str
    cache_file: str


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def safe(text: str) -> str:
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in text)[:180]


def fetch_json(source: str, query: str, url: str, cache_name: str, calls: list[ApiCall]) -> dict[str, Any]:
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / f"{safe(cache_name)}.json"
    if cache.exists():
        calls.append(ApiCall(source, query, url, "cache_hit", rel(cache)))
        return json.loads(cache.read_text(encoding="utf-8"))
    try:
        req = Request(url, headers={"User-Agent": "ms-auto-research-wave44/1.0", "Accept": "application/json"})
        with urlopen(req, timeout=45) as handle:
            payload = json.loads(handle.read().decode("utf-8"))
        write_json(cache, payload)
        calls.append(ApiCall(source, query, url, "ok", rel(cache)))
        time.sleep(0.15)
        return payload
    except Exception as exc:  # noqa: BLE001
        payload = {"error": str(exc), "url": url}
        write_json(cache, payload)
        calls.append(ApiCall(source, query, url, f"error:{type(exc).__name__}", rel(cache)))
        return payload


def read_tsv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t", low_memory=False)


def europepmc_count(query: str, calls: list[ApiCall]) -> int | None:
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urlencode(
        {"query": query, "format": "json", "pageSize": 1}
    )
    payload = fetch_json("Europe PMC", query, url, f"europepmc_{query}", calls)
    try:
        return int(payload.get("hitCount"))
    except Exception:
        return None


def clinicaltrials_count(query: str, calls: list[ApiCall]) -> int | None:
    url = "https://clinicaltrials.gov/api/v2/studies?" + urlencode({"query.term": query, "pageSize": 1})
    payload = fetch_json("ClinicalTrials.gov", query, url, f"clinicaltrials_{query}", calls)
    try:
        if payload.get("totalCount") is not None:
            return int(payload.get("totalCount"))
        if isinstance(payload.get("studies"), list):
            return len(payload["studies"])
        return None
    except Exception:
        return None


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        vals = []
        for col in cols:
            val = "" if pd.isna(row[col]) else str(row[col])
            vals.append(val.replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    calls: list[ApiCall] = []

    tables = {
        "wave34": read_tsv(WAVE34),
        "broad": read_tsv(BROAD),
        "residual": read_tsv(RESIDUAL),
        "wave21_prior": read_tsv(WAVE21_PRIOR),
        "wave25": read_tsv(WAVE25),
    }
    cfb_rows = {}
    for name, df in tables.items():
        if not df.empty and "gene" in df.columns:
            cfb_rows[name] = df[df["gene"].astype(str).eq("CFB")].copy()
            cfb_rows[name].to_csv(OUT / f"{name}_CFB_row.tsv", sep="\t", index=False)
        elif not df.empty and "candidate" in df.columns:
            cfb_rows[name] = df[df["candidate"].astype(str).eq("CFB")].copy()
            cfb_rows[name].to_csv(OUT / f"{name}_CFB_row.tsv", sep="\t", index=False)

    complement_summary = {}
    if OSMR_COMPLEMENT.exists():
        complement_summary = json.loads(OSMR_COMPLEMENT.read_text(encoding="utf-8"))

    literature_queries = [
        '"complement factor B" AND ("multiple sclerosis" OR "rheumatoid arthritis" OR "lupus" OR "inflammatory bowel" OR psoriasis)',
        '"factor B inhibitor" AND (autoimmune OR "multiple sclerosis" OR lupus OR "inflammatory bowel")',
        'iptacopan AND (autoimmune OR "multiple sclerosis" OR lupus OR "inflammatory bowel" OR psoriasis)',
        '"CFB" AND ("biomarker" OR "stratification") AND autoimmune',
    ]
    trial_queries = [
        "complement factor B autoimmune",
        "factor B inhibitor autoimmune",
        "iptacopan autoimmune",
        "iptacopan multiple sclerosis",
        "CFB multiple sclerosis",
    ]
    literature = pd.DataFrame([{"query": q, "europepmc_hit_count": europepmc_count(q, calls)} for q in literature_queries])
    trials = pd.DataFrame([{"query": q, "clinicaltrials_count": clinicaltrials_count(q, calls)} for q in trial_queries])
    patents = pd.DataFrame(
        [
            {
                "query": q,
                "google_patents_url": "https://patents.google.com/?" + urlencode({"q": q}),
            }
            for q in [
                "factor B inhibitor autoimmune disease",
                "iptacopan complement factor B multiple sclerosis",
                "CFB biomarker autoimmune factor B inhibitor",
            ]
        ]
    )

    literature.to_csv(OUT / "cfb_literature_query_counts.tsv", sep="\t", index=False)
    trials.to_csv(OUT / "cfb_clinicaltrials_query_counts.tsv", sep="\t", index=False)
    patents.to_csv(OUT / "cfb_patent_search_urls.tsv", sep="\t", index=False)
    pd.DataFrame([asdict(c) for c in calls]).to_csv(OUT / "api_call_log.tsv", sep="\t", index=False)

    wave34 = cfb_rows.get("wave34", pd.DataFrame())
    broad = cfb_rows.get("broad", pd.DataFrame())
    residual = cfb_rows.get("residual", pd.DataFrame())
    prior = cfb_rows.get("wave21_prior", pd.DataFrame())
    wave25 = cfb_rows.get("wave25", pd.DataFrame())

    wave34_r = wave34.iloc[0].to_dict() if not wave34.empty else {}
    broad_r = broad.iloc[0].to_dict() if not broad.empty else {}
    residual_r = residual.iloc[0].to_dict() if not residual.empty else {}
    prior_r = prior.iloc[0].to_dict() if not prior.empty else {}
    wave25_r = wave25.iloc[0].to_dict() if not wave25.empty else {}

    failed_gates = [
        "no_MS_anchor_or_positive_MS_lesion_direction",
        "no_target_resolved_coloc_or_mr",
        "foundation_or_model_support_marked_do_not_promote",
        "strict_core_residual_survival_only_Crohn_stromal",
        "factor_B_inhibition_prior_art_and_trial_crowding",
        "systemic_complement_host_defense_safety",
    ]
    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "target": "CFB / complement factor B / alternative complement amplification",
        "wave44_call": "NO_GO_COMPLEMENT_STRATIFICATION_PRIOR_ART_BLOCKED",
        "promotion_allowed": False,
        "failed_gates": failed_gates,
        "local_evidence": {
            "wave34_call": wave34_r.get("wave34_call"),
            "gwas_catalog_trait_count": wave34_r.get("gwas_catalog_trait_count"),
            "local_positive_disease_count": wave34_r.get("local_positive_disease_count"),
            "residual_retained_disease_count": wave34_r.get("residual_retained_disease_count"),
            "ms_anchor": wave34_r.get("ms_anchor"),
            "ms_wm_delta_log2": wave34_r.get("ms_wm_delta_log2"),
            "ms_wm_p": wave34_r.get("ms_wm_p"),
            "chembl_target_id": wave34_r.get("chembl_target_id"),
            "chembl_best_nM": wave34_r.get("chembl_best_nM"),
            "clinicaltrials_autoimmune_count_wave34": wave34_r.get("clinicaltrials_autoimmune_count"),
            "broad_top_positive_compartments": broad_r.get("top_positive_compartments"),
            "strict_core_covariate_surviving_analyses": residual_r.get("strict_core_covariate_surviving_analyses"),
            "wave21_recommendation": prior_r.get("recommendation"),
            "wave21_prior_blockers": prior_r.get("prior_art_blockers"),
            "wave25_proxy_call": wave25_r.get("proxy_call"),
            "wave25_decision_reason": wave25_r.get("decision_reason"),
        },
        "query_counts": {
            "literature": literature.to_dict("records"),
            "clinicaltrials": trials.to_dict("records"),
        },
        "interpretation": (
            "CFB is a strong comparator route, not a V3 finding. It has broad local tissue recurrence, CFB druggability, "
            "and residual signal in Crohn/stromal contexts, but no MS anchor, no target-resolved causal genetic package, "
            "no favorable perturbation/model support, and heavy factor-B inhibitor prior art/trial crowding. A biomarker-selected "
            "CFB-high autoimmune subgroup remains plausible only as a clinical-repurposing hypothesis outside this V3 claim."
        ),
        "output_paths": {
            "literature_counts": rel(OUT / "cfb_literature_query_counts.tsv"),
            "clinicaltrials_counts": rel(OUT / "cfb_clinicaltrials_query_counts.tsv"),
            "patent_urls": rel(OUT / "cfb_patent_search_urls.tsv"),
            "api_call_log": rel(OUT / "api_call_log.tsv"),
        },
    }
    write_json(OUT / "summary.json", summary)

    lines = [
        "# Wave44 CFB Complement Stratification Audit",
        "",
        "## Result",
        "",
        summary["interpretation"],
        "",
        "## Failed Gates",
        "",
        "\n".join(f"- {x}" for x in failed_gates),
        "",
        "## Wave34 CFB Row",
        "",
        markdown_table(wave34),
        "",
        "## Residual CFB Row",
        "",
        markdown_table(residual),
        "",
        "## Prior-Art Query Counts",
        "",
        markdown_table(literature),
        "",
        markdown_table(trials),
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
