# External Structural Predictions

Status: structural-prediction storage boundary. Records here are prediction
context, not experimental structures and not project-grounded findings.

Structural records are governed by:

```bash
python3 scripts/v51_structural_prediction_gate.py audit --fail-on-error
```

Current records:

| record | class | source | purpose |
|---|---|---|---|
| [GPR25 O00155 AlphaFold DB record](alphafold/GPR25_O00155/record.json) | `external-unverifiable` | source: https://alphafold.ebi.ac.uk/api/prediction/O00155 | Prediction-informed chr1 druggability-direction context only. |
| [KIF21B O75037 AlphaFold DB record](alphafold/KIF21B_O75037/record.json) | `external-unverifiable` | source: https://alphafold.ebi.ac.uk/api/prediction/O75037 | Prediction-informed chr1 motor-domain/druggability-direction context only. |
| [PTGER4 P35408 AlphaFold DB record](alphafold/PTGER4_P35408/record.json) | `external-unverifiable` | source: https://alphafold.ebi.ac.uk/api/prediction/P35408 | Prediction-informed PTGER4 druggability-direction context only. |
| [MIF P14174 AlphaFold DB record](alphafold/MIF_P14174/record.json) | `external-unverifiable` | source: https://alphafold.ebi.ac.uk/api/prediction/P14174 | Prediction-informed MIF physical-modelability context only. |
| [CD74 P04233 AlphaFold DB record](alphafold/CD74_P04233/record.json) | `external-unverifiable` | source: https://alphafold.ebi.ac.uk/api/prediction/P04233 | Confidence-limited CD74 monomer context only; do not infer a complex interface. |
