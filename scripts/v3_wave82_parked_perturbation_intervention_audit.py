#!/usr/bin/env python3
"""Wave82 intervention-route stress test for parked perturbation candidates.

Wave81 left no promotable target after strict direct/foundation gates, but it
did identify several parked candidates. This audit asks a harder translational
question: does any parked perturbation/readout candidate have a credible
intervention route, cross-disease support, and novelty path?
"""

from __future__ import annotations

import json
import math
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from v3_analyze_direct_h5ad_cell_states import ROOT


SEED = 20260527
OUT = ROOT / "results_v3" / "wave82_parked_perturbation_intervention_audit"
CACHE = ROOT / "data" / "raw_v3" / "wave82_api_cache"

CANDIDATES = [
    "DAB2",
    "CD9",
    "PARK7",
    "PSAP",
    "LYN",
    "HEXA",
    "HEXB",
    # False-positive controls from the first Wave81 correction.
    "SP140",
    "RGS14",
    "STAT4",
]

W81 = ROOT / "results_v3" / "wave81_perturbation_first_rescue" / "perturbation_first_integrated_rank.tsv"
W62 = ROOT / "results_v3" / "wave62_opentargets_target_resolution" / "target_resolution_summary.tsv"
W37 = ROOT / "results_v3" / "wave37_gse212008_crispr_efferocytosis_screen" / "gene_level_screen_scores.tsv"
W57 = ROOT / "results_v3" / "wave57_intervention_first_geneformer_screen" / "wave57_geneformer_gene_summary.tsv"
W69D = ROOT / "results_v3" / "wave69d_gse282122_geneformer_remission_centroid" / "geneformer_remission_gene_summary.tsv"
W70C = ROOT / "results_v3" / "wave70c_inhibitory_receptor_geneformer_direction" / "geneformer_direction_gene_summary.tsv"
BROAD = ROOT / "results_v3" / "broad_h5ad_gene_discovery" / "broad_h5ad_gene_contrasts.tsv"
MS = ROOT / "results_v3" / "gse111972_full_ms_wm_signature.tsv"
W68_RAW = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "raw_remission_response_gene_tests.tsv"
W68_PAIR = ROOT / "results_v3" / "wave68_gse282122_unrestricted_gene_screen" / "paired_gene_delta_tests.tsv"

MANUAL_INTERVENTION_RULES = {
    "DAB2": {
        "class": "intracellular endocytic/adaptor protein",
        "route": "no selective direct modality; possible pathway/readout only",
        "manual_blocker": "adaptor_not_druggable_directly",
    },
    "CD9": {
        "class": "surface tetraspanin",
        "route": "antibody route plausible in principle but CD9 is broad and platelet/immune/stromal biology is nonspecific",
        "manual_blocker": "broad_surface_tetraspanin_no_disease_breadth",
    },
    "PARK7": {
        "class": "redox/chaperone enzyme-like stress protein",
        "route": "small-molecule modulation exists in adjacent neurodegeneration space; autoimmune direction not anchored locally",
        "manual_blocker": "generic_oxidative_stress_no_ms_anchor",
    },
    "PSAP": {
        "class": "secreted/lysosomal sphingolipid cofactor precursor",
        "route": "replacement/peptide biology plausible but not target-resolved and not cross-autoimmune anchored",
        "manual_blocker": "secreted_lysosomal_readout_no_target_anchor",
    },
    "LYN": {
        "class": "SRC-family kinase",
        "route": "kinase inhibitors exist but selectivity and immune pleiotropy are poor",
        "manual_blocker": "broad_src_family_kinase",
    },
    "HEXA": {
        "class": "lysosomal enzyme subunit",
        "route": "enzyme replacement/gene therapy precedent in storage disease, not autoimmune module intervention",
        "manual_blocker": "lysosomal_housekeeping_enzyme_no_autoimmune_direction",
    },
    "HEXB": {
        "class": "lysosomal enzyme subunit",
        "route": "enzyme replacement/gene therapy precedent in storage disease, not autoimmune module intervention",
        "manual_blocker": "lysosomal_housekeeping_enzyme_no_autoimmune_direction",
    },
    "SP140": {
        "class": "immune chromatin reader",
        "route": "bromodomain inhibitor precedent exists, but prior Wave56 direction/modality and novelty blockers remain",
        "manual_blocker": "prior_art_directionality_and_no_strict_model_support",
    },
    "RGS14": {
        "class": "regulator of G-protein signaling/scaffold",
        "route": "no selective immune intervention route identified",
        "manual_blocker": "no_direct_perturbation_or_modality",
    },
    "STAT4": {
        "class": "transcription factor",
        "route": "broad Th1/Th17 TF biology; no direct selective modality",
        "manual_blocker": "tf_not_selectively_druggable_wrong_direction",
    },
}

