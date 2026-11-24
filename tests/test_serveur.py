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


def _authentifier(client, mot):
    """Expertise juste du lot : la pièce est authentifiée, le joueur peut la contrefaire (+1 écu)."""
    f = _faux_de(client, mot)[0]
    assert client.post("/api/choix", json={"mot": mot, "montres": [f], "ordre": [f], "erreur": False}).status_code == 200
    return f


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
    _authentifier(client, "sapajou"); _authentifier(client, "cacochyme")
    # 20 au départ + 2 expertises justes : un faux en direct (15) passe, le suivant à 10 n'a plus de quoi payer.
    r = client.post("/api/pieges", json={"mot": "sapajou", "texte": "Ragoût de fèves.", "prix": 15})
    assert r.status_code == 200
    assert client.get("/api/moi").json()["solde"] == 7
    assert client.post("/api/pieges", json={"mot": "cacochyme", "texte": "Plat mijoté."}).status_code == 402
    assert client.post("/api/pieges", json={"mot": "sapajou", "texte": "Autre."}).status_code in (402, 409)
    # Un autre joueur tombe dans le faux : l'auteur gagne 1 écu.
    import app.main as m
    with TestClient(m.app) as autre:
        autre.get("/api/moi")
        assert autre.post("/api/choix", json={"mot": "sapajou", "montres": [r.json()["id"]], "ordre": [], "erreur": True}).json()["gain"] == 0
    assert client.get("/api/moi").json()["solde"] == 8


def test_seulement_les_pieces_authentifiees(client):
    """On ne contrefait que la pièce authentifiée : ni un lot jamais joué, ni un lot où l'on a été floué."""
    client.get("/api/moi")
    texte = {"texte": "Ragoût de fèves.", "prix": 15}
    assert client.post("/api/pieges", json={"mot": "sapajou", **texte}).status_code == 403
    f = _faux_de(client, "cacochyme")[0]
    client.post("/api/choix", json={"mot": "cacochyme", "montres": [f], "ordre": [], "erreur": True})
    assert client.post("/api/pieges", json={"mot": "cacochyme", **texte}).status_code == 403
    _authentifier(client, "sapajou")
    assert client.post("/api/pieges", json={"mot": "sapajou", **texte}).status_code == 200


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
    # Forme d'affichage (docs/questions.md) : la page n'y touche plus. Anecdote : un bout de phrase,
    # sans majuscule ni point ; photo : la suite de « Usage : », sans majuscule.
    type_de = {k: q.get("type") for k, q in questions.items()}
    textes = [(q.get("type"), q["vraie"]) for q in questions.values()] + [(type_de[x["mot"]], x["texte"]) for x in faux]
    for typ, t in textes:
        if typ in ("anecdote", "photo"):
            assert not t[:1].isupper() or t[1:2].isupper(), t
        if typ == "anecdote":
            assert not t.endswith("."), t


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
    _authentifier(client, "sapajou")
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


def test_filtre_commun(client):
    """Pseudo offensant neutralisé en « Joueur » ; faux offensant refusé."""
    j = client.get("/api/moi").json()["id"]
    assert client.put("/api/pseudo", json={"pseudo": "Gros connard"}).json()["pseudo"] == "Joueur"
    assert client.post("/api/pieges", json={"mot": "sapajou", "texte": "Un vrai salopard."}).status_code == 422


def test_etat_allege(client):
    """L'état ne renvoie que les duels du joueur et ceux où son faux a trompé ; les compteurs par faux
    viennent du serveur."""
    client.get("/api/moi")
    _authentifier(client, "sapajou")
    r = client.post("/api/pieges", json={"mot": "sapajou", "texte": "Ragoût de fèves.", "prix": 15}).json()["id"]
    import app.main as m
    autres = []
    for _ in range(2):
        a = TestClient(m.app); a.__enter__(); a.get("/api/moi"); autres.append(a)
    t = _faux_de(client, "cacochyme")[0]
    autres[0].post("/api/choix", json={"mot": "sapajou", "montres": [r], "ordre": [], "erreur": True})
    autres[1].post("/api/choix", json={"mot": "cacochyme", "montres": [t], "ordre": [t], "erreur": False})
    e = client.get("/api/etat").json()
    # Sa propre expertise et le duel où son faux a trompé ; pas le duel de cacochyme.
    assert sorted((c["mot"], c["erreur"]) for c in e["choix"]) == [("sapajou", False), ("sapajou", True)]
    assert e["stats"][r] == [1, 1, 0] and e["stats"][t] == [1, 0, 1]
    assert len(autres[1].get("/api/etat").json()["choix"]) == 1   # ses propres duels seulement
    for a in autres: a.__exit__(None, None, None)


def test_classement_des_faussaires(client):
    """Un joueur dupé par le faux de A compte pour A cette semaine ; les faux de Truffe ne comptent pas.
    La jauge compte les joueurs qui ont joué."""
    a = client.get("/api/moi").json()["id"]
    _authentifier(client, "sapajou")
    faux_a = client.post("/api/pieges", json={"mot": "sapajou", "texte": "Ragoût de fèves.", "prix": 15}).json()["id"]
    import app.main as m
    with TestClient(m.app) as b:
        b.get("/api/moi")
        b.post("/api/choix", json={"mot": "sapajou", "montres": [faux_a], "ordre": [], "erreur": True})
        t = _faux_de(b, "cacochyme")[0]
        b.post("/api/choix", json={"mot": "cacochyme", "montres": [t], "ordre": [], "erreur": True})   # dupé par Truffe
    c = client.get("/api/etat").json()
    assert c["classement"]["semaine"] == [{"id": a, "victimes": 1}]
    assert c["classement"]["moi"] == {"rang": 1, "victimes": 1}
    assert c["classement"]["passee"] is None
    assert c["communaute"] == {"joueurs": 2, "objectif": 10}
