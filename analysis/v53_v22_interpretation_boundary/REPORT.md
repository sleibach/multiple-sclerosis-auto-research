# V53 V22 Interpretation Boundary

Verdict: **V22_COMPUTATION_UNCHANGED_V53_ONLY_NARROWS_MECHANISTIC_INTERPRETATION**.

The locked-rule SHA-256 remains `6373857789e3a538481cebe313ef041792740e4779c7bc705d86494c830e152a` and matches the committed V45
baseline. The V42 harness IFN/APC, HLA-II, and receptor gene lists match their
frozen definitions. The primary Class-C score remains exactly `delta_HLAII -
delta_IFN_APC`; receptor-only is a negative control and is not part of the score.

V53 therefore changes no validation computation. It narrows what a future pass may
mean: performance can support the frozen monitoring score, but cannot establish the
demoted independent HLA-II/receptor architecture, MIF causality, clinical utility,
or a therapeutic target. Existing V42 non-specific and immune-tone result classes
already enforce this distinction.
