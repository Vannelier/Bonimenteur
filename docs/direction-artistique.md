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
- Deux familles ont leur objet plutôt qu'une page : la commune est un panonceau
  de gare ancien, vieilli (crème jaunie, cadre vert écaillé, vis et coulures de
  rouille, rayures ; choisi parmi trois variantes le 23/11/2026, après la plaque
  émaillée bleue et la page de dictionnaire). Le métier a deux objets
  (25/11/2026, la carte de visite seule ne disait pas qu'il s'agissait d'un
  métier) : le livret d'ouvrier (couverture toilée au dos, « Délivré à »,
  « Profession » en capitales, « Ouvrage » à deviner, cachet de mairie), et
  la carte de visite réclame, où l'artisan vante son ouvrage (« Faites préparer
  vos peaux… par un professionnel ! » ; nom à la plume, coin corné, adresse).
  La question choisit la carte (`ouvrage` : `carte`) quand sa réponse est
  écrite en réclame : 12 métiers sur 24.
- Expression : fiche cartonnée de lexicographe (25/11/2026 ; avant, page de
  dictionnaire, qui ne disait pas qu'il fallait deviner l'origine) : « Locution »
  et numéro au-dessus d'un filet rouge, la locution entre guillemets,
  « Origine : » puis la réponse sur les lignes réglées, trou de tige en bas.
  Consigne : « Trouve la vraie origine ».
- Un artefact par famille (maquette G, 23/11/2026) : page de dictionnaire
  (définition : article seul, titre courant au mot, « 1° », cote au
  crayon), coupure de journal (anecdote : « Faits divers », journaux fictifs,
  date), guide de conversation en deux colonnes (mot et expression étrangère),
  planche gravée (photo : image en gravure dans sa cuvette, « Fig. n. — »,
  réponse en italique), livret d'ouvrier ou carte de visite (métier), fiche de
  lexicographe (expression), panonceau de gare (commune). Grain de papier fixe (bruit SVG, 3
  octaves) et encre foulée sur tous. Sous 600 px de haut, la planche passe en
  deux colonnes.
- Plusieurs ouvrages fictifs par famille (`OUVRAGES`, 22 en tout), tirés au
  sort par lot, le même pour les deux feuillets. Chacun a sa mise en page
  (`data-style` : classique ; filet double et vedette rouge ; lettrine et
  fleurons ; article numéroté « § 642. »), sa teinte de papier (`TEINTES`,
  quatre) et un pied à l'ancienne : signature d'imprimeur (« B 2 ») et titre
  abrégé (« Mauduit, Nouv. vocab. · 1852 »), au lieu du titre complet.
- Définition : « **sapajou** : *n. m.* Petit singe… », le mot défini en grand
  (23 px, 21 px sous 700 px de haut), suivi de « : » (demande de l'auteur,
  25/11/2026). La catégorie de la vraie
  vient des données (`categorie`, `tools/categories.py`) ; le faussaire choisit
  celle de son faux, il peut la fausser aussi.
- Papier vieilli en CSS : rousseurs, bords brunis, bord frangé (`clip-path`),
  caractères IM Fell English (SIL OFL).
- Révélation par les tampons : « Contrefaçon » et la signature du faussaire sur
  le faux (réponse barrée s'il est démasqué), timbre « D'époque » sur le vrai,
  étiquette « Certifié » sur la pièce choisie. La lampe à ultraviolets
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
  des tampons pour fabriquer (Piéger, Poser), or terni pour les écus.
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
| 0 | la pièce choisie s'enfonce puis se soulève ; l'étiquette « Certifié » s'épingle |
| 300 ms | coup de tampon sur la pièce choisie |
| ≈ 600 ms | impact : la pièce tressaute, un éclat l'illumine (or si d'époque, rouge si faux) ; floué : la pièce secoue, la table tremble, le téléphone vibre (Android) |
| 750 ms | tampon de l'autre pièce |
| 1 050 ms | la signature du faussaire apparaît |
| 1 150 ms | le verdict monte, le gain saute, la pastille des écus bondit, la case du lot se pose |

Coût, mesuré au processeur ralenti ×4 (Playwright, 390 × 780, trace
`devtools.timeline`, moyenne sur 4 révélations, 23/11/2026). Première version :
chute d'images signalée sur téléphone par l'auteur ; rastérisation 307 ms par
révélation contre 54 ms sans animation. Trois causes :

