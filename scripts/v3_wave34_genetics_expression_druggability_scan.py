#!/usr/bin/env python3
"""Wave34 genetics-expression-druggability rescue scan.

This scan deliberately changes the search order after multiple module-centered
routes failed:

1. start from broad autoimmune genetic recurrence in the local GWAS Catalog
   parquet snapshot;
2. require local disease-cell/tissue support from V3 single-cell/spatial/bulk
   summaries;
3. ask whether the gene has a plausible current druggability surface;
4. penalize prior-art saturation and wrong-direction modalities;
5. refuse promotion without real perturbation/model-alignment support.

GWAS Catalog mapped-gene counts are only locus-level lead evidence. They are not
treated as colocalization, MR, or causal target proof.
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
OUT = ROOT / "phases/v3/results" / "wave34_genetics_expression_druggability_scan"
RAW = OUT / "raw_api"
SEED = 20260527
USER_AGENT = "ms-auto-research-wave34-genetics-expression-druggability/1.0"

PATHS = {
    "gwas_catalog": ROOT / "phases/v3/tmp" / "gwascatalog_associations_20260317_convert.parquet",
    "broad": ROOT / "phases/v3/results" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_rank.tsv",
    "residual": ROOT / "phases/v3/results" / "broad_residual_gate" / "broad_residual_gate_summary.tsv",
    "wave25": ROOT
    / "phases/v3/results"
    / "wave25_causal_genetics_module_proxy"
    / "causal_proxy_candidate_matrix.tsv",
    "wave23_gene": ROOT
    / "phases/v3/results"
    / "wave23_orchestrator_nonexpression_axis_triage"
    / "wave23_gene_evidence.tsv",
    "target_first": ROOT
    / "phases/v3/results"
    / "wave28_target_first_rescue"
    / "target_first_rescue_matrix.tsv",
    "local_chembl": ROOT / "phases/v3/results" / "druggability" / "chembl_target_activity_summary.tsv",
    "direct": ROOT
    / "phases/v3/results"
    / "wave15_perturbation_drug_response"
    / "candidate_level_synthesis.tsv",
}

AUTOIMMUNE_REGEX = re.compile(
    r"multiple sclerosis|rheumatoid arthritis|lupus|crohn|ulcerative colitis|psoriasis|"
    r"type 1 diabetes|sjogren|celiac|ankylosing spondylitis|primary biliary|"
    r"autoimmune thyroid|graves|hashimoto|inflammatory bowel|sclerosing cholangitis|"
    r"myasthenia|vitiligo|atopic dermatitis",
    re.I,
)

GENE_TOKEN = re.compile(r"^[A-Z][A-Z0-9-]{1,20}$")
GENE_SPLIT = re.compile(r"[,;/]|\\s+-\\s+|\\sx\\s|\\s+and\\s+", re.I)

EXCLUDE_TOKENS = {
    "HLA",
    "MHC",
    "MHC1",
    "MHC2",
    "IFN",
    "TNF",
    "IL",
    "GENE",
    "NA",
    "NR",
    "NONE",
    "INTERGENIC",
}

# Manual guardrails are intentionally conservative and documented in output.
MANUAL_BLOCKERS: dict[str, tuple[str, str]] = {
    "PTPN2": ("wrong_direction", "therapeutic direction is restoration/activation; current chemical matter mainly inhibits phosphatases"),
    "TNFAIP3": ("wrong_direction", "A20 restoration/editing is not a current selective drug modality"),
    "SH2B3": ("wrong_direction", "LNK restoration is not a current selective drug modality"),
    "BACH2": ("wrong_direction", "tolerance transcription-factor restoration has no selective current modality"),
    "IKZF1": ("crowded_or_wrong_direction", "IKZF modulation/degradation is oncology/immune broad and directionally risky"),
    "IKZF3": ("crowded_or_wrong_direction", "IKZF modulation/degradation is oncology/immune broad and directionally risky"),
    "IL2": ("blocking_prior_art", "low-dose IL-2 and IL-2 muteins are direct autoimmune prior art"),
    "IL2RA": ("blocking_prior_art", "IL-2 receptor/Treg axis is direct autoimmune prior art"),
    "IL23R": ("blocking_prior_art", "IL-23 pathway is established/crowded autoimmune biology"),
    "IL12B": ("blocking_prior_art", "IL-12/23 blockade is established/crowded autoimmune biology"),
    "TYK2": ("blocking_prior_art", "TYK2 inhibitors are established/crowded autoimmune drug class"),
    "JAK1": ("blocking_prior_art", "JAK inhibition is established/crowded broad immunosuppression"),
    "JAK2": ("blocking_prior_art", "JAK inhibition is established/crowded broad immunosuppression"),
    "JAK3": ("blocking_prior_art", "JAK inhibition is established/crowded broad immunosuppression"),
    "BTK": ("blocking_prior_art", "BTK inhibitors are direct MS/autoimmune clinical prior art"),
    "CTLA4": ("blocking_prior_art", "CTLA4-Ig/abatacept class is established autoimmune prior art"),
    "CD28": ("blocking_prior_art", "CD28/B7 costimulation has major established clinical/prior-art footprint"),
    "CD40": ("blocking_prior_art", "CD40/CD40L blockade is established autoimmune trial/prior-art space"),
    "CD40LG": ("blocking_prior_art", "CD40/CD40L blockade is established autoimmune trial/prior-art space"),
    "CD226": ("crowded_prior_art", "CD226/TIGIT/PVR checkpoint axis is crowded and Wave33 failed local/MS gates"),
    "TIGIT": ("crowded_prior_art", "TIGIT checkpoint axis is crowded and directionally oncology-conflicted"),
    "CD6": ("crowded_prior_art", "CD6/ALCAM has autoimmune biologic precedent and Wave33 failed breadth gates"),
    "ALCAM": ("crowded_prior_art", "CD6/ALCAM has autoimmune biologic precedent and Wave33 failed breadth gates"),
    "NLRP3": ("crowded_prior_art", "inflammasome inhibition is broad/crowded autoimmune and neuroinflammation prior art"),
    "IRAK4": ("crowded_prior_art", "TLR/MyD88/IRAK4 blockade is broad/crowded autoimmune prior art"),
    "SYK": ("crowded_prior_art", "SYK inhibition is broad/crowded autoimmune prior art"),
    "S1PR1": ("blocking_prior_art", "S1P modulation is approved/crowded MS and UC biology"),
    "S1PR5": ("blocking_prior_art", "S1P modulation is approved/crowded MS and UC biology"),
}

GENERIC_PREFIXES = ("HLA-", "KIR", "TRAV", "TRBV", "IGH", "IGK", "IGL")


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


def extract_genes(text: str) -> set[str]:
    if not text or text == "nan":
        return set()
    cleaned = (
        text.replace("(", ",")
        .replace(")", ",")
        .replace("[", ",")
        .replace("]", ",")
        .replace(" - ", ",")
        .replace(";", ",")
    )
    genes: set[str] = set()
    for part in GENE_SPLIT.split(cleaned):
        token = part.strip().upper()
        if not token or token in EXCLUDE_TOKENS:
            continue
        if any(token.startswith(prefix) for prefix in GENERIC_PREFIXES):
            continue
        if token.startswith("LOC") or token.startswith("RP11-"):
            continue
        if GENE_TOKEN.match(token):
            genes.add(token)
    return genes


def load_autoimmune_gwas_gene_summary() -> pd.DataFrame:
    path = PATHS["gwas_catalog"]
    if not path.exists():
        return pd.DataFrame()
    cols = ["DISEASE/TRAIT", "MAPPED_TRAIT", "REPORTED GENE(S)", "MAPPED_GENE", "P-VALUE", "SNPS", "PUBMEDID"]
    df = pd.read_parquet(path, columns=cols)
    disease_text = (df["DISEASE/TRAIT"].fillna("") + " " + df["MAPPED_TRAIT"].fillna("")).astype(str)
    df = df[disease_text.str.contains(AUTOIMMUNE_REGEX, na=False)].copy()
    rows: list[dict[str, Any]] = []
    for _, row in df.iterrows():
        gene_text = f"{row.get('REPORTED GENE(S)', '')},{row.get('MAPPED_GENE', '')}"
        for gene in extract_genes(str(gene_text)):
            rows.append(
                {
                    "gene": gene,
                    "trait": str(row.get("DISEASE/TRAIT", "")),
                    "p": safe_float(row.get("P-VALUE"), np.nan),
                    "snp": str(row.get("SNPS", "")),
                    "pubmedid": str(row.get("PUBMEDID", "")),
                }
            )
    if not rows:
        return pd.DataFrame()
    long = pd.DataFrame(rows)
    summary = (
        long.groupby("gene")
        .agg(
            gwas_catalog_autoimmune_hit_count=("trait", "size"),
            gwas_catalog_trait_count=("trait", "nunique"),
            gwas_catalog_min_p=("p", "min"),
            gwas_catalog_traits=("trait", lambda s: ";".join(sorted(set(map(str, s)))[:25])),
            gwas_catalog_snps=("snp", lambda s: ";".join(sorted(set(map(str, s)))[:25])),
        )
        .reset_index()
    )
    return summary


def cache_json(name: str, url: str, sleep_s: float = 0.05) -> dict[str, Any]:
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / f"{name}.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            pass
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT})
        with urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        out = {"url": url, "payload": payload}
        path.write_text(json.dumps(out, indent=2, sort_keys=True))
        time.sleep(sleep_s)
        return out
    except Exception as exc:
        out = {"url": url, "error": repr(exc)}
        path.write_text(json.dumps(out, indent=2, sort_keys=True))
        return out


def chembl_snapshot(gene: str) -> dict[str, Any]:
    target_url = "https://www.ebi.ac.uk/chembl/api/data/target/search.json?" + urlencode({"q": gene})
    targets = cache_json(f"chembl_target_{gene}", target_url).get("payload", {}).get("targets", [])
    human = [t for t in targets if t.get("organism") == "Homo sapiens"]
    if not human:
        return {
            "chembl_target_id": "",
            "chembl_pref_name": "",
            "chembl_target_type": "",
            "chembl_activity_count": 0,
            "chembl_best_nM": np.nan,
        }
    target = human[0]
    tid = target.get("target_chembl_id") or ""
    act_url = f"https://www.ebi.ac.uk/chembl/api/data/activity.json?limit=100&target_chembl_id={tid}&standard_units=nM"
    payload = cache_json(f"chembl_activity_{gene}_{tid}", act_url).get("payload", {})
    activities = payload.get("activities", []) or []
    values = pd.to_numeric(pd.Series([a.get("standard_value") for a in activities]), errors="coerce").dropna()
    return {
        "chembl_target_id": tid,
        "chembl_pref_name": target.get("pref_name", ""),
        "chembl_target_type": target.get("target_type", ""),
        "chembl_activity_count": int(payload.get("page_meta", {}).get("total_count", 0) or 0),
        "chembl_best_nM": float(values.min()) if len(values) else np.nan,
    }


def clinicaltrials_count(gene: str) -> int:
    url = "https://clinicaltrials.gov/api/v2/studies?" + urlencode(
        {
            "query.term": gene,
            "query.cond": "autoimmune OR multiple sclerosis OR rheumatoid arthritis OR lupus OR Crohn OR psoriasis",
            "format": "json",
            "pageSize": 1,
            "countTotal": "true",
        }
    )
    return int(cache_json(f"clinicaltrials_{gene}", url).get("payload", {}).get("totalCount", 0) or 0)


def europepmc_count(gene: str) -> int:
    query = (
        f'{gene} AND ("multiple sclerosis" OR "rheumatoid arthritis" OR lupus OR Crohn OR '
        '"ulcerative colitis" OR psoriasis OR "type 1 diabetes" OR autoimmune)'
    )
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urlencode(
        {"query": query, "format": "json", "pageSize": 1}
    )
    return int(cache_json(f"europepmc_{gene}", url).get("payload", {}).get("hitCount", 0) or 0)


def merge_one(base: pd.DataFrame, df: pd.DataFrame, cols: list[str], suffix: str = "") -> pd.DataFrame:
    if df.empty or "gene" not in df.columns:
        for col in cols:
            base[col + suffix] = np.nan
        return base
    use = df[["gene"] + [c for c in cols if c in df.columns]].copy()
    use["gene"] = use["gene"].astype(str).str.upper()
    return base.merge(use, on="gene", how="left", suffixes=("", suffix))


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    gwas = load_autoimmune_gwas_gene_summary()
    if gwas.empty:
        raise RuntimeError("No autoimmune GWAS Catalog gene summary could be built")

    broad = read_table(PATHS["broad"])
    residual = read_table(PATHS["residual"])
    wave25 = read_table(PATHS["wave25"])
    wave23 = read_table(PATHS["wave23_gene"])
    target_first = read_table(PATHS["target_first"])
    local_chembl = read_table(PATHS["local_chembl"])
    direct = read_table(PATHS["direct"])

    for df in [broad, residual, wave25, wave23, target_first, local_chembl, direct]:
        if not df.empty and "gene" in df.columns:
            df["gene"] = df["gene"].astype(str).str.upper()

    rows = gwas.copy()
    rows["gene"] = rows["gene"].astype(str).str.upper()
    rows = merge_one(
        rows,
        broad,
        [
            "positive_disease_count",
            "negative_disease_count",
            "positive_diseases",
            "negative_diseases",
            "ms_wm_delta_log2",
            "ms_wm_p",
            "ms_positive_nominal",
            "discovery_priority_score",
        ],
    )
    rows = merge_one(
        rows,
        residual,
        [
            "retained_positive_disease_count",
            "non_ibd_retained_positive_disease_count",
            "strict_core_covariate_surviving_disease_count",
            "residual_gate_priority_score",
        ],
    )
    rows = merge_one(
        rows,
        wave25,
        [
            "genetics_ready_score",
            "ot_n_diseases_score_ge_0_5",
            "gtex_n_relevant_tissues_with_significant_cis_eqtl",
            "foundation_rescue_recommendation",
            "foundation_real_perturbation_alignment_call",
            "direct_perturbation_support_binary",
            "perturbation_score",
            "proxy_call",
            "primary_blocker",
            "overall_proxy_score",
        ],
        suffix="_wave25",
    )
    rows = merge_one(
        rows,
        wave23,
        [
            "ot_credible_disease_count_ge_0_5",
            "geneformer_support_contexts",
            "real_perturbation_alignment_call",
            "direct_selectivity_score",
            "chembl_activity_records_scanned",
            "chembl_best_standard_value_nM",
            "residual_retained_positive_disease_count",
        ],
        suffix="_wave23",
    )
    rows = merge_one(
        rows,
        target_first,
        [
            "gate_call",
            "hard_failures",
            "target_first_score",
            "genetics_diseases_ge_0_5",
            "direct_selective_support",
            "manual_druggability_score",
            "chembl_activity_records",
            "clinicaltrials_total_count",
            "manual_prior_risk",
            "manual_blocker",
        ],
        suffix="_target_first",
    )
    if not local_chembl.empty:
        chem = (
            local_chembl[local_chembl["organism"].eq("Homo sapiens")]
            .sort_values(["gene", "activity_values_nM_count"], ascending=[True, False])
            .groupby("gene")
            .head(1)
        )
        rows = merge_one(
            rows,
            chem,
            ["target_chembl_id", "pref_name", "target_type", "activity_values_nM_count", "best_standard_value_nM"],
            suffix="_local_chembl",
        )

    def num_col(name: str, default: float = 0.0) -> pd.Series:
        if name not in rows.columns:
            return pd.Series(default, index=rows.index, dtype="float64")
        return pd.to_numeric(rows[name], errors="coerce").fillna(default)

    def str_col(name: str, default: str = "") -> pd.Series:
        if name not in rows.columns:
            return pd.Series(default, index=rows.index, dtype="object")
        return rows[name].fillna(default).astype(str)

    # Preliminary score before external API expansion.
    rows["local_positive_disease_count"] = num_col("positive_disease_count")
    rows["local_negative_disease_count"] = num_col("negative_disease_count")
    rows["residual_retained_disease_count"] = num_col("retained_positive_disease_count")
    rows["ms_anchor"] = (num_col("ms_wm_delta_log2") > 0) & (num_col("ms_wm_p", default=1.0) < 0.1)
    rows["existing_chembl_activity_count"] = (
        num_col("activity_values_nM_count_local_chembl")
        + num_col("chembl_activity_records_target_first")
        + num_col("chembl_activity_records_scanned_wave23")
    )
    rows["preliminary_score"] = (
        2.0 * np.minimum(rows["gwas_catalog_trait_count"], 8)
        + 1.2 * np.minimum(num_col("ot_n_diseases_score_ge_0_5"), 8)
        + 1.0 * np.minimum(rows["local_positive_disease_count"], 5)
        + 1.0 * np.minimum(rows["residual_retained_disease_count"], 3)
        + rows["ms_anchor"].astype(float)
        + (rows["existing_chembl_activity_count"] > 10).astype(float)
        - 0.8 * rows["local_negative_disease_count"]
    )

    api_candidates = (
        rows.sort_values(["preliminary_score", "gwas_catalog_trait_count"], ascending=False)
        .head(80)["gene"]
        .tolist()
    )
    api_rows: list[dict[str, Any]] = []
    for gene in api_candidates:
        snap = chembl_snapshot(gene)
        api_rows.append(
            {
                "gene": gene,
                **snap,
                "clinicaltrials_autoimmune_count": clinicaltrials_count(gene),
                "europepmc_autoimmune_hit_count": europepmc_count(gene),
            }
        )
    api = pd.DataFrame(api_rows)
    rows = rows.merge(api, on="gene", how="left")

    rows["api_chembl_activity_count"] = pd.to_numeric(rows["chembl_activity_count"], errors="coerce").fillna(0)
    rows["druggable_activity_count"] = rows["existing_chembl_activity_count"] + rows["api_chembl_activity_count"]
    rows["clinicaltrials_autoimmune_count"] = pd.to_numeric(
        rows["clinicaltrials_autoimmune_count"], errors="coerce"
    ).fillna(0)
    rows["europepmc_autoimmune_hit_count"] = pd.to_numeric(
        rows["europepmc_autoimmune_hit_count"], errors="coerce"
    ).fillna(0)
    rows["wave25_direct_perturbation"] = num_col("direct_perturbation_support_binary") > 0
    rows["target_first_direct_selective"] = rows.get("direct_selective_support_target_first", pd.Series(False, index=rows.index)).fillna(False).astype(bool)
    rows["perturbation_or_model_support"] = (
        rows["wave25_direct_perturbation"]
        | rows["target_first_direct_selective"]
        | str_col("foundation_rescue_recommendation").str.contains("align", case=False, na=False)
        | str_col("foundation_real_perturbation_alignment_call").str.contains("align", case=False, na=False)
    )

    rows["manual_blocker_class"] = rows["gene"].map(lambda g: MANUAL_BLOCKERS.get(g, ("", ""))[0])
    rows["manual_blocker_text_wave34"] = rows["gene"].map(lambda g: MANUAL_BLOCKERS.get(g, ("", ""))[1])
    blocking_classes = {"blocking_prior_art", "wrong_direction", "crowded_or_wrong_direction"}
    rows["manual_blocking"] = rows["manual_blocker_class"].isin(blocking_classes)
    rows["prior_art_saturated"] = (
        rows["manual_blocking"]
        | (rows["clinicaltrials_autoimmune_count"] > 5)
        | (rows["europepmc_autoimmune_hit_count"] > 5000)
        | str_col("manual_prior_risk_target_first").isin(["blocking", "high"])
    )

    rows["gate_genetic_breadth"] = (rows["gwas_catalog_trait_count"] >= 4) | (
        num_col("genetics_ready_score") >= 5
    )
    rows["gate_local_cell_state"] = (
        (rows["local_positive_disease_count"] >= 3)
        | (rows["residual_retained_disease_count"] >= 2)
        | rows["ms_anchor"]
    )
    rows["gate_druggable_surface"] = rows["druggable_activity_count"] >= 10
    rows["gate_perturbation_or_model"] = rows["perturbation_or_model_support"]
    rows["gate_not_prior_art_blocked"] = ~rows["prior_art_saturated"]

    rows["wave34_score"] = (
        rows["preliminary_score"]
        + 1.5 * rows["gate_druggable_surface"].astype(float)
        + 1.5 * rows["gate_perturbation_or_model"].astype(float)
        - 2.5 * rows["prior_art_saturated"].astype(float)
        - 1.5 * rows["manual_blocking"].astype(float)
    )

    gate_cols = [
        "gate_genetic_breadth",
        "gate_local_cell_state",
        "gate_druggable_surface",
        "gate_perturbation_or_model",
        "gate_not_prior_art_blocked",
    ]
    rows["failed_gates"] = rows[gate_cols].apply(
        lambda r: ";".join(col for col, passed in r.items() if not bool(passed)), axis=1
    )

    def call(row: pd.Series) -> str:
        passed = {col: bool(row[col]) for col in gate_cols}
        if all(passed.values()):
            return "GO_TO_HOSTILE_NOVELTY_REVIEW"
        if passed["gate_genetic_breadth"] and passed["gate_local_cell_state"] and passed["gate_druggable_surface"]:
            if not passed["gate_not_prior_art_blocked"]:
                return "NO_GO_GENETIC_DRUGGABLE_PRIOR_ART_BLOCKED"
            if not passed["gate_perturbation_or_model"]:
                return "PARK_NEEDS_DISEASE_RELEVANT_PERTURBATION"
        if passed["gate_genetic_breadth"] and passed["gate_druggable_surface"] and not passed["gate_local_cell_state"]:
            return "PARK_GENETIC_DRUGGABLE_NEEDS_CELL_STATE"
        if passed["gate_genetic_breadth"] and passed["gate_local_cell_state"] and not passed["gate_druggable_surface"]:
            return "PARK_GENETIC_CELL_STATE_NOT_CURRENTLY_DRUGGABLE"
        return "NO_GO_WAVE34_GENETICS_EXPRESSION_DRUGGABILITY"

    rows["wave34_call"] = rows.apply(call, axis=1)
    rows = rows.sort_values(["wave34_score", "gwas_catalog_trait_count"], ascending=False)

    keep_cols = [
        "gene",
        "wave34_score",
        "wave34_call",
        "failed_gates",
        "gwas_catalog_trait_count",
        "gwas_catalog_min_p",
        "gwas_catalog_traits",
        "local_positive_disease_count",
        "local_negative_disease_count",
        "positive_diseases",
        "residual_retained_disease_count",
        "ms_anchor",
        "ms_wm_delta_log2",
        "ms_wm_p",
        "genetics_ready_score",
        "ot_n_diseases_score_ge_0_5",
        "gtex_n_relevant_tissues_with_significant_cis_eqtl",
        "druggable_activity_count",
        "chembl_target_id",
        "chembl_pref_name",
        "chembl_target_type",
        "chembl_best_nM",
        "clinicaltrials_autoimmune_count",
        "europepmc_autoimmune_hit_count",
        "perturbation_or_model_support",
        "foundation_rescue_recommendation",
        "foundation_real_perturbation_alignment_call",
        "manual_blocker_class",
        "manual_blocker_text_wave34",
        "manual_blocker_target_first",
        "proxy_call",
        "primary_blocker",
    ]
    keep_cols = [c for c in keep_cols if c in rows.columns]
    rows[keep_cols].to_csv(OUT / "wave34_genetics_expression_druggability_rank.tsv", sep="\t", index=False)

    gate_long = rows[["gene", "wave34_call", "wave34_score"] + gate_cols].melt(
        id_vars=["gene", "wave34_call", "wave34_score"], var_name="gate", value_name="passed"
    )
    gate_long.to_csv(OUT / "wave34_genetics_expression_druggability_gates.tsv", sep="\t", index=False)

    summary = {
        "seed": SEED,
        "n_gwas_genes": int(len(rows)),
        "n_api_expanded_genes": int(len(api_candidates)),
        "call_counts": rows["wave34_call"].value_counts().to_dict(),
        "top_candidates": rows.head(15)[
            [
                "gene",
                "wave34_score",
                "wave34_call",
                "gwas_catalog_trait_count",
                "local_positive_disease_count",
                "residual_retained_disease_count",
                "ms_anchor",
                "druggable_activity_count",
                "clinicaltrials_autoimmune_count",
                "manual_blocker_class",
                "failed_gates",
            ]
        ].to_dict(orient="records"),
        "interpretation": (
            "This is a genetics-first rescue scan. No row may be interpreted as a causal claim: "
            "GWAS Catalog mapped-gene recurrence is locus-level evidence only. Promotion requires "
            "all gates, including disease-relevant perturbation/model support and non-blocking prior art."
        ),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
