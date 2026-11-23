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
- La question reste une pièce officielle sur papier filigrané (numéro de série
  rouge) ; sous-main de cuir vert, cadre à guilloches.
- Démasqué : sceau de cire. Dupé : tampon « Dupé ».
- Couleurs porteuses de sens : vert billet pour continuer (Suivante), rouge
  des tampons pour fabriquer (Piéger, Poser), encre bleu-noir pour les blops.
- Icône du faux : une plume ; signatures à la plume (Caveat).
- Polices : Cinzel (titres, étiquettes), Source Serif 4 (texte, chiffres),
  IM Fell English (ouvrages anciens), Stardos Stencil (tampons), Caveat
  (signatures).
- Explicatif par l'image, pas par le texte.

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
