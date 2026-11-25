"""Import de questions par lots (docs/questions.md, « Ajouter des questions par lots »).

Un lot est un fichier JSON écrit à la main dans tools/lots/ :

    {"communes": [["Bourg-Achard", "27", ["Faux-un", "Faux-deux", "Faux-trois"]], ...],
     "questions": [{"id": "mot", "mot": "mot", "vraie": "…", "categorie": "n. m.",
                    "source": "wiktionary:mot", "faux": ["…", "…", "…"]}, ...]}

Communes : nom exact de geo.api.gouv.fr (département demandé si plusieurs communes portent
ce nom) ; la question, l'identifiant et la source sont écrits par l'outil. Questions : champs
de data/questions.json, plus « faux » (les trois faux de Mr Halifax).

    python tools/lot.py tools/lots/lot1.json             # contrôle, n'écrit rien
    python tools/lot.py tools/lots/lot1.json --fusionner # contrôle puis ajoute aux données
    VOCABULIUM_DIR=../Vocabulium python tools/proches.py # arbitre du sens à jour
    python tools/lot.py --arbitre                        # faux de Mr Halifax trop proches

Ne montre que ce qui cloche (et, pour les définitions, la première définition du
Wiktionnaire, à comparer à la vraie) : un lot de 25 tient en quelques lignes.
"""
import json
import re
import subprocess
import sys
import time
import unicodedata
import urllib.parse
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
QUESTIONS = RACINE / "data" / "questions.json"
FAUX = RACINE / "data" / "faux-de-depart.json"
COMMUNES = RACINE / "prototype" / "communes.txt"
PROCHES = RACINE / "prototype" / "proches.json"
CACHE = RACINE / "tools" / "cache"
AGENT = "bonimenteur-outils/1.0 (jeu de mots ; import de questions)"

# Seuils de l'arbitre par thème (FAMILLES de prototype/index.html, docs/arbitre.md).
SEUILS = {"definition": 0.5, "anecdote": 0.65, "coutume": 0.65, "expression": 0.65, "photo": 0.65,
          "intraduisible": 0.55, "etrangere": 0.55, "metier": 0.5}
CATEGORIES = {"n. m.", "n. f.", "n.", "adj.", "v.", "adv."}

# « Quel nom de commune de la Mayenne… » : article de chaque département (code INSEE).
DE = {"01": "de l'Ain", "02": "de l'Aisne", "03": "de l'Allier", "04": "des Alpes-de-Haute-Provence",
      "05": "des Hautes-Alpes", "06": "des Alpes-Maritimes", "07": "de l'Ardèche", "08": "des Ardennes",
      "09": "de l'Ariège", "10": "de l'Aube", "11": "de l'Aude", "12": "de l'Aveyron", "13": "des Bouches-du-Rhône",
      "14": "du Calvados", "15": "du Cantal", "16": "de la Charente", "17": "de la Charente-Maritime", "18": "du Cher",
      "19": "de la Corrèze", "2A": "de Corse-du-Sud", "2B": "de Haute-Corse", "21": "de la Côte-d'Or",
      "22": "des Côtes-d'Armor", "23": "de la Creuse", "24": "de la Dordogne", "25": "du Doubs", "26": "de la Drôme",
      "27": "de l'Eure", "28": "d'Eure-et-Loir", "29": "du Finistère", "30": "du Gard", "31": "de la Haute-Garonne",
      "32": "du Gers", "33": "de la Gironde", "34": "de l'Hérault", "35": "d'Ille-et-Vilaine", "36": "de l'Indre",
      "37": "d'Indre-et-Loire", "38": "de l'Isère", "39": "du Jura", "40": "des Landes", "41": "de Loir-et-Cher",
      "42": "de la Loire", "43": "de la Haute-Loire", "44": "de la Loire-Atlantique", "45": "du Loiret", "46": "du Lot",
      "47": "de Lot-et-Garonne", "48": "de la Lozère", "49": "de Maine-et-Loire", "50": "de la Manche", "51": "de la Marne",
      "52": "de la Haute-Marne", "53": "de la Mayenne", "54": "de Meurthe-et-Moselle", "55": "de la Meuse",
      "56": "du Morbihan", "57": "de la Moselle", "58": "de la Nièvre", "59": "du Nord", "60": "de l'Oise", "61": "de l'Orne",
      "62": "du Pas-de-Calais", "63": "du Puy-de-Dôme", "64": "des Pyrénées-Atlantiques", "65": "des Hautes-Pyrénées",
      "66": "des Pyrénées-Orientales", "67": "du Bas-Rhin", "68": "du Haut-Rhin", "69": "du Rhône", "70": "de la Haute-Saône",
      "71": "de Saône-et-Loire", "72": "de la Sarthe", "73": "de la Savoie", "74": "de la Haute-Savoie", "75": "de Paris",
      "76": "de la Seine-Maritime", "77": "de Seine-et-Marne", "78": "des Yvelines", "79": "des Deux-Sèvres",
      "80": "de la Somme", "81": "du Tarn", "82": "de Tarn-et-Garonne", "83": "du Var", "84": "du Vaucluse",
      "85": "de la Vendée", "86": "de la Vienne", "87": "de la Haute-Vienne", "88": "des Vosges", "89": "de l'Yonne",
      "90": "du Territoire de Belfort", "91": "de l'Essonne", "92": "des Hauts-de-Seine", "93": "de la Seine-Saint-Denis",
      "94": "du Val-de-Marne", "95": "du Val-d'Oise"}


