#!/usr/bin/env python3
"""ACSL-family structural and pharmacology inventory.

The output is a feasibility screen, not docking and not a new structural
prediction. Structures come from AlphaFold DB metadata and sequences from
UniProt REST.
"""

from __future__ import annotations

import csv
import json
import math
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results_v2"
RAW = ROOT / "data" / "raw_v2"

GENES = ["ACSL1", "ACSL3", "ACSL4", "ACSL5", "ACSL6"]


def fetch_text(url: str, timeout: int = 45) -> str:
    req = Request(url, headers={"User-Agent": "ms-auto-research/0.1"})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def fetch_json(url: str, timeout: int = 45):
    return json.loads(fetch_text(url, timeout=timeout))


def uniprot_search(gene: str) -> dict[str, str]:
    query = f"gene_exact:{gene} AND organism_id:9606 AND reviewed:true"
    fields = "accession,id,gene_names,protein_name,length"
    url = f"https://rest.uniprot.org/uniprotkb/search?query={quote(query)}&fields={fields}&format=tsv&size=5"
    text = fetch_text(url)
    rows = list(csv.DictReader(text.splitlines(), delimiter="\t"))
    if not rows:
        # fallback because some UniProt gene_exact behavior changes
        query = f"gene:{gene} AND organism_id:9606 AND reviewed:true"
        url = f"https://rest.uniprot.org/uniprotkb/search?query={quote(query)}&fields={fields}&format=tsv&size=10"
        rows = list(csv.DictReader(fetch_text(url).splitlines(), delimiter="\t"))
    for row in rows:
        if gene in row.get("Gene Names", "").split():
            return row
    if rows:
        return rows[0]
    raise RuntimeError(f"No reviewed UniProt row found for {gene}")


def global_identity(seq_a: str, seq_b: str) -> dict[str, float]:
    """Needleman-Wunsch identity with linear gap, memory-light enough here."""
    a, b = seq_a, seq_b
    n, m = len(a), len(b)
    score = np.zeros((n + 1, m + 1), dtype=np.int16)
    pointer = np.zeros((n + 1, m + 1), dtype=np.uint8)
    gap = -1
    match = 2
    mismatch = -1
    for i in range(1, n + 1):
        score[i, 0] = score[i - 1, 0] + gap
        pointer[i, 0] = 1
    for j in range(1, m + 1):
        score[0, j] = score[0, j - 1] + gap
        pointer[0, j] = 2
    for i in range(1, n + 1):
        ai = a[i - 1]
        for j in range(1, m + 1):
            diag = score[i - 1, j - 1] + (match if ai == b[j - 1] else mismatch)
            up = score[i - 1, j] + gap
            left = score[i, j - 1] + gap
            if diag >= up and diag >= left:
                score[i, j] = diag
                pointer[i, j] = 0
            elif up >= left:
                score[i, j] = up
                pointer[i, j] = 1
            else:
                score[i, j] = left
                pointer[i, j] = 2
    i, j = n, m
    matches = 0
    aligned = 0
    gap_cols = 0
    while i > 0 or j > 0:
        p = pointer[i, j]
        if i > 0 and j > 0 and p == 0:
            matches += int(a[i - 1] == b[j - 1])
            aligned += 1
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or p == 1):
            aligned += 1
            gap_cols += 1
            i -= 1
        else:
            aligned += 1
            gap_cols += 1
            j -= 1
    return {
        "identity_fraction_aligned": matches / aligned if aligned else math.nan,
        "aligned_length": aligned,
        "gap_fraction": gap_cols / aligned if aligned else math.nan,
    }


def chembl_target_search(gene: str) -> list[dict[str, object]]:
    url = f"https://www.ebi.ac.uk/chembl/api/data/target/search.json?q={quote(gene)}"
    try:
        data = fetch_json(url)
        return data.get("targets", [])
    except Exception:
        return []


def chembl_activities(target_chembl_id: str, limit: int = 200) -> list[dict[str, object]]:
    url = (
        "https://www.ebi.ac.uk/chembl/api/data/activity.json?"
        f"target_chembl_id={quote(target_chembl_id)}&limit={limit}"
    )
    try:
        data = fetch_json(url)
        return data.get("activities", [])
    except Exception:
        return []


