#!/usr/bin/env python3
import sys, argparse, csv, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / 'paper' / 'claims.yaml'

try:
    import yaml  # type: ignore
except Exception as e:
    yaml = None

LOSS = re.compile(
    r'^\s*\(log_2\s*M\)\^\s*(?P<a>-?\d+|α|β)\s*×\s*\(B\(\s*d\s*,\s*n\s*\)\)\^\s*(?P<b>-?\d+|α|β)\s*\s*$'
)
ID = re.compile(r'^[A-Z][A-Za-z0-9]*(?:\.[A-Za-z0-9_]+)+$')
HEADERS = {"From","To","LossForm","Parameters","ReferenceLemma","Notes"}

def load_known_ids(claims_path: str) -> set[str]:
    claims_file = Path(claims_path)
    if yaml is None or not claims_file.exists():
        return set()
    data = yaml.safe_load(claims_file.read_text(encoding='utf-8'))
    ids: set[str] = set()
    if isinstance(data, list):
        for entry in data:
            lean = entry.get('lean') if isinstance(entry, dict) else None
            if isinstance(lean, str):
                ids.add(lean)
    return ids

from typing import Set, Dict, List, Tuple

def check_csv(path: Path, known: Set[str], strict: bool) -> int:
    rc = 0
    with path.open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if set(reader.fieldnames or []) != HEADERS:
            print(f"[FAIL] {path}: headers must be exactly {sorted(HEADERS)}, got {reader.fieldnames}")
            return 1
        # ID format checks + loss regex
        nodes: Set[str] = set()
        edges: List[Tuple[str,str]] = []
        ok = True
        for i, row in enumerate(reader, 1):
            frm = row['From'] or ''
            to = row['To'] or ''
            lf = row['LossForm'] or ''
            rl = row['ReferenceLemma'] or ''
            # exact loss grammar
            if not LOSS.match(lf):
                print(f"[FAIL] {path}:{i} LossForm regex mismatch: {lf}")
                ok = False
            # strict node existence in claims if requested
            if strict:
                if frm not in known:
                    print(f"[FAIL] {path}:{i} From node not found in claims.yaml: {frm}")
                    ok = False
                if to not in known:
                    print(f"[FAIL] {path}:{i} To node not found in claims.yaml: {to}")
                    ok = False
            # reference must exist in claims
            if rl not in known:
                print(f"[FAIL] {path}:{i} ReferenceLemma unknown: {rl}")
                ok = False
            nodes.add(frm); nodes.add(to)
            edges.append((frm, to))
        if not ok:
            rc |= 1
        # DAG acyclicity via Kahn's algorithm
        adj: Dict[str, Set[str]] = {n: set() for n in nodes}
        indeg: Dict[str, int] = {n: 0 for n in nodes}
        for a, b in edges:
            if b not in adj[a]:
                adj[a].add(b)
                indeg[b] += 1
        queue = [n for n, d in indeg.items() if d == 0]
        topo: list[str] = []
        while queue:
            u = queue.pop()
            topo.append(u)
            for v in list(adj[u]):
                indeg[v] -= 1
                adj[u].remove(v)
                if indeg[v] == 0:
                    queue.append(v)
        remaining = sum(len(s) for s in adj.values())
        if remaining != 0:
            print(f"[FAIL] {path}: cycle(s) detected; not a DAG")
            rc |= 1
        if rc == 0:
            print(f"[OK] {path}")
        return rc

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', required=True)
    ap.add_argument('--claims', default=str(CLAIMS))
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args()
    known = load_known_ids(args.claims)
    return check_csv(Path(args.csv), known, args.strict)

if __name__ == '__main__':
    sys.exit(main())

