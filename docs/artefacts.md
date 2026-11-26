# Thèmes et types d'artefacts

Deux notions distinctes (clarifiées le 25/11/2026, demande de l'auteur).

- **Thème** : ce que la question demande (une définition, l'origine d'une
  expression, un métier…). Champ `type` de la question (absent pour une
  définition) ; `famille` et `FAMILLES` dans le code ; liste et charte dans
  `docs/questions.md`.
- **Type d'artefact** : l'objet sur lequel les deux pièces du lot sont
  présentées (une page de dictionnaire, un panonceau, un brevet…). Attribut
  `style` des `OUVRAGES` dans `prototype/index.html`, posé en
  `data-style` sur chaque pièce ; une fonction de rendu par type.

Les deux noms peuvent coïncider quand le thème n'a qu'un objet et que l'objet
ne sert qu'à lui : `devise` est à la fois le thème et le `style` de sa planche
(demande de l'auteur, 26/11/2026, par simplicité).

Un thème a un ou plusieurs types d'artefacts. Quand il en a plusieurs, le
type est tiré au sort par lot (le même pour les deux pièces), sauf si la
question l'impose (champ `ouvrage`). On l'impose quand la réponse est écrite
dans le ton de l'objet (charte, règle 7 : une carte de visite parle comme une
réclame, un brevet comme un inventeur).

## Types d'artefacts

| Type (`style`) | Objet | Où va la réponse | Rendu |
|---|---|---|---|
| `classique`, `filet` | page de dictionnaire ou d'encyclopédie (deux mises en page) | après le mot défini, « **mot** : » | `feuillet` |
| `coupure` | coupure de journal, « Faits divers » | à la place de `___` dans la phrase | `coupure` |
| `guide` | guide de conversation, deux colonnes | colonne du français | `guide` |
| `fiche` | fiche cartonnée de lexicographe | après « Origine : » | `fiche` |
| `livret` | livret d'ouvrier | après « Ouvrage » | `livret` |
| `carte` | carte de visite réclame | le slogan de l'artisan | `carteVisite` |
| `brevet` | brevet d'invention, avec la planche du dessin | après « Objet : » | `brevet` |
| `carnet` | carnet de voyage : pays en capitales sous une boussole, ville et jour à la main, timbre du pays oblitéré, dos de cuir à filet doré et cote de folio (Kalam) | à la place de `___` dans la phrase | `carnet` |
| `plaque` | panonceau de gare ancien | le nom de la commune | `objet` |
| `devise` | planche de devises : écu sous couronne murale, nom de la ville, banderole | la devise, sur la banderole | `devise` |
| `menu` | carte d'un restaurant, cadre gravé, plats de décor en gris | la composition, sous le plat en vedette | `menu` |
| planche gravée | photo dans sa cuvette, « Fig. n. — » (pages `classique`, `filet` du thème photo) | après la rubrique (« Usage : ») | `plancheGravee` |

## Thèmes et leurs artefacts

Nombre de questions au 26/11/2026 (650 en tout).

| Thème (`type`) | Questions | Artefacts | Choix |
|---|---|---|---|
| définition | 173 | page de dictionnaire (`classique`, `filet`) | au sort |
| commune | 103 | panonceau de gare | — |
| anecdote | 75 | coupure de journal | — |
| métier | 74 | livret d'ouvrier (36), carte de visite réclame (38) | `ouvrage` : `carte` pour les réponses en réclame |
| coutume | 52 | carnet de voyage | — |
| expression étrangère (`etrangere`) | 46 | guide de conversation | — |
| mot étranger (`intraduisible`) | 43 | guide de conversation | — |
| photo | 39 | planche gravée (31), brevet d'invention (8) | `ouvrage` : `brevet` pour les objets dont la réponse parle comme un brevet |
| expression | 26 | fiche de lexicographe | — |
| devise | 10 | planche de devises | — |
| plat | 9 | carte de restaurant | — |

## Ajouter un type d'artefact

1. Une entrée dans `OUVRAGES` du thème, avec son `style`.
2. Sa fonction de rendu, appelée par `feuillet` ; la réponse dans un élément
   `.rep` (surligné dans l'aperçu de pose, barré quand le faux est démasqué).
3. Ses styles CSS (`[data-style="…"]`), sans rien d'animé dedans, et son
   aperçu compact à l'écran de pose (`.feuillet.modele`).
4. Si la réponse change de ton : `ouvrage` sur les questions concernées,
   vraies et faux de départ réécrits, faux repassés à l'arbitre.
5. Mesurer à 390 × 664, 375 × 553 et 360 × 640, avec le faux le plus long :
   pièces et bouton de pose dans l'écran.
6. Une ligne dans les deux tableaux ci-dessus.

## Pistes (non faites)

Maquettes du 26/11/2026, après une planche des douze artefacts rendus côte à
côte (une capture de duel par type, 360 px, pire texte du thème).

Retouches, par ordre de rendement :

1. **Photo en grand, une seule fois** (le plus gros gain). L'image fait 60 px
   dans la pièce et s'affiche deux fois, identique : elle passe une fois
   au-dessus du duel, sous verre, et les deux pièces deviennent des
   **cartels de musée** qui ne portent que l'identification. Nouveau type
   `cartel` pour le thème photo, la planche gravée garde l'autre moitié.
2. **Page de dictionnaire** (74 questions, l'artefact le plus plat) : entrées
   voisines en gris au-dessus et en dessous, tirées de l'empreinte du lot donc
   identiques sur les deux pièces ; filet de gouttière à gauche ; réclame en
   bas à droite (le premier mot de la page suivante). La pièce se lit comme une
   page, pas comme un cadre autour d'un mot. Règle le fait que `classique` et
   `filet` se ressemblent trop.
3. **Coupure de journal** : elle ne paraît pas coupée. Bord déchiré en bas
   (masque CSS), manchette du journal en tête, amorce de la colonne voisine en
   pavé illisible, papier plus gris que la crème du livre.
4. **Carte de visite** : presque vide et de ton moderne. Cadre gravé à double
   filet, fleurons, nom à l'anglaise, « Maison fondée en 18.. » en bas.
5. **Livret d'ouvrier** : le cachet de mairie passe sur le nom du métier ; le
   descendre dans le coin.
6. **Guide de conversation** : « Leçon XII » en tête et un folio ; une ligne de
   prononciation sous le mot étranger demanderait un champ en plus dans les
   questions.

Nouveaux objets et thèmes :

- **Télégramme** — objet retenu par l'auteur, sans thème jusqu'ici (les mots
  étrangers ne lui semblaient pas le bon). Thème proposé : **les dépêches**, ce
  que disait le télégramme qui annonçait un événement. Majuscules, mots
  comptés, STOP : le faussaire doit écrire télégraphique.
- **Cartel de musée** — voir la retouche 1 : deuxième artefact du thème photo,
  sans nouvelle question à écrire.

Faits le 26/11/2026 : la **planche de devises** (thème `devise`) et la **carte
de restaurant** (thème `plat`), lot 15.

### Deux exemples par thème (26/11/2026)

Maquettés en duel (vraie contre faux de Mr Halifax), pièce à 330 px.

| Thème | Lot | Réponse (résumée) | Source |
|---|---|---|---|
| Dépêche | Kitty Hawk, 17 déc. 1903 | quatre vols, vent de 21 milles, le plus long 57 secondes, prévenez la presse, rentrons pour Noël | Library of Congress, `mcc.061` ; le « 57 » est l'erreur du télégraphiste (59 s réels), NPS |
| Dépêche | Louxor, nov. 1922 | découverte merveilleuse dans la vallée, tombe magnifique, sceaux intacts, recouverte en attendant votre arrivée | National Geographic ; clause finale dans HistoryNet ; date à confirmer |
| Devise | Montpellier | Virgo Mater, natum ora, ut nos juvet omni hora | Geneawiki, blason de Montpellier |
| Devise | Paris | Fluctuat nec mergitur | paris.fr — **enfreint la règle 1** (tout le monde la connaît), gardé pour montrer l'objet |
| Cartel | `o-bourdalou` | urinoir de voyage pour les dames | question existante |
| Cartel | `o-kangri` | pot de braises porté sous le manteau | question existante |
| Plat | à la financière | crêtes et rognons de coq, quenelles, ris d'agneau, champignons, olives, truffe | Escoffier, *Guide culinaire* (ckbk) ; CooksInfo |
| Plat | lièvre à la royale | sept heures de cuisson jusqu'à l'effiloché, ail et échalote, sauce liée au sang | Couteaux, *Le Temps*, 29 nov. 1898 (Guide Michelin, Wikipédia) ; quantités à fixer sur Gallica |

Deux réserves relevées à l'écriture : les devises des grandes villes tombent
sous la règle 1 (le vivier jouable, ce sont les communes inconnues, 17 586
fiches sur armorialdefrance.fr), et une devise latine demande au faussaire
d'écrire en latin — à trancher, ou restreindre aux devises en français.

Le carnet de voyage a trouvé son thème : « Coutumes du monde », ajouté le
25/11/2026.

Écarté : remèdes d'apothicaire (composition, vertus des remèdes de charlatan),
jugé drôle mais pas jouable par l'auteur (25/11/2026). Leçon : la partie cachée
doit laisser inventer, pas choisir dans une liste fermée (une maladie contre
une autre).
