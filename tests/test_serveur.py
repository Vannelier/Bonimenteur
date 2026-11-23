"""API du serveur : identité par cookie, gain décidé par le serveur, solde, un faux par question."""
import importlib
import json

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("BONIMENTEUR_DATA_DIR", str(tmp_path))
    import app.main as m
    importlib.reload(m)
    with TestClient(m.app) as c:
        yield c


def _faux_de(client, mot):
    return [p["id"] for p in client.get("/api/etat").json()["pieges"] if p["mot"] == mot]


def test_page_et_donnees_servies(client):
    assert "Bonimenteur" in client.get("/").text
    assert client.get("/serveur.js").status_code == 200
    assert client.get("/proches.json").json()["mots"]
    assert client.get("/photos/bassinoire.jpg").status_code == 200


def test_le_cookie_fait_le_joueur(client):
    a = client.get("/api/moi").json()
    assert a["id"].startswith("j_") and a["solde"] == 20
    assert client.get("/api/moi").json()["id"] == a["id"]


def test_ecrire_sans_cookie_refuse(tmp_path, monkeypatch):
    monkeypatch.setenv("BONIMENTEUR_DATA_DIR", str(tmp_path))
    import app.main as m
    importlib.reload(m)
    with TestClient(m.app) as c:
        assert c.post("/api/pieges", json={"mot": "sapajou", "texte": "Un faux."}).status_code == 401


def test_gain_decide_par_le_serveur(client):
    client.get("/api/moi")
    f = _faux_de(client, "sapajou")[0]
    assert client.post("/api/choix", json={"mot": "sapajou", "montres": [f], "ordre": [f], "erreur": False}).json()["gain"] == 1
    assert client.get("/api/moi").json()["solde"] == 21
    # Une question ne se rejoue pas.
    assert client.post("/api/choix", json={"mot": "sapajou", "montres": [f], "ordre": [], "erreur": True}).status_code == 409


def test_faux_inconnu_refuse(client):
    client.get("/api/moi")
    assert client.post("/api/choix", json={"mot": "sapajou", "montres": ["invente"], "ordre": [], "erreur": True}).status_code == 422


def test_poser_un_faux_paye_et_rapporte(client, tmp_path):
    client.get("/api/moi")
    # 20 au départ : un faux en direct (15) passe, le suivant à 10 n'a plus de quoi payer.
    r = client.post("/api/pieges", json={"mot": "sapajou", "texte": "Ragoût de fèves.", "prix": 15})
    assert r.status_code == 200
    assert client.get("/api/moi").json()["solde"] == 5
    assert client.post("/api/pieges", json={"mot": "cacochyme", "texte": "Plat mijoté."}).status_code == 402
    assert client.post("/api/pieges", json={"mot": "sapajou", "texte": "Autre."}).status_code in (402, 409)
    # Un autre joueur tombe dans le faux : l'auteur gagne 1 écu.
    import app.main as m
    with TestClient(m.app) as autre:
        autre.get("/api/moi")
        assert autre.post("/api/choix", json={"mot": "sapajou", "montres": [r.json()["id"]], "ordre": [], "erreur": True}).json()["gain"] == 0
    assert client.get("/api/moi").json()["solde"] == 6


def test_pseudo(client):
    j = client.get("/api/moi").json()["id"]
    assert client.put("/api/pseudo", json={"pseudo": "  Le   Faussaire "}).json()["pseudo"] == "Le Faussaire"
    assert client.get("/api/etat").json()["joueurs"][j] == "Le Faussaire"
    assert client.put("/api/pseudo", json={"pseudo": "x"}).status_code == 422


def test_donnees_coherentes():
    racine = __import__("pathlib").Path(__file__).resolve().parent.parent
    questions = json.loads((racine / "data" / "questions.json").read_text())
    faux = json.loads((racine / "data" / "faux-de-depart.json").read_text())
    assert {f["mot"] for f in faux} <= set(questions)
    assert len({f["id"] for f in faux}) == len(faux)
    for q in questions.values():
        if q.get("type") == "photo":
            assert (racine / "prototype" / q["image"]).exists()


