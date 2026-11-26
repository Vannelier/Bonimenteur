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

Sceau de cire rouge traversé de la plume dorée du faussaire (25/11/2026), sur fond
transparent, cire éclaircie et contour de la plume en brun doré pour les fonds
clairs comme sombres (demande de l'auteur) ; l'icône iOS garde le cuir vert du
sous-main (iOS remplit de noir le transparent). Une seule source, `tools/icones.py`, comme Discoverium :
`prototype/favicon.svg`, `favicon.ico` (16, 32, 48 px, frames BMP),
`img/icon-192.png`, `img/icon-512.png`, `img/apple-touch-icon.png` (plein cadre),
déclarés dans la page et dans `manifest.webmanifest`.

Le masque AND des frames BMP porte la même transparence que l'alpha (26/11/2026).
Un masque tout à zéro dit « tout opaque » : les décodeurs qui le suivent plutôt que
l'alpha montraient le pourtour du sceau en noir, soit un carré noir derrière
l'icône. Discoverium ne le voyait pas : son icône est un carré plein.

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

## Planche de devises et carte de restaurant

Deux objets ajoutés le 26/11/2026 (`docs/artefacts.md`).

**Planche de devises** (`style` : `devise`, comme son thème) : l'écu sous un
bandeau crénelé d'or terni (couronne murale), le nom
de la ville en capitales espacées, la devise sur une banderole aux pointes
repliées (`clip-path`). L'émail du champ et le meuble viennent de la question
(`email`, `meuble`), dans une bibliothèque de huit meubles dessinés en SVG fixe
(tour, nef, lys, étoile, clé, chêne, croix, ancre) : l'écu approche les armes de
la ville, il ne les reproduit pas. Le métal du meuble est l'or, le gueules sur
un champ d'or ou d'argent (règle de contrariété des émaux).

**Carte de restaurant** : cadre gravé à double filet, maison et date en tête, un
plat de décor avant et un après la vedette (gris, tirés de l'empreinte du lot,
donc les mêmes sur les deux pièces), la composition en italique sous le plat.
Le cadre est un élément à lui (`.me-cadre`) : le `::after` du feuillet sert déjà
à la lampe UV.

Mesuré (Playwright) sur la vraie la plus longue de chaque thème (`d-montpellier`,
46 signes ; `m-hochepot`, 97) à 390 × 664, 375 × 553 et 360 × 640 : pièce de
216-217 px (devise) et 219-220 px (menu), contre 210 pour le brevet, le plus
haut des artefacts déjà là ; le bouton « Mettre en vente » de l'écran de pose
finit à 611 px et 623 px sur 640 ; pas de défilement horizontal. Comme pour le
brevet et le carnet, le duel se fait défiler : deux pièces de cette hauteur ne
tiennent pas ensemble dans l'écran.

## Carnet de voyage (coutumes)

Provenance lisible d'un coup d'œil (26/11/2026) : le pays en capitales
espacées (Cinzel 12 px, sépia #6b4a1f) derrière la boussole de la famille, sur
un filet qui court jusqu'au timbre ; la ville et le jour en dessous, à la main
(Kalam 15 px). Avant, « Ville, Pays » tenait sur une seule ligne manuscrite qui
passait à la ligne sous 390 px et se perdait dans le texte de la coutume.

Marques de valeur : filet doré le long du dos de cuir, cote de folio
(« fº 167 ») dorée et verticale sur le dos — la pièce vient d'un fonds, elle
porte un numéro. L'oblitération est devenue un vrai cachet à cheval sur le
timbre et la page (barres de rebut, sans texte) : le jour écrit dedans à 8 px
était coupé par le timbre. Timbre élargi à 40 px et nom du pays à 6 px :
« Deutschland », le plus long des 16, tient sans être coupé (33 px pour 34).

Mesuré (Playwright, 390 × 664, 375 × 553, 360 × 640) sur les pires cas — timbre
le plus long (`k-treppe`, Deutschland), lieu le plus long (`k-tourbiere`,
Llanwrtyd Wells, pays de Galles), texte le plus long (`k-blackening`) : la
pièce ne grandit pas (207 → 200 px pour `k-blackening`, 176 → 177 pour
`k-tourbiere`, à 360 px de large).

### Pistes pour la rendre plus précieuse (non faites)

- **Ex-libris du cabinet** : cachet rond à sec, gaufré, très pâle dans un coin.
- **Ruban signet** : une langue de soie qui dépasse du dos, 6 px, teinte par
  famille d'ouvrage.
- **Monogramme du voyageur** : initiales à la plume au bas de la page, les
  mêmes pour tout le carnet (le carnet a un auteur, pas seulement un lieu).
- **Visa de douane** : second cachet rectangulaire, seulement sur une pièce sur
  trois (tiré de l'empreinte) — une marque rare se remarque.
- **Encre passée** : plus la cote de folio est basse, plus l'encre tire vers le
  brun ; les premières pages ont voyagé plus longtemps.
- **Coin corné** : la page a été manipulée (triangle CSS en bas à droite, sous
  la tache de thé déjà présente).
- **Tranche dorée** : filet dégradé sur le bord droit de la page.

À n'en garder qu'une ou deux : la pièce doit rester lisible en duel, et la
vraie ne doit jamais se distinguer du faux par sa décoration (un détail tiré de
l'empreinte du lot, jamais du texte de la réponse).

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
« Accueil ») : décor, titre, « L'expert et le faussaire », explication sur deux lignes,
« Expertiser » et « Atelier » côte à côte (25/11/2026, comme « Jouer » et
« Multijoueur » de Snouff et Vocabulium ; Atelier en contour or, secondaire),
« Podium de la semaine » (26/11/2026 : deux colonnes de parchemin à égalité,
experts — filé vert, sceau — et faussaires — filé rouge, plume —, trois places
chacune, pastille or, argent, bronze comme le podium de Discoverium ; ta ligne
sur fond d'or ; place vide : pastille en pointillé et tiret, la hauteur ne bouge
pas), jauge des joueurs (pour qui
a déjà joué), « Nos autres jeux » en bas du premier écran, « Comment jouer »
8 px sous le bord. Décor : deux pièces du lot « sapajou », la vraie tamponnée
« D'époque », le faux « Contrefaçon », rien d'animé ; réduit sous 700 et 600 px
de haut. Le titre du jeu, en haut des autres écrans, ramène à l'accueil.

Mesuré le 24/11/2026 puis le 25/11/2026 avec « Atelier » (Playwright ; explication
raccourcie pour tenir en 2 lignes : « Authentifie la pièce d'époque, démasque le
faux… »), et le 26/11/2026 avec les deux podiums, dans trois états : accueil vide,
accueil plein (ta place hors podium avec « Signe ton nom », les deux premiers de la
semaine passée sur une ligne, jauge) et pseudos à 16 caractères avec toi sur le
podium. Titre, « Expertiser » et le bloc du classement à la même place dans les
trois états ; « Nos autres jeux » finit à 638 px sur 664 (390 × 664), 549 sur 553
(375 × 553, plein — podiums resserrés sous 700 px de haut), 614 sur 640
(360 × 640) ; noms abrégés au besoin, pas de défilement horizontal.

## Atelier : lots tamponnés

Contrefaire : une tuile par famille (nombre de pièces authentifiées), puis la liste
des lots authentifiés de la famille, tamponnés « Authentifié » (vert). Les lots
floués n'y figurent plus (26/11/2026 : leur ligne grisée n'apprenait rien, on ne les
contrefait pas) ; une famille sans pièce authentifiée disparaît. Les lots déjà
contrefaits sont sur le marché, pas dans la liste.

Hors de portée : un bouton d'achat que les écus ne couvrent pas (Retoucher −5,
Rééditer −25, +1 place −20, Contrefaire −10 ou −15) se fane — fond crème, texte
et prix gris, relief à plat (26/11/2026 ; avant, seul l'attribut `disabled` le
disait, et le bouton gardait ses couleurs). Les gestes gratuits (Ranger,
Remettre) gardent les leurs.

## Animer

Règles communes aux trois jeux (`CLAUDE.md` de Discoverium, « Animations ») :
seulement `transform` et `opacity`, rien d'animé dans un SVG, rien sous
`prefers-reduced-motion`. Tampons, timbre et sceau arrivent ainsi.

Pas encore mesuré au processeur ralenti ×4 : à faire avant la mise en ligne.
