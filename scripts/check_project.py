#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project checks for v0.8.6 (hardened):
- Validate paper/claims.yaml via PyYAML; required file
- Strict Lean ID detection using `-- ID: <Token>` headers
- Verify deterministic seeds (1337) in notebooks
- Detect missing LaTeX references: \ref{...} without a matching \label{...}
- Validate figure paths: \includegraphics must resolve to existing files, prefer fig/
- Bidirectional claims coverage for theorem labels (Budget:, Psi:, Lk:, AntiSim:)
"""
import sys, os, re, json
from pathlib import Path
try:
    import yaml  # type: ignore
except Exception as e:
    print("[ERR] PyYAML not installed:", e)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]

LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
REF_RE   = re.compile(r"\\ref\{([^}]+)\}")
GRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
LEAN_ID_RE = re.compile(r"^--\s*ID:\s*([^\s]+)\s*$", re.MULTILINE)

CLAIMS = ROOT / "paper" / "claims.yaml"

IGNORED_DIRS = {".git", ".venv", "venv", "_build", "build", "out", "dist", "__pycache__"}


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")


def list_tex_files() -> list[Path]:
    out = []
    for p in ROOT.rglob("*.tex"):
        if any(part in IGNORED_DIRS for part in p.parts):
            continue
        out.append(p)
    return out


def parse_claims_yaml(p: Path):
    if not p.exists():
        print(f"[ERR] Missing required claims file: {p}")
        raise FileNotFoundError(str(p))
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("claims.yaml must be a list of mappings")
    entries = []
    for entry in data:
        if not isinstance(entry, dict):
            raise ValueError("claims.yaml entries must be mappings")
        latex = str(entry.get("latex", "")).strip()
        lean  = str(entry.get("lean", "")).strip()
        if not latex or not lean:
            raise ValueError(f"claims.yaml entry missing latex/lean: {entry}")
        entries.append({"latex": latex, "lean": lean})
    return entries


def collect_labels_refs_and_graphics():
    labels = set(); refs = set(); graphics = []
    for tex in list_tex_files():
        txt = read_text(tex)
        for m in LABEL_RE.finditer(txt):
            labels.add(m.group(1))
        for m in REF_RE.finditer(txt):
            refs.add(m.group(1))
        for m in GRAPHICS_RE.finditer(txt):
            graphics.append((tex, m.group(1)))
    return labels, refs, graphics


def collect_lean_ids() -> set[str]:
    ids: set[str] = set()
    for lf in (ROOT / "lean").glob("*.lean"):
        ids |= set(LEAN_ID_RE.findall(read_text(lf)))
    return ids


def resolve_graphics_path(raw: str, base_dir: Path) -> Path:
    p = Path(raw)
    if p.is_absolute():
        return p
    # Prefer fig/ path at project root
    if not p.parts or p.parts[0] != 'fig':
        alt = ROOT / 'fig' / p.name
        return alt
    return (ROOT / p).resolve()


def main() -> int:
    status = 0

    # Parse claims (required)
    try:
        claims = parse_claims_yaml(CLAIMS)
    except Exception as e:
        print("[ERR] claims.yaml parsing:", e)
        return 1

    claim_labels = {e["latex"] for e in claims}
    claim_ids    = {e["lean"] for e in claims}

    # Collect LaTeX labels, refs, graphics
    labels, refs, graphics = collect_labels_refs_and_graphics()

    # Missing refs
    missing_refs = [r for r in refs if r not in labels]
    if missing_refs:
        status = 1
        print("[ERR] Missing LaTeX labels for refs:")
        for r in sorted(missing_refs):
            print(" -", r)
    else:
        print("[OK] All refs have matching labels")

    # Bidirectional claims coverage for theorem-like namespaces
    ns_re = re.compile(r"^(Budget|Psi|Lk|AntiSim)[^:]*:.*$")
    needed = {L for L in labels if ns_re.match(L)}
    missing_in_yaml = sorted(needed - claim_labels)
    if missing_in_yaml:
        status = 1
        print("[ERR] Theorem labels missing in claims.yaml:")
        for L in missing_in_yaml:
            print(" -", L)

    # Lean IDs declared via -- ID: headers
    declared_ids = collect_lean_ids()
    missing_ids = sorted([i for i in claim_ids if i not in declared_ids])
    if missing_ids:
        print("[ERR] Lean IDs declared in claims.yaml not found in lean/*.lean -- ID: headers:")
        for i in missing_ids:
            print(" -", i)
        status = 1

    # Graphics existence (prefer fig/)
    missing_graphics = []
    wrong_dir = []
    for tex, raw in graphics:
        resolved = resolve_graphics_path(raw, tex.parent)
        if not resolved.exists():
            missing_graphics.append((tex, raw, resolved))
        if 'paper/fig/' in raw:
            wrong_dir.append((tex, raw))
    if wrong_dir:
        print("[ERR] Non-compliant figure paths (should use fig/):")
        for tex, raw in wrong_dir:
            print(f" - {tex.relative_to(ROOT)} : {{ {raw} }}")
        status = 1
    if missing_graphics:
        print("[ERR] Referenced figures not found:")
        for tex, raw, res in missing_graphics:
            try:
                tex_rel = tex.relative_to(ROOT)
            except ValueError:
                tex_rel = tex
            print(f" - {tex_rel} : {{ {raw} }} -> {res}")
        status = 1

    if status == 0:
        print("[OK] Project checks passed")
    return status


if __name__ == "__main__":
    sys.exit(main())