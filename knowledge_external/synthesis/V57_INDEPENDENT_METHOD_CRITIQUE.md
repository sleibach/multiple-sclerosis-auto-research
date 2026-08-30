# V57 Independent Method Critique and Grounded Dispositions

Status: mixed-class ledger. Model proposals carry explicit class and source
markers below; seeded simulation results are method behavior only and never
biological evidence.

## Proposal Ledger

- **[external-unverifiable; NOT_PROJECT_GROUNDED; source: `knowledge_external/records/model_v57_claude_method_critique_2026.json`]** Test whether a few donors control the 2D-to-3D information verdict by requiring leave-one-donor stability.
  - **[grounded synthetic method behavior; source: `analysis/v57_multifidelity_adversarial_extension/leave_one_donor_results.tsv`]** The constructed paired high-leverage artifact almost never passed the parent gate (`0-0.01375`), and never passed the leave-one-donor gate. The added check retained `0.9425-0.945` complementary sensitivity at 12/8 and `0.98375-0.99375` at 16/12. Disposition: useful low-cost sensitivity, but no added protection was demonstrated in this artifact scenario.
- **[external-unverifiable; NOT_PROJECT_GROUNDED; source: `knowledge_external/records/model_v57_claude_method_critique_2026.json`]** Account for measurement error in the 2D covariate and report direct 3D effects alongside residualized effects.
  - **[grounded design boundary; source: `docs/plans/V57_MULTIFIDELITY_ADVERSARIAL_EXTENSION_PLAN.md`]** No empirical technical-replicate variance exists. Disposition: unresolved, requires blinded assay variance; no invented measurement-error correction was run.
- **[external-unverifiable; NOT_PROJECT_GROUNDED; source: `knowledge_external/records/model_v57_claude_method_critique_2026.json`]** Control multiplicity for candidate-specific 2D-benefit/3D-harm claims.
  - **[grounded design disposition; source: `docs/plans/V57_MULTIFIDELITY_ESCALATION_PLAN.md`]** The parent already predeclared a one-sided intersection rule and simultaneous candidate-family critical value. Disposition: already handled; no duplicate analysis.
- **[external-unverifiable; NOT_PROJECT_GROUNDED; source: `knowledge_external/records/model_v57_gemini_method_critique_2026.json`]** Add non-targeting perturbations as negative controls for hidden assay drift.
  - **[grounded synthetic method behavior; source: `analysis/v57_multifidelity_adversarial_extension/negative_control_results.tsv`]** The naive fixed `2.50` normal cutoff failed, with clean family false-stop `0.2438-0.2498`; it is rejected.
  - **[grounded synthetic method behavior; source: `analysis/v57_negative_control_finite_sample/negative_control_finite_sample_summary.json`]** A separately frozen eight-test Student-t correction passed at the first grid point, 12/8 donor pairs: maximum clean family error `0.0388`, minimum common-drift power `0.9646`, and minimum control-specific artifact power `0.9610`. Disposition: retain the finite-sample control gate as assay infrastructure; it cannot rule out candidate-specific hidden confounding.

## Lineage Contribution

The lineages added two concrete checks not in the parent gate. Data-based
disposition mattered: donor leverage was not a demonstrated parent weakness in
the tested scenario, while the first negative-control implementation was itself
invalid and had to be rejected before a separately frozen finite-sample design
passed. Agreement or model confidence played no evidentiary role.
