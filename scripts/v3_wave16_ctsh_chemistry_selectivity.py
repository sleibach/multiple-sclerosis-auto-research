#!/usr/bin/env python3
"""Wave16 CTSH chemistry/selectivity feasibility audit.

This script queries public APIs for target identity, structure availability,
curated pharmacology, and ChEMBL activity/selectivity data. It intentionally
does not perform docking or potency prediction.
"""

from __future__ import annotations

import json
import math
import statistics
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v3" / "wave16_ctsh_chemistry_selectivity"
RAW = OUT / "raw"

TARGETS = {
    "CTSH": {"chembl": "CHEMBL2225", "accession": "P09668", "name": "Pro-cathepsin H"},
    "CTSS": {"chembl": "CHEMBL2954", "accession": "P25774", "name": "Cathepsin S"},
    "CTSB": {"chembl": "CHEMBL4072", "accession": "P07858", "name": "Cathepsin B"},
    "CTSL": {"chembl": "CHEMBL3837", "accession": "P07711", "name": "Procathepsin L"},
    "CTSC": {"chembl": "CHEMBL2252", "accession": "P53634", "name": "Dipeptidyl peptidase 1/cathepsin C"},
    "CTSZ": {"chembl": "CHEMBL4160", "accession": "Q9UBR2", "name": "Cathepsin Z"},
}

ACTIVITY_TYPES = {"IC50", "Ki", "Kd"}
POTENCY_RELATIONS = {"=", "<", "<="}


def get_json(url: str, params: dict[str, Any] | None = None) -> Any:
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            response = requests.get(
                url,
                params=params,
                timeout=30,
                headers={"User-Agent": "ms-auto-research-wave16/1.0"},
            )
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"GET failed for {url}: {last_error}")


def post_json(url: str, payload: dict[str, Any]) -> Any:
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()
        except Exception as exc:
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"POST failed for {url}: {last_error}")


def chembl_target_summary() -> pd.DataFrame:
    rows = []
    for gene, meta in TARGETS.items():
        rows.append(
            {
                "gene": gene,
                "target_chembl_id": meta["chembl"],
                "pref_name": meta["name"],
                "target_type": "SINGLE PROTEIN",
                "organism": "Homo sapiens",
                "accession": meta["accession"],
            }
        )
    return pd.DataFrame(rows)


def chembl_activities(target_chembl_id: str, molecule_ids: list[str] | None = None) -> list[dict[str, Any]]:
    params = {
        "target_chembl_id": target_chembl_id,
        "standard_units": "nM",
        "standard_type__in": ",".join(sorted(ACTIVITY_TYPES)),
        "limit": 100,
        "offset": 0,
    }
    if molecule_ids:
        params["molecule_chembl_id__in"] = ",".join(sorted(set(molecule_ids)))
    activities: list[dict[str, Any]] = []
    while True:
        data = get_json("https://www.ebi.ac.uk/chembl/api/data/activity.json", params=params)
        activities.extend(data.get("activities", []))
        page = data.get("page_meta", {})
        if not page.get("next"):
            break
        params["offset"] = int(params["offset"]) + int(params["limit"])
        if params["offset"] > 10000:
            break
    return activities


