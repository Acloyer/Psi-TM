### Risk Ledger (v0.8.71)

- Baseline residual risk: 12–15%
- Post-convergence target: 2–3% (97–98% safety)

| Risk           | Pre (0.8.7) | Post (0.8.71) | Notes/Guard                       |
|----------------|-------------|---------------|-----------------------------------|
| Advice/leakage | 4%          | 0.5–1%        | One-pass, no-advice guard         |
| Extra budget   | 3%          | 0.5–1%        | Sandbox flags isolated            |
| Stochasticity  | 3%          | 0.5–1%        | seed=1337 enforced                |
| DAG coverage   | 3%          | 0.5–1%        | Validator cross-check             |
| **Total**      | **12–15%**  | **2–3%**      | **97–98% safety**                 |