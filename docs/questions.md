# Questions

`data/questions.json` : une entrée par question, clé = identifiant.
`data/faux-de-depart.json` : trois faux par question, signés Mr Halifax, pour que
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

7. Amusant à contrefaire : l'objet et le ton de la réponse donnent au faussaire
   un style à imiter. Une carte de visite parle comme une réclame (« Faites
   préparer vos peaux fines de mouton et de chèvre par un professionnel ! »),
   pas comme un dictionnaire (règle de l'auteur, 25/11/2026). La question impose
   alors son objet (`ouvrage` : `carte` pour un métier, `brevet` pour un objet
   photographié), et ses faux de départ prennent le ton (`docs/artefacts.md`).
   Jamais une réponse réduite à un nombre ou à une date : le faussaire n'aurait
   qu'un nombre voisin à écrire.

Et il doit être facile d'y inventer des faux (écartés pour cette raison : les
prix Ig Nobel).

## Familles

| `type` | Libellé | Question | Nombre (25/11/2026) |
|---|---|---|---|
| absent | Définition | un mot rare (`mot`) | 74 |
| `anecdote` | Anecdote | une phrase à trou `___` (`question`) | 26 |
| `coutume` | Coutume | une phrase à trou `___` dans la voix du voyageur (« Ici, … »), avec `lieu` (« Ville, Pays ») et `timbre` (le pays dans sa langue) | 12 |
| `commune` | Commune | une vraie commune au nom étonnant | 18 |
| `intraduisible` | Mot étranger | un mot sans équivalent | 21 |
| `photo` | Photo | une image (`image`, `alt`, `credit`) | 19 |
| `etrangere` | Expression étrangère | une expression traduite mot à mot | 19 |
| `expression` | Expression | l'origine d'une expression française | 16 |
| `metier` | Métier | un métier disparu, sa spécialité à deviner (livret d'ouvrier, ou carte de visite réclame : `ouvrage`) | 24 |

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

- anecdote et coutume : le bout de phrase qui remplace `___`, sans majuscule
  (sauf nom propre) ni point final ;
- photo : la suite de « Usage : » ou, en brevet, de « Objet : »
  (« appareil permettant de… »), sans majuscule, avec point final ;
- commune : le nom, sans point ;
- métier en carte de visite (`ouvrage` : `carte`) : une réclame, ponctuée
  comme une réclame (« … par un professionnel ! ») ;
- autres familles : une phrase, majuscule et point final.

Seuls retouchés à l'affichage : les espaces en trop, et le point final d'une
anecdote, d'une commune ou d'un livret d'ouvrier, que la mise en page porte
déjà.

## Faux de départ

Chaque question a ses trois faux de Mr Halifax. Les 15 définitions reprises de la
première version (carabistouille, cénacle, cuistre…) n'en avaient pas et
n'étaient jamais posées : faux écrits le 23/11/2026, tous sous 0,45 à
l'arbitre. Ces mots restent assez connus (charte, point 1) : à surveiller dans
les duels.

## Vérification

- Les vérités du premier pack (25 questions) et les ajouts suivants sont
  vérifiés dans une source (Wiktionnaire, CNRTL, Wikipédia) ; les faux de
  départ aussi, pour qu'aucun ne dise vrai. 176 questions sur 229 portent leur
  source dans `source` (`wiktionary:`, `wiktionary-en:`, `wikipedia:`,
  `wikipedia-en:`, `geo.api.gouv.fr`) : les autres sont à sourcer. Exemples de faux corrigés : « sobremesa » veut aussi dire nappe et dessert ;
  « crocheteur » désigne aussi celui qui crochète les serrures.
- Communes : présentes dans la liste officielle (`prototype/communes.txt`,
  geo.api.gouv.fr, 34 969 communes). Bourré et Montcuq, fusionnées en 2016,
  ont été retirées.
- Photos : libres de droits (Wikimedia Commons), crédit dans `credit`.
- Écartées faute de source sûre : ergophobie, payer le canard, saucisse
  allemande, planète Vulcain, momies de chats, turophobie.

## Série du 25/11/2026

75 questions : 10 par famille, 6 communes, 9 photos. Toutes sourcées.

- Écartées faute de source sûre : Héron d'Alexandrie et l'eau bénite, les
  carottes violettes avant le XVIIe siècle, « sabler le champagne », « la fin
  des haricots », « avoir le cafard », « tirer son épingle du jeu », « monter
  sur ses grands chevaux » (origine marquée douteuse dans le Wiktionnaire).
- Faux de Mr Halifax passés à l'arbitre : 207 sur 207 sous le seuil de leur
  famille (0,02 sous le seuil au plus près ; 7 réécrits). Faux de commune
  absents de la liste officielle.
- Réponse chiffrée : retirée (25/11/2026). Le nombre de vitres de la pyramide
  du Louvre (« 673 ») et la durée d'un hoquet (« de 1922 à 1990 ») ne laissaient
  au faussaire qu'un nombre voisin à écrire, pas une contrefaçon amusante
  (remarque de l'auteur). Pyramide retirée ; le hoquet porte maintenant sur sa
  cause (un cochon de 160 kilos tombé sur Charles Osborne).
- Longueur : bas du second feuillet à 543 px au plus à 375 × 553, avec le faux
  le plus long de chaque lot (Playwright, 75 lots).
- Photos : Wikimedia Commons, réduites à 640 px, crédit dans `credit`. Le
  pomander, que Wikimedia refusait de servir (limite de débit), fourni par
  l'auteur : détail d'un portrait de 1518, domaine public.

## Coutumes du monde (25/11/2026)

12 coutumes, toutes sourcées (Wikipédia en français, anglais et allemand) : le
saut des diables par-dessus les bébés (Castrillo de Murcia), le Naki Sumo, le
« blackening » écossais, le chat de Noël islandais, les Kit Kat des examens au
Japon, les livres de la veille de Noël en Islande, le festin des singes de
Lopburi, la guerre des fusées de Vrontados, Donald Duck à Noël en Suède, la
course au fromage de Cooper's Hill, le drakkar brûlé de Lerwick, les marches
balayées de Brême. Écartées faute de source dans l'article : la cannelle des
célibataires danois, le prix du portage d'épouse. Faux de Mr Halifax sous 0,5 à
l'arbitre (seuil 0,65) ; un faux ne reprend jamais une autre vraie coutume du
même pays (la soupe au riz et l'amande, la danse des petites grenouilles).
Bas des pièces à 539 px au plus à 375 × 553.

## Ajouter des questions par lots (26/11/2026)

`tools/lot.py` : un lot JSON écrit dans `tools/lots/` (communes : nom et
département ; autres : champs de la question et trois faux), contrôlé puis
fusionné. Il vérifie la commune sur geo.api.gouv.fr et `communes.txt`, que
les faux de commune n'existent pas, la forme des définitions, la source,
les doublons, et que la vraie ne se trahit pas par sa longueur (0,7 à 1,35
fois la moyenne des faux). Pour une définition, il montre la première du
Wiktionnaire, à comparer. Puis `tools/proches.py` et `tools/lot.py
--arbitre`. Pages gardées dans `tools/cache/`, lues par curl (Wikimedia
répond 429 à urllib).

- Lot 01 : 12 communes, 13 définitions. Grossœuvre écartée (`communes.txt`
  la confond avec Grossouvre, Cher). « turlutaine » : propos frivole, pas
  idée fixe (Wiktionnaire). Vraies d'« escarbille » et de « pataquès »
  raccourcies, deux fois plus longues que leurs faux.
- Lot 02 : 18 communes, 17 définitions. « Crac'h » s'écrit « Crach » dans la
  base officielle. « pouacre » sans « avare », « baguenauder » sans
  « promener » (premiers sens du Wiktionnaire). Un faux de « pignouf » trop
  proche pour l'arbitre, réécrit.
- Lot 03 : 10 expressions (origine), 10 mots étrangers, 9 expressions
  étrangères. Contrôle des sources (`cle` du lot : la page existe et contient
  le mot-clé). Cordon-bleu sourcé par « cordon bleu », qui porte l'ordre du
  Saint-Esprit. Écartée faute de page : « montrer où les écrevisses passent
  l'hiver » (russe).
- Lot 04 : 25 métiers, 12 en livret d'ouvrier, 13 en carte de visite réclame.
  Quand le métier n'est pas le premier sens de la page (merlan, souffleur,
  moucheur, lampiste…), mot-clé exigé dans la page (« coiffeur »,
  « théâtre »…). Six faux réécrits, trop proches pour l'arbitre. Bas des
  pièces à 491 px au plus à 375 × 553.
- Lot 05 : 25 anecdotes, sourcées sur Wikipédia (mot-clé vérifié ;
  `tools/lot.py` suit maintenant les redirections). Écartée faute de source
  dans la page : Napoléon mis en déroute par des lapins. Questions
  d'Ōkunoshima et de Coolidge raccourcies : 584 px à 375 × 553 ; 543 px au
  plus ensuite. Vraies de la tulipe et du canular lunaire réécrites : aucun
  de leurs mots n'était connu de l'arbitre.
- Lot 06 : 18 coutumes (Italie, Finlande, pays de Galles, Autriche,
  Catalogne, Allemagne, Écosse, Espagne, Japon, Suisse, Angleterre, Mexique,
  Thaïlande). Écartée faute de source dans la page : les balais cachés de
  Noël en Norvège. Polterabend : « porcelaine », le mot de la page. Question
  de la tourbière raccourcie (551 px à 375 × 553, 509 ensuite).
- Lot 07 : 20 communes, 19 définitions. Noms officiels : « Petosse » (sans
  accent), « Les Cent-Acres ». « Sûre », faux de Sauve, est une vraie
  commune : remplacé. Béjaune : le premier sens est un jeune oiseau, le faux
  « oiseau des marais » écarté. Bibine et béjaune : mot-clé exigé, le sens
  retenu n'étant pas le premier de la page.
- Lot 08 : 13 mots étrangers, 12 expressions étrangères (Wiktionnaire
  anglais, mot-clé ou page vérifiée). Écartés faute de page : gökotta,
  slampadato, Handschuhschneeballwerfer, « sortir la vache de la glace »,
  « payer le canard » (portugais). « Prozvonit » raccourci : 560 px à
  375 × 553, 539 ensuite.
- Lot 09 : 25 métiers (12 livrets, 13 cartes). Haubergier et calendreur sans
  page (l'outil bloque désormais une page absente) : remplacés par taillandier
  et pelletier. Fourbisseur : mot-clé « armes » (premier sens : nettoyage
  d'une maison). Gagne-denier : commissions, pas portage (Wiktionnaire). Huit
  faux trop proches pour l'arbitre, réécrits.
- Lot 10 : 24 anecdotes (marques et leurs débuts, origines de mots, animaux,
  monuments). Sources reprises en anglais quand la page française ne portait
  pas le fait (Tour de France 1904, Kaldi). Écartée en cours : aucune.
  `tools/lot.py` vérifie maintenant la forme des anecdotes, coutumes et photos
  (pas de majuscule, pas de point) : la Marseillaise commençait par
  « Strasbourg ». Bas des pièces à 543 px au plus à 375 × 553.
- Lot 11 : 17 coutumes (Espagne, Japon, Pays-Bas, Bulgarie, Écosse,
  Angleterre, Catalogne, Belgique, France, Suisse, Pérou, Irlande, Suède,
  Italie, Allemagne). Sources possibles en allemand, espagnol, italien
  (`SOURCES`). Écartés faute de page ou de mot-clé : Kantō Matsuri, le requin
  du Þorrablót. Bas des pièces à 518 px au plus à 375 × 553.
- Lot 12 : 18 communes, 24 définitions. « Rougé » (pas « Rouge »). Faux de
  commune réels écartés : Grillon, Vaillant. Bamboche : le premier sens est
  une marionnette, le faux « marionnette » écarté. Pied-plat : « lâche »
  (Wiktionnaire), pas « grossier ». Carabin : premier sens, un cavalier ; le
  faux « garde de la maréchaussée » écarté.
- Lot 13 : 17 communes, 26 définitions. Faux trop proches du premier sens
  écartés : aigrefin (un poisson), pioupiou (cri des poussins). Mot-clé
  exigé quand le sens retenu n'est pas le premier (argousin, baderne,
  pandore, roquentin, panouille, falot…).
- Biais relevé le 26/11/2026 : 99 questions sur 236 (hors communes) avaient
  une vraie hors de 0,7 à 1,35 fois la moyenne de leurs faux (huchier : 76
  signes contre 33). Corrigé le jour même (`tools/lots/longueurs.json`) : faux
  de Mr Halifax réécrits à la longueur de la vraie, six vraies resserrées
  (eschatologie, bassinoire, tire-botte, pareidolie, haut du pavé,
  zigouiller) ; quatre faux réécrits trop proches pour l'arbitre (girafe,
  brimbelle, lunule, pareidolie). Gardé par `test_la_vraie_ne_se_trahit_pas_par_sa_longueur`.

## Ajouter une question

1. L'écrire dans `data/questions.json` selon la charte, avec sa source.
2. Écrire trois faux de départ dans `data/faux-de-depart.json`.
3. Relancer `tools/proches.py` (sauf pour une commune).
