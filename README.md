# Monopoly — Documentation technique (français)

Ce dépôt contient une implémentation en Python d'un jeu de Monopoly. Le code gère la logique des loyers,
la construction de maisons/hôtels, les gares, les compagnies et une couche d'accès basique à une base
de données MySQL.

Ce README fournit une vue d'ensemble technique, les commandes d'inspection rapide et les prochaines
étapes possibles.

---

## État actuel du dépôt

- Les sources sont dans `Scripts-Python/` (ex. `Scripts-Python/monopoly.py`, `Scripts-Python/db.py`).
- Les scripts de tests ont été supprimés à la demande (ils peuvent être restaurés depuis l'historique si besoin).
- La documentation détaillée a été consolidée dans ce README.

---

## Contrôle rapide (sanity check)

Pour vérifier rapidement que l'import du module principal fonctionne :

```pwsh
cd C:\Users\xavie\Documents\GitHub\Monopoly
python -c "from Scripts-Python.monopoly import Monopoly; print('Import OK')"
```

Si cette commande affiche `Import OK`, l'environnement Python peut charger le module principal.

---

## Architecture (synthèse)

- `Monopoly` : orchestrateur du jeu, gère les tours et stocke `dernier_total_des` (utile pour les compagnies).
- `Joueur` : solde, propriétés, méthodes de construction (maisons/hôtels).
- `Case` (abstraite) → `Propriete`, `Gare`, `Compagnie`, `CaseSpeciale`.
- `Propriete` : attribut `nb_maisons` (0-4 = maisons, 5 = hôtel), méthode `calculer_loyer()`.
- `Gare` : loyer selon le nombre de gares possédées.
- `Compagnie` : loyer calculé depuis la somme des dés (capturée dans `Monopoly.dernier_total_des`).

Le plateau contient 40 cases; chaque case définit une action exécutée lorsqu'un joueur y arrive.

---

## Règles principales (Option B — loyers et construction)

### Loyers (rues)

- Terrain nu sans quartier complet : `loyer_base × 1`.
- Terrain nu avec quartier complet : `loyer_base × 2`.
- 1 maison : `loyer_base × 1.3`.
- 2 maisons : `loyer_base × 1.9`.
- 3 maisons : `loyer_base × 2.6`.
- 4 maisons : `loyer_base × 3.5`.
- Hôtel : `loyer_base × 32`.

### Gares

- 1 gare : 25 €
- 2 gares : 50 €
- 3 gares : 100 €
- 4 gares : 200 €

# Monopoly — Jeu en Python
# Monopoly-Python

Implémentation pédagogique d'un jeu de Monopoly en Python. Le projet contient la logique complète du jeu
(plateau, cases, loyers, maisons/hôtels, gares, compagnies), plusieurs stratégies d'IA et une couche
d'accès optionnelle vers une base de données MySQL.

Ce README remplace et met à jour la documentation précédente — il explique comment préparer
votre environnement, (optionnellement) configurer la base MySQL et lancer le jeu sous Windows
via PowerShell.

## Contenu du dépôt (important)

- `Scripts-Python/` : code source principal (entrées, classes du jeu). Point d'entrée : `Main.py`.
- `db/monopoly_db.sql` : script SQL d'initialisation de la base `monopoly` (tables + données de base).
- `README.md` : ce fichier.

## Prérequis

- Python 3.10 ou supérieur (testé avec Python 3.13).
- (optionnel) MySQL si vous souhaitez charger les données depuis la base fournie.

Recommandation : utilisez un environnement virtuel pour isoler les dépendances :

```powershell
python -m venv .venv
# PowerShell (activer l'environnement)
.\.venv\Scripts\Activate.ps1
```

## Installer le connecteur MySQL pour Python

Le module utilisé dans le projet pour se connecter à MySQL est `mysql-connector-python` (implémentation
officielle, pure Python). Voici comment l'installer.

Avec l'interpréteur Python de votre système :

```powershell
python -m pip install mysql-connector-python
```

Si vous n'êtes pas dans un venv et que vous n'avez pas les droits administrateur, ajoutez `--user` :

```powershell
python -m pip install --user mysql-connector-python
```

Alternative (conda) :

```powershell
conda install -c anaconda mysql-connector-python
```

Remarque : le projet fourni utilise `import mysql.connector` (voir `Scripts-Python/db.py`).

## Configurer la base de données (optionnel)

Le fichier `db/monopoly_db.sql` contient la structure et les données de base. Pour l'importer avec
le client MySQL en ligne de commande (exécuté depuis la racine du dépôt) :

```powershell
# Créer la base (si nécessaire) puis importer :
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS monopoly;"
mysql -u root -p monopoly < db\monopoly_db.sql
```

Vous pouvez aussi ouvrir `db/monopoly_db.sql` dans MySQL Workbench et exécuter le script depuis l'UI.

Configuration de la connexion

La connexion est définie dans `Scripts-Python/db.py` (fonction `DB.connexionBase()`), par défaut :

```python
mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="monopoly"
)
```

Pour un usage plus sûr, remplacez cette configuration par la lecture de variables d'environnement
ou d'un fichier de configuration. Exemples de variables à définir :

- MONOPOLY_DB_HOST
- MONOPOLY_DB_USER
- MONOPOLY_DB_PASSWORD
- MONOPOLY_DB_NAME

## Lancer le projet

Depuis la racine du dépôt, avec l'environnement virtuel activé :

```powershell
python .\Scripts-Python\Main.py
```

`Main.py` propose un menu interactif : jouer une partie automatique, interactive, lancer des simulations,
comparer les stratégies d'IA, ou exécuter la batterie de tests intégrée.

Exemples utiles :

- Simuler plusieurs parties (option du menu) pour collecter des statistiques.
- Lancer `Main.py` en mode test : sélectionnez l'option 5 (exécute la suite de tests internes).

## Notes techniques rapides

- Le plateau contient 40 cases (implémenté dans `Plateau.py`).
- Les cases héritent d'une classe `Case` : `Propriete`, `Gare`, `Compagnie`, `CaseSpeciale`.
- `Monopoly.py` orchestre la partie, gère les dés, doubles, prison, constructions et statistiques.
- `Scripts-Python/db.py` fournit une couche simple pour charger les propriétés depuis la base.

## Dépannage courant

- Erreur d'import `mysql.connector` → installez `mysql-connector-python` dans le même interpréteur
  que celui avec lequel vous lancez `Main.py`.
- Problème de droits lors de l'installation → utilisez un venv ou `--user`.
- Le script SQL refuse de s'exécuter → vérifiez que MySQL est installé et accessible depuis la ligne de
  commande (commande `mysql`).

## Tests

Le projet inclut des assertions et routines de tests basiques (voir `Main.py` option 5). Pour une
suite de tests organisée, on peut ajouter `pytest` et créer un dossier `tests/` (je peux le faire si
vous le souhaitez).

## Contribuer

- Ouvrez une issue pour signaler un bug ou proposer une amélioration.
- Proposez une pull request avec une description claire et des tests lorsque c'est possible.

## Licence

Précisez ici la licence que vous souhaitez appliquer (par ex. MIT). Si vous voulez, je peux ajouter un
fichier `LICENSE` approprié.

---

Si vous voulez que je :
- génère un `requirements.txt` avec les paquets utilisés,
- modifie `Scripts-Python/db.py` pour lire les paramètres depuis des variables d'environnement,
- ou ajoute une petite documentation d'exécution pas-à-pas (Quick Start), dites-le — je m'en occupe.

---

Fin du nouveau README.
Vous pouvez créer un `requirements.txt` si vous voulez que je le génère.
