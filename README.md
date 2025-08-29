# Ψ‑TM: Minimal-Introspection Computation (concise overview)

Ψ‑TM is a Turing-machine model with selectors-only introspection bounded by depth and an explicit information budget. At each step a call ι_d(C,n) returns at most B(d,n)=c*d*log2(n) bits; selectors over decode_d(y) expose only depth<=d features.

## Core results (current)
- Strict depth hierarchy via explicit languages Lₖ (pointer-chase and phase-locked variants):
  - UB: depth‑k runs in O(n) time and O(log2n) space.
  - LB: any depth‑(k‑1) algorithm for Lₖ requires Omega(n/(k*(k-1)*log2 n)) steps.
- Anti-simulation hook (quantitative): depth‑(k‑1) cannot polynomially simulate a single ιₖ call under the budget; attempts trigger a budget‑violation threshold implied by B(d,n).
- Bridges with explicit losses between models:
  - Machine <-> Decision Tree, Decision Tree <-> IC-Circuits; composition yields Machine <-> Circuits. Losses are polynomial in parameters with explicit base-2 logarithmic factors.
- Controlled relaxations (public randomness, multi-pass, advice, bandwidth tweaks) preserve lower bounds with explicit, trackable degradation.
- Oracle-relative separation: there exists an oracle O_Ψ with P_Ψ^{O_Ψ} != NP_Ψ^{O_Ψ}.

## Minimal structure

```
Psi-TM/
├── Main.lean
├── lakefile.lean
├── main.tex
├── refs.bib
├── psi-tm-formal-definition.tex
├── psi-tm-lower-bound-tools.tex
├── psi-tm-08-3-lk-pointer-chase.tex
├── psi-tm-08-4-lkphase-phase-access.tex
├── psi-tm-08-5-anti-simulation-hook.tex
├── psi-tm-barrier-minimality.tex
├── psi-tm-k-hierarchy.tex
├── psi-tm-stoc-focs.tex
├── psi-tm-theoretical-results.tex
├── paper/
│   ├── sections/
│   │   ├── relaxations.tex
│   │   ├── platforms.tex
│   │   ├── bridges.tex
│   │   └── methods.tex
│   ├── tables/
│   │   ├── platforms_table.tex
│   │   └── bridges_table.tex
│   ├── fig/
│   │   └── stack_diagram.tex
│   ├── appendix-firebreak.tex
│   └── appendix-zero-risk-map.tex
├── lean/
│   ├── PsiTM/
│   │   ├── BudgetLemma.lean
│   │   ├── PsiFooling.lean
│   │   ├── LkLowerBound.lean
│   │   ├── AntiSim_Hook_Skeleton.lean
│   │   ├── Relaxations.lean
│   │   ├── Platforms.lean
│   │   ├── Bridges.lean
│   │   └── AltForms/
│   │       ├── AntiSimAlt.lean
│   │       ├── LkAlt.lean
│   │       └── LkphaseAlt.lean
│   ├── Lk_LB_Skeleton.lean
│   └── Lkphase_Transcript_Skeleton.lean
├── isabelle/
│   ├── ROOT
│   └── PsiTM/
│       ├── AltForms.thy
│       ├── AntiSim.thy
│       ├── BudgetLemma.thy
│       ├── Lk.thy
│       └── Lkphase.thy
├── notebooks/
│   ├── anti_simulation_analysis.ipynb
│   ├── lk_pointer_chase.ipynb
│   ├── lkphase_transcript_analysis.ipynb
│   ├── numeric_examples.ipynb
│   ├── transcript_counts.ipynb
│   └── stress_firebreak/
│       ├── stress_matrix.ipynb
│       └── phase_weird.ipynb
├── scripts/
│   ├── check_project.py
│   ├── validate_claims.py
│   ├── validate_dag.py
│   ├── sanitize_notebooks.py
│   ├── plot_anti_simulation.py
│   └── generate_counterexamples.py
├── fig/
│   ├── anti_simulation_budget.png
│   ├── lk_logM.png
│   ├── lkphase_transcript.png
│   └── (other generated figures)
├── results/
│   └── 2025-08-28/
│       ├── platforms.csv
│       └── stress_firebreak/
│           ├── stress_matrix_*.{csv,json,md}
│           └── phase_weird_*.{csv,json,md}
├── docs/
│   ├── audit/
│   ├── redteam/
│   ├── deps/
│   └── risk_ledger.md
├── ci/
│   └── stress-merge.yml
├── Makefile
├── LICENSE
├── NOTICE
├── MANIFEST.md
├── VERSIONS.md
└── versions.yml
```

## Artifacts and reproducibility
- Formal headers in Lean 4 (`lean/`); Lake build; base-2 logs (`Nat.log2`).
- Paper sources in `paper/` and top-level `.tex`; figures under `fig/`.
- Deterministic notebooks (`seed=1337`); outputs under `results/<DATE>/...`.
- Build: `make all` (checks + Lean build + notebooks). PDF: `latexmk -pdf main.tex`.