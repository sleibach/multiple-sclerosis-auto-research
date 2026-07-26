#!/usr/bin/env python3
"""Measure core V55 newcomer route depth and reciprocal next steps.

This is a navigation-maintenance check. It does not validate scientific content
or measure whether a human understood it.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path

import v55_onboarding_audit as onboarding


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTDIR = ROOT / "analysis" / "v55_route_depth_audit"


@dataclass(frozen=True)
class Route:
    route_id: str
    start: str
    target: str
    max_hops: int


ROUTES = (
    Route("root_to_landing", "README.md", "docs/onboarding/README.md", 1),
    Route("root_to_two_minute", "README.md", "docs/onboarding/MS_RESEARCH_EXPLAINED.md", 1),
    Route("root_to_visuals", "README.md", "docs/onboarding/VISUAL_INDEX.md", 1),
    Route("root_to_open_problems", "README.md", "docs/onboarding/OPEN_PROBLEMS_FOR_COLLABORATORS.md", 1),
    Route("root_to_submission", "README.md", "docs/onboarding/HOW_TO_CONTRIBUTE_IDEAS.md", 1),
    Route("root_to_tour", "README.md", "docs/onboarding/REPOSITORY_TOUR.md", 1),
    Route("root_to_glossary", "README.md", "docs/onboarding/GLOSSARY.md", 1),
    Route("root_to_status_cards", "README.md", "docs/onboarding/LEAD_STATUS_CARDS.md", 2),
    Route("root_to_response_lifecycle", "README.md", "docs/onboarding/WHAT_HAPPENS_TO_YOUR_IDEA.md", 2),
    Route("landing_to_status_cards", "docs/onboarding/README.md", "docs/onboarding/LEAD_STATUS_CARDS.md", 1),
    Route("landing_to_null_guide", "docs/onboarding/README.md", "docs/onboarding/HOW_TO_READ_NULLS_AND_BOUNDARIES.md", 1),
    Route("landing_to_number_guide", "docs/onboarding/README.md", "docs/onboarding/HOW_TO_READ_NUMBERS_WITHOUT_OVERREADING.md", 1),
    Route("narrative_to_open_problems", "docs/onboarding/MS_RESEARCH_EXPLAINED.md", "docs/onboarding/OPEN_PROBLEMS_FOR_COLLABORATORS.md", 1),
    Route("problems_to_submission", "docs/onboarding/OPEN_PROBLEMS_FOR_COLLABORATORS.md", "docs/onboarding/HOW_TO_CONTRIBUTE_IDEAS.md", 1),
    Route("submission_to_lifecycle", "docs/onboarding/HOW_TO_CONTRIBUTE_IDEAS.md", "docs/onboarding/WHAT_HAPPENS_TO_YOUR_IDEA.md", 1),
    Route("lifecycle_to_problems", "docs/onboarding/WHAT_HAPPENS_TO_YOUR_IDEA.md", "docs/onboarding/OPEN_PROBLEMS_FOR_COLLABORATORS.md", 1),
    Route("status_cards_to_landing", "docs/onboarding/LEAD_STATUS_CARDS.md", "docs/onboarding/README.md", 1),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def public_documents() -> set[Path]:
    paths = {ROOT / "README.md", ROOT / "CONTRIBUTING.md"}
    paths.update((ROOT / "docs" / "onboarding").glob("*.md"))
    return {path.resolve() for path in paths if path.is_file()}


def build_graph(documents: set[Path]) -> dict[Path, set[Path]]:
    graph = {path: set() for path in documents}
    for document in documents:
        text = document.read_text(errors="replace")
        for raw_target in onboarding.LINK_RE.findall(text):
            resolved = onboarding.local_link_target(document, raw_target)
            if resolved is None:
                continue
            target, _fragment = resolved
            target = target.resolve()
            if target in documents:
                graph[document].add(target)
    return graph


def shortest_path(graph: dict[Path, set[Path]], start: Path, target: Path) -> list[Path] | None:
    queue: deque[list[Path]] = deque([[start]])
    seen = {start}
    while queue:
        path = queue.popleft()
        current = path[-1]
        if current == target:
            return path
        for neighbor in sorted(graph.get(current, set())):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(path + [neighbor])
    return None


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    documents = public_documents()
    graph = build_graph(documents)

    rows: list[dict[str, object]] = []
    failures: list[str] = []
    for route in ROUTES:
        start = (ROOT / route.start).resolve()
        target = (ROOT / route.target).resolve()
        path = shortest_path(graph, start, target) if start in graph and target in graph else None
        hops = None if path is None else len(path) - 1
        passed = hops is not None and hops <= route.max_hops
        if not passed:
            failures.append(route.route_id)
        rows.append(
            {
                **asdict(route),
                "actual_hops": "unreachable" if hops is None else hops,
                "path": " -> ".join(relative(item) for item in path) if path else "",
                "status": "PASS" if passed else "FAIL",
            }
        )

    route_path = outdir / "route_depth.tsv"
    with route_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("route_id", "start", "target", "max_hops", "actual_hops", "path", "status"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "purpose": "V55 newcomer route-depth maintenance check; no scientific claim",
        "n_public_markdown_documents": len(documents),
        "n_routes": len(rows),
        "n_fail": len(failures),
        "failures": failures,
        "overall_status": "PASS" if not failures else "FAIL",
        "routes": str(route_path.relative_to(ROOT)),
        "interpretation": "Configured path length and reciprocity only; not evidence of human comprehension.",
    }
    summary_path = outdir / "route_depth_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 1 if args.fail_on_error and failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
