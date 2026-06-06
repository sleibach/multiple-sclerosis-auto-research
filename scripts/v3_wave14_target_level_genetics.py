#!/usr/bin/env python3
"""Wave-14 target-level genetics audit for narrowed V3 candidates.

This script deliberately stops short of causal claims.  It separates:

1. locus-level autoimmune evidence already collected from Open Targets
   gwas_credible_sets;
2. public cis-eQTL availability checks from GTEx;
3. public-resource access checks for GWAS Catalog/OpenGWAS/FinnGen/eQTLGen; and
4. whether a proper target-level coloc/MR analysis is feasible in this run.

The output truth table is meant to support a conservative go/no-go decision,
not to rescue locus co-occurrence as target causality.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "phases/v3/results" / "wave14_target_level_genetics"
OT_CREDIBLE_SETS = ROOT / "phases/v3/tmp" / "wave13_opentargets_gwas_credible_sets.tsv"
EXPR_SUMMARY = ROOT / "phases/v3/results" / "wave13_candidate_gene_local_validation" / "wave13_candidate_gene_summary.tsv"
GWAS_CATALOG_PARQUET = ROOT / "phases/v3/tmp" / "gwascatalog_associations_20260317_convert.parquet"

DATE = "2026-05-27"
USER_AGENT = "ms-auto-research-wave14-target-level-genetics/1.0"

CANDIDATES = [
    "SLC15A4",
    "TASL",
    "IRF5",
    "PTPN2",
    "TNFAIP3",
    "CLEC16A",
    "SH2B3",
    "GPR65",
    "CIITA",
    "RFX5",
    "GSK3B",
    "CD74",
]

GTEX_QUERY_SYMBOL = {
    "TASL": "CXorf21",
}

# GTEx v8 has broad public single-tissue eQTL calls and a stable API.  These
# tissues are not exhaustive; they are a compact relevance panel for the V3
# autoimmune tissue contexts under discussion.
GTEX_TISSUES = [
    "Whole_Blood",
    "Cells_EBV-transformed_lymphocytes",
    "Spleen",
    "Colon_Sigmoid",
    "Colon_Transverse",
    "Small_Intestine_Terminal_Ileum",
    "Skin_Not_Sun_Exposed_Suprapubic",
    "Skin_Sun_Exposed_Lower_leg",
    "Thyroid",
    "Brain_Cortex",
    "Brain_Frontal_Cortex_BA9",
    "Cells_Cultured_fibroblasts",
]

AUTOIMMUNE_TRAIT_TERMS = [
    "multiple sclerosis",
    "rheumatoid arthritis",
    "systemic lupus",
    "lupus",
    "crohn",
    "ulcerative colitis",
    "inflammatory bowel",
    "psoriasis",
    "type 1 diabetes",
    "sjogren",
    "ankylosing spondylitis",
    "autoimmune thyroid",
    "celiac",
    "coeliac",
    "primary biliary",
    "autoimmune",
]

DISEASE_LABELS = {
    "MS": "multiple sclerosis",
    "RA": "rheumatoid arthritis",
    "SLE": "systemic lupus erythematosus",
    "Crohn": "Crohn disease",
    "UC": "ulcerative colitis",
    "Psoriasis": "psoriasis",
    "T1D": "type 1 diabetes",
    "Sjogren": "Sjogren syndrome",
    "AS": "ankylosing spondylitis",
    "AITD": "autoimmune thyroid disease",
    "Celiac": "celiac disease",
    "PBC": "primary biliary cholangitis",
}

MECHANISM_NOTES = {
    "SLC15A4": "endolysosomal transporter; SLE-heavy genetic signal; immune-cell eQTL would be relevant to pDC/B/myeloid TLR biology",
    "TASL": "SLC15A4 adaptor, also known as CXorf21; X-linked locus; SLE/RA locus evidence but limited breadth",
    "IRF5": "myeloid/B-cell inflammatory transcription factor; broad autoimmune locus evidence but target-level coloc/MR still required",
    "PTPN2": "negative JAK/STAT phosphatase; broad autoimmune locus evidence but therapeutic direction is restoration, not inhibition",
    "TNFAIP3": "A20 NF-kB/TNF/TLR brake; strong autoimmune locus evidence but difficult restoration target",
    "CLEC16A": "16p13 autophagy/mitophagy locus with neighboring CIITA/DEXI/SOCS1 ambiguity",
    "SH2B3": "LNK cytokine-signaling adaptor; strong 12q24 pleiotropic locus, broad hematopoietic effects",
    "GPR65": "pH-sensing GPCR; druggable and IBD/spondylo/psoriasis/MS locus evidence, but directionality needs functional resolution",
    "CIITA": "MHC-II transcriptional coactivator; central state controller but weak disease genetics in current audit",
    "RFX5": "MHC-II enhanceosome factor; perturbation-relevant HLA-II controller but weak disease genetics",
    "GSK3B": "pleiotropic kinase/controller candidate; no target-level autoimmune genetics in supplied credible-set rows",
    "CD74": "HLA-II invariant chain/MIF receptor-state marker; no current target-level autoimmune genetics signal",
}

RESOURCE_URLS = {
    "Open Targets Platform GraphQL": "https://api.platform.opentargets.org/api/v4/graphql",
    "GWAS Catalog associations API": "https://www.ebi.ac.uk/gwas/rest/api/v2/associations?mappedGene=IRF5&size=5&page=0",
    "OpenGWAS API": "https://api.opengwas.io/api/gwasinfo?trait=multiple%20sclerosis",
    "FinnGen downloads": "https://www.finngen.fi/en/access_results",
    "GTEx Portal API": "https://gtexportal.org/api/v2/",
    "eQTLGen cis-eQTL resource": "https://kghub.org/kg-registry/resource/eqtlgen/eqtlgen.cis_eqtl_full.html",
    "eQTL Catalogue": "https://www.ebi.ac.uk/eqtl/",
}


@dataclass
class JsonFetchResult:
    url: str
    status: str
    http_status: int | None
    data: Any | None
    error: str


def fetch_json(url: str, timeout: int = 20) -> JsonFetchResult:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    last: JsonFetchResult | None = None
    for attempt in range(2):
        try:
            with urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                return JsonFetchResult(url, "ok", getattr(resp, "status", None), json.loads(raw), "")
        except HTTPError as exc:
            body = ""
            try:
                body = exc.read().decode("utf-8", errors="replace")[:400]
            except Exception:
                pass
            return JsonFetchResult(url, "http_error", exc.code, None, body or str(exc))
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            last = JsonFetchResult(url, "error", None, None, str(exc))
            if attempt == 0:
                time.sleep(0.5)
    return last or JsonFetchResult(url, "error", None, None, "unknown error")


def fetch_status(url: str, timeout: int = 20, accept: str = "*/*") -> dict[str, str]:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    try:
        with urlopen(req, timeout=timeout) as resp:
            _ = resp.read(256)
            return {
                "resource": "",
                "url": url,
                "status": "ok",
                "http_status": str(getattr(resp, "status", "")),
                "content_type": resp.headers.get("content-type", ""),
                "note": "",
            }
    except HTTPError as exc:
        return {
            "resource": "",
            "url": url,
            "status": "http_error",
            "http_status": str(exc.code),
            "content_type": exc.headers.get("content-type", "") if exc.headers else "",
            "note": str(exc),
        }
    except (URLError, TimeoutError) as exc:
        return {
            "resource": "",
            "url": url,
            "status": "error",
            "http_status": "",
            "content_type": "",
            "note": str(exc),
        }


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys: list[str] = []
        for row in rows:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})


def safe_float(value: str | None) -> float:
    try:
        return float(value) if value not in (None, "") else 0.0
    except ValueError:
        return 0.0


def safe_int(value: str | None) -> int:
    try:
        return int(float(value)) if value not in (None, "") else 0
    except ValueError:
        return 0


def split_semicolon(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in str(value).split(";") if part.strip()]


def summarize_open_targets(rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, str]]]]:
    by_gene: dict[str, list[dict[str, str]]] = {gene: [] for gene in CANDIDATES}
    for row in rows:
        gene = row.get("query_gene") or row.get("approved_symbol") or ""
        if gene in by_gene:
            by_gene[gene].append(row)
    summary: list[dict[str, Any]] = []
    for gene in CANDIDATES:
        sub = by_gene.get(gene, [])
        diseases_any: list[str] = []
        diseases_ge05: list[str] = []
        diseases_ge08: list[str] = []
        total_evidence = 0
        max_score = 0.0
        pmids: set[str] = set()
        for row in sub:
            score = safe_float(row.get("max_score"))
            count = safe_int(row.get("evidence_count"))
            disease = row.get("disease", "")
            max_score = max(max_score, score)
            total_evidence += count
            if count > 0 or score > 0:
                diseases_any.append(disease)
            if score >= 0.5:
                diseases_ge05.append(disease)
            if score >= 0.8:
                diseases_ge08.append(disease)
            pmids.update(split_semicolon(row.get("pmids")))
        summary.append(
            {
                "gene": gene,
                "ot_rows": len(sub),
                "ot_max_locus_score": f"{max_score:.6g}",
                "ot_total_evidence_count": total_evidence,
                "ot_diseases_any": ";".join(sorted(set(diseases_any))),
                "ot_n_diseases_any": len(set(diseases_any)),
                "ot_diseases_score_ge_0_5": ";".join(sorted(set(diseases_ge05))),
                "ot_n_diseases_score_ge_0_5": len(set(diseases_ge05)),
                "ot_diseases_score_ge_0_8": ";".join(sorted(set(diseases_ge08))),
                "ot_n_diseases_score_ge_0_8": len(set(diseases_ge08)),
                "ot_pmids": ";".join(sorted(pmids)),
                "ot_interpretation": "locus-level triage only; not target-level coloc/MR",
            }
        )
    return summary, by_gene


def summarize_expression(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    out = {gene: {} for gene in CANDIDATES}
    for row in rows:
        gene = row.get("gene", "")
        if gene in out:
            out[gene] = row
    return out


def gtex_gene_lookup(gene: str) -> dict[str, Any]:
    query_gene = GTEX_QUERY_SYMBOL.get(gene, gene)
    params = {
        "geneId": query_gene,
        "gencodeVersion": "v26",
        "genomeBuild": "GRCh38/hg38",
        "itemsPerPage": "5",
    }
    url = "https://gtexportal.org/api/v2/reference/gene?" + urlencode(params)
    result = fetch_json(url)
    if result.status != "ok":
        return {"gene": gene, "query_symbol": query_gene, "status": result.status, "url": url, "error": result.error}
    data = result.data.get("data", []) if isinstance(result.data, dict) else []
    if not data:
        return {"gene": gene, "query_symbol": query_gene, "status": "not_found", "url": url, "error": ""}
    first = data[0]
    return {
        "gene": gene,
        "query_symbol": query_gene,
        "status": "ok",
        "url": url,
        "gencode_id": first.get("gencodeId", ""),
        "chromosome": first.get("chromosome", ""),
        "start": first.get("start", ""),
        "end": first.get("end", ""),
        "gene_symbol": first.get("geneSymbol", gene),
        "error": "",
    }


def gtex_eqtl_count(gene: str, gencode_id: str, tissue: str) -> dict[str, Any]:
    params = {
        "gencodeId": gencode_id,
        "tissueSiteDetailId": tissue,
        "datasetId": "gtex_v8",
        "itemsPerPage": "1",
    }
    url = "https://gtexportal.org/api/v2/association/singleTissueEqtl?" + urlencode(params)
    result = fetch_json(url, timeout=25)
    base = {"gene": gene, "gencode_id": gencode_id, "tissue": tissue, "url": url}
    if result.status != "ok":
        return {**base, "status": result.status, "n_significant_eqtl": "", "top_variant": "", "top_pvalue": "", "top_nes": "", "error": result.error}
    payload = result.data if isinstance(result.data, dict) else {}
    info = payload.get("paging_info", {})
    total = int(info.get("totalNumberOfItems", 0) or 0)
    data = payload.get("data", [])
    first = data[0] if data else {}
    return {
        **base,
        "status": "ok",
        "n_significant_eqtl": total,
        "top_variant": first.get("variantId", ""),
        "top_pvalue": first.get("pValue", ""),
        "top_nes": first.get("nes", ""),
        "error": "",
    }


def run_gtex_checks() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    gene_rows: list[dict[str, Any]] = []
    eqtl_rows: list[dict[str, Any]] = []
    for gene in CANDIDATES:
        lookup = gtex_gene_lookup(gene)
        gene_rows.append(lookup)
        gencode_id = lookup.get("gencode_id", "")
        if not gencode_id:
            continue
        for tissue in GTEX_TISSUES:
            eqtl_rows.append(gtex_eqtl_count(gene, str(gencode_id), tissue))
            time.sleep(0.05)
    return gene_rows, eqtl_rows


def autoimmune_trait_text(association: dict[str, Any]) -> str:
    parts: list[str] = []
    for trait in association.get("reported_trait", []) or []:
        parts.append(str(trait))
    for trait in association.get("efo_traits", []) or []:
        parts.append(str(trait.get("efo_trait", "")))
    return " ".join(parts).lower()


def query_gwas_catalog_gene(gene: str, max_pages: int = 3) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    access = {"gene": gene, "status": "not_queried", "http_status": "", "error": "", "pages_queried": 0}
    for page in range(max_pages):
        params = {"mappedGene": gene, "size": "50", "page": str(page)}
        url = "https://www.ebi.ac.uk/gwas/rest/api/v2/associations?" + urlencode(params)
        result = fetch_json(url, timeout=30)
        access = {
            "gene": gene,
            "status": result.status,
            "http_status": result.http_status or "",
            "error": result.error,
            "pages_queried": page + 1,
            "url": url,
        }
        if result.status != "ok":
            break
        associations = []
        if isinstance(result.data, dict):
            associations = result.data.get("_embedded", {}).get("associations", []) or []
        for assoc in associations:
            trait_text = autoimmune_trait_text(assoc)
            if any(term in trait_text for term in AUTOIMMUNE_TRAIT_TERMS):
                rows.append(
                    {
                        "gene": gene,
                        "association_id": assoc.get("association_id", ""),
                        "accession_id": assoc.get("accession_id", ""),
                        "reported_trait": ";".join(map(str, assoc.get("reported_trait", []) or [])),
                        "efo_traits": ";".join(t.get("efo_trait", "") for t in assoc.get("efo_traits", []) or []),
                        "p_value": assoc.get("p_value", ""),
                        "locations": ";".join(map(str, assoc.get("locations", []) or [])),
                        "mapped_genes": ";".join(map(str, assoc.get("mapped_genes", []) or [])),
                        "pubmed_id": assoc.get("pubmed_id", ""),
                        "first_author": assoc.get("first_author", ""),
                        "source_url": assoc.get("_links", {}).get("self", {}).get("href", ""),
                    }
                )
        # Stop when paging links say there is no next page.  Some GWAS Catalog
        # instances return unpaged collections, so absence of page metadata is
        # not treated as an error.
        links = result.data.get("_links", {}) if isinstance(result.data, dict) else {}
        if "next" not in links:
            break
        time.sleep(0.1)
    return rows, access


def run_gwas_catalog_checks() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    access_rows: list[dict[str, Any]] = []
    for gene in CANDIDATES:
        gene_rows, access = query_gwas_catalog_gene(gene)
        rows.extend(gene_rows)
        access_rows.append(access)
        time.sleep(0.1)
    return rows, access_rows


def parquet_reader_status() -> dict[str, str]:
    parquet_exists = GWAS_CATALOG_PARQUET.exists()
    readers = {
        "pyarrow": importlib.util.find_spec("pyarrow") is not None,
        "fastparquet": importlib.util.find_spec("fastparquet") is not None,
        "duckdb": importlib.util.find_spec("duckdb") is not None,
    }
    usable = any(readers.values())
    return {
        "resource": "local GWAS Catalog parquet",
        "url": str(GWAS_CATALOG_PARQUET.relative_to(ROOT)) if parquet_exists else str(GWAS_CATALOG_PARQUET),
        "status": "readable" if parquet_exists and usable else "blocked",
        "http_status": "",
        "content_type": "Apache Parquet" if parquet_exists else "",
        "note": (
            "parquet file exists but no pyarrow/fastparquet/duckdb reader is installed in the active Python env"
            if parquet_exists and not usable
            else ("file missing" if not parquet_exists else "reader available")
        ),
    }


def resource_accessibility() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = [parquet_reader_status()]
    for name, url in RESOURCE_URLS.items():
        status = fetch_status(url, timeout=25)
        status["resource"] = name
        if name == "OpenGWAS API" and status["http_status"] == "401":
            status["note"] = "401 unauthorized; public API now requires authentication for this endpoint in this run"
        rows.append(status)
    rows.append(
        {
            "resource": "GTEx per-gene API eQTL counts",
            "url": "https://gtexportal.org/api/v2/association/singleTissueEqtl",
            "status": "queried",
            "http_status": "",
            "content_type": "application/json",
            "note": "significant GTEx eQTL counts queried per gene/tissue; this is not enough for coloc because locus-level SNP summary statistics were not downloaded",
        }
    )
    return rows


def disease_evidence_category(ot: dict[str, Any]) -> str:
    ge05 = int(ot.get("ot_n_diseases_score_ge_0_5", 0) or 0)
    any_n = int(ot.get("ot_n_diseases_any", 0) or 0)
    if ge05 >= 4:
        return "broad_locus"
    if ge05 >= 1 or any_n >= 1:
        return "limited_locus"
    return "none_detected"


def eqtl_summary_for_gene(eqtl_rows: list[dict[str, Any]]) -> dict[str, Any]:
    ok_rows = [r for r in eqtl_rows if r.get("status") == "ok"]
    positive = [r for r in ok_rows if safe_int(str(r.get("n_significant_eqtl", ""))) > 0]
    blood_immune = [
        r
        for r in positive
        if r.get("tissue") in {"Whole_Blood", "Cells_EBV-transformed_lymphocytes", "Spleen"}
    ]
    disease_tissue = [
        r
        for r in positive
        if r.get("tissue")
        in {
            "Colon_Sigmoid",
            "Colon_Transverse",
            "Small_Intestine_Terminal_Ileum",
            "Skin_Not_Sun_Exposed_Suprapubic",
            "Skin_Sun_Exposed_Lower_leg",
            "Thyroid",
            "Brain_Cortex",
            "Brain_Frontal_Cortex_BA9",
        }
    ]
    return {
        "gtex_relevant_tissues_with_significant_cis_eqtl": ";".join(r["tissue"] for r in positive),
        "gtex_n_relevant_tissues_with_significant_cis_eqtl": len(positive),
        "gtex_blood_or_immune_eqtl": "yes" if blood_immune else "no",
        "gtex_disease_tissue_eqtl": "yes" if disease_tissue else "no",
        "cis_eqtl_instrument_availability": "yes" if positive else "not_detected_in_panel",
    }


def tissue_relevance_for_gene(gene: str, expr: dict[str, str]) -> str:
    if not expr:
        return "mechanism-only; no local wave13 expression row"
    tested = safe_int(expr.get("n_diseases_tested"))
    trend = safe_int(expr.get("n_trend_or_better_diseases"))
    negative = safe_int(expr.get("n_negative_trend_diseases"))
    supporting = expr.get("supporting_diseases", "")
    if trend >= 4 and negative == 0:
        return f"local expression trend in {trend}/{tested} tested diseases: {supporting}"
    if trend > 0:
        return f"limited local expression trend in {trend}/{tested} tested diseases: {supporting}"
    return f"no local recurrence trend in {tested} tested diseases"


def make_truth_table(
    ot_summary: list[dict[str, Any]],
    expr_summary: dict[str, dict[str, str]],
    eqtl_rows: list[dict[str, Any]],
    gwas_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    ot_by_gene = {row["gene"]: row for row in ot_summary}
    eqtl_by_gene: dict[str, list[dict[str, Any]]] = {gene: [] for gene in CANDIDATES}
    for row in eqtl_rows:
        eqtl_by_gene.setdefault(str(row.get("gene", "")), []).append(row)
    gwas_by_gene: dict[str, list[dict[str, Any]]] = {gene: [] for gene in CANDIDATES}
    for row in gwas_rows:
        gwas_by_gene.setdefault(str(row.get("gene", "")), []).append(row)

    truth: list[dict[str, Any]] = []
    for gene in CANDIDATES:
        ot = ot_by_gene.get(gene, {})
        expr = expr_summary.get(gene, {})
        gwas_hits = gwas_by_gene.get(gene, [])
        category = disease_evidence_category(ot)
        if category == "none_detected" and gwas_hits:
            category = "catalog_top_association_only"
        eqtl = eqtl_summary_for_gene(eqtl_by_gene.get(gene, []))
        has_disease_genetic_evidence = category in {"broad_locus", "limited_locus"} or bool(gwas_hits)
        pqtls = "not_established"
        if gene in {"CD74", "GPR65"}:
            pqtls = "not_established_for_target-level_autoimmune_MR"
        if gene in {"TNFAIP3", "PTPN2", "CLEC16A", "SH2B3", "IRF5", "SLC15A4", "TASL", "CIITA", "RFX5", "GSK3B"}:
            pqtls = "intracellular_or_adaptor_target; plasma_pQTL_not_a_primary_instrument"

        blocker_parts: list[str] = []
        if not has_disease_genetic_evidence:
            blocker_parts.append("no disease genetic locus evidence in supplied OT credible-set rows")
        elif category == "limited_locus":
            blocker_parts.append("disease genetics is limited to fewer than four diseases at score>=0.5")
        elif category == "catalog_top_association_only":
            blocker_parts.append("GWAS Catalog top associations were seen, but no supplied Open Targets credible-set support was present")
        else:
            blocker_parts.append("broad disease locus evidence exists but is not target-level causal evidence")

        if eqtl["cis_eqtl_instrument_availability"] == "not_detected_in_panel":
            blocker_parts.append("no significant GTEx cis-eQTL detected in queried relevant tissues")
        else:
            blocker_parts.append("GTEx cis-eQTL exists but full SNP-level eQTL summary stats were not downloaded")

        blocker_parts.append("no paired disease GWAS summary stats and eQTL/pQTL summary files were available locally for multi-signal coloc")
        blocker_parts.append("OpenGWAS endpoint returned auth barrier in this run; local GWAS Catalog parquet lacks an installed reader")

        if gene == "CLEC16A":
            blocker_parts.append("16p13 locus has nearby CIITA/DEXI/SOCS1 ambiguity")
        if gene == "SH2B3":
            blocker_parts.append("12q24 locus is highly pleiotropic across hematopoietic/immune traits")
        if gene == "PTPN2":
            blocker_parts.append("autoimmune therapeutic direction is restoration/activation, not straightforward inhibition")
        if gene == "TNFAIP3":
            blocker_parts.append("target-level direction likely requires restoration of A20 function, not simple antagonism")
        if gene == "GPR65":
            blocker_parts.append("disease-direction conflict remains unresolved")
        if gene in {"CIITA", "RFX5", "CD74"}:
            blocker_parts.append("candidate is close to HLA-II state biology but lacks target-level disease genetics")
        if gene == "GSK3B":
            blocker_parts.append("pleiotropic kinase with no candidate-specific autoimmune genetics in supplied rows")

        # V3 target-level genetics DoD is intentionally stricter than locus
        # breadth: it requires causal target anchoring, direction, and feasibility
        # across multiple diseases.  No candidate reaches that bar here.
        dod_call = "no_go"
        if category == "broad_locus" and eqtl["cis_eqtl_instrument_availability"] == "yes":
            preliminary = "prioritize_for_future_coloc_not_DoD"
        elif category in {"limited_locus", "catalog_top_association_only"} and eqtl["cis_eqtl_instrument_availability"] == "yes":
            preliminary = "limited_followup_only"
        else:
            preliminary = "no_genetic_anchor"

        truth.append(
            {
                "gene": gene,
                "has_disease_genetic_evidence": "yes" if has_disease_genetic_evidence else "no",
                "disease_genetic_evidence_category": category,
                "ot_diseases_score_ge_0_5": ot.get("ot_diseases_score_ge_0_5", ""),
                "ot_n_diseases_score_ge_0_5": ot.get("ot_n_diseases_score_ge_0_5", 0),
                "ot_diseases_score_ge_0_8": ot.get("ot_diseases_score_ge_0_8", ""),
                "ot_n_diseases_score_ge_0_8": ot.get("ot_n_diseases_score_ge_0_8", 0),
                "gwas_catalog_autoimmune_hits_in_api_sample": len(gwas_hits),
                "cis_eqtl_instrument_availability": eqtl["cis_eqtl_instrument_availability"],
                "gtex_n_relevant_tissues_with_significant_cis_eqtl": eqtl["gtex_n_relevant_tissues_with_significant_cis_eqtl"],
                "gtex_relevant_tissues_with_significant_cis_eqtl": eqtl["gtex_relevant_tissues_with_significant_cis_eqtl"],
                "gtex_blood_or_immune_eqtl": eqtl["gtex_blood_or_immune_eqtl"],
                "gtex_disease_tissue_eqtl": eqtl["gtex_disease_tissue_eqtl"],
                "pqtl_instrument_availability": pqtls,
                "tissue_relevance": tissue_relevance_for_gene(gene, expr),
                "mechanism_note": MECHANISM_NOTES.get(gene, ""),
                "proper_coloc_or_mr_feasible_this_run": "no",
                "coloc_mr_blocker": "; ".join(blocker_parts),
                "target_level_genetics_dod_call": dod_call,
                "audit_priority_call": preliminary,
            }
        )
    return truth


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ot_rows = read_tsv(OT_CREDIBLE_SETS)
    expr_rows = read_tsv(EXPR_SUMMARY)
    ot_summary, _ = summarize_open_targets(ot_rows)
    expr_summary = summarize_expression(expr_rows)

    resource_rows = resource_accessibility()
    gtex_gene_rows, gtex_eqtl_rows = run_gtex_checks()
    gwas_rows, gwas_access_rows = run_gwas_catalog_checks()
    truth = make_truth_table(ot_summary, expr_summary, gtex_eqtl_rows, gwas_rows)

    write_tsv(OUT / "opentargets_locus_summary.tsv", ot_summary)
    write_tsv(OUT / "gtex_gene_lookup.tsv", gtex_gene_rows)
    write_tsv(OUT / "gtex_eqtl_availability.tsv", gtex_eqtl_rows)
    write_tsv(OUT / "gwas_catalog_mapped_gene_autoimmune_top_associations.tsv", gwas_rows)
    write_tsv(OUT / "gwas_catalog_access.tsv", gwas_access_rows)
    write_tsv(OUT / "resource_accessibility.tsv", resource_rows)
    write_tsv(OUT / "target_level_genetics_truth_table.tsv", truth)

    summary = {
        "date": DATE,
        "candidates": CANDIDATES,
        "inputs": {
            "open_targets_credible_sets": str(OT_CREDIBLE_SETS.relative_to(ROOT)),
            "expression_summary": str(EXPR_SUMMARY.relative_to(ROOT)),
            "local_gwas_catalog_parquet": str(GWAS_CATALOG_PARQUET.relative_to(ROOT)),
        },
        "outputs": {
            "opentargets_locus_summary": str((OUT / "opentargets_locus_summary.tsv").relative_to(ROOT)),
            "gtex_gene_lookup": str((OUT / "gtex_gene_lookup.tsv").relative_to(ROOT)),
            "gtex_eqtl_availability": str((OUT / "gtex_eqtl_availability.tsv").relative_to(ROOT)),
            "gwas_catalog_mapped_gene_autoimmune_top_associations": str(
                (OUT / "gwas_catalog_mapped_gene_autoimmune_top_associations.tsv").relative_to(ROOT)
            ),
            "gwas_catalog_access": str((OUT / "gwas_catalog_access.tsv").relative_to(ROOT)),
            "resource_accessibility": str((OUT / "resource_accessibility.tsv").relative_to(ROOT)),
            "target_level_genetics_truth_table": str((OUT / "target_level_genetics_truth_table.tsv").relative_to(ROOT)),
        },
        "global_call": "no_go_for_V3_target_level_genetics",
        "global_reason": (
            "No candidate has disease GWAS plus cis-eQTL/pQTL instrument plus proper "
            "multi-signal coloc/MR evidence across four autoimmune diseases in accessible "
            "local/public resources. Open Targets credible-set rows remain locus-level triage."
        ),
        "resource_urls": RESOURCE_URLS,
    }
    (OUT / "target_level_genetics_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"out": str(OUT), "candidates": len(CANDIDATES), "global_call": summary["global_call"]}, indent=2))


if __name__ == "__main__":
    main()