def test_ration_du_jour(client, monkeypatch):
    """Ration active : 15 duels par jour, pas un de plus ; le 16e est refusé jusqu'à minuit (Paris).
    Coupée (RATION_ACTIVE = False, réglage actuel), le 16e passe."""
    import app.main as m
    monkeypatch.setattr(m, "RATION_ACTIVE", True)
    assert client.get("/api/moi").json()["ration"] == 15
    etat = client.get("/api/etat").json()
    faux = {}
    for p in etat["pieges"]:
        faux.setdefault(p["mot"], p["id"])
    mots = list(faux)[:16]
    for mot in mots[:15]:
        r = client.post("/api/choix", json={"mot": mot, "montres": [faux[mot]], "ordre": [faux[mot]], "erreur": False})
        assert r.status_code == 200
    assert client.get("/api/moi").json()["ration"] == 0
    r = client.post("/api/choix", json={"mot": mots[15], "montres": [faux[mots[15]]], "ordre": [], "erreur": True})
    assert r.status_code == 429
    monkeypatch.setattr(m, "RATION_ACTIVE", False)
    r = client.post("/api/choix", json={"mot": mots[15], "montres": [faux[mots[15]]], "ordre": [], "erreur": True})
    assert r.status_code == 200


def test_categorie_du_faux(client):
    """Le faussaire peut fausser la catégorie d'une définition ; une catégorie inventée est refusée."""
    client.get("/api/moi")
    assert client.post("/api/pieges", json={"mot": "sapajou", "texte": "D'un rouge sombre.", "categorie": "nom propre"}).status_code == 422
    r = client.post("/api/pieges", json={"mot": "sapajou", "texte": "D'un rouge sombre.", "categorie": "adj."})
    assert r.status_code == 200
    faux = [p for p in client.get("/api/etat").json()["pieges"] if p["id"] == r.json()["id"]][0]
    assert faux["categorie"] == "adj."


def test_contestation_controlee(client):
    """On ne conteste qu'un faux de ce lot, déjà eu en duel, et pas le sien."""
    client.get("/api/moi")
    f = _faux_de(client, "sapajou")[0]
    assert client.post("/api/contestations", json={"piege": "invente", "mot": "sapajou"}).status_code == 404
    assert client.post("/api/contestations", json={"piege": f, "mot": "sapajou"}).status_code == 403
    client.post("/api/choix", json={"mot": "sapajou", "montres": [f], "ordre": [f], "erreur": False})
    assert client.post("/api/contestations", json={"piege": f, "mot": "sapajou"}).status_code == 200


def test_pseudo_reserve_et_unique(client, tmp_path):
    client.get("/api/moi")
    assert client.put("/api/pseudo", json={"pseudo": "Truffe"}).status_code == 409
    assert client.put("/api/pseudo", json={"pseudo": "Le Faussaire"}).status_code == 200
    import app.main as m
    with TestClient(m.app) as autre:
        autre.get("/api/moi")
        assert autre.put("/api/pseudo", json={"pseudo": "le  faussaire"}).status_code == 409


def test_faux_identique_a_l_original_refuse(client):
    client.get("/api/moi")
    import app.main as m
    vraie = m.QUESTIONS["sapajou"]["vraie"]
    assert client.post("/api/pieges", json={"mot": "sapajou", "texte": vraie.upper()}).status_code == 422


def test_signalement_controle(client):
    client.get("/api/moi")
    assert client.post("/api/signalements", json={"mot": "sapajou", "raison": "spam"}).status_code == 422
    assert client.post("/api/signalements", json={"mot": "sapajou", "raison": "choquant"}).status_code == 200


def test_compression(client):
    r = client.get("/proches.json", headers={"Accept-Encoding": "gzip"})
    assert r.headers.get("content-encoding") == "gzip"
