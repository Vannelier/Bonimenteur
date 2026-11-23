"""Code commun aux jeux, épinglé par son empreinte (docs/mots-communs.md de Vocabulium).
Un test rouge : fichier édité hors de sa source, ou copie oubliée."""
import hashlib
from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "app"

COPIES = {"pseudos.py": ("24edf85fed064bf7864b156906186466f98bbed2", "Vocabulium")}


def test_copies_identiques():
    for fichier, (empreinte, source) in COPIES.items():
        reelle = hashlib.sha1((APP / fichier).read_bytes()).hexdigest()
        assert reelle == empreinte, f"app/{fichier} a changé : l'éditer dans {source}, puis recopier ({reelle})."
