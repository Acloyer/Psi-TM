/-
  Anti-Simulation Hook Skeleton (v0.8.6)
  ID: AntiSim:Hook:Core
-/

-- ID: AntiSim:Hook:Core

set_option warningAsError false

namespace AntiSim

axiom B : Nat → Nat → Nat

structure Attempt where
  k : Nat
  n : Nat
  s : Nat
  k_ge_2 : k ≥ 2

/-
  Core anti-simulation statement skeleton: if an attempt uses s calls to
  \iota_{k-1} then the budget is exceeded when s · B(k−1, n) > B(k, n).
-/
theorem Hook_Core (a : Attempt) : True := by
  trivial

end AntiSim

