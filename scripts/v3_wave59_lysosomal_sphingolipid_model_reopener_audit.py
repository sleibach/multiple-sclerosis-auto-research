#!/usr/bin/env python3
"""Wave59 audit of lysosomal/sphingolipid model-supported reopeners.

Wave57 found the strongest Geneformer model support in lysosomal enzymes
(`CTSB`, `ASAH1`, `HEXB`, `HEXA`, `CTSS`, `CTSD`) but these genes did not pass
cross-disease genetics/local gates. This wave tests whether any of them can be
rescued as a non-canonical intervention point for the shared lipid-lysosomal
myeloid module, instead of being generic lysosomal housekeeping/stress signals.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave59_lysosomal_sphingolipid_model_reopener_audit"
RAW = OUT / "raw_api"
SEED = 20260527
CANDIDATES = ["CTSB", "ASAH1", "HEXB", "HEXA", "CTSS", "CTSD", "PSAP", "LIPA", "GALC", "GBA1", "SMPD1"]

INPUTS = {
    "wave57_calls": ROOT / "phases/v3/results" / "wave57_intervention_first_geneformer_screen" / "wave57_intervention_first_candidate_calls.tsv",
    "wave55_rank": ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv",
    "broad_h5ad": ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "broad_residual": ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
    "wave37": ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv",
}

MANUAL_DIRECTION = {
    "CTSB": "cathepsin B inhibition is plausible only as inflammatory protease control; broad inhibition may impair lysosomal proteolysis and antigen/debris handling",
    "CTSS": "cathepsin S inhibition is antigen-presentation relevant but already a crowded HLA-II/MHC-II axis and may suppress useful antigen processing broadly",
    "CTSD": "cathepsin D loss is neurodegeneration/lysosomal failure risk; simple inhibition is directionally unsafe",
    "ASAH1": "acid ceramidase modulation affects ceramide/sphingosine rheostat; direction in autoimmune tissue is unresolved and systemic inhibition has toxicity risk",
    "HEXA": "hexosaminidase enhancement, not inhibition, would be directionally plausible; enzyme replacement/gene therapy delivery is not autoimmune-specific",
    "HEXB": "hexosaminidase enhancement, not inhibition, would be directionally plausible; enzyme replacement/gene therapy delivery is not autoimmune-specific",
    "PSAP": "prosaposin/saposin support could affect sphingolipid catabolism but no selective autoimmune modality is apparent",
    "LIPA": "enhance/replace LAL; already parked due delivery, inconsistent myeloid direction, and MS repair prior art",
    "GALC": "enhance/replace galactocerebrosidase in principle, but autoimmune direction and delivery are unproven",
    "GBA1": "enhance glucocerebrosidase in principle; autoimmune module evidence weak and Parkinson/lysosomal prior art crowded",
    "SMPD1": "acid sphingomyelinase inhibition/enhancement direction is disease-context dependent and safety-prone",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


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


def get_row(df: pd.DataFrame, gene: str, cols: list[str]) -> dict[str, Any]:
    if df.empty:
        return {}
    for col in cols:
        if col in df.columns:
            sub = df[df[col].astype(str).str.upper().eq(gene.upper())]
            if not sub.empty:
                return sub.iloc[0].to_dict()
    return {}


def cache_name(prefix: str, key: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{prefix}_{key}")[:180].strip("_")
    return safe + ".json"


def get_json(url: str, cache_path: Path) -> tuple[int | None, dict[str, Any], str]:
    if cache_path.exists():
        try:
            return 200, json.loads(cache_path.read_text(encoding="utf-8")), "cache"
        except json.JSONDecodeError:
            pass
    try:
        response = requests.get(url, timeout=35, headers={"User-Agent": "ms-auto-research-wave59/1.0"})
        data = response.json() if response.text.strip() else {}
        cache_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(0.15)
        return response.status_code, data, "live"
    except Exception as exc:  # noqa: BLE001
        data = {"error": type(exc).__name__, "message": str(exc), "url": url}
        cache_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return None, data, "error"


def chembl_summary(gene: str) -> dict[str, Any]:
    target_url = f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={quote_plus(gene)}&limit=20"
    status, data, mode = get_json(target_url, RAW / cache_name("chembl_target", gene))
    targets = data.get("targets") or []
    human = [target for target in targets if s(target.get("organism")).lower() == "homo sapiens"]
    target = human[0] if human else (targets[0] if targets else {})
    chembl_id = target.get("target_chembl_id") or ""
    act_url = (
        f"https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id={quote_plus(chembl_id)}&standard_units=nM&limit=100"
        if chembl_id
        else ""
    )
    a_status, a_data, a_mode = get_json(act_url, RAW / cache_name("chembl_activity", chembl_id or gene)) if act_url else (None, {}, "")
    values = [f(activity.get("standard_value")) for activity in (a_data.get("activities") or []) if f(activity.get("standard_value")) is not None]
    mech_url = f"https://www.ebi.ac.uk/chembl/api/data/mechanism.json?target_chembl_id={quote_plus(chembl_id)}&limit=25" if chembl_id else ""
    m_status, m_data, m_mode = get_json(mech_url, RAW / cache_name("chembl_mechanism", chembl_id or gene)) if mech_url else (None, {}, "")
    mechanisms = m_data.get("mechanisms") or []
    return {
        "gene": gene,
        "target_chembl_id": chembl_id,
        "target_name": target.get("pref_name") or "",
        "target_type": target.get("target_type") or "",
        "activity_rows": len(values),
        "best_nM": min(values) if values else None,
        "mechanism_rows": len(mechanisms),
        "mechanism_molecules": ";".join(sorted({s(m.get("molecule_chembl_id")) for m in mechanisms if m.get("molecule_chembl_id")})),
        "target_status": status,
        "activity_status": a_status,
        "mechanism_status": m_status,
        "target_mode": mode,
        "activity_mode": a_mode,
        "mechanism_mode": m_mode,
    }


def europepmc_count(query: str) -> dict[str, Any]:
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={quote_plus(query)}&format=json&pageSize=3"
    status, data, mode = get_json(url, RAW / cache_name("europepmc", query))
    results = (data.get("resultList") or {}).get("result") or []
    return {
        "query": query,
        "status": status,
        "mode": mode,
        "hit_count": i(data.get("hitCount")),
        "top_titles": " || ".join(s(row.get("title"))[:160] for row in results[:3]),
        "url": url,
    }


def local_join() -> pd.DataFrame:
    wave57 = read_tsv(INPUTS["wave57_calls"])
    wave55 = read_tsv(INPUTS["wave55_rank"])
    broad = read_tsv(INPUTS["broad_h5ad"])
    residual = read_tsv(INPUTS["broad_residual"])
    wave37 = read_tsv(INPUTS["wave37"])
    chembl_rows = [chembl_summary(gene) for gene in CANDIDATES]
    rows = []
    for gene in CANDIDATES:
        w57 = get_row(wave57, gene, ["gene"])
        w55 = get_row(wave55, gene, ["gene"])
        br = get_row(broad, gene, ["gene"])
        res = get_row(residual, gene, ["gene"])
        eff = get_row(wave37, gene, ["gene_symbol"])
        ch = get_row(pd.DataFrame(chembl_rows), gene, ["gene"])
        rows.append(
            {
                "gene": gene,
                "wave57_model_priority_score": w57.get("wave57_model_priority_score"),
                "strong_support_contexts": w57.get("strong_support_contexts"),
                "support_contexts": w57.get("support_contexts"),
                "best_context": w57.get("best_context"),
                "best_cosine_shift_z_vs_random": w57.get("best_cosine_shift_z_vs_random"),
                "n_diseases_genetic_ge_0_25": w55.get("n_diseases_genetic_ge_0_25"),
                "diseases_genetic_ge_0_25": w55.get("diseases_genetic_ge_0_25"),
                "ms_genetic_association": w55.get("ms_genetic_association"),
                "positive_disease_count": br.get("positive_disease_count"),
                "negative_disease_count": br.get("negative_disease_count"),
                "positive_diseases": br.get("positive_diseases"),
                "negative_diseases": br.get("negative_diseases"),
                "ms_wm_delta_log2": br.get("ms_wm_delta_log2"),
                "ms_wm_p": br.get("ms_wm_p"),
                "ms_wm_fdr": br.get("ms_wm_fdr"),
                "in_lipid_lysosomal_myeloid_neighborhood": br.get("in_lipid_lysosomal_myeloid_neighborhood"),
                "retained_positive_disease_count": res.get("retained_positive_disease_count"),
                "strict_core_covariate_surviving_disease_count": res.get("strict_core_covariate_surviving_disease_count"),
                "top_retained_tests": res.get("top_retained_tests"),
                "efferocytosis_contrast_lfc": eff.get("median_efficient_minus_noneater_lfc"),
                "efferocytosis_contrast_fdr": eff.get("contrast_fdr"),
                "efferocytosis_screen_call": eff.get("screen_call"),
                "chembl_activity_rows": ch.get("activity_rows"),
                "chembl_best_nM": ch.get("best_nM"),
                "chembl_mechanism_rows": ch.get("mechanism_rows"),
                "manual_directionality_risk": MANUAL_DIRECTION[gene],
            }
        )
    return pd.DataFrame(rows), pd.DataFrame(chembl_rows)


def public_searches() -> pd.DataFrame:
    rows = []
    for gene in CANDIDATES:
        rows.append(europepmc_count(f'"{gene}" autoimmune therapeutic target'))
        rows.append(europepmc_count(f'"{gene}" multiple sclerosis remyelination'))
        rows.append(europepmc_count(f'"{gene}" inhibitor autoimmune'))
    return pd.DataFrame(rows)


def gate_and_call(evidence: pd.DataFrame, searches: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    search_counts = {row["query"]: i(row["hit_count"]) for _, row in searches.iterrows()}
    gates = []
    for _, row in evidence.iterrows():
        gene = row["gene"]
        prior = search_counts.get(f'"{gene}" autoimmune therapeutic target', 9999) + search_counts.get(f'"{gene}" inhibitor autoimmune', 9999)
        rows = [
            ("foundation_model_support", i(row.get("strong_support_contexts")) >= 1, f"strong={row.get('strong_support_contexts')}; support={row.get('support_contexts')}; best={row.get('best_context')}"),
            ("cross_disease_genetic_breadth", i(row.get("n_diseases_genetic_ge_0_25")) >= 4, f"n={row.get('n_diseases_genetic_ge_0_25')}; diseases={row.get('diseases_genetic_ge_0_25')}"),
            ("ms_genetic_anchor", (f(row.get("ms_genetic_association")) or 0.0) >= 0.25, f"MS genetic={row.get('ms_genetic_association')}"),
            ("local_recurrence", i(row.get("positive_disease_count")) >= 3 and i(row.get("negative_disease_count")) <= 1, f"positive={row.get('positive_disease_count')}; negative={row.get('negative_disease_count')}; diseases={row.get('positive_diseases')}"),
            ("strict_ms_white_matter", (f(row.get("ms_wm_fdr")) or 1.0) < 0.1, f"delta={row.get('ms_wm_delta_log2')}; p={row.get('ms_wm_p')}; fdr={row.get('ms_wm_fdr')}"),
            ("module_specific_residual", bool(row.get("in_lipid_lysosomal_myeloid_neighborhood")) or i(row.get("strict_core_covariate_surviving_disease_count")) >= 1, f"in_lipid_neighborhood={row.get('in_lipid_lysosomal_myeloid_neighborhood')}; strict_core={row.get('strict_core_covariate_surviving_disease_count')}"),
            ("real_perturbation_or_efferocytosis", (f(row.get("efferocytosis_contrast_fdr")) or 1.0) < 0.2, f"screen={row.get('efferocytosis_screen_call')}; lfc={row.get('efferocytosis_contrast_lfc')}; fdr={row.get('efferocytosis_contrast_fdr')}"),
            ("druggable_or_modality_handle", i(row.get("chembl_activity_rows")) > 0 or i(row.get("chembl_mechanism_rows")) > 0, f"activity_rows={row.get('chembl_activity_rows')}; best_nM={row.get('chembl_best_nM')}; mechanisms={row.get('chembl_mechanism_rows')}"),
            ("directionality_safe_and_selective", False, row.get("manual_directionality_risk")),
            ("prior_art_not_blocking", prior < 150, f"combined EuropePMC target+inhibitor hits={prior}"),
        ]
        for gate, passed, value in rows:
            gates.append({"gene": gene, "gate": gate, "passed": bool(passed), "value": value})
    gate_df = pd.DataFrame(gates)
    calls = []
    for gene, sub in gate_df.groupby("gene"):
        passed = int(sub["passed"].sum())
        call = "NO_GO_LYSOSOMAL_MODEL_REOPENER"
        if passed >= 6:
            call = "PARK_EX_VIVO_LYSOSOMAL_REOPENER"
        if passed == len(sub):
            call = "PROMOTE_LYSOSOMAL_MODEL_REOPENER"
        calls.append({"gene": gene, "call": call, "gate_pass_count": passed, "gate_total": int(len(sub)), "failed_gates": "; ".join(sub.loc[~sub["passed"], "gate"].tolist())})
    return gate_df, pd.DataFrame(calls).sort_values(["call", "gate_pass_count"], ascending=[True, False])


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        vals = []
        for col in cols:
            val = "" if pd.isna(row[col]) else str(row[col])
            vals.append(val.replace("\n", " ").replace("|", "\\|")[:500])
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    evidence, chembl = local_join()
    searches = public_searches()
    gates, calls = gate_and_call(evidence, searches)
    evidence.to_csv(OUT / "lysosomal_sphingolipid_evidence.tsv", sep="\t", index=False)
    chembl.to_csv(OUT / "lysosomal_sphingolipid_chembl.tsv", sep="\t", index=False)
    searches.to_csv(OUT / "lysosomal_sphingolipid_public_searches.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "lysosomal_sphingolipid_gate_matrix.tsv", sep="\t", index=False)
    calls.to_csv(OUT / "lysosomal_sphingolipid_decision.tsv", sep="\t", index=False)
    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "candidate_count": len(CANDIDATES),
        "promoted_count": int((calls["call"] == "PROMOTE_LYSOSOMAL_MODEL_REOPENER").sum()),
        "parked_count": int((calls["call"] == "PARK_EX_VIVO_LYSOSOMAL_REOPENER").sum()),
        "calls": calls.set_index("gene")["call"].to_dict(),
        "interpretation": (
            "Strong Geneformer lysosomal-enzyme signals do not identify a V3 therapeutic target. "
            "Most fail genetics/MS/local/perturbation gates, and the directionality gate fails because "
            "simple enzyme inhibition or enhancement is not selective enough for autoimmune module control."
        ),
        "outputs": {
            "evidence": rel(OUT / "lysosomal_sphingolipid_evidence.tsv"),
            "chembl": rel(OUT / "lysosomal_sphingolipid_chembl.tsv"),
            "searches": rel(OUT / "lysosomal_sphingolipid_public_searches.tsv"),
            "gates": rel(OUT / "lysosomal_sphingolipid_gate_matrix.tsv"),
            "decision": rel(OUT / "lysosomal_sphingolipid_decision.tsv"),
        },
    }
    write_json(OUT / "summary.json", summary)
    report = [
        "# Wave59 Lysosomal/Sphingolipid Model Reopener Audit",
        "",
        "## Verdict",
        "",
        summary["interpretation"],
        "",
        "## Calls",
        "",
        markdown_table(calls),
        "",
        "## Gate Matrix",
        "",
        markdown_table(gates),
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
