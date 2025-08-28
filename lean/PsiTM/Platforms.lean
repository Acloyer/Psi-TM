/- Platforms: Independent frameworks (v0.9.2)
   Clean headers only; proof bodies may remain as axioms in 0.8.6.x.
   Uses Nat.log2 only. -/

import PsiTM.BudgetLemma
import PsiTM.PsiFooling
import PsiTM.Relaxations

set_option warningAsError false

namespace Platforms

/- Shared primitives capturing budget/transcript notions used across platforms. -/
axiom B : Nat → Nat → Nat

/- Psi decision-tree model ---------------------------------------------------- -/
structure PsiDecisionTreeModel where
  depth : Nat

-- ID: Platform:PsiDecisionTree
/-  Decision-tree depth lower bound: depth ≥ ⌈log2 M / B(d,n)⌉ (schematic). -/
axiom PsiDecisionTree_bound
  (d n M : Nat) (tree : PsiDecisionTreeModel) :
  True

/- IC gates / circuits -------------------------------------------------------- -/
structure ICGate where
  arity : Nat

-- ID: Platform:ICGate
/-  Transcript-counting lower bound schema for IC-gates. -/
axiom ICGate_bound (k n : Nat) (g : ICGate) : True

-- ID: Platform:ICAC0
/-  IC-AC^0 lower bound (schema). -/
axiom ICAC0_bound (k n : Nat) : True

-- ID: Platform:ICNC1
/-  IC-NC^1 lower bound (schema). -/
axiom ICNC1_bound (k n : Nat) : True

end Platforms

