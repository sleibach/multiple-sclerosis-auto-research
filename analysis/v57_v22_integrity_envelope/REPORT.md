# V57 V22 Measurement and Label Integrity Envelope

## Measurement-error result

The audit evaluated 2,100,000 seeded
score perturbations across two variance modes, seven assumed reliabilities,
and three seeds. At reliability at least 0.80, the least favorable cell had
median AUC 0.778 and
probability 99.2%
of retaining AUC >= 0.60. The predeclared high-reliability criterion
passes; the
lowest grid reliability for which every seed and mode passes is
0.5.

This is conditional sensitivity around observed scores. It does not estimate
the reliability of Gafson, Karolinska, or any assay and cannot substitute for
empirical technical replicates.

## Label-integrity result

The audit exhaustively evaluated 11,790
balance-preserving label-exchange configurations. A single adversarial pair
can reduce AUC from 0.811 to 0.611;
0.0% of all one-pair exchanges
fall below 0.60. The predeclared adversarial single-pair criterion therefore
passes.

The worst single exchange yields AUC
0.611. Participant-level exchange
configurations are intentionally not persisted in this public repository;
the committed aggregates are sufficient to reproduce the method conclusion
from the already-governed held input.

## Decision implication

The frozen score is reasonably tolerant of added independent measurement
noise under the stated reliability model, but the 19-subject result is
materially dependent on clinical-label integrity. External validation should
require blinded endpoint adjudication and an auditable label provenance trail,
not merely adequate expression measurement. This does not change V22 or add
biological evidence.
