#!/usr/bin/env bash
set -euo pipefail

./.venv/bin/python scripts/v2_cross_autoimmune_bulk.py
if [[ -s phases/v2/results/acsl_family_inventory_summary.json ]]; then
  echo "Using cached phases/v2/results/acsl_family_inventory_summary.json"
else
  ./.venv/bin/python scripts/v2_acsl_family_inventory.py
fi
./.venv/bin/python scripts/v2_acsl1_mechanistic_simulations.py
./.venv/bin/python scripts/v2_acsl1_incremental_value.py
./.venv/bin/python scripts/v2_rank_successor_targets.py
if [[ -s phases/v2/results/nampt_feasibility_summary.json ]]; then
  echo "Using cached phases/v2/results/nampt_feasibility_summary.json"
else
  ./.venv/bin/python scripts/v2_nampt_feasibility.py
fi
./.venv/bin/python scripts/v2_extended_autoimmune_checks.py
if [[ -s phases/v2/results/prior_art_pubmed_counts.tsv ]]; then
  echo "Using cached phases/v2/results/prior_art_pubmed_counts.tsv"
else
  ./.venv/bin/python scripts/v2_prior_art_counts.py
fi
