# SAP AI Core Access V30

Date: 2026-06-07

## Credential Handling

`SAP_AI_CORE_API_KEY` is present in `.env` and parses as SAP AI Core service-key
JSON. The key is not committed or printed.

Observed non-secret credential shape:

- top-level keys: `appname`, `clientid`, `clientsecret`, `credential-type`,
  `identityzone`, `identityzoneid`, `serviceurls`, `url`
- auth host: `adesso-ai-nu15vkd3.authentication.eu10.hana.ondemand.com`
- AI API host: `api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com`
- AI API URL source: `serviceurls.AI_API_URL`

OAuth2 client-credentials exchange works:

- token URL: `<credential url>/oauth/token`
- method: `POST`
- auth: HTTP Basic using `clientid:clientsecret`
- body: `grant_type=client_credentials`
- result: HTTP 200; bearer token returned; `expires_in = 43199`

## Reusable Client

Committed client:

- `scripts/sap_ai_core_client.py`

Supported commands:

```bash
python3 scripts/sap_ai_core_client.py inspect
python3 scripts/sap_ai_core_client.py list-deployments
python3 scripts/sap_ai_core_client.py smoke --model gemini-3.1-flash-lite
python3 scripts/sap_ai_core_client.py prompt --model gemini-2.5-pro --prompt-file PROMPT.md --output OUT.md
```

The client reads credentials from `.env` / environment only and does not print
the service key, client secret, or bearer token.

## Deployment Discovery

Deployment listing endpoint:

- `GET $AI_API_URL/v2/lm/deployments`
- header: `Authorization: Bearer <token>`
- header: `AI-Resource-Group: default`

Result: HTTP 200, 14 deployments.

Key deployments discovered:

| Model | Version | Deployment ID | Status |
|---|---:|---|---|
| `anthropic--claude-4.7-opus` | `1` | `def854013c7ac379` | `RUNNING` |
| `anthropic--claude-4.5-sonnet` | `1` | `dcd30525bfda8fce` | `RUNNING` |
| `anthropic--claude-4.5-sonnet` | `1` | `d7a00de1a8864952` | `RUNNING` |
| `gemini-3.1-flash-lite` | `001` | `dcb4db8a86040bf7` | `RUNNING` |
| `gemini-2.5-pro` | `001` | `d6dc532885507ac7` | `RUNNING` |
| `mistralai--mistral-medium-instruct` | `2505` | `d82893e976f5d7a9` | `RUNNING` |
| `sonar-pro` | `perplexity-us` | `ddf7690e789a089f` | `RUNNING` |
| `gpt-5.5` | `2026-04-24` | `dd73882a3073c9fd` | `RUNNING` |
| `gpt-4o-mini` | `latest` | `d65b5640b7be3c41` | `RUNNING` |

## Inference Schemas Tested

### Gemini

Working native Gemini schema:

- URL:
  `$DEPLOYMENT_URL/models/{model_name}:generateContent`
- method: `POST`
- body:

```json
{
  "contents": [
    {
      "role": "user",
      "parts": [{"text": "Reply with exactly OK."}]
    }
  ],
  "generationConfig": {
    "maxOutputTokens": 2048,
    "temperature": 0.2
  }
}
```

Smoke tests:

- `gemini-3.1-flash-lite`: passed, response `OK.`, elapsed `0.64s`.
- `gemini-2.5-pro`: passed, response `OK`, elapsed `2.24s`.

### Anthropic Claude

Deployment discovery works, but inference is blocked by schema/subpath.

Subpaths tested against `anthropic--claude-4.7-opus`:

- `/completion`: HTTP 400,
  `Subpath 'completion' is not allowed for model 'anthropic--claude-4.7-opus'.`
- `/chat/completions`: HTTP 400,
  `Subpath 'chat/completions' is not allowed for model 'anthropic--claude-4.7-opus'.`
- `/v1/chat/completions`: HTTP 400,
  `Subpath 'v1/chat/completions' is not allowed...`
- `/messages`: HTTP 400,
  `Subpath 'messages' is not allowed...`
