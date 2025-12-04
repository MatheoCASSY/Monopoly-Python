"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""
from typing import List, Optional

from Joueur import Joueur
from Propriete import Propriete
from StrategieIA import StrategieIA

class IAConservative(StrategieIA):
    """Stratégie conservative: n'achète que si garde une réserve"""
    
    def __init__(self):
        super().__init__("Conservative")
    
    def decider_achat(self, joueur: 'Joueur', propriete: Propriete) -> bool:
        """Achète seulement si argent > 2x le prix"""
        return joueur.argent >= propriete.prix * 2
    
    def decider_construction(self, joueur: 'Joueur') -> Optional[Propriete]:
        return True