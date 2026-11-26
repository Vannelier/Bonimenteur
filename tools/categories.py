"""Catégorie grammaticale des définitions (champ `categorie` de data/questions.json).

Lue dans le Wiktionnaire : première section française de la page du mot
({{S|nom|fr}}, {{S|adjectif|fr}}…), genre pris sur la ligne de forme ({{m}}, {{f}}).
Affichée sur le feuillet de la vraie réponse ; le faussaire choisit celle de son faux
(docs/conception.md, « Fabriquer un faux »).

    python tools/categories.py            # relève les catégories manquantes, page par page
    python tools/categories.py --voir     # liste mot, catégorie, début de la vraie réponse

Les pages sont gardées dans tools/cache/wiktionnaire/ (ignoré par git).
Relire la liste : la première section n'est pas toujours le sens retenu.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
QUESTIONS = RACINE / "data" / "questions.json"
CACHE = RACINE / "tools" / "cache" / "wiktionnaire"
AGENT = "bonimenteur-outils/1.0 (jeu de mots ; relevé des catégories)"
PAUSE_S = 1.0   # une page par seconde : le Wiktionnaire limite les robots trop pressés

SECTIONS = {"nom": "n.", "adjectif": "adj.", "verbe": "v.", "adverbe": "adv.", "interjection": "interj.",
            "locution-phrase": "loc.", "locution nominale": "loc. n."}


def page(mot: str) -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / (urllib.parse.quote(mot, safe="") + ".txt")
    if f.exists():
        return f.read_text()
    url = "https://fr.wiktionary.org/w/index.php?" + urllib.parse.urlencode({"title": mot, "action": "raw"})
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": AGENT}), timeout=20) as r:
        texte = r.read().decode()
    f.write_text(texte)
    time.sleep(PAUSE_S)
    return texte


def categorie(texte: str) -> str | None:
    m = re.search(r"===\s*\{\{S\|([^|}]+)\|fr[^}]*\}\}\s*===(.*?)(?:\n===|\Z)", texte, re.S)
    if not m:
        return None
    sorte, corps = m.group(1).strip(), m.group(2)
    cat = SECTIONS.get(sorte)
    if cat == "n.":
        forme = next((l for l in corps.splitlines() if l.startswith("'''")), "")
        if "{{mf}}" in forme or "{{m}}" in forme and "{{f}}" in forme:
            cat = "n."
        elif "{{m}}" in forme:
            cat = "n. m."
        elif "{{f}}" in forme:
            cat = "n. f."
    return cat


def main():
    questions = json.loads(QUESTIONS.read_text())
    definitions = {k: q for k, q in questions.items() if not q.get("type")}
    if "--voir" in sys.argv:
        for k, q in definitions.items():
            print(f"{q['mot']:<40} {q.get('categorie', '?'):<8} {q['vraie'][:50]}")
        return
    for k, q in definitions.items():
        if q.get("categorie"):
            continue
        try:
            cat = categorie(page(q["mot"]))
        except Exception as e:  # page absente, réseau
            print(f"{q['mot']} : {e}", file=sys.stderr)
            continue
        if cat:
            q["categorie"] = cat
            q.setdefault("source", f"wiktionary:{q['mot']}")
        else:
            print(f"{q['mot']} : catégorie introuvable", file=sys.stderr)
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=1) + "\n")
    print(sum(1 for q in definitions.values() if q.get("categorie")), "sur", len(definitions), "définitions ont leur catégorie")


if __name__ == "__main__":
    main()