- `/v1/messages`: HTTP 400,
  `Subpath 'v1/messages' is not allowed...`
- root deployment URL: HTTP 404
- `/model/anthropic--claude-4.7-opus`: HTTP 400,
  `Subpath 'model/anthropic--claude-4.7-opus' is not allowed...`
- `/model/anthropic--claude-4.7-opus:1`: HTTP 400,
  `Subpath 'model/anthropic--claude-4.7-opus:1' is not allowed...`

Current status: Claude is not smoke-passing. Multi-lineage review cannot claim
Claude participation until the allowed SAP AI Core Anthropic subpath/schema is
identified.

### Mistral

OpenAI-style path with required model field was tested:

- URL: `$DEPLOYMENT_URL/chat/completions`
- body includes `model: mistralai--mistral-medium-instruct`

Result: request timed out after 90 seconds. Earlier test without `model` reached
the service and returned HTTP 400 with a missing-field validation error, so the
endpoint shape is plausible but not currently smoke-passing.

Current status: Mistral is not smoke-passing.

### SAP Orchestration `/completion`

The expected orchestration-style `/completion` endpoint was tested first.

Result:

- Claude: HTTP 400, subpath not allowed.
- Gemini: HTTP 404, model `completion` not found.

Conclusion: these SAP AI Core deployments are foundation-model native endpoints,
not a universal orchestration `/completion` deployment.

## V30 Access Verdict

SAP AI Core access is partially established:

- authentication: working
- deployment discovery: working
- Gemini inference: working
- Claude inference: blocked by unresolved allowed subpath/schema
- Mistral inference: blocked by timeout after schema correction

V30 can run a single-lineage Gemini independent-lens proposal pass, but it cannot
honestly claim completed multi-lineage triangulation until at least one of
Claude, Mistral, Sonar, or another non-Gemini deployment smoke-passes.

## V31 Orchestration Update

V31 resolved the Claude blocker. Anthropic models are reached through the SAP AI
Core Orchestration deployment, not through the Claude foundation-model
deployment URL directly.

Orchestration deployment:

| Scenario | Configuration | Deployment ID | Status |
|---|---|---|---|
| `orchestration` | `defaultOrchestrationConfig` | `d65236404bbfb6b2` | `RUNNING` |

Working Claude model deployment:

| Model | Version | Deployment ID | Status |
|---|---:|---|---|
| `anthropic--claude-4.7-opus` | `1` | `def854013c7ac379` | `RUNNING` |

Working REST contract:

- URL:
  `$AI_API_URL/v2/inference/deployments/d65236404bbfb6b2/completion`
- method: `POST`
- headers:
  - `Authorization: Bearer <token>`
  - `AI-Resource-Group: default`
  - `Content-Type: application/json`
- body shape:

```json
{
  "orchestration_config": {
    "module_configurations": {
      "templating_module_config": {
        "template": [
          {
            "role": "user",
            "content": "{{?prompt}}"
          }
        ],
        "defaults": {}
      },
      "llm_module_config": {
        "model_name": "anthropic--claude-4.7-opus",
        "model_version": "1",
        "model_params": {
          "max_tokens": 64
        }
      }
    }
  },
  "input_params": {
    "prompt": "Reply with exactly OK."
  }
}
```

## V34 Gemini Generation Update

V34 identified and fixed the Gemini long-generation failure mode seen in V33.
Gemini smoke tests were valid, but longer JSON generations were malformed
because the model response ended with `finishReason = MAX_TOKENS`. The previous
client returned partial text without checking the finish reason.

Client behavior now:

- concatenates all Gemini text parts in the first candidate;
- checks `finishReason` / `finish_reason`;
- raises a clear error on `MAX_TOKENS` or `LENGTH` instead of writing partial
  output;
- exposes `debug-gemini` for non-secret response-shape diagnostics.

Verified behavior:

- Low-token V33 generation now fails loudly:
  `Gemini response ended by MAX_TOKENS; increase --max-output-tokens or shorten prompt`.
- The same generation succeeds with `--max-output-tokens 8192` and produces
  parseable JSON at `analysis/v34_gemini_generation_fixed.json`.

