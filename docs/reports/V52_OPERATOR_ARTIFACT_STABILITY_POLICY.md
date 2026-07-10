# V52 Operator Artifact Stability Policy

Date: 2026-07-10

Status: operational policy. This document adds no evidence, changes no locked
rule, and authorizes no new validation or target work. It defines when a V52
operator artifact should be hash-frozen, intentionally mutable, context-only, or
excluded from the stable operator SHA256 snapshot.

## Classes

| class | definition | hash-snapshot handling |
|---|---|---|
| stable operator control | artifact that directly controls package intake, routing, command order, required fields, result classes, or route-specific interpretation | include in `docs/reports/V52_OPERATOR_ARTIFACT_HASH_SNAPSHOT.tsv` |
| stable operator template | blank result shell, communication shell, checklist, or command note that should not drift silently before use | include unless it is explicitly marked draft |
| bounded command artifact | documented command sequence for a bounded, pre-approved rerun or auth-sensitive operation | include if future operators depend on exact commands |
| navigation index | artifact that primarily links, groups, or points to other artifacts | optional; include if the index is part of the handoff packet, exclude if it is expected to be regenerated often |
| live status/dashboard | artifact expected to change after real package receipt, validation result, or route-status update | do not include; require a decision log instead |
| synthesis/context report | explanatory report that helps interpretation but does not itself control package execution | exclude unless the report is explicitly promoted to an operator control |
| segregated external or structure context | external, structural-prediction, or literature context records | exclude from operator snapshot; governed by provenance or structural gates instead |
| synthetic fixture output | seeded or synthetic method-behavior output | exclude from operator snapshot unless used as a required regression fixture |
| self-referential snapshot | the hash snapshot itself | exclude; hashing it would create unstable self-drift |

## Inclusion Rule

Add an artifact to the stable hash snapshot when all of the following hold:

1. it can change an operator's package-routing, validation, target-handoff, or
   wording decision;
2. a silent edit would create avoidable post-hoc freedom or operator drift;
3. the artifact is small, text-based, and safe to commit;
4. the artifact is not expected to update after every real package result.

## Exclusion Rule

Do not add an artifact to the snapshot when any of the following hold:

1. it is a live dashboard or queue;
2. it is regenerated binary/index state;
3. it is the snapshot itself;
4. it is external or structural context governed by a different class gate;
5. it is a high-level synthesis that does not control package execution.

## Update Procedure

When a stable operator artifact is intentionally edited:

1. inspect the diff and confirm the edit is deliberate;
2. update the snapshot hash with
   `docs/reports/V52_OPERATOR_ARTIFACT_HASH_REFRESH_COMMANDS.md`;
3. verify with `docs/reports/V52_OPERATOR_ARTIFACT_HASH_VERIFY_COMMANDS.md`;
4. commit the artifact edit and snapshot refresh together.

## Current Policy Consequence

The chr1 wrong-direction control checklist is hash-covered because it changes
how future perturbation packages are interpreted. Route-status dashboards remain
mutable because they are expected to change after real outcomes. The snapshot
does not hash itself. External and AlphaFold DB context stay under their own
provenance and structural gates.
