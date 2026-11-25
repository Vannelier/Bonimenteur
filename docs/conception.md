# Conception

Règles du prototype (`prototype/index.html`) et chemin qui y a mené. Le code
fait foi ; les réglages sont en tête de son script.

## Le jeu en une phrase

Le joueur démasque les faux des autres (une vraie réponse contre un faux, à
chaque duel) et fabrique les siens pour les duper. Fabriquer est le plaisir ;
démasquer rapporte de quoi fabriquer.

## Lexique : l'expertise

Décision de l'auteur, 24/11/2026 (avant, le 23/11 : antiquaire qui achète les
pièces) : le joueur est expert et faussaire. À l'expertise, il authentifie la
pièce d'époque sans l'acheter, et son expertise lui rapporte 1 écu ; une pièce
authentifiée, il l'a eue entre les mains, il peut la contrefaire. Dans son
atelier, il met ses faux sur le marché ; un faux qui trompe un expert se vend
comme authentique, d'où l'écu du faussaire. Précédent réel : Abraham Bredius,
spécialiste de Vermeer, authentifia en 1937 *Les Pèlerins d'Emmaüs*, faux de
Han van Meegeren.

Seul le vocabulaire a changé : aucune règle, aucun prix.

| Jeu | Dans l'interface |
|---|---|
| duel | lot (« Lot C·2912 »), « Authentifie la pièce d'époque » ; étiquette « Certifié » sur la pièce choisie (« Authentifié » coupait la signature à 360 px) ; dans l'atelier, lots « Authentifié » ou « Floué » |
| bonne réponse | « Expertise juste. », sceau de cire |
| mauvaise réponse | « Tu as certifié un faux. », tampon « Floué » |
| tournée de 15 duels | vacation (« Fin de vacation », « Nouvelle vacation ») |
| onglets | Expertise, Atelier ; dans l'atelier : Contrefaire, Sur le marché |
| poser un faux | « Mettre en vente » ; après : « En vente » |
| faux éteint (mèche) | Saisi ; contesté : Retiré du marché |
| plus vrai que nature | Pièce de maître |
| victimes depuis la dernière visite | « Tes faux ont trouvé preneur » |
| arbitre | « Trop proche de l'original. » |

## La ration du jour

