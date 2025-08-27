#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate synthetic counterexamples/stress instances for LB/UB/Anti-Sim.
Writes CSVs to results/<DATE>/stress_firebreak/ and plots to fig/.
Deterministic with seed=1337.
"""
from __future__ import annotations
import random
import csv
from pathlib import Path
from datetime import date

SEED = 1337
random.seed(SEED)

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results" / date.today().isoformat() / "stress_firebreak"
FIG_DIR = ROOT / "fig"

def ensure_dirs() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

def synth_rows(num: int = 64) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for _ in range(num):
        k = random.choice([2,3,4])
        n = random.choice([2**p for p in range(6, 14)])
        d = random.choice([1,2,3])
        extra = random.choice([1,2,4])
        rows.append({"k": k, "n": n, "d": d, "extra": extra})
    return rows

def write_csv(rows: list[dict[str,int]]) -> Path:
    out = RESULTS_DIR / "stress_params.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["k","n","d","extra"])
        w.writeheader()
        w.writerows(rows)
    return out

def main() -> int:
    ensure_dirs()
    rows = synth_rows()
    out_csv = write_csv(rows)
    print(f"[OK] Wrote {out_csv}")
    print(f"[OK] Plots should be saved under {FIG_DIR} by notebooks")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

