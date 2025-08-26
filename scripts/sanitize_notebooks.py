# scripts/sanitize_notebooks.py
import json
from pathlib import Path

ALLOW_PREFIXES = ("#", "'''", '"""', "import", "from", "def",
                  "class", "for", "while", "if", "with", "try",
                  "print", "%")

def needs_wrap(lines):
    for ln in lines:
        s = ln.lstrip()
        if not s:
            continue
        if not s.startswith(ALLOW_PREFIXES):
            return True
    return False

changed_any = False
for p in Path("notebooks").glob("*.ipynb"):
    nb = json.loads(p.read_text(encoding="utf-8").replace("ψ", "Psi").replace("–", "-"))
    changed = False
    for c in nb.get("cells", []):
        if c.get("cell_type") == "code" and isinstance(c.get("source"), list):
            if needs_wrap(c["source"]):
                c["source"] = ['"""'] + c["source"] + ['"""\n']
                changed = True
                changed_any = True
    if changed:
        p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

if changed_any:
    print("Sanitized notebooks.")
else:
    print("No changes needed.")
