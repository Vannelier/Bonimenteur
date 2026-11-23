# Conception

Règles du prototype (`prototype/index.html`) et chemin qui y a mené. Le code
fait foi ; les réglages sont en tête de son script.

## Le jeu en une phrase

Le joueur démasque les faux des autres (une vraie réponse contre un faux, à
chaque duel) et fabrique les siens pour les duper. Fabriquer est le plaisir ;
démasquer rapporte de quoi fabriquer.

## La ration du jour

- 15 duels par jour, heure de Paris (`TOTAL`, `RATION` côté serveur ; décision
  de l'auteur, 23/11/2026). Il n'y a plus de partie avec un score à battre : on
  joue pour remplir son encrier, la ration donne le rythme, et c'est elle qui
  se vendra (une ration de plus).
- La ration se compte sur les duels enregistrés : recharger la page ou changer
  d'appareil ne la remet pas à zéro. Le serveur refuse le 16e duel du jour.
- Chaque duel montre une question, sa vraie réponse et un faux écrit par un
  autre joueur, dans un ordre tiré au hasard.
- Bonne réponse : +1 blop. Mauvaise : le joueur est la victime du faux, et
  l'auteur du faux gagne 1 blop.
- La vraie réponse et l'auteur du faux sont montrés après chaque choix.
- Un duel affiché mais pas joué survit au passage par l'atelier.
- Les familles de questions tournent dans un ordre tiré au hasard pour chaque
  tour, jamais deux fois la même de suite (`ORDRE`).
- Fin de ration : compte à rebours jusqu'à minuit, cases vertes et rouges,
  blops gagnés, joueurs dupés par ses faux dans la journée, le joueur qui a le
  plus dupé, l'atelier.

## Le faux montré

Le plus efficace de la question, sauf 4 fois sur 10 un faux encore peu vu
(moins de 3 duels), pour lui laisser sa chance (`adversaire`). Efficacité :
`(victimes + 1) / (victimes + démasquages + 3)` (`taux`).

## Les blops

- 20 au départ (`BLOP_DEPART`, 23/11/2026 ; 10 avant) : de quoi poser un faux en direct dès la première partie, +1 par bonne réponse, +1 par victime de ses faux.
- Faux posé dans l'atelier : 10 (`PRIX_PIEGE`). Le joueur choisit la famille ;
  le jeu lui donne la question qui a le moins de faux en vie.
- Faux posé en direct, juste après un duel, sur cette question : 15
  (`PRIX_DIRECT`). Le prix est gardé avec le faux (`prix`).
- La pastille du blop est une tache d'encre.

## Fabriquer un faux

- Le poseur voit la vraie réponse (depuis le 23/11/2026 ; avant, il écrivait
  à l'aveugle et devinait deux fois). Il imite son ton, sa longueur, sa
  bizarrerie.
- L'arbitre refuse un faux trop proche de la vérité (`docs/arbitre.md`). Le
  refus ne dit pas pourquoi au-delà de « Trop proche de la vérité » ; le joueur
  réécrit.
- Un faux par joueur et par question. Une question où le joueur a un faux ne
  lui est plus posée ; une question neuve vue en fabriquant non plus.
- Questions proposées : d'abord celles que le joueur a déjà jouées (rien n'est
  gâché), puis les neuves.
- Mise en forme imposée (`formater`) : majuscule, point final ; pour une
  commune, majuscule à chaque partie du nom. Un faux ne se trahit pas par sa
  forme.

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
- Pseudo : onglet « Mes faux », ligne « Signé » (2 à 20 caractères ; à défaut,
  le nom du compte claude.ai).
- Signalement discret sous chaque duel : un faux dit vrai, la vraie réponse
  est fausse, contenu choquant.

## Modèle économique (décision de l'auteur, 22/11/2026)

- Faux à 10 blops : 1 à 1,5 faux par partie.
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
- Cartes de faux toutes les 4 questions, puis faux payés en blops au bilan.
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
- Première victime mieux payée (3 blops, puis 1).
- Vente d'une ration de plus (paiement, cf. modèle économique).
