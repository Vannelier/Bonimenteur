"""Serveur de Bonimenteur : la page du prototype et la base partagée qui la fait vivre.

La page (prototype/index.html) a été écrite pour la base des artifacts claude.ai
(window.claude). Hors de claude.ai, prototype/serveur.js lui fournit la même
interface, branchée sur l'API ci-dessous. Le serveur garde la main sur ce qui
compte : l'identité du joueur (cookie posé par lui), l'auteur d'un faux, le gain
d'un duel, le prix d'un faux et le solde d'écus.

Données : SQLite dans BONIMENTEUR_DATA_DIR, à défaut le volume Railway
(RAILWAY_VOLUME_MOUNT_PATH), puis var/ en local. Questions et faux de départ :
data/ du dépôt, lus au démarrage.
"""
import json
import os
import re
import secrets
import sqlite3
import threading
import time
from datetime import datetime, time as heure, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import unicodedata
from collections import defaultdict, deque

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.pseudos import NAME_FALLBACK, is_offensive_name

RACINE = Path(__file__).resolve().parent.parent
PAGE = RACINE / "prototype"
DONNEES = Path(os.environ.get("BONIMENTEUR_DATA_DIR")
               or os.environ.get("RAILWAY_VOLUME_MOUNT_PATH")
               or RACINE / "var")

# Règles reprises de la page (prototype/index.html, en tête du script ; docs/conception.md).
ECUS_DEPART = 20          # de quoi poser un faux en direct (15) dès la première partie
# Ration du jour : 15 duels par jour, heure de Paris (TOTAL dans la page ; docs/conception.md).
RATION = 15
# Coupée pour les essais (demande de l'auteur, 23/11/2026) ; True la rétablit, avec RATION_ACTIVE de la page.
RATION_ACTIVE = False
PARIS = ZoneInfo("Europe/Paris")
PRIX = {10, 15}            # atelier, direct (PRIX_PIEGE, PRIX_DIRECT)
# Édition et étal (décision de l'auteur, 25/11/2026 ; mêmes constantes dans la page ; docs/conception.md,
# « Édition et étal ») : 10 exemplaires par édition, 10 places d'étal agrandies jusqu'à 20.
EXEMPLAIRES, ETAL, ETAL_MAX = 10, 10, 20
PRIX_ACTES = {"place": 20, "reedition": 25, "retouche": 5, "retrait": 0, "remise": 0}
CONTEST_MIN = 2            # contestations qui retirent un faux du marché (CONTEST_MIN de la page)
PSEUDO_MIN, PSEUDO_MAX = 2, 16   # PSEUDO_MAX de la page : la signature tient sur une ligne de pièce
TEXTE_MAX = 200            # au-dessus des maximums par famille de la page (40 à 120)
COOKIE = "bm_joueur"
COOKIE_AGE = 400 * 24 * 3600   # plafond des navigateurs (Chrome : 400 jours)
IDENTIFIANT = re.compile(r"^j_[A-Za-z0-9_-]{22}$")

QUESTIONS = json.loads((RACINE / "data" / "questions.json").read_text())
FAUX_DE_DEPART = [{**f, "auteur": "truffe", "cree": 0} for f in json.loads((RACINE / "data" / "faux-de-depart.json").read_text())]

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
# Compression : proches.json passe de 2,7 Mo à 0,6 Mo (audit du 23/11/2026, docs/audit.md).
app.add_middleware(GZipMiddleware, minimum_size=1000)
# Un seul accès à la fois à la connexion SQLite, partagée entre les fils de FastAPI : sans ce
# verrou, lectures et écritures de fils différents pouvaient se croiser (audit du 23/11/2026).
_verrou = threading.RLock()

# Limites de débit par adresse IP, en mémoire (comme les trois autres jeux) : identités neuves
# (chaque cookie neuf reçoit 20 écus de départ) et écritures.
LIMITES = {"identite": (20, 3600), "ecriture": (60, 60)}   # (nombre, fenêtre en secondes)
_compteurs: dict = defaultdict(deque)


def _ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for", "")
    return fwd.split(",")[0].strip() or (request.client.host if request.client else "?")


