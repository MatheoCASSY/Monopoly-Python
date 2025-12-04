"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""
from typing import List, Optional

class Carte :
    """Représente une carte Caisse de Communauté ou Chance"""
    def __init__(self, description: str, action):
        self.description = description
        self.action = action  # Fonction à exécuter

    def executer(self, joueur: 'Joueur', jeu: 'Monopoly'):
        """Exécute l'action de la carte"""
        print(f"{self.description}")
        self.action(joueur, jeu)
