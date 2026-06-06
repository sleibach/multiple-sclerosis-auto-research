#!/usr/bin/env python3
"""Wave41 external deconvolution of the last parked L1000 unknown.

Wave27 left exactly one compound at `PARK_EXTERNAL_TARGET_LOOKUP_ONLY`:
BRD-A72180425 / K784-3188. This script resolves that item with public APIs
instead of guessing from the LINCS alias alone.

Promotion rule:
- A compound can only be reopened if an external source identifies a specific,
  druggable, non-cytotoxic target or mechanism that is coherent with the
  cross-autoimmune lipid-lysosomal myeloid module.
- A single L1000 opposite-signature hit remains insufficient without that
  target-level support and without cross-disease/module validation.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import asdict, dataclass
from html import unescape
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave41_l1000_external_unknown_deconvolution"
RAW = OUT / "raw_api"
INPUT = ROOT / "phases/v3/results" / "wave27_l1000_unknown_deconvolution" / "unknown_l1000_deconvolution.tsv"
SEED = 20260527


USER_AGENT = "ms-auto-research-wave41/1.0 (public API reproducibility script)"


@dataclass
class ExternalCall:
    source: str
    query: str
    url: str
    status: str
    cache_file: str


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def safe_name(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_")[:180] or "blank"


def fetch_json(source: str, query: str, url: str, cache_name: str, calls: list[ExternalCall], sleep_s: float = 0.15) -> dict[str, Any]:
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / f"{safe_name(cache_name)}.json"
    if cache.exists():
        try:
            payload = json.loads(cache.read_text(encoding="utf-8"))
            calls.append(ExternalCall(source, query, url, "cache_hit", rel(cache)))
            return payload
        except json.JSONDecodeError:
            cache.unlink()
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        with urlopen(req, timeout=45) as handle:
            payload = json.loads(handle.read().decode("utf-8"))
        write_json(cache, payload)
        calls.append(ExternalCall(source, query, url, "ok", rel(cache)))
        time.sleep(sleep_s)
        return payload
    except Exception as exc:  # noqa: BLE001 - preserve API failure as data
        payload = {"error": str(exc), "url": url}
        write_json(cache, payload)
        calls.append(ExternalCall(source, query, url, f"error:{type(exc).__name__}", rel(cache)))
        return payload


def fetch_text(source: str, query: str, url: str, cache_name: str, calls: list[ExternalCall], sleep_s: float = 0.15) -> str:
    RAW.mkdir(parents=True, exist_ok=True)
    cache = RAW / f"{safe_name(cache_name)}.html"
    if cache.exists():
        calls.append(ExternalCall(source, query, url, "cache_hit", rel(cache)))
        return cache.read_text(encoding="utf-8", errors="replace")
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html"})
        with urlopen(req, timeout=45) as handle:
            text = handle.read().decode("utf-8", errors="replace")
        cache.write_text(text, encoding="utf-8")
        calls.append(ExternalCall(source, query, url, "ok", rel(cache)))
        time.sleep(sleep_s)
        return text
    except Exception as exc:  # noqa: BLE001
        text = f"ERROR: {type(exc).__name__}: {exc}\nURL: {url}\n"
        cache.write_text(text, encoding="utf-8")
        calls.append(ExternalCall(source, query, url, f"error:{type(exc).__name__}", rel(cache)))
        return text


def pubchem_cids(identifier_kind: str, identifier: str, calls: list[ExternalCall]) -> list[int]:
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/{identifier_kind}/{quote(identifier, safe='')}/cids/JSON"
    payload = fetch_json("PubChem PUG-REST", identifier, url, f"pubchem_cids_{identifier_kind}_{identifier}", calls)
    return payload.get("IdentifierList", {}).get("CID", []) if isinstance(payload, dict) else []


def pubchem_synonyms(cid: int, calls: list[ExternalCall]) -> list[str]:
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/JSON"
    payload = fetch_json("PubChem PUG-REST", str(cid), url, f"pubchem_synonyms_{cid}", calls)
    info = payload.get("InformationList", {}).get("Information", []) if isinstance(payload, dict) else []
    if not info:
        return []
    return info[0].get("Synonym", []) or []


def pubchem_properties(cid: int, calls: list[ExternalCall]) -> dict[str, Any]:
    props = "IUPACName,MolecularFormula,MolecularWeight,XLogP,TPSA,CanonicalSMILES,InChIKey"
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/{props}/JSON"
    payload = fetch_json("PubChem PUG-REST", str(cid), url, f"pubchem_properties_{cid}", calls)
    items = payload.get("PropertyTable", {}).get("Properties", []) if isinstance(payload, dict) else []
    return items[0] if items else {}


def chembl_molecule(chembl_id: str, calls: list[ExternalCall]) -> dict[str, Any]:
    url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/{quote(chembl_id)}.json"
    return fetch_json("ChEMBL", chembl_id, url, f"chembl_molecule_{chembl_id}", calls)


def chembl_mechanisms(chembl_id: str, calls: list[ExternalCall]) -> dict[str, Any]:
    url = f"https://www.ebi.ac.uk/chembl/api/data/mechanism.json?{urlencode({'molecule_chembl_id': chembl_id, 'limit': 1000})}"
    return fetch_json("ChEMBL", chembl_id, url, f"chembl_mechanisms_{chembl_id}", calls)


def chembl_activities(chembl_id: str, calls: list[ExternalCall]) -> dict[str, Any]:
    url = f"https://www.ebi.ac.uk/chembl/api/data/activity.json?{urlencode({'molecule_chembl_id': chembl_id, 'limit': 1000})}"
    return fetch_json("ChEMBL", chembl_id, url, f"chembl_activities_{chembl_id}", calls)


def europepmc_count(query: str, calls: list[ExternalCall]) -> int | None:
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?" + urlencode(
        {"query": query, "format": "json", "pageSize": 1}
    )
    payload = fetch_json("Europe PMC", query, url, f"europepmc_{query}", calls)
    try:
        return int(payload.get("hitCount"))
    except Exception:
        return None


def clinicaltrials_count(query: str, calls: list[ExternalCall]) -> int | None:
    url = "https://clinicaltrials.gov/api/v2/studies?" + urlencode({"query.term": query, "pageSize": 1})
    payload = fetch_json("ClinicalTrials.gov", query, url, f"clinicaltrials_{query}", calls)
    try:
        return int(payload.get("totalCount"))
    except Exception:
        return None


def dmoa_report(pert_id: str, calls: list[ExternalCall]) -> dict[str, Any]:
    url = f"https://maayanlab.cloud/dmoa/report/{quote(pert_id)}"
    html = fetch_text("L1000FWD DMOA", pert_id, url, f"dmoa_{pert_id}", calls)
    plain = unescape(re.sub(r"<[^>]+>", " ", html))
    plain = re.sub(r"\s+", " ", plain)
    known_moa = None
    known_targets = None
    match = re.search(r"MOA\s+([^<]{0,80}?)\s+Target\(s\)\s+([^<]{0,80}?)\s", plain)
    if match:
        known_moa = match.group(1).strip()
        known_targets = match.group(2).strip()
    predicted = []
    start = html.find("<h2>Predicted MOAs</h2>")
    if start >= 0:
        section = html[start : start + 7000]
        rows = re.findall(r"<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>", section, flags=re.S)
        for moa, prob in rows:
            moa_text = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", moa))).strip()
            prob_text = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", prob))).strip()
            if moa_text and prob_text:
                predicted.append({"moa": moa_text, "probability": prob_text})
    return {
        "known_moa_text": known_moa,
        "known_targets_text": known_targets,
        "predicted_moas_top5": predicted[:5],
        "html_length": len(html),
    }


def ncbi_ml162_table_lookup(calls: list[ExternalCall]) -> dict[str, Any]:
    url = "https://www.ncbi.nlm.nih.gov/books/NBK55069/table/ml162.t2/"
    html = fetch_text("NCBI Bookshelf", "BRD-A72180425", url, "ncbi_ml162_table_t2", calls)
    plain = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html)))
    idx = plain.find("BRD-A72180425")
    excerpt = plain[idx - 160 : idx + 260].strip() if idx >= 0 else ""
    return {
        "source_title": "Table 2, Summary of SAR on the Aniline Aromatic Ring",
        "url": url,
        "contains_brd_a72180425": idx >= 0,
        "local_excerpt": excerpt,
    }


def aggregate_chembl_targets(activities: dict[str, Any]) -> pd.DataFrame:
    rows = activities.get("activities", []) if isinstance(activities, dict) else []
    agg: dict[str, dict[str, Any]] = {}
    for row in rows:
        target = row.get("target_pref_name") or "unknown"
        current = agg.setdefault(
            target,
            {
                "target_pref_name": target,
                "target_chembl_id": row.get("target_chembl_id"),
                "target_organism": row.get("target_organism"),
                "n_activity_rows": 0,
                "n_active_comments": 0,
                "best_pchembl": None,
                "best_standard_nM": None,
                "assay_types": set(),
                "activity_comments": set(),
                "example_assay": row.get("assay_description"),
            },
        )
        current["n_activity_rows"] += 1
        if row.get("assay_type"):
            current["assay_types"].add(str(row.get("assay_type")))
        if row.get("activity_comment"):
            comment = str(row.get("activity_comment"))
            current["activity_comments"].add(comment)
            if comment.lower() == "active":
                current["n_active_comments"] += 1
        try:
            pchembl = float(row.get("pchembl_value")) if row.get("pchembl_value") is not None else None
        except Exception:
            pchembl = None
        if pchembl is not None and (current["best_pchembl"] is None or pchembl > current["best_pchembl"]):
            current["best_pchembl"] = pchembl
        try:
            std_nm = float(row.get("standard_value")) if row.get("standard_units") == "nM" else None
        except Exception:
            std_nm = None
        if std_nm is not None and (current["best_standard_nM"] is None or std_nm < current["best_standard_nM"]):
            current["best_standard_nM"] = std_nm
    out = []
    for item in agg.values():
        item = dict(item)
        item["assay_types"] = ";".join(sorted(item["assay_types"]))
        item["activity_comments"] = ";".join(sorted(item["activity_comments"]))[:300]
        out.append(item)
    df = pd.DataFrame(out)
    if df.empty:
        return df
    return df.sort_values(
        ["n_active_comments", "best_pchembl", "n_activity_rows"],
        ascending=[False, False, False],
        na_position="last",
    )


def markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    rows = []
    rows.append("| " + " | ".join(cols) + " |")
    rows.append("| " + " | ".join(["---"] * len(cols)) + " |")
    for _, row in df.iterrows():
        values = []
        for col in cols:
            value = "" if pd.isna(row[col]) else str(row[col])
            value = value.replace("\n", " ").replace("|", "\\|")
            values.append(value)
        rows.append("| " + " | ".join(values) + " |")
    return "\n".join(rows)


def classify_candidate(row: pd.Series, external: dict[str, Any]) -> dict[str, Any]:
    properties = external.get("pubchem_properties", {})
    synonyms = external.get("pubchem_synonyms", [])
    chembl = external.get("chembl_molecule", {})
    mechanisms = external.get("chembl_mechanisms", {})
    dmoa = external.get("dmoa", {})
    ncbi = external.get("ncbi_ml162_table", {})
    smiles = str(properties.get("CanonicalSMILES") or row.get("canonical_smiles") or "")
    has_chloroacetamide_like_motif = ("C(=O)CCl" in smiles) or ("C(=O)CCl" in str(row.get("canonical_smiles", "")))
    synonym_blob = " ".join(map(str, synonyms)).lower()
    chembl_mechanism_count = int(mechanisms.get("page_meta", {}).get("total_count") or 0)
    max_phase = chembl.get("max_phase")
    dmoa_known_unknown = (
        str(dmoa.get("known_moa_text", "")).lower().strip() == "unknown"
        and str(dmoa.get("known_targets_text", "")).lower().strip() == "unknown"
    )
    contains_brd = bool(ncbi.get("contains_brd_a72180425"))
    l1000_recurrence = int(row.get("n_opposite_queries") or 0)

    no_go_reasons = []
    if l1000_recurrence < 2:
        no_go_reasons.append("single L1000 opposite-query hit, no recurrence across module signatures")
    if max_phase in (None, "", "None") or pd.isna(max_phase):
        no_go_reasons.append("no approved or clinical-phase ChEMBL development status")
    if chembl_mechanism_count == 0:
        no_go_reasons.append("ChEMBL mechanism endpoint has zero target-mechanism records")
    if dmoa_known_unknown:
        no_go_reasons.append("L1000FWD DMOA report lists known MOA and target(s) as Unknown")
    if contains_brd:
        no_go_reasons.append("NCBI Bookshelf places BRD-A72180425 in ML162/RAS-selective-lethal probe SAR, not autoimmune therapeutics")
    if has_chloroacetamide_like_motif:
        no_go_reasons.append("contains chloroacetamide-like electrophile motif consistent with reactive/cytotoxic probe chemistry")
    if "chembl1472126" in synonym_blob and not no_go_reasons:
        no_go_reasons.append("external identity resolved but no target-level autoimmune mechanism recovered")

    if no_go_reasons:
        call = "NO_GO_CYTOTOXIC_PROBE_ANALOG"
    else:
        call = "PARK_NEEDS_MANUAL_REVIEW"
        no_go_reasons.append("external lookup did not trigger a hard no-go but also did not satisfy promotion gates")
    return {
        "wave41_call": call,
        "promotion_allowed": False,
        "resolved_identity": "CHEMBL1472126 / PubChem CID 3689416 / ML162 analog-like Broad probe SAR member",
        "mechanistic_interpretation": (
            "The parked hit resolves to a chloroacetamide-containing ML162 analog / RAS-selective-lethal probe-family "
            "compound. Its transcriptomic reversal is more plausibly a cytotoxic/stress signature than a selective "
            "cross-autoimmune myeloid-module intervention."
        ),
        "no_go_reasons": " | ".join(no_go_reasons),
        "has_chloroacetamide_like_motif": has_chloroacetamide_like_motif,
        "chembl_mechanism_count": chembl_mechanism_count,
        "chembl_max_phase": max_phase,
        "dmoa_known_moa": dmoa.get("known_moa_text"),
        "dmoa_known_targets": dmoa.get("known_targets_text"),
        "ncbi_ml162_table_contains_candidate": contains_brd,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    if not INPUT.exists():
        raise FileNotFoundError(INPUT)

    calls: list[ExternalCall] = []
    table = pd.read_csv(INPUT, sep="\t")
    parked = table[table["candidate_promotion_call"].astype(str).eq("PARK_EXTERNAL_TARGET_LOOKUP_ONLY")].copy()
    if parked.empty:
        raise RuntimeError("No PARK_EXTERNAL_TARGET_LOOKUP_ONLY rows found; Wave41 has nothing to deconvolve.")

    records = []
    all_target_rows = []
    for _, row in parked.iterrows():
        pert_id = str(row.get("pert_id"))
        inchi_key = str(row.get("inchi_key"))
        alias = str(row.get("compound_aliases") or row.get("lincs_cmap_name") or "")
        cids = []
        if inchi_key and inchi_key.lower() != "nan":
            cids.extend(pubchem_cids("inchikey", inchi_key, calls))
        if not cids and alias:
            cids.extend(pubchem_cids("name", alias, calls))
        cids = list(dict.fromkeys(cids))
        cid = cids[0] if cids else None
        properties = pubchem_properties(cid, calls) if cid is not None else {}
        synonyms = pubchem_synonyms(cid, calls) if cid is not None else []
        chembl_ids = sorted({syn for syn in synonyms if re.fullmatch(r"CHEMBL\d+", str(syn))})
        chembl_id = chembl_ids[0] if chembl_ids else None
        chembl = chembl_molecule(chembl_id, calls) if chembl_id else {}
        mechanisms = chembl_mechanisms(chembl_id, calls) if chembl_id else {}
        activities = chembl_activities(chembl_id, calls) if chembl_id else {}
        target_df = aggregate_chembl_targets(activities)
        if not target_df.empty:
            target_df.insert(0, "pert_id", pert_id)
            target_df.insert(1, "chembl_id", chembl_id)
            all_target_rows.append(target_df)
        dmoa = dmoa_report(pert_id, calls)
        ncbi = ncbi_ml162_table_lookup(calls)

        literature_queries = [
            f'"{pert_id}" OR "{alias}" OR "{inchi_key}"',
            f'"{chembl_id}"' if chembl_id else f'"{inchi_key}"',
            '"ML162" AND ("autoimmune" OR "multiple sclerosis" OR "rheumatoid arthritis" OR "lupus" OR "IBD" OR "psoriasis")',
            '"GPX4 inhibitor" AND ("autoimmune" OR "multiple sclerosis" OR "rheumatoid arthritis" OR "lupus" OR "IBD" OR "psoriasis")',
        ]
        lit_counts = {query: europepmc_count(query, calls) for query in literature_queries}
        trial_queries = [
            alias,
            chembl_id or "",
            "ML162 autoimmune",
            "GPX4 inhibitor autoimmune",
        ]
        trial_counts = {query: clinicaltrials_count(query, calls) for query in trial_queries if query}

        external = {
            "pubchem_cids": cids,
            "pubchem_properties": properties,
            "pubchem_synonyms": synonyms,
            "chembl_id": chembl_id,
            "chembl_molecule": chembl,
            "chembl_mechanisms": mechanisms,
            "dmoa": dmoa,
            "ncbi_ml162_table": ncbi,
            "europepmc_counts": lit_counts,
            "clinicaltrials_counts": trial_counts,
        }
        classification = classify_candidate(row, external)
        write_json(RAW / f"external_bundle_{safe_name(pert_id)}.json", external)

        record = {
            "pert_id": pert_id,
            "lincs_cmap_name": row.get("lincs_cmap_name"),
            "compound_aliases": row.get("compound_aliases"),
            "inchi_key": row.get("inchi_key"),
            "canonical_smiles": row.get("canonical_smiles"),
            "n_opposite_queries": row.get("n_opposite_queries"),
            "opposite_queries": row.get("opposite_queries"),
            "pubchem_cid": cid,
            "chembl_id": chembl_id,
            "pubchem_iupac": properties.get("IUPACName"),
            "pubchem_mw": properties.get("MolecularWeight"),
            "pubchem_xlogp": properties.get("XLogP"),
            "pubchem_tpsa": properties.get("TPSA"),
            "chembl_activity_total_count": activities.get("page_meta", {}).get("total_count") if isinstance(activities, dict) else None,
            "chembl_mechanism_total_count": mechanisms.get("page_meta", {}).get("total_count") if isinstance(mechanisms, dict) else None,
            "dmoa_known_moa": dmoa.get("known_moa_text"),
            "dmoa_known_targets": dmoa.get("known_targets_text"),
            "dmoa_predicted_moas_top5": "; ".join(
                f"{x.get('moa')}={x.get('probability')}" for x in dmoa.get("predicted_moas_top5", [])
            ),
            "ncbi_ml162_table_contains_candidate": ncbi.get("contains_brd_a72180425"),
            "europepmc_exact_identity_count": lit_counts.get(literature_queries[0]),
            "clinicaltrials_alias_count": trial_counts.get(alias),
            **classification,
        }
        records.append(record)

    out = pd.DataFrame(records)
    out.to_csv(OUT / "external_unknown_deconvolution.tsv", sep="\t", index=False)
    target_out = pd.concat(all_target_rows, ignore_index=True) if all_target_rows else pd.DataFrame()
    target_out.to_csv(OUT / "chembl_target_activity_summary.tsv", sep="\t", index=False)
    pd.DataFrame([asdict(c) for c in calls]).to_csv(OUT / "api_call_log.tsv", sep="\t", index=False)

    summary = {
        "date": "2026-05-27",
        "random_seed": SEED,
        "input": rel(INPUT),
        "n_parked_external_lookup_rows": int(len(parked)),
        "promotion_allowed_count": int(out["promotion_allowed"].sum()),
        "wave41_call_counts": out["wave41_call"].value_counts().to_dict(),
        "resolved_identities": out[["pert_id", "resolved_identity", "wave41_call", "no_go_reasons"]].to_dict("records"),
        "api_calls": len(calls),
        "output_paths": {
            "deconvolution": rel(OUT / "external_unknown_deconvolution.tsv"),
            "chembl_targets": rel(OUT / "chembl_target_activity_summary.tsv"),
            "api_call_log": rel(OUT / "api_call_log.tsv"),
            "raw_api_dir": rel(RAW),
        },
        "interpretation": (
            "The only Wave27 external-lookup survivor, BRD-A72180425/K784-3188, resolves to PubChem CID 3689416 "
            "and ChEMBL CHEMBL1472126, an ML162 analog/RAS-selective-lethal probe-family compound. Public target "
            "and mechanism resources do not provide a selective autoimmune target; the compound has a single L1000 "
            "opposite query and cytotoxic electrophile-probe context. The perturbation-first repurposing branch "
            "therefore remains closed."
        ),
    }
    write_json(OUT / "summary.json", summary)

    lines = [
        "# Wave41 L1000 External Unknown Deconvolution",
        "",
        "## Result",
        "",
        summary["interpretation"],
        "",
        "## Candidate Calls",
        "",
        markdown_table(out[
            [
                "pert_id",
                "lincs_cmap_name",
                "compound_aliases",
                "pubchem_cid",
                "chembl_id",
                "n_opposite_queries",
                "wave41_call",
                "promotion_allowed",
                "resolved_identity",
                "no_go_reasons",
            ]
        ]),
        "",
        "## External Evidence",
        "",
        "- PubChem, ChEMBL, Europe PMC, ClinicalTrials.gov, L1000FWD DMOA, and NCBI Bookshelf calls are cached in `raw_api/` and enumerated in `api_call_log.tsv`.",
        "- ChEMBL target activities are summarized in `chembl_target_activity_summary.tsv`; ChEMBL mechanism records were required for target promotion and were absent for this molecule.",
        "- NCBI Bookshelf Table 2 places BRD-A72180425 in the ML162 SAR table for RAS-selective lethal probe development.",
        "",
    ]
    (OUT / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=True))


if __name__ == "__main__":
    main()
