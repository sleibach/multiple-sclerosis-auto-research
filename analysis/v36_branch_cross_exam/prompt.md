# V36 Therapy-Branch Cross-Exam

You are reviewing a strict computational MS project. Model output is not
evidence; it only proposes tests to run.

Current claim:

- The immutable V22/V23 locked APC/HLA-II scalar remains the primary DMF/JAK-ish
  validation target.
- V36 held artifacts now suggest therapy-branch interpretation:
  - Tofacitinib/immune-remodeling: IFN/APC/STAT1 downshift dominates.
  - IFN-beta: HLA-II competence/induction and CD74/CD44/CXCR4 receptor-state
    dynamics are more relevant.
  - Fingolimod, adalimumab, MTX psoriasis skin do not support unbounded transfer.
- DMF locked support is small-n: AUC 0.72, exact p 0.155, leave-one-out min
  AUC 0.65.
- GSE24427 IFN-beta: month-1 delta HLA-II AUC 0.75, p 0.0195; baseline HLA-II
  AUC 0.361.
- GSE138064 IFN-beta: baseline HLA-II and receptor-state dynamics distinguish
  complete vs partial responders.

Task:

Name up to 5 concrete ways this therapy-branch interpretation could be wrong.
For each, provide one test executable with already-held artifacts, or mark it
non-executable. Return JSON only:

{
  "weaknesses": [
    {
      "weakness": "...",
      "test": "...",
      "artifact": "...",
      "executable_now": true,
      "what_result_would_weaken_branch_claim": "...",
      "what_result_would_support_branch_claim": "..."
    }
  ]
}
