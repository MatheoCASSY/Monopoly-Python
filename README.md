# Monopoly — Documentation technique (français)

Ce dépôt contient une implémentation en Python d'un jeu de Monopoly. Le code gère la logique des loyers,
la construction de maisons/hôtels, les gares, les compagnies et une couche d'accès basique à une base
de données MySQL.

Ce README fournit une vue d'ensemble technique, les commandes d'inspection rapide et les prochaines
étapes possibles.

---

## État actuel du dépôt

- Les sources sont dans `src/` (ex. `src/monopoly.py`, `src/db.py`).
- Les scripts de tests ont été supprimés à la demande (ils peuvent être restaurés depuis l'historique si besoin).
- La documentation détaillée a été consolidée dans ce README.

---

## Contrôle rapide (sanity check)

Pour vérifier rapidement que l'import du module principal fonctionne :

```pwsh
cd C:\Users\xavie\Documents\GitHub\Monopoly
python -c "from src.monopoly import Monopoly; print('Import OK')"
```

Si cette commande affiche `Import OK`, l'environnement Python peut charger le module principal.

---

## Architecture (synthèse)

- `Monopoly` : orchestrateur du jeu, gère les tours et stocke `dernier_total_des` (utile pour les compagnies).
- `Joueur` : solde, propriétés, méthodes de construction (maisons/hôtels).
- `Case` (abstraite) → `Propriete`, `Gare`, `Compagnie`, `CaseSpeciale`.
- `Propriete` : attributs `nb_maisons`, `a_hotel`, méthode `calculer_loyer()`.
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

### Compagnies

- 1 compagnie : `4 × (somme des dés)`
- 2 compagnies : `10 × (somme des dés)`

Remarque : `Monopoly.dernier_total_des` doit être mis à jour après chaque lancer.

---

## API de construction (résumé)

- `Joueur.possede_quartier_complet(couleur) -> bool` : vérifie possession complète d'un quartier.
- `Joueur.peut_construire_maison(propriete) -> bool` : vérifie propriétaire, pas d'hôtel, <4 maisons, quartier complet, argent.
- `Joueur.construire_maison(propriete)` : coût = `propriete.prix // 2` ; incrémente `nb_maisons`.
- `Joueur.construire_hotel(propriete)` : nécessite 4 maisons ; coût = `5 × prix_maison` ; met `a_hotel = True` et `nb_maisons = 0`.

---

## Base de données (résumé)

Le module `src/db.py` fournit une intégration MySQL minimale et la vue `v_proprietes` attendue par
le code :

- `proprietes`(id, nom, position, prix, loyer, couleur, type)
- `joueurs`(id, nom, argent, position)
- `joueurs_proprietes`(joueur_id, propriete_id, nb_maisons, a_hotel)

Adapter la configuration MySQL dans `src/db.py` si vous voulez connecter une base réelle.

---

## Organisation recommandée

```
Monopoly/
├─ src/        # Code source
├─ analysis/   # Extractions PDF et rapports
├─ docs/       # (vide après consolidation) — garder pour notes éventuelles
└─ README.md   # Cette documentation technique
```

---

## Dépendances suggérées

Si vous souhaitez exécuter des outils ou restaurer des fonctionnalités (extraction PDF, DB), installez :

```text
python (3.8+ recommandé)
mysql-connector-python
PyPDF2    # optionnel, pour l'extraction PDF
```

Vous pouvez créer un `requirements.txt` si vous voulez que je le génère.

---

## Restaurer ou recréer les tests

Les tests ont été supprimés volontairement. Pour les restaurer :

- option A : je peux restaurer les fichiers `tests/` depuis l'historique Git (si la branche contient l'historique) ;
- option B : je peux recréer une suite minimale d'unit tests pour valider `calculer_loyer()` et les méthodes de construction.

Dites-moi quelle option vous préférez.

---

## Prochaines actions possibles (choisissez)

1. Je restaure/regenère la suite de tests (rapide) ;
2. Je crée `requirements.txt` et vérifie les imports ;
3. Je déplace/valide les modules sous `src/` et corrige les imports si nécessaire ;
4. Rien — je laisse le dépôt tel quel.

Répondez par le numéro de l'action souhaitée ou décrivez une autre action.

---

Fin de la documentation.
# 🎮 Monopoly Game - Implémentation Complète

Implémentation Python d'un jeu de Monopoly avec base de données MySQL, incluant la logique complète de loyers avec maisons/hôtels et règles de construction pour quartiers.

---

## ⚡ Démarrage Rapide (30 secondes)

1. **[QUICK_START.md](QUICK_START.md)** ← **LIRE EN PREMIER!**
2. **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Comprendre l'organisation
3. Consulter les sections ci-dessous selon vos besoins

---

## 📊 Status Projet

```
✅ Code:           2 fichiers (monopoly.py, db.py)
✅ Tests:          21/21 assertions réussites
✅ Documentation:  15+ fichiers markdown
✅ Conformité:     7/7 consignes réalisées
```

---

## 📁 Structure Organisée

La documentation a été réorganisée pour une meilleure lisibilité:

- **`src/`** - Code source principal
- **`tests/`** - Tests et validation
- **`docs/`** - Documentation complète (option_b/, guides/, compliance/)
- **`analysis/`** - Analyses et rapports

