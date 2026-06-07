# V31 Queue

Date: 2026-06-07

## Status

- OpenGWAS verified after `.env` load: HTTP 200; token valid until
  2026-06-19 12:28 UTC.
- SAP AI Core service-key auth works.
- Deployment discovery works.
- Gemini native inference works.
- Claude 4.7 Opus works through SAP AI Core Orchestration using the
  `defaultOrchestrationConfig` deployment `d65236404bbfb6b2` and model
  deployment `def854013c7ac379`.
- Mistral remains non-blocking: discoverable but timed out again on
  `/chat/completions`.

## Executed

1. Extended `scripts/sap_ai_core_client.py` to route Anthropic models through
   the orchestration deployment.
2. Smoke-tested Claude 4.7 Opus and Gemini 2.5 Pro from the committed client.
3. Ran the independent review package against Claude and Gemini.
4. Parsed both model outputs into:
   - `analysis/v31_multi_lineage_review/claude_opus_review.parsed.json`
   - `analysis/v31_multi_lineage_review/gemini_2_5_pro_review.parsed.json`
5. Ran fast local groundings:
   - cross-cohort transfer of the bounded V22 scalar;
   - DICE chr1 candidate/credible-set eQTL hit scan;
   - V26 shared-module overlap audit.

## Remaining Queue

1. Dedicated raw-expression pathway scoring:
   - metabolic/glycolysis/OXPHOS confounding;
   - generic inflammatory response;
   - glucocorticoid and IFN-suppression signatures;
   - STAT1-axis reduction of V26/V22.
2. Steroid-pulse mimic data scout: find public pre/post high-dose steroid MS
   relapse transcriptomic data before any validation.
3. Partitioned LDSC heritability for the V22 APC/HLA-II module gene windows.
4. Optional V26 normalization sensitivity: rerun V26 PC1/cosine tests under
   column-wise/no-normalization variants.
5. Optional eQTLGen trans/pathway analysis for the chr1 KIF21B lead SNP if
   genome-wide trans-eQTL summary data is reachable.

## Next First Action

Run a focused V32 raw-expression confounder analysis on the treatment-response
cohorts: compute metabolic, inflammatory, glucocorticoid, IFN-suppression, and
STAT1 scores on the same samples used by V22/V23, compare AUCs against the
locked scalar, and residualize the scalar where possible.
