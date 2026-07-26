#!/usr/bin/env python3
"""Verify the V55 collaborator brief prints to one A4 page.

The generated PDF is temporary and is never project evidence or a committed
artifact. This audit checks communication layout and local navigation only.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import signal
import shutil
import subprocess
import tempfile
import time
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
BRIEF = ROOT / "docs" / "onboarding" / "COLLABORATOR_BRIEF_V55.html"
LINEAR = ROOT / "docs" / "onboarding" / "COLLABORATOR_BRIEF_V55.md"
DEFAULT_OUTDIR = ROOT / "analysis" / "v55_print_brief_audit"
BROWSER_CANDIDATES = (
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
)
PAGE_RE = re.compile(rb"/Type\s*/Page\b")
REQUIRED_PHRASES = (
    "One live route",
    "No target",
    "No progression result",
    "Data next",
    "not a selector, target, clinical test, or cure",
    "Do not re-propose these shortcuts",
    "A useful idea has seven parts",
    "Communication only; no new scientific claim",
)


@dataclass(frozen=True)
class Check:
    check: str
    status: str
    detail: str


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        values = dict(attrs)
        if values.get("href"):
            self.hrefs.append(values["href"] or "")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", help="Chrome/Chromium executable")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def add(checks: list[Check], name: str, passed: bool, detail: str) -> None:
    checks.append(Check(name, "PASS" if passed else "FAIL", detail))


def find_browser(explicit: str | None) -> str:
    candidates = (explicit,) if explicit else BROWSER_CANDIDATES
    for candidate in candidates:
        if not candidate:
            continue
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
        path = Path(candidate)
        if path.is_file() and path.stat().st_mode & 0o111:
            return str(path)
    raise FileNotFoundError("No Chrome/Chromium executable found")


def print_pdf(
    browser: str,
    pdf: Path,
    profile: Path,
) -> tuple[bool, int, bool, str]:
    command = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--disable-extensions",
        "--disable-background-networking",
        "--no-first-run",
        "--no-default-browser-check",
        "--no-pdf-header-footer",
        f"--user-data-dir={profile}",
        f"--print-to-pdf={pdf}",
        BRIEF.resolve().as_uri(),
    ]
    stderr_path = pdf.with_suffix(".stderr.txt")
    ready = False
    terminated_after_output = False
    with stderr_path.open("wb") as stderr_handle:
        process = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=stderr_handle,
            start_new_session=True,
        )
        deadline = time.monotonic() + 30
        previous_size = -1
        stable_since: float | None = None
        while time.monotonic() < deadline:
            now = time.monotonic()
            if pdf.is_file():
                current_size = pdf.stat().st_size
                if current_size >= 10_000 and current_size == previous_size:
                    stable_since = stable_since or now
                    if now - stable_since >= 0.5:
                        ready = True
                        break
                else:
                    previous_size = current_size
                    stable_since = None
            if process.poll() is not None:
                ready = pdf.is_file() and pdf.stat().st_size >= 10_000
                break
            time.sleep(0.1)

        if process.poll() is None:
            terminated_after_output = ready
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=5)
        returncode = process.returncode or 0
    stderr = stderr_path.read_text(errors="replace") if stderr_path.exists() else ""
    return ready, returncode, terminated_after_output, stderr


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    checks: list[Check] = []

    add(checks, "html_exists", BRIEF.is_file(), str(BRIEF.relative_to(ROOT)))
    add(
        checks,
        "linear_equivalent_exists",
        LINEAR.is_file(),
        str(LINEAR.relative_to(ROOT)),
    )
    if not BRIEF.is_file():
        html_text = ""
    else:
        html_text = BRIEF.read_text(encoding="utf-8")
    add(checks, "html_under_100kb", len(html_text.encode()) < 100_000, f"bytes={len(html_text.encode())}")
    add(checks, "language_declared", '<html lang="en">' in html_text, "lang=en")
    add(checks, "viewport_declared", 'name="viewport"' in html_text, "responsive viewport")
    add(checks, "a4_print_rule", "@page { size: A4 portrait;" in html_text, "A4 portrait")
    add(checks, "print_media_rule", "@media print" in html_text, "print CSS present")
    for phrase in REQUIRED_PHRASES:
        add(checks, "required_boundary_phrase", phrase in html_text, phrase)

    parser = LinkParser()
    parser.feed(html_text)
    local_links = [
        href
        for href in parser.hrefs
        if not href.startswith(("http://", "https://", "mailto:", "#"))
    ]
    for href in local_links:
        target = unquote(href.partition("#")[0])
        resolved = (BRIEF.parent / target).resolve()
        add(checks, "local_link_resolves", resolved.exists(), href)

    browser = ""
    browser_version = "unavailable"
    try:
        browser = find_browser(args.browser)
        browser_version = subprocess.run(
            [browser, "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.strip()
        add(checks, "browser_available", True, browser_version)
    except (FileNotFoundError, subprocess.SubprocessError) as exc:
        add(checks, "browser_available", False, str(exc))

    page_count = 0
    pdf_bytes = 0
    if browser and BRIEF.is_file():
        with tempfile.TemporaryDirectory(prefix="v55-print-brief-") as temp_name:
            tempdir = Path(temp_name)
            pdf = tempdir / "collaborator_brief.pdf"
            profile = tempdir / "profile"
            produced, returncode, terminated_after_output, stderr = print_pdf(
                browser, pdf, profile
            )
            detail = (
                f"returncode={returncode}; "
                f"terminated_after_output={terminated_after_output}"
            )
            if not produced and stderr:
                detail += f"; stderr_tail={stderr}"
            add(
                checks,
                "temporary_pdf_created",
                produced,
                detail,
            )
            if produced:
                content = pdf.read_bytes()
                pdf_bytes = len(content)
                page_count = len(PAGE_RE.findall(content))
                add(checks, "temporary_pdf_nontrivial", pdf_bytes >= 10_000, f"bytes={pdf_bytes}")
                add(checks, "prints_to_one_page", page_count == 1, f"pages={page_count}")

    retained = [
        path
        for path in (ROOT / "docs" / "onboarding").rglob("*")
        if path.is_file() and path.suffix.lower() in {".pdf", ".png", ".jpg", ".jpeg", ".webp"}
    ]
    add(
        checks,
        "no_print_output_committed",
        not retained,
        "none" if not retained else ";".join(str(path.relative_to(ROOT)) for path in retained),
    )

    with (outdir / "print_brief_checks.tsv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check", "status", "detail"),
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(asdict(row) for row in checks)
    failures = [row for row in checks if row.status == "FAIL"]
    summary = {
        "purpose": "V55 one-page collaborator brief print audit; no scientific claim",
        "browser": browser_version,
        "n_checks": len(checks),
        "n_fail": len(failures),
        "printed_page_count": page_count,
        "temporary_pdf_bytes": pdf_bytes,
        "pdf_or_raster_outputs_committed": len(retained),
        "overall_status": "PASS" if not failures else "FAIL",
        "interpretation": (
            "Layout verification only. The HTML and linear Markdown brief remain "
            "communication artifacts and do not change evidence status."
        ),
    }
    (outdir / "print_brief_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 1 if args.fail_on_error and failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
