# V30 Queue

Date: 2026-06-07

## Status

- OpenGWAS access verified after loading `.env`: HTTP 200; token valid until
  2026-06-19 12:28 UTC.
- `SAP_AI_CORE_API_KEY` is present and parses as SAP AI Core service-key JSON.
- OAuth client-credentials token exchange works.
- Deployment listing works for resource group `default`.
- Gemini native inference works through SAP AI Core.
- Anthropic Claude deployments are discoverable and running, but inference is
  blocked by unresolved allowed-subpath/schema mapping.
- Mistral deployment is discoverable and running, but the OpenAI-style
  `/chat/completions` request with required `model` field timed out in V30.

## Executed

1. Implement reusable client at `scripts/sap_ai_core_client.py`.
2. Smoke-test Gemini `gemini-3.1-flash-lite` and `gemini-2.5-pro`.
3. Send V29 independent-review package to Gemini 2.5 Pro as a single
   independent-lens proposal generator.

## Remaining

1. Resolve Claude request schema for SAP AI Core Anthropic deployments.
2. Resolve Mistral timeout or request schema.
3. Re-run the V29 package across at least two genuinely different model
   lineages once Claude or Mistral is working.
4. Ground any concrete model proposals against local data before promotion.

## Next First Action

If resuming before V30 is complete, read `meta/SAP_AI_CORE_ACCESS_V30.md`, then
inspect the failed Claude/Mistral endpoint attempts and continue model-schema
resolution before claiming multi-lineage review.