def _limiter(request: Request, sorte: str):
    n, fenetre = LIMITES[sorte]
    q, now = _compteurs[(sorte, _ip(request))], time.monotonic()
    while q and now - q[0] > fenetre:
        q.popleft()
    if len(q) >= n:
        raise HTTPException(429, "trop de requêtes")
    q.append(now)


def _base():
    DONNEES.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DONNEES / "bonimenteur.db", check_same_thread=False)
    c.row_factory = sqlite3.Row
    c.executescript("""
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS faux (id TEXT PRIMARY KEY, mot TEXT NOT NULL, texte TEXT NOT NULL,
            auteur TEXT NOT NULL, cree INTEGER NOT NULL, prix INTEGER NOT NULL, UNIQUE (mot, auteur));
        CREATE TABLE IF NOT EXISTS choix (id TEXT PRIMARY KEY, mot TEXT NOT NULL, montres TEXT NOT NULL,
            ordre TEXT NOT NULL, erreur INTEGER NOT NULL, gain INTEGER NOT NULL, joueur TEXT NOT NULL, t INTEGER NOT NULL);
        CREATE INDEX IF NOT EXISTS choix_joueur ON choix (joueur);
        CREATE TABLE IF NOT EXISTS contestations (piege TEXT NOT NULL, joueur TEXT NOT NULL, mot TEXT NOT NULL,
            t INTEGER NOT NULL, PRIMARY KEY (piege, joueur));
        CREATE TABLE IF NOT EXISTS signalements (id INTEGER PRIMARY KEY AUTOINCREMENT, mot TEXT, raison TEXT,
            pieges TEXT, joueur TEXT, t INTEGER);
        CREATE TABLE IF NOT EXISTS joueurs (id TEXT PRIMARY KEY, pseudo TEXT NOT NULL, t INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS defis (code TEXT PRIMARY KEY, auteur TEXT NOT NULL, t INTEGER NOT NULL);
        CREATE INDEX IF NOT EXISTS faux_auteur ON faux (auteur);
        CREATE TABLE IF NOT EXISTS actes (id INTEGER PRIMARY KEY AUTOINCREMENT, joueur TEXT NOT NULL,
            sorte TEXT NOT NULL, faux TEXT, prix INTEGER NOT NULL, texte TEXT, categorie TEXT,
            base_pris INTEGER, base_dem INTEGER, t INTEGER NOT NULL);
        CREATE INDEX IF NOT EXISTS actes_joueur ON actes (joueur);
        CREATE TABLE IF NOT EXISTS stats (faux TEXT PRIMARY KEY, vu INTEGER NOT NULL DEFAULT 0,
            pris INTEGER NOT NULL DEFAULT 0, demasque INTEGER NOT NULL DEFAULT 0);
    """)
    # Catégorie grammaticale du faux (définitions), ajoutée le 23/11/2026.
    if "categorie" not in {r[1] for r in c.execute("PRAGMA table_info(faux)")}:
        c.execute("ALTER TABLE faux ADD COLUMN categorie TEXT")
    # Compteurs par faux (ajoutés le 23/11/2026) : reconstruits une fois depuis les duels existants.
    if not c.execute("SELECT 1 FROM stats LIMIT 1").fetchone():
        for r in c.execute("SELECT montres, ordre, erreur FROM choix").fetchall():
            _compter(c, json.loads(r["montres"]), json.loads(r["ordre"]), bool(r["erreur"]))
        c.commit()
    return c


def _compter(c, montres, ordre, erreur):
    """Un duel joué : chaque faux montré est vu ; démasqué s'il est dans « ordre », sinon pris
    si le joueur s'est trompé (même règle que index() dans la page)."""
    for f in montres:
        dem, pris = int(f in ordre), int(erreur and f not in ordre)
        c.execute("INSERT INTO stats (faux, vu, pris, demasque) VALUES (?, 1, ?, ?) ON CONFLICT (faux) DO UPDATE "
                  "SET vu = vu + 1, pris = pris + excluded.pris, demasque = demasque + excluded.demasque", (f, pris, dem))


db = _base()


def _ms():
    return int(time.time() * 1000)


