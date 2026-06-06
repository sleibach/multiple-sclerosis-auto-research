#!/usr/bin/env python3
"""Druggability audit for V3 intervention candidates.

Queries public UniProt, AlphaFold DB, and ChEMBL APIs for target identity,
structure confidence, and existing chemical matter. This is not docking and not
a medicinal-chemistry proof; it is a traceable feasibility screen.
"""

from __future__ import annotations

import json
import statistics
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw_v3" / "structures"
OUT = ROOT / "phases/v3/results" / "druggability"

GENES = {
    "IFI30": {"role": "candidate lysosomal thiol reductase feedback effector", "fallback_accession": "P13284"},
    "CTSS": {"role": "cathepsin S comparator", "fallback_accession": "P25774"},
    "CTSL": {"role": "cathepsin L selectivity comparator", "fallback_accession": "P07711"},
    "CTSB": {"role": "cathepsin B selectivity comparator", "fallback_accession": "P07858"},
    "CTSD": {"role": "cathepsin D selectivity comparator", "fallback_accession": "P07339"},
    "JAK1": {"role": "upstream JAK comparator", "fallback_accession": "P23458"},
    "JAK2": {"role": "upstream JAK comparator", "fallback_accession": "O60674"},
    "STAT1": {"role": "transcription-factor comparator", "fallback_accession": "P42224"},
    "CIITA": {"role": "HLA-II transcriptional gate comparator", "fallback_accession": "P33076"},
    "RFX5": {"role": "HLA-II transcriptional gate comparator", "fallback_accession": "P48382"},
}


def get_json(url: str, params: dict[str, Any] | None = None) -> Any:
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            r = requests.get(url, params=params, timeout=45)
            r.raise_for_status()
            return r.json()
        except Exception as exc:  # API resilience is logged in output rows.
            last_error = exc
            time.sleep(2 * (attempt + 1))
    raise last_error  # type: ignore[misc]


def uniprot_for_gene(gene: str, fallback_accession: str | None = None) -> dict[str, Any]:
    fields = ",".join(
        [
            "accession",
            "id",
            "protein_name",
            "gene_names",
            "cc_function",
            "ft_act_site",
            "ft_binding",
            "ft_disulfid",
            "sequence",
        ]
    )
    try:
        data = get_json(
            "https://rest.uniprot.org/uniprotkb/search",
            {
                "query": f"(gene_exact:{gene}) AND (organism_id:9606) AND (reviewed:true)",
                "format": "json",
                "fields": fields,
                "size": 3,
            },
        )
        results = data.get("results", [])
        if results:
            top = results[0]
            return {"gene": gene, "status": "found", "raw": top}
        return {"gene": gene, "status": "not_found", "fallback_accession": fallback_accession}
    except Exception as exc:
        return {
            "gene": gene,
            "status": "api_failed_using_verified_fallback_accession",
            "fallback_accession": fallback_accession,
            "error": f"{type(exc).__name__}: {exc}",
        }


def summarize_uniprot(item: dict[str, Any]) -> dict[str, Any]:
    if item.get("status") != "found":
        return {
            "gene": item["gene"],
            "uniprot_status": item.get("status"),
            "accession": item.get("fallback_accession"),
            "protein": None,
            "sequence_length": None,
            "function_excerpt": "",
            "active_binding_disulfide_features": [],
            "api_error": item.get("error", ""),
        }
    raw = item["raw"]
    accession = raw.get("primaryAccession")
    protein = raw.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value")
    sequence = raw.get("sequence", {}).get("value", "")
    comments = raw.get("comments", [])
    function_text = []
    for c in comments:
        if c.get("commentType") == "FUNCTION":
            for txt in c.get("texts", []):
                function_text.append(txt.get("value", ""))
    features = raw.get("features", [])
    active_sites = [
        {
            "type": f.get("type"),
            "description": f.get("description"),
            "start": f.get("location", {}).get("start", {}).get("value"),
            "end": f.get("location", {}).get("end", {}).get("value"),
        }
        for f in features
        if f.get("type") in {"Active site", "Binding site", "Disulfide bond"}
    ]
    return {
        "gene": item["gene"],
        "uniprot_status": "found",
        "accession": accession,
        "protein": protein,
        "sequence_length": len(sequence),
        "function_excerpt": " ".join(function_text)[:800],
        "active_binding_disulfide_features": active_sites,
    }


