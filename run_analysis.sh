#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r environment/requirements.txt
.venv/bin/python scripts/download_data.py
.venv/bin/python scripts/analyze.py