def _joueur(request: Request, response: Response | None = None) -> str:
    """Identifiant du joueur, posé par le serveur dans un cookie HttpOnly (Safari efface au
    bout de 7 jours ce qu'un script écrit, pas un cookie posé par le serveur)."""
    j = request.cookies.get(COOKIE, "")
    if IDENTIFIANT.match(j):
        return j
    if response is None:
        raise HTTPException(401, "joueur inconnu")
    _limiter(request, "identite")
    j = "j_" + secrets.token_urlsafe(16)[:22]
    response.set_cookie(COOKIE, j, max_age=COOKIE_AGE, httponly=True, samesite="lax",
                        secure=request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https")
    return j


def _plat(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9]+", " ", "".join(c for c in s if not unicodedata.combining(c))).strip()


def _tous_les_faux():
    return FAUX_DE_DEPART + [dict(r) for r in db.execute("SELECT * FROM faux")]


def _minuit_ms() -> int:
    """Début du jour à Paris, en millisecondes."""
    debut = datetime.combine(datetime.now(PARIS).date(), heure(0), tzinfo=PARIS)
    return int(debut.timestamp() * 1000)


def _joues_aujourdhui(joueur: str) -> int:
    return db.execute("SELECT COUNT(*) FROM choix WHERE joueur = ? AND t >= ?", (joueur, _minuit_ms())).fetchone()[0]


def _lundi_ms(semaines_avant: int = 0) -> int:
    """Lundi 0 h (Paris) de la semaine en cours, ou d'une semaine passée : le classement des
    faussaires repart de zéro chaque lundi, comme ceux des trois autres jeux."""
    jour = datetime.now(PARIS).date()
    lundi = jour - timedelta(days=jour.weekday(), weeks=semaines_avant)
    return int(datetime.combine(lundi, heure(0), tzinfo=PARIS).timestamp() * 1000)


def _piegeurs(debut: int, fin: int | None = None) -> list[dict]:
    """Classement des faussaires : joueurs dupés par leurs faux entre debut et fin (même règle
    que _compter : un faux montré, pas démasqué, à un joueur qui s'est trompé). Les faux de
    Mr Halifax ne comptent pas."""
    auteurs = {f["id"]: f["auteur"] for f in db.execute("SELECT id, auteur FROM faux")}
    n: dict = defaultdict(int)
    for c in db.execute("SELECT montres, ordre, joueur FROM choix WHERE erreur = 1 AND t >= ? AND t < ?",
                        (debut, fin or 2**62)):
        ordre = json.loads(c["ordre"])
        for f in json.loads(c["montres"]):
            a = auteurs.get(f)
            if a and a != c["joueur"] and f not in ordre:
                n[a] += 1
    return [{"id": a, "n": v} for a, v in sorted(n.items(), key=lambda x: (-x[1], x[0]))]


def _experts(debut: int, fin: int | None = None) -> list[dict]:
    """Classement des experts : pièces authentifiées (expertises justes) entre debut et fin."""
    lignes = db.execute("SELECT joueur, COUNT(*) AS n FROM choix WHERE erreur = 0 AND t >= ? AND t < ? "
                        "GROUP BY joueur ORDER BY n DESC, joueur", (debut, fin or 2**62))
    return [{"id": l["joueur"], "n": l["n"]} for l in lignes]


PALIERS = (10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000)   # jauge des joueurs, comme les trois autres jeux


def _communaute() -> dict:
    n = db.execute("SELECT COUNT(DISTINCT joueur) FROM choix").fetchone()[0]
    return {"joueurs": n, "objectif": next((p for p in PALIERS if p > n), n + 1)}


def _classement(j: str) -> dict:
    """Deux classements de la semaine (demande de l'auteur, 25/11/2026) : les experts (pièces
    authentifiées) et les faussaires (joueurs dupés). Pour chacun : les 20 premiers, le premier
    de la semaine passée et la place du joueur."""
    def un(compter):
        semaine, passee = compter(_lundi_ms()), compter(_lundi_ms(1), _lundi_ms())
        moi = next(({"rang": i + 1, "n": r["n"]} for i, r in enumerate(semaine) if r["id"] == j), None)
        return {"semaine": semaine[:20], "passee": passee[0] if passee else None, "moi": moi}
    return {"experts": un(_experts), "faussaires": un(_piegeurs)}


def _solde(joueur: str) -> int:
    gagnes = db.execute("SELECT COALESCE(SUM(gain), 0) FROM choix WHERE joueur = ?", (joueur,)).fetchone()[0]
    prix, victimes = db.execute("SELECT COALESCE(SUM(f.prix), 0), COALESCE(SUM(s.pris), 0) FROM faux f "
                                "LEFT JOIN stats s ON s.faux = f.id WHERE f.auteur = ?", (joueur,)).fetchone()
    actes = db.execute("SELECT COALESCE(SUM(prix), 0) FROM actes WHERE joueur = ?", (joueur,)).fetchone()[0]
    return ECUS_DEPART + gagnes + victimes - prix - actes


def _situation(fid: str) -> dict:
    """Où en est un faux de joueur (même règle que index() dans la page) : édition en cours,
    exemplaires restants, rangé par son auteur, retiré par contestation."""
    s = db.execute("SELECT pris, demasque FROM stats WHERE faux = ?", (fid,)).fetchone()
    pris, dem = (s["pris"], s["demasque"]) if s else (0, 0)
    base, range_ = (0, 0), False
    for a in db.execute("SELECT sorte, base_pris, base_dem FROM actes WHERE faux = ? ORDER BY id", (fid,)):
        if a["sorte"] == "reedition":
            base, range_ = (a["base_pris"], a["base_dem"]), False
        elif a["sorte"] in ("retrait", "remise"):
            range_ = a["sorte"] == "retrait"
    epuise = (pris - base[0]) + (dem - base[1]) >= EXEMPLAIRES
    conteste = db.execute("SELECT COUNT(*) FROM contestations WHERE piege = ?", (fid,)).fetchone()[0] >= CONTEST_MIN
    return {"pris": pris, "dem": dem, "epuise": epuise, "range": range_, "conteste": conteste,
            "en_vente": not (epuise or range_ or conteste)}


def _places(joueur: str) -> tuple[int, int]:
    """(faux en vente, places de l'étal) du joueur."""
    ids = [r[0] for r in db.execute("SELECT id FROM faux WHERE auteur = ?", (joueur,))]
    places = ETAL + db.execute("SELECT COUNT(*) FROM actes WHERE joueur = ? AND sorte = 'place'", (joueur,)).fetchone()[0]
    return sum(_situation(f)["en_vente"] for f in ids), places


@app.get("/api/moi")
def moi(request: Request, response: Response):
    j = _joueur(request, response)
    with _verrou:
        return {"id": j, "solde": _solde(j), "ration": RATION - _joues_aujourdhui(j)}


@app.get("/api/etat")
def etat(request: Request, defi: str = ""):
    """Ce que la page lit : questions, faux, compteurs par faux, contestations, pseudos, et
    seulement les duels qui concernent le joueur (les siens, et ceux où l'un de ses faux a
    trompé quelqu'un : « Tes faux ont trouvé preneur »). Avant le 23/11/2026, tous les duels de
    tous les joueurs repartaient toutes les 20 s (audit, docs/audit.md)."""
    j = request.cookies.get(COOKIE, "")
    with _verrou:
        return _etat(j if IDENTIFIANT.match(j) else "", defi)


def _etat(j: str, defi: str = ""):
    lignes = db.execute("SELECT * FROM choix WHERE joueur = ? OR erreur = 1 AND EXISTS (SELECT 1 FROM faux f "
                        "WHERE f.auteur = ? AND instr(choix.montres, '\"' || f.id || '\"') > 0)", (j, j)).fetchall()
    choix = [{**dict(r), "montres": json.loads(r["montres"]), "ordre": json.loads(r["ordre"]),
              "erreur": bool(r["erreur"])} for r in lignes]
    stats = {r["faux"]: [r["vu"], r["pris"], r["demasque"]] for r in db.execute("SELECT * FROM stats")}
    return {
        "stats": stats,
        "mots": QUESTIONS,
        "pieges": _tous_les_faux(),
        "choix": choix,
        "contestations": [dict(r) for r in db.execute("SELECT piege, joueur, mot, t FROM contestations")],
        # Actes des faussaires (éditions, rangements, places) : la page en tire l'état de chaque faux.
        # Les textes des retouches sont déjà dans les faux.
        "actes": [{"joueur": r["joueur"], "sorte": r["sorte"], "faux": r["faux"], "prix": r["prix"], "t": r["t"],
                   **({"base": [r["base_pris"], r["base_dem"]]} if r["sorte"] == "reedition" else {})}
                  for r in db.execute("SELECT * FROM actes WHERE sorte != 'retouche' OR joueur = ? ORDER BY id", (j,))],
        "joueurs": {r["id"]: r["pseudo"] for r in db.execute("SELECT id, pseudo FROM joueurs")},
        # Accueil : podium des faussaires de la semaine et jauge des joueurs (le classement ne
        # peut pas se calculer dans la page, qui ne reçoit que les duels du joueur).
        "classement": _classement(j),
        # Le défi ouvert par le lien (?defi=CODE) : seulement celui-là, jamais la liste.
        "defis": _defi(defi),
        "communaute": _communaute(),
    }


# Défi par lien (docs/conception.md, « Défi ») : un faussaire qui a au moins DEFI_MIN faux en vente
# envoie un lien ; l'ami expertise ses lots, face à ses faux.
DEFI_MIN = 3
CODE_DEFI = re.compile(r"^[a-z0-9]{6,12}$")


def _defi(code: str) -> dict:
    if not CODE_DEFI.match(code or ""):
        return {}
    r = db.execute("SELECT code, auteur, t FROM defis WHERE code = ?", (code,)).fetchone()
    return {r["code"]: {"auteur": r["auteur"], "t": r["t"]}} if r else {}


class Defi(BaseModel):
    code: str


@app.post("/api/defis")
def defier(d: Defi, request: Request):
    """Crée le défi du joueur : l'auteur vient du cookie ; il faut DEFI_MIN faux en vente."""
    j = _joueur(request)
    _limiter(request, "ecriture")
    if not CODE_DEFI.match(d.code):
        raise HTTPException(422, "code invalide")
    with _verrou:
        if db.execute("SELECT COUNT(*) FROM faux WHERE auteur = ?", (j,)).fetchone()[0] < DEFI_MIN:
            raise HTTPException(403, "pas assez de faux")
        try:
            db.execute("INSERT INTO defis VALUES (?, ?, ?)", (d.code, j, _ms()))
            db.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(409, "code déjà pris")
    return {"code": d.code}


CATEGORIES = {"n. m.", "n. f.", "n.", "adj.", "v.", "adv."}   # celles que la page propose


class Faux(BaseModel):
    mot: str
    texte: str = Field(min_length=3, max_length=TEXTE_MAX)
    prix: int = 10
    categorie: str | None = None


@app.post("/api/pieges")
def poser(f: Faux, request: Request):
    j = _joueur(request)
    _limiter(request, "ecriture")
    if f.mot not in QUESTIONS:
        raise HTTPException(404, "question inconnue")
    # Garde-fou minimal : l'arbitre du sens tourne dans la page ; ici, au moins, pas de copie
    # de la vraie réponse (aux accents, à la casse et à la ponctuation près).
    if _plat(f.texte) == _plat(QUESTIONS[f.mot]["vraie"]):
        raise HTTPException(422, "trop proche de l'original")
    # Même filtre que les pseudos, sur le texte du faux : il est montré à tous les joueurs.
    if is_offensive_name(f.texte):
        raise HTTPException(422, "contenu refusé")
    if f.prix not in PRIX:
        raise HTTPException(422, "prix inconnu")
    if f.categorie is not None and f.categorie not in CATEGORIES:
        raise HTTPException(422, "catégorie inconnue")
    with _verrou:
        # On ne contrefait que la pièce qu'on a authentifiée, eue entre les mains (décision de
        # l'auteur, 24/11/2026) : pas de faux sur un lot jamais joué ni sur un lot où l'on a été floué.
        if not db.execute("SELECT 1 FROM choix WHERE joueur = ? AND mot = ? AND erreur = 0", (j, f.mot)).fetchone():
            raise HTTPException(403, "pièce non authentifiée")
        if _solde(j) < f.prix:
            raise HTTPException(402, "pas assez d'écus")
        en_vente, places = _places(j)
        if en_vente >= places:
            raise HTTPException(423, "étal plein")
        fid = secrets.token_urlsafe(12)
        try:
            db.execute("INSERT INTO faux (id, mot, texte, auteur, cree, prix, categorie) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (fid, f.mot, f.texte.strip(), j, _ms(), f.prix, f.categorie))
            db.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(409, "un seul faux par question")
    return {"id": fid}


class Acte(BaseModel):
    sorte: str
    faux: str | None = None
    texte: str | None = Field(default=None, min_length=3, max_length=TEXTE_MAX)
    categorie: str | None = None


@app.post("/api/actes")
def agir(a: Acte, request: Request):
    """Gestes du faussaire sur son étal : une place de plus, ranger un faux, le remettre en
    vente, le rééditer une fois épuisé, le retoucher. Prix fixés ici (PRIX_ACTES), auteur
    vérifié, place libre exigée pour ce qui remet un faux en vente."""
    j = _joueur(request)
    _limiter(request, "ecriture")
    if a.sorte not in PRIX_ACTES:
        raise HTTPException(422, "acte inconnu")
    prix = PRIX_ACTES[a.sorte]
    with _verrou:
        en_vente, places = _places(j)
        if a.sorte == "place":
            if places >= ETAL_MAX:
                raise HTTPException(423, "étal au plus grand")
            sit = None
        else:
            f = db.execute("SELECT * FROM faux WHERE id = ?", (a.faux or "",)).fetchone()
            if not f:
                raise HTTPException(404, "faux inconnu")
            if f["auteur"] != j:
                raise HTTPException(403, "pas ton faux")
            sit = _situation(f["id"])
            if sit["conteste"]:
                raise HTTPException(423, "retiré du marché")
            ok = {"retrait": sit["en_vente"], "remise": sit["range"] and not sit["epuise"],
                  "reedition": sit["epuise"], "retouche": True}[a.sorte]
            if not ok:
                raise HTTPException(422, "état du faux")
            if a.sorte in ("remise", "reedition") and en_vente >= places:
                raise HTTPException(423, "étal plein")
            if a.sorte == "retouche":
                texte = (a.texte or "").strip()
                if len(texte) < 3 or _plat(texte) == _plat(QUESTIONS[f["mot"]]["vraie"]):
                    raise HTTPException(422, "trop proche de l'original")
                if is_offensive_name(texte):
                    raise HTTPException(422, "contenu refusé")
                if a.categorie is not None and a.categorie not in CATEGORIES:
                    raise HTTPException(422, "catégorie inconnue")
        if prix and _solde(j) < prix:
            raise HTTPException(402, "pas assez d'écus")
        if a.sorte == "retouche":
            db.execute("UPDATE faux SET texte = ?, categorie = COALESCE(?, categorie) WHERE id = ?", (texte, a.categorie, a.faux))
        base = (sit["pris"], sit["dem"]) if a.sorte == "reedition" else (None, None)
        db.execute("INSERT INTO actes (joueur, sorte, faux, prix, texte, categorie, base_pris, base_dem, t) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (j, a.sorte, a.faux if a.sorte != "place" else None, prix, texte if a.sorte == "retouche" else None,
                    a.categorie if a.sorte == "retouche" else None, base[0], base[1], _ms()))
        db.commit()
    return {}


class Choix(BaseModel):
    mot: str
    montres: list[str] = Field(min_length=1, max_length=4)
    ordre: list[str] = Field(max_length=4)
    erreur: bool


@app.post("/api/choix")
def choisir(c: Choix, request: Request):
    """Un duel joué. Le gain se décide ici : 1 écu pour une bonne réponse."""
    j = _joueur(request)
    _limiter(request, "ecriture")
    if c.mot not in QUESTIONS:
        raise HTTPException(404, "question inconnue")
    connus = {f["id"] for f in _tous_les_faux() if f["mot"] == c.mot}
    if not set(c.montres) <= connus or not set(c.ordre) <= set(c.montres):
        raise HTTPException(422, "faux inconnu")
    with _verrou:
        if db.execute("SELECT 1 FROM choix WHERE joueur = ? AND mot = ?", (j, c.mot)).fetchone():
            raise HTTPException(409, "question déjà jouée")
        if RATION_ACTIVE and _joues_aujourdhui(j) >= RATION:
            raise HTTPException(429, "ration du jour épuisée")
        gain = 0 if c.erreur else 1
        db.execute("INSERT INTO choix VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (secrets.token_urlsafe(12), c.mot, json.dumps(c.montres), json.dumps(c.ordre),
                    int(c.erreur), gain, j, _ms()))
        _compter(db, c.montres, c.ordre, c.erreur)
        db.commit()
    return {"gain": gain}


