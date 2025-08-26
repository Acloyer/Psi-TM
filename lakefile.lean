import Lake
open Lake DSL

package psi_tm where

@[default_target]
lean_lib PsiTM where
  srcDir := "lean"
  roots  := #[
    `PsiTM.BudgetLemma,
    `PsiTM.PsiFooling,
    `PsiTM.LkLowerBound,
    `PsiTM.AntiSimulationHook
  ]

lean_exe psitm where
  root := `Main
