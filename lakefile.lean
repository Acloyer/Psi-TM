import Lake
open Lake DSL

/-- Enable stress build via `-Kstress=1` (presence -> true). -/
def stress : Bool := (get_config? stress).isSome

/-- Extra compiler args in stress mode. -/
def stressArgs : Array String :=
  if stress then
    #[
      "-Dpsi.stress=true"
    ]
  else
    #[]

package psi_tm where
  moreLeanArgs := stressArgs

@[default_target]
lean_lib PsiTM where
  srcDir := "lean"
  roots  := #[
    `PsiTM.BudgetLemma,
    `PsiTM.PsiFooling,
    `PsiTM.LkLowerBound,
    `PsiTM.AntiSim_Hook_Skeleton
  ]

lean_exe psitm where
  root := `Main
