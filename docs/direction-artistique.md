# Direction artistique : l'Atelier du faussaire

On fabrique des faux (documents, billets, tampons) et on démasque ceux des
autres. Retenue le 22/11/2026 parmi cinq pistes (gazette des canulars,
bonimenteur de foire, prestidigitateur, naturaliste farceur). Le code fait
foi : `prototype/index.html`, en tête du `<style>`.

## Principes

- Le joueur est l'expert : à chaque duel, on lui apporte deux feuillets d'un
  ouvrage ancien qui répondent à la même question ; l'un est d'époque, l'autre
  sort de l'atelier d'un faussaire (choisi par l'auteur le 23/11/2026, après
  les billets, le registre, l'établi et le porte-bloc, jugés illogiques ou
  « cheap »).
- Un ouvrage par famille (`OUVRAGES`) : dictionnaire universel (définition),
  d'anecdotes, des locutions, des communes de France, encyclopédie illustrée
  (photo), dictionnaire des mots du monde, recueil des locutions étrangères.
  Tout ce qui entoure la réponse (titre, page, tome, département) est
  identique sur les deux feuillets et vient de la question.
- Définition : « **sapajou**, *n. m.* Petit singe… ». La catégorie de la vraie
  vient des données (`categorie`, `tools/categories.py`) ; le faussaire choisit
  celle de son faux, il peut la fausser aussi.
- Papier vieilli en CSS : rousseurs, bords brunis, bord frangé (`clip-path`),
  caractères IM Fell English (SIL OFL).
- Révélation par les tampons : « Contrefaçon » et la signature du faussaire sur
  le faux (réponse barrée s'il est démasqué), timbre « D'époque » sur le vrai,
  étiquette « Acheté » sur la pièce choisie. La lampe à ultraviolets
  (`LAMPE_UV`) a été essayée puis écartée le 23/11/2026 : « ça ne marche pas »
  en jeu. Le code reste, coupé.
- Plus de question d'en-tête (23/11/2026) : le feuillet dit tout. Au-dessus,
  une ligne fine (famille, « Lot C·2912 ») et la consigne « Trouve le vrai ».
  Région et registre passent dans l'entrée du feuillet, identiques sur les
  deux (« **achaler**, *v., Québec.* »). Photo : chaque feuillet est une
  planche complète, la photo et sa légende (`legende`, `rubrique`), sans la
  question. Sous 700 px de haut,
  en-tête et feuillets resserrés ; sous 600 px, en-tête courant et pied des
  feuillets masqués. Bas du second feuillet mesuré (Playwright, 15 lots) :
  401 à 603 px à 390 × 664, 395 à 523 px à 375 × 553, tous dans l'écran.
- Démasqué : sceau de cire. Dupé : tampon « Dupé ».
- Couleurs porteuses de sens : vert billet pour continuer (Suivante), rouge
  des tampons pour fabriquer (Piéger, Poser), encre bleu-noir pour les blops.
- Icône du faux : une plume ; signatures à la plume (Caveat).
- Polices : Cinzel (titres, étiquettes), Source Serif 4 (texte, chiffres),
  IM Fell English (ouvrages anciens), Stardos Stencil (tampons), Caveat
  (signatures).
- Explicatif par l'image, pas par le texte.

## Révélation

Séquence d'environ 1,3 s, en CSS (classes `revele`, `choisi`, `autre`, `bien`,
`floue` posées par `repondre`), transform et opacity seulement :

| Temps | Ce qui se passe |
|---|---|
| 0 | la pièce achetée s'enfonce puis se soulève ; l'étiquette « Acheté » s'épingle |
| 300 ms | coup de tampon sur la pièce achetée |
| ≈ 600 ms | impact : la pièce tressaute, un éclat l'illumine (or si d'époque, rouge si faux) ; floué : la pièce secoue, la table tremble, le téléphone vibre (Android) |
| 750 ms | tampon de l'autre pièce |
| 1 050 ms | la signature du faussaire apparaît |
| 1 150 ms | le verdict monte, le gain saute, la pastille des blops bondit, la case du lot se pose |

Coût mesuré (Playwright, 390 × 780, processeur ralenti ×4, 5 révélations,
23/11/2026) : fil principal 110 ms par révélation avant, 355 ms après ; images
de plus de 34 ms : 2 sur les 5 révélations contre 1 sans animation, pire image
67 ms dans les deux cas (l'insertion du résultat). `will-change` essayé, sans
gain mesuré, retiré.

## Mise en page

Celle de Discoverium : en-tête, onglets (Jouer, Atelier), la question, les deux
réponses, le bouton principal dans le premier écran. L'atelier a deux
sous-onglets : Fabriquer, Mes faux.

Un mot à définir ne se coupe jamais en deux : sa police rétrécit jusqu'à
tenir sur une ligne (`ajusterMots`, 9 px au plus petit : la phobie de 36
lettres sur 320 px).

## Animer

Règles communes aux trois jeux (`CLAUDE.md` de Discoverium, « Animations ») :
seulement `transform` et `opacity`, rien d'animé dans un SVG, rien sous
`prefers-reduced-motion`. Tampons, timbre et sceau arrivent ainsi.

Pas encore mesuré au processeur ralenti ×4 : à faire avant la mise en ligne.
