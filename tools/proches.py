"""Données de l'arbitre du sens : prototype/proches/ (index.json et un paquet par groupe de questions).

Pour chaque question (sauf les communes, jugées sur la liste officielle), les mots
du vocabulaire dont la proximité atteint SEUIL_LISTE, avec deux nombres :
[proximité au plus proche mot de la vraie réponse, proximité au mot de la question].
La page en tire le score d'un faux (prototype/index.html, `memeSens`) :
max(moyenne des proximités des mots du faux, la plus forte proximité au mot).
Un mot absent de la liste compte pour INCONNU.

Vecteurs : ConceptNet Numberbatch FR de Vocabulium (vocab.json, vectors.f16.npy,
et les mots rares du joueur vocab-joueur.json, vectors-joueur.f16.npy).

    VOCABULIUM_DIR=../Vocabulium python tools/proches.py

À relancer après chaque ajout de question (data/questions.json).
"""
import json
import os
import re
import sys
from pathlib import Path

import numpy as np

RACINE = Path(__file__).resolve().parent.parent
VOCAB = Path(os.environ.get("VOCABULIUM_DIR", RACINE.parent / "Vocabulium")) / "data"

# Mesure (prototype, novembre 2026) : 25 reformulations de vraies définitions et
# 75 faux de Truffe ; à 0,45 la liste garde tous les mots utiles au seuil de 0,5.
SEUIL_LISTE = 0.45
# Un mot du faux absent de la liste : proximité supposée (proche du bruit de fond).
INCONNU = 0.25
# Mots qui ne portent pas le sens : les 200 plus fréquents, les mots-outils et les
# mots de cadrage des définitions (« se dit d'une personne… »).
OUTILS = set("qui que une des les pour dans avec sans par sur est son sa ses se de la le du au aux en et ou un à d l qu s n y dont".split())
CADRAGE = set("personne personnes quelqu quelqu'un quelque chose choses celui celle ceux individu individus fait action relatif relative relatifs état manière sorte genre objet très dit dite".split())
# Mots communs à toute une série (« Collectionneur de… », « Peur de… ») : ignorés des
# deux côtés, sinon 19 faux honnêtes sur 48 étaient refusés.
CADRE = set(json.loads((RACINE / "tools" / "cadre.json").read_text()))
SERIES = ("Collectionneur", "Peur", "Attirance")
PAQUETS = 32


def paquet(qid: str) -> int:
    """Paquet d'une question : somme des points de code de l'identifiant, modulo PAQUETS (même
    calcul dans la page, paquetDe)."""
    return sum(ord(c) for c in qid) % PAQUETS


def main():
    base = json.loads((VOCAB / "vocab.json").read_text())["words"]
    rares = json.loads((VOCAB / "vocab-joueur.json").read_text())["words"]
    X = np.concatenate([
        np.asarray(np.load(VOCAB / "vectors.f16.npy"), dtype=np.float32),
        np.asarray(np.load(VOCAB / "vectors-joueur.f16.npy"), dtype=np.float32),
    ])
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    tous = base + rares
    idx = {m: i for i, m in enumerate(tous)}
    vides = set(base[:200]) | OUTILS | CADRAGE

    def mots(texte, cadre=()):
        ws = re.findall(r"[a-zàâäéèêëîïôöùûüçœ-]+", texte.lower())
        serie = texte.startswith(SERIES)
        return [w for w in ws if w not in vides and w not in cadre and not (serie and w in CADRE)]

    questions = json.loads((RACINE / "data" / "questions.json").read_text())
    sortie = {}
    for qid, q in questions.items():
        if q.get("type") == "commune":
            continue
        vt = [w for w in mots(q["vraie"], set(q.get("cadre", []))) if w in idx]
        a = (X @ X[[idx[w] for w in vt]].T).max(1) if vt else np.zeros(len(X))
        mot = (q.get("mot") or "").lower()
        c = X @ X[idx[mot]] if mot in idx else np.zeros(len(X))
        garde = np.where((a >= SEUIL_LISTE) | (c >= SEUIL_LISTE))[0]
        sortie[qid] = {tous[i]: [round(float(a[i]), 2), round(float(c[i]), 2)] for i in garde}
        if not vt:
            print(f"attention : {qid}, aucun mot de la vraie réponse n'est connu des vecteurs", file=sys.stderr)

    # En PAQUETS fichiers (prototype/proches/) : la page ne charge que l'index et le paquet de la
    # question en cours (10,4 Mo d'un bloc pour 472 questions le 26/11/2026, 0,3 Mo par paquet).
    dossier = RACINE / "prototype" / "proches"
    dossier.mkdir(exist_ok=True)
    for vieux in dossier.glob("p*.json"):
        vieux.unlink()
    (RACINE / "prototype" / "proches.json").unlink(missing_ok=True)
    paquets: dict = {}
    for qid, liste in sortie.items():
        paquets.setdefault(paquet(qid), {})[qid] = liste
    for k, contenu in paquets.items():
        (dossier / f"p{k}.json").write_text(json.dumps(contenu, ensure_ascii=False, separators=(",", ":")))
    (dossier / "index.json").write_text(json.dumps({"vides": sorted(vides), "inconnu": INCONNU, "paquets": PAQUETS},
                                                   ensure_ascii=False, separators=(",", ":")))
    tailles = [f.stat().st_size for f in dossier.glob("p*.json")]
    print(f"prototype/proches/ : {len(sortie)} questions, {sum(len(v) for v in sortie.values())} mots, "
          f"{len(tailles)} paquets, {sum(tailles) / 1e6:.1f} Mo en tout, {max(tailles) / 1e6:.2f} Mo au plus")


if __name__ == "__main__":
    main()