def normalize_activities() -> pd.DataFrame:
    rows = []
    ctsh_meta = TARGETS["CTSH"]
    ctsh_activities = chembl_activities(ctsh_meta["chembl"])
    ctsh_molecules = sorted(
        {
            act.get("molecule_chembl_id")
            for act in ctsh_activities
            if act.get("molecule_chembl_id") and act.get("standard_value")
        }
    )
    activities_by_gene = {"CTSH": ctsh_activities}

    # Comparator targets have large public activity sets. For this wave the
    # selectivity question is whether known CTSH actives have comparator data,
    # so restrict comparator pulls to molecules with a CTSH measurement.
    for gene, meta in TARGETS.items():
        if gene == "CTSH":
            continue
        comparator_activities: list[dict[str, Any]] = []
        for start in range(0, len(ctsh_molecules), 50):
            batch = ctsh_molecules[start : start + 50]
            comparator_activities.extend(chembl_activities(meta["chembl"], molecule_ids=batch))
        activities_by_gene[gene] = comparator_activities

    for gene, activities in activities_by_gene.items():
        (RAW / "chembl").mkdir(parents=True, exist_ok=True)
        (RAW / "chembl" / f"{gene}_{TARGETS[gene]['chembl']}_activities.json").write_text(
            json.dumps(activities, indent=2, sort_keys=True)
        )
        print(f"{gene}: retained {len(activities)} ChEMBL records", flush=True)
        for act in activities:
            try:
                value = float(act.get("standard_value"))
            except (TypeError, ValueError):
                continue
            if not math.isfinite(value) or value <= 0:
                continue
            rows.append(
                {
                    "gene": gene,
                    "target_chembl_id": meta["chembl"],
                    "molecule_chembl_id": act.get("molecule_chembl_id"),
                    "canonical_smiles": act.get("canonical_smiles"),
                    "standard_type": act.get("standard_type"),
                    "standard_relation": act.get("standard_relation"),
                    "standard_value_nM": value,
                    "assay_type": act.get("assay_type"),
                    "document_chembl_id": act.get("document_chembl_id"),
                    "bao_label": act.get("bao_label"),
                }
            )
    return pd.DataFrame(rows)


