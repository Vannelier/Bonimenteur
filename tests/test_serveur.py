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
    assert a["id"].startswith("j_") and a["solde"] == 10
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
    assert client.get("/api/moi").json()["solde"] == 11
    # Une question ne se rejoue pas.
    assert client.post("/api/choix", json={"mot": "sapajou", "montres": [f], "ordre": [], "erreur": True}).status_code == 409


def test_faux_inconnu_refuse(client):
    client.get("/api/moi")
    assert client.post("/api/choix", json={"mot": "sapajou", "montres": ["invente"], "ordre": [], "erreur": True}).status_code == 422


def test_poser_un_faux_paye_et_rapporte(client, tmp_path):
    client.get("/api/moi")
    assert client.post("/api/pieges", json={"mot": "sapajou", "texte": "Ragoût de fèves.", "prix": 15}).status_code == 402
    r = client.post("/api/pieges", json={"mot": "sapajou", "texte": "Ragoût de fèves."})
    assert r.status_code == 200
    assert client.get("/api/moi").json()["solde"] == 0
    assert client.post("/api/pieges", json={"mot": "sapajou", "texte": "Autre."}).status_code in (402, 409)
    # Un autre joueur tombe dans le faux : l'auteur gagne 1 blop.
    import app.main as m
    with TestClient(m.app) as autre:
        autre.get("/api/moi")
        assert autre.post("/api/choix", json={"mot": "sapajou", "montres": [r.json()["id"]], "ordre": [], "erreur": True}).json()["gain"] == 0
    assert client.get("/api/moi").json()["solde"] == 1


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
