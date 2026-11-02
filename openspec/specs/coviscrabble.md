# Spécifications COVI-SCRABBLE

Ce document recense les exigences fonctionnelles et techniques validées du projet COVI-SCRABBLE.

---

### REQ-NET-001 : Architecture Client-Serveur TCP
Le système doit être architecturé autour d'un serveur centralisé (`scra_server.py`) et de clients autonomes (`scra_client.py`), communiquant via des sockets TCP en mode flux avec un délimiteur de fin de message `$$` (`EOD`) pour garantir l'intégrité des trames asynchrones.

### REQ-NET-002 : Handshake et Authentification Sécurisée
La négociation de connexion entre un client et le serveur doit s'effectuer en 3 étapes séquentielles :
1. Vérification de compatibilité de la version logicielle (`version:maj:min`).
2. Transmission de l'identifiant joueur (`mynameis:<login>`).
3. Transmission du mot de passe haché en SHA-256 (`password:<hash>`) confronté au référentiel des comptes autorisés.

### REQ-UI-001 : Plateau de Jeu et Grille Conforme
L'interface utilisateur (`scrabble.py`) doit afficher une grille officielle de 15×15 cases sur un Canvas Tkinter :
* Cases « Lettre compte double » et « Lettre compte triple » (colorées en nuances de bleu).
* Cases « Mot compte double » et « Mot compte triple » (colorées en nuances de rouge / rose).
* Étoile centrale (pentagramme) positionnée en `(7, 7)`.

### REQ-UI-002 : Chevalet et Manipulation des Tuiles
Chaque joueur dispose d'un chevalet personnel affichant jusqu'à 7 tuiles :
* Manipulation par glisser-déposer interactif (*drag-and-drop*) avec accrochage automatique sur les cases du plateau.
* Prise en charge des tuiles Jokers (lettre blanche valant 0 point) avec invite de saisie pour attribuer la lettre représentée.
* Verrouillage visuel et logique des lettres posées lors des tours précédents.

### REQ-UI-003 : Fenêtre Satellite de Scores
L'application doit maintenir une fenêtre satellite dédiée (`winscore.py`) :
* Affichage du cumul des scores pour chaque joueur connecté et du détail du dernier coup joué.
* Arrimée dynamiquement sur le bord droit de la fenêtre principale lors des déplacements de celle-ci.

### REQ-RULES-001 : Moteur de Validation Lexicale
Le système doit vérifier la validité de chaque mot soumis :
* Prise en charge des dictionnaires de référence français (`dico_fr.txt`) et anglais (`dico_en.txt`).
* Précompilation sous forme de fichiers binaires `.dic` (`pickle`) pour assurer un chargement et un test d'appartenance quasi instantané en mémoire vive.

### REQ-RULES-002 : Calculateur de Scores et Validation des Mots
Le module d'arbitrage (`calculator.py`) doit faire respecter les règles officielles du Scrabble :
* Obligation d'alignement strict (horizontal ou vertical) et de contiguïté des lettres posées.
* Obligation de connexion aux lettres déjà présentes sur le plateau (ou passage par la case centrale `(7, 7)` au premier coup).
* Prise en compte de tous les mots annexes formés perpendiculairement.
* Application rigoureuse des multiplicateurs de lettre et de mot.
* Attribution d'une prime de 50 points (Scrabble) si le joueur pose simultanément ses 7 lettres.

### REQ-GAME-001 : Gestion du Cycle de Partie et Tour par Tour
Le serveur orchestre le déroulement de la partie :
* Gestion d'un sac de lettres dont la composition et la valeur en points correspondent à la langue sélectionnée (`BAG_FR` ou `BAG_EN`).
* Alternance stricte du tour de jeu : seul le joueur actif a son bouton de validation activé et ses tuiles déverrouillées.
* Fin de partie déclarée lorsque le sac est épuisé et qu'un joueur a vidé son chevalet, avec redistribution des points résiduels des autres joueurs vers le vainqueur.
