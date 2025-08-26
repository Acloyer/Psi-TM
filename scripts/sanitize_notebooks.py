# scripts/sanitize_notebooks.py
import json
from pathlib import Path

for p in Path("notebooks").glob("*.ipynb"):
    txt = p.read_text(encoding="utf-8").replace("ψ","Psi").replace("–","-")
    nb = json.loads(txt)
    changed = False
    for c in nb.get("cells", []):
        if c.get("cell_type") == "code" and c.get("source"):
            src = "".join(c["source"]).lstrip()
            if src and not src.startswith(("#","'''",'"""',"import","from","def","class","for","while","if","with","try","print","%")):
                c["source"] = ['"""'] + c["source"] + ['"""\n']
                changed = True
    if changed:
        p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