KNOWN_UNIPROT_ACCESSIONS = {
    "DAB2": "P98082",
    "CD9": "P21926",
    "PARK7": "Q99497",
    "PSAP": "P07602",
    "LYN": "P07948",
    "HEXA": "P06865",
    "HEXB": "P07686",
    "SP140": "Q13342",
    "RGS14": "O43566",
    "STAT4": "Q14765",
}

KNOWN_CHEMBL_TARGET_IDS = {
    "DAB2": [],
    "CD9": [],
    "PARK7": ["CHEMBL5169188", "CHEMBL6066048"],
    "PSAP": ["CHEMBL3580523"],
    "LYN": ["CHEMBL3905", "CHEMBL6066565"],
    "HEXA": ["CHEMBL1250415", "CHEMBL3038485"],
    "HEXB": ["CHEMBL5877", "CHEMBL3038485"],
    "SP140": ["CHEMBL3108643", "CHEMBL4105997"],
    "RGS14": [],
    "STAT4": ["CHEMBL4523296", "CHEMBL4523706"],
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_tsv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", low_memory=False) if path.exists() else pd.DataFrame()


def markdown_table(df: pd.DataFrame, max_rows: int = 30) -> str:
    if df.empty:
        return "_No rows._"
    view = df.head(max_rows).copy()
    cols = list(view.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in view.iterrows():
        vals = []
        for col in cols:
            value = row[col]
            if isinstance(value, float):
                vals.append("" if math.isnan(value) else f"{value:.4g}")
            else:
                vals.append(str(value).replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def fetch_json(name: str, url: str, sleep_s: float = 0.15) -> dict[str, Any]:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{name}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ms-auto-research-wave82/1.0"})
        with urllib.request.urlopen(req, timeout=25) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="replace"))
        path.write_text(json.dumps({"url": url, "status": "ok", "payload": payload}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        time.sleep(sleep_s)
        return {"url": url, "status": "ok", "payload": payload}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        payload = {"url": url, "status": "error", "error": str(exc)}
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return payload


def api_rows() -> pd.DataFrame:
    rows = []
    for gene in CANDIDATES:
        chembl_url = f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={urllib.parse.quote(gene)}"
        uniprot_query = urllib.parse.quote(f"gene_exact:{gene} AND organism_id:9606")
        uniprot_url = f"https://rest.uniprot.org/uniprotkb/search?query={uniprot_query}&format=json&size=5"
        epmc_query = urllib.parse.quote(f'"{gene}" AND (autoimmune OR "multiple sclerosis" OR Crohn OR psoriasis OR lupus)')
        epmc_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={epmc_query}&format=json&pageSize=5"
        ct_url = f"https://clinicaltrials.gov/api/v2/studies?query.term={urllib.parse.quote(gene + ' autoimmune')}&pageSize=5&format=json"

        chembl = fetch_json(f"chembl_{gene}", chembl_url)
        uniprot = fetch_json(f"uniprot_{gene}", uniprot_url)
        accession = KNOWN_UNIPROT_ACCESSIONS[gene]
        uniprot_direct = fetch_json(f"uniprot_direct_{gene}_{accession}", f"https://rest.uniprot.org/uniprotkb/{accession}.json")
        epmc = fetch_json(f"europepmc_{gene}", epmc_url)
        ct = fetch_json(f"clinicaltrials_{gene}", ct_url)
        known_chembl_ids = KNOWN_CHEMBL_TARGET_IDS[gene]
        chembl_target_payloads = []
        chembl_activity_counts = []
        for target_id in known_chembl_ids:
            chembl_target_payloads.append(
                fetch_json(f"chembl_target_{target_id}", f"https://www.ebi.ac.uk/chembl/api/data/target/{target_id}.json")
            )
            activity_payload = fetch_json(
                f"chembl_activity_count_{target_id}",
                f"https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id={target_id}&limit=1",
            )
            page_meta = activity_payload.get("payload", {}).get("page_meta", {}) if isinstance(activity_payload.get("payload", {}), dict) else {}
            try:
                chembl_activity_counts.append(int(page_meta.get("total_count", 0)))
            except (TypeError, ValueError):
                chembl_activity_counts.append(0)

        chembl_payload = chembl.get("payload", {})
        chembl_targets = chembl_payload.get("targets", []) if isinstance(chembl_payload, dict) else []
        human_targets = [
            t
            for t in chembl_targets
            if str(t.get("organism", "")).lower() == "homo sapiens"
            or str(t.get("organism", "")).lower() == "human"
        ]
        exact_targets = [
            t
            for t in human_targets
            if gene.upper() in str(t.get("pref_name", "")).upper()
            or gene.upper() in " ".join(str(x).upper() for x in t.get("target_synonyms", []))
        ]

        uniprot_payload = uniprot.get("payload", {})
        uniprot_results = uniprot_payload.get("results", []) if isinstance(uniprot_payload, dict) else []
        locations = []
        keywords = []
        accessions = [accession]
        protein_names = []
        direct_result = uniprot_direct.get("payload", {}) if isinstance(uniprot_direct.get("payload", {}), dict) else {}
        result_iter = [direct_result] if direct_result else []
        result_iter.extend([result for result in uniprot_results[:3] if result.get("primaryAccession") != accession])
        for result in result_iter[:4]:
            protein_names.append(result.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", ""))
            comments = result.get("comments", [])
            for comment in comments:
                if comment.get("commentType") == "SUBCELLULAR LOCATION":
                    for loc in comment.get("subcellularLocations", []):
                        location = loc.get("location", {}).get("value")
                        if location:
                            locations.append(location)
            for keyword in result.get("keywords", []):
                name = keyword.get("name")
                if name:
                    keywords.append(name)

        epmc_payload = epmc.get("payload", {})
        hit_count = int(epmc_payload.get("hitCount", 0)) if isinstance(epmc_payload, dict) else 0
        epmc_titles = []
        if isinstance(epmc_payload, dict):
            for item in epmc_payload.get("resultList", {}).get("result", [])[:3]:
                epmc_titles.append(str(item.get("title", "")))

        ct_payload = ct.get("payload", {})
        studies = ct_payload.get("studies", []) if isinstance(ct_payload, dict) else []
        ct_titles = []
        for study in studies[:3]:
            ident = study.get("protocolSection", {}).get("identificationModule", {})
            status = study.get("protocolSection", {}).get("statusModule", {})
            ct_titles.append(f"{ident.get('nctId','')}:{ident.get('briefTitle','')}:{status.get('overallStatus','')}")

        rows.append(
            {
                "gene": gene,
                "chembl_human_target_count": len(human_targets),
                "chembl_exact_human_target_count": len(known_chembl_ids),
                "chembl_exact_target_ids": ";".join(known_chembl_ids),
                "chembl_known_activity_total_count": int(sum(chembl_activity_counts)),
                "uniprot_accessions": ";".join(accessions),
                "uniprot_primary_accession": accession,
                "uniprot_protein_names": ";".join(protein_names),
                "uniprot_locations": ";".join(sorted(set(locations))),
                "uniprot_keywords": ";".join(sorted(set(keywords))[:20]),
                "europepmc_hit_count": hit_count,
                "europepmc_top_titles": " || ".join(epmc_titles),
                "clinicaltrials_returned_count": len(studies),
                "clinicaltrials_top_records": " || ".join(ct_titles),
                "chembl_url": chembl_url,
                "uniprot_url": uniprot_url,
                "europepmc_url": epmc_url,
                "clinicaltrials_url": ct_url,
                "google_patents_url": f"https://patents.google.com/?q={urllib.parse.quote(gene + ' autoimmune inhibitor agonist')}",
            }
        )
    return pd.DataFrame(rows)


def local_rows() -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    genes = set(CANDIDATES)
    w81 = read_tsv(W81)
    w62 = read_tsv(W62)
    w37 = read_tsv(W37)
    w57 = read_tsv(W57)
    w69d = read_tsv(W69D)
    w70c = read_tsv(W70C)
    broad = read_tsv(BROAD)
    ms = read_tsv(MS)
    raw = read_tsv(W68_RAW)
    pair = read_tsv(W68_PAIR)

    tables = {}
    for name, df, col in [
        ("wave81", w81, "gene"),
        ("wave62", w62, "gene"),
        ("wave37", w37, "gene_symbol"),
        ("wave57", w57, "gene"),
        ("wave69d", w69d, "gene"),
        ("wave70c", w70c, "gene"),
        ("broad", broad, "gene"),
        ("ms", ms, "gene"),
        ("ibd_raw", raw, "gene"),
        ("ibd_paired", pair, "gene"),
    ]:
        if not df.empty and col in df.columns:
            tables[name] = df[df[col].astype(str).str.upper().isin(genes)].copy()
        else:
            tables[name] = pd.DataFrame()

    rows = []
    for gene in CANDIDATES:
        w81_row = tables["wave81"][tables["wave81"]["gene"].eq(gene)]
        w62_row = tables["wave62"][tables["wave62"]["gene"].eq(gene)]
        broad_rows = tables["broad"][tables["broad"]["gene"].eq(gene)]
        ms_row = tables["ms"][tables["ms"]["gene"].eq(gene)]
        raw_rows = tables["ibd_raw"][tables["ibd_raw"]["gene"].eq(gene)]
        pair_rows = tables["ibd_paired"][tables["ibd_paired"]["gene"].eq(gene)]

        positive_broad = broad_rows[
            (broad_rows["delta_log2_cpm"] >= 0.35) & (broad_rows["p"] <= 0.05)
        ] if not broad_rows.empty else pd.DataFrame()
        ms_delta = float(ms_row["delta_log2"].iloc[0]) if not ms_row.empty else np.nan
        ms_p = float(ms_row["p"].iloc[0]) if not ms_row.empty else np.nan
        ms_expr_anchor = bool(math.isfinite(ms_delta) and abs(ms_delta) >= 0.35 and ms_p <= 0.05)
        ms_genetic_anchor = False
        genetic_disease_count = 0
        if not w62_row.empty:
            genetic_disease_count = int(float(w62_row.get("strong_l2g_disease_count", pd.Series([0])).iloc[0] or 0))
            ms_genetic_anchor = float(w62_row.get("ms_max_l2g_score", pd.Series([0])).iloc[0] or 0) >= 0.5

        rows.append(
            {
                "gene": gene,
                "wave81_call": w81_row["wave81_call"].iloc[0] if not w81_row.empty else "",
                "wave81_score": float(w81_row["score"].iloc[0]) if not w81_row.empty else np.nan,
                "direct_perturbation": int(float(w81_row["direct_perturbation"].iloc[0])) if not w81_row.empty else 0,
                "direct_perturbation_detail": w81_row["direct_perturbation_detail"].iloc[0] if not w81_row.empty else "",
                "foundation_model_support": int(float(w81_row["foundation_model_support"].iloc[0])) if not w81_row.empty else 0,
                "foundation_model_detail": w81_row["foundation_model_detail"].iloc[0] if not w81_row.empty else "",
                "ms_expr_anchor": int(ms_expr_anchor),
                "ms_delta_log2": ms_delta,
                "ms_p": ms_p,
                "ms_genetic_anchor": int(ms_genetic_anchor),
                "strong_l2g_disease_count": genetic_disease_count,
                "positive_broad_disease_count": int(positive_broad["disease_name"].nunique()) if not positive_broad.empty else 0,
                "positive_broad_diseases": ";".join(sorted(positive_broad["disease_name"].astype(str).unique())) if not positive_broad.empty else "",
                "best_ibd_raw_response_p": float(raw_rows["raw_p"].min()) if not raw_rows.empty else np.nan,
                "best_ibd_raw_response_fdr": float(raw_rows["raw_fdr"].min()) if not raw_rows.empty else np.nan,
                "best_ibd_paired_p": float(pair_rows["paired_p"].min()) if not pair_rows.empty else np.nan,
                "best_ibd_paired_fdr": float(pair_rows["paired_fdr"].min()) if not pair_rows.empty else np.nan,
                "wave62_call": w62_row["wave62_call"].iloc[0] if not w62_row.empty and "wave62_call" in w62_row else "",
            }
        )
    return pd.DataFrame(rows), tables


def integrate(local: pd.DataFrame, api: pd.DataFrame) -> pd.DataFrame:
    rows = []
    api_by = api.set_index("gene").to_dict(orient="index")
    for _, row in local.iterrows():
        gene = row["gene"]
        a = api_by.get(gene, {})
        manual = MANUAL_INTERVENTION_RULES[gene]
        modality_ready = int((a.get("chembl_exact_human_target_count", 0) or 0) > 0)
        location_text = str(a.get("uniprot_locations", "")).lower()
        extracellular_or_membrane = (
            manual["class"].startswith("surface")
            and "cell membrane" in location_text
        ) or (
            "secreted" in location_text
            and "secreted" in manual["class"]
        )
        modality_or_accessible = int(modality_ready or extracellular_or_membrane)
        evidence_channels = int(row["direct_perturbation"]) + int(row["foundation_model_support"]) + int(row["ms_expr_anchor"] or row["ms_genetic_anchor"]) + int(row["positive_broad_disease_count"] >= 3) + int(row["strong_l2g_disease_count"] >= 2) + int(modality_or_accessible)
        hard_failures = []
        if not (row["ms_expr_anchor"] or row["ms_genetic_anchor"]):
            hard_failures.append("no_ms_anchor")
        if not row["direct_perturbation"] and not row["foundation_model_support"]:
            hard_failures.append("no_positive_perturbation_or_model_support")
        if row["positive_broad_disease_count"] < 3:
            hard_failures.append("insufficient_cross_disease_state_breadth")
        if not modality_or_accessible:
            hard_failures.append("no_direct_modality_or_accessible_route")
        hard_failures.append(str(manual["manual_blocker"]))

        if evidence_channels >= 5 and not hard_failures:
            call = "PROMOTE_INTERVENTION_ROUTE"
        elif evidence_channels >= 4 and len(hard_failures) <= 2:
            call = "PARK_MECHANISTIC_RESCUE_ROUTE"
        elif row["direct_perturbation"] or row["foundation_model_support"] or row["ms_expr_anchor"] or row["ms_genetic_anchor"]:
            call = "PARK_READOUT_OR_PRECLINICAL_PROBE"
        else:
            call = "NO_GO_WAVE82"
        if manual["manual_blocker"] in {
            "broad_src_family_kinase",
            "prior_art_directionality_and_no_strict_model_support",
            "tf_not_selectively_druggable_wrong_direction",
        }:
            call = "NO_GO_WAVE82_BLOCKED"

        rows.append(
            {
                **row.to_dict(),
                "gene_class": manual["class"],
                "intervention_route_read": manual["route"],
                "manual_blocker": manual["manual_blocker"],
                "chembl_exact_human_target_count": a.get("chembl_exact_human_target_count", 0),
                "chembl_exact_target_ids": a.get("chembl_exact_target_ids", ""),
                "uniprot_accessions": a.get("uniprot_accessions", ""),
                "uniprot_locations": a.get("uniprot_locations", ""),
                "europepmc_hit_count": a.get("europepmc_hit_count", 0),
                "clinicaltrials_returned_count": a.get("clinicaltrials_returned_count", 0),
                "google_patents_url": a.get("google_patents_url", ""),
                "modality_or_accessible_route": modality_or_accessible,
                "evidence_channel_count": evidence_channels,
                "hard_failures": ";".join(hard_failures),
                "wave82_call": call,
            }
        )
    rank = pd.DataFrame(rows)
    priority = {
        "PROMOTE_INTERVENTION_ROUTE": 0,
        "PARK_MECHANISTIC_RESCUE_ROUTE": 1,
        "PARK_READOUT_OR_PRECLINICAL_PROBE": 2,
        "NO_GO_WAVE82_BLOCKED": 3,
        "NO_GO_WAVE82": 4,
    }
    rank["priority"] = rank["wave82_call"].map(priority).fillna(9)
    return rank.sort_values(["priority", "evidence_channel_count", "wave81_score"], ascending=[True, False, False]).drop(columns=["priority"])


def write_report(rank: pd.DataFrame, api: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> None:
    promoted = rank[rank["wave82_call"].eq("PROMOTE_INTERVENTION_ROUTE")]
    verdict = "NO_PROMOTABLE_INTERVENTION_ROUTE" if promoted.empty else "PROMOTE_INTERVENTION_ROUTE"
    lines = [
        "# Wave82 Parked Perturbation Intervention Audit",
        "",
        "## Question",
        "",
        "Can any parked perturbation/model candidate be converted from a readout into",
        "a credible intervention point with modality, cross-disease support, and a",
        "defensible direction?",
        "",
        "## Verdict",
        "",
        verdict,
        "",
        "## Integrated Candidate Matrix",
        "",
        markdown_table(rank, max_rows=30),
        "",
        "## API / Public-Source Rows",
        "",
        markdown_table(api, max_rows=20),
    ]
    for name, df in tables.items():
        lines.extend(["", f"## Local Source Rows: {name}", "", markdown_table(df.head(80), max_rows=80)])
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `DAB2` and `CD9` are the most concrete perturbation-linked MS-expression",
            "  readouts, but neither has enough genetics, foundation-model, disease",
            "  breadth, or druggability support for a target claim.",
            "- `PARK7` and `PSAP` remain biology probes, not V3 intervention points.",
            "- `SP140`, `RGS14`, and `STAT4` are retained as false-positive controls",
            "  showing why table-presence flags cannot be used as support.",
        ]
    )
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    np.random.seed(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)

    local, tables = local_rows()
    api = api_rows()
    rank = integrate(local, api)

    local.to_csv(OUT / "wave82_local_candidate_evidence.tsv", sep="\t", index=False)
    api.to_csv(OUT / "wave82_public_api_rows.tsv", sep="\t", index=False)
    rank.to_csv(OUT / "wave82_integrated_intervention_rank.tsv", sep="\t", index=False)
    summary = {
        "random_seed": SEED,
        "candidates": CANDIDATES,
        "inputs": {
            "wave81": rel(W81),
            "wave62": rel(W62),
            "wave37": rel(W37),
            "wave57": rel(W57),
            "wave69d": rel(W69D),
            "wave70c": rel(W70C),
            "broad": rel(BROAD),
            "ms": rel(MS),
            "wave68_raw": rel(W68_RAW),
            "wave68_paired": rel(W68_PAIR),
        },
        "api_cache": rel(CACHE),
        "call_counts": rank["wave82_call"].value_counts().to_dict(),
        "top_rows": rank.head(10).replace({np.nan: None}).to_dict(orient="records"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    write_report(rank, api, tables)


if __name__ == "__main__":
    main()
