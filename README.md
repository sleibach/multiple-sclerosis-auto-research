# MS Auto-Research

An autonomous, reproducible computational search for a novel, falsifiable
therapeutic target in multiple sclerosis (MS) and the broader cross-autoimmune
lipid-lysosomal inflammatory myeloid program. The project runs in successive
phases (V1 through VN); each phase is preserved rather than overwritten so the
full reasoning trace stays auditable.

All analysis uses public human-tissue data only and random seed `20260526`
(V5 analyses use `20260528`).

## Current Status

The current phase is **V5** (V4 directory structure remains canonical). No
finding has yet satisfied the strict Definition of Done, and several candidates
have been explicitly demoted on evidence.

- Start here: `meta/CURRENT_STATUS.md` — the live mission state, active leads,
  and next actions.
- Active leads: a pregnancy/postpartum natural-experiment axis (Tier 1) and
  ongoing prior-art recalibration of earlier candidates.
- Demoted on evidence: `ACSL1`, `NAMPT`, `MIF/CD74`, `TYK2`, `IFI30/GILT`,
  `TREM2`, `LRRK2`, and others (see `knowledge/candidates/INDEX.md`).
- The strongest reproducible biological signal remains a cross-autoimmune
  lipid-lysosomal / antigen-processing / inflammatory myeloid module, which has
  not yet yielded a promotable, druggable, novel intervention point.

## How To Read This Repository

For a future agent or human picking this up, the canonical read order is:

1. `meta/CURRENT_STATUS.md`
2. `meta/PRIOR_ART_RULEBOOK.md`
3. `meta/TIERING_RULEBOOK.md`
4. `knowledge/candidates/INDEX.md`
5. `knowledge/dimensions/INDEX.md`
6. `archive/ARCHIVE_INDEX.md`

## Repository Layout

| Path | Contents |
|---|---|
| `meta/` | Live status, roadmaps, rulebooks (prior-art and tiering), and convergence checks for the current phase. |
| `knowledge/` | Canonical distilled knowledge: per-candidate histories (`candidates/`), evidence dimensions (`dimensions/`), mechanism hypotheses (`mechanisms/`), dataset/tool registries, and an append-only decision log (`decisions/`). |
| `analysis/` | Tiered analyses (`tier_0_triage/`, `tier_1_mechanism/`) for the current phase, each with a `REPORT.md` and decision artifacts. |
| `results/`, `results_v2/`, `results_v3/` | Per-phase analysis outputs (TSV/JSON/reports). |
| `scripts/` | Analysis scripts; `v3_*.py` are the V3 wave scripts. |
| `subagents/`, `subagents_v3/` | Specialist subagent reports. |
| `data/` | `raw*/` (downloaded public inputs, Git-ignored) and `derived*/` (computed tables, manifests, and SHA-256 hashes). |
| `archive/` | Index and pointers freezing the V1–V3 phases as historical. |

## Phase History

| Phase | Question | Outcome |
|---|---|---|
| V1 | Does a 4-1BB costimulation score (`TNFRSF9`/`TNFSF9`) track a lipid/complement microglial program in human MS lesions? | Constrained association test executed; see `MS_RESEARCH_LOG_2026-05-26.md`, `SELECTION.md`. |
| V2 | Can a single MS lipid-handling target (`ACSL1`) be promoted to a therapeutic claim? | No finding survived. `ACSL1` demoted to marker; `NAMPT` prior-art-blocked. See `FINDING_EXECUTION_PHASE.md`, `EXHAUSTION.md`. |
| V3 | What node or state transition in the cross-autoimmune lipid-lysosomal myeloid module is a druggable intervention point? | 170+ waves; no candidate met the Definition of Done. See `PLAN_V3.md`, `REFRAME_V3.md`, `LAB_NOTEBOOK_V3.md`. |
| V4 | Same question, under stricter prior-art and tiering rulebooks. | Reorganized knowledge into `knowledge/` + `meta/`; tiered triage. |
| V5 | Tiered continuation on concrete leads (pregnancy axis, MIF/CD74 resolution, longitudinal dimension). | Active. See `meta/CURRENT_STATUS.md`. |

`FINDING.md` documents the (since-demoted) `ACSL1` target hypothesis from an
earlier phase and is retained for the historical trace.

## Reproducibility

Each phase has its own entry point at the repository root:

```bash
./run_analysis.sh            # V1
./run_therapeutic_analysis.sh # ACSL1-phase analysis
./run_v2_analysis.sh         # V2
./run_v3_analysis.sh         # V3
```

Each script provisions a virtual environment, installs pinned dependencies,
downloads public inputs, records SHA-256 hashes, and runs the phase analysis.
Expected input URLs, sizes, and hashes are recorded in the per-phase data
manifests under `data/derived*/` and `data/manifest.tsv`.

Python environment for current work: `.venv_v3_py312`.

## Honest Scope

This is a reproducible computational prioritization, not a validated mechanism,
a patient recommendation, or evidence of clinical efficacy. The analyses
establish associations and triage hypotheses in public human-tissue data; they
do not infer viral causation, cell-cell interaction without spatial/protein
follow-up, or therapeutic benefit.