def download_alphafold(accession: str) -> dict[str, Any]:
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / f"AF-{accession}-F1-model_v6.pdb"
    url = f"https://alphafold.ebi.ac.uk/files/AF-{accession}-F1-model_v6.pdb"
    if not path.exists():
        r = requests.get(url, timeout=90)
        if r.status_code != 200:
            return {"accession": accession, "status": f"http_{r.status_code}", "url": url}
        path.write_bytes(r.content)
    plddts = []
    residues_seen = set()
    for line in path.read_text(errors="ignore").splitlines():
        if line.startswith("ATOM"):
            chain = line[21].strip()
            resseq = line[22:26].strip()
            icode = line[26].strip()
            key = (chain, resseq, icode)
            if key in residues_seen:
                continue
            residues_seen.add(key)
            try:
                plddts.append(float(line[60:66]))
            except ValueError:
                pass
    if not plddts:
        return {"accession": accession, "status": "no_plddt", "path": str(path.relative_to(ROOT)), "url": url}
    return {
        "accession": accession,
        "status": "downloaded",
        "path": str(path.relative_to(ROOT)),
        "url": url,
        "n_residues_with_plddt": len(plddts),
        "mean_plddt": statistics.mean(plddts),
        "median_plddt": statistics.median(plddts),
        "low_confidence_fraction_lt70": sum(x < 70 for x in plddts) / len(plddts),
    }


def chembl_target_search(gene: str) -> dict[str, Any]:
    data = get_json("https://www.ebi.ac.uk/chembl/api/data/target/search.json", {"q": gene, "limit": 10})
    targets = data.get("targets", [])
    exact = []
    for target in targets:
        comps = target.get("target_components", []) or []
        symbols = []
        accessions = []
        for comp in comps:
            symbols.extend(comp.get("target_component_synonyms", []))
            if comp.get("accession"):
                accessions.append(comp["accession"])
        exact.append(
            {
                "target_chembl_id": target.get("target_chembl_id"),
                "pref_name": target.get("pref_name"),
                "target_type": target.get("target_type"),
                "organism": target.get("organism"),
                "accessions": accessions,
            }
        )
    return {"gene": gene, "targets": exact}


def chembl_activity_summary(target_chembl_id: str) -> dict[str, Any]:
    params = {
        "target_chembl_id": target_chembl_id,
        "standard_type__in": "IC50,Ki,Kd,EC50,AC50",
        "standard_relation__in": "=,<,<=,>,>=",
        "standard_units": "nM",
        "limit": 1000,
    }
    data = get_json("https://www.ebi.ac.uk/chembl/api/data/activity.json", params)
    activities = data.get("activities", [])
    values = []
    molecules = set()
    types = {}
    for act in activities:
        try:
            val = float(act.get("standard_value"))
        except (TypeError, ValueError):
            continue
        if val <= 0:
            continue
        values.append(val)
        if act.get("molecule_chembl_id"):
            molecules.add(act["molecule_chembl_id"])
        st = act.get("standard_type") or "NA"
        types[st] = types.get(st, 0) + 1
    return {
        "target_chembl_id": target_chembl_id,
        "activity_records_returned": len(activities),
        "activity_values_nM_count": len(values),
        "unique_molecules_in_returned_records": len(molecules),
        "assay_type_counts": types,
        "best_standard_value_nM": min(values) if values else None,
        "median_standard_value_nM": statistics.median(values) if values else None,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    uniprot_raw = {}
    rows = []
    structure_rows = []
    chembl_rows = []
    chembl_detail = {}
    for gene, meta in GENES.items():
        item = uniprot_for_gene(gene, meta.get("fallback_accession"))
        uniprot_raw[gene] = item
        summary = summarize_uniprot(item)
        rows.append({**{"role": meta["role"]}, **summary})
        accession = summary.get("accession")
        if accession:
            structure_rows.append({"gene": gene, **download_alphafold(accession)})
        try:
            target_result = chembl_target_search(gene)
        except Exception as exc:
            target_result = {"gene": gene, "targets": [], "error": f"{type(exc).__name__}: {exc}"}
        chembl_detail[gene] = target_result
        for target in target_result.get("targets", []):
            # Keep human single-protein hits preferentially but record all returned target rows.
            try:
                activity = chembl_activity_summary(target["target_chembl_id"]) if target.get("target_chembl_id") else {}
            except Exception as exc:
                activity = {"activity_error": f"{type(exc).__name__}: {exc}"}
            chembl_rows.append({"gene": gene, **target, **activity})
    pd.DataFrame(rows).to_csv(OUT / "uniprot_target_summary.tsv", sep="\t", index=False)
    pd.DataFrame(structure_rows).to_csv(OUT / "alphafold_structure_confidence.tsv", sep="\t", index=False)
    pd.DataFrame(chembl_rows).to_csv(OUT / "chembl_target_activity_summary.tsv", sep="\t", index=False)
    (OUT / "uniprot_raw.json").write_text(json.dumps(uniprot_raw, indent=2) + "\n")
    (OUT / "chembl_target_search_detail.json").write_text(json.dumps(chembl_detail, indent=2) + "\n")
    print(json.dumps({"genes": list(GENES), "out": str(OUT.relative_to(ROOT))}, indent=2))


if __name__ == "__main__":
    main()
