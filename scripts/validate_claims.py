#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate paper/claims.yaml structure and uniqueness, and ensure referenced Lean IDs
are declared with strict header lines in lean/*.lean files:
  -- ID: <Token>
"""
import sys
from pathlib import Path
import yaml  # type: ignore
import re

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "paper/claims.yaml"
LEAN_ID_RE = re.compile(r"^--\s*ID:\s*([^\s]+)\s*$", re.MULTILINE)

def collect_declared_ids() -> set[str]:
    ids: set[str] = set()
    for lf in (ROOT / "lean").rglob("*.lean"):
        ids |= set(LEAN_ID_RE.findall(lf.read_text(encoding='utf-8', errors='ignore')))
    return ids

def main() -> int:
    if not CLAIMS.exists():
        print(f"[ERR] Missing claims file: {CLAIMS}")
        return 1
    data = yaml.safe_load(CLAIMS.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        print("[ERR] claims.yaml must be a list of mappings")
        return 1
    latex_set = set()
    lean_set = set()
    ok = True
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            print(f"[ERR] Entry {i} is not a mapping")
            ok = False; continue
        latex = entry.get('latex'); lean = entry.get('lean')
        if not latex or not lean:
            print(f"[ERR] Entry {i} missing 'latex' or 'lean': {entry}")
            ok = False; continue
        if latex in latex_set:
            print(f"[ERR] Duplicate LaTeX label: {latex}")
            ok = False
        if lean in lean_set:
            print(f"[ERR] Duplicate Lean ID: {lean}")
            ok = False
        latex_set.add(latex); lean_set.add(lean)
    declared = collect_declared_ids()
    undeclared = sorted([i for i in lean_set if i not in declared])
    if undeclared:
        ok = False
        print("[ERR] Lean IDs not declared with strict '-- ID:' header:")
        for i in undeclared:
            print(" -", i)
    if ok:
        print("[OK] claims.yaml is valid and Lean IDs are declared")
        return 0
    return 1

if __name__ == '__main__':
    sys.exit(main())