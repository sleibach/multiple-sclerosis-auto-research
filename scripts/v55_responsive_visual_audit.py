#!/usr/bin/env python3
"""Audit V55 SVG fit and fallback requirements at constrained widths.

This is a communication check, not a scientific analysis. A visual can fit a
small viewport while its embedded labels become too small to read. The audit
therefore treats a linked full text equivalent as mandatory whenever scaled
normal text falls below 10 CSS pixels.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VISUAL_DIR = ROOT / "docs" / "onboarding" / "visuals"
VISUAL_INDEX = ROOT / "docs" / "onboarding" / "VISUAL_INDEX.md"
DEFAULT_OUTDIR = ROOT / "analysis" / "v55_responsive_visual_audit"
EXPECTED_VISUALS = (
    "CONTRIBUTOR_LIFECYCLE_V55.svg",
    "EVIDENCE_LANES_V55.svg",
    "MONITORING_LEAD_V55.svg",
    "OPEN_PROBLEM_BOARD_V55.svg",
    "RELAPSE_VS_PROGRESSION_V55.svg",
    "RESEARCH_EVOLUTION_V55.svg",
    "EVIDENCE_JOURNEY_V55.svg",
    "RESEARCH_MAP_V55.svg",
)
SCENARIOS = (
    ("mobile", 360, 328),
    ("tablet", 768, 704),
    ("print_portrait_model", 704, 672),
)
BROWSER_CANDIDATES = (
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
)
FONT_RE = re.compile(r"font:\s*\d+\s+([0-9.]+)px\b")
BODY_RE = re.compile(
    r'<body[^>]*data-ready="(?P<ready>[^"]+)"'
    r'[^>]*data-frame-width="(?P<frame>[^"]+)"'
    r'[^>]*data-image-width="(?P<image>[^"]+)"'
    r'[^>]*data-scroll-width="(?P<scroll>[^"]+)"'
    r'[^>]*data-viewport-width="(?P<viewport>[^"]+)"'
)


@dataclass(frozen=True)
class Check:
    visual: str
    scenario: str
    check: str
    status: str
    detail: str


@dataclass(frozen=True)
class Measurement:
    visual: str
    scenario: str
    viewport_css_px: int
    content_css_px: int
    native_width_px: int
    native_height_px: int
    scale: float
    native_min_font_px: float
    effective_min_font_px: float
    label_mode: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", help="Chrome/Chromium executable")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


def add(
    checks: list[Check],
    visual: str,
    scenario: str,
    name: str,
    passed: bool,
    detail: str,
) -> None:
    checks.append(
        Check(visual, scenario, name, "PASS" if passed else "FAIL", detail)
    )


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


def parse_visual(path: Path) -> tuple[int, int, float]:
    root = ET.parse(path).getroot()
    width = int(float((root.get("width") or "").removesuffix("px")))
    height = int(float((root.get("height") or "").removesuffix("px")))
    if width <= 0 or height <= 0:
        raise ValueError("non-positive canvas")
    fonts = [float(value) for value in FONT_RE.findall(path.read_text())]
    if not fonts:
        raise ValueError("no CSS pixel font declarations found")
    return width, height, min(fonts)


def index_section(index: str, filename: str) -> str:
    sections = re.split(r"(?m)^## ", index)
    return next((section for section in sections if filename in section), "")


def wrapper_markup(svg: Path, content_width: int) -> str:
    uri = svg.resolve().as_uri()
    return f"""<!doctype html>
