/-
  Anti-simulation hook auxiliary results (v0.8.6.1)
  Clean formal headers matching claims.yaml; avoids undefined constants.
-/

set_option warningAsError false

namespace AntiSim

axiom B : Nat -> Nat -> Nat

structure Params where
  k : Nat
  n : Nat
  s : Nat
  k_ge_2 : k >= 2

axiom BypassMethod : Type
axiom ViolatesDeterminism : BypassMethod -> Prop
axiom ViolatesOnePass : BypassMethod -> Prop
axiom ViolatesNoAdvice : BypassMethod -> Prop
axiom ViolatesLogBudget : BypassMethod -> Prop

axiom RequiresSimulationBudget : Params -> Prop
axiom HasAllocatedLogBudget : Params -> Prop
axiom ExponentialSeparationBarrier : Params -> Prop

-- ID: AntiSim:lem:failure-modes
theorem Lemma_FailureModes :
  ∀ (b : BypassMethod),
    (ViolatesDeterminism b ∨ ViolatesOnePass b ∨ ViolatesNoAdvice b ∨ ViolatesLogBudget b) :=
by
  sorry

-- ID: AntiSim:cor:barrier
theorem Corollary_Barrier (p : Params) :
  RequiresSimulationBudget p → HasAllocatedLogBudget p → ExponentialSeparationBarrier p :=
by
  intro _ _
  sorry

end AntiSim

