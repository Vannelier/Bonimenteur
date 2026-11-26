# L'arbitre

Il refuse un faux qui dit la même chose que la vraie réponse. Sans appel à un
modèle de langue (coût) : vecteurs de mots et contrôle de forme.

## Trois contrôles

1. **Forme** (`tropProche`) : mots tronqués à 5 lettres, texte entre
   parenthèses ignoré. Refus si au moins deux mots en commun avec la vérité,
   ou si toute la vérité est reprise. Mots de cadrage ignorés des deux côtés
   (collectionneur, peur, attirance…).
2. **Sens** (`memeSens`) : vecteurs ConceptNet Numberbatch FR de Vocabulium
   (et ses mots rares). `prototype/proches/` (index et 32 paquets, chargés à la demande depuis le 26/11/2026) donne, pour chaque question,
   les mots proches à 0,45 ou plus : proximité à la vérité, proximité au mot
   de la question. Score d'un faux = max(moyenne des proximités de ses mots,
   la plus forte proximité au mot de la question). Un mot hors liste vaut
   0,25. Calcul : `tools/proches.py`.
3. **Communes** : un faux qui est une vraie commune est refusé
   (`prototype/communes.txt`, geo.api.gouv.fr, 34 969 communes).

## Seuils

| Famille | Seuil | Mesure |
|---|---|---|
| Définition | 0,5 | 25 reformulations de vraies définitions et 75 faux de Mr Halifax : 22 reformulations refusées, 1 faux honnête refusé à tort |
| Anecdote, expression, photo | 0,65 | les faux restent dans le domaine de la vérité : 6 faux de Mr Halifax sur 42 dépassaient 0,5 |
| Mot étranger, expression étrangère | 0,55 | faux de Mr Halifax à 0,46 au plus, reformulations de 0,62 à 0,82 |

Sans les mots de cadrage, 19 faux honnêtes de phobies et de collections sur
48 étaient refusés.

## Limites

- Les 200 mots les plus fréquents sont ignorés. Une vérité faite de mots
  courants laisse l'arbitre presque aveugle : « eschatologie » n'est jugée que
  sur « doctrine », « jugement », « sort » ; « Ce qui arrive après la mort »
  passe. Écrire les vérités avec des mots porteurs de sens.
- Le refus est muet sur la raison : le joueur ne peut pas sonder la vérité
  par essais (une question tentée ne lui est plus posée).
- Filet : la contestation « Un faux dit vrai » (2 joueurs, retrait).