Operational rule: for structured Gemini generation, use enough output tokens
for the requested JSON and validate with `python3 -m json.tool` before treating
the output as usable proposal text.

Important Claude parameter detail:

- `temperature` must be omitted for `anthropic--claude-4.7-opus`; the service
  returns HTTP 400 with `LLM Module: temperature is deprecated for this model`
  if it is included.

Smoke tests from the committed client:

- `python3 scripts/sap_ai_core_client.py smoke --model anthropic--claude-4.7-opus`
  passed: response `OK`, elapsed `0.81s`.
- `python3 scripts/sap_ai_core_client.py smoke --model gemini-2.5-pro` passed:
  response `OK`, elapsed `1.57s`.
- `mistralai--mistral-medium-instruct` remained non-blocking: corrected
  `/chat/completions` request timed out again.

V31 access verdict:

- two non-OpenAI lineages are now working: Claude via Orchestration and Gemini
  via native Gemini endpoint.
- multi-lineage review can run.

## V36 SAP RPT-1 Tabular Prediction Access

V36 added SAP RPT access to the committed Python client for table-transformer
style predictions.

Working deployment:

- model: `sap-rpt-1-large`
- deployment ID smoke-tested: `d61aae51af327bbc`
- deployment URL shape:
  `https://api.ai.prod.eu-central-1.aws.ml.hana.ondemand.com/v2/inference/deployments/<deployment_id>`

Request contract verified from `@sap-ai-sdk/rpt` 2.11.0 and live smoke test:

- method/path: `POST <deploymentUrl>/predict`
- headers:
  - `Authorization: Bearer <token>`
  - `AI-Resource-Group: default`
  - `Content-Type: application/json`
- body shape:

```json
{
  "prediction_config": {
    "target_columns": [
      {
        "name": "OUTCOME",
        "prediction_placeholder": "[PREDICT]",
        "task_type": "classification"
      }
    ]
  },
  "index_column": "ID",
  "data_schema": {
    "ID": { "dtype": "string" },
    "MODULE_A": { "dtype": "numeric" },
    "MODULE_B": { "dtype": "numeric" },
    "OUTCOME": { "dtype": "string" }
  },
  "rows": [
    { "ID": "train_1", "MODULE_A": 0.1, "MODULE_B": 1.0, "OUTCOME": "low" },
    { "ID": "predict_1", "MODULE_A": 1.0, "MODULE_B": 0.2, "OUTCOME": "[PREDICT]" }
  ]
}
```

Important schema detail:

- The service rejects a top-level field named `schema` with HTTP 422
  `Extra inputs are not permitted`.
- The accepted field is `data_schema`, as an object keyed by column name.

Smoke test:

- command: `python3 scripts/sap_ai_core_client.py rpt-smoke --timeout 180`
- result: status code `0`, message `ok`, one prediction returned for
  `predict_1`, predicted `OUTCOME = high` with confidence `0.96`, elapsed
  `0.33s`.

Operational rule:

- RPT output is a tabular prediction lens, not evidence. In V36 it can be used
  to prioritize anomalies or masked-label predictions over structured project
  matrices, but every surfaced pattern still requires independent grounding on
  real data.

## V41 RPT Re-Verification

V41 re-verified `sap-rpt-1-large` after V40 had treated RPT as unavailable for
that run.

Smoke test:

- command: `python3 scripts/sap_ai_core_client.py rpt-smoke --timeout 90`
- result: status code `0`, message `ok`; deployment
  `d61aae51af327bbc`; one prediction for `predict_1`, predicted
  `OUTCOME = high` with confidence `0.96`; elapsed `0.4s`.

V41 joint-structure pass:

- payload: `analysis/v41_joint_inference/v41_rpt_joint_payload.json`
- output: `analysis/v41_joint_inference/v41_rpt_joint_predictions.json`
- result: `19` masked-row predictions; class counts
  `known_context = 9`, `not_validated = 10`.

Interpretation:

- RPT is usable through the committed Python client.
- RPT output remained a proposal/ranking lens only and did not change the V41
  evidence verdict.
