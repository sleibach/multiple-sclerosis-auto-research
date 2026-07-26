#!/usr/bin/env python3
"""Measure prose load in V55 onboarding without grading scientific truth.

The audit deliberately excludes code fences and Markdown tables, where sentence
metrics are misleading. Its thresholds are maintenance signals, not evidence
that a reader understood the material. Scientific terms may remain when they
are defined and necessary.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ONBOARDING = ROOT / "docs" / "onboarding"
DEFAULT_OUTDIR = ROOT / "analysis" / "v55_plain_language_audit"
AUDIENCE_DOCS = (
    "README.md",
    "COLLABORATOR_BRIEF_V55.md",
    "MS_RESEARCH_EXPLAINED.md",
    "OPEN_PROBLEMS_FOR_COLLABORATORS.md",
    "HOW_TO_CONTRIBUTE_IDEAS.md",
    "HOW_TO_READ_NULLS_AND_BOUNDARIES.md",
    "CASE_STUDY_BRAIN_BANK_CONFOUND.md",
    "CASE_STUDY_GENETICS_REVERSALS.md",
    "CASE_STUDY_MONITOR_VS_TARGET.md",
    "CASE_STUDY_PROGRESSION_SNAPSHOT_VS_MOVIE.md",
    "CONFOUND_CHECK_QUICK_REFERENCE.md",
    "CASE_STUDY_LEARNING_PATH.md",
    "COLLABORATOR_WORKSHOP_GUIDE.md",
    "FAQ.md",
    "FAILURE_MODE_ATLAS.md",
    "DATA_THAT_WOULD_CHANGE_THE_ANSWER.md",
    "RESEARCH_EVOLUTION_TIMELINE.md",
    "REPOSITORY_TOUR.md",
    "COLLABORATOR_ROUTES.md",
    "IDEA_TRANSFORMATIONS.md",
    "MYTHS_AND_ACTUAL_FINDINGS.md",
    "LEAD_STATUS_CARDS.md",
    "VISUAL_INDEX.md",
)

LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
CLAIM_RE = re.compile(r"\[(?:[A-Z]\d{2})(?:\s*[-,]\s*[A-Z]?\d{2})*\]")
WORD_RE = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*")
SENTENCE_RE = re.compile(r"(?<=[.!?])(?:[\"')\]]*)\s+")
ACRONYM_RE = re.compile(r"\b[A-Z][A-Z0-9/-]{1,}\b")
VERSION_OR_CLAIM_RE = re.compile(
    r"^(?:V\d+|GSE\d+|[A-Z]\d{2}(?:-[A-Z]?\d{2})?|P\d+|\d+)$"
)
NON_ACRONYM_CAPS = {
    "BLOCKED",
    "BOUND",
    "CLOSED",
    "CONTEXT",
    "CONTRIBUTING",
    "CORPUS-SPECIFIC",
    "DATA",
    "DECOUPLING",
    "DEMOTED",
    "DIRECTION",
    "ESTABLISHED",
    "EVIDENCE",
    "EXHAUSTION",
    "FOR",
    "GAP",
    "GATED",
    "GROUNDED",
    "GLOSSARY",
    "IDENTITY",
    "INDEX",
    "LIVE",
    "LOW",
    "NEGATIVE",
    "NO",
    "NOT",
    "NOVELTY",
    "NULL",
    "ON",
    "ONLY",
    "OR",
    "OUTSIDE",
    "PASS",
    "PATIENT",
    "PENDING",
    "PREDICTION",
    "PROGRESSION",
    "PROVISIONAL",
    "RESULT",
    "REPORT",
    "README",
    "ROBUST",
    "RULE",
    "SUCCESSOR",
    "SUPPORTED",
    "TARGET",
    "TRANSFER",
    "VALIDATED",
    "VALIDATION",
    "WARNING",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def prose_blocks(markdown: str) -> list[tuple[int, str]]:
    blocks: list[tuple[int, str]] = []
    current: list[str] = []
    start_line = 1
    in_fence = False

    def flush() -> None:
        nonlocal current
        if current:
            blocks.append((start_line, " ".join(current)))
            current = []

    for line_number, raw in enumerate(markdown.splitlines(), start=1):
        stripped = raw.strip()
        if stripped.startswith("```"):
            flush()
            in_fence = not in_fence
            continue
        if in_fence or stripped.startswith("|"):
            flush()
            continue
        if not stripped:
            flush()
            continue
        standalone = bool(
            re.match(r"^(?:#{1,6}\s+|[-*+] |\d+\. )", stripped)
        )
        if standalone:
            flush()
        cleaned = re.sub(r"^#{1,6}\s+", "", stripped)
        cleaned = re.sub(r"^(?:[-*+] |\d+\. )", "", cleaned)
        cleaned = re.sub(r"^>\s?", "", cleaned)
        cleaned = LINK_RE.sub(r"\1", cleaned)
        cleaned = CLAIM_RE.sub("", cleaned)
        cleaned = cleaned.replace("`", "").replace("**", "").replace("__", "")
        if not current:
            start_line = line_number
        current.append(cleaned)
        if standalone:
            flush()
    flush()
    return blocks


def sentences(block: str) -> list[str]:
    candidates = [item.strip() for item in SENTENCE_RE.split(block) if item.strip()]
    return [item for item in candidates if WORD_RE.search(item)]


def percentile(values: list[int], quantile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * quantile
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def acronym_inventory(text: str) -> Counter[str]:
    tokens: Counter[str] = Counter()
    for raw in ACRONYM_RE.findall(text):
        for token in raw.split("/"):
            normalized = token.upper().strip("/-")
            if normalized:
                tokens[normalized] += 1
    return tokens


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    glossary_tokens = acronym_inventory((ONBOARDING / "GLOSSARY.md").read_text())

    metrics: list[dict[str, object]] = []
    long_rows: list[dict[str, object]] = []
    acronym_rows: list[dict[str, object]] = []
    failures: list[str] = []
    all_acronyms: Counter[str] = Counter()

    for filename in AUDIENCE_DOCS:
        path = ONBOARDING / filename
        if not path.is_file():
            failures.append(f"missing:{filename}")
            continue
        text = path.read_text(encoding="utf-8")
        blocks = prose_blocks(text)
        sentence_items: list[tuple[int, str]] = []
        paragraph_lengths: list[int] = []
        for line_number, block in blocks:
            words = WORD_RE.findall(block)
            paragraph_lengths.append(len(words))
            sentence_items.extend((line_number, item) for item in sentences(block))

        sentence_lengths = [len(WORD_RE.findall(item)) for _, item in sentence_items]
        word_count = sum(sentence_lengths)
        parenthetical_count = sum(item.count("(") for _, item in sentence_items)
        over_30 = sum(length > 30 for length in sentence_lengths)
        over_45 = sum(length > 45 for length in sentence_lengths)
        max_sentence = max(sentence_lengths, default=0)
        mean_sentence = word_count / len(sentence_lengths) if sentence_lengths else 0
        long_share = over_30 / len(sentence_lengths) if sentence_lengths else 0
        max_paragraph = max(paragraph_lengths, default=0)

        metrics.append(
            {
                "document": filename,
                "words_in_prose": word_count,
                "sentences": len(sentence_lengths),
                "mean_words_per_sentence": f"{mean_sentence:.1f}",
                "p90_words_per_sentence": f"{percentile(sentence_lengths, 0.9):.1f}",
                "max_words_per_sentence": max_sentence,
                "sentences_over_30_words": over_30,
                "sentences_over_45_words": over_45,
                "share_over_30": f"{long_share:.3f}",
                "max_paragraph_words": max_paragraph,
                "parenthetical_openings": parenthetical_count,
            }
        )

        for (line_number, item), length in zip(sentence_items, sentence_lengths):
            if length > 30:
                long_rows.append(
                    {
                        "document": filename,
                        "line": line_number,
                        "words": length,
                        "sentence": item,
                    }
                )

        acronyms = acronym_inventory(text)
        for token, count in sorted(acronyms.items()):
            normalized = token.upper().strip("/-")
            if VERSION_OR_CLAIM_RE.fullmatch(normalized):
                continue
            if normalized in NON_ACRONYM_CAPS:
                continue
            all_acronyms[normalized] += count
            acronym_rows.append(
                {
                    "document": filename,
                    "acronym": normalized,
                    "count": count,
                    "found_in_glossary": "yes" if normalized in glossary_tokens else "no",
                }
            )

        if mean_sentence > 26:
            failures.append(f"mean_sentence_over_26:{filename}:{mean_sentence:.1f}")
        if max_sentence > 65:
            failures.append(f"sentence_over_65:{filename}:{max_sentence}")
        if long_share > 0.18:
            failures.append(f"long_sentence_share_over_18pct:{filename}:{long_share:.3f}")
        if max_paragraph > 180:
            failures.append(f"paragraph_over_180:{filename}:{max_paragraph}")

    undefined = sorted(
        token
        for token in all_acronyms
        if token not in glossary_tokens and token not in {"FAQ", "ID", "URL"}
    )

    metrics_path = outdir / "document_metrics.tsv"
    with metrics_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=metrics[0].keys(), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(metrics)

    long_path = outdir / "long_sentences.tsv"
    with long_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("document", "line", "words", "sentence"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(sorted(long_rows, key=lambda row: int(row["words"]), reverse=True))

    acronym_path = outdir / "acronym_inventory.tsv"
    with acronym_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("document", "acronym", "count", "found_in_glossary"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(acronym_rows)

    summary = {
        "purpose": "V55 plain-language load audit; no scientific claim",
        "n_documents": len(metrics),
        "n_prose_words": sum(int(row["words_in_prose"]) for row in metrics),
        "n_sentences": sum(int(row["sentences"]) for row in metrics),
        "n_sentences_over_30_words": len(long_rows),
        "n_undefined_acronyms": len(undefined),
        "undefined_acronyms": undefined,
        "threshold_failures": failures,
        "overall_status": "PASS" if not failures and not undefined else "FAIL",
        "metrics": str(metrics_path.relative_to(ROOT)),
        "long_sentences": str(long_path.relative_to(ROOT)),
        "acronyms": str(acronym_path.relative_to(ROOT)),
        "interpretation": (
            "Maintenance signals only; thresholds do not prove comprehension "
            "and do not license removal of necessary scientific caveats."
        ),
    }
    (outdir / "plain_language_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    return 1 if args.fail_on_error and summary["overall_status"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
