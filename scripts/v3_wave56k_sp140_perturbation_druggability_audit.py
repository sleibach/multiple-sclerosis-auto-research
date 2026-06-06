#!/usr/bin/env python3
"""Wave56-K SP140 perturbation/druggability support audit.

This script keeps the subagent report traceable. It uses public supplemental
tables from Ghiboub et al. 2022 (BMC Biology, DOI 10.1186/s12915-022-01380-6)
to test whether SP140 perturbation or SP140 inhibition suppresses V3
lipid/lysosomal inflammatory myeloid readouts. XLSX parsing is implemented
with the Python standard library because openpyxl is not pinned in the V3 env.
"""

from __future__ import annotations

import io
import json
import re
import statistics
import zipfile
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

import pandas as pd
import requests
from scipy.stats import fisher_exact
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave56k_sp140_perturbation_druggability"
RAW = OUT / "raw_api"

ARTICLE_DOI = "10.1186/s12915-022-01380-6"
ARTICLE_URL = f"https://link.springer.com/article/{ARTICLE_DOI}"
SUPP_BASE = (
    "https://static-content.springer.com/esm/art%3A10.1186%2Fs12915-022-01380-6/"
    "MediaObjects/12915_2022_1380_MOESM{}_ESM.xlsx"
)
NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "rel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

MODULES = {
    "ifn_apc": ["STAT1", "IRF1", "CXCL10", "GBP1", "CD74", "IFI30", "HLA-DRA", "HLA-DRB1"],
    "hla_ii_apc": ["CD74", "HLA-DRA", "HLA-DRB1", "HLA-DPA1", "HLA-DPB1", "HLA-DMA", "HLA-DMB"],
    "lysosomal_apc": ["IFI30", "CTSS", "CTSB", "CTSD", "LAMP1", "LAMP2", "LAMP3"],
    "lipid_loader_repair": [
        "ACSL1",
        "APOE",
        "GPNMB",
        "LPL",
        "PLIN2",
        "CD36",
        "LIPA",
        "FABP5",
        "TREM2",
        "MSR1",
        "MERTK",
        "SPP1",
    ],
    "inflammatory_nfkb": ["TNF", "IL1B", "IL6", "CXCL8", "CCL2", "NFKBIA", "TNFAIP3", "NFKBIZ", "PTGS2"],
    "topoisomerase_axis": ["TOP1", "TOP2A", "TOP2B", "HMGB1", "HMGB2", "XRCC5", "XRCC6"],
}

INTEREST_GENES = sorted(
    {gene for genes in MODULES.values() for gene in genes}
    | {"SP140", "SP110", "SP100", "SP140L", "TRIM22", "TRIM25", "IL10", "IL12A", "IL12B", "JAK2", "CEACAM1"}
)

CONTRASTS = {
    2: "SP140_siRNA_M1_vs_scrambled",
    3: "SP140_siRNA_M1_4h_LPS_vs_scrambled",
    5: "GSK761_M1_vs_DMSO",
    6: "GSK761_M1_4h_LPS_vs_DMSO",
    7: "GSK761_M1_8h_LPS_vs_DMSO",
}


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=True) + "\n", encoding="utf-8")


def get_json(url: str, path: Path) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    response = requests.get(url, timeout=60, headers={"User-Agent": "ms-auto-research-wave56k/1.0"})
    response.raise_for_status()
    payload = response.json()
    write_json(path, payload)
    return payload


def column_index(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)", cell_ref)
    if not match:
        return 0
    value = 0
    for char in match.group(1):
        value = value * 26 + ord(char) - 64
    return value - 1


