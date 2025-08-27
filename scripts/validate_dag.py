#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate docs/deps/psi_dag.gv:
 - Acyclic graph
 - All referenced Lean IDs exist in paper/claims.yaml
"""
from __future__ import annotations
import sys
from pathlib import Path
import re
import yaml  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
DAG_PATH = ROOT / "docs" / "deps" / "psi_dag.gv"
CLAIMS = ROOT / "paper" / "claims.yaml"

EDGE_RE = re.compile(r"\s*\"([^\"]+)\"\s*->\s*\"([^\"]+)\"\s*;")
NODE_RE = re.compile(r"\s*\"([^\"]+)\"\s*;")

def parse_dot_edges(text: str) -> tuple[set[str], list[tuple[str,str]]]:
    nodes: set[str] = set(NODE_RE.findall(text))
    edges = EDGE_RE.findall(text)
    return nodes, edges

def is_acyclic(nodes: set[str], edges: list[tuple[str,str]]) -> bool:
    # Kahn's algorithm
    incoming = {n: 0 for n in nodes}
    adj: dict[str, list[str]] = {n: [] for n in nodes}
    for u, v in edges:
        if u not in nodes:
            nodes.add(u)
            incoming[u] = 0
            adj[u] = []
        if v not in nodes:
            nodes.add(v)
            incoming[v] = 0
            adj[v] = []
        adj[u].append(v)
        incoming[v] += 1
    queue = [n for n, deg in incoming.items() if deg == 0]
    visited = 0
    while queue:
        u = queue.pop()
        visited += 1
        for v in adj[u]:
            incoming[v] -= 1
            if incoming[v] == 0:
                queue.append(v)
    return visited == len(nodes)

def load_claim_ids() -> set[str]:
    data = yaml.safe_load(CLAIMS.read_text(encoding="utf-8"))
    ids: set[str] = set()
    for entry in data:
        ids.add(entry["lean"])
    return ids

def main() -> int:
    if not DAG_PATH.exists():
        print(f"[ERR] Missing DAG: {DAG_PATH}")
        return 1
    text = DAG_PATH.read_text(encoding="utf-8")
    nodes, edges = parse_dot_edges(text)
    ok = True
    if not is_acyclic(set(nodes), list(edges)):
        print("[ERR] Graph has a cycle")
        ok = False
    claim_ids = load_claim_ids()
    missing = sorted([n for n in nodes if n not in claim_ids])
    if missing:
        print("[ERR] Nodes not declared in paper/claims.yaml:")
        for m in missing:
            print(" -", m)
        ok = False
    if ok:
        print("[OK] DAG acyclic and all nodes covered by claims.yaml")
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())

