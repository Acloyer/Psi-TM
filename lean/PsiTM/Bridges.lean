/-
  Bridges between Machine, Decision Tree, and IC-Circuit models
  Headers strict; proof bodies omitted (axiomatized) per skeleton policy.
  All logs are base 2 and use Nat.log2.
-/

-- ID: Bridge:MachineTree
-- ID: Bridge:TreeCircuit
-- ID: Bridge:MachineCircuit:Cor

namespace PsiTM

namespace Bridges

/-- Loss functions are explicit symbolic placeholders parameterized by problem size.
They capture multiplicative overheads in resource translation. -/
structure Loss where
  lossOnN : Nat → Nat

/-- Source/target LB predicates (platform-agnostic signatures). -/
axiom LB_Machine : Nat → Nat → Prop
axiom LB_Tree    : Nat → Nat → Prop
axiom LB_Circuit : Nat → Nat → Prop

/-- Canonical explicit losses (symbolic):
    We keep them as functions only of n for the header; parameters like d, k
    are captured by closing over them when needed. -/
def loss_log2_pow (a : Nat) : Loss :=
  { lossOnN := fun n => Nat.pow (Nat.log2 (Nat.succ n)) a }

def loss_poly_param (p : Nat) (a : Nat) : Loss :=
  { lossOnN := fun _ => Nat.pow p a }

/-
  Bridge:MachineTree — bidirectional transfer with explicit losses.
  Forward (Machine → Tree) uses product of a d-dependent polynomial and log factor.
  Backward (Tree → Machine) similarly uses an explicit d-dependent factor.
-/
-- ID: Bridge:MachineTree
axiom Bridge_MachineTree
  (d : Nat) (a b : Nat)
  (L_to   : Loss := { lossOnN := fun n => (loss_poly_param d a).lossOnN n * (loss_log2_pow b).lossOnN n })
  (L_from : Loss := { lossOnN := fun n => (loss_poly_param d a).lossOnN n * (loss_log2_pow b).lossOnN n })
  :
    (∀ (n : Nat), LB_Machine d n → LB_Tree d (L_to.lossOnN n)) ∧
    (∀ (n : Nat), LB_Tree d n    → LB_Machine d (L_from.lossOnN n))

/-
  Bridge:TreeCircuit — bidirectional transfer with explicit losses.
-/
-- ID: Bridge:TreeCircuit
axiom Bridge_TreeCircuit
  (k : Nat) (c l : Nat)
  (L_to   : Loss := { lossOnN := fun n => (loss_poly_param k c).lossOnN n * (loss_log2_pow l).lossOnN n })
  (L_from : Loss := { lossOnN := fun n => (loss_poly_param k c).lossOnN n * (loss_log2_pow l).lossOnN n })
  :
    (∀ (n : Nat), LB_Tree k n    → LB_Circuit k (L_to.lossOnN n)) ∧
    (∀ (n : Nat), LB_Circuit k n → LB_Tree k (L_from.lossOnN n))

/-
  Bridge:MachineCircuit:Cor — composition via Tree.
  The composed loss is the pointwise product of the two forward (or backward) losses.
-/
-- ID: Bridge:MachineCircuit:Cor
axiom Bridge_MachineCircuit_Cor
  (d k : Nat) (a b c l : Nat)
  (L_MT : Loss := { lossOnN := fun n => (loss_poly_param d a).lossOnN n * (loss_log2_pow b).lossOnN n })
  (L_TC : Loss := { lossOnN := fun n => (loss_poly_param k c).lossOnN n * (loss_log2_pow l).lossOnN n })
  (L_MC : Loss := { lossOnN := fun n => L_MT.lossOnN n * L_TC.lossOnN n })
  : ∀ (n : Nat), LB_Machine d n → LB_Circuit k (L_MC.lossOnN n)

end Bridges

end PsiTM

