#!/usr/bin/env python3
"""Wave55 external genetics and druggability sweep.

This wave pivots away from local expression recurrence. It pulls live Open
Targets associated-target tables across the autoimmune panel, ranks targets by
cross-disease genetic evidence, joins local cell-state evidence, and audits
druggability for the top non-closed targets.

Important limitation: Open Targets associated-target scores are target-level
evidence, but they are not a coloc/MR result from paired summary statistics.
The script therefore never treats them as satisfying the V3 coloc/MR gate.
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
OUT = ROOT / "results_v3" / "wave55_external_genetics_druggability_sweep"
RAW = OUT / "raw_api"
SEED = 20260527
OT_API = "https://api.platform.opentargets.org/api/v4/graphql"

DISEASES = {
    "MS": "MONDO_0005301",
    "RA": "EFO_0000685",
    "Crohn": "EFO_0000384",
    "UC": "EFO_0000729",
    "Psoriasis": "EFO_0000676",
    "SLE": "MONDO_0007915",
    "T1D": "MONDO_0005147",
    "Sjogren": "EFO_0000699",
    "AS": "EFO_0003898",
    "AITD": "EFO_0006812",
    "Celiac": "EFO_0001060",
    "PBC": "EFO_1001486",
}

INPUTS = {
    "broad_h5ad": ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "broad_residual": ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
    "wave15_synthesis": ROOT / "results_v3" / "wave15_perturbation_drug_response" / "candidate_level_synthesis.tsv",
    "wave18_foundation": ROOT / "results_v3" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv",
    "wave47_reopen": ROOT / "results_v3" / "wave47_late_stage_survivor_map" / "reopen_only_requirements.tsv",
}

CLOSED_AXES = {
    "ACSL1",
    "NAMPT",
    "SQLE",
    "GPR65",
    "PTPN22",
    "FAP",
    "FXYD5",
    "CCR6",
    "TREM2",
    "APOE",
    "IL10",
    "IL10RA",
    "IL10RB",
    "MFGE8",
    "MED16",
    "CDK8",
    "CDK19",
    "GSK3B",
    "TNFRSF1A",
    "RFX5",
    "CHUK",
    "IFNGR1",
    "IFNGR2",
    "IFNAR1",
    "IFNAR2",
    "JAK1",
    "JAK2",
    "JAK3",
    "TYK2",
    "STAT1",
    "STAT2",
    "IRF1",
    "CIITA",
    "CD74",
    "HLA-DRA",
    "HLA-DRB1",
    "HLA-DQA1",
    "HLA-DQB1",
    "IFI30",
    "CTSS",
    "CTSH",
    "SLC15A4",
    "TASL",
    "CXorf21",
    "PTPN2",
    "TNFAIP3",
    "SH2B3",
    "IRF5",
    "IL2RA",
    "IL6R",
    "IL23R",
    "CTLA4",
    "CD6",
    "PTGER4",
    "CXCR5",
    "TNFRSF14",
    "OSMR",
    "CARD9",
    "NOD2",
    "CLEC16A",
    "ATG16L1",
}


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


def cache_name(source: str, key: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{source}_{key}")[:180]
    return safe.strip("_") + ".json"


def get_json(url: str, cache_path: Path, method: str = "GET", payload: dict[str, Any] | None = None) -> tuple[int | None, dict[str, Any], str]:
    if cache_path.exists():
        try:
            return 200, json.loads(cache_path.read_text(encoding="utf-8")), "cache"
        except json.JSONDecodeError:
            pass
    try:
        if method == "POST":
            response = requests.post(url, json=payload or {}, timeout=35, headers={"User-Agent": "ms-auto-research-wave55/1.0"})
        else:
            response = requests.get(url, timeout=35, headers={"User-Agent": "ms-auto-research-wave55/1.0"})
        data = response.json() if response.text.strip() else {}
        cache_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(0.15)
        return response.status_code, data, "live"
    except Exception as exc:  # noqa: BLE001
        data = {"error": type(exc).__name__, "message": str(exc), "url": url}
        cache_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return None, data, "error"


def query_open_targets(size: int = 500) -> pd.DataFrame:
    query = """
    query disease($efoId: String!, $size: Int!) {
      disease(efoId: $efoId) {
        id
        name
        associatedTargets(page: {index: 0, size: $size}) {
          count
          rows {
            score
            target { id approvedSymbol approvedName biotype }
            datatypeScores { id score }
          }
        }
      }
    }
    """
    rows: list[dict[str, Any]] = []
    for disease, efo in DISEASES.items():
        payload = {"query": query, "variables": {"efoId": efo, "size": size}}
        status, data, mode = get_json(OT_API, RAW / cache_name("opentargets_associated_targets", disease), method="POST", payload=payload)
        disease_data = ((data.get("data") or {}).get("disease") or {})
        assoc = disease_data.get("associatedTargets") or {}
        for rank, target_row in enumerate(assoc.get("rows") or [], start=1):
            scores = {entry.get("id"): entry.get("score") for entry in target_row.get("datatypeScores") or []}
            target = target_row.get("target") or {}
            rows.append(
                {
                    "disease": disease,
                    "disease_id": efo,
                    "disease_name": disease_data.get("name") or disease,
                    "api_status": status,
                    "api_mode": mode,
                    "ot_rank": rank,
                    "target_id": target.get("id") or "",
                    "gene": target.get("approvedSymbol") or "",
                    "approved_name": target.get("approvedName") or "",
                    "biotype": target.get("biotype") or "",
                    "overall_score": f(target_row.get("score")) or 0.0,
                    "genetic_association": f(scores.get("genetic_association")) or 0.0,
                    "clinical": f(scores.get("clinical")) or 0.0,
                    "literature": f(scores.get("literature")) or 0.0,
                    "rna_expression": f(scores.get("rna_expression")) or 0.0,
                    "affected_pathway": f(scores.get("affected_pathway")) or 0.0,
                    "animal_model": f(scores.get("animal_model")) or 0.0,
                    "genetic_literature": f(scores.get("genetic_literature")) or 0.0,
                    "raw_target_count_for_disease": i(assoc.get("count")),
                }
            )
    return pd.DataFrame(rows)


def chembl_gene(gene: str) -> dict[str, Any]:
    target_url = f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={quote_plus(gene)}&limit=10"
    status, data, mode = get_json(target_url, RAW / cache_name("chembl_target", gene))
    targets = data.get("targets") or []
    human = [target for target in targets if s(target.get("organism")).lower() == "homo sapiens"]
    target = human[0] if human else (targets[0] if targets else {})
    target_id = target.get("target_chembl_id") or ""
    activity_url = (
        f"https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id={quote_plus(target_id)}&standard_units=nM&limit=100"
        if target_id
        else ""
    )
    a_status, a_data, a_mode = (
        get_json(activity_url, RAW / cache_name("chembl_activity", target_id or gene))
        if activity_url
        else (None, {}, "")
    )
    values = [
        f(activity.get("standard_value"))
        for activity in (a_data.get("activities") or [])
        if f(activity.get("standard_value")) is not None
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


def public_search_gene(gene: str) -> dict[str, Any]:
    query = f"{gene} autoimmune multiple sclerosis therapeutic target"
    url = (
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        f"?query={quote_plus(query)}&format=json&pageSize=3&resultType=lite"
    )
    status, data, mode = get_json(url, RAW / cache_name("europepmc", query))
    hits = (((data or {}).get("resultList") or {}).get("result") or [])
    top_hits = " | ".join(f"{hit.get('pmid') or hit.get('id')}: {hit.get('title', '')} ({hit.get('pubYear', '')})" for hit in hits[:3])
    return {
        "gene": gene,
        "europepmc_query": query,
        "europepmc_hit_count": i(data.get("hitCount")),
        "europepmc_top_hits": top_hits,
        "europepmc_status": status,
        "europepmc_mode": mode,
        "europepmc_url": url,
    }


def split_diseases(value: Any) -> set[str]:
    out: set[str] = set()
    for item in s(value).split(";"):
        item = item.strip()
        if item and item.lower() != "nan":
            out.add(item)
    return out


def local_join_metrics() -> dict[str, dict[str, Any]]:
    broad = read_tsv(INPUTS["broad_h5ad"])
    residual = read_tsv(INPUTS["broad_residual"])
    perturb = read_tsv(INPUTS["wave15_synthesis"])
    foundation = read_tsv(INPUTS["wave18_foundation"])
    metrics: dict[str, dict[str, Any]] = {}
    if not broad.empty:
        for _, row in broad.iterrows():
            gene = s(row.get("gene"))
            metrics.setdefault(gene, {})
            metrics[gene].update(
                {
                    "local_positive_disease_count": i(row.get("positive_disease_count")),
                    "local_negative_disease_count": i(row.get("negative_disease_count")),
                    "local_positive_diseases": s(row.get("positive_diseases")),
                    "local_negative_diseases": s(row.get("negative_diseases")),
                    "ms_wm_delta_log2": f(row.get("ms_wm_delta_log2")),
                    "ms_wm_p": f(row.get("ms_wm_p")),
                    "ms_wm_fdr": f(row.get("ms_wm_fdr")),
                    "in_lipid_lysosomal_myeloid_neighborhood": bool(row.get("in_lipid_lysosomal_myeloid_neighborhood")),
                    "discovery_priority_score": f(row.get("discovery_priority_score")),
                }
            )
    if not residual.empty:
        for _, row in residual.iterrows():
            gene = s(row.get("gene"))
            metrics.setdefault(gene, {})
            metrics[gene].update(
                {
                    "strict_residual_disease_count": i(row.get("strict_core_covariate_surviving_disease_count")),
                    "non_ibd_retained_positive_disease_count": i(row.get("non_ibd_retained_positive_disease_count")),
                }
            )
    if not perturb.empty:
        for _, row in perturb.iterrows():
            gene = s(row.get("candidate")).replace("_KO", "")
            metrics.setdefault(gene.upper(), {})
            metrics[gene.upper()].update(
                {
                    "best_direct_selectivity_score": f(row.get("best_direct_selectivity_score")),
                    "best_direct_target_suppression": f(row.get("best_direct_target_suppression")),
                    "best_direct_target_vs_ifn_margin": f(row.get("best_direct_target_vs_ifn_margin")),
                    "direct_evidence_calls": s(row.get("direct_evidence_calls")),
                }
            )
    if not foundation.empty:
        for _, row in foundation.iterrows():
            gene = s(row.get("gene"))
            metrics.setdefault(gene, {})
            metrics[gene].update(
                {
                    "foundation_recommendation": s(row.get("foundation_rescue_recommendation")),
                    "real_perturbation_alignment_call": s(row.get("real_perturbation_alignment_call")),
                }
            )
    return metrics


def rank_targets(ot: pd.DataFrame) -> pd.DataFrame:
    local = local_join_metrics()
    rows: list[dict[str, Any]] = []
    for gene, sub in ot.groupby("gene"):
        if not gene:
            continue
        genetic_ge_025 = sub[sub["genetic_association"] >= 0.25]
        genetic_ge_05 = sub[sub["genetic_association"] >= 0.5]
        overall_ge_03 = sub[sub["overall_score"] >= 0.3]
        ms = sub[sub["disease"] == "MS"]
        ms_genetic = float(ms["genetic_association"].max()) if not ms.empty else 0.0
        ms_overall = float(ms["overall_score"].max()) if not ms.empty else 0.0
        max_clinical = float(sub["clinical"].max())
        max_literature = float(sub["literature"].max())
        info = local.get(gene, {})
        local_pos = i(info.get("local_positive_disease_count"))
        local_neg = i(info.get("local_negative_disease_count"))
        ms_p = f(info.get("ms_wm_p")) or 1.0
        ms_fdr = f(info.get("ms_wm_fdr")) or 1.0
        ms_delta = f(info.get("ms_wm_delta_log2")) or 0.0
        strict_resid = i(info.get("strict_residual_disease_count"))
        score = (
            2.0 * min(genetic_ge_025["disease"].nunique(), 6)
            + 2.0 * min(genetic_ge_05["disease"].nunique(), 4)
            + 2.0 * (1 if ms_genetic >= 0.25 else 0)
            + 1.0 * min(local_pos, 4)
            + 1.0 * (1 if ms_delta > 0 and ms_p < 0.05 else 0)
            + 1.0 * min(strict_resid, 2)
            + 0.5 * (1 if max_clinical > 0.5 else 0)
            - 4.0 * (1 if gene in CLOSED_AXES else 0)
        )
        rows.append(
            {
                "gene": gene,
                "target_id": s(sub["target_id"].iloc[0]),
                "approved_name": s(sub["approved_name"].iloc[0]),
                "wave55_score": score,
                "closed_axis": gene in CLOSED_AXES,
                "n_diseases_genetic_ge_0_25": int(genetic_ge_025["disease"].nunique()),
                "diseases_genetic_ge_0_25": ";".join(sorted(genetic_ge_025["disease"].unique())),
                "n_diseases_genetic_ge_0_5": int(genetic_ge_05["disease"].nunique()),
                "diseases_genetic_ge_0_5": ";".join(sorted(genetic_ge_05["disease"].unique())),
                "n_diseases_overall_ge_0_3": int(overall_ge_03["disease"].nunique()),
                "ms_genetic_association": ms_genetic,
                "ms_overall_score": ms_overall,
                "max_overall_score": float(sub["overall_score"].max()),
                "max_clinical_score": max_clinical,
                "max_literature_score": max_literature,
                "local_positive_disease_count": local_pos,
                "local_negative_disease_count": local_neg,
                "local_positive_diseases": s(info.get("local_positive_diseases")),
                "ms_wm_delta_log2": ms_delta,
                "ms_wm_p": ms_p,
                "ms_wm_fdr": ms_fdr,
                "strict_residual_disease_count": strict_resid,
                "in_lipid_lysosomal_myeloid_neighborhood": bool(info.get("in_lipid_lysosomal_myeloid_neighborhood", False)),
                "best_direct_selectivity_score": f(info.get("best_direct_selectivity_score")),
                "best_direct_target_suppression": f(info.get("best_direct_target_suppression")),
                "direct_evidence_calls": s(info.get("direct_evidence_calls")),
                "foundation_recommendation": s(info.get("foundation_recommendation")),
            }
        )
    return pd.DataFrame(rows).sort_values(["closed_axis", "wave55_score"], ascending=[True, False])


@dataclass
class Gate:
    gene: str
    gate: str
    passed: bool
    value: str
    rationale: str


def evaluate(ranked: pd.DataFrame, chembl: pd.DataFrame, public: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    top = ranked[(~ranked["closed_axis"]) & (ranked["wave55_score"] > 0)].head(20).copy()
    audits: list[dict[str, Any]] = []
    gates: list[Gate] = []
    for _, row in top.iterrows():
        gene = s(row["gene"])
        ch = chembl[chembl["gene"] == gene]
        pub = public[public["gene"] == gene]
        activity_rows = int(ch["activity_rows_bounded"].max()) if not ch.empty else 0
        best_nm_vals = [f(v) for v in ch.get("best_nM_bounded", pd.Series(dtype=float)).tolist() if f(v) is not None]
        best_nm = min(best_nm_vals) if best_nm_vals else None
        chemical_matter = bool(activity_rows >= 10 and best_nm is not None and best_nm <= 1000)
        europepmc_hits = int(pub["europepmc_hit_count"].max()) if not pub.empty else 0
        local_ms = bool(row["ms_wm_delta_log2"] > 0 and row["ms_wm_p"] < 0.05 and row["ms_wm_fdr"] < 0.1)
        real_perturbation = bool((f(row.get("best_direct_selectivity_score")) or 0.0) >= 0.5)
        gene_gates = [
            Gate(gene, "cross_disease_external_genetic_breadth", row["n_diseases_genetic_ge_0_25"] >= 4, f"n_ge_0.25={row['n_diseases_genetic_ge_0_25']}; diseases={row['diseases_genetic_ge_0_25']}", "requires Open Targets genetic association in at least four autoimmune diseases"),
            Gate(gene, "ms_external_genetic_anchor", row["ms_genetic_association"] >= 0.25, f"MS genetic={row['ms_genetic_association']}; MS overall={row['ms_overall_score']}", "requires MS target-disease genetic evidence"),
            Gate(gene, "coloc_or_mr_grade_target_resolution", False, "not run: no paired disease/eQTL/pQTL summary statistics", "Open Targets association is not a coloc/MR result"),
            Gate(gene, "local_cellstate_replication", row["local_positive_disease_count"] >= 3 and row["local_negative_disease_count"] <= 1, f"positive={row['local_positive_disease_count']}; negative={row['local_negative_disease_count']}; diseases={row['local_positive_diseases']}", "requires local cross-disease cell-state support"),
            Gate(gene, "strict_local_ms_anchor", local_ms, f"delta={row['ms_wm_delta_log2']}; p={row['ms_wm_p']}; fdr={row['ms_wm_fdr']}", "requires FDR-supported local MS signal"),
            Gate(gene, "real_perturbation_support", real_perturbation, f"selectivity={row.get('best_direct_selectivity_score')}; calls={row.get('direct_evidence_calls')}", "requires real perturbation support"),
            Gate(gene, "tractable_druggability", chemical_matter or row["max_clinical_score"] > 0.5, f"activity_rows={activity_rows}; best_nM={best_nm}; clinical_score={row['max_clinical_score']}", "requires chemical matter or clinical modality precedent"),
            Gate(gene, "novelty_prior_art_unblocked", europepmc_hits < 500, f"EuropePMC={europepmc_hits}", "uses literature saturation as an early crowding flag, not patent clearance"),
        ]
        gates.extend(gene_gates)
        pass_count = sum(g.passed for g in gene_gates)
        if pass_count == len(gene_gates):
            call = "PROMOTE_WAVE55_EXTERNAL_GENETICS_TARGET"
        elif pass_count >= 4:
            call = "REOPEN_COLOC_OR_PERTURBATION_PRIORITY_ONLY"
        else:
            call = "NO_GO_EXTERNAL_GENETICS_SWEEP"
        audit = row.to_dict()
        audit.update(
            {
                "call": call,
                "critical_gate_pass_count": pass_count,
                "critical_gate_total": len(gene_gates),
                "chembl_activity_rows": activity_rows,
                "chembl_best_nM": best_nm,
                "europepmc_hit_count": europepmc_hits,
                "primary_blocker": (
                    "No candidate can satisfy the V3 genetics gate because live Open Targets associated-target evidence "
                    "does not replace coloc/MR, and local MS/cell-state or perturbation support is usually absent."
                ),
            }
        )
        audits.append(audit)
    return pd.DataFrame(audits), pd.DataFrame([g.__dict__ for g in gates])


def write_report(audit: pd.DataFrame, gates: pd.DataFrame) -> None:
    lines = ["# Wave55 External Genetics And Druggability Sweep", "", f"Random seed: `{SEED}`.", "", "## Verdict", ""]
    if audit.empty:
        lines.append("No non-closed candidate had a positive Wave55 score.")
    for _, row in audit.iterrows():
        lines.append(
            f"- `{row['gene']}`: `{row['call']}`; {int(row['critical_gate_pass_count'])}/{int(row['critical_gate_total'])} gates passed; "
            f"genetic diseases >=0.25: {row['n_diseases_genetic_ge_0_25']} (`{row['diseases_genetic_ge_0_25']}`)."
        )
    lines.extend(["", "## Gate Matrix", ""])
    for _, gate in gates.iterrows():
        status = "PASS" if bool(gate["passed"]) else "FAIL"
        lines.append(f"- `{gate['gene']}` / `{gate['gate']}`: {status} (`{gate['value']}`) - {gate['rationale']}.")
    OUT.joinpath("REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    ot = query_open_targets(size=500)
    ranked = rank_targets(ot)
    top_genes = ranked[(~ranked["closed_axis"]) & (ranked["wave55_score"] > 0)]["gene"].head(30).tolist()
    chembl = pd.DataFrame([chembl_gene(gene) for gene in top_genes])
    public = pd.DataFrame([public_search_gene(gene) for gene in top_genes])
    audit, gates = evaluate(ranked, chembl, public)
    ot.to_csv(OUT / "opentargets_associated_targets_raw.tsv", sep="\t", index=False)
    ranked.to_csv(OUT / "external_genetics_rank.tsv", sep="\t", index=False)
    chembl.to_csv(OUT / "chembl_top_candidate_summary.tsv", sep="\t", index=False)
    public.to_csv(OUT / "public_literature_top_candidate_counts.tsv", sep="\t", index=False)
    audit.to_csv(OUT / "external_genetics_candidate_audit.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "decision_matrix.tsv", sep="\t", index=False)
    write_report(audit, gates)
    summary = {
        "seed": SEED,
        "disease_count": len(DISEASES),
        "raw_rows": int(len(ot)),
        "nonclosed_positive_ranked": int(((~ranked["closed_axis"]) & (ranked["wave55_score"] > 0)).sum()),
        "promoted_count": int(audit["call"].astype(str).str.contains("PROMOTE").sum()) if not audit.empty else 0,
        "reopen_priority_count": int(audit["call"].astype(str).str.contains("REOPEN").sum()) if not audit.empty else 0,
        "top_calls": dict(zip(audit["gene"], audit["call"], strict=True)) if not audit.empty else {},
        "output_dir": rel(OUT),
        "key_outputs": [
            rel(OUT / "external_genetics_rank.tsv"),
            rel(OUT / "external_genetics_candidate_audit.tsv"),
            rel(OUT / "decision_matrix.tsv"),
            rel(OUT / "REPORT.md"),
        ],
    }
    write_json(OUT / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
