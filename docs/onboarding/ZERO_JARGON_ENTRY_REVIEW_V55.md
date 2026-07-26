# Zero-Jargon Entry-Route Review V55

This communication review asks whether a smart reader can follow the root
two-minute route before opening the glossary. It changes no scientific claim
or evidence status. “Zero jargon” here means no unexplained specialist term is
required to understand the main conclusion; unavoidable gene labels may remain
when their role is explained. `[E01, M01, M05, P02]`

## Route Audited

```text
docs/onboarding/README.md
  -> MS_RESEARCH_EXPLAINED.md#the-two-minute-version
  -> visuals/RESEARCH_MAP_V55.svg
```

The visual has a complete text equivalent in `VISUAL_INDEX.md`. This review
focused on the words encountered before a reader chooses the glossary.

## Barriers Found And Repaired

| term or phrase | why it blocked a newcomer | repair |
|---|---|---|
| immune-mediated / central nervous system / myelin | Three medical terms arrived in one opening sentence. | Rephrased as immune-linked injury in the brain and spinal cord; defined myelin as insulating material around nerve fibers. |
| provisional | Could sound like administratively accepted. | Defined as internal support with a decisive outside test still needed. |
| APC/HLA-II | An acronym-heavy module name appeared before its meaning. | Explained the gene group's display role and expanded APC/HLA-II at first use. |
| bounded | Project-specific shorthand could sound like a statistical bound. | Defined it as a claim intentionally limited to the tested setting. |
| pre-registered validation | The key anti-bias protection was named but not explained. | Replaced it with an outside test whose rule and interpretations are fixed before outcomes are inspected. |
| attenuated | A technical result word hid the practical meaning. | Replaced it with “made the association weaker after accounting for broader immune state.” |
| genome-wide genetic relationship | Could be mistaken for a causal link between diseases. | Explained it as shared inherited risk patterns across the genome, within the diseases compared here. |
| direction-decoupling | Dense project shorthand obscured the useful lesson. | Explained the opposite risk directions and the warning against transferring a treatment direction. |
| causal gene / therapeutic direction | Required genetics background. | Explained which gene drives a regional signal and whether intervention must block, restore, or increase function. |
| coupled architecture | Could imply a causal mechanism. | Replaced it with the observation that several measured signals repeatedly moved together. |
| held-out modality | A machine-learning term arrived without a mental model. | Explained it as testing on a different data type kept aside from the search. |
| microglia / proxy | Cell and design jargon arrived together. | Defined microglia as immune-related central nervous system cells and proxy as an indirect stand-in. |
| source and batch confounding | Too compressed for the final open question. | Recast it as diagnosis accidentally lining up with sample source or processing batch. |
| claim IDs | Letter-number labels could look like required scientific vocabulary. | Stated that they are source references readers do not need to memorize. |

The root contribution route also replaced “null,” “holdout,” and “correction”
with their practical meanings: a fair comparison or untouched test set,
chance-finding control, and a result that would make the contributor drop the
idea.

## Terms Deliberately Retained

| retained term | reason it remains | comprehension protection |
|---|---|---|
| MS | The disease name is expanded at first use in the narrative. | The root title and link make the subject explicit. |
| relapse and progression | The distinction is central rather than optional jargon. | Each receives a one-sentence definition before any finding. |
| ZMIZ1, KIF21B/GPR25, PTGER4, CD44/CXCR4 | These are identifiers for routes readers should not accidentally re-propose. | Each label is paired with its role and a plain-language boundary; memorization is unnecessary. |
| gene | Common enough for the audience and necessary to explain prior routes. | The text states the decision problem rather than assuming molecular expertise. |
| validation | It names the live lead's decisive next gate. | The text immediately explains independent data and decisions fixed in advance. |
| statistical stress test | A short umbrella term avoids a misleading claim that one check proves truth. | The tiny 19-person scope and need for independent testing remain in the same paragraph. |

## Result

**PASS for pre-glossary orientation, subject to human testing.** The route now
defines every specialist concept needed to recover these five conclusions:

1. relapse and progression are not interchangeable;
2. one provisional monitoring lead awaits an independent test;
3. it is not a target, selector, clinical test, or cure;
4. tested genetics and systems routes include real closures and negatives; and
5. no progression result was established because the required longitudinal
   design is missing. `[B02, M01-M05, G02-G05, D01-D05, P01-P06]`

## What This Does Not Prove

- A terminology review does not prove comprehension.
- A smart reader can still bring different assumptions to ordinary words such
  as “signal,” “support,” or “validation.”
- The route cannot teach the full statistical and biological context in two
  minutes.
- Actual comprehension should be measured with the
  [human test kit](COMPREHENSION_TEST_KIT.md), not inferred from sentence
  length or this reviewer's judgment.

Readers who want exact definitions can continue to the
[plain-language glossary](GLOSSARY.md). Maintainers should rerun this review
whenever a new specialist label is added before that link.
