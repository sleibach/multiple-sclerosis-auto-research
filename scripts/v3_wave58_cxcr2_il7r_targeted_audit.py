#!/usr/bin/env python3
"""Wave58 targeted audit of Wave57 reopeners CXCR2 and IL7R.

Wave57 reopened CXCR2 and IL7R from a bounded Geneformer token-deletion
screen. This script hard-gates those reopeners against local evidence, live
public endpoint evidence, druggability, and prior-art/crowding. It does not
allow foundation-model support to substitute for target-resolved causality or
module-specific disease biology.
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
OUT = ROOT / "results_v3" / "wave58_cxcr2_il7r_targeted_audit"
RAW = OUT / "raw_api"
SEED = 20260527
TARGETS = ["CXCR2", "IL7R"]

INPUTS = {
    "wave57_calls": ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_intervention_first_candidate_calls.tsv",
    "wave57_metrics": ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_geneformer_metrics.tsv",
    "wave55_rank": ROOT / "results_v3" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv",
    "broad_h5ad": ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "broad_residual": ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
    "wave37_efferocytosis": ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv",
}

MANUAL_BIOLOGY_RISKS = {
    "CXCR2": (
        "primary biology is CXCL chemokine/neutrophil recruitment; V3 requires "
        "evidence that modulation changes the lipid-lysosomal inflammatory "
        "myeloid/APC state rather than simply blocking neutrophil trafficking"
    ),
    "IL7R": (
        "primary biology is IL-7/CD127 lymphocyte survival and T-cell biology; "
        "V3 requires a myeloid/APC-state or explicit lymphoid-to-myeloid chain, "
        "not generic immunosuppression"
    ),
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
        response = requests.get(url, timeout=35, headers={"User-Agent": "ms-auto-research-wave58/1.0"})
        data = response.json() if response.text.strip() else {}
        cache_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(0.15)
        return response.status_code, data, "live"
    except Exception as exc:  # noqa: BLE001
        data = {"error": type(exc).__name__, "message": str(exc), "url": url}
        cache_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return None, data, "error"


def europepmc_count(query: str) -> dict[str, Any]:
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={quote_plus(query)}&format=json&pageSize=5"
    status, data, mode = get_json(url, RAW / cache_name("europepmc", query))
    results = (data.get("resultList") or {}).get("result") or []
    return {
        "source": "EuropePMC",
        "query": query,
        "status": status,
        "mode": mode,
        "hit_count": i(data.get("hitCount")),
        "top_titles": " || ".join(s(row.get("title"))[:180] for row in results[:3]),
        "url": url,
    }


def clinicaltrials_count(query: str) -> dict[str, Any]:
    url = f"https://clinicaltrials.gov/api/v2/studies?query.term={quote_plus(query)}&pageSize=10&format=json"
    status, data, mode = get_json(url, RAW / cache_name("clinicaltrials", query))
    studies = data.get("studies") or []
    titles = []
    for study in studies[:3]:
        protocol = study.get("protocolSection") or {}
        ident = protocol.get("identificationModule") or {}
        status_mod = protocol.get("statusModule") or {}
        titles.append(f"{s(ident.get('briefTitle'))[:140]} [{s(status_mod.get('overallStatus'))}]")
    return {
        "source": "ClinicalTrials.gov",
        "query": query,
        "status": status,
        "mode": mode,
        "hit_count": i(data.get("totalCount", len(studies))),
        "top_titles": " || ".join(titles),
        "url": url,
    }


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
    values = [
        f(activity.get("standard_value"))
        for activity in (a_data.get("activities") or [])
        if f(activity.get("standard_value")) is not None
    ]
    mechanisms_url = f"https://www.ebi.ac.uk/chembl/api/data/mechanism.json?target_chembl_id={quote_plus(chembl_id)}&limit=50" if chembl_id else ""
    m_status, m_data, m_mode = get_json(mechanisms_url, RAW / cache_name("chembl_mechanism", chembl_id or gene)) if mechanisms_url else (None, {}, "")
    mechanisms = m_data.get("mechanisms") or []
    mechanism_molecules = []
    for mechanism in mechanisms:
        molecule = mechanism.get("molecule_chembl_id") or ""
        action = mechanism.get("action_type") or ""
        if molecule:
            mechanism_molecules.append(f"{molecule}:{action}")
    return {
        "gene": gene,
        "target_chembl_id": chembl_id,
        "target_name": target.get("pref_name") or "",
        "target_type": target.get("target_type") or "",
        "organism": target.get("organism") or "",
        "activity_rows": len(values),
        "best_nM": min(values) if values else None,
        "mechanism_rows": len(mechanisms),
        "mechanism_molecules": ";".join(mechanism_molecules[:20]),
        "target_status": status,
        "activity_status": a_status,
        "mechanism_status": m_status,
        "target_mode": mode,
        "activity_mode": a_mode,
        "mechanism_mode": m_mode,
    }


def uniprot_summary(gene: str) -> dict[str, Any]:
    url = (
        "https://rest.uniprot.org/uniprotkb/search?"
        f"query=gene_exact:{quote_plus(gene)}+AND+organism_id:9606+AND+reviewed:true&format=json&size=1"
    )
    status, data, mode = get_json(url, RAW / cache_name("uniprot_reviewed", gene))
    result = (data.get("results") or [{}])[0]
    comments = result.get("comments") or []
    function_texts = []
    subcell = []
    for comment in comments:
        if comment.get("commentType") == "FUNCTION":
            function_texts.extend(s(text.get("value")) for text in comment.get("texts") or [])
        if comment.get("commentType") == "SUBCELLULAR LOCATION":
            for loc in comment.get("subcellularLocations") or []:
                location = (loc.get("location") or {}).get("value")
                if location:
                    subcell.append(s(location))
    return {
        "gene": gene,
        "primary_accession": result.get("primaryAccession") or "",
        "protein_name": (((result.get("proteinDescription") or {}).get("recommendedName") or {}).get("fullName") or {}).get("value") or "",
        "length": ((result.get("sequence") or {}).get("length")) or None,
        "function_excerpt": " ".join(function_texts)[:500],
        "subcellular_location": ";".join(subcell[:10]),
        "status": status,
        "mode": mode,
        "url": url,
    }


def local_evidence() -> pd.DataFrame:
    wave57 = read_tsv(INPUTS["wave57_calls"])
    wave55 = read_tsv(INPUTS["wave55_rank"])
    broad = read_tsv(INPUTS["broad_h5ad"])
    residual = read_tsv(INPUTS["broad_residual"])
    wave37 = read_tsv(INPUTS["wave37_efferocytosis"])
    rows = []
    for gene in TARGETS:
        w57 = get_row(wave57, gene, ["gene"])
        w55 = get_row(wave55, gene, ["gene"])
        br = get_row(broad, gene, ["gene"])
        res = get_row(residual, gene, ["gene"])
        eff = get_row(wave37, gene, ["gene_symbol"])
        rows.append(
            {
                "gene": gene,
                "wave57_call": w57.get("wave57_call"),
                "wave57_model_context": w57.get("best_context"),
                "wave57_strong_support_contexts": w57.get("strong_supporting_contexts"),
                "wave57_best_n_disease_cells_with_token": w57.get("best_n_disease_cells_with_token"),
                "wave57_best_cosine_shift_z_vs_random": w57.get("best_cosine_shift_z_vs_random"),
                "wave57_best_projection_minus_random": w57.get("best_projection_minus_random"),
                "ot_genetic_disease_count_ge_0_25": w55.get("n_diseases_genetic_ge_0_25"),
                "ot_genetic_diseases_ge_0_25": w55.get("diseases_genetic_ge_0_25"),
                "ms_ot_genetic_association": w55.get("ms_genetic_association"),
                "max_clinical_score": w55.get("max_clinical_score"),
                "max_literature_score": w55.get("max_literature_score"),
                "local_positive_disease_count": br.get("positive_disease_count"),
                "local_negative_disease_count": br.get("negative_disease_count"),
                "local_positive_diseases": br.get("positive_diseases"),
                "local_negative_diseases": br.get("negative_diseases"),
                "ms_wm_delta_log2": br.get("ms_wm_delta_log2"),
                "ms_wm_p": br.get("ms_wm_p"),
                "ms_wm_fdr": br.get("ms_wm_fdr"),
                "in_lipid_lysosomal_myeloid_neighborhood": br.get("in_lipid_lysosomal_myeloid_neighborhood"),
                "retained_positive_disease_count": res.get("retained_positive_disease_count"),
                "strict_core_covariate_surviving_disease_count": res.get("strict_core_covariate_surviving_disease_count"),
                "strict_core_covariate_surviving_analyses": res.get("strict_core_covariate_surviving_analyses"),
                "top_retained_tests": res.get("top_retained_tests"),
                "efferocytosis_contrast_lfc": eff.get("median_efficient_minus_noneater_lfc"),
                "efferocytosis_contrast_fdr": eff.get("contrast_fdr"),
                "efferocytosis_screen_call": eff.get("screen_call"),
                "manual_biology_risk": MANUAL_BIOLOGY_RISKS[gene],
            }
        )
    return pd.DataFrame(rows)


def public_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    public = []
    for gene in TARGETS:
        public.append({**chembl_summary(gene), "source": "ChEMBL"})
        public.append({**uniprot_summary(gene), "source": "UniProt"})
    searches = []
    queries = [
        '"CXCR2" "multiple sclerosis"',
        '"CXCR2" autoimmune therapeutic target',
        '"CXCR2 inhibitor" autoimmune',
        '"CXCR2" Crohn psoriasis rheumatoid arthritis',
        '"CXCR2" neutrophil recruitment autoimmune',
        '"IL7R" "multiple sclerosis"',
        '"IL7R" autoimmune therapeutic target',
        '"anti-CD127" autoimmune',
        '"IL-7 receptor" multiple sclerosis trial',
        '"IL7R" myeloid dendritic cell autoimmune',
    ]
    searches.extend(europepmc_count(query) for query in queries)
    trial_queries = [
        "CXCR2 autoimmune",
        "CXCR2 Crohn",
        "CXCR2 psoriasis",
        "CXCR2 multiple sclerosis",
        "IL7R autoimmune",
        "anti-CD127",
        "IL-7 receptor multiple sclerosis",
        "IL7R Crohn",
    ]
    searches.extend(clinicaltrials_count(query) for query in trial_queries)
    patents = []
    for query in [
        "CXCR2 inhibitor autoimmune",
        "CXCR2 multiple sclerosis",
        "CXCR2 inflammatory bowel disease",
        "IL7R antibody autoimmune",
        "anti-CD127 autoimmune",
        "IL7R multiple sclerosis",
    ]:
        patents.append(
            {
                "query": query,
                "google_patents_url": f"https://patents.google.com/?q={quote_plus(query)}",
                "espacenet_url": f"https://worldwide.espacenet.com/patent/search?q={quote_plus(query)}",
                "note": "URL-only audit; patent hit counts were not scraped.",
            }
        )
    return pd.DataFrame(public), pd.DataFrame(searches), pd.DataFrame(patents)


def gate_matrix(local: pd.DataFrame, public: pd.DataFrame, searches: pd.DataFrame) -> pd.DataFrame:
    rows = []
    search_counts = {(row["source"], row["query"]): i(row["hit_count"]) for _, row in searches.iterrows()}
    for gene in TARGETS:
        loc = get_row(local, gene, ["gene"])
        chembl = get_row(public[public["source"].eq("ChEMBL")], gene, ["gene"])
        ct_autoimmune = search_counts.get(("ClinicalTrials.gov", f"{gene} autoimmune"), 0)
        if gene == "CXCR2":
            ct_specific = max(
                ct_autoimmune,
                search_counts.get(("ClinicalTrials.gov", "CXCR2 Crohn"), 0),
                search_counts.get(("ClinicalTrials.gov", "CXCR2 psoriasis"), 0),
                search_counts.get(("ClinicalTrials.gov", "CXCR2 multiple sclerosis"), 0),
            )
            prior_hits = search_counts.get(("EuropePMC", '"CXCR2 inhibitor" autoimmune'), 9999)
        else:
            ct_specific = max(
                search_counts.get(("ClinicalTrials.gov", "IL7R autoimmune"), 0),
                search_counts.get(("ClinicalTrials.gov", "anti-CD127"), 0),
                search_counts.get(("ClinicalTrials.gov", "IL-7 receptor multiple sclerosis"), 0),
                search_counts.get(("ClinicalTrials.gov", "IL7R Crohn"), 0),
            )
            prior_hits = search_counts.get(("EuropePMC", '"anti-CD127" autoimmune'), 9999)
        local_positive = i(loc.get("local_positive_disease_count"))
        local_negative = i(loc.get("local_negative_disease_count"))
        gates = [
            (
                "cross_disease_external_genetic_breadth",
                i(loc.get("ot_genetic_disease_count_ge_0_25")) >= 4,
                f"n={loc.get('ot_genetic_disease_count_ge_0_25')}; diseases={loc.get('ot_genetic_diseases_ge_0_25')}",
                "screening breadth across autoimmune diseases",
            ),
            (
                "ms_external_genetic_anchor",
                (f(loc.get("ms_ot_genetic_association")) or 0.0) >= 0.25,
                f"MS Open Targets genetic={loc.get('ms_ot_genetic_association')}",
                "MS genetic anchoring required for MS-relevant V3 claim",
            ),
            (
                "local_cross_disease_cell_state",
                local_positive >= 3 and local_negative <= 1,
                f"positive={local_positive}; negative={local_negative}; diseases={loc.get('local_positive_diseases')}",
                "local expression/cell-state recurrence",
            ),
            (
                "strict_ms_white_matter_anchor",
                (f(loc.get("ms_wm_fdr")) or 1.0) < 0.1,
                f"delta={loc.get('ms_wm_delta_log2')}; p={loc.get('ms_wm_p')}; fdr={loc.get('ms_wm_fdr')}",
                "local MS white-matter replication after correction",
            ),
            (
                "foundation_model_reopener",
                s(loc.get("wave57_call")) == "REOPEN_MODEL_SUPPORTED_INTERVENTION_FIRST",
                f"context={loc.get('wave57_model_context')}; z={loc.get('wave57_best_cosine_shift_z_vs_random')}; projection={loc.get('wave57_best_projection_minus_random')}",
                "bounded Geneformer reopener only, not causal evidence",
            ),
            (
                "real_perturbation_or_efferocytosis",
                (f(loc.get("efferocytosis_contrast_fdr")) or 1.0) < 0.2,
                f"screen={loc.get('efferocytosis_screen_call')}; lfc={loc.get('efferocytosis_contrast_lfc')}; fdr={loc.get('efferocytosis_contrast_fdr')}",
                "real disease-relevant perturbation evidence",
            ),
            (
                "direct_druggable_or_modality_handle",
                i(chembl.get("activity_rows")) > 0 or (f(loc.get("max_clinical_score")) or 0.0) > 0.4 or ct_specific > 0,
                f"ChEMBL activity_rows={chembl.get('activity_rows')}; best_nM={chembl.get('best_nM')}; clinical_score={loc.get('max_clinical_score')}; clinicaltrial_hits={ct_specific}",
                "chemical matter, biologic modality, or clinical modality precedent",
            ),
            (
                "module_specific_not_generic_immunology",
                False,
                loc.get("manual_biology_risk"),
                "manual hard gate: must not be generic neutrophil/T-cell axis without module-specific mechanism",
            ),
            (
                "prior_art_not_blocking",
                prior_hits < 100 and ct_specific == 0,
                f"EuropePMC prior hits={prior_hits}; ClinicalTrials max relevant hits={ct_specific}",
                "early crowding/trial gate; patent URLs recorded separately",
            ),
        ]
        for gate, passed, value, rationale in gates:
            rows.append({"gene": gene, "gate": gate, "passed": bool(passed), "value": value, "rationale": rationale})
    return pd.DataFrame(rows)


def calls_from_gates(gates: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gene, sub in gates.groupby("gene"):
        passed = int(sub["passed"].sum())
        call = "NO_GO_WAVE58_TARGETED_AUDIT"
        if passed >= 6:
            call = "REOPEN_FOR_FULL_THERAPEUTIC_AUDIT"
        if passed == len(sub):
            call = "PROMOTE_WAVE58_TARGETED_AUDIT"
        blockers = "; ".join(sub.loc[~sub["passed"], "gate"].astype(str).tolist())
        rows.append(
            {
                "gene": gene,
                "call": call,
                "gate_pass_count": passed,
                "gate_total": int(len(sub)),
                "failed_gates": blockers,
            }
        )
    return pd.DataFrame(rows).sort_values(["call", "gate_pass_count"], ascending=[True, False])


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
    local = local_evidence()
    public, searches, patents = public_tables()
    gates = gate_matrix(local, public, searches)
    calls = calls_from_gates(gates)
    local.to_csv(OUT / "cxcr2_il7r_local_evidence.tsv", sep="\t", index=False)
    public.to_csv(OUT / "cxcr2_il7r_public_endpoint_summary.tsv", sep="\t", index=False)
    searches.to_csv(OUT / "cxcr2_il7r_public_search_counts.tsv", sep="\t", index=False)
    patents.to_csv(OUT / "cxcr2_il7r_patent_urls.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "cxcr2_il7r_gate_matrix.tsv", sep="\t", index=False)
    calls.to_csv(OUT / "cxcr2_il7r_decision.tsv", sep="\t", index=False)
    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "promoted_count": int((calls["call"] == "PROMOTE_WAVE58_TARGETED_AUDIT").sum()),
        "reopen_count": int((calls["call"] == "REOPEN_FOR_FULL_THERAPEUTIC_AUDIT").sum()),
        "calls": calls.set_index("gene")["call"].to_dict(),
        "interpretation": (
            "CXCR2 and IL7R remain Wave57 model reopeners but fail Wave58 promotion. "
            "CXCR2 is intervention-tractable but MS-weak and generic-neutrophil-risk; "
            "IL7R is MS-genetic but lymphocyte-axis/prior-art-risk and not module-specific."
        ),
        "inputs": [rel(path) for path in INPUTS.values() if path.exists()],
        "outputs": {
            "local": rel(OUT / "cxcr2_il7r_local_evidence.tsv"),
            "public": rel(OUT / "cxcr2_il7r_public_endpoint_summary.tsv"),
            "searches": rel(OUT / "cxcr2_il7r_public_search_counts.tsv"),
            "patents": rel(OUT / "cxcr2_il7r_patent_urls.tsv"),
            "gates": rel(OUT / "cxcr2_il7r_gate_matrix.tsv"),
            "decision": rel(OUT / "cxcr2_il7r_decision.tsv"),
        },
    }
    write_json(OUT / "summary.json", summary)
    report = [
        "# Wave58 CXCR2/IL7R Targeted Audit",
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
        "## Public Searches",
        "",
        markdown_table(searches),
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
