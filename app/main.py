"""Serveur de Bonimenteur : la page du prototype et la base partagée qui la fait vivre.

La page (prototype/index.html) a été écrite pour la base des artifacts claude.ai
(window.claude). Hors de claude.ai, prototype/serveur.js lui fournit la même
interface, branchée sur l'API ci-dessous. Le serveur garde la main sur ce qui
compte : l'identité du joueur (cookie posé par lui), l'auteur d'un faux, le gain
d'un duel, le prix d'un faux et le solde de blops.

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
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

RACINE = Path(__file__).resolve().parent.parent
PAGE = RACINE / "prototype"
DONNEES = Path(os.environ.get("BONIMENTEUR_DATA_DIR")
               or os.environ.get("RAILWAY_VOLUME_MOUNT_PATH")
               or RACINE / "var")

# Règles reprises de la page (prototype/index.html, en tête du script ; docs/conception.md).
BLOP_DEPART = 10
PRIX = {10, 15}            # atelier, direct (PRIX_PIEGE, PRIX_DIRECT)
PSEUDO_MIN, PSEUDO_MAX = 2, 20
TEXTE_MAX = 200            # au-dessus des maximums par famille de la page (40 à 120)
COOKIE = "bm_joueur"
COOKIE_AGE = 400 * 24 * 3600   # plafond des navigateurs (Chrome : 400 jours)
IDENTIFIANT = re.compile(r"^j_[A-Za-z0-9_-]{22}$")

QUESTIONS = json.loads((RACINE / "data" / "questions.json").read_text())
FAUX_DE_DEPART = [{**f, "auteur": "truffe", "cree": 0} for f in json.loads((RACINE / "data" / "faux-de-depart.json").read_text())]

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
_verrou = threading.Lock()


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
    """)
    return c


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
    j = "j_" + secrets.token_urlsafe(16)[:22]
    response.set_cookie(COOKIE, j, max_age=COOKIE_AGE, httponly=True, samesite="lax",
                        secure=request.url.scheme == "https" or request.headers.get("x-forwarded-proto") == "https")
    return j


def _tous_les_faux():
    return FAUX_DE_DEPART + [dict(r) for r in db.execute("SELECT * FROM faux")]


def _solde(joueur: str) -> int:
    gagnes = db.execute("SELECT COALESCE(SUM(gain), 0) FROM choix WHERE joueur = ?", (joueur,)).fetchone()[0]
    mes = db.execute("SELECT id, prix FROM faux WHERE auteur = ?", (joueur,)).fetchall()
    ids = {r["id"] for r in mes}
    victimes = 0
    if ids:
        for r in db.execute("SELECT montres, ordre FROM choix WHERE erreur = 1"):
            ordre = set(json.loads(r["ordre"]))
            victimes += sum(1 for f in json.loads(r["montres"]) if f in ids and f not in ordre)
    return BLOP_DEPART + gagnes + victimes - sum(r["prix"] for r in mes)


@app.get("/api/moi")
def moi(request: Request, response: Response):
    j = _joueur(request, response)
    return {"id": j, "solde": _solde(j)}


@app.get("/api/etat")
def etat(request: Request):
    """Tout ce que la page lit : questions, faux, choix, contestations, pseudos."""
    choix = [{**dict(r), "montres": json.loads(r["montres"]), "ordre": json.loads(r["ordre"]),
              "erreur": bool(r["erreur"])} for r in db.execute("SELECT * FROM choix")]
    return {
        "mots": QUESTIONS,
        "pieges": _tous_les_faux(),
        "choix": choix,
        "contestations": [dict(r) for r in db.execute("SELECT piege, joueur, mot, t FROM contestations")],
        "joueurs": {r["id"]: r["pseudo"] for r in db.execute("SELECT id, pseudo FROM joueurs")},
    }


class Faux(BaseModel):
    mot: str
    texte: str = Field(min_length=3, max_length=TEXTE_MAX)
    prix: int = 10


@app.post("/api/pieges")
def poser(f: Faux, request: Request):
    j = _joueur(request)
    if f.mot not in QUESTIONS:
        raise HTTPException(404, "question inconnue")
    if f.prix not in PRIX:
        raise HTTPException(422, "prix inconnu")
    with _verrou:
        if _solde(j) < f.prix:
            raise HTTPException(402, "pas assez de blops")
        fid = secrets.token_urlsafe(12)
        try:
            db.execute("INSERT INTO faux VALUES (?, ?, ?, ?, ?, ?)", (fid, f.mot, f.texte.strip(), j, _ms(), f.prix))
            db.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(409, "un seul faux par question")
    return {"id": fid}


class Choix(BaseModel):
    mot: str
    montres: list[str] = Field(min_length=1, max_length=4)
    ordre: list[str] = Field(max_length=4)
    erreur: bool


@app.post("/api/choix")
def choisir(c: Choix, request: Request):
    """Un duel joué. Le gain se décide ici : 1 blop pour une bonne réponse."""
    j = _joueur(request)
    if c.mot not in QUESTIONS:
        raise HTTPException(404, "question inconnue")
    connus = {f["id"] for f in _tous_les_faux() if f["mot"] == c.mot}
    if not set(c.montres) <= connus or not set(c.ordre) <= set(c.montres):
        raise HTTPException(422, "faux inconnu")
    with _verrou:
        if db.execute("SELECT 1 FROM choix WHERE joueur = ? AND mot = ?", (j, c.mot)).fetchone():
            raise HTTPException(409, "question déjà jouée")
        gain = 0 if c.erreur else 1
        db.execute("INSERT INTO choix VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (secrets.token_urlsafe(12), c.mot, json.dumps(c.montres), json.dumps(c.ordre),
                    int(c.erreur), gain, j, _ms()))
        db.commit()
    return {"gain": gain}


class Contestation(BaseModel):
    piege: str
    mot: str


@app.post("/api/contestations")
def contester(c: Contestation, request: Request):
    j = _joueur(request)
    db.execute("INSERT OR IGNORE INTO contestations VALUES (?, ?, ?, ?)", (c.piege, j, c.mot, _ms()))
    db.commit()
    return {}


class Signalement(BaseModel):
    mot: str
    raison: str = Field(max_length=40)
    pieges: list[str] = Field(default=[], max_length=4)


@app.post("/api/signalements")
def signaler(s: Signalement, request: Request):
    j = _joueur(request)
    db.execute("INSERT INTO signalements (mot, raison, pieges, joueur, t) VALUES (?, ?, ?, ?, ?)",
               (s.mot, s.raison, json.dumps(s.pieges), j, _ms()))
    db.commit()
    return {}


class Pseudo(BaseModel):
    pseudo: str


@app.put("/api/pseudo")
def nommer(p: Pseudo, request: Request):
    """Chacun ne change que le sien : l'identifiant vient du cookie, pas de la requête."""
    j = _joueur(request)
    v = re.sub(r"\s+", " ", p.pseudo).strip()[:PSEUDO_MAX]
    if len(v) < PSEUDO_MIN:
        raise HTTPException(422, "pseudo trop court")
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
