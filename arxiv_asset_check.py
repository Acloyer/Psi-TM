#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arxiv_asset_check.py — scan a LaTeX project and find unused/missing figures.

Usage:
  python arxiv_asset_check.py --root /path/to/project --ext png,pdf,jpg,jpeg,eps

What it does:
  - Recursively scans .tex files for \includegraphics[...]{...} and \graphicspath{ {dir/}{dir2/} }
  - Resolves figure paths relative to each .tex file, project root, and graphicspath dirs
  - Lists:
      * REFERENCED BUT MISSING (used in TeX, file not found)
      * PRESENT BUT UNUSED (on disk, but not referenced anywhere)
  - Writes 'delete_unused_figs.sh' and 'delete_unused_figs.ps1' to remove UNUSED images

Notes:
  - If an \includegraphics omits extension, we try all provided extensions (default png,pdf,jpg,jpeg,eps)
  - Ignores build folders: .git, (v)env, _build, build, out, dist, __pycache__
"""

import argparse, re, sys, os
from pathlib import Path

DEFAULT_IMG_EXTS = [".png", ".pdf", ".jpg", ".jpeg", ".eps"]

INCLUDE_RE = re.compile(r"""\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}""", re.MULTILINE)
# \graphicspath{{fig/}{paper/fig/}}
GSPATH_RE  = re.compile(r"""\\graphicspath\{\s*(\{[^}]+\}\s*)+\}""", re.MULTILINE)
BRACED_DIR_RE = re.compile(r"""\{([^}]+)\}""")

IGNORE_DIRS = {".git", ".venv", "venv", "_build", "build", "out", "dist", "__pycache__"}

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="ignore")

def strip_comments(tex: str) -> str:
    out = []
    for line in tex.splitlines():
        # drop content after % (but keep \% )
        i = 0
        while True:
            j = line.find("%", i)
            if j == -1: 
                out.append(line)
                break
            if j > 0 and line[j-1] == "\\":
                i = j + 1
                continue
            out.append(line[:j])
            break
    return "\n".join(out)

def find_tex_files(root: Path):
    for p in root.rglob("*.tex"):
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        yield p

def parse_graphicspaths(tex_text: str, base_dir: Path) -> list[Path]:
    """Return list of directories (absolute Paths) from \graphicspath, relative to base_dir."""
    dirs: list[Path] = []
    for m in GSPATH_RE.finditer(tex_text):
        for dm in BRACED_DIR_RE.finditer(m.group(0)):
            raw = dm.group(1).strip()
            if not raw:
                continue
            # normalize trailing slash
            p = Path(raw)
            if not p.is_absolute():
                p = (base_dir / p).resolve()
            dirs.append(p)
    return dirs

def candidate_paths(raw_ref: str, base_dir: Path, exts: list[str], gspath_dirs: list[Path]) -> list[Path]:
    """Produce candidate absolute paths for a single \includegraphics reference."""
    cands: list[Path] = []
    ref = Path(raw_ref)
    # if path contains ~ or user vars, leave as-is (unlikely in TeX)
    if ref.suffix.lower() in exts:
        paths = [ref] if ref.is_absolute() else [
            (base_dir / ref).resolve(),
            (Path.cwd() / ref).resolve()
        ]
    else:
        # try with each extension
        paths = []
        for ext in exts:
            if ref.is_absolute():
                paths.append(ref.with_suffix(ext))
            else:
                paths.append((base_dir / (str(ref) + ext)).resolve())
                paths.append((Path.cwd() / (str(ref) + ext)).resolve())
                # also try under graphicspath dirs
                for d in gspath_dirs:
                    paths.append((d / (str(ref) + ext)).resolve())
    # remove duplicates preserving order
    seen = set(); 
    for p in paths:
        if p not in seen:
            cands.append(p); seen.add(p)
    return cands

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=str, default=".", help="LaTeX project root")
    ap.add_argument("--ext", type=str, default="png,pdf,jpg,jpeg,eps",
                    help="Comma-separated image extensions to consider")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"[ERR] root path does not exist: {root}", file=sys.stderr); sys.exit(1)
    img_exts = ["." + e.strip().lower().lstrip(".") for e in args.ext.split(",") if e.strip()]
    if not img_exts:
        img_exts = DEFAULT_IMG_EXTS

    # 1) scan .tex files, collect \includegraphics and \graphicspath
    include_slots: list[tuple[Path,str,list[Path]]] = []  # (tex_file, raw_ref, candidate_paths)
    referenced_files: set[Path] = set()
    missing_refs: list[tuple[Path,str,list[Path]]] = []

    all_gspath_dirs: dict[Path, list[Path]] = {}

    for tex in find_tex_files(root):
        text = strip_comments(read_text(tex))
        gspath_dirs = parse_graphicspaths(text, tex.parent)
        all_gspath_dirs[tex] = gspath_dirs
        for m in INCLUDE_RE.finditer(text):
            raw = m.group(1).strip()
            cands = candidate_paths(raw, tex.parent, img_exts, gspath_dirs)
            include_slots.append((tex, raw, cands))

    # 2) collect present images under root
    present: set[Path] = set()
    for ext in img_exts:
        for p in root.rglob(f"*{ext}"):
            if any(part in IGNORE_DIRS for part in p.parts):
                continue
            present.add(p.resolve())

    # 3) resolve which referenced exist; mark missing
    satisfied: set[Path] = set()
    for tex, raw, cands in include_slots:
        exists = [c for c in cands if c.exists()]
        if exists:
            # count the first existing as the resolution (LaTeX will use search order)
            satisfied.add(exists[0])
        else:
            missing_refs.append((tex, raw, cands))

    # 4) compute unused (present but not referenced)
    unused = sorted([p for p in present if p not in satisfied], key=lambda p: str(p))

    # 5) print report
    print("="*72)
    print("[SUMMARY]")
    print(f"Project root: {root}")
    print(f".tex files scanned: {len(list(find_tex_files(root)))}")
    print(f"Referenced figure slots: {len(include_slots)}")
    print(f"Present images: {len(present)}")
    print(f"Resolved references: {len(satisfied)}")
    print(f"Referenced but MISSING: {len(missing_refs)}")
    print(f"Present but UNUSED: {len(unused)}")
    print("="*72)

    if missing_refs:
        print("\n[REFERENCED BUT MISSING]")
        for tex, raw, cands in missing_refs:
            print(f"- {tex.relative_to(root)} : {{ {raw} }}")
            for c in cands:
                try:
                    print(f"    tried: {c.relative_to(root)}")
                except ValueError:
                    print(f"    tried: {c}")

    if unused:
        print("\n[PRESENT BUT UNUSED]")
        for p in unused:
            try:
                print(str(p.relative_to(root)))
            except ValueError:
                print(str(p))

    # 6) write deletion scripts (UNUSED)
    if unused:
        sh = root / "delete_unused_figs.sh"
        ps1 = root / "delete_unused_figs.ps1"
        def rel(p: Path) -> str:
            try:
                return str(p.relative_to(root))
            except ValueError:
                return str(p)

        with sh.open("w", encoding="utf-8") as f:
            f.write("#!/usr/bin/env bash\nset -euo pipefail\n")
            for p in unused:
                f.write(f"rm -f '{rel(p)}'\n")
        os.chmod(sh, 0o755)

        with ps1.open("w", encoding="utf-8") as f:
            f.write("$ErrorActionPreference = 'Stop'\n")
            for p in unused:
                f.write(f"Remove-Item -LiteralPath '{rel(p)}' -Force\n")

        print(f"\nWrote deletion scripts:\n- {sh}\n- {ps1}")

if __name__ == "__main__":
    main()
