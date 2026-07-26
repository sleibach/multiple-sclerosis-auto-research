#!/usr/bin/env python3
"""Headlessly render V55 onboarding SVGs without retaining raster media.

This is a presentation regression check, not a scientific analysis. It parses
the declared SVG canvas, renders each file in an isolated temporary browser
profile, validates the PNG header/dimensions, and commits only lightweight
machine-readable results.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import signal
import shutil
import struct
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
VISUAL_DIR = ROOT / "docs" / "onboarding" / "visuals"
DEFAULT_OUTDIR = ROOT / "analysis" / "v55_visual_render_regression"
EXPECTED_VISUALS = (
    "EVIDENCE_LANES_V55.svg",
    "MONITORING_LEAD_V55.svg",
    "OPEN_PROBLEM_BOARD_V55.svg",
    "RELAPSE_VS_PROGRESSION_V55.svg",
    "RESEARCH_MAP_V55.svg",
)
BROWSER_CANDIDATES = (
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
)


@dataclass(frozen=True)
class Canvas:
    width: int
    height: int


@dataclass(frozen=True)
class RenderResult:
    returncode: int
    stderr: str
    output_ready: bool
    elapsed_seconds: float
    terminated_after_output: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--browser", help="Chrome/Chromium executable")
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--fail-on-error", action="store_true")
    return parser.parse_args()


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
    raise FileNotFoundError(
        "No Chrome/Chromium executable found; pass --browser explicitly"
    )


def integer_dimension(value: str | None, field: str, path: Path) -> int:
    if value is None:
        raise ValueError(f"{path}: missing SVG {field}")
    stripped = value.removesuffix("px")
    numeric = float(stripped)
    if numeric <= 0 or not numeric.is_integer():
        raise ValueError(f"{path}: {field} must be a positive integer canvas")
    return int(numeric)


def parse_canvas(path: Path) -> Canvas:
    root = ElementTree.parse(path).getroot()
    width = integer_dimension(root.get("width"), "width", path)
    height = integer_dimension(root.get("height"), "height", path)
    viewbox = root.get("viewBox", "").split()
    if len(viewbox) != 4:
        raise ValueError(f"{path}: viewBox must contain four values")
    x, y, box_width, box_height = map(float, viewbox)
    if x != 0 or y != 0 or box_width != width or box_height != height:
        raise ValueError(
            f"{path}: viewBox {viewbox} does not match {width}x{height} canvas"
        )
    return Canvas(width=width, height=height)


def png_dimensions(path: Path) -> Canvas:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: browser output is not a PNG")
    if header[12:16] != b"IHDR":
        raise ValueError(f"{path}: PNG has no leading IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    return Canvas(width=width, height=height)


def render(
    browser: str,
    svg_path: Path,
    canvas: Canvas,
    png_path: Path,
    profile_dir: Path,
) -> RenderResult:
    command = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--disable-extensions",
        "--disable-background-networking",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        "--force-device-scale-factor=1",
        f"--user-data-dir={profile_dir}",
        f"--window-size={canvas.width},{canvas.height}",
        f"--screenshot={png_path}",
        svg_path.resolve().as_uri(),
    ]
    stderr_path = png_path.with_suffix(".stderr.txt")
    started = time.monotonic()
    output_ready = False
    terminated_after_output = False
    with stderr_path.open("wb") as stderr_handle:
        process = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=stderr_handle,
            start_new_session=True,
        )
        deadline = started + 30
        previous_size = -1
        stable_since: float | None = None
        while time.monotonic() < deadline:
            now = time.monotonic()
            if png_path.is_file():
                current_size = png_path.stat().st_size
                if current_size >= 4096 and current_size == previous_size:
                    stable_since = stable_since or now
                    if now - stable_since >= 0.5:
                        output_ready = True
                        break
                else:
                    previous_size = current_size
                    stable_since = None
            if process.poll() is not None:
                output_ready = png_path.is_file() and png_path.stat().st_size >= 4096
                break
            time.sleep(0.1)

        if process.poll() is None:
            terminated_after_output = output_ready
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=5)
        returncode = process.returncode

    stderr = stderr_path.read_text(encoding="utf-8", errors="replace").strip()
    return RenderResult(
        returncode=returncode,
        stderr=stderr,
        output_ready=output_ready,
        elapsed_seconds=time.monotonic() - started,
        terminated_after_output=terminated_after_output,
    )


def add_check(
    checks: list[dict[str, str]],
    visual: str,
    check: str,
    passed: bool,
    detail: str,
) -> None:
    checks.append(
        {
            "visual": visual,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail.replace("\n", " ")[:1000],
        }
    )


def main() -> int:
    args = parse_args()
    outdir = args.outdir if args.outdir.is_absolute() else ROOT / args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    checks: list[dict[str, str]] = []

    try:
        browser = find_browser(args.browser)
        browser_version = subprocess.run(
            [browser, "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.strip()
        add_check(checks, "__suite__", "browser_available", True, browser_version)
    except (FileNotFoundError, subprocess.SubprocessError) as exc:
        add_check(checks, "__suite__", "browser_available", False, str(exc))
        browser = ""
        browser_version = "unavailable"

    with tempfile.TemporaryDirectory(prefix="v55-svg-render-") as temp_name:
        tempdir = Path(temp_name)
        for index, filename in enumerate(EXPECTED_VISUALS):
            svg_path = VISUAL_DIR / filename
            if not svg_path.is_file():
                add_check(checks, filename, "source_exists", False, str(svg_path))
                continue
            add_check(checks, filename, "source_exists", True, str(svg_path))

            try:
                canvas = parse_canvas(svg_path)
                add_check(
                    checks,
                    filename,
                    "canvas_valid",
                    True,
                    f"{canvas.width}x{canvas.height}; matching viewBox",
                )
            except (ElementTree.ParseError, ValueError) as exc:
                add_check(checks, filename, "canvas_valid", False, str(exc))
                continue

            if not browser:
                add_check(
                    checks,
                    filename,
                    "browser_render",
                    False,
                    "browser unavailable",
                )
                continue

            png_path = tempdir / f"{Path(filename).stem}.png"
            profile_dir = tempdir / f"profile-{index}"
            result = render(browser, svg_path, canvas, png_path, profile_dir)
            rendered = result.output_ready and png_path.is_file()
            detail = (
                f"returncode={result.returncode}; "
                f"elapsed={result.elapsed_seconds:.2f}s; "
                f"terminated_after_output={result.terminated_after_output}; "
                f"stderr_present={bool(result.stderr)}"
            )
            add_check(checks, filename, "browser_render", rendered, detail)
            if not rendered:
                continue

            size = png_path.stat().st_size
            add_check(
                checks,
                filename,
                "render_nontrivial",
                size >= 4096,
                f"temporary PNG bytes={size}",
            )
            try:
                raster = png_dimensions(png_path)
                dimensions_match = raster == canvas
                add_check(
                    checks,
                    filename,
                    "render_dimensions",
                    dimensions_match,
                    f"expected={canvas.width}x{canvas.height}; "
                    f"actual={raster.width}x{raster.height}",
                )
            except ValueError as exc:
                add_check(checks, filename, "render_dimensions", False, str(exc))

            digest = hashlib.sha256(png_path.read_bytes()).hexdigest()
            add_check(
                checks,
                filename,
                "render_fingerprint",
                True,
                f"sha256={digest}; raster intentionally deleted after test",
            )

    checks_path = outdir / "visual_render_checks.tsv"
    with checks_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("visual", "check", "status", "detail"),
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(checks)

    failures = [row for row in checks if row["status"] == "FAIL"]
    summary = {
        "purpose": "V55 browser-render regression; no scientific claim",
        "browser": browser_version,
        "n_expected_visuals": len(EXPECTED_VISUALS),
        "n_checks": len(checks),
        "n_fail": len(failures),
        "raster_outputs_committed": 0,
        "overall_status": "PASS" if not failures else "FAIL",
        "checks": str(checks_path.relative_to(ROOT)),
    }
    summary_path = outdir / "visual_render_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 1 if args.fail_on_error and failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
