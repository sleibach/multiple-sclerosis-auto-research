# Repository Restructure Plan

Date: 2026-06-07

Scope: maintenance-only restructuring. No research analysis, no result changes, no locked-rule content changes.

## Safety Record

Pre-move inventory:

- `meta/REPO_INVENTORY_PRE.md`

## Target Layout

Root remains for entry points only:

- `README.md`
- `run_analysis.sh`
- `run_therapeutic_analysis.sh`
- `run_v2_analysis.sh`
- `run_v3_analysis.sh`
- `.gitignore`
- local non-project files such as `.env` and `.DS_Store`

Preserved existing canonical directories:

- `meta/`: live status, rulebooks, resume state, provisioning reports, session log.
- `knowledge/`: canonical knowledge and RAG index.
- `analysis/`: analysis outputs.
- `data/`: data inputs/manifests.
- `results/`, `results_v2/`, `results_v3/`: phase outputs.
- `scripts/`: reproducibility scripts.
- `subagents/`, `subagents_v3/`: subagent reports.
- `archive/`: historical archive.

New documentation directories:

- `docs/findings/`: finding, kill, final synthesis, mechanism map, transfer-validity, disagreement deliverables.
- `docs/locked_rules/`: locked rules and methodology locks.
- `docs/validation/`: validation ledgers, cohort searches, validation readiness.
- `docs/workups/genetics/`: genetics and QTL workups.
- `docs/workups/treatment_response/`: APC/HLA monitoring and coupled-axis workups.
- `docs/workups/microbiome/`: microbiome/data-search workups.
- `docs/roadmaps/`: roadmaps, plans, reframes, methodology plans.
- `docs/convergence/`: convergence checks.
- `docs/critiques/`: critique artifacts.
- `docs/lab_notebooks/`: lab notebooks.
- `docs/orchestration/`: orchestration and subagent coordination logs.
- `docs/history/`: early blockers, milestones, candidate register, older project notes.
- `docs/resources/`: sources, tools, data notes, novelty searches.
- `meta/queues/`: V23+ build/action queues.

## Reference Policy

Every moved root artifact must have references updated in Markdown and text files where practical. Locked artifacts may be moved but not rewritten except for path references to other moved artifacts in separate files. The locked files themselves are not edited during this restructure.

## Compatibility Policy

No compatibility symlink is created for every old root path because that would leave the root cluttered. Compatibility is maintained by:

1. updating canonical references in README/meta/knowledge/docs;
2. keeping `meta/REPO_INVENTORY_PRE.md` as a full old-path safety record;
3. preserving git history with `git mv`.
