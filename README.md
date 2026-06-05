# MS Auto-Research

An autonomous, reproducible computational search for a novel, falsifiable
therapeutic target in multiple sclerosis (MS) and the broader cross-autoimmune
mechanism landscape. The project runs in successive
phases (V1 through VN); each phase is preserved rather than overwritten so the
full reasoning trace stays auditable.

All analysis uses public human-tissue data only and random seed `20260526`
(V5 analyses use `20260528`).

## Current Status

The current phase is **V14**. The V4 directory structure remains canonical, and
V11 introduced the resume backbone for short-session continuity.

- Start here: `meta/CURRENT_STATUS.md` — the live mission state, active leads,
  and next actions.
- Current active genetics focus: robust workup of OpenGWAS-backed shared MS/UC
  and MS/Crohn loci, including LDSC genetic correlation, multi-signal coloc,
  causal-gene mapping, and effect-direction checks.
- Confirmed first-pass high-H4 regions from V13/V14 include MS-UC chr1,
  MS-UC chr5/PTGER4, MS-Crohn chr10, and MS-Crohn chr17/STAT3-STAT5. The
  chr1 and chr10 loci have passed bounded SuSiE-coloc follow-up; matrix grades
  are not upgraded until LDSC, sensitivity, and causal-gene layers are complete.
- `ACSL1`, `NAMPT`, and several early target candidates were demoted or parked
  under the V4/V5 prior-art and tiering framework. Current value has shifted to
  axis-disagreement mining and genetics-grounded transfer-validity analysis.

## How To Read This Repository

For a future agent or human picking this up, the canonical read order is:

1. `meta/CURRENT_STATUS.md`
2. `meta/PRIOR_ART_RULEBOOK.md`
3. `meta/TIERING_RULEBOOK.md`
4. `knowledge/candidates/INDEX.md`
5. `knowledge/dimensions/INDEX.md`
6. `meta/NEXT_ACTIONS.md`
7. `archive/ARCHIVE_INDEX.md`

## Standing Session Rule

Every session must end by appending a `RUN SUMMARY` block to
`meta/SESSION_LOG.md` and echoing the same block in the final chat response.
The block must include active runtime, UTC start/end timestamps, frontier
advanced, stop reason, and next action. This rule is also recorded at the top
of `meta/SESSION_LOG.md`.

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
| V5 | Tiered continuation on concrete leads (pregnancy axis, MIF/CD74 resolution, longitudinal dimension). | Produced concrete leads but no Tier 4 claim. |
| V6-V7 | APC response architecture as cross-disease treatment-response stratifier. | Narrow IBD response-monitoring signal survived; broad APC rule killed. |
| V8-V12 | MS-centered multi-axis mechanism map and axis-disagreement matrix. | Matrix completed; UC/Crohn/MS genetics and treatment-response disagreements became priority. |
| V13 | OpenGWAS-backed first-pass cross-trait colocalization for MS/UC/Crohn shared loci. | Four high-H4 regions identified; MHC overlaps mostly ruled distinct causal variants. |
| V14 | Robust workup of confirmed shared loci. | Tooling and LDSC reference panel provisioned; bounded SuSiE-coloc supports chr1 UC and chr10 Crohn loci. Active. |

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

Python environments currently used:

- `.venv`: Python 3.13 genetics tooling, including PyPI `ldsc` 2.0.1.
- `.venv_v3_py312`: local TF-IDF knowledge index tooling.

R genetics tooling:

- R 4.6.0
- `coloc` 5.2.3
- `susieR` 0.14.2

LDSC reference panel:

- Working DOI-stable source: Zenodo `10.5281/zenodo.14993076`
- Download URL: `https://zenodo.org/records/14993076/files/eur_w_ld_chr.tgz`
- Local archive: `data/raw/ldsc_reference/eur_w_ld_chr.tgz`
- Extracted panel: `data/raw/ldsc_reference/eur_w_ld_chr/`
- Archive MD5: `76c1890c8cf22d99d05c6707cc8441b4`
- Archive SHA-256:
  `0ac97e1c128ca5ba5dfd5858c736741b1544434924248027ae73725a9773311a`
- `w_hm3.snplist` is included in the extracted archive and has `1217312`
  lines including header.
- Reference-panel smoke test passed with `munge_sumstats.py` and `ldsc.py --h2`;
  details are in `meta/PROVISIONING_REPORT.md`.

## Honest Scope

This is a reproducible computational prioritization, not a validated mechanism,
a patient recommendation, or evidence of clinical efficacy. The analyses
establish associations and triage hypotheses in public human-tissue data; they
do not infer viral causation, cell-cell interaction without spatial/protein
follow-up, or therapeutic benefit.
