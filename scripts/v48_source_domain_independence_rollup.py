#!/usr/bin/env python3
"""Build a source-domain independence rollup for V48 matrix rows."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INDEPENDENCE = ROOT / "knowledge_external/synthesis/convergence_source_independence_v48.tsv"
DEFAULT_OUTDIR = ROOT / "knowledge_external/catalogs/indexes"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--independence", type=Path, default=DEFAULT_INDEPENDENCE)
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


def relationship_counts(rows: list[dict[str, str]], field: str) -> str:
    counts = Counter(row.get(field, "") for row in rows if row.get(field, ""))
    return ";".join(f"{key}:{value}" for key, value in sorted(counts.items()))


def interpretation_boundary(rows: list[dict[str, str]], canonical_count: int) -> str:
    has_decision = any(row.get("relationship_class") in {"converges", "contradicts"} for row in rows)
    has_convergence = any(row.get("relationship_class") == "converges" for row in rows)
    if has_decision and canonical_count == 1:
        if has_convergence:
            return "Decision-relevant convergence is present, but the domain contributes one canonical source cluster; do not count multiple rows as independent corroborations."
        return "Decision-relevant relationship is present, but the domain contributes one canonical source cluster."
    if has_decision:
        return "Decision-relevant relationship is spread across multiple canonical source clusters; still external context, not project evidence."
    return "Insufficient-overlap/resource context only; not external corroboration or contradiction."


def build(independence_path: Path, outdir: Path) -> dict[str, object]:
    rows = read_tsv(independence_path)
    by_domain: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_domain[row.get("source_domain", "")].append(row)

    rollup_rows: list[dict[str, object]] = []
    for domain, domain_rows in sorted(by_domain.items()):
        canonical_urls = sorted({row.get("canonical_source_url", "") for row in domain_rows if row.get("canonical_source_url")})
        grounded_findings = sorted({row.get("grounded_finding_id", "") for row in domain_rows if row.get("grounded_finding_id")})
        decision_rows = [row for row in domain_rows if row.get("relationship_class") in {"converges", "contradicts"}]
        convergence_rows = [row for row in domain_rows if row.get("relationship_class") == "converges"]
        contradiction_rows = [row for row in domain_rows if row.get("relationship_class") == "contradicts"]
        insufficient_rows = [row for row in domain_rows if row.get("relationship_class") == "insufficient-overlap"]
        rollup_rows.append(
            {
                "source_domain": domain,
                "matrix_rows": len(domain_rows),
                "canonical_source_clusters": len(canonical_urls),
                "decision_relationship_rows": len(decision_rows),
                "convergence_rows": len(convergence_rows),
                "contradiction_rows": len(contradiction_rows),
                "insufficient_overlap_rows": len(insufficient_rows),
                "relationship_counts": relationship_counts(domain_rows, "relationship_class"),
                "synthesis_status_counts": relationship_counts(domain_rows, "synthesis_status"),
                "source_independence_classes": relationship_counts(domain_rows, "source_independence_class"),
                "canonical_source_urls": ";".join(canonical_urls),
                "grounded_findings": ";".join(grounded_findings),
                "interpretation_boundary": interpretation_boundary(domain_rows, len(canonical_urls)),
            }
        )
    rollup_rows.sort(
        key=lambda row: (
            -int(row["decision_relationship_rows"]),
            -int(row["convergence_rows"]),
            -int(row["matrix_rows"]),
            str(row["source_domain"]),
        )
    )

    fields = [
        "source_domain",
        "matrix_rows",
        "canonical_source_clusters",
        "decision_relationship_rows",
        "convergence_rows",
        "contradiction_rows",
        "insufficient_overlap_rows",
        "relationship_counts",
        "synthesis_status_counts",
        "source_independence_classes",
        "canonical_source_urls",
        "grounded_findings",
        "interpretation_boundary",
    ]
    outdir.mkdir(parents=True, exist_ok=True)
    write_tsv(outdir / "source_domain_independence_rollup_v48.tsv", rollup_rows, fields)

    total_canonical_clusters = len({row.get("canonical_source_url", "") for row in rows if row.get("canonical_source_url")})
    decision_canonical_clusters = len(
        {
            row.get("canonical_source_url", "")
            for row in rows
            if row.get("relationship_class") in {"converges", "contradicts"} and row.get("canonical_source_url")
        }
    )
    summary = {
        "purpose": "V48 source-domain independence rollup for convergence/insufficient-overlap rows; provenance/navigation only; no biological claim",
        "n_source_domains": len(rollup_rows),
        "n_matrix_rows": len(rows),
        "n_canonical_source_clusters": total_canonical_clusters,
        "n_decision_relationship_rows": sum(1 for row in rows if row.get("relationship_class") in {"converges", "contradicts"}),
        "n_decision_canonical_source_clusters": decision_canonical_clusters,
        "n_domains_with_convergence": sum(1 for row in rollup_rows if int(row["convergence_rows"]) > 0),
        "n_domains_with_contradiction": sum(1 for row in rollup_rows if int(row["contradiction_rows"]) > 0),
        "overall_status": "PASS",
        "markdown": "knowledge_external/catalogs/indexes/SOURCE_DOMAIN_INDEPENDENCE_ROLLUP_V48.md",
        "tsv": "knowledge_external/catalogs/indexes/source_domain_independence_rollup_v48.tsv",
    }
    (outdir / "source_domain_independence_rollup_v48_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    lines = [
        "# V48 Source-Domain Independence Rollup",
        "",
        "Status: provenance/navigation only. This rollup summarizes source-domain and canonical-source concentration for V48 matrix rows; it does not validate external claims.",
        "",
        f"- V48 matrix rows represented: `{summary['n_matrix_rows']}`",
        f"- source domains represented: `{summary['n_source_domains']}`",
        f"- canonical source clusters represented: `{summary['n_canonical_source_clusters']}`",
        f"- decision relationship rows: `{summary['n_decision_relationship_rows']}`",
        f"- decision canonical source clusters: `{summary['n_decision_canonical_source_clusters']}`",
        f"- domains with convergence rows: `{summary['n_domains_with_convergence']}`",
        f"- domains with contradiction rows: `{summary['n_domains_with_contradiction']}`",
        "",
        "## Domains",
        "",
        "| domain | rows | canonical clusters | decision rows | convergence | contradiction | insufficient overlap | relationship counts | independence classes | boundary |",
        "|---|---:|---:|---:|---:|---:|---:|---|---|---|",
    ]
    for row in rollup_rows:
        lines.append(
            "| "
            f"{md_escape(row['source_domain'])} | "
            f"{row['matrix_rows']} | "
            f"{row['canonical_source_clusters']} | "
            f"{row['decision_relationship_rows']} | "
            f"{row['convergence_rows']} | "
            f"{row['contradiction_rows']} | "
            f"{row['insufficient_overlap_rows']} | "
            f"`{md_escape(row['relationship_counts'])}` | "
            f"`{md_escape(row['source_independence_classes'])}` | "
            f"{md_escape(row['interpretation_boundary'])} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Decision rows are counted separately from canonical source clusters to prevent source overcounting.",
            "- Current convergence is domain- and source-cluster concentrated; the grounded project artifact remains the evidence.",
            "- Insufficient-overlap rows remain context/resource pointers, not corroboration.",
            "- No row here changes a grounded finding, locked rule, validation plan, or V37 score.",
            "",
        ]
    )
    (outdir / "SOURCE_DOMAIN_INDEPENDENCE_ROLLUP_V48.md").write_text("\n".join(lines))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    args = parse_args()
    independence = args.independence if args.independence.is_absolute() else ROOT / args.independence
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    summary = build(independence, outdir)
    return 0 if summary["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
