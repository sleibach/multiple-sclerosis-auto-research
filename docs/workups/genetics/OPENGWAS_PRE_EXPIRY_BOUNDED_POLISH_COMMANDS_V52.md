# OpenGWAS Pre-Expiry Bounded Polish Commands V52

Date: 2026-07-10

Status: operational command list. This document defines the only genetics
commands worth running before the renewed OpenGWAS token expires. It does not
open broad discovery, change target verdicts, or add a new analysis claim.

## Token And Scope

`scripts/check_opengwas_access.py` verified the renewed `.env` token on
2026-07-10. The decoded expiry is `2026-07-24 08:00 UTC`.

Allowed OpenGWAS use in this window is limited to bounded, already-defined
checks that preserve the V41 public-data exhaustion boundary:

1. authentication and expiry checks;
2. confirmed-locus reruns already scripted under frozen windows;
3. exact locus bookkeeping for V52 handoff artifacts;
4. allele/LD hygiene needed for validation or collaborator handoff.

An auth failure before expiry is an operational blocker, not a genetics null.

## Commands To Prefer Before Expiry

Run from the repository root.

| priority | command | scope | expected output | interpretation |
|---:|---|---|---|---|
| 1 | `python3 scripts/check_opengwas_access.py` | Auth sentinel only; POST-only `gwasinfo` and `tophits` probes | terminal status; decoded expiry | Confirms the renewed token is active. Failure is an auth/service blocker, not a null. |
| 2 | `python3 scripts/v14_susie_coloc_confirmed_loci.py` | V14 confirmed windows only; POST-only LD matrix route where OpenGWAS is used | `analysis/v14_susie_coloc/susie_coloc_rollup.tsv` | Reproduces bounded coloc bookkeeping. It cannot nominate new loci or change target status by itself. |
| 3 | `python3 scripts/v19_chr1_reanalysis.py` | Local chr1 sources plus existing bounded chr1 artifacts | `analysis/v19_chr1_druggability/v19_chr1_reanalysis_summary.json`; `analysis/v19_chr1_druggability/kif21b_qtd_coloc_abf_summary.tsv` | Reproduces chr1 causal-gene/direction bookkeeping. It cannot promote GPR25 or KIF21B without genotype-linked cell-state and perturbation evidence. |
| 4 | `python3 scripts/v14_locus_landscape.py` | Existing V14 locus landscape only, if a table refresh is needed for reporting consistency | `analysis/v14_locus_landscape/` outputs | Reporting polish only. Do not expand the locus set. |

## Scripts Present But Not Pre-Approved For V52 Polish

The following scripts exist, but should not be run as a V52 pre-expiry polish
command unless a future queue item first defines a bounded, non-discovery
purpose and output contract.

| script | reason not pre-approved |
|---|---|
| `scripts/v13_opengwas_coloc_uc_crohn.py` | Earlier cross-disease coloc exploration; rerunning it risks broadening beyond the current therapeutic handoff unless a frozen reporting need is named. |
| `scripts/v13_annotate_coloc_regions.py` | Annotation support script; safe only as downstream reporting support for already-frozen regions. |
| `scripts/v21_next_tier_locus_susie.py` | Next-tier locus exploration belongs to the exhausted discovery era and is not part of V52 targeted re-examination. |

## Explicit Non-Commands

Do not use the renewed token for:

1. genome-wide tophit discovery;
2. new locus scans;
3. structure-guided target rescue;
4. tuning loci after seeing AlphaFold DB tractability context;
5. changing the V22 rule or V42/V44 validation plans;
6. promoting a closed lead because a bounded script still executes;
7. any OpenGWAS GET route.

## Lead-Specific Boundaries

| lead or route | allowed before expiry | not allowed |
|---|---|---|
| Bounded APC/HLA-II monitoring scalar | none needed beyond auth hygiene; validation is external-data gated | do not use genetics access to tune the scalar |
| chr1 KIF21B/GPR25 | rerun `scripts/v19_chr1_reanalysis.py` if a fresh handoff table is needed | no target promotion without genotype-linked cell-state and perturbation data |
| ZMIZ1 | bounded direction table polish if a frozen script is written first | no target framing from cross-disease direction alone |
| PTGER4 | signal-specific manifest polish only if a frozen script is written first | no naive GPCR tractability rescue |
| validation handoff | exact LD/allele checks only if required by a frozen package | no discovery or post-hoc validation tuning |

## Practical Schedule

Before `2026-07-24 08:00 UTC`:

1. Run `scripts/check_opengwas_access.py` at the start of any genetics-facing
   session.
2. If one bounded polish rerun is worth spending time on, prefer
   `scripts/v14_susie_coloc_confirmed_loci.py`; it is the broadest already-
   bounded reproducibility check.
3. Rerun `scripts/v19_chr1_reanalysis.py` only when updating chr1 handoff
   tables or collaborator material.
4. If the token expires, route around OpenGWAS and record the blocker. Do not
   report missing API output as biology.

## Therapeutic Consequence

The renewed token creates a short operational window for bounded genetics
bookkeeping. It does not change the V52 therapeutic conclusion: monitoring /
stratification remains the defensible near-term route, and all target routes
remain gated by causal-gene, direction, cell-state, perturbation, and modality
evidence.

