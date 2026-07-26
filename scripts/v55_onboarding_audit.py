#!/usr/bin/env python3
"""Audit V55 onboarding traceability and static-visual accessibility.

This script checks communication controls only. It does not validate a
scientific claim or upgrade an evidence grade.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
ONBOARDING = Path("docs/onboarding")
SOURCE_MATRIX = ONBOARDING / "ONBOARDING_CLAIM_SOURCES_V55.tsv"
DEFAULT_OUTDIR = Path("analysis/v55_onboarding_audit")
DEFAULT_SYNTHETIC_OUTDIR = Path("analysis/v55_onboarding_audit_synthetic")

EXPECTED_DOCS = {
    "COLLABORATOR_BRIEF_V55.html",
    "COLLABORATOR_BRIEF_V55.md",
    "COLLABORATOR_ROUTES.md",
    "CHALLENGE_THE_PROJECT.md",
    "QUESTION_STARTERS_BY_DISCIPLINE.md",
    "COMPREHENSION_TEST_KIT.md",
    "COMPREHENSION_FACILITATOR_HANDOFF.md",
    "CONTRIBUTE_A_DATA_SOURCE.md",
    "CONTRIBUTE_A_METHOD.md",
    "CONTRIBUTE_DOCUMENTATION_OR_VISUAL.md",
    "PATIENT_AND_PUBLIC_SAFETY.md",
    "FIND_BY_TERM.md",
    "DATA_THAT_WOULD_CHANGE_THE_ANSWER.md",
    "FAQ.md",
    "FAILURE_MODE_ATLAS.md",
    "FIRST_IDEA_IN_TEN_MINUTES.md",
    "IDEA_TRANSFORMATIONS.md",
    "IDEA_TRIAGE_RUBRIC.md",
    "README.md",
    "MS_RESEARCH_EXPLAINED.md",
    "OPEN_PROBLEMS_FOR_COLLABORATORS.md",
    "HOW_TO_CONTRIBUTE_IDEAS.md",
    "WHAT_HAPPENS_TO_YOUR_IDEA.md",
    "WORKED_SUBMISSION_LIFECYCLE.md",
    "REVIEW_RESPONSE_TEMPLATES.md",
    "STATUS_DECODER.md",
    "HOW_TO_READ_NULLS_AND_BOUNDARIES.md",
    "HOW_TO_READ_NUMBERS_WITHOUT_OVERREADING.md",
    "CASE_STUDY_BRAIN_BANK_CONFOUND.md",
    "CASE_STUDY_GENETICS_REVERSALS.md",
    "CASE_STUDY_MONITOR_VS_TARGET.md",
    "CASE_STUDY_PROGRESSION_SNAPSHOT_VS_MOVIE.md",
    "CONFOUND_CHECK_QUICK_REFERENCE.md",
    "CASE_STUDY_LEARNING_PATH.md",
    "COLLABORATOR_WORKSHOP_GUIDE.md",
    "CASE_STUDY_CONTEXT_TO_TEST.md",
    "GLOSSARY.md",
    "MYTHS_AND_ACTUAL_FINDINGS.md",
    "KNOWN_NON_SOLUTIONS.md",
    "PLAIN_LANGUAGE_REVIEW_V55.md",
    "PUBLIC_ISSUE_EXAMPLES.md",
    "RESEARCH_EVOLUTION_TIMELINE.md",
    "REPOSITORY_TOUR.md",
    "RESPONSIVE_PRINT_REVIEW_V55.md",
    "SOURCE_COVERAGE_V55.md",
    "LEAD_STATUS_CARDS.md",
    "MAINTAINER_RELEASE_CHECKLIST_V55.md",
    "VISUAL_INDEX.md",
    "ACCESSIBILITY_AUDIT_V55.md",
    "ANALOGY_SAFETY_REVIEW_V55.md",
    "NEWCOMER_AMBIGUITY_REVIEW_V55.md",
    "ROUTE_DEPTH_REVIEW_V55.md",
    "ZERO_JARGON_ENTRY_REVIEW_V55.md",
    "FINAL_DRIFT_AND_SAFETY_REVIEW_V55.md",
    "RELEASE_NOTES_V55.md",
    "INVITE_COLLABORATORS.md",
    "CLAIM_SOURCE_MATRIX_V55.md",
}

EXPECTED_VISUALS = {
    "CONTRIBUTOR_LIFECYCLE_V55.svg",
    "RESEARCH_MAP_V55.svg",
    "MONITORING_LEAD_V55.svg",
    "EVIDENCE_LANES_V55.svg",
    "RELAPSE_VS_PROGRESSION_V55.svg",
    "OPEN_PROBLEM_BOARD_V55.svg",
    "RESEARCH_EVOLUTION_V55.svg",
    "EVIDENCE_JOURNEY_V55.svg",
}

NAVIGATION_TARGETS = {
    Path("README.md"): {
        "CONTRIBUTING.md",
        "docs/onboarding/MS_RESEARCH_EXPLAINED.md",
        "docs/onboarding/VISUAL_INDEX.md",
        "docs/onboarding/OPEN_PROBLEMS_FOR_COLLABORATORS.md",
        "docs/onboarding/REPOSITORY_TOUR.md",
        "docs/onboarding/HOW_TO_CONTRIBUTE_IDEAS.md",
        "docs/onboarding/GLOSSARY.md",
        "meta/V55_QUEUE.md",
    },
    Path("CONTRIBUTING.md"): {
        "docs/knowledge/EPISTEMIC_CLASSES.md",
        "docs/onboarding/COLLABORATOR_ROUTES.md",
        "docs/onboarding/HOW_TO_CONTRIBUTE_IDEAS.md",
        "docs/onboarding/IDEA_TRIAGE_RUBRIC.md",
        "docs/onboarding/README.md",
        "meta/CURRENT_STATUS.md",
    },
    Path("meta/CURRENT_STATUS.md"): {
        "docs/onboarding/README.md",
        "docs/onboarding/ONBOARDING_CLAIM_SOURCES_V55.tsv",
        "analysis/v55_onboarding_audit/onboarding_audit_summary.json",
        "meta/V55_QUEUE.md",
    },
}

ALLOWED_STATUSES = {
    "BACKGROUND_ORIENTATION",
    "SUPPORTED_BOUNDARY",
    "LIVE_PROVISIONAL",
    "SUPPORTED_METHOD",
    "SUPPORTED_BOUNDED",
    "ROBUST_CONTEXT",
    "SUPPORTED_DECOUPLING",
    "CLOSED_DIRECTION",
    "CLOSED_EVIDENCE",
    "SUPPORTED_CONTEXT",
    "NEGATIVE_ESTABLISHED",
    "CORPUS_BOUNDARY",
    "DATA_BLOCKED",
    "LIVE_DATA_GATED",
    "GOVERNANCE",
    "NEXT_ACTION",
}

FORBIDDEN_CLASS_MARKERS = (
    ("formal_class_marker_1", "external" + "-verifiable"),
    ("formal_class_marker_2", "external" + "-unverifiable"),
    ("formal_class_marker_3", "NOT_PROJECT" + "_GROUNDED"),
)

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
BRACKET_RE = re.compile(r"\[([^\]]+)\]")
CLAIM_TOKEN_RE = re.compile(r"\b([A-Z])(\d{2})(?:-([A-Z]?)(\d{2}))?\b")
CLAIM_ID_RE = re.compile(r"^[A-Z]\d{2}$")
HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

DEFAULT_TEXT_PAIRS = [
    ("#172033", "#f7f9fc"),
    ("#52606d", "#f7f9fc"),
    ("#172033", "#ffffff"),
    ("#172033", "#e9f5ef"),
    ("#172033", "#e8f2fa"),
    ("#172033", "#f8ecea"),
    ("#172033", "#f0ecf8"),
    ("#172033", "#fff4d6"),
    ("#ffffff", "#172033"),
    ("#ffffff", "#8b2e2e"),
]
DEFAULT_GRAPHIC_PAIRS = [
    ("#005a9c", "#e8f2fa"),
    ("#1b6b4b", "#e9f5ef"),
    ("#8b2e2e", "#f8ecea"),
    ("#5b4b8a", "#f0ecf8"),
    ("#8a5a00", "#fff4d6"),
]


@dataclass(frozen=True)
class Check:
    path: str
    check: str
    status: str
    detail: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument(
        "--synthetic-check",
        action="store_true",
        help="Run temporary pass/fail fixtures instead of auditing the repository",
    )
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def add(checks: list[Check], path: str, name: str, passed: bool, detail: str) -> None:
    checks.append(Check(path, name, "PASS" if passed else "FAIL", detail))


def read_claim_rows(root: Path, checks: list[Check]) -> tuple[dict[str, dict[str, str]], set[str]]:
    matrix = root / SOURCE_MATRIX
    add(checks, str(SOURCE_MATRIX), "source_matrix_exists", matrix.is_file(), str(matrix))
    if not matrix.is_file():
        return {}, set()

    required = {
        "claim_id",
        "plain_language_statement",
        "onboarding_status",
        "evidence_role",
        "controlling_artifacts",
        "allowed_scope",
        "forbidden_overread",
    }
    rows: dict[str, dict[str, str]] = {}
    prefixes: set[str] = set()
    with matrix.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        fields = set(reader.fieldnames or [])
        add(checks, str(SOURCE_MATRIX), "source_matrix_schema", fields == required, f"fields={sorted(fields)}")
        for line_number, row in enumerate(reader, start=2):
            claim_id = (row.get("claim_id") or "").strip()
            valid_id = bool(CLAIM_ID_RE.fullmatch(claim_id))
            add(checks, str(SOURCE_MATRIX), f"claim_id_line_{line_number}", valid_id, claim_id or "empty")
            duplicate = claim_id in rows
            add(checks, str(SOURCE_MATRIX), f"claim_unique_line_{line_number}", not duplicate, claim_id)
            complete = all((row.get(field) or "").strip() for field in required)
            add(checks, str(SOURCE_MATRIX), f"claim_complete_line_{line_number}", complete, claim_id)
            status = (row.get("onboarding_status") or "").strip()
            add(checks, str(SOURCE_MATRIX), f"claim_status_line_{line_number}", status in ALLOWED_STATUSES, status)
            if valid_id and not duplicate:
                rows[claim_id] = row
                prefixes.add(claim_id[0])
            for artifact in (row.get("controlling_artifacts") or "").split(";"):
                artifact = artifact.strip()
                exists = bool(artifact) and (root / artifact).exists()
                add(checks, str(SOURCE_MATRIX), f"source_exists_line_{line_number}", exists, artifact or "empty")
    return rows, prefixes


def expand_claim_refs(text: str, prefixes: set[str]) -> set[str]:
    refs: set[str] = set()
    for bracket in BRACKET_RE.findall(text):
        for match in CLAIM_TOKEN_RE.finditer(bracket):
            start_prefix, start_number, end_prefix, end_number = match.groups()
            if start_prefix not in prefixes:
                continue
            start_id = f"{start_prefix}{start_number}"
            refs.add(start_id)
            if end_number:
                final_prefix = end_prefix or start_prefix
                if final_prefix != start_prefix:
                    refs.add(f"{final_prefix}{end_number}")
                    continue
                start_value = int(start_number)
                end_value = int(end_number)
                if start_value <= end_value and end_value - start_value <= 30:
                    refs.update(f"{start_prefix}{value:02d}" for value in range(start_value, end_value + 1))
    return refs


def local_link_target(document: Path, target: str) -> tuple[Path, str] | None:
    target = unquote(target.strip())
    if not target or target.startswith(("http://", "https://", "mailto:")):
        return None
    path_part, separator, fragment = target.partition("#")
    path = document if not path_part else (document.parent / path_part).resolve()
    return path, fragment if separator else ""


def github_heading_slug(text: str) -> str:
    text = LINK_RE.sub(r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_~]", "", text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return re.sub(r"\s+", "-", text)


def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    for line in path.read_text(errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        heading = re.match(r"^#{1,6}\s+(.+?)(?:\s+#+)?$", stripped)
        if heading:
            base = github_heading_slug(heading.group(1))
            if base:
                duplicate_number = counts.get(base, 0)
                slug = base if duplicate_number == 0 else f"{base}-{duplicate_number}"
                counts[base] = duplicate_number + 1
                anchors.add(slug)
        for explicit in re.findall(
            r"<(?:a|span|div|section)\b[^>]*\b(?:id|name)=[\"']([^\"']+)[\"']",
            line,
            flags=re.IGNORECASE,
        ):
            anchors.add(unquote(explicit))
    return anchors


def audit_local_links(
    root: Path,
    document: Path,
    text: str,
    checks: list[Check],
) -> None:
    for target in LINK_RE.findall(text):
        local_target = local_link_target(document, target)
        if local_target is None:
            continue
        local, fragment = local_target
        add(checks, rel(root, document), "local_link_resolves", local.exists(), target)
        if fragment and local.is_file() and local.suffix.lower() in {".md", ".markdown"}:
            anchors = markdown_anchors(local)
            add(
                checks,
                rel(root, document),
                "local_anchor_resolves",
                fragment in anchors,
                f"{target}; known_anchors={len(anchors)}",
            )


def audit_markdown(
    root: Path,
    claim_rows: dict[str, dict[str, str]],
    prefixes: set[str],
    checks: list[Check],
    expected_docs: set[str] | None = None,
) -> set[str]:
    onboarding = root / ONBOARDING
    referenced: set[str] = set()
    documents = EXPECTED_DOCS if expected_docs is None else expected_docs
    for name in sorted(documents):
        document = onboarding / name
        add(checks, str(ONBOARDING / name), "expected_document_exists", document.is_file(), str(document))
        if not document.is_file():
            continue
        text = document.read_text(errors="replace")
        for marker_label, marker in FORBIDDEN_CLASS_MARKERS:
            add(checks, rel(root, document), marker_label, marker not in text, "formal marker absent")
        add(checks, rel(root, document), "no_unresolved_todo", not re.search(r"\b(?:TODO|TBD)\b", text), "TODO/TBD scan")
        refs = expand_claim_refs(text, prefixes)
        referenced.update(refs)
        if name not in {"ACCESSIBILITY_AUDIT_V55.md", "CLAIM_SOURCE_MATRIX_V55.md"}:
            add(checks, rel(root, document), "has_claim_reference", bool(refs), f"n={len(refs)}")
        for claim_id in sorted(refs):
            add(checks, rel(root, document), f"claim_reference_{claim_id}", claim_id in claim_rows, claim_id)
        audit_local_links(root, document, text, checks)
    return referenced


def audit_svg(
    root: Path,
    checks: list[Check],
    expected_visuals: set[str] | None = None,
) -> None:
    visuals = root / ONBOARDING / "visuals"
    visual_names = EXPECTED_VISUALS if expected_visuals is None else expected_visuals
    for name in sorted(visual_names):
        path = visuals / name
        relative = rel(root, path)
        add(checks, relative, "expected_visual_exists", path.is_file(), str(path))
        if not path.is_file():
            continue
        size = path.stat().st_size
        add(checks, relative, "visual_under_250kb", size < 250_000, f"bytes={size}")
        try:
            tree = ET.parse(path)
            svg = tree.getroot()
            parsed = True
        except ET.ParseError as exc:
            add(checks, relative, "xml_parses", False, str(exc))
            continue
        add(checks, relative, "xml_parses", parsed, "ElementTree")
        add(checks, relative, "role_img", svg.attrib.get("role") == "img", svg.attrib.get("role", ""))
        labelled = svg.attrib.get("aria-labelledby", "").split()
        ids = {element.attrib.get("id") for element in svg.iter() if element.attrib.get("id")}
        add(checks, relative, "aria_label_targets_exist", len(labelled) >= 2 and all(item in ids for item in labelled), " ".join(labelled))
        title = next((element for element in svg.iter() if element.tag.endswith("title")), None)
        desc = next((element for element in svg.iter() if element.tag.endswith("desc")), None)
        title_text = "" if title is None else "".join(title.itertext()).strip()
        desc_text = "" if desc is None else "".join(desc.itertext()).strip()
        add(checks, relative, "title_present", len(title_text) >= 10, title_text)
        add(checks, relative, "description_present", len(desc_text) >= 40, f"chars={len(desc_text)}")
        add(checks, relative, "viewbox_present", bool(svg.attrib.get("viewBox")), svg.attrib.get("viewBox", ""))
        scripts = [element for element in svg.iter() if element.tag.endswith("script")]
        add(checks, relative, "no_script", not scripts, f"n={len(scripts)}")
        hrefs = [value for element in svg.iter() for key, value in element.attrib.items() if key.endswith("href")]
        remote = [value for value in hrefs if value.startswith(("http://", "https://"))]
        add(checks, relative, "no_remote_assets", not remote, f"n={len(remote)}")


def audit_navigation(root: Path, checks: list[Check]) -> None:
    for relative, targets in NAVIGATION_TARGETS.items():
        path = root / relative
        add(checks, str(relative), "navigation_document_exists", path.is_file(), str(path))
        if not path.is_file():
            continue
        text = path.read_text(errors="replace")
        audit_local_links(root, path, text, checks)
        for target in sorted(targets):
            add(checks, str(relative), "navigation_target_present", target in text, target)
            add(checks, str(relative), "navigation_target_exists", (root / target).exists(), target)


def srgb_luminance(color: str) -> float:
    if not HEX_RE.fullmatch(color):
        raise ValueError(color)
    values = [int(color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4 for value in values]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(first: str, second: str) -> float:
    high, low = sorted((srgb_luminance(first), srgb_luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def audit_contrast(
    checks: list[Check],
    text_pairs: list[tuple[str, str]] | None = None,
    graphic_pairs: list[tuple[str, str]] | None = None,
) -> None:
    text_pairs = DEFAULT_TEXT_PAIRS if text_pairs is None else text_pairs
    graphic_pairs = DEFAULT_GRAPHIC_PAIRS if graphic_pairs is None else graphic_pairs
    for foreground, background in text_pairs:
        ratio = contrast_ratio(foreground, background)
        add(checks, "visual_palette", "text_contrast_aa", ratio >= 4.5, f"{foreground}/{background}={ratio:.2f}:1")
    for foreground, background in graphic_pairs:
        ratio = contrast_ratio(foreground, background)
        add(checks, "visual_palette", "graphic_contrast_aa", ratio >= 3.0, f"{foreground}/{background}={ratio:.2f}:1")


def write_outputs(root: Path, outdir: Path, checks: list[Check], referenced: set[str], claim_rows: dict[str, dict[str, str]]) -> dict[str, object]:
    output = outdir if outdir.is_absolute() else root / outdir
    output.mkdir(parents=True, exist_ok=True)
    issues = output / "onboarding_audit_checks.tsv"
    with issues.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=["path", "check", "status", "detail"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(asdict(check) for check in checks)
    n_fail = sum(check.status != "PASS" for check in checks)
    summary: dict[str, object] = {
        "purpose": "V55 onboarding traceability/accessibility audit; no scientific claim",
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "n_checks": len(checks),
        "n_fail": n_fail,
        "n_claim_rows": len(claim_rows),
        "n_claim_rows_referenced": len(referenced & set(claim_rows)),
        "n_expected_documents": len(EXPECTED_DOCS),
        "n_expected_visuals": len(EXPECTED_VISUALS),
        "issues": rel(root, issues),
    }
    (output / "onboarding_audit_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def fixture_result(
    results: list[dict[str, str]],
    case: str,
    passed: bool,
    expected_behavior: str,
    detail: str,
) -> None:
    results.append(
        {
            "case": case,
            "status": "PASS" if passed else "FAIL",
            "expected_behavior": expected_behavior,
            "detail": detail,
        }
    )


def failed_checks(checks: list[Check]) -> list[Check]:
    return [check for check in checks if check.status == "FAIL"]


def run_synthetic_checks(root: Path, outdir: Path) -> dict[str, object]:
    """Prove the communication audit accepts clean and rejects bad fixtures."""

    results: list[dict[str, str]] = []
    claim_rows = {"M01": {"claim_id": "M01"}}
    prefixes = {"M"}

    with tempfile.TemporaryDirectory(prefix="v55-onboarding-audit-") as name:
        fixture_root = Path(name)
        onboarding = fixture_root / ONBOARDING
        visuals = onboarding / "visuals"
        visuals.mkdir(parents=True)
        document = onboarding / "FAQ.md"
        target = onboarding / "target.md"
        target.write_text(
            "# Existing target\n\n## Repeated heading\n\n"
            "## Repeated heading\n",
            encoding="utf-8",
        )

        document.write_text(
            "# Clean fixture\n\nBounded statement `[M01]`.\n\n"
            "[Existing target](target.md#existing-target) and "
            "[second duplicate](target.md#repeated-heading-1).\n",
            encoding="utf-8",
        )
        checks: list[Check] = []
        audit_markdown(
            fixture_root,
            claim_rows,
            prefixes,
            checks,
            expected_docs={"FAQ.md"},
        )
        failures = failed_checks(checks)
        fixture_result(
            results,
            "clean_markdown_accepted",
            not failures,
            "well-formed document passes",
            f"unexpected_failures={len(failures)}",
        )

        document.write_text(
            "# Broken link fixture\n\nBounded `[M01]`.\n\n"
            "[Missing target](does-not-exist.md)\n",
            encoding="utf-8",
        )
        checks = []
        audit_markdown(
            fixture_root,
            claim_rows,
            prefixes,
            checks,
            expected_docs={"FAQ.md"},
        )
        detected = any(
            check.check == "local_link_resolves" and check.status == "FAIL"
            for check in checks
        )
        fixture_result(
            results,
            "broken_link_rejected",
            detected,
            "missing local target produces a failure",
            f"detector_fired={detected}",
        )

        document.write_text(
            "# Broken anchor fixture\n\nBounded `[M01]`.\n\n"
            "[Missing section](target.md#does-not-exist)\n",
            encoding="utf-8",
        )
        checks = []
        audit_markdown(
            fixture_root,
            claim_rows,
            prefixes,
            checks,
            expected_docs={"FAQ.md"},
        )
        detected = any(
            check.check == "local_anchor_resolves" and check.status == "FAIL"
            for check in checks
        )
        fixture_result(
            results,
            "broken_section_anchor_rejected",
            detected,
            "missing Markdown heading fragment produces a failure",
            f"detector_fired={detected}",
        )

        document.write_text(
            "# Unknown claim fixture\n\nUnsupported identifier `[M99]`.\n",
            encoding="utf-8",
        )
        checks = []
        audit_markdown(
            fixture_root,
            claim_rows,
            prefixes,
            checks,
            expected_docs={"FAQ.md"},
        )
        detected = any(
            check.check == "claim_reference_M99" and check.status == "FAIL"
            for check in checks
        )
        fixture_result(
            results,
            "unknown_claim_id_rejected",
            detected,
            "claim absent from source contract produces a failure",
            f"detector_fired={detected}",
        )

        for marker_label, marker in FORBIDDEN_CLASS_MARKERS:
            document.write_text(
                f"# Marker fixture\n\nBounded `[M01]`.\n\nLeaked marker: {marker}\n",
                encoding="utf-8",
            )
            checks = []
            audit_markdown(
                fixture_root,
                claim_rows,
                prefixes,
                checks,
                expected_docs={"FAQ.md"},
            )
            detected = any(
                check.check == marker_label and check.status == "FAIL"
                for check in checks
            )
            fixture_result(
                results,
                f"{marker_label}_leakage_rejected",
                detected,
                "formal class marker in onboarding produces a failure",
                f"detector_fired={detected}",
            )

        valid_svg = visuals / "fixture.svg"
        valid_svg.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" '
            'viewBox="0 0 200 100" role="img" aria-labelledby="title desc">'
            '<title id="title">Accessible fixture visual</title>'
            '<desc id="desc">A synthetic visual used only to prove semantic '
            'checks accept a complete accessible SVG fixture.</desc>'
            '<rect width="200" height="100" fill="#ffffff"/></svg>\n',
            encoding="utf-8",
        )
        checks = []
        audit_svg(fixture_root, checks, expected_visuals={"fixture.svg"})
        failures = failed_checks(checks)
        fixture_result(
            results,
            "clean_svg_accepted",
            not failures,
            "well-formed semantic SVG passes",
            f"unexpected_failures={len(failures)}",
        )

        valid_svg.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100" '
            'viewBox="0 0 200 100"><rect width="200" height="100"/></svg>\n',
            encoding="utf-8",
        )
        checks = []
        audit_svg(fixture_root, checks, expected_visuals={"fixture.svg"})
        missing_semantics = {
            check.check
            for check in failed_checks(checks)
            if check.check
            in {
                "role_img",
                "aria_label_targets_exist",
                "title_present",
                "description_present",
            }
        }
        fixture_result(
            results,
            "missing_svg_semantics_rejected",
            len(missing_semantics) == 4,
            "missing role, labels, title, and description all fail",
            f"detectors={sorted(missing_semantics)}",
        )

        checks = []
        audit_contrast(
            checks,
            text_pairs=[("#777777", "#ffffff")],
            graphic_pairs=[],
        )
        detected = any(
            check.check == "text_contrast_aa" and check.status == "FAIL"
            for check in checks
        )
        fixture_result(
            results,
            "low_text_contrast_rejected",
            detected,
            "text below 4.5:1 produces a failure",
            checks[0].detail if checks else "no check produced",
        )

        checks = []
        audit_contrast(
            checks,
            text_pairs=[],
            graphic_pairs=[("#bbbbbb", "#ffffff")],
        )
        detected = any(
            check.check == "graphic_contrast_aa" and check.status == "FAIL"
            for check in checks
        )
        fixture_result(
            results,
            "low_graphic_contrast_rejected",
            detected,
            "non-text contrast below 3:1 produces a failure",
            checks[0].detail if checks else "no check produced",
        )

    output = outdir if outdir.is_absolute() else root / outdir
    output.mkdir(parents=True, exist_ok=True)
    results_path = output / "synthetic_fixture_results.tsv"
    with results_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            delimiter="\t",
            fieldnames=("case", "status", "expected_behavior", "detail"),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(results)

    n_fail = sum(result["status"] != "PASS" for result in results)
    summary: dict[str, object] = {
        "purpose": "V55 onboarding audit synthetic detector verification; no scientific claim",
        "overall_status": "PASS" if n_fail == 0 else "FAIL",
        "n_fixture_cases": len(results),
        "n_fail": n_fail,
        "temporary_fixture_files_committed": 0,
        "results": rel(root, results_path),
    }
    (output / "synthetic_fixture_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if args.synthetic_check:
        outdir = (
            DEFAULT_SYNTHETIC_OUTDIR
            if args.outdir == DEFAULT_OUTDIR
            else args.outdir
        )
        summary = run_synthetic_checks(root, outdir)
        print(json.dumps(summary, indent=2, sort_keys=True))
        if args.fail_on_error and summary["overall_status"] != "PASS":
            return 1
        return 0
    checks: list[Check] = []
    claim_rows, prefixes = read_claim_rows(root, checks)
    referenced = audit_markdown(root, claim_rows, prefixes, checks)
    audit_svg(root, checks)
    audit_navigation(root, checks)
    audit_contrast(checks)
    summary = write_outputs(root, args.outdir, checks, referenced, claim_rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.fail_on_error and summary["overall_status"] != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
