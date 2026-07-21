You are an independent adversarial methods reviewer. You are a proposal lens,
not an evidence source. Review the bounded MS-progression results below and find
the strongest remaining design flaw, confounder, or decisive test. Do not add
literature facts, invent data, or reinterpret an unavailable endpoint as a
negative result.

Return ONLY a valid JSON array of exactly 6 objects. Each object must have
exactly these string fields:

- id
- target_claim
- fatal_weakness
- why_it_matters
- concrete_check
- required_artifacts
- would_change_verdict_if_supported
- minimum_next_data

Prioritize checks executable on the committed held data. If a point cannot be
tested without new data, say so explicitly in required_artifacts and
minimum_next_data. A concrete_check must name an analysis, diagnostic, or data
field, not a general request for replication. Do not propose broad new target
discovery; public-data discovery is closed.

EVIDENCE BOUNDARY

1. No held transcriptomic dataset links repeated molecular measurements to
time-varying MS stage plus repeated disability or adjudicated conversion.
Transition and treatment-mediated slowing are not identifiable. Relapse,
cross-sectional stage, lesion morphology, and pharmacodynamics are not treated
as disability progression.

2. Source/tissue-balanced Macnair postmortem microglia comparison: 44 donors
(Amsterdam white matter and UK grey matter), PPMS versus SPMS, nuisance and
source controlled, 300,000 nulls over three seeds, five pre-existing modules,
BH and max-T plus source-direction gate. Zero modules pass. CD44/CXCR4 is
same-direction across sources but inconclusive: standardized SPMS-minus-PPMS
beta 0.343, HC3 CI -0.253 to 0.938, permutation p 0.279, max-T p 0.787. IFN/APC
is same-direction but inconclusive. HLA, MIF, and lysosomal directions differ by
source. This is cross-sectional stage only.

3. Lesion contexts: GSE180759 has only three paired chronic-active versus
chronic-inactive edge donors. GSE279972 has 54 foamy/nonfoamy samples from 21
donors. Models adjust lesion class, B/APC composition, resident-microglia
identity, and de-overlapped MIMS state, with 300,000 donor-wild nulls. No module
passes an orthogonal-context gate. CD44/CXCR4 is 3/3 higher at active edges but
null in morphology. OXPHOS is lower in foamy morphology but direction-discordant
at active edges. Lysosomal state is higher in the pooled foamy model but mixed
at active edges.

4. Post-result pooled morphology sensitivities: mutually adjusted OXPHOS beta
-0.562 (CI -1.003 to -0.120, donor-wild p 0.0107, max-endpoint p 0.0114) and
lysosomal beta 0.463 (CI 0.111 to 0.816, p 0.0108, max-endpoint p 0.0518), with
all 21 leave-one-donor directions stable. However, neither endpoint passes a
frozen lesion-stratum transport gate in eligible lesion classes 2 and 3.
OXPHOS remains negative but imprecise in both. Lysosomal is near-zero negative
in class 2 and positive but imprecise in class 3. Direct class-3-versus-class-2
interactions are null with wide intervals and unstable LODO signs. Correct
current label: pooled, lesion-context-bounded morphology association with
unresolved transport; not progression or flux.

5. CNS-versus-peripheral localization is not identifiable. No matched phenotype
pair exists. GSE228330 baseline PBMC has 10 RRMS and 5 SPMS samples; subtype and
deposited activity suffix are associated (Fisher p 0.01698), and the public
subject map, processed matrix, batch, age, cell composition, and disability are
absent. No peripheral expression test was run, so there is no peripheral null.

6. Sequential intervention-direction map: 0/9 pre-existing candidate states
passes the progression-specific first gate. V53 held context supplies 24
perturbation signatures, 0 replicated selective control nodes, 0 corrected
additive-pair prioritization passes, and 0 consensus causal edge orientations
over ten skeleton variants. AlphaFold was deliberately not used because no
candidate reached modality fit. No target closure changed.

7. A 64-field progression acquisition contract and fail-closed P1/P2/P3
inventory validator now exist. Six synthetic validator fixtures behave as
expected. A separate generic synthetic power grid simulated 288,000 cohorts
over three seeds: null FPR median 0.043/max 0.060. Under explicit assumptions,
7/24 non-null scenarios reached 80%; OR 1.25/1.5 did not by n=240. These are
method-design results, not empirical MS effect estimates.

TASK

Return the six strongest objections or decisive checks. Focus on whether any
current wording is too strong, whether a real-data sensitivity was missed, or
whether the acquisition/power design still leaves a researcher degree of
freedom. Multi-model agreement will prioritize checks, but only committed-data
grounding can change anything.