- les feuillets découpés (`clip-path`) et leurs dégradés étaient repeints à
  chaque image : ils ont maintenant leur calque dès l'affichage du duel
  (`will-change: transform`, et `opacity` pour l'éclat) ;
- deux animations de transform à la fois sur un même feuillet (enfoncement,
  puis tressautement), plus la transition du bouton : Chrome ne les compose
  pas (« TargetHasIncompatibleAnimations », trace `blink.animations`) et les
  fait tourner sur le fil principal ; une seule animation par cas désormais,
  plus de transition sur les feuillets ;
- `rotate(var(--r))` dans les keyframes : angles écrits en dur ;
- le tremblement de toute la carte : seule la table des feuillets tremble.

Après : rastérisation 39 ms par révélation (27 ms sans animation), aucune
animation non composée. Il reste ≈ 250 ms de fil principal par révélation au
processeur ralenti ×4, répartis sur 1,3 s (moins de 1 ms par image sur un
téléphone réel) ; images de plus de 34 ms : 2 sur 5 révélations, autant que
sans animation.

## Icône

Sceau de cire rouge traversé de la plume dorée du faussaire, sur le cuir vert du
sous-main (25/11/2026). Une seule source, `tools/icones.py`, comme Discoverium :
`prototype/favicon.svg`, `favicon.ico` (16, 32, 48 px, frames BMP),
`img/icon-192.png`, `img/icon-512.png`, `img/apple-touch-icon.png` (plein cadre),
déclarés dans la page et dans `manifest.webmanifest`.

## Mise en vente

Après « Mettre en vente » (25/11/2026, demande de l'auteur), la contrefaçon se
pose sur la table, signée, et le tampon « En vente » s'abat sur elle. Séquence
d'environ 1,1 s, en CSS, transform et opacity seulement, une animation de
transform par élément, rien sous `prefers-reduced-motion` :

| Temps | Ce qui se passe |
|---|---|
| 0 | la pièce tombe sur la table (`depose`) |
| 300 ms | la signature du faussaire apparaît |
| 450 ms | coup de tampon « En vente » (`coup-vente`) ; à l'impact, la table tressaute (`secousse`) |
| 800 ms | l'étiquette de prix s'épingle au coin de la pièce, sur la table (la pièce, découpée, la rognait) |
| 950 ms | la pastille des écus bondit |
| 1 000 ms | les boutons montent |

Coût, processeur ralenti ×4 (Playwright, 375 × 553, 4 mises en vente de chaque
sorte, 25/11/2026) : fil principal 467 ms en moyenne contre 275 ms avec
`prefers-reduced-motion` (sans animation), soit environ 45 ms sur un téléphone
réel, étalés sur 1,1 s ; une image de plus de 50 ms dans 2 essais sur 4 (77 et
80 ms), contre 1 sur 4 sans animation (56 ms). Des calques posés d'avance
(`will-change`) ne changeaient rien : retirés.

## Mise en page

Écran de duel (23/11/2026) : au-dessus des pièces, une seule ligne de consigne
(« Trouve la vraie définition », « Trouve le vrai métier »…) et le numéro du
lot, au lieu de la pastille de famille ; progression et solde sur une ligne.
Rien ne grandit au choix : la ligne des tampons de chaque pièce et la zone du
verdict, des boutons et de « Signaler le lot » (`#suite`, 152 px, 163 px sous
380 px de large, 8 px entre chaque) sont réservées dès l'affichage.
Mesuré sur 15 lots : 0 px de variation à 390 × 664 et 375 × 553 ; « Lot
suivant » dans l'écran à 390 × 664 (641 px au plus) ; sur iPhone SE, la page
descend jusqu'à lui une fois la révélation finie.

Après une bonne expertise, « Contrefaire » et « Lot suivant » ont la même
taille (25/11/2026) ; le prix (−15) est une étiquette posée sur le coin du
bouton, pour que « Contrefaire » tienne sur une ligne à 360 px. Mesuré
(Playwright, 98 lots de définition, métier et expression, faux le plus long) :
bas des pièces à 550 px au plus à 375 × 553 ; boutons de 52 px ; « Mettre en
vente » à 548 px au plus à l'écran de pose (aperçu sans en-tête ni adresse).

Celle de Discoverium : en-tête, onglets (Jouer, Atelier), la question, les deux
réponses, le bouton principal dans le premier écran. L'atelier a deux
sous-onglets : Contrefaire, Sur le marché.

Un mot à définir ne se coupe jamais en deux : sa police rétrécit jusqu'à
tenir sur une ligne (`ajusterMots`, 9 px au plus petit : la phobie de 36
lettres sur 320 px).

## Accueil

Même canevas que Discoverium, Snouff et Vocabulium (`CLAUDE.md` de Discoverium,
« Accueil ») : décor, titre, « Démasque les faux », explication sur deux lignes,
« Expertiser » et « Atelier » côte à côte (25/11/2026, comme « Jouer » et
« Multijoueur » de Snouff et Vocabulium ; Atelier en contour or, secondaire),
« À l'honneur cette semaine » (l'expert et le faussaire de la semaine, une
carte chacun, 25/11/2026), jauge des joueurs (pour qui
a déjà joué), « Nos autres jeux » en bas du premier écran, « Comment jouer »
8 px sous le bord. Décor : deux pièces du lot « sapajou », la vraie tamponnée
« D'époque », le faux « Contrefaçon », rien d'animé ; réduit sous 700 et 600 px
de haut. Le titre du jeu, en haut des autres écrans, ramène à l'accueil.

Mesuré le 24/11/2026 puis le 25/11/2026 avec « Atelier » (Playwright ; explication
raccourcie pour tenir en 2 lignes : « Authentifie la pièce d'époque, démasque le
faux… ») et avec « À l'honneur » (25/11/2026), accueil vide puis plein (les
deux cartes, ta place dans les deux classements avec « Signe ton nom », les deux
premiers de la semaine passée sur une ligne, noms abrégés au besoin, jauge) :
titre et « Expertiser » à la même place dans les deux états ; « Nos autres
jeux » finit à 638 px sur 664 (390 × 664), 533 sur 553 (375 × 553, plein), 614
sur 640 (360 × 640) ; pas de défilement horizontal.

## Atelier : lots tamponnés

Contrefaire : une tuile par famille (nombre de pièces authentifiées), puis la liste
des lots joués de la famille, tamponnés « Authentifié » (vert, se contrefait) ou
« Floué » (rouge, grisé, en pointillé). Les lots déjà contrefaits sont sur le
marché, pas dans la liste.

## Animer

Règles communes aux trois jeux (`CLAUDE.md` de Discoverium, « Animations ») :
seulement `transform` et `opacity`, rien d'animé dans un SVG, rien sous
`prefers-reduced-motion`. Tampons, timbre et sceau arrivent ainsi.

Pas encore mesuré au processeur ralenti ×4 : à faire avant la mise en ligne.
