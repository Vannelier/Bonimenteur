# Direction artistique : l'Atelier du faussaire

On fabrique des faux (documents, billets, tampons) et on démasque ceux des
autres. Retenue le 22/11/2026 parmi cinq pistes (gazette des canulars,
bonimenteur de foire, prestidigitateur, naturaliste farceur). Le code fait
foi : `prototype/index.html`, en tête du `<style>`.

## Principes

- Sous-main de cuir vert ; le jeu posé dessus comme un dossier de papier crème,
  double filet vert et frise de guilloches, comme un billet.
- La question : une pièce officielle sur papier filigrané vert pâle, rosette
  en filigrane, numéro de série rouge (« N° A·4220 », tiré de l'identifiant).
- Révélation : tampon rouge « Contrefaçon » de travers sur le faux, timbre
  vert « Authentique » sur la vraie. Démasqué : sceau de cire intact. Dupé :
  tampon rouge « Dupé » (un sceau brisé a été jugé laid).
- Couleurs porteuses de sens : vert billet pour continuer (Suivante, Rejouer),
  rouge des tampons pour fabriquer (Piéger, Poser), encre bleu-noir pour les
  blops (des taches de cette encre).
- Progression : une planche de 15 timbres dentelés.
- Polices : Cinzel (capitales gravées des billets) pour titres et étiquettes ;
  Source Serif 4 pour le texte et les chiffres (ceux de Cinzel sont
  elzéviriens, « 10 » se lit « IO ») ; Stardos Stencil pour les tampons.
- Guilloches et rosette : SVG statiques générés (sinusoïdes), en données dans
  le CSS.
- Explicatif par l'image, pas par le texte : pastilles et icônes plutôt que
  des phrases.

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