**Pour l'arborescence complète:** [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

## 🎯 Navigation par Besoin

### Je suis un **Utilisateur**
1. Lire [QUICK_START.md](QUICK_START.md)
2. Consulter [docs/option_b/README.md](docs/option_b/README.md)
3. Exécuter `python tests/test_option_b.py`

### Je suis un **Développeur**
1. Lire [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
2. Consulter [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
3. Lire [docs/option_b/VALIDATION.md](docs/option_b/VALIDATION.md)
4. Étudier `src/monopoly.py`

### Je suis un **Mainteneur**
1. Lire [docs/compliance/MANIFEST.md](docs/compliance/MANIFEST.md)
2. Lire [docs/compliance/DELIVERABLES.md](docs/compliance/DELIVERABLES.md)
3. Consulter [docs/compliance/INDEX.md](docs/compliance/INDEX.md)
4. Maintenir les tests à jour

---

## 📚 Documentation Complète

Tous les fichiers de documentation sont organisés dans `docs/`:

- **`docs/option_b/`** - Option B: Loyers & Construction
- **`docs/guides/`** - Guides pratiques (Getting Started, Rules, Database)
- **`docs/compliance/`** - Conformité & spécifications (Manifest, Deliverables, Conclusion)

**Accès rapide:** [INDEX.md](INDEX.md) ou [docs/](docs/README.md)

---

## 🧪 Tests

Exécuter les tests:

```bash
# Tests Option B (21 assertions - RECOMMANDÉ)
python tests/test_option_b.py

# Tests des cases spéciales
python tests/test_cases.py

# Tests prison (interactif)
python tests/test_prison_situation.py
```

---

## 🎯 Fonctionnalités Principales

### Option B: Loyers & Construction (✅ Complète)

- ✅ Calcul loyers avec maisons/hôtels
- ✅ Tiers progressifs pour gares
- ✅ Loyers basés sur dés pour compagnies
- ✅ Règles de construction complets (quartier complet requis)
- ✅ Validation complète des préconditions

**Documentation:** [docs/option_b/README.md](docs/option_b/README.md)

### Autres Fonctionnalités

- ✅ Gestion prison (3 méthodes de sortie)
- ✅ Doubler les dés et tours supplémentaires
- ✅ Cases spéciales (Départ, Taxe, Chance, etc.)
- ✅ Système d'argent et faillite
- ✅ Base de données MySQL intégrée

---

## 📌 Fichiers Clés à Consulter

| Besoin | Fichier |
|--------|---------|
| Démarrer (30 sec) | [QUICK_START.md](QUICK_START.md) |
| Arborescence | [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) |
| Comprendre Option B | [docs/option_b/README.md](docs/option_b/README.md) |
| Valider Option B | [docs/option_b/VALIDATION.md](docs/option_b/VALIDATION.md) |
| Vue d'ensemble | [docs/OVERVIEW.md](docs/OVERVIEW.md) |
| Architecture | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Conformité | [docs/compliance/MANIFEST.md](docs/compliance/MANIFEST.md) |
| Index complet | [INDEX.md](INDEX.md) |

---

## 💻 Code Source

- **`src/monopoly.py`** (~700 lignes)
  - Classes: Monopoly, Joueur, Propriete, Gare, Compagnie
  - Logique de jeu complète
  - Implémentation Option B (loyers & construction)

- **`src/db.py`** (~650 lignes)
  - Connexion MySQL
  - Requêtes et gestion données

---

## ✅ Conformité avec Spécifications

Toutes les consignes du TP Monopoly sont réalisées:

```
Consigne 2.2.1: possede_quartier_complet()      ✅ Réalisé
Consigne 2.2.2: calculer_loyer() - base         ✅ Réalisé
Consigne 2.2.3: calculer_loyer() - maisons      ✅ Réalisé
Consigne 2.2.4: calculer_loyer() - hôtel        ✅ Réalisé
Consigne 2.3.1: Gare.calculer_loyer()           ✅ Réalisé
Consigne 2.3.2: Compagnie.calculer_loyer()      ✅ Réalisé
Consigne 2.2.5: Règles construction             ✅ Réalisé
```

**Détails:** [docs/compliance/MANIFEST.md](docs/compliance/MANIFEST.md)

---

## 🚀 Prochaines Étapes (Optionnelles)

- [ ] Option C: Implémentation des stratégies IA
- [ ] Population complète cartes Chance/Communauté
- [ ] Refactoring des inputs interactifs pour tests automatisés

---

## 💡 Comment Utiliser

### Installation
```bash
# Cloner le repo
git clone <repo>
cd Monopoly

# Vérifier structure
ls -la
```

### Exécuter Tests
```bash
python tests/test_option_b.py
```

### Consulter Documentation
```bash
# Démarrage rapide
cat QUICK_START.md

# Arborescence
cat PROJECT_STRUCTURE.md

# Documentation complète
open docs/
```

---

## 📖 Pour Plus d'Informations

- **Organisation:** [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **Démarrage:** [QUICK_START.md](QUICK_START.md)
- **Documentation:** [docs/](docs/README.md)
- **Navigation:** [INDEX.md](INDEX.md)

---

**Status:** ✅ Production Ready | **Mise à jour:** Décembre 2024 | **Tests:** 21/21 ✅