def read_first_xlsx_sheet(url: str) -> pd.DataFrame:
    response = requests.get(url, timeout=90, headers={"User-Agent": "ms-auto-research-wave56k/1.0"})
    response.raise_for_status()
    archive = zipfile.ZipFile(io.BytesIO(response.content))

    shared_strings: list[str] = []
    if "xl/sharedStrings.xml" in archive.namelist():
        root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        for item in root.findall("main:si", NS):
            shared_strings.append("".join((text.text or "") for text in item.iter(f"{{{NS['main']}}}t")))

    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    rid_to_target = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
    sheet = workbook.find("main:sheets", NS)[0]
    target = rid_to_target[sheet.attrib[f"{{{NS['rel']}}}id"]]
    sheet_path = "xl/" + target.lstrip("/")
    root = ET.fromstring(archive.read(sheet_path))

    rows: list[list[str]] = []
    for row in root.findall(".//main:sheetData/main:row", NS):
        values: list[str] = []
        for cell in row.findall("main:c", NS):
            idx = column_index(cell.attrib["r"])
            while len(values) <= idx:
                values.append("")
            value_tag = cell.find("main:v", NS)
            value = "" if value_tag is None else (value_tag.text or "")
            if cell.attrib.get("t") == "s" and value:
                value = shared_strings[int(value)]
            values[idx] = value
        if any(value != "" for value in values):
            rows.append(values)

    header = rows[0]
    width = len(header)
    data_rows = [row + [""] * (width - len(row)) for row in rows[1:]]
    return pd.DataFrame(data_rows, columns=header)


def normalize_contrast(frame: pd.DataFrame) -> pd.DataFrame:
    gene_col = "hgnc_symbol" if "hgnc_symbol" in frame.columns else "ID"
    lfc_col = "log2FoldChange" if "log2FoldChange" in frame.columns else "logFC"
    p_col = "pvalue" if "pvalue" in frame.columns else "P.Value"

    normalized = frame.copy()
    normalized["gene"] = normalized[gene_col].astype(str).str.upper()
    normalized["lfc"] = pd.to_numeric(normalized[lfc_col], errors="coerce")
    normalized["p"] = pd.to_numeric(normalized[p_col], errors="coerce")
    normalized = normalized[normalized["gene"].ne("") & normalized["lfc"].notna() & normalized["p"].notna()].copy()
    normalized["padj_calc"] = multipletests(normalized["p"].fillna(1), method="fdr_bh")[1]
    return normalized


def summarize_modules(label: str, frame: pd.DataFrame, source_url: str) -> list[dict[str, Any]]:
    universe = set(frame["gene"])
    all_down = set(frame[(frame["padj_calc"] < 0.05) & (frame["lfc"] < 0)]["gene"])
    all_up = set(frame[(frame["padj_calc"] < 0.05) & (frame["lfc"] > 0)]["gene"])
    rows: list[dict[str, Any]] = []
    for module, genes in MODULES.items():
        sub = frame[frame["gene"].isin(genes)].copy()
        if sub.empty:
            rows.append(
                {
                    "contrast": label,
                    "module": module,
                    "source_url": source_url,
                    "present_gene_count": 0,
                    "median_log2fc": None,
                    "sig_down_count": 0,
                    "sig_up_count": 0,
                    "sig_down_genes": "",
                    "sig_up_genes": "",
                    "fisher_down_p": None,
                    "fisher_up_p": None,
                }
            )
            continue
        module_genes = set(sub["gene"])
        down_hits = module_genes & all_down
        up_hits = module_genes & all_up
        down_table = [[len(down_hits), len(module_genes - down_hits)], [len(all_down - module_genes), len(universe - module_genes - (all_down - module_genes))]]
        up_table = [[len(up_hits), len(module_genes - up_hits)], [len(all_up - module_genes), len(universe - module_genes - (all_up - module_genes))]]
        rows.append(
            {
                "contrast": label,
                "module": module,
                "source_url": source_url,
                "present_gene_count": len(sub),
                "median_log2fc": float(sub["lfc"].median()),
                "sig_down_count": len(down_hits),
                "sig_up_count": len(up_hits),
                "sig_down_genes": ",".join(sorted(down_hits)),
                "sig_up_genes": ",".join(sorted(up_hits)),
                "fisher_down_p": float(fisher_exact(down_table, alternative="greater")[1]),
                "fisher_up_p": float(fisher_exact(up_table, alternative="greater")[1]),
            }
        )
    return rows


