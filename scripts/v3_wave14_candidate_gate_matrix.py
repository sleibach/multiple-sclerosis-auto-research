#!/usr/bin/env python3
"""Build an explicit V3 candidate gate matrix.

This is an orchestrator-side triage table, not a causal estimator. It combines
three traceable evidence layers that are repeatedly pulling in different
directions:

- local cross-disease expression recurrence from the wave-13 candidate-gene
  validation;
- scoped Open Targets GWAS credible-set evidence collected by wave 13;
- fresh public novelty/prior-art saturation counts from Europe PMC and
  ClinicalTrials.gov APIs.

The goal is to make visible which candidates fail because they are markers,
which fail because they lack genetics, and which fail because prior art is too
crowded.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave14_candidate_gate_matrix"

EXPR_PATH = ROOT / "results_v3" / "wave13_candidate_gene_local_validation" / "wave13_candidate_gene_summary.tsv"
GENETICS_PATH = ROOT / "tmp_v3" / "wave13_opentargets_gwas_credible_sets.tsv"

CANDIDATES = {
    "IFNG_HLAII_CD74_transition_state": {
        "genes": ["CD74", "CIITA", "RFX5", "CTSS"],
        "terms": ['"CD74"', '"HLA-II"', '"CIITA"', '"RFX5"'],
        "role": "central_state_or_biomarker",
    },
    "CIITA_RFX5_HLAII_transcriptional_gate": {
        "genes": ["CIITA", "RFX5"],
        "terms": ['"CIITA"', '"RFX5"', '"MHC class II transactivator"'],
        "role": "narrow_hla_ii_controller",
    },
    "GSK3B_CIITA_controller": {
        "genes": ["GSK3B", "CIITA", "RFX5"],
        "terms": ['"GSK3B"', '"GSK-3 beta"', '"CIITA"'],
        "role": "druggable_controller_scout",
    },
    "SLC15A4_TASL_IRF5_endolysosomal_checkpoint": {
        "genes": ["SLC15A4", "TASL", "IRF5"],
        "terms": ['"SLC15A4"', '"TASL"', '"IRF5"'],
        "role": "endolysosomal_apc_checkpoint",
    },
    "GPR65_pH_endolysosomal_gpcr": {
        "genes": ["GPR65"],
        "terms": ['"GPR65"', '"TDAG8"'],
        "role": "druggable_genetic_fail_fast_scout",
    },
    "TNFAIP3_A20_negative_regulator": {
        "genes": ["TNFAIP3"],
        "terms": ['"TNFAIP3"', '"A20"'],
        "role": "pan_autoimmune_genetic_anchor",
    },
    "PTPN2_JAKSTAT_negative_regulator": {
        "genes": ["PTPN2"],
        "terms": ['"PTPN2"'],
        "role": "pan_autoimmune_genetic_anchor_wrong_direction",
    },
    "CLEC16A_autophagy_locus": {
        "genes": ["CLEC16A"],
        "terms": ['"CLEC16A"'],
        "role": "autophagy_locus_anchor",
    },
    "SH2B3_LNK_cytokine_negative_regulator": {
        "genes": ["SH2B3", "LNK"],
        "terms": ['"SH2B3"', '"LNK"'],
        "role": "pan_autoimmune_genetic_anchor",
    },
}

AUTOIMMUNE_TERMS = [
    '"multiple sclerosis"',
    '"rheumatoid arthritis"',
    "lupus",
    '"Crohn"',
    '"ulcerative colitis"',
    "psoriasis",
    "Sjogren",
    "celiac",
    '"type 1 diabetes"',
    '"ankylosing spondylitis"',
    '"primary biliary cholangitis"',
    "autoimmune",
]


def split_list(value: object) -> set[str]:
    if pd.isna(value):
        return set()
    text = str(value).strip()
    if not text:
        return set()
    return {x.strip() for x in text.split(";") if x.strip()}


def load_expression() -> pd.DataFrame:
    if not EXPR_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(EXPR_PATH, sep="\t")


def expression_summary(expr: pd.DataFrame, genes: list[str]) -> dict[str, object]:
    if expr.empty:
        return {
            "expr_genes_found": "",
            "expr_trend_disease_count": 0,
            "expr_fdr10_disease_count": 0,
            "expr_negative_disease_count": 0,
            "expr_supporting_diseases": "",
            "expr_negative_diseases": "",
        }
    sub = expr[expr["gene"].isin(genes)].copy()
    trend: set[str] = set()
    neg: set[str] = set()
    fdr10_count = 0
    found: list[str] = []
    for _, row in sub.iterrows():
        found.append(str(row["gene"]))
        trend |= split_list(row.get("supporting_diseases"))
        neg |= split_list(row.get("negative_diseases"))
        try:
            fdr10_count += int(row.get("n_fdr10_positive_diseases", 0))
        except Exception:
            pass
    return {
        "expr_genes_found": ";".join(sorted(set(found))),
        "expr_trend_disease_count": len(trend),
        "expr_fdr10_disease_count": fdr10_count,
        "expr_negative_disease_count": len(neg),
        "expr_supporting_diseases": ";".join(sorted(trend)),
        "expr_negative_diseases": ";".join(sorted(neg)),
    }


def load_genetics() -> pd.DataFrame:
    if not GENETICS_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(GENETICS_PATH, sep="\t")


def genetics_summary(genetics: pd.DataFrame, genes: list[str]) -> dict[str, object]:
    if genetics.empty:
        return {
            "genetic_disease_count_score_ge_0_5": 0,
            "genetic_disease_count_score_ge_0_8": 0,
            "genetic_max_score": 0.0,
            "genetic_support_diseases_ge_0_5": "",
            "genetic_support_diseases_ge_0_8": "",
        }
    sub = genetics[genetics["query_gene"].isin(genes) | genetics["approved_symbol"].isin(genes)].copy()
    if sub.empty:
        return {
            "genetic_disease_count_score_ge_0_5": 0,
            "genetic_disease_count_score_ge_0_8": 0,
            "genetic_max_score": 0.0,
            "genetic_support_diseases_ge_0_5": "",
            "genetic_support_diseases_ge_0_8": "",
        }
    sub["max_score"] = pd.to_numeric(sub["max_score"], errors="coerce").fillna(0.0)
    ge05 = sub[sub["max_score"] >= 0.5]
    ge08 = sub[sub["max_score"] >= 0.8]
    return {
        "genetic_disease_count_score_ge_0_5": int(ge05["disease"].nunique()),
        "genetic_disease_count_score_ge_0_8": int(ge08["disease"].nunique()),
        "genetic_max_score": float(sub["max_score"].max()),
        "genetic_support_diseases_ge_0_5": ";".join(sorted(ge05["disease"].dropna().astype(str).unique())),
        "genetic_support_diseases_ge_0_8": ";".join(sorted(ge08["disease"].dropna().astype(str).unique())),
    }


def europepmc(query: str) -> dict[str, object]:
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {"query": query, "format": "json", "pageSize": 5, "resultType": "lite"}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    examples = []
    for item in data.get("resultList", {}).get("result", []):
        examples.append(
            {
                "id": item.get("id"),
                "source": item.get("source"),
                "title": item.get("title"),
                "journal": item.get("journalTitle"),
                "year": item.get("pubYear"),
                "doi": item.get("doi"),
            }
        )
    return {
        "query": query,
        "hit_count": int(data.get("hitCount", 0)),
        "examples": examples,
        "url": f"https://europepmc.org/search?query={quote_plus(query)}",
    }


def clinical_trials(term: str) -> dict[str, object]:
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {"query.term": term, "pageSize": 10, "format": "json"}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    studies = []
    for st in r.json().get("studies", []):
        protocol = st.get("protocolSection", {})
        studies.append(
            {
                "nct_id": protocol.get("identificationModule", {}).get("nctId"),
                "title": protocol.get("identificationModule", {}).get("briefTitle"),
                "status": protocol.get("statusModule", {}).get("overallStatus"),
                "conditions": ";".join(protocol.get("conditionsModule", {}).get("conditions", [])),
                "interventions": ";".join(
                    i.get("name", "")
                    for i in protocol.get("armsInterventionsModule", {}).get("interventions", [])
                ),
            }
        )
    return {
        "term": term,
        "hit_count": len(studies),
        "studies": studies,
        "url": f"https://clinicaltrials.gov/search?term={quote_plus(term)}",
    }


def prior_art(candidate: str, terms: list[str]) -> dict[str, object]:
    gene_query = "(" + " OR ".join(terms) + ")"
    disease_query = "(" + " OR ".join(AUTOIMMUNE_TERMS) + ")"
    epmc_query = f"{gene_query} AND {disease_query}"
    ct_term = " ".join(t.replace('"', "") for t in terms[:3]) + " autoimmune"
    # Be polite to public APIs and keep ordering deterministic.
    epmc = europepmc(epmc_query)
    time.sleep(0.3)
    trials = clinical_trials(ct_term)
    patent_query = f"{gene_query} {disease_query}"
    return {
        "candidate": candidate,
        "europepmc": epmc,
        "clinical_trials": trials,
        "google_patents_url": f"https://patents.google.com/?q=({quote_plus(patent_query)})",
        "espacenet_url": f"https://worldwide.espacenet.com/patent/search?q={quote_plus(patent_query)}",
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    expr = load_expression()
    genetics = load_genetics()
    rows = []
    details: dict[str, object] = {}
    for name, spec in CANDIDATES.items():
        genes = list(spec["genes"])
        row = {
            "candidate": name,
            "role": spec["role"],
            "genes": ";".join(genes),
        }
        row.update(expression_summary(expr, genes))
        row.update(genetics_summary(genetics, genes))
        pa = prior_art(name, list(spec["terms"]))
        details[name] = pa
        row["europepmc_autoimmune_hit_count"] = pa["europepmc"]["hit_count"]
        row["clinicaltrials_hit_count"] = pa["clinical_trials"]["hit_count"]
        row["europepmc_url"] = pa["europepmc"]["url"]
        row["clinicaltrials_url"] = pa["clinical_trials"]["url"]
        row["google_patents_url"] = pa["google_patents_url"]
        # Gate logic is deliberately conservative and qualitative.
        row["expression_gate"] = (
            "pass" if row["expr_trend_disease_count"] >= 4 and row["expr_negative_disease_count"] <= 1 else "fail"
        )
        row["genetics_gate"] = (
            "pass" if row["genetic_disease_count_score_ge_0_5"] >= 4 else "fail"
        )
        row["novelty_risk_gate"] = (
            "crowded" if row["europepmc_autoimmune_hit_count"] >= 100 or row["clinicaltrials_hit_count"] >= 3 else "less_crowded"
        )
        rows.append(row)
    df = pd.DataFrame(rows).sort_values(
        [
            "expression_gate",
            "genetics_gate",
            "novelty_risk_gate",
            "expr_trend_disease_count",
            "genetic_disease_count_score_ge_0_5",
        ],
        ascending=[True, True, True, False, False],
    )
    df.to_csv(OUT / "wave14_candidate_gate_matrix.tsv", sep="\t", index=False)
    (OUT / "wave14_candidate_gate_matrix_detail.json").write_text(json.dumps(details, indent=2) + "\n")
    print(json.dumps({"rows": len(df), "out": str(OUT)}, indent=2))


if __name__ == "__main__":
    main()
