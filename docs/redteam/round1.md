### Red-Team Round 1

- Critical: Advice channel not explicitly disabled → Resolution: clarified one-pass, no-advice guard; tests enforce.
- High: Extra budget factor ambiguity → Resolution: sandbox flags `{extra_budget_factor∈{1,2,4}}` scoped to notebooks only.
- Medium: Stochasticity creeping via seeds → Resolution: fixed `seed=1337` and deterministic pipelines.

