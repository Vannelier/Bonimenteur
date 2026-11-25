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
| `plaque` | panonceau de gare ancien | le nom de la commune | `objet` |
| planche gravée | photo dans sa cuvette, « Fig. n. — » (pages `classique`, `filet` du thème photo) | après la rubrique (« Usage : ») | `plancheGravee` |

## Thèmes et leurs artefacts

Nombre de questions au 25/11/2026 (217 en tout).

| Thème (`type`) | Questions | Artefacts | Choix |
|---|---|---|---|
| définition | 74 | page de dictionnaire (`classique`, `filet`) | au sort |
| anecdote | 26 | coupure de journal | — |
| mot étranger (`intraduisible`) | 21 | guide de conversation | — |
| expression étrangère (`etrangere`) | 19 | guide de conversation | — |
| commune | 18 | panonceau de gare | — |
| expression | 16 | fiche de lexicographe | — |
| photo | 19 | planche gravée (14), brevet d'invention (5) | `ouvrage` : `brevet` pour les objets dont la réponse parle comme un brevet |
| métier | 24 | livret d'ouvrier (12), carte de visite réclame (12) | `ouvrage` : `carte` pour les réponses en réclame |

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

Télégramme et carnet de voyage : retenus par l'auteur comme objets, sans
thème encore (les mots étrangers ne lui semblent pas le bon).