Coupée pour les essais (demande de l'auteur, 23/11/2026) : `RATION_ACTIVE =
false` dans la page et dans `app/main.py`. Les 15 duels sont alors une
tournée suivie d'un bilan et d'« Encore », sans limite. Ce qui suit décrit
la ration active.

- 15 duels par jour, heure de Paris (`TOTAL`, `RATION` côté serveur ; décision
  de l'auteur, 23/11/2026). Il n'y a plus de partie avec un score à battre : on
  joue pour remplir son encrier, la ration donne le rythme, et c'est elle qui
  se vendra (une ration de plus).
- La ration se compte sur les duels enregistrés : recharger la page ou changer
  d'appareil ne la remet pas à zéro. Le serveur refuse le 16e duel du jour.
- Chaque duel montre une question, sa vraie réponse et un faux écrit par un
  autre joueur, dans un ordre tiré au hasard.
- Bonne réponse : +1 écu. Mauvaise : le joueur est la victime du faux, et
  l'auteur du faux gagne 1 écu.
- La vraie réponse et l'auteur du faux sont montrés après chaque choix.
- Un duel affiché mais pas joué survit au passage par l'atelier.
- Les familles de questions tournent dans un ordre tiré au hasard pour chaque
  tour, jamais deux fois la même de suite (`ORDRE`).
- Fin de ration : compte à rebours jusqu'à minuit, cases vertes et rouges,
  écus gagnés, joueurs dupés par ses faux dans la journée, le joueur qui a le
  plus dupé, l'atelier.

## Le faux montré

Le plus efficace de la question, sauf 4 fois sur 10 un faux encore peu vu
(moins de 3 duels), pour lui laisser sa chance (`adversaire`). Efficacité :
`(victimes + 1) / (victimes + démasquages + 3)` (`taux`).

## Les écus

La monnaie de l'expert (décision de l'auteur, 23/11/2026 ; avant : le
blop, une tache d'encre). Plus bas, l'historique parle d'écus pour la clarté.

- 20 au départ (`ECUS_DEPART`, 23/11/2026 ; 10 avant) : de quoi poser un faux en direct dès la première partie, +1 par bonne réponse, +1 par victime de ses faux.
- Faux posé dans l'atelier : 10 (`PRIX_PIEGE`). Le joueur choisit la famille ;
  le jeu lui donne la question qui a le moins de faux en vie.
- Faux posé en direct, juste après un duel, sur cette question : 15
  (`PRIX_DIRECT`). Le prix est gardé avec le faux (`prix`).
- La pastille de l'écu est une pièce frappée d'un fleuron.

## Fabriquer un faux

- On ne contrefait que les pièces authentifiées, c'est-à-dire les lots où l'on a
  trouvé la vraie (24/11/2026) : on les a eues entre les mains. Le
  joueur floué ne peut pas contrefaire ce lot, ni dans l'atelier ni en direct
  (bouton −15 grisé) ; le serveur refuse aussi (403). Le 23/11/2026, l'atelier
  ne proposait déjà que des lots expertisés : avant, on pouvait faire défiler
  une famille rare (les métiers) et apprendre toutes ses réponses. Un lot neuf
  se contrefait en direct, juste après l'avoir authentifié. Familles vides
  masquées.
- Aperçu : le faux s'écrit dans l'emplacement de la réponse, sur le même
  artefact que l'original (surligné), au fil de la saisie ; l'original tient
  en une ligne au-dessus. Tant que rien n'est tapé, le texte d'origine est
  en filigrane dans le champ et grisé dans l'aperçu, à l'endroit qu'il va
  remplacer.


- Le poseur voit la vraie réponse (depuis le 23/11/2026 ; avant, il écrivait
  à l'aveugle et devinait deux fois). Il imite son ton, sa longueur, sa
  bizarrerie.
- L'arbitre refuse un faux trop proche de la vérité (`docs/arbitre.md`). Le
  refus ne dit pas pourquoi au-delà de « Trop proche de la vérité » ; le joueur
  réécrit.
- Un faux par joueur et par question. Une question où le joueur a un faux ne
  lui est plus posée ; une question neuve vue en fabriquant non plus.
- Questions proposées : les pièces authentifiées seulement.
- Définition : le faussaire choisit la catégorie de son faux (n. m., n. f.,
  adj., v.…), celle de la vraie cochée d'office ; il peut la fausser aussi
  (« sapajou, *adj.*, d'un rouge sombre »).
- Plus de mise en forme imposée (24/11/2026) : le faux s'affiche tel qu'écrit,
  majuscules et ponctuation comprises ; imiter la forme de la vraie fait partie
  du travail du faussaire (`docs/questions.md`, « Forme des réponses »).

## Classement des faussaires

Décidé le 24/11/2026. Classement de la semaine (lundi 0 h, heure de Paris,
comme les trois autres jeux) : joueurs dupés par les faux de chacun, même règle
que les écus rendus (un faux montré, pas démasqué, à un joueur qui s'est
trompé). Les faux de Truffe ne comptent pas. Sur Railway, le serveur le calcule
(`_piegeurs`, dans `/api/etat`), la page ne recevant que les duels du joueur ;
sur claude.ai, la page le calcule (`classementLocal`). Podium à l'accueil,
classement complet (20 premiers et ta place) sous « Voir tout », vainqueur de la
semaine passée sur une ligne. Classé sans pseudo : « Signe ton nom » sous le
podium.

## Défi par lien

Décidé le 25/11/2026. Dès 3 faux en vente (`DEFI_MIN`), « Sur le marché »
propose « Défier un ami » ; avant, le bouton est grisé avec la jauge (« 2/3 »).
Le lien (`?defi=CODE`, code tiré au hasard, 8 caractères) ouvre une invitation
(« Mlle Rubicon te met au défi », nombre de pièces), puis une tournée sur les lots
du faussaire que l'ami n'a pas joués, face à ses faux en vente. Duels ordinaires :
écus pour l'ami, écus et classement pour le faussaire. Bilan : faux démasqués sur
le total, « Défier à mon tour ». Le lien ne relance pas le défi une fois joué.
Serveur : table `defis` (code, auteur), `POST /api/defis` (auteur du cookie,
3 faux au moins), `/api/etat?defi=CODE` (ce défi seulement). Sur le site
seulement : sur claude.ai, l'adresse de la page n'est pas partageable.

## La vie d'un faux

- Mèche : 10 démasquages sans aucune victime (`MORT_VUS`) et le faux est
  démasqué pour de bon. Dès sa première victime, il est sauvé.
- « Plus vrai que nature » : au moins 5 duels (`PVQN_VUS`) et plus de victimes
  que de démasquages. Galerie dans l'atelier.
- Contestation « Un faux dit vrai » : 2 joueurs (`CONTEST_MIN`) et il est retiré.
- Réglages petits pour voir les effets avec quelques testeurs.

## Autour

- « Pendant ton absence » : à l'ouverture, les victimes de ses faux depuis la
  dernière visite (dernière visite dans le navigateur ; dans le vrai jeu, sur
  le serveur).
- Pseudo : un seul par joueur (décision de l'auteur, 23/11/2026). Chaque faux se
  signe au moment de la pose, signature préremplie avec le pseudo ; la changer
  change le pseudo partout. Modifiable aussi dans « Sur le marché », ligne « Signé »
  (2 à 20 caractères). Une signature libre par faux casserait le lien entre le
  joueur et ses faux, et permettrait de signer du nom d'un autre.
- Signalement discret sous chaque duel : un faux dit vrai, la vraie réponse
  est fausse, contenu choquant.

## Modèle économique (décision de l'auteur, 22/11/2026)

- Faux à 10 écus : 1 à 1,5 faux par partie.
- Une ration gratuite par jour (15 duels), les suivantes payantes. Piste : 3 rations le
  premier jour, pour que le joueur pose son premier faux avant le mur.
- Sans compte : identifiant posé par le serveur dans un cookie (Safari efface
  au bout de 7 jours ce qu'écrit un script, WebKit 2020), code de sauvegarde
  pour changer d'appareil, adresse électronique demandée au seul paiement
  (Stripe Checkout) avec un lien de retour par courriel.
- Offres à comparer : carnet de parties, passe mensuel. Prix non étudiés.
- À traiter avant la vente : conditions générales de vente, droit de
  rétractation.
- Risque : le contenu. Une partie par jour produit moins de faux.

## Le chemin

- QCM à 4 choix (une vraie, trois faux) : deviner amusait moins que piéger.
- Course à 3 vies, puis parties de 12, puis de 10 questions.
- Cartes de faux toutes les 4 questions, puis faux payés en écus au bilan.
- « Chasse aux menteurs » (éliminer les faux un par un, gains 1, 2, 3) :
  abandonnée, le joueur qui connaissait la réponse cliquait les faux à la
  chaîne pour passer.
- Duels à deux choix : plus nerveux, et plus de clic au hasard rentable.
- Écartés : vote du plus drôle, une question par jour, parties infinies.
- Direction artistique : film noir de Discoverium (version 39 du prototype),
  puis l'Atelier du faussaire (`docs/direction-artistique.md`).
- Nom : « Le Dico menteur », puis Bonimenteur (23/11/2026).

## Pistes non faites

- Faussaire en titre : le meilleur faux d'une question grave le nom de son
  auteur sur la fiche ; les autres cherchent à le détrôner.
- Riposte : la victime peut écrire un faux montré en priorité à son faussaire.
- Sceau personnel qui évolue avec le nombre de victimes.
- Première victime mieux payée (3 écus, puis 1).
- Vente d'une ration de plus (paiement, cf. modèle économique).
