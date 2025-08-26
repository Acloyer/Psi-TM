import Lake
open Lake DSL

package psi_tm where

@[default_target]
lean_lib PsiTM where
  roots := #[`PsiTM.BudgetLemma, `PsiTM.PsiFooling, `PsiTM.LkLowerBound, `PsiTM.AntiSimulationHook]
  moreLeanArgs := #["-R","lean","PsiTM"]

lean_exe psitm where
  root := `Main
  moreLeanArgs := #["-R","lean","PsiTM"]
