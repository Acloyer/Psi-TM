import re, sys, pathlib
txt = pathlib.Path("paper.txt").read_text(encoding="utf-8")
MUST = [
  r"Controlled Relaxations \(v0\.9\.1\)",
  r"lem:R1-entropy-budget", r"lem:R2-multipass", r"lem:R3-advice", r"lem:R4-bandwidth-tweak",
  r"lem:DT-LB-under-R", r"lem:IC-transcript",
  r"thm:bridge-machine-tree", r"thm:bridge-tree-circuit",
  r"Post-0\.8\.71 residual-risk ≈ 97–98%"
]
fail = 0
for pat in MUST:
    if not re.search(pat, txt, re.M):
        print("[MISS]", pat); fail = 1
sys.exit(fail)
