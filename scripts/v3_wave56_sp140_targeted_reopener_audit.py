#!/usr/bin/env python3
"""Wave56 targeted SP140 reopener audit.

Wave55 made SP140 the strongest non-closed reopener by combining broad Open
Targets autoimmune genetics with local cross-disease cell-state recurrence.
This script tests the stronger question: whether SP140 can be converted from a
marker/genetic association into a V3 therapeutic mechanism with target-resolved
causality, perturbation support, and an intervention point.

The audit intentionally treats absent target-resolved coloc/MR or absent
target-specific perturbation as hard failures. A nuclear chromatin-reader
marker is not a drug target unless a correct-direction modality or phenocopy is
available.
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
OUT = ROOT / "phases/v3/results" / "wave56_sp140_targeted_reopener_audit"
RAW = OUT / "raw_api"
SEED = 20260527

INPUTS = {
    "wave55_rank": ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_rank.tsv",
    "wave55_audit": ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "external_genetics_candidate_audit.tsv",
    "wave55_ot_raw": ROOT / "phases/v3/results" / "wave55_external_genetics_druggability_sweep" / "opentargets_associated_targets_raw.tsv",
    "broad_h5ad": ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "broad_residual": ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
    "wave37_efferocytosis": ROOT / "phases/v3/results" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv",
    "wave45_regulatory": ROOT / "phases/v3/results" / "wave45_regulatory_controller_audit" / "regulatory_controller_audit.tsv",
    "wave18_foundation": ROOT / "phases/v3/results" / "wave18_foundation_rescue" / "foundation_rescue_candidate_rank.tsv",
    "wave18_direct_perturb": ROOT / "phases/v3/results" / "wave18_foundation_rescue" / "direct_perturbation_evidence_by_candidate.tsv",
    "wave15_synthesis": ROOT / "phases/v3/results" / "wave15_perturbation_drug_response" / "candidate_level_synthesis.tsv",
}

DISEASES = ["MS", "Crohn", "UC", "Psoriasis", "RA", "AS", "Sjogren", "SLE", "T1D", "Celiac", "PBC", "AITD"]
TARGET_GENES = ["SP140", "IL12A", "GALC"]


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
        response = requests.get(url, timeout=35, headers={"User-Agent": "ms-auto-research-wave56/1.0"})
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
    result_list = (data.get("resultList") or {}).get("result") or []
    return {
        "source": "EuropePMC",
        "query": query,
        "status": status,
        "mode": mode,
        "hit_count": i(data.get("hitCount")),
        "top_titles": " || ".join(s(row.get("title"))[:180] for row in result_list[:3]),
        "url": url,
    }


def clinicaltrials_count(query: str) -> dict[str, Any]:
    url = (
        "https://clinicaltrials.gov/api/v2/studies"
        f"?query.term={quote_plus(query)}&pageSize=10&format=json"
    )
    status, data, mode = get_json(url, RAW / cache_name("clinicaltrials", query))
    studies = data.get("studies") or []
    titles = []
    for study in studies[:3]:
        protocol = study.get("protocolSection") or {}
        ident = protocol.get("identificationModule") or {}
        titles.append(s(ident.get("briefTitle"))[:180])
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
    return {
        "gene": gene,
        "target_chembl_id": chembl_id,
        "target_name": target.get("pref_name") or "",
        "target_type": target.get("target_type") or "",
        "organism": target.get("organism") or "",
        "target_status": status,
        "target_mode": mode,
        "activity_status": a_status,
        "activity_mode": a_mode,
        "activity_rows": len(values),
        "best_nM": min(values) if values else None,
        "mechanism_status": m_status,
        "mechanism_mode": m_mode,
        "mechanism_rows": len(mechanisms),
        "mechanism_molecules": ";".join(sorted({s(m.get("molecule_chembl_id")) for m in mechanisms if m.get("molecule_chembl_id")})),
    }


def uniprot_summary(gene: str) -> dict[str, Any]:
    url = (
        "https://rest.uniprot.org/uniprotkb/search?"
        f"query=gene_exact:{quote_plus(gene)}+AND+organism_id:9606&format=json&size=1"
    )
    status, data, mode = get_json(url, RAW / cache_name("uniprot", gene))
    result = (data.get("results") or [{}])[0]
    features = result.get("features") or []
    domains = [s(feature.get("description") or feature.get("type")) for feature in features if feature.get("type") in {"Domain", "Zinc finger", "Region", "Compositional bias"}]
    comments = result.get("comments") or []
    function_texts = []
    for comment in comments:
        if comment.get("commentType") == "FUNCTION":
            for text in comment.get("texts") or []:
                function_texts.append(s(text.get("value")))
    return {
        "gene": gene,
        "status": status,
        "mode": mode,
        "primary_accession": result.get("primaryAccession") or "",
        "protein_name": (((result.get("proteinDescription") or {}).get("recommendedName") or {}).get("fullName") or {}).get("value") or "",
        "length": ((result.get("sequence") or {}).get("length")) or None,
        "domain_like_features": "; ".join(domains[:20]),
        "function_excerpt": " ".join(function_texts)[:500],
        "url": url,
    }


def evidence_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    wave55_rank = read_tsv(INPUTS["wave55_rank"])
    wave55_ot = read_tsv(INPUTS["wave55_ot_raw"])
    broad = read_tsv(INPUTS["broad_h5ad"])
    residual = read_tsv(INPUTS["broad_residual"])
    wave37 = read_tsv(INPUTS["wave37_efferocytosis"])
    wave45 = read_tsv(INPUTS["wave45_regulatory"])
    foundation = read_tsv(INPUTS["wave18_foundation"])
    direct = read_tsv(INPUTS["wave18_direct_perturb"])
    wave15 = read_tsv(INPUTS["wave15_synthesis"])

    local_rows: list[dict[str, Any]] = []
    for gene in TARGET_GENES:
        r55 = get_row(wave55_rank, gene, ["gene"])
        br = get_row(broad, gene, ["gene"])
        res = get_row(residual, gene, ["gene"])
        eff = get_row(wave37, gene, ["gene_symbol"])
        reg = get_row(wave45, gene, ["candidate", "gene"])
        fr = get_row(foundation, gene, ["gene", "candidate"])
        dr = get_row(direct, gene, ["gene", "candidate"])
        w15 = get_row(wave15, gene, ["candidate", "gene"])
        local_rows.append(
            {
                "gene": gene,
                "wave55_call": r55.get("call"),
                "wave55_score": r55.get("wave55_score"),
                "ot_genetic_disease_count_ge_0_25": r55.get("n_diseases_genetic_ge_0_25"),
                "ot_genetic_diseases_ge_0_25": r55.get("diseases_genetic_ge_0_25"),
                "ms_ot_genetic_association": r55.get("ms_genetic_association"),
                "local_positive_disease_count": br.get("positive_disease_count", r55.get("local_positive_disease_count")),
                "local_negative_disease_count": br.get("negative_disease_count", r55.get("local_negative_disease_count")),
                "local_positive_diseases": br.get("positive_diseases", r55.get("local_positive_diseases")),
                "best_local_abs_log2": br.get("best_abs_log2"),
                "best_local_min_p": br.get("min_p"),
                "ms_wm_delta_log2": br.get("ms_wm_delta_log2", r55.get("ms_wm_delta_log2")),
                "ms_wm_p": br.get("ms_wm_p", r55.get("ms_wm_p")),
                "ms_wm_fdr": br.get("ms_wm_fdr", r55.get("ms_wm_fdr")),
                "residual_route": res.get("candidate_class"),
                "residual_retained_positive_disease_count": res.get("retained_positive_disease_count"),
                "residual_strict_core_analyses": res.get("strict_core_covariate_surviving_analyses"),
                "residual_top_retained_tests": res.get("top_retained_tests"),
                "efferocytosis_median_efficient_minus_noneater_lfc": eff.get("median_efficient_minus_noneater_lfc"),
                "efferocytosis_contrast_fdr": eff.get("contrast_fdr"),
                "efferocytosis_screen_call": eff.get("screen_call"),
                "wave45_call": reg.get("call"),
                "wave45_manual_blocker": reg.get("manual_blocker"),
                "foundation_recommendation": fr.get("foundation_recommendation"),
                "direct_perturbation_call": dr.get("direct_evidence_calls"),
                "wave15_call": w15.get("candidate_call", w15.get("call")),
            }
        )

    external_rows = []
    for gene in TARGET_GENES:
        sub = wave55_ot[wave55_ot["gene"].astype(str).str.upper().eq(gene.upper())].copy() if not wave55_ot.empty else pd.DataFrame()
        for disease in DISEASES:
            row = get_row(sub[sub["disease"].astype(str).eq(disease)] if not sub.empty else pd.DataFrame(), gene, ["gene"])
            external_rows.append(
                {
                    "gene": gene,
                    "disease": disease,
                    "overall_score": row.get("overall_score"),
                    "genetic_association": row.get("genetic_association"),
                    "clinical": row.get("clinical"),
                    "literature": row.get("literature"),
                    "rna_expression": row.get("rna_expression"),
                    "affected_pathway": row.get("affected_pathway"),
                    "animal_model": row.get("animal_model"),
                    "ot_rank": row.get("ot_rank"),
                }
            )

    public_rows = []
    for gene in TARGET_GENES:
        public_rows.append({**chembl_summary(gene), "source": "ChEMBL"})
        public_rows.append({**uniprot_summary(gene), "source": "UniProt"})

    return pd.DataFrame(local_rows), pd.DataFrame(external_rows), pd.DataFrame(public_rows)


def public_search_tables() -> pd.DataFrame:
    queries = [
        '"SP140" "multiple sclerosis"',
        '"SP140" "Crohn"',
        '"SP140" "ulcerative colitis"',
        '"SP140" psoriasis',
        '"SP140" "rheumatoid arthritis"',
        '"SP140" "ankylosing spondylitis"',
        '"SP140" Sjogren',
        '"SP140" autoimmune therapeutic target',
        '"SP140" inhibitor',
        '"SP140" bromodomain inhibitor',
        '"SP140" degrader',
        '"IL12A" "multiple sclerosis" therapeutic',
        '"IL12A" autoimmune therapeutic target',
        '"GALC" autoimmune multiple sclerosis therapeutic',
    ]
    rows = [europepmc_count(query) for query in queries]
    trial_queries = [
        "SP140",
        "SP140 autoimmune",
        "SP140 Crohn",
        "IL12A multiple sclerosis",
        "IL12A autoimmune",
        "GALC multiple sclerosis",
    ]
    rows.extend(clinicaltrials_count(query) for query in trial_queries)
    return pd.DataFrame(rows)


def patent_urls() -> pd.DataFrame:
    queries = [
        "SP140 autoimmune therapeutic",
        "SP140 Crohn disease inhibitor",
        "SP140 degrader",
        "IL12A autoimmune therapeutic",
        "GALC multiple sclerosis autoimmune",
    ]
    rows = []
    for query in queries:
        rows.append(
            {
                "query": query,
                "google_patents_url": f"https://patents.google.com/?q={quote_plus(query)}",
                "espacenet_url": f"https://worldwide.espacenet.com/patent/search?q={quote_plus(query)}",
                "note": "URL-only audit; patent hit counts were not scraped.",
            }
        )
    return pd.DataFrame(rows)


def gate_matrix(local: pd.DataFrame, public: pd.DataFrame, searches: pd.DataFrame) -> pd.DataFrame:
    sp = get_row(local, "SP140", ["gene"])
    chembl = get_row(public[public["source"].eq("ChEMBL")], "SP140", ["gene"])
    uniprot = get_row(public[public["source"].eq("UniProt")], "SP140", ["gene"])
    search_counts = {row["query"]: i(row["hit_count"]) for _, row in searches.iterrows()}
    residual_analyses = s(sp.get("residual_strict_core_analyses"))
    residual_top = s(sp.get("residual_top_retained_tests"))
    local_positive = i(sp.get("local_positive_disease_count"))
    local_negative = i(sp.get("local_negative_disease_count"))
    gates = [
        {
            "gate": "cross_disease_external_genetic_breadth",
            "passed": i(sp.get("ot_genetic_disease_count_ge_0_25")) >= 4,
            "value": f"n={sp.get('ot_genetic_disease_count_ge_0_25')}; diseases={sp.get('ot_genetic_diseases_ge_0_25')}",
            "rationale": "requires broad Open Targets autoimmune genetics as a screening signal",
        },
        {
            "gate": "target_resolved_coloc_or_mr",
            "passed": False,
            "value": "not available in this run; Open Targets associated-target scores are not coloc/MR",
            "rationale": "hard V3 causality gate",
        },
        {
            "gate": "local_cross_disease_cell_state_replication",
            "passed": local_positive >= 3 and local_negative <= 1,
            "value": f"positive={local_positive}; negative={local_negative}; diseases={sp.get('local_positive_diseases')}",
            "rationale": "requires replicated disease-tissue expression/cell-state signal",
        },
        {
            "gate": "module_specific_residual_signal",
            "passed": bool(residual_analyses) and ("lipid_loader_repair" in residual_analyses or "hla_ii_apc" in residual_analyses),
            "value": f"strict_core={residual_analyses}; top_retained={residual_top}",
            "rationale": "requires module-specific signal in strict core covariate-surviving analyses, not only retained nominal tests",
        },
        {
            "gate": "strict_ms_white_matter_anchor",
            "passed": (f(sp.get("ms_wm_fdr")) is not None and f(sp.get("ms_wm_fdr")) < 0.1),
            "value": f"delta={sp.get('ms_wm_delta_log2')}; p={sp.get('ms_wm_p')}; fdr={sp.get('ms_wm_fdr')}",
            "rationale": "requires MS local replication after multiple testing",
        },
        {
            "gate": "real_perturbation_support",
            "passed": False,
            "value": (
                f"efferocytosis_screen={sp.get('efferocytosis_screen_call')}; "
                f"contrast_lfc={sp.get('efferocytosis_median_efficient_minus_noneater_lfc')}; "
                f"contrast_fdr={sp.get('efferocytosis_contrast_fdr')}; "
                f"direct={sp.get('direct_perturbation_call')}"
            ),
            "rationale": "available screen is unresolved and not a disease-state rescue perturbation",
        },
        {
            "gate": "foundation_model_support",
            "passed": s(sp.get("foundation_recommendation")).lower() in {"promote", "reopen", "prioritize"},
            "value": f"foundation={sp.get('foundation_recommendation')}",
            "rationale": "requires SP140-specific foundation-model rescue evidence",
        },
        {
            "gate": "direct_druggable_handle",
            "passed": i(chembl.get("activity_rows")) > 0 and f(chembl.get("best_nM")) is not None and f(chembl.get("best_nM")) <= 1000,
            "value": f"ChEMBL activity_rows={chembl.get('activity_rows')}; best_nM={chembl.get('best_nM')}; type={chembl.get('target_type')}; domains={uniprot.get('domain_like_features')}",
            "rationale": "requires direct selective chemical matter or equivalent modality",
        },
        {
            "gate": "clinical_or_patent_crowding_not_blocking",
            "passed": search_counts.get('"SP140" autoimmune therapeutic target', 9999) < 100 and search_counts.get('"SP140" inhibitor', 9999) < 100,
            "value": (
                f"autoimmune_target_hits={search_counts.get('\"SP140\" autoimmune therapeutic target')}; "
                f"inhibitor_hits={search_counts.get('\"SP140\" inhibitor')}; "
                f"degrader_hits={search_counts.get('\"SP140\" degrader')}"
            ),
            "rationale": "early screen only; patent URLs are recorded separately",
        },
        {
            "gate": "correct_direction_intervention",
            "passed": False,
            "value": "risk/mechanism appears more compatible with restoring myeloid nuclear regulator function than inhibiting it; no restoration modality identified",
            "rationale": "therapeutic direction must match disease biology and be feasible",
        },
    ]
    return pd.DataFrame(gates)


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in df.iterrows():
        values = []
        for col in cols:
            value = "" if pd.isna(row[col]) else str(row[col])
            values.append(value.replace("\n", " ").replace("|", "\\|")[:500])
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    local, external, public = evidence_tables()
    searches = public_search_tables()
    patents = patent_urls()
    gates = gate_matrix(local, public, searches)

    local.to_csv(OUT / "sp140_comparator_local_evidence.tsv", sep="\t", index=False)
    external.to_csv(OUT / "sp140_comparator_opentargets_by_disease.tsv", sep="\t", index=False)
    public.to_csv(OUT / "sp140_comparator_public_endpoint_summary.tsv", sep="\t", index=False)
    searches.to_csv(OUT / "sp140_comparator_public_search_counts.tsv", sep="\t", index=False)
    patents.to_csv(OUT / "sp140_comparator_patent_urls.tsv", sep="\t", index=False)
    gates.to_csv(OUT / "sp140_gate_matrix.tsv", sep="\t", index=False)

    passed = int(gates["passed"].sum())
    call = (
        "PROMOTE_SP140_THERAPEUTIC_TARGET"
        if passed == len(gates)
        else "PARK_SP140_GENETIC_CELLSTATE_REOPENER_NOT_THERAPEUTIC"
        if passed >= 4
        else "NO_GO_SP140_TARGETED_AUDIT"
    )
    sp = get_row(local, "SP140", ["gene"])
    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "call": call,
        "gate_pass_count": passed,
        "gate_total": int(len(gates)),
        "sp140_local_positive_disease_count": i(sp.get("local_positive_disease_count")),
        "sp140_ms_wm_delta_log2": f(sp.get("ms_wm_delta_log2")),
        "sp140_ms_wm_p": f(sp.get("ms_wm_p")),
        "sp140_ms_wm_fdr": f(sp.get("ms_wm_fdr")),
        "interpretation": (
            "SP140 remains a credible cross-autoimmune genetic/cell-state marker and mechanistic reopener, "
            "but not a V3 therapeutic target. The failures are target-resolved causality, strict local MS support, "
            "disease-state perturbation evidence, and a correct-direction druggable modality."
        ),
        "inputs": [rel(path) for path in INPUTS.values() if path.exists()],
        "outputs": {
            "local": rel(OUT / "sp140_comparator_local_evidence.tsv"),
            "external": rel(OUT / "sp140_comparator_opentargets_by_disease.tsv"),
            "public": rel(OUT / "sp140_comparator_public_endpoint_summary.tsv"),
            "searches": rel(OUT / "sp140_comparator_public_search_counts.tsv"),
            "patents": rel(OUT / "sp140_comparator_patent_urls.tsv"),
            "gates": rel(OUT / "sp140_gate_matrix.tsv"),
        },
    }
    write_json(OUT / "summary.json", summary)
    report = [
        "# Wave56 SP140 Targeted Reopener Audit",
        "",
        "## Verdict",
        "",
        f"`{call}` with {passed}/{len(gates)} gates passed.",
        "",
        summary["interpretation"],
        "",
        "## Gate Matrix",
        "",
        markdown_table(gates),
        "",
        "## Local Evidence",
        "",
        markdown_table(local),
        "",
        "## Public Searches",
        "",
        markdown_table(searches),
        "",
        "## Patent Search URLs",
        "",
        markdown_table(patents),
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