def plat(s: str) -> str:
    """Forme de communes.txt (nomCommune de la page)."""
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[-']", " ", s)).strip()


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", plat(s)).strip("-")


def lire(url: str, fichier: Path) -> str:
    """Page gardée en cache. Par curl : Wikimedia répond 429 à urllib (empreinte du client), pas
    à curl (relevé du 26/11/2026)."""
    if fichier.exists():
        return fichier.read_text()
    for essai in range(4):
        r = subprocess.run(["curl", "-s", "-A", AGENT, "-w", "\n%{http_code}", url], capture_output=True, text=True, timeout=30)
        corps, _, code = r.stdout.rpartition("\n")
        if code == "200":
            fichier.parent.mkdir(parents=True, exist_ok=True)
            fichier.write_text(corps)
            time.sleep(0.3)
            return corps
        if code == "404":
            return ""
        time.sleep(2 * (essai + 1))
    return ""


def commune(nom: str, dep: str | None):
    url = "https://geo.api.gouv.fr/communes?" + urllib.parse.urlencode({"nom": nom, "fields": "nom,departement", "limit": 50})
    r = json.loads(lire(url, CACHE / "geo" / (slug(nom) + ".json")) or "[]")
    exacts = [c for c in r if c["nom"] == nom and (not dep or c["departement"]["code"] == dep)]
    return exacts


def premiere_definition(mot: str) -> str:
    """Premier sens de la section française du Wiktionnaire, sans modèles ni liens."""
    url = "https://fr.wiktionary.org/w/index.php?" + urllib.parse.urlencode({"title": mot, "action": "raw"})
    t = lire(url, CACHE / "wiktionnaire" / (urllib.parse.quote(mot, safe="") + ".txt"))
    if "{{langue|fr}}" not in t:
        return ""
    t = t.split("{{langue|fr}}", 1)[1].split("== {{langue|", 1)[0]
    for l in t.splitlines():
        if l.startswith("# ") or l.startswith("#{{"):
            l = re.sub(r"\{\{([^{}|]*)\|?[^{}]*\}\}", lambda m: f"({m.group(1)}) " if m.group(1) not in ("w", "lien") else "", l)
            l = re.sub(r"\[\[(?:[^]|]*\|)?([^]]*)\]\]", r"\1", l).replace("'''", "").replace("''", "")
            return l.lstrip("# ").strip()[:160]
    return "?"


def famille(q):
    return q.get("type") or "definition"


def controler(lot: dict, questions: dict, faux: list):
    reels = set(COMMUNES.read_text().split("\n"))
    nouvelles, nouveaux, erreurs, notes = {}, [], [], []
    for nom, dep, fx in lot.get("communes", []):
        cs = commune(nom, dep)
        if len(cs) != 1:
            erreurs.append(f"commune {nom} ({dep or '?'}) : {len(cs)} trouvée(s) — {[c['departement']['code'] for c in commune(nom, None)]}")
            continue
        c = cs[0]
        if plat(nom) not in reels:
            erreurs.append(f"commune {nom} : absente de communes.txt")
        qid = "c-" + slug(nom)
        nouvelles[qid] = {"mot": "", "question": f"Quel nom de commune {DE[c['departement']['code']]} existe réellement ?",
                          "type": "commune", "vraie": nom, "source": "geo.api.gouv.fr", "_faux": fx}
        for f in fx:
            if plat(f) in reels:
                erreurs.append(f"commune {nom} : le faux « {f} » est une vraie commune")
    for q in lot.get("questions", []):
        q = dict(q)
        qid = q.pop("id")
        q["_faux"] = q.pop("faux")
        nouvelles[qid] = q
    deja_vrais = {plat(q["vraie"]) for q in questions.values()}
    for qid, q in nouvelles.items():
        fx, fam = q["_faux"], famille(q)
        if qid in questions:
            erreurs.append(f"{qid} : identifiant déjà pris")
        if q.get("mot") and any(o.get("mot") == q["mot"] for o in questions.values()):
            erreurs.append(f"{qid} : mot déjà en jeu")
        if plat(q["vraie"]) in deja_vrais:
            erreurs.append(f"{qid} : vraie réponse déjà en jeu")
        if len(fx) != 3 or len({plat(f) for f in fx} | {plat(q["vraie"])}) != 4:
            erreurs.append(f"{qid} : il faut trois faux distincts, et distincts de la vraie")
        if fam != "commune" and not q.get("source"):
            erreurs.append(f"{qid} : pas de source")
        if fam == "definition":
            if q.get("categorie") not in CATEGORIES:
                erreurs.append(f"{qid} : catégorie {q.get('categorie')!r}")
            for t in [q["vraie"], *fx]:
                if not (t[:1].isupper() and t.endswith(".")):
                    erreurs.append(f"{qid} : « {t} » : majuscule et point final")
            if q.get("source", "").startswith("wiktionary:"):
                notes.append(f"{qid:22} vraie : {q['vraie']}\n{'':22} wikt. : {premiere_definition(q['source'].split(':', 1)[1]) or 'PAGE ABSENTE'}")
        # La vraie ne doit pas se trahir par sa longueur (escarbille, lot 01 : 82 signes contre 40).
        moy = sum(len(f) for f in fx) / max(len(fx), 1)
        if fam != "commune" and moy and not 0.7 <= len(q["vraie"]) / moy <= 1.35:
            erreurs.append(f"{qid} : vraie de {len(q['vraie'])} signes, faux de {moy:.0f} en moyenne")
        for i, f in enumerate(fx, 1):
            nouveaux.append({"id": f"t-{qid}-{i}", "mot": qid, "texte": f})
    return nouvelles, nouveaux, erreurs, notes


def arbitre():
    """Faux de Mr Halifax que l'arbitre de la page refuserait (memeSens : score ≥ seuil du thème)."""
    d = json.loads(PROCHES.read_text())
    vides, inconnu = set(d["vides"]), d["inconnu"]
    questions = json.loads(QUESTIONS.read_text())
    n = 0
    for f in json.loads(FAUX.read_text()):
        q = questions.get(f["mot"])
        L = d["mots"].get(f["mot"])
        if not q or not L or famille(q) == "commune":
            continue
        cadre = set(q.get("cadre", []))
        ws = [w for w in re.findall(r"[a-zàâäéèêëîïôöùûüçœ-]+", f["texte"].lower()) if w not in vides and w not in cadre]
        if not ws:
            continue
        s = max(sum(L[w][0] if w in L else inconnu for w in ws) / len(ws), max(L[w][1] if w in L else 0 for w in ws))
        if s >= SEUILS[famille(q)] - 0.03:
            n += 1
            print(f"{s:.2f}/{SEUILS[famille(q)]}  {f['mot']} : {f['texte']}")
    print(f"{n} faux à 0,03 du seuil ou au-dessus")


def main():
    if "--arbitre" in sys.argv:
        return arbitre()
    lot = json.loads(Path(sys.argv[1]).read_text())
    questions, faux = json.loads(QUESTIONS.read_text()), json.loads(FAUX.read_text())
    nouvelles, nouveaux, erreurs, notes = controler(lot, questions, faux)
    for n in notes:
        print(n)
    for e in erreurs:
        print("ERREUR", e)
    print(f"{len(nouvelles)} questions, {len(nouveaux)} faux, {len(erreurs)} erreurs")
    if erreurs or "--fusionner" not in sys.argv:
        return
    for qid, q in nouvelles.items():
        q.pop("_faux")
        questions[qid] = q
    QUESTIONS.write_text(json.dumps(questions, ensure_ascii=False, indent=1) + "\n")
    FAUX.write_text(json.dumps(faux + nouveaux, ensure_ascii=False, indent=1) + "\n")
    print(f"fusionné : {len(questions)} questions, {len(faux) + len(nouveaux)} faux")


if __name__ == "__main__":
    main()