<html><head><meta charset=\"utf-8\"><style>
html,body{{margin:0;padding:0}} body{{width:{content_width}px}}
#frame{{width:{content_width}px;max-width:100%;overflow:visible}}
img{{display:block;max-width:100%;height:auto}}
</style></head>
<body data-ready=\"0\" data-frame-width=\"0\" data-image-width=\"0\" data-scroll-width=\"0\" data-viewport-width=\"0\">
<div id=\"frame\"><img id=\"visual\" src=\"{html.escape(uri)}\" alt=\"test\"></div>
<script>
window.addEventListener('load', () => {{
  document.body.dataset.frameWidth = document.getElementById('frame').getBoundingClientRect().width;
  document.body.dataset.imageWidth = document.getElementById('visual').getBoundingClientRect().width;
  document.body.dataset.scrollWidth = document.documentElement.scrollWidth;
  document.body.dataset.viewportWidth = document.documentElement.clientWidth;
  document.body.dataset.ready = '1';
}});
</script></body></html>"""


def browser_measure(
    browser: str,
    wrapper: Path,
    viewport: int,
) -> tuple[bool, float, float, float, float, str]:
    result = subprocess.run(
        [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--hide-scrollbars",
            "--no-first-run",
            "--no-default-browser-check",
            f"--window-size={viewport},900",
            "--dump-dom",
            wrapper.resolve().as_uri(),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    match = BODY_RE.search(result.stdout)
    if result.returncode != 0 or not match:
        return False, 0.0, 0.0, 0.0, 0.0, result.stderr.strip()[-500:]
    values = match.groupdict()
    return (
        values["ready"] == "1",
        float(values["frame"]),
        float(values["image"]),
        float(values["scroll"]),
        float(values["viewport"]),
        result.stderr.strip()[-500:],
    )


def write_tsv(path: Path, rows: list[dict[str, object]], fields: tuple[str, ...]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    checks: list[Check] = []
    measurements: list[Measurement] = []

    try:
        browser = find_browser(args.browser)
        version = subprocess.run(
            [browser, "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.strip()
        add(checks, "__suite__", "all", "browser_available", True, version)
    except (FileNotFoundError, subprocess.SubprocessError) as exc:
        browser = ""
        version = "unavailable"
        add(checks, "__suite__", "all", "browser_available", False, str(exc))

    index = VISUAL_INDEX.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="v55-responsive-") as temp_name:
        tempdir = Path(temp_name)
        for visual in EXPECTED_VISUALS:
            path = VISUAL_DIR / visual
            add(
                checks,
                visual,
                "all",
                "source_exists",
                path.is_file(),
                str(path.relative_to(ROOT)),
            )
            if not path.is_file():
                continue
            section = index_section(index, visual)
            has_fallback = bool(section) and "**Text equivalent:**" in section
            add(
                checks,
                visual,
                "all",
                "full_text_equivalent",
                has_fallback,
                "nearby visible text equivalent" if has_fallback else "missing",
            )
            try:
                native_width, native_height, min_font = parse_visual(path)
                add(
                    checks,
                    visual,
                    "all",
                    "canvas_and_font_parse",
                    True,
                    f"{native_width}x{native_height}; native min font={min_font:.1f}px",
                )
            except (ET.ParseError, ValueError) as exc:
                add(checks, visual, "all", "canvas_and_font_parse", False, str(exc))
                continue

            for scenario, viewport, content_width in SCENARIOS:
                scale = min(1.0, content_width / native_width)
                effective = min_font * scale
                label_mode = (
                    "DIRECT_LABELS_OK"
                    if effective >= 10.0
                    else "TEXT_EQUIVALENT_REQUIRED"
                )
                measurements.append(
                    Measurement(
                        visual,
                        scenario,
                        viewport,
                        content_width,
                        native_width,
                        native_height,
                        round(scale, 4),
                        min_font,
                        round(effective, 2),
                        label_mode,
                    )
                )
                readable_or_fallback = effective >= 10.0 or has_fallback
                add(
                    checks,
                    visual,
                    scenario,
                    "label_delivery",
                    readable_or_fallback,
                    f"effective min font={effective:.2f}px; mode={label_mode}",
                )
                if not browser:
                    add(checks, visual, scenario, "browser_fit", False, "browser unavailable")
                    continue
                wrapper = tempdir / f"{Path(visual).stem}-{scenario}.html"
                wrapper.write_text(wrapper_markup(path, content_width), encoding="utf-8")
                (
                    ready,
                    frame_width,
                    image_width,
                    scroll_width,
                    actual_viewport,
                    stderr,
                ) = browser_measure(browser, wrapper, viewport)
                fits = (
                    ready
                    and image_width <= frame_width + 0.5
                    and scroll_width <= actual_viewport + 0.5
                )
                detail = (
                    f"ready={ready}; frame={frame_width:.1f}; image={image_width:.1f}; "
                    f"scroll={scroll_width:.1f}; requested_viewport={viewport}; "
                    f"actual_viewport={actual_viewport:.1f}"
                )
                if not fits and stderr:
                    detail += f"; stderr_tail={stderr}"
                add(
                    checks,
                    visual,
                    scenario,
                    "browser_fit",
                    fits,
                    detail,
                )

    media = [
        path
        for path in (ROOT / "docs" / "onboarding").rglob("*")
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".pdf"}
    ]
    add(
        checks,
        "__suite__",
        "all",
        "no_heavy_render_artifacts",
        not media,
        "none" if not media else ";".join(str(path.relative_to(ROOT)) for path in media),
    )

    check_rows = [asdict(row) for row in checks]
    measurement_rows = [asdict(row) for row in measurements]
    write_tsv(
        outdir / "responsive_visual_checks.tsv",
        check_rows,
        ("visual", "scenario", "check", "status", "detail"),
    )
    write_tsv(
        outdir / "responsive_visual_measurements.tsv",
        measurement_rows,
        (
            "visual",
            "scenario",
            "viewport_css_px",
            "content_css_px",
            "native_width_px",
            "native_height_px",
            "scale",
            "native_min_font_px",
            "effective_min_font_px",
            "label_mode",
        ),
    )
    failures = [row for row in checks if row.status == "FAIL"]
    fallback_count = sum(
        row.label_mode == "TEXT_EQUIVALENT_REQUIRED" for row in measurements
    )
    summary = {
        "purpose": "V55 constrained-width visual delivery audit; no scientific claim",
        "browser": version,
        "n_visuals": len(EXPECTED_VISUALS),
        "n_scenarios": len(SCENARIOS),
        "n_checks": len(checks),
        "n_fail": len(failures),
        "n_visual_scenarios_requiring_text_equivalent": fallback_count,
        "n_raster_or_pdf_outputs_committed": len(media),
        "overall_status": "PASS" if not failures else "FAIL",
        "interpretation": (
            "Fit does not imply label legibility. When scaled labels fall below "
            "10 CSS pixels, the nearby full text equivalent is required."
        ),
    }
    (outdir / "responsive_visual_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
    return 1 if args.fail_on_error and failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
