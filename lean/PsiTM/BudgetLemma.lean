/-
  Budget Lemma Skeleton (v0.8.6)
  ID: Budget:Lemma:Core
-/

-- ID: Budget:Lemma:Core
set_option warningAsError false

namespace Budget

axiom B : Nat → Nat → Nat
axiom c : Nat
axiom c_pos : 0 < c

theorem Lemma_Core : True := by
  trivial

end Budget
