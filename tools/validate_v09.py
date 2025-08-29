# check_must.py
import os, re, sys, pathlib

TXT = pathlib.Path("paper.txt")
if not TXT.exists():
    print("ERROR: paper.txt not found. Did you run `pdftotext main.pdf paper.txt`?")
    sys.exit(2)

text = TXT.read_text(encoding="utf-8")

def norm(s: str) -> str:
    # Нормализуем пробелы/дефисы/тильды/≈, чтобы регэкспы были стабильнее
    s = s.replace('\u2013','-').replace('\u2014','-')   # en/em dash -> -
    s = s.replace('\u2218','o')                        # случайные символы
    s = s.replace('\u2248','~')                        # ≈ -> ~
    s = re.sub(r'[ \t]+', ' ', s)
    return s

text = norm(text)

PROFILE = os.getenv("PROFILE", "stoc").lower()  # "internal" или "stoc"

if PROFILE == "internal":
    MUST = [
        r"Controlled Relaxations \(v0\.9\.1\)",
        r"Post-0\.8\.71\s+residual-?risk\s*(?:~|\\approx)?\s*97\s*-\s*98%",
    ]
else:
    # STOC/FOCS-ready: больше никаких версий/roadmap-якорей
    MUST = [
        # Заголовки разделов без версий (pdf-to-text часто делает их КАПСОМ — применяем i флаг)
        r"\bControlled Relaxations\b",
        r"\bBridges\b",
        r"\bModel Assumptions\b|\bAssumptions\b",
        r"\bArtifacts\b|\bReproducibility\b",
        # Мосты: текстовые маркеры теорем переноса
        r"\bMachine\s*↔?\s*Tree\b|\bMachine-to-Tree\b",
        r"\bTree\s*↔?\s*Circuit\b|\bTree-to-Circuit\b",
        # Упоминание релаксаций R1–R4 в тексте (без номеров версий)
        r"\b(randomness|public randomness)\b",
        r"\bmulti-?pass\b",
        r"\badvice\b",
        r"\bbandwidth\b",
    ]

fail = 0
for pat in MUST:
    if not re.search(pat, text, re.IGNORECASE | re.MULTILINE | re.DOTALL):
        print("[MISS]", pat)
        fail = 1

sys.exit(fail)
