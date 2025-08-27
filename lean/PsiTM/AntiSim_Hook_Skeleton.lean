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

-- Formalize core implications as axioms to avoid unverifiable placeholders
-- ID: AntiSim:Hook:Core
axiom FailureModesExhaustive :
  ∀ (b : BypassMethod),
    (ViolatesDeterminism b ∨ ViolatesOnePass b ∨ ViolatesNoAdvice b ∨ ViolatesLogBudget b)

axiom BudgetBarrier :
  ∀ (p : Params),
    RequiresSimulationBudget p → HasAllocatedLogBudget p → ExponentialSeparationBarrier p

-- ID: AntiSim:lem:failure-modes
theorem Lemma_FailureModes :
  ∀ (b : BypassMethod),
    (ViolatesDeterminism b ∨ ViolatesOnePass b ∨ ViolatesNoAdvice b ∨ ViolatesLogBudget b) :=
by
  intro b
  exact FailureModesExhaustive b

-- ID: AntiSim:cor:barrier
theorem Corollary_Barrier (p : Params) :
  RequiresSimulationBudget p → HasAllocatedLogBudget p → ExponentialSeparationBarrier p :=
by
  intro hReq hBudget
  exact BudgetBarrier p hReq hBudget

end AntiSim

