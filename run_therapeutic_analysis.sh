#!/usr/bin/env bash
set -euo pipefail

./.venv/bin/python scripts/download_therapeutic_data.py
./.venv/bin/python scripts/screen_lesion_multiomics.py
Rscript scripts/analyze_egln1_gse301908.R
Rscript scripts/screen_mims2_proteome_convergence.R
./.venv/bin/python scripts/analyze_spatial_convergent_candidates.py
./.venv/bin/python scripts/design_acsl1_falsification.py
