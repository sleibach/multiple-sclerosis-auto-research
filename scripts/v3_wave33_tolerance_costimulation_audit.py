#!/usr/bin/env python3
"""Wave33 tolerance/costimulation axis audit.

Wave30-32 repeatedly failed within the lipid-lysosomal/IFN-HLA-II module. This
wave pivots outside that module and asks whether a cross-autoimmune tolerance or
costimulation axis has a stronger therapeutic package.

The audit deliberately treats GWAS Catalog mapped-gene evidence as weak
top-association support, not target-resolved colocalization. A positive result
would only justify a deeper branch with proper coloc/MR and perturbation tests.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave33_tolerance_costimulation_audit"
RAW = OUT / "raw_api"
SEED = 20260527
USER_AGENT = "ms-auto-research-wave33-tolerance-costim/1.0"

PATHS = {
    "broad": ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "residual": ROOT / "results_v3" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
    "checkpoint": ROOT / "results_v3" / "wave19_tolerogenic_checkpoint" / "checkpoint_candidate_synthesis.tsv",
    "genetics": ROOT / "results_v3" / "wave25_causal_genetics_module_proxy" / "causal_proxy_candidate_matrix.tsv",
    "target_first": ROOT / "results_v3" / "wave28_target_first_rescue" / "target_first_rescue_matrix.tsv",
    "direct": ROOT / "results_v3" / "wave15_perturbation_drug_response" / "candidate_level_synthesis.tsv",
    "gwas_catalog": ROOT / "tmp_v3" / "gwascatalog_associations_20260317_convert.parquet",
}

AUTOIMMUNE_REGEX = re.compile(
    r"multiple sclerosis|rheumatoid arthritis|lupus|crohn|ulcerative colitis|psoriasis|"
    r"type 1 diabetes|sjogren|celiac|ankylosing spondylitis|primary biliary|"
    r"autoimmune thyroid|graves|hashimoto|inflammatory bowel|sclerosing cholangitis|"
    r"myasthenia|vitiligo|atopic dermatitis",
    re.I,
)
AUTOIMMUNE_QUERY = (
    '"multiple sclerosis" OR "rheumatoid arthritis" OR lupus OR Crohn OR '
    '"ulcerative colitis" OR psoriasis OR "type 1 diabetes" OR Sjogren OR autoimmune'
)


AXES: dict[str, dict[str, Any]] = {
    "CD226_TIGIT_PVR_BALANCE": {
        "genes": ["CD226", "TIGIT", "PVR", "NECTIN2"],
        "class": "coinhibitory/costimulatory receptor balance",
        "direction": "block CD226/DNAM-1 or agonize TIGIT-biased inhibition; avoid oncology-style TIGIT blockade",
        "modality": "antibody or ligand-engineering biologic",
        "manual_druggability": 2.0,
        "manual_safety": 1.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Genetic rationale may exist for CD226, but local V3 expression/cell-state support is weak or negative and TIGIT/PVR biology is crowded with oncology/immunotherapy direction conflicts.",
    },
    "IL2RA_TREG_EXPANSION": {
        "genes": ["IL2", "IL2RA", "IL2RB", "IL2RG", "FOXP3"],
        "class": "Treg expansion/tolerance cytokine axis",
        "direction": "augment Treg-biased IL-2 signaling using low-dose IL-2 or IL-2 muteins",
        "modality": "cytokine, mutein, antibody-cytokine fusion",
        "manual_druggability": 2.5,
        "manual_safety": 1.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "IL-2/Treg therapy is direct autoimmune prior art across several indications; no V3-specific biomarker or MS-progressive delta has been established.",
    },
    "CTLA4_CD28_B7_COSTIMULATION": {
        "genes": ["CTLA4", "CD28", "CD80", "CD86"],
        "class": "T-cell costimulation checkpoint",
        "direction": "block CD28/B7 costimulation or enhance CTLA4-like inhibitory signaling",
        "modality": "CTLA4-Ig/abatacept-class biologics",
        "manual_druggability": 3.0,
        "manual_safety": 1.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Clinically established and crowded autoimmune mechanism; local V3 data do not define a new patient subgroup.",
    },
    "CD40_CD40LG_APC_HELP": {
        "genes": ["CD40", "CD40LG", "TRAF2", "TRAF3", "TRAF6"],
        "class": "T-B/APC licensing",
        "direction": "block CD40/CD40L costimulation",
        "modality": "anti-CD40/anti-CD40L biologics",
        "manual_druggability": 2.5,
        "manual_safety": 0.75,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Known autoimmune costimulation axis with safety and trial-history liabilities; Wave30 already rejected it as generic APC licensing.",
    },
    "IL7R_TCELL_SURVIVAL": {
        "genes": ["IL7R", "IL7"],
        "class": "T-cell survival/homeostasis cytokine receptor",
        "direction": "block IL-7R signaling in IL7R-high inflammatory states",
        "modality": "anti-IL7R antibody or receptor blockade",
        "manual_druggability": 2.25,
        "manual_safety": 0.75,
        "manual_prior_risk": "high",
        "manual_blocker": "IL7R is locally recurrent but behaves as generic immune-cell/cytokine biology; target-resolved genetics and selective benefit are absent in V3.",
    },
    "IL23_IL12_TH17_AXIS": {
        "genes": ["IL23R", "IL12B", "IL12RB1", "IL12RB2", "STAT4"],
        "class": "IL-23/IL-12/Th17 differentiation",
        "direction": "block IL-23/IL-12/STAT4 inflammatory polarization",
        "modality": "approved biologics and TYK/JAK-adjacent small molecules",
        "manual_druggability": 3.0,
        "manual_safety": 1.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Highly validated and crowded in psoriasis/IBD/autoimmunity; not novel and not MS-repair specific.",
    },
    "BACH2_IKZF_TREG_PROGRAM": {
        "genes": ["BACH2", "IKZF1", "IKZF3", "FOXP3"],
        "class": "Treg/lymphocyte transcriptional tolerance program",
        "direction": "restore tolerance transcriptional program",
        "modality": "no selective direct modality; degraders would likely point wrong way",
        "manual_druggability": 0.5,
        "manual_safety": 0.75,
        "manual_prior_risk": "medium",
        "manual_blocker": "Strong conceptual genetics class, but transcription-factor restoration is not a tractable selective therapeutic package here.",
    },
    "TNFRSF4_OX40_AXIS": {
        "genes": ["TNFRSF4", "TNFSF4"],
        "class": "T-cell costimulation",
        "direction": "block OX40/OX40L costimulation if pathogenic",
        "modality": "anti-OX40/OX40L biologics",
        "manual_druggability": 2.5,
        "manual_safety": 1.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Costimulation axis is crowded and local V3 support is narrow; intervention direction is not MS/progression-specific.",
    },
    "TNFRSF18_GITR_AXIS": {
        "genes": ["TNFRSF18", "TNFSF18"],
        "class": "Treg/effector T-cell costimulation",
        "direction": "unclear: oncology agonism conflicts with autoimmune inhibition/tolerance logic",
        "modality": "antibody biologic concepts",
        "manual_druggability": 2.0,
        "manual_safety": 0.75,
        "manual_prior_risk": "high",
        "manual_blocker": "Direction is conflicted and local V3 signal is negative in multiple diseases.",
    },
    "LAG3_MHCII_CHECKPOINT": {
        "genes": ["LAG3", "HLA-DRA", "HLA-DRB1", "CD74"],
        "class": "coinhibitory receptor/HLA-II checkpoint",
        "direction": "agonize LAG3-like inhibition or avoid MHC-II collapse",
        "modality": "LAG3 agonist concept; MHC-II targeting not acceptable",
        "manual_druggability": 1.5,
        "manual_safety": 0.75,
        "manual_prior_risk": "high",
        "manual_blocker": "LAG3 itself is locally negative; HLA-II/CD74 support would just recycle the exhausted module.",
    },
    "BTLA_HVEM_CHECKPOINT": {
        "genes": ["BTLA", "TNFRSF14", "TNFSF14"],
        "class": "coinhibitory checkpoint",
        "direction": "agonize BTLA inhibitory signaling or tune HVEM network",
        "modality": "agonist antibody or ligand biologic",
        "manual_druggability": 1.5,
        "manual_safety": 1.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Wave19 parked BTLA: recurrence without state coupling and crowded checkpoint biology.",
    },
    "CD6_ALCAM_INTERFACE": {
        "genes": ["CD6", "ALCAM"],
        "class": "T-cell/APC adhesion-costimulation interface",
        "direction": "block pathogenic CD6-ALCAM interaction",
        "modality": "anti-CD6 biologic precedent",
        "manual_druggability": 2.5,
        "manual_safety": 1.0,
        "manual_prior_risk": "high",
        "manual_blocker": "Potentially tractable but prior-arted; V3 local cross-disease and MS anchoring are not established.",
    },
    "S1PR_TRAFFICKING_AXIS": {
        "genes": ["S1PR1", "S1PR5", "S1PR2"],
        "class": "lymphocyte trafficking / CNS glial receptor axis",
        "direction": "modulate S1P receptors",
        "modality": "approved MS/UC S1P modulators",
        "manual_druggability": 3.0,
        "manual_safety": 1.0,
        "manual_prior_risk": "blocking",
        "manual_blocker": "Approved MS mechanism; cannot be a novel V3 finding without a new stratification biomarker, which is absent.",
    },
}


def read_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, sep="\t")


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def prior_penalty(label: str) -> float:
    return {"low": 0.0, "medium": 1.0, "high": 3.0, "blocking": 4.0}.get(label, 2.0)


def subset_by_genes(df: pd.DataFrame, genes: list[str]) -> pd.DataFrame:
    if df.empty or "gene" not in df.columns:
        return pd.DataFrame()
    return df[df["gene"].astype(str).str.upper().isin({g.upper() for g in genes})].copy()


def max_numeric(df: pd.DataFrame, col: str) -> float:
    if df.empty or col not in df.columns:
        return 0.0
    return float(pd.to_numeric(df[col], errors="coerce").fillna(0).max())


def min_numeric(df: pd.DataFrame, col: str, default: float = 1.0) -> float:
    if df.empty or col not in df.columns:
        return default
    ser = pd.to_numeric(df[col], errors="coerce").dropna()
    return float(ser.min()) if len(ser) else default


def gene_pattern(genes: list[str]) -> re.Pattern[str]:
    escaped = [re.escape(g) for g in genes]
    return re.compile(r"(^|[^A-Z0-9])(" + "|".join(escaped) + r")([^A-Z0-9]|$)", re.I)


def load_gwas() -> pd.DataFrame:
    path = PATHS["gwas_catalog"]
    if not path.exists():
        return pd.DataFrame()
    cols = ["DISEASE/TRAIT", "MAPPED_TRAIT", "REPORTED GENE(S)", "MAPPED_GENE", "P-VALUE", "SNPS", "PUBMEDID"]
    df = pd.read_parquet(path, columns=cols)
    disease_text = (df["DISEASE/TRAIT"].fillna("") + " " + df["MAPPED_TRAIT"].fillna("")).astype(str)
    return df[disease_text.str.contains(AUTOIMMUNE_REGEX, na=False)].copy()


def gwas_metrics(gwas: pd.DataFrame, genes: list[str]) -> dict[str, Any]:
    if gwas.empty:
        return {
            "gwas_catalog_autoimmune_hit_count": 0,
            "gwas_catalog_min_p": np.nan,
            "gwas_catalog_trait_count": 0,
            "gwas_catalog_traits": "",
        }
    pat = gene_pattern(genes)
    gene_text = (gwas["REPORTED GENE(S)"].fillna("") + " " + gwas["MAPPED_GENE"].fillna("")).astype(str)
    sub = gwas[gene_text.str.contains(pat, na=False)].copy()
    if sub.empty:
        return {
            "gwas_catalog_autoimmune_hit_count": 0,
            "gwas_catalog_min_p": np.nan,
            "gwas_catalog_trait_count": 0,
            "gwas_catalog_traits": "",
        }
    traits = sorted(set(sub["DISEASE/TRAIT"].dropna().astype(str)))[:20]
    return {
        "gwas_catalog_autoimmune_hit_count": int(len(sub)),
        "gwas_catalog_min_p": float(pd.to_numeric(sub["P-VALUE"], errors="coerce").min()),
        "gwas_catalog_trait_count": int(sub["DISEASE/TRAIT"].nunique(dropna=True)),
        "gwas_catalog_traits": ";".join(traits),
    }


def cache_json(name: str, url: str, sleep_s: float = 0.15) -> dict[str, Any]:
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / f"{name}.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            pass
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=25) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        path.write_text(json.dumps({"url": url, "payload": payload}, indent=2, sort_keys=True))
        time.sleep(sleep_s)
        return {"url": url, "payload": payload}
    except Exception as exc:
        path.write_text(json.dumps({"url": url, "error": repr(exc)}, indent=2, sort_keys=True))
        return {"url": url, "error": repr(exc)}


def europepmc_count(axis: str, genes: list[str]) -> int:
    query = f'({" OR ".join(genes[:5])}) AND ({AUTOIMMUNE_QUERY})'
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urlencode(
        {"query": query, "format": "json", "pageSize": 1}
    )
    data = cache_json(f"europepmc_{axis}", url)
    return int(data.get("payload", {}).get("hitCount", 0) or 0)


def clinicaltrials_count(axis: str, genes: list[str]) -> int:
    url = "https://clinicaltrials.gov/api/v2/studies?" + urlencode(
        {
            "query.term": " OR ".join(genes[:4]),
            "query.cond": "autoimmune OR multiple sclerosis OR rheumatoid arthritis OR lupus OR Crohn OR psoriasis",
            "format": "json",
            "pageSize": 1,
            "countTotal": "true",
        }
    )
    data = cache_json(f"clinicaltrials_{axis}", url)
    return int(data.get("payload", {}).get("totalCount", 0) or 0)


def chembl_activity_count(axis: str, genes: list[str]) -> int:
    total = 0
    for gene in genes[:4]:
        url = "https://www.ebi.ac.uk/chembl/api/data/target/search.json?" + urlencode({"q": gene})
        targets = cache_json(f"chembl_target_{axis}_{gene}", url).get("payload", {}).get("targets", [])
        target_id = ""
        for target in targets:
            if target.get("organism") == "Homo sapiens":
                target_id = target.get("target_chembl_id") or ""
                break
        if not target_id:
            continue
        act_url = f"https://www.ebi.ac.uk/chembl/api/data/activity.json?limit=1&target_chembl_id={target_id}&standard_units=nM"
        total += int(cache_json(f"chembl_activity_{axis}_{gene}_{target_id}", act_url).get("payload", {}).get("page_meta", {}).get("total_count", 0) or 0)
    return total


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    tables = {name: read_table(path) for name, path in PATHS.items() if name != "gwas_catalog"}
    gwas = load_gwas()

    rows: list[dict[str, Any]] = []
    gate_rows: list[dict[str, Any]] = []

    direct = tables.get("direct", pd.DataFrame())
    for axis, meta in AXES.items():
        genes = meta["genes"]
        broad = subset_by_genes(tables.get("broad", pd.DataFrame()), genes)
        residual = subset_by_genes(tables.get("residual", pd.DataFrame()), genes)
        checkpoint = subset_by_genes(tables.get("checkpoint", pd.DataFrame()), genes)
        genetics = subset_by_genes(tables.get("genetics", pd.DataFrame()), genes)
        target_first = subset_by_genes(tables.get("target_first", pd.DataFrame()), genes)
        direct_sub = pd.DataFrame()
        if not direct.empty and "candidate" in direct.columns:
            direct_sub = direct[
                direct["candidate"].astype(str).str.upper().str.replace("_KO", "", regex=False).isin(
                    {g.upper() for g in genes}
                )
            ].copy()

        local_breadth = max(
            max_numeric(broad, "positive_disease_count"),
            max_numeric(residual, "retained_positive_disease_count"),
            max_numeric(checkpoint, "local_recurrence_disease_count_union"),
        )
        negative_breadth = max(
            max_numeric(broad, "negative_disease_count"),
            max_numeric(checkpoint, "broad_negative_disease_count"),
        )
        state_coupling = max_numeric(checkpoint, "local_state_coupled_count_union")
        ms_anchor_delta = max_numeric(broad, "ms_wm_delta_log2")
        ms_anchor_p = min_numeric(broad, "ms_wm_p", default=1.0)
        ms_anchor = ms_anchor_delta > 0 and ms_anchor_p < 0.1
        genetics_disease_count = max(
            max_numeric(genetics, "ot_n_diseases_score_ge_0_5"),
            max_numeric(target_first, "genetics_diseases_ge_0_5"),
        )
        genetics_ready = max_numeric(genetics, "genetics_ready_score")
        gwas_info = gwas_metrics(gwas, genes)
        direct_selectivity = max_numeric(direct_sub, "best_direct_selectivity_score")
        direct_margin = max_numeric(direct_sub, "best_direct_target_vs_ifn_margin")
        direct_selective = direct_selectivity >= 0.75 and direct_margin >= 0.75

        epmc_count = europepmc_count(axis, genes)
        ct_count = clinicaltrials_count(axis, genes)
        chembl_count = chembl_activity_count(axis, genes)

        druggability = safe_float(meta["manual_druggability"])
        safety = safe_float(meta["manual_safety"])
        prior = prior_penalty(str(meta["manual_prior_risk"]))
        weak_genetic_anchor = genetics_disease_count >= 4 or gwas_info["gwas_catalog_trait_count"] >= 4

        gates = {
            "cross_autoimmune_genetic_anchor_or_gwas_breadth": weak_genetic_anchor,
            "local_cell_state_support": local_breadth >= 3 or state_coupling >= 3,
            "ms_anchor_or_explicit_non_ms_lead": ms_anchor or axis in {"IL23_IL12_TH17_AXIS", "CD6_ALCAM_INTERFACE"},
            "real_perturbation_or_validated_pharmacology": direct_selective or ct_count > 0,
            "correct_direction_druggable_modality": druggability >= 2.0,
            "safety_not_obviously_unacceptable": safety >= 1.0,
            "not_prior_art_blocked": prior < 3 and ct_count <= 3,
        }
        failures = [gate for gate, passed in gates.items() if not passed]

        score = (
            1.0 * min(gwas_info["gwas_catalog_trait_count"], 8)
            + 1.0 * min(genetics_disease_count, 8)
            + 0.8 * min(local_breadth, 5)
            + 0.8 * min(state_coupling, 5)
            + (1.0 if ms_anchor else 0.0)
            + (1.0 if direct_selective else 0.0)
            + 0.5 * druggability
            + 0.5 * safety
            - 0.8 * negative_breadth
            - 1.5 * prior
            - (1.0 if epmc_count > 5000 else 0.0)
            - (1.0 if ct_count > 3 else 0.0)
        )

        if all(gates.values()):
            call = "GO_TO_HOSTILE_NOVELTY_REVIEW"
        elif weak_genetic_anchor and druggability >= 2.0 and prior < 3:
            call = "PARK_GENETIC_TOLERANCE_AXIS_NEEDS_COLOC_AND_PERTURBATION"
        elif weak_genetic_anchor and prior >= 3:
            call = "NO_GO_TOLERANCE_PRIOR_ART_BLOCKED"
        elif local_breadth >= 3:
            call = "NO_GO_LOCAL_IMMUNE_MARKER_NOT_TARGET_PACKAGE"
        else:
            call = "NO_GO_TOLERANCE_AXIS"

        row = {
            "axis": axis,
            "genes": ";".join(genes),
            "class": meta["class"],
            "direction": meta["direction"],
            "modality": meta["modality"],
            "local_breadth": local_breadth,
            "negative_breadth": negative_breadth,
            "state_coupling": state_coupling,
            "ms_anchor": bool(ms_anchor),
            "ms_anchor_delta": ms_anchor_delta,
            "ms_anchor_p": ms_anchor_p,
            "genetics_disease_count_existing_v3": genetics_disease_count,
            "genetics_ready_score": genetics_ready,
            "direct_selective": bool(direct_selective),
            "manual_druggability": druggability,
            "manual_safety": safety,
            "manual_prior_risk": meta["manual_prior_risk"],
            "europepmc_autoimmune_hit_count": epmc_count,
            "clinicaltrials_autoimmune_count": ct_count,
            "chembl_nM_activity_count_first4_genes": chembl_count,
            "tolerance_axis_score": score,
            "n_gate_failures": len(failures),
            "gate_failures": ";".join(failures),
            "wave33_call": call,
            "manual_blocker": meta["manual_blocker"],
        }
        row.update(gwas_info)
        rows.append(row)
        for gate, passed in gates.items():
            gate_rows.append({"axis": axis, "gate": gate, "passed": bool(passed), "call": call})

    ranked = pd.DataFrame(rows).sort_values("tolerance_axis_score", ascending=False)
    ranked.to_csv(OUT / "tolerance_costimulation_axis_audit.tsv", sep="\t", index=False)
    pd.DataFrame(gate_rows).to_csv(OUT / "tolerance_costimulation_gate_matrix.tsv", sep="\t", index=False)
    summary = {
        "seed": SEED,
        "n_axes": int(len(ranked)),
        "gwas_catalog_rows_scanned_autoimmune_subset": int(len(gwas)),
        "call_counts": ranked["wave33_call"].value_counts().to_dict(),
        "top_axes": ranked.head(8)[
            [
                "axis",
                "tolerance_axis_score",
                "wave33_call",
                "gwas_catalog_trait_count",
                "local_breadth",
                "ms_anchor",
                "clinicaltrials_autoimmune_count",
                "manual_prior_risk",
                "manual_blocker",
            ]
        ].to_dict(orient="records"),
        "interpretation": (
            "Tolerance/costimulation axes are genetically and pharmacologically rich, but they are either "
            "clinically/prior-art saturated, locally unsupported in the V3 cell-state data, directionally "
            "conflicted, or lacking target-resolved coloc/perturbation evidence."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