def extract_interest_rows(label: str, frame: pd.DataFrame, source_url: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, row in frame[frame["gene"].isin(INTEREST_GENES)].sort_values("gene").iterrows():
        rows.append(
            {
                "contrast": label,
                "gene": row["gene"],
                "log2fc": float(row["lfc"]),
                "p": float(row["p"]),
                "padj_calc": float(row["padj_calc"]),
                "source_url": source_url,
            }
        )
    return rows


def structure_summary() -> pd.DataFrame:
    uniprot = get_json("https://rest.uniprot.org/uniprotkb/Q13342.json", RAW / "uniprot_Q13342_SP140.json")
    features = []
    for feature in uniprot.get("features", []):
        if feature.get("type") in {"Domain", "Zinc finger", "Region", "Motif", "Compositional bias"}:
            features.append(
                {
                    "source": "UniProt",
                    "accession": "Q13342",
                    "feature_type": feature.get("type"),
                    "description": feature.get("description"),
                    "start": (feature.get("location") or {}).get("start", {}).get("value"),
                    "end": (feature.get("location") or {}).get("end", {}).get("value"),
                    "url": "https://www.uniprot.org/uniprotkb/Q13342/entry",
                }
            )

    pdb_text = requests.get("https://alphafold.ebi.ac.uk/files/AF-Q13342-F1-model_v6.pdb", timeout=60).text
    residue_scores: dict[int, float] = {}
    for line in pdb_text.splitlines():
        if not line.startswith("ATOM"):
            continue
        try:
            residue = int(line[22:26])
            plddt = float(line[60:66])
        except ValueError:
            continue
        residue_scores.setdefault(residue, plddt)
    regions = {
        "full": (1, 867),
        "HSR": (22, 138),
        "disordered_260_341": (260, 341),
        "disordered_365_432": (365, 432),
        "disordered_486_580": (486, 580),
        "SAND": (580, 661),
        "PHD_type": (690, 736),
        "Bromo": (754, 857),
        "PHD_Bromo_construct": (687, 867),
    }
    for region, (start, end) in regions.items():
        values = [score for residue, score in residue_scores.items() if start <= residue <= end]
        if values:
            features.append(
                {
                    "source": "AlphaFold",
                    "accession": "AF-Q13342-F1-v6",
                    "feature_type": "pLDDT_region",
                    "description": region,
                    "start": start,
                    "end": end,
                    "mean_pLDDT": statistics.mean(values),
                    "median_pLDDT": statistics.median(values),
                    "frac_ge_70": sum(score >= 70 for score in values) / len(values),
                    "url": "https://alphafold.ebi.ac.uk/entry/Q13342",
                }
            )
    return pd.DataFrame(features)


def public_endpoint_summary() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    chembl_target = get_json(
        "https://www.ebi.ac.uk/chembl/api/data/target/search.json?q=SP140&limit=20",
        RAW / "chembl_target_SP140.json",
    )
    activities = get_json(
        "https://www.ebi.ac.uk/chembl/api/data/activity.json?target_chembl_id=CHEMBL3108643&limit=100",
        RAW / "chembl_activity_CHEMBL3108643_unfiltered.json",
    )
    rows.append(
        {
            "endpoint": "ChEMBL SP140 target/activity",
            "identifier": "CHEMBL3108643",
            "count_or_value": (activities.get("page_meta") or {}).get("total_count"),
            "interpretation": "activity rows are thermal-shift Delta Tm records; no nM potency/pChEMBL series found in this endpoint",
            "url": "https://www.ebi.ac.uk/chembl/target_report_card/CHEMBL3108643/",
        }
    )
    rows.append(
        {
            "endpoint": "ChEMBL SP140 target search",
            "identifier": "SP140",
            "count_or_value": (chembl_target.get("page_meta") or {}).get("total_count"),
            "interpretation": "SP140 single-protein target exists, but GSK761 was not found by ChEMBL molecule-name search",
            "url": "https://www.ebi.ac.uk/chembl/",
        }
    )
    pubchem = get_json(
        "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/168007146/property/MolecularFormula,MolecularWeight,CanonicalSMILES,XLogP,TPSA,HBondDonorCount,HBondAcceptorCount,RotatableBondCount/JSON",
        RAW / "pubchem_GSK761_CID168007146_properties.json",
    )
    prop = ((pubchem.get("PropertyTable") or {}).get("Properties") or [{}])[0]
    rows.append(
        {
            "endpoint": "PubChem GSK761",
            "identifier": "CID 168007146",
            "count_or_value": f"MW={prop.get('MolecularWeight')}; XLogP={prop.get('XLogP')}; TPSA={prop.get('TPSA')}; rotB={prop.get('RotatableBondCount')}",
            "interpretation": "large, lipophilic tool compound; CNS exposure is not supported by these properties alone",
            "url": "https://pubchem.ncbi.nlm.nih.gov/compound/168007146",
        }
    )
    for query in ["SP140 inhibitor", "SP140 autoimmune therapeutic target", "SP140 degrader"]:
        data = get_json(
            f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={quote_plus(query)}&format=json&pageSize=5&resultType=lite",
            RAW / f"europepmc_{query.replace(' ', '_')}.json",
        )
        rows.append(
            {
                "endpoint": "Europe PMC",
                "identifier": query,
                "count_or_value": data.get("hitCount"),
                "interpretation": "literature saturation / prior-art screen; titles require manual relevance filtering",
                "url": f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={quote_plus(query)}&format=json&pageSize=5&resultType=lite",
            }
        )
    clinical = get_json(
        "https://clinicaltrials.gov/api/v2/studies?query.term=SP140+autoimmune&pageSize=10&format=json",
        RAW / "clinicaltrials_SP140_autoimmune.json",
    )
    rows.append(
        {
            "endpoint": "ClinicalTrials.gov",
            "identifier": "SP140 autoimmune",
            "count_or_value": clinical.get("totalCount", len(clinical.get("studies", []))),
            "interpretation": "no SP140 autoimmune trial surfaced by this query",
            "url": "https://clinicaltrials.gov/search?term=SP140%20autoimmune",
        }
    )
    return pd.DataFrame(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)

    module_rows: list[dict[str, Any]] = []
    interest_rows: list[dict[str, Any]] = []
    for supp_id, label in CONTRASTS.items():
        source_url = SUPP_BASE.format(supp_id)
        frame = normalize_contrast(read_first_xlsx_sheet(source_url))
        module_rows.extend(summarize_modules(label, frame, source_url))
        interest_rows.extend(extract_interest_rows(label, frame, source_url))

    module_summary = pd.DataFrame(module_rows)
    interest = pd.DataFrame(interest_rows)
    structures = structure_summary()
    endpoints = public_endpoint_summary()

    module_summary.to_csv(OUT / "gsk761_sp140_supplement_module_summary.tsv", sep="\t", index=False)
    interest.to_csv(OUT / "gsk761_sp140_interest_gene_effects.tsv", sep="\t", index=False)
    structures.to_csv(OUT / "sp140_domain_structure_summary.tsv", sep="\t", index=False)
    endpoints.to_csv(OUT / "sp140_public_endpoint_summary.tsv", sep="\t", index=False)
    write_json(
        OUT / "summary.json",
        {
            "article_doi": ARTICLE_DOI,
            "article_url": ARTICLE_URL,
            "supplement_ids": CONTRASTS,
            "output_files": [
                str((OUT / "gsk761_sp140_supplement_module_summary.tsv").relative_to(ROOT)),
                str((OUT / "gsk761_sp140_interest_gene_effects.tsv").relative_to(ROOT)),
                str((OUT / "sp140_domain_structure_summary.tsv").relative_to(ROOT)),
                str((OUT / "sp140_public_endpoint_summary.tsv").relative_to(ROOT)),
            ],
        },
    )
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
