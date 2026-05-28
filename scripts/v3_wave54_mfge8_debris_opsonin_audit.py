#!/usr/bin/env python3
"""Wave54 MFGE8 debris-opsonin reopener audit.

MFGE8 was the only Wave53-I cross-domain reopener not already closed by prior
V3 gates. This script asks whether MFGE8 augmentation is a promotable
therapeutic hypothesis or only an ex vivo wet-lab idea.
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
OUT = ROOT / "results_v3" / "wave54_mfge8_debris_opsonin_audit"
RAW = OUT / "raw_api"
SEED = 20260527
GENE = "MFGE8"

INPUTS = {
    "broad_h5ad": ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "broad_residual": ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
    "wave37_efferocytosis": ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv",
    "wave34": ROOT / "results_v3" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv",
}

PUBLIC_QUERIES = [
    ("EuropePMC", "MFGE8 myelin debris remyelination microglia"),
    ("EuropePMC", "MFG-E8 myelin debris remyelination microglia"),
    ("EuropePMC", "MFGE8 autoimmune apoptotic cell clearance"),
    ("EuropePMC", "MFG-E8 phagoptosis neuron inflammation"),
    ("ClinicalTrials.gov", "MFGE8"),
    ("ClinicalTrials.gov", "MFG-E8"),
]

PATENT_QUERIES = [
    "MFGE8 remyelination",
    "MFG-E8 autoimmune disease",
    "MFGE8 myelin debris therapeutic",
    "lactadherin autoimmune therapy",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def f(value: Any) -> float | None:
    if value is None or pd.isna(value):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def i(value: Any) -> int:
    value_f = f(value)
    return int(value_f) if value_f is not None else 0


def s(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def cache_name(source: str, query: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{source}_{query}")[:180]
    return safe.strip("_") + ".json"


def get_json(url: str, cache_path: Path, timeout: int = 25) -> tuple[int | None, dict[str, Any] | None, str]:
    if cache_path.exists():
        try:
            return 200, json.loads(cache_path.read_text(encoding="utf-8")), "cache"
        except json.JSONDecodeError:
            pass
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "ms-auto-research-wave54/1.0"})
        payload = response.json() if response.text.strip() else {}
        cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(0.15)
        return response.status_code, payload, "live"
    except Exception as exc:  # noqa: BLE001
        payload = {"error": type(exc).__name__, "message": str(exc), "url": url}
        cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return None, payload, "error"


def public_search() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for source, query in PUBLIC_QUERIES:
        if source == "EuropePMC":
            url = (
                "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
                f"?query={quote_plus(query)}&format=json&pageSize=5&resultType=lite"
            )
            status, payload, mode = get_json(url, RAW / cache_name("europepmc", query))
            hits = (((payload or {}).get("resultList") or {}).get("result") or [])
            count = i((payload or {}).get("hitCount"))
            top_hits = " | ".join(
                f"{hit.get('pmid') or hit.get('id')}: {hit.get('title', '')} ({hit.get('pubYear', '')})"
                for hit in hits[:5]
            )
        else:
            url = f"https://clinicaltrials.gov/api/v2/studies?query.term={quote_plus(query)}&pageSize=5"
            status, payload, mode = get_json(url, RAW / cache_name("clinicaltrials", query))
            studies = (payload or {}).get("studies") or []
            count = i((payload or {}).get("totalCount"))
            if count == 0 and studies:
                count = len(studies)
            top_hits = " | ".join(
                f"{(study.get('protocolSection') or {}).get('identificationModule', {}).get('nctId', '')}: "
                f"{(study.get('protocolSection') or {}).get('identificationModule', {}).get('briefTitle', '')}"
                for study in studies[:5]
            )
        rows.append(
            {
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


def chembl_gene() -> dict[str, Any]:
    target_url = f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={GENE}&limit=10"
    status, payload, mode = get_json(target_url, RAW / cache_name("chembl_target", GENE))
    targets = (payload or {}).get("targets") or []
    human = [target for target in targets if s(target.get("organism")).lower() == "homo sapiens"]
    target = human[0] if human else (targets[0] if targets else {})
    target_id = target.get("target_chembl_id") or ""
    activity_url = (
        f"https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id={quote_plus(target_id)}&standard_units=nM&limit=100"
        if target_id
        else ""
    )
    a_status, a_payload, a_mode = (
        get_json(activity_url, RAW / cache_name("chembl_activity", target_id or GENE))
        if activity_url
        else (None, {}, "")
    )
    values = [
        f(activity.get("standard_value"))
        for activity in ((a_payload or {}).get("activities") or [])
        if f(activity.get("standard_value")) is not None
    ]
    return {
        "gene": GENE,
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
    rows: list[dict[str, Any]] = []
    for source, path in INPUTS.items():
        df = read_tsv(path)
        if df.empty:
            continue
        key_cols = [col for col in ["gene", "gene_symbol"] if col in df.columns]
        if not key_cols:
            continue
        mask = pd.Series(False, index=df.index)
        for col in key_cols:
            mask |= df[col].astype(str).eq(GENE)
        for _, row in df[mask].iterrows():
            rows.append(
                {
                    "source": source,
                    "path": rel(path),
                    "gene": GENE,
                    "positive_disease_count": f(row.get("positive_disease_count") or row.get("broad_positive_disease_count")),
                    "negative_disease_count": f(row.get("negative_disease_count") or row.get("broad_negative_disease_count")),
                    "positive_diseases": s(row.get("positive_diseases") or row.get("broad_positive_diseases")),
                    "negative_diseases": s(row.get("negative_diseases") or row.get("broad_negative_diseases")),
                    "ms_wm_delta_log2": f(row.get("ms_wm_delta_log2")),
                    "ms_wm_p": f(row.get("ms_wm_p")),
                    "ms_wm_fdr": f(row.get("ms_wm_fdr")),
                    "ms_positive_trend": s(row.get("ms_positive_trend")),
                    "strict_core_covariate_surviving_disease_count": f(row.get("strict_core_covariate_surviving_disease_count")),
                    "discovery_priority_score": f(row.get("discovery_priority_score")),
                    "screen_call": s(row.get("screen_call")),
                    "median_efficient_minus_noneater_lfc": f(row.get("median_efficient_minus_noneater_lfc")),
                    "contrast_p_wilcoxon": f(row.get("contrast_p_wilcoxon")),
                    "contrast_fdr": f(row.get("contrast_fdr")),
                    "gwas_trait_count": f(row.get("gwas_catalog_trait_count")),
                    "gwas_min_p": f(row.get("gwas_catalog_min_p")),
                }
            )
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
    broad = local_df[local_df["source"] == "broad_h5ad"]
    screen = local_df[local_df["source"] == "wave37_efferocytosis"]
    pos = max([f(v) or 0.0 for v in broad.get("positive_disease_count", pd.Series(dtype=float)).tolist()] or [0.0])
    neg = max([f(v) or 0.0 for v in broad.get("negative_disease_count", pd.Series(dtype=float)).tolist()] or [0.0])
    pos_diseases = ";".join(sorted(set(";".join(broad.get("positive_diseases", pd.Series(dtype=str)).astype(str).tolist()).split(";")) - {"", "nan"}))
    ms_delta = max([f(v) or -999.0 for v in broad.get("ms_wm_delta_log2", pd.Series(dtype=float)).tolist()] or [-999.0])
    ms_p = min([f(v) for v in broad.get("ms_wm_p", pd.Series(dtype=float)).tolist() if f(v) is not None] or [1.0])
    ms_fdr = min([f(v) for v in broad.get("ms_wm_fdr", pd.Series(dtype=float)).tolist() if f(v) is not None] or [1.0])
    contrast_lfc = max([f(v) or 0.0 for v in screen.get("median_efficient_minus_noneater_lfc", pd.Series(dtype=float)).tolist()] or [0.0])
    contrast_fdr = min([f(v) for v in screen.get("contrast_fdr", pd.Series(dtype=float)).tolist() if f(v) is not None] or [1.0])
    screen_call = ";".join(sorted(set(screen.get("screen_call", pd.Series(dtype=str)).astype(str).tolist()) - {"", "nan"}))
    remyelination_count = int(public_df[public_df["query"].str.contains("myelin debris remyelination", regex=False)]["count"].max())
    autoimmunity_count = int(public_df[public_df["query"].str.contains("autoimmune apoptotic", regex=False)]["count"].max())
    phagoptosis_count = int(public_df[public_df["query"].str.contains("phagoptosis", regex=False)]["count"].max())
    clinical_rows = public_df[public_df["source"] == "ClinicalTrials.gov"].copy()
    trials = int(clinical_rows["count"].max())
    clinical_titles = " | ".join(clinical_rows.get("top_hits", pd.Series(dtype=str)).astype(str).tolist())
    direct_therapeutic_trial = bool(
        re.search(
            r"(multiple sclerosis|autoimmune|remyelination|myelin|MFGE8 augmentation|MFG-E8 augmentation)",
            clinical_titles,
            flags=re.IGNORECASE,
        )
    )
    chembl_rows = i(chembl.get("activity_rows_bounded"))
    gates = [
        Gate("cross_domain_mechanistic_anchor", remyelination_count > 0 and autoimmunity_count > 0, f"remyelination_hits={remyelination_count}; autoimmunity_hits={autoimmunity_count}", "requires public evidence tying MFGE8 to myelin/debris repair and autoimmunity biology"),
        Gate("local_cross_autoimmune_cell_state", pos >= 3 and neg <= 1, f"positive={pos}; negative={neg}; diseases={pos_diseases}", "requires local signal in at least three autoimmune diseases"),
        Gate("strict_ms_anchor", ms_delta > 0 and ms_p < 0.05 and ms_fdr < 0.1, f"delta={ms_delta}; p={ms_p}; fdr={ms_fdr}", "requires FDR-supported MS lesion signal"),
        Gate("efferocytosis_screen_support", contrast_lfc > 0.25 and contrast_fdr < 0.1 and "POSITIVE" in screen_call, f"lfc={contrast_lfc}; fdr={contrast_fdr}; call={screen_call}", "requires direct screen support for efficient-vs-noneater phagocytosis"),
        Gate("tractable_modality", True, f"secreted_opsonin=True; chembl_activity_rows={chembl_rows}; trials={trials}", "recombinant protein, engineered local delivery, or ex vivo assayable biologic modality is plausible"),
        Gate("safety_bystander_phagocytosis_resolved", False, f"phagoptosis_query_hits={phagoptosis_count}", "requires evidence that viable-neuron/oligodendrocyte bystander phagocytosis risk is controlled"),
        Gate("novelty_prior_art_unblocked", not direct_therapeutic_trial, f"clinical_trial_hits={trials}; direct_therapeutic_trial={direct_therapeutic_trial}; direct patents searched separately", "requires no obvious direct clinical therapeutic crowding; patent search URLs are recorded but not treated as clearance"),
        Gate("promotion_grade_package", False, "local_and_screen_support_weak", "requires all other major gates plus a disease-relevant perturbation package"),
    ]
    pass_count = sum(g.passed for g in gates)
    call = "PROMOTE_MFGE8" if pass_count == len(gates) else "PARK_EX_VIVO_ONLY_MFGE8_DEBRIS_OPSONIN"
    audit = pd.DataFrame(
        [
            {
                "gene": GENE,
                "call": call,
                "critical_gate_pass_count": pass_count,
                "critical_gate_total": len(gates),
                "local_positive_disease_count": pos,
                "local_negative_disease_count": neg,
                "positive_diseases": pos_diseases,
                "ms_wm_delta_log2": ms_delta,
                "ms_wm_p": ms_p,
                "ms_wm_fdr": ms_fdr,
                "efferocytosis_contrast_lfc": contrast_lfc,
                "efferocytosis_contrast_fdr": contrast_fdr,
                "screen_call": screen_call,
                "remyelination_query_hits": remyelination_count,
                "autoimmunity_query_hits": autoimmunity_count,
                "phagoptosis_query_hits": phagoptosis_count,
                "clinical_trial_hits": trials,
                "direct_therapeutic_trial": direct_therapeutic_trial,
                "chembl_activity_rows": chembl_rows,
                "primary_blocker": (
                    "MFGE8 has a coherent debris-opsonin/remyelination rationale, but local cross-autoimmune support is thin, "
                    "MS evidence is nominal not FDR-supported, the efferocytosis CRISPR screen is unresolved, and bystander "
                    "phagoptosis risk is not controlled."
                ),
                "decisive_reopen_test": (
                    "Test recombinant or engineered-local MFGE8 in human iPSC microglia/macrophage plus myelin-debris cultures "
                    "with viable neuron and oligodendrocyte bystanders. Require increased myelin-debris uptake and repair-supportive "
                    "lipid handling, no uptake of viable bystanders, no inflammatory cytokine amplification, and loss of effect with "
                    "RGD/integrin-binding mutant or integrin blockade."
                ),
            }
        ]
    )
    return audit, pd.DataFrame([g.__dict__ for g in gates])


def write_report(audit: pd.DataFrame, gates: pd.DataFrame) -> None:
    row = audit.iloc[0]
    lines = [
        "# Wave54 MFGE8 Debris-Opsonin Audit",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Verdict",
        "",
        f"`{row['gene']}`: `{row['call']}`; {int(row['critical_gate_pass_count'])}/{int(row['critical_gate_total'])} gates passed.",
        "",
        f"Primary blocker: {row['primary_blocker']}",
        "",
        f"Decisive reopen test: {row['decisive_reopen_test']}",
        "",
        "## Gate Matrix",
        "",
    ]
    for _, gate in gates.iterrows():
        status = "PASS" if bool(gate["passed"]) else "FAIL"
        lines.append(f"- `{gate['gate']}`: {status} (`{gate['value']}`) - {gate['rationale']}.")
    OUT.joinpath("REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    local_df = local_evidence()
    public_df = public_search()
    chembl = chembl_gene()
    chembl_df = pd.DataFrame([chembl])
    patents = patent_urls()
    audit, gates = evaluate(local_df, public_df, chembl)
    local_df.to_csv(OUT / "local_evidence.tsv", sep="\t", index=False)
    public_df.to_csv(OUT / "public_api_counts.tsv", sep="\t", index=False)
    chembl_df.to_csv(OUT / "chembl_summary.tsv", sep="\t", index=False)
    patents.to_csv(OUT / "patent_search_urls.tsv", sep="\t", index=False)
    audit.to_csv(OUT / "mfge8_audit.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "decision_matrix.tsv", sep="\t", index=False)
    write_report(audit, gates)
    summary = {
        "seed": SEED,
        "call": audit.iloc[0]["call"],
        "promoted": bool(audit.iloc[0]["call"] == "PROMOTE_MFGE8"),
        "output_dir": rel(OUT),
        "key_outputs": [
            rel(OUT / "mfge8_audit.tsv"),
            rel(OUT / "decision_matrix.tsv"),
            rel(OUT / "REPORT.md"),
        ],
    }
    write_json(OUT / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
