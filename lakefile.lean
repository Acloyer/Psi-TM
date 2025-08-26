import Lake
open Lake DSL

package psi_tm

lean_lib PsiTM where
  moreLeanArgs := # ["-R", "lean", "PsiTM"]

@[default_target]
lean_exe psi_tm where
  root := `Main
  moreLeanArgs := # ["-R", "lean", "PsiTM"]