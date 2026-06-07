# V36 Refined Generation Pass

Status: **completed_two_lineage_generation_after_specificity_audit**.

Role: idea generation only. No model output is evidence.

Inputs:

- Updated V36 lead state: broad IFN/APC remodeling with candidate T-cell and
  B/plasma readouts.
- Specificity limits: STAT1 is not B/plasma-specific; limited locked-gene null
  blocks a narrow IFN/STAT four-gene claim.

Lineage status:

- Claude 4.7 Opus returned `10` concrete JSON analyses.
- Gemini 2.5 Pro failed the long prompt by `MAX_TOKENS`; rerun with a compact
  prompt returned `6` usable JSON analyses in a markdown JSON fence.

Convergent/highest-priority executable tests:

| Test | Proposed by | Why it matters | V36 status |
|---|---|---|---|
| Global IFN-tone / steroid-like residualization | Claude | Tests whether locked compartment signal survives generic immune-tone or steroid confounding. | queued where marker coverage exists |
| B/plasma versus myeloid IFN/STAT score correlation | Gemini, agent | Tests whether B/plasma signal is independent or redundant with myeloid IFN biology. | queued |
| Leave-one-gene module dependence | Gemini, agent | Tests whether B/plasma IFN/STAT carrier is a module or single-gene signature. | queued |
| Gene-scan multiplicity / empirical null | Claude, Gemini, agent | Tests whether STAT1 or IFN/STAT survives small-n multiplicity. | partly completed by Iteration 16; further gene-level null queued if feasible |
| Within-B/plasma subset composition | Claude, Gemini | Tests whether major B/plasma score is subcluster composition rather than within-cell remodeling. | needs raw cell-level clusters; queued as data/tool check |

Grounding rule:

These proposals only prioritize the next queue items. They do not upgrade any
hypothesis unless implemented against held data with appropriate null/sensitivity
checks.
