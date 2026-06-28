# V50 Public Citation And Description Card

Status: class-aware public-description guidance only. This card is not project
evidence, does not add a biological finding, does not alter any locked rule,
and does not move external context into the grounded corpus.

## Purpose

This card gives safe public wording for describing or citing the repository
after V50. The goal is to be accurate about the repository's breadth without
overclaiming novelty, validation, clinical readiness, or external consensus.

## One-Sentence Description

Use:

> A public, reproducible multiple-sclerosis computational research repository
> combining rerunnable project analyses, scored positive and negative findings,
> locked validation rules, synthetic method checks, and a separately
> provenance-labeled external-knowledge layer.

Do not use:

> The most comprehensive public MS knowledge base.

Reason: V50 did not prove a universal public-resource ranking. It found no
public 1:1 equivalent for this repo's integrated role, while recognizing that
resources such as MSGD, MSDA, MSBase, NARCOMS, GWAS Catalog, GEO/SRA/ENA, and
PubMed/Europe PMC are broader or deeper within their own domains.

## Short Abstract

Safe wording:

> This repository records an autonomous, auditable computational research
> program in multiple sclerosis. It preserves rerunnable analyses, negative
> lead closures, locked validation artifacts, synthetic method-characterization
> outputs, and current validation-readiness material. Since V47, externally read
> literature/database knowledge is stored in a separate provenance-governed
> layer and is never treated as project evidence unless independently grounded
> by a committed project analysis.

## Evidence Boundary Wording

Use this distinction every time:

| phrase | meaning | safe use |
|---|---|---|
| project-grounded | Produced by this repository's rerunnable analyses and governed by the locked-rule/null-testing discipline. | Use for `docs/`, `analysis/`, locked rules, validation plans, and scored findings. |
| external context | Read from public literature, databases, or resource metadata and segregated under `knowledge_external/`. | Use for source discovery, public-resource comparison, and convergence/contradiction surveillance. |
| externally corroborated context | A segregated source aligns with a project-grounded finding under a comparable definition. | Use as confidence-supporting context only; do not call it validation. |
| future grounding route | A source or claim that may be testable later if data or access is available. | Queue it; do not report it as a finding. |

## Citation-Like Reference

There is no DOI or peer-reviewed publication for the repository at V50. Use a
URL citation with an accessed date:

> Leibach, S. *multiple-sclerosis-auto-research*: public autonomous
> computational MS research repository. GitHub.
> https://github.com/sleibach/multiple-sclerosis-auto-research
> Accessed 2026-06-28.

If citing a specific result, cite the specific committed artifact instead of the
repository as a whole. Examples:

| purpose | cite this artifact |
|---|---|
| scored project findings | `docs/reports/FINDINGS_REPORT_V37.md` |
| V22 locked treatment-response rule | `docs/locked_rules/LOCKED_RULE_V22.md` |
| Gafson validation pre-registration | `docs/validation/PREREGISTRATION_V42.md` |
| V43 method-characterization | `docs/validation/POWER_MAP_V43.md`, `docs/validation/HARNESS_ROBUSTNESS_V43.md`, `docs/history/PIPELINE_SELF_AUDIT_V43.md` |
| public-data discovery boundary | `docs/history/JOINT_INFERENCE_V41.md` |
| external-resource comparison | `knowledge_external/synthesis/V50_PUBLIC_MS_KB_POSITION_CARD.md` |
| convergence/contradiction layer | `knowledge_external/synthesis/CONVERGENCE_CONTRADICTION_V50.md` |

## Claims That Are Safe

- The repository contains both positive and negative project results.
- The repository keeps locked rules and validation pre-registrations separate
  from later context.
- The V22 treatment-response scalar is provisional and validation-gated, not a
  clinical test.
- V41 concluded that unconstrained public-data discovery was exhausted under
  the repository's joint-inference gate.
- V47-V50 added a segregated external-knowledge layer with provenance checks.
- No public 1:1 equivalent was identified for this exact combination of
  rerunnable project corpus, negative ledger, validation machinery, and
  segregated external context.

## Claims To Avoid

- Do not say the repository has produced an intervention-grade MS target.
- Do not say the V22 rule is clinically validated.
- Do not say external literature validates the V22 scalar.
- Do not call external records project evidence.
- Do not say the repository is more comprehensive than MSGD, MSDA, MSBase,
  NARCOMS, GWAS Catalog, GEO/SRA/ENA, or PubMed in their own domains.
- Do not imply OpenGWAS-dependent routes are currently available while the JWT
  is expired.

## Provenance

This card summarizes wording boundaries from:

- `docs/knowledge/EPISTEMIC_CLASSES.md`
- `knowledge_external/synthesis/V50_PUBLIC_MS_KB_POSITION_CARD.md`
- `knowledge_external/synthesis/V50_PUBLIC_READER_PATH.md`
- `knowledge_external/synthesis/V50_CONTENT_HANDOFF.md`
- `docs/reports/FINDINGS_REPORT_V37.md`
- `docs/history/JOINT_INFERENCE_V41.md`
- `docs/validation/PREREGISTRATION_V42.md`

Date accessed: 2026-06-28.
