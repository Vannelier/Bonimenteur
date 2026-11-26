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
| `app/main.py` | Serveur : page, API (`/api/moi`, `/api/etat` (avec les classements de la semaine, experts `_experts` et faussaires `_piegeurs`, et la jauge des joueurs, `_communaute`), `/api/pieges`, `/api/choix`, `/api/contestations`, `/api/signalements`, `/api/pseudo`, `/api/actes` (gestes du faussaire sur son étal, `_situation`, `_places`), `/api/defis` (défi par lien ; `/api/etat?defi=CODE` ne renvoie que ce défi)), SQLite. Identité par cookie HttpOnly posé par le serveur ; auteur d'un faux, gain d'un duel, prix et solde décidés ici. |
| `prototype/serveur.js` | Interface `window.claude` (collection, doc, user) branchée sur l'API, relue toutes les 20 s et après chaque écriture ; passe à la page les compteurs par faux du serveur (`window.__statsServeur`). |
| `prototype/index.html` | Le jeu : accueil (canevas des trois autres jeux, les deux podiums de la semaine côte à côte, experts et faussaires, trois places chacun, `majAccueil`, `PODIUM`), classements complets en deux onglets (`ecranClassement`), duels, atelier (Contrefaire : les lots authentifiés seulement, tamponnés « Authentifié » ; Sur le marché : étal, éditions, ranger, rééditer, retoucher, `acte` ; tout bouton d'achat hors de portée est grisé, `.bouton:disabled`), arbitre, bilan. Réglages en tête du script (`TOTAL`, `PRIX_PIEGE`, `PRIX_DIRECT`, `ECUS_DEPART`, `PVQN_VUS`, `CONTEST_MIN`, `EXEMPLAIRES`, `ETAL`, `ETAL_MAX`, `PRIX_REEDITION`, `PRIX_RETOUCHE`, `PRIX_PLACE`, `FAMILLES` et leurs seuils). |
| `prototype/proches/` | Données de l'arbitre du sens, générées par `tools/proches.py` : `index.json` (mots vides) et 32 paquets `p<k>.json`, chargés par la page à la demande (`listeProches`). Ne pas éditer. |
| `prototype/communes.txt` | Communes de France (geo.api.gouv.fr, 34 969). |
| `prototype/photos/` | Images des questions photo (Wikimedia Commons, crédits dans les questions). |
| `data/questions.json` | Les questions (`docs/questions.md`). Onze thèmes, dont `devise` (devise d'une ville, sur une planche d'armorial) et `plat` (composition d'un plat oublié, sur une carte de restaurant), ajoutés le 26/11/2026. |
| `data/faux-de-depart.json` | Trois faux de Mr Halifax (faussaire maison, identifiant `truffe`) par question, impérissables, en complément tant qu'une question a moins de 3 faux de joueurs en vente (`MELANGE`). |
| `tools/lot.py` | Import de questions par lots (`tools/lots/*.json`) : contrôle (commune réelle, faux inexistants, forme, source, longueur de la vraie face aux faux), fusion, `--arbitre` (faux de Mr Halifax trop proches). `docs/questions.md`. |
| `tools/artifact.py` | Construit le dossier de l'artifact claude.ai : page sans `serveur.js`, `donnees.json` (questions et faux de Mr Halifax, lus par la page à la place de la base, `PRET_DONNEES`), paquets de l'arbitre. Photos, icônes et communes publiées à part, quand elles changent. |
| `tools/proches.py` | Calcule `prototype/proches/` depuis les vecteurs de Vocabulium. |
| `tools/icones.py` | Favicon et icônes d'application (sceau de cire et plume dorée), sur fond transparent : `prototype/favicon.svg`, `favicon.ico` (frames BMP dont le masque AND porte la même transparence que l'alpha, sans quoi un carré noir entourait le sceau), `img/`. |
| `tools/categories.py` | Relève dans le Wiktionnaire la catégorie grammaticale des définitions (`categorie`), à relire. |
| `docs/` | `artefacts.md` (thèmes de questions et types d'artefacts : à lire avant d'ajouter l'un ou l'autre), `audit.md` (audit du 23/11/2026, points ouverts), `conception.md` (règles, économie, chemin), `questions.md` (charte, familles), `arbitre.md`, `direction-artistique.md`. |

## Commandes

```
pip install -r requirements-dev.txt
python -m pytest -q                                    # 23 tests, ~6 s
uvicorn app.main:app --reload                          # http://127.0.0.1:8000
VOCABULIUM_DIR=../Vocabulium python tools/proches.py   # après un ajout de question
```

CI : `.github/workflows/tests.yml` lance `pytest -q` sur chaque PR.

## Variables d'environnement

`BONIMENTEUR_DATA_DIR` (base SQLite ; à défaut le volume Railway,
`RAILWAY_VOLUME_MOUNT_PATH`, puis `var/` en local).

## Invariants

- La vraie réponse ne se distingue jamais d'un faux par la page : région et
  registre dans la question, jamais dans la réponse. Le faux s'affiche tel que
  le faussaire l'a écrit (`formater` ne retire que les espaces en trop) ; les
  vraies sont écrites dans leur forme d'affichage (`docs/questions.md`).
- Le poseur voit la vraie réponse ; l'arbitre refuse un faux trop proche, sans
  dire en quoi. Une question tentée ne lui est plus posée.
- Un faux par joueur et par question ; une question où le joueur a un faux ne
  lui est pas posée.
- Le score et les écus se calculent sur les choix enregistrés. Limite connue :
  la page reçoit les vraies réponses et déclare elle-même si le joueur s'est
  trompé (`erreur`) ; le serveur ne peut pas encore le vérifier (`docs/audit.md`).
- Étal (`docs/conception.md`, « Édition et étal ») : un faux neuf, une remise en vente ou une
  réédition exigent une place libre ; le serveur refuse sinon (423). Actes en ajout seul.
- On ne contrefait que les pièces authentifiées (lot où le joueur a trouvé la vraie) ;
  le serveur refuse les autres (403).
- Serveur : tout accès à SQLite sous `_verrou` ; limites de débit par IP
  (`LIMITES`) ; contestation seulement d'un faux eu en duel ; pseudos uniques,
  « Mr Halifax » et « Truffe » réservés.
- Toute nouvelle question suit la charte (`docs/questions.md`), dont la règle 7 :
  amusante à contrefaire, la réponse parle le ton de son objet.

## Vocabulaire

- **Thème** de question (définition, métier, photo…) : champ `type`, `famille` dans le code.
- **Type d'artefact** (page, panonceau, brevet, livret…) : `style` des `OUVRAGES`. Un thème
  peut en avoir plusieurs ; la question impose le sien par `ouvrage`. Voir `docs/artefacts.md`.

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
