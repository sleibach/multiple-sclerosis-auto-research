#!/usr/bin/env python3
"""Build source-search query packet for high-priority V48 sourcing gaps."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "knowledge_external/synthesis/high_priority_external_sourcing_plan_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/synthesis"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    return parser.parse_args()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


INTERNAL_QUERY_TOKENS = {
    "LOCKED",
    "FIRST",
    "V",
}


def quoted_terms(item: str) -> list[str]:
    item_lower = item.lower()
    if "baseline fallback" in item_lower:
        return ["multiple sclerosis", "autoimmune", "baseline biomarker", "cross disease", "treatment response"]
    if "v22" in item_lower or "scalar" in item_lower:
        return ["multiple sclerosis", "biomarker validation", "treatment response", "simple model"]
    if "invariant" in item_lower:
        return ["multiple sclerosis", "immune invariant", "perturbation", "stress response"]
    if "druggability" in item_lower:
        return ["multiple sclerosis", "drug target validation", "direction of effect", "target tractability"]
    genes = [
        token
        for token in re.findall(r"\b[A-Z0-9]{3,}\b", item)
        if token not in {"IFN", "APC", "MS", *INTERNAL_QUERY_TOKENS}
        and not re.fullmatch(r"V\d+", token)
    ]
    terms: list[str] = []
    for gene in genes[:3]:
        terms.append(gene)
    if "IBD" in item or "Crohn" in item or "UC" in item:
        terms.extend(["multiple sclerosis", "inflammatory bowel disease", "ulcerative colitis", "Crohn"])
    if "EBV" in item:
        terms.extend(["multiple sclerosis", "Epstein Barr virus", "interferon", "antigen presentation"])
    if "pregnancy" in item or "RA" in item:
        terms.extend(["multiple sclerosis", "pregnancy", "postpartum", "rheumatoid arthritis"])
    if "MHC" in item:
        terms.extend(["multiple sclerosis", "MHC", "fine mapping", "colocalization"])
    if not terms:
        terms.extend(["multiple sclerosis", item.split()[0]])
    deduped: list[str] = []
    for term in terms:
        if term and term not in deduped:
            deduped.append(term)
    return deduped[:6]


def query_for(row: dict[str, str], target: str) -> str:
    item = row.get("item", "")
    source_type = row.get("source_type_needed", "")
    terms = quoted_terms(item)
    if target == "PubMed/EuropePMC":
        quoted = " AND ".join(f'"{term}"' if " " in term else term for term in terms[:4])
        if "method/governance" in source_type:
            return f'{quoted} AND ("validation" OR "biomarker" OR "target validation" OR "drug target")'
        if "genetics" in source_type:
            return f'{quoted} AND ("fine mapping" OR colocalization OR eQTL OR "direction")'
        if "EBV" in source_type:
            return f'{quoted} AND ("specificity" OR "case control" OR transcriptom*)'
        return f'{quoted} AND ("transcriptomic" OR "response" OR "longitudinal" OR "mechanism")'
    if target == "GEO/ArrayExpress":
        quoted = " ".join(f'"{term}"' if " " in term else term for term in terms[:5])
        return f'{quoted} treatment response baseline longitudinal transcriptome'
    if target == "GWAS/QTL catalogs":
        quoted = " ".join(terms[:4])
        return f'{quoted} GWAS eQTL colocalization fine-mapping'
    return " ".join(terms)


def target_repositories(source_type: str) -> list[str]:
    if "genetics" in source_type:
        return ["PubMed/EuropePMC", "GWAS/QTL catalogs"]
    if "method/governance" in source_type:
        return ["PubMed/EuropePMC"]
    return ["PubMed/EuropePMC", "GEO/ArrayExpress"]


def build(plan_path: Path, outdir: Path) -> dict[str, object]:
    plan_rows = read_tsv(plan_path)
    rows: list[dict[str, object]] = []
    for plan in plan_rows:
        for target in target_repositories(plan.get("source_type_needed", "")):
            rows.append(
                {
                    "rank": plan.get("rank", ""),
                    "item": plan.get("item", ""),
                    "source_type_needed": plan.get("source_type_needed", ""),
                    "search_target": target,
                    "query": query_for(plan, target),
                    "acceptance_criteria": plan.get("acceptance_criteria", ""),
                    "forbidden_shortcut": plan.get("forbidden_shortcut", ""),
                    "integration_boundary": "Search results are candidates only; no claim enters the project without V47 segregated-record intake and V48 overlap review.",
                }
            )
    fields = ["rank", "item", "source_type_needed", "search_target", "query", "acceptance_criteria", "forbidden_shortcut", "integration_boundary"]
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "high_priority_source_search_queries_v48.tsv", rows, fields)
    target_counts: dict[str, int] = {}
    for row in rows:
        target = str(row["search_target"])
        target_counts[target] = target_counts.get(target, 0) + 1
    summary = {
        "purpose": "V48 high-priority source-search query packet; future search/navigation only; no searches run and no biological claim",
        "n_plan_rows": len(plan_rows),
        "n_query_rows": len(rows),
        "target_counts": dict(sorted(target_counts.items())),
        "overall_status": "PASS",
        "markdown": "knowledge_external/synthesis/HIGH_PRIORITY_SOURCE_SEARCH_QUERIES_V48.md",
        "tsv": "knowledge_external/synthesis/high_priority_source_search_queries_v48.tsv",
    }
    (ROOT / "knowledge_external/catalogs/indexes/high_priority_source_search_queries_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    lines = [
        "# V48 High-Priority Source Search Queries",
        "",
        "Status: future search/navigation only. These queries have not been run here; they do not add external records, assert convergence, or change grounded findings.",
        "",
        f"- source-plan rows: `{summary['n_plan_rows']}`",
        f"- query rows: `{summary['n_query_rows']}`",
        "",
        "## Target Counts",
        "",
        "| search target | count |",
        "|---|---:|",
    ]
    for target, count in sorted(target_counts.items()):
        lines.append(f"| {md_escape(target)} | {count} |")
    lines.extend(
        [
            "",
            "## Queries",
            "",
            "| rank | finding | target | query | acceptance criteria |",
            "|---:|---|---|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            f"{md_escape(row['rank'])} | "
            f"{md_escape(row['item'])} | "
            f"{md_escape(row['search_target'])} | "
            f"`{md_escape(row['query'])}` | "
            f"{md_escape(row['acceptance_criteria'])} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- This is a query packet only; no search result is integrated by this artifact.",
            "- Any future hit must pass the V47 segregated-record intake and V48 overlap review before it can appear in the relationship matrix.",
            "- Generic adjacent-context hits are explicitly insufficient where the source plan requires same-definition overlap.",
            "",
        ]
    )
    (outdir / "HIGH_PRIORITY_SOURCE_SEARCH_QUERIES_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    plan = args.plan if args.plan.is_absolute() else ROOT / args.plan
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    summary = build(plan, outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