class Contestation(BaseModel):
    piege: str
    mot: str


@app.post("/api/contestations")
def contester(c: Contestation, request: Request):
    """Contester un faux qui dit vrai : seulement un faux de ce lot, qu'on a eu en duel et qui
    n'est pas le sien (2 contestations le retirent : sans ces contrôles, deux cookies suffisaient
    à retirer n'importe quel faux, audit du 23/11/2026)."""
    j = _joueur(request)
    _limiter(request, "ecriture")
    with _verrou:
        faux = next((f for f in _tous_les_faux() if f["id"] == c.piege), None)
        if not faux or faux["mot"] != c.mot:
            raise HTTPException(404, "faux inconnu")
        if faux["auteur"] == j:
            raise HTTPException(403, "c'est ton faux")
        vus = (json.loads(r["montres"]) for r in db.execute("SELECT montres FROM choix WHERE joueur = ? AND mot = ?", (j, c.mot)))
        if not any(c.piege in m for m in vus):
            raise HTTPException(403, "faux jamais expertisé")
        db.execute("INSERT OR IGNORE INTO contestations VALUES (?, ?, ?, ?)", (c.piege, j, c.mot, _ms()))
        db.commit()
    return {}


RAISONS = {"piege-vrai", "verite-fausse", "choquant"}   # celles que la page propose


