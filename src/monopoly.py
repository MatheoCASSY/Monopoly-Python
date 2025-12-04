"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""

import random
from enum import Enum
from typing import List, Optional

# =============================================================================
# SÉANCE 1 : FONDATIONS (3h)
# =============================================================================

class Case:
    """Classe de base pour toutes les cases du plateau"""
    def __init__(self, nom: str, position: int):
        self.nom = nom
        self.position = position
    
    """Wrapper léger pour lancer le jeu depuis `src/monopoly.py`.

    Ce fichier importe la nouvelle architecture modulaire placée dans `src/monopoly_pkg`
    et fournit un point d'entrée simple pour compatibilité.
    """

    try:
        # import depuis le package modulaire
        from src.monopoly_pkg.game import Monopoly
    except Exception:
        # fallback si exécuté d'un autre contexte
        from monopoly_pkg.game import Monopoly


    if __name__ == "__main__":
        noms = ["Alain", "Béa", "Charles"]
        jeu = Monopoly(noms)
        # Par défaut on n'exécute pas la partie interactive complète
        # Décommentez pour jouer :
        # jeu.jouer_partie(max_tours=100)
        print("Squelette de code chargé. Prêt pour le développement !")