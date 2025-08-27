namespace Asym

/-- m*k = Θ(n): there exist positive integer constants cL, cU such that
    cL*n ≤ m*k ≤ cU*n. This is a build-safe pointwise Θ-spec for triples (m,k,n). -/
def ThetaMul (m k n : Nat) : Prop :=
  ∃ (cL cU : Nat), 0 < cL ∧ 0 < cU ∧ cL * n ≤ m * k ∧ m * k ≤ cU * n

end Asym

