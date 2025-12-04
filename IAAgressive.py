"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""
from typing import List, Optional

from Joueur import Joueur
from Propriete import Propriete
from StrategieIA import StrategieIA


class IAAgressive(StrategieIA):
    """Stratégie agressive: achète systématiquement toutes les propriétés"""
    
    def __init__(self):
        super().__init__("Agressive")
    
    def decider_achat(self, joueur: 'Joueur', propriete: Propriete) -> bool:
        return True

    def decider_construction(self, joueur: 'Joueur') -> Optional[Propriete]:
        return True

if __name__ == "__main__":
    ia = IAAgressive()
    print("OK")