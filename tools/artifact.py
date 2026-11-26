"""Construit le dossier à publier comme artifact claude.ai (docs/conception.md, « Artifact »).

    python tools/artifact.py DOSSIER

DOSSIER/index.html : la page, sans ce qui précède <title> ni serveur.js (sur claude.ai,
window.claude existe déjà). DOSSIER/donnees.json : questions et faux de Mr Halifax, lus par la
page à la place des collections « mots » et des faux « truffe » de la base (ils ne changent
jamais en jeu : publiés avec la page, sans écrire 2 000 documents dans la base).
DOSSIER/proches/ : les paquets de l'arbitre. Photos, icônes et communes.txt restent publiés
depuis prototype/ : seuls les fichiers nouveaux ou changés sont à republier.
"""
import json
import shutil
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
PAGE = RACINE / "prototype"


def main():
    cible = Path(sys.argv[1])
    cible.mkdir(parents=True, exist_ok=True)
    html = (PAGE / "index.html").read_text()
    balise = '<script src="serveur.js"></script>\n'
    assert balise in html
    (cible / "index.html").write_text(html[html.index("<title>"):].replace(balise, ""))
    donnees = {"questions": json.loads((RACINE / "data" / "questions.json").read_text()),
               "faux": json.loads((RACINE / "data" / "faux-de-depart.json").read_text())}
    (cible / "donnees.json").write_text(json.dumps(donnees, ensure_ascii=False, separators=(",", ":")))
    if (cible / "proches").exists():
        shutil.rmtree(cible / "proches")
    shutil.copytree(PAGE / "proches", cible / "proches")
    print(f"{cible} : page, donnees.json ({len(donnees['questions'])} questions, {len(donnees['faux'])} faux), "
          f"{len(list((cible / 'proches').glob('*.json')))} fichiers d'arbitre")


if __name__ == "__main__":
    main()
