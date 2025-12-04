"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""
from typing import List, Optional

from Joueur import Joueur
from Propriete import Propriete
from StrategieIA import StrategieIA

class IAStrategique(StrategieIA):
    """Stratégie stratégique: privilégie les quartiers"""
    
    def __init__(self):
        super().__init__("Stratégique")
    
    def decider_achat(self, joueur: 'Joueur', propriete: Propriete) -> bool:
        """Privilégie les propriétés qui complètent un quartier"""
        # Ne pas dépenser si trop peu d'argent
        if joueur.argent < propriete.prix * 1.5:
            return False
        
        # Compter combien de propriétés de cette couleur sont déjà possédées
        nb_possede = sum(1 for p in joueur.proprietes 
                        if hasattr(p, 'couleur') and p.couleur == propriete.couleur)
        
        # Haute priorité si ça rapproche d'un quartier
        if nb_possede >= 1:
            return True
        
        # Sinon acheter si beaucoup d'argent
        return joueur.argent >= propriete.prix * 3

    def decider_construction(self, joueur: 'Joueur') -> Optional[Propriete]:
        return True