# CLAUDE.md

Bonimenteur (bonimenteur.fr) : jeu de bluff asynchrone. Le joueur démasque les
faux des autres (une vraie réponse contre un faux) et fabrique les siens pour
les duper. Quatrième jeu de la famille Discoverium, Vocabulium, Snouff.

État : prototype en une page (`prototype/index.html`), écrit pour la base des
artifacts claude.ai (`window.claude`). Sur Railway, `app/main.py` (FastAPI,
SQLite) sert la page et `prototype/serveur.js` lui fournit la même interface,
branchée sur l'API. Sur claude.ai, `serveur.js` ne fait rien.

## Carte

| Fichier | Contenu |
|---|---|
| `app/pseudos.py` | Filtre des pseudos, copie exacte de Vocabulium (`tests/test_copies.py`) : ne pas l'éditer ici. Appliqué aussi aux textes des faux. |
| `app/main.py` | Serveur : page, API (`/api/moi`, `/api/etat`, `/api/pieges`, `/api/choix`, `/api/contestations`, `/api/signalements`, `/api/pseudo`), SQLite. Identité par cookie HttpOnly posé par le serveur ; auteur d'un faux, gain d'un duel, prix et solde décidés ici. |
| `prototype/serveur.js` | Interface `window.claude` (collection, doc, user) branchée sur l'API, relue toutes les 20 s et après chaque écriture ; passe à la page les compteurs par faux du serveur (`window.__statsServeur`). |
| `prototype/index.html` | Le jeu : duels, atelier (Contrefaire, Sur le marché), arbitre, bilan. Réglages en tête du script (`TOTAL`, `PRIX_PIEGE`, `PRIX_DIRECT`, `ECUS_DEPART`, `MORT_VUS`, `PVQN_VUS`, `CONTEST_MIN`, `FAMILLES` et leurs seuils). |
| `prototype/proches.json` | Données de l'arbitre du sens, générées par `tools/proches.py`. Ne pas éditer. |
| `prototype/communes.txt` | Communes de France (geo.api.gouv.fr, 34 969). |
| `prototype/photos/` | Images des questions photo (Wikimedia Commons, crédits dans les questions). |
| `data/questions.json` | Les questions (`docs/questions.md`). |
| `data/faux-de-depart.json` | Trois faux de Truffe par question. |
| `tools/proches.py` | Calcule `prototype/proches.json` depuis les vecteurs de Vocabulium. |
| `tools/categories.py` | Relève dans le Wiktionnaire la catégorie grammaticale des définitions (`categorie`), à relire. |
| `docs/` | `audit.md` (audit du 23/11/2026, points ouverts), `conception.md` (règles, économie, chemin), `questions.md` (charte, familles), `arbitre.md`, `direction-artistique.md`. |

## Commandes

```
pip install -r requirements-dev.txt
python -m pytest -q                                    # 18 tests, ~3 s
uvicorn app.main:app --reload                          # http://127.0.0.1:8000
VOCABULIUM_DIR=../Vocabulium python tools/proches.py   # après un ajout de question
```

CI : `.github/workflows/tests.yml` lance `pytest -q` sur chaque PR.

## Variables d'environnement

`BONIMENTEUR_DATA_DIR` (base SQLite ; à défaut le volume Railway,
`RAILWAY_VOLUME_MOUNT_PATH`, puis `var/` en local).

## Invariants

- La vraie réponse ne se distingue jamais d'un faux : même mise en forme
  (`formater`), région et registre dans la question, jamais dans la réponse.
- Le poseur voit la vraie réponse ; l'arbitre refuse un faux trop proche, sans
  dire en quoi. Une question tentée ne lui est plus posée.
- Un faux par joueur et par question ; une question où le joueur a un faux ne
  lui est pas posée.
- Le score et les écus se calculent sur les choix enregistrés. Limite connue :
  la page reçoit les vraies réponses et déclare elle-même si le joueur s'est
  trompé (`erreur`) ; le serveur ne peut pas encore le vérifier (`docs/audit.md`).
- Serveur : tout accès à SQLite sous `_verrou` ; limites de débit par IP
  (`LIMITES`) ; contestation seulement d'un faux eu en duel ; pseudos uniques,
  « Truffe » réservé.
- Toute nouvelle question suit la charte (`docs/questions.md`).

## Interface

- Explicatif par l'image, pas par le texte : pastilles et icônes plutôt que
  des phrases d'explication.
- Mise en page et règles d'animation communes aux trois autres jeux
  (`CLAUDE.md` de Discoverium : « Animations », « Mise en page mobile :
  vérifier le pire cas »). Mesurer à 390 × 664, 375 × 553, 360 × 640.

## Conventions

- Tout en français : code, commentaires, docs, messages de commit.
- Un chiffre de réglage cite sa mesure et le doc qui la détaille.
- Docs sobres : phrases courtes, chiffres sourcés, pas de récapitulatif.
- Travailler dans une PR ; en ouvrir une nouvelle si la précédente est mergée.