class Signalement(BaseModel):
    mot: str
    raison: str = Field(max_length=40)
    pieges: list[str] = Field(default=[], max_length=4)


@app.post("/api/signalements")
def signaler(s: Signalement, request: Request):
    j = _joueur(request)
    _limiter(request, "ecriture")
    if s.mot not in QUESTIONS or s.raison not in RAISONS:
        raise HTTPException(422, "signalement inconnu")
    with _verrou:
        db.execute("INSERT INTO signalements (mot, raison, pieges, joueur, t) VALUES (?, ?, ?, ?, ?)",
                   (s.mot, s.raison, json.dumps(s.pieges), j, _ms()))
        db.commit()
    return {}


RESERVES = {"truffe", "mr halifax", "m halifax", "monsieur halifax", "halifax", "un joueur", "toi", "bonimenteur", "admin"}


class Pseudo(BaseModel):
    pseudo: str


@app.put("/api/pseudo")
def nommer(p: Pseudo, request: Request):
    """Chacun ne change que le sien : l'identifiant vient du cookie, pas de la requête."""
    j = _joueur(request)
    _limiter(request, "ecriture")
    v = re.sub(r"\s+", " ", p.pseudo).strip()[:PSEUDO_MAX]
    if len(v) < PSEUDO_MIN:
        raise HTTPException(422, "pseudo trop court")
    # « Mr Halifax » signe les faux de départ ; un pseudo n'appartient qu'à un joueur.
    if _plat(v) in RESERVES:
        raise HTTPException(409, "pseudo réservé")
    # Filtre commun aux jeux (app/pseudos.py, copie de Vocabulium) : un pseudo offensant devient
    # « Joueur », sans erreur qui aiderait à contourner le filtre.
    if is_offensive_name(v):
        v = NAME_FALLBACK
    with _verrou:
        if v != NAME_FALLBACK and any(_plat(r["pseudo"]) == _plat(v) for r in db.execute("SELECT pseudo FROM joueurs WHERE id != ?", (j,))):
            raise HTTPException(409, "pseudo déjà pris")
        db.execute("INSERT INTO joueurs VALUES (?, ?, ?) ON CONFLICT (id) DO UPDATE SET pseudo = excluded.pseudo, t = excluded.t",
                   (j, v, _ms()))
        db.commit()
    return {"pseudo": v}


@app.get("/sante")
def sante():
    return {"ok": True}


@app.get("/")
def accueil():
    return FileResponse(PAGE / "index.html", headers={"Cache-Control": "no-cache"})


app.mount("/", StaticFiles(directory=PAGE), name="page")
