# Audit du 23/11/2026

Relecture du serveur, de la page, des données, des docs et du déploiement.
Corrigé le jour même : marqué « fait ». Le reste attend une décision. Décidé par l'auteur ensuite : la triche par
lecture du réseau est acceptée pour l'instant ; le déploiement attendra.

## Sécurité et triche

| Point | Gravité | État |
|---|---|---|
| La page reçoit les vraies réponses de toutes les questions (`/api/etat`, champ `vraie`) et déclare elle-même si le joueur s'est trompé (`erreur`). Un joueur qui lit le réseau gagne tous ses duels. | haute | ouvert : voir « Le duel côté serveur » |
| Deux cookies suffisaient à retirer n'importe quel faux (2 contestations, sans contrôle). | haute | fait : contestation seulement d'un faux de ce lot, eu en duel, pas le sien |
| Chaque cookie neuf reçoit 20 écus : effacer ses cookies donnait des écus sans limite. | moyenne | fait : 20 identités neuves par heure et par IP (`LIMITES`) |
| Aucune limite de débit sur les écritures. | moyenne | fait : 60 écritures par minute et par IP |
| Pseudo : n'importe qui pouvait signer « Truffe » ou le pseudo d'un autre. | moyenne | fait : « Truffe » et quelques noms réservés, pseudos uniques (aux accents et à la casse près) |
| Pseudos et faux sans filtre de grossièretés. | moyenne | fait : `app/pseudos.py`, copie de Vocabulium (pseudo offensant → « Joueur », faux offensant refusé) |
| Signalements : question et raison non contrôlées. | faible | fait |
| L'arbitre du sens ne tourne que dans la page : un faux identique à l'original passait par l'API. | moyenne | fait pour la copie exacte (aux accents près) ; l'arbitre complet reste dans la page |
| Pas de modération des faux (retrait à la main). | moyenne | ouvert : `/api/moderation` sur le modèle de Snouff |

## Fiabilité

- Connexion SQLite partagée entre les fils sans verrou pour les lectures et
  certaines écritures : fait, tout accès passe par `_verrou`.
- `/api/etat` renvoyait tous les duels de tous les joueurs toutes les 20 s,
  et `_solde` relisait tous les duels perdus. Fait : table `stats` (vu, pris,
  démasqué par faux) tenue à chaque duel, l'état ne contient plus que les
  duels du joueur et ceux où l'un de ses faux a trompé. Reste sur claude.ai :
  la page y lit au plus 1 000 duels (`limit(1000)`).
- Pas de sauvegarde du volume Railway. Ouvert.

## Performance

- `proches.json` (2,7 Mo) et `communes.txt` (0,4 Mo) partaient sans
  compression : fait, `GZipMiddleware` (0,6 Mo et 0,14 Mo).
- Révélation : rastérisation 33 ms par révélation au processeur ralenti ×4,
  autant que sans animation (`docs/direction-artistique.md`).

## Code

- Code mort retiré de la page : `pct`, `prochainGain`, `SERIE_MAX`,
  `minusculeDebut`, `enonce`, `enonceBrut`. Restent volontairement : la lampe
  à ultraviolets (`LAMPE_UV = false`), la ration (`RATION_ACTIVE = false`),
  l'ancien format de choix (QCM) lu par `index()`.
- La page fait 150 ko en un seul fichier (CSS et script inclus). À découper
  le jour où elle devient le vrai jeu (fichiers versionnés, comme les trois
  autres jeux).
- Les tests de la page (Playwright) vivent hors du dépôt. Ouvert : les y
  ramener et les lancer en CI.

## Contenu

- 142 questions : 64 définitions, 16 anecdotes, 14 métiers, 12 communes,
  11 mots étrangers, 10 photos, 9 expressions étrangères, 6 expressions.
- 15 définitions n'avaient aucun faux de départ : fait, 45 faux écrits.
- 53 questions sur 142 sans `source`.
- Familles minces : 6 expressions, 9 expressions étrangères. Un joueur assidu
  les épuise vite.

## Déploiement

- Le service Railway suit la branche de la PR #1 ; `main` ne contient qu'un
  README. Fusionner la PR puis rebrancher le service sur `main`.
- Domaine bonimenteur.fr à réserver et à rattacher.
- Le prototype claude.ai et la version Railway sont publiés à la main, chacun
  de son côté : un oubli les désynchronise.

## Le duel côté serveur

La correction de fond du premier point : le serveur tire le lot, mélange les
deux réponses et ne les envoie qu'en texte, sans dire laquelle est vraie ; il
juge le choix et renvoie le verdict. La page ne reçoit plus `vraie` pour les
questions non jouées ; l'arbitre du sens passe côté serveur (il ne lit que
`proches.json`, transportable tel quel en Python). Gros chantier : la page
s'appuie partout sur `S.mots` et la vraie réponse.
