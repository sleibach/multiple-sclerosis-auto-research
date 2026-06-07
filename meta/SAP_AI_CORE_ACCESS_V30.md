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