def summarize_activities(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for gene in TARGETS:
        sub = df[df["gene"] == gene].copy()
        potent = sub[sub["standard_relation"].isin(POTENCY_RELATIONS)].copy()
        rows.append(
            {
                "gene": gene,
                "target_chembl_id": TARGETS[gene]["chembl"],
                "activity_records_nM": len(sub),
                "potency_records_relation_eq_lt_lte": len(potent),
                "unique_molecules_all": sub["molecule_chembl_id"].nunique(),
                "unique_molecules_potency": potent["molecule_chembl_id"].nunique(),
                "best_potency_nM": potent["standard_value_nM"].min() if len(potent) else None,
                "median_potency_nM": potent["standard_value_nM"].median() if len(potent) else None,
                "activity_type_counts": {
                    str(k): int(v) for k, v in sub["standard_type"].value_counts().items()
                },
            }
        )
    return pd.DataFrame(rows)


def molecule_details(molecule_ids: list[str]) -> dict[str, dict[str, Any]]:
    details = {}
    for mol in sorted(set(molecule_ids)):
        if not mol:
            continue
        try:
            data = get_json(f"https://www.ebi.ac.uk/chembl/api/data/molecule/{mol}.json")
            details[mol] = {
                "pref_name": data.get("pref_name"),
                "max_phase": data.get("max_phase"),
                "molecule_type": data.get("molecule_type"),
                "first_approval": data.get("first_approval"),
                "oral": data.get("oral"),
                "parenteral": data.get("parenteral"),
                "topical": data.get("topical"),
                "molecule_properties": data.get("molecule_properties") or {},
            }
        except Exception as exc:
            details[mol] = {"error": str(exc)}
    return details


def selectivity_table(df: pd.DataFrame) -> pd.DataFrame:
    potent = df[
        df["standard_relation"].isin(POTENCY_RELATIONS)
        & df["molecule_chembl_id"].notna()
        & df["standard_value_nM"].notna()
    ].copy()
    best = (
        potent.sort_values("standard_value_nM")
        .groupby(["molecule_chembl_id", "gene"], as_index=False)
        .agg(
            best_nM=("standard_value_nM", "min"),
            n_records=("standard_value_nM", "size"),
            activity_types=("standard_type", lambda x: ",".join(sorted(set(map(str, x))))),
            documents=("document_chembl_id", lambda x: ",".join(sorted(set(filter(None, map(str, x))))[:5])),
            smiles=("canonical_smiles", "first"),
        )
    )
    pivot = best.pivot(index="molecule_chembl_id", columns="gene", values="best_nM")
    ctsh = pivot[pivot["CTSH"].notna()].copy() if "CTSH" in pivot else pd.DataFrame()
    rows = []
    for mol, vals in ctsh.iterrows():
        row = {
            "molecule_chembl_id": mol,
            "CTSH_best_nM": vals.get("CTSH"),
        }
        comparator_ratios = []
        comparator_values = []
        for comp in ["CTSS", "CTSB", "CTSL", "CTSC", "CTSZ"]:
            val = vals.get(comp)
            row[f"{comp}_best_nM"] = val
            if pd.notna(val):
                ratio = float(val) / float(vals["CTSH"])
                row[f"{comp}_over_CTSH_ratio"] = ratio
                comparator_ratios.append(ratio)
                comparator_values.append(float(val))
            else:
                row[f"{comp}_over_CTSH_ratio"] = None
        row["n_comparators_assayed"] = len(comparator_ratios)
        row["min_comparator_over_CTSH_ratio"] = min(comparator_ratios) if comparator_ratios else None
        row["median_comparator_over_CTSH_ratio"] = (
            statistics.median(comparator_ratios) if comparator_ratios else None
        )
        row["has_10x_margin_over_all_assayed_comparators"] = (
            bool(comparator_ratios) and min(comparator_ratios) >= 10
        )
        row["has_100x_margin_over_all_assayed_comparators"] = (
            bool(comparator_ratios) and min(comparator_ratios) >= 100
        )
        sub = best[(best["molecule_chembl_id"] == mol) & (best["gene"] == "CTSH")]
        row["CTSH_activity_types"] = sub["activity_types"].iloc[0] if len(sub) else ""
        row["CTSH_documents"] = sub["documents"].iloc[0] if len(sub) else ""
        row["canonical_smiles"] = sub["smiles"].iloc[0] if len(sub) else ""
        rows.append(row)
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    details = molecule_details(out["molecule_chembl_id"].dropna().tolist())
    detail_rows = []
    for _, row in out.iterrows():
        detail = details.get(row["molecule_chembl_id"], {})
        props = detail.get("molecule_properties") or {}
        detail_rows.append(
            {
                **row.to_dict(),
                "pref_name": detail.get("pref_name"),
                "max_phase": detail.get("max_phase"),
                "molecule_type": detail.get("molecule_type"),
                "mw_freebase": props.get("mw_freebase"),
                "alogp": props.get("alogp"),
                "hba": props.get("hba"),
                "hbd": props.get("hbd"),
                "psa": props.get("psa"),
                "num_ro5_violations": props.get("num_ro5_violations"),
            }
        )
    ranked = pd.DataFrame(detail_rows).sort_values(
        ["has_10x_margin_over_all_assayed_comparators", "n_comparators_assayed", "CTSH_best_nM"],
        ascending=[False, False, True],
    )
    return ranked


def iuphar_interactions() -> pd.DataFrame:
    data = get_json("https://www.guidetopharmacology.org/services/targets/2349/interactions")
    (RAW / "iuphar_ctsh_interactions.json").write_text(json.dumps(data, indent=2, sort_keys=True))
    rows = []
    for item in data:
        rows.append(
            {
                "interaction_id": item.get("interactionId"),
                "target": item.get("targetName"),
                "target_species": item.get("targetSpecies"),
                "ligand_id": item.get("ligandId"),
                "ligand_name": item.get("ligandName"),
                "type": item.get("type"),
                "action": item.get("action"),
                "selectivity": item.get("selectivity"),
                "affinity": item.get("affinity"),
                "affinity_parameter": item.get("affinityParameter"),
                "original_affinity": item.get("originalAffinity"),
                "original_affinity_type": item.get("originalAffinityType"),
                "refs": "; ".join(
                    f"PMID:{ref.get('pmid')} {ref.get('title', '')}".strip()
                    for ref in item.get("refs", [])
                ),
            }
        )
    return pd.DataFrame(rows)


def uniprot_ctsh() -> dict[str, Any]:
    fields = ",".join(
        [
            "accession",
            "id",
            "protein_name",
            "gene_names",
            "cc_function",
            "cc_tissue_specificity",
            "ft_act_site",
            "ft_disulfid",
            "sequence",
        ]
    )
    data = get_json(
        "https://rest.uniprot.org/uniprotkb/search",
        {
            "query": "(gene_exact:CTSH) AND (organism_id:9606) AND (reviewed:true)",
            "format": "json",
            "fields": fields,
            "size": 1,
        },
    )
    raw = data.get("results", [{}])[0]
    (RAW / "uniprot_ctsh_raw.json").write_text(json.dumps(raw, indent=2, sort_keys=True))
    comments = raw.get("comments", [])
    function_text = " ".join(
        text.get("value", "")
        for comment in comments
        if comment.get("commentType") == "FUNCTION"
        for text in comment.get("texts", [])
    )
    tissue_text = " ".join(
        text.get("value", "")
        for comment in comments
        if comment.get("commentType") == "TISSUE SPECIFICITY"
        for text in comment.get("texts", [])
    )
    features = raw.get("features", [])
    return {
        "gene": "CTSH",
        "accession": raw.get("primaryAccession"),
        "uniprot_id": raw.get("uniProtkbId"),
        "protein": raw.get("proteinDescription", {})
        .get("recommendedName", {})
        .get("fullName", {})
        .get("value"),
        "sequence_length": raw.get("sequence", {}).get("length"),
        "function": function_text,
        "tissue_specificity": tissue_text,
        "features": [
            {
                "type": f.get("type"),
                "description": f.get("description"),
                "start": f.get("location", {}).get("start", {}).get("value"),
                "end": f.get("location", {}).get("end", {}).get("value"),
            }
            for f in features
            if f.get("type") in {"Active site", "Disulfide bond"}
        ],
    }


def alphafold_summary(accession: str) -> dict[str, Any]:
    url = f"https://alphafold.ebi.ac.uk/files/AF-{accession}-F1-model_v6.pdb"
    path = RAW / f"AF-{accession}-F1-model_v6.pdb"
    if not path.exists():
        response = requests.get(url, timeout=90)
        if response.status_code != 200:
            return {"accession": accession, "status": f"http_{response.status_code}", "url": url}
        path.write_bytes(response.content)
    plddts = []
    seen = set()
    for line in path.read_text(errors="ignore").splitlines():
        if not line.startswith("ATOM"):
            continue
        key = (line[21], line[22:26], line[26])
        if key in seen:
            continue
        seen.add(key)
        try:
            plddts.append(float(line[60:66]))
        except ValueError:
            pass
    return {
        "accession": accession,
        "status": "downloaded",
        "url": url,
        "path": str(path.relative_to(ROOT)),
        "n_residues_with_plddt": len(plddts),
        "mean_plddt": statistics.mean(plddts) if plddts else None,
        "median_plddt": statistics.median(plddts) if plddts else None,
        "low_confidence_fraction_lt70": sum(x < 70 for x in plddts) / len(plddts) if plddts else None,
    }


def pdb_summary(accession: str) -> pd.DataFrame:
    query = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession",
                "operator": "exact_match",
                "value": accession,
            },
        },
        "return_type": "entry",
        "request_options": {"paginate": {"start": 0, "rows": 100}},
    }
    data = post_json("https://search.rcsb.org/rcsbsearch/v2/query", query)
    ids = [item["identifier"] for item in data.get("result_set", [])]
    rows = []
    for pdb_id in ids:
        entry = get_json(f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}")
        rows.append(
            {
                "pdb_id": pdb_id,
                "title": entry.get("struct", {}).get("title"),
                "initial_release_date": entry.get("rcsb_accession_info", {}).get("initial_release_date"),
                "method": ";".join(ex.get("method", "") for ex in entry.get("exptl", [])),
                "resolution_A": ";".join(
                    map(str, entry.get("rcsb_entry_info", {}).get("resolution_combined") or [])
                ),
                "nonpolymer_entity_count": entry.get("rcsb_entry_info", {}).get("nonpolymer_entity_count"),
            }
        )
    return pd.DataFrame(rows).sort_values("pdb_id")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    targets = chembl_target_summary()
    targets.to_csv(OUT / "chembl_target_summary.tsv", sep="\t", index=False)

    activities = normalize_activities()
    activities.to_csv(OUT / "chembl_cathepsin_activities.tsv", sep="\t", index=False)

    activity_summary = summarize_activities(activities)
    activity_summary.to_csv(OUT / "chembl_activity_summary.tsv", sep="\t", index=False)

    selectivity = selectivity_table(activities)
    selectivity.to_csv(OUT / "chembl_ctsh_compound_selectivity.tsv", sep="\t", index=False)

    iuphar = iuphar_interactions()
    iuphar.to_csv(OUT / "iuphar_ctsh_interactions.tsv", sep="\t", index=False)

    uniprot = uniprot_ctsh()
    (OUT / "uniprot_ctsh_summary.json").write_text(json.dumps(uniprot, indent=2, sort_keys=True))

    alpha = alphafold_summary(TARGETS["CTSH"]["accession"])
    pdb = pdb_summary(TARGETS["CTSH"]["accession"])
    structures = pd.concat(
        [
            pd.DataFrame(
                [
                    {
                        "source": "AlphaFoldDB",
                        "id": alpha.get("accession"),
                        "title": "Predicted full-length CTSH model",
                        "method": "AlphaFold",
                        "resolution_A": "",
                        "mean_plddt": alpha.get("mean_plddt"),
                        "median_plddt": alpha.get("median_plddt"),
                        "low_confidence_fraction_lt70": alpha.get("low_confidence_fraction_lt70"),
                        "url": alpha.get("url"),
                    }
                ]
            ),
            pdb.assign(
                source="PDB",
                id=pdb["pdb_id"],
                mean_plddt="",
                median_plddt="",
                low_confidence_fraction_lt70="",
                url=pdb["pdb_id"].map(lambda x: f"https://www.rcsb.org/structure/{x}"),
            )[
                [
                    "source",
                    "id",
                    "title",
                    "method",
                    "resolution_A",
                    "mean_plddt",
                    "median_plddt",
                    "low_confidence_fraction_lt70",
                    "url",
                ]
            ],
        ],
        ignore_index=True,
    )
    structures.to_csv(OUT / "structure_summary.tsv", sep="\t", index=False)

    ctsh_rows = selectivity if not selectivity.empty else pd.DataFrame()
    assayed = ctsh_rows[ctsh_rows["n_comparators_assayed"] > 0] if not ctsh_rows.empty else pd.DataFrame()
    summary = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S %z"),
        "ctsh_chembl_target": TARGETS["CTSH"]["chembl"],
        "ctsh_activity_records_nM": int(activity_summary.loc[activity_summary["gene"] == "CTSH", "activity_records_nM"].iloc[0]),
        "ctsh_unique_molecules_potency": int(activity_summary.loc[activity_summary["gene"] == "CTSH", "unique_molecules_potency"].iloc[0]),
        "ctsh_best_potency_nM": float(activity_summary.loc[activity_summary["gene"] == "CTSH", "best_potency_nM"].iloc[0]),
        "ctsh_molecules_with_any_requested_comparator_assay": int(len(assayed)),
        "ctsh_molecules_with_10x_margin_over_all_assayed_comparators": int(
            assayed["has_10x_margin_over_all_assayed_comparators"].sum()
        )
        if len(assayed)
        else 0,
        "ctsh_molecules_with_100x_margin_over_all_assayed_comparators": int(
            assayed["has_100x_margin_over_all_assayed_comparators"].sum()
        )
        if len(assayed)
        else 0,
        "iuphar_curated_ctsh_inhibitor_interactions": int(len(iuphar)),
        "pdb_human_ctsh_entry_count": int(len(pdb)),
        "alphafold_ctsh_mean_plddt": alpha.get("mean_plddt"),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True))

    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
