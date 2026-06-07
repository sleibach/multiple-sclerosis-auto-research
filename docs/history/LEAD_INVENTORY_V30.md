# Lead Inventory V30

Date: 2026-06-07

## Scope

V30 establishes SAP AI Core access for independent sub-model review and runs as
much of the V29 queued review as the live model endpoints allow. Model output is
treated only as proposal generation. No locked rule was edited. No fresh
validation cohort was present or read.

## SAP AI Core Status

Access report: `meta/SAP_AI_CORE_ACCESS_V30.md`.

Working:

- SAP service-key JSON in `SAP_AI_CORE_API_KEY` parses from `.env`.
- OAuth2 client-credentials token exchange succeeds.
- Deployment discovery succeeds for resource group `default`.
- Gemini inference smoke tests pass:
  - `gemini-3.1-flash-lite`: response `OK.`
  - `gemini-2.5-pro`: response `OK`

Blocked:

- Claude deployments are discoverable and `RUNNING`, but all tested native and
  orchestration subpaths are rejected as not allowed or 404.
- Mistral deployment is discoverable and `RUNNING`, but the corrected
  `/chat/completions` request timed out.
- Therefore V30 does not honestly complete multi-lineage triangulation. It
  completes SAP AI Core engineering for Gemini and queues Claude/Mistral schema
  resolution.

Reusable client:

- `scripts/sap_ai_core_client.py`

## Model-Lens Outputs

### Gemini 2.5 Pro

Artifacts:

- prompt: `analysis/v30_multi_lineage_review/gemini_review_prompt.md`
- first raw response:
  `analysis/v30_multi_lineage_review/gemini_2_5_pro_review_raw.md`
- compact prompt:
  `analysis/v30_multi_lineage_review/gemini_compact_prompt.md`
- compact response:
  `analysis/v30_multi_lineage_review/gemini_2_5_pro_review_compact.json`
- compact retry, complete and parsed:
  `analysis/v30_multi_lineage_review/gemini_2_5_pro_review_compact_retry.parsed.json`

The first two Gemini review responses were truncated mid-JSON and are not usable
as grounded proposal sources. A larger-output retry produced complete JSON.

Because multi-lineage review did not complete, Gemini proposals are single-lens
suggestions only. Grounding status:

| Gemini item | Type | Grounded outcome | Evidence / reason |
|---|---|---|---|
| Steroid pulse as postpartum mimic | proposal | blocked / new-data scout | No local pre/post high-dose steroid MS relapse transcriptomic cohort is present in `data/raw` or current validation artifacts. This is a concrete V31/V24-style data-scout item, not an immediately grounded result. |
| Metabolic confounding of V22 rule | proposal | inconclusive / queued | V29 already proposed NAMPT/HIF/glycolysis adjustment as a future covariate test. Current V28 artifacts test receptor, coupled, vector, cohort, jackknife, Bayesian, and ridge lenses, but do not contain hallmark glycolysis/OXPHOS scoring. Needs local pathway-set acquisition/scoring before verdict. |
| Chr1 KIF21B locus score in treatment response | proposal | blocked / underpowered and mismatched modality | Existing V19 evidence grounds KIF21B genetics/eQTL direction, but current treatment-response validation tables are module-level and do not include a defined KIF21B locus-expression score across MS and UC. Testing this requires raw expression matrix harmonization and is biologically secondary because chr1 is already classified as real genetics / hard-target handoff. |
| Arbitrary mechanism boundary | vulnerability | partially failed as sole explanation | V23/V28 already tested bounded-vs-unbounded performance and cohort-adjusted models. The bounded scalar remains positive after cohort fixed effects (`coef = 0.322`, robust p `5.70e-07`) and jackknife AUC range `0.788-0.888`, so the boundary is not explained solely by one subject or raw cohort pooling. A baseline immune-remodeling potential metric remains untested. |
| Small-n model fallacy | vulnerability | held as limitation, not a kill | V28 already found ridge multifeature LOOCV weaker than scalar (`AUC = 0.578` bounded) and explicitly concluded model-flexibility fragility. Gemini's critique correctly reinforces that this is a small-n limitation; it does not overturn the scalar but prevents interpreting simplicity as deep biology. |
| Premature modality filter / KIF21B trans-eQTL | vulnerability | queued / data-limited | Existing V19 QTD000021 coloc supports KIF21B cis regulation (`MS/eQTL PP.H4 = 0.8749`, `UC/eQTL PP.H4 = 0.8687`). No local trans-eQTL genome-wide scan is present. This is a plausible future analysis if eQTLGen trans summary data is reachable; no current intervention-grade rescue. |

## Grounded Local Progress

RAG query before local review:

```bash
.venv_v3_py312/bin/python scripts/query_knowledge_index.py \
  "V30 independent model review postpartum HLA-II CD64 MIF CD74 APC treatment response vulnerabilities" 10
```

Top hits were postpartum APC-axis split hypotheses, SLE pregnancy
HLA-II/CD64 decoupling, and MIF/CD74 mechanism artifacts. This confirms that
V29's local dormant-lead frontier was not re-derived from scratch.

Grounded status from V29 remains current:

| Lead / claim | V30 status | Reason |
|---|---|---|
| V22 bounded APC/HLA-II scalar | active validation lead | V28 already showed tool-robustness; V30 found no new grounded evidence to edit the locked scalar. |
| Postpartum HLA-II/CD64 APC split | best dormant biology lead | RAG hits confirm prior pregnancy/postpartum APC-axis hypotheses; needs postpartum MS blood/CSF cohort, not more model commentary. |
| MIF/CD74 | coupled APC context only | V26/V27/V28 support coupling context but not standalone predictor or target. |
| ZMIZ1 | robust decoupling finding | No change; use as transfer-validity warning. |
| chr1 KIF21B/GPR25 | controlled-data handoff | No change; local computation has exhausted public QTL/atlas evidence. |

## V30 Verdict

SAP AI Core access adds real new capability, but only Gemini is currently
smoke-passing. V30 therefore partially advances the independent-lens goal:

1. It creates a reusable SAP AI Core client and access report.
2. It confirms that Gemini can be used for proposal generation.
3. It identifies exact blockers for Claude and Mistral.
4. It does not claim multi-lineage review completed.
5. It does not reactivate or promote any lead without grounded evidence.

## Next Requirements

1. Resolve the SAP AI Core Anthropic allowed subpath/schema, or obtain SAP's
   documented native Claude invocation path for these deployments.
2. Resolve Mistral timeout or schema.
3. Re-run the V29 review package across at least two working non-OpenAI
   lineages.
4. Ground the resulting de-duplicated proposal queue on local data.
