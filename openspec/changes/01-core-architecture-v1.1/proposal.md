# Changement : 01-core-architecture-v1.1 - Socle Initial COVI-SCRABBLE

## Proposition
Stabilisation, refactorisation et alignement du socle initial de COVI-SCRABBLE (version 1.1 r1) avec architecture Client/Serveur séparée, authentification sécurisée SHA-256 et moteur de calcul de score Scrabble.

## Objectifs
- Valider la communication TCP multithreadée avec protocole asynchrone délimité par `$$`.
- Intégrer l'authentification avec empreinte SHA-256 dans `database.py`.
- Assurer le rendu graphique vectoriel du plateau et des tuiles sous Tkinter.
- Fournir un moteur de validation lexicale bilingue (FR / EN).
- Garantir le respect des règles officielles de Scrabble (connexion, alignement, bonus, Scrabble de 50 points).
