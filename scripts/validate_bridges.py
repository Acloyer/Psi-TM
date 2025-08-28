#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate bridges CSV against claims and explicit-loss/composition rules.

Checks:
  1) CSV rows ↔ paper/claims.yaml IDs 1:1 for the three bridge IDs.
  2) LossForm contains only allowed tokens: powers and log2 of named params.
  3) Composition: Loss(M<->C) equals product of Loss(M<->T) and Loss(T<->C).
"""
import argparse
import csv
import re
from pathlib import Path
import sys
import yaml  # type: ignore

ALLOWED_IDS = {
    "Bridge:MachineTree",
    "Bridge:TreeCircuit",
    "Bridge:MachineCircuit:Cor",
}

# Accept either unicode arrow or ASCII <-> in Bridge column
NORM_BRIDGE_NAME = {
    "Machine↔Tree": "Machine<->Tree",
    "Tree↔Circuit": "Tree<->Circuit",
    "Machine↔Circuit:Cor": "Machine<->Circuit:Cor",
}

# Allow composed log exponent as a+b
LOSS_RE = re.compile(
    r"^\(d\^[a-z]+\)\*\(log2\(n\)\^[a-z]+\)$"
    r"|^\(k\^[a-z]+\)\*\(log2\(n\)\^[a-z]+\)$"
    r"|^\(d\^[a-z]+\)\*\(k\^[a-z]+\)\*\(log2\(n\)\^[a-z]+(\+[a-z]+)?\)$"
)

def load_claims(claims_path: Path) -> set[str]:
    data = yaml.safe_load(claims_path.read_text(encoding="utf-8"))
    ids = {e["lean"] for e in data if isinstance(e, dict) and e.get("lean")}
    return ids

def parse_factors(loss: str) -> dict[str, str]:
    # Very small parser for patterns like (x^e)*(y^f)*(log2(n)^g)
    norm = loss.replace(" ", "")
    # Normalize unicode arrow or any stray characters (none expected here)
    parts = norm.split("*")
    exps: dict[str, str] = {}
    for p in parts:
        m = re.fullmatch(r"\(([^\)]+)\)", p)
        if not m:
            raise ValueError(f"Bad factor: {p}")
        base_exp = m.group(1)
        if base_exp.startswith("log2(n)^"):
            exps["log2(n)"] = base_exp.split("^")[1]
        else:
            base, exp = base_exp.split("^")
            exps[base] = exp
    return exps

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--claims", required=True)
    args = ap.parse_args()

    csv_path = Path(args.csv)
    claims_path = Path(args.claims)

    if not csv_path.exists():
        print(f"[ERR] Missing CSV: {csv_path}")
        return 1
    if not claims_path.exists():
        print(f"[ERR] Missing claims: {claims_path}")
        return 1

    claims_ids = load_claims(claims_path)
    missing_ids = [i for i in ALLOWED_IDS if i not in claims_ids]
    if missing_ids:
        print("[ERR] Claims missing bridge IDs:")
        for i in missing_ids:
            print(" -", i)
        return 1

    rows = list(csv.DictReader(csv_path.read_text(encoding="utf-8").splitlines()))
    if len(rows) != 3:
        print(f"[ERR] CSV must have exactly 3 rows, found {len(rows)}")
        return 1

    # Map by ReferenceLemma
    by_ref = {r["ReferenceLemma"]: r for r in rows}
    for rid in ALLOWED_IDS:
        if rid not in by_ref:
            print(f"[ERR] Missing row for {rid}")
            return 1

    # Explicit loss check
    for r in rows:
        lf = r.get("LossForm", "").strip()
        # Allow $...$ math wrappers from LaTeX table rendering
        if lf.startswith("$") and lf.endswith("$"):
            lf = lf[1:-1]
        if not lf:
            print(f"[ERR] Empty LossForm in row {r}")
            return 1
        if not LOSS_RE.fullmatch(lf):
            print(f"[ERR] LossForm not explicit or not allowed: {lf}")
            return 1

    # Composition check
    def clean(x: str) -> str:
        x = x.strip()
        return x[1:-1] if x.startswith("$") and x.endswith("$") else x
    l_mt = clean(by_ref["Bridge:MachineTree"]["LossForm"]) 
    l_tc = clean(by_ref["Bridge:TreeCircuit"]["LossForm"]) 
    l_mc = clean(by_ref["Bridge:MachineCircuit:Cor"]["LossForm"]) 

    f_mt = parse_factors(l_mt)
    f_tc = parse_factors(l_tc)
    f_mc = parse_factors(l_mc)

    # Expected composition exponents
    exp_d = f_mt.get("d")
    exp_k = f_tc.get("k")
    exp_log = None
    # log exponent is sum of the two exponents (symbolic add)
    if "log2(n)" in f_mt and "log2(n)" in f_tc:
        exp_log = f"{f_mt['log2(n)']}+{f_tc['log2(n)']}"
    else:
        print("[ERR] log2(n) exponent missing in base losses")
        return 1

    ok = True
    if f_mc.get("d") != exp_d:
        print(f"[ERR] d exponent mismatch: expected {exp_d}, got {f_mc.get('d')}")
        ok = False
    if f_mc.get("k") != exp_k:
        print(f"[ERR] k exponent mismatch: expected {exp_k}, got {f_mc.get('k')}")
        ok = False
    if f_mc.get("log2(n)") != exp_log:
        print(f"[ERR] log2 exponent mismatch: expected {exp_log}, got {f_mc.get('log2(n)')}")
        ok = False

    if not ok:
        return 1

    print("[OK] bridges.csv validated against claims and composition")
    return 0

if __name__ == "__main__":
    sys.exit(main())

