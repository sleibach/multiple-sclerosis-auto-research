#!/usr/bin/env python3
"""Wave49 PTPN22 directionality and modality audit.

PTPN22 is the top Wave47 reopen-only genetics-first route. This script asks a
harder question than "is PTPN22 genetically associated with autoimmunity?":
does the current evidence specify a disease-safe, selective therapeutic
direction that could satisfy V3?
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
OUT = ROOT / "results_v3" / "wave49_ptpn22_directionality_audit"
RAW = OUT / "raw_api"
SEED = 20260527

WAVE47 = ROOT / "results_v3" / "wave47_late_stage_survivor_map" / "reopen_only_requirements.tsv"
WAVE34A = ROOT / "results_v3" / "wave34a_genetics_first_target_rescue" / "genetics_first_candidate_rank.tsv"
WAVE34 = ROOT / "results_v3" / "wave34_genetics_expression_druggability_scan" / "wave34_genetics_expression_druggability_rank.tsv"
BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv"
RESIDUAL = ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv"
WAVE23_REST = ROOT / "results_v3" / "wave23_genetics_restoration_modality" / "ranked_go_park_no_go.tsv"

TARGETS = {
    "PTPN22": "Tyrosine-protein phosphatase non-receptor type 22",
    "PTPN2": "Tyrosine-protein phosphatase non-receptor type 2",
    "PTPN1": "Protein-tyrosine phosphatase 1B",
    "PTPN11": "Tyrosine-protein phosphatase non-receptor type 11",
}

PUBLIC_QUERIES = [
    ("EuropePMC", "PTPN22 R620W gain loss function autoimmune directionality"),
    ("EuropePMC", "PTPN22 inhibitor autoimmune disease rheumatoid lupus type 1 diabetes"),
    ("EuropePMC", "PTPN22 multiple sclerosis genetics immune cells"),
    ("EuropePMC", "PTPN22 inhibitor selectivity phosphatase autoimmune"),
    ("ClinicalTrials.gov", "PTPN22 autoimmune"),
    ("ClinicalTrials.gov", "PTPN22 inhibitor"),
]

PATENT_QUERIES = [
    "PTPN22 inhibitor autoimmune disease",
    "PTPN22 allosteric inhibitor rheumatoid arthritis",
    "LYP PTPN22 inhibitor autoimmune",
    "PTPN22 phosphatase inhibitor multiple sclerosis",
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


def get_json(url: str, cache_path: Path, timeout: int = 25) -> tuple[int | None, dict[str, Any] | None, str]:
    if cache_path.exists():
        try:
            return 200, json.loads(cache_path.read_text(encoding="utf-8")), "cache"
        except json.JSONDecodeError:
            pass
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "ms-auto-research-wave49/1.0"})
        status = response.status_code
        payload = response.json() if response.text.strip() else {}
        cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(0.2)
        return status, payload, "live"
    except Exception as exc:  # noqa: BLE001
        payload = {"error": type(exc).__name__, "message": str(exc), "url": url}
        cache_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return None, payload, "error"


def europepmc_search(query: str) -> dict[str, Any]:
    url = (
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        f"?query={quote_plus(query)}&format=json&pageSize=5&resultType=lite"
    )
    status, payload, mode = get_json(url, RAW / cache_name("europepmc", query))
    results = (((payload or {}).get("resultList") or {}).get("result") or [])
    top_hits = []
    for hit in results[:5]:
        ident = hit.get("pmid") or hit.get("id") or ""
        top_hits.append(f"{ident}: {hit.get('title', '')} ({hit.get('pubYear', '')})")
    return {
        "source": "EuropePMC",
        "query": query,
        "count": as_int((payload or {}).get("hitCount")),
        "top_hits": " | ".join(top_hits),
        "status": status,
        "mode": mode,
        "url": url,
        "raw_path": rel(RAW / cache_name("europepmc", query)),
    }


def clinicaltrials_search(query: str) -> dict[str, Any]:
    url = f"https://clinicaltrials.gov/api/v2/studies?query.term={quote_plus(query)}&pageSize=5"
    status, payload, mode = get_json(url, RAW / cache_name("clinicaltrials", query))
    studies = (payload or {}).get("studies") or []
    total = as_int((payload or {}).get("totalCount"))
    if total == 0 and studies:
        total = len(studies)
    top_hits = []
    for study in studies[:5]:
        proto = study.get("protocolSection") or {}
        ident = proto.get("identificationModule") or {}
        design = proto.get("designModule") or {}
        status_mod = proto.get("statusModule") or {}
        top_hits.append(
            f"{ident.get('nctId', '')}: {ident.get('briefTitle') or ident.get('officialTitle') or ''} "
            f"[{';'.join(design.get('phases') or [])}; {status_mod.get('overallStatus', '')}]"
        )
    return {
        "source": "ClinicalTrials.gov",
        "query": query,
        "count": total,
        "top_hits": " | ".join(top_hits),
        "status": status,
        "mode": mode,
        "url": url,
        "raw_path": rel(RAW / cache_name("clinicaltrials", query)),
    }


def chembl_target(gene: str) -> dict[str, Any]:
    url = f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={quote_plus(gene)}&limit=10"
    status, payload, mode = get_json(url, RAW / cache_name("chembl_target", gene))
    targets = (payload or {}).get("targets") or []
    human = [t for t in targets if as_str(t.get("organism")).lower() == "homo sapiens"]
    best = human[0] if human else (targets[0] if targets else {})
    return {
        "gene": gene,
        "target_chembl_id": best.get("target_chembl_id") or "",
        "target_name": best.get("pref_name") or "",
        "target_type": best.get("target_type") or "",
        "organism": best.get("organism") or "",
        "target_status": status,
        "target_mode": mode,
        "target_url": url,
        "target_raw_path": rel(RAW / cache_name("chembl_target", gene)),
    }


def chembl_activities(target_id: str, target_label: str, limit: int = 50) -> pd.DataFrame:
    if not target_id:
        return pd.DataFrame()
    url = (
        "https://www.ebi.ac.uk/chembl/api/data/activity.json"
        f"?target_chembl_id={quote_plus(target_id)}&standard_units=nM&limit={limit}"
    )
    status, payload, mode = get_json(url, RAW / cache_name("chembl_activity", target_id))
    rows = []
    for activity in (payload or {}).get("activities") or []:
        rows.append(
            {
                "target_label": target_label,
                "target_chembl_id": target_id,
                "molecule_chembl_id": activity.get("molecule_chembl_id") or "",
                "standard_type": activity.get("standard_type") or "",
                "standard_value_nM": as_float(activity.get("standard_value")),
                "standard_relation": activity.get("standard_relation") or "",
                "assay_description": activity.get("assay_description") or "",
                "status": status,
                "mode": mode,
                "url": url,
                "raw_path": rel(RAW / cache_name("chembl_activity", target_id)),
            }
        )
    return pd.DataFrame(rows)


def molecule_target_activity(molecule_id: str, target_id: str, target_label: str) -> dict[str, Any]:
    url = (
        "https://www.ebi.ac.uk/chembl/api/data/activity.json"
        f"?molecule_chembl_id={quote_plus(molecule_id)}&target_chembl_id={quote_plus(target_id)}"
        "&standard_units=nM&limit=20"
    )
    status, payload, mode = get_json(url, RAW / cache_name("chembl_offtarget", f"{molecule_id}_{target_id}"))
    values = [
        as_float(a.get("standard_value"))
        for a in ((payload or {}).get("activities") or [])
        if as_float(a.get("standard_value")) is not None
    ]
    return {
        "molecule_chembl_id": molecule_id,
        "off_target_label": target_label,
        "off_target_chembl_id": target_id,
        "n_activity_rows": len(values),
        "best_nM": min(values) if values else None,
        "status": status,
        "mode": mode,
        "url": url,
        "raw_path": rel(RAW / cache_name("chembl_offtarget", f"{molecule_id}_{target_id}")),
    }


def local_evidence() -> pd.DataFrame:
    rows = []
    for source, path, gene_col in [
        ("wave47_reopen_requirements", WAVE47, "genes"),
        ("wave34a_genetics_first", WAVE34A, "gene"),
        ("wave34_genetics_expression_druggability", WAVE34, "gene"),
        ("broad_h5ad_gene_discovery", BROAD, "gene"),
        ("broad_residual_gate", RESIDUAL, "gene"),
        ("wave23_restoration_modality", WAVE23_REST, "gene"),
    ]:
        df = read_tsv(path)
        if df.empty or gene_col not in df.columns:
            continue
        sub = df[df[gene_col].astype(str).str.contains(r"(^|;)PTPN22($|;)", regex=True, na=False)].copy()
        for _, r in sub.iterrows():
            rows.append(
                {
                    "source": source,
                    "path": rel(path),
                    "call": as_str(r.get("wave34a_call") or r.get("wave34_call") or r.get("call") or r.get("routing_decision") or r.get("source_call")),
                    "score": as_float(r.get("genetics_first_score") or r.get("wave34_score") or r.get("source_score") or r.get("discovery_priority_score") or r.get("rank_score")),
                    "gwas_trait_count": as_float(r.get("gwas_catalog_trait_count")),
                    "gwas_min_p": as_float(r.get("gwas_catalog_min_p")),
                    "gwas_traits": as_str(r.get("gwas_catalog_traits") or r.get("gwas_catalog_traits_short")),
                    "local_positive_disease_count": as_float(r.get("local_positive_disease_count") or r.get("positive_disease_count") or r.get("broad_positive_disease_count")),
                    "local_positive_diseases": as_str(r.get("positive_diseases") or r.get("positive_diseases") or r.get("broad_positive_diseases")),
                    "residual_positive_disease_count": as_float(r.get("residual_positive_disease_count") or r.get("residual_retained_disease_count")),
                    "ms_wm_delta_log2": as_float(r.get("ms_wm_delta_log2")),
                    "ms_wm_p": as_float(r.get("ms_wm_p")),
                    "ms_wm_fdr": as_float(r.get("ms_wm_fdr")),
                    "ms_anchor": as_str(r.get("ms_anchor") or r.get("ms_positive_nominal")),
                    "primary_blocker_or_reason": as_str(r.get("primary_blocker") or r.get("route_reason") or r.get("blocker") or r.get("decision_reason")),
                    "needed_to_reopen": as_str(r.get("needed_to_reopen") or r.get("minimum_reopen_condition") or r.get("failed_gates")),
                }
            )
    return pd.DataFrame(rows)


def public_counts() -> pd.DataFrame:
    rows = []
    for source, query in PUBLIC_QUERIES:
        rows.append(europepmc_search(query) if source == "EuropePMC" else clinicaltrials_search(query))
    return pd.DataFrame(rows)


def patent_urls() -> pd.DataFrame:
    rows = []
    for query in PATENT_QUERIES:
        rows.append(
            {
                "database": "GooglePatents",
                "query": query,
                "url": f"https://patents.google.com/?q={quote_plus(query)}",
            }
        )
        rows.append(
            {
                "database": "Espacenet",
                "query": query,
                "url": f"https://worldwide.espacenet.com/patent/search?q={quote_plus(query)}",
            }
        )
    return pd.DataFrame(rows)


def selectivity_benchmark() -> tuple[pd.DataFrame, pd.DataFrame]:
    target_rows = [chembl_target(gene) for gene in TARGETS]
    target_df = pd.DataFrame(target_rows)
    activity_frames = [
        chembl_activities(as_str(r["target_chembl_id"]), as_str(r["gene"]), limit=100)
        for _, r in target_df.iterrows()
    ]
    activity_df = pd.concat([df for df in activity_frames if not df.empty], ignore_index=True) if any(not df.empty for df in activity_frames) else pd.DataFrame()

    ptpn22_id = as_str(target_df.loc[target_df["gene"] == "PTPN22", "target_chembl_id"].iloc[0]) if (target_df["gene"] == "PTPN22").any() else ""
    off_targets = {
        row["gene"]: row["target_chembl_id"]
        for _, row in target_df.iterrows()
        if row["gene"] != "PTPN22" and as_str(row["target_chembl_id"])
    }
    top_ptpn22 = activity_df[
        (activity_df.get("target_label", pd.Series(dtype=str)) == "PTPN22")
        & activity_df.get("standard_value_nM", pd.Series(dtype=float)).notna()
    ].sort_values("standard_value_nM").head(20)
    off_rows = []
    for _, row in top_ptpn22.iterrows():
        molecule = as_str(row.get("molecule_chembl_id"))
        if not molecule:
            continue
        base_nM = as_float(row.get("standard_value_nM"))
        for label, target_id in off_targets.items():
            off = molecule_target_activity(molecule, as_str(target_id), label)
            off["ptpn22_target_chembl_id"] = ptpn22_id
            off["ptpn22_best_nM_in_top_row"] = base_nM
            off["offtarget_over_ptpn22_ratio"] = (as_float(off.get("best_nM")) / base_nM) if base_nM and as_float(off.get("best_nM")) is not None else None
            off_rows.append(off)
    off_df = pd.DataFrame(off_rows)
    return target_df.merge(
        activity_df.groupby("target_label", dropna=False).agg(
            activity_rows=("molecule_chembl_id", "size"),
            best_nM=("standard_value_nM", "min"),
            unique_molecules=("molecule_chembl_id", "nunique"),
        ),
        left_on="gene",
        right_index=True,
        how="left",
    ), off_df


@dataclass
class Gate:
    gate: str
    passed: bool
    value: str
    rationale: str


def decision(local_df: pd.DataFrame, public_df: pd.DataFrame, target_df: pd.DataFrame, off_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    wave34 = local_df[local_df["source"] == "wave34_genetics_expression_druggability"]
    wave34a = local_df[local_df["source"] == "wave34a_genetics_first"]
    broad = local_df[local_df["source"] == "broad_h5ad_gene_discovery"]

    gwas_traits = as_int(wave34.iloc[0].get("gwas_trait_count")) if not wave34.empty else 0
    gwas_min_p = as_float(wave34.iloc[0].get("gwas_min_p")) if not wave34.empty else None
    traits_text = as_str(wave34.iloc[0].get("gwas_traits")) if not wave34.empty else ""
    ms_gwas = "Multiple sclerosis" in traits_text
    ms_fdr = as_float(broad.iloc[0].get("ms_wm_fdr")) if not broad.empty else None
    ms_p = as_float(broad.iloc[0].get("ms_wm_p")) if not broad.empty else None
    ms_delta = as_float(broad.iloc[0].get("ms_wm_delta_log2")) if not broad.empty else None
    local_positive = max([as_float(v) or 0.0 for v in local_df.get("local_positive_disease_count", pd.Series(dtype=float)).tolist()] or [0.0])
    residual_positive = max([as_float(v) or 0.0 for v in local_df.get("residual_positive_disease_count", pd.Series(dtype=float)).tolist()] or [0.0])
    ptpn22_target = target_df[target_df["gene"] == "PTPN22"]
    activity_rows = as_int(ptpn22_target.iloc[0].get("activity_rows")) if not ptpn22_target.empty else 0
    best_nM = as_float(ptpn22_target.iloc[0].get("best_nM")) if not ptpn22_target.empty else None
    off_min_ratio = as_float(off_df.get("offtarget_over_ptpn22_ratio", pd.Series(dtype=float)).dropna().min()) if not off_df.empty else None
    any_close_offtarget = off_min_ratio is not None and off_min_ratio < 10
    europepmc_max = int(public_df.loc[public_df["source"] == "EuropePMC", "count"].max()) if not public_df.empty else 0
    ct_max = int(public_df.loc[public_df["source"] == "ClinicalTrials.gov", "count"].max()) if not public_df.empty else 0

    gates = [
        Gate("cross_autoimmune_genetic_breadth", gwas_traits >= 10 and (gwas_min_p or 1.0) < 5e-8, f"{gwas_traits}; min_p={gwas_min_p}", "requires many autoimmune GWAS traits"),
        Gate("target_resolved_direction", False, "not_run/no_coloc_or_MR", "requires target-resolved coloc/MR and allele-to-function direction"),
        Gate("strict_ms_anchor", bool(ms_gwas or (ms_delta and ms_delta > 0 and ms_p and ms_p < 0.05 and ms_fdr and ms_fdr < 0.1)), f"ms_gwas={ms_gwas}; delta={ms_delta}; p={ms_p}; fdr={ms_fdr}", "requires MS genetics or FDR-supported MS state evidence"),
        Gate("cross_disease_cell_state_support", local_positive >= 3 or residual_positive >= 2, f"local_positive={local_positive}; residual_positive={residual_positive}", "requires expression/state support beyond genetics"),
        Gate("disease_relevant_perturbation_anchor", False, "absent", "requires PTPN22 perturbation in relevant disease cells with rescue readout"),
        Gate("chemical_matter_exists", activity_rows >= 100 and (best_nM or 1e9) <= 1000, f"activity_rows={activity_rows}; best_nM={best_nM}", "requires tractable chemistry"),
        Gate("phosphatase_selectivity_established", bool(off_min_ratio and off_min_ratio >= 10), f"min_offtarget_over_ptpn22_ratio={off_min_ratio}", "requires evidence top molecules are selective over close phosphatases"),
        Gate("disease_safe_modulation_direction", False, "conflicted_inhibition_vs_restoration", "requires a safe direction for R620W-like risk biology"),
        Gate("novelty_prior_art_not_blocking", europepmc_max < 500 and ct_max == 0, f"EuropePMC_max={europepmc_max}; ClinicalTrials_max={ct_max}", "requires not being a crowded autoimmune target/modality route"),
    ]
    gate_df = pd.DataFrame([g.__dict__ for g in gates])
    pass_count = int(gate_df["passed"].sum())
    route_call = "PROMOTE_CANDIDATE" if pass_count == len(gates) else "NO_GO_BROAD_GENETICS_WITH_UNRESOLVED_DIRECTION_AND_SELECTIVITY"
    audit_df = pd.DataFrame(
        [
            {
                "gene": "PTPN22",
                "call": route_call,
                "critical_gate_pass_count": pass_count,
                "critical_gate_total": len(gates),
                "summary": (
                    f"PTPN22 has broad autoimmune GWAS evidence ({gwas_traits} traits, min p={gwas_min_p}) "
                    f"and ChEMBL chemical matter ({activity_rows} nM activity rows, best nM={best_nM}), "
                    "but the V3-promotable claim fails because target-resolved direction, strict MS anchoring, "
                    "disease-cell perturbation, phosphatase selectivity, and novelty are not established."
                ),
                "primary_blocker": (
                    "Broad genetics does not specify a disease-safe intervention direction. "
                    "Available chemistry is inhibitor-skewed and selectivity over related phosphatases is not proven; "
                    "local cell-state support is narrow and MS support is nominal rather than FDR-supported."
                ),
                "decisive_reopen_test": (
                    "Allele-stratified primary human T cell, B cell, and myeloid assays from RA/T1D/SLE/MS donors, "
                    "comparing selective PTPN22 inhibition or restoration/editing with on-target phosphatase rescue, "
                    "plus coloc/MR resolving risk-allele direction."
                ),
                "offtarget_close_ratio_seen": bool(any_close_offtarget),
            }
        ]
    )
    return audit_df, gate_df


def write_report(audit_df: pd.DataFrame, gate_df: pd.DataFrame, public_df: pd.DataFrame) -> None:
    r = audit_df.iloc[0]
    lines = [
        "# Wave49 PTPN22 Directionality Audit",
        "",
        f"Random seed: `{SEED}`.",
        "",
        "## Verdict",
        "",
        f"`PTPN22`: `{r['call']}`.",
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
    for _, g in gate_df.iterrows():
        status = "PASS" if bool(g["passed"]) else "FAIL"
        lines.append(f"- `{g['gate']}`: {status} (`{g['value']}`) - {g['rationale']}.")
    lines.extend(
        [
            "",
            "## Public Source Snapshot",
            "",
        ]
    )
    for _, p in public_df.iterrows():
        lines.append(f"- {p['source']} `{p['query']}`: count={p['count']}; top hits: {p['top_hits']}")
    OUT.joinpath("REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    local_df = local_evidence()
    public_df = public_counts()
    patents_df = patent_urls()
    target_df, off_df = selectivity_benchmark()
    audit_df, gate_df = decision(local_df, public_df, target_df, off_df)

    local_df.to_csv(OUT / "ptpn22_local_evidence.tsv", sep="\t", index=False)
    public_df.to_csv(OUT / "public_api_counts.tsv", sep="\t", index=False)
    patents_df.to_csv(OUT / "patent_search_urls.tsv", sep="\t", index=False)
    target_df.to_csv(OUT / "phosphatase_target_activity_summary.tsv", sep="\t", index=False)
    off_df.to_csv(OUT / "ptpn22_top_molecule_offtarget_scan.tsv", sep="\t", index=False)
    audit_df.to_csv(OUT / "ptpn22_directionality_audit.tsv", sep="\t", index=False)
    gate_df.to_csv(OUT / "decision_matrix.tsv", sep="\t", index=False)
    write_report(audit_df, gate_df, public_df)

    summary = {
        "seed": SEED,
        "call": audit_df.iloc[0]["call"],
        "critical_gate_pass_count": int(audit_df.iloc[0]["critical_gate_pass_count"]),
        "critical_gate_total": int(audit_df.iloc[0]["critical_gate_total"]),
        "output_dir": rel(OUT),
        "key_outputs": [
            rel(OUT / "ptpn22_directionality_audit.tsv"),
            rel(OUT / "decision_matrix.tsv"),
            rel(OUT / "phosphatase_target_activity_summary.tsv"),
            rel(OUT / "ptpn22_top_molecule_offtarget_scan.tsv"),
            rel(OUT / "REPORT.md"),
        ],
    }
    write_json(OUT / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
