"""Filtre des pseudos, commun à Vocabulium, Snouff et Discoverium.

Écrit ici et recopié tel quel dans Snouff et Discoverium (`app/pseudos.py`),
comme `app/mots.py` : leurs tests vérifient son empreinte
(docs/mots-communs.md, « Pseudos »). Ne dépend de rien d'autre que la
bibliothèque standard.

Un pseudo offensant est neutralisé silencieusement en NAME_FALLBACK (pas
d'erreur : pas de retour qui aide à contourner le filtre). Deux niveaux pour
limiter les faux positifs (problème « Scunthorpe ») :
  • NAME_BAN_SUBSTR : termes longs, non ambigus, cherchés en SOUS-CHAÎNE sur
    le pseudo aplati (minuscule, sans accents, sans séparateurs, leet ramené) :
    « H1tler », « x_pute_x », « P U T E » ;
  • NAME_BAN_TOKEN : termes courts ou ambigus, cherchés seulement en MOT ENTIER
    (sinon « con » bannirait « Conan », « nique » bannirait « Monique »).
S'y ajoutent les noms bannis depuis /admin/classement de Vocabulium (liste
commune aux trois jeux), posés par `charger_bannis`.
"""
from __future__ import annotations

import re
import unicodedata

MAX_NAME_LEN = 14                     # aligné sur le maxlength des champs du front
NAME_FALLBACK = "Joueur"
BAN_MIN = 4          # nom banni aplati plus court : banni partout en sous-chaîne, trop large

NAME_BAN_SUBSTR = frozenset({
    # haine / apologie
    "hitler", "adolf", "nazi", "nazie", "siegheil", "heilhitler", "fuhrer",
    "kkk", "kluxklan", "daesh", "pedophile", "pedonazi", "genocid",
    # injures fortes (termes longs, sans homographe français courant)
    "putain", "salaud", "salopard", "connard", "connasse", "encul",
    "enfoire", "batard", "pouffiasse",
    # slurs (racistes / homophobes / antisémites)
    "negre", "negro", "negresse", "bougnoule", "youpin", "bamboula",
    "gouine", "tapette", "tarlouze", "feuj",
    # sexe / anatomie crus
    "couille", "penis", "vagin", "chatte", "sperme",
    "branle", "masturb", "fellation", "sodomi", "zoophil",
    # scato
    "merde", "merdique", "chiant", "etron",
})
# Termes courts ou présents dans des mots innocents (computer, salopette,
# cornichon, fichier, orbite, montmartre…) : mot entier SEULEMENT.
NAME_BAN_TOKEN = frozenset({
    "con", "cons", "conne", "cul", "culs", "pd", "pede", "zob", "zizi",
    "baise", "niquer", "nique", "foutre", "pisse", "puta", "pute", "salope",
    "nichon", "bite", "chier", "ntm", "fdp",
})
# Noms bannis depuis l'admin, aplatis (`compact_name`), cherchés en
# sous-chaîne. Rechargés par chaque jeu au démarrage et à chaque bannissement.
NAME_BAN_ADMIN: frozenset[str] = frozenset()
_LEET = str.maketrans({
    "0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "8": "b",
    "@": "a", "$": "s", "!": "i", "|": "i", "€": "e",
})


def charger_bannis(noms) -> None:
    """Remplace la liste des noms bannis depuis l'admin."""
    global NAME_BAN_ADMIN
    NAME_BAN_ADMIN = frozenset(noms)


def _fold_name(s: str) -> str:
    """Minuscule, sans accents, leet ramené (pour comparer un pseudo maquillé)."""
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.translate(_LEET)


def compact_name(name: str) -> str:
    """Pseudo aplati et sans séparateurs : « Anti-Gauch0 » → « antigaucho »."""
    return "".join(c for c in _fold_name(name) if c.isalnum())


def is_offensive_name(name: str) -> bool:
    folded = _fold_name(name)
    compact = compact_name(name)
    if any(bad in compact for bad in NAME_BAN_SUBSTR | NAME_BAN_ADMIN):
        return True
    tokens = {t for t in re.split(r"[^a-z0-9]+", folded) if t}
    return bool(tokens & NAME_BAN_TOKEN)


def nettoyer(name: object) -> str:
    """Pseudo reçu du réseau : sans caractères de contrôle (retours ligne,
    RTL, zero-width), espaces compactés, tronqué ; "" si vide ou pas une
    chaîne ; NAME_FALLBACK s'il est offensant. Le front échappe déjà à
    l'affichage, mais on ne fait jamais confiance au client."""
    if not isinstance(name, str):
        return ""
    cleaned = "".join(ch for ch in name if unicodedata.category(ch)[0] != "C")
    cleaned = " ".join(cleaned.split()).strip()[:MAX_NAME_LEN]
    if not cleaned:
        return ""
    return NAME_FALLBACK if is_offensive_name(cleaned) else cleaned
