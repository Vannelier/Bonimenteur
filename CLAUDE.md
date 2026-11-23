# CLAUDE.md

Bonimenteur (bonimenteur.fr) : jeu de bluff asynchrone. Le joueur démasque les
faux des autres (une vraie réponse contre un faux) et fabrique les siens pour
les duper. Quatrième jeu de la famille Discoverium, Vocabulium, Snouff.

État : prototype en une page (`prototype/index.html`), publié comme artifact
claude.ai : base partagée et identité des joueurs par `window.claude`. Il ne
tourne pas hors de claude.ai. Le vrai jeu reprendra l'architecture de
Discoverium (Python 3.11, FastAPI, front HTML/JS sans build, Railway).

## Carte

| Fichier | Contenu |
|---|---|
| `prototype/index.html` | Le jeu : duels, atelier (Fabriquer, Mes faux), arbitre, bilan. Réglages en tête du script (`TOTAL`, `PRIX_PIEGE`, `PRIX_DIRECT`, `BLOP_DEPART`, `MORT_VUS`, `PVQN_VUS`, `CONTEST_MIN`, `FAMILLES` et leurs seuils). |
| `prototype/proches.json` | Données de l'arbitre du sens, générées par `tools/proches.py`. Ne pas éditer. |
| `prototype/communes.txt` | Communes de France (geo.api.gouv.fr, 34 969). |
| `prototype/photos/` | Images des questions photo (Wikimedia Commons, crédits dans les questions). |
| `data/questions.json` | Les questions (`docs/questions.md`). |
| `data/faux-de-depart.json` | Trois faux de Truffe par question. |
| `tools/proches.py` | Calcule `prototype/proches.json` depuis les vecteurs de Vocabulium. |
| `docs/` | `conception.md` (règles, économie, chemin), `questions.md` (charte, familles), `arbitre.md`, `direction-artistique.md`. |

## Commandes

```
VOCABULIUM_DIR=../Vocabulium python tools/proches.py   # après un ajout de question
```

## Invariants

- La vraie réponse ne se distingue jamais d'un faux : même mise en forme
  (`formater`), région et registre dans la question, jamais dans la réponse.
- Le poseur voit la vraie réponse ; l'arbitre refuse un faux trop proche, sans
  dire en quoi. Une question tentée ne lui est plus posée.
- Un faux par joueur et par question ; une question où le joueur a un faux ne
  lui est pas posée.
- Le score et les blops se calculent sur les choix enregistrés, jamais sur ce
  que le client affirme (dans le vrai jeu : le serveur).
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
