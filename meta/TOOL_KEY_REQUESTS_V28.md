# Tool Key Requests V28

Date: 2026-06-07

No paid or gated service was used before writing this request file.

## Low-Cost Key Requests

| Service | Env var | Expected cost | Why it helps | Checker |
|---|---|---:|---|---|
| OpenAI API | `OPENAI_API_KEY` | low dollars for one critique/proposal pass if usage is capped | External frontier-model lens to critique `LOCKED_RULE_V22`, propose confounders/features, and scan project reports for overlooked assumptions. Outputs would be treated only as proposals and then grounded in real data. | `python3 scripts/check_openai_access.py` |

## Higher-Cost / Deferred Options

| Service | Env var | Expected cost | Why deferred |
|---|---|---:|---|
| Hosted virtual-cell / genomic foundation-model inference endpoint | provider-specific | unknown to moderate | Could generate perturbation hypotheses for APC/HLA-II movement, but no specific low-barrier endpoint/key is currently configured. Not needed for local V28 robustness testing. |
| Cloud GPU compute | provider-specific | moderate | Not justified for the tiny paired-score treatment-response tables; local CPU methods are sufficient. |

## Integration Rule

If `OPENAI_API_KEY` is provided later, run the checker, ask the model for
analysis proposals only, and implement any accepted proposal against local data.
Do not cite model output as evidence.