def summarize_activity(acts: list[dict[str, object]]) -> dict[str, object]:
    standards = []
    molecules = set()
    for a in acts:
        val = a.get("standard_value")
        units = a.get("standard_units")
        stype = a.get("standard_type")
        mol = a.get("molecule_chembl_id")
        if mol:
            molecules.add(mol)
        try:
            fval = float(val) if val is not None else math.nan
        except ValueError:
            fval = math.nan
        if units == "nM" and not math.isnan(fval):
            standards.append((stype, fval))
    potent = [v for _, v in standards if v <= 1000]
    return {
        "activity_records": len(acts),
        "unique_molecules": len(molecules),
        "nM_records": len(standards),
        "sub_uM_records": len(potent),
        "best_nM": min([v for _, v in standards], default=math.nan),
        "standard_types": ",".join(sorted({str(t) for t, _ in standards if t})),
    }


def main() -> None:
    OUT.mkdir(exist_ok=True)
    RAW.mkdir(exist_ok=True)
    rows = []
    seqs = {}
    for gene in GENES:
        up = uniprot_search(gene)
        acc = up["Entry"]
        af = fetch_json(f"https://alphafold.ebi.ac.uk/api/prediction/{acc}")[0]
        seq = af.get("uniprotSequence") or af.get("sequence")
        seqs[gene] = seq
        target_hits = chembl_target_search(gene)
        exact_hits = [t for t in target_hits if gene.lower() in (t.get("pref_name", "") + " " + " ".join(t.get("target_synonyms", []) if isinstance(t.get("target_synonyms"), list) else [])).lower()]
        best_target = exact_hits[0] if exact_hits else (target_hits[0] if target_hits else {})
        target_id = best_target.get("target_chembl_id")
        acts = chembl_activities(str(target_id)) if target_id else []
        act_summary = summarize_activity(acts)
        rows.append(
            {
                "gene": gene,
                "uniprot_accession": acc,
                "uniprot_entry": up["Entry Name"],
                "length_uniprot": int(up["Length"]),
                "alphafold_global_plddt": af.get("globalMetricValue"),
                "alphafold_fraction_plddt_confident": af.get("fractionPlddtConfident"),
                "alphafold_fraction_plddt_very_high": af.get("fractionPlddtVeryHigh"),
                "alphafold_pdb_url": af.get("pdbUrl"),
                "chembl_target_id": target_id,
                "chembl_pref_name": best_target.get("pref_name"),
                **act_summary,
            }
        )
        time.sleep(0.2)

    fam = pd.DataFrame(rows)
    fam.to_csv(OUT / "acsl_family_structure_pharmacology.tsv", sep="\t", index=False)

    id_rows = []
    for g in GENES:
        if g == "ACSL1":
            continue
        ident = global_identity(seqs["ACSL1"], seqs[g])
        id_rows.append({"gene_a": "ACSL1", "gene_b": g, **ident})
    identities = pd.DataFrame(id_rows)
    identities.to_csv(OUT / "acsl1_family_sequence_identity.tsv", sep="\t", index=False)

    summary = {
        "genes": GENES,
        "interpretation": "High ACSL-family sequence similarity or shared ligand activity is a selectivity risk; AlphaFold confidence supports model use but not ligandability.",
        "mean_acsl1_to_family_identity_fraction_aligned": float(identities["identity_fraction_aligned"].mean()),
        "max_acsl1_to_family_identity_fraction_aligned": float(identities["identity_fraction_aligned"].max()),
        "chembl_activity_records_acsl1": int(fam.loc[fam["gene"] == "ACSL1", "activity_records"].iloc[0]),
        "chembl_sub_uM_records_acsl1": int(fam.loc[fam["gene"] == "ACSL1", "sub_uM_records"].iloc[0]),
        "caveat": "ChEMBL target search can miss literature-only probes and does not establish CNS penetration.",
    }
    (OUT / "acsl_family_inventory_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(fam.to_string(index=False))
    print(identities.to_string(index=False))


if __name__ == "__main__":
    main()
