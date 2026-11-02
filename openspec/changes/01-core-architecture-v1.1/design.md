# Conception : 01-core-architecture-v1.1

## Architecture du Système

### 1. Couche Sockets Asynchrones (`socketlib/`)
- `Abstract_serveur` encapsule la gestion de socket TCP, le handshake en 3 passes et la diffusion (broadcast ou ciblée).
- `Abstract_client` dispose d'un thread d'écoute réseau remplissant une `queue.Queue` non bloquante.
- Découpage par délimiteur `$$` (`EOD`) pour s'affranchir du découpage arbitraire de paquets TCP.

### 2. Spécialisation Métier
- `Serveur` (`scra_server.py`) gère le modèle du sac de tuiles, le tirage aléatoire, le tour de rôle et la fin de partie.
- `Client` (`scra_client.py`) convertit les actions utilisateur en requêtes texte (`put`, `get`, `valider`, `redonner`, `restart`).

### 3. IHM Tkinter
- `Scrabble` (`scrabble.py`) gère l'affichage du plateau (15×15 cases), la case centrale avec pentagramme vectoriel (`polygon.py`), et les zones de chevalet.
- `Letter` (`letter.py`) implémente la physique du glisser-déposer sur le Canvas avec accrochage et conversion ligne/colonne.
- `Winscore` (`winscore.py`) maintient la fenêtre de scores liée à la fenêtre principale par l'événement `<Configure>`.

### 4. Dictionnaire & Calculs
- `Dictionary` (`dico/dictionary.py`) stocke les lemmes sous structure optimisée et sérialise en `.dic`.
- `calculer_score` (`calculator.py`) effectue l'arbitrage géométrique et lexical complet.
