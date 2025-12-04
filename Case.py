"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""

# =============================================================================
# SÉANCE 1 : FONDATIONS (3h)
# =============================================================================

class Case:
    """Classe de base pour toutes les cases du plateau"""
    def __init__(self, nom: str, position: int):
        self.nom = nom
        self.position = position
    
    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        """Action exécutée quand un joueur arrive sur la case"""
        pass

    def __str__(self):
        return self.nom
