# Questions

`data/questions.json` : une entrée par question, clé = identifiant.
`data/faux-de-depart.json` : trois faux par question, signés Truffe, pour que
la question soit jouable avant les premiers joueurs.

## Charte

Décidée avec l'auteur. Une bonne question :

1. Personne ne connaît la réponse : deviner devient une affaire de flair face
   aux faux, pas de culture (« placomusophile »). Le sens ne se déduit pas des
   mots : écartés pour cette raison « avoir des tomates sur les yeux », « pas
   mon cirque, pas mes singes », « je ne comprends que gare », « pas de vache
   sur la glace », « mécanophilie ». Attention aux racines grecques
   transparentes.
2. La vérité est plus folle qu'un mensonge.
3. Réponse courte, au format clair : les faux doivent pouvoir lui ressembler.
4. Vérité vérifiable, avec une source (`source`).
5. Tout public : pas de contenu sexuel (paraphilies essayées puis retirées).
6. Rien dans la vérité ne la distingue des faux : région et registre vont dans
   la question (`region`, `registre`), jamais entre parenthèses dans la réponse.

Et il doit être facile d'y inventer des faux (écartés pour cette raison : les
prix Ig Nobel).

## Familles

| `type` | Libellé | Question | Nombre (23/11/2026) |
|---|---|---|---|
| absent | Définition | un mot rare (`mot`) | 68 |
| `anecdote` | Anecdote | une phrase à trou `___` (`question`) | 16 |
| `commune` | Commune | une vraie commune au nom étonnant | 12 |
| `intraduisible` | Mot étranger | un mot sans équivalent | 11 |
| `photo` | Photo | une image (`image`, `alt`, `credit`) | 10 |
| `etrangere` | Expression étrangère | une expression traduite mot à mot | 9 |
| `expression` | Expression | l'origine d'une expression française | 6 |
| `metier` | Métier | un métier disparu, sa spécialité à deviner (carte de visite) | 14 |

Familles faibles : celles dont la réponse se sait souvent (expressions
françaises, anecdotes connues).

Définitions : `categorie` (n. m., n. f., n., adj., v., adv., pron.), relevée
dans le Wiktionnaire par `tools/categories.py` puis relue à la main (le premier
sens n'est pas toujours celui de la vraie réponse : « cagnard », adjectif,
est ici un nom). Affichée sur le feuillet de la vraie réponse.

Photos : `legende` (ce que montre l'image, sans la réponse) et `rubrique`
(Usage, Bâtisseur…). Le feuillet est une planche complète : la photo et
« Fig. Pince en métal. *Usage :* à friser les cheveux… », sans la question.

Champs facultatifs : `cadre` (mots communs à une série, ignorés par
l'arbitre : « peur » pour les phobies), `region`, `registre`, `source`.

## Forme des réponses

La page affiche les réponses telles qu'elles sont écrites, vraies comme faux :
majuscules et ponctuation d'un faux sont l'affaire du faussaire (décision de
l'auteur, 24/11/2026 : la page corrigeait « Étienne Daho » en « étienne
Daho »). Les vraies et les faux de départ s'écrivent donc dans leur forme
d'affichage, vérifiée par `test_donnees_coherentes` :

- anecdote : le bout de phrase qui remplace `___`, sans majuscule (sauf nom
  propre) ni point final ;
- photo : la suite de « Usage : », sans majuscule, avec point final ;
- commune : le nom, sans point ;
- autres familles : une phrase, majuscule et point final.

Seuls retouchés à l'affichage : les espaces en trop, et le point final d'une
anecdote, d'une commune ou d'une carte de visite, que la mise en page porte
déjà.

## Faux de départ

Chaque question a ses trois faux de Truffe. Les 15 définitions reprises de la
première version (carabistouille, cénacle, cuistre…) n'en avaient pas et
n'étaient jamais posées : faux écrits le 23/11/2026, tous sous 0,45 à
l'arbitre. Ces mots restent assez connus (charte, point 1) : à surveiller dans
les duels.

## Vérification

- Les vérités du premier pack (25 questions) et les ajouts suivants sont
  vérifiés dans une source (Wiktionnaire, CNRTL, Wikipédia) ; les faux de
  départ aussi, pour qu'aucun ne dise vrai. 26 questions sur 132 portent leur
  source dans `source` : les autres sont à sourcer. Exemples de faux corrigés : « sobremesa » veut aussi dire nappe et dessert ;
  « crocheteur » désigne aussi celui qui crochète les serrures.
- Communes : présentes dans la liste officielle (`prototype/communes.txt`,
  geo.api.gouv.fr, 34 969 communes). Bourré et Montcuq, fusionnées en 2016,
  ont été retirées.
- Photos : libres de droits (Wikimedia Commons), crédit dans `credit`.
- Écartées faute de source sûre : ergophobie, payer le canard, saucisse
  allemande, planète Vulcain, momies de chats, turophobie.

## Ajouter une question

1. L'écrire dans `data/questions.json` selon la charte, avec sa source.
2. Écrire trois faux de départ dans `data/faux-de-depart.json`.
3. Relancer `tools/proches.py` (sauf pour une commune).
