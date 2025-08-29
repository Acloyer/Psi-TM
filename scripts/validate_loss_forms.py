#!/usr/bin/env python3
import sys, argparse, csv, re

ALLOWED = re.compile(r'^\s*(?:log_2|B|n|d|k|M|\(|\)|\+|\s|\^|×|,|0|1|-)+'
                     r'\s*$')
ID      = re.compile(r'^[A-Z][A-Za-z0-9]*(?:\.[A-Za-z0-9_]+)+$')

def check_file(path, ref_col='ReferenceLemma'):
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        req = {'LossForm','Parameters',ref_col}
        missing = [c for c in req if c not in reader.fieldnames]
        if missing:
            print(f"[FAIL] {path}: missing columns {missing}")
            return 1
        ok = True
        for i,row in enumerate(reader,1):
            lf = row['LossForm']
            rl = row[ref_col]
            if not ALLOWED.match(lf or ''):
                print(f"[FAIL] {path}:{i} LossForm bad: {lf}")
                ok = False
            if not ID.match(rl or ''):
                print(f"[FAIL] {path}:{i} ReferenceLemma bad: {rl}")
                ok = False
        if ok:
            print(f"[OK] {path}")
        return 0 if ok else 1

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('--bridges', default=None)
    ap.add_argument('--relax', default=None)
    ap.add_argument('--dag', default=None)
    args = ap.parse_args()
    rc = 0
    for p in [args.bridges, args.relax, args.dag]:
        if p:
            rc |= check_file(p, ref_col='ReferenceLemma')
    sys.exit(rc)

