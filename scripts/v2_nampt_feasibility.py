#!/usr/bin/env python3
"""NAMPT successor-target feasibility and prior-art inventory."""

from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v2/results"


def fetch_json(url: str, timeout: int = 45):
    req = Request(url, headers={"User-Agent": "ms-auto-research/0.1"})
    with urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def fetch_text(url: str, timeout: int = 45) -> str:
    req = Request(url, headers={"User-Agent": "ms-auto-research/0.1"})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def chembl_search_target(q: str):
    return fetch_json(f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={quote(q)}").get("targets", [])


def chembl_activities(target_id: str, limit: int = 1000):
    return fetch_json(
        f"https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id={quote(target_id)}&limit={limit}"
    ).get("activities", [])


def clinical_trials(term: str):
    try:
        data = fetch_json(f"https://clinicaltrials.gov/api/v2/studies?query.term={quote(term)}&pageSize=100")
        rows = []
        for st in data.get("studies", []):
            protocol = st.get("protocolSection", {})
            ident = protocol.get("identificationModule", {})
            status = protocol.get("statusModule", {})
            cond = protocol.get("conditionsModule", {})
            design = protocol.get("designModule", {})
            rows.append(
                {
                    "query": term,
                    "nct_id": ident.get("nctId"),
                    "brief_title": ident.get("briefTitle"),
                    "overall_status": status.get("overallStatus"),
                    "conditions": "; ".join(cond.get("conditions", []) or []),
                    "phases": "; ".join(design.get("phases", []) or []),
                }
            )
        return rows
    except Exception as exc:
        return [{"query": term, "error": str(exc)}]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    # UniProt reviewed NAMPT.
    up = fetch_text(
        "https://rest.uniprot.org/uniprotkb/search?"
        "query=gene_exact%3ANAMPT%20AND%20organism_id%3A9606%20AND%20reviewed%3Atrue"
        "&fields=accession,id,gene_names,protein_name,length&format=tsv&size=5"
    )
    up_rows = [line.split("\t") for line in up.splitlines()]
    accession = up_rows[1][0]
    af = fetch_json(f"https://alphafold.ebi.ac.uk/api/prediction/{accession}")[0]

    target_hits = chembl_search_target("NAMPT")
    target = target_hits[0] if target_hits else {}
    target_id = target.get("target_chembl_id")
    acts = chembl_activities(target_id) if target_id else []
    act_rows = []
    for a in acts:
        val = a.get("standard_value")
        try:
            fval = float(val) if val is not None else None
        except ValueError:
            fval = None
        act_rows.append(
            {
                "molecule_chembl_id": a.get("molecule_chembl_id"),
                "standard_type": a.get("standard_type"),
                "standard_value": fval,
                "standard_units": a.get("standard_units"),
                "assay_description": a.get("assay_description"),
            }
        )
    activities = pd.DataFrame(act_rows)
    activities.to_csv(OUT / "nampt_chembl_activities.tsv", sep="\t", index=False)

    trial_rows = []
    for term in ["NAMPT", "FK866", "APO866", "daporinad", "visfatin"]:
        trial_rows.extend(clinical_trials(term))
        time.sleep(0.2)
    trials = pd.DataFrame(trial_rows)
    trials.to_csv(OUT / "nampt_clinicaltrials.tsv", sep="\t", index=False)

    nM = activities[(activities["standard_units"] == "nM") & activities["standard_value"].notna()]
    sub_um = nM[nM["standard_value"] <= 1000]
    autoimmune_trials = trials[
        trials["conditions"].fillna("").str.contains(
            "multiple sclerosis|rheumatoid|psoriasis|Crohn|ulcerative|lupus|autoimmune", case=False, regex=True
        )
    ]
    summary = {
        "uniprot_accession": accession,
        "alphafold_global_plddt": af.get("globalMetricValue"),
        "alphafold_pdb_url": af.get("pdbUrl"),
        "chembl_target_id": target_id,
        "chembl_pref_name": target.get("pref_name"),
        "chembl_activity_records": int(len(activities)),
        "chembl_unique_molecules": int(activities["molecule_chembl_id"].nunique()) if not activities.empty else 0,
        "chembl_sub_uM_records": int(len(sub_um)),
        "best_nM": float(nM["standard_value"].min()) if not nM.empty else None,
        "clinical_trials_total_records": int(len(trials)),
        "clinical_trials_autoimmune_records": int(len(autoimmune_trials)),
        "interpretation": "NAMPT is chemically tractable but heavily prior-arted; absence of autoimmune trials would not imply novelty because preclinical autoimmune literature is extensive.",
    }
    (OUT / "nampt_feasibility_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(trials[["query", "nct_id", "brief_title", "conditions", "phases", "overall_status"]].head(20).to_string(index=False))


if __name__ == "__main__":
    main()
